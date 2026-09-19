#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p5_sc.py -- P5 单细胞 hub 定位（纯 numpy/scipy/sklearn + umap，不依赖 scanpy/numba-JIT 缓存）

用法:
    python p5_sc.py <GSE> <tissue>        tissue in {DRG, SC}

设计纪律（对齐 PROJECT_PLAN.md §4 统计铁律）:
  * 细胞层级只做描述性统计（pct_expressing / mean lognorm），不做细胞级推断；
  * 条件对比一律在 **样本级 pseudobulk** 上做，且 n=2~3/组 -> 只报方向，不报 p 值结论；
  * ambient RNA 需排查：报告每个 hub 基因的全细胞检出率与低质量细胞富集指数，超阈值标记 ambient_suspect；
  * 聚类仅用于"用 canonical marker 定义细胞类型"，注释结果全部落盘可审计。

产物:
  results/tables/P5_<GSE>_qc_summary.csv
  results/tables/P5_<GSE>_cluster_annotation.csv
  results/tables/P5_<GSE>_cellmeta.csv.gz
  results/tables/P5_<GSE>_celltype_composition.csv
  results/tables/P5_<GSE>_hub_localisation.csv
  results/tables/P5_<GSE>_hub_celltype_top.csv
  results/tables/P5_<GSE>_pseudobulk_celltype.csv
  data/processed/P5_<GSE>_embedding.npz
  results/figures/P5_<GSE>_localisation.png
"""
import os, sys, glob, re, time, json, warnings
import numpy as np, pandas as pd
import scipy.io, scipy.sparse as sp
from scipy import stats as sstats
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
T0 = time.time()
def log(*a):
    print(f"[{time.time()-T0:7.1f}s]", *a, flush=True)

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB  = os.path.join(ROOT, "results/tables")
FIG  = os.path.join(ROOT, "results/figures")
PROC = os.path.join(ROOT, "data/processed")
for d in (TAB, FIG, PROC):
    os.makedirs(d, exist_ok=True)

GSE    = sys.argv[1] if len(sys.argv) > 1 else "GSE216039"
TISSUE = (sys.argv[2] if len(sys.argv) > 2 else "DRG").upper()
# optional 3rd arg: regex to restrict which samples enter the joint analysis
# (needed for GSE328175, whose Transplant1/2 are HUMAN hg19 while Sham/SNI are mouse mm10)
SAMPLE_FILTER = sys.argv[3] if len(sys.argv) > 3 else None
RAW    = os.path.join(ROOT, f"data/raw/{GSE}/10x")
if os.path.isdir(os.path.join(ROOT, f"data/raw/{GSE}/10x_flat")):
    RAW = os.path.join(ROOT, f"data/raw/{GSE}/10x_flat")   # flattened nested archives
TAG    = f"{GSE}_{TISSUE}" + (f"_{SAMPLE_FILTER.replace('|', '')}" if SAMPLE_FILTER else "")

# ----------------------------------------------------------------------------- markers
# 注意：**禁止**把泛核/泛细胞基因（MALAT1/NEAT1/MEG3/XIST/SNHG11 等 lncRNA）放进任何 marker 集。
# 在 snRNA-seq 中这类核内 lncRNA 几乎在所有核里高表达，会把得分系统性拉向"它所在的集合"
# （实测：MEG3 放在 Neuron 集里会使 Neuron 占比虚高）。由 PAN_NUCLEAR 黑名单统一剔除。
PAN_NUCLEAR = {"MALAT1","NEAT1","MEG3","XIST","SNHG11","B2M","ACTB","GAPDH","TMSB10"}
MARKERS_DRG = {
 "Neuron":          ["TUBB3","AVIL","NEFL","NEFH","PRPH","SCN9A","SNAP25","ELAVL2","UCHL1","ISL1","STMN2","PCP4"],
 "SatelliteGlia":   ["FABP7","GJA1","KCNJ10","S100B","SOX2","HTRA1","SLC1A3","BCAN","KIRREL2","CDH19"],
 "Schwann":         ["MPZ","PMP22","PLP1","MBP","SOX10","MAG","EGR2","NCAM1"],
 "Immune":          ["PTPRC","CD68","CSF1R","LYZ2","CD14","FCGR3","AIF1","C1QA","C1QB","C1QC","TREM2","TYROBP","CTSS","HEXB"],
 "Endothelial":     ["PECAM1","CLDN5","FLT1","EMCN","CD34","RAMP2"],
 "Fibroblast":      ["DCN","PDGFRA","COL1A1","COL1A2","LUM","POSTN","COL3A1"],
 "Pericyte_VSMC":   ["RGS5","PDGFRB","MYH11","DES","ACTA2","KCNJ8","VTN"],
 "Erythrocyte":     ["HBA-A1","HBB-BS","HBA-A2","HBB-BT","ALAS2"],
}
MARKERS_SC = {
 "Neuron":          ["SNAP25","SYT1","RBFOX3","TUBB3","STMN2","NEFL","NEFM","SYP","ELAVL2","SLC17A7","GAD1","GAD2"],
 "Astrocyte":       ["AQP4","GFAP","SLC1A2","SLC1A3","ALDH1L1","SOX9","GJA1","S100B","AQP1"],
 "Microglia":       ["CX3CR1","P2RY12","TMEM119","CSF1R","CTSS","HEXB","C1QA","C1QB","TYROBP","AIF1","CD68"],
 "Oligodendrocyte": ["PLP1","MBP","MOG","MAG","SOX10","CNP","MOBP","CLDN11","ASPA"],
 "OPC":             ["PDGFRA","CSPG4","OLIG1","OLIG2","LHFPL3","SOX10","BCAN"],
 "Endothelial":     ["PECAM1","CLDN5","FLT1","EMCN","RAMP2","CD34"],
 "Pericyte":        ["RGS5","PDGFRB","KCNJ8","VTN","DES","ACTA2"],
 "Ependymal":       ["FOXJ1","CCDC153","RARRES2","TMEM212","DNAH12","HYDIN"],
 "Fibroblast_Meninges": ["DCN","COL1A1","PDGFRA","SLC6A13","LUM","COL1A2"],
}
# 剔除泛核/泛细胞基因（见上方说明）
for _ct in list(MARKERS_DRG):
    MARKERS_DRG[_ct] = [g for g in MARKERS_DRG[_ct] if g not in PAN_NUCLEAR]
for _ct in list(MARKERS_SC):
    MARKERS_SC[_ct] = [g for g in MARKERS_SC[_ct] if g not in PAN_NUCLEAR]
MARKERS = MARKERS_SC if TISSUE == "SC" else MARKERS_DRG
# 污染/低复杂度细胞类型：仅作背景描述，不参与 hub "top cell type" 评选
CONTAMINANT_CELLTYPES = {"Erythrocyte"}

MT_PREFIX = "MT-"

# ----------------------------------------------------------------------------- load
def load_sample(prefix):
    """10x mtx(genes x cells) -> cells x unique-symbol sparse matrix."""
    mtx = os.path.join(RAW, f"{prefix}_matrix.mtx.gz")
    bcs = os.path.join(RAW, f"{prefix}_barcodes.tsv.gz")
    fts = os.path.join(RAW, f"{prefix}_features.tsv.gz")
    X = scipy.io.mmread(mtx).T.tocsr().astype(np.float32)          # cells x genes(orig order)
    bc = pd.read_csv(bcs, header=None)[0].astype(str).values
    ft = pd.read_csv(fts, header=None, sep="\t")
    c0 = ft[0].astype(str)
    # v3 features.tsv = (ensembl_id, symbol, type); some GEO drops = (symbol, ...) only
    if ft.shape[1] > 1 and c0.str.upper().str.startswith(("ENS", "ENSMUSG", "ENSRNOG")).mean() > 0.5:
        sym = ft[1].astype(str).str.upper().values
    else:
        sym = c0.str.upper().values
    if X.shape[0] != len(bc):
        X = X.T.tocsr()
    assert X.shape[1] == len(sym), f"{prefix}: mtx genes {X.shape[1]} != features {len(sym)}"
    # collapse duplicate symbols by summing columns: X(cells x G) @ agg(G x U)
    uni, inv = np.unique(sym, return_inverse=True)
    agg = sp.csr_matrix((np.ones(len(inv), np.float32), (np.arange(len(inv)), inv)),
                        shape=(len(inv), len(uni)))
    Xs = (X @ agg).tocsr()
    # some GEO deposits ship the FULL 10x barcode whitelist (6,794,880 barcodes) with
    # all-zero columns for the unused ones -> keep only barcodes with >=1 counted UMI
    nz = np.diff(Xs.indptr) > 0
    if not nz.all():
        Xs, bc = Xs[nz].tocsr(), bc[nz]
    return Xs, bc, uni

files = sorted(set(os.path.basename(f).replace("_matrix.mtx.gz", "")
                   for f in glob.glob(os.path.join(RAW, "*_matrix.mtx.gz"))))
if SAMPLE_FILTER:
    allf = list(files)
    files = [f for f in files if re.search(SAMPLE_FILTER, f, flags=re.I)]
    log(f"sample filter '{SAMPLE_FILTER}': kept {files} | excluded {[f for f in allf if f not in files]}")
log(f"{GSE} samples: {files}")
assert files, f"no 10x files under {RAW} matching {SAMPLE_FILTER}"

CACHE = os.path.join(PROC, f"P5_{TAG}_counts.npz")
if os.path.exists(CACHE):
    z = np.load(CACHE, allow_pickle=True)
    X = sp.csr_matrix((z["data"], z["indices"], z["indptr"]), shape=tuple(z["shape"]))
    common = z["common"]
    obs = pd.DataFrame({"cell": z["cell"], "sample": z["sample"]}).set_index("cell")
    log(f"loaded cache: {X.shape}")
else:
    mats, bcs, syms = [], [], []
    for f in files:
        Xs, bc, uni = load_sample(f)
        mats.append(Xs); bcs.append(bc); syms.append(uni)
        log(f"  {f}: {Xs.shape}")

    common = syms[0]
    for s in syms[1:]:
        common = np.intersect1d(common, s)
    common = np.sort(common)
    log(f"common symbols: {len(common)}")

    blocks, obs = [], []
    for f, Xs, bc, uni in zip(files, mats, bcs, syms):
        idx = pd.Index(uni).get_indexer(common)
        blocks.append(Xs[:, idx])
        obs.append(pd.DataFrame({"cell": [f"{f}|{b}" for b in bc], "sample": f}))
    X = sp.vstack(blocks, format="csr").astype(np.float32)
    obs = pd.concat(obs, ignore_index=True).set_index("cell")
    del mats, blocks
    np.savez_compressed(CACHE, data=X.data, indices=X.indices, indptr=X.indptr,
                        shape=np.array(X.shape, dtype=np.int64), common=common,
                        cell=obs.index.values, sample=obs["sample"].values)
    log(f"counts cached -> {CACHE}")
log(f"combined: {X.shape}")

# ----------------------------------------------------------------------------- condition / sex
def parse_meta(name):
    up = name.upper()
    toks = set(re.split(r"[^A-Z]+", up))          # tokenise: 'FEMALE' must NOT match 'MALE'
    if "TRANSPLANT" in toks or "TRANSPLANT" in up: cond = "Transplant"
    elif "SNI" in toks:                            cond = "SNI"
    elif "SHAM" in toks or "NAIVE" in toks:        cond = "Sham"
    elif "CCI" in toks:                            cond = "CCI"
    else:                                          cond = "Other"
    sex = "Male" if "MALE" in toks else ("Female" if "FEMALE" in toks else "NA")
    return cond, sex

# per-dataset condition overrides where sample names are opaque (verified from series_matrix)
# GSE246288 sample titles: SA='PID 0'(sham) / 3A / 7A / 14A = post-SNI days 3,7,14
META_OVERRIDE = {
    "GSE246288": {"SA": ("Sham", "PID0"), "3A": ("SNI", "PID3"),
                  "7A": ("SNI", "PID7"), "14A": ("SNI", "PID14")},
}
def parse_meta_ds(gse, name):
    if gse in META_OVERRIDE:
        toks = re.split(r"[^A-Za-z0-9]+", name)
        for t in toks:
            if t.upper() in META_OVERRIDE[gse]:
                return META_OVERRIDE[gse][t.upper()]
    c, s = parse_meta(name)
    return c, s
obs[["condition", "timepoint"]] = pd.DataFrame([parse_meta_ds(GSE, s) for s in obs["sample"]], index=obs.index)
obs["sex"] = [parse_meta(s)[1] for s in obs["sample"]]
log("groups: " + str(obs.groupby(["condition", "timepoint"], observed=True).size().to_dict()))

# ----------------------------------------------------------------------------- QC
sym_upper = pd.Index(common).str.upper()
is_mt = np.asarray(sym_upper.str.startswith(MT_PREFIX))
n_genes = np.asarray((X > 0).sum(axis=1)).ravel().astype(int)
tot     = np.asarray(X.sum(axis=1)).ravel()
mt_ct   = np.asarray(X[:, is_mt].sum(axis=1)).ravel() if is_mt.any() else np.zeros(X.shape[0])
pct_mt  = np.where(tot > 0, mt_ct / np.maximum(tot, 1e-9) * 100, 0.0)
obs["n_genes"], obs["total_counts"], obs["pct_mt"] = n_genes, tot, pct_mt
log(f"pre-QC cells={X.shape[0]} median genes={np.median(n_genes):.0f} median UMIs={np.median(tot):.0f} median %mt={np.median(pct_mt):.2f}")

keep_c = (n_genes >= 200) & (pct_mt < 15) & (tot >= 500)
X, obs = X[keep_c].tocsr(), obs.loc[keep_c].copy()
det = np.asarray((X > 0).sum(axis=0)).ravel()
keep_g = det >= 3
X, common = X[:, keep_g].tocsr(), common[keep_g]
log(f"post-QC: {X.shape[0]} cells x {X.shape[1]} genes | dropped {int((~keep_c).sum())} cells")

qc = pd.DataFrame([{
    "dataset": GSE, "tissue": TISSUE, "n_samples": len(files), "n_cells": int(X.shape[0]),
    "n_genes": int(X.shape[1]), "cell_median_genes": float(np.median(obs.n_genes)),
    "cell_median_umi": float(np.median(obs.total_counts)), "cell_median_pct_mt": float(np.median(obs.pct_mt)),
    "groups": json.dumps({"|".join(map(str, k)): int(v) for k, v in
                           obs.groupby(["condition", "timepoint", "sex"], observed=True).size().items()}),
}])
qc.to_csv(os.path.join(TAB, f"P5_{TAG}_qc_summary.csv"), index=False)

# ----------------------------------------------------------------------------- normalise (log1p CP10K)
lib = np.asarray(X.sum(axis=1)).ravel()
X = sp.diags((1e4 / np.maximum(lib, 1e-9)).astype(np.float32)) @ X
X.data = np.log1p(X.data)
X = X.tocsr()
det = np.asarray((X > 0).sum(axis=0)).ravel()      # recompute AFTER combined cell+gene filtering
log("normalised & log1p")

# ----------------------------------------------------------------------------- HVG (seurat-style dispersion, pure numpy)
mu  = np.asarray(X.mean(axis=0)).ravel()
mu2 = np.asarray(X.power(2).mean(axis=0)).ravel()
var = np.maximum(mu2 - mu ** 2, 0)
valid = det >= 10
with np.errstate(divide="ignore", invalid="ignore"):
    disp = np.where(mu > 0, var / np.maximum(mu, 1e-9), 0.0)
sel = np.where(valid)[0]
q = pd.qcut(mu[sel], 20, labels=False, duplicates="drop")
zdisp = np.zeros(len(sel))
for b in np.unique(q):
    m = q == b
    v = disp[sel[m]]
    zdisp[m] = (v - v.mean()) / (v.std() + 1e-9)
hvg_idx = sel[np.argsort(-zdisp)[:2000]]
hvg = common[hvg_idx]
log(f"HVG: {len(hvg_idx)} (top: {', '.join(hvg[:8])})")

# ----------------------------------------------------------------------------- scale + PCA
Sd = np.asarray(X[:, hvg_idx].todense(), dtype=np.float32)
Sd = (Sd - Sd.mean(axis=0)) / (Sd.std(axis=0) + 1e-9)
np.clip(Sd, -10, 10, out=Sd)
pca = PCA(n_components=30, svd_solver="randomized", random_state=0)
PC = pca.fit_transform(Sd).astype(np.float32)
log(f"PCA: {PC.shape} | var explained (first 10) {np.round(pca.explained_variance_ratio_[:10], 3)}")
del Sd

# ----------------------------------------------------------------------------- KMeans
K = 25 if TISSUE == "DRG" else 30
km = KMeans(n_clusters=K, n_init=10, random_state=0)
obs["cluster"] = km.fit_predict(PC)
log(f"KMeans k={K} inertia={km.inertia_:.1f}")

# ----------------------------------------------------------------------------- UMAP
try:
    import umap
    emb2 = umap.UMAP(n_neighbors=15, min_dist=0.3, n_components=2, random_state=0).fit_transform(PC)
except Exception as e:
    log(f"umap failed ({e}); fallback to PCA-2D")
    emb2 = PC[:, :2]
obs["UMAP1"], obs["UMAP2"] = emb2[:, 0], emb2[:, 1]

# ----------------------------------------------------------------------------- marker-based annotation
clusters = sorted(obs["cluster"].unique())
allm = sorted({g.upper() for ms in MARKERS.values() for g in ms})
gpos = pd.Index(common).get_indexer(allm)
present = {allm[i]: int(gpos[i]) for i in range(len(allm)) if gpos[i] >= 0}
log(f"marker genes mapped: {len(present)}/{len(allm)}")

mean_by_cl = np.zeros((len(clusters), len(allm)), dtype=np.float32)
for ci, cl in enumerate(clusters):
    sub = X[obs["cluster"].values == cl]
    v = np.asarray(sub.mean(axis=0)).ravel()
    mean_by_cl[ci] = [v[present[g]] if g in present else np.nan for g in allm]
mean_df = pd.DataFrame(mean_by_cl, index=[f"c{c}" for c in clusters], columns=allm)
# z-score per gene across clusters -> cluster-level marker enrichment
zdf = (mean_df - mean_df.mean(axis=0)) / (mean_df.std(axis=0) + 1e-9)

anno_rows = []
for ci, cl in enumerate(clusters):
    scores = {}
    for ct, ms in MARKERS.items():
        gg = [g.upper() for g in ms if g.upper() in zdf.columns]
        gg = sorted(gg, key=lambda g: -zdf.loc[f"c{cl}", g])[:6]      # top-6 contributing markers
        gg = [g for g in gg if np.isfinite(zdf.loc[f"c{cl}", g])]
        scores[ct] = float(np.mean([zdf.loc[f"c{cl}", g] for g in gg])) if gg else -9.9
    order = sorted(scores.items(), key=lambda kv: -kv[1])
    best, second = order[0], (order[1] if len(order) > 1 else ("", -9.9))
    anno_rows.append({"cluster": cl, "n_cells": int((obs["cluster"] == cl).sum()),
                      "assigned": best[0], "score_best": round(best[1], 3),
                      "score_second": round(second[1], 3), "score_second_ct": second[0],
                      "margin": round(best[1] - second[1], 3),
                      **{f"score_{k}": round(v, 3) for k, v in scores.items()}})
anno = pd.DataFrame(anno_rows)
anno.to_csv(os.path.join(TAB, f"P5_{TAG}_cluster_annotation.csv"), index=False)
obs["celltype"] = obs["cluster"].map(dict(zip(anno.cluster, anno.assigned)))
log("cluster annotation:")
for r in anno_rows:
    log(f"   c{r['cluster']:<3} n={r['n_cells']:<5} -> {r['assigned']:<20} margin={r['margin']:.2f}")

log("celltype counts: " + str(obs.celltype.value_counts().to_dict()))

obs[["sample", "condition", "timepoint", "sex", "n_genes", "total_counts", "pct_mt", "cluster", "celltype", "UMAP1", "UMAP2"]] \
   .to_csv(os.path.join(TAB, f"P5_{TAG}_cellmeta.csv.gz"), compression="gzip")

comp = obs.groupby(["sample", "condition", "timepoint", "celltype"], observed=True).size().unstack(fill_value=0)
comp_frac = comp.div(comp.sum(axis=1), axis=0)
comp_frac.to_csv(os.path.join(TAB, f"P5_{TAG}_celltype_composition.csv"))
np.savez_compressed(os.path.join(PROC, f"P5_{TAG}_embedding.npz"), PC=PC, UMAP=emb2,
                    cluster=obs["cluster"].values, celltype=obs["celltype"].values)

# ----------------------------------------------------------------------------- hub localisation
hubdf = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
hub = hubdf["symbol"].astype(str).str.upper().tolist()
sym2idx = {}
for i, s in enumerate(np.asarray(pd.Index(common).str.upper())):
    sym2idx.setdefault(s, i)
hubp = [g for g in hub if g in sym2idx]
missing = [g for g in hub if g not in sym2idx]
log(f"hub genes present: {len(hubp)}/{len(hub)} | absent: {missing}")

cts = sorted(obs.celltype.unique())
low_q = np.quantile(obs.total_counts.values, 0.10)
lowmask = (obs.total_counts.values <= low_q)
ct_arr = obs.celltype.values
# precompute full-length vectors once per hub gene (avoid 3x redundant densify per cell type)
gvec = {}
for g in hubp:
    vg = np.asarray(X[:, sym2idx[g]].todense()).ravel()
    gvec[g] = (vg, float(vg[lowmask].mean()), float((vg > 0).mean()))
rows = []
ct_qc = obs.groupby("celltype", observed=True)["n_genes"].median().to_dict()
for ct in cts:
    m = (ct_arr == ct)
    for g in hubp:
        vg, vg_low, pct_all = gvec[g]
        v = vg[m]
        rows.append({"celltype": ct, "symbol": g, "n_cells": int(m.sum()),
                     "median_n_genes": float(ct_qc.get(ct, np.nan)),
                     "is_contaminant": ct in CONTAMINANT_CELLTYPES,
                     "mean_lognorm": float(v.mean()), "pct_expressing": float((v > 0).mean()),
                     "pct_expressing_allcells": pct_all,
                     "ambient_index": float(vg_low / (vg.mean() + 1e-9))})
loc = pd.DataFrame(rows)
loc["ambient_suspect"] = (loc.pct_expressing_allcells > 0.90) & (loc.ambient_index > 0.80)
loc.to_csv(os.path.join(TAB, f"P5_{TAG}_hub_localisation.csv"), index=False)
log("celltype median n_genes: " + str({k: int(v) for k, v in sorted(ct_qc.items())}))

spec = []
for g in hubp:
    s = loc[loc.symbol == g].sort_values("mean_lognorm", ascending=False)
    top = s.iloc[0]
    others = s.iloc[1:]
    spec.append({
        "symbol": g, "top_celltype": top.celltype, "top_mean": round(top.mean_lognorm, 4),
        "top_pct": round(top.pct_expressing, 3),
        "mean_others": round(float(others.mean_lognorm.mean()), 4),
        "specificity": round(float(top.mean_lognorm / (others.mean_lognorm.mean() + 1e-9)), 2),
        "n_celltypes": len(s),
        "ambient_index": round(float(top.ambient_index), 3),
        "ambient_suspect": bool(top.ambient_suspect),
        "n_methods": int(hubdf.loc[hubdf.symbol.str.upper() == g, "n_methods"].iloc[0]),
    })
sp_df = pd.DataFrame(spec).sort_values(["n_methods", "top_mean"], ascending=False)
sp_df.to_csv(os.path.join(TAB, f"P5_{TAG}_hub_celltype_top.csv"), index=False)
log("=== hub top cell type (top 25) ===")
log("\n" + sp_df.head(25).to_string(index=False))

# ----------------------------------------------------------------------------- sample-level pseudobulk
pbcols = [sym2idx[g] for g in hubp]
pbX = X[:, pbcols]
pbdf = pd.DataFrame(np.asarray(pbX.todense()), columns=hubp)
pbdf["sample"] = obs["sample"].values
pbdf["celltype"] = obs["celltype"].values
pb = pbdf.groupby(["celltype", "sample"], observed=True).mean().reset_index()
pb["condition"] = pb["sample"].map(dict(zip(obs["sample"], obs["condition"])))
pb["n_cells"] = [int(((obs.celltype == r.celltype) & (obs["sample"] == r.sample)).sum()) for r in pb.itertuples()]
pb = pb[pb.n_cells >= 10]
pb.to_csv(os.path.join(TAB, f"P5_{TAG}_pseudobulk_celltype.csv"), index=False)

pairs = [("CCI", "Sham"), ("SNI", "Sham"), ("Transplant", "SNI")]
res = []
for ct, sub in pb.groupby("celltype", observed=True):
    for A, B in pairs:
        sa, sb = sub[sub.condition == A], sub[sub.condition == B]
        if len(sa) < 2 or len(sb) < 2:
            continue
        for g in hubp:
            a, b = sa[g].values, sb[g].values
            res.append({"celltype": ct, "contrast": f"{A}_vs_{B}", "symbol": g,
                        "mean_A": float(a.mean()), "mean_B": float(b.mean()),
                        "delta_log": float(a.mean() - b.mean()),
                        "n_A": len(a), "n_B": len(b),
                        "welch_p": float(sstats.ttest_ind(a, b, equal_var=False).pvalue),
                        "note": f"n={len(a)}v{len(b)} sample-level; descriptive only"})
if res:
    pr = pd.DataFrame(res)
    pr["bh_q"] = np.nan
    for c in pr.contrast.unique():
        m = pr.contrast == c
        p = pr.loc[m, "welch_p"].values
        o = np.argsort(p); n = len(p)
        q = np.minimum.accumulate((p[o] * n / np.arange(1, n + 1))[::-1])[::-1]
        tmp = np.empty(n); tmp[o] = np.clip(q, 0, 1)
        pr.loc[m, "bh_q"] = tmp
    pr.to_csv(os.path.join(TAB, f"P5_{TAG}_pseudobulk_stats.csv"), index=False)
    log("pseudobulk contrast summary:")
    for (ct, cc), sub in pr.groupby(["celltype", "contrast"], observed=True):
        sig = int((sub.bh_q < 0.05).sum())
        log(f"   {ct:<20} {cc:<22} nA={sub.n_A.iloc[0]} nB={sub.n_B.iloc[0]} BH<0.05: {sig}/{len(sub)}")

# ----------------------------------------------------------------------------- figure
fig, axes = plt.subplots(2, 2, figsize=(15, 12.5))
ax = axes[0, 0]
sub = obs.sample(min(12000, len(obs)), random_state=0)
cmap = plt.get_cmap("tab10")
for i, ct in enumerate(cts):
    m = sub.celltype == ct
    ax.scatter(sub.UMAP1[m], sub.UMAP2[m], s=1.4, c=[cmap(i % 10)], label=f"{ct} ({int((obs.celltype==ct).sum())})", linewidths=0)
ax.set_xlabel("UMAP1"); ax.set_ylabel("UMAP2"); ax.set_title(f"A  {GSE} {TISSUE} cells (n={len(obs)})")
ax.legend(fontsize=6.5, markerscale=7, loc="best", frameon=False)

ax = axes[0, 1]
op = sp_df[~sp_df.ambient_suspect]
M = loc.pivot_table(index="celltype", columns="symbol", values="mean_lognorm")
order = [g for g in sp_df.symbol if g in M.columns]
M = M[order]
Mz = (M - M.mean(axis=0)) / (M.std(axis=0) + 1e-9)
im = ax.imshow(Mz.values, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
ax.set_xticks(range(len(order))); ax.set_xticklabels(order, rotation=90, fontsize=7)
ax.set_yticks(range(len(Mz.index))); ax.set_yticklabels(Mz.index, fontsize=7.5)
ax.set_title("B  hub gene enrichment across cell types (row-free z)")
fig.colorbar(im, ax=ax, fraction=0.025, pad=0.01)

ax = axes[1, 0]
cnt = obs.groupby(["condition", "celltype"], observed=True).size().unstack(fill_value=0)
frac = cnt.div(cnt.sum(axis=1), axis=0)
frac.plot(kind="bar", stacked=True, ax=ax, colormap="tab20", width=0.75, legend=False)
ax.set_ylabel("fraction of cells"); ax.set_title("C  cell-type composition per sample group")
ax.set_xlabel(""); ax.tick_params(axis="x", rotation=0, labelsize=8)
ax.legend(fontsize=6, ncol=2, loc="upper right", frameon=False)

ax = axes[1, 1]
vc = sp_df.top_celltype.value_counts()
ax.barh(range(len(vc)), vc.values, color="#4C72B0")
ax.set_yticks(range(len(vc))); ax.set_yticklabels(vc.index, fontsize=8)
ax.invert_yaxis(); ax.set_xlabel("n hub genes"); ax.set_title(f"D  hub (n={len(sp_df)}) top cell type")
for i, v in enumerate(vc.values):
    ax.text(v + 0.15, i, str(v), va="center", fontsize=8)
plt.tight_layout()
out = os.path.join(FIG, f"P5_{TAG}_localisation.png")
plt.savefig(out, dpi=200, bbox_inches="tight"); plt.close()
log(f"figure -> {out}")
log(f"=== P5 {GSE} / {TISSUE} DONE ===")
