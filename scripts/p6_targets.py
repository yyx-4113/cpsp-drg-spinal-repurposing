#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_targets.py (v2) -- P6-A：把 hub 映射为「可对接的靶蛋白」

按 PROJECT_PLAN.md §6 的锁靶规则逐条打分：
  R1 人源直系同源（UniProt reviewed/Swiss-Prot, organism 9606）
  R2 有实验 PDB 结构（优先）或 AlphaFold2 pLDDT > 70
  R3 有明确可成药口袋 —— 用**共晶小分子配体**作为口袋存在的硬证据，
     且该配体坐标可直接作为对接盒中心
  R4 可成药类别（激酶/蛋白酶/磷酸酶/转运体/GPCR/离子通道/酶…）

v2 的改动（v1 失败原因）：
  · PDBe `/mappings/uniprot/{acc}` 已返回 404 → 改用 **RCSB Search API**（可用），
    并按 `rcsb_entry_info.resolution_combined` 升序排序，再单独查"含非聚合物配体"的子集。
  · v1 跑 8 个靶标后被外部终止且丢失全部结果 → v2 **每完成一个靶标即增量落盘**，
    并支持断点续跑（`--resume`，默认开启）。

数据来源（全开放）：UniProt REST · RCSB Search/Data API · ChEMBL REST · AlphaFold DB API ·
Drug Repurposing Hub（本地 target 列 = 该基因已被哪些已批准药物靶向）。

产出：results/tables/P6_target_selection.csv · P6_target_selection_detail.json
用法：python p6_targets.py
"""
import os, re, sys, json, time, traceback, urllib.request, urllib.error, socket
import numpy as np, pandas as pd

socket.setdefaulttimeout(45)
ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
CACHE = os.path.join(TAB, "P6_target_selection_cache.json")
OUT_CSV = os.path.join(TAB, "P6_target_selection.csv")
UA = {"User-Agent": "Mozilla/5.0 (research; CPSP-target-selection)"}

ION_LIKE = {"NA", "CL", "K", "MG", "CA", "ZN", "MN", "FE", "CU", "NI", "CD", "HG", "SO4",
            "PO4", "GOL", "EDO", "HOH", "DOD", "ACT", "PEG", "PG4", "TRS", "DMS", "IOD",
            "BR", "FMT", "NO3", "MES", "EPE", "IMD", "BME", "TLA", "CIT", "FLC", "SCN",
            "AZI", "CO3", "NH4", "UNX", "UNL", "NAG", "BMA", "MAN", "FUC", "GAL", "GLC"}


def get_json(url, tries=3, sleep=0.5):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=45) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            time.sleep(sleep * (i + 1))
        except Exception:
            time.sleep(sleep * (i + 1))
    return None


def post_json(url, payload, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                         headers={**UA, "Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8", "replace"))
        except Exception:
            time.sleep(1.5 * (i + 1))
    return None


def rcsb_search(acc, rows=25, only_holo=False):
    """UniProt accession -> PDB entry 列表（按分辨率升序）

    注意：`rcsb_entry_info.nonpolymer_bound_components` 用 `exists` 算子会 **400 Bad Request**
    （该字段不可索引）。必须改用可索引的计数属性 `nonpolymer_entity_count` + `greater 0`。
    """
    nodes = [{"type": "terminal", "service": "text", "parameters": {
        "attribute": "rcsb_polymer_entity_container_identifiers.reference_sequence_identifiers.database_accession",
        "operator": "exact_match", "value": acc}}]
    if only_holo:
        nodes.append({"type": "terminal", "service": "text", "parameters": {
            "attribute": "rcsb_entry_info.nonpolymer_entity_count",
            "operator": "greater", "value": 0}})
    payload = {
        "query": (nodes[0] if len(nodes) == 1 else
                  {"type": "group", "logical_operator": "and", "nodes": nodes}),
        "return_type": "entry",
        "request_options": {
            "results_verbosity": "compact",
            "sort": [{"sort_by": "rcsb_entry_info.resolution_combined", "direction": "asc"}],
            "paginate": {"start": 0, "rows": rows}},
    }
    j = post_json("https://search.rcsb.org/rcsbsearch/v2/query", payload)
    if not j:
        return []
    return j.get("result_set", []) or []


def entry_info(pdb_id):
    e = get_json(f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}")
    if not e:
        return None
    ei = e.get("rcsb_entry_info") or {}
    return {"pdb": pdb_id,
            "resolution": (ei.get("resolution_combined") or [None])[0],
            "method": ei.get("experimental_method") or "",
            "ligands": ei.get("nonpolymer_bound_components") or [],
            "n_nonpoly": ei.get("nonpolymer_entity_count") or 0}


def method_ok(m):
    """RCSB entry 级 `experimental_method` 实际返回 'X-ray' / 'Electron microscopy'，
    不是 'X-RAY DIFFRACTION' —— 必须归一化后判断，否则会把所有结构都过滤掉（踩过）。"""
    if isinstance(m, (list, tuple)):
        m = " ".join(str(x) for x in m)
    m = str(m).lower()
    return ("x-ray" in m) or ("electron microscopy" in m) or ("electron crystallography" in m)


def pharma_ligands(ligs):
    return [l for l in (ligs or []) if l.upper() not in ION_LIKE]


# ---------------------------------------------------------------- 载入输入
hub = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
hub["symbol"] = hub["symbol"].str.upper()
HUB = hub.sort_values(["n_methods", "lasso_freq"], ascending=False).reset_index(drop=True)

core = pd.read_csv(os.path.join(TAB, "META_DRG_axis_CORE_signature.csv"))
core_col = "symbol" if "symbol" in core.columns else core.columns[0]
core_syms = set(core[core_col].astype(str).str.upper())
EXTRA = ["SIGMAR1", "CACNA2D1", "P2RX4", "P2RX7", "SCN9A", "KCNK2", "TRPV1", "ASIC3",
         "SCN10A", "SCN11A", "KCNQ2", "GABRA1", "ADRA2A", "CNR2", "OPRM1", "S1PR1"]
extra_in_core = [g for g in EXTRA if g in core_syms]
print(f"§6 优先靶标中落在元分析核心签名里的（作为附加候选）: {extra_in_core}", flush=True)

drh_path = os.path.join(ROOT, "data/raw/druglib/repurposing_drugs.txt")
drug_target_map = {}
drh = pd.read_csv(drh_path, sep="\t", skiprows=9, dtype=str, low_memory=False)
drh.columns = [c.strip() for c in drh.columns]
for _, r in drh.iterrows():
    for t in str(r.get("target", "") or "").split("|"):
        t = t.strip().upper()
        if t:
            drug_target_map.setdefault(t, []).append(
                (r.get("pert_iname"), r.get("clinical_phase"), r.get("moa"), r.get("indication")))
print(f"Drug Repurposing Hub: {len(drh)} 行，覆盖 {len(drug_target_map)} 个人类基因符号", flush=True)

# ---------------------------------------------------------------- 断点续跑
cache = json.load(open(CACHE, encoding="utf-8")) if os.path.exists(CACHE) else {}
symbols = HUB.symbol.tolist() + [g for g in extra_in_core if g not in set(HUB.symbol)]
print(f"待处理 {len(symbols)} 个（已完成 {len(cache)}）", flush=True)


def save(recs):
    T = pd.DataFrame(recs)
    T.to_csv(OUT_CSV, index=False)
    json.dump(cache, open(CACHE, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def classify(kws):
    ks = set(kws)
    if "Kinase" in ks:                                             return "Kinase"
    if "Protease" in ks or "Peptidase" in ks:                      return "Protease"
    if "Protein phosphatase" in ks:                                return "Phosphatase"
    if "Transporter" in ks:                                        return "Transporter"
    if "G-protein coupled receptor" in ks:                         return "GPCR"
    if "Ion channel" in ks:                                        return "Ion channel"
    if "Nuclear receptor" in ks:                                   return "Nuclear receptor"
    if any("Transcription" in k for k in ks):                      return "Transcription factor"
    if ks & {"Enzyme", "Hydrolase", "Transferase", "Oxidoreductase",
             "Lyase", "Isomerase", "Ligase"}:                      return "Enzyme"
    return "Other"


recs = list(cache.values())
for sym in symbols:
    if sym in cache:
        print(f"[skip] {sym}", flush=True)
        continue
    try:
        rec = {"symbol": sym}
        if sym in set(HUB.symbol):
            h = HUB[HUB.symbol == sym].iloc[0]
            rec.update(n_methods=int(h.n_methods), lasso_freq=float(h.lasso_freq),
                       shap_meanabs=float(h.shap_meanabs),
                       in_meta_core=bool(h.in_meta_core), is_hub=True)
        else:
            rec.update(n_methods=np.nan, lasso_freq=np.nan, shap_meanabs=np.nan,
                       in_meta_core=True, is_hub=False, note="§6 优先靶标（核心签名内，非 hub）")

        # R1 UniProt 人源 reviewed
        j = get_json("https://rest.uniprot.org/uniprotkb/search?"
                     f"query=gene_exact:{sym}%20AND%20organism_id:9606%20AND%20reviewed:true"
                     "&fields=accession,protein_name,length,keyword&format=json&size=5")
        acc = pname = plen = None
        kws = []
        if j and j.get("results"):
            r0 = j["results"][0]
            acc = r0.get("primaryAccession")
            pd_ = r0.get("proteinDescription") or {}
            pname = ((pd_.get("recommendedName") or {}).get("fullName") or {}).get("value") \
                or ((pd_.get("submissionNames") or [{}])[0].get("fullName") or {}).get("value")
            plen = r0.get("sequence", {}).get("length")
            kws = [k.get("name") for k in (r0.get("keywords") or [])]
        rec.update(uniprot=acc, protein=pname, length=plen,
                   uniprot_keywords=";".join(kws[:8]))
        if not acc:
            rec.update(decision="EXCLUDE", reason="无人源 reviewed UniProt 条目")
            cache[sym] = rec; recs.append(rec); save(recs)
            print(f"{sym:10s} EXCLUDE   无人源 UniProt", flush=True)
            continue

        rec["target_class"] = classify(kws)

        # 已知已批准药物靶向证据
        hits = drug_target_map.get(sym, [])
        launched = [h for h in hits if str(h[1]).strip() in ("Launched", "Phase 4")]
        rec.update(n_drugs_known=len(hits), n_drugs_launched=len(launched),
                   known_drugs=";".join(sorted({str(h[0]) for h in launched})[:6]),
                   repurposing_hook=bool(launched),
                   known_moa=";".join(sorted({str(h[2]) for h in launched if h[2]})[:3]))

        # R4 ChEMBL 可成药性
        cj = get_json("https://www.ebi.ac.uk/chembl/api/data/target.json?"
                      f"target_components__accession={acc}&limit=1")
        chembl_id, n_act = None, 0
        if cj and cj.get("targets"):
            chembl_id = cj["targets"][0]["target_chembl_id"]
            aj = get_json("https://www.ebi.ac.uk/chembl/api/data/activity.json?"
                          f"target_chembl_id={chembl_id}&limit=1")
            if aj and aj.get("page_meta"):
                n_act = int(aj["page_meta"].get("total_count") or 0)
        rec.update(chembl_target=chembl_id, chembl_n_activities=n_act)

        # R2 结构（RCSB Search）
        # holo_ids 已经过检索侧过滤（nonpolymer_entity_count > 0），可靠；
        # 不再依赖 entry 级 nonpolymer_bound_components（该字段常为 None）。
        holo_ids = rcsb_search(acc, rows=25, only_holo=True)
        all_ids = rcsb_search(acc, rows=25, only_holo=False)
        rec["n_pdb"] = len(all_ids)
        rec["n_pdb_holo"] = len(holo_ids)
        info = {}
        for pid in holo_ids[:6]:
            ei = entry_info(pid)
            if ei:
                info[pid] = ei
        good_ids = [p for p, ei in info.items() if (ei["resolution"] or 99) <= 3.5 and method_ok(ei["method"])]
        good_ids.sort(key=lambda p: info[p]["resolution"] or 99)
        # 若 holo 候选全被分辨率/方法筛掉，再看非 holo 列表里有没有合格结构
        if not good_ids:
            for pid in all_ids[:6]:
                ei = info.get(pid) or entry_info(pid)
                if ei and (ei["resolution"] or 99) <= 3.5 and method_ok(ei["method"]):
                    info[pid] = ei; good_ids.append(pid)
        rec["pdb_candidates"] = ";".join(good_ids[:6])
        if good_ids:
            b = good_ids[0]
            rec.update(pdb_id=b, pdb_resolution=info[b]["resolution"], pdb_method=info[b]["method"],
                       pdb_ligands="|".join(pharma_ligands(info[b]["ligands"])[:8]),
                       pocket_evidence="holo" if b in holo_ids else "apo/none")
        else:
            rec.update(pdb_id=None, pdb_resolution=None, pdb_method=None,
                       pdb_ligands="", pocket_evidence="none")

        # R2 兜底 AlphaFold
        af = get_json(f"https://alphafold.ebi.ac.uk/api/prediction/{acc}")
        afp = af[0].get("globalMetricValue") if (af and isinstance(af, list) and af) else None
        rec["alphafold_plddt"] = afp

        # 决策
        if good_ids and rec["pocket_evidence"] == "holo":
            rec["decision"] = "DOCK"
            rec["reason"] = (f"{rec['target_class']}; PDB {rec['pdb_id']} "
                             f"({rec['pdb_resolution']} Å, {rec['pdb_method']}); 含非聚合物配体；"
                             f"共 {len(good_ids)} 个候选结构")
        elif good_ids:
            rec["decision"] = "HOLD_APO"
            rec["reason"] = (f"{rec['target_class']}; 仅有解析结构 PDB {rec['pdb_id']}"
                             f"({rec['pdb_resolution']} Å)，无配体/配体均为非类药物 → 无法定位对接盒")
        elif afp and afp > 70:
            rec["decision"] = "HOLD_AF2"
            rec["reason"] = (f"{rec['target_class']}; 无合格实验结构 (n_pdb={len(all_ids)}), "
                             f"AF2 pLDDT={afp:.1f}，无共晶配体")
        else:
            rec["decision"] = "EXCLUDE"
            rec["reason"] = f"{rec['target_class']}; 无可用结构 (n_pdb={len(all_ids)}, AF2={afp})"

        cache[sym] = rec
        recs = [cache[k] for k in cache]
        save(recs)
        print(f"{sym:10s} {rec['decision']:9s} {rec['target_class']:20s} {acc:9s} "
              f"PDB={str(rec.get('pdb_id')):5s} res={str(rec.get('pdb_resolution')):5s} "
              f"lig={rec.get('pdb_ligands','')[:22]:22s} ChEMBLact={n_act:6d} "
              f"药={rec['n_drugs_launched']}", flush=True)
    except Exception:
        print(f"{sym:10s} ERROR\n{traceback.format_exc()}", flush=True)
        continue

recs = [cache[k] for k in cache]
T = pd.DataFrame(recs)
save(recs)
print("\n=== 决策汇总 ===")
print(T.decision.value_counts().to_dict())
d = T[T.decision == "DOCK"].sort_values(["n_methods", "lasso_freq"], ascending=False)
print("\n=== DOCK 靶标 ===")
print(d[["symbol", "n_methods", "target_class", "uniprot", "protein", "pdb_id",
         "pdb_resolution", "pdb_ligands", "chembl_n_activities", "n_drugs_launched",
         "known_drugs"]].to_string(index=False))
print("\n表 ->", OUT_CSV)
