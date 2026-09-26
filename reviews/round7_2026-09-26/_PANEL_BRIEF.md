# Panel Brief — Round 7 Independent Review (CPSP / DRG–spinal-axis meta + repurposing)

**Date:** 2026-09-26
**Manuscript under review:** `reports/MVP_ScientificReports_submission.md` (the *current* file, ~290 lines, ~81 KB).
**Target venue:** PLOS ONE (SCIE, IF ≈ 2.8, Q2, fully OA; explicit "null / negative results welcome" policy). The manuscript was pivoted here after a Scientific Reports editorial desk-reject (not a scientific defect).
**Author status:** single author, Bachelor of Medicine (B.M.) only — the author has NO MD/PhD; the manuscript must not attribute a graduate degree to the author.
**Article type:** reanalysis of public transcriptomes (GEO); no new wet-lab data generated. Positioned as an *honest-negative / methodological-boundary* paper, not a "we found a new drug target" paper.

---

## What the manuscript claims (so you can attack it)

- Integrated **12 GEO datasets, 5 studies, 6 contrasts** (4 bulk DRG nerve-injury studies + 1 surgical-incision bulk DRG study + 1 GSE265957 translatome with D4 & D63 timepoints, treated as non-independent).
- Stouffer weighted-Z meta over **16,552 genes** → **4,055-gene core** (meta_FDR<0.05 & consistency≥0.8). Under random-effects (DerSimonian–Laird) only **1,008** persist (median τ²=0.232, median I²=38.8%).
- Set-level BH-corrected gene-set tests: neuroinflammation, DAM-microglia, complement all q=0.003; OXPHOS q=0.31 (does NOT survive random-effects).
- Sodium channels SCN9A/10A/11A/8A nerve-injury down-regulated but **inverted** in the incision model.
- **Non-circular translation test**: signature built on nerve-injury contrasts only → 46.3% directional agreement with incision vs 47.1% background (−0.9 pp, p=0.14) → "does not predict incision direction."
- 35 candidate hubs; spatial mapping 17/33 detectably-expressed hubs in dorsal horn at baseline.
- Human **blood miRNA layer negative (p=0.51)** — framed as a blood-proxy boundary, not a failure.
- **Full-library docking of 3,085 drugs**: no target clears *both* the full-library and size-independent enrichment filters (ADRA2A Tier-1 0.618 → full-library 0.532, p=0.118, NS) → "honest null at library scale."

## Key declared limitations you should probe

- Ion-channel targets (SCN9A/10A/11A, KCNQ2, CACNA2D1, GABRA1) **could not be docked** (structural inaccessibility) → the repurposing screen cannot speak to the most pain-relevant targets.
- Docking enrichment ceiling ρ≈0.78 (score–enrichment correlation), so even "hits" are weak.
- Human layer fully negative; translation to incision non-predictive.
- Single author, single annotation pipeline; no experimental validation.

---

## Independence discipline (MANDATORY — read this twice)

You are a **fresh reviewer who has never seen this project**. You must NOT read any of the following (they carry the prior rounds' priors and would contaminate your judgement):

- `reviews/REVIEW_round*.md`, `reviews/round*/*` (any prior review rounds)
- Any `RESPONSE_*.md`, `REVISION_*.md`, `RESPONSE_LETTER*.md`
- `_v14_source.md`, `_v15_source.md`, `_v15_source.md.bak` (the stale render-source)
- `MVP_PLOSONE_compliance_check.md`, `MVP_ScientificReports_reporting_summary.md`
- `SUBMISSION_MANIFEST.md`, `GITHUB_PUSH_LIST*.md`, `author_verification_statement.md`, any `*.bak`
- Other reviewers' files in `reviews/round7_2026-09-26/` (do not read A1/A2/A3/A4 outputs)
- The task-status file or any project-overview/README that summarises prior review outcomes

Treat the manuscript as a **first submission**. Do NOT assume it is mature or has "already passed review." Every judgement must come from text or source data you read yourself. Any quantitative claim in the manuscript that you CAN verify, you MUST verify by recomputing from the raw sources.

The diagnostic signal that independence worked: several experts, independently, converge on the SAME defect from different angles. If you only find already-known issues, your independence leaked — look harder at the *current* text for *new* self-contradictions the prior rounds may have introduced (e.g. a caveat added in one section while an over-claim still stands in another).

---

## Output contract (every finding MUST have all four)

- **【Problem】** one sentence naming the defect.
- **【Evidence】** pinned to `file:line` in the manuscript, or table/section + exact numbers. **Numbers you cite must be ones you recomputed yourself** from the source files; state the source file and the value you got.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance at PLOS ONE.
- **【Specific fix】** a paste-ready English replacement sentence, OR an explicit spec for a new analysis (variables, strata, output columns). "Consider strengthening the discussion" is banned.

Also required in your report:
- **§ Stands up (≥3, with evidence)** — things you suspected were wrong but verified are actually correct. This is a deliverable, not filler.
- **§ Questions for the authors** — what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands run, values recomputed vs the manuscript, with any discrepancy stated explicitly.

---

## Source data & environment traps (so you don't burn budget rediscovering them)

All paths are under `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛\`.

**DEG input tables** (`results/tables/DEG_*.csv`): per-contrast differential expression. Columns include `symbol, log2FC, t, p, n_case, n_ctrl`. The meta script computes `Z = sign(t)*norm.isf(p/2)` and `w = sqrt(n_case*n_ctrl/(n_case+n_ctrl))`. Verify the manuscript's meta numbers by recomputing Stouffer Zc = (Σ Zs·ws)/sqrt(Σ ws²) with BH FDR.
- Primary 4 bulk contrasts: `DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`, `DEG_GSE212311_CCI_DRG__CCI_vs_Sham.csv`, `DEG_GSE278227_CCI_DRG__1W_IL_vs_CL_pooled.csv`, `DEG_GSE241361_S1R_DRG__SNI_vs_Naive_WT.csv`.
- Incision (5th study): `DEG_GSE267799_SMIR_DRG__acute_vs_baseline.csv` (or chronic_vs_acute) — check which the manuscript uses.
- Translations: `data/processed/GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv` / `Day63_...csv` (ribosome-profiling; the two timepoints are NON-independent — same animals).

**Meta outputs:** `results/tables/META_DRG_axis_stouffer.csv` (6-input primary), `results/tables/META_bulkonly_meta.csv` (4-bulk, NEW this round), `results/tables/META_bulkonly_sensitivity_summary.json` (contains `setcalls` + the bulk-only core size; verify the core size you recompute matches the JSON and the manuscript — there was a recent reconciliation from 1,981→2,512).

**Gene-set stats:** `results/tables/P3_geneset_stats.csv` (set-level means/Z/frac_up). Scripts: `scripts/p3_genesets.py`.

**Hub / ML:** `results/tables/P3_hub_genes.csv`, `P3_ml_metrics.csv`, `P3_lodo_auc_ci.csv`, `P3_lodo_auc_ci_leakage_controlled.csv`. Scripts: `scripts/p3_hub*.py`. Verify the "35 hubs" and any AUC/CI claims against these.

**Human miRNA layer:** `results/tables/P4_GSE158825_miRNA_LSSDS_vs_LSS.csv`, `P4_GSE158825_miRNA_painoutcome_spearman.csv`. The p=0.51 claim and the "blood-proxy" framing must be checked against these.

**Spatial localisation:** `results/tables/P4_GSE249746_hub_celltype.csv` (the 17/33 claim). Scripts: `scripts/p4_*.py`.

**Docking (P6):** `results/tables/P6_*`. The ADRA2A 0.618→0.532, p=0.118 and the "no target clears both filters" claim. Scripts: `scripts/p6_*.py`. Verify the two-filter logic and the ρ≈0.78 ceiling.

**Scripts for provenance (read these to verify methods):** `scripts/p2_deg_meta.py`, `scripts/p2_meta_sensitivity.py`, `scripts/p3_genesets.py`, `scripts/p4_*.py`, `scripts/p5_*.py`, `scripts/p6_*.py`.

**Reporting artefacts (current submission — you MAY read these, but verify independently, do not trust the author's self-mapping):**
- `reports/MVP_STROBE_checklist.md` (STROBE 22-item self-mapping)
- `reports/MVP_PLOSONE_cover_letter.md`, `submission_pack/Cover_Letter_PLOSONE.docx`
- `submission_pack/Manuscript.docx`, `submission_pack/Supporting_Information.docx`

**Trap list:**
- GSE265957 Day4 & Day63 are the SAME animals at two timepoints → NOT independent contrasts. If the manuscript treats them as 2 independent inputs, that is a design defect (check the meta weight assignment).
- "Consistency" = max(up, K-up)/K; core requires consistency≥0.8. Verify the core count is reproducible from the CSV.
- Bulk-only core uses a UNION of genes present in ≥3 of 4 bulk contrasts (same K≥3 rule as primary) → should be 2,512, not 1,981.
- ADRA2A docking: 0.618 is the Tier-1 (CNS-priori subset) enrichment; 0.532 is the full-library enrichment. The "honest null" conclusion rests on the full-library number being NS (p=0.118). Verify the two are not conflated.
- Single author with B.M. only — any "Dr." / "MD" / "PhD" attribution is a hard error.
- The manuscript was edited directly (not via the `{{key}}` source) — check that the abstract (≤200 words), reference numbering (Vancouver, first-appearance order 1–33), and in-text citations all still cohere after the recent renumbering.

---

## Your role (codename)

You are **A1 (Domain)** / **A2 (Design)** / **A3 (Implementation)** / **A4 (Venue)** — see your individual prompt. Stay in your lane but flag cross-cutting issues explicitly. Do NOT mention what tools you used; write review comments only. Write your full report to `reviews/round7_2026-09-26/<codename>_<role>.md` using the Write tool. If a tool error blocks you, re-dispatch is handled by the editor — finish your written report with what you could verify.
