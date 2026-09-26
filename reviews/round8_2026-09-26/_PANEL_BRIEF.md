# Panel Brief — Independent Review Round 8 (2026-09-26)

**Manuscript under review:** `reports/MVP_ScientificReports_submission.md`
(283 lines; title: *Conserved nerve-injury-associated transcriptional response on the
dorsal root ganglion–spinal axis: non-predictive incision translation and an honest
repurposing null*). This is a reanalysis of 12 public GEO datasets (5 studies, 6
contrasts; 4 nerve-injury models + 1 surgical-incision model) on the DRG–spinal
pain axis, plus a full-library structure-based repurposing screen. The authors
claim a nerve-injury-associated neuroimmune–metabolic axis, a non-predictive
incision translation, a negative human blood-miRNA layer, and an honest null at
library scale (3,085-drug docking against 10 tractable targets, ion-channel class
undockable). Target venue this round: **PLOS ONE** (which requires a structured
abstract, STROBE 2007 adherence, data/code availability, an AI-use declaration,
and references with resolvable identifiers).

## Independence discipline (MANDATORY — read this whole block)

You are reviewing this as a **first submission**. You have **not** seen prior
review rounds and must not. Treat every claim as unverified until you verify it.

**FORBIDDEN to read (any of these contaminates independence — do not open them):**
- `reviews/REVIEW_round2_2026-09-20.md` through `REVIEW_round7_2026-09-26.md`
- `reviews/round2_2026-09-20/`, `round4_2026-09-20/`, `round5_2026-09-21/`,
  `round6_2026-09-26/`, `round7_2026-09-26/` (any subfolder)
- any file matching `RESPONSE_*.md`, `REVISION_*.md`, `SUBMISSION_MANIFEST.md`,
  `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- `.workbuddy/memory/` (any file — this is the author's private project journal)
- `reviews/round8_2026-09-26/<any other expert's file>*.md` — do NOT read the
  other panellists' outputs; you must form your own judgement independently.
- The conversation summary / chat history of the author. You only have this brief
  and the files you open yourself.

Do not assume the manuscript is mature or has "passed" anything. Do not grade a
delta — grade the **current state**.

**Every judgement must come from text or source data you read yourself.**
**Any claim in the manuscript that you CAN verify, you MUST verify** by
recomputing from raw source files (see pointers below). "The author says so" is
not evidence.

## Output contract (every item MUST have all four parts)

For every issue you raise, write exactly:
- **【Problem】** one sentence naming the defect.
- **【Evidence】** pinned to `file:line` in the manuscript, OR `table/section + exact
  numbers`. Numbers you cite as "the manuscript is wrong" must be ones **you
  recomputed yourself** from the source files; show the value you got and the
  value the manuscript states.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a paste-ready English replacement sentence, OR an explicit
  spec for a new analysis (variables, strata, output columns). Banned: "Consider
  strengthening the discussion."

## Also required sections in your report
- **§ Stands up** (≥3, with evidence) — things you suspected were wrong but found
  correct. This is a deliverable, not filler.
- **§ Questions for the authors** — what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands run, values you recomputed
  vs the manuscript's, with any discrepancy stated.

## Source-data pointers (recompute from these; find the authoritative file yourself)
Use the managed Python: `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`
(pandas is available; if not, use stdlib `csv`). Work from the repo root
`D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛`.

Likely-authoritative source files (verify which actually contains each number):
- Core signature / FE vs RE membership: `results/tables/META_DRG_axis_CORE_signature.csv`,
  `results/tables/META_DRG_axis_stouffer.csv`
- Bulk-only sensitivity (2,512): `results/tables/META_bulkonly_meta.csv`,
  `results/tables/META_bulkonly_sensitivity_summary.json`
- Gene-set tests (q=0.003; OXPHOS FE q=0.020 / RE q=0.31):
  `results/tables/P3_geneset_stats.csv`, `results/tables/_R4_geneset_setlevel_bh.csv`
- Non-circular translation (46.3% vs 47.1%, p=0.14):
  `results/tables/_R4_translation_noncircular.json`
- Leakage-controlled LODO AUC (0.677 [0.374,0.940]):
  `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`, `P3_lodo_auc_ci.csv`
- ADRA2A docking (0.618→0.532, p=0.118; MW ΔAUC p≈0.0005):
  `results/tables/P6_breadth_paired_vs_adra2a.csv`, `P6_reverse_control.csv`,
  `P6_enrichment_mw_confounder_check.csv`
- Human miRNA layer (p=0.51, n=60): `results/tables/P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`
- Docking scale (3,085 drugs; 30,850 poses; 30,687 scored; ~3,070/target):
  `results/tables/P6_docking_scores_merged.csv`, `P6_param_summary.csv`,
  `P6_ligand_library.csv`
- Hub dorsal-horn localisation (17/33): `results/tables/P5_GSE216039_DRG_hub_localisation.csv`
- Reference DOIs: `results/tables/_R4_ref_DOIs.json`

Derived artifacts you MAY read (they are outputs, not prior reviews):
`submission_pack/Manuscript.docx`, `submission_pack/STROBE_Checklist.docx`,
`submission_pack/Cover_Letter_PLOSONE.docx`, `reports/MVP_STROBE_checklist.md`,
`scripts/p7_consistency_gate.py`, `scripts/build_sr_submission_pack.py`.

## Cross-cutting checks the editor especially wants (fresh eyes)
1. **Internal contradiction hunt.** A prior round often adds a caveat in one
   section while the original over-claim stays in another. Read the WHOLE text.
   If the Abstract/Conclusion says "honest null / methodological boundary" but a
   Results/Discussion sentence still over-claims (e.g. calls the ML a validated
   cross-model classifier, or implies ADRA2A is a confirmed hit/null), quote BOTH
   locations side by side as a P0 self-contradiction.
2. **Second-occurrence staleness.** The title, STROBE version, Zenodo DOI, and
   version strings appear in the manuscript, the STROBE checklist, and the cover
   letter. Grep every derived artifact for the VALUE (not the expected location)
   and flag any mismatch.
3. **Disclosure ≠ resolution.** Where the manuscript discloses a limitation
   (e.g. 0.677 leakage CI, GSE265957 double-weight, human-miRNA underpower),
   check whether the surrounding conclusion was actually retracted or merely
   qualified elsewhere.

## Tool talk
Do not mention what tools/scripts you used. Write review comments only, as if you
are a domain expert writing a reviewer report.
