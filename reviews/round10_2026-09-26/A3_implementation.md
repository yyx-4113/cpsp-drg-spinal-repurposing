# A3 — Implementation / Provenance Audit (independent, first-submission stance)

**Reviewer:** A3 (implementation / provenance)
**Manuscript:** `reports/MVP_PLOSONE_submission.md` (333 lines) + `MVP_PLOSONE_supplementary.md`, `MVP_STROBE_checklist.md`, `MVP_PLOSONE_cover_letter.md`, `MVP_PLOSONE_compliance_check.md`
**Venue:** PLOS ONE (resubmission)
**Independence statement:** I read only the manuscript bundle, `scripts/`, `results/tables/`, `data/processed/`, `README.md`, `PROJECT_PLAN.md`, `.gitignore` and git object history. I did not read `reviews/REVIEW_*.md`, `reviews/RESPONSE_*.md`, any `reviews/round2_*`…`round9_*` content, `.workbuddy/memory/**`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, or A1/A2 output. I did not run `scripts/p7_renumber_refs.py` or `scripts/resolve_ref_dois.py`. I did not modify the manuscript or any file under `results/tables/`; all probe output went to `_scratch/`.

---

## 0. Bottom line

The meta-analysis, gene-set, docking, single-cell/spatial, miRNA and reference layers are **numerically traceable and almost entirely reproducible** — I recomputed every headline number that has a file behind it, and 40+ of them match to the printed precision. The exception is the **hub / docking-target-set bootstrap**, which is the load-bearing evidence for the paper's "bounded stability" and "structurally determined target list" claims. Both bootstrap scripts contain **two independent implementation defects** that together reduce the three-method consensus to `RandomForest ∩ (XGBoost trained on misaligned data)`. I reproduced both defects and their correction: correcting the XGBoost index alignment alone raises mean recovery of the 17 dock-eligible hubs from **0.79 → 7.84** and P(≥3 of 17) from **0.040 → 1.000**. The published instability is an artefact, not a finding.

Separately, the **Data Availability statement's central reproducibility claim is false as written**: the cited tag `v1.0.0` (commit `5cfa2fb`, 2026-09-19) contains **none** of the six Round-4 artefacts the manuscript says it "already contains", and the current `HEAD` (`c792a1a`, 2026-09-26) still carries the **superseded bulk-only numbers (1,981 / 1,732 / 42.7%)** the manuscript explicitly disowns, plus an **uncorrected Visium table in which all 35 hubs are flagged `present=True`** (versus the paper's 33/35). A synthetic self-test copy of `P6_reverse_control.csv` (ADRA2A AUC 0.968, 400 ligands) is **tracked in git** under `results/tables/_synthetic_selftest_DO_NOT_USE/` and is not excluded by `.gitignore`.

---

## 1. Major findings

### F1 (Major) — XGBoost is trained on the **un-resampled** feature matrix with **resampled** labels: the entire hub/target-set stability result is an artefact

**【Problem】** In both bootstrap scripts the XGBoost selector is fit as `fit(Xp, yb)` where `Xp` is the full 72×800 matrix in original row order and `yb = yall[idx]` is the bootstrapped label vector, so sample *i*'s feature row is paired with sample *idx[i]*'s label.

**【Evidence】**
- `scripts/p3_hub_bootstrap.py:81-89`: `Xb=Xp[idx]; yb=yall[idx]; Xbs=StandardScaler().fit_transform(Xb)` … then line 85 `clf=xgb.XGBClassifier(...).fit(Xp,yb)` and line 86 `sv=clf.get_booster().predict(xgb.DMatrix(Xp),pred_contribs=True)`. The Random Forest on line 83 correctly uses `(Xbs, yb)`; XGBoost does not.
- `scripts/p7_targetset_bootstrap.py:105-113`: identical pattern — RF on `Xbs`, XGBoost on `Xp` with `yb`, SHAP evaluated on `Xp`.
- Diagnostic in the published artefact: `results/tables/P3_hub_bootstrap.csv` shows `rf_freq` mean ≈ 0.60 but `xgb_freq` mean ≈ **0.086**, i.e. indistinguishable from the 80/800 = **0.100** chance expectation for a random top-80 draw, while RF is 6× above chance. A correctly paired XGBoost must co-select with RF, not behave like a random draw.
- **Reproduction (my probe, `_scratch/a3_bootstrap_probe.py`, B=100, SEED=42, same POOL=800, same C_min=8.53168, output `_scratch/a3_bootstrap_probe.json`; nothing written to `results/tables/`).** The "published_bug" variant reproduces the published table almost exactly (median size 6, IQR 5–8, median Jaccard 0.026, P(≥3 of 17) = 0.040), which validates that the probe is faithful. The "index_aligned_fix" variant changes only line 85-86 to `fit(Xbs, yb)` / `DMatrix(Xbs)`:

| Quantity | Published (buggy) B=200 | My B=100 buggy repro | My B=100 index-aligned fix |
|---|---|---|---|
| mean XGB selection freq over the 35 hubs | 0.086 (from CSV) | 0.080 | **0.714** |
| mean RF selection freq | 0.597 | 0.597 | 0.597 (unchanged) |
| hub_freq median (min–max) | — (per-gene 0.005–0.155) | 0.040 (0.000–0.110) | **0.400 (0.090–1.000)** |
| hubs with hub_freq ≥ 0.9 | 0/35 | 0/35 | **1/35** |
| resampled hub-set size, median [IQR] | 6 [5–8] | 6 [5–8] | **36 [33–38]** |
| median Jaccard vs published 35 | 0.026 | 0.026 | **0.296** |
| mean dock-eligible (17) recovered | 0.79 | 0.75 | **7.84** |
| P(≥3 of 17) | 0.040 | 0.040 | **1.000** |
| P(≥5 of 17) | 0.000 | 0.000 | **0.990** |
| mean actually-docked (9) recovered | 0.35 | 0.31 | **3.28** |
| P(≥3 of 9) | 0.005 | 0.000 | **0.650** |

(Note: the fix variant still retains the LASSO defect of F2, so true stability is *higher* still.)

**【Why it matters】** Three load-bearing sentences become unsupported: (i) Results line 66 "resampled hub sets had a median size of 6 genes (IQR 5–8) and a median Jaccard overlap of 0.026"; (ii) Results line 114 / Supplementary S7 reading "The docking target set is **not statistically reproducible** … The docking target list is therefore justified by **structural tractability, not by statistical stability**"; (iii) the cover letter's selling point "a bootstrap shows the docking target set is not statistically reproducible (median 1 of 17 dock-eligible hubs recovered per resample)". Because the honest-null framing leans on "we bounded our own stability", publishing a stability bound that is a coding artefact is worse than publishing none: it manufactures false humility about a target list that is in fact ~10× more reproducible than reported, and a competent reader who re-runs the deposited script with the bug fixed will obtain the opposite conclusion and will say so.

**【Specific fix】** Fix the pairing in both scripts and re-run; do **not** merely annotate.
- `scripts/p3_hub_bootstrap.py`, replace lines 85-86 with:
  ```python
  clf = xgb.XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, subsample=0.8,
                          colsample_bytree=0.5, reg_lambda=2.0, eval_metric="logloss",
                          random_state=SEED + b, n_jobs=-1).fit(Xbs, yb)
  sv = clf.get_booster().predict(xgb.DMatrix(Xbs), pred_contribs=True)[:, :-1]
  ```
- `scripts/p7_targetset_bootstrap.py`, replace lines 110-113 with:
  ```python
  clf = xgb.XGBClassifier(n_estimators=200, max_depth=3, learning_rate=0.05, subsample=0.8,
                          colsample_bytree=0.5, reg_lambda=2.0, eval_metric="logloss",
                          random_state=SEED + b, n_jobs=-1).fit(Xbs, yb)
  sv = clf.get_booster().predict(xgb.DMatrix(Xbs), pred_contribs=True)[:, :-1]
  ```
- Add a regression guard after each fit: `assert X_fit.shape[0] == len(yb) and np.array_equal(clf.classes_, np.unique(yb))`, and log per-resample `xgb_top ∩ rf_top` size; if it stays near the chance value 8 (80×80/800) the alignment has regressed.
- Re-run B=200 and rewrite: `P3_hub_bootstrap.csv`, `_R4_targetset_bootstrap.csv/.json/_resamples.csv`, Supplementary Table S7 Panels A–B, Results lines 66 and 114, and the cover letter paragraph (ii). Paste-ready replacement for the Results sentence, once the new numbers are in hand:
  > "A 200-resample bootstrap of the 72 pooled samples (`P3_hub_bootstrap.csv`) showed that per-gene hub recovery ranged X%–Y%, with Z/35 hubs reaching the ≥0.9 stability threshold; under the same resampling the docking target set recovered a mean of A of the 17 dock-eligible hubs (median B; P(≥3 of 17) = C), so the 35-gene set is reported as a candidate set whose membership—but not whose neuroimmune identity—is resampling-sensitive."

---

### F2 (Major) — LASSO contributes **zero votes by construction** (integer indices vs gene-symbol sets); the manuscript's "LASSO makes no selections" is factually wrong

**【Problem】** `lasso_nonzero()` returns a set of **integer column indices**, which is then tested against / merged with **gene-symbol string sets**, so the LASSO route can never cast a vote. The manuscript attributes this to LASSO weakness; it is a type bug.

**【Evidence】**
- `scripts/p3_hub_bootstrap.py:69-71` returns `set(np.where(np.abs(lr.coef_[0])>1e-8)[0])` (ints); line 94 tests `if g in lnz` where `g` is a symbol string → always `False`. Hence `lasso_freq = 0.000` for all 35 hubs in `P3_hub_bootstrap.csv`.
- `scripts/p7_targetset_bootstrap.py:87-89` same return; line 117 `for s_ in (lnz, rftop, xgbtop)` adds integer keys to `votes`; line 119 requires `v >= 2`, and an integer key can only ever receive one vote → LASSO contributes nothing.
- **LASSO is not silent.** My probe recorded `len(lnz)` per resample: mean **37.7**, max **60** nonzero coefficients out of 800 at `C_min = 8.53168` (the λ.min value from `p3_ml.py:96-98`, printed in `scripts/p3_ml.out` as "lambda.min C=8.53168->45g"). Also `scripts/p3_ml.out` reports "[LASSO] bootstrap stable(>=0.6)=13" and `P3_hub_genes.csv` shows `lasso_freq` = 0.96 / 0.85 / 0.79 / 0.78 / 0.62 for SPRR1A / ATF3 / CDHR5 / GALNS / TFE3 — the LASSO route *does* drive the five three-method hubs.

**【Why it matters】** Results line 66 states "with LASSO contributing no selections under resampling (the effective consensus reduced to Random-Forest∩XGBoost agreement)". LASSO selects ~38 of 800 genes per resample; what is true is only that it selected none of the 35 published hubs, and that is caused by the type bug, not by data. Under the current code the "≥2/3 methods" rule silently degrades to a **two-method** rule, so the manuscript's headline hub definition ("dual-ML consensus … ≥2/3") does not describe the artefact that produced the stability numbers.

**【Specific fix】** Return symbols, not indices, and re-run:
```python
def lasso_nonzero_symbols(X, y, C, columns):
    lr = LogisticRegression(penalty="l1", solver="liblinear", C=C, max_iter=5000).fit(X, y)
    return set(np.array(columns)[np.abs(lr.coef_[0]) > 1e-8])
```
- `scripts/p3_hub_bootstrap.py`: replace line 71 with `return set(np.array(POOL)[np.where(np.abs(lr.coef_[0])>1e-8)[0]])` (POOL is in scope) — i.e. `lnz = lasso_nonzero(Xbs, yb, C_min)` already returns symbols; no other change needed at line 94.
- `scripts/p7_targetset_bootstrap.py`: same one-line change at line 89.
- Add `assert all(isinstance(g, str) for g in lnz)` immediately after the call.
- Paste-ready replacement for the Results clause:
  > "LASSO (λ.min, C = 8.53) selected a mean of 37.7 of the 800 pool genes per resample but none of the 35 published hubs, so under resampling the consensus effectively reduced to Random-Forest∩XGBoost agreement; the sparse-linear route is reported as non-contributing to hub membership at this λ, and λ.1se selected only 1 gene."

---

### F3 (Major) — The Data Availability statement's repository claim is false; the cited tag predates every artefact it names, and `HEAD` still carries superseded numbers

**【Problem】** The manuscript (line 267) and cover letter (line 13) assert that the public repository at tag `v1.0.0` "already contains all processed data", naming six Round-4 artefacts. None of them exists at that tag, and two of the numbers shipped at `HEAD` contradict the manuscript.

**【Evidence】**
- `git rev-parse v1.0.0` → `5cfa2fb` ("Add Zenodo deposit metadata", 2026-09-19); `git rev-parse HEAD` → `c792a1a` (2026-09-26). `git ls-tree v1.0.0 results/tables/ | grep -E "_R4|bulkonly"` returns **empty**. The manuscript's named files — `META_bulkonly_sensitivity_summary.json`, `META_bulkonly_meta.csv`, `P6_target_plausibility.json`, `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_meta.csv`, `_R4_targetset_bootstrap*.csv` — were all added after the tag.
- `git show HEAD:results/tables/META_bulkonly_sensitivity_summary.json` → `bulk_only_core_size = 1981`, `overlap = 1732`, `overlap_pct_primary = 42.713`. The manuscript (lines 50, 152, Table 1a) reports **2,512 / 2,202 / 54.3%** and explicitly writes "An earlier, more restrictive all-four-present count of 1,981 is superseded". The corrected values exist **only in the uncommitted working tree** (`git status` → ` M results/tables/META_bulkonly_sensitivity_summary.json`).
- `git show HEAD:results/tables/P5_GSE325938_hub_regionalization.csv` → `present=True` for **35/35** hubs; the working-tree file (and the manuscript, lines 78, 295; Supplementary S2) say CRISP3 and LNP1 are below detection → **33/35**, and the abstract's "17/33 hubs in the dorsal horn" depends on it. A reader using the deposited file computes 17/35 = 48.6%, not 51.5%.
- Also uncommitted: `reports/MVP_PLOSONE_submission.md` (renamed, 260-line diff), `reports/MVP_PLOSONE_supplementary.md`, `reports/MVP_PLOSONE_cover_letter.md`, `scripts/p7_consistency_gate.py`, `scripts/gate_consistency.py`.

**【Why it matters】** PLOS ONE's data-availability policy is assessed against the deposited artefact, not the author's working directory. As submitted, a reviewer or reader who clones the cited tag cannot obtain the random-effects core (1,008), the non-circular translation test (46.2%), the set-level BH q-values (0.020 / 0.31), the bulk-only sensitivity (2,512 / 54.3%), or the target-set bootstrap — i.e. **every number the cover letter calls the paper's rigour contribution**. Worse, what they *can* obtain (1,981 / 42.7%; 35/35 present) directly contradicts the text. This is a desk-reject-grade availability defect if not fixed before upload.

**【Specific fix】**
1. Commit all working-tree changes under `results/`, `reports/` and `scripts/`; create a new tag (e.g. `v1.1.0`) **after** the commit; update both occurrences of `v1.0.0` (manuscript line 267; cover letter line 13) to the new tag.
2. Add a pre-deposit gate asserting repository state, e.g. in `scripts/gate_consistency.py`:
   ```python
   j = json.load(open("results/tables/META_bulkonly_sensitivity_summary.json"))
   chk("bulk-only core", j["bulk_only_core_size"], "2512")
   reg = pd.read_csv("results/tables/P5_GSE325938_hub_regionalization.csv")
   chk("Visium present hubs", int(reg.present.sum()), "33")
   ```
   (`chk("bulk-only core", …, "2,512")` at `scripts/p7_consistency_gate.py:154` already exists — it passes only against the uncommitted file.)
3. Paste-ready replacement for the Data Availability sentence, to be used only after step 1:
   > "All code, tables and figures are deposited in the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing at tag **v1.1.0** (README + CITATION.cff + MIT LICENSE + reproduction scripts). The repository contains all processed data cited in this manuscript, including `META_bulkonly_sensitivity_summary.json` (bulk-only core 2,512; overlap 2,202/4,055), `P5_GSE325938_hub_regionalization.csv` (33/35 hubs detectably expressed), the random-effects and non-circular translation outputs `_R4_random_effects_meta.csv` and `_R4_nerveinjury_only_meta.csv`, and the target-set bootstrap `_R4_targetset_bootstrap.csv` with its per-resample recovery sets `_R4_targetset_bootstrap_resamples.csv`."

---

### F4 (Major) — A synthetic self-test copy of the docking outputs is tracked in git under `results/tables/` with the same filenames as the real ones

**【Problem】** `results/tables/_synthetic_selftest_DO_NOT_USE/` contains synthetic versions of `P6_docking_scores_merged.csv`, `P6_reverse_control.csv`, `P6_ranking_drugs.csv`, `P6_ranking_pairs.csv`, `P6_docking_scores_merged_by_tag.csv` and `P6_docking_scores__selftest.csv`; all six are **tracked** (`git ls-files` confirms) and `.gitignore` contains no rule excluding them.

**【Evidence】**
- `results/tables/_synthetic_selftest_DO_NOT_USE/P6_reverse_control.csv`: 10 rows, `n_ligands = 400` for every target, and **ADRA2A `auc_known_vs_rest = 0.967829`, `reliable = True`** — versus the real `results/tables/P6_reverse_control.csv` (ADRA2A n_ligands 3,070, AUC **0.532**, `reliable = False`). The synthetic file is built on a 400-ligand toy library, not the 3,085-drug ChEMBL library.
- `git ls-files results/tables/_synthetic_selftest_DO_NOT_USE/` lists all six files.
- `.gitignore` has no `_synthetic_selftest_DO_NOT_USE` or `_archive` entry, while the Data Availability statement declares the whole `results/` tree public.

**【Why it matters】** The paper's central result is "ADRA2A does not enrich (0.532, p = 0.118)". A reader who resolves `P6_reverse_control.csv` and lands on the synthetic copy finds ADRA2A at AUC 0.968 with 400 ligands — a number that reverses the honest null and is present in the public deposit under a filename identical to the real artefact. Even if the directory name warns, filename collision inside a declared "processed data" tree is a provenance hazard, and it is exactly the kind of thing that produces a post-publication correction.

**【Specific fix】** Move the directory out of `results/` entirely (e.g. `tools/_selftest/`), or delete it; and add to `.gitignore`:
```
results/tables/_synthetic_selftest_DO_NOT_USE/
results/tables/_archive/
```
Then `git rm -r --cached results/tables/_synthetic_selftest_DO_NOT_USE`. Paste-ready note for the Data Availability statement:
> "The `results/tables/` tree contains only artefacts generated from the 12 GEO accessions; synthetic self-test fixtures are not included."

---

## 2. Minor findings

### F5 (Minor) — The manuscript cites `results/tables/_R4_translation_noncircular.csv`, which no longer exists at that path

**【Problem】** Two documents cite a table that has been moved to `results/tables/_archive/`.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:58` ("…that appears in the exploratory `_R4_translation_noncircular.csv`…") and `reports/MVP_PLOSONE_supplementary.md:212` (listed as a source for Panel B). `results/tables/` contains only `_R4_translation_noncircular.json`; `git status` shows ` D results/tables/_R4_translation_noncircular.csv`.

**【Why it matters】** The sentence that disclaims the superseded 14,445 / 3,564 gene universe points at a file a reader cannot open; the disclaimer becomes unverifiable, and the reader cannot check which universe was superseded.

**【Specific fix】** Replace the citation with `results/tables/_archive/_R4_translation_noncircular.csv` (and in Supplementary line 212), or delete the reference and cite only `_R4_translation_noncircular.json`:
> "The marginally larger 14,445 / 3,564 gene universe computed in the earlier exploratory merge (`results/tables/_archive/_R4_translation_noncircular.csv`, superseded) is not used; all concordance statistics below use the 14,390 / 3,556 universe of `_R4_nerveinjury_only_summary.json`."

---

### F6 (Minor) — "53.8% (2,318/4,306)" is taken from the artefact the manuscript itself declares superseded

**【Problem】** The non-circular section's intermediate number comes from `_R4_translation_noncircular.json`, whose universe (14,445 / 3,564) the same paragraph disowns, and whose stratum key `meta_FDR05_NIcons_ge08` still uses the six-contrast (incision-containing) meta FDR.

**【Evidence】** `_R4_translation_noncircular.json` → `strata.meta_FDR05_NIcons_ge08 = {k: 2318, n: 4306, rate: 0.5383, ci: [0.5234, 0.5532], perm_p: 0.7866}`, and `strata.all_measured = {k: 7751, n: 14445, rate: 0.5366}`. `_R4_nerveinjury_only_summary.json` (the declared authoritative source) has no 2,318/4,306 stratum: its strata are 6,779/14,390; 3,329/7,274; 2,266/4,899; 978/2,185; 1,277/2,805.

**【Why it matters】** The manuscript reports 53.8% inside the paragraph whose stated purpose is to eliminate circularity, but that stratum's significance filter is still the incision-containing six-contrast FDR — it is only partially de-circularised. Reporting it without that qualifier overstates how clean the intermediate step is, and it mixes two gene universes (14,390 vs 14,445) inside one paragraph.

**【Specific fix】** Either drop the number or label it. Paste-ready:
> "Restricting consistency to the nerve-injury contrasts, but still using the six-contrast (incision-containing) meta FDR, gives 53.8% (2,318/4,306; 95% CI 52.3–55.3%); because that stratum is only partially de-circularised and is computed on the earlier 14,445-gene merge, it is reported as an intermediate step only, and the fully non-circular 46.2% (2,266/4,899) below is the result we rely on."

---

### F7 (Minor) — The CIs are bootstrap percentile intervals, not DeLong; and the two LODO implementations preprocess differently

**【Problem】** The manuscript calls the AUC intervals "DeLong" three times; the code computes percentile bootstrap CIs, and the leakage-controlled script additionally re-fits the scaler on the held-out fold.

**【Evidence】**
- `scripts/p3_finalize.py:66-71` — 3,000 bootstrap resamples, `np.percentile(bs,[2.5,97.5])`; this produces `P3_lodo_auc_ci.csv`. `scripts/p3_ml_leakage_controlled.py:76-89` — function is literally named `delong_bootstrap_ci` but the body is a 2,000-draw percentile bootstrap ("Bootstrap CI for AUC (robust at small n)"); this produces `P3_lodo_auc_ci_leakage_controlled.csv`.
- Manuscript line 64 "Four of the five leakage-controlled folds have degenerate **DeLong** intervals ([1.0, 1.0]) … because the **DeLong variance** collapses at small test n"; line 158 and the Fig 2 legend repeat "DeLong".
- `scripts/p3_ml_leakage_controlled.py:133` `Xte_s = StandardScaler().fit_transform(Xte[:,[si[g] for g in sel]])` — the test fold is standardised with **its own** mean/SD, whereas `scripts/p3_finalize.py:65` correctly applies the training scaler (`sc.transform(Xte)`).

**【Why it matters】** Method mislabelling is checkable and erodes trust in the statistics section; more substantively, refitting the scaler on a 6- or 9-sample held-out fold makes the test-side scores depend on held-out data and is inconsistent with the raw LODO it is meant to correct, so the two AUC tables are not strictly comparable.

**【Specific fix】** (a) Replace every "DeLong" with "bootstrap": paste-ready for line 64 —
> "Four of the five leakage-controlled folds yield degenerate bootstrap intervals ([1.0, 1.0]); only the incision fold yields an estimable interval. Intervals are 2,000-draw percentile bootstraps of the held-out AUC (`scripts/p3_ml_leakage_controlled.py`), not DeLong intervals, and at AUC = 1.0 and n = 6–9 the bootstrap distribution is degenerate, so those folds are reported as descriptive only."
(b) `scripts/p3_ml_leakage_controlled.py:133` → `Xte_s = sc.transform(Xte[:, [si[g] for g in sel]])` where `sc` is the `StandardScaler` fitted on line 132; re-run and refresh `P3_lodo_auc_ci_leakage_controlled.csv` and the 0.677 [0.374, 0.940] value if it moves.

---

### F8 (Minor) — The leakage-controlled LODO evaluates a *union* rule (139–164 genes), not the published ≥2/3 hub consensus (35 genes)

**【Problem】** The headline "hub classifier" and the leakage-controlled classifier are different models; the manuscript presents them as one.

**【Evidence】** `scripts/p3_ml_leakage_controlled.py:116` `sel = lasso_set | rf_set | xgb_set` (union), giving `n_selected` = 164 / 142 / 139 / 150 / 158 in `P3_lodo_auc_ci_leakage_controlled.csv`; the published hub rule is `≥2/3` (`scripts/p3_ml.py:128-131`) and yields 35 genes (`P3_ml_metrics.csv` `n_genes = 35`). Also line 115 fits XGBoost on the **full 13,208-gene** training matrix (`Xtr`, index `POOL_LOCAL`) while RF is fitted on the 800-gene pre-filter (`Xs`, index `pre`) — the three selectors are not even applied to the same feature space.

**【Why it matters】** A reader reproducing "the leakage-controlled LODO of the hub classifier" from `P3_hub_genes.csv` will not get 0.677 [0.374, 0.940]; the number belongs to a ~142-feature union model. The methodological claim "feature selection recomputed out-of-fold" is true but incomplete, and the manuscript's central generalisation number inherits an undocumented model change.

**【Specific fix】** Add one sentence to Methods line 158 (paste-ready):
> "Within each training fold the three selectors were recomputed and their selections combined by **union** (LASSO ∪ RF-top-80 ∪ XGBoost-top-80; 139–164 features per fold), which is deliberately more permissive than the published ≥2/3 consensus rule used to define the 35-hub candidate list; the leakage-controlled LODO therefore bounds the generalisation of the *selection pipeline*, not of the 35-gene list itself, and XGBoost in this script was fitted on the full 13,208-gene training matrix using gain importance rather than SHAP."

---

### F9 (Minor) — Two gene-set artefacts disagree and the manuscript silently quotes both

**【Problem】** `P3_geneset_stats.csv` (older) and `_R4_geneset_setlevel_bh.csv` (current, source of the q-values) give different permutation p for the same sets; the manuscript's body uses the older file's value for P2RX/P2RY while the q-values come from the newer one.

**【Evidence】** P2RX_P2RY perm p: `P3_geneset_stats.csv` = **0.4398** → manuscript line 84 "p = 0.440"; `_R4_geneset_setlevel_bh.csv` = **0.438281** (q = 0.773613). Same divergence for OXPHOS (0.003998 vs 0.004498), Nav_SCN (0.179910 vs 0.172414), Synaptic (0.111944 vs 0.105947), Myelin_OL (0.524238 vs 0.644678). Additionally `P3_geneset_stats.csv` reports Sigma1 mean_Z 2.0629 / n_present 1 whereas the set-level file leaves Sigma1 fixed-scale NaN; Myelin_OL n_present is 13 vs 14. Fig 1's legend (line 286) cites both files as sources.

**【Why it matters】** Two "authoritative" CSVs in the same deposit disagree at the third decimal for the same statistic, and one of them is used for a claim the reader will try to reproduce. It also means the permutation run is not seeded reproducibly across the two scripts.

**【Specific fix】** Declare `_R4_geneset_setlevel_bh.csv` the single source, regenerate `P3_geneset_stats.csv` from the same seeded run (add `np.random.default_rng(SEED)` and record `SEED` in both outputs), and change every body citation to the q-value file. Paste-ready for line 84:
> "In the present meta-analysis the purinergic family was itself negative: P2RX/P2RY showed no coordinate change (permutation p = 0.438 in the six-input meta, set-level BH q = 0.774; p = 0.339 in the bulk-only meta)."

---

### F10 (Minor) — STROBE checklist mislabels ADRA2A's Tier-1 AUC as 0.532 (Tier-1 is 0.618)

**【Problem】** A submitted Supporting Information file states the opposite of the paper's central "breadth flip" result.

**【Evidence】** `reports/MVP_STROBE_checklist.md:26`: "full-library docking null (**ADRA2A Tier-1 AUC 0.532**, p = 0.118 NS)". `P6_breadth_chembl_power.csv` gives Tier-1 (`t1_only`, n = 620) AUC **0.618368** and full-library (`full_library`, n = 3,070) AUC **0.532465**, p = 0.118409. The manuscript body (lines 112, 134, 298) correctly says 0.618 → 0.532.

**【Why it matters】** STROBE item 16 is the "main results" item; a checklist that reports the Tier-1 figure as the null value inverts the breadth-flip finding in a file that goes to the editor and is indexed as Supporting Information.

**【Specific fix】** `reports/MVP_STROBE_checklist.md:26` — replace with:
> "| 16 | **Main results** | Addressed. Results (lines 42–52): coordinated neuroimmune/DAM/complement↑ and OXPHOS↓; 35 hubs; full-library docking null (ADRA2A Tier-1 AUC 0.618 collapsing to full-library AUC 0.532, p = 0.118, NS). Bulk-only sensitivity (lines 44, 140, 249). |"

---

### F11 (Minor) — STROBE line-number pointers are stale against the 333-line manuscript

**【Problem】** The checklist's evidence column points to line numbers of an earlier version.

**【Evidence】** `MVP_STROBE_checklist.md:34` says "(Ethics statement, line 164)"; in `reports/MVP_PLOSONE_submission.md` line 164 is the single-cell Methods paragraph and the "### Ethics statement" heading is at **line 176**. Item 15 cites "lines 249, 262" and item 16 "lines 42–52"; the Results block runs lines 40–114 and no line 249 exists in the Results.

**【Why it matters】** Every "Addressed" verdict in the checklist is unverifiable by the editor, which voids the purpose of supplying the checklist.

**【Specific fix】** Regenerate the pointer column from the current file, or replace line pointers with section names. Paste-ready for item 19/21-style entries: "Addressed — see Methods, 'Statistical discipline, causal scope and AI-use disclosure' and 'Ethics statement' sections."

---

### F12 (Minor) — Compliance document is stale in four places relative to the manuscript it certifies

**【Problem】** `MVP_PLOSONE_compliance_check.md` states reference numbers, quoted sentences and a filename that do not match the manuscript.

**【Evidence】**
- §3.1 (lines 47-50): "**34.** Bertoch … **35.** Yin … **36.** Cooper …" — in the actual reference list Bertoch is **23**, Yin is **11**, Cooper is **12** (the doc describes a pre-renumbering state).
- §3.1 line 50: title given as "Peripheral nerve injury results **at** a biased loss…"; the manuscript (ref 12) and the real title use "results **in**".
- §15 line 27: quotes the AI-use sentence as "A large language model (LLM) was used to assist manuscript drafting and language polishing"; the manuscript (line 173) reads "A generative AI language model (**Claude, Anthropic**) was used to assist manuscript drafting and language polishing." PLOS ONE asks the tool to be named; the compliance doc certifies the un-named version. The cover letter (line 15) likewise says only "A large language model assisted language drafting".
- §18 line 30 and §4 line 66: STROBE file given as `reports/MVP_PLOSONE_STROBE_checklist.md` and Supporting Information as "S1…S8"; the file on disk is `reports/MVP_STROBE_checklist.md`, and the manuscript (lines 277, 332) enumerates S1–S7 with STROBE as an un-numbered separate file.
- §11 line 23 quotes Funding as "The author received no specific funding for this work."; the manuscript (line 261) reads "The author received no financial support for this work." plus a pending-grant sentence the quote omits.
- §1 item 3: "180 words"; the abstract is **214** words (still ≤300, so the verdict stands, the number does not).

**【Why it matters】** The compliance document is an internal certification; if it certifies text that is not in the manuscript (AI disclosure especially), it cannot be used as evidence of compliance and may cause the author to upload a manuscript whose disclosure differs from what was checked.

**【Specific fix】** Regenerate §3.1 from the live reference list (Bertoch = 23, Yin = 11, Cooper = 12; correct "results at" → "results in"); replace the §15 quote with the manuscript's exact sentence including "(Claude, Anthropic)"; replace `MVP_PLOSONE_STROBE_checklist.md` with `MVP_STROBE_checklist.md` and "S1…S8" with "S1–S7 plus the STROBE checklist as a separate file"; correct the Funding quote to the manuscript's two sentences; change "180 words" to "214 words".

---

### F13 (Minor) — Supplementary Table S5b has a duplicated Sigma1 row (20 rows for 19 sets)

**【Problem】** The set-level BH table lists Sigma1 twice, so the row count contradicts its own header.

**【Evidence】** `reports/MVP_PLOSONE_supplementary.md:190-191` both read `| Sigma1 | 1 | — | **—** | — | — | no |`. The table states "18 multi-member sets" + Sigma1 = 19 rows.

**【Why it matters】** A duplicated row in the table that carries the paper's set-level q-values invites the reader to suspect other rows are also duplicated or mis-aligned; PLOS production will query it.

**【Specific fix】** Delete line 191. If the table is generated programmatically, add `df = df.drop_duplicates(subset=["set"])` before rendering, or assert `len(df) == 19`.

---

### F14 (Minor) — Supplementary S5 mis-attributes reference 20 to *Nature Medicine*; reference 20 is *Nature*

**【Problem】** The journal name for the Tsuda P2X4 citation is wrong in the supplementary provenance column.

**【Evidence】** `reports/MVP_PLOSONE_supplementary.md:153` — "microglial P2X4 implicated in neuropathic pain (Tsuda et al., **Nat Med** 2003)". The manuscript's reference 20 (line 223) is "Tsuda, M. et al. P2X4 receptors induced in spinal microglia gate tactile allodynia after nerve injury. ***Nature*** **424**, 778–783 (2003). https://doi.org/10.1038/nature01786". The correct journal is *Nature*.

**【Why it matters】** PLOS ONE requires full, correct journal names; an abbreviated *and* incorrect journal name in a submitted table is a copy-editing flag and a citation-integrity flag.

**【Specific fix】** `reports/MVP_PLOSONE_supplementary.md:153` — replace "(Tsuda et al., Nat Med 2003)" with "(Tsuda et al., *Nature* 424:778–783, 2003; reference 20)".

---

### F15 (Minor) — The same 46.2% interval is printed as 44.9–47.7% in the manuscript and 44.9–47.6% in the supplementary

**【Problem】** A rounding divergence for one confidence limit between two submitted documents.

**【Evidence】** `_R4_nerveinjury_only_summary.json` → `NI_FDR05_AND_NIcons>=0.8.ci = [0.4486, 0.4765]`. Manuscript line 58 prints "95% CI 44.9–**47.7**%"; `reports/MVP_PLOSONE_supplementary.md:220` prints "44.9–**47.6**%". (0.4765 → 47.65%, which rounds to 47.6 or 47.7 depending on convention.)

**【Why it matters】** Two submitted documents give different intervals for the paper's single most-quoted statistic (it appears in the abstract, Results, Discussion, Conclusions and cover letter). A reviewer comparing them will question which is authoritative.

**【Specific fix】** Print more precision rather than choosing a convention. Paste-ready for both locations:
> "46.2% (2,266/4,899; 95% CI 44.9–47.7%)" → "46.25% (2,266/4,899; Wilson 95% CI 44.86–47.65%)"

---

### F16 (Minor) — `bulk_consist` in the bulk-only JSON uses a different definition from `consistency` in the bulk-only CSV

**【Problem】** Same-sounding field, different quantity, in two files the reader will use together to rebuild Table 1b.

**【Evidence】** `META_bulkonly_sensitivity_summary.json` → `scn_tab.SCN9A.bulk_consist = 0.25` (also SCN10A/11A/8A = 0.25). `META_bulkonly_meta.csv` → SCN9A `consistency = 0.75` (`n_up = 1`, `K = 4`; max(n_up, n_dn)/K = 3/4). The JSON value equals the fraction agreeing with the sign of the bulk meta Z (1/4), not the manuscript's stated definition "max(n_up, n_dn)/K".

**【Why it matters】** Table 1b's source note (line 313) points at both files. A reader validating Table 1b will find a "consistency" of 0.25 where the Methods say consistency is 0.75 and conclude the SCN direction claim is weakly supported.

**【Specific fix】** Rename the JSON field to `frac_agreeing_with_bulk_metaZ` (or emit both) and add one line to the Table 1b source note:
> "Source: `results/tables/META_bulkonly_meta.csv` (`consistency` = max(n_up, n_dn)/K = 0.75 for all four SCN genes) and `META_bulkonly_sensitivity_summary.json` (`bulk_consist` = fraction of contrasts agreeing in sign with the bulk meta Z = 0.25; a different quantity)."

---

### F17 (Minor) — Orphan and divergent duplicate artefacts in `results/tables/`

**【Problem】** Files that nothing reads, byte-identical duplicates, and `_QC_*` copies that disagree with their `P6_*` counterparts.

**【Evidence】**
- `META_collapse_meta.csv` and `P2_meta_sensitivity.csv` are **byte-identical** (189 bytes, same 8 rows) and neither is cited.
- `_QC_breadth_target_summary.csv` differs from `P6_breadth_target_summary.csv` on the ADRA2A row: `n_scored` **620** vs **3,070**, `n_t2` **0** vs **2,450**, `median_affinity` −7.127 vs −7.5055, `rank_by_depth9` 5 vs 3. `_QC_breadth_target_rank_stability.csv` puts ADRA2A `delta` at **0.0** vs **−0.379**. `_QC_*` are not cited anywhere.
- 48 files in `results/tables/` are referenced by no script and no submitted document, including `DEG_GSE241361_S1R_SC__SNI_vs_Naive_WT_SC.csv` (see F18), `DEG_GSE241361_S1R_DRG__KO_vs_WT_SNI.csv`, `DEG_GSE306403_SHSY5Y__Morphine_vs_Control.csv`, the five sex/time-specific GSE278227 DEG tables, and `_R4_targetset_bootstrap_run.log`.

**【Why it matters】** Divergent near-duplicates with confusing names are where a reader (or the author, in a later revision) picks up the wrong number; the ADRA2A `n_scored = 620` QC row in particular would change the breadth-flip denominators.

**【Specific fix】** Delete `_QC_*` and `P2_meta_sensitivity.csv` (or move both sets to `results/tables/_archive/` and add `results/tables/_archive/` to `.gitignore`); keep `META_collapse_meta.csv` and cite it as the source for the collapse row of Table 1a (core 4,294, retained 3,707/4,055 = 91.4%), which currently has no cited source.

---

### F18 (Minor) — No spinal-cord contrast enters the "DRG–spinal axis" meta-analysis; the spinal bulk table is orphaned

**【Problem】** The meta-analysis input list is DRG-only, yet the title, abstract and Discussion frame the result as an axis.

**【Evidence】** `scripts/p2_deg_meta.py:130-136` — `primary = {GSE267799 chronic_vs_baseline, GSE212311 CCI_vs_Sham, GSE278227 1W_IL_vs_CL_pooled, GSE241361_S1R_DRG SNI_vs_Naive_WT}` plus the two Xtail DRG timepoints = **six contrasts, all DRG**. The spinal-cord contrast computed at lines 103-106 (`GSE241361_S1R_SC__SNI_vs_Naive_WT_SC`) is written to `results/tables/` and then never read by any script or cited by any document. The spinal pole enters only through the ML pooling (`GSE241361_mouseSC` as one of the five datasets in `p3_ml.py:52`) and through snRNA/Visium.

**【Why it matters】** A reader can verify "five studies / six contrasts" (Methods line 144 lists exactly those, all DRG) — so the text is internally honest — but the title and the abstract's "DRG–spinal axis" promise a two-pole meta-analysis that the code does not perform. This is a claim-to-code traceability gap that a reviewer will read as over-claiming even though each individual sentence is careful.

**【Specific fix】** Add one sentence at the end of Methods "Meta-analysis" (line 144):
> "The spinal-cord arm of GSE241361 (SNI vs naive, WT) was computed as a standalone contrast (`results/tables/DEG_GSE241361_S1R_SC__SNI_vs_Naive_WT_SC.csv`) but is **not** combined into the meta-analysis: a single spinal contrast cannot be meta-combined with five DRG contrasts without conflating tissue and study effects. The axis is therefore meta-analysed at the DRG pole and cross-checked at the spinal pole by single-nucleus and spatial localisation; 'DRG–spinal axis' denotes the biological axis under study, not a two-tissue meta-analytic pooling."

---

### F19 (Minor) — `MANIFEST.sha256` is cited by two documents but is not in the deposit

**【Problem】** The integrity artefact the manuscript and cover letter point at does not exist in the tracked tree.

**【Evidence】** Manuscript line 267 "integrity verifiable via MANIFEST.sha256"; cover letter line 13 "file integrity verifiable via MANIFEST.sha256". `git ls-files | grep -i sha256` → empty; the only copy is untracked at `_manifest/MANIFEST.sha256`.

**【Why it matters】** A reproducibility claim that points at a missing file is worse than no claim; it is trivially checkable by the editor.

**【Specific fix】** Commit `MANIFEST.sha256` at the repository root covering `results/tables/**`, `scripts/*.py` and `figures/*.png`, and cite it as `MANIFEST.sha256` (root); or delete both citations.

---

### F20 (Minor) — Methods describe the LASSO route as "λ.min"; the voting route is λ.min **plus a 60% bootstrap-stability filter**

**【Problem】** The published hub definition's LASSO arm is not what the Methods say.

**【Evidence】** `scripts/p3_ml.py:106` `lasso_stable={g for g,f in lf.items() if f/B>=0.6}`; line 128 votes over `[lasso_stable, rf_top, xgb_top]`. Methods line 158 says "LASSO (λ.min, bootstrap B=100)". `scripts/p3_ml.out` reports "[LASSO] lambda.min C=8.53168->45g | lambda.1se C=0.04520->1g" and "[LASSO] bootstrap stable(>=0.6)=13" — i.e. 13 genes, not 45, enter the vote.

**【Why it matters】** The 0.6 stability threshold is a consequential, unreported choice: it is why only 5 hubs reach three-method consensus and why 30 are two-method.

**【Specific fix】** Methods line 158 — replace "LASSO (λ.min, bootstrap B=100)" with:
> "LASSO (λ.min, C = 8.53, retaining only genes selected in ≥60% of B = 100 bootstraps, n = 13 genes)"

---

### F21 (Minor) — Fig 2 legend says "three folds reach AUC 1.000" where only two cross-animal folds do

**【Problem】** An ambiguous/incorrect count in the figure legend.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:289`: "Cross-animal held-out datasets (**three folds**) reach AUC 1.000 for GSE278227 (CCI rat DRG, n = 28) and GSE212311 (CCI, n = 6), and 0.917 [0.729, 1.000] for GSE267799". `P3_lodo_auc_ci.csv`: GSE278227 1.000, GSE212311 1.000, GSE267799 0.917 — two of the three cross-animal folds are 1.000, not three.

**【Why it matters】** The legend's own sentence contradicts the table it cites, one line after it.

**【Specific fix】**
> "Of the three cross-animal held-out folds, two reach AUC 1.000 — GSE278227 (CCI rat DRG, n = 28) and GSE212311 (CCI, n = 6) — and the incision arm GSE267799 reaches 0.917 [0.729, 1.000] (n = 20), the cross-animal LODO floor."

---

### F22 (Cosmetic) — The commit that adds the per-resample audit trail is not in the deposit

**【Problem】** `_R4_targetset_bootstrap_resamples.csv` (cited by Methods line 158 and the Data Availability statement) is in the working tree but the script that writes it is uncommitted.

**【Evidence】** `git diff -- scripts/p7_targetset_bootstrap.py` shows the `resample_rows` block and the `to_csv(..._resamples.csv)` call as uncommitted additions; `git ls-tree HEAD` contains `_R4_targetset_bootstrap.csv` and `.json` but not `_resamples.csv`.

**【Why it matters】** The artefact that makes "median size 6 (IQR 5–8)", "median Jaccard 0.026" and "P(≥3 of 17) = 0.040" reproducible row-by-row is absent from the deposit.

**【Specific fix】** Commit `scripts/p7_targetset_bootstrap.py` and `results/tables/_R4_targetset_bootstrap_resamples.csv` together with F1's re-run; re-generate the file after the fix so the audit trail matches the corrected numbers.

---

### F23 (Minor) — "tibial-nerve-injury" label for GSE265957 is not supported by any artefact in the repository

**【Problem】** The manuscript's model label for GSE265957 contradicts the pipeline's own file names and the project plan.

**【Evidence】** Manuscript line 44: "one **tibial-nerve-injury** study, GSE265957"; Introduction line 36: "spanning incision, nerve-injury and **tibial-nerve-injury** models". The ingested source files are `data/processed/GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv` and `..._Day63_SNI_vs_SHM.csv` (SNI), and `PROJECT_PLAN.md:40` records GSE265957 as "**SNI/CFA 模型**". GSE241361 is likewise SNI and is not called tibial-nerve-injury.

**【Why it matters】** Model labelling is part of the external validity of the translation claim; an unsupported label that distinguishes GSE265957 from another SNI study will be queried, and it is the one study whose removal changes the core by 45.7%.

**【Specific fix】** Either justify (SNI ligates the tibial and common peroneal branches, sparing the sural) or rename. Paste-ready:
> "…because one study, GSE265957, contributes two ribosome-profiling timepoints (D4 acute and D63 chronic) from the spared-nerve-injury (SNI) model as separate inputs…"

---

## 3. § Stands up

Things I suspected, checked, and found **correct**:

1. **Fixed-effect meta numbers, exactly.** `META_DRG_axis_stouffer.csv`: 16,552 rows; 6,869 with `meta_FDR < 0.05`; 4,055 with `meta_FDR < 0.05 & consistency ≥ 0.8`; `META_DRG_axis_CORE_signature.csv` has exactly 4,055 rows. ATF3 first: `meta_Z = 10.533` → 10.53, `meta_FDR = 1.0046e-21` → 1.0e-21, `consistency = 1.00`. Weights recomputed from the deposited n: √(12·8/20) = 2.191, √(3·3/6) = 1.225, √(14·14/28) = 2.646, √(4·5/9) = 1.491, √(2·2/4) = 1.000 — all match lines 44/146 to 2 dp. Σw² = 17.52 and the 2.00/17.52 = 11.4% translatome share are arithmetically correct.
2. **Random-effects numbers, exactly.** `_R4_random_effects_meta.csv` (16,552 rows): median τ² = **0.23235** → 0.232; median I² = **38.785** → 38.8%; 41.90% with I² > 50%; 68.08% with τ² > 0; RE core (FDR_RE < 0.05 & consistency ≥ 0.8) = **1,008**; 1,008/4,055 = **24.86%** → 24.9%. All five printed values reproduce.
3. **Bulk-only sensitivity, exactly.** `META_bulkonly_meta.csv`: 15,735 genes at K ≥ 3, core (FDR < 0.05 & consistency ≥ 0.8) = **2,512**; overlap with the 4,055 primary core = **2,202** = **54.32%** → 54.3%. Bulk-only gene sets from `META_bulkonly_sensitivity_summary.json`: neuroinflammation +5.133/100% up, DAM +3.965/87.5% up, complement +3.535/93.8% up, OXPHOS −2.799 with `frac_up = 0.2778` → **72.2% down**; Nav_SCN p = 0.268, P2RX/P2RY 0.339, TRP 0.917, CACNA 0.827 — every one matches line 50.
4. **Set-level BH, and the BH arithmetic itself.** `_R4_geneset_setlevel_bh.csv`: Neuroinflammation/Complement/DAM q = **0.002999** → 0.003 each; OXPHOS q = **0.020240** → 0.020; OXPHOS random-effects q = **0.310345** → 0.31; Nav_SCN 0.4433 → 0.44; TRP 0.8881 → 0.89; CACNA 0.8488 → 0.85; Kv_KCNQ 0.8488 → 0.85. I re-derived the BH step-up by hand over n = 18 (0.0005 × 18/3 = 0.003; 0.004498 × 18/4 = 0.0202) — the correction is applied to 18 multi-member sets as stated, and mean_Z/percent-up (4.943/100%, 3.884/93.8%, 3.441/94.4%, −2.373/73.7% down) all match line 48.
5. **Non-circular translation test, exactly.** `_R4_nerveinjury_only_summary.json`, stratum `NI_FDR05_AND_NIcons>=0.8`: k = 2,266, n = 4,899, rate = **0.4625** → 46.2%, CI [0.4486, 0.4765] → 44.9–47.7%; `all_measured`: 6,779/14,390 = **0.4711** → 47.1%, CI [0.4629, 0.4793] → 46.3–47.9%; risk difference 46.25 − 47.11 = **−0.86 pp** → −0.9 pp; permutation p = **0.13957** → 0.14. The 5,000-draw null is verifiable from the p-values themselves (0.00079984 = 4/5001). NI-only core 5,412 (FE) / 3,099 (RE) match. Circular comparators 7,751/14,390 = 53.86% → 53.9% and 2,473/3,556 = **69.54%** → 69.5% (CI 68.0–71.0%) also reproduce, and 1,083/3,556 discordant is consistent.
6. **Docking, end to end.** `P6_docking_scores_merged.csv` = **30,850** rows (10 targets × 3,085), **30,687** with non-null `affinity`, **163** failures (103 TIMEOUT + 60 PDBQT parse errors) → "30,850 poses; 30,687 scored" is exact, and ≈3,070/target is right. `P6_reverse_control.csv`: AXL 0.8798→0.880, TNIK 0.8242→0.824, ACVR1 0.7970→0.797, MAPK14 0.7785→0.779, SLC2A1 0.9142→0.914, ADRA2A 0.5325→0.532. `P6_breadth_chembl_power.csv`: Tier-1 n = 620, ADRA2A AUC **0.6184** → 0.618; full-library n = 3,070, AUC **0.5325**, p = 0.1184 → 0.118. `P6_enrichment_mw_confounder_check.csv`: ADRA2A MW-adjusted AUC **0.5783** → 0.578, ΔAUC = +0.071, CI [+0.032, +0.110], p = **0.0005**; AXL ΔAUC CI [−0.030, +0.104], p = 0.141; TNIK [−0.224, +0.193], p = 0.4435; ACVR1 p = **0.5840**. `P6_BH_correction.csv`: ADRA2A size-independent BH q = **0.0025**. `P6_multivariate_physchem_control.csv`: AXL LR p = 2.6e-5 (AUC 0.8953→0.9267), TNIK 7.3e-5 (0.8516→0.8978), ACVR1 9.6e-4 (0.8983→0.9308) with Wald p = 0.172 → 0.17, MAPK14 0.066, ADRA2A 0.027 (0.7910→0.7967). EPV (= n_pos/8) reproduces 1.1 / 1.6 / 1.3 / 2.0 / 14.4 → 14. `P6_face_validity.csv`: 0/64 in Top-20 with expected 0.4, composite rank AUC 0.538 (p = 0.146), α2-agonists MW-adjusted AUC 0.428 (p = 0.760). Library: 3,085/3,311 = 93.17% → 93.2%.
7. **Table 3a / 3b, every cell.** Against `_R4_targets_fixed_vs_random.csv` and `P6_target_plausibility.json`: ADRA2A 4.84/1.5e-5/1.00/0.039/14; MAPK14 6.09/3.9e-8/1.00/0.126/25; AXL 6.14/2.9e-8/1.00/0.068/4; TNIK 8.00/4.3e-13/1.00/0.021/10; ACVR1 6.95/3.2e-10/1.00/0.188/25; SERPINE1 6.92/3.7e-10/1.00/0.060/16; SLC2A1 6.83/6.3e-10/1.00/0.0000/5; GALNS 5.79/1.8e-7/0.83/0.025/2; VASH2 6.00/6.4e-8/0.83/0.186/6; ITPKC 7.18/8.1e-11/1.00/0.296/1. Exactly 4 of 10 retain FDR_RE < 0.05 (TNIK 0.021, SLC2A1 7.0e-8, GALNS 0.025, ADRA2A 0.039). ADRA2A has the smallest |meta_Z| (4.84) of the ten. The 17-member `dock_eligible` list in `P6_target_plausibility.json` is character-for-character the list printed at line 114.
8. **Single-cell and spatial.** `P5_hub_lineage_consensus.csv`: NotLocalisable = **15** (ATF3, CDHR5, ACVR1, AGRN, ANKRD1, CCDC160, CRISP3, FLNC, ITPKC, LNP1, NPY, REG3B, SERPINE1, SLC2A1, VIP) → 20 localisable; Neuronal 8 / Glial 3 / Immune 4 / Mixed 5 sums to 20; `confident = True` count = **7** with exactly the genes named (ANKRD13B, CTTN, PTPN23, SRRM4, VASH2, TFE3, CHL1). `P5_GSE216039_DRG_hub_finetype_top.csv`: 34 rows (CRISP3 absent → 34/35 present), `detected = True` = **25**, of which **20** `top_finetype = Injured_RegenNeuron`; SPRR1A top_pct 0.981 vs others 0.168 (ratio 5.84 → 5.8×) and specificity 17.39 → 17.4×; ECEL1 25.69 → 25.7×; NPY 10.04 → 10.0×; FLNC 10.21 → 10.2×. `P5_GSE328175_SC_ShamSNI_hub_localisation.csv`: 33 symbols (CRISP3, REG3B absent) and max ambient_index AXL **3.111** → 3.11, ATF3 **2.585** → 2.59. `P5_GSE325938_hub_regionalization.csv`: `present = False` for CRISP3 and LNP1 → 33/35; DorsalHorn top_region count = **17** (17/33 = 51.5%); all 17 have `top_detection ≥ 0.05`; below-floor set is exactly {CDHR5, SERPINE1, CRISP3, LNP1, VIP, REG3B, ANKRD1}; `crossmodal = consistent` = 6, all Neuronal.
9. **Human miRNA layer.** `P4_hub_targeting_miRNAs.csv` = **3,511** rows over **33** distinct hubs, 752 with score ≥ 80; `P4_hub_miRNA_human_integration.csv` = 253 distinct miRNAs expanding to **328** hub–miRNA pairs; `P4_setlevel_test.json` n = 253, `perm_p = 0.5101` → 0.51. All four printed values reproduce.
10. **Reference list is clean.** 36 entries, numbered 1–36 with no gaps, no duplicate DOIs, every entry carries a `https://doi.org/…`, every entry is cited, and the first-occurrence order of citation markers is strictly monotonic 1→36 (Vancouver first-citation order satisfied). This independently corroborates the compliance document's §1 item 6 and §3 headline (36/36), even though that document's other numbers are stale (F12).
11. **Collapse sensitivity.** `META_collapse_meta.csv` (untracked duplicate of `P2_meta_sensitivity.csv`): collapsed_core 4,294, shared 3,707, retained_fraction 0.9142 → "core 4,294, retained 3,707/4,055 = 91.4%" is correct.
12. **LODO point estimates.** `P3_lodo_auc_ci.csv` and `P3_lodo_auc_ci_leakage_controlled.csv` match the manuscript exactly: raw GSE278227 1.000 (n = 28), GSE267799 0.917 [0.729, 1.000] (n = 20), GSE241361 DRG 1.000 (n = 9), SC 0.950 [0.709, 1.000] (n = 9), GSE212311 1.000 (n = 6); leakage-controlled four folds at 1.000 [1.0, 1.0] and the incision fold **0.677 [0.374, 0.940]**. `P3_ml_summary.json` confirms 35 hubs, 32 in meta core, pool 800, 13,208 common genes, λ.1se = 1 gene. Pooled 5×20 CV 0.999 and permutation null 0.490 ± 0.085 match `P3_ml.out`.

---

## 4. § Questions for the authors

1. **Bootstrap (F1/F2).** Was the XGBoost `fit(Xp, yb)` call and the integer-index LASSO return intentional? If intentional, what is the statistical justification for pairing resampled labels with non-resampled feature rows? If not, do you accept that the corrected run inverts the reported instability (0.79 → 7.84 dock-eligible hubs recovered; P(≥3 of 17) 0.040 → 1.000)?
2. **Which numbers are the paper's?** After the fix, will you re-report the stability figures, or retire the "structurally, not statistically, determined target list" claim? The honest-null argument in Results line 114 currently depends on the unfixed numbers.
3. **Deposit state (F3).** Which commit will actually be tagged for submission — `c792a1a` or a new commit containing the working-tree corrections? As of now the manuscript's bulk-only (2,512/54.3%) and Visium (33/35) numbers exist only in uncommitted files.
4. **Tag vs. repository.** The Data Availability statement cites tag `v1.0.0` (2026-09-19) but the Zenodo sentence says "a versioned Zenodo archive **will be deposited at submission**". Which artefact is the record of truth at the moment of submission?
5. **Synthetic fixtures (F4).** Were `_synthetic_selftest_DO_NOT_USE/*` intended to ship? If they must stay for regression testing, can they be renamed (e.g. `*.selftest.csv`) so they cannot be mistaken for `P6_*` outputs?
6. **Which gene-set file is authoritative (F9)?** `P3_geneset_stats.csv` or `_R4_geneset_setlevel_bh.csv`? The two disagree for at least five sets; the manuscript quotes both.
7. **53.8% (F6).** Do you intend the 2,318/4,306 figure to carry weight in the non-circular argument, given that it comes from the file you declare superseded and still uses the incision-containing meta FDR?
8. **LC-LODO model (F8).** Should the leakage-controlled 0.677 [0.374, 0.940] be attributed to the ~142-feature union model rather than to the 35-hub list?
9. **GSE265957 label (F23).** Is "tibial-nerve-injury" meant to describe SNI (tibial + common peroneal ligation, sural spared)? If so, why is GSE241361 — also labelled SNI in your files — not described the same way?
10. **Spinal contrast (F18).** Was the exclusion of `GSE241361_S1R_SC` from the meta a deliberate choice (my reading) or an oversight? If deliberate, the Methods should say so.
11. **`_R4_translation_noncircular.csv` (F5).** Was its move to `_archive/` deliberate? If so, both documents that cite it need the new path.
12. **MANIFEST (F19).** Will `MANIFEST.sha256` be committed at the repository root before submission, or should both citations be removed?

---

## 5. § What I actually checked

**Files read (full or partial):** `reports/MVP_PLOSONE_submission.md` (all 333 lines, including the long lines that a naive read truncates), `reports/MVP_PLOSONE_supplementary.md` (all 304 lines), `reports/MVP_STROBE_checklist.md`, `reports/MVP_PLOSONE_cover_letter.md`, `reports/MVP_PLOSONE_compliance_check.md`; scripts `p2_deg_meta.py`, `p2_bulkonly_meta_genelevel.py`, `p3_ml.py`, `p3_finalize.py`, `p3_ml_leakage_controlled.py`, `p3_hub_bootstrap.py`, `p7_targetset_bootstrap.py`, `p7b_translation_noncircular.py`, `p7c_nerveinjury_only_meta.py`; `scripts/p3_ml.out`; `.gitignore`; `PROJECT_PLAN.md` (GSE265957 rows).

**Commands/analysis run:** pandas/numpy/scipy/sklearn/xgboost recomputation of every headline number from `results/tables/`; a from-scratch 2-variant bootstrap probe (`_scratch/a3_bootstrap_probe.py` → `_scratch/a3_bootstrap_probe.json`, B = 100, SEED = 42, POOL = 800, C_min = 8.53168) that reproduces the published pipeline and then changes only the XGBoost alignment; reference-list parsing (36 entries, citation-order, DOI set); cross-document value grep for 24 statistic tokens; file-existence check of every `*.csv/json/png/py` token cited in the five documents; `git ls-files` / `git ls-tree` / `git show` / `git status` / `git diff` comparisons of working tree vs `HEAD` vs tag `v1.0.0`. No file under `results/tables/` or `reports/` was written; all probe output is under `_scratch/`.

**Cross-verification table** (MS = manuscript value, RC = my recomputation):

| Statistic | MS | RC | Source | Verdict |
|---|---|---|---|---|
| Genes tested | 16,552 | 16,552 | `META_DRG_axis_stouffer.csv` | PASS |
| meta_FDR < 0.05 | 6,869 | 6,869 | same | PASS |
| FE core | 4,055 | 4,055 | same; `META_DRG_axis_CORE_signature.csv` = 4,055 rows | PASS |
| ATF3 meta_Z / FDR | 10.53 / 1.0e-21 | 10.533 / 1.0046e-21 | same | PASS |
| Weights 2.19/1.22/2.65/1.49/1.00 | as printed | 2.191/1.225/2.646/1.491/1.000 | recomputed from deposited n | PASS |
| RE core | 1,008 | 1,008 | `_R4_random_effects_meta.csv` | PASS |
| Median τ² | 0.232 | 0.23235 | same | PASS |
| Median I² | 38.8% | 38.785 | same | PASS |
| I² > 50% / τ² > 0 | 41.9% / 68.1% | 41.90% / 68.08% | same | PASS |
| RE retention | 24.9% | 24.86% | 1,008/4,055 | PASS |
| Hub median I² / 18 of 35 | 72.8% / 18 | 72.8 / 18 | `_R4_translation_noncircular.json` | PASS |
| Bulk-only core | 2,512 | 2,512 | `META_bulkonly_meta.csv` | PASS (uncommitted vs deposit — F3) |
| Bulk-only overlap | 2,202 (54.3%) | 2,202 (54.32%) | same | PASS (F3) |
| Bulk-only OXPHOS down | 72.2% | 72.22% (frac_up 0.2778) | `META_bulkonly_sensitivity_summary.json` | PASS |
| OXPHOS q FE / RE | 0.020 / 0.31 | 0.020240 / 0.310345 | `_R4_geneset_setlevel_bh.csv` | PASS |
| Neuroinflam/DAM/Complement q | 0.003 each | 0.002999 each | same | PASS |
| Non-circular test | 2,266/4,899 = 46.2% | 0.4625 | `_R4_nerveinjury_only_summary.json` | PASS |
| Background | 6,779/14,390 = 47.1% | 0.4711 | same | PASS |
| Risk difference / perm p | −0.9 pp / 0.14 | −0.86 pp / 0.13957 | same | PASS |
| Core concordance | 2,473/3,556 = 69.5% | 0.6954 | `_R4_supplementary_summary.json` | PASS |
| Core → NI-consistency | 53.8% (2,318/4,306) | 0.5383 | `_R4_translation_noncircular.json` | PASS, but superseded source (F6) |
| NI-only core FE / RE | 5,412 / 3,099 | 5,412 / 3,099 | `_R4_nerveinjury_only_summary.json` | PASS |
| LODO incision (leakage-ctrl) | 0.677 [0.374, 0.940] | 0.677083 [0.373536, 0.940494] | `P3_lodo_auc_ci_leakage_controlled.csv` | PASS (method mislabelled — F7) |
| Hub bootstrap range / ≥0.9 | 0.5–15.5% / 0 of 35 | 0.005–0.155 / 0 | `P3_hub_bootstrap.csv` | PASS as printed, **artefact** (F1, F2) |
| "LASSO no selections" | as stated | LASSO selects mean 37.7 / 800 per resample | probe | **FAIL** (F2) |
| Target-set median size / IQR | 6 / 5–8 | 6 / 5–8 (probe buggy) | `_R4_targetset_bootstrap.json` | PASS as printed, **artefact** (F1) |
| Median Jaccard | 0.026 | 0.026 (probe buggy) | same | PASS as printed, **artefact** (F1) |
| Mean eligible recovered / P(≥3 of 17) | 0.79 / 0.040 | 0.75 / 0.040 (probe buggy) | same | PASS as printed, **artefact** (F1) |
| Docked-9 mean recovered | 0.35 | 0.31 (probe buggy) | same | PASS as printed, **artefact** (F1) |
| CDHR5 most stable | 15.5% | 0.155 | `P3_hub_bootstrap.csv` | PASS |
| λ.1se / pool / common genes | 1 gene / 800 / 13,208 | 1 / 800 / 13,208 | `P3_ml_summary.json` | PASS |
| Drugs / poses / scored | 3,085 / 30,850 / 30,687 | 3,085 / 30,850 / 30,687 (163 null) | `P6_docking_scores_merged.csv` | PASS |
| Library coverage | 93.2% | 93.17% (3,085/3,311) | `P6_ligand_library.csv` | PASS |
| ADRA2A full-library | 0.532, p = 0.118 | 0.532465, 0.118409 | `P6_enrichment_mw_confounder_check.csv` | PASS |
| ADRA2A Tier-1 | 0.618 (620 drugs) | 0.618368, n = 620 | `P6_breadth_chembl_power.csv` | PASS (STROBE wrong — F10) |
| ADRA2A MW-adjusted / ΔAUC p | 0.578 / 0.0005 | 0.578314 / 0.0005 | `P6_enrichment_mw_confounder_check.csv` | PASS |
| Size-independent BH q | 0.0025 | 0.0025 | `P6_BH_correction.csv` | PASS |
| ACVR1 size-indep p | 0.584 | 0.5840 | same | PASS |
| AXL/TNIK ΔAUC CI | [−0.030,+0.104] / [−0.224,+0.193] | identical | same | PASS |
| Multivariate LR p (AXL/TNIK/ACVR1/MAPK14/ADRA2A) | 2.6e-5 / 7.3e-5 / 9.6e-4 / 0.066 / 0.027 | 2.6e-5 / 7.3e-5 / 9.57e-4 / 0.0662 / 0.0269 | `P6_multivariate_physchem_control.csv` | PASS |
| ACVR1 Wald p | 0.17 | 0.1718 | same | PASS |
| Face validity | 0/64, AUC ≈ 0.54, α2 0.428 / p = 0.76 | 0/64 (exp 0.4), 0.538 (p = 0.146), 0.428 (p = 0.760) | `P6_face_validity.csv` | PASS |
| Hubs | 35 (5 three-method) | 35, n_methods {3:5, 2:30} | `P3_hub_genes.csv` | PASS |
| Hubs in meta core | 32/35 | 32 | same | PASS |
| Dock-eligible / docked | 17 / 9 | 17 / 9 | `P6_target_plausibility.json` | PASS |
| Single-cell NotLocalisable / localisable | 15 / 20 | 15 / 20 | `P5_hub_lineage_consensus.csv` | PASS |
| Cross-dataset lineage-consistent | 7/35 | 7 (`confident=True`) | same | PASS |
| DRG present / detected / Injured_RegenNeuron | 34/35, 25, 20 | 34, 25, 20 | `P5_GSE216039_DRG_hub_finetype_top.csv` | PASS |
| SPRR1A 98.1% vs 16.8%, 5.8×, 17.4× | as printed | 0.981 / 0.168 / 5.84× / 17.39× | same | PASS |
| Ambient ATF3 / AXL (spinal) | 2.59 / 3.11 | 2.585 / 3.111 | `P5_GSE328175_SC_ShamSNI_hub_localisation.csv` | PASS |
| Spinal present | 33/35 | 33 symbols | same | PASS |
| Visium present / dorsal horn | 33/35, 17 (51.5%) | 33, 17 (51.5%), all ≥ 5% detection | `P5_GSE325938_hub_regionalization.csv` | PASS (deposited copy says 35 — F3) |
| Cross-modal consistent | 6 | 6 | same | PASS |
| miRNA pairs / high-conf / plasma pairs / distinct | 3,511 / 752 / 328 / 253 | 3,511 / 752 / 328 / 253 | `P4_hub_targeting_miRNAs.csv`, `P4_hub_miRNA_human_integration.csv` | PASS |
| miRNA set-level p | 0.51 | 0.5101 | `P4_setlevel_test.json` | PASS |
| Collapse core / retention | 4,294 / 91.4% | 4,294 / 0.9142 | `META_collapse_meta.csv` | PASS |
| References count / order / DOIs / all cited | 36, first-citation order | 36, monotonic 1→36, 36 DOIs, 0 missing, 0 duplicates, 0 uncited | manuscript | PASS |
| Abstract length | ≤300 | 214 words | manuscript | PASS (compliance doc says 180 — F12) |

---

## 6. § Must-fix list (ordered by severity)

| # | Severity | Item | Where |
|---|---|---|---|
| 1 | **Major** | XGBoost fitted on un-resampled `Xp` with resampled `yb` in both bootstrap scripts; all hub/target-set stability numbers are artefacts. Fix the pairing, re-run B = 200, rewrite the numbers. | `scripts/p3_hub_bootstrap.py:85-86`, `scripts/p7_targetset_bootstrap.py:112-113`; Results lines 66, 114; Supplementary S7; cover letter ¶(ii) |
| 2 | **Major** | LASSO returns integer indices compared against symbol sets → zero LASSO votes by construction; "LASSO makes no selections" is false (mean 37.7 selections/resample). Return symbols; correct the sentence. | `scripts/p3_hub_bootstrap.py:71,94`, `scripts/p7_targetset_bootstrap.py:89,117`; Results line 66 |
| 3 | **Major** | Data Availability statement names tag `v1.0.0` and six artefacts that do not exist at that tag; `HEAD` still ships superseded 1,981 / 42.7% and 35/35 Visium `present`. Commit the working tree, retag, update both citations. | Manuscript line 267; cover letter line 13; `results/tables/META_bulkonly_sensitivity_summary.json`; `results/tables/P5_GSE325938_hub_regionalization.csv` |
| 4 | **Major** | Synthetic self-test docking outputs tracked in git under `results/tables/` with real filenames (ADRA2A AUC 0.968 vs 0.532). Move/delete, untrack, add gitignore rules. | `results/tables/_synthetic_selftest_DO_NOT_USE/`; `.gitignore` |
| 5 | Minor | `results/tables/_R4_translation_noncircular.csv` cited but deleted (now in `_archive/`). | Manuscript line 58; Supplementary line 212 |
| 6 | Minor | 53.8% (2,318/4,306) comes from the artefact the same paragraph declares superseded and still uses the incision-containing FDR. Label or drop. | Manuscript line 58; Supplementary line 218 |
| 7 | Minor | "DeLong" is a bootstrap percentile CI; LC-LODO additionally refits the scaler on the held-out fold. Correct the label and the scaler, re-run if the number moves. | Manuscript lines 64, 158, 289; `scripts/p3_finalize.py:66-71`; `scripts/p3_ml_leakage_controlled.py:76-89,133` |
| 8 | Minor | Leakage-controlled LODO uses the union rule (139–164 features), not the published ≥2/3 consensus (35 genes). Disclose. | Methods line 158; `scripts/p3_ml_leakage_controlled.py:116` |
| 9 | Minor | Two gene-set artefacts disagree (P2RX/P2RY 0.440 vs 0.4383; OXPHOS 0.004 vs 0.0045; Nav_SCN 0.180 vs 0.1724) and the manuscript quotes both. Declare one source; reseed. | Manuscript lines 84, 286; Supplementary S5/S5b |
| 10 | Minor | STROBE checklist prints "ADRA2A Tier-1 AUC 0.532" — Tier-1 is 0.618. | `reports/MVP_STROBE_checklist.md:26` |
| 11 | Minor | STROBE line-number pointers stale ("Ethics statement, line 164" → actually line 176). | `reports/MVP_STROBE_checklist.md:25-34` |
| 12 | Minor | Compliance doc stale: ref numbers 34/35/36 vs actual 23/11/12; "results **at**" vs "results **in**"; AI-use quote omits "Claude, Anthropic"; STROBE filename wrong; "S8" vs "S1–S7"; Funding quote not verbatim. | `reports/MVP_PLOSONE_compliance_check.md` lines 27, 30, 47-50, 66 |
| 13 | Minor | Supplementary S5b duplicates the Sigma1 row (20 rows for 19 sets). | `reports/MVP_PLOSONE_supplementary.md:191` |
| 14 | Minor | Supplementary S5 attributes ref 20 to "Nat Med 2003"; it is *Nature* 424:778–783. | `reports/MVP_PLOSONE_supplementary.md:153` |
| 15 | Minor | The 46.2% CI is 44.9–47.7% in the manuscript and 44.9–47.6% in the supplementary; print 44.86–47.65%. | Manuscript line 58; Supplementary line 220 |
| 16 | Minor | `bulk_consist` (0.25) ≠ `consistency` (0.75) for the same SCN genes; rename or annotate. | `META_bulkonly_sensitivity_summary.json`; `META_bulkonly_meta.csv`; Table 1b note line 313 |
| 17 | Minor | Orphan/duplicate/divergent artefacts: `P2_meta_sensitivity.csv` ≡ `META_collapse_meta.csv`; `_QC_*` disagree with `P6_*` (ADRA2A `n_scored` 620 vs 3,070); 48 unreferenced files. | `results/tables/` |
| 18 | Minor | No spinal-cord contrast enters the "DRG–spinal axis" meta; `DEG_GSE241361_S1R_SC__SNI_vs_Naive_WT_SC.csv` is orphaned. State the scope. | `scripts/p2_deg_meta.py:130-136`; Methods line 144 |
| 19 | Minor | `MANIFEST.sha256` cited twice but only exists untracked at `_manifest/`. | Manuscript line 267; cover letter line 13 |
| 20 | Minor | Methods say "LASSO (λ.min)"; the voting route is λ.min filtered at ≥60% bootstrap stability (13 genes). | Methods line 158; `scripts/p3_ml.py:106,128` |
| 21 | Minor | Fig 2 legend says "three folds reach AUC 1.000"; only two cross-animal folds do. | Manuscript line 289 |
| 22 | Cosmetic | The `_R4_targetset_bootstrap_resamples.csv` audit trail and its generating code are uncommitted; regenerate after the F1 fix. | `scripts/p7_targetset_bootstrap.py`; `results/tables/_R4_targetset_bootstrap_resamples.csv` |
| 23 | Cosmetic | Compliance doc abstract word count "180" vs actual 214. | `reports/MVP_PLOSONE_compliance_check.md:15` |
| 24 | Minor | "tibial-nerve-injury" for GSE265957 unsupported by any artefact (files say SNI; `PROJECT_PLAN.md:40` says "SNI/CFA"). | Manuscript lines 36, 44 |
