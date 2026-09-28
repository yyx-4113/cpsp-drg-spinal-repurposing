# Round 14 Panel Brief — PLOS ONE resubmission v1.4.0

## Manuscript under review
- Single-author resubmission to *PLOS ONE*: "DRG–spinal-axis nerve-injury transcriptome in-silico meta-analysis and FDA-drug repurposing" (single author Yongxin Yang, ORCID 0009-0004-9698-6552; GitHub yyx-4113). Reuse of public GEO mouse nerve-injury transcriptomes + human DRG scRNA + ChEMBL docking.
- Manuscript: `reports/MVP_PLOSONE_submission.md` (v1.4.0).
- Source data (recompute from these, do NOT trust the manuscript's transcribed numbers):
  - `results/tables/META_DRG_axis_stouffer.csv` (Stouffer meta; columns include `gene`, `meta_Z`, `meta_FDR`, `consistency`, per-dataset Z/log2FC, up/down flags)
  - `results/tables/_R4_supplementary_summary.json`, `_R4_nerveinjury_only_summary.json`, `_R4_translation_noncircular.json`
  - `results/tables/_R4_random_effects_meta.csv` (DerSimonian–Laird τ², I²)
  - `results/tables/P3_lodo_auc_ci_leakage_controlled.csv` (leakage-controlled LODO AUCs, n_selected)
  - `results/tables/P3_hub_genes.csv`, `P3_geneset_stats.csv`, `_R4_targetset_bootstrap_resamples.csv`
  - `results/tables/META_DRG_axis_CORE_signature.csv`
- Rebuilt submission pack: `submission_pack/*.docx` (Manuscript, Supporting, Cover, STROBE).
- Authoritative gate: `scripts/p7_consistency_gate.py` (claims 0 failure / 47 passed).

## Independence discipline (mandatory)
FORBIDDEN to read (treat as if they do not exist):
- `reviews/REVIEW_round13_2026-09-28.md`, `reviews/REVIEW_round12*.md`, any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`
- `reviews/round13_panel_2026-09-28/`, `reviews/round12_panel_*/` (any prior panel subdirectory)
- `SUBMISSION_MANIFEST.md`, `GITHUB_PUSH_LIST_v1.4.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, any `_quarantine/`
- Other reviewers' output files in `reviews/round14_panel_2026-09-28/` (do NOT read sibling `<codename>_*.md` files)
Do NOT assume the manuscript is mature or has passed prior review. Treat it as a first submission. Every judgement must come from text or source data you read yourself. Any claim in the manuscript that you CAN verify, you MUST verify by recomputing from the raw CSV/JSON.

## Output contract (every finding needs four parts)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or table/section + exact numbers; numbers you cite MUST be ones you recomputed yourself from the raw files
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 a paste-ready English sentence, or an explicit spec for a new analysis (variables, strata, output columns)
"Consider strengthening the discussion" is banned.

## Also required in every review
- § Stands up (≥3, with evidence) — things you suspected but found correct. This is a deliverable, not filler.
- § Questions for the authors — what you need to know, do not guess.
- § What I actually checked — files read, commands run, values recomputed vs the manuscript's, with any discrepancy stated.

## Per-expert focus
- A1 (domain): biological/clinical validity of the DRG–spinal-axis narrative, hub-gene plausibility, must-cite literature, whether the "nerve-injury-enriched" claim survives the within-animal paired design caveat, honesty of the CACNA2D1 4/6 framing, docking "honest null" interpretation.
- A2 (design/stats): Stouffer weighting; random-effects (DL τ², I²); LODO leakage control (within-animal paired GSE278227 vs between-animal; union vs ≥2/3 consensus); bootstrap stability (Jaccard 0.304, P=0.000); BH-FDR; EPV. Explicitly judge whether deferred T2-4 (CAMERA) and T2-5 (Knapp–Hartung) are REQUIRED for acceptance or acceptable as stated limitations.
- A3 (implementation): exact match of every manuscript number to source CSV/JSON; recompute core size, meta_FDR<0.05 count, CACNA2D1 4/6, LODO AUCs + n_selected range, docking honest-null; verify figures embedded at 350 DPI; verify gate 47/47 by re-running `scripts/p7_consistency_gate.py`.
- A4 (venue/compliance): PLOS ONE policies — abstract ≤300 words (manuscript claims 297), display items ≤8 (claims 5F+3T), title ≤20 words; figure embedding in docx; STROBE for observational; data availability; ethics; single-author (author holds Bachelor of Medicine only — NO MD/PhD); AI disclosure; reference style. Confirm the rebuilt `submission_pack/*.docx` actually contains the figures and the new v1.4.0 wording.

## Forbid tool talk
Do not mention what tools you use; write review comments only.
