# Reviewer A2 — Design & Statistics
**Manuscript:** Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion… (v1.2.0, PLOS ONE re-submission candidate)
**Role:** Independent design/statistics review (fresh reading; no prior reviews read).
**Scope of this file:** meta-analysis design, sparse-cell inference, EPV, resampling stability, FE/RE choice, pseudoreplication. Every number below was recomputed from `results/tables/*.csv|json`, not from the manuscript text.

---

## § Per-item findings

### Item 1 — The "1,707 pure 4/4 + 495 K=3" sub-breakdown of the 2,202 overlap mis-describes the 495 genes (descriptive error that overstates directional agreement)

**【Problem】** Within the 2,202 primary-core ∩ bulk-core overlap, the manuscript states "1,707 genes are concordant across all four bulk contrasts (pure 4/4) and 495 are concordant in exactly 3 of 4 (K = 3)." This phrasing implies the 495 genes had all four bulk contrasts available and three agreed. The source data show the opposite: the 495 are genes present in only **3 of the 4 bulk datasets** (the fourth is absent/filtered for that gene, i.e. lower measurement K), and all 3 available agree. **Zero** genes have 4 bulk contrasts available with exactly 3 agreeing.

**【Evidence】** `META_bulkonly_meta.csv` (15,735 rows) merged with `META_DRG_axis_CORE_signature.csv` (4,055 core genes). Among the 2,202 overlap genes, `K` value_counts = {4: 1,707; 3: 495}. Of the 1,707 K=4 genes, 1,707 have max-agree-count = 4 (0 have exactly 3-of-4). Of the 495 K=3 genes, 495 have all-3-available agreeing (consistency = 1.0 by construction of the strict bulk core, which requires consistency ≥ 0.8). Recomputed: genes with 4 available bulk contrasts and exactly 3/4 agreement = **0**. The stored `consistency` column is 1.0 for **all** 2,202 overlap genes (the strict gate ≥0.8 for K=4 forces 4/4), so the "K=3" cannot denote 3-of-4 directional concordance — it denotes missing data (K=3 available).

**【Why it matters】** "Concordant in exactly 3 of 4" reads as evidence of a weak-but-real directional consensus among four independent bulk studies. In fact those 495 genes were simply not measured in one bulk study (typical for low-expression/filtering drop-out). Presenting them as "≥3/4 concordance, not strict 4/4" conflates *missing data* with *majority concordance* and overstates how well the 4,055-gene core is supported by the bulk layer. A reader auditing robustness (e.g., a meta-reviewer or a future replicator) would mis-estimate the bulk agreement rate.

**【Specific fix】** Replace the sentence (manuscript Results, "Bulk-only sensitivity meta-analysis…" paragraph; approx. line 50) with:
> "Within the 2,202-gene overlap, 1,707 genes were concordant across all four available bulk contrasts (pure 4/4); the remaining 495 were measured in only three of the four bulk datasets (the fourth was absent from the bulk analysis for that gene, e.g. expression below the detection/QC threshold) and were concordant in those three. The 'not strict 4/4' component of the overlap is therefore driven by reduced measurement coverage (lower K), not by directional disagreement among four available contrasts."

---

### Item 2 — "the remaining 468 fall outside even the relaxed ≥3/4 overlap" is numerically ambiguous (nesting, not addition)

**【Problem】** The text presents 313 (211 present-but-NS + 102 absent) and then "the remaining 468 fall outside even the relaxed ≥3/4 overlap," which a reader parses as 313 + 468 = 781 genes outside. In fact 313 is a **subset** of the 468.

**【Evidence】** Recomputed decomposition (primary core A = 4,055; bulk strict core B = 2,512; relaxed overlap = A ∩ {bulk FDR<0.05 & bulk consistency ≥ 0.75} = 3,587):
- absent from bulk file = 102;
- present in bulk but bulk meta_FDR ≥ 0.05 = 211 (matches manuscript);
- 313 = 102 + 211 = genes lacking *any* bulk significance;
- outside relaxed overlap = 468 = 102 (absent) + 211 (present, FDR≥0.05) + 155 (present, FDR<0.05 but bulk consistency < 0.75).
So 313 ⊂ 468; the correct relation is 468 = 313 + 155, not "remaining 468" as if additive.

**【Why it matters】** Minor, but the standalone "remaining 468" invites an arithmetic misread (781 outside vs the true 468) and slightly muddies the already-correct decomposition. The headline numbers (4,055 / 2,512 / 2,202 / 3,587 = 88.5% / 313 / 468) are each individually correct against source; only the connective wording is off.

**【Specific fix】** Rewrite as:
> "Of the 4,055 primary-core genes, 313 lack any bulk-study support (211 present in the four-bulk file but with bulk meta_FDR ≥ 0.05; 102 absent from the four-bulk file entirely). A total of 468 genes fall outside even the relaxed ≥3/4 overlap, comprising those 313 plus a further 155 genes that are bulk-significant (FDR<0.05) but fall below the 3/4 consistency gate."

---

### Item 3 — The "11.4% same-animal weight" overstates the true redundancy of the GSE265957 duplication (SE inflation is ~6%, not 11%)

**【Problem】** The manuscript frames the non-independence of the two GSE265957 timepoints as "11.4% same-animal weight" and concludes the FE meta SE is "marginally anti-conservative." The 11.4% is the share of total variance weight carried by the (non-independent) study, but the *redundancy* introduced by double-counting the same animals is only the duplicated timepoint's weight, i.e. ~5.7% of Σw² — shrinking the SE by ~6%, not 11%.

**【Evidence】** From `META_bulkonly_sensitivity_summary.json` contrast weights: GSE267799 2.1909, GSE212311 1.2247, GSE278227 2.6458, GSE241361_DRG 1.4907, plus GSE265957 D4/D63 each 1.00. Σw² = 2.1909² + 1.2247² + 2.6458² + 1.4907² + 1.00² + 1.00² = **17.5222**. GSE265957 two-timepoint contribution = 2.00/17.5222 = **11.41%** (manuscript correct on the share). But de-duplicating to a single longitudinal contrast (w=1.0 instead of 2×1.0) gives Σw² = 16.5222; SE = 1/√Σw² changes from 0.2389 to 0.2538, an understatement factor of **1.0625 (~6.2% too small)**. The *extra* weight from duplication is 1.0/17.52 = 5.7% of Σw².

**【Why it matters】** The qualitative conclusion ("marginally anti-conservative") is correct and the caveat (bounded by bulk-only 54.3% and collapse 91.4% sensitivity) is adequate. But "11.4% same-animal weight" can be (mis)read as "11.4% of the result is redundant/non-independent." The honest figure is that the duplication inflates Σw² by ~5.7% and shrinks the SE by ~6%; the 11.4% is the study's total share, most of which would persist even if correctly treated as one contrast.

**【Specific fix】** Amend the Methods/Results sentence (approx. line 44) to:
> "The two GSE265957 timepoints each carry w = 1.00, together 2.00 of Σw² = 17.52 (11.4% of total variance weight). Because they are the same animals, treating them as two independent inputs double-counts one longitudinal contrast; de-duplicating to a single contrast lowers Σw² to 16.52 and lengthens the fixed-effect SE by ~6% (0.239 → 0.254). The fixed-effect SE is therefore only marginally anti-conservative, and the influence of this non-independence is bounded by the bulk-only (overlap 54.3%) and collapse (retention 91.4%) sensitivity analyses."

---

### Item 4 — The "candidate nerve-injury-enriched LODO signal" effectively rests on a single cross-animal dataset, with EPV ≪ 1 and degenerate CIs that the Results narrative still leans on

**【Problem】** The manuscript presents a "candidate nerve-injury-enriched — not universally generalisable — LODO signal" supported by AUC = 1.000 in four of five folds. On closer inspection the supportive evidence is far thinner: the genuinely independent cross-animal nerve-injury folds that reach AUC 1.0 are GSE278227 (n = 28) and GSE212311 (n = 6). The GSE212311 result is the statistical floor (exact two-sided Mann–Whitney p = 0.10, the minimum attainable for 3-vs-3), and the two GSE241361 folds (n = 9 each, same animals) are explicitly excluded from the cross-animal mean. So the cross-animal nerve-injury-enriched conclusion rests essentially on **one** dataset (GSE278227, n = 28) built by a classifier that selects 139–164 features against ~44 training samples (EPV ≈ 0.15 ≪ 1). The AUC = 1.0 point estimates are quoted in the Results as a "signal" despite DeLong CIs of [1.0, 1.0].

**【Evidence】** `P3_lodo_auc_ci_leakage_controlled.csv`: GSE278227 1.0 [1.0,1.0] n=28; GSE212311 1.0 [1.0,1.0] n=6; GSE241361_DRG 1.0 [1.0,1.0] n=9; GSE241361_SC 1.0 [1.0,1.0] n=9; GSE267799 (incision) 0.677 [0.374, 0.940] n=20. `P3_ml_summary.json`: `lasso_1se_genes = 1`, confirming the linear signal is near-empty and hubs rely on ensemble integration of 139–164 selected features. Manuscript Results (approx. line 64) and Methods (approx. line 159–160) acknowledge EPV ≪ 1 and the DeLong collapse ("reported as non-informative rather than as evidence of perfect precision") but the Results still states "four of the five folds reached AUC 1.000" as support. Exact two-sided MW p for n=3 vs n=3 complete separation = 2/C(6,3) = 0.10 (manuscript states this correctly).

**【Why it matters】** A single-dataset, overfit-prone classifier yielding AUC = 1.0 is not strong evidence of a generalizable "nerve-injury-enriched" biology. The hedging words ("candidate", "not universal") are present, but the optimistic 1.0 point estimates are foregrounded while the zero-precision caveat sits in a subordinate clause. A reader could take away "the axis is enriched for nerve injury" more strongly than the data support.

**【Specific fix】** In the Results paragraph (approx. line 64) add immediately after the AUC list:
> "Because the two GSE241361 folds are same-animal and the GSE212311 fold (n = 6) sits at the exact-test floor (p = 0.10), the cross-animal nerve-injury-enriched conclusion rests on a single dataset (GSE278227, n = 28). That fold's AUC = 1.0 carries a degenerate DeLong CI [1.0, 1.0] and was produced by a classifier selecting 139–164 features from ~44 training samples (EPV ≈ 0.15), so the estimate's precision is unquantifiable; the result is therefore reported as an exploratory, hypothesis-generating signal requiring independent validation, not as a precision estimate."

---

### Item 5 — The EPV ≈ 1 critique is applied to ACVR1 but not to AXL/TNIK, whose "significant" likelihood-ratio tests rest on comparable low EPV

**【Problem】** The docking multivariate physicochemical control correctly dismisses ACVR1 (9 known binders, ~7 parameters, EPV ≈ 1; LR p = 9.6e-4 but Wald p = 0.17) as a non-reproducible fluctuation. The same low-EPV caveat is **not** applied to AXL (13 known binders) and TNIK (10 known binders), whose LR tests (p = 2.6e-5 and 7.3e-5) are cited as evidence the docking protocol "retains signal beyond chemotype."

**【Evidence】** `reports/MVP_PLOSONE_supplementary.md` Table S3: n_known binders = ACVR1 9, AXL 13, TNIK 10. The multivariate model has 6 physicochemical descriptors + docking affinity = 7 parameters. EPV = events/parameters ≈ ACVR1 1.3, AXL 1.9, TNIK 1.4. All three are far below the EPV ≥ 10 rule of thumb for stable logistic inference, yet only ACVR1 is flagged. Manuscript Discussion (approx. line 128–130) presents AXL/TNIK/ACVR1 as "the strongest positive controls… retain docking signal beyond chemotype" while separately dismissing ACVR1's fluctuation — an internal inconsistency in how EPV is weighted.

**【Why it matters】** With EPV ≈ 1–2, likelihood-ratio tests for all three are unstable; the ACVR1/Wald discrepancy demonstrates the hazard. Treating AXL/TNIK LR p-values as supportive validation while dismissing ACVR1 on the identical grounds makes the "partial validation" claim weaker than stated and is internally inconsistent.

**【Specific fix】** Either (a) report EPV for all five ChEMBL-annotated targets in Table S4 Panel A and apply the same "EPV ≈ 1–2, treat as descriptive" caveat to AXL (1.9) and TNIK (1.4) as to ACVR1 (1.3); or (b) soften the Discussion sentence to: "The three positive controls show docking affinity adding discrimination beyond chemotype in a post-hoc likelihood-ratio test, but with EPV ≈ 1–2 for all of them these tests are unstable and are reported descriptively, not as validation."

---

### Item 6 — DeLong CI collapse at AUC = 1.0 is acknowledged but the handling is incomplete (the point estimate is still used as support)

**【Problem】** The brief asks specifically whether the DeLong CI collapse at AUC = 1.0 is "acknowledged and handled correctly." It is acknowledged (Methods line ~159–160: "Four of the five leakage-controlled folds yield degenerate DeLong intervals ([1.0, 1.0])… reported as non-informative rather than as evidence of perfect precision"). However, "acknowledged" is not "handled": the Results still quotes the 1.0 AUC values as the basis for the nerve-injury-enriched signal (Item 4) without a precision qualifier adjacent to each estimate.

**【Evidence】** `P3_lodo_auc_ci_leakage_controlled.csv` shows three folds (GSE278227, GSE241361_DRG, GSE212311) with ci_lo = ci_hi = 1.0 — a degenerate interval that conveys zero precision information. Manuscript uses these in the sentence "four of the five folds reached AUC 1.000" as affirmative support.

**【Why it matters】** A [1.0, 1.0] CI means the AUC estimate has effectively no estimable precision; quoting "AUC 1.000" next to it as if it were a measured quantity invites over-reading. The caveat exists but is decoupled from the headline statement.

**【Specific fix】** Immediately qualify every AUC = 1.0 quote: e.g., "GSE278227 reached AUC 1.0 with a degenerate DeLong CI [1.0, 1.0] (zero estimable precision at n = 28), so this is reported as a directional signal, not a calibrated accuracy." Couple the caveat to the number, not buried in Methods.

---

### Item 7 — "12 GEO datasets (four nerve-injury, one incision)" conflates 5 meta-analysed studies with 7 localisation/miRNA/cell-line datasets

**【Problem】** The abstract and Introduction refer to "12 public GEO datasets (four nerve-injury, one incision)" as if 12 transcriptomic studies inform the DRG-axis meta core. In fact the meta-analysis uses **5 studies / 6 contrasts**; the other 7 are single-cell (×3), spatial (×1), human/mouse miRNA (×2), and an SH-SY5Y cell line (×1) used for localisation, the human plasma layer, and an opioid-mechanism reference — they do not contribute to the 4,055-gene core.

**【Evidence】** Methods "Data curation" (approx. line 143) lists 12 accessions; the meta-analysis section (approx. line 145–148) states "five independent studies are represented by six contrasts." Abstract (line 14) and Introduction (line 36) say "12 GEO datasets (four nerve-injury, one incision)" — the parenthetical accounts for only 5, implicitly presenting the 12 as the axis-evidence base.

**【Why it matters】** A reader could infer the 4,055-gene core is the consensus of 12 independent transcriptomic datasets when it rests on 5 studies (one of which, GSE265957, contributes two same-animal timepoints). This inflates the apparent evidentiary base for the core.

**【Specific fix】** Change the abstract/Introduction phrasing to:
> "We reanalysed 12 public GEO datasets — 5 transcriptomic studies (6 contrasts: four nerve-injury, one incision) that constitute the DRG-axis meta-analysis, plus 7 single-cell, spatial and miRNA datasets used for localisation and the human plasma layer."

---

### Item 8 — Independence of the 72 pooled ML samples is not stated; within-dataset non-independence could inflate effective n and understate EPV

**【Problem】** The dual-ML hub step "pooled into 72 samples" from 5 datasets and selects 139–164 features, giving EPV ≪ 1. The manuscript never states whether the 72 samples are independent biological replicates (e.g., multiple samples per animal/group would induce within-dataset correlation). LODO protects the *test* set from dataset-level dependence, but the training n and the EPV denominator (72) assume independence that may not hold.

**【Evidence】** Methods (approx. line 159): "Five DRG-axis datasets… were intra-dataset gene-z-scored, intersected to 13,208 common genes, and pooled into 72 samples." No statement on animal-level grouping, technical vs biological replicate status, or whether samples within a dataset are independent. `P3_ml_summary.json` reports `n_common_genes = 13208`, `lasso_1se_genes = 1`, consistent with heavy feature selection relative to sample size.

**【Why it matters】** If samples are not independent (e.g., repeated measures / multiple samples per animal), the effective n is below 72, EPV is even smaller than stated, and the "candidate" hubs are even less stable than the bootstrap (Item 9) already shows. The absence of this statement is a transparency gap.

**【Specific fix】** Add to Methods: "The 72 pooled samples comprise N independent biological replicates per dataset (state N per GSE); where a dataset contributed multiple samples per animal, these were treated as clustered and the LODO split respects animal identity so no animal appears in both train and test." If independence cannot be guaranteed, add "effective sample size is smaller than 72; reported EPV is an upper bound."

---

### Item 9 — Fixed-effect reported as primary foregrounds the heterogeneity-sensitive, optimistic core (only 24.9% persists under random effects)

**【Problem】** With 41.9% of genes showing I² > 50% and hub median I² = 72.8%, the FE core (4,055) is highly heterogeneity-sensitive; under DerSimonian–Laird RE the core shrinks to 1,008 (24.9%). Reporting FE as primary and leading with "a 4,055-gene core emerged" foregrounds the optimistic, anti-conservative estimate.

**【Evidence】** `_R4_supplementary_summary.json`: core_fixed_effect = 4,055, core_random_effects = 1,008, RE_retains_pct = 24.9, median_I2_pct = 38.8, pct_genes_I2_gt50 = 41.9. Manuscript abstract (line 18) leads with "A 4,055-gene core emerged under fixed effects but only 1,008 persisted under random effects" (transparent) yet the Results "coordinated axis" section (line 44–46) presents 4,055 first and the FE core as "the primary result."

**【Why it matters】** Choosing FE is defensible (real-sample-size weighting convention; heterogeneity-sensitivity is itself the object of the RE/bulk-only/collapse suite), and the manuscript does flag FE-conditional claims. But the narrative emphasis on 4,055 can lead a reader to over-read robustness. The defense is present; the emphasis is the issue.

**【Specific fix】** At the first mention of 4,055 in Results (approx. line 44), prefix: "a 4,055-gene core emerged under fixed effects (primary, heterogeneity-sensitive estimate; FE-conditional — see random-effects sensitivity below)." This keeps the number but immediately qualifies it.

---

## § Stands up (verified correct against raw sources)

1. **q = 0.003 is a genuine upper bound, not a point estimate (Check #3).** Recomputed from `P3_geneset_stats.csv` (perm_p for Neuroinflammation/DAM/Complement = 0.00049975 = 1/2001, the permutation resolution floor) and `_R4_geneset_setlevel_bh.csv` (perm_q = 0.0029985 ≈ 0.003 for all three). Because the true perm_p ≤ 1/2001, the true BH q ≤ 0.003; the manuscript's framing ("upper bound… significant beyond the resolution of 2,000 permutations") is statistically correct, and the sets are appropriately ordered by Stouffer Z rather than by sub-floor p.

2. **Headline core decomposition is correct (Check #1).** Recomputed from `META_DRG_axis_CORE_signature.csv` (4,055), `META_bulkonly_meta.csv` (bulk strict core = 2,512; overlap = 2,202; relaxed overlap A ∩ {bulk FDR<0.05 & consistency ≥ 0.75} = 3,587 = 88.5%), with 313 = 211 (present, bulk FDR≥0.05) + 102 (absent), and 468 outside relaxed. Every one of these matches the manuscript. The "45.7% translatome-dependence" reframe as a threshold/concordance artefact is supported.

3. **The non-circular translation test is honestly executed and reported (Check: nerve-injury-only).** `_R4_nerveinjury_only_summary.json`: NI core FE = 5,412, RE = 3,099; non-circular test NI_FDR05_AND_NIcons≥0.8 = 2,266/4,899 = 46.25%, permutation p = 0.1396 (manuscript 46.2%, p = 0.14); background 6,779/14,390 = 47.11%; risk difference −0.9 pp. The circular concordance (69.5% → 53.8% → 46.2%) is correctly downgraded and the 50% null is rightly rejected as inappropriate. This is a genuine strength.

4. **Bootstrap hub stability is framed honestly (Check #6).** `P3_hub_bootstrap.csv`: hub_freq ranges 0.14–1.0 (manuscript "14.0%–100.0%", correct); only 2/35 exceed ≥0.9 (SPRR1A 1.00, ATF3 0.935), 9 in the 0.5–0.75 "borderline" tier. The manuscript states the three-method consensus is genuine but "the remainder require prospective validation" — an accurate, non-overstated framing. (Note: the panel brief's premise "max 15.5% recovery, 0/35 at ≥0.9" does **not** match the source; the data show max 100% and 2/35 at ≥0.9, i.e. the manuscript's own statement is the correct one.)

5. **The honest docking null is well-supported (Check: docking).** No target clears both the full-library MW-corrected enrichment filter and the size-independent filter; ADRA2A full-library AUC = 0.532, p = 0.118 (non-informative); the ion-channel class was structurally undockable and explicitly never screened. The ACVR1 EPV ≈ 1 reasoning is correctly used to dismiss a spurious fluctuation. The "methodological boundary, not a false lead" framing is justified by the data.

6. **DeLong collapse is at least acknowledged (Check #5).** The manuscript does state the [1.0,1.0] intervals are non-informative (see Item 6 for the residual handling gap).

---

## § Questions for the authors

1. For the 495 K=3 overlap genes, what specifically causes the missing fourth bulk contrast (low expression / QC filtering / platform-specific dropout)? Reporting the per-study detection rate for those 495 would let readers judge whether "lower K" is benign.
2. Is the GSE265957 translatome a true longitudinal paired design (same animals D4 vs D63)? If so, have you considered a within-animal difference contrast as the single proper input, and would the FE core change materially?
3. For the dual-ML step, what is the animal-level / sample-level structure of the 72 pooled samples per dataset? Are any samples from the same animal, and does LODO respect animal identity?
4. The nerve-injury-enriched claim rests on GSE278227 (n = 28) alone among cross-animal folds. Is there any independent nerve-injury transcriptomic dataset (not used in the meta) that could serve as an external validation of the 35-hub set's enrichment?
5. For the docking multivariate control, can you report EPV (events/parameters) for AXL (13) and TNIK (10) alongside ACVR1 (9), and confirm the Wald vs LR discrepancy is not present for the former two?
6. The "12 datasets" wording — do you agree to rephrase as 5 meta-analysed studies plus 7 localisation/miRNA datasets, to avoid implying 12 independent transcriptomic replicates of the core?

---

## § What I actually checked (files read, commands run, values recomputed vs manuscript)

**Manuscript files read in full:** `reports/MVP_PLOSONE_submission.md` (lines 1–200+; abstract, results, discussion, methods, references) and `reports/MVP_PLOSONE_supplementary.md` (S1–S7, including S5b and S6 which cite the `_R4_*` sources).

**Source files recomputed (managed Python, `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`):**
- `META_DRG_axis_CORE_signature.csv` (4,055 rows) — primary core set A.
- `META_bulkonly_meta.csv` (15,735 rows) — bulk strict core B = {FDR<0.05 & consistency≥0.8} = 2,512; overlap A∩B = 2,202; K value_counts within overlap {4:1,707; 3:495}; 0 genes with 4-available-and-3-agree; relaxed overlap A∩{FDR<0.05 & consistency≥0.75} = 3,587; absent-from-bulk = 102; present-but-bulk-FDR≥0.05 = 211; outside-relaxed = 468. **Discrepancy vs manuscript:** none on the headline integers; the sub-breakdown wording "concordant in exactly 3 of 4 (K=3)" is inaccurate (those 495 have only 3 bulk contrasts *available*). The "remaining 468" is a subset relation, not additive.
- `META_collapse_meta.csv` — collapsed_core = 4,294, shared_core = 3,707, retained_fraction = 0.9142 (91.4%, matches manuscript).
- `META_bulkonly_sensitivity_summary.json` — contrast weights; Σw² = 17.52; GSE265957 share = 11.41%; de-duplicated Σw² = 16.52, SE lengthens ~6.2%. Manuscript's 11.4% share correct; its redundancy implication overstated (Item 3).
- `P3_geneset_stats.csv` and `_R4_geneset_setlevel_bh.csv` — perm_p floor = 1/2001 = 0.00049975; perm_q = 0.0029985 ≈ 0.003 for Neuroinflammation/Complement/DAM. **No discrepancy:** q=0.003 is a correct upper bound (Item, Stands-up #1).
- `P3_lodo_auc_ci.csv` and `P3_lodo_auc_ci_leakage_controlled.csv` — three folds with degenerate [1.0,1.0] CIs (GSE278227 n=28, GSE241361_DRG n=9, GSE212311 n=6); incision fold 0.677 [0.374,0.940]. Matches manuscript; handling gap noted (Items 4, 6).
- `P3_hub_bootstrap.csv` — hub_freq 0.14–1.0; 2/35 ≥0.9 (SPRR1A 1.0, ATF3 0.935); 9 in 0.5–0.75. **Discrepancy with panel brief's "max 15.5%, 0/35":** the brief's figure is wrong; the manuscript's "max 100%, 2/35 at ≥0.9" is correct.
- `P3_hub_genes.csv` — 35 hubs, `in_meta_core` boolean (32 True, 3 False: REG3B, ANKRD1, MEGF11); matches manuscript "32/35 (91%) in core."
- `P3_ml_summary.json` — lasso_1se_genes = 1; n_common_genes = 13,208; confirms sparse linear signal and EPV≪1 context.
- `_R4_nerveinjury_only_summary.json` — NI core FE 5,412 / RE 3,099; non-circular 2,266/4,899 = 46.25%, p = 0.1396; background 47.11%; −0.9 pp. Matches manuscript (Item, Stands-up #3).
- `_R4_supplementary_summary.json` — FE core 4,055, RE core 1,008 (24.9%), median I² 38.8%, 41.9% genes I²>50%. Matches manuscript (Item 9).
- `_R4_targets_fixed_vs_random.csv` and `_R4_targetset_bootstrap.csv` — RE retains 4/10 targets; dock-eligible recovery frequencies 0.125–0.885 (TFE3 0.885, CDHR5 0.875). Matches manuscript.
- `reports/MVP_PLOSONE_supplementary.md` Table S3/S4 — n_known binders ACVR1 9, AXL 13, TNIK 10; EPV critique applied to ACVR1 only (Item 5).

**Commands run (summary):** pandas reads of the above; set operations for overlap/relaxed; `np.sign`/`value_counts` for K and concordance; json loads for weights and summaries; BH q recomputation cross-checked against `_R4_geneset_setlevel_bh.csv`. All recomputed integers (4,055 / 2,512 / 2,202 / 3,587 / 88.5% / 313 / 211 / 102 / 468 / 1,008 / 24.9% / 46.2% / 47.1% / −0.9 pp / 0.003 / 11.4% / 6.2%) are stated above with their source.

**Explicit non-discrepancies:** the core decomposition headline integers, the q=0.003 upper-bound status, the non-circular translation statistics, the bootstrap stability framing (max 100%, 2/35 stable), and the honest docking null are all reproducible and correctly stated.

**Discrepancies / issues raised:** (a) Item 1 — "1,707 4/4 + 495 K=3" mis-describes the 495 as 3-of-4 concordant when they are 3-of-4 *available*; (b) Item 2 — "remaining 468" subset ambiguity; (c) Item 3 — 11.4% vs ~6% redundancy framing; (d) Item 4/6 — nerve-injury-enriched claim rests on one cross-animal dataset with EPV≪1 and degenerate CIs still quoted as support; (e) Item 5 — EPV critique applied inconsistently across ACVR1/AXL/TNIK; (f) Item 7 — "12 datasets" conflation; (g) Item 8 — ML sample independence unstated; (h) Item 9 — FE-primary emphasis.

**Independence note:** I did not read any `reviews/REVIEW_*.md`, `reviews/RESPONSE_*.md`, `reviews/REVISION_*.md`, other round12 siblings, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `PROJECT_PLAN.md`, `方案二_*.md`, or any gate script/output. All judgements derive from the manuscript text and the raw CSV/JSON sources listed above.
