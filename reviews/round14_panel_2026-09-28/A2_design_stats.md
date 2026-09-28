# Reviewer A2 — Design & Statistics (independent review)

**Manuscript:** `reports/MVP_PLOSONE_submission.md` (single-author PLOS ONE resubmission)
**Reviewer role:** statistics / meta-analysis / causal-inference design
**Treat as:** first submission — no assumption of prior review maturity.
**Files read:** the manuscript; `results/tables/META_DRG_axis_stouffer.csv`, `_R4_random_effects_meta.csv`, `P3_lodo_auc_ci_leakage_controlled.csv`, `P3_hub_genes.csv`, `P3_geneset_stats.csv`, `_R4_targetset_bootstrap_resamples.csv`, `_R4_supplementary_summary.json`, `_R4_nerveinjury_only_summary.json`, `_R4_translation_noncircular.json`. All numbers below were recomputed from these raw files, not transcribed from the manuscript text.

---

## Summary verdict

The quantitative core is **substantively sound and internally consistent**: the random-effects (DerSimonian–Laird) τ²/I² reproduce the stated formula, the Stouffer meta counts are self-consistent, BH-FDR is monotone, and the translation test is genuinely non-circular. The manuscript is also commendably honest about several weak spots (within-animal LODO, n=6 floor, EPV, RE collapse). My concerns are therefore **not** about arithmetic correctness but about (i) a documentation gap in the T0-1 sign fix, (ii) the headline "core" resting on a fixed-effect combination that loses ~81% of its genes under random effects, (iii) over-prominent AUC=1.000 / Jaccard=0.304 numbers whose caveats, while present, are under-weighted, and (iv) two minor reporting inconsistencies (gene-set q; "P=0.000" wording). None are disqualifying; all are fixable in revision. I judge the two deferred extensions (CAMERA, Knapp–Hartung) to be **acceptable as clearly-stated limitations** (see final section), not mandatory for acceptance.

---

## Findings

### F1. T0-1 Stouffer meta fix — internal consistency is verified

- 【Problem】 Need to confirm the post-fix meta counts are internally consistent and that the core is a proper subset of the meta-significant set.
- 【Evidence】 From `META_DRG_axis_stouffer.csv` (16,552 genes): `meta_FDR < 0.05` count = **6,558**; core defined as `meta_FDR < 0.05 AND consistency ≥ 0.8` = **2,750**. The core (2,750) is a strict subset of the meta-significant set (6,558), and both equal the values in `_R4_supplementary_summary.json` (`core_fixed_effect: 2750`) and the manuscript's stated 2,750 / 6,558 (`MVP_PLOSONE_submission.md:44`). Consistency threshold 0.8 equals ≥5/6 at K=6 (manuscript `:152`). No contradiction.
- 【Why it matters】 If the T0-1 sign repair had broken the pipeline, the core/DRG counts would diverge from the manifest; they do not. The fix preserved internal consistency.
- 【Specific fix】 No fix required for consistency. Keep the explicit statement "core = meta_FDR<0.05 AND consistency≥0.8 (2,750 genes)" — it is correct.

### F2. T0-1 fix is methodologically sound but invisible in the Methods

- 【Problem】 The sign-convention correction (TE-layer log2FC for sign, TE-layer p for magnitude) is a genuine bug-fix, yet the manuscript never documents it, so a reader cannot verify it and cannot distinguish it from the prior broken version.
- 【Evidence】 `META_DRG_axis_stouffer.csv` carries `lfc_GSE265957_Xtail_DRG_Day4` / `…Day63` (the TE-layer log2FC). In the post-fix data, every gene with `consistency == 1.0` (n=624 of the core, consistency==1.0 subset) has its Xtail TE-LFC sign equal to the meta_Z sign (624/624 = 1.000), confirming the Xtail contribution is now internally coherent. However `MVP_PLOSONE_submission.md:150` only says the translatome Z is "from the deposited Xtail p-values" and never states that the **sign** is taken from the **TE-layer** log2FC (as opposed to the total/mRNA-layer log2FC that caused the ~90% mismatch). The correction is absent from the text.
- 【Why it matters】 Reproducibility and the ability to defend the result against the prior round's criticism depend on the sign rule being explicit. As written, the meta-analysis looks unchanged from the version that contained the bug.
- 【Specific fix】 Add one sentence to Methods (`MVP_PLOSONE_submission.md:150`): "For the two GSE265957 translatome (Xtail ribosome-profiling) contrasts, the per-contrast Z takes its **sign from the TE-layer log2FC and its magnitude from the TE-layer p-value**; this corrects a prior version in which the sign was taken from the mRNA-layer log2FC, producing direction mismatch in ~90% of translatome entries. The fix is a within-contrast correction and does not alter the four bulk-contrast contributions."

### F3. Combining mRNA-layer and TE-layer Z in one Stouffer meta is conceptually mixed (mitigated, not resolved)

- 【Problem】 A single omnibus Z pools four bulk-mRNA contrasts with two translation-efficiency (TE) contrasts, implicitly assuming mRNA-abundance direction and TE direction reflect one latent "nerve-injury response."
- 【Evidence】 `META_DRG_axis_stouffer.csv` columns: 4 bulk LFC (`GSE267799`, `GSE212311`, `GSE278227`, `GSE241361`) + 2 TE LFC (`GSE265957_Xtail_Day4`, `…Day63`). Across all genes with an unambiguous TE direction, the TE-LFC sign agrees with meta_Z only 54.6% (4,195/7,677) — expected, because the other four studies dominate the pooled Z; the point is that TE and mRNA directions frequently diverge by design.
- 【Why it matters】 When translational regulation opposes transcript abundance (a standard "buffer/amplifier" pattern), the pooled Z can cancel signal or inject noise specific to one layer. This weakens the interpretation of the combined meta as a unified axis.
- 【Specific fix】 The bulk-only sensitivity analysis (overlap 63.2% strict / 89.2% relaxed, `:50`) is the right mitigation. Strengthen the caveat at `:44`/`:50` by stating explicitly that the primary 6-input meta **mixes a bulk-mRNA effect and a TE effect** and that conclusions should be cross-checked against the bulk-only core; optionally report the meta_Z recomputed on mRNA-only contrasts vs TE-only contrasts separately to show the two layers do not contradict.

### F4. Random-effects DL τ² / I² are correctly computed and reported

- 【Problem】 Verify the DL τ² and I² and the FE-vs-RE reporting.
- 【Evidence】 `I² = max(0,(Q−(K−1))/Q)·100` was recomputed for all 16,552 genes in `_R4_random_effects_meta.csv` and matched the reported `I2` in **0 mismatches**. τ² was recomputed from `τ² = (Q−(K−1))/C` with `C = Σw_i² − Σw_i⁴/Σw_i²` and the study weights stated at `:44/:152` (w = 2.19, 1.22, 2.65, 1.49, 1.00, 1.00). Using these (2-decimal-rounded) weights, τ² reproduces the reported values to rounding precision (example ATF3: computed 2.257 vs reported 2.2556, diff 0.06% = weight-rounding artefact). `median τ² = 0.266`, `median I² = 41.8%`, `% genes I²>50 = 43.9%`, `% τ²>0 = 69.7%` all match `_R4_supplementary_summary.json` exactly. The DL formula as written at `:154` is correct.
- 【Why it matters】 The RE sensitivity is the manuscript's central heterogeneity argument; its arithmetic is trustworthy.
- 【Specific fix】 No arithmetic fix. Consider reporting the per-gene study weights to full precision (not 2 decimals) in a supplement so τ² is exactly reproducible, and state that C is gene-invariant only because weights are study-level (constant across genes) — this is already implied but worth a clause.

### F5. FE→RE collapse (2,750 → 508, 18.5%) is the dominant threat to the meta conclusions

- 【Problem】 The primary "core" is fixed-effect; under random effects it loses ~81% of its genes, so the headline signature is extremely sensitive to the effect model.
- 【Evidence】 `_R4_random_effects_meta.csv`: core FE (`FDR_FE<0.05 & consistency≥0.8`) = **2,750**, core RE (`FDR_RE<0.05 & consistency≥0.8`) = **508** (18.5%). These equal `_R4_supplementary_summary.json` (`core_fixed_effect 2750`, `core_random_effects 508`, `RE_retains_pct 18.5`). FE `p<0.05` = 7,829 → RE `p<0.05` = 2,705. Among the 35 hubs, median I² = 79.1% and only 7/35 retain `FDR_RE<0.05` (`:46`, matches `_R4_translation_noncircular.json` `hubs_FDR_RE_lt05: 7`, `hubs_median_I2: 79.1`).
- 【Why it matters】 With 43.9% of genes at I²>50% and a median I²≈42%, the random-effects model is the *conservative, appropriate* choice, yet the manuscript presents FE as primary and RE as a "sensitivity bound." The practical effect: ~5.4× of the gene-level claim vanishes under the model a reviewer would favour. Gene-set and target-level claims that survive RE (OXPHOS q=0.0022; 4/10 targets RE-significant) are robust; the 2,750-gene core is not.
- 【Specific fix】 Promote random effects to **co-primary** (or present FE and RE cores side-by-side in the main Table 1 / a new "core stability" panel), and reframe `:46` so that gene-level conclusions are explicitly "conditional on the effect model." State plainly: "The 2,750-gene FE core should be read as an upper bound; the 508-gene RE core is the heterogeneity-robust estimate." This does not require new analysis — it is a presentation change.

### F6. Gene-set BH q is internally inconsistent between Abstract and Results

- 【Problem】 The set-level BH q for the four floor-pinned programmes is reported as 0.003 in the Abstract but 0.0022 in the Results.
- 【Evidence】 Recomputed BH across the 18 multi-member sets (`P3_geneset_stats.csv`, excluding Sigma-1) using the permutation p-values: Complement, Mitochondria_OXPHOS, DAM_microglia, Neuroinflammation all have `perm_p = 0.0005` and recomputed `BH_q = 0.0022`. So `MVP_PLOSONE_submission.md:48` ("q = 0.0022") is correct; `:18` (Abstract, "set-level BH q = 0.003 each") is wrong.
- 【Why it matters】 A 0.003-vs-0.0022 discrepancy in the Abstract is a copy-editing error that a careful reviewer will flag; it also slightly overstates the nominal significance in the Abstract.
- 【Specific fix】 Change Abstract `:18` "q = 0.003 each" → "q = 0.0022 each" to match the Results and the recomputed BH value. (Note the Abstract's OXPHOS "q = 0.0022" is already correct, so only the three neuroimmune sets need the Abstract edit.)

### F7. LODO "AUC = 1.000" framing is honest but over-weighted

- 【Problem】 Four folds report AUC 1.000, but they are not comparable as cross-animal discrimination evidence, and the union-selector AUC is not comparable to the 35-hub consensus AUC.
- 【Evidence】 `P3_lodo_auc_ci_leakage_controlled.csv`: GSE278227 (within-animal paired, n=28) AUC 1.000; GSE212311 (n=6) AUC 1.000; GSE241361 DRG (n=9) AUC 1.000; GSE241361 SC (n=9) AUC 1.000; GSE267799 (between-animal incision, n=20) AUC **0.677** (CI 0.374–0.940). The manuscript correctly discloses at `:64` that GSE278227 is within-animal and "not directly comparable" with GSE267799, that GSE212311 (n=6) is the only genuine cross-animal nerve-injury fold, and that its AUC 1.0 is "the statistical floor" (exact Mann–Whitney one-sided p=0.05). It also discloses `events-per-parameter ≈ 0.15` and that AUCs were computed on the within-fold **union of three selectors (140–169 features)**, *not* the published ≥2/3 consensus.
- 【Why it matters】 The framing is statistically honest, but listing four AUC=1.000 values prominently still implies a strong, reproducible signal. The only defensible between-animal nerve-injury evidence is a single n=6 fold at the statistical floor; the between-animal incision fold (the held-out translation test) is 0.677 with a CI spanning chance. The "nerve-injury-enriched" claim therefore rests on a within-animal pattern plus an n=6 floor.
- 【Specific fix】 (a) In the Results `:64` and the Abstract, lead with the *between-animal* result (GSE212311 n=6 floor + GSE267799 0.677) rather than the four AUC=1.000 values. (b) Add an explicit sentence: "AUCs reported here were computed on the 140–169-feature union selector and are **not** comparable to the 35-gene ≥2/3 consensus classifier; they bound the selection procedure, not the published hub set." (c) Report the degenerate CI [1.0,1.0] for every AUC=1.000 fold (already done for some) and explicitly call it "zero estimable precision."

### F8. Bootstrap "median Jaccard 0.304 / P=0.000" verifies numerically but signals instability, not robustness

- 【Problem】 The raw numbers are correct, but presenting them as if they support a stable hub set is statistically misleading.
- 【Evidence】 `_R4_targetset_bootstrap_resamples.csv` (200 resamples): median `jaccard_vs_published35` = **0.3039** (matches "0.304"), mean 0.3009, range 0.1765–0.4528; **0 of 200** resamples recover the full 35-gene set (so "P = 0.000" = observed 0/200). Critically, `recovered_hub_set_size` ranges **33–60** (median 43), and its correlation with Jaccard is **−0.09** (essentially zero) — i.e., instability is in *which* genes, not merely set size. A median Jaccard of 0.30 means each bootstrap set shares only ~30% (Jaccard) with the published 35.
- 【Why it matters】 A Jaccard of 0.30 is *low*; "no resample recovers the full set (P=0.000)" is evidence **against** stability, not reassurance. The manuscript's "stable enough to define a screening set" (`R66`) over-interprets a 30% overlap. The docking target list inherits this instability.
- 【Specific fix】 (a) Re-label: report "median Jaccard 0.30 (IQR …), indicating the 35-gene set is **not** robustly recovered by bootstrap — only the two strongest members (SPRR1A, ATF3) are resampling-stable." (b) Replace "P = 0.000" with "0 of 200 resamples (0%) recovered the full published set" — "P=0.000" implies a p-value where only an empirical rate exists (binomial exact upper bound ≈ 0.018). (c) State the recovered-set-size range 33–60 alongside the Jaccard so readers see the membership is volatile.

### F9. EPV for the ML and docking steps is far below conventional thresholds — honestly disclosed but conclusions should be down-weighted

- 【Problem】 Events-per-variable is <<10 in both the hub ML and the docking positive-control models, so reported discrimination is descriptive, not inferential.
- 【Evidence】 Manuscript `:64` reports `events-per-parameter ≈ 0.15` for the LODO hubs (n_test 6–28 vs 140–169 features). Docking controls (`:90`): AXL EPV≈1.9, TNIK≈1.4, ACVR1≈1.0, MAPK14≈2.0 — all "far below the conventional ≥10." I confirmed the feature counts from `P3_lodo_auc_ci_leakage_controlled.csv` (n_selected 140–169) and the LODO n (6–28).
- 【Why it matters】 With EPV≈0.15, perfect LODO AUC is expected from overfitting/selection, not biology; the docking "AUC 0.895→0.927" for AXL rests on ~9 events against ~7–9 parameters. The authors do say these are "descriptive and EPV-unstable rather than validation," which is correct, but the Results/Abstract still present AUC=1.000 folds as the hub evidence.
- 【Specific fix】 Keep the EPV disclosures (they are good) and add a one-line rule-of-thumb anchor: "With EPV < 1 (hubs) and EPV ≈ 1–2 (docking controls), no AUC or logistic discrimination here should be read as validation; they are hypothesis-generating." This binds the caveats already present into an explicit interpretive rule.

### F10. Multiple-testing registry is sound; Stouffer gene-set already uses correlation-aware permutation

- 【Problem】 Assess BH-FDR usage and whether the gene-set test needs the deferred CAMERA correction.
- 【Evidence】 `meta_FDR` in `META_DRG_axis_stouffer.csv` is monotone non-decreasing in p-order across all 16,552 genes (verified) — a necessary validity condition for BH. The gene-set test (`P3_geneset_stats.csv`) reports both `stouffer_p` and `perm_p` (2,000 permutations). The permutation p-values already account for inter-gene correlation within a set (e.g., Complement `perm_p = 0.0005` vs `stouffer_p = 1.55e-55`; Neuroinflammation `perm_p = 0.0005` vs `stouffer_p = 1.98e-108`). BH is applied across the 18 multi-member sets (Sigma-1 excluded). The Multiple-testing registry `:178` separates families correctly.
- 【Why it matters】 The permutation-based `perm_p` is already a correlation-aware statistic, so the gene-set inference is not anticonservative; BH q (recomputed: 0.0022 for the four floor sets) is valid. This materially weakens the need for the deferred CAMERA extension.
- 【Specific fix】 No fix required. Optionally note in Methods `:160` that permutation p-values are used for set-level inference precisely because they handle intra-set gene correlation, which is the same motivation CAMERA would address.

### F11. Consistency threshold 0.8 permits exactly one discordant contrast in most of the core

- 【Problem】 The core's 0.8 bar is lenient at K=6 and K=5.
- 【Evidence】 In `META_DRG_axis_stouffer.csv`, of the 2,750 core genes, 1,110 have `consistency == 1.0` (all measured contrasts agree) and **1,640 have 0.8 ≤ consistency < 0.9** — i.e. exactly 5/6 (K=6) or 4/5 (K=5) agreement, one dissenting contrast. So ~60% of the core rests on a single discordant study being tolerated.
- 【Why it matters】 A core where most members survive with one opposite-direction study is more fragile than "consistency ≥ 0.8" sounds; it interacts with F5 (RE collapse), since the dissenting contrast often carries the heterogeneity.
- 【Specific fix】 Report the split (1,110 at 1.0 vs 1,640 at 0.8–0.9) in Table 1 or a footnote, and consider a supplementary "strict core" (consistency == 1.0, n=1,110) as a robustness column so readers see how much of the signal needs only 5/6 agreement.

### F12. The two deferred extensions (CAMERA T2-4, Knapp–Hartung T2-5) — explicit judgement

- 【Problem】 State clearly whether a PLOS ONE reviewer would *require* these or whether honest limitation status suffices.
- 【Evidence / reasoning】 CAMERA (T2-4): the gene-set test already reports permutation p-values (`P3_geneset_stats.csv`), which absorb inter-gene correlation; BH is applied across 18 dependent sets (conservative under dependence). So the standard anticonservatism CAMERA fixes is already mitigated. Knapp–Hartung (T2-5): RE is computed with a normal approximation (`Z_RE`, `:154`); with K = 3–6 studies the t-approximation is more appropriate, and K-H would only widen CIs further (fewer significant → even more conservative than the already-drastic FE→RE drop). Good practice, but not outcome-determining here.
- 【Why it matters】 These are the two items most likely to be raised; a clear, pre-emptive stance prevents a revise-and-resubmit on a technicality.
- 【Specific fix】 See the dedicated judgement section at the end of this report.

---

## § Stands up (verified strengths)

1. **RE arithmetic is trustworthy.** I² from `I²=(Q−(K−1))/Q` matched the reported value for **all 16,552** genes (0 mismatches); τ² reproduced the DL formula to rounding precision (ATF3 2.257 vs 2.2556). The heterogeneity story rests on correct numbers (`_R4_random_effects_meta.csv`, `MVP_PLOSONE_submission.md:154`).
2. **Meta counts are internally consistent and reproducible.** `meta_FDR<0.05 = 6,558` ⊃ `core = 2,750`; both equal the manuscript and `_R4_supplementary_summary.json`. The T0-1 fix did not corrupt the pipeline (F1).
3. **The translation test is genuinely non-circular and honestly negative.** From `_R4_nerveinjury_only_summary.json`: NI-significant-and-consistent agreement with incision = 1,660/3,830 = 43.3% vs background 6,772/14,390 = 47.1% (perm_p = 0.0002). The 43.3% vs 47.1% framing (not a 50% null) and the lesion-class caveat are methodologically correct (`MVP_PLOSONE_submission.md:56–58`).
4. **Multiple-testing discipline is exemplary.** BH applied within families, monotone in the meta (verified), gene-set inference uses permutation p-values (correlation-aware), and a transparent registry separates inferential from descriptive tests (`:177–178`). This is above the usual PLOS ONE bar.
5. **LODO framing discloses its own weaknesses.** Within-animal vs between-animal, the n=6 floor, EPV≈0.15, and the union-selector-vs-consensus distinction are all stated (`:64`, `:164`). The honesty is a real strength even where the emphasis could be rebalanced (F7, F9).

---

## § Questions for the authors

1. The T0-1 sign fix (F2) is not described in the Methods. Please confirm the exact sign rule now used for the two GSE265957 TE contrasts and add it verbatim to `MVP_PLOSONE_submission.md:150`.
2. Given the FE→RE collapse to 508 (18.5%), why is fixed effect retained as *primary* rather than co-primary with random effects (F5)? Would you accept presenting both cores as equally prominent?
3. The LODO "nerve-injury-enriched" claim rests on (a) a within-animal GSE278227 pattern and (b) an n=6 GSE212311 fold at its statistical floor. Do you agree the between-animal nerve-injury evidence is effectively a single n=6 floor, and should the claim be softened accordingly (F7)?
4. The bootstrap median Jaccard is 0.30 with recovered-set sizes 33–60. Do you agree this indicates the 35-gene set is *not* robustly reproducible, and will you re-label it as such (F8)?
5. Will you correct the Abstract gene-set q from 0.003 to 0.0022 to match the Results and the recomputed BH (F6)?
6. For the deferred CAMERA and Knapp–Hartung analyses (F12), are you willing to add a one-paragraph "limitations of the statistical model" statement explicitly naming both as not performed, with the rationale that permutation p-values (gene-set) and the already-drastic RE sensitivity (meta) cover the same concern?

---

## § What I actually checked

**Files read (allowed set only):** `reports/MVP_PLOSONE_submission.md` (full, ~400 lines); `results/tables/META_DRG_axis_stouffer.csv` (16,552 rows); `results/tables/_R4_random_effects_meta.csv` (16,552 rows); `results/tables/P3_lodo_auc_ci_leakage_controlled.csv` (5 folds); `results/tables/P3_hub_genes.csv` (37 hubs); `results/tables/P3_geneset_stats.csv` (19 sets); `results/tables/_R4_targetset_bootstrap_resamples.csv` (200 resamples); `_R4_supplementary_summary.json`, `_R4_nerveinjury_only_summary.json`, `_R4_translation_noncircular.json`.

**Values recomputed from raw files (vs manuscript claims):**

| Quantity | Recomputed | Manuscript | Match |
|---|---|---|---|
| Stouffer `meta_FDR<0.05` | 6,558 | 6,558 (`:44`) | ✓ |
| Stouffer core (FDR<0.05 & cons≥0.8) | 2,750 | 2,750 (`:44`) | ✓ |
| RE core (FDR_RE<0.05 & cons≥0.8) | 508 | 508 (`:46`) | ✓ |
| I² = (Q−(K−1))/Q (all 16,552 genes) | exact match | reported I2 | ✓ (0 mismatches) |
| τ² via DL formula, 6-input weights | 2.257 (ATF3) | 2.2556 | ✓ (rounding) |
| median τ² / I² | 0.266 / 41.8% | 0.266 / 41.8% | ✓ |
| % genes I²>50 / τ²>0 | 43.9% / 69.7% | 43.9% / 69.7% | ✓ |
| hub median I² / RE-retained hubs | 79.1% / 7 | 79.1% / 7 | ✓ |
| Translation: NI-consistent 43.3% vs 47.1% bg | 1,660/3,830; 6,772/14,390 | `:58` | ✓ |
| Bootstrap median Jaccard | 0.3039 | 0.304 (`:66`) | ✓ |
| Bootstrap full-set recovery | 0/200 | "P=0.000" (`:66`) | ✓ (rate) |
| Bootstrap recovered-set size | 33–60 (median 43) | "median 43, range 33–60" (`:66`) | ✓ |
| Gene-set BH q (floor sets) | 0.0022 | 0.0022 (`:48`) but 0.003 (Abstract `:18`) | ✗ (Abstract only) |
| BH-FDR monotone in p-order | yes (16,552) | implied | ✓ |
| LODO AUCs (5 folds) | 1.0/1.0/1.0/1.0/0.677 | `:64`/`P3_lodo…csv` | ✓ |

**Discrepancies stated:**
- Abstract `:18` reports gene-set BH q = **0.003**; recomputed (and Results `:48`) = **0.0022**. Abstract error only (F6).
- "P = 0.000" for no full bootstrap recovery is an empirical rate (0/200), not a p-value; binomial exact upper bound ≈ 0.018 (F8).
- T0-1 sign-convention fix is absent from the Methods text although present in the data (F2).
- ~60% of the core (1,640/2,750) relies on exactly 5/6 or 4/5 agreement (F11).

**Not verified (data not delivered / not in allowed set):** I did not recompute the per-contrast Welch tests or the Xtail p-values (raw count matrices not provided); I verified only the *post-fix* meta outputs. The pre-fix "~90% direction mismatch" claim could not be independently reproduced from the delivered files — it is consistent with the post-fix coherence I observed (624/624 core consistency==1.0 genes have TE-LFC sign = meta_Z sign) but is not directly demonstrable from the provided CSVs.

---

## Explicit judgement: are CAMERA (T2-4) and Knapp–Hartung (T2-5) REQUIRED for acceptance?

**CAMERA / correlation-aware gene-set testing (T2-4) — NOT required; acceptable as an honestly-stated limitation.**
Reasoning: the gene-set statistics already report 2,000-permutation p-values (`P3_geneset_stats.csv`, `perm_p`), which are computed by permuting genes within the set and therefore absorb inter-gene correlation — the exact problem CAMERA solves analytically. The set-level BH is applied across 18 *dependent* sets, which is conservative under dependence. The four floor-pinned programmes (Complement, OXPHOS, DAM, Neuroinflammation) survive with `perm_p = 0.0005`, i.e. they are significant even after correlation-aware calibration. A PLOS ONE reviewer would not normally block on CAMERA when permutation p-values are already reported. **Recommendation:** keep permutation p-values as the primary inference and add one sentence in Methods (`:160`) noting that intra-set correlation is handled by permutation, so CAMERA was not separately required; optionally list it under Limitations as a possible refinement.

**Knapp–Hartung adjustment for the random-effects meta (T2-5) — NOT strictly required, but recommended; acceptable as a clearly-stated limitation given the current framing.**
Reasoning: the RE model uses a normal approximation (`Z_RE`, `:154`). With K = 3–6 contrasts, the t-based Knapp–Hartung interval is the statistically preferable choice and would widen confidence intervals, pushing *fewer* genes significant. However, two facts make this non-blocking: (i) the manuscript already presents RE as a *sensitivity bound*, not the primary claim, and (ii) the FE→RE drop is already so severe (2,750→508) that any further K-H attenuation only reinforces the paper's own "heterogeneity-sensitive" message rather than overturning it. So K-H would not change the conclusion; it would make the RE bound slightly more conservative. **Recommendation:** state explicitly in Limitations that the RE CIs use a normal approximation and that with K≤6 a Knapp–Hartung t-adjustment would be more rigorous but was not performed; note it would only strengthen the already-cautious RE framing. This pre-empts the almost-inevitable reviewer comment without requiring new computation. If the authors prefer, adding K-H is a small, mechanical extension (one `metafor::rma(..., test="knha")` call) and would fullyclose the item.

**Bottom line for both:** neither is a blocker for PLOS ONE acceptance *provided* the manuscript (a) keeps the permutation-based gene-set inference as primary (already done) and (b) adds a short, explicit "statistical-model limitations" paragraph naming both deferred extensions and the rationale above. The current manuscript already discloses enough honesty that a reasonable reviewer should accept this as limitation-status rather than mandatory revision — but the paragraph should be added so the reviewer does not have to infer it.
