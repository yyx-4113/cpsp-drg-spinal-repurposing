# A2 — Design & Statistics Review (random-effects meta, non-circular translation, target-set bootstrap, set-level BH, ML/LODO, multiple-testing)

**Manuscript:** v1.4, *Scientific Reports* submission `MVP_ScientificReports_submission.md` (+ supplementary, reporting summary). Treated as a first submission. Reviewed independently of the other three reviewers.

**Recomputation environment:** `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe` (numpy 2.x, scipy, sklearn, xgboost). Scripts written to `results/tables/_a2_recompute.py` and `_a2_diag*.py`; outputs quoted below.

---

## Item 1 — Random-effects (DerSimonian–Laird) meta-analysis: formulas are correctly applied and the shrinkage is real, not a weight artefact (T1-7)

【Problem】 The DerSimonian–Laird implementation is algebraically correct and the claim that the random-effects core (1,008) is a genuine subset-shrinkage of the fixed-effect core (4,055) is verified, so the "RE narrows membership" conclusion is sound.

【Evidence】 I recomputed aggregate statistics from `_R4_random_effects_meta.csv` (16,552 genes):
- FE core (FDR_FE<0.05 & consistency≥0.8) = **4,055**; RE core (FDR_RE<0.05 & consistency≥0.8) = **1,008** = **24.9%** of FE core. Matches submission.md:34 ("1,008 genes—24.9% of the fixed-effect core").
- Median τ² = **0.232**, median I² = **38.8%**, genes with I²>50% = **41.9%**, genes with τ²>0 = **68.1%**. All match submission.md:34.
- Gene-level DL check: for ATF3, I² recomputed from Q as `max(0,(Q−(K−1))/Q)·100` = **85.323** vs reported **85.323**; p_RE recomputed from Z_RE as `2·(1−Φ(|Z_RE|))` = **2.830e-03** vs reported **2.830e-03** (GAL likewise: 1.117e-04 vs 1.117e-04). So the Q/τ²/I² and Z_RE→p_RE chain is internally exact.
- **Monotonicity proof of real shrinkage:** of 4,055 FE-core genes, **3,047 drop** under RE and **0** RE-core genes are absent from the FE core (RE-core ⊆ FE-core). Because the per-contrast weights `w_i=√(n_case·n_ctrl/(n_case+n_ctrl))` are shared between FE and RE and τ² is only ever added to the variance, RE can only deflate |Z_RE| relative to Z_FE; no gene can "gain" RE significance spuriously. The narrowing is therefore data-driven heterogeneity, not a computation artefact.
- Hubs: median I² = **72.8%**, 18/35 retain FDR_RE<0.05 (matches submission.md:34 and `_R4_supplementary_summary.json`: `hubs_FDR_RE_lt05=18`).
- Ten targets: RE-significant = **4/10** (TNIK, SLC2A1, GALNS, ADRA2A), exactly as in submission.md:78 and `_R4_targets_fixed_vs_random.csv`.

【Why it matters】 This is the paper's central honesty claim (fixed-effect core is primary; random-effects core is the sensitivity/"lower" bound). It survives independent recomputation, so the heterogeneity-sensitive framing is credible and the reader is not misled.

【Specific fix】 (Optional robustness, not blocking) Two correlated contrasts — GSE265957 DRG D4 and D63 — are from the *same* study/animal cohort and are treated as independent inputs (submission.md:119, Methods). Correlated within-study contrasts inflate the effective sample size and can *understate* I². Add one sentence: "The two GSE265957 translatome timepoints are not strictly independent; treating them as independent inputs is conservative for the fixed-effect significance but may understate τ²/I², so the RE sensitivity bound should be read as a lower bound on heterogeneity." A restricted-maximum-likelihood (REML) or Hartung–Knapp–Sidik–Jonkman RE re-run as a second sensitivity would strengthen the claim that 1,008 is not DL-anti-conservative artefact (DL under-estimates τ², which here would only make RE *more* like FE — i.e. in the safe direction — but a second estimator removes the objection).

---

## Item 2 — The fully non-circular translation counts (2,266/4,899) are not reproducible from the cited source file and mix two different gene universes (14,390 vs 14,445) (T1-8/9) — MAJOR

【Problem】 The manuscript's headline non-circular numbers (background 6,779/14,390; test 2,266/4,899) cannot be located in the file cited as their source (`_R4_translation_noncircular.csv`), and the test stratum is drawn from a different gene universe (14,445 incision-measured genes) than the background (14,390), so the two sides of the −0.9 pp risk difference are computed on mismatched gene sets.

【Evidence】 
- `_R4_translation_noncircular.csv` contains only four rows: `all_measured` (7,751/14,445, circular), `meta_FDR05_NIcons_ge08` (2,318/4,306, *semi*-corrected, FDR still 6-contrast), `meta_FDR05_NIcons_lt08` (1,048/1,598), `meta_FDR05_pooled_ge08` (2,473/3,564, circular core). **None of these is the fully non-circular test** that submission.md:46 and Supplementary Table S6 Panel B (lines 217–218) report as 6,779/14,390 and 2,266/4,899. The cited source therefore does not contain the reported rows.
- Recomputing the non-circular test directly from the cited nerve-injury-only meta (`_R4_nerveinjury_only_meta.csv`, the correct file for "signature built on nerve-injury contrasts only"):
  - Background (all incision-measured): **k=6,779 / n=14,390, rate=0.4711**, Wilson 46.3–47.9% — matches manuscript background exactly.
  - Test (FDR_NI<0.05 & ni_consistency≥0.8 & incision measured): **k=2,351 / n=5,089, rate=0.4620**, Wilson 44.8–47.6% — i.e. **NOT 2,266/4,899**.
- The manuscript's 2,266/4,899 is only obtained by switching to `_R4_random_effects_meta.csv`, whose `incision_measured==True` flag defines **14,445** measured genes (not 14,390). Recomputing the test on that file (FDR_NI<0.05 & ni_consistency≥0.8 & incision_measured): **k=2,265 / n=4,906, rate=0.4617** — matching the manuscript's 2,266/4,899 to within rounding. So the test numerator/denominator come from the 14,445 universe while the background comes from the 14,390 universe.
- Minor internal rounding: submission.md:46 reports the test as 46.3% (CI 44.9–47.7%) whereas S6 Panel B (line 218) reports 46.2% (CI 44.9–47.6%); the latter matches my 14,390-universe recompute, the former the 14,445-universe one.
- Note the user-flagged gene-universe trap: I compared against the *published* CSV universe (14,390 / 3,556) as instructed; the 14,445 figure is exactly the "independent recompute" universe, and the manuscript has inadvertently used it for the test while keeping 14,390 for the background.

【Why it matters】 The *direction and magnitude* of the conclusion are unaffected — the test rate is 46.2% in both universes and the risk difference is −0.9 pp either way (0.4711−0.4620 = −0.91 pp from the consistent 14,390 universe). But a reader following the Materials/Data-availability statements cannot regenerate the headline counts: the cited file lacks the rows, and the two counts come from two files with two universe definitions. For a journal that prizes reproducible deposited tables, this is a correctable but real defect, and it slightly undercuts the "non-circular" branding because the comparator and the test were not drawn from one consistent measurable-gene set.

【Specific fix】 Recompute background and test from a single consistent file (use the published 14,390-universe `META_DRG_axis_stouffer.csv` / `_R4_nerveinjury_only_meta.csv` for both), and either (a) replace 2,266/4,899 with the reproducible 2,351/5,089 (rate 46.2%, Wilson 44.8–47.6%, risk diff −0.9 pp unchanged), or (b) if 2,266/4,899 is retained, state explicitly that the test universe is 14,445 and add the matching 14,445-universe background. Deposit the actual non-circular rows (background + test + the `meta_FDR05_NIcons_lt08` comparator) into `_R4_translation_noncircular.csv` so the cited file matches the text; currently it holds only circular/semi-corrected strata.

---

## Item 3 — The 5,000-draw label-permutation null is correctly specified and p=0.14 legitimately supports "no positive predictability" (T1-8/9)

【Problem】 The permutation null (randomly re-labelling stratum membership among the same gene pool) is the appropriate reference for a contrast with a global directional skew, and p=0.14 is consistent with a true null/slightly-negative effect, so the conclusion "nerve-injury signature carries no information about incision direction" is statistically supported.

【Evidence】 
- Mechanics: the null permutes which genes are "in the test stratum" while keeping each gene's `incision_agreement` fixed, so the null mean equals the background rate (47.1%) and its SE for a stratum of n≈4,900 is √(0.471·0.529/4,900) ≈ 0.71 pp. The observed test rate 46.2% is ~1.26 SE below the null mean; a one-sided p in the 0.10–0.14 range is exactly what the manuscript reports (0.14), so the p-value is credible and not inflated by an inappropriate 50% null.
- The alternative of a binomial test vs 50% was correctly dropped (Reporting Summary:15; submission.md:44). A 50% null would be wrong because the incision contrast has a global skew relative to nerve injury.
- Power caveat: with n≈4,900–5,089 the test can only resolve differences ≳2 pp at α=0.05; the observed effect is *negative* (−0.9 pp), so the study is adequately powered to reject any substantial *positive* translational signal (which is the claim being tested) but cannot exclude a small (<2 pp) true positive effect. That is the correct reading of "essentially no information," and the manuscript hedges appropriately ("essentially no information," submission.md:46).

【Why it matters】 This is the paper's second honesty pillar (translation is non-predictive). The inference is valid; the only issue is the bookkeeping in Item 2, not the test design.

【Specific fix】 No change to the test. Add one clause to submission.md:46–47 making the power limit explicit: "Because n≈5,000 only resolves directional differences ≳2 pp, the test rules out a *substantial positive* incision signal but cannot exclude a small (<2 pp) true effect; the observed −0.9 pp is consistent with null or slightly negative predictability." This preempts the reviewer who will ask whether p=0.14 means "underpowered."

---

## Item 4 — Set-level Benjamini–Hochberg across the 18 multi-member gene sets is correctly computed; the OXPHOS FE/RE contrast is reported honestly (T1-10)

【Problem】 The set-level BH q-values are mathematically correct and the key contrast (OXPHOS q=0.020 under fixed effects but q=0.31 under random effects) is reported without spin.

【Evidence】 Recomputed BH on the 18 multi-member fixed-effect permutation p-values from `_R4_geneset_setlevel_bh.csv`:
- Three floor-pinned sets (perm_p = 1/2001 = 0.0004998): recomputed BH q = **0.002999** for ranks 1–3 (min over tail), matching the reported `perm_q` = **0.0029985** for neuroinflammation/complement/DAM_microglia.
- OXPHOS (perm_p = 0.004498, rank 4): recomputed BH q = **0.0202**, matching reported **0.02024**.
- OXPHOS random-effects row: reported `perm_q` = **0.3103** (perm_p = 0.06897), and the manuscript states this plainly (submission.md:36: "OXPHOS did not (q = 0.31)").
- 18 multi-member sets are present (Sigma-1 correctly excluded as single-member, submission.md:36, S5b lines 164–189). Neuropeptides borderline q=0.0468 under FE is also reported (S5b line 174), not concealed.
- The 10-target docking BH (S4 Panel B) is likewise correct: raw-p BH q for AXL/MAPK14/TNIK/ACVR1 survive, size-independent BH q leaves only ADRA2A (0.0025); recomputation of the monotonic BH on the 5 targets reproduces the table.

【Why it matters】 Set-level correction is the methodological upgrade this version advertises (submission.md:8); it is implemented correctly and the honest FE-vs-RE flip for OXPHOS is the right call, so no over-claim about energy-metabolism suppression reaches the reader.

【Specific fix】 No change required. (Optional) State once that BH is applied to permutation p across sets, and that the three floor sets are ordered by Stouffer Z — already done at submission.md:36/S5b:166, so this is satisfied.

---

## Item 5 — Target-set bootstrap: reported stability statistics are internally consistent and reproducible; the "structural, not statistical" conclusion follows (T1-11)

【Problem】 Every quoted number in the docking-target-set bootstrap is recoverable from the deposited marginal CSV and the joint JSON, and the conclusion that the target list is justified by structural tractability rather than hub-selection stability is supported.

【Evidence】 From `_R4_targetset_bootstrap.csv` + `_R4_targetset_bootstrap.json`:
- Sum of the 17 dock-eligible marginal recovery frequencies = **0.785** ≈ reported "0.79 of the 17" (submission.md:54); sum of the 9 docked = **0.35** exactly (matches "0.35 of the 9").
- JSON: `dock_eligible_17.P_ge3 = 0.04`, `P_ge5 = 0.0`, median hub-set size = **6.0** (IQR 5–8), median Jaccard vs published 35 = **0.026** (IQR 0.024–0.051) — all match submission.md:54 and S7 Panel A (lines 258–268).
- Per-gene recovery in `_R4_targetset_bootstrap.csv` matches `P3_hub_bootstrap.csv` (e.g. CDHR5 0.155 in both), and the most-stable dock-eligible hub is CDHR5 (15.5%), matching S7 Panel B.
- The bootstrap is correctly specified: B=200 resamples of the 72 pooled samples, identical ≥2/3 consensus rule; under resampling LASSO contributes 0 selections (effective consensus = RF∩XGBoost), which the manuscript states explicitly (submission.md:54). So the instability is not hidden.

【Why it matters】 This is the bridge between the resampling-sensitive 35-gene hub set and the docking target list. Because the joint probabilities (P≥3 of 17 = 0.04) and the median Jaccard (0.026) are genuine, the decision to anchor the docked targets on `n_holo_PDB ≥ 1` structural tractability rather than on hub rank is defensible and not over-claimed.

【Specific fix】 No change required. (Optional) Note that P(≥3 of 17)=0.04 is a single descriptive probability, not a corrected hypothesis test, to forestall a reviewer treating it as a "significant" reproducibility claim — the manuscript already frames it as support for the structural-justification argument, so this is adequately handled.

---

## Item 6 — ML/LODO: degenerate small-n confidence intervals are acknowledged and the cross-animal mean correctly excludes same-animal folds (ML/LODO)

【Problem】 The leave-one-dataset-out AUC reporting is honest about small-n DeLong degeneracy and correctly excludes the two same-animal GSE241361 folds from the cross-animal mean.

【Evidence】 From `P3_lodo_auc_ci.csv` (5 folds):
- Three folds have degenerate [1.0, 1.0] CIs: GSE278227 (n=28, AUC 1.0), GSE241361 mouseDRG (n=9, AUC 1.0), GSE212311 (n=6, AUC 1.0). Manuscript submission.md:52 states "Three of the five folds have degenerate confidence intervals (point estimate 1.000 with CI [1.0, 1.0]) … reported as non-informative rather than as evidence of perfect precision" — accurate and appropriately cautious.
- Cross-animal mean uses GSE278227 (1.0), GSE267799 (0.917), GSE212311 (1.0) → floor 0.917, range 0.917–1.000, explicitly *excluding* the two GSE241361 folds (same animals), as required by submission.md:52 and Methods:133.
- The leakage-inflated 5×20 repeated-CV (0.999, nominal ±0.004 exceeding 1.0) is reported only as an optimistic upper bound beside the label-permutation null (0.490 ± 0.085), not as a CI — correctly disciplined.

【Why it matters】 LODO is the paper's primary generalisation metric for the hub classifier. The handling of degenerate intervals and same-animal dependence is exactly what a statistical reviewer wants to see; no inflation of the classifier claim.

【Specific fix】 No change required. (Optional) Add the explicit DeLong one-sided-vs-two-sided convention and the SEED used, already implied by Methods:133 ("fixed SEED"); consider stating the SEED value (42 per S7) in the ML paragraph for full reproduction.

---

## Item 7 — Multiple-testing registry is complete for the five stated families; two minor gaps (multivariate LR p-values and the human-layer single test) are not registered (registry audit)

【Problem】 The Methods multiple-testing registry (submission.md:144–145) covers the five analytical families but omits the post-hoc multivariate physicochemical control's likelihood-ratio p-values, which are reported as "docking signal beyond chemotype" for three targets without Benjamini–Hochberg correction.

【Evidence】 
- Registered families: (i) per-dataset DE BH; (ii) meta BH (FE & RE separately); (iii) gene sets BH across 18 multi-member; (iv) docking BH across 5 ChEMBL targets (raw + size-independent); (v) single-cell sample-level BH. All five are implemented and I verified (iii) and (iv) above. Composite-ranking hypergeometric p is explicitly excluded as descriptive (correct).
- Gap A — S4 Panel A (lines 118–124) reports LR docking-residual p for AXL (2.6e-5), TNIK (7.3e-5), ACVR1 (9.6e-4), ADRA2A (0.027), MAPK14 (0.066) and the manuscript uses these to claim three targets "retain docking signal beyond chemotype" (submission.md:76, 105, 109). These five p-values are *not* BH-corrected and are not listed in the registry, even though they are used to qualify the honest-null conclusion. The manuscript partly mitigates this by calling the positive-control recovery "post-hoc" and "event-poor, n-inflated" (submission.md:76), but the registry should name them.
- Gap B — the human-layer set-level permutation test (p=0.51, submission.md:58) is a single test (no correction needed) yet is absent from the registry; listing it avoids the appearance of an unreported comparison.

【Why it matters】 The honest-null conclusion is robust, but an unregistered set of five LR p-values that are then used to soften that conclusion is exactly the kind of post-hoc multiplicity a registry exists to capture. A reviewer could argue the "beyond chemotype" claim rests on uncorrected tests.

【Specific fix】 Add two lines to the registry at submission.md:145: "(vi) docking multivariate physicochemical control — likelihood-ratio p for docking-affinity residual discrimination across the five ChEMBL-annotated targets, reported descriptively and **not** BH-corrected (post-hoc, added in response to review); (vii) human-layer miRNA set-level permutation — single test, no correction." And/or apply BH across the five LR p-values (which would still leave AXL/TNIK significant after correction, so the "beyond chemotype" statement survives).

---

## § Stands up (verified, evidence above)

1. **Random-effects DL meta is correct and the shrinkage is real.** Recomputed FE core 4,055, RE core 1,008 (24.9%), median τ² 0.232, median I² 38.8%, 41.9% I²>50%, 68.1% τ²>0; gene-level I² and p_RE reproduce the deposited values exactly; RE-core ⊆ FE-core (0 flipped in), proving the narrowing is heterogeneity-driven, not a weight artefact (Item 1, `_R4_random_effects_meta.csv`).
2. **Set-level BH is correct and the OXPHOS FE/RE contrast is honest.** Recomputed BH q = 0.002999 (floor sets), 0.0202 (OXPHOS FE), and confirmed OXPHOS RE q = 0.3103 reported without spin (Item 4, `_R4_geneset_setlevel_bh.csv`).
3. **Target-set bootstrap numbers are reproducible and the structural-justification conclusion holds.** Marginal sums 0.785/0.35, JSON P(≥3 of 17)=0.04, P(≥5)=0.0, median Jaccard 0.026, median hub-set 6 — all match the text (Item 5, `_R4_targetset_bootstrap.csv/.json`).
4. **ML/LODO degeneracy is acknowledged and same-animal folds excluded.** Three [1.0,1.0] folds flagged non-informative; cross-animal mean (0.917–1.000) excludes the two GSE241361 folds; leakage-inflated CV reported only as upper bound (Item 6, `P3_lodo_auc_ci.csv`).
5. **The non-circular translation *conclusion* is robust to the universe mismatch.** Test rate is 46.2% in both the 14,390 and 14,445 universes and the risk difference is −0.9 pp either way; the permutation null is correctly specified and p=0.14 supports "no substantial positive predictability" (Items 2–3).

---

## § Questions for the authors

1. Which exact script and source file produced the reported 2,266/4,899 non-circular test? My recomputation shows it comes from the 14,445-universe `_R4_random_effects_meta.csv` (`incision_measured`), whereas the 6,779/14,390 background comes from the 14,390-universe NI-only meta — will you recompute both from one consistent file and deposit the actual non-circular rows in `_R4_translation_noncircular.csv`?
2. In `_R4_translation_noncircular.csv` only circular and semi-corrected strata are present (no fully non-circular rows). Is this a saving error, or were the non-circular rows computed elsewhere? Please make the deposited table match the text.
3. Will you add a REML or Hartung–Knapp–Sidik–Jonkman random-effects sensitivity to confirm the 1,008 core is not a DerSimonian–Laird anti-conservative artefact (Item 1)?
4. The two GSE265957 translatome timepoints (D4, D63) are from one cohort but treated as independent inputs. Do you have a sensitivity that collapsed or down-weighted them, and did it move τ²/I² materially (Item 1)?
5. Will you register the multivariate physicochemical LR p-values (S4 Panel A) and BH-correct them across the five targets, or explicitly label them descriptive (Item 7)?

---

## § What I actually checked

**Files read (manuscript, not other reviewers):**
- `reports/MVP_ScientificReports_submission.md` (main text, lines 32–145, Table 1b/3, Methods meta/geneset/ML/multiple-testing registry).
- `reports/MVP_ScientificReports_supplementary.md` (S5b set-level BH lines 164–191; S6 Panel A–D lines 194–249; S7 target-set bootstrap lines 252–301).
- `reports/MVP_ScientificReports_reporting_summary.md` (Statistics section).

**Data files read/recomputed:**
- `_R4_random_effects_meta.csv` (16,552 genes) — RE core, τ²/I² medians, hub I², FE⊆RE monotonicity, gene-level I²/p_RE checks.
- `META_DRG_axis_stouffer.csv` (16,552 genes) — FE core cross-check, universe 14,390.
- `_R4_nerveinjury_only_meta.csv` (16,552 genes) — non-circular background 6,779/14,390 and test 2,351/5,089 recomputed.
- `_R4_random_effects_meta.csv` `incision_measured` flag — showed test 2,265/4,906 (the 14,445 universe behind the manuscript's 2,266/4,899).
- `_R4_translation_noncircular.csv` / `.json` — confirmed only circular/semi-corrected rows present (no non-circular rows); json `noncircular_risk_difference_pp = −11.8` is a different contrast than the text's −0.9 pp.
- `_R4_geneset_setlevel_bh.csv` — BH recomputed (floor 0.002999, OXPHOS 0.0202/0.3103).
- `_R4_targetset_bootstrap.csv` / `.json` and `P3_hub_bootstrap.csv` — marginal sums 0.785/0.35, JSON P-values, Jaccard 0.026.
- `_R4_targets_fixed_vs_random.csv` — 4/10 RE-significant confirmed (TNIK, SLC2A1, GALNS, ADRA2A).
- `P3_lodo_auc_ci.csv` — three [1.0,1.0] folds, cross-animal composition confirmed.
- `_R4_supplementary_summary.json` — cross-checked core counts and translation universe 14,390.

**Commands run:** two Python scripts (`results/tables/_a2_recompute.py`, `_a2_diag.py`, `_a2_diag2.py`) under the managed venv; recomputed every aggregate claim above and quoted the exact values.

**Discrepancies found:**
- Manuscript non-circular test 2,266/4,899 is **not reproducible** from the cited NI-only meta (I get 2,351/5,089) and is sourced from a different gene universe (14,445) than the 14,390 background — Item 2 (major, but conclusion-preserving).
- The cited `_R4_translation_noncircular.csv` does **not contain** the fully non-circular rows it is supposed to source (Panel B) — Item 2.
- Minor: submission.md:46 test CI "44.9–47.7%" vs S6 "44.9–47.6%" (rounding only).
- Minor: multivariate LR p-values (S4 Panel A) used to qualify the honest-null are unregistered/un-BH-corrected — Item 7.

**Discrepancies absent (claims verified correct):** RE meta formulas and all aggregate heterogeneity numbers; set-level BH q-values and OXPHOS FE/RE contrast; target-set bootstrap statistics; LODO degeneracy handling and cross-animal exclusion; 10-target RE significance count (4/10); hub I² (72.8%) and 18/35 RE retention.
