# Round-4 Independent Review — A3 (Implementation / provenance & recomputation auditor)

**Manuscript:** `reports/MVP_ScientificReports_submission.md` (v1.3, 2026-09-20)
**Auditor role:** A3 — recompute every headline number from raw/processed source files; flag every mismatch, broken table, and internal contradiction.
**Independence statement:** I read only the manuscript, the supplementary file, the panel brief, and the raw/processed data under `results/tables/`, `data/`, `docking/`, `scripts/`. I did **not** read any `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md`, the `reviews/` outputs of other rounds/experts, `PROJECT_PLAN.md`, `README.md`, the author verification statement, `submission_pack/`, or other reviewers' files.

**Conflict-resolution note (mandatory disclosure).** The forbidden-list instruction says "any `*_R3_*.json`". However, the recomputation checklist explicitly requires me to verify items 3 and 14 from `results/tables/_R3_bulkonly_meta_summary.json` and `results/tables/_R3_plausibility.json`. These two files live in the explicitly-permitted `results/tables/` data directory and are pure computational outputs (bulk-only meta summary; 10-target docking-eligibility/plausibility table), **not** prior-review verdicts or author rebuttals. Reading them preserves the spirit of independence (no prior-reviewer opinion was ingested). I therefore read them and flag this decision for the editor's transparency. Every number I cite from them was cross-checked against the corresponding CSV where one exists (e.g., SCN bulk meta_Z/FDR, docking AUCs, BH q-values).

---

## A. Mandatory recomputation checklist — verdict per item

| # | Claim | Verdict | Evidence |
|---|-------|---------|----------|
| 1 | Core 4,055 / 16,552 genes | **MATCH** | stouffer 16,552 rows; core 4,055; def `meta_FDR<0.05 & consistency≥0.8` reproduces 4,055 exactly |
| 2 | Translation 53.9% = 7,751/14,390; core 69.5% = 2,473/3,556; binomial ≈10⁻²⁰ | **MATCH** | recomputed 7,751/14,390 (0.5386); 2,473/3,556 (0.6954); binom p = 1.93e-20 |
| 3 | Bulk-only core 1,981; overlap 1,732/4,055 = 42.7% | **MATCH** | `_R3_bulkonly_meta_summary.json`: 1981 / 1732 / 42.71% |
| 4 | Gene-set: Neuroinf +4.94/100%up; DAM +3.88/93.8%up; Complement +3.44/94.4%up; OXPHOS −2.37/73.7%down/p=0.004 | **MATCH (primary)** — but see Finding F1 (bulk-only OXPHOS mislabeled) | `P3_geneset_stats.csv` rows |
| 5 | SCN9A/10A/11A/8A bulk meta_Z/FDR + per-contrast directions | **MATCH** (labeling caveat F5) | stouffer lfc signs + `_R3_bulkonly_meta_summary.json` scn_tab |
| 6 | 35 hubs; 32/35 in core; 5/35 three-method | **MATCH** | `P3_hub_genes.csv` |
| 7 | LODO AUCs + CIs | **MATCH (values)** — CI-honesty caveat F4 | `P3_lodo_auc_ci.csv` |
| 8 | Bootstrap 0/35 ≥0.9; max 15.5% | **MATCH** | `P3_hub_bootstrap.csv` hub_freq max 0.155 |
| 9 | Human miRNA 3,511 / 752 / 253 | **MISMATCH on 253** — see Finding F2 | `P4_hub_targeting_miRNAs.csv`, `P4_hub_miRNA_human_integration.csv` |
| 10 | DRG GSE216039 25 detected, 20/25 injured-neuron, folds | **MATCH** | `P5_GSE216039_DRG_hub_finetype_top.csv` |
| 11 | Spinal GSE328175 33/35 present, 24 detectable, 7/35 cross-dataset | **MATCH except "16 localisable"** — see Finding F3 | `P5_hub_lineage_consensus.csv` |
| 12 | Visium 33 detectable, 17/33 dorsal horn, floor check | **MATCH** | `P5_GSE325938_hub_regionalization.csv` |
| 13 | Docking reverse-control AUCs, ADRA2A breadth 0.618→0.532, Table 3b BH q | **MATCH** | `P6_reverse_control.csv`, `P6_breadth_chembl_power.csv`, `P6_BH_correction.csv` |
| 14 | 17 dock-eligible hubs; 10 actually docked | **MISMATCH (subset logic)** — see Finding F6 | `_R3_plausibility.json` + Table 3a + Methods |

Detailed 4-part findings for every **mismatch / contradiction** follow. Matched items are confirmed above and in § "What I actually checked".

---

## B. Detailed findings (every item carries the four mandatory parts)

### F1 — Bulk-only OXPHOS polarity fraction is inverted (T2)

**【Problem】** The bulk-only sensitivity meta-analysis states OXPHOS is "−2.80, 27.8% down", but the source JSON records `frac_up = 0.2778` for bulk-only OXPHOS, i.e. 27.8% *up* / **72.2% down** — the manuscript printed the fraction-up as if it were fraction-down, which inverts the apparent polarity of a central programme.

**【Evidence】** Manuscript `reports/MVP_ScientificReports_submission.md:36` — "OXPHOS (−2.80, 27.8% down, perm p ≤ 0.0005, polarity-opposed)". Source `results/tables/_R3_bulkonly_meta_summary.json:128-134`:
```
"Mitochondria_OXPHOS": { "n": 18, "mean_Z": -2.7987661349437634,
  "stouffer_Z": -11.874159077843995, "perm_p": 0.0004997501249375312,
  "frac_up": 0.2777777777777778 }
```
`frac_up = 0.2778` ⇒ 27.8% of members are *up*, so 72.2% are down. The primary six-input OXPHOS is correctly reported as 73.7% down (`P3_geneset_stats.csv` `frac_up 0.2632`). So the bulk-only value should read 72.2% down (or "27.8% up"), not "27.8% down".

**【Why it matters】** This is a headline sensitivity analysis used to claim "the neuroimmune–metabolic axis *interpretation* … is unchanged" (manuscript line 36). As written, "27.8% down" makes OXPHOS look majority-*up* in the bulk-only analysis (72.2% up), which would contradict the primary 73.7%-down finding and undermine the "axis survives intact" claim. The underlying result is actually *consistent* (72.2% down ≈ primary 73.7% down); only the reported sign/fraction is wrong, but a reader cannot tell that from the text.

**【Specific fix】** Replace the clause in line 36 with:
> "OXPHOS (−2.80, 72.2% down, perm p ≤ 0.0005, polarity-opposed)"
(or "27.8% up / 72.2% down"). Optionally add a one-line note that bulk-only OXPHOS remains majority-down, consistent with the primary meta.

---

### F2 — Human-miRNA "253" high-confidence plasma pairs is mislabeled; true pair count is 328 (T2)

**【Problem】** The manuscript reports "253 of those [the 752 high-confidence pairs] involved human-plasma-detectable miRNAs", but 253 is the count of *distinct plasma-detectable miRNAs*, not of high-confidence *pairs*. The recomputed number of high-confidence hub→miRNA pairs involving a plasma-detectable miRNA is **328** (spanning 29 hubs; 253 distinct plasma miRNAs).

**【Evidence】** Manuscript `reports/MVP_ScientificReports_submission.md:48` and abstract `:14` — "253 of those involved human-plasma-detectable miRNAs". Recomputation command and output:
```
python - <<'PY'
import pandas as pd
h = pd.read_csv("results/tables/P4_hub_targeting_miRNAs.csv")
integ = pd.read_csv("results/tables/P4_hub_miRNA_human_integration.csv")
hc = h[h['score']>=80]
plasma_mir = set(integ['miRNA'])
hc_plasma = hc[hc['miRNA'].isin(plasma_mir)]
print(len(h), len(hc), hc['symbol'].nunique())          # 3511 752 31
print(len(integ), len(plasma_mir))                       # 253 253
print(len(hc_plasma), hc_plasma['symbol'].nunique())     # 328 29
PY
# -> 3511 pairs ; 752 HC(>=80) ; 31 hubs in HC set ; integ 253 rows = 253 plasma miRNAs ; HC plasma pairs = 328 ; 29 hubs
```
Enumerating the `targets` column of `P4_hub_miRNA_human_integration.csv` (splitting on `;`) yields 328 (hub,miRNA) pairs, all of which are score≥80, spanning 253 distinct miRNAs and 29 hubs. The number 253 is real but denotes *miRNAs* (and it is also the `n` of the set-level permutation test: `P4_setlevel_test.json` → `"n":253, "perm_p":0.5101`), not *pairs*.

**【Why it matters】** The sentence asserts a count of *pairs* ("253 of those [752 pairs]"), which a reader will compare against the 752. The correct pair count is 328 (44% of the high-confidence set, not 34%). The statement also understates the human-plasma coverage of the high-confidence layer. It is a units error, not a fabrication, but it is a wrong number in a result that the manuscript frames as an "honest negative boundary".

**【Specific fix】** Replace line 48 (and the abstract line 14) with a units-correct version, e.g.:
> "of which 752 were high-confidence (score ≥ 80); these high-confidence pairs involved 253 distinct human-plasma-detectable miRNAs (328 of the 752 high-confidence pairs)"
(keep "set-level permutation test returned p = 0.51" — verified).

---

### F3 — Spinal "16 localisable" conflicts with the consensus file (15 NotLocalisable ⇒ 20 localisable) and Fig. 4 (T3)

**【Problem】** Results line 54 states "16 localisable across neuron/microglia/astrocyte/OPC" for the spinal snRNA, but the cross-dataset consensus table it is checked against (`P5_hub_lineage_consensus.csv`) has 15 `NotLocalisable` hubs ⇒ 20 localisable, and Fig. 4's own legend reports "NotLocalisable n=15" (⇒ 20 localisable). The number 16 cannot be reproduced from the consensus file and is inconsistent with the manuscript's own Fig. 4.

**【Evidence】** Manuscript `reports/MVP_ScientificReports_submission.md:54` — "24 detectable (mean pseudobulk expression > 0 in ≥1 lineage), 16 localisable across neuron/microglia/astrocyte/OPC." Source `results/tables/P5_hub_lineage_consensus.csv` (35 rows): `consensus_lineage == NotLocalisable` for exactly 15 symbols (ATF3, CDHR5, ACVR1, AGRN, ANKRD1, CCDC160, CRISP3, FLNC, ITPKC, LNP1, NPY, REG3B, SERPINE1, SLC2A1, VIP) ⇒ 20 localisable. Fig. 4 legend (`submission.md:190`) states "Neuronal n=8, Glial n=3, Immune n=4, Mixed n=5, NotLocalisable n=15" (8+3+4+5+15 = 35). The panel brief also lists "15 NotLocalisable" for this file. No defensible threshold applied to the consensus file yields 16 (excluding the 5 Mixed gives 15; excluding the 4 Immune gives 16, but microglia/astrocyte/OPC are explicitly included in the manuscript's own wording).

**【Why it matters】** A secondary descriptive count is internally inconsistent with the manuscript's own figure and source table. It does not change the 7/35 cross-dataset-lineage finding (verified, correct), but it is the kind of unreconciled number that an auditor must flag, and it suggests the "16" may be a leftover from an earlier single-dataset cut.

**【Specific fix】** Either (a) change line 54 to "20 localisable (15 NotLocalisable in the cross-dataset consensus; see Fig. 4)", or (b) if "16" is a deliberately stricter GSE328175-only metric, define it explicitly (e.g., "16 localisable at pseudobulk detection fraction > X in GSE328175 alone") and cite the GSE328175-specific file rather than implying it comes from the consensus. Reconcile with the Fig. 4 "NotLocalisable n=15" wording.

---

### F4 — LODO CI for n=6 (and two other folds) is degenerate [1.0, 1.0]; "honest" only in the narrow computational sense (T3)

**【Problem】** The cross-animal LODO fold GSE212311 (n=6) reports AUC 1.000 with CI [1.000, 1.000] — a zero-width interval that conveys false certainty. Two further folds (GSE278227 n=28 and GSE241361 mouseDRG n=9) also report degenerate [1.0,1.0] CIs. The manuscript presents these CIs without noting they collapse at perfect separation.

**【Evidence】** `results/tables/P3_lodo_auc_ci.csv`:
```
GSE278227_1W_ratDRG   1.0   1.0   1.0   28   <- width 0
GSE267799_incision... 0.9167 0.7291 1.0 20   <- width 0.2709
GSE241361_mouseDRG    1.0   1.0   1.0   9    <- width 0
GSE241361_mouseSC     0.95  0.7086 1.0 9    <- width 0.2914
GSE212311_CCI_ratDRG  1.0   1.0   1.0   6    <- width 0
```
Recomputed widths: three of five folds are exactly 0. The DeLong/bootstrap CI is pinned at 1.0 because AUC=1 with no overlapping predictions cannot estimate a lower bound; this is a known failure mode, not genuine precision.

**【Why it matters】** The checklist explicitly asks to "verify the CI width for n=6 is honest." A [1.0,1.0] CI on n=6 (3 cases / 3 controls) is the method's output but is misleading: with six samples and perfect separation the *true* generalisation is highly uncertain. The same applies to the n=28 fold, where a zero-width CI on 28 held-out samples hints at either exceptionally strong signal or subtle leakage/over-fitting in that LODO split. Reporting these without comment overstates confidence in the cross-animal floor.

**【Specific fix】** Add a methods/results caveat, e.g.:
> "Three LODO folds (GSE278227 n=28, GSE212311 n=6, GSE241361 DRG n=9) reached AUC 1.000 and their DeLong CIs collapsed to [1.0, 1.0] at perfect separation; these bounds are undefined rather than precise, and the cross-animal floor should be read from the non-degenerate GSE267799 fold (0.917 [0.729, 1.000])."
Consider replacing DeLong with a bias-corrected bootstrap CI, or reporting the CI only for folds where it is non-degenerate.

---

### F5 — Table 1b per-contrast parenthetical values are Z-statistics, not log-fold-changes; magnitudes differ from the stouffer `lfc_*` columns (T3)

**【Problem】** Table 1b prints per-contrast values such as SCN9A "UP (+1.22), DN (−0.72), DN (−4.46), DN (−1.02)". These are per-contrast **Z-statistics** (they match `_R3_bulkonly_meta_summary.json` `scn_tab`), whereas the `lfc_*` columns of `META_DRG_axis_stouffer.csv` hold log-fold-changes of different magnitude (SCN9A GSE267799 lfc = +0.607, GSE212311 −0.073, GSE278227 −0.285, GSE241361 −2.710). The table does not label the quantity, inviting a reader to mistake them for effect sizes.

**【Evidence】** `reports/MVP_ScientificReports_submission.md:201-206` (Table 1b). Stouffer CSV `META_DRG_axis_stouffer.csv` `lfc_*` for SCN9A:
```
GSE267799 +0.607 (UP) | GSE212311 -0.073 (DN) | GSE278227 -0.285 (DN) | GSE241361 -2.710 (DN)
```
`_R3_bulkonly_meta_summary.json` `scn_tab.SCN9A.per_contrast`:
```
GSE267799 Z 1.224 (UP) | GSE212311 Z -0.716 (DN) | GSE278227 Z -4.465 (DN) | GSE241361 Z -1.016 (DN)
```
The **signs/directions match** across both sources and Table 1b (verified — the checklist's direction check passes). Only the *magnitudes* differ because they are different statistics (lfc vs Z). Table 1b's numbers equal the JSON Z-values, not the stouffer lfc.

**【Why it matters】** Directions are correct, so this is not a contradiction in sign — but the unlabeled parentheticals will be read as fold-changes by most readers, and they cannot be reconciled with the `lfc_*` columns a reviewer would open. Transparency requires labeling the statistic.

**【Specific fix】** Add a Table 1b footnote:
> "Parenthetical per-contrast values are signed Z-statistics (bulk-only meta), not log₂ fold-changes; directions were confirmed against the Stouffer per-contrast lfc columns."
(or rename the column header to "Per-contrast Z (direction)").

---

### F6 — "17 dock-eligible hubs, of which 10 were actually docked" is internally inconsistent (T2)

**【Problem】** Results line 85 says 17 hubs were docking-eligible and "of these, 10 had a pocket suitable … and were actually docked." But the 10 actually-docked targets are **not a subset of the 17 eligible hubs**: ADRA2A (docked, in Table 3a / JSON `plausibility`) is *not* among the 17 eligible hubs, and TFE3 (in the 17 eligible hubs) was *not* docked (absent from Table 3a and from the JSON `plausibility` array).

**【Evidence】** Manuscript `reports/MVP_ScientificReports_submission.md:85` lists 17 eligible hubs (…TFE3…, no ADRA2A) and claims "10 … actually docked". Methods `:121-122` lists the 10 dockable targets as "GALNS, SLC2A1, TNIK, ITPKC, AXL, SERPINE1, MAPK14, VASH2, ACVR1, ADRA2A" — i.e. 9 of the 17 hubs + ADRA2A, and **excludes TFE3**. Table 3a (`submission.md:70-81`) likewise omits TFE3 and includes ADRA2A. Source `results/tables/_R3_plausibility.json`: `dock_eligible` (17) = {ACVR1, AXL, CDHR5, CTTN, FLNC, FLRT3, GALNS, ITPKC, MAPK14, NPY, PTPN23, RUBCN, SERPINE1, SLC2A1, TFE3, TNIK, VASH2}; `plausibility` (10 docked) = {GALNS, SLC2A1, TNIK, ITPKC, AXL, SERPINE1, MAPK14, VASH2, ACVR1, ADRA2A}. Intersection of docked with the 17 = 9 (all except ADRA2A); TFE3 is eligible but not docked. So "10 of the 17" is false; it is "9 of the 17 + ADRA2A".

**【Why it matters】** The Results sentence conflates "hubs docked" with "targets docked". A reader tallying the 17→10 subset will find ADRA2A (not a hub) in the docked set and TFE3 (an eligible hub) missing, and cannot reconcile line 85 with Methods/Table 3a. The *counts* (17 eligible, 10 docked) are each correct; only the subset relationship is wrong.

**【Specific fix】** Rephrase line 85 to:
> "Seventeen hubs carried a tractable holo-PDB target (n_holo_PDB ≥ 1); of these, nine (ACVR1, AXL, GALNS, ITPKC, MAPK14, SERPINE1, SLC2A1, TNIK, VASH2) were docked, ADRA2A was additionally docked as a known analgesic target (10 docked targets total; see Table 3a), and TFE3 — though eligible — lacked a suitable pocket and was not docked."

---

### F7 — ACVR1 single-variable size-independent p is stated as 0.172 in prose but 0.584 in the manuscript's own Table 3b and source files (T2)

**【Problem】** The Results prose draws the ACVR1 contradiction as "multivariate p = 9.6e-4 vs single-variable size-independent Wald test (p = 0.172)", but every source file and the manuscript's own Table 3b give the single-variable size-independent p as **0.584**, not 0.172.

**【Evidence】** Manuscript `reports/MVP_ScientificReports_submission.md:66` — "the ACVR1 likelihood-ratio 'significance' contradicts its own single-variable size-independent Wald test (p = 0.172)". But:
- Table 3b (`submission.md:219`): ACVR1 "Size-indep. ΔAUC p = 0.584".
- `results/tables/P6_BH_correction.csv:2`: `ACVR1,0.797,0.00103,0.584,0.00129,0.584` → `deltaAUC_vs_size_only_p_le0 = 0.584`.
- `results/tables/P6_enrichment_mw_confounder_check.csv:3`: ACVR1 `deltaAUC_vs_size_only_p_le0 = 0.584`.
No file contains 0.172 for ACVR1. The multivariate LR p = 9.6e-4 is correct (`P6_multivariate_physchem_control.csv` / S4 Panel A: ACVR1 `LR docking-residual p = 9.6e-4`).

**【Why it matters】** This is the manuscript's central "honest contradiction" example (the docking signal for ACVR1 survives only in a post-hoc multivariate model, not the simpler size-independent test). The prose number (0.172) contradicts the manuscript's own Table 3b and all three source files (0.584). The *substance* of the contradiction is valid (9.6e-4 vs ~0.58), but the quoted single-variable p is wrong, which weakens the very point the author is making and looks like a stale draft value.

**【Specific fix】** Replace "p = 0.172" with "p = 0.584" in line 66 (and anywhere else 0.172 appears). The sentence then reads consistently with Table 3b:
> "… contradicts its own single-variable size-independent test (p = 0.584, Table 3b) …"

---

### F8 — Abstract "honest null" for ADRA2A slightly understates the Results' "inconclusive" MW-adjusted signal (T3)

**【Problem】** The abstract frames ADRA2A as an "honest full-library repurposing [that] does not yet support a specific analgesic" (full-library AUC 0.532, p = 0.118), omitting the Results' nuance that the MW-adjusted AUC is 0.578 with ΔAUC p ≈ 0.0005 ("inconclusive, not a confirmed null").

**【Evidence】** Abstract `submission.md:14` — "A full-library docking screen of 3,085 drugs found no size-independent enrichment for any of 10 tractable targets (ADRA2A Tier-1 0.618 → full-library 0.532, p = 0.118). Honest full-library repurposing does not yet support a specific analgesic." Results `submission.md:83` — "after MW adjustment the AUC was 0.578 with a weak but significant ΔAUC (p ≈ 0.0005), so the ADRA2A docking result is inconclusive, not a confirmed null." Source `P6_enrichment_mw_confounder_check.csv:4`: ADRA2A `AUC_MW_adjusted 0.578`, `deltaAUC_vs_size_only_p_le0 0.0005`.

**【Why it matters】** The full-library AUC (0.532, NS) genuinely supports "no robust enrichment", so the abstract is defensible. But the abstract's unqualified "honest null" drops the MW-adjusted "inconclusive" signal that the Results highlights, so the two sections are not perfectly aligned in nuance. A reader relying on the abstract alone would miss the borderline MW-adjusted effect.

**【Specific fix】** Add a clause to the abstract, e.g.:
> "… (ADRA2A Tier-1 0.618 → full-library 0.532, p = 0.118; MW-adjusted 0.578, inconclusive)."
This keeps the abstract consistent with the Results' "inconclusive" framing.

---

## C. Markdown table & cross-document consistency checks

**Tables 1b and 3b are well-formed (no broken pipes).** Table 1b (`submission.md:201-206`) has 8 columns in both header and every data row (8 cells each). Table 3b (`submission.md:217-223`) has 8 columns in header and all 5 data rows. No ragged rows found. ✔

**Title = 19 words** (`submission.md:1`) — recomputed `len(title.split()) = 19`. ✔ matches the claimed "title (19 words)".
**Abstract ≈ 195 words** (between `## Abstract` and the following `---`); the brief caps it at ≤200. ✔ within limit.
**12 GEO datasets / 5 studies / 6 contrasts** — abstract `:14` "12 GEO datasets … (5 independent studies, 6 contrasts)" matches Methods `:104` (12 accessions listed) and `:107` ("five independent studies are represented by six contrasts"). ✔ consistent.
**References — 22 listed, all cited, no orphan, no duplicate.** Reference list is numbered 1–22 consecutively (`submission.md:134-155`). In-text citations cover 1–22; reference 20 and 21 are cited via the range "¹⁹–²²" at `submission.md:91` (standard range notation spanning 19–22), so 21 is *not* an orphan. No duplicated numbers. ✔ (I initially flagged 21 as missing from an automated superscript scan, but it is covered by the 19–22 range — confirmed by reading the line.)

---

## D. § Stands up (recomputed and found correct — delivered, not filler)

1. **Meta core size and gene count (item 1).** `META_DRG_axis_stouffer.csv` has exactly 16,552 data rows; `META_DRG_axis_CORE_signature.csv` has exactly 4,055; re-applying the stated definition `meta_FDR < 0.05 & consistency ≥ 0.8` reproduces 4,055 and the symbol set is identical to the file (`set(core_def)==set(core)` → True). The single most foundational number is exactly right.

2. **Incision translation fractions + binomial (item 2).** Recomputed directly: `concordant_incision` True = 7,751 of 14,390 shared genes (0.5386 → "53.9%"); among the 4,055 core, 2,473 of 3,556 (0.6954 → "69.5%"). Two-sided binomial test vs 0.5 gives p = 1.93e-20 (the claimed "≈10⁻²⁰" is plausible and correct); the core-restricted test gives an even smaller p = 3.3e-123. The reframing as "conserved nerve-injury response, not CPSP-specific" rests on a correctly computed 53.9%.

3. **Gene-set statistics (item 4, primary meta).** `P3_geneset_stats.csv`: Neuroinflammation mean_Z 4.943 / frac_up 1.0 (100% up); DAM 3.884 / 0.9375 (93.8% up); Complement 3.441 / 0.9444 (94.4% up); OXPHOS −2.373 / frac_up 0.2632 (73.7% down) / perm_p 0.003998 (≈0.004). All four match the manuscript to the decimal. The permutation-calibrated neuroimmune–metabolic axis is real in the data.

4. **SCN bulk meta_Z/FDR and directions (item 5).** `_R3_bulkonly_meta_summary.json` `scn_tab` gives SCN9A −2.9247/0.01078, SCN10A −3.0337/0.00795, SCN11A −3.408/0.00264, SCN8A −4.9236/1.009e-5 — matching Table 1b (−2.92/0.011, −3.03/0.008, −3.41/0.003, −4.92/1.0e-5). Per-contrast signs (UP in GSE267799, DN elsewhere, DN in translatome) match both the stouffer `lfc_*` columns and Table 1b. SCN8A being the most significant is correct.

5. **Hub set and stability (items 6, 8).** `P3_hub_genes.csv`: 35 rows; `in_meta_core` True for 32 (only REG3B, ANKRD1, MEGF11 False); `n_methods == 3` for exactly 5 (SPRR1A, ATF3, TFE3, CDHR5, GALNS). `P3_hub_bootstrap.csv`: max `hub_freq` = 0.155 (CDHR5) and 0/35 reach ≥0.9. Both claims are exact.

6. **DRG and Visium spatial localisation (items 10, 12).** `P5_GSE216039_DRG_hub_finetype_top.csv`: 25 detected, 20 of 25 with `top_finetype == Injured_RegenNeuron`, and the quoted folds (SPRR1A 17.39→17.4×, ECEL1 25.69→25.7×, NPY 10.04→10.0×, FLNC 10.21→10.2×) match. `P5_GSE325938_hub_regionalization.csv`: 33 detectably expressed (CRISP3 & LNP1 all-zero excluded), 17 DorsalHorn, and **all 17 have `top_detection ≥ 0.05`** (min among them = ITPKC 0.123); the below-floor set (CDHR5, SERPINE1, VIP, REG3B, ANKRD1 + CRISP3, LNP1) is exactly the 7 hubs with `top_detection < 0.05`. Both spatial claims are exact.

7. **Docking AUCs, breadth flip, and BH q (item 13).** `P6_reverse_control.csv`: AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779, ADRA2A 0.532. `P6_breadth_chembl_power.csv`: ADRA2A Tier-1 0.6184 → full 0.5325 (p=0.118 ✓). `P6_BH_correction.csv` BH q-values (ACVR1 0.584, ADRA2A 0.0025, AXL 0.353, MAPK14 0.584, TNIK 0.584) match Table 3b exactly. The entire docking honesty narrative is internally consistent with its data.

8. **Human-miRNA totals and set-level p (items 9 partial).** 3,511 total predicted hub→miRNA pairs and 752 high-confidence (score≥80) both verify exactly; the set-level permutation p = 0.51 verifies (`P4_setlevel_test.json` → `perm_p 0.5101`, `n 253`). Only the "253 pairs" label is wrong (Finding F2); the surrounding negative-layer claim is sound.

---

## E. § Questions for the authors

1. **OXPHOS bulk-only polarity (F1):** Do you intend "72.2% down" (consistent with the primary 73.7% down) for the bulk-only OXPHOS? The JSON `frac_up = 0.2778` unambiguously means 27.8% up / 72.2% down.
2. **Human-miRNA 253 vs 328 (F2):** Was "253" meant as the count of distinct plasma miRNAs (which it is) rather than high-confidence pairs? The recomputed high-confidence plasma *pairs* number is 328 — please confirm which quantity the text should report.
3. **ACVR1 p 0.172 vs 0.584 (F7):** Is 0.172 a stale draft value? Every source file and your own Table 3b give 0.584 for the single-variable size-independent test. Please confirm 0.584.
4. **10-of-17 docking (F6):** Should line 85 state "9 of the 17 eligible hubs + ADRA2A" rather than "10 of the 17"? ADRA2A is not in the 17 eligible hubs and TFE3 (eligible) was not docked — please reconcile with Methods/Table 3a.
5. **"16 localisable" (F3):** What exact definition yields 16 for the spinal snRNA? The consensus file and Fig. 4 give 15 NotLocalisable (20 localisable). Please specify the metric or correct to 20.
6. **LODO degenerate CIs (F4):** Will you add the DeLong-collapse caveat and/or report a bootstrap CI, especially for the n=28 GSE278227 fold whose [1.0,1.0] CI could hint at leakage?

---

## F. § What I actually checked (every file read, every recompute, verdict)

**Files read (allowed):**
- `reports/MVP_ScientificReports_submission.md` (full manuscript, 228 lines) — source of all claimed numbers.
- `reports/MVP_ScientificReports_supplementary.md` (full, 163 lines) — Tables S1–S5; used to cross-check S1 (lineage), S2 (Visium), S4 (multivariate + BH), S5 (gene-set members).
- `reviews/round4_2026-09-20/_PANEL_BRIEF.md` (orientation only).
- `results/tables/META_DRG_axis_stouffer.csv` (16,552 rows) — items 1, 2, 5.
- `results/tables/META_DRG_axis_CORE_signature.csv` (4,055 rows) — item 1.
- `results/tables/_R3_bulkonly_meta_summary.json` — items 3, 4 (bulk-only), 5 (SCN). *(Read despite the `*.json` forbidden glob; see conflict note — it is raw/processed data, not a review artifact.)*
- `results/tables/_R3_plausibility.json` — item 14. *(Same conflict note.)*
- `results/tables/P3_geneset_stats.csv` — item 4.
- `results/tables/P3_hub_genes.csv` — item 6.
- `results/tables/P3_lodo_auc_ci.csv` — item 7.
- `results/tables/P3_hub_bootstrap.csv` — item 8.
- `results/tables/P4_hub_targeting_miRNAs.csv`, `P4_hub_miRNA_human_integration.csv`, `P4_setlevel_test.json` — item 9.
- `results/tables/P5_GSE216039_DRG_hub_finetype_top.csv` — item 10.
- `results/tables/P5_hub_lineage_consensus.csv`, `P5_GSE328175_SC_ShamSNI_hub_celltype_top.csv` — item 11.
- `results/tables/P5_GSE325938_hub_regionalization.csv` — item 12.
- `results/tables/P6_reverse_control.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_BH_correction.csv`, `P6_breadth_chembl_power.csv` — item 13.

**Recomputes run (managed Python `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`):**

1. Core/genes: `len(st)=16552`, `len(core)=4055`, `set(core_def)==set(core)` → **MATCH**.
2. Translation: `concordant_incision` value_counts `{True:7751, False:6639}`; shared=14,390 (0.5386); core-restricted 2,473/3,556 (0.6954); binom p 1.93e-20 and 3.3e-123 → **MATCH** (binomial ≈10⁻²⁰ plausible).
3. Bulk-only: JSON `bulk_only_core_size 1981`, `overlap 1732`, `overlap_pct_primary 42.71` → **MATCH**.
4. Gene-sets: Neuroinf 4.943/1.0; DAM 3.884/0.9375; Complement 3.441/0.9444; OXPHOS −2.373/0.2632/perm 0.004 → **MATCH (primary)**; bulk-only OXPHOS `frac_up 0.2778` → **MISMATCH** (F1).
5. SCN: stouffer `lfc_*` signs match Table 1b; JSON bulk meta_Z/FDR match Table 1b → **MATCH**; parentheticals are Z not lfc → **caveat F5**.
6. Hubs: 35 rows, 32 `in_meta_core` True, 5 `n_methods==3` → **MATCH**.
7. LODO: AUCs 1.0/1.0/0.9167/1.0/0.95 with n 28/6/20/9/9; 3 folds zero-width CI → **MATCH values**, **caveat F4**.
8. Bootstrap: max `hub_freq` 0.155, 0/35 ≥0.9 → **MATCH**.
9. miRNA: 3,511 pairs; 752 score≥80 (31 hubs); integration 253 miRNAs; high-conf plasma pairs = 328 (29 hubs) → **MISMATCH on "253 pairs"** (F2); set-level p 0.5101 → **MATCH**.
10. DRG: 25 detected, 20 Injured_RegenNeuron, folds 17.4/25.7/10.0/10.2 → **MATCH**.
11. Spinal: consensus 15 NotLocalisable (⇒20 localisable); 7 confident cross-dataset (TFE3, ANKRD13B, CTTN, PTPN23, SRRM4, VASH2, CHL1) → **MATCH 7/35**; "16 localisable" → **MISMATCH** (F3).
12. Visium: 33 detectable, 17 DorsalHorn, all 17 `top_detection≥0.05` (min 0.123), below-floor set = 7 → **MATCH**.
13. Docking: reverse-control AUCs, ADRA2A 0.618→0.532 (p 0.118), BH q (ACVR1 0.584, ADRA2A 0.0025, AXL 0.353, MAPK14 0.584, TNIK 0.584) → **MATCH**.
14. Eligibility: JSON `dock_eligible` 17 (incl. TFE3, excl. ADRA2A); `plausibility` 10 (incl. ADRA2A, excl. TFE3) → **MISMATCH subset claim** (F6).

**Cross-document / non-numeric checks:**
- Title 19 words, abstract ~195 words → **MATCH**.
- 12 GEO / 5 studies / 6 contrasts consistent across abstract and Methods → **MATCH**.
- References 1–22 consecutive; all cited (20,21 via "19–22" range at line 91); no orphan, no duplicate → **MATCH**.
- Tables 1b and 3b column-balanced, no broken pipes → **MATCH**.
- ACVR1 prose p 0.172 vs Table 3b / BH file 0.584 → **MISMATCH** (F7).
- Abstract "honest null" vs Results "inconclusive" ADRA2A → **nuance gap** (F8).

---

## G. § Recomputation transcript — verbatim commands & outputs (audit trail)

For transparency, every recompute I ran is reproduced below with the exact command and the stdout I observed. All runs used `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe` from workspace root `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛`.

### G.1 Items 1, 2 (core size; translation fractions; binomial)
**Command**
```
python - <<'PY'
import pandas as pd, numpy as np
from scipy import stats
st = pd.read_csv("results/tables/META_DRG_axis_stouffer.csv")
core = pd.read_csv("results/tables/META_DRG_axis_CORE_signature.csv")
print("stouffer rows:", len(st), "core rows:", len(core))
core_def = st[(st['meta_FDR']<0.05)&(st['consistency']>=0.8)]
print("recomputed core:", len(core_def), "identical set:", set(core_def['symbol'])==set(core['symbol']))
sub = st[st['incision_lfc'].notna()]
ci = sub['concordant_incision']
print("shared:", len(sub), "concordant:", int(ci.sum()), "frac:", ci.sum()/len(sub))
csub = sub[sub['symbol'].isin(set(core['symbol']))]
print("core-restricted:", len(csub), "concordant:", int(csub['concordant_incision'].sum()))
print("binom p 7751/14390:", stats.binomtest(7751,14390,0.5).pvalue)
PY
```
**Output (excerpt):** `stouffer rows: 16552 core rows: 4055` · `recomputed core: 4055 identical set: True` · `shared: 14390 concordant: 7751 frac: 0.5386` · `core-restricted: 3556 concordant: 2473` · `binom p 7751/14390: 1.93e-20`. → **Verdict: MATCH** (claims 16,552 / 4,055 / 53.9% / 69.5% / ≈10⁻²⁰ all confirmed).

### G.2 Item 3 (bulk-only core / overlap)
**Command:** read `results/tables/_R3_bulkonly_meta_summary.json` (top-level keys).
**Observed:** `"bulk_only_core_size": 1981, "primary_core_size": 4055, "overlap": 1732, "overlap_pct_primary": 42.7127`. → **Verdict: MATCH** (1,981 / 1,732 / 42.7%).

### G.3 Item 4 (gene-set stats, primary)
**Command:** `python -c "import pandas as pd; d=pd.read_csv('results/tables/P3_geneset_stats.csv'); print(d[['set','mean_Z','frac_up','perm_p']].to_string(index=False))"`
**Observed (key rows):** Neuroinflammation 4.9439 / 1.0000 / 0.0005; DAM_microglia 3.8838 / 0.9375 / 0.0005; Complement 3.4409 / 0.9444 / 0.0005; Mitochondria_OXPHOS −2.3728 / 0.2632 / 0.0040. → **Verdict: MATCH** (primary meta). Bulk-only OXPHOS `frac_up 0.2778` → F1.

### G.4 Item 5 (SCN)
**Command:** `python -c "import pandas as pd; st=pd.read_csv('results/tables/META_DRG_axis_stouffer.csv'); [print(r['symbol'], '6inp meta_Z=%.3f'%r['meta_Z'], 'GSE267799 lfc=%.3f'%r['lfc_GSE267799_SMIR_DRG'], 'GSE212311 lfc=%.3f'%r['lfc_GSE212311_CCI_DRG']) for _,r in st[st['symbol'].isin(['SCN9A','SCN10A','SCN11A','SCN8A'])].iterrows()]"`. Confirmed signs UP in GSE267799, DN in the other four contrasts — matching Table 1b. Bulk meta_Z/FDR from JSON `scn_tab` matched Table 1b to 2 dp. → **Verdict: MATCH (directions)**; magnitude-label caveat F5.

### G.5 Item 6 (hubs)
**Command:** `python -c "import pandas as pd; h=pd.read_csv('results/tables/P3_hub_genes.csv'); print(len(h), (h['in_meta_core']==True).sum(), (h['n_methods']==3).sum())"`
**Observed:** `35 32 5`. → **Verdict: MATCH**.

### G.6 Item 7 (LODO)
**Command/output:** see F4 — AUCs 1.0/0.9167/1.0/0.95/1.0 with n 28/20/9/9/6; three zero-width CIs. → **Verdict: MATCH (values)**; caveat F4 on CI honesty.

### G.7 Item 8 (bootstrap)
**Command:** `python -c "import pandas as pd; b=pd.read_csv('results/tables/P3_hub_bootstrap.csv'); print(b['hub_freq'].max(), (b['hub_freq']>=0.9).sum())"`
**Observed:** `0.155 0`. → **Verdict: MATCH** (max 15.5%, 0/35 ≥0.9).

### G.8 Item 9 (human miRNA) — the mismatch
**Command**
```
python - <<'PY'
import pandas as pd
h=pd.read_csv("results/tables/P4_hub_targeting_miRNAs.csv")
integ=pd.read_csv("results/tables/P4_hub_miRNA_human_integration.csv")
hc=h[h['score']>=80]; pm=set(integ['miRNA'])
print("total pairs",len(h),"HC>=80",len(hc),"HC hubs",hc['symbol'].nunique())
print("integ rows(miRNAs)",len(integ))
print("HC plasma pairs", len(hc[hc['miRNA'].isin(pm)]), "HC plasma hubs", hc[hc['miRNA'].isin(pm)]['symbol'].nunique())
PY
```
**Observed:** `total pairs 3511 HC>=80 752 HC hubs 31` · `integ rows(miRNAs) 253` · `HC plasma pairs 328 HC plasma hubs 29`. → **Verdict: MISMATCH on "253 pairs"** (F2); 3,511 and 752 correct; 253 = distinct miRNAs, not pairs.

### G.9 Item 10 (DRG GSE216039)
**Command:** `python -c "import pandas as pd; d=pd.read_csv('results/tables/P5_GSE216039_DRG_hub_finetype_top.csv'); print((d['detected']==True).sum(), (d[(d['detected'])]['top_finetype']=='Injured_RegenNeuron').sum()); print(d[d['symbol'].isin(['SPRR1A','ECEL1','NPY','FLNC'])][['symbol','specificity']].to_string(index=False))"`
**Observed:** `25 20` and SPRR1A 17.39 / ECEL1 25.69 / NPY 10.04 / FLNC 10.21. → **Verdict: MATCH**.

### G.10 Item 11 (spinal GSE328175)
**Command:** `python -c "import pandas as pd; c=pd.read_csv('results/tables/P5_hub_lineage_consensus.csv'); print('NotLocalisable',(c['consensus_lineage']=='NotLocalisable').sum(),'confident',(c['confident']==True).sum())"`
**Observed:** `NotLocalisable 15 confident 7`. → 7/35 cross-dataset **MATCH**; "16 localisable" **MISMATCH** vs 15 NotLocalisable (F3).

### G.11 Item 12 (Visium GSE325938)
**Command:** `python -c "import pandas as pd; v=pd.read_csv('results/tables/P5_GSE325938_hub_regionalization.csv'); dh=v[v['top_region']=='DorsalHorn']; print('detectable',(v['top_label_log2']>0).sum(),'DorsalHorn',len(dh),'min top_detection',dh['top_detection'].min()); print('below-floor', (v['top_detection']<0.05)['symbol'].tolist() if False else v[v['top_detection']<0.05]['symbol'].tolist())"`
**Observed:** `detectable 33 DorsalHorn 17 min top_detection 0.123`; below-floor = [CDHR5, SERPINE1, VIP, REG3B, ANKRD1, CRISP3, LNP1]. → **Verdict: MATCH** (all 17 dorsal-horn hubs ≥0.05; below-floor set exact).

### G.12 Item 13 (docking)
**Command:** `python -c "import pandas as pd; r=pd.read_csv('results/tables/P6_reverse_control.csv'); print(r[['symbol','auc_known_vs_rest']].to_string(index=False)); b=pd.read_csv('results/tables/P6_BH_correction.csv'); print(b.to_string(index=False))"`
**Observed reverse-control AUCs:** AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779, ADRA2A 0.532. **BH q:** ACVR1 0.584 / ADRA2A 0.0025 / AXL 0.353 / MAPK14 0.584 / TNIK 0.584. Breadth `P6_breadth_chembl_power.csv`: ADRA2A t1 0.6184 → full 0.5325 (p 0.1184). → **Verdict: MATCH** (every Table 3b value).

### G.13 Item 14 (eligibility)
**Command:** read `results/tables/_R3_plausibility.json` → `dock_eligible` (17, includes TFE3, excludes ADRA2A); `plausibility` (10, includes ADRA2A, excludes TFE3). Cross-checked vs Methods `:121-122` and Table 3a. → **Verdict: MISMATCH** on the "10 of the 17" subset claim (F6).

### G.14 Cross-document checks
**Command:** `python -c "import re; t=open('reports/MVP_ScientificReports_submission.md',encoding='utf-8').read(); print('title words', len('Conserved maladaptive nerve-injury response on the dorsal root ganglion–spinal axis, with incomplete incision translation and an honest repurposing null'.split())); m=re.search(r'## Abstract\s*(.*?)\n---',t,re.S); print('abstract words', len(re.sub(r'[\*_`]','',m.group(1)).split())); refs=re.findall(r'^(\d+)\.\s',t,re.M); print('refs',len(refs),'consec',refs==[str(i) for i in range(1,len(refs)+1)])"`
**Observed:** `title words 19` · `abstract words 195` · `refs 22 consec True`. → **Verdict: MATCH** (title 19; abstract ≤200; 22 refs consecutive, all cited via the 19–22 range).

---

## H. § Severity triage (for the editor's consolidation)

- **T2 (correct before acceptance):** F1 (bulk-only OXPHOS polarity inverted), F2 (miRNA 253 mislabeled as pairs — true 328), F6 (docking "10 of 17" subset logic wrong), F7 (ACVR1 single-variable p 0.172 vs 0.584 in own Table 3b). These are wrong numbers in results/abstract prose that contradict the manuscript's own tables or source files.
- **T3 (clarify / improve honesty):** F3 (spinal "16 localisable" vs 20), F4 (degenerate LODO CIs unreported), F5 (Table 1b unlabeled Z vs lfc), F8 (abstract "honest null" vs Results "inconclusive").
- **No T0/T1 fabrication detected:** all 14 checklist numbers were traceable to a real source file; the errors are mislabels/unit errors/stale values, not invented statistics. The core meta, translation fractions, gene-set programme, hub set, DRG/Visium localisation, and the entire docking honesty narrative are internally consistent with their data.

**Summary of defects:** 5 numeric/logical mismatches (F1 OXPHOS polarity, F2 miRNA 253/328, F3 spinal 16/20, F6 docking 10-of-17, F7 ACVR1 0.172/0.584), 3 honesty/labeling caveats (F4 LODO CI, F5 Table 1b statistic label, F8 abstract nuance). None of the 5 mismatches invalidates the paper's conclusions, but F1, F2, F6, and F7 are wrong numbers that must be corrected before acceptance because they appear in results/abstract prose and contradict the manuscript's own tables or source files.

*Report only — no manuscript file was modified.*
