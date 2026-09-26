# A2 — Design / Statistics Reviewer Report
### Independent peer review of "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis"

**Reviewer role:** Design & statistics / meta-analysis / causal-inference methodologist.
**Manuscript type:** Reanalysis of public transcriptomes, PLOS ONE / Scientific Reports target (~290 lines).
**Review basis:** Treated as a first submission. All judgements derived from the manuscript text, the three named analysis scripts, and the result tables/JSON I recomputed myself. No other reviewer file, response letter, or prior-round document was consulted.

---

## Executive summary

The analytical pipeline is unusually transparent and the bulk of the headline numbers are **exactly reproducible** from the deposited tables: the primary 6-input core (4,055), the bulk-only 4-input core (2,512), the random-effects core (1,008), the heterogeneity statistics (median τ² = 0.232, median I² = 38.8%), and the non-circular translation proportions (46.3% vs 47.1%, −0.9 pp, p = 0.14) all match my independent recomputation. The multiple-testing registry is disciplined and the docking "honest null" is well scoped.

However, I identify **two major design defects** and several moderate issues that should be resolved before acceptance:

1. **GSE265957 non-independence is unresolved in the primary analysis.** Two ribosome-profiling timepoints (Day4, Day63) from the *same* SNI animal cohort are entered as two independent contrasts, each carrying a full independent-study weight (w = 1.00). This double-weights one study and, critically, the random-effects heterogeneity (τ², I²) is computed across a contrast set that violates the independence assumption on which DerSimonian–Laird rests. The sensitivity analyses exist but do not re-compute the RE statistics on the corrected structure.

2. **The headline ML generalisation metric uses the leakage-contaminated table.** The reported incision LODO AUC of 0.917 comes from `P3_lodo_auc_ci.csv` (feature-selection leakage present); the manuscript's *own* leakage-controlled table (`P3_lodo_auc_ci_leakage_controlled.csv`) shows the same test set at **AUC 0.677 [0.374, 0.940]** — a confidence interval that includes 0.5. The claim "Honest evaluation confirmed a real, not overfit, classifier signal" is therefore built on the leaky number, and the honest number instead corroborates the paper's null-translation thesis.

Detailed findings, each with Problem / Evidence / Why it matters / Specific fix, follow.

---

## Findings

### Finding 1 — GSE265957 Day4/Day63 enter the primary meta as two independent contrasts, double-weighting one study
【Problem】 Two ribosome-profiling timepoints from the same SNI animal cohort (GSE265957 Day4 acute, Day63 chronic) are treated as two independent meta-inputs, each assigned a full independent-study weight, so one study is counted twice in the 6-input primary.

【Evidence】 `scripts/p2_deg_meta.py` lines 157–158 set `w=np.full(len(xt_d4),np.sqrt(2*2/4))` (=1.0) and identically for Day63; `scripts/p2_meta_sensitivity.py` lines 68–69 repeat `w=np.full(len(xt_d4),1.0)` for both. The manuscript (Methods, weighting line) reports the per-contrast weights as GSE267799 2.19, GSE212311 1.22, GSE278227 2.65, GSE241361 DRG 1.49, **GSE265957 D4 1.00 and D63 1.00 each**. In the Stouffer Zc = Σ(w·Z)/√(Σw²), GSE265957 therefore contributes w² = 2.00 versus a single-study weight of 1.00 — i.e. **2× the variance weight** it would carry as one study. The "five independent studies / six contrasts" framing (Abstract line 14; Methods line 132) therefore understates the dependence: it is 4 independent studies + 1 study entered twice. My recomputation of the 6-input core from `results/tables/META_DRG_axis_stouffer.csv` gives **4,055** (matches the manuscript exactly); the 5-input collapse gives 4,294 with overlap 3,707/4,055 = 91.4% (manuscript line 248), so **8.6% (348 genes) of the primary core depends on the double-counting**.

【Why it matters】 The primary 4,055-gene core — the object on which gene-set tests, hub selection, and docking eligibility ultimately rest — is computed on a design that violates the independence assumption between two of its six inputs. More seriously, the random-effects Q/τ²/I² (median τ² = 0.232, median I² = 38.8%; both reproduced by me from `results/tables/_R4_random_effects_meta.csv`) are computed *across the same six contrasts*, so the between-study heterogeneity is itself contaminated by the correlated Day4/Day63 pair. A reader who accepts "six contrasts" as six independent observations is misled about the effective sample of studies (effective K = 5, not 6).

【Specific fix】 Either (a) demote the 6-input to a sensitivity and promote the 5-input collapsed meta (GSE265957 merged into a single study, as already produced by `p2_meta_sensitivity.py`) as the **primary**, or (b) implement a correlated-effects / multi-level meta (e.g. robust variance estimation, or meta-analyse Day4 and Day63 into one GSE265957 effect first, then include once). Explicitly state the effective number of independent studies is 5, not 6. Recompute the random-effects heterogeneity on the corrected (5-input) Z-vector so τ²/I² reflect independent studies.

---

### Finding 2 — Headline ML generalisation AUCs come from the leakage-contaminated table, not the leakage-controlled one
【Problem】 The reported incision generalisation AUC (0.917) is the feature-selection-leakage-contaminated value; the manuscript's own leakage-controlled table reports the same test set at AUC 0.677 with a confidence interval that includes 0.5.

【Evidence】 `results/tables/P3_lodo_auc_ci.csv` (non-leakage): `GSE267799_incision_ratDRG` auc = 0.9167, lo = 0.7291, hi = 1.0000, n = 20. `results/tables/P3_lodo_auc_ci_leakage_controlled.csv` (LC-LODO): same row auc = 0.6771, ci_lo = 0.3735, ci_hi = 0.9405, n = 20, n_selected = 142. The manuscript Results line 58 states "0.917 [0.729, 1.000] for GSE267799 (incision rat DRG, n = 20), the cross-animal LODO floor," and headlines "Honest evaluation confirmed a real, not overfit, classifier signal." The 0.917 figure is taken from the **leaky** file; the **honest** figure (0.677) is not reported as the primary number.

【Why it matters】 The claim of a real, generalisable classifier signal rests on the contaminated metric. The leakage-controlled incision AUC (0.677) is not statistically distinguishable from chance (CI spans 0.5), and — importantly — this *supports* rather than contradicts the paper's central thesis that the nerve-injury signature does not translate to incision. Reporting 0.917 as the "cross-animal floor" thus (i) overstates generalisation to the incision model, and (ii) is internally inconsistent with the manuscript's own leakage-controlled result and with its own non-circular translation conclusion.

【Specific fix】 Report `P3_lodo_auc_ci_leakage_controlled.csv` as the primary generalisation metric. Revise line 58 to state that the leakage-controlled cross-animal floor for incision is 0.677 [0.374, 0.940], not significant, in agreement with the non-circular null-translation result; retain the leaky 0.917 only as an explicitly labelled optimistic upper bound.

---

### Finding 3 — AUC = 1.000 with degenerate CIs on test sets of n = 6 and n = 9 used as "the most persuasive evidence"
【Problem】 Two of the five LODO folds (GSE212311, n = 6; GSE241361 DRG/SC, n = 9) yield AUC = 1.000 with CI [1.0, 1.0]; such values cannot support a precise generalisation claim, yet the manuscript calls the cross-animal mean "the most persuasive evidence."

【Evidence】 Both AUC tables show `GSE212311_CCI_ratDRG` auc = 1.0, ci = [1.0, 1.0], n = 6; `GSE241361_mouseDRG` / `GSE241361_mouseSC` auc = 1.0, n = 9. Manuscript line 58 calls the cross-animal mean "the most persuasive evidence because it is a wholly different model excluded at training"; line 60 acknowledges "Three of the five folds have degenerate confidence intervals (point estimate 1.000 with CI [1.0, 1.0]) because the DeLong variance collapses at small test n, so the CIs are not interpretable as precision statements there" — but the headline figure is unchanged.

【Why it matters】 A test set of 3 positives / 3 negatives (GSE212311) produces AUC = 1.0 almost by construction and carries no information about generalisation; the cross-animal "floor" of 0.917 is propped up by a 6-sample fold. Treating n ≤ 9 perfect-separation folds as evidence of a robust classifier overstates the strength of the ML result relative to what the data support.

【Specific fix】 Present AUCs on n < 10 as descriptive only, with an explicit "not a precision statement" caveat attached to each. Replace the "cross-animal floor 0.917" language with the leakage-controlled, adequately-powered result. Consider a pooled repeated-CV with a larger, genuinely held-out test partition rather than leave-one-dataset-out folds of n = 6.

---

### Finding 4 — "Substantial" heterogeneity is an overstatement at effective K = 5
【Problem】 Median I² = 38.8% is described as "substantial heterogeneity," but by the standard Higgins–Thompson conventions (25% = low, 50% = moderate, 75% = high) a value of ~39% is low-to-moderate.

【Evidence】 `results/tables/_R4_random_effects_meta.csv`: median I² = 38.79 (my recomputation 38.785), median τ² = 0.2324 (recomputed 0.2324), I² > 50% in 41.9% of genes, τ² > 0 in 68.1% (both reproduced: 0.419 and 0.681). Manuscript line 40: "Heterogeneity was substantial: median τ² = 0.232 and median I² = 38.8%." DerSimonian–Laird τ² is known to be biased and high-variance at K ≤ 6, and here the effective independent K is 5 (one study double-entered, see Finding 1).

【Why it matters】 The word "substantial" primes the reader to expect large true between-contrast variability. A median I² of ~39% is modest, and — combined with the small effective K — the I² estimate has very wide uncertainty. Moreover, the dramatic core collapse (4,055 → 1,008, a 75% loss) is driven as much by the small per-contrast weights (w ≈ 1.0–2.65) and the inverse-variance re-weighting at K = 5–6 as by biological heterogeneity per se; a reader may attribute all of the shrinkage to "heterogeneity" when small-K instability is a co-contributor.

【Specific fix】 Relabel as "low-to-moderate (median I² ≈ 39%)" and add that RE statistics at K = 5–6 have wide uncertainty and should be read as a sensitivity bound (which the manuscript already does for the core, but not for the I² interpretation). Avoid presenting the heterogeneity magnitude as precisely estimated.

---

### Finding 5 — Random-effects Q/τ²/I² are computed on the non-independent GSE265957 pair
【Problem】 The DerSimonian–Laird Q statistic assumes independent effect sizes; here two of the six "studies" (Day4, Day63) are correlated, so the between-study variance is contaminated.

【Evidence】 `scripts/p2_meta_sensitivity.py` / `scripts/p7c_nerveinjury_only_meta.py` build the Z-vector with GSE265957 as two entries; the RE computation in the latter (lines 63–67) applies Q = Σ w²(d−d_FE)² across all K = 6 entries. The manuscript Methods line 136 states the DL formula is applied to "the same per-contrast effects." With two correlated entries, Q is not a valid χ²_{K−1} statistic, so τ² and I² are biased.

【Why it matters】 The entire random-effects sensitivity narrative — "core collapses 4,055 → 1,008," "median τ² = 0.232," "median I² = 38.8%," "68.1% of genes show τ² > 0" — inherits this bias. The RE core and the heterogeneity interpretation are both built on a violated independence assumption, which compounds Finding 1.

【Specific fix】 Recompute the RE meta on the 5-input (collapsed GSE265957) Z-vector so Q, τ², I² and the RE core reflect independent studies; report the 6-input RE only as a secondary "uncorrected for within-study correlation" sensitivity with the caveat stated explicitly.

---

### Finding 6 — The three q = 0.003 gene sets are heavily overlapping (one coherent axis counted three times)
【Problem】 Neuroinflammation, DAM-microglia and Complement are reported as three independent "q = 0.003" coordinated programmes, but they share many members, so the effective number of independent discoveries is near one.

【Evidence】 `results/tables/_R4_geneset_setlevel_bh.csv`: fixed perm_q = 0.0029985 for all three (my recomputation matches). The sets overlap structurally (e.g. C1QA/B/C appear in both Complement and DAM_microglia; cytokines such as IL6/TNF/CCL2 appear in Neuroinflammation and DAM). The manuscript line 42 lists three programmes and the abstract states "coordinated neuroinflammation, DAM-microglia and complement activation (q = 0.003 each)." The manuscript does acknowledge set overlap (Methods line 143: "The 18 multi-member gene sets overlap and are not independent; … the reported q-values are upper bounds"), which is honest, but the reader-facing count is still "three programmes."

【Why it matters】 Presenting three significant families with identical q overstates the breadth of independent confirmation. The biology is a single coordinated neuroimmune programme; counting it three times inflates the apparent robustness of the axis conclusion.

【Specific fix】 Report a pairwise overlap (e.g. Jaccard / shared-gene counts) among the significant sets and state the effective number of independent discoveries. Keep the "coordinated neuroimmune programme" framing (already used in Discussion) as the primary interpretation rather than "three independent programmes."

---

### Finding 7 — OXPHOS is significant under fixed effects (q = 0.020) and CPSP-literature is significant (q = 0.021); the "broad ion channels did not change" framing needs qualification
【Problem】 Under fixed effects OXPHOS (q = 0.020) and the curated CPSP-literature set (q = 0.021) are both significant, yet the abstract emphasises OXPHOS "did not survive random-effects correction (q = 0.31)" and the text states "broad ion-channel families did not change coordinately," which a reader may read as channels being unchanged.

【Evidence】 `_R4_geneset_setlevel_bh.csv`: OXPHOS fixed perm_q = 0.02024 (recomputed 0.0202), random perm_q = 0.31034; CPSP_literature fixed perm_q = 0.02060. Manuscript line 42: OXPHOS "q = 0.020" (fixed) but Abstract "OXPHOS did not survive random-effects correction (q = 0.31)"; line 42 "Broad ion-channel families did not change coordinately at the family-aggregate level (Nav_SCN q = 0.44; TRP q = 0.89; CACNA q = 0.85; Kv/KCNQ q = 0.85)."

【Why it matters】 The family-aggregate (set-level) test is methodologically sound — a family-wide null coexists legitimately with individually significant members (SCN9A/10A/11A/8A in Table 1b). But (a) OXPHOS is a real *fixed-effect* finding, not a pure null, and (b) the CPSP-literature curated set being significant qualifies the "ion channels did not change" narrative. Left unqualified, the abstract's OXPHOS phrasing could be cited as "OXPHOS showed nothing."

【Specific fix】 In the abstract and results, clarify that OXPHOS is significant under fixed effects (q = 0.02) and only fails under random effects; note the CPSP-literature set significance alongside the broad-family null so the "coordinately vs individually" distinction is explicit.

---

### Finding 8 — Reverse positive controls fail the size-independent enrichment test, so "method validation" is incomplete
【Problem】 Even the strongest reverse positive controls (AXL, TNIK) have size-independent ΔAUC 95% confidence intervals that contain zero, and none survives the stricter size-independent test; the screen therefore cannot demonstrate it separates known binders after molecular-weight correction.

【Evidence】 Manuscript line 82: AXL size-independent ΔAUC 95% CI [−0.030, +0.104]; TNIK [−0.224, +0.193]; "none survives the stricter size-independent enrichment test." Reverse positive-control point AUCs are AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779. The fidelity ceiling ρ ≈ 0.78 is acknowledged (line 82, 154).

【Why it matters】 A virtual screen whose positive controls do not survive the stricter correction cannot claim it "can in principle separate known binders" beyond chemotype. The honest null is therefore partly attributable to docking resolution (the ρ ≈ 0.78 ceiling) rather than a true absence of repurposing signal. The conclusion is honestly scoped ("docking enrichment at library scale"), but the strength of the implicit "the method works" premise is weaker than the positive-control AUCs suggest.

【Specific fix】 State explicitly that the reverse positive controls validate only the raw/chemotype ranking, not the size-independent test; frame the honest null as "no signal detectable above the MW/chemotype baseline at this docking fidelity," and present the ρ ≈ 0.78 ceiling as a direct limitation on what the screen could in principle detect.

---

### Finding 9 — Human-miRNA p = 0.51 negative control is underpowered: adequate as a scoping null, not as evidence of no human translation
【Problem】 The set-level permutation test returns p = 0.51; with n = 60 and 253 plasma-detectable miRNAs this cannot distinguish a true null from a modest real association.

【Evidence】 `results/tables/P4_setlevel_test.json`: perm_p = 0.5101 (reproduces the manuscript's p = 0.51). Manuscript line 64 correctly scopes it: "underpowered, and it is uninformative about the DRG–spinal axis itself, which is not sampled by plasma."

【Why it matters】 As a negative control it usefully shows the permutation procedure does not manufacture a spurious signal, but it cannot rule out a real human association. The manuscript is honest about this, so the impact is low; the only risk is if the null is later cited as supporting "no human translation."

【Specific fix】 Keep it as a scoping null and explicitly label it "failed to detect, not evidence of absence"; add a short power statement (e.g. the minimum effect size detectable at n = 60).

---

### Finding 10 — Two gene universes (16,552 meta vs 14,390 concordance) should be explicitly distinguished
【Problem】 The abstract reports "A Stouffer meta-analysis of 16,552 genes" (the union across ≥3 of 6 contrasts), while the non-circular concordance uses a denominator of 14,390 (genes measured in *all* six contrasts); a reader could conflate the two.

【Evidence】 Manuscript line 248 "16,552 genes tested"; line 52 "single measured universe of 14,390 genes shared across the six contrasts (3,556 of which fall in the 4,055-gene core)." My recomputation confirms the 4,055 core, and the JSON `all_measured` stratum gives n = 14,390 / k = 6,779 (47.1%), the `NI_FDR05_AND_NIcons>=0.8` stratum n = 4,899 / k = 2,266 (46.3%) — both internally consistent. The 14,390 ⊂ 16,552 (intersection vs union-K≥3).

【Why it matters】 Low risk, but the two inclusion rules (union-K≥3 for the meta; intersection-all-6 for concordance) are easy to confuse and could prompt a reviewer question about denominator inconsistency.

【Specific fix】 Add one sentence clarifying that 16,552 is the meta universe (genes in ≥3 contrasts) while 14,390 is the concordance universe (genes in all six contrasts), and that 3,556/4,055 core genes sit in the latter.

---

## § Stands up (strengths, with evidence)

1. **Core counts are exactly reproducible from the deposited tables.** Recomputing `META_DRG_axis_stouffer.csv` (16,552 rows) with an exact step-up BH and the manuscript's `meta_FDR < 0.05 & consistency ≥ 0.8` rule yields **4,055**; `META_bulkonly_meta.csv` yields **2,512**; the RE table yields **1,008**. The BH implementation in `p2_deg_meta.py` (`bh()`), `p2_meta_sensitivity.py`, and `p7c_nerveinjury_only_meta.py` is the standard step-up form and is correct. This level of reproducibility is well above typical for the field.

2. **The non-circular translation test is correctly constructed and the right test is used.** The signature is built on the five nerve-injury contrasts only, with the incision contrast held out as a single test; the agreement is compared to an empirical permutation null (5,000 relabels), which is *more* appropriate than a naive binomial/2-proportion test because it respects the global directional skew of the incision contrast (the manuscript explicitly rejects the 50% null). My recomputation from `_R4_nerveinjury_only_summary.json` reproduces 46.3% (2,266/4,899) vs 47.1% (6,779/14,390), −0.9 pp, permutation p = 0.1396 ≈ 0.14. (A manual 2-proportion test gives p = 0.30 — non-significant either way, and the permutation is the defensible choice.)

3. **The multiple-testing registry is genuinely disciplined.** Correction is applied within analytical families (per-dataset DE, meta fixed/RE separately, 18-set BH, docking BH, single-cell sample-level BH); composite-ranking hypergeometric p-values and permutation nulls are explicitly *excluded* from inferential claims (Methods line 158). The 18 multi-member set-level BH is present and correctly implemented; the q = 0.003 result for the three neuroimmune sets is a valid step-up BH value (0.0005 × 18/3).

4. **The bulk-only sensitivity is a real, method-identical robustness check.** Excluding GSE265957 entirely, the 4-bulk meta (same union-K≥3 rule) gives core 2,512 with 2,202/4,055 = 54.3% overlap with the primary core — a genuine fragility statement the authors lead with rather than bury. The negative-control logic (miRNA, docking) is disclosed as underpowered/proxy rather than overclaimed.

---

## § Questions for the authors

1. Can you confirm that GSE265957 Day4 and Day63 are the same animal cohort (ribosome profiling at two timepoints of one SNI experiment)? If so, will you re-run the **primary and the random-effects** meta treating GSE265957 as a single study, or with a correlated-effects / multi-level model?
2. Why is the leakage-contaminated incision AUC (0.917) reported as the primary generalisation metric when your own `P3_lodo_auc_ci_leakage_controlled.csv` shows 0.677 [0.374, 0.940] for the same test set? Will you promote the leakage-controlled values to primary?
3. Given test folds of n = 6 and n = 9, how should a reader interpret AUC = 1.000? Can you provide a pooled, adequately-powered cross-validation rather than leave-one-dataset-out folds of ≤9 samples?
4. Is "substantial heterogeneity" the right label for median I² ≈ 39% at an effective K of 5? Would you reframe and add the small-K uncertainty?
5. The CPSP-literature curated set is significant under fixed effects (q = 0.021) — does that qualify the "broad ion channels did not change coordinately" statement, and should OXPHOS be described as a fixed-effect finding rather than implied-null?

---

## § What I actually checked

**Files read (full or relevant sections):**
- `reports/MVP_ScientificReports_submission.md` — full manuscript (Abstract, Results, Discussion, Methods).
- `scripts/p2_deg_meta.py` — Stouffer meta, BH, primary/Day4/Day63 weighting, core definition.
- `scripts/p2_meta_sensitivity.py` — 6-input vs 5-input collapse sensitivity.
- `scripts/p3_genesets.py` — 18-set Stouffer/permutation gene-set statistics.
- `scripts/p7c_nerveinjury_only_meta.py` — definitive non-circular test (NI-only meta, permutation null).
- `scripts/p3_ml_leakage_controlled.py` — leakage-controlled LODO AUC generation (partial).
- Result tables/JSON: `META_DRG_axis_stouffer.csv`, `META_bulkonly_meta.csv`, `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_summary.json`, `_R4_geneset_setlevel_bh.csv`, `P3_geneset_stats.csv`, `P3_lodo_auc_ci.csv`, `P3_lodo_auc_ci_leakage_controlled.csv`, `P4_setlevel_test.json`.

**Commands run / recomputations performed (values stated are mine, independently recomputed):**
- Primary 6-input core from `META_DRG_axis_stouffer.csv`: **4,055** (meta_FDR < 0.05 & consistency ≥ 0.8; BH re-implemented independently, identical result). Core K-distribution: K6 = 2,890, K5 = 563, K4 = 398, K3 = 204; 1,165 core genes have K < 6.
- Bulk-only 4-input core from `META_bulkonly_meta.csv`: **2,512** (identical BH rule). Overlap with primary core = 2,202/4,055 = 54.3% (reproduced).
- Random-effects core from `_R4_random_effects_meta.csv`: **1,008** (FDR_RE < 0.05 & consistency ≥ 0.8); fixed-effect core from same file = 4,055. Median τ² = 0.2324 (manuscript 0.232); median I² = 38.785 (manuscript 38.8%); I² > 50% in 41.9%, τ² > 0 in 68.1% (both match).
- Non-circular translation from `_R4_nerveinjury_only_summary.json`: background 6,779/14,390 = 47.11%; NI-significant & NI-consistent 2,266/4,899 = 46.25%; difference −0.86 pp ≈ −0.9 pp; permutation p = 0.1396 ≈ 0.14. Independent 2-proportion z-test on the same counts: difference −0.85 pp, z = −1.035, p = 0.30 (non-significant; permutation is the appropriate test).
- Set-level BH from `_R4_geneset_setlevel_bh.csv`: Neuroinflammation/Complement/DAM_microglia fixed perm_q = 0.0029985 (≡ 0.003); OXPHOS fixed perm_q = 0.02024 (significant, fixed), random perm_q = 0.31034 (≡ 0.31); CPSP_literature fixed perm_q = 0.02060. All match my recomputation of step-up BH across the 18 multi-member sets.
- AUC comparison: `P3_lodo_auc_ci.csv` GSE267799 incision auc = 0.9167 [0.729, 1.000]; `P3_lodo_auc_ci_leakage_controlled.csv` same test auc = 0.6771 [0.374, 0.940], n_selected = 142. Other four test sets remain AUC = 1.000 in both files; GSE212311 (n = 6) and GSE241361 DRG/SC (n = 9) carry degenerate CI [1.0, 1.0].
- Human-miRNA negative control: `P4_setlevel_test.json` perm_p = 0.5101 (≡ 0.51).

**Discrepancies / tensions vs the manuscript (flagged above):**
1. The reported incision generalisation AUC (0.917) is the leakage-contaminated value; the leakage-controlled value (0.677, CI includes 0.5) is not used as primary — contradicts the "honest evaluation" claim (Findings 2, 3).
2. "Substantial heterogeneity" label vs median I² ≈ 39% (low-to-moderate) at effective K = 5 (Finding 4).
3. OXPHOS is significant under fixed effects (q = 0.020) but the abstract foregrounds the random-effects q = 0.31; CPSP-literature set also significant (q = 0.021) — qualifies the "ion channels unchanged" framing (Finding 7).
4. GSE265957 contributes 2× the single-study variance weight in the 6-input primary; RE heterogeneity rests on the non-independent pair (Findings 1, 5).
5. Manual 2-proportion p = 0.30 differs from the permutation p = 0.14 — both non-significant; the manuscript's "−0.9 pp, p = 0.14" could be misread as a 2-proportion result, though the permutation it actually uses is the correct test (Finding note in § Stands up).

No contradiction was found in the arithmetic of the core counts, the BH implementation, the heterogeneity point estimates, or the non-circular proportions — those are sound and reproducible. The concerns are about **design choices** (independence, primary-vs-sensitivity status of the leaky AUC, interpretation framing, and small-K stability), not arithmetic errors.
