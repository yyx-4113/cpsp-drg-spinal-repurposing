# A2 — DESIGN / STATISTICS REVIEW (independent, first-submission stance)

**Reviewer codename:** A2 (statistics, meta-analysis, causal inference, ML methodology)
**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
**Venue:** PLOS ONE resubmission. Single-author in-silico re-analysis.
**Files reviewed:** `reports/MVP_PLOSONE_submission.md` (332 lines), `reports/MVP_PLOSONE_supplementary.md`, `reports/MVP_PLOSONE_cover_letter.md`, plus the source tables and scripts listed in § *What I actually checked*.

**Independence statement.** I have not read `reviews/REVIEW_*.md`, `reviews/RESPONSE_*.md`, `reviews/round2_*`–`round9_*`, `.workbuddy/memory/**`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, or any other reviewer's output in `reviews/round10_2026-09-26/`. Every number below was recomputed by me from the source tables or from re-executed code.

**One-line overall verdict.** The honesty architecture of this paper is unusually good and most of its headline numbers reproduce exactly; but three load-bearing statistical products — the bootstrap stability analysis, the "45.7% translatome-dependent" fragility claim, and the LODO "nerve-injury specificity" claim — do not survive recomputation, and one of them (the bootstrap) is invalidated by an outright specification error in the code.

---

## § A. Major problems

### A1. The bootstrap stability analyses are invalid: the XGBoost leg is fitted to mis-paired features and labels in every resample

**【Problem】** In both bootstrap scripts the XGBoost selector is trained on the *full pooled feature matrix in original sample order* (`Xp`, 72 × 800) while its label vector is the *bootstrapped* label vector (`yb = yall[idx]`), so features and labels are paired at random; every stability number the paper builds on (median Jaccard 0.026, P(≥3 of 17) = 0.040, "0/35 hubs reach ≥0.9", "the target list is structurally rather than statistically determined") is therefore an artefact, not a measurement.

**【Evidence】**
- `scripts/p7_targetset_bootstrap.py:110-112`:
  `clf = xgb.XGBClassifier(...).fit(Xp, yb)` — `Xp` is defined at line 78 as `Xp = Xall[:, [cidx[g] for g in POOL]]` (all 72 samples, original order), while `yb` is defined at line 105 as `yb = yall[idx]`. The Random-Forest leg in the same loop (line 108) is correct: `.fit(Xbs, yb)` with `Xb = Xp[idx]`, `Xbs = StandardScaler().fit_transform(Xb)`.
- The identical error is in the *published* hub bootstrap: `scripts/p3_hub_bootstrap.py:85`, `.fit(Xp,yb)`.
- The non-bootstrap primary analysis is **correct**: `scripts/p3_ml.py:116`, `.fit(Xp, yall)` — aligned. So the published 35 hubs are unaffected; only the two stability analyses are.
- Consequence I verified by re-running the pipeline myself (same loaders, same `SEED=42`, `C_min = 8.5317`, identical to `P3_ml_summary.json:lasso_C_min`): with the XGBoost leg degraded to noise, the resampled hub sets collapse to a median of 6 genes. Two independent Top-80 draws from an 800-gene pool overlap by `80 × 80/800 = 8.0` genes **by chance**. The observed median (6, IQR 5–8) is at or *below* chance overlap. The bootstrap therefore does not measure "instability of a recovered signal"; it measures a rule with no operating characteristic above chance.
- The manuscript's stated mechanism is also factually wrong. `reports/MVP_PLOSONE_submission.md:66` says "LASSO contributing no selections under resampling (the effective consensus reduced to Random-Forest∩XGBoost agreement)". I re-fitted LASSO at `C = 8.5317` on three consecutive resamples: **38, 29 and 53 non-zero coefficients**. LASSO does select; what happens is that its selections never coincide with the RF/XGBoost Top-80 lists.

**【Why it matters】** This is the single most consequential defect I found, because the bootstrap is doing explicit rhetorical work in at least five places: Table 2 (`MVP_PLOSONE_submission.md:316`), Results (`:66`), Methods (`:158`), Abstract-adjacent framing, and the cover letter (`MVP_PLOSONE_cover_letter.md:11`: "a bootstrap shows the docking target set is not statistically reproducible … so target selection rests on structural tractability"). It is also the stated justification for why the docking target list does not need statistical support. If corrected, the stability numbers could move in either direction, and the paper's central "we justify the target list by tractability, not statistics" defence would need to be re-derived. It is also a reproducibility defect a PLOS ONE reviewer or reader can find in one line of code, which damages the paper's central credibility claim of full transparency.

**【Specific fix】**

1. In `scripts/p3_hub_bootstrap.py:85` and `scripts/p7_targetset_bootstrap.py:112`, replace `.fit(Xp, yb)` with `.fit(Xbs, yb)` (p7) / `.fit(StandardScaler().fit_transform(Xp[idx]), yb)` (p3_hub_bootstrap), and recompute the SHAP contributions on the *resampled* matrix, not on `Xp`. Re-emit `P3_hub_bootstrap.csv`, `_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap_resamples.csv` and `_R4_targetset_bootstrap.json`.
2. Replace the parenthetical at `MVP_PLOSONE_submission.md:66` with:

> "Under resampling the LASSO leg selects 29–53 genes but essentially none of them coincide with the tree-ensemble Top-80 lists, so the ≥2/3 vote reduces to Random-Forest∩XGBoost agreement; because two independent Top-80 draws from the 800-gene pool overlap by 8.0 genes in expectation, the observed median recovered set size of 6 (IQR 5–8) is at or below the chance level and should be read as a null operating characteristic of the consensus rule, not as a stability measurement of a recovered signal."

3. Add to Methods (`:158`), immediately after the sentence ending "`…structurally rather than statistically determined`":

> "We corrected a specification error in the bootstrap: in the previous version the XGBoost selector was fitted to the full pooled feature matrix with the resampled label vector, so features and labels were mis-paired and the XGBoost vote was noise in every resample. All three selectors are now fitted to the resampled (X, y) pair. All stability figures in this paper are from the corrected run; the previous values are retained in the repository changelog."

4. Do **not** restate the old numbers in the cover letter until the corrected run is available.

---

### A2. FE-primary is justified by a heterogeneity statistic that does not describe the reported gene set

**【Problem】** The manuscript defends fixed-effect primacy by quoting median I² = 38.8%; that median is computed over all 16,552 tested genes — a universe overwhelmingly composed of null genes — whereas the genes the paper actually reports have median I² = 52.1% and the hubs have median I² = 72.8%.

**【Evidence】** Recomputed from `results/tables/_R4_random_effects_meta.csv` (16,552 rows):
- All genes: median τ² = 0.2324, median I² = 38.79%, 41.90% of genes I² > 50%, 68.08% τ² > 0 — **all four as printed** at `:46`.
- Restricted to the 4,055 FE-core genes (FDR_FE < 0.05 & consistency ≥ 0.8): **median I² = 52.15%, median τ² = 0.4137, and 51.9% of them have I² > 50%.**
- Restricted to the 9,834 genes with K = 6 (the primary universe): median I² = 45.73%, median τ² = 0.3270, 46.4% with I² > 50%.
- Restricted to the 35 hubs: median I² = 72.8% (as printed at `:46`) and 18/35 with FDR_RE < 0.05 (as printed).

So the sentence at `:46` — "Heterogeneity was low-to-moderate by Higgins–Thompson convention (a median I² of ≈39% falls below the 50% 'moderate' threshold)" — is true of the null-dominated universe and false of the reported one. The immediately following sentence concedes the right thing ("gene-level conclusions drawn from the 4,055-gene set should be read as conditional on moderate between-contrast heterogeneity") but then labels the correct magnitude as "moderate" when the core-gene median is above the "substantial" boundary.

**【Why it matters】** The single design decision that most affects every downstream number is FE vs RE: it changes the core from 4,055 to 1,008 genes, changes OXPHOS from q = 0.020 to q = 0.31, and changes target ranking (4/10 targets retain RE significance; `:90`). Justifying that decision with a statistic computed on the wrong denominator is exactly the inferential error the rest of the paper is careful to avoid. A PLOS ONE statistical reviewer will recompute this in one line.

**【Specific fix】** Replace the first two sentences of the heterogeneity paragraph (`:46`) with:

> "Heterogeneity was summarized over two different gene universes, because the two answers differ. Across all 16,552 tested genes the median was τ² = 0.232 and I² = 38.8% (41.9% of genes with I² > 50%). Restricted to the genes this paper actually reports, heterogeneity was higher: among the 4,055 fixed-effect core genes the median was I² = 52.1% and τ² = 0.414, with 51.9% of core genes showing I² > 50%, and among the 35 hubs the median I² was 72.8%. The genome-wide median is therefore not the relevant figure for the reported set. Under random effects the core shrank to 1,008 genes (24.9% of the fixed-effect core). We consequently treat the fixed-effect core as the maximum-extent estimate and the random-effects core as the conservative bound; the only gene-level conclusion we report as robust to the model choice is the neuroimmune/complement/DAM programme, which retains set-level q = 0.003 under both models. All other gene-level statements — core membership, per-gene meta_Z ranking, the 35-hub list, and the per-target meta_Z ranking in Table 3a — are fixed-effect-conditional and are labelled as such wherever they appear."

And in the Abstract (`:18`) insert after "A 4,055-gene core emerged under fixed effects but only 1,008 persisted under random effects":

> " (fixed-effect core median I² = 52.1%)"

---

### A3. The degenerate-CI problem: the CIs are degenerate by construction, and one of the two "independent" nerve-injury folds cannot reach significance at any threshold

**【Problem】** Four of five leakage-controlled folds give AUC = 1.000 with CI [1.0, 1.0]; the manuscript attributes this to small n and then nevertheless concludes "nerve-injury-specific". Both halves are wrong: the intervals are degenerate because a percentile bootstrap of an already-perfect ranking can only return 1.0 (they are also mislabelled "DeLong" — they are 2,000-draw percentile bootstrap intervals, `scripts/p3_ml_leakage_controlled.py:76`), and exact tests show that the GSE212311 fold (3 vs 3) has p = 0.050, the largest possible p at that size.

**【Evidence】** Recomputed from `results/tables/P3_lodo_auc_ci_leakage_controlled.csv` (5 rows) and the per-dataset group sizes in `META_bulkonly_sensitivity_summary.json`:

| Fold | n_case / n_ctrl | n | AUC | 95% CI (as printed) | **exact one-sided Mann–Whitney p (my computation)** | smallest p attainable |
|---|---|---|---|---|---|---|
| GSE278227_1W_ratDRG | 14 / 14 | 28 | 1.000 | [1.000, 1.000] | **2.49 × 10⁻⁸** | 2.49 × 10⁻⁸ |
| GSE267799_incision_ratDRG | 12 / 8 | 20 | 0.677 | [0.374, 0.940] | **0.104** | 7.94 × 10⁻⁶ |
| GSE241361_mouseDRG | 4 / 5 | 9 | 1.000 | [1.000, 1.000] | **7.94 × 10⁻³** | 7.94 × 10⁻³ |
| GSE241361_mouseSC | 4 / 5 | 9 | 1.000 | [1.000, 1.000] | **7.94 × 10⁻³** | 7.94 × 10⁻³ |
| GSE212311_CCI_ratDRG | 3 / 3 | 6 | 1.000 | [1.000, 1.000] | **0.050** | 0.050 |

- The two GSE241361 folds are from the same animals, which I verified directly: `data/processed/GSE241361_sampletable.csv` pairs `E1_SNI1WTDRG` with `E5_SNI1WTMedula`, `E3_SNI3WTDRG` with `E7_SNI3WTMedula`, etc. — same SNI animal, DRG vs medulla. The manuscript's decision to exclude them from the cross-animal mean is correct.
- That leaves **two** genuinely independent nerve-injury folds, exactly as the manuscript says (`:64`). Of those two, one (n = 28) is conclusive and one (n = 6, p = 0.050) is not significant at any conventional threshold and cannot be made so — 0.050 *is* its floor. Presenting "AUC 1.000" for a 3-vs-3 fold alongside a 14-vs-14 fold, and writing that "both at AUC 1.000 … the nerve-injury-specific conclusion rests on this pattern", over-reads a degenerate estimate.
- Separately: `MVP_PLOSONE_submission.md:64` says the incision fold's CI "includes chance, **establishing** that the axis is a nerve-injury-specific response rather than a universal pain signature". Exact p = 0.104 with a CI spanning 0.374–0.940 is a failure to establish generalisation, not an establishment of non-generalisability — the mirror image of the "absence of evidence" error the paper correctly avoids elsewhere.
- **Figure 2 / Results inconsistency (disclosure ≠ resolution):** `MVP_PLOSONE_submission.md:289` (Fig. 2 legend) reports the **raw, non-leakage** numbers and lists the incision fold as "0.917 [0.729, 1.000]" — an interval that *excludes* 0.5 — with no statement that these are the leakage-inflated values. The source given is `P3_lodo_auc_ci.csv` (raw). A reader of Fig. 2A therefore sees the opposite of the headline claim. The same legend also says "Cross-animal held-out datasets (three folds) reach AUC 1.000" and then lists one of the three at 0.917.
- Additional undisclosed specification issues in the leakage-controlled run: `p3_ml_leakage_controlled.py:133` standardises the **test** set with its own mean/SD (`StandardScaler().fit_transform(Xte)`) rather than the training scaler, which at n = 6 re-centres each gene on six observations; and `:116` selects features as the **union** of the three selectors (`sel = lasso_set|rf_set|xgb_set`, 139–164 genes, see `n_selected`), not the ≥2/3 consensus used to define the published 35 hubs.

**【Why it matters】** "Nerve-injury-specific, not universal" is the title claim and the framing of the whole axis. It currently rests on one well-powered fold. If that fold's high AUC partly reflects its ipsilateral-vs-contralateral within-animal design while the incision fold is between-animal, the comparison is confounded by design, not by biology.

**【Specific fix】** Replace the LODO paragraph at `:64` with:

> "Under leakage-controlled leave-one-dataset-out, four of the five folds returned AUC = 1.000. These intervals are 2,000-resample percentile bootstrap intervals and are degenerate by construction whenever the point estimate is 1.0 — every resample preserves the observed ranking — so [1.0, 1.0] carries no information about precision and is not read as evidence of discrimination. We therefore report the exact one-sided Mann–Whitney p for each fold: GSE278227 (14 vs 14) p = 2.5 × 10⁻⁸; GSE241361 DRG and spinal cord (4 vs 5 each, drawn from the same animals) p = 7.9 × 10⁻³; GSE212311 (3 vs 3) p = 0.050, which is the smallest p attainable at that sample size. Only the GSE278227 fold is individually conclusive; the incision fold gives AUC 0.677 (exact p = 0.104; 95% CI 0.374–0.940). The incision result is therefore a failure to demonstrate generalisation, not a demonstration of nerve-injury specificity, and we make no formal comparison between the nerve-injury and incision folds, which differ in species, injury model, control design (ipsilateral/contralateral versus separate-animal baseline) and sample size."

And add to the Fig. 2 legend (`:289`):

> "Panel A shows the **raw (non-leakage-controlled)** LODO estimates; the leakage-controlled estimates reported in the text are 1.000 / 1.000 / 1.000 / 1.000 for the four nerve-injury folds and 0.677 [0.374, 0.940] for the incision fold. Raw and leakage-controlled intervals are both given in `results/tables/P3_lodo_auc_ci.csv` and `P3_lodo_auc_ci_leakage_controlled.csv`; only the leakage-controlled values are interpreted."

Also fix the legend's arithmetic sentence: "Of the three cross-animal held-out folds, two reach AUC 1.000 (GSE278227, n = 28; GSE212311, n = 6) and the incision arm reaches 0.917 [0.729, 1.000] (GSE267799, n = 20)."

---

### A4. The "45.7% of the core is translatome-dependent" claim is a threshold artefact

**【Problem】** The paper's self-declared "single most important fragility" — that removing the ribosome-profiling study loses 45.7% of the core — is almost entirely produced by the consistency threshold changing from 5/6 (0.833) at K = 6 to 4/4 (1.000) at K = 4, not by the translatome study's statistical contribution (11.4% of Σw²).

**【Evidence】** Recomputed by joining the 4,055 primary core genes (`META_DRG_axis_stouffer.csv`) to `META_bulkonly_meta.csv`:
- 102 of the 1,853 lost genes (5.5%) simply leave the tested universe under the union-K ≥ 3 rule.
- **1,512 of the 1,853 (81.6%) have bulk-only consistency exactly 0.75 (3/4)** — they fail only because at K = 4 the ≥0.8 rule can only be met by 4/4 unanimity, whereas at K = 6 it was met by 5/6.
- A further 170 have consistency 0.667 (2/3, K = 3).
- Only ~211 fail on meta_FDR alone — 11.4% of the loss, coincidentally equal to the translatome's 11.4% share of Σw².
- Counterfactual: applying the fraction-matched threshold achievable at K = 4 (consistency ≥ 0.75, i.e. 3/4) to the bulk-only meta yields a core of **3,587 genes, i.e. 88.5% of the primary 4,055** — not 54.3%.

The manuscript does disclose the threshold difference in Methods (`:146`, "5/6 at K = 6 … 4/4 at K = 4") but then attributes the whole gap to the translatome anyway, in Results (`:50`), Table 1a (`:303`: "i.e. 45.7% of the primary core is translatome-dependent") and the metadata line (`:8`).

**【Why it matters】** This inverts the paper's risk ranking. The *like-for-like* fragility measure — same genes, same K, same threshold, FE vs RE — is 4,055 → 1,008 (loses 75.1%). That is the real fragility, and the paper demotes it to a "sensitivity bound" while promoting a 54.3% figure that is largely definitional. A referee who recomputes this will conclude the authors mis-ranked their own limitations.

**【Specific fix】** Replace the bracketed clause at `:50` ("of which 2,202 (54.3%) overlapped the primary 4,055-gene core, i.e. 45.7% of the primary core was not recovered without the translatome study, the single most important fragility of the signature, and one we therefore lead with rather than report as a secondary sensitivity") with:

> "of which 2,202 (54.3%) overlapped the primary 4,055-gene core. This gap is largely definitional rather than evidential: the ≥0.8 consistency rule requires 5/6 agreements at K = 6 but can only be satisfied by 4/4 unanimity at K = 4, and 1,512 of the 1,853 non-recovered core genes (81.6%) fail the bulk-only filter solely on that step while remaining bulk-significant; 102 leave the tested universe under the union-K ≥ 3 rule. Re-scored with the fraction-matched threshold available at K = 4 (consistency ≥ 0.75, i.e. 3/4), the bulk-only core is 3,587 genes, 88.5% of the primary core. The translatome study contributes 11.4% of the total meta weight (Σw² = 17.52), and 11.4% of the non-recovered genes fail on meta_FDR alone. The dominant fragility of the signature is therefore the fixed-effect versus random-effects choice (4,055 → 1,008 genes, 75.1% loss under a like-for-like comparison), not the inclusion of GSE265957."

And correct Table 1a (`:303`) to: "core 2,512; overlap with primary core 2,202/4,055 = 54.3% (2,512/3,587 = 70.0% of the fraction-matched bulk-only core); 81.6% of the non-overlap is attributable to the K = 6 → K = 4 consistency-threshold step, not to loss of the translatome signal."

---

### A5. The two-filter rule is applied to 5 of 10 targets, and the stricter internal standard is applied to ACVR1 but not to ADRA2A

**【Problem】** The conjunction rule (must pass **both** full-library enrichment **and** the size-independent test) is coherent and is applied uniformly to the five targets for which it is computable — but (i) five of the ten targets have 0–1 ChEMBL binders and no enrichment test at all, yet the Abstract, Results and Conclusions say "none of the 10"; and (ii) the manuscript uses the multivariate Wald test on the affinity coefficient to demote ACVR1 (p = 0.17) but does not apply that same standard to ADRA2A (Wald p = 0.504), TNIK (0.251) or MAPK14 (0.407).

**【Evidence】** From `results/tables/P6_reverse_control.csv` and `P6_multivariate_physchem_control.csv`:
- Known binders per target: **ADRA2A 115**, MAPK14 16, AXL 13, TNIK 10, ACVR1 9, SLC2A1 1, and **GALNS 0, ITPKC 0, SERPINE1 0, VASH2 0**. Sum across 10 targets = 164, of which **ADRA2A alone supplies 115 (70.1%)**.
- Therefore the enrichment filters are computable for 5 targets (ADRA2A, MAPK14, AXL, TNIK, ACVR1); SLC2A1 has 1 and the other four have none.
- `MVP_PLOSONE_submission.md:90`: "The honest-null conclusion applies to all 10." — for five targets there is no test. `:18` (Abstract): "Full-library docking of 3,085 drugs against the 10 tractable targets found none clearing both the full-library and size-independent enrichment filters." `:134` (Conclusions): "found no target that cleared both the full-library and size-independent enrichment filters". All three use the denominator 10 where the tested denominator is 5.
- Wald test on the docking-affinity coefficient (source `P6_multivariate_physchem_control.csv`, column `Wald_neg_aff_p`): AXL 2.45 × 10⁻⁵, ACVR1 0.172, ADRA2A **0.504**, TNIK **0.251**, MAPK14 **0.407**. The manuscript (`:88`) cites ACVR1's Wald p = 0.17 to reject its LR p = 9.6 × 10⁻⁴, and cites ADRA2A's LR p = 0.027 as "weak", but never reports ADRA2A's Wald p = 0.504. By the paper's own stricter standard, only AXL retains docking signal beyond chemotype — and AXL fails the size-independent test (q = 0.353; ΔAUC CI [−0.030, +0.104]).
- The five "reverse positive controls" are also not five independent validations: the ChEMBL binder lists for AXL, TNIK, ACVR1 and MAPK14 are four overlapping subsets of essentially one chemotype class (AXITINIB, BOSUTINIB, CRIZOTINIB, DASATINIB, FEDRATINIB, GILTERITINIB, LENVATINIB, NINTEDANIB, PACRITINIB, PAZOPANIB, PONATINIB recur across targets). BH correction across five targets treats them as five independent tests.

**【Why it matters】** The honest-null is the paper's advertised contribution, and it is genuinely supported — but as written it over-claims scope ("all 10") and under-applies its own strictest filter to the one target with real statistical power (ADRA2A, 115 binders, EPV ≈ 14). That asymmetry is visible next to a declared competing interest (`MVP_PLOSONE_submission.md:274`), which makes it look worse than it probably is.

**【Specific fix】**

1. Change the denominator everywhere. Abstract (`:18`): "Full-library docking of 3,085 drugs against the 10 tractable targets yielded ChEMBL-annotated binder sets for five of them (ADRA2A 115, MAPK14 16, AXL 13, TNIK 10, ACVR1 9 known binders; the remaining five have 0–1 and no enrichment test is computable); of those five, none cleared both filters."
2. Conclusions (`:134`): replace "found no target that cleared both the full-library and size-independent enrichment filters" with "found no target among the five with a computable enrichment test that cleared both filters".
3. Results (`:90`): replace "The honest-null conclusion applies to all 10." with "For the five targets without a ChEMBL binder set the docking result is untested rather than null; the honest-null conclusion is stated for the five testable targets and applies to the other five only in the weaker sense that the screen produced no prioritisation evidence for them."
4. Add to `:88`, after the sentence on ACVR1:

> "The same standard applied uniformly leaves only AXL with docking discrimination beyond chemotype: the Wald test on the affinity coefficient is p = 2.4 × 10⁻⁵ for AXL but p = 0.17 for ACVR1, p = 0.25 for TNIK, p = 0.41 for MAPK14 and p = 0.50 for ADRA2A. ADRA2A's size-independent ΔAUC (BH q = 0.0025) is therefore reported as an upper bound on a weak effect and is not treated as passing the second filter."

5. Add one sentence at `:88`: "The four passing method-validation controls draw on overlapping sets of the same multi-kinase inhibitors, so they are one chemotype finding counted four times rather than four independent validations; the BH correction across five targets is correspondingly optimistic."

---

### A6. EPV is disclosed for the docking models but not for the LODO classifier, where it is far worse

**【Problem】** The docking EPV disclosure is correct and adequate; the leakage-controlled LODO logistic regression — the model producing the headline AUCs — is fitted with 139–164 features on 44–66 training samples (EPV 0.13–0.21) and this is never disclosed.

**【Evidence】**
- Docking EPV, recomputed from `P6_multivariate_physchem_control.csv` (7 descriptor parameters + intercept = 8): ACVR1 9/8 = 1.1, AXL 13/8 = 1.6, TNIK 10/8 = 1.3, MAPK14 16/8 = 2.0, ADRA2A 115/8 = 14.4 — **all five as printed** at `:88`.
- LODO: `P3_lodo_auc_ci_leakage_controlled.csv` gives `n_selected` = 164, 142, 139, 150, 158 and held-out n = 28, 20, 9, 9, 6, so n_train = 44, 52, 63, 63, 66. I recovered the class counts by re-running the loader: 37 cases / 35 controls overall (14+12+4+4+3 / 14+8+5+5+3). Training-set cases per fold are therefore 23, 25, 33, 33, 34 and the minor class 21, 20, 30, 30, 32 → **EPV = 0.13, 0.14, 0.22, 0.21, 0.20** against 164/142/139/150/158 parameters, with no regularisation (`p3_ml_leakage_controlled.py:134`: `LogisticRegression(max_iter=5000)`, default C = 1.0). The raw LODO uses 35 features on the same training sizes (EPV 0.6–0.9).
- `scripts/p3_ml_leakage_controlled.py:133` also refits the scaler on the test fold.

**【Why it matters】** The manuscript's own convention is EPV ≥ 10. A classifier with EPV ≈ 0.15 that returns AUC = 1.000 on a 6-sample test set is not evidence of anything, and this is the same reasoning the authors correctly apply to ACVR1. Applying one EPV standard to docking and none to the classifier is inconsistent.

**【Specific fix】** Add to `:64` (or Methods `:158`):

> "The leakage-controlled classifier is a regularisation-free logistic regression fitted on 139–164 selected features with 44–66 training samples (23–34 in the smaller class), i.e. events-per-parameter 0.13–0.22 — far below the ≥10 convention we apply elsewhere in this paper. The LODO AUCs are accordingly reported as descriptive generalisation checks, not as inferential estimates, and we draw no conclusion from any single fold."

And in `p3_ml_leakage_controlled.py:133` replace `Xte_s=StandardScaler().fit_transform(Xte[...])` with `Xte_s=sc.transform(Xte[...])` using the scaler fitted on the training fold, then re-emit `P3_lodo_auc_ci_leakage_controlled.csv`.

---

## § B. Minor problems

### B1. A fourth gene set passes set-level BH under fixed effects and is never reported

**【Problem】** `Neuropeptides_pain` has FE permutation q = 0.047 < 0.05 in the set-level table the manuscript cites as its primary honesty metric, but Fig. 1 and the Results enumerate only three up programmes plus OXPHOS.

**【Evidence】** `results/tables/_R4_geneset_setlevel_bh.csv`: Neuroinflammation perm_q = 0.002998, Complement 0.002998, DAM_microglia 0.002998, **Neuropeptides_pain perm_q = 0.04678 (mean_Z +2.19, 55.6% up)**, Mitochondria_OXPHOS 0.02024 (all as printed elsewhere). Under RE, Neuropeptides_pain q = 0.795 (not significant) — so it is a further FE-conditional finding, but it is not mentioned at all.

**【Why it matters】** Completeness. The paper's credibility rests on reporting everything that passes its own gate; silently dropping one of five is the kind of omission that undermines the whole honesty framing.

**【Specific fix】** Add to `:48` and to the Fig. 1 legend (`:286`): "A fourth set, neuropeptides (mean_Z +2.19, 55.6% of members up), reached set-level q = 0.047 under fixed effects but q = 0.795 under random effects and is therefore reported as fixed-effect-conditional and not interpreted."

### B2. ADRA2A's size-independent p is pinned at the bootstrap resolution floor

**【Problem】** p = 0.0005 is exactly 1/2001, the floor of a 2,000-draw bootstrap (`scripts/p6_stats.py:243`, `n_boot=2000`), and it is propagated into a BH q of 0.0025 that is then used to say ADRA2A "passes filter 2".

**【Evidence】** `P6_BH_correction.csv`: ADRA2A `deltaAUC_vs_size_only_p_le0` = 0.0005, `BH_q_size_indep` = 0.0025. `P6_enrichment_mw_confounder_check.csv`: ΔAUC CI [+0.032, +0.110].

**【Why it matters】** A floor-pinned p cannot support a q quoted to two significant figures, and "passes" is too strong for "0 of 2,000 draws ≤ 0".

**【Specific fix】** In Table 3b (`:325`) and `:112`, write "≤ 0.0005 (bootstrap resolution floor: 2,000 draws)" and "BH q ≤ 0.0025", and add a footnote: "p-values equal to 5 × 10⁻⁴ are at the 1/2001 resolution floor of the 2,000-resample bootstrap and are reported as upper bounds."

### B3. Spinal localisation mixes two denominators in one sentence

**【Problem】** `:76` reports "24 detectable … and 20 were localisable … (15 NotLocalisable)", but 20 + 15 = 35, not 24.

**【Evidence】** `results/tables/P5_hub_lineage_consensus.csv` (35 rows): NotLocalisable = 15 exactly (ATF3, CDHR5, ACVR1, AGRN, ANKRD1, CCDC160, CRISP3, FLNC, ITPKC, LNP1, NPY, REG3B, SERPINE1, SLC2A1, VIP), localisable = 20, `confident` = 7 (TFE3, ANKRD13B, CHL1, CTTN, PTPN23, SRRM4, VASH2) — all as printed. The 24 is a different quantity (snRNA detection).

**【Why it matters】** Denominator incoherence in a sentence that a reader will use to judge how much of the hub programme is actually localised.

**【Specific fix】** Rewrite as: "Of the 35 hubs, 33 were present in GSE328175 (CRISP3, REG3B absent) and 24 were detectable (mean pseudobulk expression > 0 in ≥1 lineage). Lineage consensus, computed over all 35 hubs, localised 20 and left 15 NotLocalisable; 7 of 35 (ANKRD13B, CTTN, PTPN23, SRRM4, VASH2, TFE3, CHL1) were cross-dataset lineage-consistent."

### B4. Two non-circular strata with significant *negative* concordance are computed but not reported

**【Problem】** The manuscript reports only the ≥0.8-consistency stratum (46.2%, p = 0.14). The same summary file contains two larger strata in which nerve-injury-responsive genes agree with the incision direction significantly *less* than background.

**【Evidence】** `results/tables/_R4_nerveinjury_only_summary.json`: background 6,779/14,390 = 47.11%; `NI_FDR05_any_consistency` 3,329/7,274 = 45.77%, perm p = 8.0 × 10⁻⁴; `NI_FDR05_AND_NIcons<0.8` 978/2,185 = 44.76%, perm p = 0.0148; `NI_FDR05_AND_NIcons>=0.8` 2,266/4,899 = 46.25%, perm p = 0.1396 (the reported one).

**【Why it matters】** Reporting only the null stratum while two significant strata sit in the same file invites a selective-reporting objection — and the omitted result (nerve-injury-responsive genes as a class are *anti*-concordant with incision) is a stronger and more interesting version of the paper's own claim.

**【Specific fix】** Add to `:58`: "Two larger strata from the same non-circular construction were also computed and are reported for completeness: all nerve-injury-significant genes agree with the incision direction at 45.8% (3,329/7,274; permutation p = 8 × 10⁻⁴) and nerve-injury-significant but direction-inconsistent genes at 44.8% (978/2,185; p = 0.015), both below the 47.1% background. Nerve-injury-responsive genes are therefore, as a class, slightly anti-concordant with the incision direction; the ≥0.8-consistency stratum reported above is the null case."

### B5. Permutation nulls treat genes and miRNAs as exchangeable, ignoring correlation

**【Problem】** Both permutation families — the gene-set tests (2,000 draws) and the translation test (5,000 draws) — build their null by re-drawing gene/miRNA labels independently, which assumes exchangeability of correlated units and is anti-conservative.

**【Evidence】** Methods `:155` and `:150`. The OXPHOS and complement sets are explicitly acknowledged to be co-regulated and to share members (`:48`); `P4_setlevel_test.json` shows the human layer's nominal t p = 0.029 versus permutation p = 0.51 on 253 miRNAs.

**【Why it matters】** For the null claims (translation p = 0.14, human layer p = 0.51) the anti-conservativeness is harmless — the true p is larger, so the null stands. For the positive claims it matters: OXPHOS at FE q = 0.020 is the one set-level result closest to the boundary, and it is already q = 0.31 under RE.

**【Specific fix】** Add to Methods `:155`: "The permutation null re-draws gene labels independently and therefore assumes exchangeability of genes that are in fact correlated within co-regulated sets; the resulting p-values are anti-conservative for the significant sets and conservative for the null ones. Because OXPHOS is the only set whose fixed-effect status depends on the boundary (q = 0.020 fixed, 0.31 random), we report it as fixed-effect-conditional and do not rest any conclusion on it." Optionally add a sample-label permutation (rotate the contrast sign vector across datasets) as a correlation-preserving sensitivity.

### B6. Two contrasts carry 67.3% of the meta weight, and one of them is the held-out incision arm

**【Problem】** The "six-contrast" meta is dominated by two inputs, and the second-largest is GSE267799 — the same incision contrast that is later used as the held-out translation target.

**【Evidence】** From the weights I verified (`:44` and `META_bulkonly_sensitivity_summary.json`): w² = 4.80 (GSE267799, 27.4%), 7.00 (GSE278227, 39.9%), 1.50 (GSE212311, 8.6%), 2.22 (GSE241361 DRG, 12.7%), 1.00 + 1.00 (GSE265957, 11.4%); Σw² = 17.52. GSE278227 + GSE267799 = 67.3%.

**【Why it matters】** The paper correctly flags *directional* circularity (`:56`) but not *weight* circularity: 27.4% of the primary signature is built from the dataset that the translation test is meant to be independent of. The nerve-injury-only reanalysis exists and is cited (5,412 genes FE / 3,099 RE), but the primary core used for hub validation and target ranking is the incision-contaminated one.

**【Specific fix】** Add to `:56`: "Weight circularity should be noted alongside directional circularity: GSE278227 (w² = 7.00) and GSE267799, the incision arm (w² = 4.80), together carry 67.3% of the total meta weight (Σw² = 17.52), so the primary 4,055-gene core is substantially shaped by the dataset that the translation test is intended to be independent of. This is a further reason to prefer the nerve-injury-only construction (5,412 genes fixed-effect, 3,099 random-effects) whenever the incision arm is part of the question."

### B7. Three of six contrasts have ≤5 samples per group and are treated as asymptotic z

**【Problem】** The per-contrast Welch t statistics are converted to z and treated as effect estimates with Var = 1/w²; three of the six inputs have n ≤ 5 per group (GSE265957 2/2 twice, GSE212311 3/3, GSE241361 4/5), i.e. df = 2, 4 and 7.

**【Evidence】** `:44` and `:146` disclose the conversion; group sizes from `META_bulkonly_sensitivity_summary.json` (12/8, 3/3, 14/14, 4/5) and `data/processed/GSE212311_DRG_sampletable.csv` / GSE241361.

**【Why it matters】** Under the null the conversion is exact (p is uniform), so significance is not inflated; what is affected is the *weighting*: a df = 2 contrast receives weight on the same footing as a df = 26 contrast, and the per-gene τ²/I² statistics inherit that. The disclosure is present; the consequence is not stated.

**【Specific fix】** Add to `:146`: "Because three of the six contrasts have ≤5 samples per group (df = 2, 4 and 7), the asymptotic-z approximation is materially approximate for those inputs; they retain non-zero weight in the inverse-variance combination, so the fixed-effect Z and the derived τ² and I² should be read as approximate for genes whose evidence comes predominantly from the small-n contrasts."

---

## § C. Cosmetic

- **C1.** `MVP_PLOSONE_submission.md:289` (Fig. 2 legend): "Cross-animal held-out datasets (three folds) reach AUC 1.000 for GSE278227 … and GSE212311 … , and 0.917 … for GSE267799" — the sentence asserts three folds at 1.000 and then lists one at 0.917. Rewrite as in A3.
- **C2.** "DeLong intervals" is used at `:64` and `:289`; the intervals are 2,000-draw percentile bootstrap intervals (`p3_ml_leakage_controlled.py:76`, function literally named `delong_bootstrap_ci`). Rename to "2,000-resample percentile bootstrap intervals".
- **C3.** The GSE278227 row of `P3_lodo_auc_ci_leakage_controlled.csv` has `ci_lo = 0.9999999999999999`; printing it as "[1.0, 1.0]" is fine but should not be described as an exact boundary.
- **C4.** `:88` and `:112` print "30,687 scored"; summing `n_ligands` over the ten full-library rows of `P6_breadth_chembl_power.csv` gives 30,685. Use 30,685 or state the rounding rule.
- **C5.** `:88` writes "ADRA2A only weak (p = 0.027; AUC 0.791 → 0.797)" — 0.027 is the likelihood-ratio p; the Wald p is 0.504 (see A5). Label the test.

---

## § D. Stands up — things I suspected, checked, and found correct

1. **The corrected translatome-weight statement is arithmetically right.** The manuscript (`:44`) now says the two GSE265957 timepoints contribute w² = 2.00 = 11.4% of Σw², "comparable to — not twice — a single midsize bulk study (GSE241361_DRG w² = 2.22, 12.7%; GSE212311 w² = 1.50, 8.6%)". I recomputed: w = √(n₁n₂/(n₁+n₂)) gives 2.1909, 1.2247, 2.6458, 1.4907 — exactly the values in `META_bulkonly_sensitivity_summary.json` — and 1.00 each for the two n = 2/2 translatome contrasts; Σw² = 17.522; 2.00/17.522 = 11.41%; 2.222/17.522 = 12.68%; 1.50/17.522 = 8.56%. The retracted "twice the weight" claim is genuinely corrected, and the inverse-variance derivation is correct (Var(d) = 1/n_eff with n_eff = n₁n₂/(n₁+n₂), so w = √n_eff is the inverse-variance weight).

2. **Every random-effects heterogeneity number reproduces.** median τ² = 0.2324 (printed 0.232); median I² = 38.79% (printed 38.8%); 41.90% of genes with I² > 50% (printed 41.9%); 68.08% with τ² > 0 (printed 68.1%); RE core = 1,008 exactly, = 24.86% of 4,055 (printed 24.9%); the RE core is a strict subset of the FE core (1,008/1,008 overlap). The DerSimonian–Laird algebra in Methods `:148` is stated correctly.

3. **The non-circular translation test reproduces exactly and its denominators are coherent.** Background 6,779/14,390 = 47.11% (printed 47.1%, CI 46.3–47.9% — Wilson recomputed 46.29–47.93%); test stratum 2,266/4,899 = 46.25% (printed 46.2%, CI 44.9–47.7% — recomputed 44.86–47.65%); risk difference 46.25 − 47.11 = −0.86 pp (printed −0.9 pp); permutation p = 0.1396 (printed 0.14). The superseded 14,445/3,564 universe is correctly flagged as superseded. The circular figures (7,751/14,390 = 53.86%; 2,473/3,556 = 69.54%; 1,083 = 3,556 − 2,473; 2,318/4,306 = 53.83%) all check out, and the decision not to test them against a 50% null is correct.

4. **The target table's random-effects columns and the "4 of 10" claim are exact.** From `_R4_targets_fixed_vs_random.csv`: FDR_RE < 0.05 for TNIK 0.0212, SLC2A1 7.0 × 10⁻⁸, ADRA2A 0.0386, GALNS 0.0251 — exactly four, exactly the four named at `:90`. All ten FDR_RE values in Table 3a/3b match the source to the printed precision. ADRA2A indeed has the smallest |meta_Z| (4.84) of the ten.

5. **All five BH q-values in Table 3b reproduce** from `P6_BH_correction.csv`: ACVR1 0.00129 / 0.584; ADRA2A 0.118 / 0.0025; AXL 5.55 × 10⁻⁶ / 0.3525; MAPK14 1.48 × 10⁻⁴ / 0.584; TNIK 3.27 × 10⁻⁴ / 0.584. The two-filter conjunction is applied uniformly to the five testable targets: each fails at least one filter, and no target passes both.

6. **The "same animals" exclusion is factually correct.** `data/processed/GSE241361_sampletable.csv` pairs DRG and medulla samples within the same SNI animal (`E1_SNI1WTDRG` ↔ `E5_SNI1WTMedula`, `E3_SNI3WTDRG` ↔ `E7_SNI3WTMedula`, `F1_SNI2WTDRG` ↔ `F5_SNI2WTMedula`, `F3_SNI4WTDRG` ↔ `F7_SNI4WTMedula`). Excluding the two GSE241361 folds from the cross-animal mean is the right call and is properly disclosed.

7. **The bootstrap descriptive statistics reproduce exactly from the released 200-row file** — which is what let me find the underlying bug. From `_R4_targetset_bootstrap_resamples.csv`: 200 rows; median size 6.0 (IQR 5–8); median Jaccard 0.0263 (IQR 0.0238–0.0513); mean dock-eligible recovered 0.785 (printed 0.79); mean docked recovered 0.35; P(≥3 of 17) = 0.040; P(≥5 of 17) = 0.000; P(≥1 of 9) = 0.32; CDHR5 recovered in 31/200 = 15.5% (printed 15.5%). The decision to publish the per-resample rows is good practice and made this review possible.

8. **The spinal lineage counts are exact**: 20 localisable / 15 NotLocalisable / 7 cross-dataset-consistent, with the named genes matching the `confident` flags in `P5_hub_lineage_consensus.csv`. 32/35 hubs in the meta core (printed 91%) confirmed from `P3_hub_genes.csv`.

9. **The bulk-only set-level calls reproduce**: Neuroinflammation mean_Z +5.13 / perm p ≤ 0.0005; DAM +3.96; Complement +3.54; OXPHOS −2.80 with 72.2% of members down (frac_up = 0.2778) and the corrected down-polarity. The four SCN bulk meta_Z/FDR values in Table 1b match `META_bulkonly_sensitivity_summary.json`.

10. **Pooled-CV and permutation-null reporting is honest**: `P3_ml_metrics.csv` gives pooled 5×20 CV AUC 0.999 and label-permutation null 0.490, and the manuscript labels the former a "leakage-inflated optimistic upper bound" (`:64`). Correct framing.

---

## § E. Questions for the authors

1. **Pre-specification of the two-filter conjunction.** Where, and when relative to computing the enrichment results, was the rule "must pass both the full-library enrichment filter and the size-independent filter" recorded? The Methods (`:167`) state a three-part rule ("AUC > 0.5, survived correction, and exceeded the MW-only baseline") rather than a named two-filter conjunction. The cover letter asserts the analysis "was pre-specified and registered in the public repository before reporting". Please point to the commit or file.
2. **Why does the leakage-controlled LODO use the union of three selectors** (`p3_ml_leakage_controlled.py:116`) while the published 35-hub list uses the ≥2/3 consensus? Is the AUC meant to evaluate the published hub rule or a different one?
3. **Is GSE278227 ipsilateral-vs-contralateral paired within animal?** The sample table carries `rep` and `side` but I could not determine from the deposited metadata whether IL and CL come from the same rat. If paired, the AUC = 1.000 at n = 28 partly reflects a within-animal design that the incision fold (chronic vs baseline) may not share — and this should be stated.
4. **Is GSE267799 chronic vs baseline paired?** Rep indices overlap between the two groups (baseline rep1–4, chronic rep3–6). If the same animals are sampled longitudinally, the incision fold is a paired contrast and the 0.677 AUC has a different interpretation.
5. **Which strata, if any, does the 72-sample bootstrap preserve?** It is not stratified by dataset, so a resample can contain 0–6 GSE212311 samples. Given the strong dataset structure, is a dataset-level (cluster) bootstrap or a leave-one-dataset-out stability check available?
6. **Power of the human layer.** `P4_setlevel_test.json` gives mean ρ = 0.017 over 253 miRNAs, nominal t p = 0.029, permutation p = 0.51. What mean ρ would the permutation null detect at 80% power? The paper calls the layer "underpowered" without quantifying it.
7. **Tail rule for the ΔAUC p-values.** `p6_stats.py:243` — is `p_le0` computed as (count + 1)/(n_boot + 1)? If so, 0.0005 is exactly "0 of 2,000" and should be reported as ≤.
8. **Composite-ranking scoring set.** The composite ranking blends a "pharmacological-prior" term and is scored against the ADRA2A ChEMBL binder set. Are the prior terms derived from the same ChEMBL annotations used as labels? The manuscript says the hypergeometric p-values "largely restate the prior terms"; please state explicitly whether the prior was constructed from the same binder labels.

---

## § F. What I actually checked

**Files read in full or in part**
- `reports/MVP_PLOSONE_submission.md` (all 332 lines)
- `reports/MVP_PLOSONE_supplementary.md` (S4 region, lines 108–130)
- `reports/MVP_PLOSONE_cover_letter.md` (lines 11–13)
- `results/tables/META_DRG_axis_stouffer.csv`, `_R4_random_effects_meta.csv`, `_R4_targets_fixed_vs_random.csv`, `META_bulkonly_meta.csv`, `META_collapse_meta.csv`, `META_bulkonly_sensitivity_summary.json`
- `results/tables/P3_lodo_auc_ci.csv`, `P3_lodo_auc_ci_leakage_controlled.csv`, `P3_ml_metrics.csv`, `P3_ml_summary.json`, `P3_hub_genes.csv`
- `results/tables/P3_geneset_stats.csv`, `_R4_geneset_setlevel_bh.csv`
- `results/tables/P6_reverse_control.csv`, `P6_BH_correction.csv`, `P6_multivariate_physchem_control.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_breadth_chembl_power.csv`
- `results/tables/_R4_targetset_bootstrap_resamples.csv` (all 200 rows), `_R4_targetset_bootstrap.json`, `_R4_nerveinjury_only_summary.json`, `P4_setlevel_test.json`, `P5_hub_lineage_consensus.csv`
- `scripts/p3_ml.py`, `scripts/p3_hub_bootstrap.py`, `scripts/p7_targetset_bootstrap.py`, `scripts/p3_ml_leakage_controlled.py`, `scripts/p6_stats.py` (targeted)
- `data/processed/GSE278227_DRG_sampletable.csv`, `GSE267799_DRG_sampletable.csv`, `GSE212311_DRG_sampletable.csv`, `GSE241361_sampletable.csv`

**Recomputations performed**
- Core counts (16,552 tested; 6,869 FDR < 0.05; core 4,055) — exact match.
- Full recomputation of the random-effects table statistics, globally and stratified by K and by core membership, plus FE-core and hub I²/τ² medians.
- Weights from group sizes; Σw² and all percentage shares.
- Bulk-only loss decomposition (102 / 1,512 / 170 / ~211) and the fraction-matched counterfactual (3,587 = 88.5%).
- All 200-row bootstrap statistics and the per-gene dock-eligible recovery counts.
- Exact Mann–Whitney null distributions for all five LODO folds by dynamic programming.
- EPV for the five docking logistic models and for all five LODO folds.
- Re-execution of the p7 bootstrap pipeline (loaders, z-scoring, Top-800 pre-screen, `LogisticRegressionCV`, LASSO) to obtain `C_min = 8.5317` and per-resample LASSO non-zero counts (38 / 29 / 53), and the pooled class counts (37 cases / 35 controls).
- Wilson intervals for the reported concordance proportions.

**Discrepancies found between manuscript and source data**
1. `P3_geneset_stats.csv` gives OXPHOS perm p = 0.00400 while `_R4_geneset_setlevel_bh.csv` gives 0.00450 for the same set — two live artifacts disagree; the manuscript cites the latter. Harmless but should be reconciled (seed / draw count).
2. "30,687 scored" vs 30,685 summed from `P6_breadth_chembl_power.csv`.
3. The manuscript's "LASSO contributing no selections under resampling" is contradicted by my re-run (29–53 non-zero coefficients per resample).
4. All other numbers I checked matched the manuscript exactly; see § D.

---

## § G. Must-fix list, ordered by severity

| # | Severity | Item | One-line action |
|---|---|---|---|
| 1 | **Major** | A1 — XGBoost fitted to mis-paired (Xp, yb) in `p3_hub_bootstrap.py:85` and `p7_targetset_bootstrap.py:112` | Fix to `(Xbs, yb)`, re-run both bootstraps, re-emit all stability numbers and every sentence that cites them (Results `:66`, Table 2 `:316`, Methods `:158`, cover letter) |
| 2 | **Major** | A2 — FE-primary justified by a null-dominated median I² (38.8%) while the reported genes have median I² = 52.1% | Report both medians; demote gene-level claims to FE-conditional; keep the neuroimmune programme as the RE-robust claim |
| 3 | **Major** | A4 — "45.7% translatome-dependent" is 81.6% a consistency-threshold artefact | Replace with the decomposition and the 88.5% fraction-matched figure; re-rank the fragility (FE→RE is the dominant one) |
| 4 | **Major** | A3 — degenerate CIs and AUC = 1.0 at n = 6 (exact p = 0.050) | Report exact per-fold Mann–Whitney p; drop "establishing"; label Fig. 2A as raw and restate the leakage-controlled values |
| 5 | **Major** | A5 — two-filter rule applied to 5 of 10 targets; Wald standard applied to ACVR1 but not ADRA2A (Wald p = 0.504) | Correct the denominator to 5 in Abstract/Results/Conclusions; apply the Wald standard uniformly; note the shared-chemotype non-independence |
| 6 | **Major** | A6 — LODO classifier EPV 0.13–0.22 undisclosed; test set re-standardised on its own scaler | Disclose EPV per fold; fix `p3_ml_leakage_controlled.py:133`; re-emit the LC table |
| 7 | Minor | B1 — Neuropeptides_pain FE q = 0.047 unreported | Add one sentence to Results and the Fig. 1 legend |
| 8 | Minor | B2 — ADRA2A size-independent p = 0.0005 is the 2,000-draw bootstrap floor | Report as ≤ 0.0005 / q ≤ 0.0025 with a footnote |
| 9 | Minor | B3 — "24 detectable … 20 localisable (15 NotLocalisable)" mixes denominators | Split into two sentences with explicit denominators |
| 10 | Minor | B4 — two significant anti-concordant strata computed but unreported | Report `NI_FDR05_any_consistency` (45.8%, p = 8 × 10⁻⁴) and `NI_FDR05_AND_NIcons<0.8` (44.8%, p = 0.015) |
| 11 | Minor | B5 — permutation nulls assume gene/miRNA exchangeability | State the direction of the bias and its consequence for OXPHOS; add a correlation-preserving sensitivity if feasible |
| 12 | Minor | B6 — 67.3% of meta weight in two contrasts, one of them the held-out incision arm | Add the weight-circularity disclosure |
| 13 | Minor | B7 — three contrasts with df = 2, 4, 7 treated as asymptotic z | State the consequence for weighting and for τ²/I² |
| 14 | Cosmetic | C1 — Fig. 2 legend "three folds reach AUC 1.000" then lists 0.917 | Rewrite the sentence |
| 15 | Cosmetic | C2 — "DeLong intervals" are 2,000-draw percentile bootstrap intervals | Rename |
| 16 | Cosmetic | C4 — 30,687 vs 30,685 scored | Reconcile |
| 17 | Cosmetic | C5 — "ADRA2A p = 0.027" is the LR p; Wald p = 0.504 | Label the test |
