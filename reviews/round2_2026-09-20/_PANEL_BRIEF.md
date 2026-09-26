# Panel Brief — Independent Review of the CPSP DRG–Spinal Axis manuscript (v1.1)

> This brief is shared by all four reviewers. It encodes the independence discipline
> that makes this review worth more than the automated gates. Read it once; the
> per-expert prompt repeats the non-negotiable parts.

## 1. Manuscript under review

- **Main manuscript:** `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛\reports\MVP_ScientificReports_submission.md`
- **Supplementary:** `reports/MVP_ScientificReports_supplementary.md`
- **Reporting summary:** `reports/MVP_ScientificReports_reporting_summary.md`
- **Cover letter:** `reports/MVP_ScientificReports_cover_letter.md`

**Venue targeted:** *Scientific Reports* (Nature Portfolio), submitted as an **Article** (original research).

**One-line claim:** A purely computational, 12-GEO-dataset reanalysis defines a 4,055-gene "neuroimmune–metabolic" chronic postsurgical pain (CPSP) dorsal-root-ganglion–spinal-cord axis; a leakage-controlled dual-ML consensus locks 35 hub genes; a prospectively specified, full-library structure-based docking screen of 3,085 FDA-approved drugs yields an *honest null* (no robust, size-independent target enrichment).

**Status assumption:** Treat this as a **first submission**. Do NOT assume it has been reviewed, revised, or gated. Every judgement must come from text or source data you read yourself.

## 2. Independence discipline (MANDATORY — violation voids the review)

Forbidden to read (any of these contaminates independence):
- `reports/REVIEW_round1_2026-09-20.md` (prior-round review)
- `submission_pack/SUBMISSION_MANIFEST.md`
- `PROJECT_PLAN.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `README.md`, `CITATION.cff`
- Other reviewers' output files inside `reviews/round2_2026-09-20/` (do not open `A1_*`, `A2_*`, `A3_*`, `A4_*` before your own draft is written)
- The gate scripts `scripts/gate_consistency.py`, `scripts/gate_word.py`, `scripts/verify_sr_docx.py` — you MAY read the **analysis** scripts `scripts/p2*.py`…`scripts/p6*.py` to audit methodology, but you MUST recompute the headline numbers yourself from raw CSVs; never cite a gate's PASS/FAIL as your verification.

Any claim in the manuscript that you **can** verify, you **must** verify by recomputation.

## 3. Source data (the source of record — recompute from these)

- `results/tables/META_DRG_axis_CORE_signature.csv` — meta-analysis core signature (cols: symbol,K,meta_Z,meta_p,consistency,n_up,n_dn,lfc_*,meta_FDR,incision_lfc,concordant_incision)
- `results/tables/P3_hub_genes.csv` — 35 hubs (symbol,n_methods,lasso_freq,rf_gini,shap_meanabs,in_meta_core)
- `results/tables/P3_lodo_auc_ci.csv` — LODO AUC with 95% CI
- `results/tables/P3_geneset_stats.csv` — 19 gene-set statistics (permutation p)
- `results/tables/P5_GSE216039_DRG_hub_finetype_top.csv` — DRG neuron-subtype localisation
- `results/tables/P5_hub_lineage_consensus.csv`, `results/tables/P5_GSE325938_hub_regionalization.csv` — spinal single-cell + Visium
- `results/tables/P6_ranking_drugs.csv` — 3,078-drug docking ranking
- `results/tables/P6_reverse_control.csv` — reverse positive-control AUCs
- `results/tables/P6_enrichment_mw_confounder_check.csv` — MW correction
- `results/tables/P6_multivariate_physchem_control.csv`, `results/tables/P6_BH_correction.csv` — Supplementary Table S4
- `results/tables/DEG_*.csv` — per-dataset sample sizes / group n
- **Python interpreter:** `C:/Users/Administrator/.workbuddy/binaries/python/versions/3.13.12/python.exe`

## 4. Output contract (every item needs all four)

- **【Problem】** one sentence — what is wrong.
- **【Evidence】** pinned to `manuscript:line` OR `table/section` + exact numbers; numbers you cite MUST be recomputed by you, not quoted from the text.
- **【Why it matters】** concrete effect on conclusions / credibility / acceptance.
- **【Specific fix】** a paste-ready English replacement sentence, OR an explicit spec for a new analysis (variables, strata, output columns). "Consider strengthening the discussion" is BANNED.

## 5. Also required (deliverables, not filler)

- **§ Stands up (≥3, with evidence)** — things you suspected were wrong but found correct; explicitly mark them.
- **§ Questions for the authors** — state what you need to know; do NOT guess answers.
- **§ What I actually checked** — files read, commands run, values you recomputed vs the manuscript's, with any discrepancy stated.

## 6. Environment traps

- Some CSVs are large (P6_ranking_drugs ≈ 3,078 rows). Read with python `csv`, do not eyeball.
- **Gene-set permutation p floor:** 2,000 permutations → the minimum observable p is exactly **0.0005**. Any gene-set p reported as exactly 0.0005 sits AT the floor — it cannot be "more significant" than that; treat "p = 0.0005" and "p ≤ 0.0005" as equivalent and note the resolution limit.
- **Sidedness:** docking AUC enrichment p is one-sided; permutation-calibration p is two-sided — confirm against the Reporting Summary.
- **ADRA2A has 115 known ChEMBL pairs** out of ~3,070 docked ligands. If docking worked it should be *easy* to separate; its low AUC (0.532) is the honest signal, not a hard-to-separate target.
- **Reference citation completeness:** in Nature style every reference must be cited in the text. Check that refs 5, 11, 12 (and all 18) actually appear as in-text superscripts.
