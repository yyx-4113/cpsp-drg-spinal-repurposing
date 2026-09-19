#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p5_summarize.py -- P5 hub 定位结果整合与假信号剔除

主流程 p5_sc.py 的 "top celltype" 有五个已知陷阱，本脚本逐条修补：

  (1) **除零假象**：CDHR5 全数据几乎不表达（top_mean=1.4e-3），却因分母趋零得到
      specificity=197 → 改用 log2 富集 + **可定位性门槛**。
  (2) **文库复杂度混杂**（最关键）：log-normalized 均值随该细胞类型的检出基因数
      系统性升高（神经元核 ~6400 基因 vs 少突胶质核 ~1500 基因）。ATF3 在 DRG 里
      Schwann=1.030 / Neuron=1.029 几乎相同，若只比均值会把它判成 Schwann 特异。
      → 必须 **均值富集与检出率富集同时达标** 才算"特异"，并把结论降级为
        restricted / enriched / broad / undetected / rare_compartment / ambient_caution。
  (3) **小簇伪影 vs 稀有区室**：Endothelial 只有 31/43 个核，噪声易夺冠；但 SLC2A1
      的真信号恰恰就在内皮。→ 不把小簇踢出候选，而是**保留指派并标为 rare_compartment**，
      交由下游按需采信（既不冤枉真信号，也不让噪声冒充主结论）。
  (4) **环境 RNA（ambient RNA）**：ATF3 在脊髓 snRNA 里 ambient_index=2.59
      （最空的 10% 细胞比全局高 2.6 倍）→ 该基因的细胞归属不可采信，单列降级。
  (5) **血液污染簇**：Erythrocyte（HBB/HBA）不参与候选，避免 MAPK14 这类管家基因
      被红细胞的深度差异带走。

输出：
  results/tables/P5_hub_localisation_summary.csv   逐 hub × 逐数据集 定位明细（含全部诊断列）
  results/tables/P5_hub_localisation_dropped.csv   被降级/剔除的 hub 及其原因（可审计）
  results/tables/P5_hub_lineage_consensus.csv      跨数据集谱系一致性（主结论表）
  results/figures/P5_hub_lineage_consensus.png     谱系定位热图 + 一致性条形图

用法: python p5_summarize.py
"""
import os, glob, re
import numpy as np, pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB, FIG = os.path.join(ROOT, "results/tables"), os.path.join(ROOT, "results/figures")
EPS = 1e-3

# 阈值（先验设定，不随数据调参）
MIN_TOP_MEAN   = 0.05    # top 细胞类型的 log-norm 均值下限
MIN_TOP_PCT    = 0.05    # top 细胞类型的检出率下限
ENR_MEAN_RESTR = 1.00    # >=2.0 倍 均值富集
ENR_MEAN_ENR   = 0.58    # >=1.5 倍 均值富集
ENR_PCT_RESTR  = 0.58    # 检出率富集须同时 >=1.5 倍
AMBIENT_MAX    = 1.50    # ambient_index 上限

LINEAGE = {
    "Neuron": "Neuronal", "Injured_RegenNeuron": "Neuronal", "Peptidergic_Nociceptor": "Neuronal",
    "NonPeptidergic_Noci": "Neuronal", "Myelinated_Proprio": "Neuronal",
    "SatelliteGlia": "Glial", "Schwann": "Glial", "Astrocyte": "Glial",
    "Oligodendrocyte": "Glial", "OPC": "Glial", "Ependymal": "Glial",
    "Immune": "Immune", "Microglia": "Immune",
    "Endothelial": "Vascular_Stroma", "Pericyte": "Vascular_Stroma", "Pericyte_VSMC": "Vascular_Stroma",
    "Fibroblast": "Vascular_Stroma", "Fibroblast_Meninges": "Vascular_Stroma",
    "Erythrocyte": "Blood_contaminant",
}
EXCLUDE_CELLTYPES = {"Erythrocyte"}
# 只让"横跨多个谱系"的数据集参与共识；Cd11b+ 小胶质专用数据集的定位几乎必然为 Immune，
# 纳入共识会人为制造 Mixed（假不一致）-> 单独做描述性分析。
CONSENSUS_DATASETS = {"GSE216039", "GSE328175"}
DATASET_LABEL = {
    "GSE216039_DRG":        ("GSE216039", "DRG",         "CCI-7d vs Sham · Pirt-EGFP FACS 神经元富集 scRNA"),
    "GSE328175_SC_ShamSNI": ("GSE328175", "SpinalCord",   "SNI vs Sham · L4-6 腰段脊髓 FANS snRNA"),
    "GSE246288_SC":         ("GSE246288", "SpinalCord",   "SNI PID0/3/7/14 · Cd11b+ 背角小胶质 scRNA（描述性）"),
}

hubdf = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
hubdf["symbol"] = hubdf["symbol"].str.upper()
nm = dict(zip(hubdf.symbol, hubdf.n_methods))
hub_order = hubdf.sort_values(["n_methods", "symbol"], ascending=[False, True]).symbol.tolist()


def complexity_map(tag):
    p = os.path.join(TAB, f"P5_{tag}_cellmeta.csv.gz")
    if not os.path.exists(p):
        return {}
    cm = pd.read_csv(p)
    if "n_genes" not in cm.columns or "celltype" not in cm.columns:
        return {}
    return cm.groupby("celltype")["n_genes"].median().to_dict()


rows, notes = [], []
for f in sorted(glob.glob(os.path.join(TAB, "P5_*_hub_localisation.csv"))):
    tag = re.search(r"P5_(.+)_hub_localisation\.csv", os.path.basename(f)).group(1)
    loc = pd.read_csv(f)
    loc["symbol"] = loc["symbol"].str.upper()
    ct_size = loc.groupby("celltype")["n_cells"].first()
    N = int(ct_size.sum())
    min_cells = max(50, int(0.0025 * N))
    cand = set(ct_size.index) - EXCLUDE_CELLTYPES
    rare = set(ct_size[ct_size < min_cells].index) & cand
    cplx = complexity_map(tag)
    glob_med = np.median(list(cplx.values())) if cplx else np.nan
    notes.append(f"{tag}: N={N}, rare_threshold={min_cells} cells -> rare compartments {sorted(rare)}; "
                 f"median_n_genes_by_ct={ {k: int(v) for k, v in sorted(cplx.items())} }")

    for g, s in loc.groupby("symbol"):
        sel = s[s.celltype.isin(cand)].sort_values("mean_lognorm", ascending=False)
        if sel.empty:
            continue
        top, oth = sel.iloc[0], sel.iloc[1:]
        top_mean, top_pct = float(top.mean_lognorm), float(top.pct_expressing)
        top_n = int(top.n_cells)
        oth_mean = float(oth.mean_lognorm.mean()) if len(oth) else 0.0
        oth_pct = float(oth.pct_expressing.mean()) if len(oth) else 0.0
        enr_mean = float(np.log2((top_mean + EPS) / (oth_mean + EPS)))
        enr_pct = float(np.log2((top_pct + EPS) / (oth_pct + EPS)))
        amb = float(top.ambient_index)
        if top_mean <= MIN_TOP_MEAN or top_pct < MIN_TOP_PCT:
            tier = "undetected"
        elif top_n < min_cells:
            tier = "rare_compartment"
        elif amb > AMBIENT_MAX:
            tier = "ambient_caution"
        elif enr_mean >= ENR_MEAN_RESTR and enr_pct >= ENR_PCT_RESTR:
            tier = "restricted"
        elif enr_mean >= ENR_MEAN_ENR:
            tier = "enriched"
        else:
            tier = "broad"
        rows.append({
            "dataset_tag": tag,
            "dataset": DATASET_LABEL.get(tag, (tag, "", ""))[0],
            "tissue": DATASET_LABEL.get(tag, ("", tag, ""))[1],
            "in_consensus_set": DATASET_LABEL.get(tag, (tag,))[0] in CONSENSUS_DATASETS,
            "n_methods": nm.get(g, np.nan), "symbol": g,
            "overall_pct": round(float(s.pct_expressing_allcells.iloc[0]), 4),
            "max_mean": round(top_mean, 4),
            "localisable": bool(tier in ("restricted", "enriched")), "tier": tier,
            "top_celltype": top.celltype, "top_lineage": LINEAGE.get(top.celltype, "NA"),
            "top_n_cells": top_n, "top_pct": round(top_pct, 3),
            "log2_enrich_mean": round(enr_mean, 2), "log2_enrich_pct": round(enr_pct, 2),
            "ambient_index": round(amb, 3),
            "top_ct_median_n_genes": (int(cplx[top.celltype]) if top.celltype in cplx else np.nan),
            "global_median_n_genes": (int(glob_med) if pd.notna(glob_med) else np.nan),
            "n_candidates": len(sel),
        })
S = pd.DataFrame(rows)
S.to_csv(os.path.join(TAB, "P5_hub_localisation_summary.csv"), index=False)
print("\n".join(notes))
print(f"\nsummary rows: {len(S)}")
print("tier counts: " + str(S.tier.value_counts().to_dict()))

drop = S[~S.localisable].sort_values(["dataset", "tier", "n_methods"], ascending=[True, True, False])
drop[["dataset", "symbol", "n_methods", "tier", "top_celltype", "top_n_cells",
      "max_mean", "top_pct", "log2_enrich_mean", "log2_enrich_pct", "ambient_index"]].to_csv(
    os.path.join(TAB, "P5_hub_localisation_dropped.csv"), index=False)
print(f"dropped/降级明细 -> results/tables/P5_hub_localisation_dropped.csv ({len(drop)} 行)")

# ---- 跨数据集谱系一致性（仅横跨多谱系的数据集） ----
L = S[S.localisable & S.in_consensus_set]
cons = L.pivot_table(index="symbol", columns="dataset", values="top_lineage", aggfunc="first").reindex(hub_order)
agg = L.groupby("symbol").agg(
    n_datasets=("dataset", "nunique"),
    lineages=("top_lineage", lambda x: "|".join(sorted(set(x)))),
    celltypes=("top_celltype", lambda x: "|".join(sorted(set(x)))),
    mean_enrich=("log2_enrich_mean", "mean"),
    tiers=("tier", lambda x: "|".join(sorted(set(x)))),
).reindex(hub_order).reset_index()
agg["n_methods"] = agg.symbol.map(nm)
agg["consensus_lineage"] = [
    ("Mixed" if len(set(str(v).split("|"))) > 1 else str(v).split("|")[0]) if pd.notna(v)
    else "NotLocalisable" for v in agg.lineages]
agg["confident"] = (agg.n_datasets >= 2) & (~agg.consensus_lineage.isin(["Mixed", "NotLocalisable"]))
agg = agg[["symbol", "n_methods", "n_datasets", "celltypes", "consensus_lineage",
           "confident", "mean_enrich", "tiers", "lineages"]]
agg.to_csv(os.path.join(TAB, "P5_hub_lineage_consensus.csv"), index=False)
print("\n=== lineage consensus ===")
print(agg[["symbol", "n_methods", "n_datasets", "celltypes", "consensus_lineage", "confident", "mean_enrich"]]
      .to_string(index=False))
print("\nconsensus counts: " + str(agg.consensus_lineage.value_counts().to_dict()))
print("confident (>=2 datasets, 同谱系): " + str(agg[agg.confident].consensus_lineage.value_counts().to_dict()))
print("confident genes: " + str(agg[agg.confident].symbol.tolist()))
print("not resolved in any dataset: " + str(agg[agg.consensus_lineage == "NotLocalisable"].symbol.tolist()))

# ---- 图 ----
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
dshow = [d for d in dict.fromkeys(S.dataset.tolist()) if d in CONSENSUS_DATASETS]
fig, axes = plt.subplots(1, 2, figsize=(13.5, 9.5), gridspec_kw={"width_ratios": [1, 1.35]})
ax = axes[0]
lin_order = ["Neuronal", "Glial", "Immune", "Vascular_Stroma", "NotLocalisable"]
M = np.full((len(hub_order), len(dshow)), np.nan)
for i, g in enumerate(hub_order):
    for j, d in enumerate(dshow):
        v = S[(S.symbol == g) & (S.dataset == d)]
        M[i, j] = (lin_order.index(v.top_lineage.iloc[0]) if (len(v) and v.localisable.iloc[0])
                   else lin_order.index("NotLocalisable")) if len(v) else np.nan
cmap = matplotlib.colors.ListedColormap(["#C44E52", "#4C72B0", "#55A868", "#8172B2", "#FFFFFF"])
ax.imshow(M, aspect="auto", cmap=cmap, vmin=-0.5, vmax=4.5)
ax.set_xticks(range(len(dshow)))
ax.set_xticklabels([f"{d}\n({DATASET_LABEL[[k for k, v in DATASET_LABEL.items() if v[0] == d][0]][1]})"
                    for d in dshow], rotation=12, fontsize=8)
ax.set_yticks(range(len(hub_order)))
ax.set_yticklabels([f"{g} ({int(nm[g])})" for g in hub_order], fontsize=7)
nconf = int(agg.confident.sum())
ax.set_title("A  hub top lineage per dataset (white = not localisable)\n"
             f"bold gene names = same lineage in both datasets  ({nconf}/{len(hub_order)})", fontsize=10)
for i, g in enumerate(hub_order):
    if agg.loc[agg.symbol == g, "confident"].iloc[0]:
        ax.get_yticklabels()[i].set_fontweight("bold")
for i in range(len(hub_order)):
    for j in range(len(dshow)):
        if np.isnan(M[i, j]):
            ax.text(j, i, "n/a", ha="center", va="center", fontsize=5, color="#999")
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in ["#C44E52", "#4C72B0", "#55A868", "#8172B2", "#FFFFFF"]]
ax.legend(handles, lin_order, fontsize=7, bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)

ax = axes[1]
vc = agg.consensus_lineage.value_counts()
colors = {"Neuronal": "#C44E52", "Glial": "#4C72B0", "Immune": "#55A868",
          "Vascular_Stroma": "#8172B2", "Mixed": "#CCB974", "NotLocalisable": "#CCCCCC"}
ax.barh(range(len(vc)), vc.values, color=[colors.get(k, "#999") for k in vc.index])
ax.set_yticks(range(len(vc))); ax.set_yticklabels(vc.index, fontsize=9); ax.invert_yaxis()
ax.set_xlabel("n hub genes"); ax.set_title("B  consensus lineage (DRG + spinal cord snRNA)", fontsize=10)
for i, v in enumerate(vc.values):
    ax.text(v + 0.15, i, str(v), va="center", fontsize=9)
ax.text(0.98, 0.02, f"same lineage in both datasets: {nconf}/{len(hub_order)}",
        transform=ax.transAxes, ha="right", va="bottom", fontsize=8, color="#444")
plt.tight_layout()
out = os.path.join(FIG, "P5_hub_lineage_consensus.png")
plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()
print("figure ->", out)
