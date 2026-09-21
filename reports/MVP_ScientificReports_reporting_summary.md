# Nature Portfolio Reporting Summary — MVP CPSP DRG–Spinal Axis (to be transferred to the fillable PDF)

> Source template: `nature.com/documents/nr-reporting-summary-flat.pdf` (complete in Adobe Reader; negative disclosures required, do not leave blank or write "n/a" where the form forbids it—use the negative phrasing shown below).
> Study type: **Life sciences** (reanalysis of public transcriptomics). Field-specific branch = Life sciences study design; all animal/human-work items are *negative disclosures* because we generated no new in-vivo/in-human data.

---

## Statistics
- **Exact sample size (n) per group:** Reported per dataset in Methods and in `results/tables/DEG_*.csv` and `P3_lodo_auc_ci_leakage_controlled.csv`. Examples: GSE267799 incision DRG n_case=12/n_ctrl=8; GSE278227 1-week IL/CL n=14/14; GSE241361 n=9 total (≈4–5 per group); GSE158825 n=60 (30 LSS / 30 LSS+DS); single-cell pseudobulk n=2–3/group.
- **Distinct samples vs repeated measures:** Distinct biological samples per dataset; single-cell uses sample-level pseudobulk (never repeated measures on the same cell). Stated in Methods §"Statistical discipline".
- **Statistical tests and sidedness:** Welch t (two-sided) + BH FDR; Stouffer weighted Z meta-analysis (two-sided); one-sample t and 2,000/5,000 same-size permutation tests (two-sided); Spearman ρ; LODO / 5×20 CV / label-permutation null; AUC with one-sided enrichment p. All named in Methods.
- **Covariates tested:** Species and model were used as meta-analysis strata/consistency filters (K≥3, consistency ≥0.8), not as regression covariates. Because the pooled consistency filter mixes incision with nerve-injury contrasts, a separate `nerve_injury_consistency` (five nerve-injury contrasts only) and `incision_agreement` are reported, and a nerve-injury-only meta-analysis is used for the non-circular translation test.
- **Assumptions / corrections:** BH multiple-comparison correction applied *within* each analytical family, with a registry of families in Methods: (i) per-dataset DE, (ii) meta-analysis (fixed and random effects separately), (iii) gene sets — **set-level BH across the 18 multi-member sets**, (iv) docking — BH across the five ChEMBL-annotated targets for raw and size-independent p, (v) single-cell sample-level BH; composite-ranking hypergeometric p-values are descriptive and not counted as inferential. A DerSimonian–Laird random-effects meta-analysis (per-gene τ² and I²) is reported as the primary, heterogeneity-robust result; the fixed-effect (inverse-variance/Stouffer) meta-analysis defines a 4,055-gene discovery superset used for hypothesis generation. Permutation calibration of gene-set and set-level miRNA statistics; molecular-weight (MW) triple correction in docking (MW-only baseline, MW-linear-adjusted, MW-quintile-stratified) plus a multivariate physicochemical control. Normality not assumed—permutation used.
- **Parameters / variation / uncertainty:** Reported as mean_Z, permutation p, AUC with 95% CI (LODO, leakage-controlled; four folds have degenerate DeLong intervals [1.0, 1.0] at test n ≤ 28 and are non-informative, while the only adequately sized fold (GSE267799, n = 20) yields 0.677 [0.374, 0.940]), label-permutation null 0.490 ± 0.085, Wilson 95% CIs for concordance proportions, and bootstrap recovery frequencies (B = 200). CIs given for LODO AUC, with four folds flagged as having degenerate DeLong intervals at small test n.
- **Test statistic, effect sizes, P values:** Exact p reported (e.g., 0.0005, 0.118, 9.4e-9, 0.584); effect sizes as mean_Z, log2-fold enrichment (17.4× etc.), AUC/lift (×18.69), and **risk differences in percentage points with Wilson CIs** for concordance. The previously quoted binomial p ≈ 10⁻²⁰ against a 50% null has been **removed**: a 50% reference is inappropriate for a contrast with a global directional skew, so concordance is now reported as a proportion with a Wilson CI against a 5,000-draw label-permutation null.
- **Bayesian analysis:** Not used.
- **Hierarchical/complex designs:** Single-cell pseudobulk aggregated per animal before testing to avoid pseudoreplication; level of test = animal/sample, not cell. Stated in Methods.
- **Effect-size estimates:** mean_Z, log2 enrichment, AUC/lift; calculated as described in Methods.

## Software and code
- **Data collection:** Public GEO datasets retrieved via GEO/ENTREZ; no bespoke collection software.
- **Data analysis:** Python 3.13 (managed venv) with numpy/scipy/scikit-learn/xgboost/RDKit/Meeko/Open Babel/gemmi; AutoDock Vina 1.2.5. Custom scripts in `scripts/` (p2–p6). Code deposited in the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (MIT LICENSE, CITATION.cff); Zenodo DOI on acceptance.

## Data
- **Availability statement (manuscript):** All code/tables/figures in the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing; processed data mirrored to Zenodo (DOI on acceptance); not "available on request". GEO accessions: GSE267799, GSE212311, GSE278227, GSE241361, GSE265957, GSE158825, GSE222979, GSE216039, GSE328175, GSE246288, GSE306403, GSE325938.
- **Restrictions:** None beyond GEO access terms.

## Research involving human participants, their data, or biological material
- **Reporting on sex and gender:** Not applicable (reanalysis of public datasets; original studies report sex where relevant).
- **Reporting on race, ethnicity, or other socially relevant groupings:** Not applicable.
- **Population characteristics:** Not applicable (no primary human recruitment).
- **Recruitment:** Not applicable.
- **Ethics oversight:** Original GEO studies obtained IRB/IACUC approval and consent as reported therein; this secondary reanalysis generated no new human/animal data, so no additional approval was required. Stated in Methods §"Ethics oversight".

## Animal research (ARRIVE-aligned negative disclosures)
- We performed **no new animal experiments**; all animal-derived data are public GEO deposits from prior approved studies.

## Field-specific reporting — Life sciences study design
- **Sample size:** Determined by public-dataset availability (n per group listed above); not prospectively powered by us.
- **Data exclusions:** None beyond per-dataset QC (cells with <X genes, all-zero barcodes dropped per standard 10x QC; documented in `P5_RESULTS.md` §1).
- **Replication:** Meta-analysis and ML trained/tested across 5–6 independent datasets; LODO provides cross-dataset replication; results are reproducible from deposited code.
- **Randomization:** Not applicable—no experiment performed; ML used fixed train/test splits and LODO.
- **Blinding:** Not applicable—no experiment performed; outcome scoring is computational and pre-specified.

## Specific materials / systems
- **Antibodies / Eukaryotic cell lines / Palaeontology / Animals:** N/A (public data).
- **Clinical data:** Human miRNA data are public de-identified (GSE158825); no new clinical data.
- **Dual-use research of concern / Hazards:** N/A.

## Competing interests
- The author declares no financial competing interests.
- The author has a pending grant application (Fujian Natural Science Foundation) in which ADRA2A is listed among the candidate targets; this application did not fund and did not influence the present analyses, results, or conclusions, and the manuscript was written independently of the grant.

## AI disclosure (per Scientific Reports Editorial Policy)
- An LLM assisted manuscript drafting/language polishing; scientific content, analyses and conclusions were authored and verified by Y.Y. No LLM is an author.
