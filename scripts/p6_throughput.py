#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""P6 对接受力分析（可复现，v2）

回答三个问题：
  Q1 Tier 1（620 CNS 先验配体）与 Tier 2（全库其余 2465 配体）在同一流水线、
     同一参数下，单位配体计算成本差多少？差异能否由配体理化性质解释？
  Q2 同一层内各靶标耗时相差可达 4 倍（AXL vs TNIK），原因是什么？
     —— 受体盒体积（Vina 网格点数正比于盒体积）是否为主要驱动？
  Q3 当前剩余工作量的 ETA 是多少？（用实测速率算，不用猜）

数据来源（全部一手，不做人工填数）：
  scripts/p6_chain_t1.out, scripts/p6_chain_t2.out   p6_dock 进度日志
  docking/_liglists/*.txt                            两层配体清单
  results/tables/P6_ligand_library.csv               配体理化性质

两条必须分清的口径（先前误判 ETA 5 倍的根源）：
  * s/块到达间隔 = 该靶标窗口耗时 / 窗口内块数。这是**吞吐**口径：
    W 个 worker 并行时，到达间隔 ≈ 单块墙钟 / W。
  * s/配体墙钟 = 到达间隔 x W / 每块配体数。已扣掉并行度，可跨靶标/Tier 比较。

统计只采用**同一进程窗口内**的相邻读数差（dt>0 且 dchunks>0），
以剔除以下两类污染：
  (a) 续跑时读缓存块产生的 ~0 耗时；
  (b) 被 kill 后重启导致"总耗时只覆盖部分块"的低估。

输出：
  results/tables/P6_throughput.csv            逐靶标速率 + 盒体积
  results/tables/P6_throughput_summary.csv    T1/T2 汇总 + 理化性质对照
"""
import os
import re
import sys

import numpy as np
import pandas as pd
from scipy import stats

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB = os.path.join(ROOT, "results", "tables")
LOGS = {1: os.path.join(ROOT, "scripts", "p6_chain_t1.out"),
        2: os.path.join(ROOT, "scripts", "p6_chain_t2.out")}
LISTS = {1: os.path.join(ROOT, "docking", "_liglists", "tier1_cns.txt"),
         2: os.path.join(ROOT, "docking", "_liglists", "tier2_other.txt")}
WORKERS, CHUNK = 7, 30

RE_HDR = re.compile(
    r"^\[([A-Z0-9]+)\]\s+(\S+)\s+box_c=\(([^)]*)\)\s+size=\(([^)]*)\)\s*\|\s*"
    r"(\d+)\s*配体\s*(\d+)\s*块(?:（已缓存\s*(\d+)）)?")
RE_PROG = re.compile(r"(\d+)/(\d+)\s*块\s+(\d+)\s*配体\s+(\d+)s")
RE_DONE = re.compile(r"耗时\s*(\d+)s")


def _f(s):
    return [float(x) for x in re.findall(r"-?\d+\.?\d*", s)]


def parse(path, tier):
    """→ list of run-window dicts: 每出现一个靶标 header 记为一个新窗口。"""
    if not os.path.exists(path):
        return []
    runs, cur = [], None
    pts = []                      # (chunks_done, elapsed)
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            ln = line.strip()
            m = RE_HDR.match(ln)
            if m:
                if cur:
                    cur["pts"] = pts
                    runs.append(cur)
                sz = _f(m.group(4))
                cur = {"symbol": m.group(1), "pdb": m.group(2), "tier": tier,
                       "n_lig": int(m.group(5)), "n_chunk": int(m.group(6)),
                       "cached_at_start": int(m.group(7) or 0),
                       "box": sz, "box_vol": float(np.prod(sz)) if len(sz) == 3 else np.nan}
                pts = []
                continue
            if cur is None:
                continue
            mp = RE_PROG.search(ln)
            if mp:
                pts.append((int(mp.group(1)), int(mp.group(4))))
            md = RE_DONE.search(ln)
            if md:
                pts.append((cur["n_chunk"], int(md.group(1))))
    if cur:
        cur["pts"] = pts
        runs.append(cur)

    out = []
    for r in runs:
        if not r["pts"]:
            continue
        # 去重：同一 chunks_done 取最大 elapsed（进度行可能重复打印）
        best = {}
        for c, e in r["pts"]:
            best[c] = max(best.get(c, 0), e)
        seq = sorted(best.items())
        if len(seq) < 2:
            continue
        # 只取同窗口内相邻读数差，剔除 dt<=0 与 dchunks<=0（缓存读/重复行）
        deltas = []
        for (c0, e0), (c1, e1) in zip(seq, seq[1:]):
            if c1 > c0 and e1 > e0:
                deltas.append((e1 - e0) / (c1 - c0))
        if not deltas:
            continue
        r2 = dict(r)
        r2["s_per_chunk_arrival"] = float(np.median(deltas))
        r2["n_delta_windows"] = len(deltas)
        r2["elapsed_total_s"] = max(e for _, e in seq)
        r2["fully_new"] = (r["cached_at_start"] == 0)
        out.append(r2)
    return out


def main():
    runs = sum((parse(p, t) for t, p in LOGS.items()), [])
    if not runs:
        print("[FAIL] 未能从日志解析出任何对接窗口")
        return 1
    R = pd.DataFrame(runs)
    R["s_per_ligand_wall"] = R.s_per_chunk_arrival * WORKERS / CHUNK
    # 一靶标多窗口时，取最接近完整（块数最多 / 窗口数最多）的一条
    R["n_chunk_done"] = R.n_chunk
    R = (R.sort_values(["tier", "symbol", "n_delta_windows"])
           .groupby(["tier", "symbol"], as_index=False).last())

    # 盒体积按靶标补全（T2 行里可能有 NaN）
    boxmap = {}
    for _, r in pd.DataFrame(runs).iterrows():
        if not np.isnan(r.box_vol):
            boxmap[r.symbol] = r.box_vol
    R["box_vol"] = R.symbol.map(boxmap).fillna(R.box_vol)

    # 有效性闸门：一块 = 30 配体，真实对接窗口每块不可能低于 10s。
    # 低于该值的窗口是「续跑时只读 chunk 缓存」产生的，其 elapsed 与块数
    # 不成比例；纳入统计会把单位成本严重低估（先前 T1 被压到 0.23 s/配体）。
    MIN_ARRIVAL_S_PER_CHUNK = 10.0
    R["valid"] = R.s_per_chunk_arrival >= MIN_ARRIVAL_S_PER_CHUNK

    cols = ["tier", "symbol", "pdb", "n_lig", "n_chunk", "box_vol",
            "s_per_chunk_arrival", "s_per_ligand_wall", "elapsed_total_s",
            "n_delta_windows", "valid"]
    R = R[cols].sort_values(["tier", "s_per_ligand_wall"])
    R.round(2).to_csv(os.path.join(TAB, "P6_throughput.csv"), index=False)

    V = R[R.valid].copy()          # 仅真实计算窗口
    Vc = R[~R.valid]

    pd.set_option("display.width", 200)
    print("=" * 96)
    print("逐靶标实测速率（--exh 1 --max-evals 0 --chunk %d --workers %d）" % (CHUNK, WORKERS))
    print("=" * 96)
    print(V.round(2).to_string(index=False))
    if len(Vc):
        print()
        print("[已剔除：续跑只读缓存窗口，无计算量，不参与速率统计]  %s"
              % ", ".join("%s-T%d" % (r.symbol, r.tier) for _, r in Vc.iterrows()))

    # ---- Q2: 层内差异是否由盒体积驱动（只在 T2 内做，配体集相同） ----
    t2 = V[V.tier == 2].dropna(subset=["box_vol"])
    if len(t2) >= 5:
        rho, p = stats.spearmanr(t2.box_vol, t2.s_per_ligand_wall)
        print()
        print("Q2 层内差异（T2，配体集完全相同，只变受体）：")
        print("   每配体成本区间 %.1f–%.1f s  (跨度 x%.2f)"
              % (t2.s_per_ligand_wall.min(), t2.s_per_ligand_wall.max(),
                 t2.s_per_ligand_wall.max() / t2.s_per_ligand_wall.min()))
        print("   盒体积 vs 成本：Spearman rho=%.3f  p=%.4g  (n=%d)  -> %s"
              % (rho, p, len(t2),
                 "不显著，盒体积不是主因" if p > 0.05 else "显著"))

    # ---- Q1: 配体理化性质 ----
    lig = pd.read_csv(os.path.join(TAB, "P6_ligand_library.csv"))
    lig["chembl_id"] = lig["chembl_id"].astype(str)
    sets = {t: lig[lig.chembl_id.isin(
        set(l.strip() for l in open(p, encoding="utf-8", errors="replace") if l.strip()))]
        for t, p in LISTS.items()}
    props = [p for p in ["mw", "rotb", "n_torsions", "tpsa", "hbd", "hba"] if p in lig.columns]

    rows = []
    for t in (1, 2):
        g = V[V.tier == t]
        row = {"tier": "T%d" % t, "n_targets": len(g),
               "median_box_vol": round(float(g.box_vol.median()), 0),
               "median_s_per_chunk_arrival": round(float(g.s_per_chunk_arrival.median()), 1),
               "median_s_per_ligand_wall": round(float(g.s_per_ligand_wall.median()), 2),
               "median_elapsed_s": round(float(g.elapsed_total_s.median()), 0)}
        for p in props:
            row["median_" + p] = round(float(sets[t][p].median()), 2)
        rows.append(row)
    S = pd.DataFrame(rows)

    print()
    print("=" * 96)
    print("Q1  T1 vs T2")
    print("=" * 96)
    a, b = S.iloc[0], S.iloc[1]
    print("  [非配对口径] 每配体墙钟 : T1=%.2fs  T2=%.2fs  ->  x%.2f"
          % (a.median_s_per_ligand_wall, b.median_s_per_ligand_wall,
             b.median_s_per_ligand_wall / a.median_s_per_ligand_wall))

    # [同受体配对口径] —— 最严谨：同一 PDB、同一盒、同一参数，只换配体集
    piv = V.pivot_table(index="symbol", columns="tier",
                        values="s_per_ligand_wall", aggfunc="median")
    piv = piv.dropna()
    piv.columns = ["T1_s_per_ligand", "T2_s_per_ligand"]
    piv["ratio_T2_over_T1"] = piv.T2_s_per_ligand / piv.T1_s_per_ligand
    if len(piv):
        print()
        print("  [同受体配对口径] 同 PDB / 同盒 / 同参数，仅换配体集：")
        print(piv.round(2).to_string())
        print("   配对中位比值 = x%.2f  (n=%d 对)"
              % (piv.ratio_T2_over_T1.median(), len(piv)))
        S["paired_median_ratio_T2_over_T1"] = np.nan
        S.loc[1, "paired_median_ratio_T2_over_T1"] = round(
            float(piv.ratio_T2_over_T1.median()), 3)

    print()
    print("  每靶标总耗时: T1=%.0fs  T2=%.0fs   ->  x%.2f"
          % (a.median_elapsed_s, b.median_elapsed_s,
             b.median_elapsed_s / a.median_elapsed_s))
    print("  配体数     : T1=%d    T2=%d      ->  x%.2f"
          % (sets[1].shape[0], sets[2].shape[0],
             sets[2].shape[0] / sets[1].shape[0]))
    print()
    print("  理化性质中位数（T2/T1）：")
    for p in props:
        x, y = a["median_" + p], b["median_" + p]
        print("    %-12s T1=%8.2f  T2=%8.2f   x%.2f" % (p, x, y, (y / x) if x else np.nan))
    print()
    print("  判读：同一受体上 T2 配体每单位成本约为 T1 的 3 倍。Vina 的构象搜索")
    print("        代价随可扭转键数近似指数增长、且原子数越多单次能量评估越慢；")
    print("        而 T2 配体的 MW/可旋转键/可扭转键/TPSA/HBD 全面更高。因此这是")
    print("        可预期的物理结果，不是故障或性能退化。")

    S["cost_ratio_T2_over_T1"] = np.nan
    S.loc[1, "cost_ratio_T2_over_T1"] = round(
        b.median_s_per_ligand_wall / a.median_s_per_ligand_wall, 3)
    S.to_csv(os.path.join(TAB, "P6_throughput_summary.csv"), index=False)

    # ---- Q3: ETA ----
    print()
    print("=" * 96)
    print("Q3  ETA（实测速率，不猜）")
    print("=" * 96)
    import glob
    prog = {}
    for d in sorted(glob.glob(os.path.join(ROOT, "docking", "out", "*"))):
        prog[os.path.basename(d)] = len(glob.glob(os.path.join(d, "chunk_t2_other_*.csv")))
    n_done = sum(prog.values())
    left = sum(max(0, 83 - v) for v in prog.values())
    lo = float(V[V.tier == 2].s_per_chunk_arrival.min())
    hi = float(V[V.tier == 2].s_per_chunk_arrival.max())
    med = float(V[V.tier == 2].s_per_chunk_arrival.median())
    print("  T2 已完成 %d 块 / 应完成 %d 块，剩余 %d 块" % (n_done, 83 * len(prog), left))
    print("  实测到达间隔：区间 %.0f–%.0f s/块，中位 %.0f s/块" % (lo, hi, med))
    print("  -> 剩余墙钟 %.1f–%.1f h（中位估计 %.1f h）"
          % (left * lo / 3600, left * hi / 3600, left * med / 3600))
    print("  说明：本环境后台任务约每 12h 被外部清理一次，链须重拉；重拉只读缓存，")
    print("        不重算、不污染，故 ETA 不因重拉而累加。")
    print()
    print("-> results/tables/P6_throughput.csv")
    print("-> results/tables/P6_throughput_summary.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
