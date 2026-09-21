#!/usr/bin/env python3
# p7b_translation_noncircular.py -- Round-4 remediation: T1-8 / T1-9 addendum.
#
# The published concordance statistic has a CIRCULARITY problem that the Round-4 panel
# implied (T1-9) but did not compute: the pooled "direction consistency >= 0.8" filter is
# taken across all 6 contrasts, ONE OF WHICH IS THE INCISION CONTRAST ITSELF. Any gene
# entering the 4,055-gene core has therefore already been selected for agreeing with the
# incision direction, so "69.5% of the core translates to incision" is partly guaranteed by
# construction.
#
# This script computes the NON-CIRCULAR version: select genes by nerve-injury consistency
# only (the 5 nerve-injury contrasts, incision excluded), then ask how often the incision
# contrast agrees. Wilson CIs and a label-permutation null are supplied for every stratum.
#
# It also reports the 35 hubs / 10 docking targets under the random-effects meta (T1-7).
import os, json, numpy as np, pandas as pd
from scipy import stats

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB  = os.path.join(ROOT, "results/tables")
rng  = np.random.default_rng(42)

fe  = pd.read_csv(os.path.join(TAB, "_R4_random_effects_meta.csv"))
pub = pd.read_csv(os.path.join(TAB, "META_DRG_axis_stouffer.csv"))

# ---- reconcile: recompute the published strata straight off the published CSV ----
p = pub.set_index("symbol")
meas = p["lfc_GSE267799_SMIR_DRG"].notna()
concord = (np.sign(p["meta_Z"]) == np.sign(p["lfc_GSE267799_SMIR_DRG"]))
print("[reconcile] straight from META_DRG_axis_stouffer.csv")
print(f"  genes total                       : {len(p)}")
print(f"  genes with incision measured      : {meas.sum()}")
print(f"  concordant among ALL measured     : {int(concord[meas].sum())}/{int(meas.sum())} = {concord[meas].mean():.1%}")
sig = (p["meta_FDR"] < 0.05) & (p["consistency"] >= 0.6)
print(f"  meta_FDR<0.05 & consistency>=0.6  : {int((sig&meas).sum())} measured; concordant {int(concord[sig&meas].sum())}/{int((sig&meas).sum())} = {concord[sig&meas].mean():.1%}")
core = (p["meta_FDR"] < 0.05) & (p["consistency"] >= 0.8)
print(f"  core (consistency>=0.8)           : {int((core&meas).sum())} measured; concordant {int(concord[core&meas].sum())}/{int((core&meas).sum())} = {concord[core&meas].mean():.1%}")

# ---- non-circular strata using the R4 table ----
f = fe.set_index("symbol")
def wilson(k, n, z=1.959963985):
    if n == 0: return (np.nan, np.nan)
    ph = k / n; d = 1 + z*z/n
    c = (ph + z*z/(2*n)) / d
    h = z*np.sqrt(ph*(1-ph)/n + z*z/(4*n*n)) / d
    return (max(0.0, c-h), min(1.0, c+h))

NIge = f["nerve_injury_consistency"] >= 0.8
Kni  = f["K_nerve_injury"] >= 3
meas = f["incision_measured"]
agr  = f["incision_agreement"].astype(float)

strata = {
    "all_measured":            meas,
    "meta_FDR05_NIcons_ge08":  meas & (f["FDR_RE"]*0 + (f["meta_FDR"] < 0.05)) & NIge & Kni,
    "meta_FDR05_NIcons_lt08":  meas & (f["meta_FDR"] < 0.05) & (~NIge) & Kni,
    "meta_FDR05_pooled_ge08":  meas & (f["meta_FDR"] < 0.05) & (f["consistency"] >= 0.8),
}
rows = []
NP = 5000
pool = np.where(meas.values)[0]; agrp = agr.values[pool]
res = {}
for name, m in strata.items():
    m = m.values
    n = int(m.sum()); k = int(np.nansum(agr.values[m]))
    r = k / n if n else np.nan
    lo, hi = wilson(k, n)
    null = np.array([np.nanmean(agrp[rng.choice(len(pool), n, replace=False)]) for _ in range(NP)])
    pperm = (np.sum(np.abs(null - null.mean()) >= abs(r - null.mean())) + 1) / (NP + 1)
    rows.append({"stratum": name, "k": k, "n": n, "rate": r, "ci_lo": lo, "ci_hi": hi,
                 "perm_p_vs_measured_background": pperm})
    res[name] = {"k": k, "n": n, "rate": round(r, 4), "ci": [round(lo,4), round(hi,4)], "perm_p": float(pperm)}
    print(f"\n[{name}]  {k}/{n} = {r:.1%}  Wilson [{lo:.1%}, {hi:.1%}]  perm p={pperm:.4g}")

rd = res["meta_FDR05_NIcons_ge08"]["rate"] - res["meta_FDR05_NIcons_lt08"]["rate"]
print(f"\n[NON-CIRCULAR risk difference] NI-consistent>=0.8 minus NI-inconsistent: {rd*100:+.1f} pp")
rnd = res["meta_FDR05_pooled_ge08"]["rate"] - res["meta_FDR05_NIcons_ge08"]["rate"]
print(f"[circularity inflation] pooled(core) minus NI-only: {rnd*100:+.1f} pp")
print(f"[core genes that are NI-consistent but incision-DISCORDANT]: "
      f"{int(np.nansum((agr.values==0)[(meas & NIge & Kni & (f['meta_FDR']<0.05)).values]))}")

# ---- hubs / docking targets under random effects ----
hub = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
sub = f.reindex(hub.symbol)
print("\n[35 hubs under random-effects meta]")
print(f"  p_RE < 0.05 : {int((sub.p_RE < 0.05).sum())}/35     FDR_RE < 0.05 : {int((sub.FDR_RE < 0.05).sum())}/35")
print(f"  p_FE < 0.05 : {int((sub.p_FE < 0.05).sum())}/35     FDR_FE < 0.05 : {int((sub.FDR_FE < 0.05).sum())}/35")
print(f"  median I2 across hubs: {np.nanmedian(sub.I2):.1f}%")

TRG = ["TNIK","SLC2A1","ACVR1","SERPINE1","MAPK14","AXL","VASH2","GALNS","ITPKC","ADRA2A"]
t = f.reindex(TRG)[["Z_FE","p_FE","FDR_FE","Z_RE","p_RE","FDR_RE","I2","tau2","consistency","nerve_injury_consistency","incision_agreement"]]
print("\n[10 docking targets: fixed vs random effects]")
print(t.round(4).to_string())

json.dump({"strata": res,
           "noncircular_risk_difference_pp": round(rd*100, 1),
           "circularity_inflation_pp": round(rnd*100, 1),
           "hubs_p_RE_lt05": int((sub.p_RE < 0.05).sum()),
           "hubs_FDR_RE_lt05": int((sub.FDR_RE < 0.05).sum()),
           "hubs_p_FE_lt05": int((sub.p_FE < 0.05).sum()),
           "hubs_median_I2": round(float(np.nanmedian(sub.I2)), 1)},
          open(os.path.join(TAB, "_R4_translation_noncircular.json"), "w"), indent=2)
pd.DataFrame(rows).to_csv(os.path.join(TAB, "_R4_translation_noncircular.csv"), index=False)
t.to_csv(os.path.join(TAB, "_R4_targets_fixed_vs_random.csv"))
print("\n[written] _R4_translation_noncircular.csv/.json, _R4_targets_fixed_vs_random.csv")
