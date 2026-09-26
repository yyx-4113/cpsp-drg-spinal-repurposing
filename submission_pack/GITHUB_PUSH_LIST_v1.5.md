# GitHub push list — v1.5 (repository is NOT yet in sync with the manuscript)

Repository: https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (public, main, 196 entries, last push 2026-09-19)

**Why this matters:** the manuscript's Data Availability statement says the repository "already
contains all processed data". That claim is currently FALSE — the 5 JSON/CSV named in the statement,
the `p7_*.py` scripts, the figures, and the v1.5 source/docs are all absent from the last push
(2026-09-19). Push everything below before submitting.

**Two repo-state notes for v1.5:**
- `.gitignore` was updated to exclude `submission_pack/SUBMISSION_MANIFEST.md` and
  `submission_pack/GITHUB_PUSH_LIST_v1.4.md` (this file is itself gitignored). The two internal
  docs will NOT be pushed — that is intended; do not force-add them.
- `figures/` is gitignored in the repo, so the 5 PNGs must be force-added: `git add -f figures/`.

## Exact commands (run from the project root)

```bash
git add -f figures/Fig1_geneset_programme.png figures/Fig2_hub_convergence.png \
          figures/Fig3_DRG_neuron_subtype_localisation.png \
          figures/Fig4_spinal_lineage_visium.png figures/Fig5_docking_honest_null.png
git add results/tables/ scripts/ reports/ CITATION.cff .gitignore README.md
git commit -m "v1.5: non-circular translation, RE meta, set-level BH, honest-null framing; add Costigan 2002 & Schafer 2012"
git push origin main
```

## A. Cited by the manuscript but MISSING from the repository (must add)

- [ ] `figures/Fig1_geneset_programme.png`            (force-add: gitignored)
- [ ] `figures/Fig2_hub_convergence.png`             (force-add: gitignored)
- [ ] `figures/Fig3_DRG_neuron_subtype_localisation.png` (force-add: gitignored)
- [ ] `figures/Fig4_spinal_lineage_visium.png`       (force-add: gitignored)
- [ ] `figures/Fig5_docking_honest_null.png`         (force-add: gitignored)
- [ ] `results/tables/P3_hub_bootstrap.csv`
- [ ] `results/tables/P5_GSE325938_hub_regionalization.csv`
- [ ] `results/tables/P6_multivariate_physchem_control.csv`
- [ ] `results/tables/_R4_geneset_setlevel_bh.csv`
- [ ] `results/tables/_R4_random_effects_meta.csv`
- [ ] `results/tables/_R4_targets_fixed_vs_random.csv`
- [ ] `results/tables/_R4_targetset_bootstrap.csv`
- [ ] `results/tables/_R4_translation_concordance_effectsize.csv`
- [ ] `scripts/p3_hub_bootstrap.py`
- [ ] `scripts/p7_targetset_bootstrap.py`

## B. New v1.4/v1.5 analysis artifacts (must add)

- [ ] `results/tables/_R4_geneset_members.json`
- [ ] `results/tables/_R4_geneset_setlevel_bh.csv`
- [ ] `results/tables/_R4_nerveinjury_only_meta.csv`
- [ ] `results/tables/_R4_nerveinjury_only_summary.json`
- [ ] `results/tables/_R4_random_effects_meta.csv`
- [ ] `results/tables/_R4_reference_map.json`
- [ ] `results/tables/_R4_supplementary_summary.json`
- [ ] `results/tables/_R4_targets_fixed_vs_random.csv`
- [ ] `results/tables/_R4_targetset_bootstrap.csv`
- [ ] `results/tables/_R4_targetset_bootstrap.json`
- [ ] `results/tables/_R4_translation_concordance_effectsize.csv`
- [ ] `results/tables/_R4_translation_noncircular.csv`
- [ ] `results/tables/_R4_translation_noncircular.json`
- [ ] `results/tables/META_bulkonly_sensitivity_summary.json`   (Data Availability named file)
- [ ] `results/tables/P6_target_plausibility.json`             (Data Availability named file)
- [ ] `results/tables/_R4_nerveinjury_only_meta.csv`           (Data Availability named file)
- [ ] `results/tables/_R4_targetset_bootstrap.csv`             (Data Availability named file)

## C. Scripts (must add)

- [ ] `scripts/p7_build_supplementary_v14.py`
- [ ] `scripts/p7_consistency_gate.py`
- [ ] `scripts/p7_renumber_refs.py`          (now points at `_v15_source.md`)
- [ ] `scripts/p7_round4_supplementary.py`
- [ ] `scripts/p7_targetset_bootstrap.py`
- [ ] `scripts/p7b_translation_noncircular.py`
- [ ] `scripts/p7c_nerveinjury_only_meta.py`

## D. Updated documents (must overwrite)

- [ ] `README.md`
- [ ] `CITATION.cff`                          (title synced to manuscript in v1.5)
- [ ] `.gitignore`                           (added internal-doc exclusions in v1.5)
- [ ] `reports/MVP_ScientificReports_submission.md`
- [ ] `reports/MVP_ScientificReports_supplementary.md`
- [ ] `reports/MVP_ScientificReports_cover_letter.md`
- [ ] `reports/MVP_ScientificReports_reporting_summary.md`
- [ ] `reports/_v14_source.md`
- [ ] `reports/_v15_source.md`               (new v1.5 source)

---

## E. Already present (no action needed) — spot check

- [x] `LICENSE`
- [x] `results/tables/META_DRG_axis_stouffer.csv`
- [x] `results/tables/P3_geneset_stats.csv`
- [x] `results/tables/P3_hub_genes.csv`
