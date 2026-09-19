#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_dock.py -- P6-C2：AutoDock Vina 全库对接（配体级并行）

【为什么不用 --batch】
本机 `tools/vina.exe`（AutoDock Vina 1.2.5）的 `--batch` 与官方文档语义不符：
它把 batch 参数指向的文件**本身**当作一个 PDBQT 解析（报
"Failed parsing <列表文件>.txt. Skipping it."），而不是当作"配体路径列表"。
已系统测试 6 种组合：路径列表（正/反斜杠、绝对/相对）、纯内容拼接、
MODEL/ENDMDL 包裹 —— 全部失败，其中 MODEL 变体明确回话
"Unexpected multi-MODEL tag found in flex residue or ligand PDBQT file.
 Use vina_split to split flex residues or ligands in multiple PDBQT files"，
即该参数期望的文件只能含单个配体。故改用**单文件模式 `--ligand`**。

【并行设计】
Vina 对**单个配体**的多线程加速很差，并行的正确轴是"配体"：
每进程 `--cpu 1`，用 W 个进程各跑一批配体。

【耗时与参数】
实测（本机 8 核、盒约 24×29×21 Å）单配体默认设置（exh=4）约 8-49 s，
与可旋转键数强相关；19 靶标 × 3,085 配体将需数十小时。虚拟筛选只需
**相对排序**可靠，故 stage1 压低 MC 预算（见 STAGE 表），stage2 再精算 top。
`--seed 42` 固定 → 同参数下结果可复现；实际使用的参数写进结果表。

产出：docking/out/<SYM>/chunk*.csv（断点续跑单元）、scores_stage<N>.csv、
      results/tables/P6_docking_scores_stage<N>.csv
用法：python p6_dock.py --stage 1 [--only SYM1,SYM2] [--workers 7] [--lig-limit N]
"""
import os, re, sys, json, glob, time, argparse, subprocess, concurrent.futures as cf
import numpy as np, pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
REC = os.path.join(ROOT, "docking/receptors")
LIG = os.path.join(ROOT, "docking/ligands")
OUT = os.path.join(ROOT, "docking/out")
VINA = os.path.join(ROOT, "tools/vina.exe")

# stage1 粗筛全库（快、够排序）；stage2 精算 top（慢、够精度）
# max_evals: 0 = 用 Vina 启发式（很慢）；显式给值才能把单配体压到秒级。
STAGE = {1: dict(exh=2, modes=3, max_evals=1500),
         2: dict(exh=8, modes=9, max_evals=0)}

# 打分表行：mode、affinity、rmsd_lb、rmsd_ub
# 【踩过的坑】mode 1 行的两个 rmsd 是整数 `0`（无小数点），旧正则要求 `\d+\.\d+`
# 会漏掉 mode 1 —— 而下游只取 mode 1，等于结果全空。故必须用 `-?\d+(?:\.\d+)?`。
LINE_MODE = re.compile(r"^\s*(\d+)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s+(-?\d+(?:\.\d+)?)\s*$")


def parse_vina(text):
    """单文件模式 stdout -> [(mode, affinity, rmsd_lb, rmsd_ub), ...]"""
    out = []
    for line in text.splitlines():
        if "|" in line:            # 表头 mode | affinity | dist from best mode
            continue
        m = LINE_MODE.match(line)
        if m:
            out.append((int(m.group(1)), float(m.group(2)),
                        float(m.group(3)), float(m.group(4))))
    return out


def dock_one(lig_path, box6, cfg):
    """跑单个配体。注意 subprocess **不能用 text=True** ——
    Vina 的 stdout 含非 UTF-8 字节，text=True 会让 .stdout 变成 None，
    随后解析静默得到 0 行结果（踩过）。一律取 bytes 再手动 decode。
    """
    cid = os.path.basename(lig_path)[:-6]
    odir = cfg["outdir"]
    pose = (os.path.join(odir, "poses", f"{cid}.pdbqt") if cfg["keep_pose"]
            else os.path.join(odir, "_scratch", f"w{cfg['wid']}.pdbqt"))
    cmd = [VINA, "--receptor", cfg["receptor"], "--ligand", lig_path.replace("\\", "/"),
           "--out", pose.replace("\\", "/"),
           "--center_x", f"{box6[0]:.3f}", "--center_y", f"{box6[1]:.3f}",
           "--center_z", f"{box6[2]:.3f}",
           "--size_x", f"{box6[3]:.2f}", "--size_y", f"{box6[4]:.2f}", "--size_z", f"{box6[5]:.2f}",
           "--scoring", "vina", "--cpu", "1", "--seed", "42",
           "--exhaustiveness", str(cfg["exh"]), "--num_modes", str(cfg["modes"]),
           "--verbosity", "1"]
    if cfg.get("max_evals"):
        cmd += ["--max_evals", str(cfg["max_evals"])]
    t0 = time.time()
    p = None
    last_err = None
    # 【修复】Windows 下从 ProcessPoolExecutor 工作进程 spawn vina 会间歇性抛
    # PermissionError [WinError 5]（CreateProcess 被拒）。主进程 spawn 经实测稳定，
    # 故上层已改 ThreadPoolExecutor；此处再加 4 次 spawn 重试 + 退避，吸收偶发失败，
    # 不再让单点 spawn 失败炸掉整条池。
    for _att in range(4):
        try:
            p = subprocess.run(cmd, capture_output=True, timeout=cfg["timeout"])
            last_err = None
            break
        except subprocess.TimeoutExpired:
            return {"chembl_id": cid, "affinity": np.nan, "n_modes": 0,
                    "sec": round(time.time() - t0, 2), "rc": -9, "err": "TIMEOUT"}
        except Exception as e:
            last_err = repr(e)
            time.sleep(1.5)
    if p is None:
        return {"chembl_id": cid, "affinity": np.nan, "n_modes": 0,
                "sec": round(time.time() - t0, 2), "rc": -5,
                "err": f"SPAWN_FAIL:{last_err}"[:110]}
    so = (p.stdout or b"").decode("utf-8", "replace")
    se = (p.stderr or b"").decode("utf-8", "replace")
    modes = parse_vina(so)
    if not modes:
        return {"chembl_id": cid, "affinity": np.nan, "n_modes": 0,
                "sec": round(time.time() - t0, 2), "rc": p.returncode,
                "err": (se.strip()[:120] or "no_score_line")}
    best = min(modes, key=lambda t: t[1])
    return {"chembl_id": cid, "affinity": best[1], "n_modes": len(modes),
            "rmsd_lb": best[2], "rmsd_ub": best[3],
            "sec": round(time.time() - t0, 2), "rc": p.returncode, "err": ""}


def chunk_path(odir, tag, ci):
    """chunk 缓存路径。**必须带 tag** —— 否则不同筛选层（不同参数）会互相复用
    缓存，导致 Tier2 直接继承 Tier1 的结果而参数完全不同。"""
    return os.path.join(odir, f"chunk_{tag}_{ci}.csv")


def run_chunk(job):
    """worker：跑一个配体分块，结果写 chunk_<tag>_<N>.csv（断点续跑的单元）"""
    sym, ci, ligs, box6, cfg = job
    cpath = chunk_path(cfg["outdir"], cfg["tag"], ci)
    if os.path.exists(cpath) and not cfg.get("force"):
        try:
            return pd.read_csv(cpath).to_dict("records")
        except Exception:
            pass
    os.makedirs(os.path.join(cfg["outdir"], "poses"), exist_ok=True)
    os.makedirs(os.path.join(cfg["outdir"], "_scratch"), exist_ok=True)
    rows = [dock_one(l, box6, cfg) for l in ligs]
    try:
        pd.DataFrame(rows).to_csv(cpath, index=False)
    except Exception:
        pass
    return rows


def load_box(sym):
    j = json.load(open(os.path.join(REC, sym, "box.json"), encoding="utf-8"))
    return list(j["box_center"]) + list(j["box_size"])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=1, choices=[1, 2])
    ap.add_argument("--only", default=None, help="逗号分隔的靶标符号")
    ap.add_argument("--workers", type=int, default=7)
    ap.add_argument("--lig-limit", type=int, default=None)
    ap.add_argument("--liglist", default=None, help="只跑该文件列出的 chembl_id（stage2 用）")
    ap.add_argument("--timeout", type=int, default=600, help="单配体超时（秒）")
    ap.add_argument("--chunk", type=int, default=30, help="每个 chunk 的配体数（小 chunk 利于负载均衡）")
    ap.add_argument("--keep-pose", action="store_true", help="保留每个配体的 pose 文件")
    ap.add_argument("--force", action="store_true", help="忽略已有 chunk 缓存")
    # 分层筛选需要按层覆盖参数：CNS 先验层用"无 max_evals 限制"的精算设置，
    # 其余层用快筛（其排序已知不可靠，仅作探索，见 P6_stage1_param_validation）。
    ap.add_argument("--exh", type=int, default=None, help="覆盖 STAGE 的 exhaustiveness")
    ap.add_argument("--max-evals", type=int, default=None,
                    help="覆盖 max_evals；0=用 Vina 启发式（无偏倚但慢）")
    ap.add_argument("--tag", default=None, help="结果文件标签，默认 stage<N>")
    a = ap.parse_args()

    T = pd.read_csv(os.path.join(TAB, "P6_target_selection.csv"))
    rows_R = pd.read_csv(os.path.join(TAB, "P6_receptors.csv"))
    ok_syms = set(rows_R[rows_R.status == "OK"].symbol.str.upper()) if "status" in rows_R.columns else set()
    D = T[T.decision == "DOCK"].copy()
    D = D[D.symbol.str.upper().isin(ok_syms)]
    if a.only:
        want = {s.strip().upper() for s in a.only.split(",")}
        D = D[D.symbol.str.upper().isin(want)]

    ligs = sorted(glob.glob(os.path.join(LIG, "*.pdbqt")))
    if a.liglist:
        keep = {l.strip() for l in open(a.liglist, encoding="utf-8") if l.strip()}
        ligs = [l for l in ligs if os.path.basename(l)[:-6] in keep]
    if a.lig_limit:
        ligs = ligs[:a.lig_limit]

    S = dict(STAGE[a.stage])
    if a.exh is not None:
        S["exh"] = a.exh
    if a.max_evals is not None:
        S["max_evals"] = a.max_evals
    tag = a.tag or f"stage{a.stage}"
    print(f"tag={tag}  exh={S['exh']}  num_modes={S['modes']}  max_evals={S['max_evals'] or 'heuristic(无偏倚)'}")
    print(f"靶标 {len(D)} 个 | 配体 {len(ligs)} 个 | workers {a.workers} | chunk {a.chunk}")
    print(f"总对接次数 {len(D)*len(ligs):,}", flush=True)
    assert len(D) and len(ligs), "没有可用的靶标或配体"

    rows_all = []
    for _, t in D.iterrows():
        sym = str(t.symbol).upper()
        odir = os.path.join(OUT, sym)
        os.makedirs(odir, exist_ok=True)
        box6 = load_box(sym)
        cfg = {"receptor": os.path.join(REC, sym, "receptor.pdbqt"),
               "exh": S["exh"], "modes": S["modes"], "max_evals": S["max_evals"],
               "timeout": a.timeout, "outdir": odir, "keep_pose": a.keep_pose,
               "force": a.force, "tag": tag}
        if not os.path.exists(cfg["receptor"]):
            print(f"  [skip] {sym} 缺受体 PDBQT", flush=True); continue

        chunks = [ligs[i:i + a.chunk] for i in range(0, len(ligs), a.chunk)]
        jobs = []
        for i, ch in enumerate(chunks):
            cc = dict(cfg); cc["wid"] = i % a.workers
            jobs.append((sym, i, ch, box6, cc))
        n_cached = sum(1 for j in jobs if os.path.exists(chunk_path(odir, tag, j[1])))
        print(f"[{sym}] {t.pdb_id} box_c=({box6[0]:.1f},{box6[1]:.1f},{box6[2]:.1f}) "
              f"size=({box6[3]:.0f},{box6[4]:.0f},{box6[5]:.0f}) | {len(ligs)} 配体 {len(jobs)} 块"
              f"（已缓存 {n_cached}）", flush=True)

        t0 = time.time()
        got = 0
        # 【修复】改用 ThreadPoolExecutor：vina 由主进程 spawn（实测稳定），
        # 避免 ProcessPoolExecutor 工作进程 spawn 孙进程时偶发 WinError 5。
        # 线程在 subprocess.run 等待时释放 GIL，7 路 vina 仍真并行。
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for k, res in enumerate(ex.map(run_chunk, jobs), 1):
                got += len(res)
                if k % 5 == 0 or k == len(jobs):
                    el = time.time() - t0
                    print(f"    {k}/{len(jobs)} 块  {got} 配体  {el:.0f}s", flush=True)
        df = pd.concat([pd.read_csv(chunk_path(odir, tag, j[1])) for j in jobs],
                       ignore_index=True)
        df = df.drop_duplicates("chembl_id")
        df["symbol"] = sym
        df["tag"] = tag
        df["exh"] = S["exh"]
        df["max_evals"] = S["max_evals"] or 0
        df.to_csv(os.path.join(odir, f"scores_{tag}.csv"), index=False)
        # 清理 stage1 临时 pose：
        # ⚠ 本沙箱挂载了 safe-delete 批量删除守卫——os.remove 单文件会被拦截并阻塞 ~10s、
        # 超时抛 SAFE_DELETE_BULK_GUARD_ERROR（非 OSError，except OSError 拦不住），会拖垮甚至
        # 中断流水线（已实证：9 靶标 × 数百 scratch 文件导致 rc=1、顶合并表写不出）。
        # 临时 pose 不影响任何下游产物（下游只读 chunk/scores CSV），故直接跳过删除。
        # 若确需清理，改用 os.rename 移入 _trash（move 非 delete，守卫不拦截）并 broad-except。
        pass
        ok = int(df.affinity.notna().sum())
        print(f"    -> {ok}/{len(df)} 有打分，最佳 {df.affinity.min():.2f} kcal/mol，"
              f"耗时 {time.time()-t0:.0f}s", flush=True)
        rows_all.append(df)

    if rows_all:
        A = pd.concat(rows_all, ignore_index=True)
        keep = [c for c in ["symbol", "chembl_id", "affinity", "n_modes", "rmsd_lb", "rmsd_ub",
                            "sec", "rc", "err", "tag", "exh", "max_evals"] if c in A.columns]
        mfp = os.path.join(TAB, f"P6_docking_scores_{tag}.csv")
        # 【已修 2026-09-19】`--only` 部分重跑时 rows_all 只含本次靶标，若直接覆盖合并表
        # 会抹掉其它靶标数据。改为 merge-append：读入旧合并表 → 删掉本次靶标行 → 拼回新行，
        # 保留其它靶标的既有结果。（p6_score.py 另有自愈重建作双保险。）
        if os.path.exists(mfp):
            try:
                old = pd.read_csv(mfp)
                done = set(A.symbol.astype(str).str.upper())
                old = old[~old.symbol.astype(str).str.upper().isin(done)]
                A = pd.concat([old, A], ignore_index=True)
            except Exception:
                pass
        A[keep].to_csv(mfp, index=False)
        print(f"\n汇总 -> results/tables/P6_docking_scores_{tag}.csv ({len(A):,} 行)")
        print(A.groupby("symbol").affinity.agg(["count", "min", "median"]).round(2).to_string())


if __name__ == "__main__":
    main()
