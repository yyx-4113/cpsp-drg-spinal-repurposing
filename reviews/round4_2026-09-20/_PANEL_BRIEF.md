# Round-4 Independent Review Panel — Shared Brief

**Editor:** 小团 (acting journal editor for this round)
**Target venue:** *Scientific Reports* (Nature Portfolio), Article type, single author (Yang Y / 杨永新), single-author computational study.
**Manuscript under review:** `reports/MVP_ScientificReports_submission.md` (v1.3, 2026-09-20) + `reports/MVP_ScientificReports_supplementary.md`.
**Independence date:** 2026-09-20. Treat this as a *first submission*. Do NOT assume it has passed prior review.

---

## 1. Independence discipline (mandatory)

Forbidden to read (these contain prior-round reviews, author rebuttals, or project-status files that would contaminate a fresh read):
- `reports/REVIEW_round3_2026-09-20.md`, `reports/RESPONSE_round3_2026-09-20.md`, any `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md` in the repo
- `reviews/` directory contents (other than this brief and your own output file)
- `PROJECT_PLAN.md`, `README.md`, `CITATION.cff`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `submission_pack/`
- Any `*_R3_*.json` interpretation notes, task-status files, `.workbuddy/` memory files
- Other reviewers' output files in this round-4 directory

You MAY read:
- `reports/MVP_ScientificReports_submission.md` (the manuscript)
- `reports/MVP_ScientificReports_supplementary.md` (supplementary)
- Any raw/processed data under `results/tables/`, `data/`, `docking/`
- `scripts/` (only to verify how a number was computed — not for prior-review context)

Every judgement must come from text or source data you read yourself. Any claim in the manuscript that you CAN verify, you MUST verify by recomputing from raw sources. Do not take the author's numbers on trust.

---

## 2. Output contract (mandatory)

For every item, four mandatory parts:
- **【Problem】** one sentence
- **【Evidence】** pinned to file:line, or table/section + exact numbers; numbers you cite MUST be ones you recomputed yourself
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance
- **【Specific fix】** a paste-ready English replacement sentence, OR an explicit spec for a new analysis (variables, strata, output columns)

"Consider strengthening the discussion" / "the writing could be clearer" are BANNED. Every item must be actionable.

Also required (as § sections at the end of your file):
- **§ Stands up (≥3, with evidence)** — things you suspected but found to be correct. Deliverable, not filler.
- **§ Questions for the authors** — state what you need to know; do not guess answers.
- **§ What I actually checked** — files read, commands run, values recomputed vs the manuscript, with the discrepancy stated explicitly (or "no discrepancy").

---

## 3. Manuscript summary (self-contained — read the manuscript yourself; this is only orientation)

The study is a purely computational reanalysis of 12 public GEO datasets spanning incision, nerve-injury and tibial-nerve-injury models (rat/mouse/human) on the dorsal root ganglion (DRG)–spinal cord axis, aiming to (a) define a "core axis signature" by Stouffer weighted-Z meta-analysis, (b) test pathway coordination via permutation-calibrated gene-set statistics, (c) identify 35 candidate "hub" genes by a dual-ML consensus (LASSO/RF/XGBoost, leave-one-dataset-out), (d) localise hubs in single-cell / spatial transcriptomes, and (e) run a full-library structure-based docking screen of 3,085 approved drugs against 10 tractable targets with reverse positive controls and MW correction.

Headline claims to scrutinise:
- Core signature = 4,055 genes (meta_FDR<0.05 & direction consistency≥0.8) from 16,552 genes / 6 contrasts. Real per-contrast sample-size weighting.
- Nerve-injury→incision translation concordance 53.9% (7,751/14,390) — reframed as "conserved nerve-injury response, NOT a CPSP-specific pathway".
- Neuroimmune–metabolic axis: neuroinflammation +4.94, DAM +3.88, complement +3.44 (all up, perm p≤0.0005 ceiling), OXPHOS −2.37 (p=0.004).
- SCN9A/10A/11A/8A down in nerve-injury but UP in incision; SCN8A −4.92/FDR 1.0e-5.
- 35 hubs, 32/35 in core, 5/35 three-method; LODO cross-animal floor 0.917; bootstrap 0/35 stable.
- Human miRNA layer negative (set-perm p=0.51).
- Visium: 17/33 detectable hubs in dorsal horn (Sham tissue).
- Docking honest null: ADRA2A Tier-1 AUC 0.618 → full-library 0.532 (p=0.118 NS); no target clears both filters.
- Uniform 10-target plausibility table; ADRA2A framed as weakest on meta-evidence.
- Pending FJNSF grant lists ADRA2A; declared as competing interest, claims no influence.

---

## 4. Source-data inventory (the auditor's mandatory checkpoints)

All under `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛\`

- `results/tables/META_DRG_axis_stouffer.csv` — 16,552-gene Stouffer output; translation concordance (columns `incision_lfc`, `concordant_incision`). Recompute 7,751/14,390 and 2,473/3,556.
- `results/tables/META_DRG_axis_CORE_signature.csv` — core gene list; confirm 4,055 and 32/35 hubs inside.
- `results/tables/_R3_bulkonly_meta_summary.json` — bulk-only core 1,981, overlap 1,732/4,055, SCN directions.
- `results/tables/_R3_plausibility.json` — 10-target meta_Z/FDR/consistency/n_holo_PDB; 17 dock-eligible hubs.
- `results/tables/P3_geneset_stats.csv` — 19 gene sets, mean_Z, %up, perm p.
- `results/tables/P3_hub_genes.csv` — 35 hubs, n_methods, in_meta_core.
- `results/tables/P3_lodo_auc_ci.csv` — LODO AUCs + CIs.
- `results/tables/P3_hub_bootstrap.csv` — per-gene stability.
- `results/tables/P4_hub_targeting_miRNAs.csv`, `P4_hub_miRNA_human_integration.csv` — 3,511 / 752 / 253.
- `results/tables/P5_GSE216039_DRG_hub_finetype_top.csv` — DRG 25 detected, 20/25 localised, enrichment folds.
- `results/tables/P5_hub_lineage_consensus.csv` — 7/35 cross-dataset lineage; 15 NotLocalisable.
- `results/tables/P5_GSE325938_hub_regionalization.csv` — 33 detect, 17 dorsal horn, below-floor set.
- `results/tables/P6_reverse_control.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_BH_correction.csv`, `P6_breadth_chembl_power.csv` — docking AUCs, ΔAUC CIs, BH q, breadth flip.

**Recomputation environment:** managed Python `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe` (has pandas, numpy, scipy, matplotlib). Use it for all recomputes.

---

## 5. Rules for the editor's consolidation

The four experts review independently. The editor will (i) verify the single most severe finding with an independent script, (ii) build a cross-verification table of every recomputed number, (iii) grade issues T0–T3, (iv) adjudicate disagreements rather than averaging, (v) preserve disagreement, and (vi) write a reframe note. Report only; do not modify the manuscript.
