#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p5_subtype.py -- 神经元亚型细化 + hub 富集（严格规避循环论证）

为什么单独一个脚本：
  GSE216039 是 Pirt-EGFP **神经元富集**数据，把全部 cluster 归为一个大类 "Neuron" 后，
  "hub 在神经元表达" 几乎无信息量。有价值的问法是：hub 是否集中在 **CCI 诱导的损伤/再生神经元亚型**。
  但 ATF3 / NPY / SPRR1A / VIP / FLRT3 / ECEL1 既是 hub **又是**该亚型的经典 marker
  —— 用它们注释亚型再报"hub 富集于此" = 循环论证（double-dipping）。

本脚本的三条红线：
  1. **注释只用非 hub marker**（Injured_Regen 亚型仅用 GAL/GAP43/SOX11/VGF/MMP16/CDK5R1/SCG2）；
     被排除的 hub-marker 逐条打印留痕。
  2. hub 来自 **不同数据集**的 bulk 分析（GSE278227/267799/241361/212311），与 GSE216039
     单细胞聚类相互独立 → 聚类本身不含 hub 信息。
  3. 同时给出 **cluster 级**（无监督，完全不经注释）与 **亚型级** 两套富集结果，
     并计算 leave-one-out（去掉注释基因后）富集是否稳健。

用法: python p5_subtype.py <GSE> <TISSUE> [TAG_SUFFIX]
"""
import os, sys, re, time, json
import numpy as np, pandas as pd
import scipy.sparse as sp
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.1f}s]", *a, flush=True)

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB, FIG, PROC = [os.path.join(ROOT, p) for p in ("results/tables", "results/figures", "data/processed")]
GSE = sys.argv[1] if len(sys.argv) > 1 else "GSE216039"
TISSUE = (sys.argv[2] if len(sys.argv) > 2 else "DRG").upper()
SUF = sys.argv[3] if len(sys.argv) > 3 else ""
TAG = f"{GSE}_{TISSUE}{SUF}"
if TISSUE != "DRG":
    log("subtype refinement is DRG-specific; nothing to do"); sys.exit(0)
SRC = f"{GSE}_{TISSUE}"

# ---- 载入 P5 主流程的缓存与产物 ----
z = np.load(os.path.join(PROC, f"P5_{SRC}_counts.npz"), allow_pickle=True)
Xcnt = sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))
common = z["common"]; sym2idx = {}
for i, s in enumerate(np.asarray(pd.Index(common).str.upper())):
    sym2idx.setdefault(s, i)
meta = pd.read_csv(os.path.join(TAB, f"P5_{SRC}_cellmeta.csv.gz"), index_col=0)
hubdf = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
hub = hubdf["symbol"].astype(str).str.upper().tolist()
hubset = set(hub)
log(f"counts {Xcnt.shape} | cells in meta {meta.shape[0]} | hub {len(hub)}")

# ---- 同一 QC / 归一化（复用主流程规则，保证一致） ----
# 注意：counts 缓存是 **QC 前** 矩阵（23691 cells），cellmeta 是 **QC 后**（22063）。
# 因此 keep 掩码作用在 Xcnt 上得到 QC 后矩阵，行序与 cellmeta 完全一致（主流程同序写出）。
obs = meta.copy()
n_genes = np.asarray((Xcnt > 0).sum(axis=1)).ravel().astype(int)
tot = np.asarray(Xcnt.sum(axis=1)).ravel()
is_mt = np.asarray(pd.Index(common).str.upper().str.startswith("MT-"))
mt = np.asarray(Xcnt[:, is_mt].sum(axis=1)).ravel() if is_mt.any() else np.zeros(Xcnt.shape[0])
pct_mt = np.where(tot > 0, mt / np.maximum(tot, 1e-9) * 100, 0.0)
keep = (n_genes >= 200) & (pct_mt < 15) & (tot >= 500)
X = Xcnt[keep].tocsr()
assert X.shape[0] == obs.shape[0], f"QC 对齐失败: X={X.shape[0]} vs meta={obs.shape[0]}"
log(f"QC 对齐 OK: {X.shape[0]} cells（drop {int((~keep).sum())}）")
det = np.asarray((X > 0).sum(axis=0)).ravel(); kg = det >= 3
X, common = X[:, kg].tocsr(), common[kg]
lib = np.asarray(X.sum(axis=1)).ravel()
X = sp.diags((1e4 / np.maximum(lib, 1e-9)).astype(np.float32)) @ X
X.data = np.log1p(X.data); X = X.tocsr()
sym2idx = {}
for i, s in enumerate(np.asarray(pd.Index(common).str.upper())):
    sym2idx.setdefault(s, i)
log(f"aligned matrix: {X.shape}, cells {obs.shape[0]}")

# ---- 神经元亚型 marker：**只用非 hub 基因** ----
NEU_SUBTYPES = {
 "Injured_RegenNeuron":   ["GAL", "GAP43", "SOX11", "VGF", "MMP16", "CDK5R1", "SCG2", "NCAM1"],
 "Peptidergic_Nociceptor": ["CALCA", "CALCB", "TAC1", "TRPV1", "SST", "TACR1", "NTRK1", "ADCYAP1"],
 "NonPeptidergic_Noci":   ["MRGPRD", "P2RX3", "MRGPRA3", "CTNNA2", "SLC10A4", "RET"],
 "Myelinated_Proprio":    ["PVALB", "RUNX3", "NEFH", "ETV1", "SLC17A6", "MAFA"],
}
excluded = []
for k, ms in NEU_SUBTYPES.items():
    for g in list(ms):
        if g.upper() in hubset:
            excluded.append((k, g)); ms.remove(g)
log(f"REMOVED hub genes from subtype markers (circularity guard): {excluded}")
for k, ms in NEU_SUBTYPES.items():
    log(f"  {k}: {ms}  (mapped {sum(g.upper() in sym2idx for g in ms)}/{len(ms)})")

neu_clusters = sorted(obs.loc[obs.celltype == "Neuron", "cluster"].unique())
oth_clusters = sorted(set(obs["cluster"].unique()) - set(neu_clusters))
log(f"Neuron clusters: {len(neu_clusters)} | non-Neuron clusters: {len(oth_clusters)}")

def cl_mean(idxs, cols):
    return np.asarray(X[idxs][:, cols].mean(axis=0)).ravel()

cols = [sym2idx[g.upper()] for g in sum(NEU_SUBTYPES.values(), []) if g.upper() in sym2idx]
names = [g for g in sum(NEU_SUBTYPES.values(), []) if g.upper() in sym2idx]
rows = []
for cl in sorted(obs["cluster"].unique()):
    idxs = (obs["cluster"].values == cl)
    v = dict(zip(names, cl_mean(idxs, cols)))
    rows.append({"cluster": int(cl), "n_cells": int(idxs.sum()),
                 "current_celltype": obs.loc[idxs, "celltype"].iloc[0],
                 "is_neuron_cluster": cl in neu_clusters, **{k: round(v[k], 3) for k in names}})
M = pd.DataFrame(rows)
Mz = M[names].copy()
Mz = (Mz - Mz.mean(axis=0)) / (Mz.std(axis=0) + 1e-9)
for k, ms in NEU_SUBTYPES.items():
    gg = [g for g in ms if g in names]
    M[f"subscore_{k}"] = Mz[gg].mean(axis=1) if gg else np.nan
sub_cols = [c for c in M.columns if c.startswith("subscore_")]
M["assigned_subtype"] = M[sub_cols].idxmax(axis=1).str.replace("subscore_", "", regex=False)
M.loc[~M.is_neuron_cluster, "assigned_subtype"] = "non-neuronal"
M.sort_values(sub_cols[0], ascending=False).to_csv(os.path.join(TAB, f"P5_{TAG}_neuron_subtype_scores.csv"), index=False)
log("\n=== neuron subtype scores ===")
log(M[["cluster", "n_cells", "current_celltype"] + sub_cols + ["assigned_subtype"]].to_string(index=False))

obs["neuronsubtype"] = obs["cluster"].map(dict(zip(M.cluster, M.assigned_subtype)))
obs["finetype"] = np.where(obs.neuronsubtype == "non-neuronal", obs.celltype, obs.neuronsubtype)
log("fine cell types: " + str(obs.finetype.value_counts().to_dict()))

# ---- hub 富集：cluster 级（无监督） ----
hubp = [g for g in hub if g in sym2idx]
gvec = {}
for g in hubp:
    vg = np.asarray(X[:, sym2idx[g]].todense()).ravel(); gvec[g] = vg
cl_rows = []
for cl in sorted(obs["cluster"].unique()):
    idxs = (obs["cluster"].values == cl)
    for g in hubp:
        v = gvec[g][idxs]
        cl_rows.append({"cluster": int(cl), "n_cells": int(idxs.sum()),
                        "current_celltype": obs.loc[idxs, "celltype"].iloc[0],
                        "assigned_subtype": obs.loc[idxs, "neuronsubtype"].iloc[0],
                        "symbol": g, "mean_lognorm": float(v.mean()), "pct_expressing": float((v > 0).mean())})
clloc = pd.DataFrame(cl_rows)
clloc.to_csv(os.path.join(TAB, f"P5_{TAG}_hub_localisation_by_cluster.csv"), index=False)

# ---- hub 富集：亚型级 (finetype) ----
ft_rows = []
for ct in sorted(obs.finetype.unique()):
    idxs = (obs.finetype.values == ct)
    if idxs.sum() < 10: continue
    for g in hubp:
        v = gvec[g][idxs]
        ft_rows.append({"finetype": ct, "n_cells": int(idxs.sum()), "symbol": g,
                        "mean_lognorm": float(v.mean()), "pct_expressing": float((v > 0).mean())})
ftloc = pd.DataFrame(ft_rows)
ftloc.to_csv(os.path.join(TAB, f"P5_{TAG}_hub_localisation_finetype.csv"), index=False)

top = []
for g in hubp:
    s = ftloc[ftloc.symbol == g].sort_values("mean_lognorm", ascending=False)
    if s.empty: continue
    t, o = s.iloc[0], s.iloc[1:]
    om, op = float(o.mean_lognorm.mean()), float(o.pct_expressing.mean())
    enr_m = float(np.log2((t.mean_lognorm + 1e-3) / (om + 1e-3)))
    enr_p = float(np.log2((t.pct_expressing + 1e-3) / (op + 1e-3)))
    det = (float(t.mean_lognorm) > 0.05) and (float(t.pct_expressing) >= 0.05)
    tier = ("undetected" if not det else
            "restricted" if (enr_m >= 1.0 and enr_p >= 0.58) else
            "enriched" if enr_m >= 0.58 else "broad")
    top.append({"symbol": g, "top_finetype": t.finetype, "top_mean": round(float(t.mean_lognorm), 4),
                "top_pct": round(float(t.pct_expressing), 3),
                "others_mean": round(om, 4), "others_pct": round(op, 3),
                "log2_enrich_mean": round(enr_m, 2), "log2_enrich_pct": round(enr_p, 2),
                "specificity": round(float(t.mean_lognorm / (om + 1e-9)), 2),
                "detected": bool(det), "tier": tier,
                "n_methods": int(hubdf.loc[hubdf.symbol.str.upper() == g, "n_methods"].iloc[0])})
topdf = pd.DataFrame(top).sort_values(["n_methods", "top_mean"], ascending=False)
topdf.to_csv(os.path.join(TAB, f"P5_{TAG}_hub_finetype_top.csv"), index=False)
log("\n=== hub top FINETYPE ===")
log(topdf.to_string(index=False))
det = topdf[topdf.detected]
log(f"\nhub 在 DRG 可检出: {len(det)}/{len(topdf)}（剔除 top_pct<5% 或 mean<0.05 的近乎不表达基因）")
log("detected hub 的 top 亚型分布: " + str(det.top_finetype.value_counts().to_dict()))
log("tier 分布（含未检出）: " + str(topdf.tier.value_counts().to_dict()))
log("tier 分布（仅可检出）: " + str(det.tier.value_counts().to_dict()))
topdf = topdf[topdf.detected].copy()   # 下游图/富集只用可检出基因

# ---- 稳健性：逐个剔除"用于注释的非 hub marker"，看亚型划定是否稳定 ----
# 目的：证明 "Injured_RegenNeuron" 这个亚型不是靠某一个 marker 撑起来的。
inj = [g for g in NEU_SUBTYPES["Injured_RegenNeuron"] if g in names]
base_score = Mz[[g for g in inj]].mean(axis=1).values
base_assign = M["assigned_subtype"].values
loo = []
for drop in inj:
    gg = [g for g in inj if g != drop]
    sc = Mz[gg].mean(axis=1).values if gg else np.zeros(len(Mz))
    # 用剩余 marker 重算 Injured 亚型得分，其余亚型得分不变，重新取 argmax
    alt_all = M[sub_cols].copy()
    alt_all["subscore_Injured_RegenNeuron"] = sc
    alt_assign = alt_all[sub_cols].idxmax(axis=1).str.replace("subscore_", "", regex=False).values
    alt_assign = np.where(~M.is_neuron_cluster.values, "non-neuronal", alt_assign)
    n_same = int((alt_assign == base_assign).sum())
    # 秩相关（Spearman）看分数整体是否重排
    rx = pd.Series(base_score).rank().to_numpy(); ry = pd.Series(sc).rank().to_numpy()
    rx, ry = rx - rx.mean(), ry - ry.mean()
    d = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    loo.append({"dropped_marker": drop, "n_clusters_same_assignment": n_same,
                "n_clusters": int(len(M)), "frac_same": round(n_same / len(M), 3),
                "spearman_vs_full_score": round(float((rx * ry).sum() / d), 3) if d > 0 else np.nan,
                "injured_clusters_full": int((base_assign == "Injured_RegenNeuron").sum()),
                "injured_clusters_alt": int((alt_assign == "Injured_RegenNeuron").sum())})
loo_df = pd.DataFrame(loo)
loo_df.to_csv(os.path.join(TAB, f"P5_{TAG}_subtype_marker_LOO.csv"), index=False)
log("\n=== leave-one-marker-out: 亚型划定稳健性 ===")
log(loo_df.to_string(index=False))
log(f"（基线：{int((base_assign=='Injured_RegenNeuron').sum())} 个 cluster 判为 Injured_RegenNeuron）")

# ---- 图 ----
fig, axes = plt.subplots(1, 3, figsize=(19, 6))
ax = axes[0]
piv = clloc.pivot_table(index="cluster", columns="symbol", values="mean_lognorm")
piv = piv[[g for g in topdf.symbol if g in piv.columns]]
pz = (piv - piv.mean(axis=0)) / (piv.std(axis=0) + 1e-9)
im = ax.imshow(pz.T.values, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
ax.set_yticks(range(len(pz.columns))); ax.set_yticklabels(pz.columns, fontsize=6.5)
ax.set_xticks(range(len(pz.index)))
ax.set_xticklabels([f"c{c}\n{M.set_index('cluster').loc[c,'assigned_subtype'][:9]}" for c in piv.index],
                   rotation=90, fontsize=5.5)
ax.set_title("A  hub enrichment per unsupervised cluster"); fig.colorbar(im, ax=ax, fraction=0.03)

ax = axes[1]
ftl = ftloc.pivot_table(index="finetype", columns="symbol", values="mean_lognorm")
ftz = (ftl - ftl.mean(axis=0)) / (ftl.std(axis=0) + 1e-9)
im = ax.imshow(ftz.T.values, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
ax.set_yticks(range(ftz.shape[0])); ax.set_yticklabels(ftz.index, fontsize=7)
ax.set_xticks(range(ftz.shape[1])); ax.set_xticklabels(ftz.columns, rotation=90, fontsize=6.5)
ax.set_title("B  hub enrichment per fine cell type"); fig.colorbar(im, ax=ax, fraction=0.03)

ax = axes[2]
vc = topdf.top_finetype.value_counts()
ax.barh(range(len(vc)), vc.values, color="#C44E52")
ax.set_yticks(range(len(vc))); ax.set_yticklabels(vc.index, fontsize=8); ax.invert_yaxis()
ax.set_xlabel("n hub genes"); ax.set_title(f"C  hub (n={len(topdf)}) top fine cell type")
for i, v in enumerate(vc.values): ax.text(v + 0.2, i, str(v), va="center", fontsize=8)
plt.tight_layout()
out = os.path.join(FIG, f"P5_{TAG}_subtype_localisation.png")
plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()
log(f"figure -> {out}")
obs[["sample", "condition", "sex", "cluster", "celltype", "neuronsubtype", "finetype"]] \
   .to_csv(os.path.join(TAB, f"P5_{TAG}_cellmeta_finetype.csv.gz"), compression="gzip")
log("=== subtype refinement DONE ===")
