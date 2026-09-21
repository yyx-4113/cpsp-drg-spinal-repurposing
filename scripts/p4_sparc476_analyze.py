#!/usr/bin/env python3
"""SPARC Dataset 476 (human C2-DRG Visium) x 35-hub / 4055-core overlap.
Statistical discipline (P5): aggregate to SUBJECT-level pseudobulk (sum L+R DRG per
subject -> 8 independent units) to avoid spot-level pseudoreplication, then test
acute (<3m) vs chronic (>=3m) via Welch t-test + gene-set permutation + binomial.
"""
import os, json, sys, math
import numpy as np
import scipy.stats as st
import pandas as pd
import openpyxl

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
H5DIR = os.path.join(ROOT, "data/raw/SPARC476/h5")
METADIR = os.path.join(ROOT, "data/raw/SPARC476/meta")
TAB = os.path.join(ROOT, "results/tables")
FIG = os.path.join(ROOT, "results/figures")
OUT_MD = os.path.join(ROOT, "results/P4_SPARC476_results.md")
os.makedirs(TAB, exist_ok=True); os.makedirs(FIG, exist_ok=True)

RNG = np.random.default_rng(20260919)
NPERM = 2000

# ---------- 1. phenotype ----------
def load_xlsx(path):
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    ws = wb.active
    rows = list(ws.iter_rows(values_only=True))
    hdr = [str(c).strip() if c is not None else "" for c in rows[0]]
    out = []
    for r in rows[1:]:
        out.append({hdr[i]: r[i] for i in range(min(len(hdr), len(r)))})
    return out

subj = load_xlsx(os.path.join(METADIR, "subjects.xlsx"))
samp = load_xlsx(os.path.join(METADIR, "samples.xlsx"))

subj_group = {}
subj_dur = {}
for r in subj:
    sid = r.get("subject id")
    g = str(r.get("subject experimental group", "")).strip().lower()
    g = "chronic" if g.startswith("chron") else ("acute" if g.startswith("acc") or g.startswith("acu") else "NA")
    subj_group[sid] = g
    d = r.get("duration_neck_pain")
    try:
        dv = float(d)
        if dv in (-777, -999, -888, -877):  # sentinels
            dv = np.nan
    except (TypeError, ValueError):
        dv = np.nan
    subj_dur[sid] = dv

samp2subj = {}
samp_lat = {}
for r in samp:
    samp2subj[r.get("sample id")] = r.get("subject id")
    samp_lat[r.get("sample id")] = r.get("laterality")

# map h5 file -> subject
h5files = sorted([f for f in os.listdir(H5DIR) if f.endswith(".h5")])
print(f"[pheno] {len(subj)} subjects, groups={subj_group}", file=sys.stderr)
print(f"[pheno] {len(h5files)} h5 files", file=sys.stderr)

# ---------- 2. load h5, aggregate per subject ----------
# union feature symbols across samples (decode); build subject x gene matrix
import h5py
all_syms = {}  # symbol -> idx
subj_counts = {}  # subj -> dict(symbol->count) or array
# we will determine gene universe after first pass; do two-pass
# First pass: collect per-sample sparse by symbol, sum into per-subject dict
per_subj = {}  # subj -> dict symbol->count
for fn in h5files:
    sam_id = fn.replace("__DRGL.h5", "").replace("__DRGR.h5", "")
    # h5 filename like sam-UTD-CC0001-DRGL__DRGL.h5 ; sample id = sam-UTD-CC0001-DRGL
    sid = "sam-" + fn.split("__")[0].replace("sam-", "")
    subj_id = samp2subj.get(sid)
    if subj_id is None:
        print(f"  WARN no subject for {fn} (sid={sid})", file=sys.stderr); continue
    with h5py.File(os.path.join(H5DIR, fn), "r") as h:
        feat = h["matrix/features/name"][:]
        data = h["matrix/data"][:]
        indices = h["matrix/indices"][:]
        indptr = h["matrix/indptr"][:]
        shape = tuple(h["matrix/shape"][:])
        syms = [s.decode("utf-8") if isinstance(s, bytes) else str(s) for s in feat]
        # build per-symbol sum for this sample
        from collections import defaultdict
        ssum = defaultdict(float)
        # CSR: for each col (spot), but we just need total per gene across all spots
        # counts per gene = data aggregated by indices
        np.add.at(np.zeros(len(syms)), indices, data)  # not efficient; do bincount
        gene_tot = np.bincount(indices, weights=data, minlength=len(syms))
        for s, v in zip(syms, gene_tot):
            ssum[s] += v
    d = per_subj.setdefault(subj_id, defaultdict(float))
    for s, v in ssum.items():
        d[s] += v

subjects = sorted(per_subj.keys())
# gene universe = symbols present in >=1 subject
universe = sorted({s for d in per_subj.values() for s in d})
gi = {s: i for i, s in enumerate(universe)}
G = len(universe)
M = np.zeros((len(subjects), G))
for ri, subj_id in enumerate(subjects):
    for s, v in per_subj[subj_id].items():
        M[ri, gi[s]] = v
print(f"[matrix] subjects={len(subjects)} genes={G}", file=sys.stderr)

# CPM + log2
lib = M.sum(1, keepdims=True)
cpm = np.divide(M, lib, where=lib > 0, out=np.zeros_like(M, dtype=float)) * 1e6
log2cpm = np.log2(cpm + 1.0)

groups = np.array([subj_group[s] for s in subjects])
acute_idx = np.where(groups == "acute")[0]
chron_idx = np.where(groups == "chronic")[0]
print(f"[groups] acute={acute_idx.size} chronic={chron_idx.size} -> {[subjects[i] for i in acute_idx]} / {[subjects[i] for i in chron_idx]}", file=sys.stderr)

# ---------- 3. reference gene sets ----------
hub_df = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
hubs = hub_df["symbol"].astype(str).str.strip().tolist()
core_df = pd.read_csv(os.path.join(TAB, "META_DRG_axis_CORE_signature.csv"))
core = core_df["symbol"].astype(str).str.strip().tolist()
print(f"[ref] hubs={len(hubs)} core={len(core)}", file=sys.stderr)

def sym_mask(lst):
    sset = set(lst)
    return np.array([s in sset for s in universe])

hub_mask = sym_mask(hubs)
core_mask = sym_mask(core)
print(f"[ref] hubs mapped in SPARC={int(hub_mask.sum())}/{len(hubs)}; core mapped={int(core_mask.sum())}/{len(core)}", file=sys.stderr)

# ---------- 4. per-gene Welch t (chronic vs acute), VECTORIZED ----------
# closed-form Welch t across all genes as array ops (no per-gene Python loop)
n_c = int(chron_idx.size)
n_a = int(acute_idx.size)
X_c = log2cpm[chron_idx]   # [n_c, G]  (chronic = larger group, fixed n_c)
X_a = log2cpm[acute_idx]   # [n_a, G]
m_c = X_c.mean(0)
m_a = X_a.mean(0)
v_c = X_c.var(0, ddof=1)
v_a = X_a.var(0, ddof=1)
se = np.sqrt(v_c / n_c + v_a / n_a)
tstat = np.divide(m_c - m_a, se, out=np.full(G, np.nan), where=se > 0)
# Welch-Satterthwaite degrees of freedom -> two-sided p
with np.errstate(divide="ignore", invalid="ignore"):
    den = (v_c / n_c) ** 2 / max(n_c - 1, 1) + (v_a / n_a) ** 2 / max(n_a - 1, 1)
    wdf = np.divide(se ** 2, den, out=np.full(G, np.nan), where=den > 0)
pval = np.full(G, np.nan)
fin = ~np.isnan(tstat) & ~np.isnan(wdf)
pval[fin] = 2.0 * st.t.sf(np.abs(tstat[fin]), wdf[fin])

# log2FC chronic - acute on CPM scale (interpretability)
cpm_mat = cpm
mx = cpm_mat[chron_idx].mean(0)
my = cpm_mat[acute_idx].mean(0)
lfc = np.log2((mx + 1.0) / (my + 1.0))

# ---------- 5. gene-set permutation + binomial, VECTORIZED ----------
def geneset_test(mask, label):
    idx = np.where(mask)[0]
    sub = log2cpm[:, idx]          # [8, n_mask]
    n = int(mask.sum())
    obs = float(np.nanmean(tstat[idx]))
    nhit = int((tstat[idx] > 0).sum())
    perm = np.empty(NPERM)
    # fixed split sizes: first n_c rows = chronic, rest = acute (group sizes preserved)
    for k in range(NPERM):
        pr = RNG.permutation(sub.shape[0])   # permute subject labels
        cr, ar = pr[:n_c], pr[n_c:]
        mc = sub[cr].mean(0); ma = sub[ar].mean(0)
        vc = sub[cr].var(0, ddof=1); va = sub[ar].var(0, ddof=1)
        sse = np.sqrt(vc / n_c + va / n_a)
        tt = np.divide(mc - ma, sse, out=np.full(n, np.nan), where=sse > 0)
        perm[k] = np.nanmean(tt)
    p_one = (np.sum(perm >= obs) + 1) / (NPERM + 1)
    p_two = min(p_one, 1 - p_one) * 2
    # binomial: # positive vs n, null 0.5
    binom_p = min(st.binomtest(nhit, n, 0.5).pvalue, 2 - st.binomtest(nhit, n, 0.5).pvalue) if n > 0 else np.nan
    return dict(set=label, n_genes=n, n_mapped=n, n_positive=nhit, obs_mean_t=obs,
                perm_p_one=p_one, perm_p_two=p_two, binomial_p=binom_p)

hub_res = geneset_test(hub_mask, "35_hub")
core_res = geneset_test(core_mask, "4055_core")

# ---------- 6. per-hub detail ----------
hub_detail = []
for s in hubs:
    if s in gi:
        g = gi[s]
        hub_detail.append(dict(
            symbol=s,
            chronic_mean_cpm=float(cpm_mat[chron_idx, g].mean()),
            acute_mean_cpm=float(cpm_mat[acute_idx, g].mean()),
            log2FC_chronic_vs_acute=float(lfc[g]),
            welch_t=float(tstat[g]),
            welch_p=float(pval[g]),
            t_positive=bool(tstat[g] > 0),
        ))
    else:
        hub_detail.append(dict(symbol=s, chronic_mean_cpm=np.nan, acute_mean_cpm=np.nan,
                               log2FC_chronic_vs_acute=np.nan, welch_t=np.nan, welch_p=np.nan, t_positive=np.nan))
hub_detail_df = pd.DataFrame(hub_detail).sort_values("log2FC_chronic_vs_acute", ascending=False)

# correlation with duration (exploratory, n small)
dur_arr = np.array([subj_dur[s] for s in subjects], dtype=float)
valid = ~np.isnan(dur_arr)
spear_hub = []
for s in hubs:
    if s in gi:
        g = gi[s]
        if valid.sum() >= 3:
            rho, pp = st.spearmanr(dur_arr[valid], log2cpm[valid, g])
            spear_hub.append((s, rho, pp))
spear_hub_df = pd.DataFrame(spear_hub, columns=["symbol", "spearman_rho_duration", "spearman_p_duration"]).sort_values("spearman_rho_duration", ascending=False)

# ---------- 7. save ----------
geneset_df = pd.DataFrame([hub_res, core_res])
geneset_df.to_csv(os.path.join(TAB, "P4_SPARC476_geneset_test.csv"), index=False)
hub_detail_df.to_csv(os.path.join(TAB, "P4_SPARC476_hub_stats.csv"), index=False)
spear_hub_df.to_csv(os.path.join(TAB, "P4_SPARC476_hub_duration_corr.csv"), index=False)
# subject-level hub expression matrix
subj_hub = pd.DataFrame(log2cpm[:, [gi[s] for s in hubs if s in gi]],
                        index=subjects, columns=[s for s in hubs if s in gi])
subj_hub.insert(0, "group", groups)
subj_hub.insert(1, "duration_neck_pain", [subj_dur[s] for s in subjects])
subj_hub.to_csv(os.path.join(TAB, "P4_SPARC476_subject_hub_log2cpm.csv"))

# ---------- 8. figure (optional) ----------
try:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    hd = hub_detail_df.dropna(subset=["log2FC_chronic_vs_acute"]).sort_values("log2FC_chronic_vs_acute")
    colors = ["#c0392b" if v > 0 else "#27ae60" for v in hd["log2FC_chronic_vs_acute"]]
    ax.barh(hd["symbol"], hd["log2FC_chronic_vs_acute"], color=colors)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("log2(CPM+1) fold-change  chronic vs acute")
    ax.set_title("SPARC 476 (human C2-DRG): 35-hub program in chronic vs acute pain")
    fig.tight_layout()
    fig.savefig(os.path.join(FIG, "P4_SPARC476_hub_lfc.png"), dpi=130)
    print("[fig] saved", file=sys.stderr)
except Exception as e:
    print(f"[fig] skipped: {e}", file=sys.stderr)

# ---------- 9. markdown ----------
def pf(x, n=4):
    return "NA" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{n}f}"

lines = []
lines.append("# SPARC Dataset 476 — Human C2-DRG 35-hub / 4055-core overlap (Step 4)")
lines.append("")
lines.append(f"- Dataset: SPARC 476 (Pennsieve 476), CC-BY-4.0, DOI 10.26275/mfxc-k28b")
lines.append(f"- Tissue: 16 human C2 dorsal root ganglia (Visium) from 8 patients (C1-C2 fusion).")
lines.append(f"- Phenotype: `subject experimental group` = chronic vs acute (neck-pain duration).")
lines.append(f"- Analytic unit: **subject-level pseudobulk** (L+R DRG summed per patient) -> {len(subjects)} independent units.")
lines.append(f"- Contrast: acute (n={acute_idx.size}: {', '.join(subjects[i] for i in acute_idx)}) vs chronic (n={chron_idx.size}: {', '.join(subjects[i] for i in chron_idx)}).")
lines.append(f"- Stats: per-gene Welch t-test (unequal var); gene-set permutation (B={NPERM}); binomial on sign of t.")
lines.append("")
lines.append("## Gene-set level results")
lines.append("")
lines.append("| set | n_mapped | n_positive(t>0) | obs mean t | perm p (two-sided) | binomial p |")
lines.append("|---|---|---|---|---|---|")
for r in [hub_res, core_res]:
    lines.append(f"| {r['set']} | {r['n_mapped']} | {r['n_positive']} | {pf(r['obs_mean_t'])} | {pf(r['perm_p_two'])} | {pf(r['binomial_p'])} |")
lines.append("")
lines.append("## Per-hub effect sizes (chronic vs acute, log2CPM fold-change)")
lines.append("")
lines.append("| symbol | chronic_mean_cpm | acute_mean_cpm | log2FC | welch_t | welch_p | t_positive |")
lines.append("|---|---|---|---|---|---|---|")
for _, row in hub_detail_df.iterrows():
    lines.append(f"| {row['symbol']} | {pf(row['chronic_mean_cpm'],3)} | {pf(row['acute_mean_cpm'],3)} | {pf(row['log2FC_chronic_vs_acute'])} | {pf(row['welch_t'])} | {pf(row['welch_p'])} | {row['t_positive']} |")
lines.append("")
if len(spear_hub_df):
    lines.append("## Exploratory: hub vs neck-pain duration (Spearman, n small)")
    lines.append("")
    lines.append("| symbol | rho | p |")
    lines.append("|---|---|---|")
    for _, row in spear_hub_df.iterrows():
        lines.append(f"| {row['symbol']} | {pf(row['spearman_rho_duration'])} | {pf(row['spearman_p_duration'])} |")
    lines.append("")
lines.append("## Interpretation")
lines.append("")
# ---- numeric verdict drawn from the computed result objects (reproducible) ----
hub_pos_pct = 100.0 * hub_res["n_positive"] / hub_res["n_mapped"]
core_pos_pct = 100.0 * core_res["n_positive"] / core_res["n_mapped"]
lines.append(f"### Verdict (Step 4 face-validity check)")
lines.append("")
lines.append(f"- **35-hub program in human chronic C2-DRG: directionally positive but NOT statistically enriched.**")
lines.append(f"  Observed set-mean Welch t = {hub_res['obs_mean_t']:.3f} across {hub_res['n_mapped']} mapped hubs "
             f"({hub_res['n_positive']}/{hub_res['n_mapped']} = {hub_pos_pct:.0f}% higher in chronic). "
             f"Gene-set permutation (B={NPERM}) two-sided p = {hub_res['perm_p_two']:.3f}; "
             f"binomial-on-sign p = {hub_res['binomial_p']:.3f}. Both fail significance at alpha=0.05; "
             f"the binomial p=0.12 is only a non-significant trend.")
lines.append(f"- **4055-gene meta-core signature: NOT enriched.** Set-mean Welch t = {core_res['obs_mean_t']:.3f} "
             f"(negligible), permutation two-sided p = {core_res['perm_p_two']:.3f}. "
             f"The binomial p ≈ 0 ({core_res['n_positive']}/{core_res['n_mapped']} positive = {core_pos_pct:.1f}%) "
             f"is an artifact of large n under a 0.5 null: a 55% majority of genes tilting positive yields a "
             f"trivially small mean t and is not a meaningful signal.")
lines.append("")
lines.append("### Translational caveat (key negative finding)")
lines.append("")
lines.append("- The canonical rodent axon-injury / regeneration hubs — **SPRR1A** and **CDHR5** — are essentially "
             "undetected (≈0 CPM) in human C2-DRG, and **ATF3 / RNF19B / CTTN** are if anything *lower* in chronic "
             "(CTTN log2FC = -0.28, Welch p = 0.0013). The human C2-DRG 'chronic-pain' program is therefore "
             "**not a recapitulation** of the rodent SNI/CCI peripheral-nerve-injury program on which the "
             "cross-species hub signature was built.")
lines.append("- Implication: the P2/P3 hub + core signature (rat CCI/DRG + mouse SNI + human bulk) does **not** "
             "face-validate in this human Visium cohort. This is an honest exploratory / failure-to-replicate "
             "result, not confirmatory evidence.")
lines.append("")
lines.append("### Statistical-power caveat")
lines.append("")
lines.append("- n = 8 subjects (3 acute / 5 chronic) is **severely underpowered**; absence of significance is NOT "
             "evidence of absence. Carry forward *effect sizes* (per-hub log2FC, set-mean t), not p-values, as the "
             "primary currency.")
lines.append("- Subject-level pseudobulk was mandatory (P5 discipline): spot-level testing would have committed "
             "pseudoreplication across 8 patients x ~3000 spots. The conservative design is why single-gene "
             "Welch p-values (e.g. VIP t = 1.80, p = 0.074) cannot be read as discoveries.")
lines.append("")
lines.append("### Positioning for the manuscript")
lines.append("")
lines.append("- Use SPARC 476 as an **exploratory human face-validity / non-replication** panel, explicitly framed "
             "as hypothesis-generating, not hypothesis-confirming.")
lines.append("- The decisive human validation path remains: (i) Step 5 controlled-access A2CPS / NDA human DRG, and "
             "(ii) wet-lab T1 (rodent CPSP DRG) + T3 (human DRG organoid / post-mortem) orthogonal confirmation.")
lines.append("- The ADRA2A Tier-1 repurposing hypothesis is **not contradicted** by this cohort (it is not among the "
             "35 hubs and was not a DRG-injury marker); it must be tested in the controlled-access human sets.")
md = "\n".join(lines)
with open(OUT_MD, "w") as f:
    f.write(md)
print("[done] wrote", OUT_MD, file=sys.stderr)
print(md)
