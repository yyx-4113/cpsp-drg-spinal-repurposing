# Reviewer A2 — Study design and statistical methodology

**Manuscript:** `reports/MVP_PLOSONE_submission.md` (385 lines) + `reports/MVP_PLOSONE_supplementary.md`
**Reviewed under enforced independence:** no file under `reviews/` was opened; `MVP_STROBE_checklist.md` and `MVP_PLOSONE_compliance_check.md` were not opened. All judgments below derive from the manuscript, `scripts/`, `results/tables/` and `data/processed/`.
**Reviewer lane:** design and statistics. Domain biology (A1), code/reproducibility (A3) and journal compliance (A4) are out of lane and are only touched where they are inseparable from a statistical defect.

---

## Recommendation

# MAJOR REVISION

**Justification.** This is an unusually self-critical manuscript: the FE/RE discrepancy (4,055 → 1,008; OXPHOS q = 0.31 under RE), the circularity of the pooled consistency gate, the DeLong degeneracy, the EPV collapse, the permutation resolution floor and the docking null are all disclosed, and I verified that most of the arithmetic is correct (see *Independent recomputation*). The paper does not over-claim, and in several places it under-claims.

It cannot be accepted as it stands for one reason: **the primary gene-level result is not reproducible as reported**, because the two GSE265957 translatome inputs combine a direction taken from one Xtail column with a p-value taken from a different Xtail column (**T0-1**). When the sign is matched to the p-value actually used, the 4,055-gene core becomes a 2,750-gene core (Jaccard 0.337; 57.7% of the published core changes) and 7 of the 35 hubs change `in_meta_core` status. Every downstream number built on that core — hub core-membership, the non-circular translation strata, the gene-set vectors — is therefore conditional on an unspecified estimand. This is fixable by a re-run, not by reframing.

A second major issue sits one level down (**T1-1**): GSE278227 is a **within-animal paired** ipsilateral-vs-contralateral design. The manuscript never says so, and reports it as "n = 28" independent samples and as one of "the two genuinely independent cross-animal nerve-injury folds". That single fold carries the entire "nerve-injury-enriched" LODO conclusion (AUC 1.000), and a within-animal discrimination is not comparable with the between-animal incision fold (0.677).

Neither defect is a matter of interpretation; both are specification errors that change numbers. With T0-1 and T1-1 fixed and re-run, and with the T1/T2 wording corrections below, the statistical content would in my view be publishable.

---

## Findings

### T0 — submission-blocking

---

#### **T0-1** — GSE265957 translatome inputs: the Z direction comes from a different Xtail column than the p-value

**Location.**
- `scripts/p2_deg_meta.py:142` — `z = np.sign(xt["mRNA_log2FC"]) * stats.norm.isf(xt["pvalue_final"]/2)`
- `scripts/p2_meta_sensitivity.py:38` — identical construct
- `scripts/p7c_nerveinjury_only_meta.py:49` — identical construct
- Manuscript Methods → *Meta-analysis*: "the two translatome timepoints 1.00 each"; Results (line 44): "GSE265957's DRG input is a *translatome* (Xtail ribosome-profiling log2FC)".

**What is wrong.** In `data/processed/GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv` the columns are `mRNA_log2FC`, `RPF_log2FC`, `log2FC_TE_v1/pvalue_v1`, `log2FC_TE_v2/pvalue_v2`, `log2FC_TE_final/pvalue_final`. `pvalue_final` is the significance of the **translational-efficiency** change `log2FC_TE_final` (= `RPF_log2FC − mRNA_log2FC`); Xtail supplies no p-value for `mRNA_log2FC`. The code therefore attaches the **mRNA** direction to a **TE** p-value. Measured consequence:

| | genes with `pvalue_final` < 0.05 | sign(mRNA) ≠ sign(TE) |
|---|---|---|
| Day4 | 1,504 | 1,388 (92.3%) |
| Day63 | 270 | 244 (90.4%) |

**Why it matters.** The sign of a Z is the sign of the effect that its p-value tests. For ~90% of the genes that carry signal in these two inputs, the meta-analysis is summing a magnitude in one direction with a sign in the other. These two inputs carry 2.00 of Σw² = 17.52 (11.4%) and — more importantly — they are two of the six direction votes, so at K = 5 (where consistency ≥ 0.8 requires 5/5) a single flipped vote can eject a gene from the core.

Re-running the six-input meta with the sign taken from `log2FC_TE_final` (i.e. from the column whose p-value is used), everything else unchanged:

| | as published (`mRNA_log2FC`) | sign matched (`log2FC_TE_final`) |
|---|---|---|
| genes tested (K ≥ 3) | 16,552 | 16,552 |
| meta_FDR < 0.05 | 6,869 | 6,558 |
| core (FDR < 0.05 & consistency ≥ 0.8) | **4,055** | **2,750** |
| shared / Jaccard | — | 1,715 / **0.337** |
| hubs changing `in_meta_core` | — | AGRN, ANKRD13B, CTTN, ECEL1, PTPN23, RUBCN, WDR81 |

(Using `RPF_log2FC` as the sign instead gives meta_Z correlation r = 0.977 and 95.4% sign agreement with the published vector — a milder but still non-null change. The manuscript never states which of the three estimands it wants.)

**Fix.** State the estimand for GSE265957 explicitly (TE, or RPF-level translatome, or mRNA-level transcriptome), take **sign and p-value from the same column**, re-run `p2_deg_meta.py`, `p2_meta_sensitivity.py`, `p7c_nerveinjury_only_meta.py`, `p7b_translation_noncircular.py`, the gene-set stage and the hub `in_meta_core` flags, and update every number in the manuscript and supplement that descends from the core. If the mRNA-level direction is genuinely intended, `pvalue_final` cannot be used at all and the contrast must be re-derived from the deposited counts.

---

### T1 — major

---

#### **T1-1** — GSE278227 is a within-animal paired design; this is nowhere disclosed and it carries the central ML claim

**Location.** Results line 64: "the two genuinely independent cross-animal nerve-injury folds are GSE278227 (n = 28) and GSE212311 (n = 6)"; Methods → *Meta-analysis* ("GSE278227 14/14 → 2.65"); Methods → *Dual-ML hub identification* ("pooled into 72 samples"); Fig. 2 legend.

**What is wrong.** `data/processed/GSE278227_DRG_sampletable.csv` shows `DRG_M_1W_IL_R1 … R7` and `DRG_M_1W_CL_R1 … R7` (and the female set): ipsilateral and contralateral DRG from the **same animal**, matched by replicate index. The "1W pooled" contrast is therefore 14 animals × 2 sides, not 28 independent samples. Consequences:

1. **Meta weight.** For a paired standardised difference, n_eff = number of pairs = 14, so w should be √14 = 3.74, not √(14·14/28) = √7 = 2.65. As coded, the largest-weighted contrast is simultaneously analysed by an unpaired Welch test (which discards the pairing and attenuates Z) and weighted as if 28 independent units.
2. **ML fold.** The held-out fold on which the entire "candidate nerve-injury-enriched" conclusion rests (AUC 1.000, n = 28) is a **within-animal** discrimination. Removing all animal-level variation makes AUC = 1.0 far easier to attain than in the incision fold, which is a **between-animal** comparison (0.677). The manuscript's headline contrast — "nerve-injury folds 1.000 vs incision fold 0.677" — is confounded by design, not only by biology.
3. **Pooled 5×20 CV (0.999).** Splits can place one side of an animal in train and the other in test. The manuscript labels this "leakage-inflated" but attributes the inflation only to feature selection.
4. **Bootstrap unit.** The 72 "samples" are 49 animals (GSE278227 28 → 14; GSE241361 DRG 9 + SC 9 → 9; GSE267799 20; GSE212311 6). Both bootstrap scripts resample 72 sample rows with replacement.

**Fix.** Add to Methods: *"GSE278227 is a within-animal paired design: ipsilateral and contralateral DRG were profiled from the same rat (14 animals, 7 male and 7 female, at 1 week), giving 28 libraries from 14 animals. The contrast was analysed as an unpaired Welch test on 14 vs 14 libraries, which is conservative relative to a paired analysis; correspondingly the meta weight was computed from n = 14 vs 14 rather than from 14 pairs, which under-weights this contrast. The held-out GSE278227 LODO fold is therefore a within-animal discrimination and is not directly comparable with the between-animal incision fold; the nerve-injury-versus-incision contrast should be read as confounded by this design difference."* And to the ML paragraph: *"the 72 pooled libraries comprise 49 animals; the bootstrap resamples libraries, not animals, and so does not reproduce the within-animal pairing — stability figures are conditional on that simplification."* Ideally, add a paired re-analysis of GSE278227 (weight √14) as a sensitivity column, and re-run the hub bootstrap resampling **animals** (49 clusters).

---

#### **T1-2** — The "leakage-controlled LODO" does not evaluate the published hub rule

**Location.** Results line 64: "A leakage-controlled re-estimation (feature selection recomputed out-of-fold …) confirms the four nerve-injury folds at AUC 1.000 and the incision fold at 0.677"; Methods line 164; `scripts/p3_ml_leakage_controlled.py:116`.

**What is wrong.** `select_features()` returns `sel = lasso_set | rf_set | xgb_set` — the **union**, i.e. genes nominated by *any one* method (139–164 features, per `P3_lodo_auc_ci_leakage_controlled.csv`). The published hub rule is **≥2/3 consensus** (35 genes). The leakage-controlled AUCs therefore do not estimate the generalisation of the classifier actually described in the paper. Two further inconsistencies with the published pipeline: XGBoost is fitted on `Xtr` (all 13,208 common genes), not on the Top-800 pre-filter used in `p3_ml.py`, and uses *gain* importance rather than |SHAP|; RF and LASSO *are* fitted on the pre-filter.

**Why it matters.** The honest-evaluation number that the manuscript elevates to primary status is produced by a different estimator on a ~4× larger feature set. With EPV ≈ 0.13–0.22, feature-set size matters.

**Fix.** Either (a) re-run `p3_ml_leakage_controlled.py` with `sel = {g for g,v in votes.items() if v >= 2}` and the XGBoost trained on the Top-800 pre-filter with |SHAP|, or (b) relabel the existing table. Suggested wording for (b):

> *"A leakage-controlled re-estimation (feature selection recomputed out-of-fold) was run on the within-fold **union** of the three selectors (139–164 features), not on the published ≥2/3 consensus rule; it is therefore a leakage-controlled bound on the selection procedure, not a validation of the 35-hub classifier itself."*

---

#### **T1-3** — Test-set standardisation is fitted on the test set

**Location.** `scripts/p3_ml_leakage_controlled.py:133`:
```python
Xte_s = StandardScaler().fit_transform(Xte[:, [si[g] for g in sel]])
```

**What is wrong.** The scaler should be the one fitted on training (`sc.transform`). Here each held-out fold is re-centred and re-scaled using its own mean and SD, with n_test = 6, 9, 20 or 28. This is preprocessing adaptation to the test data and can move the decision scores — and hence the AUC — in an unpredictable direction at these sample sizes.

**Fix.** Replace with `sc.transform(...)` where `sc = StandardScaler().fit(Xtr_s)`, re-run, and update `P3_lodo_auc_ci_leakage_controlled.csv`, Results line 64, Table/Fig. 2 and the supplement. If the AUCs are unchanged, say so.

---

#### **T1-4** — "3,587/4,055 = 88.5%" is achieved by admitting one dissenting dataset, and 495 of those genes were never measured in a fourth dataset

**Location.** Results line 50 and Methods line 158: "the overlap rises to 3,587/4,055 = 88.5%, recovering 1,385 of the 1,853 genes that appear lost under the stricter gate"; "1,707 are pure 4/4 … and a further 495 were measured in only three of the four bulk datasets with all three agreeing, K = 3 by availability". Abstract/Table 1a carry the 88.5% figure.

**What I recomputed** (from `META_DRG_axis_stouffer.csv` and `META_bulkonly_meta.csv`):

| set | K = 3 | K = 4 | total | /4,055 |
|---|---|---|---|---|
| strict (bulk consistency ≥ 0.8) overlap | 495 | 1,707 | 2,202 | 54.30% |
| relaxed (bulk consistency ≥ 0.75) overlap | 495 | 3,092 | 3,587 | 88.46% |

So of the 3,092 K = 4 genes in the relaxed overlap, **1,385 are 3-of-4 concordant — i.e. they have an explicit dissenting bulk dataset** — and only 1,707 are 4/4. **Only 1,707/4,055 = 42.1% of the primary core is concordant across all four bulk datasets.** The 495 K = 3 genes are counted in both the strict and the relaxed overlap and never had a fourth measurement.

**Why it matters.** "Recovering 1,385 of the 1,853 genes that appear lost" implies the genes were lost to a threshold artefact. In fact 1,385 of them were lost because one of four datasets disagrees in direction — which is evidence about heterogeneity, not about a threshold. Reporting "88.5%" as the headline bulk-concordance figure, even with the caveats present, inflates the appearance of replication. (The K = 3-by-availability component is, as the manuscript says, a coverage issue rather than a disagreement, and calling it K = 3 is acceptable *provided* the count is never presented as 4-way replication.)

**Fix.** Report the decomposition as the primary statement. Suggested replacement for the Results sentence:

> *"Under the strict gate the overlap is 2,202/4,055 = 54.3%, of which 1,707 (42.1% of the core) are concordant in all four bulk datasets and 495 were measured in only three (K = 3 by availability). Relaxing the gate to ≥3/4 raises the overlap to 3,587/4,055 = 88.5%, but 1,385 of the 1,385 recovered K = 4 genes are 3-of-4 concordant with one explicit dissenting dataset. We therefore report 42.1% (1,707/4,055) as the strict four-way replication rate and 88.5% only as a ≥3/4 majority-concordance upper bound; the 45.7% shortfall is not solely a threshold artefact."*

---

#### **T1-5** — "Events-per-parameter ≤ 2 for all ChEMBL-annotated positive controls" is false, and two EPV conventions coexist

**Location.** Conclusions: "events-per-parameter ≤ 2 for all ChEMBL-annotated positive controls"; Results line 90: "AXL (… EPV ≈ 1.9) … TNIK (… EPV ≈ 1.4) … ACVR1 … EPV ≈ 1"; Discussion line 130: "ACVR1 1.1, AXL 1.6, TNIK 1.3, MAPK14 2.0, ADRA2A ≈14".

**What I recomputed.** `P6_multivariate_physchem_control.csv` and `scripts/P6_multivariate_BH_checks.py` show the fitted model is `binder ~ 1 + MW + logP + TPSA + HBD + HBA + rotB + neg_aff` → **8 parameters**. With `n_pos` from `P6_multivariate_physchem_control.csv`:

| target | n_pos | EPV (7 params) | EPV (8 params) |
|---|---|---|---|
| ACVR1 | 9 | 1.29 | **1.12** |
| ADRA2A | 115 | 16.43 | **14.38** |
| AXL | 13 | 1.86 | **1.62** |
| MAPK14 | 16 | 2.29 | **2.00** |
| TNIK | 10 | 1.43 | **1.25** |

**Why it matters.** ADRA2A's EPV is ≈14, not ≤2; the Conclusions sentence as written is a false statistical statement. The Results paragraph uses a 7-parameter convention and the Discussion an 8-parameter one for the same three models, so the manuscript gives two different EPVs for AXL (1.9 and 1.6), TNIK (1.4 and 1.3) and ACVR1 (~1 and 1.1).

**Fix.** Use 8 parameters throughout (7 fitted coefficients + intercept is the count the model actually estimates; if the intercept is excluded, say so explicitly). Replace the Conclusions clause with:

> *"events-per-parameter ≤ 2 for the four ChEMBL-annotated positive controls with adequate annotation (ACVR1 1.1, AXL 1.6, TNIK 1.3, MAPK14 2.0; ADRA2A 14.4)"*

and reconcile the Results paragraph to the same table.

---

### T2 — moderate

---

#### **T2-1** — The Abstract reports q = 0.003 without the resolution-floor caveat

**Location.** Abstract: "Gene-set tests confirmed a neuroimmune/DAM-like programme (q = 0.003 each)"; also Fig. 1 legend. The body (Results line 48) discloses the floor correctly and honestly.

**Why it matters.** The three headline gene-set results are pinned **at** the permutation floor. I verified the algebra: with 18 multi-member sets and three tied at the floor, BH gives q = (18/3)·(1/2001) = 6/2001 = **0.0029985**, which is exactly the `perm_q = 0.002999` in `_R4_geneset_setlevel_bh.csv`. So q = 0.003 is not an estimate of the FDR; it is the achievable ceiling. A reader who reads only the Abstract (or the Fig. 1 legend) cannot know this.

**Fix (Abstract).** *"Gene-set tests confirmed a neuroimmune/DAM-like programme; with 2,000 permutations the resolution floor is 1/2001, so the BH-adjusted q = 0.003 is an upper bound (significant beyond permutation resolution), not a calibrated FDR."* Add the same clause to the Fig. 1 legend.

---

#### **T2-2** — Both hub bootstraps hold the pre-screen and the LASSO penalty fixed at full-data values and resample libraries, not animals

**Location.** `scripts/p3_hub_bootstrap.py:61-68` and `scripts/p7_targetset_bootstrap.py:78-85`: the Top-800 Welch pre-filter (`POOL`) and `C_min` are computed once on all 72 samples, then reused in every resample; `rng.choice(len(yall), …)` resamples sample rows.

**Why it matters.** The pre-screen is the strongest selector in the pipeline (13,208 → 800) and is never re-derived, so the bootstrap measures only the stability of the three selectors *conditional on* a pool that was chosen using the full data. Reported stability (SPRR1A 1.00, ATF3 0.94) is therefore an upper bound. Resampling libraries rather than animals compounds this (see T1-1.4).

**Fix.** Either move the pre-filter inside the resampling loop (and re-select C by CV per resample, or at minimum state that C is fixed), or add: *"the Top-800 univariate pre-screen and the LASSO penalty were estimated once on all 72 libraries and held fixed across resamples, so the reported frequencies quantify selector stability conditional on a fixed candidate pool and are upper bounds on the stability of the full pipeline."*

*(Verification credit where due: I checked the specific bug flagged in the brief — XGBoost fitted on a non-resampled feature matrix against resampled labels. It is **genuinely fixed**. Both scripts do `Xb = Xp[idx]; yb = yall[idx]` and fit LASSO, RF and XGBoost on `Xb/yb`, with SHAP computed on `Xbs` (`p3_hub_bootstrap.py:82-92`, `p7_targetset_bootstrap.py:105-117`). Features and labels are resampled together.)*

---

#### **T2-3** — "reproducibly recovered as a structurally-tractable set" overstates the bootstrap evidence

**Location.** Results line 66 and supplement S7 line 302 ("The docking target set is **reproducibly recovered**"), citing mean 8.70/17 and P(≥3 of 17) = 1.000.

**Why it matters.** A mean of 8.70 of 17 is **51%** recovery; the docked nine are recovered at 3.93/9 = **44%**; `P(all 17) = P(all 9) = 0.000`; `P(≥5 of 9 docked) = 0.355`; median Jaccard with the published 35 is **0.304** (so ~70% of the union differs on a typical resample). Thresholds of "≥3 of 17" and "≥5 of 17" are near-trivial given a mean of 8.7 and do not support the word "reproducibly".

**Fix.** *"On a typical resample 8.70 of the 17 dock-eligible hubs (51%) and 3.93 of the 9 docked hubs (44%) are recovered; no resample recovers the full set (P = 0.000) and the median Jaccard with the published 35 is 0.304. The dock-eligible list is therefore recovered as a partially stable, structurally tractable subset — stable enough to define a screening set, not stable enough to treat individual membership as reproducible."* Report `P(≥9 of 17) = 0.525` and `P(≥5 of 9) = 0.355` alongside the trivial thresholds.

---

#### **T2-4** — The gene-set permutation reference ignores within-set gene–gene correlation

**Location.** Methods → *Gene-set statistics*: "calibrated by 2,000 same-size permutation tests"; `results/tables/_R4_geneset_setlevel_bh.csv`.

**Why it matters.** Sampling random same-size gene sets from the meta_Z vector is a competitive test whose null assumes exchangeability of genes. Real pathway members are co-regulated and correlated, so the true null variance of `mean_Z` is larger than the permutation reference and the calibration is anti-conservative. BH across sets is conservative under positive dependence between sets, but that does not fix correlation **within** a set. This is most consequential exactly where the manuscript's conclusion is threshold-sensitive: OXPHOS is FE q = 0.020 (called significant) and RE q = 0.31 (not); a variance-inflated (CAMERA-style) test could move the FE value across 0.05.

**Fix.** Add a rotation / sample-label-permutation or CAMERA-style variance-inflated gene-set test and report both; or state: *"the same-size random-gene-set reference does not model correlation among pathway members and is therefore anti-conservative; the neuroimmune sets (Stouffer Z ≈ +15 to +22) are far beyond any plausible inflation, whereas the OXPHOS result (Z = −10.3 FE, −4.1 RE) is the one most exposed to it."*

---

#### **T2-5** — DerSimonian–Laird with K = 3–6 per gene and a normal reference

**Location.** Methods → *Random-effects sensitivity (DerSimonian–Laird)*; `scripts/p7c_nerveinjury_only_meta.py:61-68`.

**Why it matters.** The number of contrasts per gene is 3–6 (I verified: of the 4,055 core genes, 204 have K = 3, 398 K = 4, 563 K = 5, 2,890 K = 6). DL's τ² estimator is downward-biased at small K, and the RE Wald statistic referred to a normal distribution (rather than a Knapp–Hartung t with K−1 df) is anti-conservative. The RE analysis is used to *shrink* the result, so the direction of the error is favourable here, but the 1,008-gene RE core and the per-target FDR_RE values inherit it.

**Fix.** State the limitation, and preferably add a Knapp–Hartung (or permutation) reference for `Z_RE` as a second column in Supplementary Table S6.

---

#### **T2-6** — "DeLong confidence interval" is a misnomer

**Location.** Results line 64 / Methods line 164 ("degenerate DeLong intervals"); `scripts/p3_ml_leakage_controlled.py:76-89` defines `delong_bootstrap_ci()`, which is a 2,000-draw **bootstrap percentile** CI.

**Why it matters.** DeLong is a closed-form variance estimator; its variance does not "collapse" — a bootstrap percentile CI degenerates when resamples are non-informative (here: complete separation at n = 6–9). The explanation offered ("because the DeLong variance collapses at small test n") attributes the degeneracy to the wrong estimator.

**Fix.** Replace "DeLong" with "bootstrap percentile (2,000 draws)" throughout, and replace the explanation with: *"the percentile bootstrap degenerates at complete separation and small n: resamples that contain only one class are discarded, so the 2.5th and 97.5th percentiles both sit at 1.0. These intervals carry no precision information."*

---

#### **T2-7** — "32/35 (91%) fell inside the meta core signature" is not independent corroboration

**Location.** Results line 62 and Discussion line 124 ("our contribution is the convergence and prioritisation across independent computational routes").

**Why it matters.** The hubs were selected by ML on a 72-library pool drawn from GSE278227, GSE267799, GSE241361 DRG and GSE212311 — four of the five studies that enter the six-contrast meta. The meta core is computed on the same data. The 91% overlap is therefore largely constructed, not convergent. (The spinal-cord fold and the localisation layers are the genuinely quasi-independent part.)

**Fix.** *"32/35 hubs also satisfy the meta core gate. Because the hub classifiers were trained on four of the five studies entering the meta-analysis, this overlap is not independent corroboration; it records that the ML-selected genes are also genome-wide significant under the meta model, and the independent evidence for the hubs comes only from the held-out spinal-cord fold and the single-cell/spatial layers."*

---

#### **T2-8** — The multivariate physicochemical family is excluded from the multiplicity registry but asserted positively in the Discussion

**Location.** Methods → *Multiple-testing registry*: "this five-test family is reported as a post-hoc physicochemical control and is explicitly not counted among the corrected inferential tests"; Discussion line 130: "the strongest positive controls (AXL, TNIK, ACVR1) retain docking discrimination beyond chemotype".

**Why it matters.** A positive claim cannot rest on a family the authors have declared non-inferential. The good news is that the claim survives correction: BH across the five LR p-values (`P6_multivariate_physchem_control.csv`) gives q = 1.28e-4 (AXL), 1.81e-4 (TNIK), 1.59e-3 (ACVR1), 0.034 (ADRA2A), 0.066 (MAPK14). Stating this strengthens rather than weakens the paper.

**Fix.** Either add the family to the registry with the BH q-values above, or soften the Discussion to: *"nominally (BH q = 1.3e-4, 1.8e-4 and 1.6e-3 across the five-target family), but at EPV ≈ 1–2 and in contradiction with the size-independent ΔAUC test, so we treat it as a method-capability demonstration."*

---

#### **T2-9** — Small-n Welch → asymptotic z with no distributional diagnostics

**Location.** Methods → *Meta-analysis*; `scripts/p2_deg_meta.py:154`.

**Why it matters.** Per-contrast Z are `sign(t)·Φ⁻¹(p/2)` from Welch tests with n = 3/3 (GSE212311), 4/5 (GSE241361) and 2/2 (GSE265957, and those are not even t-tests — they are Xtail TE p-values). The t → z conversion is exact only under within-group normality, which is untestable at n = 2–3. These three contrasts carry (1.50 + 2.22 + 1.00 + 1.00)/17.52 = **32.7%** of Σw².

**Fix.** Add one sentence: *"With per-group n as low as 2–5, the asymptotic normal reference for the per-contrast Z cannot be verified; contrasts with n ≤ 5 carry 32.7% of the total inverse-variance weight, and the collapse and bulk-only sensitivity analyses bound their influence."* Ideally also report a rank-based or permutation-based per-contrast p for the two smallest studies.

---

### T3 — minor

---

#### **T3-1** — 46.2% is a rounding of 46.25%
`2,266/4,899 = 0.46254` → 46.3% to one decimal. The manuscript writes 46.2% (from `round(r,4) = 0.4625`). Use 46.3% consistently, or state 46.25%.

#### **T3-2** — Fig. 1 legend omits the floor caveat
It repeats "q = 0.003" three times and "q = 0.020" once with no mention of the 1/2001 ceiling. Add the T2-1 clause.

#### **T3-3** — "real per-group sample size" counts RNA pools for GSE267799
Per the deposited GEO description, "RNA samples from seven to nine biological replicates at each time point were separated into three independent pools"; the DRG chronic-vs-baseline contrast is 12 vs 8 **pools**, not 12 vs 8 animals. Say "12 vs 8 sequencing libraries (each a pool of 2–3 animals)".

#### **T3-4** — "~44 training samples" applies only to the GSE278227 fold
Training sizes are 44, 52, 63, 63 and 66 for the five folds; the EPV range is 0.13–0.22. State the range or say "44 for the GSE278227 fold".

#### **T3-5** — Two superseded artifacts remain citable
`_R4_translation_noncircular.json` (universe 14,445) is superseded by `_R4_nerveinjury_only_summary.json` (14,390) — the manuscript says so, but the CSV remains in the release with a perm p of 0.79 for a stratum that the reported analysis gives as p = 0.14. Mark the file superseded in the supplement to prevent mis-citation.

---

## Independent recomputation

All recomputations were done from input artifacts (DEG tables, Xtail tables, meta CSVs), independently of the scripts' printed output. Where a script's output was used as a cross-check it is labelled "published". Python (numpy/pandas/scipy), no manuscript or script was modified.

### (1) Σw², the same-animal de-duplication and the fixed-effect SE correction

Inputs: per-group n from `data/processed/GSE267799_DRG_sampletable.csv` (12 chronic / 8 baseline), `GSE212311_DRG_sampletable.csv` (3/3), `GSE278227_DRG_sampletable.csv` (14 IL / 14 CL at 1W), `GSE241361_sampletable.csv` (4 SNI WT DRG / 5 Naive WT DRG), and the hardcoded 2/2 in `scripts/p2_deg_meta.py:157-158`.

```
w = sqrt(n1*n2/(n1+n2))
GSE267799    12/8   w = 2.190890  w^2 = 4.800000
GSE212311     3/3   w = 1.224745  w^2 = 1.500000
GSE278227    14/14  w = 2.645751  w^2 = 7.000000
GSE241361     4/5   w = 1.490712  w^2 = 2.222222
GSE265957 D4  2/2   w = 1.000000  w^2 = 1.000000
GSE265957 D63 2/2   w = 1.000000  w^2 = 1.000000
-------------------------------------------------
SUM w^2                          = 17.5222     (manuscript 17.52)   OK
de-duplicated (drop one w=1)      = 16.5222    (manuscript 16.52)   OK
reduction  (17.5222-16.5222)/17.5222 = 5.707 %  (manuscript 5.7 %)  OK
SE(d_FE) = 1/sqrt(SUM w^2):
  0.238894  ->  0.246017   ;  lengthening = 2.98 %  (manuscript "~3 %")  OK
```

Cross-check against `results/tables/META_bulkonly_sensitivity_summary.json` → `contrast_info[*].weight` = 2.19089023, 1.22474487, 2.64575131, 1.49071198. Identical.

**Judgment.** The arithmetic is correct. Note that 16.5222 is exactly the correct effective precision *if* the two same-animal timepoints are treated as having perfectly correlated sampling error (ρ = 1: two redundant measurements of one quantity carry the precision of one). The manuscript's "5.7% / ~3%" should be stated as that worst case: *"assuming ρ = 1 between the two same-animal timepoints"*. This is a disclosure point, not an error.

### (2) The bulk-overlap fractions and their K decomposition

Inputs: `results/tables/META_DRG_axis_stouffer.csv` (primary six-contrast meta) and `results/tables/META_bulkonly_meta.csv` (four-bulk meta). Gates reproduced exactly as in `scripts/p2_bulkonly_meta_genelevel.py` (`meta_FDR < 0.05`, `consistency = max(n_up,n_dn)/K`).

```
primary core (meta_FDR<0.05 & consistency>=0.8)      = 4,055      (manuscript 4,055)  OK
bulk-only rows with K>=3                              = 15,735
bulk meta_FDR<0.05                                    = 5,445  (with consistency>=0.8: 2,512)
strict  overlap (>=0.8)  with core                    = 2,202 / 4,055 = 54.30 %  (MS 54.3 %)   OK
relaxed overlap (>=0.75) with core                    = 3,587 / 4,055 = 88.46 %  (MS 88.5 %)   OK
K decomposition, strict 2,202 : {K=3: 495, K=4: 1,707}   (MS: 495 + 1,707)  OK
K decomposition, relaxed 3,587: {K=3: 495, K=4: 3,092}
  -> of the 3,092 K=4 genes, 3,092 - 1,707 = 1,385 are 3-of-4 (one dissenting dataset)
  -> 4,055 - 2,202 = 1,853 "lost" under the strict gate ; 3,587 - 2,202 = 1,385 recovered   OK
  -> 4,055 - 3,587 = 468 outside even the relaxed gate                                        OK
strict four-way replication rate = 1,707 / 4,055 = 42.1 %   (not stated in the manuscript)
bulk-only core internal composition: {K=3: 561, K=4: 1,951} -> 22.3 % of the 2,512 bulk core
                                     rests on only 3 of 4 datasets
primary core K distribution (six contrasts): {3: 204, 4: 398, 5: 563, 6: 2,890}
  -> only 71.3 % of the primary core was measured in all six contrasts
```

### (3) Stouffer Z for named genes, rebuilt from the per-contrast inputs

Inputs: `DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`, `DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv`, `DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv`, `DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv` (Z = sign(t)·Φ⁻¹(p/2)), and `GSE265957_Xtail_DRG_Day4/Day63_SNI_vs_SHM.csv` (Z = sign(mRNA_log2FC)·Φ⁻¹(pvalue_final/2), i.e. **as published**). Weights as in (1).

| gene | K | recomputed meta_Z | published meta_Z (`META_DRG_axis_stouffer.csv`) | published meta_FDR |
|---|---|---|---|---|
| ATF3 | 6 | **10.5333** | 10.5333 | 1.0e-21 |
| SPRR1A | 6 | 8.1841 | 8.1841 | 1.3e-13 |
| AXL | 6 | 6.1424 | 6.1424 | 2.9e-08 |
| TNIK | 6 | 8.0017 | 8.0017 | 4.3e-13 |
| ADRA2A | 6 | 4.8370 | 4.8370 | 1.5e-05 |
| GALNS | 6 | 5.7935 | 5.7935 | 1.8e-07 |
| SCN8A | 6 | −5.1129 | −5.1129 | 4.6e-06 |
| REG3B | 4 | 8.2782 | 8.2782 | 7.1e-14 |

All reproduce to 4 decimal places; "ATF3 ranked first (meta_Z 10.53, FDR 1.0e-21, consistency 1.00)" is confirmed, as are the Table 3 meta_Z values (ADRA2A 4.84, MAPK14 6.09, AXL 6.14, TNIK 8.00, ACVR1 6.95, SERPINE1 6.92, SLC2A1 6.83, GALNS 5.79, VASH2 6.00, ITPKC 7.18). Also reproduced: 16,552 genes tested and 6,869 at meta_FDR < 0.05. **The Stouffer machinery itself is implemented correctly.**

### (4) Events-per-parameter for the multivariate docking control

See the T1-5 table. Computed as `n_pos` / 8 from `results/tables/P6_multivariate_physchem_control.csv` with the parameter count taken from `scripts/P6_multivariate_BH_checks.py:125-126` (`Xb = [1, MW, logP, TPSA, HBD, HBA, rotB, neg_aff]`). **ADRA2A = 14.38**, so the Conclusions clause "events-per-parameter ≤ 2 for all ChEMBL-annotated positive controls" is false as written.

### (5) LODO events-per-parameter

From `P3_lodo_auc_ci_leakage_controlled.csv` (`n_selected`) with training size 72 − n:

| fold | n_test | training | n_selected | EPV (minority class ≈ training/2) |
|---|---|---|---|---|
| GSE278227 | 28 | 44 | 164 | 0.134 |
| GSE267799 | 20 | 52 | 142 | 0.183 |
| GSE241361 DRG | 9 | 63 | 139 | 0.223 |
| GSE241361 SC | 9 | 63 | 150 | 0.207 |
| GSE212311 | 6 | 66 | 158 | 0.209 |

"events-per-parameter ≈ 0.15" for the pivotal GSE278227 fold is confirmed. **The EPV caveats are appropriately disclosed.**

### (6) The BH permutation-floor algebra

`results/tables/_R4_geneset_setlevel_bh.csv` gives `perm_p = 0.000500` (= 1/2001 = 0.00049975) for Neuroinflammation, Complement and DAM_microglia under both FE and RE, and `perm_q = 0.002999`. With m = 18 multi-member sets and three tied at rank 3:

```
q = (18/3) * (1/2001) = 6/2001 = 0.0029985  ->  0.003      OK, matches perm_q = 0.002999
```

so q = 0.003 is exactly the BH-adjusted resolution ceiling, as the manuscript says. Also confirmed: OXPHOS FE `perm_q = 0.020240` (MS 0.020) and OXPHOS RE `perm_q = 0.310345` (MS 0.31). **The FE-only status of the OXPHOS limb is reported honestly** — the manuscript states it in the Abstract, Results, Discussion, Limitations, Conclusions and the Fig. 1 legend.

### (7) The GSE265957 sign/p-value mismatch (T0-1)

Input: `data/processed/GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv`, `…Day63_SNI_vs_SHM.csv`.

```
Day4 : genes with pvalue_final < 0.05 = 1,504 ; sign(mRNA_log2FC) != sign(log2FC_TE_final) = 1,388 (92.3 %)
       categories among significant: transcription_only 829, stable 266, translation_only 225,
                                     homodirectional 140, opposite_change 44
Day63: genes with pvalue_final < 0.05 =   270 ; sign(mRNA) != sign(TE) = 244 (90.4 %)
```

Re-running the full six-input meta with the sign taken from `log2FC_TE_final` (all else identical; my pipeline reproduces 16,552 / 6,869 / 4,055 exactly under the published convention):

```
core (FDR<0.05 & consistency>=0.8):  4,055 (as published)  ->  2,750 (sign matched)
shared = 1,715 ; only-as-published = 2,340 ; only-if-corrected = 1,035 ; Jaccard = 0.337
meta_FDR<0.05: 6,869 -> 6,558
hubs losing in_meta_core: AGRN, ANKRD13B, CTTN, ECEL1, PTPN23, RUBCN, WDR81
```

Sign taken from `RPF_log2FC` instead: r(meta_Z) = 0.9767 with the published vector, 95.4% sign agreement.

### (8) Bootstrap artifacts (verification of the reported stability claims)

`results/tables/P3_hub_bootstrap.csv` and `_R4_targetset_bootstrap.json`:
- per-gene recovery range 0.140 (CTTN) – 1.000 (SPRR1A) → "14.0%–100.0%" **OK**
- ≥0.9 stability: SPRR1A 1.000, ATF3 0.935 → "2/35 (SPRR1A 1.00, ATF3 0.94)" **OK**
- borderline 0.5–0.75: 9 hubs **OK**
- median resampled set size 43 (IQR 41–46), median Jaccard 0.304, mean 8.70/17, mean 3.93/9, P(≥3 of 17) = 1.000, P(≥5 of 17) = 0.990, TFE3 0.885 **all OK**
- also present in the JSON and not quoted in the manuscript: **P(all 17) = 0.000**, **P(all 9) = 0.000**, **P(≥5 of 9 docked) = 0.355**

### (9) Non-circular translation test

`_R4_nerveinjury_only_summary.json`: background 6,779/14,390 = 0.4711 (MS 47.1%, Wilson 46.3–47.9% — verified by hand: p̂ = 0.47109, SE = 0.004161, ±1.96 SE → [0.4628, 0.4792]); strong stratum 2,266/4,899 = 0.4625 (MS 46.2%); difference −0.86 pp (MS −0.9 pp); perm p = 0.1396 (MS 0.14). All confirmed. `P3_hub_bootstrap.csv` recovery range and the EPV table were re-derived as shown.

---

## Summary of what is statistically sound

For balance, the following were checked and are correct or appropriately caveated:
- The inverse-variance (effective-n) justification for w = √(n₁n₂/(n₁+n₂)) and the Σw² / de-duplication arithmetic (§1).
- The Stouffer implementation, the 16,552 / 6,869 / 4,055 counts and every hub/target meta_Z I spot-checked (§3).
- The FE-vs-RE discrepancy is reported honestly and repeatedly; OXPHOS (FE q = 0.020, RE q = 0.31) is never quietly upgraded to a finding.
- The non-circular translation test is correctly constructed (selection on nerve-injury contrasts only, incision used once), the permutation null is appropriate, and the circular 69.5% figure is explicitly withdrawn (§9).
- The permutation-floor disclosure in the *body* is exemplary (§6).
- The bootstrap bug flagged in the brief is genuinely fixed (§T2-2).
- The docking null, the breadth flip and the MW-confounder logic are internally consistent; ADRA2A is held to the same standard as the other nine targets.
- Cell-level pseudoreplication is avoided in the single-cell stage by using sample-level pseudobulk only, and the localisation findings are labelled "directional hints".

---

**Finding counts:** T0 × 1, T1 × 5, T2 × 9, T3 × 5.
