# Round-5 Independent Review — Consolidated Editor Report

**Manuscript:** *Scientific Reports* submission — "Conserved nerve-injury-associated transcriptional response …: non-predictive incision translation and an honest repurposing null" (CPSP DRG–spinal-axis + FDA repurposing virtual screen), v1.4.
**Review date:** 2026-09-21.
**Editor:** independent consolidation (小团), per `independent-review-panel` skill.
**Panel:** A1 domain · A2 design/statistics · A3 provenance/recompute · A4 venue/reporting (4 expert files in `reviews/round5_2026-09-21/`).

---

## 1. Independence statement

Mechanism: each expert was forbidden from reading any prior-round artefact (`REVIEW_round*.md`, `RESPONSE_round*.md`, `REVISION*.md`, the `round4_2026-09-20/` folder, `SUBMISSION_MANIFEST.md`, `GITHUB_PUSH_LIST_v1.4.md`, `README.md`, `GITHUB_DEPOSIT_SOP.md`, other reviewers' files). They reviewed the v1.4 text as a first submission and recomputed numbers from raw source CSV/JSON.

Evidence the discipline worked (and where it paid off):
- **A1 (domain) independently re-hit the ADRA2A headline tension** that a prior round had also flagged — but A1 reached it fresh from reading Table 3b/S4 vs the abstract, not from the prior report. This is the diagnostic signature the method is designed to surface.
- **A3 (provenance) reported a false positive** (abstract "contains a citation") that the editor caught on verification (the `²` is the I² heterogeneity statistic, not a reference). This shows the editor-verification gate is doing its job: a reviewer's finding was demoted, not forwarded.
- **A2 (design) reported the non-circular count "not reproducible"** — editor verification showed the number (2,266/4,899) is fully reproducible from `_R4_nerveinjury_only_summary.json` (stratum `NI_FDR05_AND_NIcons>=0.8`); A2 had looked at the wrong file. Demoted to a traceability-clarity fix.

---

## 2. Verdict table

| Expert | Layer | Severity verdict | Basis |
|---|---|---|---|
| A1 | Domain | **Major (narrow)** | Headline honest-null contradicted by ADRA2A size-independent q=0.0025; OXPHOS FE-only over-statement; missing must-cite literature |
| A2 | Design/Stats | **Minor** | All statistics reproduce exactly; only a source-file traceability gap + an uncorrected post-hoc LR family |
| A3 | Provenance | **Minor** | 9/10 headline numbers reconcile; 1 false-positive (abstract citation) |
| A4 | Venue | **Major (narrow)** | Abstract word count ≥200 (hard-fail); Data Availability claim currently false; CITATION.cff title mismatch |

**Distribution:** 2 × narrow-Major (both wording/metadata, no new analysis), 2 × Minor. **No conclusion-invalidating defect.** Recommended handling: **Minor revision** — every item is fixable in one pass without new computation; two items carry desk-reject risk if submitted unaddressed (abstract length, Data Availability).

> Editor note: v1.4 was itself a major-revision response to Round-4. Round-5 finds the *science* intact and the *previous* internal contradictions (ACVR1 0.172, OXPHOS polarity, miRNA 253/328, spinal 16/20, docking 10-of-17) all resolved. What remains is headline-precision, format, and one deposit-action.

---

## 3. Cross-verification table (manuscript claim vs independently recomputed)

| # | Location | Manuscript claims | Recomputed (editor/agent) | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | Core signature | 4,055 / 16,552 | 16,552→6,869→4,055 | A3 | ✅ match |
| 2 | Non-circular translation | 2,266/4,899 = 46.3%, perm p=0.14 | JSON `NI_FDR05_AND_NIcons>=0.8`: 2,266/4,899, rate 0.4625, perm_p 0.1396 | **Editor** | ✅ match (source = JSON, not the CSV A2 read) |
| 3 | Background | 6,779/14,390 = 47.1% | 6,779/14,390 = 0.4711 | A3/Editor | ✅ match |
| 4 | RE core | 1,008 = 24.9% of 4,055 | exact; RE-core ⊆ FE-core (0 flipped) | A2 | ✅ match |
| 5 | τ² / I² | 0.232 / 38.8%; 41.9% I²>50% | exact from raw 16,552-row CSV | A2/A3 | ✅ match |
| 6 | OXPHOS bulk | 72.2% down (frac_up 0.2778) | `META_bulkonly_sensitivity_summary.json` 0.2778 | A1/A3 | ✅ match |
| 7 | OXPHOS set-level BH | FE q=0.020 / RE q=0.31 | recomputed 0.0202 / 0.3103 | A2 | ✅ match (honestly reported) |
| 8 | ACVR1 size-indep | p=0.584 | `P6_BH_correction.csv` & confounder CSV both 0.584; old 0.172 purged | A3 | ✅ match |
| 9 | **ADRA2A size-indep** | abstract: "no size-independent enrichment for any of 10" | source `P6_BH_correction.csv`: ADRA2A size-indep **p=0.0005, BH q=0.0025** | **Editor** | ⚠️ **data significant vs headline "none"** — see T1-1 |
| 10 | miRNA | 328 pairs / 253 distinct | 3,511/752/328 pairs / 253 distinct | A3 | ✅ match |
| 11 | Spinal localisation | 20 localisable (15 NotLocalisable) | 15+20=35; 7 confident | A3 | ✅ match |
| 12 | Docking | 9/17 hubs + ADRA2A; TFE3 not docked | source confirms | A3 | ✅ match |
| 13 | References | 24, first-citation order | 24, ascending order in body | A3 | ✅ match |
| 14 | **Abstract length** | — | 209 words (Nature limit 200) | **Editor** | ⚠️ **over limit** — see T0-1 |
| 15 | **Data Availability** | "repo already contains all processed data" | `figures/` gitignored; 5 JSONs + p7 scripts untracked | A4/Editor | ⚠️ **false at current state** — see T0-2 |

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion/acceptance-blocking (must fix before submission)
- **T0-1 (Abstract over length).** Nature/*Scientific Reports* abstract ≤ 200 words; recomputed count = **209** (even counting hyphenated compounds as single words). Borderline-to-over. *Fix:* trim ~15–25 words (e.g. compress the miRNA/spatial sentences). **Desk-reject risk if unaddressed.** (A4 + editor-verified)
- **T0-2 (Data Availability false).** Manuscript states the GitHub repo "already contains all processed data" and names 5 files; in the current local repo `figures/` is **gitignored** (5 PNGs never committed) and the 5 named JSON/CSV + `p7_targetset_bootstrap.py`/`p3_hub_bootstrap.py` are **untracked/uncommitted**. The claim does not hold if submitted today. *Fix:* push everything per `submission_pack/GITHUB_PUSH_LIST_v1.4.md` (A–G groups) before submitting, OR soften the wording to "data will be made available upon acceptance / deposited at submission." **Desk-reject risk.** (A4 + editor-confirmed; consistent with prior round's blocking item)

### Tier 1 — analyses/clarity that border on contradiction (must reword; no new compute except one registry line)
- **T1-1 (ADRA2A headline vs data — editor-verified worst claim).** Abstract (line 14) and the honest-null framing say "no size-independent enrichment for any of 10 tractable targets," but the source shows **ADRA2A size-independent p=0.0005, BH q=0.0025** (significant). The manuscript resolves this correctly in Methods (line 142) and Discussion (line 105/107) by requiring a target to clear *both* the raw/full-library filter *and* the size-independent filter, and ADRA2A fails the full-library AUC (0.532, p=0.118 NS) → "inconclusive, not a clean null." But the **abstract's blanket "no size-independent enrichment for any of 10" is imprecise** because ADRA2A's size-independent channel IS significant. *Fix:* reword the abstract to mirror Discussion line 105 — *"no candidate target cleared both the raw/full-library and the size-independent (MW-adjusted) enrichment filters"* — removing the absolute "for any of 10 tractable targets." This aligns headline with the (honest, correct) two-filter logic already in the body. (A1 + editor-verified)
- **T1-2 (Multiple-testing registry incomplete).** The multivariate physicochemical logistic-regression likelihood-ratio p-values (AXL 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4; S4) are a 5-test family but are **not listed in the Methods multiple-testing registry** (line 145 lists raw + size-independent BH across 5 targets, not the LR family) and are not BH-corrected. *Fix:* add the LR family to the registry sentence, or explicitly state it is a post-hoc/descriptive control not counted among corrected inferential tests (consistent with how composite-ranking p-values are already excluded). (A2)

### Tier 2 — wording / scope / literature
- **T2-1 (OXPHOS over-stated in Discussion).** Discussion line 101 says OXPHOS suppression is "consistent with … energy-metabolism dysfunction," but OXPHOS did **not** survive random-effects (q=0.31, FE-only). The sentence scopes it to "fixed-effect analysis" but the surrounding prose reads as a confirmed component. *Fix:* add "fixed-effect only; this did not survive random-effects correction (q=0.31)" so the FE-only status is unmistakable. (A1)
- **T2-2 (Missing must-cite literature).** Costigan et al. 2002 (classic DRG injury transcriptome), Schafer et al. 2012 (C1q complement pruning in retinogeniculate, the canonical complement-mechanism citation), and a current DAM-in-neuropathy primary should be cited where DAM/complement is claimed. *Fix:* add ≤3 citations. (A1)
- **T2-3 (Title "conserved" nuance).** "Conserved" holds at the *programme/pathway* level (neuroinflammation-DAM-complement↑/OXPHOS↓) but only 24.9% of genes survive random-effects. *Fix:* acceptable as-is, but the abstract already hedges ("core membership is heterogeneity-sensitive"); ensure the Conclusion does not re-imply gene-level conservation. (A1)
- **T2-4 (CDHR5 / annotation outliers).** A1 flags CDHR5 (intestinal epithelial cadherin) as biologically implausible as a DRG hub. The manuscript already flags it (line 70) as an annotation outlier "pending orthogonal confirmation." **Stands up** — no change needed; keep as-is. (A1)
- **T2-5 (SCN8A/Nav1.6 literature tension).** A1 notes the manuscript hedges the SCN direction inversion but could cite the contrasting Nav1.6-upregulation primary more prominently. Already partially handled (line 40). Minor.

### Tier 3 — format / metadata / traceability
- **T3-1 (CITATION.cff title mismatch).** `CITATION.cff` title = "Multi-dataset target lock-in and structure-based drug repurposing for chronic postsurgical pain" vs manuscript title. *Fix:* sync the cff title to the manuscript title (single source of truth). (A4 + editor-verified)
- **T3-2 (Non-circular source pointer).** The text should point readers to the definitive non-circular number's file. 2,266/4,899 lives in `_R4_nerveinjury_only_summary.json` (stratum `NI_FDR05_AND_NIcons>=0.8`); the CSV `_R4_translation_noncircular.csv` holds the circular/semi-corrected rows (2,318/4,306). *Fix:* cite the JSON stratum explicitly so a reader regenerates the exact number. (A2, demoted)
- **T3-3 (Refs in submission_pack internal docs).** `submission_pack/GITHUB_PUSH_LIST_v1.4.md` and `SUBMISSION_MANIFEST.md` must stay out of the public repo. *Fix:* ensure they are gitignored or removed before push. (A4)
- **T3-4 (Abstract I² not a citation).** Confirmed non-issue — the `²` in the abstract is the I² statistic. No action. (A3 false positive, editor-demoted)

---

## 5. Consensus / complementarity / disagreement

**Consensus (hit by ≥2 independents):**
- The v1.4 *science* is sound; all headline statistics reproduce exactly (RE meta, set-level BH, target-set bootstrap, NI-only translation, ACVR1 0.584, OXPHOS 72.2% down, miRNA, docking 9/17).
- The "honest null" framing is the manuscript's real contribution and is defensible *if* the headline is tightened (T1-1).
- Deposit/Data-Availability honesty is the top acceptance risk (T0-2).

**Complementarity (each caught what others couldn't):**
- A1 caught the ADRA2A headline-vs-data tension (domain reading of Table 3b vs abstract).
- A2 caught the uncorrected post-hoc LR family and the source-file traceability gap (design reading).
- A3 confirmed 9/10 numbers reconcile and purged stale values (provenance).
- A4 caught abstract word count and CITATION.cff mismatch (venue reading).

**Disagreement (adjudicated):**
- **A3 "abstract contains a citation" vs editor:** A3 read the I² superscript as a reference. Editor verification: the abstract has no reference marker; the `²` is I² heterogeneity. **Adopted editor verdict — non-issue (false positive).** A3's self-limited scope ("I only scanned for superscripts") does not cover the design/statistics reading; the stricter editor reading wins.
- **A2 "2,266/4,899 not reproducible" vs editor:** A2 read the wrong CSV. Editor verification from the JSON confirms exact reproducibility. **Adopted editor verdict — demote to T3-2 traceability clarity.** The number is correct; only the file pointer needs fixing.
- **Severity of ADRA2A (A1 Major vs A2/A3 silent):** A1 returned Major (headline contradiction); A2/A3 did not flag it. Adopt the **stricter verdict (T1-1)**: a reviewer reading only the abstract sees "no size-independent enrichment for any of 10" while Table 3b shows ADRA2A q=0.0025 — this is the exact "headline stands, caveat buried" P0 pattern. Fix is wording-only, so it does not escalate the recommendation, but it must be fixed.

---

## 6. Priority must-fix list

**DESK-REJECT flags:** T0-1 (abstract >200 words), T0-2 (Data Availability false).

**Must add analysis vs must reword split:**
- *Must reword (no new compute):* T0-1, T1-1, T2-1, T2-3, T3-1, T3-3.
- *Must add a statement/registry line (no new compute):* T1-2 (add LR family to multiple-testing registry or label post-hoc), T2-2 (add citations), T3-2 (cite JSON stratum).
- *Must act (deposit):* T0-2 (push repo per GITHUB_PUSH_LIST_v1.4.md).
- *No action:* T2-4 (CDHR5 already flagged), T3-4 (I² false positive), T2-5 (minor).

None of the must-fix items requires re-running the pipeline. The previous Round-4 four new computations (RE meta, set-level BH, non-circular translation, target-set bootstrap) all **reproduce exactly** and need no revision.

---

## 7. What stands up (do NOT change)

- Random-effects DL meta: FE core 4,055 → RE core 1,008 (24.9%); median τ²=0.232, I²=38.8%; RE-core ⊆ FE-core (real shrinkage, not weight artefact). **Keep as primary sensitivity.**
- set-level BH: Neuroinf/DAM/Complement q=0.003 (FE); OXPHOS q=0.020 (FE) honestly reported as q=0.31 (RE). **Keep.**
- Non-circular translation: 46.3% vs 47.1% background, −0.9 pp, perm p=0.14. **Keep** — robust to universe choice (46.2% either way).
- Target-set bootstrap: Jaccard 0.026, restores 0.79/17, P(≥3)=0.04. **Keep** — supports "dockability, not statistical stability" framing.
- ACVR1 size-indep p=0.584 (old 0.172 fully purged). **Keep.**
- Docking 9/17 + ADRA2A (non-hub) + TFE3 not docked. **Keep.**
- CDHR5 flagged as annotation outlier. **Keep.**
- ML/LODO: three [1.0,1.0] folds correctly flagged non-informative; cross-animal mean excludes same-animal folds. **Keep.**

---

## 8. Recommended handling path

**Path A (recommended): Minor revision, same article type.** All 15 issues are wording/format/metadata/one deposit action; no new computation. Estimated one focused pass. Submit only after T0-1 and T0-2 are closed (desk-reject risk otherwise).

Path B (downgrade) — **not recommended**: the strongest finding (honest null at library scale + non-circular translation) is a genuine methodological contribution; downgrading would waste it.
Path C (wording-only) — **not viable as stated** because T0-2 is a deposit action, not wording; but T0-2 can be closed by pushing, after which the manuscript is wording-only.

---

## 9. Process lessons (what gates could not catch)

- **A gate passing at 100% is evidence about arithmetic, not design.** All four v1.4 gates were green, yet A1 still found the ADRA2A headline-vs-data tension and A4 found the abstract word count. Design/venue defects are invisible to arithmetic gates.
- **The gene-universe trap is now a standing risk.** A2's "not reproducible" was caused by mixing the 14,445 universe (circular CSV) with the 14,390 universe (NI-only JSON). Recommend a gate assertion: every translation-percentage claim must cite the *exact* source file + stratum, and a script should regenerate each from that one file. Extends gate coverage to the design layer.
- **Headline-vs-caveat contradiction is the recurring failure mode.** Round-4 left ADRA2A's size-independent significance in Table 3b while the abstract said "no size-independent enrichment." A fresh panel caught it instantly. Recommend a gate that cross-checks every abstract "no/none/negative" claim against the corresponding table cell.
- **Deposit-metadata consistency is outside manuscript gates.** CITATION.cff title and the Data Availability claim are not checked by any manuscript gate. Recommend a deposit-gate: diff the cff title against the manuscript title, and `git ls-files` the 5 named Data-Availability files before submit.

---

*Audit trail: `reviews/round5_2026-09-21/A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`, `_PANEL_BRIEF.md`. Editor-verified worst claims: ADRA2A size-independent q (source `P6_BH_correction.csv`), non-circular 2,266/4,899 (source `_R4_nerveinjury_only_summary.json`), abstract word count (regex on rendered submission.md), CITATION.cff title, Data Availability repo state.*
