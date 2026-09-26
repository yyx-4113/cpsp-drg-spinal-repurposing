# Panel Brief — Independent Expert Review Round 6 (2026-09-26)

## Manuscript under review
- **Title:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
- **Author:** Y.Y. (single author, anesthesiology, Fujian). Reanalysis of 12 public GEO datasets; no new wet-lab data.
- **Target venue:** PLOS ONE (pivoted after a Scientific Reports desk-reject that said the finding was "not sufficiently valid or original"). Article type: Research Article (observational bioinformatics reanalysis).
- **Read the manuscript here (canonical rendered text, includes references):**
  `reports/MVP_ScientificReports_submission.md`
  (Source-with-markers also at `reports/_v15_source.md` if you need to see raw `{{ref}}` keys, but the rendered MS is the submission.)
- **Data / provenance (read these to verify numbers):**
  - Meta-analysis core & stats: `results/tables/META_DRG_axis_stouffer.csv`, `results/tables/META_DRG_axis_CORE_signature.csv`, `results/tables/META_bulkonly_sensitivity_summary.json`
  - Random-effects + non-circular translation: `results/tables/_R4_random_effects_meta.csv`, `results/tables/_R4_nerveinjury_only_meta.csv`, `results/tables/_R4_nerveinjury_only_summary.json`, `results/tables/_R4_translation_noncircular.json`, `results/tables/_R4_translation_concordance_effectsize.csv`
  - Gene sets: `results/tables/P3_geneset_stats.csv`, `results/tables/_R4_geneset_setlevel_bh.csv`, `results/tables/_R4_geneset_members.json`
  - Hubs / ML: `results/tables/P3_hub_genes.csv`, `results/tables/P3_lodo_auc_ci.csv`, `results/tables/P3_hub_bootstrap.csv`, `results/tables/_R4_targetset_bootstrap.csv`
  - Docking: `results/tables/P6_reverse_control.csv`, `results/tables/P6_enrichment_mw_confounder_check.csv`, `results/tables/P6_breadth_chembl_power.csv`, `results/tables/P6_BH_correction.csv`, `results/tables/P6_face_validity.csv`, `results/tables/P6_multivariate_physchem_control.csv`, `results/tables/P6_target_plausibility.json`
  - Repo (optional cross-check): https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (tag v1.0.0)

## Independence discipline (MANDATORY, every expert)
- **Forbidden to read:** any file named `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`; anything under `reviews/round2_2026-09-20/`, `reviews/round4_2026-09-20/`, `reviews/round5_2026-09-21/`; `PROJECT_PLAN.md`, `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, and every other reviewer's output file in this round directory.
- Treat this as a **first submission**. Do NOT assume the manuscript is mature or has passed prior review.
- Do NOT read other experts' files mid-review. Every judgement must come from text or source data you read yourself.
- Any claim in the manuscript that you CAN verify, you MUST verify by recomputing from the raw tables above.

## Output contract (every finding needs all four)
- 【Problem】 one sentence
- 【Evidence】 pinned to file:line of the manuscript, OR a table name + exact recomputed numbers; numbers you cite must be ones you recomputed yourself
- 【Why it matters】 concrete effect on conclusions / credibility / acceptance
- 【Specific fix】 a paste-ready English replacement sentence, or an explicit spec for a new analysis (variables, strata, output columns)

"Consider strengthening the discussion" is banned. Each item must be actionable.

## Also required at the end of your file
- **§ Stands up** (≥3, with evidence): things you suspected were wrong but found correct. This is a deliverable, not filler.
- **§ Questions for the authors**: what you need to know; do NOT guess answers.
- **§ What I actually checked**: files read, commands run, values recomputed vs the manuscript, and any discrepancy stated explicitly.

## Cross-cutting expectations
- The manuscript leans hard on an "honest negative" framing (negative human miRNA layer; negative full-library docking; non-predictive translation). Assess whether the negative is genuinely supported or whether some negatives are over-claimed / some positives are under-claimed given the fragility admitted elsewhere.
- The author repeatedly admits fragility (57.3% of core is translatome-dependent; 0/35 hubs stable; same-animal folds; underpowered human n=60). Check for internal contradiction between these honest caveats and any still-overconfident headline statements.
- Single author, no statistics/bioinformatics co-author. Flag methods that are beyond what a single clinician-scientist should assert without an explicit methodological collaborator, and where the manuscript already hedges appropriately.
