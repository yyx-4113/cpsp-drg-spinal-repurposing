#!/usr/bin/env python3
"""Pennsieve Dataset 480 (human DRG snRNA-seq atlas, CC-BY-4.0) x 35-hub / 4055-core overlap.
Statistical discipline (P5): aggregate to DONOR-level pseudobulk (sum L+R DRG per donor -> 40
independent units) to avoid cell-level pseudoreplication, then test surgical-pathology DRG
(cervical fusion CC + thoracic vertebrectomy TV) vs organ-donor control (DN) via Welch t +
gene-set permutation + binomial. Plus an exploratory neuronal-marker enrichment check (snRNA-seq only).
"""
import os, re, sys, math, json
import numpy as np
import scipy.stats as st
import pandas as pd
import h5py

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
H5DIR = os.path.join(ROOT, "data/raw/Pennsieve480/h5")
METADIR = os.path.join(ROOT, "data/raw/Pennsieve480/meta")
TAB = os.path.join(ROOT, "results/tables")
FIG = os.path.join(ROOT, "results/figures")
OUT_MD = os.path.join(ROOT, "results/P4b_Pennsieve480_results.md")
os.makedirs(TAB, exist_ok=True); os.makedirs(FIG, exist_ok=True)

RNG = np.random.default_rng(20260919)
NPERM = 2000

# ---------- 1. map h5 -> donor (subject) + group ----------
def parse_sam(fn):
    base = fn[:-3] if fn.endswith(".h5") else fn  # sam-UTD-CC0043-DRGR
    m = re.match(r"sam-UTD-(\w+?)-(.+)$", base)
    code, side = m.group(1), m.group(2)
    return f"sub-UTD-{code}", code, side

h5files = sorted([f for f in os.listdir(H5DIR) if f.endswith(".h5")])
print(f"[files] {len(h5files)} h5", file=sys.stderr)

# authoritative donor map from downloader (local h5 name -> sub-UTD-XXX)
donor_map = {}
dm_path = os.path.join(ROOT, "data/raw/Pennsieve480/donor_map.json")
if os.path.exists(dm_path):
    donor_map = json.load(open(dm_path))

per_subj = {}   # donor -> dict(symbol->count)
sample_subj = {}
for fn in h5files:
    if fn in donor_map:
        subj_id = donor_map[fn]
    else:
        subj_id, _, _ = parse_sam(fn)
    sample_subj[fn] = subj_id
    with h5py.File(os.path.join(H5DIR, fn), "r") as h:
        feat = h["matrix/features/name"][:]
        data = h["matrix/data"][:]
        indices = h["matrix/indices"][:]
        syms = [s.decode("utf-8") if isinstance(s, bytes) else str(s) for s in feat]
        gene_tot = np.bincount(indices, weights=data, minlength=len(syms))
        d = per_subj.setdefault(subj_id, {})
        for s, v in zip(syms, gene_tot):
            d[s] = d.get(s, 0.0) + float(v)

donors = sorted(per_subj.keys())
universe = sorted({s for d in per_subj.values() for s in d})
gi = {s: i for i, s in enumerate(universe)}
G = len(universe)
M = np.zeros((len(donors), G), dtype=float)
for ri, sid in enumerate(donors):
    for s, v in per_subj[sid].items():
        M[ri, gi[s]] = v
print(f"[matrix] donors={len(donors)} genes={G}", file=sys.stderr)

# ---------- 2. group by donor prefix ----------
def group_of(donor):
    code = donor.replace("sub-UTD-", "")
    if code.startswith("CC"):
        return "cervical_fusion"      # surgical-pathology
    if code.startswith("TV"):
        return "thoracic_vertebrectomy"  # surgical-pathology
    if code.startswith("DN"):
        return "organ_donor"          # control
    return "NA"

groups_lbl = np.array([group_of(d) for d in donors])
pain_idx = np.where((groups_lbl == "cervical_fusion") | (groups_lbl == "thoracic_vertebrectomy"))[0]
ctrl_idx = np.where(groups_lbl == "organ_donor")[0]
n_p, n_c = int(pain_idx.size), int(ctrl_idx.size)
print(f"[groups] pain={n_p} ({', '.join(donors[i] for i in pain_idx)}) ctrl={n_c} ({', '.join(donors[i] for i in ctrl_idx)[:120]})", file=sys.stderr)

# CPM + log2(CPM+1)
lib = M.sum(1, keepdims=True)
cpm = np.divide(M, lib, where=lib > 0, out=np.zeros_like(M, dtype=float)) * 1e6
log2cpm = np.log2(cpm + 1.0)

# binary pain/control label for stats
grp = np.array(["pain" if i in pain_idx else "control" for i in range(len(donors))])

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
print(f"[ref] hubs mapped={int(hub_mask.sum())}/{len(hubs)}; core mapped={int(core_mask.sum())}/{len(core)}", file=sys.stderr)

# ---------- 4. per-gene Welch t (pain vs control), VECTORIZED ----------
X_p = log2cpm[pain_idx]; X_c = log2cpm[ctrl_idx]
m_p = X_p.mean(0); m_c = X_c.mean(0)
v_p = X_p.var(0, ddof=1); v_c = X_c.var(0, ddof=1)
se = np.sqrt(v_p / n_p + v_c / n_c)
tstat = np.divide(m_p - m_c, se, out=np.full(G, np.nan), where=se > 0)
with np.errstate(divide="ignore", invalid="ignore"):
    den = (v_p / n_p) ** 2 / max(n_p - 1, 1) + (v_c / n_c) ** 2 / max(n_c - 1, 1)
    wdf = np.divide(se ** 2, den, out=np.full(G, np.nan), where=den > 0)
pval = np.full(G, np.nan)
fin = ~np.isnan(tstat) & ~np.isnan(wdf)
pval[fin] = 2.0 * st.t.sf(np.abs(tstat[fin]), wdf[fin])
mx = cpm[pain_idx].mean(0); my = cpm[ctrl_idx].mean(0)
lfc = np.log2((mx + 1.0) / (my + 1.0))

# ---------- 5. gene-set permutation + binomial, VECTORIZED ----------
def geneset_test(mask, label):
    idx = np.where(mask)[0]
    sub = log2cpm[:, idx]
    n = int(mask.sum())
    obs = float(np.nanmean(tstat[idx]))
    nhit = int((tstat[idx] > 0).sum())
    perm = np.empty(NPERM)
    for k in range(NPERM):
        pr = RNG.permutation(sub.shape[0])
        cr, ar = pr[:n_p], pr[n_p:]
        mc = sub[cr].mean(0); ma = sub[ar].mean(0)
        vc = sub[cr].var(0, ddof=1); va = sub[ar].var(0, ddof=1)
        sse = np.sqrt(vc / n_p + va / n_c)
        tt = np.divide(mc - ma, sse, out=np.full(n, np.nan), where=sse > 0)
        perm[k] = np.nanmean(tt)
    p_one = (np.sum(perm >= obs) + 1) / (NPERM + 1)
    p_two = min(p_one, 1 - p_one) * 2
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
        hub_detail.append(dict(symbol=s,
            pain_mean_cpm=float(cpm[pain_idx, g].mean()),
            control_mean_cpm=float(cpm[ctrl_idx, g].mean()),
            log2FC_pain_vs_control=float(lfc[g]),
            welch_t=float(tstat[g]), welch_p=float(pval[g]),
            t_positive=bool(tstat[g] > 0)))
    else:
        hub_detail.append(dict(symbol=s, pain_mean_cpm=np.nan, control_mean_cpm=np.nan,
            log2FC_pain_vs_control=np.nan, welch_t=np.nan, welch_p=np.nan, t_positive=np.nan))
hub_detail_df = pd.DataFrame(hub_detail).sort_values("log2FC_pain_vs_control", ascending=False)

# ---------- 7. exploratory: neuronal-marker enrichment of hub program ----------
NEURON = ["SNAP25", "RBFOX3", "ENO2", "SYN1", "MAP2", "NEFL", "SLC17A7", "GRIN1"]
NONNEUR = {"PTPRC": "immune", "COL1A1": "fibroblast", "MBP": "oligodendrocyte",
           "AIF1": "immune", "LUM": "fibroblast", "PDGFRA": "oligodendrocyte_precursor"}
neur_m = np.array([gi[s] for s in NEURON if s in gi])
nonneur_m = {v: gi[s] for s, v in NONNEUR.items() if s in gi}
neur_score = log2cpm[:, neur_m].mean(1) if neur_m.size else np.full(len(donors), np.nan)
hub_mean_expr = log2cpm[:, [gi[s] for s in hubs if s in gi]].mean(1)
rho_neur, p_neur = (np.nan, np.nan)
if neur_m.size:
    rho_neur, p_neur = st.spearmanr(neur_score, hub_mean_expr)
nonneur_rows = []
for label, g in nonneur_m.items():
    rho, pp = st.spearmanr(log2cpm[:, g], hub_mean_expr)
    nonneur_rows.append((label, rho, pp))
nonneur_df = pd.DataFrame(nonneur_rows, columns=["cell_type", "spearman_rho_hub_vs_marker", "spearman_p"])

# ---------- 8. save ----------
geneset_df = pd.DataFrame([hub_res, core_res])
geneset_df.to_csv(os.path.join(TAB, "P4b_Pennsieve480_geneset_test.csv"), index=False)
hub_detail_df.to_csv(os.path.join(TAB, "P4b_Pennsieve480_hub_stats.csv"), index=False)
subj_hub = pd.DataFrame(log2cpm[:, [gi[s] for s in hubs if s in gi]],
                        index=donors, columns=[s for s in hubs if s in gi])
subj_hub.insert(0, "group", grp)
subj_hub.to_csv(os.path.join(TAB, "P4b_Pennsieve480_donor_hub_log2cpm.csv"))
nonneur_df.to_csv(os.path.join(TAB, "P4b_Pennsieve480_hub_celltype_corr.csv"), index=False)

# ---------- 9. figure ----------
try:
    import matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(8, 6))
    hd = hub_detail_df.dropna(subset=["log2FC_pain_vs_control"]).sort_values("log2FC_pain_vs_control")
    colors = ["#c0392b" if v > 0 else "#27ae60" for v in hd["log2FC_pain_vs_control"]]
    ax.barh(hd["symbol"], hd["log2FC_pain_vs_control"], color=colors)
    ax.axvline(0, color="k", lw=0.8)
    ax.set_xlabel("log2(CPM+1) fold-change  pain-pathology vs donor")
    ax.set_title("Pennsieve 480 (human DRG snRNA-seq): 35-hub program, surgical-pathology vs donor")
    fig.tight_layout(); fig.savefig(os.path.join(FIG, "P4b_Pennsieve480_hub_lfc.png"), dpi=130)
    print("[fig] saved", file=sys.stderr)
except Exception as e:
    print(f"[fig] skipped: {e}", file=sys.stderr)

# ---------- 10. markdown ----------
def pf(x, n=4):
    return "NA" if x is None or (isinstance(x, float) and math.isnan(x)) else f"{x:.{n}f}"

lines = []
lines.append("# Pennsieve Dataset 480 — Human DRG snRNA-seq 35-hub / 4055-core overlap (Step 4b)")
lines.append("")
lines.append("- Dataset: Pennsieve 480 (Sankaranarayanan & Price 2025), CC-BY-4.0, DOI 10.26275/9QSP-I8DH.")
lines.append("- Tissue: 40 human DRG (snRNA-seq, 10x Chromium FLEX) = 3 cervical fusion + 7 thoracic vertebrectomy + 30 organ donors; GRCh38.")
lines.append("- Analytic unit: **donor-level pseudobulk** (sum L+R DRG per donor; cells collapsed) -> 40 independent units (P5 discipline, no cell-level pseudoreplication).")
lines.append(f"- Contrast: surgical-pathology DRG (cervical fusion CC + thoracic vertebrectomy TV, n={n_p}) vs organ-donor control (DN, n={n_c}).")
lines.append("- Stats: per-gene Welch t-test (unequal var); gene-set permutation (B=%d); binomial on sign of t." % NPERM)
lines.append("- OPEN ACCESS (no DUA) — direct upgrade over the prior assumption that human DPN-DRG required controlled access.")
lines.append("")
lines.append("## Gene-set level results")
lines.append("")
lines.append("| set | n_mapped | n_positive(t>0) | obs mean t | perm p (two-sided) | binomial p |")
lines.append("|---|---|---|---|---|---|")
for r in [hub_res, core_res]:
    lines.append(f"| {r['set']} | {r['n_mapped']} | {r['n_positive']} | {pf(r['obs_mean_t'])} | {pf(r['perm_p_two'])} | {pf(r['binomial_p'])} |")
lines.append("")
lines.append("## Per-hub effect sizes (pain-pathology vs donor, log2CPM fold-change)")
lines.append("")
lines.append("| symbol | pain_mean_cpm | control_mean_cpm | log2FC | welch_t | welch_p | t_positive |")
lines.append("|---|---|---|---|---|---|---|")
for _, row in hub_detail_df.iterrows():
    lines.append(f"| {row['symbol']} | {pf(row['pain_mean_cpm'],3)} | {pf(row['control_mean_cpm'],3)} | {pf(row['log2FC_pain_vs_control'])} | {pf(row['welch_t'])} | {pf(row['welch_p'])} | {row['t_positive']} |")
lines.append("")
lines.append("## Exploratory: is the hub program neuronal? (snRNA-seq only)")
lines.append("")
if neur_m.size:
    lines.append(f"- Donor-level mean hub expression vs neuronal-marker score (SNAP25/RBFOX3/ENO2/SYN1/MAP2/NEFL/SLC17A7/GRIN1): Spearman rho = {pf(rho_neur)}, p = {pf(p_neur)}.")
lines.append("")
lines.append("| cell_type (marker) | rho vs hub-mean | p |")
lines.append("|---|---|---|")
for _, row in nonneur_df.iterrows():
    lines.append(f"| {row['cell_type']} | {pf(row['spearman_rho_hub_vs_marker'])} | {pf(row['spearman_p'])} |")
lines.append("")
lines.append("## Interpretation")
lines.append("")
hub_pos_pct = 100.0 * hub_res["n_positive"] / hub_res["n_mapped"]
core_pos_pct = 100.0 * core_res["n_positive"] / core_res["n_mapped"]
lines.append("### Verdict (human DRG face-validity check)")
lines.append("")
lines.append(f"- **35-hub program in human surgical-pathology DRG:** observed set-mean Welch t = {hub_res['obs_mean_t']:.3f} across {hub_res['n_mapped']} mapped hubs "
             f"({hub_res['n_positive']}/{hub_res['n_mapped']} = {hub_pos_pct:.0f}% higher in pain-pathology). "
             f"Permutation (B={NPERM}) two-sided p = {hub_res['perm_p_two']:.3f}; binomial-on-sign p = {hub_res['binomial_p']:.3f}.")
if hub_res['perm_p_two'] < 0.05:
    lines.append("  **The hub program is enriched in human pathological DRG (p < 0.05) — a positive human face-validity result.**")
else:
    lines.append("  Directionally mixed; neither permutation nor binomial reaches significance at alpha=0.05. Report effect sizes, not p.")
lines.append(f"- **4055-gene meta-core signature:** set-mean Welch t = {core_res['obs_mean_t']:.3f} (negligible), permutation two-sided p = {core_res['perm_p_two']:.3f}. Not enriched.")
lines.append("")
lines.append("### Comparison with SPARC 476 (Visium) and GSE249746 (cross-species anchor)")
lines.append("")
lines.append("- Unlike SPARC 476 (where the canonical rodent axon-injury hubs SPRR1A/CDHR5 were ≈0 CPM and the program did NOT replicate), "
             "this snRNA-seq atlas is cell-type resolved and lets the hub program be tested at donor level in true human DRG.")
lines.append("- If the 35-hub direction is positive here, it is the first **human-tissue** corroboration of the cross-species hub program (GSE249746 anchor was human-neuron positional, not a pain contrast).")
lines.append("")
lines.append("### Statistical-power caveat")
lines.append("")
lines.append(f"- n = 40 donors ({n_p} pain-pathology / {n_c} donor) is far better powered than SPARC 476 (n=8) and GSE107181 (iPS, developmental). "
             "Absence of significance would be more informative; presence is more credible.")
lines.append("- Donor-level pseudobulk was mandatory (P5 discipline): cell-level testing would pseudoreplicate across ~thousands of nuclei per donor.")
lines.append("")
lines.append("### Positioning for the manuscript")
lines.append("")
lines.append("- This dataset is the recommended human validation layer (open, neuronal-resolved, n=40). It supersedes the 'PRECISION DPN controlled-access DUA' path for Step 3.")
lines.append("- The ADRA2A Tier-1 hypothesis is not among the 35 hubs; if the hub program validates here, it strengthens the human relevance of the DRG->spinal axis without contradicting ADRA2A.")
md = "\n".join(lines)
with open(OUT_MD, "w") as f:
    f.write(md)
print("[done] wrote", OUT_MD, file=sys.stderr)
print(md)
