#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_score.py -- P6-D：反向阳性对照 + 四维排序

PROJECT_PLAN.md §6 要求两件事，本脚本就是它们的实现：

【反向阳性对照（§6.5，方法学校验必做）】
  把**已知镇痛药-靶点配对**（`PAIN_PRIOR`，以及与本地 Drug Repurposing Hub 的交叉注释）
  当作"阳性探针"投进对接结果里，检验流程能否召回它们：
    · 每个靶标上，已知配对的结合能分位（percentile）
    · 该靶标上"已知配体 vs 其余全部配体"的可分性 **AUC（Mann–Whitney U）**
      AUC≈0.5 → 打分在该靶标上没有区分力，该靶标的排序结果不可信 → 降权
  这不是装饰：它给出**每个靶标结论的可信度权重**。

【四维评分排序（§6.4）】
  D1 结合亲和力：靶标内百分位（越高越强），并统计"多靶点命中广度"
  D2 已有多靶点药理学合理性：该药在 Drug Repurposing Hub 中已注释的靶点与 35 hub 的重叠度
  D3 临床可及性：CNS-MPO 式类药性 + 该药已有神经系统适应症 + 鞘内给药友好度
  D4 反向对照可信度：该靶标的反向对照 AUC（未测到则取中性 0.5）
  综合分 = 0.40·D1 + 0.25·D2 + 0.20·D3 + 0.15·D4（权重写在 W 里，可审计）

产出：results/tables/P6_docking_scores_merged.csv、P6_reverse_control.csv、
      P6_ranking_pairs.csv、P6_ranking_drugs.csv、results/P6_RESULTS.md（由 p6_report.py 生成）
用法：python p6_score.py [--stage 1]
"""
import os, re, json, argparse, glob
import importlib.util          # 必需：下面要用 importlib.util.spec_from_file_location
import numpy as np, pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
OUT = os.path.join(ROOT, "docking/out")   # 逐靶标 scores 源真值目录（自愈重建用）
UA_DRUGS = os.path.join(ROOT, "data/raw/druglib/repurposing_drugs.txt")

W = {"D1_affinity": 0.40, "D2_pharm_prior": 0.25, "D3_accessibility": 0.20, "D4_reliability": 0.15}

# 与 p6_ligands.py 同步的已知镇痛药-靶点标注（反向对照用）
sys_path = os.path.join(ROOT, "scripts")
import importlib.util
spec = importlib.util.spec_from_file_location("ligmod", os.path.join(sys_path, "p6_ligands.py"))
ligmod = importlib.util.module_from_spec(spec)
try:
    spec.loader.exec_module(ligmod)   # 只取常量，main() 不会被调用（有 __main__ guard）
except Exception:
    pass
PAIN_PRIOR = getattr(ligmod, "PAIN_PRIOR", {})


def mann_whitney_auc(pos, neg):
    """AUC = P(pos > neg) + 0.5 P(tie)，用秩公式（含结平处理）"""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    allv = np.concatenate([pos, neg])
    r = pd.Series(allv).rank().to_numpy()
    Rp = r[:len(pos)].sum()
    U = Rp - len(pos) * (len(pos) + 1) / 2.0
    return float(U / (len(pos) * len(neg)))


def _rebuild_tag_table(tg):
    """从 docking/out/<SYM>/scores_<tg>.csv（逐靶标源真值）重建 results/tables/P6_docking_scores_<tg>.csv。

    【为何必须 · 2026-09-19 修复】
    p6_dock.py 写合并表时 `A = concat(rows_all)`，而 rows_all 只含**本次 invocation 实际对接的
    靶标**；用 `--only AXL --tag t1_cns` 做部分重跑时，它会用仅含 AXL 的 ~620 行**覆盖**整层
    合并表，抹掉其余 9 个靶标的 t1 数据。后果：p6_score 在残缺合并表上重排 → 其余 9 靶标的
    t1 排名凭空消失 → 稿件数字基于假数据（且无任何报错，因为"行数变少"不触发异常）。

    逐靶标 scores 文件各自完整（每个靶标只写自己的），拼接即得正确合并表。本函数在读取合并表
    **之前**先自愈重建，彻底杜绝上述失效模式。幂等、可复现；若无任何逐靶标文件则跳过（交还旧逻辑）。
    """
    frames = []
    try:
        subs = sorted(d for d in os.listdir(OUT) if os.path.isdir(os.path.join(OUT, d)))
    except Exception:
        return False
    for sd in subs:
        sp = os.path.join(OUT, sd, f"scores_{tg}.csv")
        if os.path.isfile(sp):
            try:
                d = pd.read_csv(sp)
            except Exception:
                continue
            if "tag" not in d.columns:
                d["tag"] = tg
            frames.append(d)
    if not frames:
        return False
    out = pd.concat(frames, ignore_index=True)
    out.to_csv(os.path.join(TAB, f"P6_docking_scores_{tg}.csv"), index=False)
    print(f"  [rebuild] P6_docking_scores_{tg}.csv <- {len(out):,} 行"
          f"（来自 {len(frames)} 个逐靶标 scores_{tg}.csv 源真值；自愈合并表覆盖缺陷）")
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", type=int, default=1, help="（兼容旧参数）")
    ap.add_argument("--tags", default=None,
                    help="逗号分隔的结果标签，可合并多层；默认 stage<N>。"
                         "分层的动机见 P6_stage1_param_validation：带 --max_evals 的快筛"
                         "排序保真度不足（ρ≈0.1-0.3），只能作探索层。")
    a = ap.parse_args()
    tags = [t.strip() for t in (a.tags or f"stage{a.stage}").split(",") if t.strip()]

    lig = pd.read_csv(os.path.join(TAB, "P6_ligand_library.csv"))
    lig = lig[lig["pass"] == True].copy()
    lig["chembl_id"] = lig.chembl_id.astype(str)
    lig["drug_lc"] = lig.pref_name.astype(str).str.strip().str.lower()
    print(f"配体库（可用）: {len(lig)}")

    parts = []
    for tg in tags:
        _rebuild_tag_table(tg)   # 自愈：用逐靶标源真值重建合并表，避免 --only 部分重跑覆盖掉其它靶标
        fp = os.path.join(TAB, f"P6_docking_scores_{tg}.csv")
        if not os.path.exists(fp):
            print(f"  [warn] 缺 {fp}，跳过"); continue
        _p = pd.read_csv(fp)
        _p["tag"] = tg
        parts.append(_p)
        print(f"  载入 {tg}: {len(_p)} 行")
    sc = pd.concat(parts, ignore_index=True)
    sc["chembl_id"] = sc.chembl_id.astype(str)
    # 同一"靶标-配体"若在多层出现，取**搜索更充分**的那层（max_evals 小者优先）
    if "max_evals" in sc.columns:
        sc["_mep"] = pd.to_numeric(sc["max_evals"], errors="coerce").fillna(0)
        sc = sc.sort_values("_mep").drop_duplicates(["symbol", "chembl_id"], keep="first")
        sc = sc.drop(columns=["_mep"])
    else:
        sc = sc.drop_duplicates(["symbol", "chembl_id"], keep="first")
    print(f"对接打分: {len(sc)} 行，靶标 {sc.symbol.nunique()} 个，配体 {sc.chembl_id.nunique()} 个，层 {sorted(sc.tag.unique())}")

    # 【踩过的坑 · 已修】列清单里**必须含 `drug_lc`**。它在 lig 上于 line 74 建好，
    # 但早期版本漏在 merge 清单外，于是 M/P 里没有该列，d2()/d3() 里的
    # `row.drug_lc` 直接抛 `AttributeError: 'Series' object has no attribute 'drug_lc'`
    # —— 评分器在写完两行表之后就崩。这个 bug 由 _p6_score_selftest.py 在真实对接
    # 跑完前提前捕获（否则要等数小时算力白白耗掉才能暴露）。
    M_all = sc.merge(lig[["chembl_id", "drug_lc", "pref_name", "mw", "logp", "tpsa", "hbd", "hba",
                          "rotb", "charge", "n_torsions", "drh_phase", "drh_moa", "drh_indication",
                          "pain_prior", "atc"]], on="chembl_id", how="left")

    # ---------- 未打分配体（对接失败）：显式剔除 + 留痕 + 上界证明 ----------
    # 【踩过的坑 · 已修 2026-09-19】Tier 2 全库（3,085 配体 × 10 靶标 = 30,850 对）跑完后
    # p6_score 崩在：
    #   ValueError: idxmax with skipna=True encountered all NA values in a group
    # 根因：**有配体在全部 10 个靶标上都对接失败** → 其 composite 全为 NA →
    # `P.groupby("chembl_id").composite.idxmax()` 遇到"整组全 NA"直接抛异常。
    # 这些分子是：
    #   (a) 6 个**含硼药物**（BORTEZOMIB / IXAZOMIB CITRATE / TAVABOROLE / CRISABOROLE /
    #       VABORBACTAM / BORTEZOMIB D-MANNITOL）—— Vina 的 PDBQT 解析器不认原子类型 `B`
    #       （"Atom type B is not a valid AutoDock type"），**与靶标无关**，故 10 个靶标全败；
    #   (b) 若干 600 s 超时的大环/高柔性分子（紫杉烷、大环内酯、长春碱类等）。
    # Tier 1 只有 620 个配体时恰好一个都不含，所以该缺陷**只在广度跑完后才暴露**——
    # 这是"广度会暴露单层看不见的失效模式"的又一次应验。
    # 正确处理不是打补丁绕过异常，而是**显式剔除 + 留痕 + 证明剔除不影响结论**：
    # ① 剔除只发生在已打分对上算分（NaN 不参与 rank，百分位分母用实际打分对数）；
    # ② 全部失败对写入 P6_ligands_unscored.csv（含原因分类）；
    # ③ 见下方"剔除影响上界证明"——用同一套 D2/D3/D4 公式证明这些对**不可能**进入 Top-K。
    M_all["scored"] = M_all.affinity.notna()
    M = M_all[M_all.scored].copy()
    zero_cov = sorted(set(M_all.chembl_id) - set(M.chembl_id))

    def _why(e):
        e = str(e)
        if "not a valid AutoDock type" in e:
            return "unsupported_atom_type_B（含硼药物，Vina 无法解析）"
        if "TIMEOUT" in e.upper():
            return "timeout_600s（大环/高柔性分子）"
        return "other：" + e[:80]

    UNSC = (M_all[~M_all.scored]
            .assign(reason=lambda d: d.err.map(_why))
            [["symbol", "chembl_id", "pref_name", "drug_lc", "mw", "logp", "tpsa", "hbd", "rotb",
              "tag", "rc", "sec", "reason"]]
            .reset_index(drop=True))
    UNSC.to_csv(os.path.join(TAB, "P6_ligands_unscored.csv"), index=False)
    print(f"\n未打分（对接失败）：{len(UNSC)} 个 靶标×配体（{UNSC.chembl_id.nunique()} 个配体），"
          f"占全部 {len(M_all)} 对的 {len(UNSC)/max(len(M_all),1):.3%}")
    print(UNSC.reason.value_counts().to_string())
    print(f"  在**全部**靶标上都未打分的配体：{len(zero_cov)} 个 → {zero_cov}")
    print("  → 明细见 results/tables/P6_ligands_unscored.csv（评分只用已打分对）")

    # 靶标内百分位（affinity 越负越好 → 用 -affinity 排序，越大越好）。
    # 分母必须是**该靶标实际打分的配体数**，不能用"尝试数"——把失败对算进分母会虚增 n，
    # 也会让"配体组成受控"的跨靶标比较失真（GALNS/SLC2A1/TNIK 各有 15–21 个失败对）。
    M["neg_aff"] = -M.affinity
    M["pct_in_target"] = M.groupby("symbol").neg_aff.rank(pct=True) * 100.0
    M["n_ligands_target"] = M.groupby("symbol").chembl_id.transform("nunique")
    M["z_in_target"] = M.groupby("symbol").neg_aff.transform(
        lambda x: (x - x.mean()) / (x.std(ddof=0) + 1e-9))
    # 回填到全表（失败行保持 NaN），保留未打分行的可追溯性
    M_all = M_all.merge(M[["symbol", "chembl_id", "neg_aff", "pct_in_target",
                           "n_ligands_target", "z_in_target"]],
                        on=["symbol", "chembl_id"], how="left")
    M_all.to_csv(os.path.join(TAB, "P6_docking_scores_merged.csv"), index=False)
    M.groupby("tag").affinity.describe()[["count", "min", "50%"]].to_csv(
        os.path.join(TAB, "P6_docking_scores_merged_by_tag.csv"))
    print(f"  各靶标实际打分配体数：{M.groupby('symbol').chembl_id.nunique().to_dict()}")

    # ---------- 反向阳性对照 ----------
    docked_targets = set(M.symbol.str.upper())
    known_pairs = []   # (chembl_id, symbol)
    name2cid = dict(zip(lig.drug_lc, lig.chembl_id))
    for drug, tgts in PAIN_PRIOR.items():
        cid = name2cid.get(drug.strip().lower())
        if not cid:
            continue
        for t in tgts:
            if t.upper() in docked_targets:
                known_pairs.append((cid, t.upper()))
    # 再补一层：Drug Repurposing Hub 里已注明靶向该靶标的已批准药物
    # 【踩过的坑 · 已修】旧条件写成 `if t in docked_targets and t not in hub`。
    # 但 10 个可对接靶标里有 **9 个本身就是 hub 基因**（只有 ADRA2A 不是），
    # 因此该条件把 DRH 层阳性配对**几乎全部滤掉** → 反向对照退化为"只有 PAIN_PRIOR
    # 一层"，且仅对 ADRA2A 有 DRH 阳性 → 根本不足以校验流程（"对照悄悄没有阳性"）。
    # 阳性配对的定义里没有任何理由排除 hub 靶标，故去掉该子句。
    # `hub` 仍保留：D2 维度要用它算药物注释靶点与 hub 的重叠度。
    hub = set(pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv")).symbol.str.upper())
    drh = pd.read_csv(UA_DRUGS, sep="\t", skiprows=9, dtype=str, low_memory=False)
    drh.columns = [c.strip() for c in drh.columns]
    for _, r in drh.iterrows():
        nm = str(r.get("pert_iname", "") or "").strip().lower()
        cid = name2cid.get(nm)
        if not cid:
            continue
        for t in str(r.get("target", "") or "").split("|"):
            t = t.strip().upper()
            if t in docked_targets:
                known_pairs.append((cid, t))
    # 第三层（**主用**）：ChEMBL 实测活性阳性集，由 scripts/p6_reverse_control.py 生成。
    #
    # 【重要口径决策 · 2026-09-19】反向对照测的是「对接打分能否区分**真正结合**该靶标的
    # 分子」，因此标签必须是**结合型**（实测 IC50/Kd/Ki ≤ 1 µM），不能掺入**适应症/注释型**
    # 标签（PAIN_PRIOR 记的是"这药是已知镇痛药"，DRH target 字段记的是"注释靶点"）。
    # 两类标签回答的是不同问题；把后者混进结合富集检验会引入标签噪声、稀释信号 ——
    # 实测 ADRA2A：纯 ChEMBL n=88 → AUC 0.618；掺入 DRH(+11)/PAIN_PRIOR(+2) 后
    # n=101 → AUC 0.592。故只要 ChEMBL 表可用，就**只用它**，保证定义单一、客观、可复现。
    # 只有当 ChEMBL 表不存在时才降级使用前两层（并在下方打印明确告警）。
    rcp_fp = os.path.join(TAB, "P6_reverse_control_positives.csv")
    n_before = len(set(known_pairs))
    chembl_mode = False
    if os.path.exists(rcp_fp):
        try:
            RCP = pd.read_csv(rcp_fp)
            chembl_pairs = []
            for _, r_ in RCP.iterrows():
                t = str(r_.symbol).upper()
                if t in docked_targets:
                    chembl_pairs.append((str(r_["chembl_id"]), t))
            if chembl_pairs:
                known_pairs = chembl_pairs          # 替换为纯 ChEMBL 口径
                chembl_mode = True
                print(f"  反向对照标签 = 纯 ChEMBL 实测活性（pChEMBL≥6）：{len(set(known_pairs))} 条配对"
                      f"（已弃用 PAIN_PRIOR/DRH 注释层 {n_before} 条：适应症型标签会稀释结合信号）")
            else:
                print("  [warn] ChEMBL 阳性表为空，降级使用前两层")
        except Exception as e:
            print(f"  [warn] ChEMBL 阳性表读取失败，跳过该层: {type(e).__name__}: {e}")
    else:
        print("  [warn] 无 ChEMBL 阳性表，降级使用前两层：PAIN_PRIOR + DRH 靶点注释"
              "（此时标签为适应症/注释型，AUC 不可与 ChEMBL 口径直接比较）")

    known_pairs = sorted(set(known_pairs))
    print(f"已知药-靶阳性配对（两端都在库内）: {len(known_pairs)}")

    rev = []
    for sym, g in M.groupby("symbol"):
        pos_cids = {c for c, t in known_pairs if t == sym.upper()}
        gp = g[g.chembl_id.isin(pos_cids)]
        gn = g[~g.chembl_id.isin(pos_cids)]
        auc = mann_whitney_auc(gp.neg_aff.values, gn.neg_aff.values) if len(gp) else np.nan
        rev.append({"symbol": sym, "n_known_pairs": int(len(gp)),
                    "n_ligands": int(g.chembl_id.nunique()),
                    "known_median_aff": float(gp.affinity.median()) if len(gp) else np.nan,
                    "all_median_aff": float(gn.affinity.median()) if len(gn) else np.nan,
                    "known_median_pct": float(gp.pct_in_target.median()) if len(gp) else np.nan,
                    "auc_known_vs_rest": auc,
                    "reliable": bool((auc is not None) and (not np.isnan(auc)) and auc >= 0.60)
                                if len(gp) >= 3 else None,
                    "known_drugs": ";".join(sorted(set(gp.pref_name.astype(str)))[:8])})
    REV = pd.DataFrame(rev)
    # `reliable` 为 True/False/None（None = 阳性数太少未评估）三态混排，object dtype
    # 排序在 None 与 bool 之间比较不可靠；用显式布尔键把"未评估"稳定排到最后，
    # 同时保留原三态列不变。
    REV["_rel_sort"] = (REV.reliable == True).astype(bool)
    REV = (REV.sort_values(["_rel_sort", "auc_known_vs_rest"], ascending=[False, False])
              .drop(columns=["_rel_sort"]))
    REV.to_csv(os.path.join(TAB, "P6_reverse_control.csv"), index=False)
    print("\n=== 反向阳性对照（逐靶标）===")
    print(REV[["symbol", "n_known_pairs", "known_median_aff", "all_median_aff",
               "known_median_pct", "auc_known_vs_rest", "reliable"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    auc_map = dict(zip(REV.symbol, REV.auc_known_vs_rest.fillna(0.5)))

    # ---------- 四维评分 ----------
    P = M.copy()
    P["D1_affinity"] = P.pct_in_target / 100.0

    # D2：药理学合理性 —— DRH 注释靶点与 35 hub 的重叠
    name2tgts = {}
    for _, r in drh.iterrows():
        nm = str(r.get("pert_iname", "") or "").strip().lower()
        tv = r.get("target", "")
        # 注意 NA：`nan or ""` 里 nan 是**真值**，会被 str() 成 "nan" → 产出假靶标 "NAN"。
        # 必须先判 NA 再切分。
        tv = "" if pd.isna(tv) else str(tv)
        name2tgts[nm] = {t.strip().upper() for t in tv.split("|") if t.strip()}
    # 【踩过的坑 · 已修】DRH 表里 disease_area / indication 有大量空值（indication 缺 4,576 行）。
    # 在 pandas 3.x 下 `read_csv(dtype=str)` 得到的是新的 `str`(StringDtype)；
    # 此时 **`.astype(str)` 是空操作、会原样保留 NA**（而旧 object dtype 下 NaN 会被
    # 转成字符串 "nan"）。于是 name2ind 里 4,576 个值是 float nan，
    # `any(k in ind ...)` 抛 `TypeError: argument of type 'float' is not iterable`。
    # d3 里的 `"neurology" in area` 是同一个雷。统一用 `.fillna("")` 显式补空串。
    def _txt(s):
        """把可能含 NA 的列安全地变成小写字符串（NA → ""）。"""
        return s.fillna("").astype(str).str.strip().str.lower()

    name2area = dict(zip(_txt(drh.pert_iname), _txt(drh.disease_area)))
    name2ind = dict(zip(_txt(drh.pert_iname), _txt(drh.indication)))
    PAINKW = ("pain", "neuralgia", "neuropath", "migraine", "fibromyalgia", "analges")

    def d2(row):
        tg = name2tgts.get(row.drug_lc, set())
        ov = len(tg & hub)
        s = 0.0
        s += min(ov, 3) / 3.0 * 0.6                      # hub 重叠（最多 3 个记满分）
        if row.symbol.upper() in tg:
            s += 0.4                                     # 该药已知作用于本靶标
        ind = str(name2ind.get(row.drug_lc, "") or "")
        if any(k in ind for k in PAINKW):
            s = min(1.0, s + 0.2)
        return min(s, 1.0)

    P["D2_pharm_prior"] = P.apply(d2, axis=1)

    # D3：临床可及性（CNS-MPO 式 5 项 + 神经系统适应症 + 鞘内友好度）
    def d3(row):
        # 注意：不要写 `row.tpsa is not np.nan` —— `is` 比较的是对象身份，
        # `np.nan is not np.nan` 恒为 True，该判断完全失效（旧写法靠
        # `NaN <= 90 == False` 侥幸没出错）。用 pd.notna() 明确表达意图。
        s = 0.0
        s += 1 if (pd.notna(row.tpsa) and row.tpsa <= 90) else 0
        s += 1 if (pd.notna(row.mw) and row.mw <= 450) else 0
        s += 1 if (pd.notna(row.logp) and 1.0 <= row.logp <= 4.0) else 0
        s += 1 if (pd.notna(row.hbd) and row.hbd <= 3) else 0
        s += 1 if (pd.notna(row.rotb) and row.rotb <= 8) else 0
        base = s / 5.0
        area = str(name2area.get(row.drug_lc, "") or "")
        if "neurology" in area or "psychiatry" in area:
            base = min(1.0, base + 0.15)
        if pd.notna(row.mw) and row.mw < 400 and pd.notna(row.tpsa) and row.tpsa < 70:
            base = min(1.0, base + 0.10)      # 鞘内给药友好（小、极性适中）
        return base

    P["D3_accessibility"] = P.apply(d3, axis=1)
    P["D4_reliability"] = P.symbol.map(lambda s: auc_map.get(s, 0.5))
    P["D4_reliability"] = P.D4_reliability.fillna(0.5)
    P["composite"] = (W["D1_affinity"] * P.D1_affinity + W["D2_pharm_prior"] * P.D2_pharm_prior +
                      W["D3_accessibility"] * P.D3_accessibility + W["D4_reliability"] * P.D4_reliability)

    # ---------- 剔除影响上界证明（exclusion bound） ----------
    # 对每个"未打分对"，用**完全相同的 D2/D3/D4 公式**算 D1 取满 (=1.0) 时的最大可能复合分。
    # 若全部上界都低于实际 Top-K 门槛，则"剔除不影响 Top-K 名单"是**可证的**，
    # 而不是"失败率只有 0.53% 所以无妨"这类托辞。比单报失败率强得多。
    if len(UNSC):
        UB = UNSC.copy()
        UB["D1_affinity"] = 1.0
        UB["D2_pharm_prior"] = UB.apply(d2, axis=1)
        UB["D3_accessibility"] = UB.apply(d3, axis=1)
        UB["D4_reliability"] = UB.symbol.map(lambda s: auc_map.get(s, 0.5)).fillna(0.5)
        UB["composite_upper_bound"] = (W["D1_affinity"] * UB.D1_affinity +
                                       W["D2_pharm_prior"] * UB.D2_pharm_prior +
                                       W["D3_accessibility"] * UB.D3_accessibility +
                                       W["D4_reliability"] * UB.D4_reliability)
        Psort = P.composite.dropna().sort_values(ascending=False).reset_index(drop=True)
        _thr = {k: (float(Psort.iloc[k - 1]) if len(Psort) >= k else float("nan"))
                for k in (10, 20, 50, 100)}
        UB["top_k_threshold_top20"] = _thr[20]
        UB["exceeds_top20_bound"] = UB.composite_upper_bound >= _thr[20]
        UB = UB.sort_values("composite_upper_bound", ascending=False)
        UB.to_csv(os.path.join(TAB, "P6_exclusion_bound.csv"), index=False)
        print("\n=== 剔除影响上界证明（D1 取满时的最大可能复合分）===")
        print(f"  实际门槛：Top-10 {_thr[10]:.4f} | Top-20 {_thr[20]:.4f} | "
              f"Top-50 {_thr[50]:.4f} | Top-100 {_thr[100]:.4f}")
        print(f"  未打分对的复合分上界最大值 = {UB.composite_upper_bound.max():.4f}"
              f"（{UB.iloc[0].chembl_id} @ {UB.iloc[0].symbol}）")
        _n20 = int(UB.exceeds_top20_bound.sum())
        print(f"  上界达到/超过 Top-20 门槛的未打分对：{_n20} / {len(UB)}"
              f"{'  → 剔除不影响 Top-20（可证）' if _n20 == 0 else '  → ⚠ 需逐例讨论'}")
    P["in_top1pct"] = P.pct_in_target >= 99.0
    P["in_top5pct"] = P.pct_in_target >= 95.0
    P = P.sort_values(["composite"], ascending=False)
    P.to_csv(os.path.join(TAB, "P6_ranking_pairs.csv"), index=False)

    # 药物级汇总：多靶点广度
    # 【踩过的坑 · 已修】药物级表原先只输出 `D2`/`D3` 两个聚合列，既没有 D1/D4，
    # 也没有 p6_figures.fig_ranking 期望的 `D1_affinity`/`D2_pharm_prior`/`D3_accessibility`/
    # `D4_reliability` ⇒ 堆叠条形图**四段一段都画不出来**，只留一张空白图 + 一句
    # "No artists with labels found" 告警（该告警很容易被当成无害噪音忽略）。
    # 修法：直接取每个药物**最佳配对**那一行的四维值 —— 这样四段之和**恰好等于**
    # best_composite，图上可核验；而"各维分别取 max"会取自不同靶标，四段之和对不上总分，
    # 属于会骗人的画法。
    # 【踩过的坑 · 已在源头修复】上游已把"全靶标失败"的配体剔除，理论上不再有整组全 NA。
    # 此处再挡一道：`groupby(...).idxmax()` 对"整组全 NA"会抛
    # ValueError（skipna=True encountered all NA values in a group），
    # 而它抛出的位置在**药物级汇总**，前面已经写了两张表 → 看起来像"部分成功"，
    # 极容易被漏看。显式 dropna + 告警，把静默失败变成响亮失败。
    Pn = P.dropna(subset=["composite"])
    _n_drop = P.chembl_id.nunique() - Pn.chembl_id.nunique()
    if _n_drop:
        print(f"  [warn] 仍有 {_n_drop} 个配体复合分全为 NA，药物级汇总不含它们（见 P6_ligands_unscored.csv）")
    bi = Pn.groupby("chembl_id").composite.idxmax()
    BEST = (Pn.loc[bi, ["chembl_id", "symbol", "affinity", "pct_in_target", "D1_affinity",
                       "D2_pharm_prior", "D3_accessibility", "D4_reliability", "composite"]]
            .rename(columns={"symbol": "best_target", "composite": "best_composite",
                             "pct_in_target": "best_pct_in_target",
                             # 关键：这是「best_target 这一对」的亲和力，与 best_target 严格配对。
                             # 另有一个跨所有靶标取最小的 best_affinity_any_target（见下），
                             # 二者通常不相等 —— 曾在稿件中把后者误标到前者名下（张冠李戴），此处拆开。
                             "affinity": "affinity_at_best_target"}))

    D = P.groupby(["chembl_id", "pref_name"], dropna=False).agg(
        n_targets=("symbol", "nunique"),
        n_top1pct=("in_top1pct", "sum"),
        n_top5pct=("in_top5pct", "sum"),
        mean_composite=("composite", "mean"),
        # 注意语义：这是该药物在**任意靶标**上的最强亲和力（跨靶标取 min），
        # 其所属靶标**未必**是 best_target。引用时必须与 affinity_at_best_target 区分，
        # 否则会把 A 靶标的亲和力标到 B 靶标名下（Top20 中 19/20 会踩这个坑）。
        best_affinity_any_target=("affinity", "min"),
        med_affinity=("affinity", "median"),
        pain_prior=("pain_prior", "first"),
        drh_phase=("drh_phase", "first"), drh_moa=("drh_moa", "first"),
        drh_indication=("drh_indication", "first"),
        mw=("mw", "first"), logp=("logp", "first"), tpsa=("tpsa", "first"),
    ).reset_index().merge(BEST, on="chembl_id", how="left")
    # 堆叠图可核验：四段加权和应当等于 best_composite
    D["sum_check"] = (W["D1_affinity"] * D.D1_affinity + W["D2_pharm_prior"] * D.D2_pharm_prior +
                      W["D3_accessibility"] * D.D3_accessibility + W["D4_reliability"] * D.D4_reliability)
    _dev = (D.sum_check - D.best_composite).abs().max()
    if not (_dev < 1e-9):
        print(f"  [warn] 四维分解之和与 best_composite 最大偏差 {_dev:.2e}（应为 0）")
    # 广度加权：命中多个 hub 靶标者上调
    D["breadth_bonus"] = np.log1p(D.n_top5pct) / np.log1p(P.symbol.nunique())
    D["drug_rank_score"] = 0.75 * D.best_composite + 0.25 * D.breadth_bonus
    D = D.sort_values("drug_rank_score", ascending=False)
    D.to_csv(os.path.join(TAB, "P6_ranking_drugs.csv"), index=False)

    print("\n=== Top 20 药物（四维排序）===")
    print(D.head(20)[["pref_name", "best_target", "affinity_at_best_target",
                      "best_affinity_any_target", "n_top1pct", "n_top5pct",
                      "best_composite", "D2_pharm_prior", "D3_accessibility", "pain_prior", "drh_phase"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print("\n=== Top 20 药物-靶标配对 ===")
    print(P.head(20)[["pref_name", "symbol", "affinity", "pct_in_target", "D1_affinity",
                      "D2_pharm_prior", "D3_accessibility", "D4_reliability", "composite"]]
          .to_string(index=False, float_format=lambda v: f"{v:.3f}"))
    print("\n表 -> P6_ranking_pairs.csv / P6_ranking_drugs.csv / P6_reverse_control.csv")


if __name__ == "__main__":
    main()
