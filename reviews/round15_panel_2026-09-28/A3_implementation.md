# A3 — Implementation, Code-Provenance & Empirical Recomputation (Round 15)

**Reviewer:** A3 (independent; did NOT read round 13/14 reviews — judged solely from products + code)
**Manuscript:** v1.5.0 (git tag `v1.5.0` → commit `a5c610a146cdaed1f11ec40329c60248db4194fe` = HEAD)
**Target:** PLOS ONE
**Date:** 2026-09-28

---

## 1. Executive verdict

**Verdict: MINOR-REVISION.**

The manuscript's analytical code and the authoritative product files are *internally consistent* and every key statistic I independently recomputed from the raw products matches the text. The three prior bugs flagged for re-checking are either fixed or mitigated. The only defects are (i) a stale version string in a **derived self-audit document** (`compliance_check.md` still says v1.3.0 while the manuscript says v1.5.0), (ii) a latent gate-design weakness in `p7_consistency_gate.py`'s `chk()` that could let a future product/manuscript drift pass silently, and (iii) a stale committed gate log. None affect the submitted manuscript itself.

A "gate all green" claim is NOT taken on faith here: I re-ran the current gates (all pass) **and** recomputed the headline numbers directly from the CSV/JSON. The gates pass *because* the numbers are correct.

---

## 2. Prior-bug re-audit (a)/(b)/(c)

### (a) XGBoost `fit(Xp, yb)` feature/label resampling-index mismatch — **FIXED**
`scripts/p3_ml.py:70-79` builds `Xall, yall` via `make_xy()` where gene-expression rows and labels are appended **in lockstep** (each dataset's positive rows → label 1, negative rows → label 0). `Xp = Xall[:,[cidx[g] for g in POOL]]` is a pure *column* subset, so row order is preserved; `yall` is untouched. The XGBoost fit is `clf.XGBClassifier(...).fit(Xp, yall)` (line 116) — features and labels share the same row index by construction. The only resampling is the LASSO bootstrap (lines 102-105): `idx = rng.choice(len(yall),...)` and **both** `Xp_s[idx]` and `yall[idx]` are indexed by the *same* `idx` (line 105), so no misalignment. No `yb` variable exists anywhere in the ML scripts. Bug absent in current code.

`scripts/p3_ml_leakage_controlled.py:114` similarly fits `XGBClassifier(...).fit(Xtr, ytr)` with no resampling of labels. Clean.

### (b) Gate reading WRONG source CSV (Stouffer instead of bulk-only) — **FIXED**
- `scripts/gate_consistency.py:46`: `meta = rd("META_bulkonly_meta.csv")` — reads the **bulk-only** file for the SCN-FDR checks, which is correct because the manuscript §"SCN-channel directions" explicitly states Table 1b bulk meta_Z/FDR come from "the four bulk contrasts" (manuscript L322). The SCN gate (`gate_consistency.py:50-63`) asserts SCN9A/10A/11A meta_Z∈[-5,-2] and FDR∈(0.001,0.05]; these match `META_bulkonly_meta.csv` (verified in §3).
- `scripts/p7_consistency_gate.py:145` reads `META_DRG_axis_stouffer.csv` **only** for the *primary* (6-contrast) core — which is the correct source for the primary core; it reads `_R4_random_effects_meta.csv` for the RE core (line 150) and `META_bulkonly_sensitivity_summary.json` for bulk-only sensitivity (line 155). No SCN check in p7 uses the wrong file. Bug fixed.

### (c) Gate expectations hardcoded to stale numbers — **PARTIALLY addressed (residual blind spot)**
The `chk()` function (`p7_consistency_gate.py:138-143`) computes `expect` dynamically from the product, **but only asserts that the hardcoded `needle` literal is present in the manuscript text** — it never compares `expect` to `needle`. So the summary-number checks (core, RE core, I², τ², etc.) would still PASS if the *product* drifted while the manuscript text kept the old literal, provided the literal string is still present. This is exactly the class of failure that caused prior rounds' stale numbers.

**Mitigations present:**
- The bootstrap-derived checks (lines 182-189) build `needle` *from* the product (`f"{bt[...]:.2f}"`), so those are genuinely dynamic.
- **[4b] block (lines 220-261)** does real cell-by-cell reconciliation: it parses Table 3a from the manuscript and compares `meta_Z`, `meta_FDR`, `consistency`, `FDR_RE`, `n_holo_PDB` of every target against `META_DRG_axis_stouffer.csv` / `_R4_random_effects_meta.csv` / `P6_target_selection.csv` with tolerances. It passed **10/10 targets**.
- I re-ran the current gates and all pass (§4), confirming the literals happen to be correct *today*.

**Recommendation:** harden `chk()` to `assert abs(computed-expect_as_float) < tol` against the literal, so a future drift is caught. This is the one genuine gate blind spot remaining.

---

## 3. Independent recomputation of key statistics (from raw products)

All recomputations use `results/tables/` authoritative files only.

| # | Statistic (manuscript claim) | Recomputed from product | Match? |
|---|---|---|---|
| 1 | Strict non-circular stratum **1660/3830 = 43.3%** vs **47.1%** background, **p = 0.0002** | `_R4_nerveinjury_only_summary.json`: `NI_FDR05_AND_NIcons>=0.8` k=1660/n=3830 → 0.4334; `all_measured` rate=0.4706; perm_p=0.00019996 | **YES** |
| 2 | Four core gene sets **BH q = 0.0022** | `_R4_geneset_setlevel_bh.csv` (fixed scale): Neuroinflammation/Complement/Mitochondria_OXPHOS/DAM_microglia `perm_q` = 0.0022489 each → 0.0022 | **YES** |
| 3 | **median I² = 41.8%**; **median τ² = 0.266** | `_R4_random_effects_meta.csv` (16,552 rows): median I² = 41.7707; median τ² = 0.2664 | **YES** |
| 4 | **core = 2,750** (meta_FDR<0.05 AND consistency≥0.8) | same file: `sum(meta_FDR<0.05 & consistency≥0.8)` = 2750 | **YES** |
| 5 | **26/35** hubs in meta-core; **7/35** RE-significant | `P3_hub_genes.csv` `in_meta_core=True` = 26; cross-check vs meta: meta_FDR<0.05 & consistency≥0.8 = 26; `FDR_RE<0.05` = 7 (SPRR1A, GALNS, SRRM4, FLRT3, TNIK, CRISP3, LNP1) | **YES** |
| 6 | SCN bulk meta_Z/FDR (Table 1b): SCN9A −2.92/0.011, SCN10A −3.03/0.008, SCN11A −3.41/0.003, SCN8A −4.92/1.0e-5 | `META_bulkonly_meta.csv`: −2.9247/0.01078, −3.0337/0.00795, −3.4080/0.00264, −4.9236/1.009e-5 | **YES** |
| 7 | RE core 508 (18.5% of FE core) | `(_R4_random_effects_meta.csv FDR_RE<0.05 & consistency≥0.8).sum()` = 508 | **YES** |
| 8 | genes tested 16,552; meta_FDR<0.05 = 6,558 | `META_DRG_axis_stouffer.csv` len=16552; `(meta_FDR<0.05).sum()`=6558 | **YES** |

Per-contrast SCN lfc in Table 1b also match `META_bulkonly_meta.csv` lfc columns exactly (SCN9A: +0.61/−0.07/−0.29/−2.71). **Partial verification note:** the *per-contrast Z* magnitudes in Table 1b (e.g. GSE278227 Z −4.46) were not independently re-derived from the raw per-study DEG CSVs in this review (gene-id column naming and the exact GSE278227 contrast sub-file feeding the meta were not resolved); their *signs* are consistent with the verified lfc, and the summary bulk meta_Z/FDR are verified. This is a disclosure, not a discrepancy.

**Conclusion:** the manuscript's headline numbers are reproducible from the products. No number in the text that I checked is fabricated or stale.

---

## 4. Gate re-run (authoritative current status)

Re-ran the current gate scripts against the current working tree (the committed `scripts/_gate_out.txt` is **stale** — it predates the v1.5.0 sweep and shows pre-fix numbers such as 6,869 meta-FDR, 1,008 RE core, 0.232 τ²; it must not be trusted):

- `p7_consistency_gate.py` → **RESULT: 0 failure(s), 0 warning(s), 49 check(s) passed**; Table 3a 10/10 reconcile.
- `gate_consistency.py` → **PASS: 57 FAIL: 0**.
- `gate_word.py` → **WORD GATE: ALL PASS** (abstract now ≤300 words; 5 fig + 3 tab; all figures ≥300 DPI).

So "gates green" is correct *for the current files* — and, importantly, my §3 recomputations confirm the numbers behind the green are right.

---

## 5. Data availability, version, phantom-Zenodo audit

- **git tag `v1.5.0` exists** and resolves to `a5c610a...` = HEAD (verified via `git rev-list`/`git show-ref`). Matches the stated review version. Remote GitHub release status is not network-verifiable in this sandbox, but the local tag is present and the DA statement is internally consistent with it.
- **DA statement (manuscript L284-287):** cites the *public GitHub repo at v1.5.0*, lists the enumerated product files (incl. `META_bulkonly_meta.csv`, `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_meta.csv`), and states "no Zenodo snapshot has been deposited … available from the versioned GitHub release, not on request." **Honest, no phantom DOI.** ✔
- **No `10.5281/zenodo.XXXXXXX` placeholder** anywhere in `Manuscript.docx`, `Cover_Letter.docx`, or `Supporting_Information.docx` (verified by text extraction). The deferred Zenodo archive is described only as a future post-acceptance option. ✔
- **Version-block inconsistency (REAL, minor):** `reports/MVP_PLOSONE_compliance_check.md` still says **v1.3.0** at lines 22 and 74 ("Public GitHub repo (v1.3.0 …)", "cites the versioned GitHub release (v1.3.0)"), while the manuscript and cover letter correctly say **v1.5.0** (12 occurrences). The gates do **not** cover this derived document, so this slipped through. Fix: bump both to v1.5.0. (Does not affect the submitted manuscript, but a reviewer cross-reading the compliance self-audit would see a version mismatch.)

---

## 6. Docx figure embedding & text-layer consistency

- `Manuscript.docx` embeds **5 PNG figures** (word/media/image1–5.png), all 350 DPI (≥300 PLOS requirement). `Supporting_Information.docx` has 0 media (tables only — expected). ✔
- Text-layer extraction of `Manuscript.docx` confirms presence of: 2,750 / 16,552 / 6,558 / 43.3% / 47.1% / 0.0002 / 0.0022 / 41.8 / 0.266 / 26/35 / 7/35 / v1.5.0 / SCN8A 1.0e-5. **No `v1.3.0`, no `zenodo` placeholder.** The docx text layer is consistent with `MVP_PLOSONE_submission.md`. ✔
- Build script `scripts/build_sr_submission_pack.py` embeds the PNGs from `submission_pack/*.png`; the embedded figures and numbers match the source md.

---

## 7. Code–manuscript narrative alignment (selected methods)

- **Resampling / index alignment** (§2, ML): verified in §2(a) — aligned.
- **Meta FE/RE:** manuscript describes Stouffer FE (w = √(n_case·n_ctrl/(n_case+n_ctrl))) and DerSimonian–Laird RE. Products contain `Z_FE`/`p_FE` and `Z_RE`/`p_RE`/`FDR_RE`/`tau2`/`I2` columns; recomputed I²/τ² match. ✔
- **Translation test (non-circular):** `_R4_translation_noncircular.csv`/`json` and `_R4_nerveinjury_only_*` implement the strict (meta-core, consistency≥0.8, non-circular pooled excluded) stratum; the 1660/3830 result reconciles (§3 #1). The "circularity inflation 24.5 pp" and "non-circular risk diff −9.2 pp" in the json are consistent with the reported strata. ✔
- **Consistency gate:** `p7_consistency_gate.py` and `gate_consistency.py` both enforce the consistency≥0.8 rule; the hub `in_meta_core` flag is exactly that gate applied to `P3_hub_genes.csv`. ✔

---

## 8. Findings summary

| ID | Type | Severity | Description |
|---|---|---|---|
| F1 | Real bug (consistency) | **Minor** | `reports/MVP_PLOSONE_compliance_check.md` lines 22 & 74 still read **v1.3.0**; should be **v1.5.0**. Gates don't cover this derived doc. |
| F2 | Gate blind spot | **Minor (process)** | `p7_consistency_gate.py:138` `chk()` checks only `needle in txt`; it never compares the dynamically-computed `expect` to the literal. A future product↔manuscript drift could pass silently. Harden to assert `expect≈needle`. |
| F3 | Hygiene | **Trivial** | `scripts/_gate_out.txt` is a **stale** log (pre-v1.5.0 numbers); it would mislead anyone reading the repo's gate history. Regenerate it. |
| F4 | Disclosure | — | Per-contrast SCN Z magnitudes in Table 1b not independently re-derived from raw DEG CSVs (signs/directions and bulk summary verified). Not a discrepancy. |

**Already-fixed (verified, not a current defect):** prior bugs (a) XGBoost index mismatch, (b) wrong-source-CSV gate, (c) as hardened by the [4b] Table-3a reconciliation and dynamic bootstrap needles — all confirmed resolved in current code.

**No reviewer-misread / no fabricated numbers found.** Every headline figure I recomputed is reproducible.

---

## 9. Recommended actions for the author (minor-revision)

1. `compliance_check.md`: replace the two `v1.3.0` strings with `v1.5.0` (F1).
2. `p7_consistency_gate.py` `chk()`: add `assert abs(float(expect)-float(needle))<tol` (or equivalent) so the dynamic expectation is actually enforced (F2).
3. Regenerate `scripts/_gate_out.txt` after the above so the committed log reflects current green status (F3).
4. (Optional) Add a one-line gate assertion that `compliance_check.md` / `SUBMISSION_MANIFEST.md` version == the manuscript version, to close the version-block blind spot.

The manuscript (`MVP_PLOSONE_submission.md` + `Manuscript.docx`), supplementary, cover letter, and data-availability statement are **correct, reproducible, and submission-ready** once the derived-doc version string is fixed.
