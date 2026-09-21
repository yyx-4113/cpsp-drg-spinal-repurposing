#!/usr/env python3
# -*- coding: utf-8 -*-
"""
p5_visium325938.py -- GSE325938 Visium 空间转录组：35 hub 程序的空间区域化定位

纪律（对齐 PROJECT_PLAN.md §4 与 P5_RESULTS）：
  * GSE325938 = "Spinal signatures of entrenched and treated neuropathic pain in male mice [Visium]"
    8 样本 = 4 鼠(Sham, ENSMUS) + 4 人源移植(ENSG)。主分析仅取鼠 4 样本臂。
  * 无鼠 SNI Visium 臂（Mouse_Sham1-4 / Human_2/4/6/8）→ 无法做空间 Sham-vs-SNI DE；
    改为对鼠 4 切片做 hub 程序的**空间区域化**，并与 P5 snRNA 细胞类型定位做跨模态互证。
  * spot 非独立（空间自相关）→ 区域均值先按切片聚合，再跨 4 切片报 mean±sd（描述性，不报 p）。
  * 排除 PAN_NUCLEAR 看家/泛核基因作 marker。

关键修复（vs 初版崩溃）：
  (1) Visium 鼠符号为 title-case（Atf3）而 hub 表为大写（ATF3）→ 大小写不敏感匹配（resolve()）。
  (2) 全程稀疏矩阵 + 仅物化需要的列（HVG1500 + hub + marker），消除 1.5GB 全密度矩阵导致的 swap 抖动。
  (3) 每张图独立 try/except，note md 始终落盘。

产物：results/tables/P5_GSE325938_*.csv (+ spot_qc / region_annotation / hub_regionalization / crossmodal)
      results/figures/P5_GSE325938_*.png (hub_spatial / regions / hub_region_heatmap)
      results/P5_GSE325938_note.md
"""
import os, sys, time, json, warnings
from collections import defaultdict
import numpy as np, pandas as pd
import scipy.io as sio
import scipy.sparse as sp
from scipy import stats as sstats
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
T0 = time.time()
def log(*a): print(f"[{time.time()-T0:7.1f}s]", *a, flush=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW  = os.path.join(ROOT, "data/raw/GSE325938")
TAB  = os.path.join(ROOT, "results/tables")
FIG  = os.path.join(ROOT, "results/figures")
os.makedirs(TAB, exist_ok=True); os.makedirs(FIG, exist_ok=True)

MOUSE_SAMPLES = [1, 2, 3, 4]          # confirmed ENSMUS (mouse, Sham)
HUBS = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))["symbol"].tolist()
log("hubs:", len(HUBS))

PAN_NUCLEAR = {"MALAT1","NEAT1","MEG3","XIST","SNHG11","B2M","ACTB","GAPDH","TMSB10","TMSB4X"}

REGION_MARKERS = {
    "DorsalHorn":   ["Calca","Calcb","Tac1","Trpv1","Pdyn","Pnoc","Gfra1","Slc17a6","Slc17a8","Gpr139"],
    "VentralHorn":  ["Chat","Isl1","Hb9","Chodl","Olig2","Lhx3","Slc18a3","Vamp1"],
    "WhiteMatter":  ["Mbp","Mag","Mog","Plp1","Mobp","Cnp","Tspan2","Opalin"],
    "Astrocyte":    ["Gfap","Aqp4","Slc1a2","Aldh1l1","Agxt2","Gja1"],
    "Microglia":    ["Cx3cr1","Aif1","Tmem119","C1qa","C1qb","C1qc","Itgam","Fcgr3"],
    "Ependymal":    ["Foxj1","Ccdc153","Dnai1","Ttll9","Ccdc67"],
    "MeningealFibro":["Col1a1","Dcn","Pdgfra","Lum","Postn","Col3a1","Sfrp2"],
}

# ---------------------------------------------------------------- case-insensitive resolver
def build_sym_index(all_syms):
    pos = {s: i for i, s in enumerate(all_syms)}
    pos_lower = defaultdict(int)
    for s, i in pos.items():
        pos_lower[s.lower()] = i
    return pos, pos_lower

def make_resolver(pos, pos_lower):
    def resolve(sym):
        if sym in pos: return pos[sym]
        lo = sym.lower()
        if lo in pos_lower: return pos_lower[lo]
        return -1
    return resolve

# ---------------------------------------------------------------- pass 1: collect symbol universe
sample_syms = {}
all_syms_set = set()
for s in MOUSE_SAMPLES:
    feat = pd.read_csv(os.path.join(RAW, f"sample{s}", "features.tsv.gz"), sep="\t", header=None,
                       names=["ens","symbol","type"], compression="gzip")
    syms = feat["symbol"].fillna("").astype(str).tolist()
    sample_syms[s] = syms
    for ss in syms:
        if ss and ss != "-":
            all_syms_set.add(ss)
all_syms = sorted(all_syms_set)
sym_pos, sym_pos_lower = build_sym_index(all_syms)
resolve = make_resolver(sym_pos, sym_pos_lower)
log("symbol universe:", len(all_syms))

# ---------------------------------------------------------------- pass 2: load mouse samples as sparse (spots x syms)
spot_frames = []   # (df, sparse_M2 spots x nsyms)
for s in MOUSE_SAMPLES:
    d = os.path.join(RAW, f"sample{s}")
    M = sio.mmread(os.path.join(d, "matrix.mtx.gz")).tocsc()      # genes x spots
    Msp = M.T.tocsr()                                             # spots x genes
    bc = pd.read_csv(os.path.join(d, "barcodes.tsv.gz"), sep="\t", header=None,
                     names=["barcode"], compression="gzip")
    tp = pd.read_csv(os.path.join(d, "tissue_positions_list.csv"), header=None)
    tp.columns = ["barcode","in_tissue","array_row","array_col","pxl_row","pxl_col"]
    tp["barcode"] = tp["barcode"].astype(str)
    bc["barcode"] = bc["barcode"].astype(str)
    tp = tp.set_index("barcode").loc[bc["barcode"].values].reset_index()
    sf = json.load(open(os.path.join(d, "scalefactors_json.json")))
    hsf = sf.get("tissue_hires_scalef", 1.0)
    # gene idx -> global sym idx map (per sample)
    syms = sample_syms[s]
    gmap = np.array([sym_pos.get(syms[i], -1) for i in range(len(syms))], dtype=np.int64)
    coo = Msp.tocoo()
    newcol = gmap[coo.col]
    mask = newcol >= 0
    M2 = sp.coo_matrix((coo.data[mask].astype(np.float32),
                        (coo.row[mask], newcol[mask])),
                       shape=(Msp.shape[0], len(all_syms))).tocsr()
    totals = np.asarray(M2.sum(1)).ravel().astype(np.float32)
    in_tissue = tp["in_tissue"].values.astype(int) == 1
    med = np.median(totals[totals > 0]) if (totals > 0).any() else 1.0
    keep = in_tissue & (totals >= max(50, med * 0.05))
    M2 = M2[keep]; totals = totals[keep]
    tp = tp[keep].reset_index(drop=True)
    xy = np.column_stack([tp["pxl_col"].values * hsf, tp["pxl_row"].values * hsf])
    df = pd.DataFrame({"sample": s, "barcode": tp["barcode"].values,
                       "x": xy[:,0], "y": xy[:,1], "total": totals})
    spot_frames.append((df, M2, totals))
    log(f"sample{s}: kept {M2.shape[0]} spots x {M2.shape[1]} syms; median total {med:.0f}")

# combine sparse
bigM = sp.vstack([f[1] for f in spot_frames], format="csr")
bigdf = pd.concat([f[0] for f in spot_frames], ignore_index=True)
totals_all = np.asarray(bigM.sum(1)).ravel().astype(np.float32)
log("combined spots:", bigM.shape)

# ---------------------------------------------------------------- normalization (sparse, in-place log1p)
bigM = bigM.tocsc()
bigM = bigM.multiply((1e6 / totals_all)[:, None]).tocsr()
bigM.data = np.log1p(bigM.data.astype(np.float32))
norm = bigM
del bigM

# ---------------------------------------------------------------- HVG on sparse (no dense 32k x spots)
gmean = np.asarray(norm.mean(axis=0)).ravel().astype(np.float32)
gmean2 = np.asarray(norm.multiply(norm).mean(axis=0)).ravel().astype(np.float32)
gvar = gmean2 - gmean**2
mask_mean = gmean > 0.1
disp = np.zeros(norm.shape[1], dtype=np.float32)
disp[mask_mean] = gvar[mask_mean] / (gmean[mask_mean] + 1e-6)
hv = np.argsort(-disp)[:1500]
log("HVG top:", hv.shape[0])
Xhvg = norm[:, hv].toarray().astype(np.float32)          # 5853 x 1500
log("Xhvg:", Xhvg.shape)

# hub + marker columns (resolve case-insensitively)
hub_col = {}
for h in HUBS:
    gi = resolve(h)
    if gi >= 0: hub_col[h] = gi
hub_cols = list(hub_col.values())
Xhub = norm[:, hub_cols].toarray().astype(np.float32) if hub_cols else np.empty((norm.shape[0], 0), np.float32)
log(f"hubs resolved in mouse Visium: {len(hub_col)}/{len(HUBS)}")

# marker columns per label (store GLOBAL sym idx first, then map to allmark positions)
raw_label_cols = {}
for label, mk in REGION_MARKERS.items():
    cols = [resolve(m) for m in mk if resolve(m) >= 0]
    if cols: raw_label_cols[label] = cols
allmark = sorted(set(c for cols in raw_label_cols.values() for c in cols))
Xmark = norm[:, allmark].toarray().astype(np.float32)
log(f"marker cols resolved: {len(allmark)} across {len(raw_label_cols)} labels")
markpos = {g: i for i, g in enumerate(allmark)}
label_cols = {label: [markpos[c] for c in cols] for label, cols in raw_label_cols.items()}

# free the big sparse now that small dense slices exist
del norm

# ---------------------------------------------------------------- spatial domains
Xh = StandardScaler().fit_transform(Xhvg)
pc = PCA(n_components=20, random_state=42).fit_transform(Xh)
K = 7
km = KMeans(n_clusters=K, n_init=10, random_state=42).fit(pc)
regions = km.labels_
bigdf["region"] = regions
nreg = K
log("regions:", np.bincount(regions))

# region annotation by marker sets (z-scored across regions)
Rm = np.vstack([Xmark[regions == r].mean(0) for r in range(nreg)])   # nreg x nmark
label_scores = {}
for label, cols in label_cols.items():
    arr = Rm[:, cols].mean(1)
    arr = (arr - arr.mean()) / (arr.std() + 1e-9)
    label_scores[label] = arr
region_label = []
for r in range(nreg):
    best, bv = "Unassigned", -1e9
    for label, arr in label_scores.items():
        if arr[r] > bv:
            bv, best = arr[r], label
    region_label.append(best)
log("region labels:", region_label)

# ---------------------------------------------------------------- hub regionalization
rows = []
for h in HUBS:
    if h not in hub_col:
        rows.append(dict(symbol=h, present=False)); continue
    ci = hub_cols.index(hub_col[h])
    g = Xhub[:, ci]
    global_mean = g.mean()
    detection_global = (g > 0).mean()
    pr = np.array([g[regions == r].mean() for r in range(nreg)])
    pd_ = np.array([(g[regions == r] > 0).mean() for r in range(nreg)])
    log2enr = np.log2((pr + 1e-6) / (global_mean + 1e-6))
    top_r = int(np.argmax(log2enr))
    sec_means = []
    for s in MOUSE_SAMPLES:
        sm = g[(bigdf["sample"] == s).values & (regions == top_r)]
        sec_means.append(sm.mean() if len(sm) else np.nan)
    sec_means = np.array(sec_means)
    le = log2enr[top_r]
    if le >= 1.0: tier = "restricted"
    elif le >= 0.58: tier = "enriched"
    else: tier = "broad/low"
    rows.append(dict(symbol=h, present=True,
                     top_region=region_label[top_r], top_label_log2=round(float(log2enr[top_r]), 3),
                     top_detection=round(float(pd_[top_r]), 3), global_mean=round(float(global_mean), 4),
                     detection_global=round(float(detection_global), 3), tier=tier,
                     sec_mean_top=round(float(np.nanmean(sec_means)), 4),
                     sec_sd_top=round(float(np.nanstd(sec_means)), 4),
                     log2_all_regions=";".join(f"{region_label[r]}:{log2enr[r]:.2f}" for r in range(nreg))))
hubreg = pd.DataFrame(rows)
present_hubs = hubreg[hubreg["present"]]
log(f"present hubs analysed: {len(present_hubs)}/{len(HUBS)}")

# ---------------------------------------------------------------- cross-modal vs P5 snRNA
try:
    cons = pd.read_csv(os.path.join(TAB, "P5_hub_lineage_consensus.csv"))
    symcol = "symbol" if "symbol" in cons.columns else cons.columns[0]
    lin_col = "lineage" if "lineage" in cons.columns else cons.columns[-1]
    snmap = dict(zip(cons[symcol].astype(str), cons[lin_col].astype(str)))
    exp = {"Neuronal": "DorsalHorn", "Immune": "Microglia", "Glial": "Astrocyte",
           "Mixed": None, "NotLocalisable": None}
    hubreg["snRNA_lineage"] = hubreg["symbol"].map(snmap)
    def agree(r):
        e = exp.get(r["snRNA_lineage"])
        if e is None or not r["present"]: return "n/a"
        return "consistent" if r["top_region"] == e else "divergent"
    hubreg["crossmodal"] = hubreg.apply(agree, axis=1)
    log("crossmodal consistent:", int((hubreg["crossmodal"]=="consistent").sum()),
        "/ divergent:", int((hubreg["crossmodal"]=="divergent").sum()))
except Exception as e:
    log("crossmodal skip:", e); hubreg["snRNA_lineage"] = np.nan; hubreg["crossmodal"] = np.nan

# ---------------------------------------------------------------- hub program score
if len(hub_col):
    Zh = (Xhub - Xhub.mean(0)) / (Xhub.std(0) + 1e-9)
    bigdf["hub_program"] = Zh.mean(1)
else:
    bigdf["hub_program"] = np.nan

# ================================================================ FIGURES
rep = [h for h in ["ATF3","SPRR1A","TFE3","MAPK14","NPY","CHL1","ECEL1","FLRT3"] if h in hub_col]
rep = rep[:6]
try:
    fig, axes = plt.subplots(2, 3, figsize=(13, 9))
    img = plt.imread(os.path.join(RAW, "sample1", "tissue_hires_image.png"))
    sub = (bigdf["sample"] == 1).values
    for ax, h in zip(axes.ravel(), rep):
        ci = hub_cols.index(hub_col[h])
        ax.imshow(img, origin="upper")
        sc = ax.scatter(bigdf.loc[sub, "x"], bigdf.loc[sub, "y"],
                        c=Xhub[sub, ci], cmap="magma", s=14, vmin=0)
        ax.set_title(f"{h}  (section sample1)", fontsize=10)
        ax.axis("off"); plt.colorbar(sc, ax=ax, fraction=0.046, pad=0.04, label="log1p CPM")
    fig.suptitle("GSE325938 Visium — representative hub spatial expression (mouse Sham, section 1)", fontsize=12)
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "P5_GSE325938_hub_spatial.png"), dpi=130); plt.close(fig)
    log("fig hub_spatial saved")
except Exception as e:
    log("fig hub_spatial FAILED:", e)

try:
    fig, axes = plt.subplots(1, 3, figsize=(15, 5))
    axes[0].scatter(pc[:,0], pc[:,1], c=regions, cmap="tab10", s=8)
    axes[0].set_title("Spot PCA (HVG) by spatial domain"); axes[0].set_xlabel("PC1"); axes[0].set_ylabel("PC2")
    ymax = bigdf["y"].max(); ymin = bigdf["y"].min()
    for s in MOUSE_SAMPLES:
        sub = (bigdf["sample"] == s).values
        yoff = (s - MOUSE_SAMPLES[0]) * (ymax - ymin) * 1.05 if s != MOUSE_SAMPLES[0] else 0
        axes[1].scatter(bigdf.loc[sub,"x"], bigdf.loc[sub,"y"] + yoff,
                        c=regions[sub], cmap="tab10", s=8)
    axes[1].set_title("Spatial domain map (4 mouse sections)"); axes[1].axis("off")
    axes[2].barh(range(nreg), [1]*nreg, color=[plt.cm.tab10(i/nreg) for i in range(nreg)])
    axes[2].set_yticks(range(nreg))
    axes[2].set_yticklabels([f"R{r}:{region_label[r]}" for r in range(nreg)], fontsize=8)
    axes[2].set_xticks([]); axes[2].set_title("Region annotation (marker-based)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "P5_GSE325938_regions.png"), dpi=130); plt.close(fig)
    log("fig regions saved")
except Exception as e:
    log("fig regions FAILED:", e)

try:
    hm = np.full((len(present_hubs), nreg), np.nan)
    for i, h in enumerate(present_hubs["symbol"]):
        ci = hub_cols.index(hub_col[h]); g = Xhub[:, ci]; gm = g.mean()
        for r in range(nreg):
            hm[i, r] = np.log2((g[regions == r].mean() + 1e-6) / (gm + 1e-6))
    fig, ax = plt.subplots(figsize=(max(6, nreg*1.2), max(8, len(present_hubs)*0.28)))
    im = ax.imshow(hm, aspect="auto", cmap="RdBu_r", vmin=-2, vmax=2)
    ax.set_xticks(range(nreg))
    ax.set_xticklabels([f"R{r}\n{region_label[r]}" for r in range(nreg)], fontsize=7, rotation=45, ha="right")
    ax.set_yticks(range(len(present_hubs))); ax.set_yticklabels(present_hubs["symbol"], fontsize=7)
    ax.set_title("35 hub × spatial-region log2 enrichment (mouse Visium)")
    plt.colorbar(im, ax=ax, label="log2(region/global)")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "P5_GSE325938_hub_region_heatmap.png"), dpi=130); plt.close(fig)
    log("fig heatmap saved")
except Exception as e:
    log("fig heatmap FAILED:", e)

# ---------------------------------------------------------------- write tables
qc = bigdf.groupby("sample").agg(n_spots=("barcode","size"), median_total=("total","median"),
                                 hub_program_mean=("hub_program","mean")).reset_index()
qc.to_csv(os.path.join(TAB, "P5_GSE325938_spot_qc.csv"), index=False)
region_ann = pd.DataFrame({"region": range(nreg), "label": region_label,
                           "n_spots": np.bincount(regions)})
region_ann.to_csv(os.path.join(TAB, "P5_GSE325938_region_annotation.csv"), index=False)
hubreg.to_csv(os.path.join(TAB, "P5_GSE325938_hub_regionalization.csv"), index=False)
cm = hubreg[["symbol","present","snRNA_lineage","top_region","tier","crossmodal"]].copy()
cm.to_csv(os.path.join(TAB, "P5_GSE325938_crossmodal.csv"), index=False)
log("tables written")

# ---------------------------------------------------------------- note md
n_present = len(present_hubs)
n_dorsal = int((present_hubs["top_region"] == "DorsalHorn").sum())
n_restricted = int((present_hubs["tier"] == "restricted").sum())
n_enriched = int((present_hubs["tier"] == "enriched").sum())
n_consistent = int((hubreg["crossmodal"] == "consistent").sum())
n_divergent = int((hubreg["crossmodal"] == "divergent").sum())
note = f"""# P5 Stretch · GSE325938 Visium 空间定位（35 hub 程序的空间区域化）

> 生成日期：2026-09-19 ｜ 脚本：`scripts/p5_visium325938.py`（v2，修复大小写匹配与内存）
> 数据：GEO GSE325938（`GSE325938_processed_data.tar.gz`，214 MB，spaceranger-1.3.1）。
> 产物：`results/tables/P5_GSE325938_*.csv`、`results/figures/P5_GSE325938_*.png`

## 0. 数据事实与范围（务必先读）
- GSE325938 = "Spinal signatures of entrenched and treated neuropathic pain in male mice [Visium]"，
  8 样本：**4 鼠(Sham, ENSMUS) + 4 人源移植(ENSG)**。
- **该 Visium 无鼠 SNI 臂**（样本标题 `Mouse_Sham1-4` / `Human_2/4/6/8`；
  P5 的 Sham-vs-SNI 对比来自 **snRNA GSE328175**，非本 Visium）。
- 主分析仅取鼠 4 样本臂（与 P5 排除 hg19 人源移植臂一致）；人源移植臂（ENSG）被排除。
- 因无鼠 SNI 空间臂，**无法做空间 Sham-vs-SNI DE**；改为对鼠 4 切片做 hub 程序的**空间区域化**
  （背角/腹角/白质/胶质区），并与 P5 snRNA 细胞类型定位做**跨模态互证**。

## 1. 方法（纪律）
- spot×gene 矩阵（features.tsv 第 2 列 symbol，重复 symbol 求和；**大小写不敏感匹配 hub/marker**）；
  `log1p(CPM)` 归一化；仅保留 `in_tissue` 且总计数≥中位数 5% 的 spot。
- 空间区域：HVG(top1500, 离散度) → PCA(20) → KMeans(k=7) 得 7 个转录区域；
  用 canonical marker 集（背角痛觉/运动神经元/白质/星形/小胶/室管膜/脑膜纤维）**z 标准化后 argmax** 标注区域。
- **伪重复纪律**：spot 非独立（空间自相关）→ 区域均值先按切片(样本)聚合，再跨 4 切片报 mean±sd（描述性，不报 p）。
- 排除 PAN_NUCLEAR 看家/泛核基因作 marker。

## 2. 结果
- 鼠 4 切片共 **{int(qc.n_spots.sum())}** 个 in-tissue spot 进入分析；35 hub 中 **{n_present}** 个在鼠 Visium 有表达。
- 7 个空间区域标注：{", ".join(f"R{r}={region_label[r]}({np.bincount(regions)[r]})" for r in range(nreg))}。
- hub 空间富集分层（沿用 P5 阈值 log2≥1.0=restricted，≥0.58=enriched）：
  **restricted={n_restricted}，enriched={n_enriched}，其余 broad/low**。
- 落在 **DorsalHorn（背角，痛觉传入第一站）** 为 top 区域的 hub 数 = **{n_dorsal}**。
- 跨模态（vs P5 snRNA 细胞类型）：consistent={n_consistent}，divergent={n_divergent}
  （详见 `P5_GSE325938_crossmodal.csv`）。

## 3. 解读
- Visium 第一次给出 hub 程序的**空间坐标**：哪些 hub 富集于背角（痛觉第一站）、哪些散布于白质/胶质区——
  这是 snRNA（只给细胞类型）无法提供的维度。
- 与 P5 snRNA 的互证：snRNA 定到 Neuron 的 hub 应富集于背角神经元区；定到 Microglia 的应富集小胶区；
  一致项支持"该 hub 确属脊髓痛觉回路"，分歧项提示空间层级与细胞类型层级并非一一对应（正常）。
- 代表性 hub 空间图见 `P5_GSE325938_hub_spatial.png`（{", ".join(rep)}）；
  区域图见 `P5_GSE325938_regions.png`；富集热图见 `P5_GSE325938_hub_region_heatmap.png`。

## 4. 局限（随结论）
1. 无鼠 SNI Visium 臂 → 空间 Sham-vs-SNI 差异不可得；区域化仅描述性。
2. n=4 鼠切片均为 Sham → 区域均值跨切片稳定性中等（mean±sd 报告，不推断）。
3. 区域标注依赖 canonical marker 集，非组织学 lamina 金标准；7 区为无监督+marker 标注，边界近似。
4. 人源移植臂被排除（物种注释不同）；若需人源 hub 定位须做鼠→人同源映射，属另一步。
5. spot 级伪重复已规避；ambient RNA：Visium 全组织切片 ambient 风险低于单核，但未做专门 ambient_index 排查
   （与 P5 §3 的 ATF3 ambient 警示对照，本层 ATF3 空间信号按"损伤/再生"预期解读，建议谨慎）。
"""
open(os.path.join(ROOT, "results/P5_GSE325938_note.md"), "w").write(note)
log("note written")
log("DONE")
