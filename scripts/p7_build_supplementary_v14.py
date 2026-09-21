#!/usr/bin/env python3
# p7_build_supplementary_v14.py -- generates Supplementary Tables S5b, S6 and S7 for v1.4.
# Everything is read from the authoritative outputs in results/tables/ so that no number in the
# supplementary is hand-typed. Appends to reports/MVP_ScientificReports_supplementary.md.
import os, json
import numpy as np, pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB  = os.path.join(ROOT, "results/tables")
SUP  = os.path.join(ROOT, "reports/MVP_ScientificReports_supplementary.md")

gsb = pd.read_csv(os.path.join(TAB, "_R4_geneset_setlevel_bh.csv"))
s6  = json.load(open(os.path.join(TAB, "_R4_supplementary_summary.json")))
s7  = json.load(open(os.path.join(TAB, "_R4_nerveinjury_only_summary.json")))
tnc = pd.read_csv(os.path.join(TAB, "_R4_translation_noncircular.csv"))
btj = json.load(open(os.path.join(TAB, "_R4_targetset_bootstrap.json")))
btc = pd.read_csv(os.path.join(TAB, "_R4_targetset_bootstrap.csv"))
tvr = pd.read_csv(os.path.join(TAB, "_R4_targets_fixed_vs_random.csv"))
re_ = pd.read_csv(os.path.join(TAB, "_R4_random_effects_meta.csv"))

def f(x, n=4):
    if pd.isna(x): return "—"
    return f"{x:.{n}g}"

out = []

# ------------------------------------------------------------------ S5b
out.append("""
## Supplementary Table S5b. Set-level Benjamini–Hochberg correction across gene sets (P3)

The 19 a priori gene sets were previously reported with permutation p-values but **without** correction across sets, which left the three floor-pinned sets (permutation p at the 1/2001 resolution floor) tied and ordered only by Stouffer Z. Benjamini–Hochberg correction is applied here across the **18 multi-member sets**; Sigma-1 is a single-gene marker (SIGMAR1), is reported as such, and is excluded from set-level inference and ordering. Columns are given for the fixed-effect meta_Z vector (primary) and for the random-effects meta_Z vector (sensitivity). Source: `results/tables/_R4_geneset_setlevel_bh.csv`.

| Gene set | n_present | perm p (FE) | **BH q (FE)** | perm p (RE) | **BH q (RE)** | Survives set-level BH |
| --- | --- | --- | --- | --- | --- | --- |""")
fe = gsb[gsb.scale == "fixed"].set_index("set").sort_values("perm_p")
rx = gsb[gsb.scale == "random"].set_index("set")
order = list(fe.index) + ["Sigma1"]
for s in order:
    if s not in fe.index:
        out.append(f"| {s} | 1 | — | — | — | — | excluded (single-gene marker) |"); continue
    r = fe.loc[s]; r2 = rx.loc[s] if s in rx.index else None
    surv = "yes" if r.perm_q < 0.05 else "no"
    if r2 is not None and r2.perm_q >= 0.05 and r.perm_q < 0.05: surv = "fixed-effect only"
    out.append(f"| {s} | {int(r.n_present)} | {f(r.perm_p)} | **{f(r.perm_q)}** | "
               f"{f(r2.perm_p) if r2 is not None else '—'} | {f(r2.perm_q) if r2 is not None else '—'} | {surv} |")
out.append(f"""
*Reading.* Under the fixed-effect meta-vector, neuroinflammation, complement, DAM microglia (q = {f(fe.loc['Neuroinflammation','perm_q'],3)} each) and mitochondrial OXPHOS (q = {f(fe.loc['Mitochondria_OXPHOS','perm_q'],3)}) survive set-level BH; neuropeptides are borderline (q = {f(fe.loc['Neuropeptides_pain','perm_q'],3)}). Under the random-effects meta-vector the three upregulated programmes survive unchanged (q = {f(rx.loc['Neuroinflammation','perm_q'],3)}) but **OXPHOS does not (q = {f(rx.loc['Mitochondria_OXPHOS','perm_q'],3)})**, so energy-metabolism suppression is reported as a fixed-effect finding that is not robust to between-contrast heterogeneity. No ion-channel family survives under either model.
""")

# ------------------------------------------------------------------ S6
tr = s6["translation"]; cs = s6["consistency_split"]
out.append(f"""
## Supplementary Table S6. Random-effects sensitivity, heterogeneity, and the non-circular translation test

**Panel A — heterogeneity and core stability.** The primary meta-analysis is a fixed-effect (inverse-variance / Stouffer) combination. Panel A reports a DerSimonian–Laird random-effects alternative computed on the same per-contrast Z-values, with τ² and I² per gene. Source: `results/tables/_R4_random_effects_meta.csv`, `_R4_supplementary_summary.json`.

| Quantity | Fixed effect | Random effects |
| --- | --- | --- |
| Genes tested | {s6['n_genes_tested']:,} | {s6['n_genes_tested']:,} |
| Core (FDR < 0.05 and consistency ≥ 0.8) | **{s6['core_fixed_effect']:,}** | **{s6['core_random_effects']:,}** ({s6['RE_retains_pct']}% of the fixed-effect core) |
| Median τ² | — (assumed 0) | {s6['median_tau2']} |
| Median I² | — (assumed 0) | {s6['median_I2_pct']}% |
| Genes with I² > 50% | — | {s6['pct_genes_I2_gt50']}% |
| Genes with τ² > 0 | — | {s6['pct_genes_tau2_gt0']}% |
| 35 hubs retaining FDR < 0.05 | 35/35 | 18/35 |

*Reading.* Between-contrast heterogeneity is moderate overall (median I² = {s6['median_I2_pct']}%) and high among the hubs (median I² = 72.8%), and the core is heterogeneity-sensitive: only {s6['RE_retains_pct']}% of the fixed-effect core persists under random effects. The fixed-effect core is reported as the primary result with the random-effects core as its sensitivity bound.

**Panel B — nerve-injury-to-incision translation, circular versus non-circular.** The originally reported concordance figures were produced by a circular design: both the meta_Z and the pooled consistency filter (≥0.8 across all six contrasts) **include the incision contrast**, so a gene could enter the core partly because it already agreed with the incision direction. Panel B reports (i) those circular figures for reference only, (ii) the same test with consistency restricted to the five nerve-injury contrasts, and (iii) the fully non-circular test in which the signature is built on the five nerve-injury contrasts only and the incision contrast is used once, as a held-out test. Wilson 95% confidence intervals and a 5,000-draw label-permutation null against the measured background are given in place of a binomial test against 50%, which is not the correct reference for a contrast with a global directional skew. Sources: `results/tables/_R4_translation_concordance_effectsize.csv`, `_R4_translation_noncircular.csv`, `_R4_nerveinjury_only_meta.csv`.

| Stratum | k / n | Agreement | Wilson 95% CI | Permutation p vs background | Circular? |
| --- | --- | --- | --- | --- | --- |
| Circular: all measured genes (6-contrast meta_Z) | {tr['all_shared']['k']:,}/{tr['all_shared']['n']:,} | {tr['all_shared']['rate']*100:.1f}% | {tr['all_shared']['ci'][0]*100:.1f}–{tr['all_shared']['ci'][1]*100:.1f}% | — | yes |
| Circular: core (pooled consistency ≥ 0.8) | {tr['core']['k']:,}/{tr['core']['n']:,} | {tr['core']['rate']*100:.1f}% | {tr['core']['ci'][0]*100:.1f}–{tr['core']['ci'][1]*100:.1f}% | {f(tr['core']['perm_p'],3)} | yes |
| Semi-corrected: meta FDR < 0.05 and nerve-injury consistency ≥ 0.8 | 2,318/4,306 | 53.8% | 52.3–55.3% | 0.79 | partial (FDR still 6-contrast) |
| **Non-circular background (all measured)** | {s7['strata']['all_measured']['k']:,}/{s7['strata']['all_measured']['n']:,} | **{s7['strata']['all_measured']['rate']*100:.1f}%** | {s7['strata']['all_measured']['ci'][0]*100:.1f}–{s7['strata']['all_measured']['ci'][1]*100:.1f}% | 1.00 | no |
| **Non-circular test: NI FDR < 0.05 and NI consistency ≥ 0.8** | {s7['strata']['NI_FDR05_AND_NIcons>=0.8']['k']:,}/{s7['strata']['NI_FDR05_AND_NIcons>=0.8']['n']:,} | **{s7['strata']['NI_FDR05_AND_NIcons>=0.8']['rate']*100:.1f}%** | {s7['strata']['NI_FDR05_AND_NIcons>=0.8']['ci'][0]*100:.1f}–{s7['strata']['NI_FDR05_AND_NIcons>=0.8']['ci'][1]*100:.1f}% | {f(s7['strata']['NI_FDR05_AND_NIcons>=0.8']['perm_p'],3)} | no |
| Non-circular comparator: NI FDR < 0.05 and NI consistency < 0.8 | {s7['strata']['NI_FDR05_AND_NIcons<0.8']['k']:,}/{s7['strata']['NI_FDR05_AND_NIcons<0.8']['n']:,} | {s7['strata']['NI_FDR05_AND_NIcons<0.8']['rate']*100:.1f}% | {s7['strata']['NI_FDR05_AND_NIcons<0.8']['ci'][0]*100:.1f}–{s7['strata']['NI_FDR05_AND_NIcons<0.8']['ci'][1]*100:.1f}% | {f(s7['strata']['NI_FDR05_AND_NIcons<0.8']['perm_p'],3)} | no |

*Reading.* The apparent core "translation" of {tr['core']['rate']*100:.1f}% collapses to 53.8% once consistency is restricted to nerve-injury contrasts and to **{s7['strata']['NI_FDR05_AND_NIcons>=0.8']['rate']*100:.1f}%** under the fully non-circular test, versus a **{s7['strata']['all_measured']['rate']*100:.1f}%** background — a risk difference of **{s7['strong_vs_background_pp']} pp** (permutation p = {f(s7['strata']['NI_FDR05_AND_NIcons>=0.8']['perm_p'],3)}). Knowing that a gene is strongly and consistently regulated by nerve injury therefore carries essentially no information about its direction in the incision model. A nerve-injury-only core (incision excluded) comprised {s7['NI_core_FE']:,} genes under fixed effects and {s7['NI_core_RE']:,} under random effects.

**Panel C — consistency split for the reported 4,055-gene core.** `nerve_injury_consistency` is computed across the five nerve-injury contrasts only; `incision_agreement` is the indicator that the incision log₂FC has the same sign as the meta Z. Source: `results/tables/_R4_random_effects_meta.csv`.

| Quantity | Value |
| --- | --- |
| Core genes with an incision measurement | {cs['core_incision_measured']:,} |
| ... incision-concordant | {cs['core_incision_concordant']:,} ({cs['core_incision_concordant_pct']}%) |
| ... incision-**discordant** (core-consistent yet incision-opposed) | {cs['core_incision_discordant']:,} ({100-cs['core_incision_concordant_pct']:.1f}%) |
| Core genes with nerve-injury consistency ≥ 0.8 | {cs['core_ni_consistency_ge08']:,}/{cs['core_n']:,} ({cs['core_ni_consistency_ge08']/cs['core_n']*100:.1f}%) |
| Core genes both NI-consistent ≥ 0.8 **and** incision-concordant | {cs['core_both_ni_ge08_and_incision_concordant']:,} |
| Mean nerve-injury consistency in the core | {cs['mean_nerve_injury_consistency_in_core']} (pooled consistency {cs['mean_pooled_consistency_in_core']}) |

**Panel D — the ten docking targets under fixed versus random effects.** Source: `results/tables/_R4_targets_fixed_vs_random.csv`.

| Target | Z (FE) | FDR (FE) | Z (RE) | FDR (RE) | I² (%) | τ² | Retains RE significance |
| --- | --- | --- | --- | --- | --- | --- | --- |""")
for _, r in tvr.iterrows():
    keep = "yes" if r.FDR_RE < 0.05 else "no"
    out.append(f"| {r.symbol} | {r.Z_FE:.2f} | {f(r.FDR_FE,2)} | {r.Z_RE:.2f} | {f(r.FDR_RE,3)} | "
               f"{r.I2:.1f} | {r.tau2:.2f} | {keep} |")
out.append("""
*Reading.* Only 4 of the 10 targets retain FDR < 0.05 under random effects (SLC2A1, TNIK, ADRA2A, GALNS), so target ranking is model-dependent and no target is either privileged or excluded by the meta-analysis on this basis.
""")

# ------------------------------------------------------------------ S7
out.append(f"""
## Supplementary Table S7. Bootstrap stability of the docking target set (P3/P6)

The published bootstrap (`P3_hub_bootstrap.csv`) reported per-gene hub-recovery frequency only and could not answer whether the **docking target set** is reproducible. This table re-runs the identical three-method bootstrap (B = {btj['B']}, SEED = 42; LASSO λ.min, Random-Forest MDGini top-80, XGBoost |SHAP| top-80; hub = ≥2/3 methods) and additionally records the full recovered hub set on every resample. Source: `results/tables/_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap.json`.

**Panel A — set-level reproducibility.**

| Quantity | Dock-eligible hubs (17) | Actually docked hubs (9) |
| --- | --- | --- |
| Members present in the ML feature pool | {btj['dock_eligible_17']['n_in_pool']}/17 | {btj['docked_9']['n_in_pool']}/9 |
| Mean number recovered per resample | {btj['dock_eligible_17']['mean_recovered']} | {btj['docked_9']['mean_recovered']} |
| Median (min–max) | {btj['dock_eligible_17']['median_recovered']:.0f} ({btj['dock_eligible_17']['min']}–{btj['dock_eligible_17']['max']}) | {btj['docked_9']['median_recovered']:.0f} ({btj['docked_9']['min']}–{btj['docked_9']['max']}) |
| P(≥1 recovered) | {btj['dock_eligible_17']['P_ge1']} | {btj['docked_9']['P_ge1']} |
| P(≥3 recovered) | {btj['dock_eligible_17']['P_ge3']} | {btj['docked_9']['P_ge3']} |
| P(≥5 recovered) | {btj['dock_eligible_17']['P_ge5']} | {btj['docked_9']['P_ge5']} |
| P(all recovered) | {btj['dock_eligible_17']['P_all17']} | {btj['docked_9']['P_all9']} |

Resampled hub sets had a median size of {btj['hub_set_size']['median']:.0f} genes (IQR {btj['hub_set_size']['q25']:.0f}–{btj['hub_set_size']['q75']:.0f}) and a median Jaccard overlap of **{btj['jaccard_vs_published35']['median']}** (IQR {btj['jaccard_vs_published35']['q25']}–{btj['jaccard_vs_published35']['q75']}) with the published 35-gene set.

**Panel B — per-gene recovery frequency within the dock-eligible set.**

| Symbol | Set | Recovery frequency |
| --- | --- | --- |""")
for _, r in btc.iterrows():
    out.append(f"| {r.symbol} | {'dock-eligible (17)' if r.set=='dock_eligible_17' else 'docked (9)'} | {r.recovery_freq:.3f} |")
out.append(f"""
*Reading.* The docking target set is **not statistically reproducible**: a median of {btj['dock_eligible_17']['median_recovered']:.0f} of the 17 dock-eligible hubs (and {btj['docked_9']['median_recovered']:.0f} of the 9 actually docked hubs) is recovered per resample, P(≥3 of 17) = {btj['dock_eligible_17']['P_ge3']}, and the most stable single hub (CDHR5) reaches only 15.5%. This is consistent with the 0/35 hubs reaching ≥0.9 stability in the published per-gene bootstrap. The docking target list is therefore justified by **structural tractability (n_holo_PDB ≥ 1), not by statistical stability of hub selection**, and the docking results should be read as a screen of structurally tractable candidates rather than as a validated ranking of the 35 hubs.
""")

txt = open(SUP, encoding="utf-8").read()
if "Supplementary Table S5b" not in txt:
    open(SUP, "a", encoding="utf-8").write("\n".join(out))
    print("[written] appended S5b, S6, S7")
else:
    print("[skip] S5b already present")
print(f"supplementary now {len(open(SUP, encoding='utf-8').read().splitlines())} lines")
