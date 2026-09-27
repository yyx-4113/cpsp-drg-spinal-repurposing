# REVIEW Round 12 — Consolidated Independent Expert Panel (v1.2.0, PLOS ONE re-submission)

**Date:** 2026-09-27
**Manuscript:** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null* (v1.2.0)
**Article type under review:** PLOS ONE Research Article (original investigation)
**Panel:** A1 Domain · A2 Design & statistics · A3 Implementation/provenance · A4 Venue/reporting
**Editor:** 小团 (consolidated; did not review as an expert, only verified and adjudicated)

---

## 1. Independence statement

**Mechanism.** Four reviewers were briefed from a shared `_PANEL_BRIEF.md` that **forbids** reading any prior round (`REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `reviews/round*_*/**`, other Round-12 siblings), the deposit SOP, the author-verification statement, the project plan, and all gate scripts/output. Each was told to treat the manuscript as a **first submission** and to recompute every number from **raw CSV/JSON**, never from the text or a gate file. Prompts were self-contained (no shared conversational memory).

**Evidence independence worked (the diagnostic signature):** several defects were hit by *different* reviewers from *different* starting points, with no knowledge of each other —
- **T0-1 (docx Table 2 header/data misalignment)** was found by **A3 (provenance)** by inspecting the built `.docx` directly. No text reviewer (A1/A2/A4) would have caught a *render* bug, because the markdown source table is correctly ordered. A3 reached it independently.
- **The "DRG–spinal axis" vs DRG-only contradiction** was flagged by **A1 (text reading)** *and* **A2 (dataset counting)** independently — A1 from the title/abstract/intro wording, A2 from noting the meta-analysis uses 5 studies (DRG-only) while the body keeps invoking a "DRG–spinal axis."
- **The K=3 mis-description** (T1-3) was caught by **A2** from the raw `META_bulkonly_meta.csv`; the editor re-verified it from scratch (see §3).
- The four reviewers' "§ Stands up" lists overlap heavily (reproducibility of all headline numbers, honest-null framing, no-fabricated-DOI, embedded 350-DPI figures) — confirming they converged on what is *correct*, not on a shared prior.

This is the pattern the panel method is designed to produce: design/display defects surface only when layers are independent.

---

## 2. Verdict table

| Reviewer | Layer | Recommendation | DESK-REJECT? | Headline finding |
|---|---|---|---|---|
| A1 | Domain | Major revision (wording/framing) | No | DRG-only title reframe not followed in body; "not CPSP-specific" over-stated from p=0.14; OXPHOS limb RE-fragile; missing must-cite α2δ mechanism |
| A2 | Design/statistics | Major revision (honesty tightening) | No | K=3 mis-described as 3-of-4 concordant (actually 3-of-4 *available*); nerve-injury-enriched claim rests on 1 dataset w/ degenerate CI; EPV critique inconsistent; FE-primary over-emphasised |
| A3 | Implementation/provenance | **Major revision — BLOCKER** | No (but blocks submission until fixed) | **docx Table 2 header/data column misalignment (CRITICAL display bug)**; all 8 headline recomputations reconcile; no fabricated DOI |
| A4 | Venue/reporting | Minor revision (artefact fixes) | No | compliance_check.md has wrong numbers (abstract 180→256, title 166→143); STROBE Item 16 mislabels ADRA2A AUC; STROBE line-citations stale; GitHub-only data availability = soft query risk |

**Distribution:** 0 reject / 1 submission-blocking build defect (fixable, not scientific) / 3 major-revision (honesty+framing) / 1 minor (artefact). **No reviewer recommended rejection.** The manuscript is honest, evidence-appropriate, and within PLOS ONE's explicit null-result welcome — it needs tightening, not restructuring of the science.

---

## 3. Cross-verification table (manuscript claim vs independently recomputed)

Editor re-ran the two most severe claims with a fresh script (raw sources only). All other rows below were recomputed by the named reviewer from `results/tables/*.csv|json`.

| # | Location | Manuscript claim | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | Table 2 (docx) | headers: Hub/Methods/In meta core/LASSO/RF Gini/SHAP | body col2 = lasso_freq (0.96), col6 = Yes/No → **headers shifted +1 from col2** | **Editor (own script)** | **DEFECT (T0-1)** |
| 2 | Results overlap | 1,707 pure 4/4 + 495 K=3 | overlap=2,202; K=4:1,707, K=3:495; genes w/ 4 available & exactly 3/4 agreeing = **0**; 495 K=3 have consistency=1.0 (all 3 available agree) | **Editor (own script)** | **MIS-WORDED (T1-3)** |
| 3 | Core | 4,055 (FE) / 1,008 (RE, 24.9%) | 4,055 / 1,008 / 24.9% | A2, A3 | ✅ |
| 4 | Bulk-only / strict / relaxed overlap | 2,512 / 2,202 / 3,587 (88.5%) | 2,512 / 2,202 / 3,587 / 88.5% | A2, A3 | ✅ |
| 5 | Outside relaxed | 313 (211+102) + 468 | 313⊂468 (468 = 313 + 155); integers correct, connective wording off | A2, A3 | ✅ numbers / ⚠ wording (T2-3) |
| 6 | Gene-set q | q=0.003 = BH permutation upper bound | perm_p floor 1/2001=0.00049975 → BH q 0.0029985; genuine upper bound | A2 | ✅ |
| 7 | Non-circular translation | 46.2% vs 47.1%, p=0.14 | 2,266/4,899=46.25%, p=0.1396; background 47.11% | A2 | ✅ |
| 8 | GSE265957 | 11.4% same-animal weight, "marginally anti-conservative" | share 11.41% correct; true SE shrinkage ≈6% (not 11%) | A2 | ✅ share / ⚠ framing (T2-4) |
| 9 | Bootstrap | 2/35 ≥0.9 (max 100%) | 2/35 (SPRR1A 1.0, ATF3 0.94); max 1.0 | A3 | ✅ (brief's "max 15.5%" was wrong; manuscript correct) |
| 10 | Docking null | ADRA2A full-library AUC 0.532 p=0.118 NS; ion-channel class undockable | 0.532 / 0.118; 3,085 drugs; ion-channel list confirmed | A3 | ✅ |
| 11 | Figures | 5 embedded @350 DPI | 5 inline_shapes; PNG dpi 350.012 | A3, A4 | ✅ |
| 12 | DOIs | 37/37 verified | 10/10 spot-check resolve (Crossref); compliance claim dated Round 9 | A3, A4 | ✅ sample / ⚠ re-verify (T3-7) |

**Net:** every *headline integer* reproduces exactly. The defects are (a) one docx render bug, (b) a cluster of *honesty-wording* inaccuracies that gates cannot catch (they are prose, not number mismatches), and (c) stale compliance/STROBE artefacts.

---

## 4. Graded consolidated issue list

### TIER 0 — submission-blocking (must fix before submit)
- **T0-1 (A3, editor-verified).** `Manuscript.docx` Table 2 (35-hub table) header row is shifted +1 column from the body from column 2 onward: `In meta core` sits over the LASSO-frequency values, `LASSO freq` over RF-Gini, `RF Gini` over SHAP, and `SHAP |abs|` over the Yes/No `in_meta_core` membership. A reader sees "In meta core = 0.96" and "SHAP |abs| = Yes". Values are correct and recoverable (32 Yes / 3 No match `P3_hub_genes.csv`); only the labels are misaligned. **Fix:** rebuild Table 2 from a single consistent column order (Header `Hub | Methods (n/3) | In meta core | LASSO freq | RF Gini | SHAP |abs|` must map to body `symbol | n_methods | in_meta_core(Yes/No) | lasso_freq | rf_gini | shap_meanabs`). Add a CI assertion: `header[2]=="In meta core"` AND `set(body col2) ⊆ {Yes,No}`. The root cause is the build script pulling body cells from the raw CSV column order while stamping the markdown header — audit `scripts/build_sr_submission_pack.py` `build_table2`.

### TIER 1 — analyses to add / material rewording (affects interpretation)
- **T1-1 (A1-5, A2-7).** "DRG–spinal axis" / "peripheral–central axis" appears in Abstract L14, Intro L32 & L36, Author Summary L26, Discussion L122 — but the meta-analysis is DRG-only (5 studies, 6 contrasts, all DRG). Spinal is localisation only. **Fix:** replace with "DRG-centred nerve-injury response with spinal-cord localisation"; add a Methods sentence: "No spinal-cord bulk transcriptome entered the Stouffer meta-analysis; spinal datasets (GSE241361 spinal, GSE328175, GSE246288, GSE325938) were used for hub localisation only."
- **T1-2 (A1-6, A2-8).** GSE241361 *spinal cord* is in the 72-sample ML pool that defines the 35 hubs (Methods L159; Fig.2 legend L293) — contradicting "spinal = localisation only," and it re-imports the same-animal non-independence (GSE241361 DRG+spinal are same animals). **Fix (option a, cleaner):** remove GSE241361 spinal from the ML pool, re-derive hubs DRG-only, re-run docking eligibility on the revised set. **Fix (option b):** if retained, drop the "DRG-only" absolutism and state spinal expression contributed to hub convergence. Editor recommends (a).
- **T1-3 (A2-1, editor-verified).** "1,707 genes concordant across all four bulk contrasts (pure 4/4) and 495 concordant in exactly 3 of 4 (K=3)" implies the 495 had 4 available contrasts with 3 agreeing. **They did not** — 0 genes have 4 available with exactly 3/4 agreement; the 495 were measured in only **3 of 4 bulk datasets** (4th absent) and all 3 available agree (consistency=1.0). **Fix:** "the remaining 495 were measured in only three of the four bulk datasets (the fourth absent for that gene, e.g. below detection/QC) and were concordant in those three; the 'not strict 4/4' component reflects reduced measurement coverage (lower K), not directional disagreement among four available contrasts."
- **T1-4 (A2-4, A2-6).** The "candidate nerve-injury-enriched" LODO claim is foregrounded as "four of five folds reached AUC 1.000," but the cross-animal support rests essentially on **one** dataset (GSE278227, n=28); GSE212311 (n=6) is at the exact-test floor (p=0.10) and the two GSE241361 folds are same-animal. AUC=1.0 carries degenerate DeLong CI [1.0,1.0] (zero estimable precision) yet is quoted as support. **Fix:** attach the precision caveat to every AUC=1.0 quote; state the conclusion rests on a single n=28 fold from a classifier selecting 139–164 features from ~44 training samples (EPV≈0.15), reported as exploratory/hypothesis-generating, not a precision estimate.
- **T1-5 (A2-5).** The docking multivariate physicochemical control dismisses ACVR1 (EPV≈1.3) but presents AXL (EPV≈1.9) and TNIK (EPV≈1.4) LR tests (p=2.6e-5, 7.3e-5) as supportive validation — internally inconsistent EPV weighting. **Fix:** report EPV for all five ChEMBL-annotated targets in S4 Panel A and apply the same "EPV≈1–2, descriptive" caveat to AXL/TNIK, or soften the Discussion to "descriptive, not validation."
- **T1-6 (A1-8).** Conclusions L136 states the axis "is a nerve-injury-associated … response rather than a CPSP-specific pathway" as an affirmative, but it rests on a non-significant translation test (p=0.14, underpowered). **Fix:** "on available evidence the nerve-injury signature is **not established as** CPSP-specific — the translation test to the sole incision arm was non-significant (p=0.14) and underpowered, and the inference is provisional and does not demonstrate either CPSP-specificity or its absence."
- **T1-7 (A1-7).** No analysed dataset captures *established* CPSP (>3 months); the incision arm is acute-to-subacute. **Fix:** add "No analysed dataset captures established chronic postsurgical pain (>3 months); the incision arm models acute-to-subacute postoperative pain as a translational proxy, so the CPSP-specificity question is necessarily provisional."

### TIER 2 — wording / framing
- **T2-1 (A1-2).** "neuroimmune–*metabolic* programme" over-states the OXPHOS limb, which fails random effects (q=0.31, hub median I²=72.8%). **Fix:** "neuroimmune programme with a fixed-effect-only, random-effects-fragile metabolic (OXPHOS-down) limb (q=0.31 under RE)."
- **T2-2 (A1-3).** "DAM-like/microglial" over-assigns a bulk DRG signal to microglia; in DRG the post-injury immune infiltrate is largely infiltrating macrophages. **Fix:** "DAM-like neuroimmune programme of myeloid (resident microglia and/or infiltrating macrophage) origin" until single-cell deconvolution attributes it.
- **T2-3 (A2-2).** "the remaining 468 fall outside even the relaxed ≥3/4 overlap" reads as additive (313+468). 313⊂468 (468 = 313 + 155). **Fix:** "A total of 468 genes fall outside even the relaxed overlap, comprising those 313 plus a further 155 bulk-significant but below the 3/4 consistency gate."
- **T2-4 (A2-3).** "11.4% same-animal weight" implies 11.4% redundancy; true SE shrinkage ≈6% (de-dup Σw² 17.52→16.52). **Fix:** state both the 11.4% share and the ~6% SE lengthening.
- **T2-5 (A2-9).** FE-primary emphasis despite only 24.9% persists under RE. **Fix:** qualify first mention — "a 4,055-gene core emerged under fixed effects (primary, heterogeneity-sensitive estimate; FE-conditional)."
- **T2-6 (A2-7).** "12 GEO datasets (four nerve-injury, one incision)" implies 12 inform the core. **Fix:** "5 transcriptomic studies (6 contrasts: four nerve-injury, one incision) constitute the meta-analysis, plus 7 single-cell/spatial/miRNA datasets for localisation and the human plasma layer."
- **T2-7 (A1-11/12).** Missing must-cite: α2δ-1/gabapentinoid DRG mechanism; DRG myeloid neuroimmune sentinel. **Fix:** add (verify DOIs before insertion — A1 flagged these as memory-based, not verified).
- **T2-8 (A1-9/10).** The ion-channel honest-null is *silent* (not *negative*) on the only validated non-opioid analgesic classes. **Fix:** promote the exclusion to the head of Limitations; state the null is silent on gabapentinoids/NaV1.8 by construction.
- **T2-9 (A1-14).** "MAPK14, AXL and TFE3 have the strongest prior biological rationale" edges toward soft prioritisation while TFE3 was never docked and only 4/10 retain RE significance. **Fix:** rephrase with the instability caveat.

### TIER 3 — format / artefact
- **T3-1 (A4-6.1).** STROBE Item 16 mislabels ADRA2A full-library AUC **0.532** as "Tier-1" (Tier-1 = 0.618). **Fix:** "full-library AUC 0.532, p=0.118 NS; Tier-1 subset AUC 0.618 — the breadth flip is the point."
- **T3-2 (A4-2.1/4.2).** compliance_check.md states abstract = 180 words (actual **256**) and title = 166 chars (actual **143**). Both still ≤ limits, but the compliance doc is wrong. **Fix:** correct to 256 / 143.
- **T3-3 (A4-4.3).** compliance_check §4 instructs to replace a `10.5281/zenodo.XXXXXXX` placeholder that **does not exist** in the manuscript (manuscript states "no Zenodo snapshot deposited"). **Fix:** replace §4 with an accurate optional-deposit note; do not introduce a placeholder.
- **T3-4 (A4-2.3).** compliance_check credits "gate_word ALL PASS" for the 350-DPI claim, but a docx stores no DPI — the gate cannot measure it. **Fix:** evidence = PNG metadata (350.012 DPI, verified).
- **T3-5 (A4-6.2).** STROBE line-citations are systematically offset from the final manuscript (e.g., Item 8 "line 129" for the 12 accessions; Item 22 "line 211" for Funding; Item 5 "line 164" for Ethics). **Fix:** re-anchor to section names (layout-stable).
- **T3-6 (A4-6.3).** STROBE 2007 is a stretch for an in-silico reanalysis. **Fix:** add one sentence justifying STROBE-by-analogy (the single human cohort GSE158825) and that N/A items are primary-deposition delegations.
- **T3-7 (A4-4.5).** 37/37 DOI verification is dated Round 9. **Fix:** re-run a Crossref batch on all 37 before submission; record date.
- **T3-8 (A3-Q2).** A3 could not reach GitHub from the sandbox to confirm the v1.2.0 tag exists at the MANIFEST commit. **Fix (pre-submission):** externally confirm `git ls-remote` shows `refs/tags/v1.2.0` at the cited commit (the editor confirmed this in the v1.2.0 publish step; re-confirm at submit time).
- **T3-9 (A4-2.6).** GitHub-only data availability (no Zenodo) is usually accepted but may draw an editor query. **Recommendation:** deposit a versioned Zenodo/figshare archive and cite its real DOI — *deferred per author instruction (Zenodo on hold)*; if staying GitHub-only, add one sentence confirming the v1.2.0 release tag is immutable.

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (all four):** the manuscript's core numbers are fully reproducible; the "honest null" + ion-channel exclusion is transparent (not hidden); no fabricated DOI; figures embedded at 350 DPI; AI disclosure present and specific; the 45.7% "translatome-dependence" is correctly reframed as a counting artefact in both manuscript and STROBE; positioning as a negative/null study aligns with PLOS ONE's scope. These are the paper's real contribution and they stand.

**Complementarity (each layer caught a distinct category):** A3 = build/render defect (T0-1) invisible to text reviewers; A2 = numeric honesty mis-descriptions (T1-3, T1-4, T1-5, T2-4/5/6); A1 = domain/framing gaps (T1-1, T1-2, T1-6, T1-7, T2-1/2/7/8/9); A4 = stale compliance/STROBE artefacts (T3-1…6). No overlap in *type* of defect — exactly the multi-layer coverage the method buys.

**Disagreement:** none material. A4's "GitHub-only = soft query risk" is a recommendation, not a contradiction. A1's OXPHOS demotion (T2-1) and A2's RE-fragility note (T2-5) are complementary, not conflicting. No reviewer disputed another's severity.

---

## 6. Priority must-fix list

**BLOCKER (fix before submission):**
- **T0-1** — docx Table 2 column misalignment. Build-script fix + CI assertion. (Not a scientific retraction; a render bug.)

**Must-reword (honesty, Tier 1):** T1-1, T1-2, T1-3, T1-4, T1-5, T1-6, T1-7.
**Must-reword (Tier 2):** T2-1…T2-9.
**Must-fix artefacts (Tier 3):** T3-1…T3-9 (T3-8/T3-9 deferred/verify-only).

**DESK-REJECT flags:** **None.** T0-1 is submission-blocking but trivially fixable (rebuild docx) and does not invalidate any result. No scientific claim is retracted; the recommended path is resubmit-as-same-article-type with revisions.

**"Must add analysis" vs "must reword" split:** only T1-2 (optional re-derivation of hubs DRG-only) is a potential *re-analysis*; everything else is reword/reframe or artefact correction. No new experiment or new dataset is required.

---

## 7. What stands up (do NOT change)

1. All headline integers: 4,055 / 2,512 / 2,202 / 3,587 (88.5%) / 313 / 468 / 1,008 (RE) / 16,552 tested / 6,869 significant / collapse 4,294·3,707·91.4%.
2. q=0.003 is a genuine BH permutation-resolution **upper bound**, not a point estimate.
3. The non-circular translation test (46.2% vs 47.1%, p=0.14) is honestly executed; the circular 69.5% is correctly disowned.
4. The honest docking null is well-supported (no target clears both filters; ADRA2A AUC 0.532 p=0.118; ion-channel class explicitly undockable and never screened).
5. Bootstrap hub stability is framed honestly (max 100%, only 2/35 ≥0.9; remainder need prospective validation).
6. Figures embedded (5) at 350 DPI; AI disclosure specific (names Claude/Anthropic); no fabricated DOI; competing-interests and ethics statements correct and non-contradictory.
7. The DRG-only title reframe is the *right* move — the body just needs to follow through (T1-1/T1-2).

---

## 8. Recommended handling path

**Path A — Revise and resubmit as the same article type (Research Article).** Recommended. The science is sound and honestly framed; the fixes are (i) one build bug (T0-1), (ii) DRG-only consistency (T1-1/T1-2), (iii) statistical-honesty tightening (T1-3…T1-7, T2-1…T2-6), (iv) artefact corrections (T3-1…T3-7). No desk-reject-level blocker, no new data.

**Path B — Downgrade article type.** Not indicated; the work is a full research article.

**Path C — Wording-only.** Not viable: T0-1 is a real defect and T1 items materially affect interpretation (they change how a reader weights the nerve-injury-enriched and CPSP-specific claims).

---

## 9. Process lessons (what gates could NOT catch, and how to extend coverage)

The four submission gates (`p7_consistency_gate.py`, `verify_sr_docx.py`, `gate_consistency.py`, `gate_word.py`) passed at v1.2.0, yet this panel found a submission-blocking defect and a cluster of honesty mis-wordings. **Gates verify arithmetic/self-consistency, not design or render correctness.** Specific gaps:

1. **Render bug (T0-1).** `verify_sr_docx.py` counted "5 tables, 35-row hub table present" but never checked that *header labels align with body columns*. **New assertion:** for the hub table, assert `header[2]=="In meta core"` AND `set(body_col2_values) ⊆ {Yes,No}` AND `body_col3` is float. Also a **markdown→docx round-trip check**: render each markdown table and assert the docx cell order equals the markdown cell order (catches the +1 shift at build time).
2. **Descriptive mis-wording (T1-3).** "K=3 = 3-of-4 concordant" is prose, not a number mismatch — gates cannot see it. **New artefact:** a `results/tables/_bulk_K3_interpretation.md` that states explicitly "K=3 ⇒ 3 of 4 bulk datasets measured (4th absent); all 3 available agree," and the manuscript must quote that file's wording.
3. **Stale compliance/STROBE artefacts (T3-1…T3-5).** `compliance_check.md` and `STROBE_checklist.md` drifted from the manuscript after the T2/T3 edits (abstract 256 vs claimed 180; ADRA2A AUC mislabel; line-citations offset). **New gate:** re-derive the compliance_check numbers (abstract word count, title char count, ADRA2A AUC values) from the *current* manuscript at gate time, and grep the STROBE checklist for any `10.5281/zenodo.XXXXXXX` that does not exist in the manuscript.
4. **Single-source-of-truth for the title** (T1-1): grep the exact title string across all five artefacts; the panel found the body still says "DRG–spinal axis" while the title says DRG-only. A gate asserting "title string present and identical in manuscript/cover/CITATION" would not catch *body* contradictions — so add a body-grep for the forbidden phrase "DRG–spinal axis"/"peripheral–central axis" and fail if found.

These four new assertions would have caught T0-1, T1-3, T3-1, T3-2, T3-3, T3-5 at the gate layer — extending coverage from "arithmetic" to "design + render + artefact freshness."

---

*Prepared by the editor (小团) from four independent, enforced-independence reviews. The two most severe findings (T0-1, T1-3) were re-verified by the editor from raw sources before consolidation. No prior-review file was read by any reviewer or by the editor during consolidation.*
