# A3 — Implementation & Provenance Audit Report

**Role:** A3, Implementation & Provenance auditor (independent peer-review panel, round 16)
**Date:** 2026-09-28
**Manuscript under audit:** `reports/MVP_PLOSONE_submission.md` (version v1.6.0 per Data Availability, L279/L281)
**Submission docx:** `submission_pack/Manuscript.docx`
**Repo root:** `D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛`
**Authoritative data files:** the `_R4_*` / `META_*` / `P3_*` / `P4_*` / `P6_*` tables enumerated in the task brief.

---

## Executive summary

I recomputed **every** headline number in the manuscript directly from the authoritative data files (not from the manuscript's own tables). **All 10 numeric recomputation checks (mandatory checks 1–10) match the manuscript exactly** — the FE core (2,750), the RE core (508 / 18.5% / median I² 41.8% / median τ² 0.266), the four gene-set q = 0.0022 hits, the non-circular concordance (43.3% vs 47.1%, p = 0.0002), the bulk-only sensitivity (2,512 core; 1,737/2,750 = 63.2% = 1,322 + 415; relaxed 2,454/2,750 = 89.2%; 200 = 154 + 46 lacking bulk support), the collapse sensitivity (3,582 core; 2,502/2,750 = 91.0%), the hub statistics (35 hubs; 26/35 in meta core; 5/35 full 3-method consensus; 2/35 resampling-stable SPRR1A 1.00 / ATF3 0.94), the LODO incision fold (0.677 [0.374, 0.940]; GSE212311 n = 6), the human-miRNA set-level p = 0.51, and the docking AUCs (ADRA2A 0.532 p = 0.118; Tier-1 0.618; MW-adjusted 0.578; reverse-control AXL 0.880 / TNIK 0.824 / ACVR1 0.797 / MAPK14 0.779) all reproduce.

The **abstract** is a single unstructured paragraph, 266 words, with all headline numbers correct. **All 19 cited Table/Figure source paths exist** (0 broken). The **docx duplicate-Table-2 bug is resolved** (hub Table 2 appears exactly once) and the docx embeds **5 inline figures**. Cross-artefact version/number consistency among the deliverables (manuscript, cover letter, compliance check, README, CITATION.cff, docx) is clean at **v1.6.0** with no numeric drift.

**The only issues found are provenance/hygiene items, not numeric errors in the reported results:**
1. A `MANIFEST.sha256` file **exists** at the repo root (and in `_manifest/`) — contradicting `MVP_PLOSONE_compliance_check.md` L95 which states "no MANIFEST exists" and the brief's premise of "no MANIFEST file".
2. `.zenodo.json` still carries `"version": "v1.0.0"` — a stale version token (the manuscript explicitly states no Zenodo snapshot was deposited, L281).
3. `.github/workflows/release.yml` contains a commented `v1.0.0` example and a step that *generates* `_manifest/MANIFEST.sha256`.
4. The human-miRNA set-level p = 0.51 is authoritative in `P4_setlevel_test.json` (perm_p = 0.5101), not in the per-miRNA spearman CSV the task pointer named; the manuscript does not cite a source file for it.

None of these change any reported result. The manuscript is internally consistent and its math holds.

---

## 1. Cross-verification table (manuscript claim vs independently recomputed)

| # | Manuscript claim (location) | Manuscript value | Recomputed value (authoritative source) | Match? |
|---|---|---|---|---|
| 1 | FE core (L38, L315) | 2,750 | 2,750 genes satisfy `meta_FDR < 0.05 & consistency ≥ 0.8` in `META_DRG_axis_CORE_signature.csv` (file is exactly 2,750 rows, all qualifying) | ✅ |
| 2 | RE core (L40, L315) | 508 (18.5%); median I² 41.8%; median τ² 0.266 | `_R4_random_effects_meta.csv`: 508 genes satisfy `FDR_RE < 0.05 & consistency ≥ 0.8` (508/2,750 = 18.47% → 18.5%); median I² = 41.77% → 41.8%; median τ² = 0.2664 → 0.266 (over all 16,552 genes) | ✅ |
| 3 | Gene-set q = 0.0022 ×4 (L14, L42) | q = 0.0022 each (4 programmes) | `_R4_geneset_setlevel_bh.csv`: the four core sets (Neuroinflammation, Complement, Mitochondria_OXPHOS, DAM_microglia) each have perm_q = 0.002249 → 0.0022, under both fixed and random scales | ✅ |
| 4 | Non-circular (L52, L136) | 43.3% (1,660/3,830); 47.1% (6,772/14,390); p = 0.0002 | `_R4_nerveinjury_only_summary.json`: stratum `NI_FDR05_AND_NIcons>=0.8` → k = 1,660 / n = 3,830 / rate = 0.4334; `all_measured` → k = 6,772 / n = 14,390 / rate = 0.4706; perm_p = 0.00019996 → 0.0002 | ✅ |
| 5 | Bulk-only (L44, L315) | 2,512 core; 1,737/2,750 = 63.2% (1,322 + 415); relaxed 2,454/2,750 = 89.2%; 200 lacking (154 + 46) | `META_bulkonly_sensitivity_summary.json` + `META_bulkonly_meta.csv`: bulk_only_core_size = 2,512; overlap = 1,737 (63.16% → 63.2%); within overlap K = 4 → 1,322, K = 3 → 415; relaxed overlap (consistency ≥ 0.75) = 2,454 (89.2%); present-but-non-significant = 154, absent = 46, sum = 200 | ✅ |
| 6 | Collapse (L315) | 3,582 core; 2,502/2,750 = 91.0% | `META_collapse_meta.csv`: collapsed_core = 3,582; shared_core = 2,502; retained_fraction = 0.9102 → 91.0% | ✅ |
| 7 | Hubs (L56, L60, L118) | 35 hubs; 26/35 in meta core; 5/35 full 3-method consensus; 2/35 resampling-stable (SPRR1A 1.00, ATF3 0.94) | `P3_hub_genes.csv`: 35 rows; 26 `in_meta_core = True`; 5 with `n_methods = 3` (SPRR1A, ATF3, TFE3, CDHR5, GALNS). `P3_hub_bootstrap.csv`: hub_freq ≥ 0.9 → exactly SPRR1A 1.00 and ATF3 0.935 → 0.94 | ✅ |
| 8 | LODO (L58, L300–301) | incision fold 0.677 [0.374, 0.940]; GSE212311 n = 6 | `P3_lodo_auc_ci_leakage_controlled.csv`: `GSE267799_incision_ratDRG` auc = 0.677083, ci [0.373536, 0.940494], n = 20; `GSE212311_CCI_ratDRG` n = 6 | ✅ |
| 9 | Human miRNA (L62, L64) | p = 0.51 | `P4_setlevel_test.json`: perm_p = 0.5101 (n = 253 plasma-detectable miRNAs). (See finding F-4 on source-file provenance.) | ✅ |
| 10 | Docking (L84, L108, L310) | ADRA2A full-library 0.532 (p = 0.118); Tier-1 0.618; MW-adjusted 0.578; reverse-control AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779 | `P6_breadth_chembl_power.csv`: ADRA2A full_library auc = 0.532465 (p_auc_mwu_onesided = 0.118409); t1_only auc = 0.618368; auc_mw_adjusted = 0.578314. `P6_reverse_control.csv`: AXL 0.8798 → 0.880, TNIK 0.8242 → 0.824, ACVR1 0.7970 → 0.797, MAPK14 0.7785 → 0.779 | ✅ |
| 11 | Version consistency (whole repo) | v1.6.0 in all deliverables; no stale tokens | All deliverables (manuscript L279/L281, cover letter L13, compliance L22/L74/L89, README L238/L239/L245, CITATION.cff L2, docx text) = v1.6.0; no `v1.0.0`–`v1.5.0` / `4055` / `54.3` / `91.4` / `MANIFEST.sha256` in any deliverable. **Stray tokens found in non-deliverable files** — see findings F-1/F-2/F-3 | ⚠️ (partial) |
| 12 | Abstract (L12–14) | single unstructured paragraph; ≤300 words (expect 266); all headline numbers correct | Confirmed single paragraph, no Background/Methods/Results/Conclusions labels; docx abstract = 266 words; every number (2,750; 508/18.5%/I² 41.8%; q 0.0022; 43.3/47.1/0.0002; 17/33; p 0.51; 0.618→0.532 p 0.118) recomputes as above | ✅ |
| 13 | Table/Figure source integrity | cited source files exist & numbers match | 19 cited `results/tables/...` + `figures/...` paths; **0 missing**. Fig-1 set means/percentages (Neuroinflammation +5.075/100% up; DAM +3.833/87.5% up; Complement +3.700/94.4% up; OXPHOS −2.922/78.9% down; all q 0.0022) match `_R4_geneset_setlevel_bh.csv`. Fig-4 17/33 dorsal-horn matches `P5_GSE325938_hub_regionalization.csv` (33 present, 17 DorsalHorn) | ✅ |
| 14 | docx duplicate-table bug (hub Table 2) | Table 2 once; ≥5 inline figures | `Manuscript.docx` word/document.xml: exactly **1** table contains both SPRR1A and ATF3 (hub Table 2 rendered once; "Table 2" text appears 4× as references only). `word/media/` = 5 images, all inline (`wp:inline` = 5, `a:blip` = 5) | ✅ |
| 15 | Cross-artefact drift | cover/compliance/CITATION/README = v1.6.0 + same core/RE/I² | Cover letter L11 states 2,750→508, I² 41.8%, q 0.0022, 43.3/47.1/−3.7, p 0.0002, ADRA2A 0.618→0.532 p 0.118 — all match manuscript. Compliance (L93/L96) documents the corrections. README/CITATION state v1.6.0 with no conflicting numbers. Only `.zenodo.json` = v1.0.0 (F-2) | ⚠️ (one stray) |

**Result: 13/15 checks fully clean; 2 carry minor provenance caveats (F-1, F-2/F-3) that do not affect reported numbers.**

---

## 2. Detailed findings (4-part format)

### F-1 — A `MANIFEST.sha256` file exists, contradicting the compliance self-audit

- 【Problem】 A `MANIFEST.sha256` file is present at the repo root and in `_manifest/`, even though `MVP_PLOSONE_compliance_check.md` L95 claims the "false `MANIFEST.sha256` Data-Availability reference was removed (no MANIFEST exists)" and the audit brief asserts "no MANIFEST file".
- 【Evidence】 Repo root `MANIFEST.sha256` (15,598 bytes, 2026-09-27 23:40) and `_manifest/MANIFEST.sha256` (28,392 bytes) both exist. `MVP_PLOSONE_compliance_check.md` L95 states "no MANIFEST exists". The deliverables (manuscript, cover letter, compliance, README, CITATION, docx) do **not** reference `MANIFEST.sha256` (grep over them returns no hit), so the file is a stray artifact, not a cited input.
- 【Why it matters】 A checksum manifest that the compliance statement says does not exist is an internal contradiction that a careful reviewer or a Zenodo/GitHub release bundling step will notice. It does not alter any reported number, but it undermines the "integrity verifiable via CITATION.cff + immutable tag" claim and could be auto-bundled into a release as an orphan file.
- 【Specific fix】 Either (a) delete `MANIFEST.sha256` (root) and `_manifest/MANIFEST.sha256`, and remove/disable the `release.yml` step that regenerates `_manifest/MANIFEST.sha256` (see F-3); **or** (b) if the manifest is intentionally kept, correct `MVP_PLOSONE_compliance_check.md` L95 to state that a `MANIFEST.sha256` is generated by the release workflow for internal integrity but is **not** referenced by the manuscript's Data Availability statement. Option (a) is cleaner and matches the stated design.

### F-2 — Stale version token `v1.0.0` in `.zenodo.json`

- 【Problem】 `.zenodo.json` still declares `"version": "v1.0.0"`, a stale version label that conflicts with the manuscript's v1.6.0 release.
- 【Evidence】 `.zenodo.json` L24: `"version": "v1.0.0"`. The manuscript Data Availability (L279/L281) and cover letter (L13) both state **v1.6.0**, and L281 explicitly states "no Zenodo snapshot has been deposited".
- 【Why it matters】 If a Zenodo deposit is ever made from this file (the repo ships `GITHUB_DEPOSIT_SOP.md` and `_zenodo_deposit_local.py`), it would publish the wrong version tag. Even if unused, a `v1.0.0` metadata file in a v1.6.0 release is a drift flag.
- 【Specific fix】 Bump `.zenodo.json` `"version"` to `"v1.6.0"` (and `upload_type`/metadata as applicable), or delete `.zenodo.json` entirely since the manuscript states no Zenodo snapshot is deposited.

### F-3 — Commented `v1.0.0` example and MANIFEST generation in the release workflow

- 【Problem】 `.github/workflows/release.yml` contains a commented `v1.0.0` tag example and a step that writes `_manifest/MANIFEST.sha256`, which is the source of the stray F-1 file.
- 【Evidence】 `.github/workflows/release.yml` L5–L6: `# git tag -a v1.0.0 ...`; L68–L82: `> _manifest/MANIFEST.sha256` and a release-note line referencing `MANIFEST.sha256`.
- 【Why it matters】 The commented example is a copy-paste trap that could reintroduce a stale tag on the next release; the MANIFEST-generation step is what creates the orphan file flagged in F-1.
- 【Specific fix】 Update the commented example to `v1.6.0` and either remove the MANIFEST-generation step (recommended) or keep it but align the compliance statement (F-1 option b).

### F-4 — Provenance of the human-miRNA set-level p = 0.51 is not cited to its authoritative file

- 【Problem】 The task brief points to `P4_GSE158825_miRNA_painoutcome_spearman.csv` "for human p = 0.51", but that file is a per-miRNA Spearman table (`miRNA, rho, p, FDR`) and does **not** contain the set-level permutation p. The authoritative value lives in `P4_setlevel_test.json` (perm_p = 0.5101, n = 253). The manuscript (L62/L64) states the number but cites no source file for it in the Figure/Table source list (L297–311).
- 【Evidence】 `P4_setlevel_test.json`: `perm_p = 0.5100979804039192`, `n = 253`. `P4_GSE158825_miRNA_painoutcome_spearman.csv` columns are `miRNA, rho, p, FDR` (per-miRNA only). The manuscript's source list contains no entry for the human-miRNA set-level test.
- 【Why it matters】 This is a provenance/traceability gap, not a numeric error — the value p = 0.51 is confirmed correct. But a provenance auditor (and PLOS ONE's data-availability scrutiny) expects every headline number to trace to a named file.
- 【Specific fix】 Add an explicit source citation, e.g. in the Figure/Table source list: "Human-miRNA set-level permutation test: `results/tables/P4_setlevel_test.json` (perm_p = 0.51, n = 253)". The value itself needs no change.

---

## 3. § Stands up — things I suspected were wrong but found correct

1. **FE core "2,750" as a rounded/aspirational number.** I expected the filter `meta_FDR < 0.05 & consistency ≥ 0.8` to produce a number near but not exactly 2,750. Recounting `META_DRG_axis_CORE_signature.csv` returns exactly 2,750 qualifying genes (the file is precisely the core). The number is real, not rounded.
2. **The ATF3 bootstrap "0.94" as a rounding artifact or one of several ≥0.9 hubs.** I suspected more than two hubs might cross the 0.9 stability threshold. Exactly two do: SPRR1A (1.00) and ATF3 (0.935 → 0.94); all others are below 0.9. The "2/35" claim is exact.
3. **The docx duplicate-Table-2 bug might still be present.** A prior bug rendered hub Table 2 twice. Parsing `word/document.xml` shows exactly one table containing the SPRR1A/ATF3 hub rows; "Table 2" appears 4× only as textual references. The bug is fixed.
4. **Stale 4,055 / 54.3% / 91.4% numbers might linger in the manuscript.** A full-token grep over the manuscript, cover letter, compliance check, README and CITATION.cff returned zero occurrences of `4055`, `4,055`, `54.3`, `91.4`, or `MANIFEST.sha256`. The Round-14 re-derivation (B1, per compliance L93) is clean.
5. **The non-circular 43.3%/47.1% might be a hand-computed fraction.** Recomputed from `_R4_nerveinjury_only_summary.json`: 1,660/3,830 = 0.4334 → 43.3%; 6,772/14,390 = 0.4706 → 47.1%; perm_p = 0.00019996 → 0.0002. Exact.
6. **Abstract "266 words" might be over-counted.** Word count of the docx abstract paragraph = 266, matching the compliance self-report (L95) and the ≤300 limit. Single unstructured paragraph confirmed (no Background/Methods/Results/Conclusions labels).

---

## 4. § Questions for the authors

1. **MANIFEST.sha256:** Is the root `MANIFEST.sha256` intended to ship, or is it an orphan from the release workflow? The compliance statement says it does not exist — which is the intended state?
2. **`.zenodo.json` v1.0.0:** Will a Zenodo deposit actually be made? If not, should `.zenodo.json` be removed so it cannot publish a wrong version tag?
3. **Human-miRNA source citation:** Will you add `P4_setlevel_test.json` as the explicit source for p = 0.51 in the Figure/Table source list? (The number is correct; only the citation is missing.)
4. **`P6_enrichment_mw_confounder_check.csv` in Fig-5 source (L310):** I confirmed the file exists and the reverse-control / breadth AUCs reproduce from `P6_reverse_control.csv` and `P6_breadth_chembl_power.csv`; I did not independently recompute the MW-confounder ΔAUC CIs (AXL [−0.030, +0.104], TNIK [−0.224, +0.193]) because that file was not in the authoritative list — can you confirm those CIs are regenerated from it?
5. **`P3_lodo_auc_ci.csv` vs `P3_lodo_auc_ci_leakage_controlled.csv` (both cited, L160/L300):** The manuscript cites the leakage-controlled file for the reported fold; the non-controlled `P3_lodo_auc_ci.csv` is also listed as the computation source. For the record, which file holds the incision fold 0.677 used in the abstract/Fig-2? (The leakage-controlled file is the one that matches; both exist.)

---

## 5. § What I actually checked

**Files read (manuscript & deliverables):**
- `reports/MVP_PLOSONE_submission.md` (full; line-referenced claims L12–L381)
- `reports/MVP_PLOSONE_cover_letter.md` (version/number cross-check)
- `reports/MVP_PLOSONE_compliance_check.md` (version/number + changelog cross-check; read only to verify the author's self-audit, per permitted scope)
- `README.md`, `CITATION.cff` (version cross-check)
- `submission_pack/Manuscript.docx` (unpacked: `word/document.xml`, `word/media/` — Table-2 duplication, inline-image, version-token checks)

**Authoritative data files recomputed (all values above are re-derived, not transcribed):**
- `results/tables/META_DRG_axis_CORE_signature.csv` (FE core)
- `results/tables/_R4_random_effects_meta.csv` (RE core, median I², median τ²)
- `results/tables/_R4_geneset_setlevel_bh.csv` (gene-set q = 0.0022)
- `results/tables/_R4_nerveinjury_only_summary.json` (non-circular concordance)
- `results/tables/META_bulkonly_sensitivity_summary.json` + `META_bulkonly_meta.csv` (bulk-only)
- `results/tables/META_collapse_meta.csv` (collapse)
- `results/tables/P3_hub_genes.csv` + `P3_hub_bootstrap.csv` (hubs)
- `results/tables/P3_lodo_auc_ci_leakage_controlled.csv` (LODO)
- `results/tables/P4_setlevel_test.json` + `P4_GSE158825_miRNA_painoutcome_spearman.csv` (human miRNA)
- `results/tables/P6_reverse_control.csv` + `P6_breadth_chembl_power.csv` (docking)
- `results/tables/P5_GSE325938_hub_regionalization.csv` (17/33 dorsal horn)
- `results/tables/P3_geneset_stats.csv`, `P5_GSE216039_DRG_hub_finetype_top.csv`, `P5_hub_lineage_consensus.csv`, `_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap_resamples.csv` (source-path existence)

**Repository hygiene files inspected (non-deliverable, for version audit):**
- `.zenodo.json` (L24 stale `v1.0.0`)
- `.github/workflows/release.yml` (commented `v1.0.0`, MANIFEST generation)
- repo-root `MANIFEST.sha256` and `_manifest/MANIFEST.sha256` (stray, F-1)

**Discrepancies stated:**
- **Zero numeric discrepancies** between manuscript claims and authoritative re-computation across all 10 mandatory numeric checks and the abstract.
- **Four provenance/hygiene issues** (F-1 through F-4) — none alter any reported result; F-1/F-2/F-3 are stray-token/file artifacts, F-4 is a missing source citation.

**Independence note:** I did not read `reviews/REVIEW_round*.md`, `reviews/RESPONSE_*.md`, `reviews/REVISION_*.md`, `submission_pack/SUBMISSION_MANIFEST.md`, `submission_pack/Reporting_Summary.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, sibling `reviews/round16_panel_2026-09-28/*` reports other than this one, or any `_archive/`/`.bak` file. `MVP_PLOSONE_compliance_check.md` was consulted only to cross-check the author's version/number self-audit, not as authoritative.

---

*Bottom line for the panel: the implementation and provenance of the reported numbers are sound — every headline figure reproduces from the authoritative tables. The manuscript is safe to advance on numeric grounds; the four minor hygiene items (F-1–F-4) should be cleaned up before final deposit but are not blocking.*
