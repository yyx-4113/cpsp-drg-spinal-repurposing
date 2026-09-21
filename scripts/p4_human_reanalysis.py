#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
P4 human re-analysis (Step 1-2 of P4_HUMAN_REANALYSIS_COHORTS.md)
- GSE249746: cross-species anchor. Project 35 mouse hubs (+ADRA2A) onto 1136 human DRG
  single-soma neurons; cluster cells (KMeans), annotate clusters to DRG neuronal subtypes via
  marker-argmax, test whether hubs peak in human nociceptor/IB4+/NPY+ (pain-relevant) neurons.
- GSE107181: human iPS-DRG neurons vs iPS precursors (4 donor lines). Test whether the 35-hub
  program is human DRG-neuron enriched (per-line paired Welch + gene-set permutation, same as P3).

Statistical discipline (consistent with P2-P5):
- single-cell level = descriptive only; no inference at cell level.
- GSE107181 inference uses n=4 donor lines (neuron mean vs iPSC per line) -> Welch t.
- gene-set test uses permutation (label-permutation), not parametric assumption on long tail.
- fixed seed.
"""
import gzip, csv, json, os, time, warnings
import numpy as np
import pandas as pd
from scipy import sparse
from scipy.stats import spearmanr, ttest_ind
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.manifold import TSNE
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SEED = 42
np.random.seed(SEED)
warnings.filterwarnings("ignore")

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
HUB_CSV = f"{ROOT}/results/tables/P3_hub_genes.csv"
ENS9606 = f"{ROOT}/data/raw/geo_meta/ens2sym_tax9606.json"
OUT_T = f"{ROOT}/results/tables"
OUT_F = f"{ROOT}/results/figures"
os.makedirs(OUT_T, exist_ok=True); os.makedirs(OUT_F, exist_ok=True)

def log(m): print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)

# ---------- load hubs ----------
hubs = [r[0].strip().upper() for r in csv.reader(open(HUB_CSV)) if r and not r[0].startswith("symbol")]
hubs = list(dict.fromkeys(hubs))  # unique, keep order
log(f"hubs loaded: {len(hubs)}")

# =====================================================================
# PART A — GSE249746 cross-species anchor (human DRG single-soma atlas)
# =====================================================================
log("=== PART A: GSE249746 ===")
M249 = pd.read_csv(f"{ROOT}/data/raw/GSE249746/GSE249746_Expression_matrix_raw_counts.csv.gz",
                   index_col=0, compression="gzip")
genes249 = list(M249.index)
cells249 = list(M249.columns)
log(f"matrix {M249.shape[0]} genes x {M249.shape[1]} cells")
# human symbol coverage
present249 = [h for h in hubs if h in genes249] + (["ADRA2A"] if "ADRA2A" in genes249 else [])
missing249 = [h for h in hubs if h not in genes249]
log(f"hubs present in GSE249746: {len(present249)-1}/35 (+ADRA2A); missing: {missing249}")

X = M249.values.astype(np.float32)          # genes x cells
X = np.log1p(X)                               # normalize counts
# HVG: top 1500 by dispersion on log1p
mean = X.mean(axis=1)
disp = (X.var(axis=1) / (mean + 1e-6))
disp[mean < 0.05] = -1
hvg_idx = np.argsort(disp)[::-1][:1500]
Xh = X[hvg_idx, :].T                          # cells x hvg (1136 x 1500)
log(f"HVG selected: {Xh.shape}")

# PCA + KMeans (k=16 = paper neuronal types)
Xs = StandardScaler().fit_transform(Xh)
pca = PCA(n_components=50, random_state=SEED).fit_transform(Xs)
km = KMeans(n_clusters=16, random_state=SEED, n_init=10).fit(pca)
labels = km.labels_
log("KMeans done (16 clusters)")

# marker-based annotation of clusters
PAIN_MARKERS = ["TRPV1","CALCA","CALCB","NTRK1","SCN10A","SCN11A","P2RX3","RET","GFRA1","TH","NPY","SPP1"]
NONPAIN_MARKERS = ["PVALB","CNTNAP1","NTNG1","LHX1","FGF5"]
def zvec(sym):
    if sym not in genes249: return None
    v = X[genes249.index(sym)].astype(np.float64)
    return (v - v.mean())/ (v.std()+1e-9)
pain_z = np.vstack([zvec(m) for m in PAIN_MARKERS if zvec(m) is not None])     # present x cells
nonpain_z = np.vstack([zvec(m) for m in NONPAIN_MARKERS if zvec(m) is not None])
pain_score_cell = pain_z.mean(0)      # per-cell nociceptor score
nonpain_score_cell = nonpain_z.mean(0)
# cluster-level marker means
cl_pain = np.array([pain_score_cell[labels==c].mean() for c in range(16)])
cl_non = np.array([nonpain_score_cell[labels==c].mean() for c in range(16)])
# annotate: pain-relevant if pain>nonpain and pain above overall median
median_pain = np.median(cl_pain)
ann = []
for c in range(16):
    if cl_pain[c] > cl_non[c] and cl_pain[c] > median_pain:
        ann.append("pain_relevant")
    elif cl_pain[c] <= cl_non[c] and cl_non[c] > np.median(cl_non):
        ann.append("nonpain(LTMR/proprio)")
    else:
        ann.append("ambiguous")
log("cluster annotation: " + ", ".join(f"C{c}={a}" for c,a in enumerate(ann)))

# per-hub peak cluster + spearman vs pain score
hub_rows = []
for h in present249:
    gi = genes249.index(h)
    expr = X[gi].astype(np.float64)
    cl_mean = np.array([expr[labels==c].mean() for c in range(16)])
    peak = int(np.argmax(cl_mean))
    rho,_ = spearmanr(expr, pain_score_cell)
    hub_rows.append({
        "gene": h, "peak_cluster": peak, "peak_annotation": ann[peak],
        "peak_cluster_mean_expr": round(float(cl_mean[peak]),3),
        "spearman_vs_painScore": round(float(rho),3),
        "is_original_hub": h in hubs,
    })
hub249 = pd.DataFrame(hub_rows)
hub249.to_csv(f"{OUT_T}/P4_GSE249746_hub_celltype.csv", index=False)
n_pain = (hub249["peak_annotation"]=="pain_relevant").sum()
n_non = (hub249["peak_annotation"]=="nonpain(LTMR/proprio)").sum()
n_amb = (hub249["peak_annotation"]=="ambiguous").sum()
rhos = hub249[hub249.is_original_hub]["spearman_vs_painScore"].values
log(f"GSE249746 hub peak: pain_relevant={n_pain}, nonpain={n_non}, ambiguous={n_amb}")
log(f"GSE249746 hub spearman vs painScore: median={np.median(rhos):.3f}, frac>0={np.mean(rhos>0):.2f}")
pd.DataFrame({"cluster":range(16),"annotation":ann,"pain_score":cl_pain.round(3),"nonpain_score":cl_non.round(3)}).to_csv(f"{OUT_T}/P4_GSE249746_cluster_annotation.csv", index=False)

# UMAP/PCA scatter colored by pain score
proj = TSNE(n_components=2, random_state=SEED, perplexity=30, init="pca").fit_transform(pca[:, :30])
plt.figure(figsize=(6,5))
sc = plt.scatter(proj[:,0], proj[:,1], c=pain_score_cell, cmap="RdBu_r", s=6)
plt.colorbar(sc, label="human nociceptor score")
plt.title("GSE249746 human DRG neurons (n=1136)\ncolored by nociceptor score")
plt.tight_layout(); plt.savefig(f"{OUT_F}/P4_GSE249746_painScore_tsne.png", dpi=130); plt.close()
# scatter colored by hub-program (mean z of 34 hubs)
hub_mat = np.vstack([ (X[genes249.index(h)] - X[genes249.index(h)].mean())/(X[genes249.index(h)].std()+1e-9) for h in hubs if h in genes249])
hub_prog = hub_mat.mean(0)
plt.figure(figsize=(6,5))
sc = plt.scatter(proj[:,0], proj[:,1], c=hub_prog, cmap="viridis", s=6)
plt.colorbar(sc, label="35-hub program (mean z)")
plt.title("GSE249746: 35-hub program across human DRG neurons")
plt.tight_layout(); plt.savefig(f"{OUT_F}/P4_GSE249746_hubprogram_tsne.png", dpi=130); plt.close()
log("PART A figures saved")

# =====================================================================
# PART B — GSE107181 human iPS-DRG neurons vs iPS precursors
# =====================================================================
log("=== PART B: GSE107181 ===")
T = pd.read_csv(f"{ROOT}/data/raw/GSE107181/GSE107181_TOC.csv.gz", index_col=0, compression="gzip")
ens2sym = json.load(open(ENS9606))
# map ENSG -> human symbol, build symbol->row (first occurrence)
sym2row = {}
for e, row in T.iterrows():
    s = ens2sym.get(e, "")
    if s and s not in sym2row:
        sym2row[s] = row.astype(float).values
samples = list(T.columns)
neuron_cols = [c for c in samples if not c.startswith("iPSC")]
ipsc_cols   = [c for c in samples if c.startswith("iPSC")]
lines = sorted(set(c.split("_")[1] for c in samples))   # AD2, AD3, AH017, NHDF
log(f"samples={len(samples)} neuron={len(neuron_cols)} iPSC={len(ipsc_cols)} lines={lines}")
log(f"ENSG->symbol mapped genes: {len(sym2row)}")

present107 = [h for h in hubs if h in sym2row]
log(f"hubs present in GSE107181: {len(present107)}/35")

# per-line paired: neuron mean vs iPSC per line (n=4 lines)
rows = []
for h in present107:
    vec = sym2row[h]
    d = {c: vec[i] for i,c in enumerate(T.columns)}
    neu_line = []; ips_line = []
    for ln in lines:
        neu = [d[c] for c in neuron_cols if c.split("_")[1]==ln]
        ips = [d[c] for c in ipsc_cols if c.split("_")[1]==ln]
        neu_line.append(np.mean(neu) if neu else np.nan)
        ips_line.append(np.mean(ips) if ips else np.nan)
    neu_line = np.array(neu_line); ips_line = np.array(ips_line)
    log2fc = np.log2((neu_line.mean()+1)/(ips_line.mean()+1))
    t,p = ttest_ind(neu_line, ips_line, equal_var=False)
    rows.append({"gene":h, "neuron_mean":round(float(neu_line.mean()),3),
                 "ipsc_mean":round(float(ips_line.mean()),3),
                 "log2FC_neuron_vs_ipsc":round(float(log2fc),3),
                 "t":round(float(t),3), "p_welch":round(float(p),4),
                 "direction": "neuron_up" if log2fc>0 else "neuron_down"})
hub107 = pd.DataFrame(rows)
hub107.to_csv(f"{OUT_T}/P4_GSE107181_hub_neuron.csv", index=False)
n_up = (hub107.direction=="neuron_up").sum()
log(f"GSE107181: {n_up}/{len(hub107)} hubs neuron-up (human DRG neuronal)")

# gene-set permutation (like P3): rank all genes by per-line paired t (neuron vs iPSC),
# test if hub set enriched at neuron-up tail.
all_genes = list(sym2row.keys())
stat = {}
for g in all_genes:
    vec = sym2row[g]
    d = {c: vec[i] for i,c in enumerate(T.columns)}
    neu=[]; ips=[]
    for ln in lines:
        neu.append(np.mean([d[c] for c in neuron_cols if c.split("_")[1]==ln]))
        ips.append(np.mean([d[c] for c in ipsc_cols if c.split("_")[1]==ln]))
    neu=np.array(neu); ips=np.array(ips)
    if neu.std()+ips.std()==0: stat[g]=0.0
    else:
        tt,_=ttest_ind(neu,ips,equal_var=False); stat[g]=tt
ranked = sorted(all_genes, key=lambda g: stat[g], reverse=True)  # neuron-up first
Nh = len(present107)
obs_top = sum(1 for h in present107 if h in ranked[:Nh])
# permutation
rng = np.random.default_rng(SEED)
perm_counts = []
allset = np.array(all_genes)
for _ in range(2000):
    perm = rng.choice(allset, size=Nh, replace=False)
    perm_counts.append(sum(1 for h in perm if h in ranked[:Nh]))
perm_counts = np.array(perm_counts)
p_enrich = (np.sum(perm_counts >= obs_top)+1)/(len(perm_counts)+1)
log(f"GSE107181 gene-set permutation: observed top-{Nh}={obs_top}, perm p={p_enrich:.4f}")
pd.DataFrame([{"geneset":"35-hub (human orthologs)","observed_in_topN":obs_top,
               "N":Nh,"perm_p":round(float(p_enrich),4),
               "interpretation":"human DRG neuronal program enrichment"}]).to_csv(
               f"{OUT_T}/P4_GSE107181_geneset.csv", index=False)

log("DONE. PART A+B complete.")
