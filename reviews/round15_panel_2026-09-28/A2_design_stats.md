# A2 — Study Design & Statistics Review (Round 15, independent)

**Manuscript:** MVP PLOS ONE submission v1.5.0 (commit a5c610a)
**Reviewer role:** A2 — Study Design & Statistics
**Independence:** Judged solely from the manuscript, supplementary, `scripts/`, and the product CSV/JSON files listed in the brief. No prior-round review files were read.
**Verdict:** **MINOR REVISION** — the statistical methodology is sound, honestly framed, and fully reproducible; the prior real bug (feature/label resampling-index mismatch) is confirmed fixed. Only minor wording/limitation items remain.

---

## 1. Independent recomputations (from raw product files)

I recomputed the headline statistics directly from `results/tables/` and compared to the manuscript/supplementary text.

| Statistic | Source file | Recomputed | Manuscript states | Match |
|---|---|---|---|---|
| median I² (whole-genome, all genes) | `_R4_random_effects_meta.csv` (n=16,552) | **41.77% → 41.8%** | 41.8% | ✅ |
| median τ² | same | **0.2664 → 0.266** | 0.266 | ✅ |
| RE core (FDR_RE<0.05 & consistency≥0.8) | same | **508** | 508 | ✅ |
| FE core (meta_FDR<0.05 & consistency≥0.8) | `META_DRG_axis_stouffer.csv` | **2,750** | 2,750 | ✅ |
| RE retention of FE core | both | **508/2750 = 18.5%** | 18.5% | ✅ |
| % genes I²>50 | same | **43.9%** | 43.9% | ✅ |
| % genes τ²>0 | same | **69.7%** | 69.7% | ✅ |
| genes tested | `META_DRG_axis_stouffer.csv` | **16,552** | 16,552 | ✅ |
| meta FDR<0.05 | same | **6,558** | 6,558 | ✅ |
| strict non-circular stratum | `_R4_nerveinjury_only_summary.json` → `NI_FDR05_AND_NIcons>=0.8` | **1,660/3,830 = 43.34% → 43.3%** | 43.3% | ✅ |
| non-circular background | same → `all_measured` | **6,772/14,390 = 47.06% → 47.1%** | 47.1% | ✅ |
| non-circular depletion perm_p | same | **0.00019996 → 0.0002** | 0.0002 | ✅ |
| risk difference (strong vs background) | same | **−3.7 pp** | −3.7 pp | ✅ |
| 26/35 hubs in meta-core | `P3_hub_genes.csv` (in_meta_core True) | **26** | 26/35 | ✅ |
| 7/35 hubs FDR_RE<0.05 | `_R4_translation_noncircular.json` (`hubs_FDR_RE_lt05`) | **7** | 7/35 | ✅ |
| 5/35 full 3-method consensus | `P3_hub_genes.csv` (n_methods=3) | **5** | 5/35 | ✅ |
| hub bootstrap: SPRR1A/ATF3 | `P3_hub_bootstrap.csv` | **1.00 / 0.935** | 1.00 / 0.94 | ✅ |
| hub bootstrap range | same | **0.14–1.00 (14.0–100.0%)** | 14.0–100.0% | ✅ |
| targetset bootstrap | `_R4_targetset_bootstrap.json` | size median 43, Jaccard 0.304, elig mean 8.70, P(≥3)=1.000, P(≥5)=0.990 | matches | ✅ |

**Conclusion:** every audited headline number reconciles exactly with the product files. No staleness or mismatch found between text, tables, and code.

---

## 2. Focus-item assessment

### (1) Stouffer meta: FE primary, RE sensitivity — **SOUND**
- FE weighting `w = √(n_case·n_ctrl/(n_case+n_ctrl))` is algebraically the inverse-variance weight for the standardized effect `d_i = Z_i/w_i` (Var(d_i) = 1/w_i²). This is *more* correct than the naive √n Stouffer weight and is not degenerate (the manuscript addresses this explicitly).
- RE (DerSimonian–Laird) is implemented exactly as written: `Q = Σ w_i²(d_i−d_FE)²`, `C = Σw_i² − Σw_i⁴/Σw_i²`, `τ² = max(0,(Q−(K−1))/C)`, `I² = max(0,(Q−(K−1))/Q)·100`, `w* = 1/(1/w_i²+τ²)`. Verified against the product CSV (median I²=41.8%, τ²=0.266).
- Choosing FE as primary and RE as a sensitivity bound is defensible: FE is the conventional summary under real-sample-size weighting, and heterogeneity-sensitivity is the explicit object of the RE/bulk-only/collapse suite. The manuscript flags FE-conditional gene-level claims throughout. No objection.
- **Residual limitation (not a blocker):** GSE265957 contributes two translatome timepoints (D4, D63) from the *same animals* as if independent. They carry ~11.4% of Σw²; de-duplicating drops Σw² by 5.7% and lengthens the FE SE by ~3%. The anti-conservatism is modest and is heavily disclosed + bounded by bulk-only (overlap 54.3%) and collapse (retention 91.4%) sensitivity analyses. Acceptable, but a truly rigorous treatment would model/correct the within-animal correlation. Flag as a residual limitation.

### (2) Circular vs non-circular translation — **EXEMPLARY / SOUND**
- The manuscript explicitly **disavows** the circular numbers (54.0% overall, 77.2% in core) as evidence of translation, correctly noting the pooled consistency filter and meta_Z both include the incision contrast.
- The valid claim is the **non-circular** construction (nerve-injury-only meta; incision used once as held-out test): 43.3% (1,660/3,830) vs 47.1% background (6,772/14,390), permutation p=0.0002 — a **significant depletion**, honestly framed as non-informative about CPSP rather than negative. The permutation null is empirical (gene re-labelling), correctly avoiding the inappropriate 50% null given the incision contrast's directional skew.
- The exploratory `_R4_translation_noncircular.csv` uses a different denominator (14,445); the manuscript openly states this is superseded by the consistent 14,390 used in `_R4_nerveinjury_only_summary.json`. Disclosed, not a hidden error.

### (3) Bootstrap hub stability — **PRIOR BUG CONFIRMED FIXED**
- `p3_hub_bootstrap.py` lines 82–92: `idx = rng.choice(...)`; `Xb = Xp[idx]`; `yb = yall[idx]`; **all three selectors (LASSO, RF, XGBoost) are fit on the same resampled `(Xbs, yb)`** (XGBoost now `fit(Xbs, yb)`, not the old `fit(Xp, yb)`). No feature/label index mismatch remains.
- Cross-checked `p7_targetset_bootstrap.py` (lines 105–117): identical correct pattern (`Xb=Xp[idx]`, `yb=yall[idx]`, all fits on `Xbs`). Also `p3_ml.py` (line 105 `lasso_fit(Xp_s[idx], yall[idx], ...)`) and `p3_ml_leakage_controlled.py` (LODO resample `b` applied to both X and y) — all aligned. **No residual mismatch anywhere in current code.**
- Bootstrap is reproducible (SEED=42) and the published `P3_hub_bootstrap.csv` matches the manuscript (SPRR1A 1.00, ATF3 0.935, range 14.0–100.0%, 2/35 ≥0.9, 9 borderline). The honest caveat (72 libraries = 49 animals resampled as libraries, not animals; fixed Top-800 pre-screen and λ held fixed) is correctly stated.

### (4) Consistency gate — **SOUND & CONSISTENT**
- Definition `meta_FDR<0.05 AND consistency≥0.8` is applied identically in code (`p2_deg_meta.py` line 202), product (`META_DRG_axis_stouffer.csv` core = 2,750), and text (2,750). 
- Threshold is correctly scaled: at K=6 → ≥5/6 agreements (0.833); at K=4 (bulk-only) → 4/4. The manuscript reports K alongside every consistency figure. No definitional drift.

### (5) Multiple-testing — **CORRECT**
- Per-contrast DEG: BH within each contrast (correct).
- Gene-level meta: BH across 16,552 genes (`meta_FDR`) — correct.
- Set-level: BH across the 18 multi-member sets on permutation p (`perm_q`); Sigma-1 (single-member) excluded from set-level inference — correct. The 4 core sets hit the 2,000-permutation resolution floor (p=0.0005) so `perm_q = 0.0022` is a valid **upper bound**, disclosed as "a single coordinated signal rather than four independent findings." Conservative and honest.
- Translation: empirical permutation null, not BH — appropriate.
- All families are separate and correctly bounded. No inflation of false positives.

### (6) Reproducibility of all claims — **PASS**
- Every number I independently recomputed matches. The pre-submission gate (`p7_consistency_gate.py`) also reconciles text↔Table 3a↔authoritative CSVs (including the Round-14 blind-spot fix). No number in the text/supplement could not be reproduced.

---

## 3. Issues

| # | Type | Item | Severity | Recommendation |
|---|---|---|---|---|
| A2-1 | **real (wording)** | Abstract: "median I² 79.1%" reads as if whole-genome heterogeneity is 79.1%, but 79.1% is the **35-hub-subset** median; the whole-genome median I² is 41.8%. Main text (line 46) is correct. | Minor | Specify in abstract "(median I² 79.1% across the 35 hubs)" so it is not misread as global heterogeneity. |
| A2-2 | **real (limitation)** | GSE265957 D4/D63 (same animals) treated as independent 6-input meta inputs (~11.4% of Σw²). | Minor | Acceptable given disclosure + sensitivity bounds; optionally note a within-animal correlation correction as future work. |
| A2-3 | **real (clarity)** | Set-level q=0.0022 is identical across the 4 core sets *by construction* (all tied at the 2000-permutation floor). | Minor | Already largely disclosed; ensure readers understand the four q-values are floor-tied, not differentially estimated. |
| A2-4 | **already-fixed** | Prior XGBoost `fit(Xp, yb)` feature/label index mismatch. | — | Confirmed fixed in `p3_hub_bootstrap.py` and `p7_targetset_bootstrap.py` (same `idx` for X and y). |
| A2-5 | **already-fixed** | Circular translation over-claim. | — | Confirmed fixed: circular numbers explicitly disavowed; non-circular depletion is the stated claim. |
| A2-6 | **reviewer-misread (none)** | — | — | No numbers were initially misread as erroneous; the 14,390 vs 14,445 denominator gap is disclosed, not a hidden defect. |

---

## 4. Bottom line
The statistical design is rigorous and the honest-negative framing (non-circular translation depletion, human-layer null, docking null) is a genuine strength, not a weakness. No major statistical flaw, no non-reproducible number, and the previously-disclosed real bug is fixed. The three minor items (A2-1/2/3) are wording/limitation clarifications that do not require re-analysis. **Recommend MINOR REVISION.**
