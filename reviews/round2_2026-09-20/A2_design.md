# Reviewer A2 — Study design · statistical validity · permutation/MC · ML leakage · causal inference

**Manuscript:** "A neuroimmune–metabolic programme defines the chronic postsurgical pain DRG–spinal axis with an honest repurposing null" (Scientific Reports, Article)
**Reviewer role:** Design & statistics / causal inference / ML expert (independent Round-2 panel)
**Independence statement:** I have not read REVIEW_round1, the submission manifest, PROJECT_PLAN, gate scripts' outputs, README/CITATION, or any other reviewer's Round-2 file. I read only the manuscript, supplementary, reporting summary, cover letter, the `results/tables/*.csv` source-of-record tables, and `scripts/p2*.py`–`p6*.py` for method audit. Every headline number below was recomputed by me from the CSVs.

**Overall verdict:** *Major revision.* The work is unusually honest about its negative layers and the authors clearly understand leakage control in spirit. But the design and statistics contain several issues that change how strongly the conclusions can be stated — most importantly (i) a sample-relatedness/independence gap in the meta-analysis (GSE265957 split into two timepoints, undisclosed; GSE241361 same-animal leakage understated in the "honest" LODO), (ii) the pooled-CV AUC ≈ 1.0 is inflated by within-dataset leakage and is reported with an impossible ± that exceeds the AUC ceiling, and (iii) the "docking adds signal beyond chemotype" validation rests on logistic fits with only 9–13 positive cases and is internally contradicted by the simpler single-variable ΔAUC test and by ACVR1's own Wald test. None are fatal, but the manuscript currently over-states rigour in three places where it should be more cautious.

---

## § Stands up (what I verified and found correct)

1. **BH correction across the five targets is arithmetically correct.** I recomputed `P6_BH_correction.csv`. Raw Mann–Whitney p (AXL 1.11e-6, MAPK14 5.94e-5, TNIK 1.96e-4, ACVR1 1.03e-3, ADRA2A 0.118) yields BH q = 5.55e-6 / 1.48e-4 / 3.27e-4 / 1.29e-3 / 0.118, exactly matching the table. Size-independent p (ADRA2A 0.0005, AXL 0.141, TNIK 0.444, MAPK14 0.579, ACVR1 0.584) yields BH q = 0.0025 / 0.352 / 0.584 / 0.584 / 0.584 — also exactly matching. The "4/5 raw survive BH; only ADRA2A's size-independent p survives BH" reading is correct.

2. **The lift denominator for precision@10 = 0.700 is correctly the per-target known-binder prevalence, not a library-wide rate.** ADRA2A has 115 known ChEMBL binders among 3,070 scored drugs (Supplementary Table S3), base rate = 115/3070 = 0.03746. 0.700 / 0.03746 = 18.69, matching the reported lift ×18.69. This is the methodologically correct denominator for a target-specific lift. (A residual circularity concern about the composite score is raised separately below.)

3. **The honest-null docking conclusion is internally coherent and well defended.** The single-variable MW correction (`P6_enrichment_mw_confounder_check.csv`) shows that for AXL, TNIK, ACVR1 and MAPK14 the size-independent ΔAUC 95% CI *contains zero* (AXL [−0.030, +0.104]; TNIK [−0.224, +0.193]; ACVR1 [−0.176, +0.138]; MAPK14 [−0.078, +0.053]) — i.e. their raw AUC is fully explained by molecular weight. ADRA2A alone shows a significant size-independent increment (CI [+0.032, +0.110]) yet its full-library AUC is 0.532 (p = 0.118, NS) and its reverse-control AUC is 0.532 (fails). The manuscript's central claim — "no target clears all filters; honest null" — is the right call and is consistent with the data.

4. **The permuted label null (0.490 ± 0.085) confirms the ML labels carry genuine signal**, and the LODO range 0.917–1.000 for genuinely independent test sets is a real, defensible generalisation estimate (subject to the GSE241361 caveat below).

---

## Detailed findings (each with the four-part contract)

### F1 — Permutation p floor: three programmes sit exactly at the 1/2001 resolution limit (not "more significant")

【Problem】 Neuroinflammation, DAM microglia and complement are all reported at permutation p = 0.0005, which is the exact minimum observable value for a 2,000-permutation test — they are pinned to the resolution floor and cannot be ranked against each other by permutation.

【Evidence】 `P3_geneset_stats.csv`: perm_p = 0.0004997501249375312 for all three (Complement, DAM_microglia, Neuroinflammation) — that value equals 1/(2000+1) = 1/2001, the standard `(k+1)/(B+1)` permutation p with k = 0. OXPHOS is at 0.003998 (8/2001). Manuscript line 33 and Fig. 1 legend report "permutation p = 0.0005 each." Abstract line 14 says "all permutation p ≤ 0.004."

【Why it matters】 Pinning three programmes to the floor means the permutation calibration *cannot certify* that neuroinflammation is "more significant" than DAM or complement — their ordering rests entirely on the Stouffer Z (Neuroinflammation 21.55 > DAM 15.54 > Complement 14.60), not on permutation. Reporting "p = 0.0005" (an equality) overstates the precision of the calibration; it should be stated as a ceiling. This is a clarity/rigour issue, not a conclusion-breaker, but it propagates into the "coordinated neuroimmune activation … (permutation p = 0.0005 each)" framing.

【Specific fix】 Replace equality with the floor everywhere it appears: "permutation p ≤ 0.0005 (resolution floor of 2,000 permutations; programmes are not rankable against each other at this resolution; relative ordering is from the Stouffer Z)." Add one sentence in Methods: "With B = 2,000 permutations the minimum reportable two-sided p is 1/(B+1) ≈ 5.0×10⁻⁴; any gene set at this value is at the calibration floor."

### F2 — GSE265957 is split into two meta-datasets (D4, D63) from a single study, each n = 2/group, with undisclosed relatedness (potential Tier-0)

【Problem】 The Stouffer meta-analysis treats GSE265957 Day-4 and Day-63 as two independent datasets, but they are two timepoints of one tibial-nerve-injury mouse study; their relatedness (and whether they are longitudinal samples from the same animals) is never disclosed, and one study is thereby double-counted as 2 of 6 meta inputs.

【Evidence】 `scripts/p2_deg_meta.py` lines 137–158: both `GSE265957_Xtail_DRG_Day4` and `GSE265957_Xtail_DRG_Day63` are built from the *same* Xtail source and each is assigned weight `w = np.full(len, np.sqrt(2*2/4)) = 1.0` — i.e. n_case = n_ctrl = 2. The META header (`META_DRG_axis_stouffer.csv`) lists `lfc_GSE265957_Xtail_DRG_Day4` and `lfc_GSE265957_Xtail_DRG_Day63` as two of the six meta-datasets. Manuscript line 80 lists "GSE265957 DRG D4; GSE265957 DRG D63" with no relatedness caveat. Recomputed share of Σw²: GSE265957 contributes 2.0 / 17.53 ≈ **11.4%** of the meta weight from a single study; the "six-dataset" meta is in fact five independent studies, one represented twice. No `DEG_GSE265957*.csv` exists, so this cannot be cross-checked against per-contrast DEGs.

【Why it matters】 (a) *Solid, regardless of same-animal status:* one study supplying two of six meta-datasets inflates that study's influence and weakens the "independent-datasets" claim for the 4,055-gene core signature. (b) *If D4 and D63 are longitudinal samples from the same animals* (the typical design for a D4-vs-D63 time course), this is a sample-independence violation inside the meta-analysis: the two "datasets" are correlated, so the effective independent K is < 6 and the direction-consistency / permutation calibration overstates robustness. The manuscript discloses the GSE241361 DRG↔SC same-animal issue but is silent on GSE265957 — an asymmetric disclosure. This would be Tier-0 if same-animal longitudinal is confirmed. Note GSE265957 is *not* in the ML/LODO pool (that uses GSE278227, GSE267799, GSE241361 DRG, GSE241361 SC, GSE212311), so this affects only the meta core, not the 35-hub lock.

【Specific fix】 (i) Disclose explicitly: "GSE265957 contributes two timepoints (D4 acute, D63 chronic) from a single tibial-nerve-injury mouse study; each contrast has n = 2/group and both share study-level and (where applicable) animal-level relatedness." (ii) State whether D4/D63 are independent cohorts or same-animal longitudinal; if longitudinal, add a sensitivity meta-analysis that collapses GSE265957 to a single contrast (or down-weights it) and report whether the 4,055-gene core survives. (iii) In all "six-dataset" language, note it is five studies.

### F3 — Pooled CV AUC = 0.999 ± 0.004 is inflated by within-dataset leakage and is reported with an impossible ± that exceeds the AUC ceiling

【Problem】 The headline "honest evaluation confirmed real — not overfit — signal" leads with a pooled 5×20 repeated-CV AUC of 0.999 ± 0.004, but this pooled split disregards dataset boundaries (within-dataset samples can land in both train and test), inflating the number; and the reported ± implies an AUC > 1.0, which is impossible.

【Evidence】 `P3_ml_metrics.csv`: `pooled_5x20CV` AUC = 0.999209; the reporting summary line 14 and manuscript line 38 report "0.999 ± 0.004." Recomputed upper bound = 0.999209 + 0.004 = **1.0032 > 1.0** — an AUC cannot exceed 1.0, so the dispersion statistic as printed is invalid. Method (line 86) pools five datasets' 72 samples and runs "5×20 repeated stratified CV" — stratified by *label*, not by *dataset*, so correlated same-study/same-animal samples leak across the train/test split. The honest cross-dataset estimate is the LODO: mean of the five LODO AUCs = (1.0 + 0.9167 + 1.0 + 0.95 + 1.0)/5 = **0.973**, with the truly independent incision set at 0.917. So the leaked number (0.999) over-states the real generalisation (≈0.97, low 0.917) by ~0.03–0.08.

【Why it matters】 Presenting 0.999 as the proof of "not overfit" is misleading because the label-permutation null (0.490 ± 0.085) is computed on the *same leaked* split — both real and permuted labels leak equally, so the 0.999-vs-0.490 gap establishes that labels carry signal but does *not* establish no-overfit. The correct no-overfit evidence is LODO vs an LODO permutation null (not shown). The impossible ± also signals the dispersion was never sanity-checked against the [0,1] bound.

【Specific fix】 (i) Report the LODO (mean 0.973; range 0.917–1.000) as the primary generalisation metric and demote the pooled-CV to a clearly-labelled "in-sample, leakage-prone, optimistic" number, or replace it with a dataset-stratified CV that never mixes datasets in a fold. (ii) Never print a ± that crosses 1.0; if 0.004 is an SD, state it as such and cap the CI at 1.0, or report the LODO CIs (already in `P3_lodo_auc_ci.csv`). (iii) Add: "Pooled within-dataset CV is optimistic due to correlated samples within a dataset; LODO is the unbiased estimate."

### F4 — LODO for GSE241361 is same-animal leakage, understated as "not perfectly independent"

【Problem】 Both GSE241361 entries (mouse DRG AUC 1.000; mouse SC AUC 0.950) are the same animals' two tissues; when one is the LODO test set the other (same animals) remains in training, so two of the five "LODO" tests are within-animal, not cross-dataset. The manuscript discloses this but still counts both toward the "honest" LODO evidence alongside the three genuinely independent sets.

【Evidence】 Manuscript line 38: "GSE241361 DRG/spinal samples come from the same animals (LODO not perfectly independent; some test sets n < 10, widening CIs)." `P3_lodo_auc_ci.csv` shows GSE241361_mouseDRG AUC 1.000 (n=9) and GSE241361_mouseSC AUC 0.950 (n=9). The truly cross-animal independent LODO tests are only GSE278227 (1.000, n=28), GSE212311 (1.000, n=6), GSE267799 (0.917, n=20). The GSE241361 1.000 is therefore partly same-animal leakage and should not be presented on par with the others.

【Why it matters】 The "leakage-controlled dual-ML consensus" selling point is strongest for the three independent sets; folding the two same-animal GSE241361 tests into the same "LODO" banner overstates the independence guarantee. The most persuasive single number is GSE267799 at 0.917 — correctly highlighted in the text, but it is the *only* fully independent external model, and its CI is [0.729, 1.000].

【Specific fix】 In Fig. 2 and the Results, label the two GSE241361 tests explicitly as "same-animal, within-study validation (not cross-dataset)" and report the cross-animal LODO summary (n=3 tests: AUC 1.000 / 1.000 / 0.917) separately from the same-animal ones. State the honest floor as "cross-animal LODO down to 0.917."

### F5 — Sparsity (λ.1se = 1 gene) and the n = 72 / 13,208-gene / Top-800 pre-screen overfitting exposure of the 35-hub ensemble

【Problem】 The linear signal is extremely weak (the 1-SE regularised LASSO selects a single gene), so the "dual-ML consensus" is carried by RF and XGBoost on a univariate-Top-800 pre-screen built over 13,208 genes with only 72 pooled samples — a setting prone to noise-selected features and unstable hub identity.

【Evidence】 `P3_ml_summary.json`: `"lasso_1se_genes": 1`, `"n_common_genes": 13208`, `"pool": 800`. Method line 86: "Univariate t pre-screening (Top 800) fed three feature selectors." `P3_hub_genes.csv` shows the consensus is driven by RF Gini / XGBoost |SHAP| (LASSO λ.min bootstrap frequencies are modest: e.g. MAPK14 0.01, AXL 0.05, ACVR1 0.0, VASH2 0.0) — i.e. many "hubs" are RF/XGBoost picks, not LASSO picks. With n = 72 and 13,208 genes, a univariate Top-800 pre-screen over 13,208 tests is dominated by sampling noise; RF/XGBoost then easily memorise 72 samples across 800 features.

【Why it matters】 A classifier that generalises (LODO ≈ 0.97) does *not* imply the 35 individual genes are stable: any of many correlated gene sets could separate injured vs naïve. The hub *identity* may be a artefact of the noise-enriched pre-screen, which matters because the downstream single-cell/spatial localisation and the biological "35-hub programme" narrative rest on the specific gene list. The authors' own λ.1se = 1 caveat is acknowledged but under-weighted relative to the confident "35 hub genes with cross-route convergence" headline.

【Specific fix】 Add a stability analysis: bootstrap (or subsample) the full pipeline B ≥ 200 times and report, per gene, the selection-frequency across *all three* methods and the 95% CI of that frequency; demote any hub whose 3-method frequency is near the consensus threshold (≥2/3). Report the Top-800 pre-screen false-positive exposure explicitly (expected noise hits at univariate α among 13,208 tests). Consider requiring a gene to be selected in ≥ X% of bootstrap resamples to count as a hub.

### F6 — "Docking adds signal beyond chemotype" rests on logistic fits with 9–13 positive cases and is contradicted by the single-variable ΔAUC and by ACVR1's own Wald test

【Problem】 The multivariate physicochemical control is presented as validating the docking protocol for AXL/TNIK/ACVR1, but those fits have only 9–13 positive cases (events), the pooling n ≈ 3,000 overstates power, ACVR1's docking coefficient is non-significant by its own Wald test (p = 0.17) despite an "significant" LR test (p = 9.6e-4), and the effect sizes (AUC deltas 0.03–0.05) are trivial.

【Evidence】 `P6_multivariate_physchem_control.csv`: n_pos = AXL 13, TNIK 10, ACVR1 9, MAPK14 16, ADRA2A 115; `LR_dock_residual_p` = AXL 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4, MAPK14 0.066, ADRA2A 0.027; `Wald_neg_aff_p` (docking-coefficient Wald) = AXL 2.45e-5, TNIK 0.25, **ACVR1 0.172**, MAPK14 0.41, ADRA2A 0.50. So for ACVR1 the LR test says "significant" (9.6e-4) while the docking coefficient's individual Wald p is 0.172 — a direct internal contradiction explained by multicollinearity among the 6 physicochemical descriptors + docking affinity (`P6_enrichment_mw_confounder_check.csv` rho_affinity_MW: AXL −0.698, ACVR1 −0.603, MAPK14 −0.44). With only 9 events and 7 model parameters, the LR χ² approximation is unreliable; the "significance" is driven by large total n, not by a robust effect. Concurrently `P6_enrichment_mw_confounder_check.csv` shows the *single-variable* size-independent ΔAUC 95% CI contains zero for AXL, TNIK, ACVR1 and MAPK14 — i.e. the more interpretable test says docking adds no size-independent signal for these targets.

【Why it matters】 The manuscript pivots from the honest single-variable null to the multivariate LR to claim "docking affinity nonetheless still added statistically significant discrimination beyond chemotype for AXL/TNIK/ACVR1, partially validating the docking protocol" (line 54; repeated in Discussion). This over-states the validation: (a) the single-variable test — which the paper itself ran — says no increment; (b) the LR "significance" is on 9–13 events and is numerically contradicted by ACVR1's Wald p = 0.17; (c) even where "significant," the AUC deltas (AXL 0.895→0.927; TNIK 0.852→0.898; ACVR1 0.898→0.931) are small. MAPK14 (p = 0.066) is fairly called "marginal"; the AXL/TNIK/ACVR1 claim is not as solid as written.

【Specific fix】 (i) Report n_pos (events), not just total n, for every LR test; state that power is governed by the 9–13 events. (ii) Report the docking-coefficient Wald p alongside the LR p; reconcile the ACVR1 discrepancy (LR 9.6e-4 vs Wald 0.17) — do not lead with the LR p alone. (iii) Report the AUC deltas as the primary effect size; frame the LR as "a small, n-inflated, event-poor increment" rather than "validating the docking protocol." (iv) Soften "partially validating the docking protocol" to "the docking affinity contributes a small, statistically fragile increment beyond chemotype for AXL/TNIK/ACVR1 that does not survive the simpler size-independent test."

### F7 — precision@10 = 0.700 / lift ×18.69 denominator is correct (per-target), but the composite score's circularity with the test labels is unverified

【Problem】 The lift denominator is correctly ADRA2A's own known-binder prevalence (verified), but the composite ranking that achieves precision@10 = 0.700 "blends docking with pharmacological-prior terms," so testing it against ADRA2A ChEMBL binders risks circularity that the manuscript asserts away ("no double-dipping") without showing the prior terms are independent of the test labels.

【Evidence】 `scripts/p6_report.py` lines 343–344 assert "用 §7 的独立 ChEMBL 阳性集 … 无二重蘸取 (independent ChEMBL positive set … no double-dipping)," but the manuscript line 56 states the composite "blends docking with pharmacological-prior terms." If the pharmacological-prior component encodes ADRA2A-binding knowledge derived from the same ChEMBL pChEMBL ≥ 6 labels used as the test set (Supplementary Table S3 lists 115 ADRA2A ChEMBL binders), then precision@10 = 0.700 is partly tautological. Verified: base rate 115/3070 = 0.03746, 0.700/0.03746 = 18.69 (matches). The hypergeometric p = 9.4e-9 is therefore also contingent on the no-circularity assumption.

【Why it matters】 If circular, the precision@10 / lift is a prior-knowledge retrieval metric, not evidence that docking prioritises ADRA2A binders — which is exactly the distinction the manuscript tries to make ("knowledge-informed prioritisation metric rather than docking evidence"). The assertion of independence is currently unsupported by any audit showing the composite's prior terms exclude the 115 test labels.

【Specific fix】 Either (a) demonstrate that the composite's pharmacological-prior terms are computed from a *disjoint* ChEMBL subset (e.g., leave-the-target-out or a different activity source) than the 115 ADRA2A labels used for precision@10, or (b) explicitly relabel precision@10 as "knowledge-informed retrieval of known ADRA2A binders (circularity acknowledged), not an independent docking validation," and drop the hypergeometric p as a validity claim. The current single-sentence caveat is insufficient given the strong "no double-dipping" assertion.

### F8 — The "three filters (raw, size-independent, full-library)" framing collapses: raw and full-library are the same quantity

【Problem】 The honest-null logic is stated as "no candidate target cleared all three filters of raw, size-independent and full-library significance," but the "raw" and "full-library" filters are the *same* p-value (the Mann–Whitney p on the full library), so the three filters are really two.

【Evidence】 `P6_BH_correction.csv`: column `p_mannwhitney` (= raw full-library enrichment p) is what yields `BH_q_raw_enrich`; it is identical to the full-library AUC-based p in `P6_enrichment_mw_confounder_check.csv` (`p_mannwhitney` 1.11e-6 / 5.94e-5 / 1.96e-4 / 1.03e-3 / 0.118). Manuscript line 68: "no candidate target cleared all three filters of raw, size-independent and full-library significance." The real distinct filters are only (i) raw/full-library MW p and (ii) size-independent (MW-adjusted) p. ADRA2A passes only (ii); AXL/TNIK/ACVR1/MAPK14 pass only (i). None passes both.

【Why it matters】 Presenting two real filters as three overstates methodological rigour and makes the honest-null argument look like it survived one more gate than it did. The conclusion (no target clears all) is still true, but the framing is inaccurate.

【Specific fix】 Rephrase to "no target simultaneously showed a significant raw/full-library enrichment p AND a significant size-independent (MW-adjusted) p — the two distinct filters." Drop the redundant third term.

### F9 — SPRR1A "17.4×" is a mean log2-expression ratio mislabeled as a detection-fraction ratio; enrichment ratios are over-precise on n = 2–3/group

【Problem】 The manuscript reports "SPRR1A 98.1% vs 16.8% detection (17.4×)," but 98.1/16.8 = 5.84, not 17.4; the 17.4× is actually the *mean log2-expression ratio* (top_mean/others_mean = 3.0912/0.1777 = 17.41). The figure legend compounds the error by saying bars are "mean log2 expression ratio … not a detection-fraction ratio" and then parenthetically writing "SPRR1A 17.4× (98.1% vs 16.8% detection)."

【Evidence】 `P5_GSE216039_DRG_hub_finetype_top.csv`, SPRR1A row: `top_mean=3.0912, top_pct=0.981, others_mean=0.1777, others_pct=0.168, specificity=17.39`. So 17.39 = top_mean/others_mean (mean-expression ratio); 0.981/0.168 = 5.84 (detection ratio). Manuscript line 44: "SPRR1A 98.1% vs 16.8% detection (17.4×)" — the parenthetical is arithmetically wrong. Fig. 3 legend: "mean log2 expression ratio … not a detection-fraction ratio. Representative enrichments: SPRR1A 17.4× (98.1% vs 16.8% detection)" — self-contradictory.

【Why it matters】 A reader cannot tell which quantity the headline 17.4× refers to; the detection-ratio interpretation (5.84×) is materially smaller and would read as a weaker effect. More broadly, all the single-cell "×" ratios (ECEL1 25.7× = 0.989/0.0385; NPY 10.0× = 0.380/0.038; FLNC 10.2× = 0.385/0.038) are mean-expression ratios computed on pseudobulk means from **n = 2–3/group** (reporting summary line 9, manuscript line 46), yet are quoted to one decimal as if precise. Several `specificity` values are wildly unstable because the denominator is near zero (ANKRD1 123× on others_mean = 0.0002; VIP 227× on others_mean = 0.0).

【Specific fix】 (i) Correct line 44 and Fig. 3 legend to: "SPRR1A injured-neuron mean expression 17.4× that of other subtypes (detection 98.1% vs 16.8%, a 5.8× detection ratio)." Pick one ratio and use it consistently. (ii) Report these as qualitative "directional hints" with the n = 2–3/group caveat stated adjacent to every ratio, and round to whole-number or omit the decimal (e.g., "~17×"). (iii) Drop or footnote the near-zero-denominator specificity values (ANKRD1 123×, VIP 227×) as unstable.

### F10 — Single-cell n = 2–3/group yields 0 BH-significant genes, yet specific enrichment ratios are reported prominently

【Problem】 The authors correctly state all single-cell calls are "directional hints" (0 BH-significant genes at n = 2–3/group), but then feature precise enrichment ratios (SPRR1A 17.4×, ECEL1 25.7×) and regionalisation fractions (e.g., SPRR1A dorsal-horn detection 0.098, ATF3 0.077) in the abstract, Results and figures as if they were findings.

【Evidence】 Manuscript line 46: "Sample-level pseudobulk gave 0 BH-significant genes in both datasets (n = 2–3/group), so all single-cell calls are directional hints." Yet line 44 leads with "SPRR1A 98.1% vs 16.8% detection (17.4×), ECEL1 25.7×, NPY 10.0×, FLNC 10.2×"; Supplementary Table S2 reports detection fractions to three decimals (SPRR1A top_detection 0.098, etc.). With n = 2–3/group, a detection fraction of 0.098 corresponds to roughly 1–2 of ~20 spots/cells and has an enormous binomial CI.

【Why it matters】 Prominent, decimal-precise ratios on n = 2–3/group invite over-interpretation of noise; the "directional hints" disclaimer is easy to miss next to the precise numbers. This is the same over-precision issue as F9 but at the single-cell/spatial layer.

【Specific fix】 Move all n = 2–3/group quantitative ratios into a clearly bounded "exploratory / directional hints" subsection or supplementary-only, state the binomial CI (or n) next to each fraction, and avoid one-decimal precision. Keep the qualitative localisation narrative in the main text.

---

## § Questions for the authors

1. **GSE265957 relatedness (F2).** Are GSE265957 D4 and D63 independent animal cohorts or longitudinal samples from the same animals? If the latter, did you run a sensitivity meta-analysis collapsing them to one contrast, and does the 4,055-gene core survive? Please also justify the hardcoded weight w = 1.0 (n = 2/group) for both contrasts — is the true per-group n really 2, or was it taken from the provided Xtail table regardless of the original study's sample size?
2. **CV leakage (F3).** Was the pooled 5×20 CV stratified by dataset or only by label? Please provide the LODO permutation-null AUC distribution so the no-overfit claim rests on the unbiased estimate, not the leaked pooled number. What is the source of the ±0.004 — SD or SE — and why does it exceed the AUC ceiling?
3. **LR validation (F6).** For AXL/TNIK/ACVR1, please report (a) the docking-coefficient Wald p (not just LR p), (b) the actual β and 95% CI of the docking-affinity term, and (c) a bias-reduced / Firth logistic or exact-ish check given 9–13 events vs 7 parameters. How do you reconcile ACVR1 LR p = 9.6e-4 with Wald p = 0.17?
4. **Circular composite (F7).** Which exact terms constitute the composite's "pharmacological-prior" component, and are any of them derived from the same ChEMBL pChEMBL ≥ 6 ADRA2A labels used to score precision@10? If yes, please re-derive precision@10 with a leave-the-target-out prior.
5. **Hub stability (F5).** Have you bootstrapped the full pipeline to estimate per-gene selection-frequency CIs? How many of the 35 hubs survive a stricter stability threshold (e.g., selected in ≥80% of bootstrap resamples by ≥2/3 methods)?
6. **Permutation floor (F1).** Do you agree the three programmes at p = 0.0005 should be reported as a floor ("≤ 0.0005, resolution-limited") rather than as an exact, rankable p?

---

## § What I actually checked

**Files read (manuscript & supporting):**
- `reports/MVP_ScientificReports_submission.md` (full; line cites above)
- `reports/MVP_ScientificReports_supplementary.md` (full; Tables S1–S4)
- `reports/MVP_ScientificReports_reporting_summary.md` (full)
- `reports/MVP_ScientificReports_cover_letter.md` (full)

**Source-of-record tables recomputed (in `results/tables/`):**
- `P3_geneset_stats.csv` — perm_p values, frac_up; confirmed three programmes at 1/2001 = 0.00049975 floor; OXPHOS 0.003998 (=8/2001).
- `P3_lodo_auc_ci.csv`, `P3_ml_metrics.csv`, `P3_ml_summary.json`, `P3_hub_genes.csv` — LODO AUCs, pooled-CV 0.999209, λ.1se = 1, n_common = 13,208, pool = 800. Recomputed LODO mean = 0.973; pooled+SD = 1.0032 (>1.0).
- `P6_BH_correction.csv` — recomputed BH q for raw and size-independent; matched manuscript exactly (AXL 5.55e-6, MAPK14 1.48e-4, TNIK 3.27e-4, ACVR1 1.29e-3, ADRA2A 0.118; size-indep ADRA2A 0.0025, AXL 0.352, TNIK/ACVR1/MAPK14 0.584).
- `P6_multivariate_physchem_control.csv` — LR vs Wald discrepancy (ACVR1 LR 9.6e-4 vs Wald 0.172); n_pos 9–13 for AXL/TNIK/ACVR1.
- `P6_enrichment_mw_confounder_check.csv` — single-variable ΔAUC CIs all contain zero for AXL/TNIK/ACVR1/MAPK14; only ADRA2A significant; rho_affinity_MW correlations.
- `P6_face_validity.csv`, `P6_face_validity_alpha2_individual.csv` — analgesic AUC 0.538 (p=0.146); alpha-2 agonists on ADRA2A AUC 0.292 (raw) / 0.428 (MW-adj, p=0.76).
- `P6_breadth_target_summary.csv`, `_paired_vs_adra2a.csv`, `_target_rank_stability.csv` — ADRA2A Tier-1 0.618 → full-library 0.532 confirmed via `P6_enrichment_mw_confounder_check.csv`.
- `P5_GSE216039_DRG_hub_finetype_top.csv` — confirmed SPRR1A specificity 17.39 = mean ratio (3.0912/0.1777), not detection ratio (0.981/0.168 = 5.84); near-zero-denominator instability (ANKRD1 123×, VIP 227×).
- `META_DRG_axis_stouffer.csv` / `_CORE_signature.csv` headers — confirmed GSE265957 appears as two contrasts (Day4, Day63).

**Method-audit scripts read (allowed):**
- `scripts/p2_deg_meta.py` (lines 110–170) — confirmed GSE265957 D4/D63 built from one Xtail source, each w = sqrt(2·2/4) = 1.0 (n=2/group); meta is 5 studies represented as 6 datasets.
- `scripts/p6_report.py` (lines 335–377) — confirmed precision@10/lift computed against per-target base rate; "no double-dipping" assertion present but unverified.

**Commands run:** `grep` for GSE265957 across tables/scripts; `python3` recomputation of permutation floor (1/2001), GSE265957 weight share (11.4%), ADRA2A base rate (0.03746) and lift (18.69), LODO mean (0.973) and pooled+SD (1.0032), and BH q-values (matched).

**Discrepancies found vs manuscript:**
1. SPRR1A "17.4×" is a mean-expression ratio, not the 98.1%/16.8% detection ratio (which is 5.84×) — arithmetic error in line 44 and Fig. 3 legend (F9).
2. Pooled CV ±0.004 implies AUC > 1.0 — invalid dispersion (F3).
3. ACVR1 LR p (9.6e-4) contradicts its own Wald p (0.17) — selective reporting of the favourable test (F6).
4. "Three filters" = two distinct filters (raw ≡ full-library) (F8).
5. GSE265957 relatedness/independence undisclosed; one study double-counted as 2/6 meta inputs (F2).
6. GSE241361 same-animal LODO tests presented alongside independent ones without separation (F4).
7. Permutation p = 0.0005 reported as equality, not floor (F1).

**What I did NOT do:** I did not re-run AutoDock Vina or the ML training; I audited their reported outputs and the method code only. I did not access GEO to confirm GSE265957's animal-level design (flagged as a question). I treated all files as a first submission per the independence rules.

---

## Recommendation

**Major revision.** The scientific story — a neuroimmune–metabolic CPSP axis with specific nociceptor-channel down-regulation, plus an honestly negative human and docking layer — is valuable and the negative reporting is commendable. But before acceptance the authors must (a) resolve the GSE265957 relatedness/independence gap and the GSE241361 same-animal LODO framing (F2, F4), (b) stop leading with the leaked 0.999 pooled-CV and the impossible ± (F3), (c) retract or heavily qualify the "docking validates the protocol" claim given 9–13-event logistic fits and the contradicting single-variable/Wald tests (F6), (d) fix the SPRR1A ratio arithmetic and the over-precise n = 2–3/group ratios (F9, F10), and (e) correct the "three filters" and permutation-floor wording (F8, F1). None require new experiments; all are re-statements, one sensitivity meta-analysis, and one stability audit.
