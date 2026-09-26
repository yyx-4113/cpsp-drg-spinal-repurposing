# ROUND 9 — Independent Multi-Expert Panel Brief

**Manuscript:** `reports/MVP_ScientificReports_submission.md` (283 lines)
**Project dir:** `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛\`
**Target venue:** PLOS ONE (SCIE). The authors pivoted here after a Scientific Reports desk-reject. This is a *reanalysis* of 12 public GEO datasets (DRG–spinal-axis chronic postsurgical pain / nerve-injury transcriptomics + a full-library FDA-drug docking repurposing screen). The manuscript's own framing: an "honest negative" docking null + a nerve-injury-associated (not CPSP-specific) neuroimmune–metabolic axis.
**Date:** 2026-09-26
**Editor:** the panel coordinator consolidates; experts write only their own file.

---

## Independence discipline (MANDATORY)

Forbidden to read — under any circumstances:
- `reviews/REVIEW_round*.md`, `reviews/round*/*`, including this round's sibling files `reviews/round9_2026-09-26/<other experts>.md`
- `.workbuddy/memory/**`, `SUBMISSION_MANIFEST.md`, any `RESPONSE_*.md`, `REVISION_*.md`, author_verification_statement.md, `GITHUB_DEPOSIT_SOP.md`
- any conversation history / prior expert outputs

Do NOT assume the manuscript is mature, has passed review, or that prior issues were fixed. Treat it as a **first submission**. Every judgement must come from text or source data you read YOURSELF. Any claim in the manuscript that you CAN verify, you MUST verify by recomputation.

## Output contract (four mandatory parts per item)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line, or table/section + exact numbers; numbers you cite MUST be ones you recomputed yourself from the raw source
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 a paste-ready English replacement sentence, or an explicit spec for a new analysis

"Consider strengthening the discussion" is banned.

## Also required at the end of your file
- § Stands up (≥3 items, with evidence) — things you suspected but found to be CORRECT. This is a deliverable.
- § Questions for the authors — state what you need to know; do not guess answers.
- § What I actually checked — files read, commands/reads run, values recomputed vs the manuscript, with any discrepancy stated.

---

## Environment trap list (this data source) — do not rediscover these
- **Citation glyphs are Unicode superscripts** (¹…³³). Ranges like `²⁵–²⁸` expand to refs 25,26,27,28. When checking "every reference is cited", parse superscripts; a range satisfies all members.
- **Headline numbers to recompute** (source files in `results/tables/`):
  - FE core 4,055; RE core 1,008 (τ²=0.232, I²=38.8%); bulk-only 2,512; overlap 2,202/4,055=54.3% → `META_DRG_axis_stouffer.csv`, `META_bulkonly_meta.csv`, `META_bulkonly_sensitivity_summary.json`
  - collapse (5-input) 4,294; retained 3,707/4,055=91.4% → `META_collapse_meta.csv` (verify it exists and matches)
  - gene-set q=0.003 (neuroimmune/DAM/complement); OXPHOS FE q=0.020 / RE q=0.31 → `P3_geneset_stats.csv`, `_R4_geneset_setlevel_bh.csv`
  - non-circular 46.3% vs 47.1%, −0.9 pp, p=0.14 → `_R4_nerveinjury_only_summary.json` (stratum `NI_FDR05_AND_NIcons>=0.8`)
  - LODO leakage-controlled 0.677 [0.374,0.940] incision fold; other 4 nerve-injury folds AUC=1.000 → `P3_lodo_auc_ci_leakage_controlled.csv`
  - ADRA2A 0.618→0.532, p=0.118 (full-library) ; MW-adjusted ΔAUC p≈0.0005; size-indep BH q=0.0025 → `P6_BH_correction.csv`, `P6_breadth_chembl_power.csv`, `P6_reverse_control.csv`. **Two-filter rule:** a target clears only if it passes BOTH the full-library enrichment filter (ADRA2A FAILS: 0.532 p=0.118) AND the size-independent filter (ADRA2A passes: BH q=0.0025). Because it fails the first, ADRA2A is "inconclusive", NOT a confirmed hit.
  - human miRNA p=0.51 (n=60) → `P4_hub_miRNA_human_integration.csv`, `P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`
  - 3,085 drugs; 30,850 poses; 30,687 scored; ~3,070/target → `P6_ligand_library.csv`, `P6_docking_scores_merged.csv`
  - 17/33 hubs dorsal horn → `P5_GSE325938_hub_regionalization.csv` (`present` recomputed from top_detection>0; expected True=33/False=2)
  - 17/35 DRG localised → `P5_GSE216039_DRG_hub_finetype_top.csv`
- **GSE265957 weighting:** bulk-contrast w² = 2.19/1.22/2.65/1.49; the two translatome timepoints each w=1.00 (w²=1.00). Verify the manuscript's weight statement at L44.
- **Do not** re-litigate the ADRA2A "contradiction" as if it were real — the two-filter logic is internally consistent (verified prior rounds). Your job is to check for NEW defects, not rehearse old ones, but you may note if the prose is *still* unclear.

## Tool-talk forbidden
Do not mention what tools/commands you used. Write review comments only.

## Your specific scope is in your individual prompt (separate message). Write your report to `reviews/round9_2026-09-26/<codename>_<role>.md`.
