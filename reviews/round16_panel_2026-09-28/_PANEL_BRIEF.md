# Round 16 — Independent Review Panel Brief (enforced independence)

**Manuscript under review:** `reports/MVP_PLOSONE_submission.md` (single-author, Yongxin Yang / yyx-4113),
target journal **PLOS ONE**. Repository: `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`,
release tag **v1.6.0**. This is a *reanalysis of 12 public GEO transcriptome datasets* (DRG-centred
nerve-injury axis with spinal-cord localisation + an FDA-drug repurposing docking screen). No new
wet-lab data. The paper deliberately reports honestly negative results (human plasma miRNA layer
p = 0.51; full-library docking screen null) as a "methodological boundary".

## Independence discipline (MANDATORY)

You are reviewing this **as if you have never seen it**. You MUST NOT read any of the following:
- `reviews/REVIEW_round*.md`, `reviews/round*_panel_*/`, `reviews/RESPONSE_*.md`, `reviews/REVISION_*.md`
- `reports/MVP_PLOSONE_compliance_check.md`, `reports/MVP_PLOSONE_cover_letter.md`
- `submission_pack/SUBMISSION_MANIFEST.md`, `submission_pack/Reporting_Summary.md`
- `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- Other reviewers' output files inside `reviews/round16_panel_2026-09-28/` (do not read sibling `<codename>_*.md`)
- Any `_archive/` directory or `.bak` files

Treat the manuscript as a **first submission**. Do not assume it is mature or has passed prior review.
Every judgement must come from text or source data **you read yourself**. Any claim in the manuscript that
you CAN verify numerically, you MUST verify (recompute from the raw artefact files, not from the manuscript).

## Output contract (every item needs all four parts)

- **【Problem】** one sentence
- **【Evidence】** pinned to `file:line` in the manuscript, or `table/section + exact numbers`; numbers you
  cite must be ones you recomputed yourself from the authoritative files
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a new analysis

"Consider strengthening the discussion" is banned. Vague praise is banned.

## Also required (these are deliverables, not filler)

- **§ Stands up** (≥3 items, with evidence) — things you suspected might be wrong but found to be correct.
- **§ Questions for the authors** — what you need to know; do not guess the answers.
- **§ What I actually checked** — files read, commands/scripts run, values recomputed vs the manuscript,
  and the discrepancy (or "no discrepancy") stated explicitly.

## Authoritative data files (use ONLY these; do not trust any file not listed)

- Core meta-analysis: `results/tables/META_DRG_axis_CORE_signature.csv`, `results/tables/META_DRG_axis_stouffer.csv`
- Random-effects / non-circular: `results/tables/_R4_random_effects_meta.csv`, `results/tables/_R4_nerveinjury_only_summary.json`, `results/tables/_R4_nerveinjury_only_meta.csv`, `results/tables/_R4_translation_noncircular.csv`, `results/tables/_R4_translation_concordance_effectsize.csv`, `results/tables/_R4_geneset_setlevel_bh.csv`, `results/tables/_R4_geneset_members.json`, `results/tables/_R4_targets_fixed_vs_random.csv`, `results/tables/_R4_targetset_bootstrap.csv`
- Bulk-only / collapse sensitivity: `results/tables/META_bulkonly_sensitivity_summary.json`, `results/tables/META_bulkonly_meta.csv`, `results/tables/META_collapse_meta.csv`
- Hubs: `results/tables/P3_hub_genes.csv`, `results/tables/P3_hub_bootstrap.csv`, `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`, `results/tables/P3_geneset_stats.csv`
- Human miRNA: `results/tables/P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`, `results/tables/P4_GSE158825_miRNA_painoutcome_spearman.csv`, `results/tables/P4_hub_miRNA_human_integration.csv`
- Localisation: `results/tables/P5_GSE216039_DRG_hub_finetype_top.csv`, `results/tables/P5_hub_lineage_consensus.csv`, `results/tables/P5_GSE325938_hub_regionalization.csv` (note: file may be named `...regionalisation.csv` or similar — locate it)
- Docking: `results/tables/P6_reverse_control.csv`, `results/tables/P6_enrichment_mw_confounder_check.csv`, `results/tables/P6_BH_correction.csv`, `results/tables/P6_breadth_chembl_power.csv`, `results/tables/P6_target_plausibility.json`, `results/tables/P6_docking_scores_merged.csv`
- Submission pack (for Venue reviewer): `submission_pack/Manuscript.docx`, `submission_pack/Supporting_Information.docx`, `submission_pack/Cover_Letter.docx`, `reports/MVP_PLOSONE_supplementary.md`, `reports/MVP_STROBE_checklist.md`

## Environment traps (learned the hard way — do not waste budget rediscovering them)

1. **Stale cached numbers.** Older drafts claimed a 4,055-gene core, 54.3% bulk overlap, 91.4% collapse
   retention, and referenced a `MANIFEST.sha256` file that **does not exist**. The current authoritative
   values are **2,750 core / 63.2% / 91.0%**, and there is **no MANIFEST file**. Use only the files above.
2. **`_R4_*` are the re-derived Round-14 outputs.** Older siblings (`P2_meta_sensitivity.csv`,
   `P3_geneset_stats.csv`) may disagree; the manuscript's current claims are sourced from `_R4_*`.
3. **Translation denominator.** The canonical denominator is **14,390** incision-measured genes
   (used throughout the reported concordance). An exploratory file (`_R4_translation_noncircular.csv`)
   shows 14,445 / 3,564 — that file is superseded; the manuscript states this. Verify the reported
   43.3% (1,660 / 3,830) and 47.1% (6,772 / 14,390) use the 14,390 denominator consistently.
4. **ADRA2A is NOT a positive result.** Full-library AUC = **0.532 (p = 0.118, NS)** is the decisive
   null. The MW-adjusted AUC = 0.578 with ΔAUC p ≈ 0.0005 is explicitly "inconclusive" in the manuscript
   and must not be read as support. Do not let any framing invert this.
5. **Reverse-control AUCs (AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779)** are *method-validation*
   only. The authoritative enrichment test is the **size-independent (MW-adjusted) ΔAUC**, whose 95% CI
   **contains zero** for AXL and TNIK; ACVR1/MAPK14 merely match the MW-only baseline. Do not conflate.
6. **SCN bulk meta_Z / meta_FDR** in Table 1b come from the **4-bulk Stouffer** (`META_bulkonly_meta.csv`),
   not the 6-contrast primary. They are real bulk truth (e.g. SCN9A −2.92 / 0.011).
7. **FE core is reported as primary by design.** The manuscript explicitly frames the random-effects core
   (508 genes) as a *sensitivity bound*, not as a refutation of the FE result. Evaluate this analytic
   choice on its merits; it is a legitimate convention, not an error.
8. **The docking screen could not test ion channels** (SCN9A/10A/11A/KCNQ2/CACNA2D1/GABRA1) — they are
   *undockable* (no ligand-anchored pocket). The honest null is scoped to *docking enrichment at library
   scale*, never to those targets. Do not demand a docking hit there.
