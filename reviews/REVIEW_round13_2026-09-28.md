# Round 13 integration report — MVP PLOS ONE resubmission

**Date:** 2026-09-28
**Manuscript version produced:** v1.4.0 (commit + tag `v1.4.0`)
**Panel:** A1 (domain / pain neuroscience), A2 (study design & statistics). A3 (code/reproducibility) and A4 (journal compliance) were *not* run as dedicated panels this round; their lane-items were treated as cross-cutting and checked by the orchestrator (see below).
**Panel verdict:** A1 → MAJOR REVISION; A2 → MAJOR REVISION.
**Net outcome of this round:** every submission-blocking and major item was either a genuine defect (fixed by re-analysis or re-run) or a wording/disclosure gap (closed). One A1 factual claim (F3, CACNA2D1) was an independent **misread** of the data and was *not* adopted; the substantive reporting point behind it was already implemented.

---

## 1. What Round 13 actually found (verified, not assumed)

The two panel reviewers read the manuscript under enforced independence (no prior-round files, no reviews/). Their arithmetic spot-checks were, with one exception, correct. The findings cluster as:

- **T0-1 (A2, submission-blocking).** `p2_deg_meta.py` built the GSE265957 translatome Z from `sign(mRNA_log2FC) · Φ⁻¹(pvalue_final/2)` — i.e. the *direction* of a gene's mRNA layer attached to the *significance* of its translation-efficiency (TE) layer. The two layers disagree in ~90 % of TE-significant genes, so ~11 % of the meta weighting (and two of six "direction votes") could be sign-flipped. Re-running with the sign taken from the same estimand as the p-value collapses the core from **4,055 → 2,750** genes (Jaccard 0.337) and `meta_FDR < 0.05` from **6,869 → 6,558**; 7 hubs change `in_meta_core`. Every downstream number that descends from the core is conditional on this estimand. **This is the one item that, if left unfixed, makes the primary gene-level result non-reproducible as reported.**
- **T1-1 (A2, major).** GSE278227 is a *within-animal paired* design (ipsilateral vs contralateral DRG from the same 14 rats → 28 libraries, 14 animals), never disclosed. The manuscript presented it as "n = 28" independent samples and as one of "the two genuinely independent cross-animal nerve-injury folds", and it carries the entire "nerve-injury-enriched" LODO conclusion (AUC 1.000).
- **T1-2 (A2, major).** The "leakage-controlled LODO" AUCs are computed on the within-fold **union** of the three selectors (140–169 features), not on the published ≥2/3 consensus rule (35 genes). The honest-evaluation number therefore bounds the selection procedure, not the 35-hub classifier.
- **T1-3 (A2, major — real code bug).** `p3_ml_leakage_controlled.py` standardised the held-out test fold with its *own* `StandardScaler` (`fit_transform(Xte…)`) instead of the scaler fit on the training fold — preprocessing adaptation to test data.
- **T1-4 / T1-5, F1–F14, T2-x.** a mix of bulk-overlap decomposition, EPV statement, lesion-class disclosure, title/abstract hedge, reference order, IL/CL expansion, snRNA Sham/SNI pooling, Chen erratum, human-layer scoping, and several moderate statistical caveats (bootstrap pre-screen fixity, "reproducibly recovered" overstatement, 32/35 convergence-not-independent, DeLong misnomer, small-n Welch, etc.).

---

## 2. Independent re-checks performed by the orchestrator (trust-but-verify)

| Check | Result | Action |
|---|---|---|
| T0-1 core count from regenerated `META_DRG_axis_stouffer.csv` | **core = 2,750; meta_FDR<0.05 = 6,558** — exactly matches A2's independent recomputation | Re-confirmed the fix is a genuine re-run, not a relabel. `p2_deg_meta.py` now takes sign **and** p-value from `log2FC_TE_final`. |
| A1 F3 CACNA2D1 numbers (reviewer claimed 6/6, meta_Z 7.96, FDR 5.95e-13) | **Reviewer misread.** CSV gives CACNA2D1: K=6, meta_Z 7.088, meta_FDR 2.32e-10, **4/6 up** (the two Xtail translatome timepoints are *down*: lfc −0.159, −0.009). | Reviewer's numbers **rejected**; manuscript's "4/6, +7.09, 2.3e-10" is correct and retained. The reporting-omission point behind F3 was already implemented (CACNA2D1 reported prominently in Results line 86 and Fig. 1 legend). |
| T1-3 LODO re-run after scaler fix | AUCs **identical** (GSE278227 1.000, GSE267799 0.677, GSE241361 DRG/SC 1.000, GSE212311 1.000); only `n_selected` shifted to 140–169. Complete separation yields 1.000 regardless of scaling; the incision fold's 0.677 is robust. | Code fix + CSV regeneration both applied; AUCs verified unchanged → no manuscript number needed changing, but the feature-count range (140–169) was synchronised. |
| A1's remaining verified table (F1 lesion-class, F8 GSE267799 n, F10 ADRA2A wording, F11 Chen erratum, F12 reference order) | All matched the source files. | Confirmed and retained. |

---

## 3. Disposition of every Round-13 finding in v1.4.0

| ID | Severity | Verdict | v1.4.0 action |
|---|---|---|---|
| **T0-1** | submission-blocking | Genuine defect | **Fixed by re-analysis** (sign↔p-value from same Xtail estimand). Core 2,750; meta_FDR<0.05 6,558. All descendant numbers updated. |
| **T1-1** | major | Genuine gap | Disclosed in Methods (line 150: "paired within-animal, n = 14 per side") **and reconciled** in Results (line 64) and Fig. 2 legend (line 305): GSE278227 is a within-animal discrimination, not comparable to the between-animal incision fold; only GSE212311 is a genuinely cross-animal fold. |
| **T1-2** | major | Genuine gap | Results (line 64) now states the leakage-controlled AUCs use the within-fold union of selectors, not the published ≥2/3 consensus. |
| **T1-3** | major (real bug) | Genuine bug | Code fixed (scaler fit on train, applied to test) **and** `P3_lodo_auc_ci_leakage_controlled.csv` regenerated; AUCs verified unchanged. |
| **T1-4** | major | Genuine | Bulk-overlap decomposition reported as primary: strict 1,737/2,750 = 63.2 %, relaxed 2,454/2,750 = 89.2 %; 42.1 % strict four-way rate made explicit. |
| **T1-5** | major | Genuine | Conclusions/Results EPV statement corrected: "≤2 for the four ChEMBL-annotated positive controls … ADRA2A 14.4". |
| **F1** | major | Genuine gap | Lesion-class (non-axotomy SMIR) disclosed in Limitations (136), Conclusions (140) and Results (58): the translation test is non-informative, not negative. |
| **F2** | major | Genuine gap | Results (64): "nerve-injury specificity" leak replaced by "cross-dataset generalisation within nerve-injury models … no nerve-injury specificity". |
| **F3** | major | **Reviewer misread** | CACNA2D1 numbers (4/6, 7.09, 2.3e-10) are correct per CSV; reviewer's 6/6 rejected. Reporting of CACNA2D1 as the gabapentinoid target already done (86, 302). |
| **F4** | moderate | Genuine gap | "resident microglia vs infiltrating macrophages" → DRG-resident vs recruited macrophages (Results 48, Discussion 122, Limitations 136). |
| **F5** | moderate | Partial | Surgical-procedure contrast disclosed (70); follow-up interval added ("not stated in the GSE158825 deposition"). |
| **F6** | moderate | Genuine gap | Abstract (18) carries the hedge: "'Conserved' denotes recurrence in direction across five studies, not stability of membership". |
| **F7** | moderate | Genuine gap | Abstract (18): "confirmed" → "recapitulated" + resolution-floor caveat. |
| **F8** | moderate | Genuine gap | Methods (158): GSE267799 analysed contrast = SMIR DRG only, n = 12 vs 8 (not 60/48). |
| **F9** | moderate | T1-1-driven | Fig. 2 legend (305) reconciled with the within-animal disclosure. |
| **F10** | minor | Genuine gap | Table 3a (98): ADRA2A cell reworded to "descending noradrenergic and peripheral/DRG α2A components; the present signal is DRG-level". |
| **F11** | minor | Genuine gap | Reference 38: Chen erratum appended (Cell Rep 38:110308, 2022). |
| **F12** | minor | Genuine gap | References are monotonic 1–40 (Yu 2020 at #26 in order). |
| **F13** | minor | Genuine gap | IL/CL expanded at first use (150). |
| **F14** | minor | Genuine gap | snRNA Sham/SNI pooling stated (171–172). |
| **T2-2** | moderate | Genuine gap | Bootstrap pre-screen fixity note added (66): Top-800 + λ.1se held fixed; 72 libraries = 49 animals, resampled as libraries. |
| **T2-3** | moderate | Genuine gap | "reproducibly recovered" → "partially stable, structurally-tractable subset" with P=0.000 / Jaccard 0.304 (66). |
| **T2-7** | moderate | Genuine gap | "91 % overlap" → "32/35 (91 %) … not independent corroboration" (124). |
| T2-1, T2-4, T2-5, T2-6, T2-8, T2-9 | moderate | Genuine, partially addressed | Resolution-floor caveat (T2-1/F7) and "DeLong"→"bootstrap percentile" (T2-6) done in-body/legend; T2-4 (within-set correlation), T2-5 (Knapp–Hartung), T2-8 (multivariate registry BH), T2-9 (small-n Welch) acknowledged as limitations / left as sensitivity notes. These are disclosed as caveats; full method extensions (CAMERA, K–H) are **deferred** to a follow-up revision and flagged for Round 14. |

---

## 4. Honesty notes (what was a real bug vs. a relabel)

- **T0-1** was a *real, submission-blocking* bug: the previous core (4,055) and all numbers descending from it were computed on a sign/p-value mismatch. v1.4.0 re-ran the meta-analysis; the new 2,750/6,558 are the genuine, reproducible figures.
- **T1-3** was a *real* preprocessing bug; the fix is in code and the CSV was regenerated, but the AUCs happen to be invariant to it (complete separation / robust incision fold), so no headline number changed. That invariance was verified, not assumed.
- **F3** (A1) was a *reviewer error*: the claimed 6/6 / FDR 5.95e-13 does not exist in the data. Adopting it would have *introduced* a fabrication. The manuscript's 4/6 / 2.3e-10 is correct.

## 5. Forward plan (Round 14)

Round 14 should run the full four-panel review (A1–A4) on v1.4.0, with particular attention to: (i) whether the T0-1 re-analysis and T1-1/T1-2/T1-3 disclosures are now sufficient for a minor-revision / accept call; (ii) the deferred T2 method extensions (T2-4 CAMERA, T2-5 Knapp–Hartung) — whether a reviewer will require them or accept them as stated limitations; (iii) A4 journal-compliance pass on the rebuilt submission pack (docx figure embedding, abstract ≤300 words [297], display items ≤8 [5F+3T], title ≤20 words).

## 6. Release status

- v1.4.0 committed and tagged `v1.4.0`; pushed to `origin` (main) and the tag.
- Push **verified** by `git ls-remote` (tag `v1.4.0` and `main` both resolve on the remote) — not assumed.
- Authoritative gate `p7_consistency_gate.py`: **0 failure(s), 0 warning(s), 47 check(s) passed**.
- Submission pack rebuilt: `Manuscript.docx`, `Supporting_Information.docx`, `Cover_Letter.docx`, `STROBE_Checklist.docx` (all five figures embedded at 350 DPI).
