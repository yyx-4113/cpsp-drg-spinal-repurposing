# Round 10 panel brief — PLOS ONE resubmission (post-Round-9 revision)

## Independence discipline (mandatory)

You are reviewing this manuscript **as if it were a first submission you had never seen**.
You have NO knowledge of previous rounds and must not acquire any.

**Forbidden to read** (violating this invalidates your review):
- `reviews/REVIEW_*.md`, `reviews/RESPONSE_*.md`, `reviews/REVISION_*.md`
- `reviews/round2_*` … `reviews/round9_*` directories and anything inside them
- `.workbuddy/memory/**` (daily logs and long-term project memory)
- `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- Any `REVIEW_round*.md` or `roundN_*` file anywhere in the repository
- **Other reviewers' outputs in this directory** — you work alone

**Also forbidden:**
- Do NOT assume the manuscript is mature or has passed previous review. Treat it as fresh.
- Do NOT accept the manuscript's own framing ("we already checked this", "as noted above").
- Every judgement must come from text or source data **you read yourself**.
- Any claim in the manuscript that you CAN verify, you MUST verify.

## What the manuscript is (self-contained context)

- **Title:** "Conserved nerve-injury-associated transcriptional response on the dorsal root
  ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
- **Venue:** resubmission to **PLOS ONE** (SCIE). The manuscript was previously desk-rejected
  by *Scientific Reports* on non-scientific grounds; it has been rebranded and revised for PLOS ONE.
- **Article type / design:** single-author, multi-dataset **in-silico re-analysis** of public
  transcriptomes — no new experiments, no new human data collection. Two halves:
  1. A cross-dataset meta-analysis of DRG–spinal-axis transcriptional response to peripheral
     nerve injury (bulk RNA-seq/arrays + one translatome + one human plasma miRNA set),
     with hub-gene convergence, gene-set programmes, single-cell/spatial localisation, and
     a machine-learning leave-one-dataset-out (LODO) translation test.
  2. A structure-based drug-repurposing virtual screen (AutoDock Vina) against a tractable
     target subset, which the manuscript presents as an **honest null**.
- **Data provenance:** 12 public GEO accessions — GSE267799, GSE212311, GSE278227, GSE241361,
  GSE265957, GSE158825, GSE222979, GSE216039, GSE328175, GSE246288, GSE306403, GSE325938.
  All processed outputs live in `results/tables/`; reproduction scripts in `scripts/`.
- **Manuscript under review:** `reports/MVP_PLOSONE_submission.md` (332 lines).
  Supporting: `reports/MVP_PLOSONE_supplementary.md`, `reports/MVP_STROBE_checklist.md`,
  `reports/MVP_PLOSONE_cover_letter.md`, `reports/MVP_PLOSONE_compliance_check.md`.
- **Headline numbers you should be able to check** (manuscript asserts these; recompute them):
  fixed-effect meta core 4,055 genes of 16,552 tested; meta FDR<0.05 in 6,869; random-effects
  core 1,008, median τ² 0.232, median I² 38.8%; bulk-only sensitivity core 2,512 (54.3% overlap
  with 4,055); non-circular translation 46.2% vs 47.1% background, risk difference −0.9 pp,
  permutation p = 0.14; LODO incision fold AUC 0.677 [0.374, 0.940] while the four nerve-injury
  folds give AUC 1.0 with degenerate CIs [1.0, 1.0]; ADRA2A docking AUC 0.532 (p = 0.118) across
  3,085 drugs, versus 0.618 on a 620-drug CNS/analgesic-prior subset; OXPHOS set-level q = 0.020
  (fixed effect) and q = 0.31 (random effects); 35 published hub genes, 17 dock-eligible,
  15 NotLocalisable / 20 localisable in single-cell; target-set bootstrap median recovered-set
  size 6 (IQR 5–8), median Jaccard 0.026, P(≥3 of 17) = 0.040.
- **Known structural limits the manuscript itself declares** (check whether it is consistent
  about them, and whether declared limits are actually honoured in every claim):
  ion-channel targets (SCN9A/10A/11A, KCNQ2, CACNA2D1, GABRA1) could not be docked;
  the human plasma-miRNA layer is underpowered (n = 60) and null; ADRA2A is held to a
  two-filter rule and labelled "inconclusive, not a confirmed null"; single-cell claims are
  labelled "directional hints" (sample-level pseudobulk, n = 2–3/group).

## Output contract (mandatory for every item)

For every issue you raise, give four parts:

- **【Problem】** one sentence.
- **【Evidence】** pinned to `file:line`, or table/section + exact numbers. Numbers you cite
  must be ones **you recomputed yourself** from `results/tables/` or the source files.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a paste-ready English replacement sentence, or an explicit spec for a
  new analysis (variables, strata, output columns).

Banned: "consider strengthening the discussion", "the authors should clarify", any fix that is
not paste-ready or spec-complete.

## Also required in your report

- **§ Stands up** (≥3 items, with evidence) — things you suspected, checked, and found to be
  **correct**. Explicitly mark these. This is a deliverable, not filler.
- **§ Questions for the authors** — state what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands run, values recomputed vs the
  manuscript's, with **any discrepancy stated explicitly**.

## Specific hunting instructions for this round

This manuscript has just had a large revision applied. A prior round's fix often *adds a
caveat* in one section while leaving the original over-claim standing in another — that
leaves a self-contradiction, which is the highest-severity class of defect. Therefore:

1. **Disclosure ≠ resolution.** For every place the manuscript concedes a limitation
   (ion channels undockable, human layer null, ADRA2A inconclusive, LODO not generalisable,
   FE-primary conditional, EPV low, bootstrap instability), search the rest of the text —
   especially the Abstract, the new **Conclusions** section, and the cover letter — for a
   statement that still asserts the unqualified version. Quote both locations side by side.
2. **Second-occurrence staleness.** Grep for *values* (not expected locations) across the
   manuscript, supplementary, cover letter, STROBE checklist and compliance document.
   Duplicate occurrences of a statistic, version string, filename or count are where stale
   copies hide.
3. **Internal numerical coherence.** Check that derived quantities are mutually consistent
   (e.g. percentages vs counts, pp differences vs the two percentages they come from,
   CIs vs point estimates, "N of M" denominators that should match the stated set size).
4. **Reporting-standard honesty.** For the venue layer: does every STROBE item's
   "Addressed"/"N/A" status match what the manuscript actually contains? Does the
   compliance document's stated reference/DOI count match the manuscript? Is the
   AI-use disclosure specific and complete?
5. **Do not merely re-verify arithmetic** — the automated gates already do that. Find what
   the gates cannot: design-level, logic-level, and cross-statement contradictions.

## Environment notes (do not rediscover these)

- Use the managed Python at
  `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`
  (numpy / pandas / scipy / sklearn / xgboost available).
- All commands must be run from the repository root:
  `D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛`
  Use `cd "D:/2026.9/..."` (no `/d` flag — that flag fails here).
- Source data is in `results/tables/` (CSV/JSON). Reference the accession list above.
- Do NOT run `p7_renumber_refs.py` or `resolve_ref_dois.py` — they would overwrite the
  manuscript from a stale source file. Read only.

## Do not mention tools

Write review comments only. Do not describe what tools, scripts or commands you used;
report findings, evidence and fixes.
