#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_ligands.py -- P6-B：构建 FDA/已批准药物配体库（SMILES -> 3D -> PDBQT）

库来源：**ChEMBL REST**（`max_phase=4` 即已批准药物，4,225 个），这是 DrugBank
"已批准药物"的开放等价物（DrugBank 全量需授权）。同时与本地
**Drug Repurposing Hub**（Broad Institute）的 `pert_iname / clinical_phase / moa / indication`
交叉注释，使每个配体都能追溯到药物名与临床期。

过滤漏斗（全部记录在 results/tables/P6_ligand_library.csv，便于审稿追溯）：
  F1 SMILES 可被 RDKit 解析
  F2 取最大片段（去反离子/成盐），并剔除含金属、分子量 <100 或 >900
  F3 类药性：HBD<=10、HBA<=15、可旋转键<=20、|形式电荷|<=2
  F4 3D 构象生成成功（ETKDGv3, seed=42）→ MMFF94s 优化
  F5 meeko 转 PDBQT 成功（AutoDock 原子类型 + Gasteiger 电荷）

另附 **已知镇痛相关药物清单**（`PAIN_PRIOR`），仅作反向阳性对照的"标注"用途，
不参与任何筛选 —— 用于 P6-D 检验流程能否召回已知镇痛药-靶点关联。

产出：docking/ligands/*.pdbqt、results/tables/P6_ligand_library.csv、P6_ligand_funnel.json
用法：python p6_ligands.py
"""
import os, re, json, gzip, time, socket, traceback, sys
import urllib.request
import multiprocessing as mp
import numpy as np, pandas as pd

socket.setdefaulttimeout(60)


def _require(mods):
    """解释器依赖自检（护栏）。

    【踩过的坑】用错解释器时本脚本**不会报错退出**：managed python 里没有 rdkit，
    于是 3,311 个配体全部被记成 `EXC_ModuleNotFoundError:No module named 'rdkit'`，
    并把 results/tables/P6_ligand_library.csv 覆盖成 pdbqt_ok=0 的空结果 ——
    表面看像"化学上全部制备失败"，实际是环境问题。这里前置拦截，避免静默污染产物。
    """
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


_require(["rdkit", "meeko", "numpy", "pandas"])

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
LIGDIR = os.path.join(ROOT, "docking/ligands")
CACHE = os.path.join(ROOT, "data/raw/druglib/chembl_approved_molecules.json")
os.makedirs(LIGDIR, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (research; CPSP-ligand-lib)"}
NWORK = 6

# 已知/候选镇痛相关药物：仅用于 P6-D 的反向阳性对照标注
PAIN_PRIOR = {
    "gabapentin": ["CACNA2D1", "CACNA2D2"], "pregabalin": ["CACNA2D1", "CACNA2D2"],
    "mirogabalin": ["CACNA2D1"], "gabapentin enacarbil": ["CACNA2D1"],
    "carbamazepine": ["SCN9A", "SCN10A"], "oxcarbazepine": ["SCN9A", "SCN10A"],
    "eslicarbazepine": ["SCN9A"], "lamotrigine": ["SCN9A", "SCN10A"],
    "phenytoin": ["SCN9A"], "lacosamide": ["SCN9A", "SCN10A"],
    "mexiletine": ["SCN9A", "SCN10A"], "lidocaine": ["SCN9A", "SCN10A"],
    "ambroxol": ["SCN10A"], "topiramate": ["SCN9A", "GABRA1"],
    "valproic acid": ["GABRA1", "SCN9A"], "levetiracetam": ["SCN9A"],
    "perampanel": ["SCN9A"], "zonisamide": ["SCN9A"],
    "ketamine": ["OPRM1"], "esketamine": ["OPRM1"], "memantine": ["OPRM1"],
    "morphine": ["OPRM1"], "oxycodone": ["OPRM1"], "hydromorphone": ["OPRM1"],
    "fentanyl": ["OPRM1"], "sufentanil": ["OPRM1"], "remifentanil": ["OPRM1"],
    "methadone": ["OPRM1"], "tramadol": ["OPRM1", "SCN9A"],
    "tapentadol": ["OPRM1"], "buprenorphine": ["OPRM1"], "naltrexone": ["OPRM1"],
    "nalmefene": ["OPRM1"],
    "amitriptyline": ["SCN9A", "ADRA2A"], "nortriptyline": ["SCN9A", "ADRA2A"],
    "duloxetine": ["SCN9A"], "venlafaxine": ["SCN9A"], "milnacipran": ["SCN9A"],
    "clonidine": ["ADRA2A"], "dexmedetomidine": ["ADRA2A"], "tizanidine": ["ADRA2A"],
    "baclofen": ["GABRA1"],
    "clonazepam": ["GABRA1"], "diazepam": ["GABRA1"], "midazolam": ["GABRA1"],
    "flupirtine": ["KCNQ2"], "ezogabine": ["KCNQ2"], "retigabine": ["KCNQ2"],
    "sumatriptan": ["ADRA2A"], "zolmitriptan": ["ADRA2A"],
    "dronabinol": ["CNR2"], "nabilone": ["CNR2"],
    "capsaicin": ["TRPV1"], "resiniferatoxin": ["TRPV1"],
    "celecoxib": ["PTGS2"], "ibuprofen": ["PTGS2"], "diclofenac": ["PTGS2"],
    "dexamethasone": ["NR3C1"], "prednisolone": ["NR3C1"],
    "minocycline": ["CASP1"], "riluzole": ["SCN9A"],
    "fluvoxamine": ["SIGMAR1"], "donepezil": ["SIGMAR1"], "dextromethorphan": ["SIGMAR1"],
    "ifenprodil": ["SIGMAR1"], "pentoxifylline": ["PDE4A"],
    "nefopam": ["SCN9A"], "propofol": ["GABRA1"], "nitrous oxide": ["OPRM1"],
    "duloxetine hcl": ["SCN9A"], "phenytoin sodium": ["SCN9A"],
    "pregabalin ": ["CACNA2D1"], "cannabidiol": ["CNR2"],
}


def fetch_chembl_approved():
    """ChEMBL max_phase=4 分子，缓存为 json-lines"""
    if os.path.exists(CACHE) and os.path.getsize(CACHE) > 10000:
        out = [json.loads(l) for l in open(CACHE, encoding="utf-8")]
        print(f"[cache] ChEMBL approved molecules: {len(out)}")
        return out
    out = []
    offset, limit = 0, 1000
    while True:
        url = ("https://www.ebi.ac.uk/chembl/api/data/molecule.json?"
               f"max_phase=4&limit={limit}&offset={offset}")
        for attempt in range(4):
            try:
                req = urllib.request.Request(url, headers=UA)
                j = json.loads(urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "replace"))
                break
            except Exception as e:
                print(f"  page offset={offset} retry {attempt+1}: {type(e).__name__}", flush=True)
                time.sleep(3)
        else:
            print(f"  page offset={offset} FAILED, stop")
            break
        ms = j.get("molecules") or []
        if not ms:
            break
        for m in ms:
            st = m.get("molecule_structures") or {}
            out.append({"chembl_id": m.get("molecule_chembl_id"),
                        "pref_name": m.get("pref_name"),
                        "max_phase": m.get("max_phase"),
                        "first_approval": m.get("first_approval"),
                        "molecule_type": m.get("molecule_type"),
                        "smiles": st.get("canonical_smiles"),
                        "inchi_key": st.get("standard_inchi_key"),
                        "atc": ";".join(m.get("atc_classifications") or [])})
        total = (j.get("page_meta") or {}).get("total_count")
        print(f"  fetched {len(out)}/{total}", flush=True)
        offset += limit
        if offset >= (total or 0):
            break
    with open(CACHE, "w", encoding="utf-8") as f:
        for r in out:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    return out


def std_and_embed(args):
    """worker：SMILES -> 标准化 + 3D + PDBQT 字符串"""
    chembl_id, smi = args
    res = {"chembl_id": chembl_id, "pass": False, "reason": ""}
    try:
        from rdkit import Chem
        from rdkit.Chem import Descriptors, rdMolDescriptors, AllChem
        from rdkit.Chem.MolStandardize import rdMolStandardize
        from meeko import MoleculePreparation, PDBQTWriterLegacy
        from rdkit import RDLogger
        RDLogger.DisableLog("rdApp.*")

        m = Chem.MolFromSmiles(smi)
        if m is None:
            res["reason"] = "F1_parse_fail"; return res
        # 去反离子、保留最大有机片段。
        # 【踩过的坑 · 已修】旧代码用 rdMolStandardize.FragmentParent(m)：它对本库中
        # 含盐的多组分 SMILES（ChEMBL max_phase=4 里大量药物以盐形式登记）会抛
        # RuntimeError，被 `try/except: pass` 吞掉后 m 仍是带反离子的多组分分子，
        # 随后 EmbedMolecule 再抛 RuntimeError，被函数末尾 except 记成
        # EXC_RuntimeError —— 结果 1,078 个含盐药物（丙戊酸钠、色甘酸钠、普罗帕酮、
        # 沙奎那韦、阿仑膦酸钠、卡巴胆碱…全是临床常用药）被无声丢弃，且 reason 列
        # 完全看不出真因。LargestFragmentChooser 按重原子数选最大片段，对盐稳定生效
        # （已验证同流程 150/150 通过）。
        try:
            m = rdMolStandardize.LargestFragmentChooser().choose(m)
        except Exception as e:
            res["reason"] = f"F1_frag_fail:{type(e).__name__}"; return res
        if m is None or m.GetNumAtoms() == 0:
            res["reason"] = "F1_frag_empty"; return res
        if any(a.GetAtomicNum() in (3, 11, 12, 13, 19, 20, 29, 30, 26, 82, 80, 78, 46, 78)
               for a in m.GetAtoms()):
            res["reason"] = "F2_metal"; return res
        mw = Descriptors.MolWt(m)
        if mw < 100 or mw > 900:
            res["reason"] = f"F2_mw_{mw:.0f}"; return res
        hbd = rdMolDescriptors.CalcNumHBD(m); hba = rdMolDescriptors.CalcNumHBA(m)
        rot = rdMolDescriptors.CalcNumRotatableBonds(m)
        chg = Chem.GetFormalCharge(m)
        res.update(mw=round(mw, 1), hbd=hbd, hba=hba, rotb=rot, charge=chg,
                   formula=rdMolDescriptors.CalcMolFormula(m),
                   logp=round(Descriptors.MolLogP(m), 2),
                   tpsa=round(Descriptors.TPSA(m), 1))
        if hbd > 10 or hba > 15 or rot > 20 or abs(chg) > 2:
            res["reason"] = "F3_druglikeness"; return res

        mh = Chem.AddHs(m)
        ps = AllChem.ETKDGv3(); ps.randomSeed = 42
        if AllChem.EmbedMolecule(mh, ps) != 0:
            ps.useRandomCoords = True
            if AllChem.EmbedMolecule(mh, ps) != 0:
                res["reason"] = "F4_embed_fail"; return res
        try:
            AllChem.MMFFOptimizeMolecule(mh, maxIters=400)
        except Exception:
            try: AllChem.UFFOptimizeMolecule(mh, maxIters=400)
            except Exception: pass

        prep = MoleculePreparation()
        setups = prep.prepare(mh)
        if not setups:
            res["reason"] = "F5_meeko_no_setup"; return res
        txt, ok, err = PDBQTWriterLegacy.write_string(setups[0])
        if not ok or not txt:
            res["reason"] = f"F5_pdbqt_fail:{str(err)[:40]}"; return res
        n_rot = txt.count("BRANCH")
        res.update(pdbqt=txt, n_torsions=n_rot)
        res["pass"] = True          # 注意：pass 是 Python 关键字，不能写成 res.update(pass=True)
        return res
    except Exception as e:
        # 把异常消息一并写进 reason：否则只留 EXC_XxxError 一个名字，像上面
        # FragmentParent 那样的静默失败排查起来要花很久。
        res["reason"] = f"EXC_{type(e).__name__}:{str(e)[:45]}"
        return res


def main():
    print("=== 1. 拉取 ChEMBL 已批准药物 ===", flush=True)
    mols = fetch_chembl_approved()
    df = pd.DataFrame(mols)
    print(f"ChEMBL max_phase=4: {len(df)} 条；有 SMILES 的 "
          f"{df.smiles.notna().sum()}；分子类型分布 {df.molecule_type.value_counts().to_dict()}")

    # 与 Drug Repurposing Hub 交叉注释
    drh = pd.read_csv(os.path.join(ROOT, "data/raw/druglib/repurposing_drugs.txt"),
                      sep="\t", skiprows=9, dtype=str, low_memory=False)
    drh.columns = [c.strip() for c in drh.columns]
    name2 = {}
    for _, r in drh.iterrows():
        nm = str(r.get("pert_iname", "") or "").strip().lower()
        if nm:
            name2[nm] = (r.get("clinical_phase"), r.get("moa"), r.get("disease_area"),
                         r.get("indication"), r.get("target"))
    dn = df.pref_name.astype(str).str.strip().str.lower()
    df["drh_phase"] = dn.map(lambda x: (name2.get(x) or (None,))[0])
    df["drh_moa"] = dn.map(lambda x: (name2.get(x) or (None, None))[1])
    df["drh_indication"] = dn.map(lambda x: (name2.get(x) or (None, None, None, None))[3])
    df["pain_prior"] = dn.map(lambda x: x in PAIN_PRIOR)
    print(f"与 Drug Repurposing Hub 匹配到: {df.drh_phase.notna().sum()}")
    print(f"已知镇痛相关药物命中: {int(df.pain_prior.sum())} 个 "
          f"{sorted(df[df.pain_prior].pref_name.astype(str).str.lower().tolist())[:12]}")

    # 只保留小分子（对接只对有机小分子有意义）
    SMALL = {"Small molecule", "Small Molecule"}
    df["is_small"] = df.molecule_type.isin(SMALL)
    print("非小分子被排除:", df[~df.is_small].molecule_type.value_counts().to_dict())
    work = df[df.is_small & df.smiles.notna()].copy()
    work = work.drop_duplicates("inchi_key").drop_duplicates("smiles")
    print(f"待制备配体: {len(work)}", flush=True)

    print("\n=== 2. 标准化 + 3D + PDBQT（多进程）===", flush=True)
    args = list(zip(work.chembl_id, work.smiles))
    t0 = time.time()
    out = []
    with mp.Pool(NWORK) as pool:
        for i, r in enumerate(pool.imap_unordered(std_and_embed, args, chunksize=20), 1):
            out.append(r)
            if i % 250 == 0:
                print(f"  {i}/{len(args)}  elapsed {time.time()-t0:.0f}s  ok={sum(x['pass'] for x in out)}",
                      flush=True)
    R = pd.DataFrame(out)
    meta = work.merge(R, on="chembl_id", how="left")

    # 写出 PDBQT
    n_written = 0
    for _, r in meta[meta["pass"] == True].iterrows():
        cid = str(r.chembl_id)
        p = os.path.join(LIGDIR, f"{cid}.pdbqt")
        if not (os.path.exists(p) and os.path.getsize(p) > 0):
            with open(p, "w", encoding="utf-8") as f:
                f.write(r.pdbqt)
        n_written += 1
    print(f"PDBQT 写出: {n_written} 个 -> {LIGDIR}")

    funnel = {"chembl_max_phase4_total": int(len(df)),
              "with_smiles": int(df.smiles.notna().sum()),
              "small_molecule": int(work.shape[0]),
              "after_dedup": int(work.shape[0]),
              "pdbqt_ok": int((meta["pass"] == True).sum()),
              "pain_prior_in_library": int(meta[meta["pass"] == True].pain_prior.sum())}
    drops = meta[meta["pass"] != True].reason.fillna("unknown")
    drops = drops[drops != ""].value_counts().to_dict()
    funnel["dropped_reasons"] = {k: int(v) for k, v in drops.items()}
    json.dump(funnel, open(os.path.join(TAB, "P6_ligand_funnel.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)

    keep = ["chembl_id", "pref_name", "max_phase", "first_approval", "smiles", "inchi_key",
            "atc", "drh_phase", "drh_moa", "drh_indication", "pain_prior",
            "mw", "logp", "tpsa", "hbd", "hba", "rotb", "charge", "formula",
            "n_torsions", "pass", "reason"]
    keep = [c for c in keep if c in meta.columns]
    meta[keep].to_csv(os.path.join(TAB, "P6_ligand_library.csv"), index=False)
    print("\n=== 漏斗 ===")
    print(json.dumps(funnel, ensure_ascii=False, indent=1))
    print("表 -> results/tables/P6_ligand_library.csv")


if __name__ == "__main__":
    main()
