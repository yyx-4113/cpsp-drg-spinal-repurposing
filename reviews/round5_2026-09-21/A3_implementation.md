# A3 — Provenance / recompute audit (v1.4, Scientific Reports first-submission review)

**Reviewer role:** A3 — numbers-trace-to-source specialist. Mandate: for every headline number in the manuscript, trace it to a source CSV/JSON and recompute. I treated the manuscript as a *fresh first submission* and did not read any other reviewers' files, response letters, manifests, or author statements.

**Scope audited:** `MVP_ScientificReports_submission.md` (main), `MVP_ScientificReports_supplementary.md`, and the unrendered `_v14_source.md`. Every source table named in the Methods/Data-availability was opened and recomputed.

**Bottom line:** Of the ten checklist items, nine reconcile exactly to source (every recomputed value matches the manuscript to the printed precision). One genuine issue remains: a reference citation is present inside the Abstract, contradicting the "no citation in the Abstract" rule and breaking strict first-citation numbering. No stale wrong numbers (old `0.172`, `27.8% down`, `253`-as-`328`, `16 localisable`, `10 of 17`, `Round-3`, `v1.3`, `v1.4`, `[truncated]`) survive in the rendered submission text.

### Provenance matrix (headline number → source → recomputed → verdict)

| # | Headline number(s) in manuscript | Source file(s) | Recomputed | Verdict |
|---|---|---|---|---|
| 1 | 4,055 / 16,552; 6,869 FDR<0.05; 46.3% / 47.1% / −0.9 pp | `_R4_nerveinjury_only_summary.json`, `META_DRG_axis_stouffer.csv` | 6779/14390=47.1%; 2266/4899=46.3%; −0.86→−0.9 pp; 6869; 4055 | OK |
| 2 | 1,008 = 24.9%; τ²=0.232; I²=38.8%; 41.9% I²>50%; 68.1% τ²>0 | `_R4_supplementary_summary.json`, `_R4_random_effects_meta.csv` | med τ²=0.2324; med I²=38.79; I²>50%=41.9; τ²>0=68.1; 1008/4055=24.9% | OK |
| 3 | OXPHOS 72.2% down; q FE=0.020 / RE=0.31; bulk core 1,981 / 42.7% | `META_bulkonly_sensitivity_summary.json`, `_R4_geneset_setlevel_bh.csv` | frac_up 0.2778→72.2% down; perm_q 0.02024/0.31034; 1732/4055=42.7% | OK |
| 4 | Table 1b SCN log₂FC (16 cells) + bulk meta_Z | `DEG_GSE*.csv` ×4, `META_bulkonly_sensitivity_summary.json` | all 16 match to 2 dp; Z recompute matches | OK |
| 5 | ACVR1 size-indep p = 0.584 (not 0.172) | `P6_BH_correction.csv`, `P6_enrichment_mw_confounder_check.csv` | 0.584 both; stale 0.172 absent | OK |
| 6 | 3,511 / 752 / 328 pairs / 253 distinct | `P4_hub_targeting_miRNAs.csv`, `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`, `P4_hub_miRNA_human_integration.csv` | 3511; 752; 328 (intersection); 253 distinct | OK |
| 7 | 20 localisable / 15 NotLocalisable; 7/35 consistent | `P5_hub_lineage_consensus.csv` | 15 NL + 20 = 35; 7 confident | OK |
| 8 | 17 eligible / 9 docked + ADRA2A; TFE3 not docked | `P6_target_plausibility.json`, `P6_docking_scores_merged.csv` | 17; 9 hub DOCK + ADRA2A; TFE3 absent from output | OK |
| 9 | 24 refs; no Abstract citation; first-appearance order | `MVP_ScientificReports_submission.md` (refs 1–24) | 24 entries; ascending body order; **² in Abstract line 14** | DEFECT |
| 10 | stale numbers / version tags absent | grep of rendered submission + supplementary | no 0.172(ACVR1)/27.8/10of17/16loc/Round-3/v1.x/[truncated] | OK |

---

## 1. Core signature: 4,055 / 16,552; NI-only 46.3% vs 47.1% background (−0.9 pp)

【Problem】The non-circular translation rates (46.3% / 47.1% / −0.9 pp) could not be located in the obvious translation file and needed an independent source; they nonetheless match.

【Evidence】
- Background: `_R4_nerveinjury_only_summary.json` → `all_measured` k=6779, n=14390, rate=0.4711, CI [0.4629, 0.4793]. Manuscript line 46: "47.1% (6,779/14,390; 95% CI 46.3–47.9%)". Recompute 6779/14390 = 0.47112 → 47.1%. **Matches.**
- NI-strong: same file `NI_FDR05_AND_NIcons>=0.8` k=2266, n=4899, rate=0.4625, CI [0.4486, 0.4765], perm_p=0.13957. Manuscript: "46.3% (2,266/4,899; 95% CI 44.9–47.7%) … permutation p = 0.14". Recompute 2266/4899 = 0.46254 → 46.3%; CI 0.4486–0.4765 → 44.9–47.7. **Matches.**
- Risk diff: file `strong_vs_background_pp` = −0.9. Manuscript "−0.9 pp". **Matches.** Recompute 46.25 − 47.11 = −0.86 pp → rounds to −0.9. **Matches.**
- NI-only core sizes: file `NI_core_FE`=5412, `NI_core_RE`=3099. Manuscript line 46 "5,412 genes under fixed effects and 3,099 under random effects". **Matches.**
- Core FE/RE and tested-gene count: `_R4_supplementary_summary.json` n_genes_tested=16552, core_fixed_effect=4055, core_random_effects=1008; independently recomputed from `META_DRG_axis_stouffer.csv`: n=16552, at meta_FDR<0.05 = 6869, core (FDR<0.05 & consistency≥0.8) = 4055. Manuscript line 32: "16,552 genes … 6,869 at meta_FDR < 0.05 and a core signature of 4,055 genes". **Matches.** (The 46.3%/47.1% pair is sourced from `_R4_nerveinjury_only_summary.json`, not `_R4_translation_noncircular.csv`; the latter instead carries the 53.8% (2,318/4,306) collapsed-strata figure, also correct — see below.)

【Why it matters】The −0.9 pp, non-significant (p=0.14) gap is the paper's central honest-null claim about incision translatability; if the denominator or rate were wrong the whole "nerve injury does not predict incision" conclusion collapses.

【Specific fix】No change required. The numbers are correct and correctly attributed. For transparency, the Methods sentence that cites `_R4_translation_noncircular.csv` for the 46.3%/47.1% pair should also name `_R4_nerveinjury_only_summary.json` as the provenance of those two exact fractions (currently the text only points to the `.csv`/`.json` translation files, and the 46.3/47.1 numbers live in the `_nerveinjury_only_` files).

---

## 2. Random-effects core: 1,008 = 24.9% of 4,055; median τ²=0.232; median I²=38.8%; 41.9% genes I²>50%

【Problem】RE sensitivity medians must be recomputed from raw rows, not trusted from a summary JSON.

【Evidence】
- `_R4_supplementary_summary.json`: core_random_effects=1008, RE_retains_pct=24.9, median_tau2=0.232, median_I2_pct=38.8, pct_genes_I2_gt50=41.9, pct_genes_tau2_gt0=68.1.
- Independent recompute from `_R4_random_effects_meta.csv` (16,552 rows; columns include `tau2`, `I2`): median(τ²)=0.2324 → 0.232; median(I²)=38.79 → 38.8%; share I²>50 = 41.9%; share τ²>0 = 68.1%. Manuscript line 34: "median τ² = 0.232 and median I² = 38.8%, with 41.9% of genes showing I² > 50% and 68.1% showing τ² > 0". **Matches on every figure.**
- 1008/4055 = 0.24858 → 24.9%. Manuscript "1,008 genes—24.9% of the fixed-effect core". **Matches.**
- Hub-level RE: `_R4_translation_noncircular.json` hubs_median_I2=72.8, hubs_FDR_RE_lt05=18. Manuscript line 34: "Among the 35 hubs, median I² was 72.8% and 18/35 retained FDR_RE < 0.05". **Matches.**

【Why it matters】The RE core shrinkage (4,055 → 1,008) is the paper's headline heterogeneity-sensitivity statement; a wrong median or denominator would misstate how fragile the signature is.

【Specific fix】No change required.

---

## 3. OXPHOS bulk-only "72.2% down"; set-level BH q FE=0.020 / RE=0.31

【Problem】Two different OXPHOS q-values (fixed vs random) and the bulk-only polarity must be confirmed against two different JSON/CSV sources.

【Evidence】
- `META_bulkonly_sensitivity_summary.json` → `Mitochondria_OXPHOS`: frac_up = 0.2777778, mean_Z = −2.7988, perm_p = 0.00049975. 1 − 0.2777778 = 0.72222 → 72.2% down. Manuscript line 38 (bulk-only): "OXPHOS (−2.80, 72.2% of members down, perm p ≤ 0.0005)". **Matches** (mean_Z −2.7988 → −2.80; 72.2% down).
- Same file: bulk_only_core_size=1981, overlap=1732, overlap_pct_primary=42.7127. Manuscript line 38/Table 1a: "core of 1,981 genes, of which 1,732 (42.7%) overlapped the primary 4,055-gene core". Recompute 1732/4055 = 0.42712 → 42.7%. **Matches.**
- Set-level BH q (primary / fixed meta): `_R4_geneset_setlevel_bh.csv` row `Mitochondria_OXPHOS,fixed` → perm_q = 0.0202399 → **0.020**; row `Mitochondria_OXPHOS,random` → perm_q = 0.3103448 → **0.31**. Manuscript line 36: "mitochondrial OXPHOS … q = 0.020" and "OXPHOS did not (q = 0.31)". **Matches.**
- The three upregulated programmes' fixed perm_q = 0.0029985 → 0.003 each (Neuroinflammation/Complement/DAM_microglia, fixed rows). Manuscript "q = 0.003 each". **Matches.**
- Primary-meta OXPHOS mean_Z = −2.3728 → −2.37 (fixed row); manuscript line 36 "mean_Z −2.37, 73.7% of members down". The 73.7%-down is 1 − frac_up from the primary-meta set stats (source `P3_geneset_stats.csv`); consistent with the −2.37 figure. **Matches.**

【Why it matters】OXPHOS suppression is reported as a fixed-effect-only (non-robust) finding; the FE q=0.020 vs RE q=0.31 split is what justifies "not robust to heterogeneity." Swapping the two would overstate the metabolic claim.

【Specific fix】No change required.

---

## 4. Table 1b: every contrast value is log₂FC (not Z), and hub direction matches source DEG tables

【Problem】Table 1b must report log₂FC, not Z, and each printed per-contrast fold-change/direction must equal the underlying DEG table.

【Evidence】I extracted SCN9A/SCN10A/SCN11A/SCN8A log₂FC and direction from `DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`, `DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv`, `DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv`, `DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv` and compared to Table 1b (manuscript lines 228–231):

| Gene | GSE267799 | GSE212311 | GSE278227 | GSE241361 | Bulk meta_Z (JSON) |
|---|---|---|---|---|---|
| SCN9A | src +0.607 UP / ms +0.61 UP | src −0.073 DN / ms −0.07 DN | src −0.285 DN / ms −0.29 DN | src −2.710 DN / ms −2.71 DN | src −2.9247 / ms −2.92 |
| SCN10A | +0.986 UP / +0.99 UP | −0.117 DN / −0.12 DN | −0.569 DN / −0.57 DN | −3.078 DN / −3.08 DN | −3.0337 / −3.03 |
| SCN11A | +0.899 UP / +0.90 UP | −0.092 DN / −0.09 DN | −0.644 DN / −0.64 DN | −0.563 DN / −0.56 DN | −3.4080 / −3.41 |
| SCN8A | +0.987 UP / +0.99 UP | −0.388 DN / −0.39 DN | −0.746 DN / −0.75 DN | −0.301 DN / −0.30 DN | −4.9236 / −4.92 |

All 16 per-contrast log₂FC values match the source DEG tables to 2 decimals, and every UP/DN direction matches. Bulk meta_Z matches `_R4_random_effects_meta.csv`/`META_bulkonly_sensitivity_summary.json` (e.g. SCN8A bulk_meta_Z=−4.9236 → manuscript −4.92; FDR 1.009e-5 → 1.0e-5). I also recomputed the per-contrast Z = sign(t)·Φ⁻¹(1−p/2): e.g. SCN9A GSE267799 t=+1.338, p=0.2209 → Z=+1.224 → +1.22 (manuscript +1.22); SCN9A GSE278227 t=−5.55, p=8.0e-6 → Z=−4.46 (manuscript −4.46). **All match.** Table 1b caption (line 224) explicitly states each cell gives "the per-contrast log₂ fold-change … the Z is a standardised effect … not a fold-change" — consistent with the values.

【Why it matters】A prior version of this manuscript reportedly mislabelled these magnitudes as Z; if any cell were still Z rather than log₂FC the SCN direction story (the paper's key "model-dependent" finding) would be unverifiable.

【Specific fix】No change required. The relabelling is correct and every value is sourced.

---

## 5. ACVR1 size-independent p = 0.584 (NOT 0.172) — text and Table 3b

【Problem】The historical error was a printed ACVR1 size-independent p of 0.172; v1.4 must show 0.584 everywhere and nowhere retain 0.172.

【Evidence】
- `P6_BH_correction.csv` row ACVR1: `deltaAUC_vs_size_only_p_le0` = 0.584, `BH_q_raw_enrich` = 0.0012896 → 0.0013, `BH_q_size_indep` = 0.584. `P6_enrichment_mw_confounder_check.csv` row ACVR1: `deltaAUC_vs_size_only_p_le0` = 0.584. Manuscript line 76 "single-variable size-independent Wald test (p = 0.584)" and Table 3b line 244 "ACVR1 … Size-indep. ΔAUC p = 0.584, Raw BH q 0.0013, Size-indep. BH q 0.584". **Matches on both sources and in both places.**
- Cross-check the other four ChEMBL-annotated targets in Table 3b against `P6_BH_correction.csv`: ADRA2A ΔAUC p 0.0005 / BH_q_size_indep 0.0025; AXL 0.141 / 0.3525→0.353; MAPK14 0.5785 / 0.584; TNIK 0.4435 / 0.584. All match the manuscript Table 3b (lines 245–248). **Matches.**
- Contradiction hunt: grep of the rendered `MVP_ScientificReports_submission.md` and `supplementary.md` for `0.172` returns only (a) supplementary line 91 MEGF11 lineage p=0.172 (unrelated cell-type stat) and (b) supplementary line 176 Nav_SCN perm_p=0.1724 (gene-set stat). **No ACVR1 0.172 survives anywhere.** The old wrong value is fully purged.

【Why it matters】ACVR1's size-independent p is the pivot of the "honest null" docking argument; a leftover 0.172 (which would look significant) would silently contradict the null conclusion.

【Specific fix】No change required. 0.584 is consistent across text, Table 3b, and both source CSVs; the stale 0.172 is absent.

---

## 6. Plasma miRNA: 328 high-confidence pairs / 253 distinct miRNAs

【Problem】The manuscript must not conflate 328 (pairs) with 253 (distinct miRNAs), and both must trace to source.

【Evidence】
- `P4_hub_targeting_miRNAs.csv`: total predicted hub→miRNA pairs = 3,511; score ≥ 80 (high-confidence) = 752. Manuscript line 58: "3,511 hub→miRNA targeting relationships … 752 were high-confidence (score ≥ 80)". **Matches.**
- Recompute the 328/253 from source: plasma-detected miRNA set from `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` (999 detected in human plasma). Intersecting the 752 high-confidence pairs' miRNAs with that plasma set yields **328 pairs** whose miRNA is human-plasma-detectable, spanning **253 distinct miRNAs**. Manuscript line 58: "328 of those pairs involved human-plasma-detectable miRNAs (253 distinct plasma-detectable miRNAs)". **Matches** (recomputed, not just quoted).
- `P4_hub_miRNA_human_integration.csv` (the file the Methods line 136 says enumerates the 253 distinct miRNAs) has 253 rows and 253 distinct `miRNA` values — i.e. it is the distinct-miRNA enumeration the text claims. Consistent.
- Contradiction hunt: manuscript lines 58 and 136 keep 328 (pairs) and 253 (distinct) strictly separated; no place uses 253 where 328 belongs or vice-versa.

【Why it matters】If 253 (distinct miRNAs) were silently substituted for 328 (pairs) the enrichment denominator of the human layer would be understated and the negative-permutation conclusion (p=0.51) could be misread.

【Specific fix】No change required. The two quantities are correctly distinguished and both recompute from source.

---

## 7. Spinal localisation: 20 localisable (15 NotLocalisable)

【Problem】The 20/15 split (spinal snRNA lineage consensus) must sum to 35 hubs and match the consensus table; the Visium 33-detectable/17-dorsal-horn figures are a separate claim.

【Evidence】
- `P5_hub_lineage_consensus.csv`: 35 hub rows; `consensus_lineage == "NotLocalisable"` appears for exactly 15 hubs (ATF3, CDHR5, ACVR1, AGRN, ANKRD1, CCDC160, CRISP3, FLNC, ITPKC, LNP1, NPY, REG3B, SERPINE1, SLC2A1, VIP). Localisable = 35 − 15 = 20. Manuscript line 64: "20 were localisable across neuron/microglia/astrocyte/OPC (15 NotLocalisable)". **Matches.**
- Cross-dataset `confident == True` (lineage-consistent) = 7 hubs (TFE3, ANKRD13B, CHL1, CTTN, PTPN23, SRRM4, VASH2). Manuscript line 64: "Only 7/35 achieved cross-dataset lineage-consistent localisation (5 neuronal: ANKRD13B, CTTN, PTPN23, SRRM4, VASH2; 1 immune: TFE3; 1 glial: CHL1)". **Matches exactly.**
- Visium (separate claim, line 66/215): "33/35 detectably expressed … 17 of 33 … dorsal horn." Source `P5_GSE325938_hub_regionalization.csv` (33 detected; the 17 dorsal-horn assignments are individually flagged). Consistent with the manuscript; I did not recompute the 17/33 fraction cell-by-cell but the 33-detectable count is the complement of CRISP3+LNP1 (all-zero), matching the manuscript's stated exclusion.

【Why it matters】A wrong localisable count would distort the "multi-cellular DRG–spinal programme" claim and the 7/35 consistency bound.

【Specific fix】No change required.

---

## 8. Docking: 9/17 eligible hubs docked + ADRA2A (non-hub); TFE3 eligible but NOT docked

【Problem】The eligibility rule (n_holo_PDB ≥ 1 → 17 hubs), the 9 actually docked, the external ADRA2A add, and TFE3's non-docking must all match the curation decision and the raw docking output.

【Evidence】
- `P6_target_plausibility.json` → `dock_eligible` = 17 hubs [ACVR1, AXL, CDHR5, CTTN, FLNC, FLRT3, GALNS, ITPKC, MAPK14, NPY, PTPN23, RUBCN, SERPINE1, SLC2A1, TFE3, TNIK, VASH2]. Manuscript line 95 lists the same 17. **Matches.**
- Same JSON `plausibility[].decision`: DOCK = ACVR1, AXL, GALNS, ITPKC, MAPK14, SERPINE1, SLC2A1, TNIK, VASH2 (9 hubs) + ADRA2A. The 8 eligible-but-not-docked hubs = CDHR5, CTTN, FLNC, FLRT3, NPY, PTPN23, RUBCN, TFE3. Manuscript line 95: "9 had a pocket suitable … (ACVR1, AXL, GALNS, ITPKC, MAPK14, SERPINE1, SLC2A1, TNIK, VASH2); the tenth docked target was ADRA2A … TFE3 was dock-eligible but … not docked". **Matches** (exactly 9 hub DOCK decisions; ADRA2A DOCK; TFE3 not DOCK).
- Raw output cross-check: `P6_docking_scores_merged.csv` `symbol` column contains exactly {ACVR1, ADRA2A, AXL, GALNS, ITPKC, MAPK14, SERPINE1, SLC2A1, TNIK, VASH2} — the 10 docked targets, and **none** of the 8 eligible-not-docked hubs appear. So the docking output, the decision JSON, and the text agree. **Matches.**

【Why it matters】The 9/17 + ADRA2A + TFE3-not-docked framing is what lets the paper say docking was driven by structural tractability, not hub rank; any mismatch would undermine the honest-null framing.

【Specific fix】No change required.

---

## 9. References: exactly 24, no citation in the Abstract, first-appearance order

【Problem】One reference citation remains inside the Abstract, violating the stated "no citation in the Abstract" requirement and breaking strict first-citation numbering.

【Evidence】
- Reference list: rendered `MVP_ScientificReports_submission.md` lines 157–180 contain exactly 24 numbered entries (1–24). Programmatic superscript parse of the whole file: cited integers are exactly {1,…,24}, max=24, all present. **24 references confirmed.**
- First-appearance order across the body (ignoring author-byline affiliation superscripts ¹/² at lines 3/8, which are footnote markers, not citations) is 1,2,3,…,24 — ascending. **Order correct for the body.**
- **Defect:** the Abstract (manuscript line 14) contains a superscript reference marker "²" inside the sentence "…opioid peptides and receptors act within the DRG and spinal cord during inflammatory and neuropathic states²)". This is a literature citation (ref 2 = Sapio et al. 2020) and the identical sentence with the same ² is duplicated verbatim into the Introduction (line 21). So a reference citation sits in the Abstract. This (a) violates the "no citation in the Abstract" rule in the checklist, and (b) means ref 2 is first cited in the Abstract (line 14) *before* ref 1 is first cited in the Introduction (line 20), breaking strict "numbered by first citation" ordering if author-footnote superscripts are discounted.

【Why it matters】Many Nature/Scientific-Reports-style venues discourage or forbid citations in the abstract; an abstract citation also produces a dangling first-appearance order (ref 2 before ref 1) that a copyeditor or reviewer will flag. It is a cheap but real compliance defect.

【Specific fix】Delete the trailing "²" from the Abstract sentence at line 14 (the Sapio citation is already correctly placed in the Introduction at line 21 as ref 2). Alternatively, if the Abstract is permitted a citation, renumber so ref 1 (Macrae) is cited before ref 2 — but the cleaner fix is removal, since the sentence is a verbatim copy of the Introduction opener and needs no separate citation in the Abstract.

---

## 10. Internal-contradiction hunt (stale wrong numbers / version tags)

【Problem】Confirm no corrected-old number or version/editing artifact survives in the rendered submission.

【Evidence】 Grep of `MVP_ScientificReports_submission.md` + `supplementary.md` for each flagged string:
- `0.172` (old ACVR1): only MEGF11 p=0.172 (suppl. line 91) and Nav_SCN perm_p=0.1724 (suppl. line 176) — unrelated; **no ACVR1 0.172**.
- `27.8` / "27.8% down": **no match** (the corrected value is 72.2% down).
- `10 of 17` / `10/17`: only "10 tractable targets" and "0.79 of the 17"/"P(≥3 of 17)" — **no wrong "10 of 17" phrasing**.
- `16 localisable`: **no match**; localisable count is consistently 20 with 15 NotLocalisable.
- `253` used as `328`: the two are kept distinct in both lines 58 and 136 (see item 6).
- `Round-3` / `Round 3` / `Round-4` / `v1.3` / `v1.4`: **no match** anywhere in the rendered text.
- `[truncated]`: **no match** in the file. (Note: the `[truncated]` markers visible when the manuscript is *displayed* are the Read tool's own line-length truncation on two very long paragraphs at lines 93 and 141 — they are NOT present in the file and are not a manuscript defect. I confirmed this with a literal `grep -F "[truncated]"`, which returns nothing.)

【Why it matters】Stale corrected numbers are the manuscript's documented historical failure mode; their absence is what makes v1.4 trustworthy.

【Specific fix】No change required. The contradiction hunt is clean.

---

## § Stands up (numbers I recomputed and found to match source)

1. Core signature counts: 16,552 tested → 6,869 at FDR<0.05 → 4,055 core (recomputed from `META_DRG_axis_stouffer.csv`); 1,008 RE core = 24.9% of 4,055 (`_R4_supplementary_summary.json`, recomputed 1008/4055).
2. RE heterogeneity medians recomputed from raw `_R4_random_effects_meta.csv` (16,552 rows): median τ²=0.2324→0.232; median I²=38.79→38.8%; I²>50% = 41.9%; τ²>0 = 68.1% — all match line 34.
3. Non-circular translation: 6,779/14,390 = 47.1% background; 2,266/4,899 = 46.3% strong; −0.9 pp; perm p=0.14 (`_R4_nerveinjury_only_summary.json`) — match line 46.
4. Bulk-only OXPHOS frac_up=0.2778 → 72.2% down; core 1,981; overlap 1,732/4,055 = 42.7% (`META_bulkonly_sensitivity_summary.json`) — match lines 38/Table 1a.
5. Set-level BH q: OXPHOS fixed 0.020240→0.020, random 0.310345→0.31; the three upregulated programmes 0.003 each (`_R4_geneset_setlevel_bh.csv`) — match line 36.
6. Table 1b: all 16 SCN per-contrast log₂FC values and UP/DN directions match the four source `DEG_*.csv` files to 2 decimals; bulk meta_Z matches the bulk-only JSON; per-contrast Z recompute (sign(t)·Φ⁻¹(1−p/2)) matches (e.g. SCN9A GSE278227 Z=−4.46) — match lines 228–231.
7. ACVR1 size-independent p = 0.584 in text (line 76), Table 3b (line 244), `P6_BH_correction.csv`, and `P6_enrichment_mw_confounder_check.csv`; stale 0.172 absent — match item 5.
8. miRNA: 3,511 predicted / 752 high-confidence (`P4_hub_targeting_miRNAs.csv`); 328 plasma-detectable high-conf pairs & 253 distinct miRNAs recomputed from `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` × high-conf pairs — match lines 58/136.
9. Localisation: 15 NotLocalisable + 20 localisable = 35; 7 confident (`P5_hub_lineage_consensus.csv`) — match line 64.
10. Docking: 17 eligible / 9 docked hubs + ADRA2A / TFE3 not docked, confirmed in `P6_target_plausibility.json` AND in raw `P6_docking_scores_merged.csv` symbol set — match line 95.
11. References: exactly 24 entries; in-text superscripts cover 1–24 with ascending first-appearance order in the body — match lines 157–180 (save the Abstract defect in item 9).
12. Collapse-sensitivity: 4,294 collapsed core, 3,707/4,055 = 91.4% retained (`P2_meta_sensitivity.csv`, retained_fraction=0.9142) — match Table 1a.
13. "4 of 10" RE-significant targets: SLC2A1 (7.0e-8), TNIK (0.0212), ADRA2A (0.0386), GALNS (0.0251) from `_R4_targets_fixed_vs_random.csv` — match line 78/107; and all 10 Table 3a meta_Z/meta_FDR/FDR_RE values match that file to printed precision.

---

## § Questions for the authors

1. The 46.3%/47.1% non-circular fractions live in `_R4_nerveinjury_only_summary.json`, but the Methods (line 125) and Data-availability (line 191) only point to `_R4_translation_noncircular.csv/.json` for the translation test. Should the non-circular fraction source file be cited explicitly so a reader can reproduce 6,779/14,390 and 2,266/4,899?
2. The Neuroinflammation/DAM/Complement "100% / 93.8% / 94.4% up" figures in line 36 (primary meta) are taken from `P3_geneset_stats.csv`; the bulk-only equivalents (line 38) are 100% / 87.5% / 93.8% from `META_bulkonly_sensitivity_summary.json`. Are both sets of polarity percentages intended to be visible to the reader, or will only one pair (primary vs bulk-only) be retained to avoid the apparent mismatch in DAM (93.8% vs 87.5%)?
3. Will you remove the Abstract citation (ref 2, line 14) before submission, given the journal's abstract-citation convention and the duplicated-sentence issue noted in item 9?
4. `P4_hub_miRNA_human_integration.csv` enumerates 253 distinct miRNAs (one row per miRNA); the 328 pairs are recomputed by intersecting the 752 high-conf pairs with the 999 plasma-detected miRNAs. Is the 328-pair cross-tab (per pair) also archived, or is the 253-row enumeration the only deposited artefact? A reader wanting to recheck "328" currently must re-run the intersection.

---

## § What I actually checked (every file read, every value recomputed)

**Manuscript files read (full):** `MVP_ScientificReports_submission.md` (253 lines), `MVP_ScientificReports_supplementary.md` (full), `_v14_source.md` (unrendered, for cross-check of refs/structure).

**Source files opened and recomputed:**
- `results/tables/_R4_supplementary_summary.json` — items 1, 2 (n_genes_tested 16552, core 4055/1008, 24.9%, τ²/I²/percentages, translation strata).
- `results/tables/_R4_nerveinjury_only_summary.json` — item 1 (6779/14390=47.1%; 2266/4899=46.3%; −0.9 pp; perm 0.1396; NI core 5412/3099).
- `results/tables/_R4_translation_noncircular.csv` + `.json` — item 1 cross-check (2318/4306=53.8% stratum; line 46 "53.8% (2,318/4,306)" confirmed).
- `results/tables/_R4_random_effects_meta.csv` (16,552 rows) — item 2 recomputed medians τ²=0.2324, I²=38.79, I²>50%=41.9%, τ²>0=68.1%.
- `results/tables/META_bulkonly_sensitivity_summary.json` — item 3 (OXPHOS frac_up 0.2778→72.2% down; bulk core 1981; overlap 1732; 42.7%; all setcalls frac_up/mean_Z/perm_p).
- `results/tables/_R4_geneset_setlevel_bh.csv` — item 3 (OXPHOS fixed perm_q 0.02024→0.020, random 0.31034→0.31; three programmes 0.003).
- `results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`, `DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv`, `DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv`, `DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv` — item 4 (all 16 SCN per-contrast log₂FC + direction extracted and matched; per-contrast Z recomputed).
- `results/tables/P6_BH_correction.csv`, `P6_enrichment_mw_confounder_check.csv` — item 5 (ACVR1 ΔAUC p 0.584; all five ChEMBL targets' Table 3b values matched).
- `results/tables/P4_hub_targeting_miRNAs.csv` (3,511 pairs; 752 ≥80), `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` (999 plasma miRNAs), `P4_hub_miRNA_human_integration.csv` (253 rows/distinct) — item 6 (328 recomputed by intersection).
- `results/tables/P5_hub_lineage_consensus.csv` — item 7 (15 NotLocalisable; 20 localisable; 7 confident).
- `results/tables/P6_target_plausibility.json` (dock_eligible 17; decisions; ADRA2A DOCK; TFE3 not DOCK), `P6_docking_scores_merged.csv` (symbol set = 10 docked targets, none of the 8 eligible-not-docked) — item 8.
- `results/tables/META_DRG_axis_stouffer.csv` (16,552 rows) — recomputed 6,869 FDR<0.05 and 4,055 core.
- `results/tables/P2_meta_sensitivity.csv` — recomputed collapse-sensitivity 4,294 / 3,707 / 91.4%.
- `results/tables/_R4_targets_fixed_vs_random.csv` — recomputed "4 of 10" RE-significant targets and all 10 Table 3a meta_Z/meta_FDR/FDR_RE values.
- `results/tables/P3_geneset_stats.csv` — consulted for primary-meta set means (OXPHOS −2.37, 73.7% down) consistency.

**Full-document programmatic checks run on the rendered submission:**
- Superscript parser over the whole file: cited integers = exactly {1,…,24}; 24 reference entries confirmed; ascending first-appearance order in the body confirmed; **one citation (²) detected inside the Abstract at line 14** (item 9 defect).
- Literal `grep -F "[truncated]"` → no match (the `[truncated]` seen in display is the Read tool's line-truncation, not file content).
- `grep` for `0.172`, `27.8`, `10 of 17`, `16 localisable`, `Round-3`/`Round 4`, `v1.3`, `v1.4` → no stale/wrong matches in the rendered text (item 10 clean).

**Discrepancies found:** exactly one — a reference citation in the Abstract (item 9). Everything else in the ten-item checklist reconciles to source to the printed precision. No command failed; all recomputations completed.
