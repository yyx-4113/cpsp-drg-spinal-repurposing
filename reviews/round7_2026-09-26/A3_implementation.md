# A3 — Implementation / Provenance Audit

**Manuscript:** `reports/MVP_ScientificReports_submission.md` (PLOS ONE / Scientific Reports target, ~278 lines body)
**Role:** Reproducibility / recompute auditor (independent, first-submission stance)
**Audit date:** 2026-09-26
**Independence statement:** No `reviews/REVIEW_round*.md`, `reviews/round*/*`, `RESPONSE*.md`, `REVISION*.md`, `_v14_source.md`, `_v15_source.md`, `MVP_PLOSONE_compliance_check.md`, `SUBMISSION_MANIFEST.md`, other `round7_2026-09-26/*` files, `*.bak`, or `author_verification_statement.md` were read. Every number below was recomputed from the project's own result tables, not trusted from the manuscript.

---

## Executive summary

I recomputed **all 18 numbers the brief asked me to verify** from the source tables in `results/tables/`. **No headline number failed to reproduce.** The meta-analysis counts, random-effects shrinkage, bulk-only reconciliation, gene-set q-values, hub count, dorsal-horn count, human-miRNA null, ADRA2A docking flip, the two-filter null, the non-circular translation test, and the reference-DOI integrity all trace cleanly to real files with matching values.

The **highest-priority issues are not numeric mismatches** but (i) one reference (ref 31, Xiao 2002) is **missing its DOI entirely** even though the correct, verifiable DOI is sitting in an auxiliary JSON; (ii) a **provenance trail problem** — the 17/33 dorsal-horn number is real, but it is sourced from `P5_GSE325938_hub_regionalization.csv` (Visium), *not* from the `P4_GSE249825/249746_hub_celltype.csv` file the brief named, and a `GSE249746` dataset exists in the tables but is **not disclosed** in the manuscript's 12-dataset list; and (iii) two minor wording imprecisions ("3,085 drugs" vs 3,070 actually scored; Abstract exactly 200 words). None of these invalidate a result, but (i) and (ii) are credibility/provenance gaps a careful reviewer will catch.

---

## Cross-verification table (manuscript claim → recomputed value → match?)

| # | Manuscript claim (location) | Recomputed from source | Match |
|---|---|---|---|
| 1 | 16,552 genes tested (Abs L14; Res L38; Tbl 1a L248) | `META_DRG_axis_stouffer.csv` row count = **16,552** | ✅ |
| 2 | 6,869 at meta_FDR<0.05 (L38, L248) | rows with `meta_FDR`<0.05 = **6,869** | ✅ |
| 3 | core 4,055 (FDR<0.05 & consistency≥0.8) (L38, L248) | rows satisfying both = **4,055** | ✅ |
| 4 | RE core 1,008 = 24.9% of FE core (L40, L248) | `_R4_random_effects_meta.csv` FDR_RE<0.05 & cons≥0.8 = **1,008**; 1008/4055 = 24.86% | ✅ |
| 5 | τ² median 0.232, I² median 38.8% (L40) | RE file tau2 median = **0.2324**; I2 median = **38.785%** | ✅ |
| 6 | 41.9% I²>50%, 68.1% τ²>0 (L40) | I2>50 = **41.9%**; tau2>0 = **68.1%** | ✅ |
| 7 | Hub median I² 72.8%, 18/35 FDR_RE<0.05 (L40) | hub subset I2 median = **72.837%**; FDR_RE<0.05 = **18/35** | ✅ |
| 8 | Bulk-only core 2,512 (L44, L140, L248) | `META_bulkonly_sensitivity_summary.json` `bulk_only_core_size` = **2,512** | ✅ |
| 9 | overlap 2,202/4,055 = 54.3% (L44, L140) | JSON `overlap`=**2,202**, `primary_core_size`=4,055 → 54.31% | ✅ |
| 10 | SCN8A bulk meta_Z ≈ −4.923567 (L46, brief) | CSV `meta_Z`=**−4.923567449382213**; JSON `bulk_meta_Z`=**−4.923567449382212** | ✅ |
| 11 | gene-set q=0.003 neuroinflammation/DAM/complement (L42, L231) | `_R4_geneset_setlevel_bh.csv` perm_q = **0.0029985** (fixed & random) | ✅ |
| 12 | OXPHOS q=0.31 under random effects (L42, L114, L231) | random OXPHOS perm_q = **0.3103** | ✅ |
| 13 | 35 hubs; 32/35 in meta core; 5/35 full 3-method (L54–56, L260–261) | `P3_hub_genes.csv` = **35 rows**; in_meta_core True = **32**; n_methods=3 = **5** | ✅ |
| 14 | 17/33 hubs in dorsal horn (L72, L240) | `P5_GSE325938_hub_regionalization.csv`: 17 `DorsalHorn` of 35 present (CRISP3/LNP1 sub-floor) | ✅ (see F2) |
| 15 | human miRNA set-level p=0.51 (L64, L122) | `P4_setlevel_test.json` `perm_p` = **0.5101** | ✅ |
| 16 | miRNA LSS+DS min p=1.3e-4 FDR 0.128 (L64) | `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` min p=**1.286e-4**, min FDR=**0.1285** | ✅ |
| 17 | miRNA painoutcome min p=8.5e-4 FDR 0.556 (L64) | `P4_GSE158825_miRNA_painoutcome_spearman.csv` min p=**8.47e-4**, min FDR=**0.5560** | ✅ |
| 18 | ADRA2A Tier-1 (CNS) 0.618 → full 0.532, p=0.118 NS (L106, L118, L243) | `P6_breadth_chembl_power.csv`: t1 AUC=**0.61837**, full AUC=**0.53247**, p_mwu=**0.11841** | ✅ |
| 19 | 3,085 drugs (L14, L80, L106) | `P6_ligand_library.csv`=3,311 rows; dockable pdbqt=**3,085**; actual scored n≈**3,070** | ⚠ F3 |
| 20 | "no target clears both filters" (L118) | `P6_BH_correction.csv`: each target fails ≥1 of raw/size-indep BH q | ✅ |
| 21 | ρ≈0.78 fidelity ceiling (L154) | `P6_exh_validation.json` exh1 spearman = **0.7832** | ✅ |
| 22 | Translation background 47.1% (6,779/14,390) (L52) | `_R4_nerveinjury_only_summary.json` all_measured n=**14,390**, k=**6,779**, rate=**0.4711** | ✅ |
| 23 | Translation NI stratum 46.3% (2,266/4,899), p=0.14 (L52) | JSON NI_FDR05_AND_NIcons>=0.8 n=**4,899**, k=**2,266**, rate=**0.4625**, perm_p=**0.1396** | ✅ |
| 24 | −0.9 pp risk difference (L52, L114) | JSON `strong_vs_background_pp` = **−0.9** | ✅ |
| 25 | Abstract ≤200 words (brief) | computed = **200 words** | ⚠ F5 |
| 26 | Ref 33 (Irwin & Shoichet) one correct DOI (brief) | manuscript ref 33 = `10.1021/acs.jmedchem.5b02008`, verified real | ✅ |
| 27 | All 33 DOIs well-formed (brief) | 32/33 present & well-formed; **ref 31 missing** | ⚠ F1 |

**Bottom line:** 25/27 rows fully match; the 2 non-matches are wording/format gaps (F3, F5), not value errors. Two further provenance findings (F1, F2) and one stale-artifact finding (F4) are reported below.

---

## Findings (each with Problem / Evidence / Why it matters / Specific fix)

### F1 — Reference 31 (Xiao 2002) is missing its DOI  ⚠ MEDIUM
**【Problem】** The reference list entry for Xiao et al. 2002 (ref 31) ends with "(2002)." and carries **no `https://doi.org/...` line**, whereas every other reference (1–30, 32, 33) has one.

**【Evidence】** Manuscript L200: `31. Xiao, H. S. et al. ... Proceedings of the National Academy of Sciences ... 99, 8360–8365 (2002).` — no DOI suffix. The auxiliary `results/tables/_R4_ref_DOIs.json` maps `xiao2002` → `10.1073/pnas.122231899`. I verified that DOI is **genuine** via PubMed (PMID 12060780, PMCID PMC123072) — it resolves to exactly this paper ("Identification of gene expression profile of dorsal root ganglion in the rat peripheral axotomy model of neuropathic pain", PNAS 99(12):8360–8365, 2002). So the missing value is known and correct; it was simply never printed.

**【Why it matters】** A reference without a resolvable identifier is a traceability defect. Some editorial systems auto-flag missing DOIs; a reviewer checking ref 31's provenance hits a dead end. It also undercuts the manuscript's own "every claim traceable" posture.

**【Specific fix】** Append to ref 31: `https://doi.org/10.1073/pnas.122231899`. (Paste-ready: `31. Xiao, H. S. et al. Identification of gene expression profile of dorsal root ganglion in the rat peripheral axotomy model of neuropathic pain. *Proceedings of the National Academy of Sciences of the United States of America* **99**, 8360–8365 (2002). https://doi.org/10.1073/pnas.122231899`)

---

### F2 — Dorsal-horn 17/33 source file is mis-identified in the brief; an undisclosed `GSE249746` dataset lingers in the tables  ⚠ MEDIUM (provenance)
**【Problem】** The 17/33 dorsal-horn number is correct, but (a) the file the audit brief pointed to (`P4_GSE249825_hub_celltype.csv`, "filename may be GSE249746") is **not** its source, and (b) `GSE249746` appears as real table files yet is **absent from the manuscript's disclosed 12-dataset list**.

**【Evidence】** The 17/33 count reproduces from `results/tables/P5_GSE325938_hub_regionalization.csv`: of 35 hubs `present=True`, **17** have `top_region == DorsalHorn` (genes: TFE3, GALNS, CHL1, RNF19B, SRRM4, FLRT3, PTPN23, MAPK14, VASH2, TNIK, ANKRD13B, NPY, ITPKC, ACVR1, AGRN, CTTN, RUBCN). CRISP3 and LNP1 are `present=True` but `top_detection=0.0` and sit in `MeningealFibro` (broad/low), i.e. the two sub-floor hubs excluded by the "33/35 detectably expressed" denominator — so 17/33 (51.5%) is internally consistent. This file is the **Visium GSE325938** output, which *is* in the manuscript dataset list (L129) and is the source cited in Fig 4B/Results L72. The brief's `P4_GSE249746_hub_celltype.csv` is a **different** file: 36 rows (35 hubs + ADRA2A, `is_original_hub=False`), columns `peak_cluster/peak_annotation/spearman_vs_painScore` — it contains *no* dorsal-horn region field and cannot yield 17/33. Moreover `GSE249746` does **not** appear anywhere in the manuscript's Methods dataset enumeration (L129) or Data availability, yet `P4_GSE249746_cluster_annotation.csv` and `P4_GSE249746_hub_celltype.csv` exist in `results/tables/`.

**【Why it matters】** Two transparency risks: (i) if a reviewer tries to re-trace 17/33 to the cited `P4_GSE249825` file they will not find it (that filename does not exist), eroding trust in the provenance trail; (ii) an unused/undisclosed `GSE249746` dataset in the tables invites the question of whether it informed any reported result. Neither is a numeric error, but both are exactly the kind of loose end a reproducibility reviewer flags.

**【Specific fix】** (a) In the manuscript, keep the 17/33 attribution explicitly on **GSE325938 Visium** (already done in L72/240) and do **not** reference `P4_GSE249825/249746` for it. (b) Either **disclose** GSE249746 in the Methods dataset list and state what it was used for, or **remove** the orphan `P4_GSE249746_*` files from the released tables so the released artifact matches the reported analysis. State in Data availability which file backs the 17/33 claim (`P5_GSE325938_hub_regionalization.csv`).

---

### F3 — "3,085 drugs" overstates the actually scored set  ⚠ LOW
**【Problem】** Phrases "Full-library docking of 3,085 drugs" and "collapsed to 0.532 … across all 3,085 drugs" treat 3,085 as the tested N, but the per-target scored N is ~3,070.

**【Evidence】** `P6_ligand_library.csv` has **3,311** rows total; the manuscript itself states 3,085 is "93.2% of 3,311 small molecules" (pdbqt files). In `P6_breadth_chembl_power.csv` the ADRA2A `full_library` row has `n_ligands = 3,070` (other targets 3,063–3,075); the manuscript also reports "30,850 poses; 30,687 scored" (L80/L215), i.e. not all 30,850 were scored. The AUC p=0.118 is computed on the 3,070 scored ligands, not 3,085.

**【Why it matters】** A reviewer recomputing will see n=3,070 for ADRA2A and may suspect a discrepancy. Minor, but trivially avoidable.

**【Specific fix】** Reword to "the 3,085-drug library (n = 3,070 scored)" or "3,070 drugs" where the tested N is meant; reserve "3,085" for the library-size statement already in L80.

---

### F4 — Stale auxiliary reference-map JSON uses a pre-renumbering scheme  ⚠ LOW
**【Problem】** `results/tables/_R4_reference_map.json` encodes a reference order that no longer matches the manuscript's 1–33 numbering.

**【Evidence】** The JSON `numbered` map has only **26** entries and places, e.g., `divito2026`→14, `nie2025`→11, `haque2024`→16, `inoue2018`→19, `coull2005`→20 — whereas the manuscript numbers these as 20, 17, 25, 21, 22 respectively. The manuscript's own in-text superscripts, however, map correctly to the current list (spot-checked below), so the manuscript is internally consistent; the JSON is simply a leftover from before the renumbering.

**【Why it matters】** This is precisely the corruption vector the brief warned about ("after the recent renumbering"). The manuscript is fine today, but if the author regenerates citations from this stale map, mis-numbering would reappear.

**【Specific fix】** Regenerate `_R4_reference_map.json` against the final 1–33 order, or delete it from the released artifact to prevent reuse.

---

### F5 — Abstract is exactly 200 words (at the hard limit)  ⚠ LOW / BORDERLINE
**【Problem】** The Abstract word count is **exactly 200**, leaving zero margin against a "≤200 words" rule.

**【Evidence】** Extracted the Abstract block (L12–14) and counted whitespace-delimited tokens = **200**. Some journal word-counters split hyphenated/tokenised items (e.g. "4,055-gene", "q = 0.003", "17/33") differently and could push the count to 201–203.

**【Why it matters】** An automated editorial check that returns >200 triggers a desk query or auto-rejection; being exactly at the limit is fragile.

**【Specific fix】** Trim 1–2 words for safety, e.g. compress "A Stouffer meta-analysis of 16,552 genes defined a 4,055-gene core; under random effects only 1,008 genes persisted (median I² = 38.8%)" → "A Stouffer meta-analysis of 16,552 genes defined a 4,055-gene core; under random effects 1,008 genes persisted (median I² = 38.8%)".

---

### F6 — Informational: the "bogus DOI 10.1073/pnas.122231899" concern is resolved  ✓ (no action)
**【Problem / clarification】** The brief asked to confirm ref 33 does **not** carry the "previously-removed bogus `10.1073/pnas.122231899`". On investigation this string is **not bogus** — it is the genuine Xiao-2002 PNAS DOI (verified via PubMed/PMC, F1 above). It does **not** appear on ref 33; ref 33 correctly carries only `10.1021/acs.jmedchem.5b02008` (verified real via the publisher page: Irwin & Shoichet, *J. Med. Chem.* 2016, "Docking Screens for Novel Ligands Conferring New Biology"). The real defect is the inverse of the brief's worry: the string belongs on **ref 31**, which currently omits it (F1). No corruption of ref 33 or of any τ²/I² notation was found — τ²/I² appear correctly as inline text in L8, L40, L136, L157–158.

---

## § Stands up (claims that DID match, with evidence)

1. **Primary meta counts (16,552 / 6,869 / 4,055).** Recomputed directly from `META_DRG_axis_stouffer.csv` (16,552 data rows; 6,869 with `meta_FDR`<0.05; 4,055 with `meta_FDR`<0.05 AND `consistency`≥0.8). Exact match to three separate manuscript locations (Abstract, Results L38, Table 1a).
2. **Random-effects shrinkage (1,008 core; τ² median 0.232; I² median 38.8%).** From `_R4_random_effects_meta.csv`: FDR_RE<0.05 & consistency≥0.8 = 1,008 (=24.9% of 4,055); `tau2` median 0.2324; `I2` median 38.785%; 41.9% of genes I²>50 and 68.1% τ²>0 — all four figures in L40 reproduce. Hub-level RE stats (median I² 72.8%, 18/35 FDR_RE<0.05) also reproduce exactly.
3. **Bulk-only reconciliation (2,512 core; 2,202/4,055 = 54.3%).** `META_bulkonly_sensitivity_summary.json` gives `bulk_only_core_size=2,512`, `primary_core_size=4,055`, `overlap=2,202`, `overlap_pct_primary=54.3157%`. The previously-quoted 1,981 is indeed superseded. SCN8A `bulk_meta_Z` matches between the CSV (−4.923567449382213) and JSON (−4.923567449382212) to 12 decimals.
4. **Gene-set q-values (0.003 for neuroinflammation/DAM/complement; 0.31 for OXPHOS).** `_R4_geneset_setlevel_bh.csv`: fixed and random perm_q for the three upregulated programmes = 0.0029985 ≈ 0.003; random OXPHOS perm_q = 0.3103 ≈ 0.31. Fixed-effect OXPHOS perm_q = 0.0202 matches the "q = 0.020" fixed-effect statement (L42, Fig 1). The per-miRNA nulls (min p 1.3e-4/FDR 0.128; min p 8.5e-4/FDR 0.556) also reproduce.
5. **ADRA2A docking flip and the two-filter null.** `P6_breadth_chembl_power.csv`: ADRA2A Tier-1 (t1_only, n=620) AUC = 0.61837; full_library (n=3,070) AUC = 0.53247 with `p_auc_mwu_onesided` = 0.11841 (NS). `P6_BH_correction.csv` confirms **no target clears both** raw-BH-q and size-independent-BH-q < 0.05 simultaneously (ACVR1/AXL/MAPK14/TNIK pass raw but fail size-indep; ADRA2A passes size-indep but fails raw q=0.118). The ρ≈0.78 fidelity ceiling reproduces (`P6_exh_validation.json` exh1 spearman 0.7832).
6. **Non-circular translation test (47.1% vs 46.3%, −0.9 pp, p=0.14, denominator 14,390).** `_R4_nerveinjury_only_summary.json`: `all_measured` n=14,390, k=6,779, rate 0.4711 (47.1%); `NI_FDR05_AND_NIcons>=0.8` n=4,899, k=2,266, rate 0.4625 (46.3%), `perm_p` 0.1396 (≈0.14); `strong_vs_background_pp` = −0.9. All four numbers match L52/L114.
7. **Reference-DOI integrity (32/33).** Every DOI in the list (1–30, 32, 33) is well-formed (`10.x/...`). Spot-checked 6 via the web: ref 33 (10.1021/acs.jmedchem.5b02008 → Irwin & Shoichet 2016, correct), ref 17 (10.1126/sciadv.adu4270 → Nie 2025 CRPS-I, correct), ref 20 (10.3949/ccjm.93a.25087 → Divito 2026 suzetrigine, correct), ref 23 (10.1016/j.cell.2017.05.018 → Keren-Shaul 2017, correct), refs 6/7 (nature DOIs, format valid, journal matches). In-text superscripts map correctly to their papers (spot-checked all 33; e.g. ¹ Macrae CPSP 10–50%, ¹⁰ Ding Nav1.6, ¹⁷ Nie REG3β/CRPS-I, ²⁰ Divito suzetrigine, ³¹ Xiao DRG, ³²⁻³³ repurposing narratives). No duplicated or corrupted superscripts found.

---

## § Questions for the authors

1. **GSE249746:** Is `GSE249746` used in any reported result, or is it a retained earlier spinal-snRNA exploration that should be removed? If used, why is it absent from the Methods dataset list (L129)? If not used, please delete `P4_GSE249746_cluster_annotation.csv` and `P4_GSE249746_hub_celltype.csv` from the released tables.
2. **Ref 31 DOI:** Was the omission of the Xiao-2002 DOI intentional, or a drop during renumbering? The correct value (`10.1073/pnas.122231899`) is already in `_R4_ref_DOIs.json` — should it be restored to the manuscript?
3. **Drug N:** Please confirm the ADRA2A full-library AUC (0.532, p=0.118) was computed on n=3,070 scored ligands, and adjust the "3,085 drugs" wording accordingly (F3).
4. **Bulk-only denominator phrasing:** L44 states the bulk-only core used "union-K≥3" (present in ≥3 of 4 bulk contrasts). Is the 2,512 count sensitive to this union rule vs an intersection rule, and is that sensitivity already captured by the superseded-1,981 note? (Not a numeric dispute — a clarity question for reviewers.)
5. **Abstract length:** Will you trim the Abstract below 200 words to avoid a hard-limit desk query (F5)?

---

## § What I actually checked

**Files read (manuscript + source tables):**
- `reports/MVP_ScientificReports_submission.md` (full)
- `results/tables/META_DRG_axis_stouffer.csv` (header + full recompute)
- `results/tables/_R4_random_effects_meta.csv` (full recompute)
- `results/tables/META_bulkonly_sensitivity_summary.json`, `META_bulkonly_meta.csv`
- `results/tables/P3_geneset_stats.csv`, `_R4_geneset_setlevel_bh.csv`
- `results/tables/P3_hub_genes.csv`, `P3_ml_summary.json`
- `results/tables/P5_GSE325938_hub_regionalization.csv`, `P4_GSE249746_hub_celltype.csv`
- `results/tables/P4_setlevel_test.json`, `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`, `P4_GSE158825_miRNA_painoutcome_spearman.csv`
- `results/tables/P6_breadth_chembl_power.csv`, `P6_BH_correction.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_reverse_control.csv`, `P6_exh_validation.json`, `P6_param_summary.csv`, `P6_stage1_param_validation.json`, `P6_ligand_library.csv`
- `results/tables/_R4_nerveinjury_only_summary.json`
- `results/tables/_R4_ref_DOIs.json`, `_R4_reference_map.json`

**Commands / computations performed (values recomputed, not quoted):**
- Row counts and Boolean filters on the two large meta CSVs (16,552 / 6,869 / 4,055; RE core 1,008; τ²/I² medians and tail fractions).
- Per-gene SCN8A `meta_Z` extraction from both CSV and JSON (match to 12 d.p.).
- Set-level BH q extraction for the four programmes of interest.
- Hub list aggregation (35 rows, 32 in-core, 5 triple-consensus) and hub-subset RE stats (median I² 72.837%, 18/35 FDR_RE<0.05).
- Visium regionalisation count: 17 `DorsalHorn` of 35 present; confirmed CRISP3/LNP1 are sub-floor `MeningealFibro`.
- Translation JSON extraction: 14,390 / 6,779 / 0.4711; 4,899 / 2,266 / 0.4625 / perm_p 0.1396; `strong_vs_background_pp` −0.9.
- Docking breadth/reverse/BH extraction for ADRA2A (0.618 → 0.532, p 0.118) and the no-target-clears-both-filters check.
- Exhaustiveness fidelity spearman (0.7832) for the ρ≈0.78 claim.
- Library size audit (3,311 total → 3,085 dockable → ~3,070 scored).
- Abstract word count (200).
- Reference-DOI format scan (32/33 present) + web verification of 6 DOIs (refs 33, 17, 20, 23 confirmed real; refs 6, 7 blocked by publisher bot-challenge but format/journal correct) + PubMed confirmation that `10.1073/pnas.122231899` is the genuine Xiao-2002 DOI.

**Discrepancies / non-matches found:**
- Ref 31 missing DOI (F1) — confirmed against manuscript and auxiliary JSON + PubMed.
- 17/33 dorsal-horn source mis-identification + undisclosed GSE249746 tables (F2).
- "3,085 drugs" vs 3,070 scored (F3).
- Stale `_R4_reference_map.json` (F4).
- Abstract exactly 200 words (F5).
- No substantive numeric mismatch in any of the 18 brief-mandated recomputations.

**Files deliberately NOT read (independence):** any `reviews/REVIEW_round*.md`, `reviews/round*/*`, `RESPONSE*.md`, `REVISION*.md`, `_v14_source.md`, `_v15_source.md`, `MVP_PLOSONE_compliance_check.md`, `SUBMISSION_MANIFEST.md`, other `round7_2026-09-26/*` auditor files, `*.bak`, `author_verification_statement.md`.

---

## One-line verdict
Every headline number in the manuscript reproduces exactly from the project's own result tables; the manuscript is numerically sound. The actionable items are non-numeric: restore the missing ref-31 DOI, close the GSE249746 provenance gap, tighten the "3,085 drugs" wording, retire the stale reference-map JSON, and trim the Abstract below 200 words. None of these require re-running analyses.
