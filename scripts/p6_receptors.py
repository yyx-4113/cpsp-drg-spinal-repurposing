#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_receptors.py -- P6-C1：受体准备（PDB -> 去水去杂 -> 补氢 -> PDBQT + 对接盒定义）

为什么需要单独一步：
  AutoDock Vina 需要 **PDBQT** 格式的受体，且必须显式给出对接盒（center + size）。
  对接盒的可靠来源是**共晶配体**的坐标 —— 有共晶配体的结构说明该口袋真能结合小分子，
  且配体本身的坐标就是口袋中心的最佳近似。

流程（逐靶标）：
  1. 下载 PDB（优先共晶结构，其次最高分辨率可解析结构）
  2. gemmi 读入 → 按 DBREF/SEQRES 定位靶标链
  3. 优选配体作为「盒定义配体」：重原子数 15–70、不在离子/缓冲剂/糖基/脂类排除表中、
     且不是多残基肽（同 resname 连续 ≥3 个残基视为肽）
  4. 盒 = 该配体质心；尺寸 = 配体在各轴的跨度 + 2×PAD(8 Å)，并裁剪到 [16, 30] Å
  5. 受体：只留靶标链的 ATOM 记录（去水、去所有 HETATM、去氢），写 receptor.pdb
  6. obabel -xr 转 receptor.pdbqt（刚性受体，Gasteiger 电荷 + AutoDock 原子类型）

产出：docking/receptors/<SYM>/{receptor.pdb,receptor.pdbqt,ligand_ref.pdb,box.json}、
      results/tables/P6_receptors.csv
用法：python p6_receptors.py [--only SYM1,SYM2] [--max-rows N] [--manual SYM:PDBID:LIGRES]
"""
import os, re, sys, json, argparse, subprocess, urllib.request, socket, time
import numpy as np, pandas as pd

socket.setdefaulttimeout(120)


def _require(mods):
    """解释器依赖自检（护栏）：用错解释器时本脚本会在每个靶标上静默抛
    ModuleNotFoundError 并被 except 吞成 status=EXC，最终呈现"全部靶标失败"的假象。
    这里前置拦截。"""
    import importlib
    missing = []
    for m in mods:
        try:
            importlib.import_module(m)
        except Exception as e:
            missing.append(f"{m}({type(e).__name__})")
    if missing:
        raise SystemExit(
            f"[FATAL] 解释器 {sys.executable} 缺少依赖: {', '.join(missing)}\n"
            f"        本脚本须用 venv 运行：\n"
            f"        C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe")


_require(["gemmi", "numpy", "pandas"])
import gemmi


def is_aa(res):
    """判断 gemmi.Residue 是否为氨基酸。

    【踩过的坑】`gemmi.Residue` **没有** `is_amino_acid()` —— 那是
    `gemmi.ResidueInfo` 的方法，必须先 `find_tabulated_residue(name)` 查表。
    直接写 `res.is_amino_acid()` 会 AttributeError，让受体准备在第一步就全军覆没。
    （同类坑：`Chain.remove_residue` 也不存在，见 prepare_one 内的说明。）
    """
    return gemmi.find_tabulated_residue(res.name).is_amino_acid()


ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
REC = os.path.join(ROOT, "docking/receptors")
OBABEL = "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/obabel.exe"
if not os.path.exists(OBABEL):
    raise SystemExit(f"[FATAL] 找不到 obabel: {OBABEL}（受体 PDBQT 转换必需）")
UA = {"User-Agent": "Mozilla/5.0 (research; CPSP-docking)"}
PAD = 8.0
SIZE_MIN, SIZE_MAX = 16.0, 30.0

# 不作为"盒定义配体"的残基：水/离子/缓冲剂/糖基化/脂类/常见辅因子与去污剂
BAD_LIG = {
    "HOH", "DOD", "WAT", "NA", "CL", "K", "MG", "CA", "ZN", "MN", "FE", "FE2", "CU", "NI",
    "CD", "HG", "CO", "SO4", "PO4", "NO3", "CO3", "NH4", "ACT", "ACY", "FMT", "CIT", "FLC",
    "TLA", "MES", "EPE", "TRS", "IMD", "BME", "DTT", "EDO", "GOL", "PEG", "PG4", "PGE",
    "P6G", "1PE", "2PE", "DMS", "DMF", "DMI", "IOD", "BR", "SCN", "AZI", "MPD", "BTB",
    "NAG", "NDG", "BMA", "MAN", "FUC", "GAL", "GLA", "GLC", "BGC", "SIA", "XYS", "RIB",
    "PLM", "MYR", "OLA", "OLC", "STE", "Palm", "PE", "PC", "PS", "CLR", "CHL", "LPS",
    "FAD", "FMN", "NAD", "NAP", "NDP", "ADP", "ATP", "ANP", "AMP", "GDP", "GTP", "GNP",
    "SAH", "SAM", "ACP", "COA", "HEM", "BOG", "LDA", "C8E", "UNX", "UNL", "UNK", "ETA",
    "MRD", "PGO", "SER", "TAM", "PIN", "DIO", "12P", "3PG", "PPP", "TAR",
}


def download_pdb(pdb_id, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 2000:
        return dest
    for ext in (".pdb", ".cif"):
        url = f"https://files.rcsb.org/download/{pdb_id}{ext}"
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=180) as r, open(dest + ext, "wb") as f:
                f.write(r.read())
            if os.path.getsize(dest + ext) > 2000:
                return dest + ext
        except Exception as e:
            print(f"    download {pdb_id}{ext} fail: {type(e).__name__}")
    return None


def fetch_uniprot_fasta(acc):
    """取 UniProt 序列（本地缓存），用于链定位的序列匹配回退。"""
    fp = os.path.join(ROOT, "data/raw/uniprot", f"{acc}.fasta")
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    if os.path.exists(fp) and os.path.getsize(fp) > 50:
        txt = open(fp, encoding="utf-8").read()
    else:
        url = f"https://rest.uniprot.org/uniprotkb/{acc}.fasta"
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=60) as r:
                txt = r.read().decode("utf-8", "replace")
            if not txt.startswith(">"):
                return None
            open(fp, "w", encoding="utf-8").write(txt)
        except Exception:
            return None
    return "".join(l.strip() for l in txt.splitlines() if not l.startswith(">"))


def dbref_chains(pdb_path, uniprot):
    """定位对应 UniProt 的链。三级回退的第 1/2 级：
       PDB 格式 -> DBREF 行；mmCIF 格式 -> _struct_ref_seq 表
       （gemmi 0.7.5 没有 Structure.get_db_refs()，所以两种格式分别处理）
    """
    chains = set()
    acc = uniprot.upper()
    if pdb_path.endswith(".pdb"):
        for line in open(pdb_path, encoding="utf-8", errors="replace"):
            if line.startswith("DBREF") and acc in line.upper():
                chains.add(line[12])
    elif pdb_path.endswith(".cif"):
        try:
            import gemmi
            block = gemmi.cif.read(pdb_path).sole_block()
            strands = block.find_values("_struct_ref_seq.pdbx_strand_id")
            accs = block.find_values("_struct_ref_seq.pdbx_db_accession")
            for s, a in zip(strands, accs):
                if acc and acc in str(a).upper():
                    for one in re.split(r"[,\s]+", str(s)):
                        if one:
                            chains.add(one[0])
        except Exception:
            pass
    return {c for c in chains if c and c != "."}


def chain_to_seq(chain):
    """gemmi Chain -> 单字母氨基酸序列（跳过非氨基酸残基）"""
    import gemmi
    out = []
    for res in chain:
        if not is_aa(res):
            continue
        try:
            out.append(gemmi.find_tabulated_residue(res.name).one_letter_code)
        except Exception:
            out.append("X")
    return "".join(out)


def pick_chain_by_sequence(path, uniprot, prot_chains, verbose=True):
    """第 3 级回退：把 UniProt 序列与各链实测序列做比对，取 identity 最高的链。
    这比"取最长链"可靠得多 —— 复合物结构里最长链常是融合标签/抗体链而非靶标。"""
    ref = fetch_uniprot_fasta(uniprot) if uniprot else None
    if not ref:
        return None, {}
    import gemmi
    st = gemmi.read_structure(path)
    st.setup_entities()
    model = st[0]
    scores = {}
    for c in prot_chains:
        s = chain_to_seq(model[c])
        if len(s) < 20:
            continue
        # 用 ref 的最长连续匹配段长度作分数（对截短结构稳健）
        best = 0
        for i in range(0, max(1, len(s) - 30)):
            k = s[i:i + 30]
            j = ref.find(k)
            if j >= 0:
                best = max(best, 30)
        # 更精确：用 difflib 的匹配块总长
        import difflib
        sm = difflib.SequenceMatcher(None, s, ref, autojunk=False)
        matched = sum(b.size for b in sm.get_matching_blocks())
        scores[c] = matched / max(1, min(len(s), len(ref)))
    if not scores:
        return None, {}
    if verbose:
        print(f"    链序列匹配度: { {k: round(v, 3) for k, v in sorted(scores.items(), key=lambda x: -x[1])} }")
    best_c = max(scores, key=lambda k: scores[k])
    return (best_c if scores[best_c] > 0.30 else None), scores



def prepare_one(sym, uniprot, pdb_id, manual_lig=None, verbose=True):
    import gemmi
    outdir = os.path.join(REC, sym)
    os.makedirs(outdir, exist_ok=True)
    rec = {"symbol": sym, "uniprot": uniprot, "pdb_id": pdb_id}
    path = download_pdb(pdb_id, os.path.join(outdir, f"{pdb_id}"))
    if not path:
        rec.update(status="FAIL_download"); return rec
    rec["file"] = os.path.basename(path)

    st = gemmi.read_structure(path)
    st.setup_entities()
    st.remove_alternative_conformations()
    st.remove_hydrogens()
    st.remove_waters()
    model = st[0]

    # --- 靶标链（三级回退：DBREF/_struct_ref_seq -> 序列匹配 -> 最长链）---
    # 为什么不用"最长链"当默认：复合物结构里最长链常是融合标签/抗体/伴侣蛋白，
    # 而不是我们要对接的靶标。序列匹配用 UniProt 实测序列做锚，可靠得多。
    chains = dbref_chains(path, uniprot)
    prot_chains = [ch.name for ch in model if any(is_aa(r) for r in ch)]
    if not prot_chains:
        rec.update(status="FAIL_no_protein"); return rec
    how = None
    if chains & set(prot_chains):
        target_chains = sorted(chains & set(prot_chains)); how = "dbref"
    else:
        best, _ = pick_chain_by_sequence(path, uniprot, prot_chains, verbose=verbose)
        if best:
            target_chains = [best]; how = "seqmatch"
        else:
            target_chains = [max(prot_chains,
                                 key=lambda c: sum(1 for r in model[c] if is_aa(r)))]
            how = "longest"
    rec["target_chains"] = ",".join(target_chains)
    rec["chain_assignment"] = how

    # --- 选择盒定义配体 ---
    ligs = {}
    for ch in model:
        for res in ch:
            if is_aa(res) or res.name in ("HOH", "DOD", "WAT"):
                continue
            if res.name.upper() in {b.upper() for b in BAD_LIG}:
                continue
            heavy = sum(1 for a in res if a.element.name != "H")
            if heavy < 15 or heavy > 70:
                continue
            key = (ch.name, res.name, res.seqid.num, str(res.seqid.icode))
            coords = np.array([[a.pos.x, a.pos.y, a.pos.z] for a in res])
            ligs[key] = {"resname": res.name, "chain": ch.name, "resseq": res.seqid.num,
                         "n_heavy": heavy, "coords": coords}
    # 排除多残基肽。判据：**同一条链上**同 resname 且残基编号**连续** >=3 个。
    # 【踩过的坑】旧代码只看"同 resname 在全结构中出现 >=3 次"，这会把
    # **多聚体晶体里每条链各结合一个同一配体**的情形（典型：AXL 5U6B 的 7YS、
    # ACVR1 6SRH/5S75/5S78/5S7A 的 LU8）整批误判成"肽"而剔除，
    # 直接导致这两个 CPSP 机制核心靶标 FAIL_no_pocket_ligand。
    idx = {(v["chain"], v["resname"], v["resseq"]): k for k, v in ligs.items()}
    peptide = set()
    for k, v in ligs.items():
        run, n2 = 1, v["resseq"] + 1
        while (v["chain"], v["resname"], n2) in idx:
            run += 1
            n2 += 1
        if run >= 3:
            peptide.add(k)
    for k in peptide:
        ligs.pop(k, None)
    rec["n_candidate_ligands"] = len(ligs)

    chosen = None
    if manual_lig:
        for k, v in ligs.items():
            if v["resname"] == manual_lig:
                chosen = v; break
    if chosen is None and ligs:
        chosen = max(ligs.values(), key=lambda v: v["n_heavy"])
    if chosen is None:
        rec.update(status="FAIL_no_pocket_ligand")
        return rec

    coords = chosen["coords"]
    center = coords.mean(axis=0)
    extent = coords.max(axis=0) - coords.min(axis=0)
    size = np.clip(extent + 2 * PAD, SIZE_MIN, SIZE_MAX)
    rec.update(ligand_ref=chosen["resname"], ligand_chain=chosen["chain"],
               ligand_n_heavy=int(chosen["n_heavy"]),
               box_center=[round(float(x), 3) for x in center],
               box_size=[round(float(x), 2) for x in size])

    # 写盒参考配体
    with open(os.path.join(outdir, "ligand_ref.pdb"), "w", encoding="utf-8") as f:
        for ch in model:
            for res in ch:
                if (ch.name == chosen["chain"] and res.name == chosen["resname"]
                        and res.seqid.num == chosen["resseq"]):
                    for a in res:
                        f.write(f"HETATM{a.serial:5d} {a.name:<4s}{res.name:>3s} "
                                f"{ch.name}{res.seqid.num:4d}    "
                                f"{a.pos.x:8.3f}{a.pos.y:8.3f}{a.pos.z:8.3f}"
                                f"  1.00  0.00          {a.element.name:>2s}\n")

    # --- 写受体（去 HETATM，仅靶标链，去氢）---
    st2 = gemmi.read_structure(path)
    st2.setup_entities()
    st2.remove_alternative_conformations()
    st2.remove_hydrogens()
    st2.remove_waters()
    m2 = st2[0]
    for ch in list(m2):
        if ch.name not in target_chains:
            m2.remove_chain(ch.name)
    # 删掉所有非聚合物残基（配体/离子/糖基/水）。
    # 【踩过的坑】旧代码写 `ch.remove_residue(res.seqid)` —— gemmi.Chain **没有**
    # remove_residue 这个方法（删除残基的能力只在 Model 级提供），会直接
    # AttributeError 让受体准备全军覆没。改用 gemmi 原生方法。
    m2.remove_ligands_and_waters()
    recpdb = os.path.join(outdir, "receptor.pdb")
    st2.write_pdb(recpdb)

    # --- obabel -> PDBQT（刚性受体）---
    recpqt = os.path.join(outdir, "receptor.pdbqt")
    try:
        p = subprocess.run([OBABEL, "-ipdb", recpdb, "-opdbqt", "-xr", "-O", recpqt],
                           capture_output=True, text=True, timeout=300)
        if not os.path.exists(recpqt) or os.path.getsize(recpqt) < 500:
            rec.update(status="FAIL_obabel", obabel_err=(p.stderr or p.stdout)[:200])
            return rec
    except Exception as e:
        rec.update(status=f"FAIL_obabel_{type(e).__name__}")
        return rec

    n_atoms = sum(1 for l in open(recpqt, encoding="utf-8", errors="replace")
                  if l.startswith(("ATOM", "HETATM")))

    # --- 合理性检查：盒中心到受体最近重原子的距离 ---
    # 若链定位错了（例如盒定义配体其实长在别的链上），盒中心会悬在受体外面，
    # 这个距离会明显偏大（口袋内的正常值一般 < 8 Å）。用作自动质控标记。
    rcoords = []
    for l in open(recpdb, encoding="utf-8", errors="replace"):
        if l.startswith("ATOM"):
            try:
                rcoords.append((float(l[30:38]), float(l[38:46]), float(l[46:54])))
            except ValueError:
                pass
    if rcoords:
        A = np.asarray(rcoords)
        dmin = float(np.sqrt(((A - center) ** 2).sum(axis=1)).min())
        rec["center_min_dist_to_receptor"] = round(dmin, 2)
        if dmin > 12.0:
            rec["qc_warning"] = "box_center_far_from_receptor"

    rec.update(status="OK", receptor_atoms=n_atoms, receptor_pdbqt=recpqt,
               receptor_kb=round(os.path.getsize(recpqt) / 1024, 1))
    json.dump({k: v for k, v in rec.items() if k != "file"},
              open(os.path.join(outdir, "box.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    if verbose:
        print(f"  {sym:10s} {pdb_id}  chain={rec['target_chains']} "
              f"lig={rec['ligand_ref']}({rec['ligand_n_heavy']} heavy) "
              f"size={rec['box_size']} atoms={n_atoms}", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default=None)
    ap.add_argument("--max-rows", type=int, default=None)
    ap.add_argument("--manual", default=None, help="SYM:PDBID:LIGRES 覆盖自动选择")
    a = ap.parse_args()

    T = pd.read_csv(os.path.join(TAB, "P6_target_selection.csv"))
    D = T[T.decision == "DOCK"].copy()
    if a.only:
        want = {s.strip().upper() for s in a.only.split(",")}
        D = D[D.symbol.str.upper().isin(want)]
    if a.max_rows:
        D = D.head(a.max_rows)
    manual = {}
    if a.manual:
        for item in a.manual.split(";"):
            s, p, l = item.split(":")
            manual[s.upper()] = (p, l)
    print(f"待准备受体: {len(D)} 个", flush=True)

    rows = []
    for _, r in D.iterrows():
        sym = str(r.symbol).upper()
        # 候选结构按优先级回退：第一个结构若没有类药物配体，就试下一个
        cands = [p for p in str(r.get("pdb_candidates") or r.pdb_id).split(";") if p]
        if sym in manual:
            cands = [manual[sym][0]]
        lig_hint = manual[sym][1] if sym in manual else None
        print(f"[{sym}] 候选 {cands}", flush=True)
        rec = None
        for pdb_id in cands:
            try:
                rec = prepare_one(sym, r.uniprot, pdb_id, manual_lig=lig_hint)
            except Exception:
                import traceback; traceback.print_exc()
                rec = {"symbol": sym, "pdb_id": pdb_id, "status": "EXC"}
            if rec.get("status") == "OK":
                break
            print(f"    {pdb_id} -> {rec.get('status')}，尝试下一个候选", flush=True)
        if rec is None:
            rec = {"symbol": sym, "pdb_id": None, "status": "FAIL_no_candidate"}
        rows.append(rec)
        pd.DataFrame(rows).to_csv(os.path.join(TAB, "P6_receptors.csv"), index=False)

    R = pd.DataFrame(rows)
    print("\n=== 受体准备状态 ===")
    print(R.status.value_counts().to_dict())
    ok = R[R.status == "OK"]
    print("\n=== 可对接靶标 ===")
    cols = [c for c in ["symbol", "uniprot", "pdb_id", "ligand_ref", "ligand_n_heavy",
                        "target_chains", "receptor_atoms", "box_center", "box_size"] if c in ok.columns]
    print(ok[cols].to_string(index=False))
    print("\n表 -> results/tables/P6_receptors.csv")


if __name__ == "__main__":
    main()
