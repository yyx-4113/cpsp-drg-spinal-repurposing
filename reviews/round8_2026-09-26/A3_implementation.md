# Independent Provenance / Reproducibility Audit — Round 8 (Reviewer A3)

**Manuscript:** `reports/MVP_ScientificReports_submission.md`
**Remit:** Recompute every headline number from the raw source files in `results/tables/` and flag any mismatch with the manuscript. I did **not** treat the author's own `scripts/p7_consistency_gate.py` output as proof; every figure below was recomputed from the primary CSV/JSON artifacts.

---

## Headline reconciliation (manuscript value vs. independently recomputed)

| # | Manuscript headline | Recomputed from raw source | Verdict |
|---|---|---|---|
| 1a | FE core = **4,055** genes | `META_DRG_axis_CORE_signature.csv`: 4,055 rows; all satisfy meta_FDR<0.05 & consistency≥0.8 | ✅ match |
| 1b | RE core = **1,008**; τ²=0.232; I²=38.8% | `_R4_random_effects_meta.csv`: FDR_RE<0.05 & consistency≥0.8 = **1,008**; median τ²=**0.2324**, median I²=**38.79%**; 41.9% genes I²>50%; 68.1% τ²>0 | ✅ match |
| 1c | 16,552 genes tested; 6,869 at meta_FDR<0.05 | `META_DRG_axis_stouffer.csv`: 16,552 rows; 6,869 with meta_FDR<0.05 | ✅ match |
| 2a | Bulk-only core = **2,512** | `META_bulkonly_meta.csv`: 2,512 genes satisfy FDR<0.05 & consistency≥0.8 | ✅ match |
| 2b | Overlap 2,202 / 4,055 = **54.3%** | Set intersection primary∩bulk-only = **2,202**; 2,202/4,055 = **54.3%** | ✅ match |
| 3a | Neuroimmune / DAM / complement q = **0.003** each | `_R4_geneset_setlevel_bh.csv` (fixed, perm_q): Neuroinflammation 0.0029985, Complement 0.0029985, DAM_microglia 0.0029985 → 0.003 | ✅ match |
| 3b | OXPHOS FE q = **0.020**; RE q = **0.31** | `_R4_geneset_setlevel_bh.csv`: OXPHOS fixed perm_q 0.02024; random perm_q 0.31034 | ✅ match |
| 4 | Non-circular 46.3% vs 47.1%, **−0.9 pp**, p = **0.14** | `_R4_nerveinjury_only_summary.json`: all_measured 6,779/14,390 = 0.4711; stratum `NI_FDR05_AND_NIcons>=0.8` 2,266/4,899 = 0.4625; `strong_vs_background_pp` = −0.9; perm_p = 0.1396 | ✅ match (see Issue 4 re: source pointer) |
| 5 | LODO leakage-controlled **0.677 [0.374, 0.940]** | `P3_lodo_auc_ci_leakage_controlled.csv`: GSE267799 incision 0.6771 [0.3735, 0.9405] | ✅ match |
| 6a | ADRA2A 0.618 → 0.532, p = **0.118** | `P6_breadth_chembl_power.csv`: ADRA2A t1_only AUC 0.6184; full_library AUC 0.5325, p_mwu 0.1184. `P6_reverse_control.csv`: ADRA2A AUC 0.5325 | ✅ match |
| 6b | ADRA2A size-independent BH q = **0.0025** | `P6_BH_correction.csv`: BH_q_size_indep = 0.0025 | ✅ match; **does NOT contradict** "inconclusive, not a confirmed null" (see below) |
| 7 | Human miRNA set-level p = **0.51** (n=60) | `P4_setlevel_test.json`: perm_p = 0.5101 | ✅ match (source is the set-level file, not the per-miRNA CSV — see Issue 4) |
| 8 | 3,085 drugs; 30,850 poses; 30,687 scored; ~3,070/target | `P6_docking_scores_merged.csv`: unique drugs 3,085; 30,850 rows; scored=True 30,687; per-target scored 3,063–3,075. `P6_ligand_library.csv`: pass 3,085/3,311 = 93.17% | ✅ match |
| 9 | Dorsal-horn hubs **17/33** | `P5_GSE325938_hub_regionalization.csv`: detection_global>0 = 33; top_region==DorsalHorn among detectable = 17; all 17 ≥5% detection floor | ✅ match (source is GSE325938, not GSE216039 — see Issue 4) |

**Bottom line on the numbers:** Every one of the nine headline quantities recomputes exactly from the raw data and agrees with the manuscript. The substantive problems below are provenance, bibliographic, and transparency issues — not arithmetic errors.

---

## § Stands up (issues that hold, with evidence)

### Issue 1 — References 26 and 27 are listed but never cited in the text
【Problem】 Two bibliography entries (ref 26 Yousefpour 2025; ref 27 Kong 2023) appear in the reference list yet are never invoked by any in-text superscript citation.
【Evidence】 `MVP_ScientificReports_submission.md` lines 201–202 (Reference list); a scan of the body's superscript citations yields cited numbers {1–25, 28–33}; **26 and 27 are absent**. All 33 entries otherwise carry a `https://doi.org/...` URL.
【Why it matters】 Dangling references signal incomplete revision tracking and fail bibliographic-integrity checks; several journals auto-reject or require them removed, and it undermines the "every claim is sourced" discipline the manuscript asserts.
【Specific fix】 Either insert citations — e.g. in the DAM/C1q discussion ("…microbial C1q-mediated synaptic removal in neuropathic pain²⁶") and the microglial-metabolism paragraph ("…glycolysis enhancement in spinal microglia²⁷") — or delete refs 26 and 27 from the list.

### Issue 2 — Data-availability statement claims a Zenodo mirror with an unmet placeholder DOI
【Problem】 The Data availability section asserts a Zenodo archive "mirrors the GitHub release v1.0.0 (DOI: 10.5281/zenodo.XXXXXXX — to be minted at submission)" while simultaneously stating "Data are not 'available on request'."
【Evidence】 `MVP_ScientificReports_submission.md` line 222; `.zenodo.json` contains no minted DOI field — only title/creators/version metadata.
【Why it matters】 Presenting a non-existent mirror as an existing archival resource is a misleading availability claim; the "not available on request" stance is internally inconsistent with a placeholder that implies a live mirror. Some journals require the DOI to be live or explicitly pending-at-acceptance.
【Specific fix】 Mint the Zenodo deposit before submission and insert the real DOI, **or** rephrase to "a Zenodo archive will be minted upon acceptance" and strike "mirrors the GitHub release v1.0.0" until it exists.

### Issue 3 — Bulk-contrast w² range is misstated as "1.00–7.02"
【Problem】 The heterogeneity/weighting argument states GSE265957's w² = 2.00 "versus 1.00–7.02 for the four bulk contrasts," but the actual bulk w² values are 4.80, 1.50, 7.00, and 2.22 — a range of **1.50–7.00**, not 1.00–7.02. The value 1.00 is GSE265957's *per-timepoint* weight, not a bulk value.
【Evidence】 `META_bulkonly_sensitivity_summary.json` (contrast_info weights): GSE267799 w=2.1909 (w²=4.80), GSE212311 w=1.2247 (w²=1.50), GSE278227 w=2.6458 (w²=7.00), GSE241361_DRG w=1.4907 (w²=2.22). Manuscript line 44.
【Why it matters】 The translatome double-counting argument is a central honesty claim; misstating the bulk w² floor understates how much heavier the largest bulk study (GSE278227, w²=7.00) weighs relative to the two GSE265957 timepoints (w²=1.00 each) and could mislead a reader auditing the sensitivity logic.
【Specific fix】 Replace "1.00–7.02 for the four bulk contrasts" with "1.50–7.00 for the four bulk contrasts (GSE265957 per-timepoint w² = 1.00)."

### Issue 4 — Source pointers in the audit brief diverge from the manuscript's own (correct) citations; a superseded exploratory file remains in `results/tables/`
【Problem】 Three headline figures are reproducible only from files *different* from those named in the audit brief, and a superseded exploratory file containing divergent numbers is still shipped in `results/tables/`:
- The non-circular translation headline (46.3% / 47.1% / −0.9 pp / p=0.14) reproduces **only** from `_R4_nerveinjury_only_summary.json` (stratum `NI_FDR05_AND_NIcons>=0.8`) — which the manuscript correctly cites. The file named in the brief, `_R4_translation_noncircular.json`, holds *different, superseded* strata (all_measured 7,751/14,445 = 53.66%; meta_FDR05_NIcons_ge08 2,318/4,306 = 53.83%; `noncircular_risk_difference_pp` = −11.8) and is explicitly described by the manuscript (line 58) as "superseded."
- The 17/33 dorsal-horn figure reproduces from `P5_GSE325938_hub_regionalization.csv`, **not** `P5_GSE216039_DRG_hub_localisation.csv` (the latter is the DRG neuron-subtype localisation; GSE216039 has no dorsal-horn anatomy).
- The human-miRNA set-level p=0.51 reproduces from `P4_setlevel_test.json` (perm_p=0.5101), not `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` (which holds per-miRNA LSSDS-vs-LSS statistics; its min FDR = 0.128, correctly cited separately).
【Evidence】 File reads of the three named files vs. the producing files; manuscript lines 58, 70, 78, 222 (inline citations are correct).
【Why it matters】 Leaving superseded exploratory artifacts in the data release and mislabeled source pointers invites reproducibility confusion; although the manuscript's inline citations are correct, the presence of a divergent `_R4_translation_noncircular.json` (with denominators 14,445/3,564 the manuscript itself calls superseded) is a provenance hazard for any third-party auditor.
【Specific fix】 Move `_R4_translation_noncircular.csv` / `.json` (and any other exploratory outputs) to an `_deprecated/` subfolder or delete them; ensure every manuscript source pointer names the actual producing file.

### Issue 5 — Collapse-sensitivity headline (core 4,294; 3,707/4,055 = 91.4%) has no source artifact in `results/tables/`
【Problem】 Table 1a reports a collapse-sensitivity meta (merging GSE265957 D4/D63 into one contrast) giving core = **4,294** and retained **3,707/4,055 = 91.4%**, but no `META_collapse_*.csv` (or companion summary) exists in `results/tables/`; only the bulk-only and random-effects companions are present.
【Evidence】 Directory listing of `results/tables/` (no collapse file); manuscript lines 146, 254.
【Why it matters】 A headline sensitivity number that cannot be regenerated from the provided data breaks the reproducibility contract this manuscript is built around.
【Specific fix】 Deposit `META_collapse_meta.csv` (plus a summary JSON) in `results/tables/`, or — if the artifact is genuinely unavailable — drop the collapse-sensitivity figure and keep only bulk-only and random-effects as the two reported robustness checks.

### Issue 6 — `P5_GSE325938_hub_regionalization.csv` `present` column is uniformly True despite 33/35 detectable
【Problem】 The `present` flag equals True for all 35 hubs, even though the manuscript correctly states only 33/35 are detectably expressed (CRISP3 and LNP1 have `detection_global` = 0). A reader filtering on `present` would wrongly conclude 35/35 detectable.
【Evidence】 File read: `present` unique value = {True}; `detection_global`==0 only for CRISP3 and LNP1; `present & detection_global>0` = 33. Manuscript line 78.
【Why it matters】 The column's semantics contradict the manuscript's own denominator and could propagate a false detectability count in any downstream reuse.
【Specific fix】 Rename the column to reflect "in-table" or set `present=False` where `detection_global`==0; add an explicit `detectably_expressed` boolean.

*(Minor consistency note, not a separate stand-up: the core-restricted concordance denominator is 3,556 in the text [line 56: 2,473/3,556 = 69.5%] versus n=3,564 in the superseded `_R4_translation_noncircular.json`. Resolved by Issue 4's file removal.)*

---

## § Questions for the authors

1. **References 26 & 27.** Will you cite them in-text (DAM/C1q and microglial glycolysis discussions) or remove them? They are currently orphaned.
2. **Zenodo.** Is the Zenodo deposit actually minted, or is the DOI a pre-submission placeholder? The data-availability text currently asserts a mirror that does not yet exist.
3. **GSE265957 independence.** The claim that the D4 and D63 translatome timepoints come from the *same animals* (and are therefore not independent) is author-asserted; it is not verifiable from `META_DRG_axis_stouffer.csv` weights (both timepoints correctly carry w=1.00, i.e. n_case=n_ctrl=2). Please confirm this is documented in the original GEO deposition, not inferred.
4. **Collapse-sensitivity artifact.** Can you provide `META_collapse_meta.csv` so the 4,294 / 91.4% figure is reproducible, or should it be withdrawn?
5. **ADRA2A "inconclusive" framing.** The size-independent BH q = 0.0025 is formally significant while the raw full-library AUC (0.532, p=0.118) is not. The manuscript's "inconclusive, not a confirmed null" wording is internally consistent with the BH table, but we want to confirm you intend to keep ADRA2A explicitly *outside* any "validated hit" claim — which the current text does. No contradiction found; this is a clarification.
6. **`present` column.** Will you correct the misleading `present` flag in the Visium regionalisation table before release?

---

## § What I actually checked

**Files read (raw sources):**
- `META_DRG_axis_CORE_signature.csv`, `META_DRG_axis_stouffer.csv`, `_R4_random_effects_meta.csv`, `META_bulkonly_meta.csv`, `META_bulkonly_sensitivity_summary.json` (items 1, 2, GSE265957 weights)
- `P3_geneset_stats.csv`, `_R4_geneset_setlevel_bh.csv` (item 3)
- `_R4_nerveinjury_only_summary.json`, `_R4_translation_noncircular.json` (item 4)
- `P3_lodo_auc_ci_leakage_controlled.csv`, `P3_lodo_auc_ci.csv` (item 5)
- `P6_breadth_chembl_power.csv`, `P6_reverse_control.csv`, `P6_BH_correction.csv` (item 6)
- `P4_setlevel_test.json`, `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` (item 7)
- `P6_docking_scores_merged.csv`, `P6_ligand_library.csv`, `P6_param_summary.csv` (item 8)
- `P5_GSE325938_hub_regionalization.csv`, `P5_GSE216039_DRG_hub_localisation.csv` (item 9)
- `_R4_ref_DOIs.json` (ref 31 DOI), `MVP_STROBE_checklist.md`, `submission_pack/Manuscript.docx` (core.xml + document.xml), `.zenodo.json`, `CITATION.cff`
- Manuscript `MVP_ScientificReports_submission.md` in full (headers, Results, Methods, References, Display items)

**Recomputations performed (every headline value, with discrepancy stated):**
- Counted FE core rows = 4,055; RE core (FDR_RE<0.05 & consistency≥0.8) = 1,008; median τ² = 0.2324, median I² = 38.79%; fraction I²>50% = 41.9%; fraction τ²>0 = 68.1%. *No discrepancy.*
- Counted bulk-only core = 2,512; set-overlap with primary = 2,202 (54.3%). *No discrepancy.*
- Read set-level BH q-values: three upregulated programmes = 0.0029985 → 0.003; OXPHOS fixed 0.02024 → 0.020; OXPHOS random 0.31034 → 0.31. *No discrepancy.*
- From `_R4_nerveinjury_only_summary.json`: background 6,779/14,390 = 0.4711 (47.1%); stratum 2,266/4,899 = 0.4625 (46.3%); `strong_vs_background_pp` = −0.9; perm_p = 0.1396 (0.14). *No discrepancy with the manuscript's cited file.* The brief's named file `_R4_translation_noncircular.json` instead reports 53.66% / 53.83% / −11.8 pp — divergent, superseded numbers (see Issue 4).
- From leakage-controlled LODO CSV: GSE267799 incision = 0.6771 [0.3735, 0.9405]. All five folds: GSE278227 1.0 (n=28), GSE267799 0.677 [0.374, 0.940] (n=20), GSE241361 DRG 1.0 (n=9), GSE241361 SC 1.0 (n=9), GSE212311 1.0 (n=6). Cross-checked against non-leakage `P3_lodo_auc_ci.csv`: GSE267799 0.9167 [0.729, 1.0], GSE241361 SC 0.950 [0.709, 1.0] — both match the narrative. *No discrepancy.*
- ADRA2A: Tier-1 AUC 0.6184, full-library AUC 0.5325, p_mwu 0.1184; size-independent BH q = 0.0025. *No discrepancy; no contradiction with "inconclusive" framing* (size-independent passes BH, raw full-library does not).
- Human-miRNA set-level perm_p = 0.5101 (0.51). *No discrepancy* (note: source is `P4_setlevel_test.json`, not the per-miRNA CSV named in the brief).
- Docking: 3,085 unique drugs; 30,850 pose rows; 30,687 scored=True; per-target scored 3,063–3,075 (≈3,070); library pass 3,085/3,311 = 93.17%. *No discrepancy.*
- Visium dorsal horn: 33 detectable (detection_global>0), 17 assigned DorsalHorn, all 17 ≥5% detection floor. *No discrepancy* (source is GSE325938, not GSE216039 as brief states).
- References: all 33 entries carry a `doi.org` URL; ref 31 = 10.1073/pnas.122231899 matches `_R4_ref_DOIs.json` key `xiao2002`. **Discrepancy found: refs 26 and 27 are never cited in the body** (Issue 1).
- STROBE: checklist title matches manuscript title exactly; STROBE version "2007" matches. *No discrepancy.*
- `Manuscript.docx`: core title matches; creator "Yang Y"; 5 inline shapes (`wp:inline`) = the 5 figures. *No discrepancy.*
- GSE265957 weights: bulk w² = 4.80 / 1.50 / 7.00 / 2.22 (range 1.50–7.00); GSE265957 per-timepoint w² = 1.00, combined 2.00. **Discrepancy found: manuscript states bulk range "1.00–7.02" (Issue 3).**
- Zenodo: placeholder `10.5281/zenodo.XXXXXXX` present; no minted DOI in `.zenodo.json` (Issue 2).
- Collapse-sensitivity: no source artifact present for the 4,294 / 91.4% figure (Issue 5).

**Net assessment:** All nine quantitative headline claims are reproducible and correct. The audit surfaces six provenance/editorial/transparency issues (two of which — orphaned refs 26/27 and the Zenodo placeholder claim — are substantive enough to require author action before submission).
