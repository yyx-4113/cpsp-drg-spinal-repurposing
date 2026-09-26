# Independent Design & Statistics Review — A2 (design layer)

**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
**Review type:** First-submission-style independent peer review (design / meta-analysis / causal inference / ML-leakage / enrichment methodology).
**Reviewer:** A2 (design & statistics).
**Independence note:** I read only the manuscript (`reports/MVP_ScientificReports_submission.md`) and the raw result tables under `results/tables/`. I did not read any prior `REVIEW_*`/`RESPONSE_*`/`REVISION_*` files, prior round folders, or planning/verification documents. Every quantitative claim below was recomputed by me from the supplied CSV/JSON; the manuscript's self-reported numbers are treated as assertions, not evidence.

---

## F1. Stouffer weighted-Z weights: valid inverse-variance weighting, no double-counting

【Problem】None identified. The weight formula and its interpretation are arithmetically and statistically correct.

【Evidence】Weights stated in the manuscript: GSE267799 12/8 → 2.19, GSE212311 3/3 → 1.22, GSE278227 14/14 → 2.65, GSE241361 DRG 4/5 → 1.49. I recomputed `w = sqrt(n_case·n_ctrl/(n_case+n_ctrl))` and obtained 2.1909, 1.2247, 2.6458, 1.4907 respectively — exact matches. The translatome timepoints 2/2 → 1.000 each, also exact.

The statistical claim "this weighting is algebraically the inverse-variance (effective-n) weight" is correct: defining the standardized effect `d_i = Z_i/w_i`, under the null `Var(d_i) = 1/w_i²`, so the fixed-effect inverse-variance meta of `d_i` gives `d_meta = Σ(w_i·Z_i)/Σw_i²` and `Z_meta = d_meta·√Σw_i² = Σ(w_i·Z_i)/√Σw_i²` — exactly the Stouffer formula used. I also reproduced the primary meta from the bulk-only per-contrast Z (full precision) and the weights: SCN8A bulk `meta_Z = −4.923567` (manuscript −4.923567) and SCN9A `−2.924735` (manuscript −2.924735). The implementation is correct.

【Why it matters】A reviewer could suspect that combining a z-statistic with an n_eff weight "double-counts" sample size. It does not: the weight is applied once per contrast and is the inverse-standard-deviation weight for the standardized effect. Under H0, `Z_meta ~ N(0,1)` for any fixed non-random `w_i`, so the combined test is valid regardless.

【Specific fix】No change required. If anything, a one-sentence clarification that the inverse-variance interpretation is asymptotic (large-sample t→z) would pre-empt a spurious "double-counting" objection, but this is optional.

---

## F2. GSE265957 contributes two translatome timepoints treated as *independent* contrasts — within-study double representation

【Problem】The single tibial-nerve-injury study GSE265957 is entered twice (D4, D63), each as a separate input with weight 1.00. These are two ribosome-profiling timepoints from the **same animals**, so they are not independent contrasts. Treating them as independent double-represents one study in the meta and slightly violates the independence assumption of Stouffer's method.

【Evidence】`META_bulkonly_sensitivity_summary.json` lists only the four bulk studies; the primary six-contrast meta adds GSE265957 D4 and D63 (each `n_case=2, n_ctrl=2`, weight 1.00). In `META_DRG_axis_stouffer.csv` the columns `lfc_GSE265957_Xtail_DRG_Day4` and `lfc_GSE265957_Xtail_DRG_Day63` are both present, and the consistency filter uses `K=6`. The two timepoints therefore each contribute a full contrast to both the meta-Z and the consistency vote.

【Why it matters】Stouffer's method assumes independent contrasts. Two correlated timepoints from one study inflate that study's effective influence (combined weight 2.00 ≈ 11.4% of Σw²) and can bias both the meta-Z magnitude and the consistency statistic. This is distinct from, and additional to, the measurement-heterogeneity problem (F4): it is a *dependence* problem. The effect is small because the weights are only 1.00 each, but it is a real design flaw that the "bulk-only sensitivity" (which removes the whole study) does not separately isolate.

【Specific fix】Either (a) collapse GSE265957 to a single contrast (the manuscript already has a "collapse-sensitivity" analysis merging the two timepoints — report its core and note it as the dependence-corrected primary rather than a secondary sensitivity), or (b) explicitly state that the two timepoints are treated as exchangeable/non-independent and add a small inflation of the effective-K or a within-study correlation term. At minimum, add one sentence: "The two GSE265957 timepoints are from the same animals and are therefore not statistically independent; their joint contribution is disclosed and bounded by the bulk-only and collapse sensitivities."

---

## F3. Direction-consistency definition is vote-counting and the ≥0.8 threshold is not comparable across K

【Problem】Minor. `consistency = max(n_up, n_dn)/K` with `K≥3` is a vote-count statistic, and the meaning of the `≥0.8` cutoff changes with K: for K=6 (primary) it requires ≥5/6 agreement; for K=4 (bulk-only) it effectively requires 4/4 (since 3/4 = 0.75 < 0.8). The two cores therefore use different directional-stringency filters, complicating direct comparison.

【Evidence】Primary core: `meta_FDR<0.05 & consistency≥0.8` over K=6 → I recomputed 4,055 genes (matches). Bulk-only core: K=4 → 1,981 genes (matches `META_bulkonly_sensitivity_summary.json`). With K=4, the only way to reach 0.8 is 4/4, so the bulk-only core is strictly a "all-four-bulk-contrasts-agree" set, whereas the primary core admits 5/6.

【Why it matters】The two cores are filtered at different effective stringencies, so the 42.7%/57.3% overlap (F4) is partly an artifact of differing consistency thresholds, not only of the translatome's inclusion. It does not invalidate the fragility conclusion, but the threshold should be stated per-K.

【Specific fix】State the *minimum number of agreeing contrasts* implied by `≥0.8` for each K (e.g., "primary K=6 → ≥5/6; bulk-only K=4 → 4/4"), and consider a K-normalized consistency (e.g., `(max(n_up,n_dn)−min(n_up,n_dn))/K`, the directionality index) so the threshold is comparable across meta sizes. Not blocking.

---

## F4. Translatome mixing: arithmetic correct, bulk-only remedy appropriate, but the primary analysis still mixes measurement types

【Problem】The arithmetic of the headline fragility claim is correct; the remedy (bulk-only sensitivity) is the right response. The only residual issue is that the *primary* meta still combines a ribosome-profiling translatome (Xtail log2FC → z) with bulk-transcriptome z-statistics, which is a measurement-scale heterogeneity the manuscript discloses but does not fully neutralize except by sensitivity.

【Evidence】Overlap 1,732 / 4,055 = 0.4271 → 57.3% not recovered (recomputed exactly; manuscript 42.7%/57.3%). Primary core 4,055, bulk-only core 1,981, overlap 1,732 (all three match the JSON). The translatome carries only ~11.4% of Σw² yet its removal drops 57.3% of the primary core — this *is* strong evidence of fragility, and the arithmetic supports the "most important fragility" framing.

【Why it matters】The claim is honest and correctly computed. The concern is only that a reader may take the 4,055-gene primary core as the definitive result when it is demonstrably translatome-dependent. The manuscript already leads with this caveat, which is commendable.

【Specific fix】No arithmetic fix. Consider promoting the bulk-only (or collapse) core to co-primary status rather than labelling it a "sensitivity," since the translatome is the single largest source of instability. The current framing ("reported as the primary result … random-effects as sensitivity bound") is acceptable given the explicit disclosure.

---

## F5. Random-effects (DerSimonian–Laird) aggregate statistics are internally coherent — the hypothesized contradiction does not exist

【Problem】None identified. I specifically tested the prompt's hypothesis of an internal contradiction ("68.1% τ²>0" vs the D-L floor, and "median I²=38.8%" vs "41.9% I²>50%"). Neither is contradictory.

【Evidence】From `_R4_random_effects_meta.csv` (16,552 genes) I recomputed exactly: median `τ² = 0.2324` (ms 0.232); median `I² = 38.785` (ms 38.8); fraction `I²>50 = 41.9%` (ms 41.9); fraction `τ²>0 = 68.1%` (ms 68.1). Coherence checks: (i) 0 genes have `τ²>0` but `I²≤0`; (ii) `τ²>0` count = `I²>0` count = 11,269 (= 68.1%); (iii) `τ²==0` fraction = `I²==0` fraction = 31.9% — exactly the floor behavior. The I² distribution is right-skewed: 25th pct = 0, 50th = 38.8, 75th = 67.6, 90th = 79.8, 95th = 84.1; only 8.1% of genes fall in (38.8, 50]. Hence "median 38.8%" and "41.9% > 50%" coexist because the 50th percentile sits below 50 and an 8.1% sliver fills the gap — fully coherent.

The RE core = 1,008 genes (FDR_RE<0.05 & consistency≥0.8) = 24.9% of the 4,055 FE core (both recomputed exactly). Given median I²≈39% and 41.9% of genes >50%, a ~75% shrinkage of the core is consistent with the stated heterogeneity.

【Why it matters】The D-L floor `τ² = max(0, …)` means `τ²>0` is reported precisely for genes with `Q > K−1`; the 31.9% with `τ²=0` are genuinely homogeneous. There is no "τ²>0 where Q<K−1" contradiction. The aggregate statistics are sound and the RE sensitivity is a legitimate addition.

【Specific fix】No change required. Optionally, replace "68.1% showing τ²>0" with "68.1% of genes showed Q>K−1 (non-zero heterogeneity)" to make the floor relationship explicit to readers.

---

## F6. Non-circular translation test is sound; "non-predictive" is a fair conclusion

【Problem】None identified (minor clarification only).

【Evidence】From `_R4_nerveinjury_only_summary.json`: background agreement 6,779/14,390 = 47.11% (ms 47.1%); the nerve-injury-significant AND nerve-injury-consistent stratum 2,266/4,899 = 46.25% (ms 46.3%), risk difference vs background −0.9 pp (ms −0.9), permutation p = 0.1396 (ms 0.14). The nerve-injury-only core = 5,412 (FE) / 3,099 (RE) (both match). From `_R4_translation_noncircular.json`, the non-circular NI-consistency stratum 2,318/4,306 = 53.83% (ms 53.8%); circularity inflation = 15.6 pp (69.4% pooled-consistency minus 53.8%). Both non-circular strata (46.3% and 53.8%) are non-significant (p=0.14 and p=0.79), and the stricter 46.3% stratum is *below* background.

【Why it matters】The permutation/empirical-null approach (re-labelling stratum membership, 5,000 draws, against a 50% null rightly rejected for global directional skew) is appropriate. The conclusion that nerve-injury regulation carries essentially no information about incision direction is supported by the data and is honestly framed.

【Specific fix】No change required. One optional note: the two non-circular computations (46.3% from a NI-only *meta-significance* filter; 53.8% from the primary meta-significance + NI-consistency filter) are not identical; state explicitly that both are "non-circular" and that the 46.3% stratum is the stricter, pre-registered-style test used as the headline.

---

## F7. Set-level BH across 18 overlapping gene sets — correct q-values, but independence is nominal

【Problem】Minor. The BH q-values are computed correctly, but the 18 sets are *not* independent (they share genes: Neuroinflammation, Complement, DAM_microglia, MAPK_kinase, Synaptic, etc. overlap). Applying BH across 18 dependent sets is conservative (FDR still controlled under positive dependence) but the "18 tests" overstates the number of independent hypotheses.

【Evidence】I recomputed the BH from `P3_geneset_stats.csv`/`_R4_geneset_setlevel_bh.csv`. The three floor-pinned sets (Neuroinflammation, Complement, DAM_microglia) all have `perm_p = 1/2001 = 0.00049975`; the manuscript assigns them tied rank 3, giving `perm_q = 0.00049975 × 18/3 = 0.0030` each — correct tied-BH. OXPHOS fixed `perm_q = 0.0202` (ms 0.020), random `perm_q = 0.3103` (ms 0.31) — both exact. The resolution-floor handling ("reported as an upper bound; ordered by Stouffer Z") is honest and the primary q uses `perm_q`, not the astronomically small `stouffer_q` — the right choice. Sigma-1 (single member) is correctly excluded from set-level inference.

【Why it matters】BH controls FDR under arbitrary dependence conservatively, so the q-values are defensible. But the overlapping-set structure means the effective test count is <18, so the correction is slightly anti-conservative in the opposite direction only if sets are *negatively* dependent (not the case here). The practical risk is over-stating "18 independent gene-set tests passed." Low risk.

【Specific fix】Optional: state "the 18 sets overlap and are therefore not independent; BH is applied conservatively and controls FDR under dependence." Not blocking. The current reporting (q=0.003 for the three floor-pinned sets, ordered by Z) is acceptable.

---

## F8. Dual-ML hub stability and candidate-set framing are internally consistent and honestly bounded

【Problem】None identified. The bootstrap and LODO claims are all verified, and the "candidate set, not locked" framing is consistent with the docking target list being structurally determined.

【Evidence】`P3_hub_bootstrap.csv`: per-gene recovery `hub_freq` ranges 0.005–0.155; max = 0.155 (CDHR5). 0/35 reach ≥0.9 stability (recomputed). `lasso_freq = 0.0` for all 35 hubs → LASSO contributed no selections under resampling, confirming the "effective consensus reduced to RF∩XGBoost" statement. `_R4_targetset_bootstrap.json`: resampled hub-set size median 6 (IQR 5–8), Jaccard vs published 35 median 0.026, `P(≥3 of 17)=0.040`, `P(≥5 of 17)=0.000`, mean 0.79/17 dock-eligible and 0.35/9 docked recovered per resample — all match. `_R4_targetset_bootstrap.csv`: CDHR5 recovery 0.155 = "most stable dock-eligible hub" — confirmed.

`P3_lodo_auc_ci.csv` (recomputed): GSE278227 AUC 1.000 [1.0,1.0] n=28; GSE267799 0.917 [0.729,1.0] n=20; GSE241361 DRG 1.000 [1.0,1.0] n=9; GSE241361 SC 0.950 [0.709,1.0] n=9; GSE212311 1.000 [1.0,1.0] n=6. Cross-animal mean (excluding the two same-animal GSE241361 folds) = 0.917–1.000 across three folds — matches. Three folds have degenerate [1.0,1.0] CIs, correctly flagged as non-informative.

`P3_hub_genes.csv`: 32/35 in meta-core (ms 32/35), 5 full three-method consensus (SPRR1A, ATF3, TFE3, CDHR5, GALNS — matches), 30 by exactly two methods (matches).

【Why it matters】The leakage control (LODO, same-animal folds excluded from cross-animal mean, degenerate CIs not interpreted, pooled CV reported only as leakage-inflated upper bound with the 0.490±0.085 permutation null) is exemplary. The bootstrap showing 0/35 stable hubs is the honest basis for calling the 35 a candidate set, and the docking target list is correctly justified by structural tractability (`n_holo_PDB ≥ 1`), not hub rank.

【Specific fix】No change required. The λ.1se = 1 gene (sparse linear signal) caveat and the same-animal GSE241361 non-independence caveat are both already stated.

---

## F9. Docking reverse controls and MW correction are correctly computed and adequately controlled

【Problem】None identified on computation. Treating docking-score rank as an AUC is a standard, sound descriptive enrichment metric (rank of known binders vs the rest); the MW confounder correction (MW-only baseline, MW-linear, MW-quintile-stratified, and the size-independent ΔAUC) is adequate.

【Evidence】`P6_reverse_control.csv`: AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779 (all `reliable=True`, method-validation controls); ADRA2A 0.532 (`reliable=False`) — all match. `P6_enrichment_mw_confounder_check.csv`: ACVR1 ΔAUC vs size-only p = 0.584 (CI [−0.176, +0.138], contains 0); ADRA2A full-library AUC 0.532, MWU p = 0.118 (NS), MW-adjusted 0.578; AXL ΔAUC CI [−0.030, +0.104] p = 0.141; MAPK14 ΔAUC p = 0.5785; TNIK ΔAUC p = 0.4435 — all match the manuscript. `P6_breadth_chembl_power.csv`: ADRA2A Tier-1 (620-drug) AUC 0.618 → full-library (3,085-drug) 0.532, p = 0.118 — the breadth flip is verified. `P6_BH_correction.csv`: raw BH-q and size-indep BH-q across the 5 ChEMBL targets recompute exactly (e.g., ACVR1 raw q 0.00129, ADRA2A size-indep q 0.0025, AXL raw q 5.5e-6). `P6_face_validity.csv`: 0/64 analgesics in Top-20 (≈0.4 expected); rank AUC 0.538 p = 0.146; α2-agonists on ADRA2A MW-adjusted AUC 0.428 p = 0.76 — all match.

【Why it matters】The full-library breadth, reverse positive controls, and MW correction directly address the "double-dipping" risk the manuscript criticizes in the field. The honest null is well-supported: no target clears both the raw and size-independent filters, and known analgesics are not enriched.

【Specific fix】No change required.

---

## F10. ACVR1 multivariate likelihood-ratio "significance" has an *undisclosed* internal LR-vs-Wald contradiction and severe over-parameterization

【Problem】The manuscript correctly flags that ACVR1's LR p = 9.6e-4 "contradicts its own single-variable size-independent Wald test (p = 0.584)" and rests on only 9 positive events. But the raw multivariate table contains a *second*, stronger* contradiction the manuscript does not report: within the same multivariate logistic model, the LR test (p = 9.6e-4) disagrees with the **Wald test on the docking-affinity coefficient** (p = 0.172, `P6_multivariate_physchem_control.csv`, column `Wald_neg_aff_p`). LR–Wald disagreement is the classic signature of an ill-conditioned information matrix — exactly what arises when 9 positive events are fitted against ~7–8 parameters (6 chemotype descriptors + affinity + intercept; EPV ≈ 1.1–1.3, far below the 10-events-per-parameter rule of thumb).

【Evidence】`P6_multivariate_physchem_control.csv`: ACVR1 `n_pos = 9`, `AUC_phys = 0.8983`, `AUC_combined = 0.9308`, `LR_dock_residual_p = 0.0009567`, `Wald_neg_aff_p = 0.1718`. So the affinity term is "significant" by LR (0.001) but "not significant" by Wald (0.17). For AXL, TNIK, ADRA2A, MAPK14 the LR and Wald agree directionally (AXL LR 2.6e-5 / Wald 2.4e-5; TNIK LR 7.3e-5 / Wald 0.25; ADRA2A LR 0.027 / Wald 0.50; MAPK14 LR 0.066 / Wald 0.41) — but for ACVR1 specifically the LR/Wald gap is large and is the red flag. The manuscript quotes only the single-variable size-independent p (0.584) and the LR p (9.6e-4); it never cites the multivariate Wald p = 0.172.

【Why it matters】The "event-poor, n-inflated" caveat is already in the text, which is good. But presenting the LR p = 9.6e-4 in the Results ("docking affinity nonetheless still added statistically significant discrimination beyond chemotype for AXL, TNIK and ACVR1") while omitting that the *same model's* Wald test on that very coefficient is non-significant (0.17) and that EPV ≈ 1 leaves the LR p-value unstable. A reader could over-trust the ACVR1 "significance." The omission is not fatal (the family is post-hoc and excluded from inferential claims) but it undercuts the otherwise-exemplary honesty.

【Specific fix】Either (a) drop the ACVR1 LR p-value from the "still added significant discrimination" list and report only AXL and TNIK there (both have LR and Wald agreeing and far more events: 13 and 10), or (b) keep it but add: "For ACVR1 the LR test (p = 9.6e-4) disagreed with the Wald test on the affinity coefficient (p = 0.17) and the model had only 9 positive events against ~7 parameters (EPV ≈ 1), so this 'significance' is unstable and not interpreted." Paste-ready replacement for the ACVR1 clause in the Results: *"the ACVR1 likelihood-ratio test (p = 9.6e-4) is unstable: it conflicts with both its own single-variable size-independent Wald test (p = 0.584) and the multivariate Wald test on the affinity coefficient (p = 0.17), and rests on only 9 positive events against ~7 parameters (EPV ≈ 1); we therefore treat it as a non-reproducible fluctuation rather than signal."*

---

## F11. Composite (knowledge-informed) ranking is honestly framed as descriptive retrieval

【Problem】None identified. The composite ranking (precision@10 = 0.700, lift ×18.69, hypergeometric p = 9.4e-9 / 1.3e-8) is explicitly framed as prior-driven retrieval, not docking evidence, and is excluded from inferential claims in the MT registry.

【Evidence】Manuscript: "these are knowledge-informed *retrieval* metrics, not independent docking evidence, and their hypergeometric p-values … largely restate the prior terms rather than the docking term and are not cited as validating it (pure ADRA2A Vina affinity placed 0/10 known binders in the Top-10)." The MT registry states composite-ranking hypergeometric p-values "are reported as descriptive retrieval metrics and are explicitly not counted among the corrected inferential tests." This is internally consistent with F9/F10.

【Why it matters】This is the correct way to report a prior-informed ranking without letting it masquerade as a hypothesis test. No issue.

【Specific fix】No change required.

---

## F12. Multiple-testing registry is correctly separated; causal scope is appropriately hedged

【Problem】None identified. The six families are non-overlapping in hypothesis space and the post-hoc multivariate control and composite-ranking p-values are explicitly excluded from inferential claims. Causal language is consistently hedged.

【Evidence】Registry families: (i) per-dataset DE BH; (ii) meta-analysis BH (fixed & RE separately); (iii) gene sets BH across 18 sets; (iv) docking BH across 5 ChEMBL targets (raw and size-independent); (v) single-cell sample-level BH; (vi) multivariate physicochem (5-test, post-hoc, excluded). I verified the (iv) BH q-values in F9. Causal scope: the manuscript states the work is "observational reanalysis … no intervention, no temporal ordering, no perturbation; all findings are associations" and that "response"/"programme" are descriptive. The Abstract frames the axis as "nerve-injury-associated transcriptional response, not a CPSP-specific mechanism," and the non-circular test is used to deny incision translation rather than assert causation. I found no result-section sentence that implies causation.

【Why it matters】Clean separation of families and explicit exclusion of post-hoc/descriptive statistics from inference is exactly the discipline expected. The causal-scope statement is a model of transparency for an observational reanalysis.

【Specific fix】No change required. Optional: the term "programme" (e.g., "neuroimmune–metabolic programme") could be read as mechanistic by a careless reader; add "(descriptive)" on first use, consistent with the causal-scope paragraph.

---

## § Stands up (verified-robust elements, with evidence)

1. **Stouffer weighting is a correct inverse-variance weight and the implementation reproduces the meta-Z exactly.** Recomputed weights 2.1909/1.2247/2.6458/1.4907 (match) and reproduced SCN8A bulk `meta_Z = −4.923567`, SCN9A `−2.924735` from per-contrast Z and weights (F1).

2. **Random-effects D-L statistics are internally coherent — no contradiction.** Recomputed median `τ² = 0.2324`, median `I² = 38.785`, `I²>50 = 41.9%`, `τ²>0 = 68.1%` (all exact); 0 genes with `τ²>0` but `I²≤0`; `τ²>0 ⟺ I²>0`; the 8.1% of genes in (38.8, 50] reconcile the median-38.8 vs 41.9%-over-50 coexistence (F5).

3. **Non-circular translation test is methodologically sound and the "non-predictive" conclusion is fair.** Background 47.11%, NI-consistent 46.25%, −0.9 pp, permutation p = 0.14 (all recomputed); the stricter stratum is *below* background, so nerve-injury regulation carries no information about incision direction (F6).

4. **Dual-ML leakage control is exemplary.** LODO cross-animal floor 0.917–1.000 (three folds), same-animal GSE241361 folds correctly excluded from the cross-animal mean, three degenerate [1.0,1.0] CIs flagged non-informative, pooled CV reported only as leakage-inflated upper bound with permutation null 0.490±0.085; bootstrap 0/35 hubs ≥0.9 stable, LASSO 0 selections — all recomputed and consistent (F8).

5. **Docking honesty infrastructure is correct.** Reverse controls, MW correction, full-library breadth flip (0.618→0.532, p=0.118), BH across 5 targets, and face-validity (0/64 analgesics in Top-20) all recompute exactly; composite ranking correctly framed as descriptive (F9, F11).

6. **Multiple-testing registry and causal hedging are model-grade.** Six non-overlapping families; post-hoc multivariate and composite-ranking p-values explicitly excluded from inference; consistent "association, not causation" framing throughout (F12).

---

## § Questions for the authors (do NOT guess answers)

1. For GSE265957, what is the within-study correlation between the D4 and D63 translatome contrasts, and does collapsing them (the collapse-sensitivity analysis) materially change `ATF3`/positive-control ranking or the 4,055-gene core membership beyond the reported 91.4% retention? Should the collapse-sensitivity core be promoted to co-primary?

2. In the multivariate logistic model for ACVR1 (9 positive events, ~7 parameters, EPV ≈ 1), were the chemotype descriptors standardized/regularized, and does the LR–Wald disagreement (p = 9.6e-4 vs 0.17) persist under penalized estimation (e.g., Firth or ridge)? If so, should the ACVR1 LR result be removed from the "added significant discrimination" sentence?

3. The manuscript states the incision model GSE267799 CPSP-adjacency is "asserted by the source, not independently verified here" (harvest-day caveat). Given that the entire "non-predictive translation" conclusion rests on this single incision arm, what is the planned confirmatory design (e.g., an additional incision dataset or a within-species nerve-injury→incision paired contrast) and is any such data already accessible?

4. The bulk-only core (1,981) and primary core (4,055) use different consistency thresholds (4/4 vs ≥5/6). If a K-normalized consistency index were used, how many of the 57.3% "translatome-dependent" genes are recovered, i.e., how much fragility is threshold-driven vs truly translatome-driven?

5. The human-miRNA layer (GSE158825, n = 60) returns p = 0.51. Given the underpowered, blood-proxy design, was any prospective power analysis done, and at what effect size would a plasma-miRNA association have been detectable? This bears on whether the "honest negative" is informative or simply underpowered.

---

## § What I actually checked (files, recomputations, discrepancies)

**Files read:** `reports/MVP_ScientificReports_submission.md`; `results/tables/META_bulkonly_sensitivity_summary.json`, `_R4_nerveinjury_only_summary.json`, `_R4_translation_noncircular.json`, `P3_geneset_stats.csv`, `_R4_geneset_setlevel_bh.csv`, `P3_hub_bootstrap.csv`, `P3_lodo_auc_ci.csv`, `P3_hub_genes.csv`, `_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap.json`, `P6_reverse_control.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_breadth_chembl_power.csv`, `P6_BH_correction.csv`, `P6_face_validity.csv`, `P6_multivariate_physchem_control.csv`, `META_DRG_axis_stouffer.csv`, `_R4_random_effects_meta.csv`, `META_DRG_axis_CORE_signature.csv`.

**Recomputations performed (all reproduced the manuscript's numbers):**
- Stouffer weights: 2.1909 / 1.2247 / 2.6458 / 1.4907 / 1.00 (exact).
- Stouffer meta-Z from per-contrast Z + weights: SCN8A −4.923567, SCN9A −2.924735 (exact).
- Primary FE core = 4,055; genes at meta_FDR<0.05 = 6,869 (exact).
- RE: median τ² = 0.2324, median I² = 38.785, I²>50 = 41.9%, τ²>0 = 68.1%, RE core = 1,008 (24.9% of FE) — all exact. Coherence: 0 τ²>0/I²≤0 conflicts; τ²>0 count = I²>0 count = 11,269; I² percentiles 0/38.8/67.6/79.8/84.1; 8.1% in (38.8,50].
- Non-circular: background 47.11%, NI 46.25% (p=0.14), RD −0.9 pp; NI core 5,412/3,099; NI-consistency stratum 53.83% (circularity inflation 15.6 pp) — all exact.
- Gene-set BH: Neuroinflammation/Complement/DAM perm_q = 0.0030 (tied rank 3); OXPHOS fixed 0.0202, random 0.3103 — exact.
- Hub bootstrap: max 0.155 (CDHR5), 0/35 ≥0.9, all lasso_freq = 0; target-set median size 6 (IQR 5–8), Jaccard 0.026, P(≥3)=0.040, P(≥5)=0.000, mean 0.79/17 & 0.35/9 — exact.
- LODO AUC/CI/n: 1.000[1,1] n28; 0.917[0.729,1] n20; 1.000[1,1] n9; 0.950[0.709,1] n9; 1.000[1,1] n6 — exact.
- Docking: reverse-control AUCs 0.880/0.824/0.797/0.779/0.532; MW ΔAUC p 0.584/0.0005/0.141/0.5785/0.4435; breadth 0.618→0.532 (p=0.118); BH q (raw & size-indep) exact; face-validity 0/64 Top-20, rank AUC 0.538 (p=0.146), α2-agonists MW-adj 0.428 (p=0.76) — all exact.
- Multivariate: ACVR1 LR p = 9.6e-4 **but Wald_neg_aff_p = 0.172** (undisclosed internal disagreement; n_pos = 9).

**Discrepancies found:** None in the manuscript's reported arithmetic. One *omission* (not an arithmetic error): the ACVR1 multivariate Wald p = 0.17 is not reported alongside the LR p = 9.6e-4 (F10). One *design* issue: GSE265957's two timepoints are treated as independent contrasts (F2). One *minor* threshold-comparability issue: consistency ≥0.8 means different agreement counts at K=6 vs K=4 (F3). One *nominal* issue: BH across 18 overlapping (non-independent) gene sets (F7). All others verified exactly.

**Bottom line:** The design-layer statistics are, with one exception (F10), arithmetically correct and methodologically honest. The single substantive addition I request is disclosure of the ACVR1 LR–Wald contradiction and its EPV≈1 over-parameterization; the remaining items (F2, F3, F7) are clarifications that strengthen an already-transparent manuscript.
