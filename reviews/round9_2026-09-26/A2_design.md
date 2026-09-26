# A2 — Meta-analysis / Biostatistics / Causal-inference Design Review

**Manuscript:** `reports/MVP_ScientificReports_submission.md` (283 lines, PLOS ONE resubmission)
**Reviewer role:** Study-design & statistical-defensibility audit
**Date:** 2026-09-26
**Independence:** Treated as a first submission; I read only the manuscript, the panel brief, and the raw tables in `results/tables/`. Every number below was recomputed by me from those tables.

---

## 1. GSE265957 translatome double-counting: the "w² = 2.00 versus 1.22–2.65" sentence is internally inconsistent and overstates the inflation

【Problem】 The Results sentence at L44 claims GSE265957 "contributes twice the effective variance weight of a single bulk study (its w² = 2.00 versus 1.22–2.65 for the four bulk contrasts)" — this mixes a squared quantity (w²) against a raw-weight *range* (w) and the "twice" claim is false in variance-weight terms.

【Evidence】 I recomputed every weight from the stated per-group n via w = √(n_case·n_ctrl/(n_case+n_ctrl)) and squared them:
- GSE267799 12/8 → w = 2.1909 (manuscript 2.19 ✓); w² = 4.800
- GSE212311 3/3 → w = 1.2247 (1.22 ✓); w² = 1.500
- GSE278227 14/14 → w = 2.6458 (2.65 ✓); w² = 7.000
- GSE241361_DRG 4/5 → w = 1.4907 (1.49 ✓); w² = 2.222
- GSE265957 D4 2/2 → w = 1.000 ✓; D63 2/2 → w = 1.000 ✓; combined Σw² contribution = 1.00² + 1.00² = 2.000

Total Σw² = 17.5222. GSE265957's two timepoints therefore account for **2.000/17.5222 = 11.4%** of the total variance weight. The four bulk studies' individual w² values are **{1.50, 2.22, 4.80, 7.00}**, i.e. a single bulk study ranges from 8.6% (GSE212311) to 40% (GSE278227) of Σw². GSE265957's 2.00 contribution is:
- 1.33× the smallest bulk study (GSE212311 1.50),
- 0.90× GSE241361_DRG (2.22),
- 0.42× GSE267799 (4.80),
- 0.29× GSE278227 (7.00).

So GSE265957 is **comparable to one midsize bulk study (GSE241361, 12.7%), not twice any single bulk study.** Meanwhile the sentence's "1.22–2.65" is the *range of the four bulk w values* (raw w, not w²); setting "its w² = 2.00" against that w-range is a unit error. Note the sentence is also self-contradictory: it says both "w² = 2.00 versus 1.22–2.65" (implying 2.00 lies *within* a single bulk study's weight span, hence comparable to one) **and** "twice the effective variance weight of a single bulk study" — these cannot both be true.

The four bulk individual weights are correctly enumerated elsewhere in the same sentence ("1.22, 1.49, 2.19 and 2.65") and match the Methods (L140) and `META_bulkonly_sensitivity_summary.json` (weights 2.19089, 1.22474, 2.64575, 1.49071). The inconsistency is confined to the "w² = 2.00 versus 1.22–2.65 / twice" phrasing in the Results.

【Why it matters】 The double-counting concern is real (one animal cohort, D4 + D63, split into two non-independent inputs), but the prose overstates it as "twice a bulk study," which (a) is statistically false, (b) invites a methodological reject on a quantitative error, and (c) distracts from the *actual* fragility, which is the translatome *measurement type*, not the two-timepoint split. The honest robustness checks are sound: bulk-only overlap 2,202/4,055 = 54.3% (recomputed from `META_bulkonly_sensitivity_summary.json`: overlap 2202, primary_core 4055, overlap_pct 54.32%) and collapse retention 3,707/4,055 = 91.4% (recomputed from `META_collapse_meta.csv`: shared_core 3707, orig_core 4055, 0.9142). So the *bounding* is fine; only the inflation sentence is wrong.

【Specific fix】 Replace the sentence in L44 with:
> "Because the two translatome timepoints each carry weight w = 1.00, they together contribute 2.00 to Σw² (2.00/17.52 ≈ 11.4% of the total variance weight), which is comparable to — not twice — a single midsize bulk study (GSE241361_DRG w² = 2.22, 12.7%; GSE212311 w² = 1.50, 8.6%) and far below GSE278227 (w² = 7.00, 40%) or GSE267799 (w² = 4.80, 27%). The two timepoints are from the same animals and are therefore not statistically independent; their joint influence is bounded by the bulk-only (overlap 54.3%) and collapse (retention 91.4%) sensitivity analyses below."

---

## 2. Fixed-effect PRIMARY despite a heterogeneity thesis: choice is asserted, not justified, and sits in tension with the paper's own numbers

【Problem】 The paper reports the fixed-effect (FE) core (4,055) as the primary result and the random-effects (RE) core (1,008, 24.9%) as a mere sensitivity bound, even though 41.9% of genes show I² > 50% and the core collapses by 75% under RE — and no positive methodological justification for FE-primary is actually written.

【Evidence】 L46 ("Random-effects sensitivity analysis"): "median τ² = 0.232 and median I² = 38.8%, with 41.9% of genes showing I² > 50% … Under random effects the core … shrank to 1,008 genes, 24.9% of the fixed-effect core. The fixed-effect core is therefore reported as the primary result and the random-effects core as its sensitivity bound." I directly recounted the FE core from `META_DRG_axis_stouffer.csv` (rows with meta_FDR < 0.05 and consistency ≥ 0.8) = **4,055** (matches). The RE core 1,008 is stated in the manuscript and consistent with the heterogeneity statistics but I could **not** re-derive it: the primary Stouffer CSV has no RE column, and the RE computation lives in `_R4_random_effects_meta.csv` (referenced in Data Availability) which I did not have in `results/tables/`. The Methods (L140–142) labels "Fixed-effect (primary)" and defines RE as "the sensitivity bound," but the *rationale* given is circular ("is therefore reported as the primary result … as its sensitivity bound") — it restates the decision, it does not defend it against the measured heterogeneity. The specific justification the prompt asks about — "we report FE as primary because heterogeneity-sensitivity is the thesis" — is **not present** in the text. What is present is a hedge ("gene-level conclusions … should be read as conditional on moderate between-contrast heterogeneity," L46) but not a forward justification for elevating FE above RE.

【Why it matters】 The manuscript's headline contribution is precisely that the axis is "heterogeneity-sensitive" (Abstract; L44; L46; Discussion L120). Reporting the most heterogeneity-fragile number (4,055, which loses 75% of its membership under RE) as *primary* while the heterogeneity-robust number (1,008) is demoted to "sensitivity" is structurally backwards relative to the thesis. A reasonable reviewer will read this as selective emphasis on the larger, less robust figure. It does not invalidate the work (the fragility is openly disclosed and even led-with in L50), but the *primary/sensitivity* hierarchy is unjustified and should be either justified explicitly or flattened.

【Specific fix】 Either (a) present FE and RE as **co-primary** and report the FE∩RE intersection as the robust core (add one sentence: "The 1,008-gene RE core and its overlap with the 4,055-gene FE core define the heterogeneity-robust subset; gene-level claims are restricted to that overlap where stability matters"), or (b) keep FE primary but add an explicit convention-based justification in L46, e.g.: "We report the FE core as primary because the FE combination is the conventional fixed-combination summary for real-sample-size weighting and because the heterogeneity-sensitivity thesis is itself the object of the RE/bulk-only/collapse sensitivity suite; FE-conditional claims are flagged throughout." Do not leave the choice assertion-only.

---

## 3. Non-circular translation test: numbers are correct, denominator is consistent, and the empirical-null (not 50%) reference is the right one

【Problem】 None — this is a correctly executed, well-controlled test. I record it as verified (and as a "stands up" item) so the panel knows it was checked.

【Evidence】 Recomputed from `results/tables/_R4_nerveinjury_only_summary.json`, stratum `NI_FDR05_AND_NIcons>=0.8`: k = 2,266, n = 4,899 → 2,266/4,899 = **0.4625 = 46.3%** (manuscript 46.3% ✓). Background stratum `all_measured`: k = 6,779, n = 14,390 → 6,779/14,390 = **0.4711 = 47.1%** (manuscript 47.1% ✓). Risk difference = 46.25 − 47.11 = **−0.86 pp ≈ −0.9 pp** (manuscript −0.9 pp ✓). Permutation p = **0.1396 ≈ 0.14** (manuscript p = 0.14 ✓). The denominator 14,390 matches the "14,390 genes shared across the six contrasts" statement in L58 (the JSON `all_measured.n` = 14,390). The empirical-null reference is a 5,000-draw permutation of stratum membership (the JSON field `perm_p` for that stratum is 0.1396), exactly as the Methods (L144) specify ("tested against an empirical null obtained by randomly re-labelling which genes belong to the test stratum (5,000 draws) rather than against an assumed 50%"). The related L58 figures also reconcile: 2,318/4,306 = 53.8% ("collapses the apparent core translation from 69.5% to 53.8%", ✓); and 3,556 − 1,083 = 2,473, 2,473/3,556 = 69.5% (the circular concordance, ✓).

【Why it matters】 This is the paper's strongest honesty move and it holds up. The only thing I could not verify from this file is the secondary "3,556 of 14,390 fall in the 4,055-gene core" figure (the 3,556 core-subset count is not in this JSON; it presumably lives in `_R4_nerveinjury_only_meta.csv`). That number is internally plausible (≤ 4,055 and ≤ 14,390) but is the single un-recomputed quantity in this section.

【Specific fix】 No fix required for the statistic. Optional transparency add: deposit `_R4_nerveinjury_only_meta.csv` (or a one-line summary giving the 3,556 core∩universe count) so the L58 denominator chain is fully reproducible.

---

## 4. LODO leakage control: folds are disclosed, but the "0.917–1.000 across three folds" aggregate mixes leakage-controlled and non-leakage numbers, and the "three of five degenerate" caveat is wrong for the leakage-controlled file

【Problem】 Two concrete inconsistencies in the LODO reporting: (a) the headline "cross-animal mean of 0.917–1.000 across three folds" blends the leakage-controlled nerve-injury estimates (1.0) with the **non-leakage** GSE267799 value (0.917), while the leakage-controlled GSE267799 is 0.677; and (b) the statement "three of the five folds have degenerate confidence intervals" matches the non-leakage file but the leakage-controlled file the paper elevates actually has **four** degenerate-CI folds.

【Evidence】 From `P3_lodo_auc_ci_leakage_controlled.csv` (the rigorous file the paper designates as the LODO control):
- GSE278227_1W_ratDRG: AUC 1.0, CI [1.0, 1.0], n = 28
- GSE267799_incision_ratDRG: AUC 0.677083, CI [0.374, 0.940], n = 20
- GSE241361_mouseDRG: AUC 1.0, CI [1.0, 1.0], n = 9
- GSE241361_mouseSC: AUC 1.0, CI [1.0, 1.0], n = 9
- GSE212311_CCI_ratDRG: AUC 1.0, CI [1.0, 1.0], n = 6

So **four** folds carry the degenerate CI [1.0, 1.0] (GSE278227, both GSE241361 folds, GSE212311); only the incision fold has a real CI. But L64 and L151 both state "Three of the five folds have degenerate confidence intervals." The non-leakage `P3_lodo_auc_ci.csv` does have three degenerate folds (GSE278227, GSE241361_DRG, GSE212311; GSE241361_SC there is 0.95 [0.709,1.0] and GSE267799 is 0.917 [0.729,1.0]). So the "three of five" caveat was copied from the non-leakage table, yet the paper's LODO *headline* is the leakage-controlled table where it should read **four of five**.

For the aggregate: L64 says "giving a cross-animal mean of 0.917–1.000 across three independent folds and showing the signature robustly separates nerve-injury from control." The three "independent folds" = GSE278227 (leakage 1.0), GSE212311 (leakage 1.0), and GSE267799 (the **incision** model, cited at its non-leakage 0.917 from `P3_lodo_auc_ci.csv`). But GSE267799 is the *incision counterexample*, and its leakage-controlled value is 0.677 — so the "0.917–1.000" range is built on a leakage leak (optimistic non-leakage incision number) and folds the incision model into a "nerve-injury robust separation" claim. The honestly consistent leakage-controlled cross-animal mean would be (1.0 + 1.0 + 0.677)/3 = 0.892, range 0.677–1.0.

【Why it matters】 The conclusion "the axis is a nerve-injury-specific response rather than a universal pain signature" is *directionally* supported (4/4 nerve-injury folds AUC = 1.0 under leakage control; incision fails at 0.677, CI includes chance). But the magnitude of support is thinner than the prose implies: the two GSE241361 folds are same-animal and excluded from the cross-animal mean, so the *genuinely independent, cross-animal, nerve-injury* evidence reduces to GSE278227 (n = 28) plus the tiny GSE212311 (n = 6). Presenting "0.917–1.000 across three folds" (which silently swaps in the non-leakage incision number) overstates the robustness and is an internal inconsistency between the two deposited LODO tables.

【Specific fix】 (a) Change "three of the five folds have degenerate confidence intervals" to "four of the five leakage-controlled folds have degenerate CIs [1.0,1.0] (all AUC = 1.0 folds), because DeLong variance collapses at AUC = 1.0; only the incision fold yields an estimable CI." (b) Rewrite the aggregate so it never mixes files: "Under leakage control, the four nerve-injury folds reach AUC 1.000 (two of them, GSE241361 DRG and SC, are same-animal and excluded from the cross-animal mean). The two genuinely independent cross-animal nerve-injury folds are GSE278227 (n = 28) and GSE212311 (n = 6); the incision fold (GSE267799, n = 20) falls to 0.677 [0.374, 0.940]. The nerve-injury-specific — not universal — conclusion rests on this pattern." Drop the "0.917–1.000 across three folds" phrasing or recompute it purely from leakage-controlled values.

---

## 5. Bootstrap stability: per-hub stabilities verified; the target-set *aggregate* statistics are not deposited and cannot be recomputed

【Problem】 The hub bootstrap is internally consistent where checkable, but the docking target-set bootstrap aggregates ("median size 6 genes (IQR 5–8)", "median Jaccard 0.026", "P(≥3 of 17) = 0.040", "P(≥5 of 17) = 0.000", "0.79 of the 17 recovered") are not present in the deposited summary, so a reader cannot verify them.

【Evidence】 `P3_hub_bootstrap.csv`: 35 rows, `hub_freq` ranges 0.005 (ACVR1, = 0.5%) to 0.155 (CDHR5, = 15.5%). Max = 0.155, so **0/35 reach ≥ 0.9** (manuscript L66 "0/35 hubs reached a ≥0.9 stability threshold" ✓) and "single most stable dock-eligible hub was CDHR5 (15.5%)" ✓. The "per-gene recovery ranged 0.5%–15.5%" ✓. `results/tables/_R4_targetset_bootstrap.csv` lists per-hub `recovery_freq` for the 17 dock-eligible hubs (and the 9 docked as a subset) — these are **identical** to the `P3_hub_bootstrap.csv` `hub_freq` values (CDHR5 0.155, GALNS 0.10, … ACVR1 0.005), confirming the two bootstrap tables agree on marginal hub stability. Summing the 17 dock-eligible `recovery_freq` gives 0.75, i.e. an expected ~0.75 (manuscript rounds to "0.79") dock-eligible hubs recovered per resample — directionally consistent with "0.79 of the 17," but I could **not** verify the *mean* precisely nor the median/Jaccard/P-value aggregates, because the deposited CSV contains only per-hub marginal frequencies, not the per-resample recovered-set lists from which "median size 6," "median Jaccard 0.026," "P(≥3)=0.040," "P(≥5)=0.000" would be computed.

【Why it matters】 The claim that the docking target list is "justified by structural tractability, not by statistical stability" is a key honesty point and is plausible, but it currently rests on aggregate numbers that are not reproducible from the deposited artifact. A reviewer who opens `_R4_targetset_bootstrap.csv` finds only the same per-hub frequencies already in `P3_hub_bootstrap.csv` — the genuinely novel target-set statistics (median set size, Jaccard, the P(≥k) tail probabilities) are absent. This is a reproducibility gap, not a numerical error.

【Specific fix】 Deposit the per-resample recovered-set lists (or at minimum a small summary giving, per resample, the recovered-set size, its Jaccard with the published 35, and counts of recovered dock-eligible/docked hubs), and confirm the reported aggregates against them. Replace "on average only 0.79 of the 17 dock-eligible hubs … recovered per resample" with "mean (SD) of 0.79 (X.XX) of the 17 dock-eligible hubs recovered per resample (median Y; range …)" once the per-resample data are available.

---

## 6. Multiple-testing registry: the "not counted" multivariate family is used as affirmative evidence — a one-way double standard, sharpened by an un-disclosed EPV gap

【Problem】 The multivariate physicochemical control is explicitly exempted from the corrected-inferential registry (L163–164, family vi), yet its p-values are then used in the Discussion (L128) to assert "the strongest positive controls (AXL, TNIK, ACVR1) retain docking discrimination beyond chemotype." More seriously, ACVR1 is dismissed for EPV ≈ 1, but AXL and TNIK — which carry the very same "recovered signal" claim — have EPVs nearly as low (≈1.3–1.6) and that is never disclosed.

【Evidence】 From `P6_reverse_control.csv`, the number of known binder pairs (positive events) per target: ACVR1 = 9, AXL = 13, TNIK = 10, MAPK14 = 16, ADRA2A = 115. The multivariate model has ~7 physicochemical descriptors + docking affinity + intercept ≈ 8 parameters. Events-per-parameter: **ACVR1 9/8 ≈ 1.1; AXL 13/8 ≈ 1.6; TNIK 10/8 ≈ 1.25; MAPK14 16/8 = 2.0; ADRA2A 115/8 ≈ 14**. The manuscript (L88) rules ACVR1 a "non-reproducible fluctuation rather than signal" citing EPV ≈ 1 (9 events, ~7 params), the non-significant size-independent ΔAUC (p = 0.584, verified in `P6_BH_correction.csv`: ACVR1 deltaAUC p = 0.584 ✓), and the non-significant Wald on the affinity coefficient (p = 0.17). That ruling is *fair* for ACVR1. But the same paragraph presents AXL (multivariate LRT p = 2.6e-5) and TNIK (p = 7.3e-5) as having "recovered signal beyond chemotype," and the Discussion (L128) generalizes this to "the strongest positive controls (AXL, TNIK, ACVR1) retain docking discrimination beyond chemotype" — without noting that AXL (EPV ≈ 1.6) and TNIK (EPV ≈ 1.25) sit on the same low-EPV cliff as the ACVR1 (EPV ≈ 1.1) that was just disqualified. By the rule used to kill ACVR1, AXL/TNIK's LRT significance is *also* statistically fragile.

The registry itself (L163–164) is otherwise defensible: separating method-validation (family vi) from target-discovery (family iv, BH across 5 ChEMBL targets) is a legitimate design choice, and the size-independent BH q-values I verified (ACVR1 0.584, ADRA2A 0.0025, AXL 0.353, MAPK14 0.584, TNIK 0.584 from `P6_BH_correction.csv`) are correctly reported as the authoritative target-discovery test. The problem is not the exemption; it is that the exempted family is then deployed affirmatively in the Discussion while its low EPV is hidden.

【Why it matters】 This is a double standard that could be read two ways by a reviewer: either the multivariate "signal beyond chemotype" for the positive controls is overstated (because AXL/TNIK share ACVR1's low EPV), or — symmetrically — ACVR1 was dismissed too harshly. Either way, the EPV caveat must be applied uniformly. As written, the paper uses low EPV to *exclude* ACVR1 but *not* to qualify AXL/TNIK, which is inconsistent.

【Specific fix】 Add an EPV column to the multivariate control table (Supplementary Table S4) and a sentence: "Events-per-parameter were ACVR1 1.1, AXL 1.6, TNIK 1.3, MAPK14 2.0, ADRA2A ≈14; all ChEMBL-annotated positive controls except ADRA2A fall at EPV ≤ 2, far below the conventional ≥10, so the 'discrimination beyond chemotype' for AXL/TNIK/ACVR1 is itself tentative and the multivariate LRT should be read as a method-capability demonstration, not as target evidence." This converts the double standard into a single, uniform caveat.

---

## 7. Permutation floor (1/2001 ≈ 0.0005): applied consistently where I could check

【Problem】 No error found; I record this as verified and note the one place it should be re-stated for uniformity.

【Evidence】 The floor 1/2001 ≈ 0.0005 is the 2,000-permutation resolution limit. In `P3_geneset_stats.csv` the floored sets show perm_p = 0.0004997501249375312 = exactly 1/2001: Neuroinflammation, DAM_microglia, Complement (all 0.00049975), and in `META_bulkonly_sensitivity_summary.json` the bulk-only Neuroinflammation/DAM/Complement/OXPHOS also show 0.00049975. The manuscript reports these as "perm p ≤ 0.0005" (L50, bulk-only) and as q-values (neuroinflammation/DAM/Complement q = 0.003, OXPHOS q = 0.020 from `_R4_geneset_setlevel_bh.csv`, which I verified: Neuroinflammation fixed perm_q = 0.0029985 ≈ 0.003 ✓; OXPHOS fixed perm_q = 0.0202 ≈ 0.020 ✓; OXPHOS random perm_q = 0.3103 ≈ 0.31 ✓). L48 states "sub-floor p-values … reported as an upper bound" and L149 repeats "values at the floor are reported as an upper bound," and in every place I checked a floored value is indeed labeled "≤ 0.0005" rather than as an exact p. The non-circular test (5,000 permutations, floor 1/5001 ≈ 0.0002) reports p = 0.14, far above floor, so no masking there. I found no instance of a sub-floor p presented as an exact, un-bounded value.

【Why it matters】 Consistency of the floor convention protects the paper from the most common gene-set meta-reporting error (reporting 1/2001 as a real p ≈ 0.0005). The paper handles it correctly.

【Specific fix】 Minor: in L149 the gene-set section says "a resolution floor of 1/2001 ≈ 0.0005 (values at the floor are reported as an upper bound)" — good. Add the same one-line reminder at the non-circular test (L58) even though its p = 0.14 is far above floor, so the convention is visibly uniform across both permutation families (2,000 vs 5,000 draws have different floors).

---

## 8. Docking MW confounder correction: single-variable CIs verified; ACVR1 EPV ruling is fair; but a deposited table contradicts the manuscript on AXL/TNIK, and the EPV double standard (Issue 6) applies

【Problem】 The single-variable size-independent ΔAUC p-values match the manuscript (AXL/TNIK CIs contain zero; ACVR1/MAPK14 match MW-only baseline). But `P6_breadth_chembl_power.csv` labels AXL and TNIK "PASS_size_independent" while `P6_BH_correction.csv` and Table 3b correctly label them FAIL — a deposited-data contradiction. The ACVR1 "non-reproducible fluctuation" ruling is statistically fair, but only if the same low-EPV lens is applied to AXL/TNIK (see Issue 6).

【Evidence】 `P6_BH_correction.csv` (column `deltaAUC_vs_size_only_p_le0`, the authoritative size-independent test):
- ACVR1 0.584 ✓ (manuscript: matches MW-only baseline)
- ADRA2A 0.0005 ✓ (manuscript: size-indep passes BH, but full-library AUC p = 0.118 NS → inconclusive)
- AXL 0.141 ✓ (manuscript: CI contains zero)
- MAPK14 0.5785 ✓ (manuscript: matches MW-only baseline)
- TNIK 0.4435 ✓ (manuscript: CI contains zero)

These exactly match Table 3b (AXL size-indep BH q 0.353, TNIK 0.584, ACVR1 0.584, MAPK14 0.584, ADRA2A 0.0025 — all consistent with the p-values above after BH across 5 targets). So the manuscript's Table 3b and the BH file agree.

Contradiction: `P6_breadth_chembl_power.csv` `mw_control_verdict` column says AXL = "PASS_size_independent" and TNIK = "PASS_size_independent" (with reasons citing auc_dock > auc_size_only point estimates: AXL 0.880 > 0.842; TNIK 0.824 > 0.816). But the *proper* size-independent test (ΔAUC CI, P6_BH_correction) finds those differences non-significant (p = 0.141 and 0.4435) because the CIs span zero. So `P6_breadth_chembl_power.csv` is using a naive point-estimate comparison without uncertainty, while the manuscript correctly uses the significance test. A reader who opens the deposited breadth CSV will see "PASS" for AXL/TNIK and conclude they passed the size-independent test — the opposite of Table 3b. This is a deposited-artifact inconsistency that should be corrected (or the column relabeled to "dock_AUC_exceeds_MW_baseline_pointwise" with a warning that it is not a significance test).

ACVR1 ruling: the multivariate LRT p = 9.6e-4 is indeed unreliable — I confirmed three independent disqualifiers: (i) size-independent ΔAUC p = 0.584 (not significant), (ii) Wald on affinity coefficient p = 0.17 (not significant, stated in L88), (iii) EPV ≈ 1 (9 events / ~8 params) from `P6_reverse_control.csv` (ACVR1 n_known_pairs = 9). With three independent lines, the "non-reproducible fluctuation" conclusion is **fair and well-reasoned** — but, per Issue 6, AXL (13 events → EPV ≈ 1.6) and TNIK (10 events → EPV ≈ 1.25) cleared the *multivariate* bar on equally thin event counts, so the "recovered signal" for them is no more robust than the ACVR1 result the paper rejects.

【Why it matters】 The honest-null conclusion (no target clears both filters) is sound and well-supported. But two things undercut its credibility: (1) a deposited table literally contradicts the manuscript's AXL/TNIK verdicts, which a careful reviewer will catch; (2) the EPV standard used to dismiss ACVR1 is not applied to the AXL/TNIK "recovered signal," so the positive-control narrative is asymmetrically privileged.

【Specific fix】 (a) In `P6_breadth_chembl_power.csv`, rename `mw_control_verdict` to `dock_vs_sizeonly_pointwise` and append a column `size_indep_deltaAUC_p` (= 0.141, 0.4435, …) with a footnote that the point estimate exceeds the baseline but the ΔAUC CI contains zero, so the size-independent *significance* test (P6_BH_correction) is authoritative. Or simply delete the misleading "PASS_size_independent" labels and replace with "pointwise_only." (b) Apply the uniform EPV caveat from Issue 6 so ACVR1, AXL, and TNIK are judged by the same standard.

---

## § Stands up (verified correct)

1. **Non-circular translation test (Issue 3).** Recomputed exactly: 2,266/4,899 = 46.3% vs 6,779/14,390 = 47.1%, −0.9 pp, permutation p = 0.14; the 14,390 denominator matches the JSON and the empirical-null (5,000-draw) reference is correctly used instead of 50%. This is the paper's strongest, correctly-executed honesty control and survives review.
2. **Bulk-only and collapse bounding of the translatome (Issue 1).** The robustness checks are arithmetically correct: bulk-only overlap 2,202/4,055 = 54.3% (JSON: overlap 2202, primary_core 4055, 54.32%); collapse retention 3,707/4,055 = 91.4% (CSV: shared_core 3707, orig_core 4055, 0.9142); FE core 4,055 directly recounted from the Stouffer file. The *fragility is honestly led-with*, which is a genuine strength.
3. **Gene-set set-level BH (L48, L149, gene-set tables).** Recomputed from `_R4_geneset_setlevel_bh.csv`: Neuroinflammation/DAM/Complement fixed q = 0.0030 each; OXPHOS fixed q = 0.0202; OXPHOS random q = 0.3103. The "coordinated neuroimmune axis survives RE; OXPHOS does not" claim is correctly reported, and the permutation floor (1/2001) is consistently applied as an upper bound (Issue 7).
4. **Per-hub bootstrap stability (Issue 5).** `P3_hub_bootstrap.csv` confirms 0/35 hubs ≥ 0.9 (max 0.155, CDHR5), range 0.5%–15.5%; the two bootstrap tables agree on marginal hub frequencies. The "resampling-sensitive candidate set, not a locked list" framing is supported.
5. **Docking two-filter logic and honest null (Issues 6/8).** The ADRA2A two-filter outcome is internally consistent: it fails the full-library enrichment filter (AUC 0.532, p = 0.118 from `P6_breadth_chembl_power.csv` full_library p = 0.1184 ✓) and is therefore "inconclusive," not a confirmed hit — exactly as the brief's trap list anticipated. The no-reliable-hit conclusion is sound.

---

## § Questions for the authors

1. **RE core 1,008:** I could not re-derive the 1,008 RE-core count — the primary `META_DRG_axis_stouffer.csv` has no RE column and `_R4_random_effects_meta.csv` was not in `results/tables/`. Please confirm the RE core was computed on the same per-contrast Z-values with the D–L τ²/weights in L142, and deposit the RE output (or its summary) so the 1,008 and the "18/35 hubs retained FDR_RE < 0.05" can be checked.
2. **Three-fold vs four-fold degenerate CI (Issue 4):** The "three of five folds have degenerate CIs" statement matches the non-leakage `P3_lodo_auc_ci.csv`, but the leakage-controlled file you elevate has **four** degenerate-CI folds. Was the "three" carried over by mistake, or is there a reason the leakage-controlled GSE241361_SC CI [1.0,1.0] should be treated differently?
3. **EPV for AXL/TNIK (Issues 6/8):** You disclose ACVR1's EPV ≈ 1 as disqualifying, but what are the exact EPVs for AXL (13 events) and TNIK (10 events)? If they are ≈1.3–1.6, should the "recovered signal beyond chemotype" claim for them be hedged identically to ACVR1?
4. **Target-set bootstrap aggregates (Issue 5):** The deposited `_R4_targetset_bootstrap.csv` contains only per-hub marginal recovery frequencies (identical to `P3_hub_bootstrap.csv`). Where do "median size 6 (IQR 5–8)," "median Jaccard 0.026," "P(≥3 of 17) = 0.040," and "P(≥5 of 17) = 0.000" come from — can you deposit the per-resample recovered-set lists?
5. **L58 core denominator (Issue 3):** The "3,556 of 14,390 fall in the 4,055-gene core" figure — which file holds the 3,556 count? I verified 14,390 from the JSON but not 3,556.

---

## § What I actually checked

**Files read (manuscript + brief + raw tables):**
- `reports/MVP_ScientificReports_submission.md` (full: offset 0–150 and 150–283)
- `reviews/round9_2026-09-26/_PANEL_BRIEF.md`
- `results/tables/META_DRG_axis_stouffer.csv` (header + full row count for FE core)
- `results/tables/META_bulkonly_sensitivity_summary.json`
- `results/tables/META_collapse_meta.csv`
- `results/tables/_R4_nerveinjury_only_summary.json`
- `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`
- `results/tables/P3_lodo_auc_ci.csv`
- `results/tables/P3_hub_bootstrap.csv`
- `results/tables/_R4_targetset_bootstrap.csv`
- `results/tables/P3_geneset_stats.csv`
- `results/tables/_R4_geneset_setlevel_bh.csv`
- `results/tables/P6_BH_correction.csv`
- `results/tables/P6_breadth_chembl_power.csv`
- `results/tables/P6_reverse_control.csv`

**Values recomputed vs. the manuscript (all recomputed by me):**

| Quantity | Manuscript | My recomputation | File | Verdict |
|---|---|---|---|---|
| Bulk w (4 studies) | 2.19 / 1.22 / 2.65 / 1.49 | 2.1909 / 1.2247 / 2.6458 / 1.4907 | formula √(n_c·n_t/(n_c+n_t)) | ✓ |
| GSE265957 each w | 1.00 | 1.0000 (2/2) | formula | ✓ |
| GSE265957 Σw² share | "w²=2.00 vs 1.22–2.65; twice a bulk study" | 2.00/17.52 = 11.4%; comparable to GSE241361 (12.7%), not twice any | awk | **✗ inconsistent** (Issue 1) |
| FE core | 4,055 | 4,055 (rows meta_FDR<0.05 & consistency≥0.8) | awk count | ✓ |
| RE core | 1,008 | not re-derivable (no RE col in Stouffer CSV) | — | unchecked |
| Bulk-only overlap | 2,202/4,055 = 54.3% | 2202/4055 = 54.32% | JSON | ✓ |
| Collapse retention | 3,707/4,055 = 91.4% | 3707/4055 = 91.42% | CSV | ✓ |
| Non-circular NI stratum | 2,266/4,899 = 46.3% | 0.4625 | JSON | ✓ |
| Non-circular background | 6,779/14,390 = 47.1% | 0.4711 | JSON | ✓ |
| Non-circular risk diff / p | −0.9 pp / p=0.14 | −0.86 pp / perm_p 0.1396 | JSON | ✓ |
| LODO leakage folds | 4× AUC 1.0; incision 0.677 [0.374,0.940] | 4× [1.0,1.0]; incision 0.677 [0.374,0.940] | CSV | ✓ |
| LODO "three of five degenerate" | 3 | 4 in leakage file (matches non-leakage=3) | CSV | **✗ mismatch** (Issue 4) |
| LODO "0.917–1.000 across 3 folds" | 0.917–1.000 | mixes non-leakage 0.917 with leakage 1.0; leakage-only = 0.677–1.0 | two CSVs | **✗ inconsistent** (Issue 4) |
| Hub bootstrap max | CDHR5 15.5%, 0/35 ≥0.9 | 0.155 max, none ≥0.9 | CSV | ✓ |
| Target-set mean recovered | 0.79 of 17 | per-hub Σfreq=0.75 → ≈0.75–0.79 | CSV | ≈ ✓ (aggregate not deposited) |
| Gene-set q (NI/DAM/Comp) | 0.003 | 0.0030 | CSV | ✓ |
| OXPHOS q FE / RE | 0.020 / 0.31 | 0.0202 / 0.3103 | CSV | ✓ |
| Size-indep ΔAUC p (5 targets) | ACVR1 .584, ADRA2A .0005, AXL .141, MAPK .5785, TNIK .4435 | identical | P6_BH_correction.csv | ✓ |
| Reverse-control n_known_pairs | (implied) | ACVR1 9, AXL 13, TNIK 10, MAPK14 16, ADRA2A 115 | P6_reverse_control.csv | basis for EPV |
| AXL/TNIK breadth verdict | FAIL (size-indep) | CSV says "PASS_size_independent" (pointwise) | P6_breadth_chembl_power.csv | **✗ contradiction** (Issue 8) |

**Discrepancies found (must-fix or clarify):**
1. L44 "w² = 2.00 versus 1.22–2.65 / twice a bulk study" — unit error + false "twice" claim (Issue 1).
2. L64/L151 "three of five degenerate CI" vs four in the leakage-controlled file the paper elevates (Issue 4).
3. L64 "cross-animal mean 0.917–1.000 across three folds" mixes leakage-controlled (1.0) and non-leakage (0.917) numbers (Issue 4).
4. `P6_breadth_chembl_power.csv` `mw_control_verdict` = "PASS_size_independent" for AXL/TNIK contradicts Table 3b and `P6_BH_correction.csv` (Issue 8).
5. EPV double standard: ACVR1 dismissed at EPV≈1 but AXL (≈1.6) / TNIK (≈1.25) not similarly qualified (Issues 6/8).
6. FE-primary choice asserted without positive justification despite heterogeneity thesis (Issue 2).
7. Target-set bootstrap aggregates not deposited; RE core 1,008 and L58 "3,556" not re-derivable from files I had (transparency gaps, Issues 2/3/5).

**Scope note:** I did not assess biological plausibility of individual hubs/targets, the single-cell/spatial localisation claims, or the human-miRNA layer beyond what the brief listed; those are outside this design/biostatistics review.
