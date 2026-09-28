# A2 — Design & Statistics Review (independent, first-submission basis)

**Manuscript:** `reports/MVP_PLOSONE_submission.md` — Stouffer meta-analysis of 5 studies / 6 contrasts of nerve-injury transcriptomes.
**Target journal:** PLOS ONE.
**Reviewer role:** Biostatistics / meta-analysis / heterogeneity modelling / causal & reporting inference.
**Independence statement:** I read only the manuscript and the authoritative `results/tables/*` files listed in the brief. I did not read any sibling review, compliance, cover-letter, manifest, or archive file. Every numeric claim below was recomputed from the raw tables with `python3`; I do not trust the manuscript's printed numbers.

---

## Summary verdict

The statistical design is, on the whole, unusually disciplined for this literature: real-sample-size weighting, a correctly-deferred random-effects sensitivity bound, an empirically-calibrated (non-50%) translation null, set-level BH, a prospectively specified full-library docking breadth test with MW confounder correction, and an explicit multiple-testing registry. All ten mandatory counts recomputed exactly as reported (FE core = 2,750; RE core = 508 = 18.5%; median I² = 41.8%, median τ² = 0.266; gene-set q = 0.0022 under both FE and RE; 1,660/3,830 = 43.3% and 6,772/14,390 = 47.1%; bulk-only 2,512 with the full 1,322 + 415 + 2,454 + 200 + 296 decomposition; collapse 91.0%; LODO AUCs and n; 2/35 hubs ≥ 0.9; BH-q values recomputed correctly). The docking BH correction and the bulk-only arithmetic are genuinely correct.

That said, there are concrete problems: (i) the translation permutation p = 0.0002 is pinned exactly at the 5,000-permutation resolution floor and should be reported as an upper bound; (ii) the docking `verdict` column labels AXL and TNIK `PASS_size_independent` while the manuscript text correctly states they *failed* the size-independent filter — a direct data/manuscript contradiction; (iii) the stated TNIK size-independent p (0.579) does not match the data file (0.4435; BH-q 0.584); (iv) the "inconclusive" label for ADRA2A is not defined symmetrically with the "failed filter-2" labels for AXL/TNIK under the two-filter rule; and (v) Knapp–Hartung is deferred but is most needed precisely where the claim is made (35 hubs, K = 3–6, median I² = 79.1%). These are fixable without new analyses except (v).

---

## Itemised mandatory checks

### Check 1 — FE core = 2,750
- 【Problem】 No problem found; the primary core size is exactly as reported.
- 【Evidence】 `META_DRG_axis_CORE_signature.csv` has 2,750 rows, and all 2,750 satisfy `meta_FDR < 0.05 AND consistency ≥ 0.8` (recomputed: count = 2,750). Manuscript abstract line 14 and Results line 38–40 state 2,750.
- 【Why it matters】 This is the anchor number for every downstream overlap (63.2%, 91.0%) and for the FE-conditional framing; because it verifies, the sensitivity decompositions built on it are trustworthy.
- 【Specific fix】 None. Keep as is.

### Check 2 — RE core = 508 (18.5%), median I² = 41.8%, median τ² = 0.266
- 【Problem】 No problem found; RE sensitivity bound and heterogeneity medians all verify exactly.
- 【Evidence】 `_R4_random_effects_meta.csv` (16,552 genes): `FDR_RE < 0.05 AND consistency ≥ 0.8` → 508 genes; 508/2,750 = 18.5%. Median I² across all genes = 41.8%; median τ² = 0.266 (recomputed). Also verified the hub subset: median I² = 79.1% across the 35 hubs, 7/35 retaining `FDR_RE < 0.05` (SPRR1A, GALNS, SRRM4, FLRT3, TNIK, CRISP3, LNP1). Manuscript line 40 and line 132 state these.
- 【Why it matters】 The FE→RE collapse (2,750 → 508) is the single most important honesty signal in the paper; verifying it means the "heterogeneity-sensitive" framing is earned, not asserted.
- 【Specific fix】 None for the numbers. Optional: in the RE paragraph, explicitly state that the 508-gene RE core uses the *same* `consistency ≥ 0.8` gate as the FE core so the 18.5% is a like-for-like fraction, not a re-gated count.

### Check 3 — Gene-set q = 0.0022 under FE and RE
- 【Problem】 No problem with the value; the honest caveat about effective discoveries ≈ 1 is already present and should be retained.
- 【Evidence】 `_R4_geneset_setlevel_bh.csv`: Neuroinflammation, Complement, Mitochondria_OXPHOS, DAM_microglia each show `perm_q = 0.0022488755622188904` under **both** `scale = fixed` and `scale = random`. This equals the 2,000-permutation floor (1/2001 = 0.00049975) carried through BH across 18 sets: 0.00049975 × 18/4 = 0.0022489. Manuscript line 42 reports q = 0.0022 four times and explicitly notes "the effective number of independent discoveries is close to one."
- 【Why it matters】 Reporting q = 0.0022 four times *without* the effective-discoveries caveat would overstate four independent findings. The manuscript avoids that; this is a stand-out honesty point.
- 【Specific fix】 None. Keep the "single coordinated neuroimmune–complement axis" framing. (Minor: the four sets share members such as C1QA/B/C and IL6/TNF/CCL2, so the identical q is expected under BH with floor-pinned p — fine as reported.)

### Check 4 — Non-circular translation: 43.3% vs 47.1%, −3.7 pp, p = 0.0002
- 【Problem】 The permutation p = 0.0002 is pinned *exactly* at the 5,000-relabel resolution floor and is reported as a point value rather than an upper bound; and the "significant depletion, not a null" phrasing is statistically correct but under-states that the effect size (−3.7 pp) is small and biologically non-informative.
- 【Evidence】 `_R4_nerveinjury_only_summary.json`: `all_measured` k = 6,772 / n = 14,390 → rate 0.4706 (47.1%, CI 46.2–47.9); stratum `NI_FDR05_AND_NIcons>=0.8` k = 1,660 / n = 3,830 → rate 0.4334 (43.3%, CI 41.8–44.9), risk difference = −3.7 pp, `perm_p = 0.0001999600079984003` = exactly 1/5,000. The manuscript (line 52, line 136) reports 43.3% (41.8–44.9), 47.1% (46.2–47.9), −3.7 pp, p = 0.0002, "significant depletion, not a null," and states the null uses 5,000 relabels (verified by the 1/5,000 floor).
- 【Why it matters】 Because 0.0002 = 1/5000, the observed statistic was at least as extreme as *all* 5,000 relabels, so the true p ≤ 0.0002; reporting it as "p = 0.0002" hides that it is an upper bound and invites over-reading of precision. More importantly, with n = 14,390 a −3.7 pp shift is significant only by virtue of sample size; the manuscript itself concedes the result "carries essentially no information" about the incision direction, so the "significant depletion" label, while technically true, can be mistaken for a strong biological effect.
- 【Specific fix】 Replace the current phrasing with: *"Against the empirical (5,000-relabel) null the nerve-injury signature showed a small but statistically significant depletion in the incision arm (43.3% vs 47.1% background; risk difference −3.7 pp; permutation p ≤ 0.0002, i.e. at the 5,000-permutation resolution floor and reported as an upper bound). The effect size is negligible and, given the lesion-class mismatch, is non-informative rather than evidence against CPSP specificity."*

### Check 5 — Bulk-only sensitivity decomposition
- 【Problem】 No arithmetic error; every sub-number verifies. (One traceability note below.)
- 【Evidence】 `META_bulkonly_sensitivity_summary.json`: `bulk_only_core_size = 2512`, `overlap = 1737`, `overlap_pct_primary = 63.1636`. Recomputed directly from `META_bulkonly_meta.csv` ∩ `META_DRG_axis_CORE_signature.csv`: strict overlap (bulk `meta_FDR < 0.05` and `consistency ≥ 0.8`) = 1,737; of these, pure 4/4 (K = 4, consistency = 1.0) = 1,322 and K = 3 (all three concordant) = 415; relaxed (`consistency ≥ 0.75`) = 2,454 (2,454/2,750 = 89.2%, +717 vs strict); absent from bulk file = 46; present but bulk-non-significant = 154 (total 200); significant-in-bulk but `consistency < 0.75` = 96; outside relaxed = 2750 − 2454 = 296 = 46 + 154 + 96. Manuscript line 44 and line 154.
- 【Why it matters】 This is the primary robustness check for the translatome-mixing concern; because the full decomposition reconciles to 296, the "63.2% / 89.2% / 200 / 296" narrative is internally consistent and defensible.
- 【Specific fix】 None for the numbers. (Optional clarity: state that the 96 genes "outside even the relaxed overlap" are genes that *are* bulk-significant but measured in only 1–2 of the four bulk contrasts, so they fall below the union-K ≥ 3 inclusion rule — this prevents a reader from reading those 96 as bulk-*dis*agreements.)

### Check 6 — Collapse sensitivity = 91.0%
- 【Problem】 No problem found.
- 【Evidence】 `META_collapse_meta.csv`: `collapsed_core = 3582`, `shared_core = 2502`, `retained_fraction = 0.9102`; 2,502/2,750 = 0.9098 ≈ 0.910. Manuscript line 154 reports collapsed core 3,582, shared/retained 2,502/2,750 = 91.0%.
- 【Why it matters】 Confirms the same-animal translatome timepoints are not driving membership; together with bulk-only 63.2% this bounds the measurement-heterogeneity caveat.
- 【Specific fix】 None.

### Check 7 — Hub stability & LODO
- 【Problem】 The LODO AUCs, n, and [1.0, 1.0] degenerate CIs verify; the resample-level hub/bootstrap claims (median 43 hubs; median 8.70 of 17 targets recovered per resample; P(≥3 of 17) = 1.000) cannot be verified from the provided tables because only per-gene recovery frequencies, not the resample matrix, are supplied.
- 【Evidence】 `P3_lodo_auc_ci_leakage_controlled.csv`: GSE278227 AUC 1.0 [1.0, 1.0] n = 28; GSE241361 mouseDRG 1.0 [1.0,1.0] n = 9; GSE241361 mouseSC 1.0 [1.0,1.0] n = 9; GSE212311 1.0 [1.0,1.0] n = 6; incision 0.677 [0.374, 0.940] n = 20 — four folds at AUC 1.000 confirmed. `P3_hub_bootstrap.csv`: hubs with `hub_freq ≥ 0.9` = SPRR1A (1.00) and ATF3 (0.935 ≈ 0.94 reported) → 2/35 confirmed. `P3_hub_genes.csv` has 35 rows. `_R4_targetset_bootstrap.csv`: 17 dock-eligible hubs, per-gene `recovery_freq` range 0.125–0.885, median 0.465 (not 8.70 — that figure is a per-resample *count*, which requires the resample-level data not present in this file). Manuscript line 58–60.
- 【Why it matters】 The four AUC = 1.000 quotes with degenerate CIs are correctly hedged as "zero estimable precision"; the single cross-animal fold (GSE212311 n = 6) and the within-animal GSE278227 fold are correctly identified as the evidential base. The hedge is adequate. But the resample-level median/Jaccard/P(≥3) claims are currently unverifiable from the deposited artifacts, which is a reproducibility gap for a "hypothesis-generating" claim that the authors themselves want treated as bounded.
- 【Specific fix】 (a) Deposit the 200-resample hub-membership matrix (or at minimum the per-resample hub-set sizes and the per-resample target-set recovery counts) so that "median 43 hubs (IQR 41–46)", "median 8.70 of 17 recovered", and "P(≥3 of 17) = 1.000" are reproducible; (b) in the text, relabel the per-gene median (0.465 of 17) separately from the per-resample median count (8.70) so the two quantities are not conflated.

### Check 8 — Docking enrichment logic (two-filter rule)
- 【Problem】 The BH-q values are correctly computed (verified), but the `verdict` column in the data file contradicts the manuscript's own two-filter conclusion for AXL and TNIK, and the ADRA2A "inconclusive" label is not defined symmetrically; additionally a TNIK p-value is misstated.
- 【Evidence】 `P6_BH_correction.csv` (BH recomputed and confirmed): Filter 1 (full-library, MW-corrected) passes ACVR1 (BH-q 0.00129), AXL (5.55e-6), MAPK14 (0.000148), TNIK (0.000327); fails ADRA2A (0.118). Filter 2 (size-independent ΔAUC) passes only ADRA2A (BH-q 0.0025); fails ACVR1 (0.584), AXL (0.3525), MAPK14 (0.584), TNIK (0.584). So exactly zero targets pass both — consistent with "no target cleared both filters." However `P6_enrichment_mw_confounder_check.csv` labels AXL and TNIK `PASS_size_independent`, whereas the manuscript (line 84, line 122) correctly states "AXL and TNIK both failed the size-independent enrichment test (p = 0.141 and 0.579 respectively)." Manuscript line 84 states TNIK size-independent p = 0.579, but the data file `deltaAUC_vs_size_only_p_le0` for TNIK = 0.4435 (BH-q 0.584). Reverse controls (`P6_reverse_control.csv`, `reliable` flag) are correctly used only as method-validation, never as enrichment — verified.
- 【Why it matters】 The verdict label is what a reader (and a downstream meta-analyst) will grep; labelling AXL/TNIK "PASS" while the prose says "failed" is an internal contradiction that can be cited out of context as a positive result. The ADRA2A asymmetry (fails filter 1 → "inconclusive"; AXL/TNIK pass filter 1, fail filter 2 → "failed filter 2") means a target passing exactly one filter is described two different ways, which weakens the clean "pass-both-or-it-is-not-a-hit" rule the authors built. The 0.579 vs 0.4435 mismatch is a factual error in the stated statistic.
- 【Specific fix】 (a) In `P6_enrichment_mw_confounder_check.csv`, rename the `verdict` values to a single symmetric vocabulary, e.g. `PASS_BOTH` / `FAIL_FILTER1` / `FAIL_FILTER2` / `FAIL_BOTH`; AXL and TNIK become `FAIL_FILTER2` (they pass filter 1, fail filter 2), matching the prose. (b) Define "inconclusive" explicitly as `FAIL_FILTER1 with a secondary size-independent signal (filter 2 passes)` so ADRA2A is described by the same rule, not by a more charitable ad hoc label. (c) Correct the TNIK size-independent p: use the raw ΔAUC p = 0.4435, or, if citing the BH-q, write "BH-q = 0.584" — do not report 0.579, which matches neither.

### Check 9 — Multiple-testing registry
- 【Problem】 No headline claim rests on an uncorrected test; the post-hoc multivariate physicochemical control is honestly flagged as EPV-unstable and excluded. (One gap: the five multivariate LR p-values live in Supplementary Table S4, not in `results/tables/`, so I could not recompute them.)
- 【Evidence】 Manuscript line 173–174 lists six families: (i) per-dataset DE BH; (ii) meta-analysis BH FE & RE separately; (iii) gene sets BH across 18 sets; (iv) docking BH across 5 ChEMBL-annotated targets for raw and size-independent p (verified in Check 8); (v) single-cell sample-level BH; (vi) multivariate physicochemical control, explicitly "not counted among the corrected inferential tests," with EPV ≈ 1.9 (AXL), 1.4 (TNIK), 1.0 (ACVR1) flagged. The translation test uses a 5,000-relabel empirical null (not a BH family, but a permutation test against the correct reference — appropriate, not an uncorrected t-test against 50%). The human-miRNA layer reports p = 0.51 (permutation, NS). No headline claim (FE core, gene sets, bulk-only, collapse, docking FAIL/NS, hub stability) is an uncorrected test.
- 【Why it matters】 This registry is the manuscript's strongest methodological contribution versus the "Tier-1-only" repurposing literature; the EPV caveat prevents the post-hoc multivariate AXL/TNIK "significance" from being read as validation.
- 【Specific fix】 (a) Deposit the Supplementary Table S4 multivariate LR outputs (or the script that produces them) so the AXL p = 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4, MAPK14 0.066, ADRA2A 0.027 values are reproducible; (b) keep the explicit "not counted among inferential tests" sentence — it is correct and should not be softened.

### Check 10 — Knapp–Hartung deferred
- 【Problem】 Deferring K-H is acceptable as a *stated limitation* for the RE core, but it is most needed for the 35 hubs and 10 targets, where K = 3–6 and the FE→RE collapse is severe (hub median I² = 79.1%, 7/35 retain RE significance).
- 【Evidence】 Manuscript line 132 defers K-H, arguing it "would only reinforce the heterogeneity-sensitive framing." Verified: 35 hubs have median I² = 79.1% and only 7/35 `FDR_RE < 0.05`; the 10 targets have K = 3–7 and I² 13.5%–86.8% (`_R4_targets_fixed_vs_random.csv`). At K = 3 the normal approximation Z_RE can be anti-conservative; K-H (t with K−1 df) would widen intervals and could drop more of the 7 hubs / 2 targets.
- 【Why it matters】 The hub and target claims are exactly where "gene-level conclusions … are most conditional" (manuscript line 40). Presenting them with a normal-approx RE p at K = 3–6 without K-H leaves a residual inflation risk on the very subset the authors flag as fragile.
- 【Specific fix】 Add a one-paragraph mechanical extension: "We additionally applied a Knapp–Hartung t-adjustment to the random-effects model for the 35 hubs and 10 targets (K = 3–7). This widened confidence intervals and reduced the number of RE-significant hubs from 7 to [X]/35 and targets from 2 to [Y]/10, reinforcing (not changing) the heterogeneity-sensitive framing." If the authors prefer to keep it deferred, the deferral must name the hubs/targets explicitly as the subset where K-H is most material, rather than framing K-H as universally superfluous.

---

## § Stands up (suspected problems that the data did NOT confirm)

1. **FE core = 2,750 is not stale.** I suspected the older 4,055-gene figure; the authoritative table gives exactly 2,750 with the stated gate. Confirmed correct.
2. **The bulk-only overlap arithmetic is fully internally consistent.** I expected the 1,322 + 415 + 2,454 + 200 + 296 decomposition to have a gap; it reconciles exactly (46 absent + 154 present-non-sig + 96 sig-but-low-K = 296). The sensitivity narrative is trustworthy.
3. **The docking BH correction is correctly computed.** I recomputed BH across the 5 ChEMBL-annotated targets for both raw and size-independent p and reproduced every `BH_q_raw_enrich` and `BH_q_size_indep` value exactly (AXL 5.55e-6 / 0.3525; ACVR1 0.00129 / 0.584; MAPK14 0.000148 / 0.584; TNIK 0.000327 / 0.584; ADRA2A 0.118 / 0.0025). No BH error.
4. **Reverse positive controls are consistently method-validation only.** The `P6_reverse_control.csv` AUCs (AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779) are never used as enrichment evidence in the manuscript; ADRA2A's own reverse-control AUC is 0.532 (`reliable = False`), correctly reinforcing the null. The "control_passed → method-validation" discipline holds.
5. **Gene-set q = 0.0022 is honestly caveated.** Reporting the same q four times is defended by the explicit "effective discoveries ≈ 1" statement; this is correct, not deceptive.
6. **RE core = 508 / 18.5% and hub RE subset (7/35, median I² 79.1%) verify**, so the "FE-conditional, heterogeneity-sensitive" framing is earned rather than asserted.

## § Questions for the authors (do not guess)

1. **Resample-level bootstrap artifacts.** The claims "median 43 hubs (IQR 41–46, range 33–60)", "median 8.70 of 17 dock-eligible hubs recovered per resample", "P(≥3 of 17) = 1.000", and "P(≥5 of 17) = 0.990" require the 200-resample membership matrix. Only per-gene `recovery_freq` is deposited. Can you release the resample matrix (or the per-resample counts) so these are reproducible? If not, are the per-resample statistics computed in `scripts/` and can the script be cited?
2. **Multivariate physicochemical control source.** The five LR p-values (AXL 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4, MAPK14 0.066, ADRA2A 0.027) and EPV values appear in Supplementary Table S4, which is not in `results/tables/`. Are these from a single logistic fit per target, and what are the exact positive-event counts per target (the brief cites AXL ≈ 1.9, TNIK ≈ 1.4, ACVR1 ≈ 1.0 EPV)? I could not recompute them.
3. **TNIK size-independent p.** The manuscript reports 0.579 (line 84) but the table gives `deltaAUC_vs_size_only_p_le0 = 0.4435` (BH-q 0.584). Which is intended — the raw ΔAUC p or the BH-q — and is 0.579 a transcription of 0.584?
4. **Knapp–Hartung scope.** Will you run K-H at least for the 35 hubs and 10 targets (where K is smallest), or do you intend to keep the full deferral? If run, what are the resulting RE-significant counts?
5. **Empirical-null relabel count for translation.** The floor value 0.0002 = 1/5000 is consistent with 5,000 relabels as stated; please confirm the translation permutation used exactly 5,000 relabels (not 2,000) so the floor-pinning note in Check 4 is precise.

## § What I actually checked

**Files read (manuscript + authoritative tables only):**
- `reports/MVP_PLOSONE_submission.md` (383 lines, read in full).
- `META_DRG_axis_CORE_signature.csv`, `_R4_random_effects_meta.csv`, `_R4_geneset_setlevel_bh.csv`, `_R4_nerveinjury_only_summary.json`, `_R4_nerveinjury_only_meta.csv`, `_R4_translation_noncircular.csv` (read header only; superseded per brief), `_R4_targets_fixed_vs_random.csv`, `_R4_targetset_bootstrap.csv`.
- `META_bulkonly_sensitivity_summary.json`, `META_bulkonly_meta.csv`, `META_collapse_meta.csv`.
- `P3_hub_genes.csv`, `P3_hub_bootstrap.csv`, `P3_lodo_auc_ci_leakage_controlled.csv`.
- `P6_reverse_control.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_BH_correction.csv`, `P6_breadth_chembl_power.csv` (header inspected), `P6_target_plausibility.json`.

**Recomputations performed (python3, from raw files):**
1. FE core: counted `meta_FDR < 0.05 AND consistency ≥ 0.8` → 2,750. ✔
2. RE core: counted `FDR_RE < 0.05 AND consistency ≥ 0.8` → 508; 508/2,750 = 18.5%; median I² = 41.8%, median τ² = 0.266 across 16,552 genes. ✔ Hub subset: median I² = 79.1%, 7/35 `FDR_RE < 0.05`. ✔ Targets: 2/10 `FDR_RE < 0.05` (TNIK 0.034, GALNS 0.0001). ✔
3. Gene sets: extracted `perm_q` for the four core sets under `fixed` and `random` → 0.0022489 both. ✔
4. Translation: 6,772/14,390 = 47.1% (CI 46.2–47.9); 1,660/3,830 = 43.3% (CI 41.8–44.9); risk diff −3.7 pp; `perm_p = 0.0002` = 1/5,000 floor. ✔
5. Bulk-only: recomputed strict overlap 1,737 (1,322 pure 4/4 + 415 K = 3); relaxed 2,454 (89.2%); absent 46; present-non-sig 154; sig-low-K 96; outside-relaxed 296 = 46 + 154 + 96. ✔
6. Collapse: 2,502/2,750 = 0.9098 ≈ 0.910. ✔
7. LODO: four folds AUC 1.0 [1.0,1.0]; incision 0.677 [0.374,0.940] n = 20; GSE212311 n = 6. ✔ Hubs ≥ 0.9: SPRR1A 1.00, ATF3 0.935. ✔ Target-set per-gene recovery median 0.465 (resample-level 8.70 not in file).
8. Docking BH: recomputed BH across 5 targets for raw and size-independent p → reproduced all `BH_q_raw_enrich` and `BH_q_size_indep`. ✔ Verdict-label contradiction (AXL/TNIK `PASS` vs prose "failed") and TNIK p mismatch (0.579 vs 0.4435) found. ⚠
9. Multiple-testing: confirmed 6 families; no headline claim uncorrected; multivariate control explicitly excluded. (Multivariate LR p-values not in provided tables — could not recompute.) ⚠ partial.
10. Knapp–Hartung: deferred in manuscript; verified the subset where it matters most (hubs/targets, K = 3–6, high I²). Recommend running.

**Discrepancies / unresolved:**
- `P6_enrichment_mw_confounder_check.csv` `verdict` = `PASS_size_independent` for AXL and TNIK contradicts manuscript prose ("failed the size-independent enrichment test"). Data/manuscript inconsistency.
- Manuscript TNIK size-independent p = 0.579 vs table `deltaAUC_vs_size_only_p_le0` = 0.4435 (BH-q 0.584). Numeric mismatch.
- Translation `perm_p = 0.0002` is floor-pinned (1/5,000) and should be reported as p ≤ 0.0002.
- Resample-level hub/target bootstrap statistics (median 43; 8.70/17; P(≥3)=1.000) not reproducible from deposited per-gene files.
- Multivariate physicochemical LR p-values and EPV not in `results/tables/`; not independently recomputed.

**Not read (per independence rule):** any `reviews/REVIEW_round*`, `round*_panel_*`, `RESPONSE_*`, `REVISION_*`, `compliance_check`, `cover_letter`, `SUBMISSION_MANIFEST`, `Reporting_Summary`, `GITHUB_DEPOSIT_SOP`, `author_verification_statement`, sibling `A*/B*/C*` reports, `_archive/`, `.bak`.
