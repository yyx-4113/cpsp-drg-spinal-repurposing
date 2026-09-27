# A3 — Implementation / provenance auditor (Round 12, fresh independent panel)

**Reviewer role:** A3 — Implementation / provenance auditor
**Panel:** Round 12, enforced-independence peer-review panel (first-submission discipline)
**Date:** 2026-09-27
**Scope reviewed:** manuscript (`reports/MVP_PLOSONE_submission.md`), supplementary (`reports/MVP_PLOSONE_supplementary.md`), built docx (`submission_pack/Manuscript.docx`, `submission_pack/Supporting_Information.docx`), and metadata (`CITATION.cff`, `README.md`, `reports/MVP_PLOSONE_cover_letter.md`, `reports/MVP_PLOSONE_compliance_check.md`).

---

## Independence statement

I have **not** read any prior-review file (`reviews/REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, any `round*_*/**`, or sibling Round-12 reviewer files A1/A2/A4…), nor `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `PROJECT_PLAN.md`, `方案二_*.md`, or any gate script / gate output (`scripts/gate_*.py`, `scripts/_gate_out.txt`, `scripts/p7_consistency_gate.py`). Every number below was **recomputed from the raw artefact files** (`results/tables/*.csv`, `results/*.json`, `figures/*.png`, the docx binaries) using Managed Python at `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`. No gate script was treated as evidence; all figures are independently derived.

---

## Executive summary

- **One CRITICAL, submission-blocking defect:** `Manuscript.docx` Table 2 (the 35-hub table, document table index 3) has its **column headers misaligned with the body data**. The header cell `In meta core` sits over the LASSO-frequency column, and the true Yes/No meta-core membership (`in_meta_core`) is orphaned in the rightmost column mislabeled `SHAP |abs|`. The 35 data values are all present and *correct* (they match `P3_hub_genes.csv` by position), but the *visual rendering* is nonsensical (e.g. "In meta core = 0.96", "SHAP |abs| = Yes"). This must be fixed before the docx is submitted.
- **All eight headline recomputations reconcile** with the raw CSVs/JSON: core 4,055; bulk-only core 2,512; strict overlap 2,202; relaxed overlap 3,587/88.5%; 468 outside relaxed; 313 with no bulk significance (211 present-but-NS + 102 absent); 1,853 outside strict bulk core; 1,385 recovered; 1,707 pure 4/4 + 495 K=3 within the strict overlap; 16,552 genes tested; 6,869 at FDR<0.05; RE core 1,008; collapse core 4,294 / 3,707 retained / 91.4%.
- **Every other mandatory check passes:** exactly one hub table with 35 data rows (no duplicate); 5 embedded figures at 350.012 DPI; AI-disclosure sentence present; `v1.2.0` consistent across all 5 metadata files; exact title identical in 4/5 files (README omits the title string, non-defect); `P3_hub_genes.csv` carries `in_meta_core` while `P5_hub_lineage_consensus.csv` correctly carries **no** core-membership field; 10/10 spot-checked reference DOIs resolve to correct, topically-appropriate records; the only Zenodo string is a `10.5281/zenodo.XXXXXXX` post-acceptance placeholder, i.e. **no fabricated DOI**.

---

## Mandatory provenance check 1 — Recompute headline numbers from raw `results/tables/*.csv` + `results/*.json`

I recomputed every headline figure in the manuscript from source tables. All reconcile exactly.

| Claimed (manuscript) | Recomputed from raw | Source file(s) | Verdict |
|---|---|---|---|
| 16,552 genes tested | 16,552 | `META_DRG_axis_stouffer.csv` (rows) | ✅ |
| 6,869 at meta_FDR<0.05 | 6,869 | `META_DRG_axis_stouffer.csv` | ✅ |
| Core = 4,055 (meta_FDR<0.05 & consistency≥0.8) | 4,055 | `META_DRG_axis_CORE_signature.csv` (all rows FDR<0.05 & consistency 0.8–1.0); cross-checked via stouffer = 4,055 | ✅ |
| Bulk-only core = 2,512 | 2,512 | `META_bulkonly_meta.csv` (FDR<0.05 & cons≥0.8) | ✅ |
| Strict overlap = 2,202 (54.3%) | 2,202 | primary core ∩ (bulk FDR<0.05 & cons≥0.8) | ✅ |
| Within overlap: 1,707 pure 4/4 + 495 K=3 only | 1,707 + 495 = 2,202 | within strict overlap, bulk K=4 → 1,707; K=3 → 495 | ✅ |
| Relaxed overlap = 3,587 (88.5%) | 3,587 | primary core ∩ (bulk FDR<0.05 & bulk cons≥0.75) | ✅ |
| 4,055 − 3,587 = 468 outside relaxed | 468 | arithmetic | ✅ |
| Recovered by relaxing = 1,385 | 1,385 | 3,587 − 2,202 | ✅ |
| 313 lack bulk significance (211 present-but-NS + 102 absent) | 211 + 102 = 313 | present-but-bulk-FDR≥0.05 = 211; absent from bulk file = 102 | ✅ |
| 1,853 outside strict bulk core | 1,853 | 4,055 − 2,202 | ✅ |
| RE core (DerSimonian–Laird) = 1,008 (24.9%) | 1,008 | `_R4_random_effects_meta.csv` (`FDR_RE`<0.05 & cons≥0.8) | ✅ |
| Collapse core 4,294; retained 3,707/4,055 = 91.4% | 4,294 / 3,707 / 0.9142 | `META_collapse_meta.csv`, `P2_meta_sensitivity.csv` | ✅ |
| Docking library = 3,085 drugs | 3,085 | `P6_enrichment_mw_confounder_check.csv` (n_total=3,085) | ✅ |
| ADRA2A full-library AUC 0.532, p=0.118 (NS) | 0.532 / 0.118 | `P6_enrichment_mw_confounder_check.csv` | ✅ |
| ADRA2A Tier-1 (620-drug) AUC 0.618 | 0.618 | `P6_breadth_chembl_power.csv` (t1_only) | ✅ |

**Gene-set BH q-values (from `_R4_geneset_setlevel_bh.csv`):** Neuroinflammation 0.002999, Complement 0.002999, DAM_microglia 0.002999, Mitochondria_OXPHOS 0.020240, Neuropeptides_pain 0.046777, Synaptic 0.317841 — all match the manuscript's reported q-values and the stated "q=0.003" upper-bound framing for the floor-pinned sets.

**Bootstrap stability (`P3_hub_bootstrap.csv`, 35 rows):** `hub_freq` ranges 0.14–1.0; only **2/35** reach ≥0.90 — SPRR1A (1.00) and ATF3 (0.94) — exactly as the manuscript reports ("≥0.9 count = 2").

【Problem】None in this check. Every headline figure is reproducible from raw data.
【Evidence】Above table; independent recomputation via pandas on the cited CSVs.
【Why it matters】Reproducibility is the core claim of this audit; a clean pass here means the analysis pipeline and the narrative numbers are internally consistent.
【Specific fix】No fix required for the numbers themselves.

---

## Mandatory provenance check 2 — `Manuscript.docx` has EXACTLY ONE Table 2 with 35 data rows matching `P3_hub_genes.csv` `in_meta_core`→Yes/No, no duplicate hub table

**Part A — count and uniqueness: PASS.**
`Manuscript.docx` contains 5 tables total. Only one is a hub table (document table index 3): 36 rows = 1 header + **35 data rows**. No second hub table exists. `Supporting_Information.docx` contains 13 tables, none of which is the hub table (it carries the P5 lineage consensus and P5 regionalization tables instead). So the "exactly one Table 2 with 35 data rows" requirement is satisfied.

**Part B — `in_meta_core`→Yes/No mapping: DEFECT (header/data misalignment).**

The true column order in `P3_hub_genes.csv` is:
`symbol, n_methods, lasso_freq, rf_gini, shap_meanabs, in_meta_core`

The source-markdown Table 2 (`reports/MVP_PLOSONE_submission.md` line 321) is internally consistent:
`| Hub | Methods (n/3) | In meta core | LASSO freq | RF Gini | SHAP |abs| |` and body `| SPRR1A | 3 | Yes | 0.96 | 0.033 | 1.043 |`.

But the **built docx** table body uses the *raw CSV column order* while keeping the *markdown header order*. Result (docx table index 3):

| Header cell | What the data actually shows |
|---|---|
| `Hub` | correct symbol (SPRR1A, ATF3, …) |
| `Methods (n/3)` | correct n (3, 2, …) |
| `In meta core` | **lasso_freq values** (0.96, 0.85, 0.62, …) |
| `LASSO freq` | **rf_gini values** (0.033, 0.024, …) |
| `RF Gini` | **shap_meanabs values** (1.043, 0.145, …) |
| `SHAP |abs|` | **in_meta_core Yes/No** (Yes, Yes, … No) |

I dumped all 35 docx rows. The last column (under `SHAP |abs|`) holds the true membership: **Yes = 32, No = 3** (No at rows 30, 32, 35 — REG3B, ANKRD1, MEGF11), which exactly matches `P3_hub_genes.csv` (`in_meta_core` True=32 / False=3). The *values* are therefore correct and fully recoverable; only the **header labels are shifted by one column from position 2 onward**.

【Problem】In `Manuscript.docx` Table 2 the column headers do not correspond to the data columns. The `In meta core` header sits over the LASSO-frequency column, the `LASSO freq` header over RF-Gini, `RF Gini` over SHAP, and the `SHAP |abs|` header over the Yes/No `in_meta_core` membership. A reader sees, e.g., "In meta core = 0.96" and "SHAP |abs| = Yes" for SPRR1A — internally contradictory and uninterpretable.
【Evidence】python-docx inspection of `submission_pack/Manuscript.docx` table index 3 (36 rows). Header = `['Hub','Methods (n/3)','In meta core','LASSO freq','RF Gini','SHAP |abs|']`. Body row 1 = `SPRR1A | 3 | 0.96 | 0.0335 | 1.0427 | Yes`, which is the raw `P3_hub_genes.csv` order `[symbol, n_methods, lasso_freq, rf_gini, shap_meanabs, in_meta_core]`; the rightmost `Yes` correctly equals `in_meta_core=True` for SPRR1A. Cross-checked against `reports/MVP_PLOSONE_submission.md` line 321–323 (markdown body is correctly ordered: `| SPRR1A | 3 | Yes | 0.96 | 0.033 | 1.043 |`).
【Why it matters】This is the single most important display table (dual-ML hub consensus + meta-core membership). A reviewer or production editor opening the docx sees a broken, self-contradictory table; at minimum it triggers a major-revision flag, and PLOS production may reject the table entity. The defect is purely a **build/pipeline** error (markdown→docx column reorder), not a data error — but it is visually fatal as submitted.
【Specific fix】Regenerate the docx Table 2 from a single, consistent column order. The safest fix is to rebuild the table so the header and body both follow the manuscript's intended order: `Hub | Methods (n/3) | In meta core | LASSO freq | RF Gini | SHAP |abs|` with body `symbol | n_methods | in_meta_core(Yes/No) | lasso_freq | rf_gini | shap_meanabs`. Concretely, in the docx build step, do **not** pull body cells directly from the CSV column order while stamping the markdown header; instead (a) either reorder the CSV columns to `[symbol, n_methods, in_meta_core, lasso_freq, rf_gini, shap_meanabs]` before table generation, or (b) map each header to its named CSV field explicitly. After rebuild, re-open the docx and assert: header col2 == "In meta core" AND body col2 ∈ {Yes,No} (32 Yes / 3 No); header col3 == "LASSO freq" AND body col3 is a float; etc. Add a CI assertion that `set(body_col2_values)` ⊆ {Yes,No}.

---

## Mandatory provenance check 3 — Count inline_shapes and verify 350-DPI PNGs

【Problem】None.
【Evidence】`Manuscript.docx` has **5 inline_shapes** (embedded figures, not floating). Each was extracted and opened with PIL: all five return `dpi=(350.012, 350.012)` and are well-formed raster PNGs (sizes e.g. 2516×1517, 2834×1679, 2208×2109, 2814×1691, 2472×1622). This meets the PLOS ONE 350-DPI minimum for raster figures.
【Why it matters】PLOS production rejects figures below 300 DPI (prefers ≥350); confirming the exact embedded DPI closes a common desk-reject risk.
【Specific fix】No fix needed. (Optional: the DPI is 350.012 rather than exactly 350 — harmless, but if PLOS tooling is strict about an exact integer, re-export at exactly 350 DPI; the fractional value is almost certainly rounded from a 300-DPI-at-source → 350-upscaled pipeline and is fine.)

---

## Mandatory provenance check 4 — AI-disclosure statement present in the docx

【Problem】None.
【Evidence】The manuscript docx text contains the sentence: *"A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing."* under the "Statistical discipline, causal scope and AI-use disclosure" section. The cover letter likewise states LLM-assisted language drafting. This satisfies PLOS ONE's generative-AI disclosure requirement.
【Why it matters】PLOS ONE mandates an AI-use disclosure; its absence is a submission blocker.
【Specific fix】No fix needed. Verify the exact wording also appears in the docx Cover_Letter entity (already present per `MVP_PLOSONE_cover_letter.md`).

---

## Mandatory provenance check 5 — `v1.2.0` and exact title enumerated across manuscript / cover letter / CITATION.cff / README / compliance_check

**`v1.2.0` occurrences (all consistent, no conflicting version string found):**

| File | Line(s) | Context |
|---|---|---|
| `CITATION.cff` | 2 | `"…repository (version v1.2.0; integrity verifiable via MANIFEST.sha256)."` |
| `README.md` | 238, 245 | repo URL `(version v1.2.0; integrity verifiable via …)`; "cite the article and the repository (version v1.2.0); no repository DOI is minted" |
| `reports/MVP_PLOSONE_submission.md` | 271, 273 | Data Availability statement referencing `v1.2.0` and MANIFEST.sha256 |
| `reports/MVP_PLOSONE_cover_letter.md` | 13 | versioned citable archive `(v1.2.0; …)` |
| `reports/MVP_PLOSONE_compliance_check.md` | 22 | "Public GitHub repo (v1.2.0, MANIFEST.sha256)" |

**Exact title** `"Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null"` appears identically (verbatim, including British "localisation") in: `MVP_PLOSONE_submission.md` (line 1, H1), `MVP_PLOSONE_cover_letter.md` (line 3), `CITATION.cff` (line 3, `title:`), `MVP_PLOSONE_compliance_check.md` (line 3). It is **absent from `README.md`** — README is a repository readme and is not required to carry the paper title, so this is a non-defect, but noted for completeness.

【Problem】None material. (Minor note only: the paper title string is not cross-referenced in README.md; acceptable but the version tag is.)
【Evidence】Grep across the five named files enumerated above; title grep matched 4/5 files, version grep matched 5/5 with identical `v1.2.0` token and no divergent version number anywhere.
【Why it matters】Version and title consistency across submission, cover letter, citation metadata, and compliance docs is required for a citable, depositable artifact; divergence would break the GitHub-release / CITATION.cff provenance chain.
【Specific fix】No fix required. Optionally add the exact title to README.md for end-to-end traceability, but this is not blocking.

---

## Mandatory provenance check 6 — `P3_hub_genes.csv` HAS `in_meta_core`; `P5_hub_lineage_consensus.csv` has NO core-membership field

【Problem】None.
【Evidence】`P3_hub_genes.csv` columns = `['symbol','n_methods','lasso_freq','rf_gini','shap_meanabs','in_meta_core']` (35 rows; `in_meta_core` True=32, False=3). `P5_hub_lineage_consensus.csv` columns = `['symbol','n_methods','n_datasets','celltypes','consensus_lineage','confident','mean_enrich','tiers','lineages']` — there is **no** `in_meta_core`, `core`, or any core-membership column. This is the intended separation: meta-core membership lives in P3; single-cell lineage lives in P5. The docx SI Table (Supporting_Information.docx table index 0) reproduces the P5 schema without a core field, consistent with the source.
【Why it matters】Confirms the two artefacts were not accidentally merged and that the "in meta core" attribute is singularly sourced from P3 — important because the docx Table 2 defect (check 2) concerns exactly this field; verifying its sole provenance rules out a second, conflicting definition.
【Specific fix】No fix required.

---

## Mandatory provenance check 7 — Spot-check ≥8 reference DOIs (manuscript claims 37/37 verified)

I resolved **10** DOIs via the live Crossref API (`api.crossref.org/works/{doi}`). All 10 returned valid records whose titles/topics match the manuscript's citations:

| DOI | Year | Title (truncated) | Topical match |
|---|---|---|---|
| 10.1093/bja/aen099 | 2008 | Chronic post-surgical pain: 10 years on | ✅ CPSP review |
| 10.1038/s41597-024-04078-2 | 2024 | A transcriptome data set for comparing skin, muscle and dorsal root ganglion | ✅ data source |
| 10.1038/s42003-025-07506-0 | 2025 | An atlas of neuropathic pain-associated molecular pathological characterisation | ✅ |
| 10.1093/biomethods/bpaf038 | 2025 | DrugPipe: Generative artificial intelligence-assisted virtual screening | ✅ method |
| 10.3949/ccjm.93a.25087 | 2026 | Suzetrigine: A novel nonopioid systemic analgesic | ✅ |
| 10.1097/ALN.0000000000005460 | 2025 | Suzetrigine, a Non-Opioid NaV1.8 Inhibitor | ✅ |
| 10.1126/sciadv.adu4270 | 2025 | Neuronal Reg3β/macrophage TNF-α–mediated positive feedback signaling | ✅ Reg3β hub |
| 10.1038/s41467-025-59849-1 | 2025 | Targeting C1q prevents microglia-mediated synaptic removal in neuropathic | ✅ complement |
| 10.3109/00207454.2015.1004172 | 2015 | Voltage-gated sodium channel function and expression in injured DRG | ✅ sodium channels |
| 10.1038/nature05413 | 2006 | An SCN9A channelopathy causes congenital inability to experience pain | ✅ SCN9A |

【Problem】None. All 10 sampled DOIs are valid, current, and correctly matched to their citations. No fabricated, retracted, or mismatched DOI was found in the sample.
【Evidence】Live Crossref resolution (HTTP 200, parsed `message.title`/`issued`) for the 10 DOIs above; none returned 404/410 or a title mismatch.
【Why it matters】The manuscript asserts "37/37 DOIs verified." A spot-check cannot certify all 37, but a clean 10/10 sample with on-topic matches gives strong confidence the reference list is sound and not padded with fabricated identifiers.
【Specific fix】No fix required. (Residual, out-of-scope-for-this-audit caveat: a full 37/37 automated Crossref pass, if not already in the pipeline, would convert this sample into a complete certification; the manuscript's own claim should be backed by the script that produced it.)

---

## Mandatory provenance check 8 — GitHub `v1.2.0` tag consistent; no fabricated Zenodo DOI

【Problem】None.
【Evidence】Every metadata file that names a version uses the single token `v1.2.0` (check 5). The only Zenodo string in the entire submission set is in `reports/MVP_PLOSONE_compliance_check.md` line 72: *"Deposit the versioned Zenodo archive and replace the `10.5281/zenodo.XXXXXXX` placeholder in the Data Availability statement with the minted DOI (post-acceptance per PLOS policy …)"*. This is an explicit **placeholder** (`XXXXXXX`, not a real DOI) slated for post-acceptance use; the manuscript's Data Availability statement correctly states **"no Zenodo snapshot has been deposited"** and points to the versioned GitHub release instead. A grep for `10.5281/zenodo` across the manuscript, supplementary, CITATION.cff, README, cover letter, and compliance check returns **only** that one placeholder line — no fabricated live DOI is asserted as existing.
【Why it matters】A fabricated or prematurely-cited repository DOI is a serious integrity violation. Confirming the Zenodo reference is a clearly-marked, unresolved placeholder (and that the live availability statement points to GitHub, not a fake DOI) closes that risk.
【Specific fix】No fix required. Before acceptance, ensure the placeholder is replaced with the real minted DOI (per the compliance checklist's own instruction) and that the GitHub release tag `v1.2.0` exists and is tagged at the exact commit referenced by MANIFEST.sha256.

---

## Auxiliary verifications (not in the eight, but within scope of "implementation/provenance")

- **RE heterogeneity narrative:** manuscript states median I² ≈ 39% genome-wide, median I² 72.8% across the 35 hubs, 18/35 retaining FDR_RE<0.05. These are reported as sensitivity bounds and are consistent with the `_R4_random_effects_meta.csv` / `P6` RE columns; I did not recompute I² per hub (out of the eight-check scope) but the 1,008 RE-core figure (check 1) is the load-bearing number and it reconciles.
- **Gene-set fraction-up claims** (`P3_geneset_stats.csv`): Neuroinflammation 100% up, DAM 93.8% up (≈0.9375), Complement 94.4% up (≈0.9444), OXPHOS 73.7% down (≈0.2632 up) — match the manuscript's wording.
- **SI table integrity:** Supporting_Information.docx has 13 tables, 0 inline_shapes; the hub lineage/regionalization tables (T0, T1) use the correct P5 schema with no core field. The Table-2 misalignment (check 2) is **confined to the single Manuscript.docx hub table**; the SI is clean.

---

## § Stands up (provenance strengths)

1. **Every headline number is independently reproducible from raw data.** Core 4,055; bulk 2,512; strict overlap 2,202; relaxed overlap 3,587 (88.5%); 468 / 313 / 1,853 / 1,385 / 1,707+495 reconciliation; 16,552 tested; 6,869 significant; RE core 1,008; collapse 4,294/3,707/91.4%; docking 3,085; ADRA2A 0.532 (p=0.118); bootstrap 2/35 ≥0.9. No arithmetic or transcription error was found in any recomputed quantity.
2. **Figure and disclosure compliance is clean.** Five embedded raster figures at exactly 350.012 DPI (meets PLOS bar); explicit generative-AI disclosure present in both manuscript and cover letter; 10/10 reference DOIs resolve to correct, on-topic records.
3. **Versioning and artifact separation are coherent.** `v1.2.0` is used identically across all five metadata files; the exact title is verbatim in four of five; `in_meta_core` is singularly sourced from P3 while P5 correctly omits any core-membership field; the only Zenodo reference is a clearly-marked post-acceptance placeholder with no fabricated live DOI.
4. **No duplicate or silently-dropped hub table.** Exactly one 35-row hub table exists in the manuscript docx; the 35-row count and the 32-Yes/3-No membership are both recoverable from the (mislabeled but value-correct) body.

---

## § Questions (for the authors / panel)

1. **The docx Table 2 header/data misalignment (check 2) — how was the docx generated?** Was the markdown→docx step meant to reorder columns (markdown order puts `in_meta_core` third) but the body was pulled from the raw CSV order (which puts `lasso_freq` third)? Confirming the build path determines whether other docx tables share the same latent bug. (I verified the SI tables are clean, but the generation script should be audited.)
2. **Can the live GitHub `v1.2.0` release tag be confirmed to exist and to be tagged at the commit whose `MANIFEST.sha256` is cited?** I could not reach GitHub from the audit sandbox to verify the tag independently; the internal consistency (all files say `v1.2.0` + MANIFEST.sha256) is strong, but an external confirmation would convert "internally consistent" into "externally verified."
3. **Why does README.md not carry the paper title?** Non-blocking, but for deposit/DOI metadata parity it is cleaner if README references the exact title (it already references the version and the repo URL).
4. **RE-core provenance:** the FE core is the primary result and the RE core (1,008) is the sensitivity bound — was the `_R4_random_effects_meta.csv` `FDR_RE` column used (it yields exactly 1,008), or a different RE implementation? The number reconciles either way, but I want to confirm the cited file is the one behind the claim.

---

## § What I actually checked

**Files read (allowed artefacts only):** `reports/MVP_PLOSONE_submission.md`, `reports/MVP_PLOSONE_supplementary.md`, `submission_pack/Manuscript.docx`, `submission_pack/Supporting_Information.docx`, `CITATION.cff`, `README.md`, `reports/MVP_PLOSONE_cover_letter.md`, `reports/MVP_PLOSONE_compliance_check.md`.

**Raw data recomputed (Managed Python, pandas/PIL/python-docx):**
- `results/tables/META_DRG_axis_CORE_signature.csv` (4,055; FDR<0.05 & consistency 0.8–1.0)
- `results/tables/META_DRG_axis_stouffer.csv` (16,552; 6,869 FDR<0.05; FE core 4,055)
- `results/tables/META_bulkonly_meta.csv` (bulk core 2,512; overlap/relaxed computations)
- `results/tables/_R4_random_effects_meta.csv` (RE core 1,008 via `FDR_RE`)
- `results/tables/META_collapse_meta.csv`, `P2_meta_sensitivity.csv` (collapse 4,294/3,707/0.9142)
- `results/tables/P3_hub_genes.csv` (35 rows; `in_meta_core` 32/3), `P3_hub_bootstrap.csv` (2/35 ≥0.9)
- `results/tables/P5_hub_lineage_consensus.csv` (no core field — confirmed)
- `results/tables/_R4_geneset_setlevel_bh.csv` (BH q-values), `P3_geneset_stats.csv` (fraction-up)
- `results/tables/P6_enrichment_mw_confounder_check.csv`, `P6_breadth_chembl_power.csv` (ADRA2A 0.532/0.118; 3,085; 0.618)
- `submission_pack/Manuscript.docx` (5 tables, 5 inline_shapes, Table-2 header/body dump of all 35 rows, AI-disclosure scan, DPI via PIL)
- `submission_pack/Supporting_Information.docx` (13 tables, 0 inline_shapes, header scan — no hub-table misalignment)

**External calls:** live Crossref API resolution of 10 reference DOIs (all valid).

**Not checked (out of mandate / sandbox-limited):** live GitHub tag existence (flagged in Questions); the full 37/37 DOI set (sampled 10/37); per-hub I² recomputation (the load-bearing RE-core number was verified instead); any gate script or prior-review content (excluded by independence rules).

**Independence attestation:** No prior-review, response, revision, sibling-reviewer, manifest, SOP, author-statement, project-plan, or gate-script file was opened. All findings derive solely from the first-submission artefacts and raw data listed above.
