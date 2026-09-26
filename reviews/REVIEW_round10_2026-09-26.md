# Round 10 independent review — PLOS ONE resubmission (post-Round-9 revision)

**Reviewed object:** `reports/MVP_PLOSONE_submission.md` (332 lines) + supporting set
(`MVP_PLOSONE_supplementary.md`, `MVP_STROBE_checklist.md`, `MVP_PLOSONE_cover_letter.md`,
`MVP_PLOSONE_compliance_check.md`) + `results/tables/` + `scripts/`.
**Panel:** A1 domain (pain neurobiology), A2 design (statistics/meta-analysis/ML),
A3 implementation (provenance/recompute), A4 venue (PLOS ONE + reporting standards).
**Expert files:** `reviews/round10_2026-09-26/{A1_domain,A2_design,A3_implementation,A4_venue}.md`
**Brief:** `reviews/round10_2026-09-26/_PANEL_BRIEF.md`

---

## 1. Independence statement

**Mechanism.** A fresh panel was convened under a written brief (`_PANEL_BRIEF.md`) that forbids
reading any prior `REVIEW_*`, `RESPONSE_*`, `REVISION_*`, any `reviews/round2_*`…`round9_*`
directory, `.workbuddy/memory/**`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`,
`author_verification_statement.md`, **and each other's outputs**. Each expert was told to treat
the manuscript as a first submission, to accept none of its self-framing, and to verify every
claim they could verify. Each wrote to a separate file with no cross-talk.

**Evidence that independence actually worked (two independent hits on one defect).**
The single most consequential finding of this round — the bootstrap index misalignment
(§4, T0-1) — was found **independently by A2 and A3**, from different entry points and with
different reasoning:

- **A2 (design)** arrived at it by asking whether the instability *interpretation* was sound,
  and noticed the stated mechanism ("LASSO makes no selections") was false.
- **A3 (implementation)** arrived at it by reading the code line-by-line and noticing
  `fit(Xp, yb)` where Random Forest correctly used `fit(Xbs, yb)`.

Neither had seen the other's output. Both then reproduced it numerically and got the same
corrected values. That convergence is the diagnostic signature the brief asks for. A second
convergence: A1 and A4 independently flagged the manuscript/supplementary-cover-letter framing
gap (A1 as a biology-consistency issue, A4 as a cross-document claim-support issue).

**Editor's independent confirmation.** Per the brief, the editor did **not** forward the single
worst claim unverified. The editor personally re-read the source code and re-ran repository
queries. All three confirmations are reported in §3 with the raw output.

---

## 2. Verdict table

| Expert | Layer | Items raised | Major | Minor/Cosmetic | Overall verdict |
|---|---|---|---|---|---|
| A1 | Domain / pain neurobiology | 15 | 6 | 9 | **Major revision** — framework-level mismatch between the promised "DRG–spinal axis" and what the core meta actually pools; DAM-like over-claimed |
| A2 | Design / statistics / ML | 12 | 6 | 6 | **Major revision** — one invalid analysis (bootstrap), one mis-stated heterogeneity defence, one threshold artefact |
| A3 | Implementation / provenance | 24 | 4 | 20 | **Major revision** — the instability result is a coding artefact; deposit does not match the manuscript |
| A4 | Venue / reporting standards | 10 | 3 | 7 | **Do not upload yet** — data-availability statement is currently untrue (desk-reject risk) |

**Distribution.** All four experts independently returned a blocking verdict. There is no
expert who considers the current manuscript uploadable. Two of the four (A2, A3) consider a
*conclusion* — not merely a sentence — to be unsupported.

---

## 3. Cross-verification table (editor-verified rows marked ✱)

| # | Manuscript location | Manuscript claims | Independently recomputed | Who | Verdict |
|---|---|---|---|---|---|
| 1 | `scripts/p7_targetset_bootstrap.py:112`, `scripts/p3_hub_bootstrap.py:85` | Bootstrap measures target-set stability | **XGBoost fitted as `fit(Xp, yb)` — un-resampled features paired with resampled labels.** RF correctly uses `fit(Xbs, yb)`. SHAP also computed on `Xp` | A2, A3, **editor ✱** | **✗ INVALID — conclusion affected** |
| 2 | L64, L233 | "median Jaccard 0.026", "P(≥3 of 17) = 0.040", "median size 6 (IQR 5–8)" | Buggy code reproduces these exactly. After fixing only the XGBoost alignment: **Jaccard 0.296, P(≥3 of 17) = 1.000, size 36 [33–38]**, dock-eligible recovered 0.79 → 7.84 | A3 (B=100, SEED=42), A2 | **✗ artefact** |
| 3 | L112 | "LASSO made no selections" (stated mechanism) | LASSO selects a mean of **37.7 of 800** genes per resample | A2, A3 | **✗ false** |
| 4 | L44 | "median I² = 38.8%" used to defend FE-primary | True over all 16,552 genes. **Among the 4,055 core genes median I² = 52.1%; among hubs 72.8%** | A2 | **△ true but non-supporting** |
| 5 | Data availability, L267 | "The GitHub repository **already contains** all processed data … `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_meta.csv` … (version v1.0.0 … verifiable via MANIFEST.sha256)" | Tag `v1.0.0` contains **0** `_R4_*` files; `HEAD` contains **13**. `MANIFEST.sha256` is in `_manifest/`, **not tracked by git**. Real `10.5281/zenodo.<digits>`: **0 hits** repo-wide | A4, **editor ✱** | **✗ untrue as written** |
| 6 | L64 | Spinal fold AUC | "spinal cord **AUC 1.000**, n = 9" in one sentence; "spinal cord **AUC 0.950 [0.709, 1.000]**, n = 9" in the next paragraph of the same section | **editor ✱** | **✗ internal contradiction** |
| 7 | L64 | Four nerve-injury folds "AUC 1.000" used to claim nerve-injury specificity | GSE212311 is **n = 6 (3 vs 3)**; exact Mann–Whitney p = **0.050**, which is the *floor* for that design. It carries no evidential weight | A2 | **△ one of two "independent" folds is uninformative** |
| 8 | Fig. 2A vs L64 | Leakage-controlled incision AUC stated as 0.677 [0.374, 0.940] | Fig. 2A plots the **raw** 0.917 [0.729, 1.000] | A2 | **✗ figure/text mismatch** |
| 9 | `scripts/p2_deg_meta.py:130-136` | Title promises a "DRG–spinal axis" meta-analysis | All 5 `primary` meta inputs are **DRG**. `GSE241361_S1R_SC` (`axis="SC"`) is computed at line 106 but **not** entered into the meta | A1, **editor ✱** | **△ scope mismatch** |
| 10 | L52 / DAM claim | "DAM-like neuroimmune programme" up | Of 16 members only 9/16 up **and** in core. **LPL** (canonical DAM up-gene) is significantly **down** (Z −3.43, FDR 0.0026, 5/6 down). Homeostatic module that DAM *suppresses* (CX3CR1 6/6 up, FDR 4.7e-9; CD33; TMEM119; P2RY12) is **up**. All 6 meta contrasts are DRG, which contains no microglia | A1 | **✗ over-claimed** |
| 11 | L46 | OXPHOS set-level q = 0.020 (FE) / 0.31 (RE) | Reproduces exactly | A3 | ✓ |
| 12 | L58 | 46.2% (2,266/4,899) vs 47.1% background, −0.9 pp, p = 0.14 | Reproduces exactly | A2, A3 | ✓ |
| 13 | L44 | FE core 4,055 / 16,552 tested / 6,869 at FDR<0.05 | Reproduces exactly | A1, A3 | ✓ |
| 14 | L46 | RE core 1,008, τ² 0.232, I² 38.8%, retention 24.9% | Reproduces exactly | A3 | ✓ |
| 15 | L44 | GSE265957 contributes 2.00 to Σw² = 11.4% (not "twice") | **Correct** — genuinely fixed | A2, A3 | ✓ |
| 16 | L112 | ADRA2A 0.532 (p = 0.118) full library; 0.618 on 620-drug subset; size-indep q = 0.0025 | Reproduces exactly | A3 | ✓ |
| 17 | L44 | ATF3 meta_Z 10.53, FDR 1.0e-21, consistency 1.00 | Reproduces exactly | A1 | ✓ |
| 18 | References | 36 entries, first-citation order, all cited, 36/36 with DOI | Confirmed | A3, A4 | ✓ |

**Editor's raw confirmations (✱):**

```
# (5) deposit vs claim
$ git tag -l                                   → v1.0.0
$ git ls-tree -r --name-only v1.0.0 | grep -c _R4_   → 0
$ git ls-tree -r --name-only HEAD   | grep -c _R4_   → 13
$ git ls-files | grep -i manifest              → (empty — NOT TRACKED)
$ grep -rn "10\.5281/zenodo\.[0-9]" --include="*.md" .  → (0 hits)

# (9) meta scope
# p2_deg_meta.py primary{} = GSE267799_SMIR_DRG, GSE212311_CCI_DRG,
#   GSE278227_CCI_DRG, GSE241361_S1R_DRG, GSE265957_Xtail_DRG_Day4   → all DRG
# line 106: r["dataset"]="GSE241361_S1R_SC"; r["axis"]="SC"   → computed, not in primary{}

# (1) bootstrap bug — code read directly
Xb = Xp[idx]; yb = yall[idx]; Xbs = StandardScaler().fit_transform(Xb)
rf  = RandomForest(...).fit(Xbs, yb)              # correct
clf = xgb.XGBClassifier(...).fit(Xp, yb)          # ✗ Xp is NOT resampled
sv  = clf.get_booster().predict(xgb.DMatrix(Xp))  # ✗ SHAP also on Xp
```

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating / upload-blocking

**T0-1. The target-set bootstrap is invalid; the instability conclusion is a coding artefact.**
*(A2 #1, A3 headline; editor-confirmed)*
- **Problem:** In both bootstrap scripts XGBoost is fitted on the **un-resampled** feature matrix
  `Xp` while the labels `yb` **are** resampled, so features and labels are mis-paired in every
  resample; Random Forest uses the correct `Xbs`.
- **Why it matters:** Every stability number the paper reports — median Jaccard 0.026,
  P(≥3 of 17) = 0.040, median recovered-set size 6, "0.79 of 17 eligible recovered" — is an
  artefact. The manuscript's claim that *"the target list is justified by structural tractability,
  not by statistical stability"* is thereby unsupported, and the cover letter's rigour claim
  rests on it. **The primary hub set (35 hubs) is unaffected** — `p3_ml.py:116` is correct.
- **Specific fix:** Change `scripts/p3_hub_bootstrap.py:85` and
  `scripts/p7_targetset_bootstrap.py:112` from `.fit(Xp, yb)` to `.fit(Xbs, yb)`, and change the
  SHAP call from `xgb.DMatrix(Xp)` to `xgb.DMatrix(Xbs)`. **Re-run both scripts**, then rewrite
  every stability sentence from the new output. Expect the direction of the conclusion to
  *reverse* (the target set becomes stable, not unstable). Second defect in the same scripts:
  `lasso_nonzero()` returns integer column indices that are tested against gene-symbol sets
  (`:71`/`:94`, `:89`/`:117`), making the LASSO vote impossible by construction — fix by
  returning `POOL[i]` symbols.

**T0-2. The data-availability statement is not true as written — desk-reject risk.**
*(A4-05; editor-confirmed)*
- **Problem:** The statement claims the GitHub repository "already contains all processed data"
  including `_R4_random_effects_meta.csv` and `_R4_nerveinjury_only_meta.csv` at version v1.0.0,
  verifiable via `MANIFEST.sha256`. None of that holds: tag `v1.0.0` has **0** `_R4_*` files
  (13 are in `HEAD`), `MANIFEST.sha256` is untracked, and no real Zenodo DOI exists.
- **Why it matters:** A data-availability statement that asserts the presence of files that are
  not in the cited release is exactly what a technical check and an editor look for. It is the
  highest-probability desk-reject trigger in this submission.
- **Specific fix:** Do **all three** before upload: (a) re-tag the release so `v1.0.0` points at
  current `HEAD` (or tag `v1.0.1` and cite that); (b) `git add _manifest/MANIFEST.sha256` so it is
  actually in the repository; (c) create the Zenodo archive and backfill the real DOI. Until (a)
  and (b) are done, soften the sentence to: *"All code and processed data are deposited in the
  public GitHub repository at <URL> (release v1.0.1; integrity verifiable via MANIFEST.sha256).
  A versioned Zenodo archive will be deposited at submission."*

**T0-3. Internal numerical contradiction: the spinal LODO fold has two different AUCs.**
*(editor-confirmed)*
- **Problem:** L64 states "the two GSE241361 folds — mouse DRG AUC 1.000, n = 9; **spinal cord
  AUC 1.000**, n = 9 — which are excluded from the cross-animal mean", and two sentences later
  "the two GSE241361 tests (mouse DRG AUC 1.000, n = 9; **spinal cord AUC 0.950 [0.709, 1.000]**,
  n = 9)".
- **Why it matters:** A reviewer reading one paragraph sees the manuscript contradict itself about
  a number that supports the paper's central positive claim (nerve-injury specificity).
- **Specific fix:** Reconcile against `P3_lodo_auc_ci_leakage_controlled.csv` and use one value
  consistently. Also state explicitly which is leakage-controlled.

**T0-4. Figure 2A contradicts the text it illustrates.**
*(A2)*
- **Problem:** The text reports the leakage-controlled incision AUC as 0.677 [0.374, 0.940];
  Fig. 2A plots the **raw** 0.917 [0.729, 1.000] without saying so.
- **Why it matters:** The figure is what most readers look at; it silently restores the number the
  manuscript deliberately walked back.
- **Specific fix:** Re-plot Fig. 2A from
  `P3_lodo_auc_ci_leakage_controlled.csv`, or annotate the plotted bars "raw (leakage-inflated)"
  versus "leakage-controlled" and cite both in the legend.

### Tier 1 — analyses to add or redo

**T1-1. "Nerve-injury specificity" rests on one fold; the second independent fold is uninformative.**
*(A2)*
- GSE212311 is n = 6 (3 vs 3). Its exact Mann–Whitney p = **0.050**, the *minimum attainable* for
  that design — AUC = 1.0 there is not evidence, it is the floor. Only GSE278227 (n = 28) carries
  real weight. Also, degenerate CIs at AUC = 1 are degenerate **by construction**.
- **Fix:** State the per-fold exact p and the fold n alongside every AUC = 1.0, and restrict the
  specificity claim to what GSE278227 plus the same-animal GSE241361 pair can actually support.

**T1-2. The heterogeneity defence uses the wrong denominator.**
*(A2)*
- FE-primary is defended with median I² = 38.8% computed over all 16,552 genes. Among the 4,055
  **core** genes median I² = **52.1%** (51.9% of them > 50%); among hubs **72.8%**.
- **Fix:** Report the core-gene I² as the relevant figure and re-state the FE-primary justification
  against it, or move to RE-primary for gene-level claims.

**T1-3. "45.7% of the core is translatome-dependent" is a threshold artefact.**
*(A2)*
- Of the 1,853 genes lost when the translatome is excluded, 1,512 (81.6%) fail only because K
  drops 6→4, which changes the consistency rule from 5/6 to 4/4. With fraction-matched (3/4)
  thresholds the overlap is **3,587/4,055 = 88.5%**, not 54.3%.
- **Fix:** Report the fraction-matched overlap as the primary sensitivity figure and keep the
  unmatched number as a note, or state both with the threshold rule made explicit.

**T1-4. The meta-analysis does not include a spinal contrast, though the title promises an axis.**
*(A1; editor-confirmed)*
- All five `primary` meta inputs are DRG. `GSE241361_S1R_SC` is computed but excluded. The spinal
  pole appears only in the LODO folds and the Visium localisation.
- **Fix (choose one):** (a) enter the spinal contrast into the meta and report a proper
  two-tissue meta; or (b) retitle to name the DRG as the meta-analysed tissue and describe the
  spinal cord as a localisation/ML layer. Do not leave the title promising what the core
  quantitative product does not deliver.

**T1-5. "DAM-like" is over-claimed and is anatomically incoherent as stated.**
*(A1)*
- Only 9 of 16 members are up **and** in the core. **LPL**, a canonical DAM up-gene, is
  significantly **down** (Z −3.43, FDR 0.0026, 5/6 down). The homeostatic module that DAM
  characteristically *suppresses* (CX3CR1 6/6 up, FDR 4.7e-9; CD33; TMEM119; P2RY12) is **up**.
  All six meta contrasts are DRG, which contains no microglia.
- **Fix:** Drop "DAM-like" for the DRG-level signal, or rename to what the data show — e.g. *"a
  shared neuroimmune/complement-enriched programme that resembles the DAM-like signature at the
  gene-set level but is not a cell-type-resolved microglial state (LPL is down and the homeostatic
  module is up in these DRG contrasts)"*. Cite Krasemann 2017 and Deczkowska 2018 for the DAM
  definition being used.

**T1-6. The two-filter rule is not applied symmetrically.**
*(A2)*
- Only 5 of 10 targets have ChEMBL binders at all, and ADRA2A alone holds 115 of 164 binders.
  The Wald-vs-LR consistency standard is applied to ACVR1 (0.17) but not to ADRA2A (**0.504**).
- **Fix:** Either apply the same standard to every target and report the resulting table, or state
  explicitly why ADRA2A is exempt and what that does to the "inconclusive" verdict.

**T1-7. LODO EPV is undisclosed and is far worse than the docking EPV that is disclosed.**
*(A2)*
- 139–164 features on 44–66 training samples → **EPV 0.13–0.22**, versus the EPV ≥ 10 standard the
  manuscript applies elsewhere, and versus the docking EPVs (1.1–2.0) it does disclose.
- **Fix:** Disclose the LODO EPV in the same paragraph as the docking EPV, with the same caveat.

**T1-8. The "incision arm" is a mixed model and includes a timepoint at which the phenotype has resolved.**
*(A1)*
- GSE267799 contains both SMIR (n = 20) and LPI (n = 16); the "chronic vs baseline" contrast is a
  merged n = 12 vs 8. The chronic group includes **day 32** samples, and Flatters 2008 records
  that SMIR-induced mechanical hypersensitivity has resolved by day 32. The manuscript also states
  harvest days were not annotated in GEO, but they are (0d / 6h / 2d / 10d / 32d).
- **Fix:** State the mixed-model composition, split or justify the merge, and correct the
  "days not annotated" statement. Cite Flatters 2008 and Yu 2020, Kehlet 2006.

### Tier 2 — wording / presentation

- **T2-1** (A4): Of the 8 main display items, **Fig. 2–5, Table 2 and Table 3 are never cited in
  the text** (only Fig. 1 and Table 1b are). Cite every display item inline.
- **T2-2** (A4): **Table 2 has no table content** — only prose and a CSV path — yet is counted as a
  main display item. Either populate it or demote it.
- **T2-3** (A4): Line 8 still carries an internal revision log ("This version adds…", "correction
  of three printed values"). Delete.
- **T2-4** (A4): "upon acceptance it will receive a citable permanent DOI" misdescribes Zenodo,
  which mints a DOI at deposition. Reword to "will be deposited at submission and will receive a
  DOI at that point".
- **T2-5** (A1): Reference 11 is mis-attributed — Yin 2016 did not perform IB4⁺ sorting (and is
  actually the correct source for SCN3A up-regulation). Re-point the citation.
- **T2-6** (A1): "SCN3A was not among the tested sets" is false — SCN3A is in the `Nav_SCN` set.
  Correct the sentence.
- **T2-7** (A1): **11 of 35 hubs** peak in meningeal/fibroblast regions; this is never reported and
  qualifies the localisation claim. Report it.
- **T2-8** (A1): GSE265957 is SNI, not "tibial-nerve injury" as described. Correct the model name.
- **T2-9** (A1): "establishing … nerve-injury-specific" draws a positive conclusion from a
  non-significant result. Downgrade to the descriptive form.
- **T2-10** (A4): The cover letter's "CPSP DRG–spinal axis" framing contradicts the abstract's
  "not CPSP-specific". Align.
- **T2-11** (A2/A3): The stated bootstrap mechanism "LASSO makes no selections" is false — LASSO
  selects a mean of 37.7 of 800 genes per resample. Delete or correct.

### Tier 3 — deposit hygiene / format

- **T3-1** (A3): A synthetic file `results/tables/_synthetic_selftest_DO_NOT_USE/P6_reverse_control.csv`
  (ADRA2A AUC **0.968**, 400 ligands) is tracked in git and not excluded by `.gitignore`. Remove it
  from the repository or gitignore it — a reviewer who opens it will see a number that contradicts
  the paper.
- **T3-2** (A3): `HEAD` still ships the disowned bulk-only **1,981 / 42.7%** artefact. Delete or
  move to `_archive/`.
- **T3-3** (A3): The Visium table has all 35 hubs `present=True`, versus the manuscript's 33/35.
  Regenerate as A3 did (by `top_detection > 0`) or reconcile.
- **T3-4** (A4): Cosmetic — duplicate cover-letter artefact, stale lock files, and any remaining
  *Scientific Reports* branding in filenames.

---

## 5. Consensus / complementarity / disagreement

**Consensus (all four).** The manuscript is not uploadable in its current state. All four also
agree that the **quantitative core is sound** — no expert found a fabricated or mistranscribed
number in the meta-analysis, sensitivity, translation, docking, single-cell or miRNA layers
(A3 alone re-verified 40+ values exactly).

**Complementarity.** Each expert owned a distinct layer and the findings do not overlap:
A1 caught the anatomy/scope and literature-attribution errors; A2 the statistical-design defects;
A3 the code-level and deposit defects; A4 the administrative/technical-check defects. Notably,
A2 and A3 arrived at the *same* code defect from opposite directions (interpretation vs code
reading), which is the round's strongest independence signal.

**Disagreement and how it is adjudicated.**
- *Severity of the spinal-contrast exclusion (T1-4).* A1 treats it as Major (title promises an
  axis); one could argue the manuscript says "DRG-axis" in the Results. **Ruling: upheld as
  Major, but as a scope-disclosure defect, not as misrepresentation.** The manuscript does say
  "DRG-axis Stouffer meta-analysis" at L44 and does analyse the spinal cord in the LODO and
  spatial layers, so this is not data fabrication. But the title says "DRG–spinal axis" and the
  4,055-gene core — the paper's headline product — is DRG-only. The author must either add the
  spinal contrast to the meta or retitle. The cost of compliance is low; adopt the conservative
  reading.
- *Whether the bootstrap bug changes a conclusion.* One might argue the bug only affects a
  secondary stability claim. **Ruling: it changes a conclusion.** The manuscript explicitly uses
  the instability to justify the target list ("structural tractability, not statistical
  stability") and the cover letter uses it as a rigour claim. Corrected, the target set is stable.
  The direction reverses, so this is not wording-only.
- *FE-primary (T1-2).* A2 says the wrong denominator was used. **Ruling: upheld.** The manuscript
  is not wrong that median I² = 38.8% genome-wide; it is wrong to use that figure to defend a
  claim about the core genes, where I² = 52.1%. Report both.

---

## 6. Priority must-fix list

**DESK-REJECT flags (must clear before upload):**
1. **T0-2** — data-availability statement currently untrue (tag/MANIFEST/Zenodo).
2. **T0-3** — self-contradictory spinal-fold AUC in one paragraph.
3. **T3-1** — synthetic reverse-control file (ADRA2A AUC 0.968) sits in the public repository.

**Must redo an analysis (cannot be fixed by rewording):**
4. **T0-1** — fix the bootstrap index alignment, re-run, rewrite all stability claims.
5. **T1-4** — either enter the spinal contrast into the meta, or retitle.
6. **T1-2** — recompute and report I² over the core genes.
7. **T1-3** — recompute the translatome sensitivity with fraction-matched thresholds.
8. **T0-4** — re-plot Fig. 2A from leakage-controlled values.

**Must reword (with evidence):**
9. **T1-5** DAM-like; **T1-1** per-fold exact p and n; **T1-6** symmetric filter; **T1-7** LODO EPV;
   **T1-8** mixed incision model; **T2-1…T2-11** as listed.

**Cleanup:** T3-2, T3-3, T3-4.

---

## 7. What stands up — do NOT change these

Carried forward from the experts; each was checked, not assumed.

1. **No fabricated or mistranscribed numbers.** A3 re-verified 40+ values across meta-analysis,
   random effects, bulk-only sensitivity, set-level BH, translation, docking, single-cell/spatial
   and miRNA layers — all reproduce exactly (16,552 / 6,869 / 4,055; 1,008 / τ² 0.232 / I² 38.8% /
   24.9%; 2,512 / 2,202 / 54.3%; q 0.020 / 0.31; 46.2% vs 47.1%, p = 0.14; 0.677 [0.374, 0.940];
   30,850 / 30,687; 0.532 / 0.618 / 0.578 / 0.0025). A1 independently confirmed ATF3 and the
   Table 1b SCN values digit-for-digit.
2. **The corrected GSE265957 weight statement (11.4%, "not twice") is genuinely right** — A2
   recomputed and confirmed it. That fix holds.
3. **The non-circular translation test is correctly specified and honestly reported** (A2) —
   46.2% vs 47.1%, −0.9 pp, p = 0.14, with the circularity explicitly diagnosed and a
   nerve-injury-only construction substituted.
4. **The 35-gene hub set itself is unaffected by the bootstrap bug** — `p3_ml.py:116` is correct
   (A2, A3).
5. **The reference list is clean** — 36 entries, correct Vancouver first-citation order, every
   entry cited, 36/36 with DOI (A3, A4).
6. **The abstract meets PLOS ONE structure** — four subheadings, 218 words, no citations (A4).
7. **The ethics statement is honest** — IRB correctly attributed to the original deposition rather
   than implying a new approval (A4).
8. **Voluntary disclosure of uncomfortable results** — APOE not passing FDR, REG3B demoted to an
   external hypothesis, the human-layer power limit, the docking EPVs. A1 flagged this as
   genuinely good practice.

---

## 8. Recommended handling paths

**Path A — revise substantially and resubmit as the same article type. RECOMMENDED.**
Required: fix the bootstrap and re-derive the stability claims (T0-1); make the deposit match the
data-availability statement and mint the Zenodo DOI (T0-2); resolve the spinal-AUC contradiction
(T0-3) and the Fig. 2A mismatch (T0-4); then work T1-1…T1-8 and T2/T3. This keeps the paper's
honest-null identity intact, because none of the fixes threaten the null — the docking null, the
translation null and the human-layer null all stand independently of the bootstrap.

**Path B — downgrade article type.** Not indicated. The work is a methods/benchmark contribution
and PLOS ONE accepts that; no evidence supports a different type.

**Path C — wording-only. NOT VIABLE.** Rejected explicitly. T0-1 requires re-running an analysis
and will **reverse** the direction of a stated conclusion; T0-2 requires actions outside the
manuscript (re-tag, track MANIFEST, create Zenodo); T1-4 requires either a new meta-analysis or a
new title. A wording-only pass would leave the manuscript asserting a stability conclusion that
the corrected code contradicts, and a data-availability statement that a technical check can
falsify.

**Sequencing suggestion.** Do the deposit fixes (T0-2, T3-1) first because they are mechanical and
block upload. Then the bootstrap fix and re-run (T0-1), because its output changes several
sentences. Then T0-3/T0-4, then T1, then T2/T3.

---

## 9. Process lessons — what the gates could not catch

1. **A gate that recomputes published numbers validates the *output*, never the *code that made
   it*.** Every stability number reproduced exactly — and was still wrong, because the script was
   wrong. New assertion: for every stability/bootstrap/permutation artefact, require a
   **positive-control self-test** in which a known-stable input must return a high stability
   score. The current scripts have no such test, which is why a mean XGBoost selection frequency
   of 0.086 (essentially random) was never questioned.
2. **Deposits drift from manuscripts silently.** No gate checks that the cited release *tag*
   contains the files the Data Availability statement names. New assertion: `git ls-tree -r
   <cited-tag> | grep -c <artefact-prefix>` must be > 0 for every artefact the manuscript says
   the release contains; and every file referenced by URL must be in `git ls-files`.
3. **Duplicate values inside one artefact.** The spinal-fold AUC appears twice in one paragraph
   with two different values. New assertion: extract every `AUC <number>` token in the manuscript
   and require that tokens referring to the same fold agree.
4. **Figures are not covered by text gates.** Fig. 2A silently plots the number the text walked
   back. New assertion: figure-generation scripts must read from the same leakage-controlled
   source the text cites.
5. **Synthetic self-test files must be gitignored by default.** A file named
   `_synthetic_selftest_DO_NOT_USE` was still tracked and still visible to any reviewer.
6. **The "disclosure ≠ resolution" rule paid off again.** T0-2 and T0-3 are both cases where a
   statement was qualified or corrected in one place while the unqualified version survived
   elsewhere (the deposit claim; the AUC). Grep for *values*, not locations.

---

## 10. A direct note to the author

The single strongest claim that does not hold is the **instability of the hub/target set**, and
its failure is not really your fault — it is a one-line indexing error that no amount of
re-reading the manuscript could have surfaced, because every number it produced was internally
consistent and reproduced perfectly. That is precisely why it survived several rounds: the
artefact looked like a finding.

But there is a genuine upside, and it is the finding you buried. Correct the alignment and the
target set turns out to be **stable** (median Jaccard 0.296, P(≥3 of 17) = 1.000, recovered-set
size 36). In other words, the pipeline reproduces its own target list — which is a *better*
result than the fragility you currently advertise, and it strengthens the paper rather than
weakening it. You are presently arguing that your target list is justified by structural
tractability *because* it is statistically unstable; once the bug is fixed you can argue it is
justified because it is **reproducible**, and keep structural tractability as a separate,
honest scope limit. Swapping those two converts a defensive caveat into a positive methodological
result, at no cost to the three nulls that are the paper's real contribution.

The second thing to fix before anything else is not scientific at all: make the deposit match the
data-availability sentence. Right now the manuscript says the v1.0.0 release contains the
random-effects and non-circular translation outputs, and it does not. That is the item most
likely to end the submission before review, and it is mechanical to fix.
