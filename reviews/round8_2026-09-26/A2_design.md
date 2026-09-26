# Independent Peer-Review Report — Study Design & Statistical Correctness
**Reviewer role:** Biostatistician / meta-analysis methodologist (independent panel, Round 8)
**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis…" (Scientific Reports submission)
**Independence note:** Treated as a first submission; I did not read any prior review rounds, response/revision documents, `.workbuddy/memory/`, or other experts' files in this round.

---

## § Stands up (strengths — verified against the deposited tables)

1. **The non-circular translation test is correctly designed and the reported numbers are exact.** The signature is built on the five nerve-injury contrasts with the incision contrast held out, then tested once as a held-out direction test; the empirical (not 50%) null is used. I recomputed from `results/tables/_R4_nerveinjury_only_summary.json`: stratum `NI_FDR05_AND_NIcons>=0.8` = 2,266/4,899 = **46.25%** (manuscript "46.3%"), background `all_measured` = 6,779/14,390 = **47.11%** (manuscript "47.1%"), permutation p = **0.1396** (manuscript "0.14"), risk difference **−0.9 pp** (manuscript "−0.9 pp"). No circularity, no train/test leakage. This is a model of honest negative-design reporting.

2. **Set-level Benjamini–Hochberg correction is correctly implemented.** From `results/tables/_R4_geneset_setlevel_bh.csv`: the three floor-pinned sets (Neuroinflammation, Complement, DAM_microglia, perm_p = 1/2001 ≈ 0.00049975) propagate to q = 0.0029985 ≈ **0.003** under BH step-up across the 18 multi-member sets — exactly as reported (line 48, 237). OXPHOS fixed q = 0.02024 ≈ **0.020** and random-effects q = 0.3103 ≈ **0.31** are also exact. The authors correctly exclude the single-member Sigma-1 marker from set-level inference.

3. **The multiple-testing registry is explicit and family-disaggregated** (lines 163–164), and the three honesty boundaries (bulk-only overlap 54.3%, bootstrap 0/35 hubs ≥0.9 stable, human-miRNA null) are led with rather than buried. The causal-scope discipline statement (line 167) is unambiguous and appropriate.

4. **Sensitivity analyses bound the translatome fragility and are prominent.** `META_bulkonly_sensitivity_summary.json`: bulk-only core = 2,512, overlap with primary = 2,202/4,055 = **54.3%** (manuscript "45.7% of the primary core is translatome-dependent"). The collapse (5-input) core = 4,294 is also reported. These are the right robustness checks.

---

## § Issues (study-design / statistical)

### Issue A — Fixed-effect is presented as primary despite substantial heterogeneity; the 4,055→1,008 drop is a model-choice artifact, not just "fragility"
**【Problem】** The primary axis is the fixed-effect (FE) core while 41.9% of genes show I²>50% (and 55.3% show I²>30%), so the 4,055-gene FE core is an anti-conservative inflation that collapses 4-fold under random effects.
**【Evidence】** `results/tables/_R4_random_effects_meta.csv` (16,552 genes) recomputed: median τ² = **0.2324** (manuscript 0.232 ✓), median I² = **38.785%** (manuscript 38.8%/≈39% ✓), **41.9%** of genes I²>50% (manuscript 41.9% ✓), **55.3%** I²>30%, **68.1%** τ²>0 (manuscript 68.1% ✓). FE core = **4,055** and RE core = **1,008** both recomputed exactly from the CSVs (lines 46, 254). The RE computation itself is internally consistent (ATF3 row: Q=34.067 → I² recomputed 85.323 matches reported 85.323).
**【Why it matters】** Under heterogeneity, FE p-values (and the BH FDR built on them) are anti-conservative, so presenting the 4× larger FE set as primary reverses standard meta-analysis practice (Cochrane Handbook: random effects is the default when heterogeneity is anticipated/observed). Three-quarters of the "core" is heterogeneity-driven, so every gene-level claim resting on the 4,055 set is conditional on an unjustified model. The same fragility hits the hubs: `_R4_translation_noncircular.json` reports hubs_median_I² = 72.8% and hubs_FDR_RE_lt05 = 18/35 (only 18 of 35 hubs survive RE), yet 32/35 hubs sit inside the FE core that anchors the docking stage.
**【Specific fix】** *"We report the random-effects (DerSimonian–Laird) combination as the primary axis signature and present the fixed-effect core (n=4,055) as an optimistic upper bound; gene- and hub-level conclusions are drawn from the RE core (n=1,008; 18/35 hubs RE-significant) unless explicitly flagged as FE-conditional."*

### Issue B — GSE265957 is counted as two non-independent contrasts in the primary, and its weight is misstated
**【Problem】** The primary six-input meta-analysis treats two translatome timepoints from the same four animals (D4, D63) as two independent contrasts, and the manuscript misstates their relative variance weight.
**【Evidence】** Manuscript line 44: *"its w² = 2.00 versus 1.00–7.02 for the four bulk contrasts"* and *"twice the effective variance weight of a single bulk study."* Recomputed from `META_bulkonly_sensitivity_summary.json`: bulk w² = 4.80 (GSE267799), **1.50** (GSE212311), **7.00** (GSE278227), 2.22 (GSE241361). The valid bulk range is **1.50–7.00**, not 1.00–7.02; GSE265957 total w² = 2.00 is **1.33× the smallest bulk**, not "twice," and 0.29× the largest. (GSE265957 w = √(2·2/(2+2)) = 1.00 each, confirmed.)
**【Why it matters】** Two correlated contrasts from the same animals violate the independence assumption underlying Stouffer combination, inflating the effective sample size attributed to GSE265957. The misstated range ("1.00–7.02") obscures the real problem: the doubled input is an independence breach, not a 2× over-weighting, and the primary 4,055-gene result still rests on it.
**【Specific fix】** *"The primary analysis uses the collapse (5-input) or bulk-only (4-input) specification; the six-input version double-counts GSE265957 (same animals, D4+D63) and is retained only as an explicitly invalidated upper-bound sensitivity. The bulk w² range is corrected to 1.50–7.00."*

### Issue C — Leakage-controlled LODO is reported asymmetrically; 4/5 folds stay perfect under it, and the nerve-injury separations are circular with the meta core
**【Problem】** The leakage-controlled re-estimation is reported only for the incision fold, while under the *same* procedure 4 of 5 folds (including the largest, GSE278227 n=28) remain AUC = 1.000, and the perfect nerve-injury separations are expected by construction, not independent hub validation.
**【Evidence】** `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`: GSE278227 (n=28) AUC **1.000 [1.0,1.0]**; GSE212311 (n=6) **1.000**; GSE241361 DRG/SC (n=9 each) **1.000**; only GSE267799 incision drops to **0.677 [0.374,0.940]**. Manuscript line 64 reports only the 0.677 value and calls the classifier a *"resampling-sensitive candidate-generation tool rather than a validated classifier,"* but does not report that 2 of 3 cross-animal folds are perfectly classified even under leakage control.
**【Why it matters】** A perfect, leakage-controlled AUC on n=28 is implausible for noisy biological data and signals either residual leakage (e.g., the pooled gene z-scoring or union-of-fold features still inform the test fold) or trivial batch/platform separability. More fundamentally, the nerve-injury folds separate because features were *selected to be injury-discriminative across nerve-injury datasets*, so LODO re-confirms the meta core rather than independently validating the 35 hubs; the incision drop is the only honest generalization test. The manuscript's blanket "not validated" framing understates the nerve-injury signal and overstates the uniformity of the leakage correction.
**【Specific fix】** *"Under strict leakage control the cross-animal LODO floor is 0.677 (GSE267799); GSE278227 (n=28) and GSE212311 (n=6) remain 1.000 and are reported as descriptive upper bounds only, with the explicit caveat that perfect separation at n=28 indicates possible residual batch separability rather than validated hub biology; the LODO is framed as a restatement of the meta core, not independent hub validation."*

### Issue D — ADRA2A's own BH-corrected size-independent p-value is significant, contradicting "inconclusive" and "no target privileged"
**【Problem】** The manuscript labels ADRA2A docking "inconclusive, not a confirmed null" and states "no target is privileged," yet its own BH correction flags the ADRA2A size-independent ΔAUC as significant (q = 0.0025).
**【Evidence】** `results/tables/P6_BH_correction.csv`: ADRA2A size-independent ΔAUC p = **0.0005** → **Size-indep. BH q = 0.0025** — the *only* one of the five ChEMBL-annotated targets to pass BH on the size-independent test (others: 0.584, 0.3525, 0.584, 0.584). Manuscript Table 3b (line 276) and text (lines 112, 126) call it *"NS (…inconclusive)"* and *"neither prioritised nor excluded."* The MW-adjusted full-library AUC = **0.578** with a MW-only baseline of **0.462** (<0.5) on n ≈ 3,070 drugs.
**【Why it matters】** By the authors' own multiple-testing registry (family iv: BH across the five ChEMBL targets for both raw and size-independent p), ADRA2A carries a corrected-significant size-independent enrichment, which directly contradicts both the "inconclusive" verdict and the "no target privileged" claim. The p ≈ 0.0005 is also a library-size overpowering artifact (n ≈ 3,070): a negligible effect (AUC 0.578) is "significant" purely because of sample size, and the anomalous sub-0.5 MW-only baseline suggests the size-independent test is unstable for this target.
**【Specific fix】** *"ADRA2A is the single target with a Benjamini–Hochberg-significant size-independent enrichment (q=0.0025); this is reported as a weak, biologically negligible signal (MW-adjusted AUC 0.578; raw full-library AUC 0.532, NS) and is explicitly reconciled with the 'no target privileged' statement, rather than being labelled inconclusive while its own corrected p-value is significant. The size-independent test is flagged as library-size-sensitive (n≈3,070) and is not treated as independent evidence of enrichment."*

### Issue E — The plasma-miRNA layer is "underpowered" framed, but p = 0.51 is a genuine null, not a marginal miss
**【Problem】** The human plasma-miRNA layer is framed as "underpowered, not evidence of absence," yet the observed set-level p = 0.51 indicates no detectable signal to have been missed.
**【Evidence】** Manuscript line 70: set-level permutation p = **0.51**, n = 60, 253 plasma-detectable miRNAs. A p = 0.51 sits at the median of the 5,000-permutation null (observed statistic ≈ expected under null), so the test carries essentially no signal, not a small signal swamped by noise.
**【Why it matters】** "Underpowered" implies a true effect was present but undetected; with p = 0.51 the data contain no detectable association, so the honest statement is "no signal in a low-yield blood proxy." Reserving the underpowered caveat for the (untested) DRG/CSF validation is appropriate, but applying it to the plasma layer itself overstates the result.
**【Specific fix】** *"The plasma-miRNA set-level test returned p=0.51 (observed statistic at the permutation median), i.e. no detectable association in this blood proxy; we report it as a null boundary and reserve the 'underpowered' caveat for the planned DRG/CSF validation, where a true effect is plausible but untested."*

### Issue F — Impossible AUC dispersion is reported, and a wrong bulk w² endpoint compounds Issue B
**【Problem】** The pooled 5×20 repeated-CV is presented with a nominal ±0.004 dispersion that exceeds the [0,1] bound, and the manuscript's stated bulk w² range has a wrong lower endpoint.
**【Evidence】** Manuscript line 64: pooled 0.999 *"±0.004 dispersion exceeds 1.0 (a statistical impossibility)"* — acknowledged yet still displayed. Line 44's *"1.00–7.02 for the four bulk contrasts"* is wrong on both ends (recomputed valid range **1.50–7.00**; see Issue B). `P3_ml_metrics.csv` confirms pooled_5x20CV = 0.9992 vs perm null 0.4904.
**【Why it matters】** An AUC dispersion yielding an upper bound >1.0 is an impossible statistic and should not appear even as an "optimistic bound"; the wrong w² endpoint reinforces the double-weighting misstatement.
**【Specific fix】** *"The 5×20 repeated-CV is reported solely as a label-permutation-context upper bound (0.999 vs null 0.490) with no dispersion interval; the bulk w² range is corrected to 1.50–7.00."*

---

## § Questions for the authors
1. Given 41.9% of genes show I²>50% and the FE core is 4× the RE core, what is the justification for retaining FE as primary rather than RE (Cochrane default under observed heterogeneity)?
2. In `P3_lodo_auc_ci_leakage_controlled.csv`, GSE278227 (n=28) and GSE212311 (n=6) remain AUC = 1.000 under leakage control. Was out-of-fold feature selection truly applied to those folds, and if so, what explains perfect separation at n=28 — residual batch separability or incomplete leakage removal?
3. ADRA2A's size-independent ΔAUC passes your own BH correction (q = 0.0025). Do you therefore regard ADRA2A as carrying a (weak) positive signal, and how is that reconciled with "no target is privileged"?
4. For the random-effects model with only K=6 contrasts, did you consider the instability of the DerSimonian–Laird τ² estimator (and a t- rather than z-reference) given the small number of studies?
5. The MW-only baseline for ADRA2A full-library is 0.462 (<0.5). Is the size-independent test meaningful when its control baseline is anti-directed, and could this indicate MW is itself confounded with the ChEMBL annotation density for ADRA2A (88/115 actives in the analgesic subset)?

---

## § What I actually checked
**Files read (results/tables/):** `META_DRG_axis_stouffer.csv`, `META_bulkonly_meta.csv`, `META_bulkonly_sensitivity_summary.json`, `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_summary.json`, `_R4_translation_noncircular.json`, `_R4_translation_noncircular.csv`, `P3_lodo_auc_ci.csv`, `P3_lodo_auc_ci_leakage_controlled.csv`, `P3_ml_summary.json`, `P3_ml_metrics.csv`, `P3_hub_bootstrap.csv`, `_R4_targetset_bootstrap.csv`, `_R4_geneset_setlevel_bh.csv`, `P3_geneset_stats.csv`, `P6_BH_correction.csv`, `P6_breadth_chembl_power.csv`. Also read the full manuscript `reports/MVP_ScientificReports_submission.md` (283 lines).

**Commands/values recomputed (managed Python, pandas):**
- FE core = 4,055 (meta_FDR<0.05 & consistency≥0.8) — matches manuscript.
- RE core = 1,008 (FDR_RE<0.05 & consistency≥0.8) — matches manuscript.
- median τ² = 0.2324, median I² = 38.785%, 41.9% I²>50%, 55.3% I²>30%, 68.1% τ²>0 — all match manuscript except none contradicted.
- ATF3 I² recomputed from Q = 85.323 (matches reported).
- Bulk w² range recomputed = 1.50–7.00 — **discrepancy**: manuscript states "1.00–7.02".
- GSE265957 total w² = 2.00 = 1.33× smallest bulk — **discrepancy**: manuscript states "twice the effective variance weight of a single bulk study."
- Translation: 46.25% vs 47.11%, perm_p = 0.1396, RD −0.9 pp — matches manuscript (46.3%/47.1%/0.14).
- NI_core_FE = 5,412, NI_core_RE = 3,099 — match manuscript.
- Gene-set BH q values (0.003, 0.020, 0.31) — verified as correct BH floor propagation.
- ADRA2A size-independent BH q = 0.0025 — verified; contradicts manuscript's "inconclusive" framing.

**Discrepancies requiring author action:** (i) bulk w² range 1.50–7.00 not 1.00–7.02; (ii) GSE265957 is 1.33×, not 2×, the smallest bulk; (iii) ADRA2A size-independent q=0.0025 is BH-significant yet called "inconclusive." Issues A–F above are methodological, not arithmetic.
