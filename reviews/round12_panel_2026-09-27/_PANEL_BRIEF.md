# Round 12 — Independent Expert Panel Brief (CPSP DRG–spinal axis MVP, v1.2.0)

**Date:** 2026-09-27
**Manuscript version under review:** v1.2.0 (PLOS ONE re-submission candidate)
**Editor:** 小团 (consolidating; not a reviewer)

---

## 1. Independence discipline (MANDATORY)

You are reviewing this manuscript **as if you have never seen it before**. This is a
fresh panel; the manuscript has a long revision history but you must NOT read any of it.

**FORBIDDEN to read (for every reviewer):**
- `reviews/REVIEW_*.md`, `reviews/RESPONSE_*.md`, `reviews/REVISION_*.md`
- `reviews/round1*_*/**`, `reviews/round2*_*/**`, `reviews/round3*_*/**`, `reviews/round4*_*/**`,
  `reviews/round5*_*/**`, `reviews/round6*_*/**`, `reviews/round7*_*/**`, `reviews/round8*_*/**`,
  `reviews/round9*_*/**`, `reviews/round10*_*/**`, `reviews/round11*_*/**`
- `reviews/round12_panel_2026-09-27/<other reviewers' files>` (do NOT read siblings in this dir)
- `SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`
- `PROJECT_PLAN.md`, `方案二_*.md`, `_manifest/MANIFEST.sha256` (deposit artefact — not a review source)
- Any `scripts/gate_*.py`, `scripts/_gate_out.txt`, `scripts/p7_consistency_gate.py`
  (these verify arithmetic/self-consistency ONLY, not correctness — do not cite them as evidence)

**Do NOT assume the manuscript is mature or has passed prior review. Treat it as a first submission.**

Every judgement must come from text or source data you read yourself. Any claim in the
manuscript that you CAN verify, you MUST verify by recomputation from raw source files.

---

## 2. What the manuscript is (neutral pointer — verify, don't trust)

- **File:** `reports/MVP_PLOSONE_submission.md` (375 lines) + `reports/MVP_PLOSONE_supplementary.md` (302 lines)
  (absolute root: `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛`)
- **Target venue:** PLOS ONE — article type = **Research Article** (original investigation; explicit policy accepting negative/null results).
- **Study:** In-silico meta-analysis of dorsal-root-ganglion (DRG) transcription after peripheral nerve injury,
  aggregating multiple public mouse GEO datasets. Pipeline: Stouffer meta-analysis → dual-machine-learning
  hub-gene identification → single-cell / spatial localisation of hubs → structure-based repurposing
  (docking) screen of FDA-approved drugs. Secondary: a "honest null" claim that docking enrichment at
  library scale is absent, and that the ion-channel analgesic class was structurally undockable and never screened.
- **Source data live in:** `results/tables/*.csv` and `results/*.json`; raw GEO accessions are named in the text.
- **Built artefacts (verify against these, not just the .md):** `submission_pack/Manuscript.docx`,
  `submission_pack/Supporting_Information.docx` (figures must be EMBEDDED; table structure must match source).

## 3. Output contract (every reviewer)

For **every** item, four mandatory parts:
- **【Problem】** one sentence
- **【Evidence】** pinned to `file:line`, or `table/section + exact numbers` you recomputed yourself
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance
- **【Specific fix】** a paste-ready English replacement sentence, OR an explicit spec for a new analysis
  (variables, strata, output columns). "Consider strengthening the discussion" is BANNED.

Also required at the end of your file:
- **§ Stands up (≥3, with evidence)** — things you suspected were wrong but found correct. Deliverable, not filler.
- **§ Questions for the authors** — what you need to know; do NOT guess answers.
- **§ What I actually checked** — files read, commands run, values you recomputed vs the manuscript's, with the discrepancy stated (or "no discrepancy found").

## 4. Environment / recomputation traps (read before computing)

- **Gate pass ≠ correctness.** `scripts/*gate*.py` and `_gate_out.txt` only test arithmetic self-consistency
  and string matching. They CANNOT catch design-level or provenance defects. Never cite them as "the number is verified."
- **Recompute from RAW sources**, never from the manuscript text or a gate file.
- **Managed Python** (has numpy/pandas/scipy/matplotlib/python-docx):
  `C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe`
- **docx inspection:** `from docx import Document` then iterate `d.tables` and `d.inline_shapes` (figure DPI
  is NOT stored in docx; verify figures are embedded via `inline_shapes` count and that the PNGs in
  `figures/` / `submission_pack/` are 350 DPI).
- **Do NOT mention what tools you use.** Write review comments only.

## 5. Per-layer mandatory checks (in addition to the output contract)

### A1 — Domain (clinician-scientist, CPSP / DRG / neuroinflammation)
- Is the endpoint (neuroinflammation–DAM-like–complement ↑, OXPHOS ↓) mechanistically coherent with CPSP literature?
- Is the title reframe to "DRG-only" consistent throughout (spinal cord presented only as localisation, not as a meta-axis)?
- Is "not CPSP-specific" defensible given the single heterogeneous incision arm (GSE267799 pools two incision models)?
- Is the ion-channel-undockable "honest null" framing honest, or does it under-claim a real limitation?
- Are there must-cite papers (gabapentinoid/NaV1.7/NaV1.8 mechanism, DRG neuroimmune signalling) missing?

### A2 — Design & statistics
- Recompute the Stouffer meta core (4,055), bulk-only core (2,512), overlap (2,202 = 1,707 pure 4/4 + 495 K=3),
  relaxed ≥3/4 (3,587/4,055 = 88.5%), 313 (211 present-but-NS + 102 absent-from-bulk), 468 outside relaxed —
  from `META_DRG_axis_CORE_signature.csv`, `META_bulkonly_meta.csv`, `META_collapse_meta.csv`, `P2_meta_sensitivity.csv`.
- Verify the FE meta SE anti-conservative claim: 11.4% same-animal weight from GSE265957 two timepoints
  (same animals) — recompute the effective independent sample-size overstatement.
- Verify q=0.003 is the BH-adjusted permutation-resolution floor (upper bound) from `P3_geneset_stats.csv` /
  `results/tables/_R4_*` if present.
- Check EPV for the nerve-injury-enriched claim; DeLong CI collapse at AUC=1.0 in `P3_lodo_auc_ci*.csv`;
  bootstrap stability (max 15.5%, 0/35 at ≥0.9) from `P3_hub_bootstrap.csv`.
- Flag any pseudoreplication / sample-size mis-statement.

### A3 — Implementation / provenance
- Recompute every headline number from raw CSV/JSON; list discrepancies vs the manuscript.
- Verify `submission_pack/Manuscript.docx` has EXACTLY ONE Table 2 (35 data rows) and the labels match
  `P3_hub_genes.csv` (in_meta_core True/False → Yes/No). Confirm no duplicate hub table.
- Verify figures embedded (inline_shapes count) and 350 DPI; AI-disclosure statement present in docx text.
- Verify version strings = v1.2.0 and the title string are IDENTICAL across manuscript / cover letter /
  CITATION.cff / README / compliance_check (grep the VALUES, not just expected locations).
- Verify `P3_hub_genes.csv` carries `in_meta_core`; `P5_hub_lineage_consensus.csv` carries NO core-membership field.
- Spot-check reference DOIs (the "37/37" claim) against a sample of the bibliography.

### A4 — Venue / reporting (PLOS ONE editor + STROBE)
- STROBE checklist (`reports/MVP_STROBE_checklist.md`) honesty: does Item 19 etc. reframe the 45.7%
  "translatome-dependence" as a threshold/concordance artefact (not a real biology claim)?
- PLOS ONE hard-fails: abstract ≤300 words (currently stated ~240), figure legends complete, 350 DPI,
  AI-disclosure statement, data-availability (GitHub v1.2.0, NO fabricated DOI), competing-interests,
  ethics statement (public GEO data — are human/animal ethics declarations correct and present?).
- Cover letter vs manuscript: journal name, scope claim, version consistency.
- `reports/MVP_PLOSONE_compliance_check.md`: are its verdicts accurate against the actual artefacts?

---

Editor will consolidate. Write your file to
`reviews/round12_panel_2026-09-27/<codename>_<role>.md` and report a one-line summary back.
