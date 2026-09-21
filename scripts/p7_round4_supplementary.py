#!/usr/bin/env python3
# p7_round4_supplementary.py -- Round-4 review remediation: the four "must-add-analysis" items.
#
#   T1-7  Random-effects (DerSimonian-Laird) alternative to the fixed-effect Stouffer meta,
#         with tau^2 / I^2 heterogeneity; core redefined under RE; gene sets recomputed under RE.
#   T1-8  Translation concordance reframed as an EFFECT SIZE (Wilson CI, empirical/permutation
#         null) instead of a binomial p against an arbitrary 50%.
#   T1-9  Direction consistency split into nerve_injury_consistency vs incision_agreement.
#   T1-10 Set-level Benjamini-Hochberg across the 19 a priori gene sets (permutation p and
#         Stouffer p), which the original analysis never applied.
#
# Reads ONLY raw/processed source files under results/tables (no manuscript, no other review).
# Writes new tables to results/tables/_R4_* and a summary JSON.
import os, json, warnings, numpy as np, pandas as pd
from scipy import stats
warnings.filterwarnings("ignore")

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB  = os.path.join(ROOT, "results/tables")
PROC = os.path.join(ROOT, "data/processed")   # Xtail tables live here (as in p2_deg_meta.py)
SEED = 42
rng  = np.random.default_rng(SEED)

# --- contrasts: (key, source file, n_case, n_ctrl, kind) -------------------------------
BULK = [
    ("GSE267799_SMIR_DRG",  "DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv", 12, 8,  "incision"),
    ("GSE212311_CCI_DRG",   "DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv",           3, 3,  "nerve_injury"),
    ("GSE278227_CCI_DRG",   "DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv",   14, 14, "nerve_injury"),
    ("GSE241361_S1R_DRG",   "DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv",       4, 5,  "nerve_injury"),
]
XTAIL = [
    ("GSE265957_Xtail_DRG_Day4",  "GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv",  2, 2, "nerve_injury"),
    ("GSE265957_Xtail_DRG_Day63", "GSE265957_Xtail_DRG_Day63_SNI_vs_SHM.csv", 2, 2, "nerve_injury"),
]

def bh(p):
    p = np.asarray(p, float); n = len(p); o = np.argsort(p)
    q = np.empty(n); prev = 1.0
    for i in range(n - 1, -1, -1):
        prev = min(prev, p[o[i]] * n / (i + 1)); q[o[i]] = prev
    return np.minimum(q, 1.0)

def wilson(k, n, z=1.959963985):
    if n == 0: return (np.nan, np.nan)
    p = k / n; d = 1 + z*z/n
    c = (p + z*z/(2*n)) / d
    h = z*np.sqrt(p*(1-p)/n + z*z/(4*n*n)) / d
    return (max(0.0, c - h), min(1.0, c + h))

# ======================================================================================
# Load per-contrast Z, reconstructed exactly as in scripts/p2_deg_meta.py
#   bulk : Z = sign(t) * Phi^-1(p/2)
#   xtail: Z = sign(mRNA_log2FC) * Phi^-1(pvalue_final/2)
# ======================================================================================
Ztab, LFCtab, W = {}, {}, {}
for key, fn, n1, n2, kind in BULK:
    d = pd.read_csv(os.path.join(TAB, fn))
    d = d.rename(columns={d.columns[0]: "symbol"})
    d["symbol"] = d["symbol"].astype(str).str.upper()
    d = d.groupby("symbol").mean(numeric_only=True)
    Ztab[key]  = np.sign(d["t"]) * stats.norm.isf(np.clip(d["p"], 1e-300, 1) / 2)
    LFCtab[key] = d["log2FC"]
    W[key] = np.sqrt(n1 * n2 / (n1 + n2))
for key, fn, n1, n2, kind in XTAIL:
    d = pd.read_csv(os.path.join(PROC, fn)).dropna(subset=["gene", "mRNA_log2FC", "pvalue_final"])
    d["symbol"] = d["gene"].astype(str).str.upper()
    d = d.groupby("symbol").mean(numeric_only=True)
    Ztab[key]  = np.sign(d["mRNA_log2FC"]) * stats.norm.isf(np.clip(d["pvalue_final"], 1e-300, 1) / 2)
    LFCtab[key] = d["mRNA_log2FC"]
    W[key] = np.sqrt(n1 * n2 / (n1 + n2))

KEYS  = [k for k, *_ in BULK] + [k for k, *_ in XTAIL]
KIND  = {k: kind for k, _, _, _, kind in BULK + XTAIL}
NI    = [k for k in KEYS if KIND[k] == "nerve_injury"]
INC   = "GSE267799_SMIR_DRG"

Zdf  = pd.DataFrame(Ztab).dropna(how="all")
Ldf  = pd.DataFrame(LFCtab).reindex(Zdf.index)
w    = np.array([W[k] for k in KEYS])                 # Stouffer weight = sqrt(n_eff)
w2   = w ** 2                                          # = n_eff  (inverse-variance weight)

meta = pd.read_csv(os.path.join(TAB, "META_DRG_axis_stouffer.csv")).set_index("symbol")
Zdf  = Zdf.reindex(meta.index)                         # restrict to the published test universe
Ldf  = Ldf.reindex(meta.index)
print(f"[load] genes in published meta universe: {len(Zdf)}; contrasts: {len(KEYS)}")

Z   = Zdf[KEYS].values                                 # (G, K) per-contrast Z
mask = ~np.isnan(Z)
Kper = mask.sum(1)

# ---------------- fixed-effect (reproduce published Stouffer) ----------------
num = np.nansum(Z * w, axis=1); den = np.sqrt(np.nansum(np.where(mask, w2, 0), axis=1))
Z_FE = num / den
p_FE = 2 * stats.norm.sf(np.abs(Z_FE))

# ------------- random-effects (DerSimonian-Laird on the effect scale) --------
# d_i = Z_i / w_i   (standardised effect),  v_i = 1 / w_i^2
D = Z / w
V = 1.0 / w2
iv = np.where(mask, w2, 0.0)                           # 1/v_i
sum_iv  = iv.sum(1)
dFE     = np.nansum(np.where(mask, D * iv, 0), 1) / sum_iv
Q       = np.nansum(np.where(mask, iv * (D - dFE[:, None])**2, 0), 1)
sum_iv2 = (iv ** 2).sum(1)
C       = sum_iv - sum_iv2 / sum_iv
tau2    = np.maximum(0.0, (Q - (Kper - 1)) / np.where(C > 0, C, np.nan))
I2      = np.where(Q > 0, np.maximum(0.0, (Q - (Kper - 1)) / np.where(Q > 0, Q, np.nan)) * 100, 0.0)

wstar = 1.0 / (V + tau2[:, None])                      # RE weights
wstar = np.where(mask, wstar, 0.0)
dRE   = np.nansum(np.where(mask, D * wstar, 0), 1) / wstar.sum(1)
seRE  = 1.0 / np.sqrt(wstar.sum(1))
Z_RE  = dRE / seRE
p_RE  = 2 * stats.norm.sf(np.abs(Z_RE))
FDR_RE = bh(p_FE * 0 + p_RE)

fe = pd.DataFrame({"symbol": Zdf.index, "K": Kper, "Z_FE": Z_FE, "p_FE": p_FE,
                   "Q": Q, "tau2": tau2, "I2": I2, "Z_RE": Z_RE, "p_RE": p_RE,
                   "FDR_RE": FDR_RE})
fe["consistency"] = meta.loc[Zdf.index, "consistency"].values
fe["meta_FDR"]    = meta.loc[Zdf.index, "meta_FDR"].values
fe["FDR_FE"]      = bh(p_FE)

# ---------------- consistency split (T1-9) ----------------
L   = Ldf[KEYS].values
ni_idx = [KEYS.index(k) for k in NI]; inc_idx = KEYS.index(INC)
Lni = L[:, ni_idx]; Linc = L[:, inc_idx]
up_ni = np.nansum(Lni > 0, 1); dn_ni = np.nansum(Lni < 0, 1); K_ni = (~np.isnan(Lni)).sum(1)
fe["nerve_injury_consistency"] = np.where(K_ni >= 3, np.maximum(up_ni, dn_ni) / np.maximum(K_ni, 1), np.nan)
fe["K_nerve_injury"] = K_ni
fe["incision_lfc"] = Linc
fe["incision_measured"] = ~np.isnan(Linc)
fe["incision_agreement"] = np.where(np.isnan(Linc), np.nan,
                                    (np.sign(Linc) == np.sign(np.where(np.isnan(Z_FE), 0, Z_FE))).astype(float))

core_FE = (fe.FDR_FE.values < 0.05) & (fe.consistency.values >= 0.8)
core_RE = (fe.FDR_RE.values < 0.05) & (fe.consistency.values >= 0.8)
print(f"\n[RE] core fixed-effect   n = {core_FE.sum()}")
print(f"[RE] core random-effects n = {core_RE.sum()}")
print(f"[RE] RE core retains {np.sum(core_FE & core_RE)}/{core_FE.sum()} "
      f"= {np.sum(core_FE & core_RE)/core_FE.sum():.1%} of the FE core")
print(f"[RE] heterogeneity: median tau2 = {np.nanmedian(tau2):.3f}; median I2 = {np.nanmedian(I2):.1f}%")
print(f"[RE] genes with I2 > 50% : {np.mean(I2 > 50)*100:.1f}%")
print(f"[RE] genes with tau2 > 0 : {np.mean(tau2 > 0)*100:.1f}%")

fe.to_csv(os.path.join(TAB, "_R4_random_effects_meta.csv"), index=False)

# ---------------- gene sets under RE + set-level BH (T1-10) ----------------
# Recover the a priori member lists verbatim from scripts/p3_genesets.py (single source of truth).
import ast
src = open(os.path.join(ROOT, "scripts/p3_genesets.py"), encoding="utf-8").read()
tree = ast.parse(src)
SETS = None
for node in tree.body:
    if isinstance(node, ast.Assign) and getattr(node.targets[0], "id", None) == "SETS":
        SETS = ast.literal_eval(node.value); break
assert SETS is not None, "could not recover SETS from scripts/p3_genesets.py"
json.dump(SETS, open(os.path.join(TAB, "_R4_geneset_members.json"), "w"), indent=1)

rows = []
if SETS is not None:
    zfe_vec = pd.Series(Z_FE, index=Zdf.index)
    zre_vec = pd.Series(Z_RE, index=Zdf.index)
    NPERM = 2000
    for name, mem in SETS.items():
        mem2 = [g for g in mem if g in zfe_vec.index]
        for scale, vec in (("fixed", zfe_vec), ("random", zre_vec)):
            v = vec.loc[mem2].dropna()
            if len(v) < 2:
                rows.append({"set": name, "scale": scale, "n_present": len(v),
                             "mean_Z": np.nan, "stouffer_Z": np.nan, "perm_p": np.nan}); continue
            mz = v.mean(); sz = v.sum() / np.sqrt(len(v))
            # same-size permutation null on the Stouffer statistic (identical to p3_genesets.py)
            bg = vec.dropna().values
            null = np.array([np.abs(np.sum(rng.choice(bg, len(v), replace=False)) / np.sqrt(len(v)))
                             for _ in range(NPERM)])
            pperm = (np.sum(null >= abs(sz)) + 1) / (NPERM + 1)
            rows.append({"set": name, "scale": scale, "n_present": len(v), "mean_Z": mz,
                         "stouffer_Z": sz, "perm_p": pperm})
    gsx = pd.DataFrame(rows)
    # set-level BH across multi-member sets (Sigma1 is a single-gene marker, excluded)
    out = []
    for scale in ["fixed", "random"]:
        sub = gsx[(gsx.scale == scale) & (gsx.n_present > 1)].copy()
        sub["perm_q"] = bh(sub.perm_p.values)
        sub["stouffer_p"] = 2 * stats.norm.sf(np.abs(sub.stouffer_Z))
        sub["stouffer_q"] = bh(sub.stouffer_p.values)
        sing = gsx[(gsx.scale == scale) & (gsx.n_present <= 1)].copy()
        sing["perm_q"] = np.nan; sing["stouffer_p"] = np.nan; sing["stouffer_q"] = np.nan
        out.append(pd.concat([sub, sing]))
    gsx = pd.concat(out).sort_values(["scale", "perm_p"])
    gsx.to_csv(os.path.join(TAB, "_R4_geneset_setlevel_bh.csv"), index=False)
    print("\n[BH] set-level Benjamini-Hochberg (permutation p):")
    print(gsx[gsx.scale == "fixed"].to_string(index=False, float_format=lambda v: f"{v:.4g}"))
    print("\n[BH] under random effects:")
    print(gsx[gsx.scale == "random"].to_string(index=False, float_format=lambda v: f"{v:.4g}"))
else:
    print("\n[BH] gene-set member list not found; set-level BH deferred.")

# ---------------- translation concordance: effect size + real null (T1-8) ----------------
sig   = (fe.FDR_FE.values < 0.05) & (fe.consistency.values >= 0.6)
core  = core_FE
meas  = fe.incision_measured.values
agr   = fe.incision_agreement.values

def rate(m):
    n = int(np.sum(m & meas)); k = int(np.nansum(agr[m & meas]))
    return k, n, (k / n if n else np.nan)

k_sig,  n_sig,  r_sig  = rate(sig)
k_core, n_core, r_core = rate(core)
k_all,  n_all,  r_all  = rate(np.ones(len(fe), bool))
k_nonsig, n_nonsig, r_nonsig = rate(~sig)

# comparison set: meta-significant but NOT core (0.6 <= consistency < 0.8)
sig_nc = sig & ~core
k_nc, n_nc, r_nc = rate(sig_nc)

lo_sig,  hi_sig  = wilson(k_sig, n_sig)
lo_core, hi_core = wilson(k_core, n_core)
lo_all,  hi_all  = wilson(k_all, n_all)
lo_nc,   hi_nc   = wilson(k_nc, n_nc)

# empirical null: randomly relabel which genes are "meta-significant", keeping n_sig
NP = 5000
pool = np.where(meas)[0]
null_sig = np.empty(NP); null_core = np.empty(NP)
nmeas = len(pool); agr_pool = agr[pool]
for b in range(NP):
    pick = rng.choice(nmeas, n_sig, replace=False); null_sig[b] = np.nanmean(agr_pool[pick])
    pick = rng.choice(nmeas, n_core, replace=False); null_core[b] = np.nanmean(agr_pool[pick])
p_emp_sig  = (np.sum(np.abs(null_sig  - null_sig.mean())  >= abs(r_sig  - null_sig.mean()))  + 1) / (NP + 1)
p_emp_core = (np.sum(np.abs(null_core - null_core.mean()) >= abs(r_core - null_core.mean())) + 1) / (NP + 1)

rd = r_core - r_nc
print("\n[TRANSLATION] effect-size framing (replaces the binomial p vs 50%)")
print(f"  all shared genes                 : {k_all}/{n_all} = {r_all:.1%}  Wilson [{lo_all:.1%}, {hi_all:.1%}]")
print(f"  meta-significant (FDR<.05,c>=.6) : {k_sig}/{n_sig} = {r_sig:.1%}  Wilson [{lo_sig:.1%}, {hi_sig:.1%}]")
print(f"  core (FDR<.05, c>=0.8)           : {k_core}/{n_core} = {r_core:.1%}  Wilson [{lo_core:.1%}, {hi_core:.1%}]")
print(f"  meta-sig but not core (.6<=c<.8) : {k_nc}/{n_nc} = {r_nc:.1%}  Wilson [{lo_nc:.1%}, {hi_nc:.1%}]")
print(f"  risk difference core vs meta-sig-not-core: {rd*100:+.1f} pp")
print(f"  empirical label-permutation null (5,000 draws): sig-rate p={p_emp_sig:.4g}; core-rate p={p_emp_core:.4g}")
print(f"  null SD of the core rate: {null_core.std():.4f}")

tr = pd.DataFrame([
    {"stratum": "all_shared_genes", "k": k_all, "n": n_all, "rate": r_all, "ci_lo": lo_all, "ci_hi": hi_all},
    {"stratum": "meta_significant_FDR05_c06", "k": k_sig, "n": n_sig, "rate": r_sig, "ci_lo": lo_sig, "ci_hi": hi_sig},
    {"stratum": "core_FDR05_c08", "k": k_core, "n": n_core, "rate": r_core, "ci_lo": lo_core, "ci_hi": hi_core},
    {"stratum": "meta_sig_not_core", "k": k_nc, "n": n_nc, "rate": r_nc, "ci_lo": lo_nc, "ci_hi": hi_nc},
])
tr.to_csv(os.path.join(TAB, "_R4_translation_concordance_effectsize.csv"), index=False)

# ---------------- consistency-split summary (T1-9) ----------------
cm = fe[core_FE]
cm_meas = cm[cm.incision_measured]
print("\n[CONSISTENCY SPLIT] within the 4,055-gene core:")
print(f"  core genes with incision measured      : {len(cm_meas)}")
print(f"  ... incision-concordant (agreement=1)  : {int(cm_meas.incision_agreement.sum())} "
      f"= {cm_meas.incision_agreement.mean():.1%}")
print(f"  ... incision-DISCORDANT (core-consistent but incision disagrees): "
      f"{int((cm_meas.incision_agreement==0).sum())} = {(cm_meas.incision_agreement==0).mean():.1%}")
ni_hi = cm[cm.nerve_injury_consistency >= 0.8]
print(f"  core genes with nerve-injury consistency >= 0.8 : {len(ni_hi)}/{len(cm)} = {len(ni_hi)/len(cm):.1%}")
both = cm[(cm.nerve_injury_consistency >= 0.8) & (cm.incision_agreement == 1)]
print(f"  BOTH ni-consistent >=0.8 AND incision-concordant : {len(both)} (CPSP-consistent subset)")
print(f"  mean nerve_injury_consistency in core : {cm.nerve_injury_consistency.mean():.3f} "
      f"(vs pooled consistency {cm.consistency.mean():.3f})")

summary = {
    "n_genes_tested": int(len(fe)),
    "core_fixed_effect": int(core_FE.sum()),
    "core_random_effects": int(core_RE.sum()),
    "RE_retains_of_FE_core": int(np.sum(core_FE & core_RE)),
    "RE_retains_pct": round(float(np.sum(core_FE & core_RE) / core_FE.sum() * 100), 1),
    "median_tau2": round(float(np.nanmedian(tau2)), 3),
    "median_I2_pct": round(float(np.nanmedian(I2)), 1),
    "pct_genes_I2_gt50": round(float(np.mean(I2 > 50) * 100), 1),
    "pct_genes_tau2_gt0": round(float(np.mean(tau2 > 0) * 100), 1),
    "translation": {
        "all_shared": {"k": k_all, "n": n_all, "rate": round(r_all, 4), "ci": [round(lo_all, 4), round(hi_all, 4)]},
        "meta_sig": {"k": k_sig, "n": n_sig, "rate": round(r_sig, 4), "ci": [round(lo_sig, 4), round(hi_sig, 4)],
                     "perm_p": float(p_emp_sig)},
        "core": {"k": k_core, "n": n_core, "rate": round(r_core, 4), "ci": [round(lo_core, 4), round(hi_core, 4)],
                 "perm_p": float(p_emp_core)},
        "meta_sig_not_core": {"k": k_nc, "n": n_nc, "rate": round(r_nc, 4)},
        "risk_difference_core_vs_sig_not_core_pp": round(float(rd * 100), 1),
    },
    "consistency_split": {
        "core_n": int(core_FE.sum()),
        "core_incision_measured": int(len(cm_meas)),
        "core_incision_concordant": int(cm_meas.incision_agreement.sum()),
        "core_incision_concordant_pct": round(float(cm_meas.incision_agreement.mean() * 100), 1),
        "core_incision_discordant": int((cm_meas.incision_agreement == 0).sum()),
        "core_ni_consistency_ge08": int(len(ni_hi)),
        "core_both_ni_ge08_and_incision_concordant": int(len(both)),
        "mean_nerve_injury_consistency_in_core": round(float(cm.nerve_injury_consistency.mean()), 3),
        "mean_pooled_consistency_in_core": round(float(cm.consistency.mean()), 3),
    },
}
json.dump(summary, open(os.path.join(TAB, "_R4_supplementary_summary.json"), "w"), indent=2)
print("\n[written] _R4_random_effects_meta.csv, _R4_geneset_setlevel_bh.csv, "
      "_R4_translation_concordance_effectsize.csv, _R4_supplementary_summary.json")
