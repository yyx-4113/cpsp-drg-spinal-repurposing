# Round-5 Independent Review Panel — Brief

**Manuscript under review (v1.4):** *Scientific Reports* submission
"CPSP DRG–脊髓轴 + FDA 老药新用虚拟筛选 / virtual repurposing screen"
Main text: `reports/MVP_ScientificReports_submission.md`
Supplementary: `reports/MVP_ScientificReports_supplementary.md`
Cover letter: `reports/MVP_ScientificReports_cover_letter.md`
Reporting summary: `reports/MVP_ScientificReports_reporting_summary.md`
Source (same content, unrendered refs): `reports/_v14_source.md`

This is a **fresh, first-submission-style review of the CURRENT v1.4 text.** The
manuscript is a bioinformatics + in-silico docking repurposing study of chronic
post-surgical pain (CPSP) along the DRG–spinal axis. It (1) builds a cross-dataset
conserved "nerve-injury-associated" transcriptional signature via Stouffer
meta-analysis, (2) localises hub genes to cell types via scRNA-seq + Visium,
(3) runs an FDA-approved-drug docking screen, and (4) explicitly argues the
repurposing screen is an *honest null* (no therapeutic priority drawn).

## Independence discipline (MANDATORY)
You must review as if you have NEVER seen this manuscript before.

**FORBIDDEN to read (these would leak prior-round priors):**
- `reviews/REVIEW_round*.md`, `reviews/RESPONSE_round*.md`, `reviews/REVISION*.md`
- the entire `reviews/round4_2026-09-20/` directory
- `submission_pack/SUBMISSION_MANIFEST.md`
- `submission_pack/GITHUB_PUSH_LIST_v1.4.md`
- `README.md` (project overview), `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- ANY other reviewer's file inside `reviews/round5_2026-09-21/`

Do NOT assume the manuscript is mature or has passed prior review. Treat it as a
first submission. Every judgement must come from text/source data you read
yourself. Any claim in the manuscript that you CAN verify numerically, you MUST
verify numerically against the source files (below).

## Source data you may read (to recompute claims)
- `results/tables/*.csv`, `results/tables/*.json` — pipeline outputs
- `data/processed/*.csv` — per-dataset DEG / Xtail tables
- `scripts/p3_genesets.py` — gene-set (SETS) definitions
- Key files to cross-check manuscript numbers against:
  - `results/tables/META_DRG_axis_CORE_signature.csv`, `META_DRG_axis_stouffer.csv`
  - `results/tables/P3_hub_genes.csv`, `P3_hub_bootstrap.csv`, `P3_lodo_auc_ci.csv`, `P3_ml_summary.json`
  - `results/tables/P3_geneset_stats.csv`, `P4_setlevel_test.json`
  - `results/tables/P5_GSE216039_DRG_hub_localisation.csv`, `P5_GSE246288_SC_*` (Visium)
  - `results/tables/_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_meta.csv`,
    `_R4_translation_noncircular.csv/.json`, `_R4_targetset_bootstrap.csv/.json`,
    `_R4_geneset_setlevel_bh.csv`, `_R4_supplementary_summary.json`
  - `results/tables/META_bulkonly_sensitivity_summary.json` (OXPHOS frac_up)
  - `data/processed/GSE265957_Xtail_*.csv` (translation direction checks)
  - `results/tables/P6_BH_correction.csv`, `P6_enrichment_mw_confounder_check.csv` (ACVR1 p)
  - `results/tables/P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`, `P4_hub_targeting_miRNAs.csv` (miRNA 328/253)

**Environment traps (learned the hard way — do not re-discover by burning budget):**
1. Gene universe mismatch: the manuscript's Z_FE universe is 14,390 (axon) /
   3,556 (dendrite); an independent recompute can yield 14,445 / 3,564. If you
   recompute the translation concordance percentages, compare to the PUBLISHED
   CSV universe (14,390 / 3,556), not your own. Flag any place where the two
   disagree.
2. NCBI E-utilities is often blocked ("Access Denied"). To verify references use
   **Europe PMC API** or **Crossref API**, not eutils.
3. Python: use the managed venv
   `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`
   (has xgboost, sklearn, scipy).

## Output contract (every item needs all four)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or section + exact numbers you RERAN
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 a paste-ready English replacement sentence, or an explicit spec
  for a new analysis (variables, strata, output columns)
  ("Consider strengthening the discussion" is banned.)

Also required at the end of your file:
- § Stands up (≥3, with evidence) — things you suspected but found correct.
- § Questions for the authors — what you need to know, do not guess answers.
- § What I actually checked — files read, commands run, values recomputed vs the
  manuscript's, with the discrepancy stated.

## Venue reporting-standard facts (for A4)
Nature / *Scientific Reports*: Title ≤ 20 words; Abstract ≤ 200 words, no
citations; ≤ 8 display items (figures+tables) in main text; figure legends ≤ 350
words; figures ≥ 300 DPI; Data Availability statement must be literally true.
