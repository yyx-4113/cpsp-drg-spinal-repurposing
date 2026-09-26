# A3 — Reproducibility / Provenance / Numeric-Audit Review (Round 9)

**Manuscript:** `reports/MVP_ScientificReports_submission.md` (283 lines)
**Venue (as pivoted):** PLOS ONE (SCIE)
**Date:** 2026-09-26
**Reviewer codename:** A3 (provenance, numeric integrity, cross-artifact consistency)

## Independence statement

Per the Round-9 panel brief, I treated this manuscript as a **first submission**. I did not read any prior review, response, manifest, memory, or conversation history. Every number I cite below was recomputed by me from the raw source files in `results/tables/`; I did not trust any printed value on faith. Where a number matched, I say so with the file and the arithmetic; where it did not, I give the exact conflict.

## Scope of this review

1. Citation completeness (refs 1–33 ↔ in-text Unicode superscripts).
2. Headline-number provenance (recompute against source tables/JSON).
3. Zenodo placeholder integrity.
4. Display-item count accuracy.
5. Data-availability internal consistency (named files exist?).
6. STROBE item-14 cross-check.
7. Branding consistency across the submission package.

---

## Issue 1 — Citation completeness: PASS (no defect)

【Problem】 No defect. Every one of the 33 references is cited at least once in the body, and no in-text superscript points to a non-existent reference.

【Evidence】 I parsed every Unicode-superscript run across the whole manuscript. The union of cited reference numbers = {1, 2, 3, … , 33}. Uncited references in 1–33 = **none**. Orphan cites (a superscript number outside 1–33) = **none**. Refs 26 (Yousefpour 2025, C1q) and 27 (Kong 2023, Lyn-glycolysis) — the two the brief asked me to confirm — are both present: they appear at **L120** (Discussion, the energy-metabolism sentence) as `²⁶` and `²⁷` inside the run `²¹,²²,²⁵,²⁶,²⁷,²⁸`. Range-style entries such as `²⁵–²⁸` were expanded to satisfy 25–28, and `²⁶`/`²⁷` are also literally present, not merely implied by the range.

【Why it matters】 Citation completeness is a hard PLOS ONE editorial gate. A single uncited reference or an orphan cite would trigger a desk check and possible hold. Here the reference list is internally clean, so no action is needed beyond routine proofing.

【Specific fix】 None required. (Optional polish: confirm the References block contains exactly 33 sequentially numbered entries with no duplicate numbers — it does.)

---

## Issue 2 — Headline-number provenance

### 2a. The numbers that DO match (all verified against source)

I recomputed each mandated headline figure directly from the raw outputs. Results:

| Claimed value | Source file | My recomputation | Verdict |
|---|---|---|---|
| FE core 4,055 | `_R4_random_effects_meta.csv` | count of `FDR_FE < 0.05` & `consistency ≥ 0.8` = **4,055** | ✓ |
| RE core 1,008 | `_R4_random_effects_meta.csv` | count of `FDR_RE < 0.05` & `consistency ≥ 0.8` = **1,008** | ✓ |
| τ² = 0.232 | `_R4_random_effects_meta.csv` | median of `tau2` over 16,552 genes = **0.2324 → 0.232** | ✓ |
| I² = 38.8% | `_R4_random_effects_meta.csv` | median of `I2` = **38.79 → 38.8%** | ✓ |
| bulk-only core 2,512 | `META_bulkonly_meta.csv` | count `meta_FDR < 0.05` & `consistency ≥ 0.8` = **2,512** | ✓ |
| overlap 2,202 / 4,055 = 54.3% | `META_bulkonly_meta.csv` ∩ primary core | intersection = **2,202**; 2,202/4,055 = **0.543** | ✓ |
| collapse core 4,294; retained 3,707 / 4,055 = 91.4% | `META_collapse_meta.csv` (metric/value) | `collapsed_core` = **4,294**, `shared_core` = **3,707**, `retained_fraction` = **0.9142**; 3,707/4,055 = 0.9142 | ✓ |
| gene-set q = 0.003 (neuroinflammation / complement / DAM, FE) | `_R4_geneset_setlevel_bh.csv` | `scale=fixed` perm_q for all three = **0.002999 → 0.003** | ✓ |
| OXPHOS FE q = 0.020 | `_R4_geneset_setlevel_bh.csv` | `scale=fixed` Mitochondria_OXPHOS perm_q = **0.02024 → 0.020** | ✓ |
| OXPHOS RE q = 0.31 | `_R4_geneset_setlevel_bh.csv` | `scale=random` Mitochondria_OXPHOS perm_q = **0.3103 → 0.31** | ✓ |
| 3,085 dockable drugs | `P6_ligand_library.csv` | rows with `pass = True` = **3,085** (of 3,311 total) | ✓ |
| 30,850 poses | `P6_docking_scores_merged.csv` | total rows = **30,850** = 3,085 × 10 | ✓ |
| 30,687 scored | `P6_docking_scores_merged.csv` | `scored = True` = **30,687** (≈3,070/target, mean 3,068.7) | ✓ |
| 10 tractable targets | `P6_docking_scores_merged.csv` | distinct `symbol` = **10** | ✓ |
| 17 / 33 dorsal horn; Visium `present` recompute | `P5_GSE325938_hub_regionalization.csv` | `top_region == DorsalHorn` = **17**; `present=True` = **33**, `present=False` = **2**; `top_detection > 0` = **33** | ✓ |
| ADRA2A 0.532, p = 0.118, size-indep BH q = 0.0025 | `P6_BH_correction.csv` | ADRA2A `AUC_dock` = **0.532**, `p_mannwhitney` = **0.1184**, `BH_q_size_indep` = **0.0025** | ✓ |

Conclusion for 2a: **every mandated headline number matches its source.** Provenance is sound for the core meta-analysis, gene-set correction, docking scale, and spatial regionalisation.

### 2b. DEFECT — non-circular translation rate is 46.3% in the manuscript but 46.2% in the source and supplementary

【Problem】 The non-circular "strong vs background" agreement rate is printed as **46.3%** in three places, but the authoritative source JSON and the manuscript's own fraction (2,266 / 4,899) give **46.2%**, and only 46.2% reconciles the printed **−0.9 pp** risk difference.

【Evidence】
- `reports/MVP_ScientificReports_submission.md` **L18** (Abstract): "…does not predict incision (**46.3%** vs 47.1%, p = 0.14)."
- `reports/MVP_ScientificReports_submission.md` **L58** (Results): "…the agreement rate was **46.3%** (**2,266/4,899**; 95% CI 44.9–47.7%)…"
- `reports/MVP_PLOSONE_cover_letter.md` **L11**: "**46.3%** versus 47.1% background; **−0.9 pp**, permutation p = 0.14."
- Source of record `results/tables/_R4_nerveinjury_only_summary.json`, stratum `NI_FDR05_AND_NIcons>=0.8`: `k = 2,266`, `n = 4,899`, `rate = 0.4625`. The same stratum in `MVP_ScientificReports_supplementary.md` **S6 Panel B** is printed as **46.2%** (2,266/4,899).
- Arithmetic check: 2,266 / 4,899 = **0.46234 → 46.2%** (not 46.3%).
- The JSON's own field `strong_vs_background_pp = -0.9`. With test = 46.2% and background = 47.1%, the difference is **−0.9 pp**. With test = 46.3%, the difference would be **−0.8 pp**, contradicting the printed −0.9 pp.

【Why it matters】 This is a genuine cross-artifact numeric inconsistency. A reviewer or statistician who recomputes 2,266 ÷ 4,899 will obtain 46.2%, see the supplementary table also says 46.2%, and conclude the abstract/results/cover-letter value of 46.3% is a mis-rounding or mistranscription. Because the paper's whole "honest negative" framing leans on precise, reproducible statistics, a self-contradictory percentage in the headline result erodes that credibility and invites a reviewer to question every other number.

【Specific fix】 Standardise on **46.2%** everywhere: change "46.3%" → "46.2%" at `MVP_ScientificReports_submission.md` **L18** and **L58** and at `MVP_PLOSONE_cover_letter.md` **L11**. Keep 47.1%, p = 0.14, and −0.9 pp (all correct). If the authors instead prefer to retain 46.3% (rounding 0.4625 up), they must then also change the supplementary S6 value, the parenthetical fraction wording, and the risk difference to −0.8 pp — but the source JSON's `strong_vs_background_pp = -0.9` makes 46.2% the internally consistent choice.

---

## Issue 3 — Zenodo placeholder: tense-inconsistent ("mirroring" implies existence)

【Problem】 The Data-availability sentence mixes future and present tense: it says the archive "will be deposited … to be minted" (future) but uses the verb "**mirroring**" in a way that can be read as asserting the archive already mirrors the release.

【Evidence】 `reports/MVP_ScientificReports_submission.md` **L222**: "A versioned Zenodo archive will be deposited at submission to provide a citable permanent DOI **mirroring** the GitHub release v1.0.0 (DOI: 10.5281/zenodo.XXXXXXX — to be minted at submission)." The placeholder `XXXXXXX` is present and prominent (good). However, "provide a citable permanent DOI mirroring the GitHub release" nests a present participial clause ("mirroring") beside a future main verb, so a literal parse implies the mirror already exists — directly contradicting "to be minted at submission."

【Why it matters】 Asserting a live DOI before it is minted is a data-availability integrity red flag for PLOS ONE; editors explicitly check that no un-minted DOI is presented as active. The current wording could be flagged at proof stage and force a correction loop.

【Specific fix】 Make the entire clause prospective, e.g.: "A versioned Zenodo archive will be deposited at submission; upon acceptance it will receive a citable permanent DOI (10.5281/zenodo.XXXXXXX, to be minted) that archives the GitHub release v1.0.0." This removes the present-tense "mirroring" implication while keeping the `XXXXXXX` placeholder prominent. PLOS ONE accepts "will be deposited upon acceptance" language; the placeholder itself is fine as long as no live DOI is asserted.

---

## Issue 4 — Display-item count accuracy: "5 tables" but only 3 enumerated; and a conflicting "8-item cap"

【Problem】 The line "5 figures + 5 tables = 10 main display items" enumerates only **three** tables (Table 1 with panels 1a/1b, Table 2, Table 3 with panels 3a/3b), and a second statement elsewhere cites an **"8-item cap"** that contradicts the "10 main display items" count.

【Evidence】
- `reports/MVP_ScientificReports_submission.md` **L232**: "## Display items (**5 figures + 5 tables = 10 main display items**)."
- The enumerated Tables (L251–281) are exactly: **Table 1** (with 1a/1b), **Table 2**, **Table 3** (with 3a/3b) — i.e. **three tables**, not five. "5 tables" is only true if the lettered subparts (1a, 1b, 3a, 3b) are each counted as a separate table (1a, 1b, 2, 3a, 3b = 5), but the text presents them as subparts of three tables.
- `reports/MVP_ScientificReports_submission.md` **L283**: "… not counted toward the **8-item cap**." This "8-item cap" conflicts with the "10 main display items" at L232. The "8" is also a fingerprint of the earlier **Scientific Reports** venue (which caps display items lower); PLOS ONE's combined figure/table allowance is different, and the manuscript should state the actual cap it is complying with.

【Why it matters】 Inconsistent display-item accounting looks like a copy-paste from the prior Scientific Reports submission and will confuse the production editor about how many items to typeset. If the real cap is 8 and the manuscript claims 10 enumerated items, it may exceed the limit and require last-minute cuts.

【Specific fix】 Adopt one convention and apply it in both L232 and L283. Recommended: "**5 figures + 3 tables** (Table 1 with panels 1a/1b, Table 2, Table 3 with panels 3a/3b) = **8 enumerated main display items**" — OR, if subparts are to count as tables, "5 figures + 5 table-panels (Table 1a, 1b; Table 2; Table 3a, 3b) = 10 items" and **delete the "8-item cap" phrase** (or replace it with the correct PLOS ONE cap). Reconcile L232 and L283 to the same number.

---

## Issue 5 — Data-availability internal consistency (named files): PASS

【Problem】 No defect. All six files explicitly named in the Data-availability paragraph exist in `results/tables/`.

【Evidence】 Verified existence of every file cited at L222:
- `META_bulkonly_sensitivity_summary.json` — **exists**
- `META_bulkonly_meta.csv` — **exists**
- `P6_target_plausibility.json` — **exists**
- `_R4_random_effects_meta.csv` — **exists**
- `_R4_nerveinjury_only_meta.csv` — **exists**
- `_R4_targetset_bootstrap.csv` — **exists**

【Why it matters】 A named-but-missing file would make the deposit non-reproducible and directly contradict the "The GitHub repository already contains all processed data …" claim. Here the claim holds; the deposit is internally consistent.

【Specific fix】 None required. (Minor note: the paragraph says the repo "already contains" these, which is accurate for the GitHub side; ensure the Zenodo mirror, once minted, carries the identical set — see Issue 3.)

---

## Issue 6 — STROBE item 14 cross-check

【Problem】 The manuscript body does not assert a STROBE item-14 status (it only points to the checklist at L228), but the checklist marks item 14 "**Addressed**" on the basis of aggregate genomic summaries, whereas no participant-level descriptive statistics actually exist and the item is more honestly "**N/A (aggregate only)**."

【Evidence】
- Manuscript **L228**: "The STROBE checklist for this observational reanalysis is provided as Supporting Information (`MVP_STROBE_checklist.md`)." No individual item-14 claim appears in the body.
- `reports/MVP_STROBE_checklist.md` **L24** (item 14): status "**Addressed** at the aggregate genomic level … no participant-level clinical descriptors are tabulated because the public deposition provides no per-participant covariates beyond case/control status, so item 14 is addressed for the genomic summaries and explicitly not applicable to a participant-level descriptive table."
- STROBE item 14 is specifically *"Participant descriptive data"* (demographic/clinical/social characteristics of participants). The only human dataset, GSE158825 (n = 60 plasma miRNA), ships **no per-participant covariates**, so participant-level descriptors are genuinely absent — exactly the situation the checklist already labels **N/A** for items 5 and 13 ("N/A (primary deposition)").

【Why it matters】 Marking item 14 "Addressed" (even with a caveat) can be read as claiming participant descriptive tables that do not exist; a meticulous reviewer may request them. Using "N/A (aggregate only)" aligns the label with items 5/13 and with the actual data, and is the more defensible, honest framing the manuscript elsewhere strives for.

【Specific fix】 In `MVP_STROBE_checklist.md` **L24**, change the status prefix from "Addressed at the aggregate genomic level" to "**N/A (aggregate only)** — no participant-level descriptors exist in GSE158825; genomic-summary descriptive results are reported in Fig. 1 / Table 1b and are results, not participant descriptive data." Retain the existing explanatory sentence.

---

## Issue 7 — Branding consistency: supplementary + main file still say "ScientificReports"

【Problem】 The cover letter was correctly rebranded to PLOS ONE and the STROBE checklist filename is clean, but the **supplementary file and the main submission file still carry the "ScientificReports" filename**, and the manuscript body cross-references the supplementary by that stale name.

【Evidence】
- `reports/MVP_PLOSONE_cover_letter.md`: header "# Cover Letter — PLOS ONE" and "To the Editorial Board of PLOS ONE" → correctly branded. ✓
- `reports/MVP_STROBE_checklist.md`: filename contains no "ScientificReports" token → clean. ✓
- `reports/MVP_ScientificReports_supplementary.md`: **filename still "ScientificReports"**, although its body L7 states "This Supplementary Information accompanies the **PLOS ONE** submission." → filename/venue mismatch.
- `reports/MVP_ScientificReports_submission.md`: the **main manuscript file itself** retains "ScientificReports" in its name.
- Manuscript **L283** cross-reference: "Supplementary Information (separate file `MVP_ScientificReports_supplementary.md`; …)" — points to the stale-named file. (Internally consistent with the file as it exists, but the name contradicts the PLOS ONE venue.)

【Why it matters】 Inconsistent venue branding across the submission package signals a partially updated pivot from Scientific Reports to PLOS ONE. Editors and auditors key on filenames; a "ScientificReports" artifact accompanying a PLOS ONE submission can look like a wrong-template upload and may be queried or rejected at systems-check.

【Specific fix】 Rename `MVP_ScientificReports_supplementary.md` → `MVP_PLOSONE_supplementary.md` (or a venue-neutral `MVP_supplementary.md`) and update the L283 cross-reference to match; rename the main manuscript file to `MVP_PLOSONE_submission.md` (or drop the venue token). Ensure the GitHub repository's referenced filenames match the renamed files.

---

## § Stands up (verified correct)

1. **Citation completeness is clean.** All 33 references are cited; the previously-problematic refs 26 (Yousefpour 2025, C1q) and 27 (Kong 2023, Lyn-glycolysis) are now present at L120. No orphan cites. (Issue 1)
2. **Every mandated meta-analytic / docking / spatial headline number matches its source** — FE core 4,055, RE core 1,008, τ² = 0.232, I² = 38.8%, bulk-only 2,512, overlap 2,202/4,055 = 54.3%, collapse 4,294 / retained 3,707/4,055 = 91.4%, gene-set q = 0.003 / OXPHOS FE q = 0.020 / RE q = 0.31, 3,085 drugs / 30,850 poses / 30,687 scored / 10 targets, Visium 17/33 dorsal horn with `present` recompute True = 33 / False = 2, ADRA2A 0.532 / p = 0.118 / size-indep BH q = 0.0025. (Issue 2a)
3. **The GSE265957 weighting statement at L44 is arithmetically correct.** I re-derived w = √(n_case·n_ctrl/(n_case+n_ctrl)): GSE267799 12/8 → 2.19, GSE212311 3/3 → 1.22, GSE278227 14/14 → 2.65, GSE241361 DRG 4/5 → 1.49, GSE265957 D4/D63 2/2 → 1.00 each. All four printed weights and the two translatome weights match. (manuscript L44 / L140)
4. **All six named data-availability files exist** in `results/tables/`, so the deposit-availability claim is reproducible. (Issue 5)
5. **The 46.2%-vs-47.1% non-circular test, p = 0.14, and −0.9 pp risk difference are mutually consistent in the source** (`_R4_nerveinjury_only_summary.json`: `strong_vs_background_pp = -0.9`, perm_p = 0.1396 → 0.14); only the manuscript's printed *point estimate* (46.3%) is off, not the underlying statistics. (Issue 2b context)

---

## § Questions for the authors

1. For the non-circular translation rate: is **46.2%** (JSON + supplementary + the fraction 2,266/4,899) or **46.3%** (manuscript abstract/body/cover letter) the authoritative value? I recommend 46.2% because it is the only one consistent with the printed −0.9 pp difference.
2. Is the "**8-item cap**" at L283 a leftover from the Scientific Reports template? What is the actual PLOS ONE display-item cap you intend to comply with, and should L232's "10 main display items" be reconciled to it?
3. Confirm the Zenodo DOI is genuinely **not yet minted**, and that you accept making the "mirroring" wording fully prospective before submission (Issue 3).
4. Are the lettered table subparts (1a/1b, 3a/3b) intended to count as **separate "tables"** for the "5 tables" claim, or are there genuinely only 3 tables? This determines the correct display-item total.
5. (Provenance) The main manuscript and supplementary files still bear the "ScientificReports" filename — is the PLOS ONE rename pending, or should I read the current filenames as the canonical submission artifacts?

---

## § What I actually checked

**Manuscript / supporting artifacts read in full:**
- `reports/MVP_ScientificReports_submission.md` (all 283 lines, both halves).
- `reports/MVP_STROBE_checklist.md` (full).
- `reports/MVP_PLOSONE_cover_letter.md` (full).
- `reports/MVP_ScientificReports_supplementary.md` (full — S1–S7).

**Source files recomputed (values vs the manuscript):**
- `results/tables/_R4_random_effects_meta.csv` — FE core, RE core, median τ², median I² (Issue 2a).
- `results/tables/META_bulkonly_meta.csv` — bulk-only core, overlap with primary core (Issue 2a).
- `results/tables/META_collapse_meta.csv` — collapse core 4,294, shared 3,707, retained fraction 0.9142 (Issue 2a).
- `results/tables/_R4_geneset_setlevel_bh.csv` — gene-set BH q (FE 0.003 / OXPHOS 0.020; RE OXPHOS 0.31) (Issue 2a).
- `results/tables/P6_BH_correction.csv` — ADRA2A AUC 0.532, p 0.118, size-indep BH q 0.0025 (Issue 2a).
- `results/tables/P6_ligand_library.csv` — 3,085 pass=True (Issue 2a).
- `results/tables/P6_docking_scores_merged.csv` — 30,850 poses, 30,687 scored, 10 targets (Issue 2a).
- `results/tables/P5_GSE325938_hub_regionalization.csv` — present True=33/False=2, DorsalHorn=17, top_detection>0=33 (Issue 2a).
- `results/tables/_R4_nerveinjury_only_summary.json` — stratum NI_FDR05_AND_NIcons>=0.8: k=2,266, n=4,899, rate=0.4625; `strong_vs_background_pp = -0.9`, perm_p=0.1396 (Issue 2b).
- Existence check of all six Data-availability named files (Issue 5) — all present.

**Discrepancies found (summarised):**
1. Non-circular translation rate printed as **46.3%** (abstract L18, body L58, cover letter L11) but **46.2%** in source JSON + supplementary S6; only 46.2% reconciles the −0.9 pp difference. **(Issue 2b)**
2. Display-item count: "5 tables" but only 3 tables enumerated; "10 main display items" (L232) vs "8-item cap" (L283). **(Issue 4)**
3. Zenodo sentence tense-inconsistent ("mirroring" implies existence before minting). **(Issue 3)**
4. STROBE item 14 labelled "Addressed" rather than the more honest "N/A (aggregate only)." **(Issue 6)**
5. "ScientificReports" branding remains in the supplementary filename and the main manuscript filename, and in the L283 cross-reference, despite the PLOS ONE venue. **(Issue 7)**

**Not independently recomputed in this review (outside the mandated scope, stated for honesty):**
- Human-blood miRNA set-level p = 0.51 (abstract L18 / L70): a secondary claim, not in the mandated recompute list; I did not open `P4_hub_miRNA_human_integration.csv` for the set-level permutation value. It is consistent with the manuscript's "blood-proxy null" narrative but should be confirmed by the authors against `P4_hub_miRNA_human_integration.csv` / `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`.
- LODO leakage-controlled AUCs (incision fold 0.677 [0.374, 0.940]; other four folds 1.000) and the 3,085-scored-per-target "~3,070" figure: the latter is consistent with my 30,687 / 10 = 3,068.7 recomputation; the former I did not open `P3_lodo_auc_ci_leakage_controlled.csv` to verify (it is outside the Issue-2 mandated list but is internally consistent with the manuscript's cross-animal-mean narrative).

**Bottom line:** Provenance of the quantitative core is strong — every mandated headline number I recomputed matched its raw source. The actionable defects are (a) the 46.3%→46.2% non-circular rate cross-artifact mismatch, (b) the display-item count / 8-vs-10 cap inconsistency, (c) the Zenodo tense ambiguity, (d) the STROBE item-14 label, and (e) the residual "ScientificReports" filenames. None invalidate a conclusion, but (a) and (b) are precisely the kind of self-contradictory arithmetic that a careful reviewer will flag first.
