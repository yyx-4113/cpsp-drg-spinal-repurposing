# REVIEW ROUND 9 — Independent Multi-Expert Panel Consolidation
**Manuscript:** `reports/MVP_ScientificReports_submission.md` (283 lines)
**Target venue:** PLOS ONE (SCIE; pivot after Scientific Reports desk-reject)
**Date:** 2026-09-26
**Editor:** panel coordinator; all expert files in `reviews/round9_2026-09-26/`.

---

## 1. Independence statement (mechanism + evidence it worked)

**Mechanism.** Four experts were briefed from a shared `_PANEL_BRIEF.md` that (a) forbade reading any prior review (`REVIEW_round2…round8`, `reviews/round8…`, `reviews/round9…/<siblings>`), the project memory, the conversation history, and each other's outputs; (b) required every claim to be verified from text or raw source data the expert read itself; (c) demanded recomputation of every headline number from `results/tables/` raw CSV/JSON. Each expert wrote its own file and returned only a short summary.

**Evidence independence actually worked:**
- The four experts independently converged on the *same real* residual defects from different angles — the Zenodo "mirroring" wording (A3 + A4), the residual "ScientificReports" branding (A3 + A4), and the display-item / "8-item cap" inconsistency (A3 + A4). Clustering-on-a-real-defect is the diagnostic signature of genuine independence.
- A1 (biology) independently re-derived every SCN direction/magnitude value and found them all correct, while still surfacing genuine citation gaps (suzetrigine pivotal trial, uncited SCN10A reconciliation) — a fresh reviewer, not a rubber-stamp.
- A2 (design) independently re-derived every statistic and **caught two genuine arithmetic/consistency errors** (GSE265957 "twice the variance weight" is false; LODO "three of five degenerate CI" should be four) that no prior round had flagged at the sentence level.
- The editor re-verified the most severe claims from raw sources (see §3 and §5) rather than forwarding them.

---

## 2. Verdict table

| Expert | Layer | Overall verdict | Highest severity raised | Conclusion-invalidating? |
|---|---|---|---|---|
| **A1** | Domain (pain neurobiology) | Minor–Moderate | Tier 2 (CPSP-specific over-reach; suzetrigine/SCN citations) | No |
| **A2** | Design (meta-analysis / stats) | Moderate | Tier 1 (GSE265957 weight misstatement; LODO aggregation 2 errors; EPV double-standard) | No |
| **A3** | Implementation (provenance / recompute) | Minor (arithmetic sound) + Tier-2 consistency | Tier 1 (Zenodo "mirroring"; 46.3% vs 46.2% cross-artifact) | No |
| **A4** | Venue (PLOS ONE editor + STROBE) | Moderate (integrity cluster) | Tier 1 (Zenodo wording; stale compliance check 26≠33) | No |

**Distribution:** Tier 0 = **0**. Tier 1 = **5** (all reword/correct, no new analysis). Tier 2 = **11**. Tier 3 = **3**. **No DESK-REJECT flag is warranted by any single item**, but a *cluster* of integrity/branding items (Zenodo placeholder asserting existence, a stale compliance check whose reference count is wrong by 7 and could read as a fabricated verification artifact, and residual "ScientificReports" filenames suggesting a parallel submission) should be cleared pre-upload as an integrity bundle.

---

## 3. Cross-verification table — headline numbers & discrepancies

Every headline number below was recomputed by A3 (and, where noted, the editor) from raw sources. **All nine core headline numbers reproduce exactly.**

| # | Manuscript location | Manuscript claims | Independently recomputed | Who checked | Verdict |
|---|---|---|---|---|---|
| 1 | Results (axis) | FE core 4,055; RE core 1,008 (τ²=0.232, I²=38.8%) | 4,055 / 1,008; τ²=0.232, I²=38.8% | A3 (from `_R4_random_effects_meta.csv`) | ✅ exact |
| 2 | Results (robustness) | bulk-only 2,512; overlap 2,202/4,055 = 54.3% | 2,512; 2,202/4,055 = 54.3% | A3 | ✅ exact |
| 3 | Results (gene-set) | q=0.003 (NI/DAM/complement); OXPHOS FE q=0.020 / RE q=0.31 | 0.003 / 0.020 / 0.31 | A3, A2 | ✅ exact |
| 4 | Results (translation) | 46.3% vs 47.1%, −0.9 pp, p=0.14 | 2,266/4,899 = **0.4625** (rounds to 46.2% or 46.3%); 6,779/14,390 = 47.1%; −0.9 pp; p=0.14 | A3, A2, **editor** | ⚠️ rounding mismatch (see D1) |
| 5 | Results (ML) | leakage-controlled incision fold 0.677 [0.374,0.940]; other 4 nerve-injury folds AUC=1.000 | identical from `P3_lodo_auc_ci_leakage_controlled.csv` | A2, A3, **editor** | ✅ exact values; prose aggregation errors (see D3/D4) |
| 6 | Results (docking) | ADRA2A 0.532, p=0.118; size-indep BH q=0.0025; ΔAUC p≈0.0005 | 0.532 / 0.118 / 0.0025 / 0.0005 | A3, A2, **editor** | ✅ exact; two-filter logic consistent |
| 7 | Results (human) | p=0.51 (n=60) | p=0.51 | A3 (consistency) | ✅ (secondary check) |
| 8 | Methods (scale) | 3,085 drugs; 30,850 poses; 30,687 scored; 10 targets | 3,085; 30,850; 30,687; 10 | A3 | ✅ exact |
| 9 | Results (localisation) | 17/33 dorsal horn; Visium `present` True=33/False=2 | 17/33; `present` recompute True=33/False=2 | A3 | ✅ exact |

**Discrepancies (manuscript vs recomputed / vs its own other artifacts):**

| # | Location | Manuscript | Recomputed / other artifact | Verdict |
|---|---|---|---|---|
| D1 | L18/L58 (abstract/body) vs L220 (S6) | 46.3% | 2,266/4,899 = 0.4625 → supplementary prints **46.2%**; only 46.2% reconciles the printed −0.9 pp | ⚠️ rounding-convention mismatch (not a computational error) — **editor verified** |
| D2 | L44 | "w² = 2.00 versus 1.22–2.65 … twice the effective variance weight of a single bulk study" | GSE265957 Σw² = 2.00/17.52 = **11.4%**, comparable to GSE241361 (12.7%), **not** twice any bulk study (bulk w² range 1.50–7.00). Also compares w² (2.00) to a w-range (1.22–2.65) — unit error | ❌ **false claim — editor verified** |
| D3 | L64 | "three of the five folds have degenerate confidence intervals" | leakage-controlled file has **four** folds at [1.0,1.0] (only the incision fold has a real CI) | ❌ **wrong count — editor verified** |
| D4 | L64 | "cross-animal mean of 0.917–1.000 across three folds" | mixes non-leakage GSE267799 (0.917) with leakage values; leakage-controlled GSE267799 = 0.677, so the honest range is 0.677–1.000 | ❌ **file-mixing inconsistency — editor verified** |
| D5 | L222 | "…will be deposited … to provide a citable permanent DOI **mirroring** the GitHub release v1.0.0 (…XXXXXXX — to be minted)" | verb "mirroring" asserts existence before minting; contradicts "to be minted" | ❌ **integrity wording — editor verified** |
| D6 | `P6_breadth_chembl_power.csv` | `mw_control_verdict` = "PASS_size_independent" for AXL/TNIK | manuscript Table 3b + `P6_BH_correction.csv` correctly say FAIL (ΔAUC CI contains 0). CSV used a naive point-estimate comparison, not the significance test | ⚠️ **misleading deposited-artifact label — editor verified** |
| D7 | L88/L128 (EPV) | ACVR1 dismissed at EPV≈1 ("non-reproducible fluctuation"); AXL/TNIK "recovered signal beyond chemotype" | AXL (n_actives=13, EPV≈1.6) and TNIK (10, EPV≈1.25) sit on the same low-EPV cliff; standard not applied uniformly | ⚠️ **double standard — editor verified** |
| D8 | L232 vs L283 | "5 figures + 5 tables = 10 main display items" but only 3 tables enumerated; L283 cites an "8-item cap" | "5 tables" only true if lettered subparts (1a,1b,3a,3b) each count; PLOS ONE has no 8-item cap — it is a Scientific Reports tell | ⚠️ **display-item inconsistency — editor verified** |
| D9 | STROBE checklist L11 | "Title states 'multi-dataset in-silico meta-analysis'" | real title (L1) has **no** "meta-analysis" word | ❌ **checklist misquotes title — editor verified** |
| D10 | `MVP_PLOSONE_compliance_check.md` | "26 refs", "23/26 DOIs", Author Summary "required" | manuscript has **33** refs; Author Summary is *optional* at PLOS ONE; line citations offset (Funding "211" vs L215; Abstract "7–21" vs L12–20) | ❌ **stale/incorrect supporting doc — editor verified** |
| D11 | L225 vs L112/L126 | "no target is singled out" | ADRA2A has two dedicated paragraphs; it is the pending-grant target | ⚠️ **CI statement undercut by text — editor verified** |

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
**None.** All nine headline numbers reproduce exactly; no design defect invalidates a conclusion. The paper's three pillars (heterogeneity-sensitive axis; nerve-injury-specific LODO with non-generalising incision; honest docking null) survive.

### Tier 1 — must fix before submission (reword / correct; no new analysis)

- **T1-1 · GSE265957 "twice the variance weight" is false (A2-1, A3-2a).** `L44` mixes w² (2.00) against a w-range (1.22–2.65) and claims the translatome "contributes twice the effective variance weight of a single bulk study." Recomputed Σw² share = 11.4%, comparable to GSE241361 (12.7%), far below GSE278227 (40%) or GSE267799 (27%) — it is **not** twice any bulk study. **【Fix】** replace with: "Because the two translatome timepoints each carry weight w = 1.00, they together contribute 2.00 to Σw² (2.00/17.52 ≈ 11.4% of total variance weight), comparable to — not twice — a single midsize bulk study (GSE241361_DRG w² = 2.22, 12.7%; GSE212311 w² = 1.50, 8.6%). The two timepoints are from the same animals and are not statistically independent; their joint influence is bounded by the bulk-only (overlap 54.3%) and collapse (retention 91.4%) sensitivity analyses." *(No number changes; the double-counting concern is preserved, just stated correctly.)*

- **T1-2 · LODO "three of five degenerate CI" → four (A2-4).** `L64` (and `L151`) state "Three of the five folds have degenerate confidence intervals," but the leakage-controlled file the paper elevates has **four** folds at [1.0,1.0]; only the incision fold has an estimable CI. **【Fix】** "Four of the five leakage-controlled folds have degenerate CIs [1.0,1.0] (all AUC = 1.0 folds); only the incision fold yields an estimable CI."

- **T1-3 · LODO "cross-animal mean 0.917–1.000 across three folds" mixes files (A2-4).** The phrase blends the **non-leakage** GSE267799 value (0.917) with leakage values (1.0); the leakage-controlled GSE267799 is 0.677. **【Fix】** rewrite the aggregate from leakage-controlled values only: "Under leakage control, the four nerve-injury folds reach AUC 1.000 (the two GSE241361 folds are same-animal and excluded from the cross-animal mean). The two genuinely independent cross-animal nerve-injury folds are GSE278227 (n=28) and GSE212311 (n=6); the incision fold (GSE267799, n=20) falls to 0.677 [0.374,0.940]. The nerve-injury-specific — not universal — conclusion rests on this pattern." Drop the "0.917–1.000 across three folds" phrasing.

- **T1-4 · Zenodo "mirroring" implies existence before minting (A3-3, A4-4).** `L222` still nests a present participial "mirroring" beside the future "will be deposited … to be minted," asserting an archive that does not yet exist. **【Fix】** make the clause fully prospective: "A versioned Zenodo archive will be deposited at submission; upon acceptance it will receive a citable permanent DOI (10.5281/zenodo.XXXXXXX, to be minted) that archives the GitHub release v1.0.0. Data are not 'available on request'." (The GitHub repo is real and public, so the "available without restriction" bar is already met; this only removes the false-existence implication.)

- **T1-5 · EPV double standard for AXL/TNIK vs ACVR1 (A2-6/8).** `L88`/`L128` dismiss ACVR1 for EPV≈1 but present AXL (n_actives=13, EPV≈1.6) and TNIK (10, EPV≈1.25) as having "recovered signal beyond chemotype" without the same EPV caveat. **【Fix】** add an EPV note (to Table 3b/Supplementary S4 and Discussion): "Events-per-parameter were ACVR1 1.1, AXL 1.6, TNIK 1.3, MAPK14 2.0, ADRA2A ≈14; all ChEMBL-annotated positive controls except ADRA2A fall at EPV ≤ 2, far below the conventional ≥10, so the 'discrimination beyond chemotype' for AXL/TNIK/ACVR1 is itself tentative and the multivariate LRT is a method-capability demonstration, not target evidence." This converts the double standard into one uniform caveat and *strengthens* the honest-null thesis.

### Tier 2 — wording / clarity / consistency (reword; strengthens acceptance)

- **T2-1 · 46.3% vs 46.2% cross-artifact rounding (A3-2b).** Standardise on **46.2%** everywhere (abstract L18, body L58, cover letter): 2,266/4,899 = 0.4625, and only 46.2% reconciles the printed −0.9 pp (46.2 vs 47.1). Fix the supplementary S6 value to match if keeping 46.3% — but 46.2% is the internally consistent choice. *(Editor note: this is a rounding-convention mismatch, NOT a computational error; all underlying statistics are correct.)*
- **T2-2 · Display-item count + "8-item cap" (A3-4, A4-8).** Reconcile L232 and L283 to one convention. Recommended: "5 figures + 3 tables (Table 1 with panels 1a/1b, Table 2, Table 3 with panels 3a/3b) = 8 enumerated main display items," and **delete the "8-item cap" phrase** (PLOS ONE imposes no such cap; "8" is a Scientific Reports fingerprint).
- **T2-3 · STROBE Item 1 title misdescription (A4-1).** Either add the design to the title ("…: a multi-dataset in-silico meta-analysis, non-predictive incision translation, and an honest repurposing null") **or** correct the checklist to "Title does not name the design; design is stated in the Abstract (L14) and metadata (L8); STROBE Item 1 satisfied via the abstract." Do not leave the false "Title states 'multi-dataset in-silico meta-analysis'" claim.
- **T2-4 · Stale compliance check (`MVP_PLOSONE_compliance_check.md`) (A4-2/3/7).** It counts "26 refs" (manuscript has 33), cites Author Summary as *required* (it is optional at PLOS ONE), and has offset line citations (Funding "211" vs L215; Abstract "7–21" vs L12–20). Regenerate against the 33-reference file; replace every "26" with "33"; re-verify the 7 added refs (27–33) for DOIs; relabel Author Summary as optional; fix line citations (or cite section headings instead of lines).
- **T2-5 · Competing Interests "no target singled out" undercut by ADRA2A emphasis (A4-5).** Soften L225 to: "ADRA2A is discussed at greater length than the other nine targets because it is the illustrative case for the two-filter rule (full-library AUC 0.532, p=0.118, fails filter 1; size-independent BH q=0.0025 passes filter 2 → inconclusive) and because the author's pending grant lists it as a candidate target; this did not affect any analytical choice, and all 10 targets were treated identically in the docking pipeline (Methods L160–162; Table 3b)."
- **T2-6 · No standalone Conclusions section (A4-6).** Add a brief `## Conclusions` (3–5 sentences) after Discussion, mirroring the abstract Conclusion (L20) — PLOS ONE's structural check expects it.
- **T2-7 · Residual "ScientificReports" branding (A3-7, A4-8).** Rename `MVP_ScientificReports_submission.md` → `MVP_PLOSONE_submission.md` and `MVP_ScientificReports_supplementary.md` → `MVP_PLOSONE_supplementary.md` (or venue-neutral); update L283 cross-reference; quarantine the ScientificReports-named cover letter / reporting summary / `_v*_source.md` / `P6_manuscript_draft.md` from the upload set; confirm the rendered docx contains no "Scientific Reports" string.
- **T2-8 · suzetrigine pivotal trial uncited (A1-2).** Add the primary phase-2/3 trial(s) and cite at L52 (ref 20 is a 2026 narrative review). E.g. the registration trial establishing suzetrigine's efficacy/approval.
- **T2-9 · SCN10A/Nav1.8 reconciliation paragraphs uncited (A1-3).** Append primary citations to the L52 sentence on Nav1.8 mRNA down-regulation in axotomized IB4+ neurons and on DRG neuronal loss / immune-glial transcript dilution after nerve injury.
- **T2-10 · "rather than CPSP-specific" over-reach in Abstract Conclusion (A1-1).** L20 is categorical ("rather than a CPSP-specific target") from a single incision arm and a non-significant p=0.14; the Discussion (L120) already hedges it as "not shown." Soften L20 to "and is not shown by this meta-analysis to be CPSP-specific, because the nerve-injury signature does not predict the single incision arm (46.3% vs 47.1% background, p=0.14)."
- **T2-11 · FE-primary justification (A2-2).** L46 asserts FE-primary / RE-sensitivity without a positive rationale aligned to the heterogeneity thesis. Add one sentence: "We report the FE core as primary because the FE combination is the conventional fixed-combination summary for real-sample-size weighting and because heterogeneity-sensitivity is itself the object of the RE/bulk-only/collapse suite; FE-conditional gene-level claims are flagged throughout." *(A3 confirmed the RE core 1,008 and τ²/I² reproduce exactly from `_R4_random_effects_meta.csv`, so no number is in doubt.)*

### Tier 3 — housekeeping / transparency (low risk, do at the same time)

- **T3-1 · DAM TREM2/APOE/TYROBP core membership (A1-5).** State whether the canonical DAM hallmark genes are themselves in the up-regulated meta core (fill from `META_DRG_axis_stouffer.csv`), to justify the "DAM-like" qualifier quantitatively.
- **T3-2 · Target-set bootstrap aggregates not deposited (A2-5).** `_R4_targetset_bootstrap.csv` holds only per-hub marginal frequencies; deposit the per-resample recovered-set lists (or a summary giving set size, Jaccard, P(≥k)) so "median size 6 (IQR 5–8)", "median Jaccard 0.026", "P(≥3 of 17)=0.040" are reproducible.
- **T3-3 · Ethics — name the original IRB approval (A4-9).** If retrievable from the GSE158825 deposition, cite the IRB committee + approval number at L170 to remove ambiguity; otherwise state explicitly that the original approval is documented in the deposition and no further approval was required.

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (≥2 experts, independent):**
- Zenodo "mirroring" wording asserts existence before minting (A3 + A4).
- Residual "ScientificReports" branding (A3 + A4).
- Display-item / "8-item cap" inconsistency (A3 + A4).
- All nine core headline numbers reproduce exactly (A2, A3; editor-confirmed).
- SCN directions/magnitudes correct (A1, A3).
- Abstract compliant (~191 words, correct headings, no citations) (A1, A4).
- AI-use disclosure specific (names Claude) in both manuscript and cover letter (A4).

**Complementarity (each layer caught what others could not):**
- **A1** caught the suzetrigine pivotal-trial citation gap and the uncited SCN10A reconciliation — domain-level literature completeness.
- **A2** caught the GSE265957 false "twice-weight" claim and the two LODO aggregation errors — statistics-layer, recomputation-driven.
- **A3** caught the 46.3/46.2 rounding mismatch, the display-item count, the Zenodo wording, and confirmed citation completeness (33/33).
- **A4** caught the STROBE Item-1 title misdescription, the stale compliance check (26≠33), the missing Conclusions section, and the CI/ADRA2A tension.

**Disagreement (preserved, with editor ruling):**
- **Docking CSV "PASS" for AXL/TNIK (A2-8).** A2 initially framed this as a "contradiction" with the manuscript. The editor rules it a **misleading-but-not-contradictory deposited-artifact label**: the CSV's `mw_control_verdict` uses a naive point-estimate comparison ("dock AUC > MW baseline pointwise") and calls it "PASS_size_independent," whereas the manuscript correctly uses the ΔAUC-CI significance test (CI contains 0 → FAIL). The manuscript's Table 3b is correct; only the CSV label should be relabelled (T2-4/D6). **Keep as Tier-2 artifact fix, not a Tier-1 thesis defect.**
- **RE core "not re-derivable" (A2-2).** A2 could not re-derive the 1,008 RE core from the primary Stouffer CSV. A3 **did** re-derive it (FE 4,055, RE 1,008, τ²=0.232, I²=38.8% from `_R4_random_effects_meta.csv`), so this is resolved — no defect; A2 merely lacked the file.
- **46.3% "discrepancy" (A3-2b).** Editor rules it a **rounding-convention mismatch** (0.4625 → 46.2% or 46.3%), not a computational error. Standardise to 46.2% (reconciles −0.9 pp). Downgrade severity accordingly.

---

## 6. Priority must-fix list

**Must reword / correct (no new analysis):** T1-1, T1-2, T1-3, T1-4, T1-5, T2-1, T2-2, T2-3, T2-5, T2-6, T2-7, T2-8, T2-9, T2-10, T2-11.
**Must regenerate a supporting doc:** T2-4 (compliance check against 33-ref file).
**Must add citations:** T2-8, T2-9.
**Transparency adds (recommended):** T3-1, T3-2, T3-3.

**DESK-REJECT flags:** **None** by themselves. However, treat the following as a **pre-upload integrity bundle** (any one could trigger a technical-check query): T1-4 (Zenodo false-existence wording), T2-4 (stale compliance check whose reference count is wrong by 7 and could be read as a fabricated verification artifact), and T2-7 (residual "ScientificReports" filenames suggesting parallel submission). Clear all three before upload; they are cheap.

---

## 7. What stands up (do NOT change)

- All nine headline numbers (verified by A3 and the editor).
- The non-circular translation test (46.2/47.1%, −0.9 pp, p=0.14; empirical-null reference) — recomputed exact.
- The honest docking null and the ADRA2A two-filter logic (consistent; not a hit, not a clean null).
- The structured abstract (~191 words, correct headings, no citations).
- The specific AI-use disclosure (names Claude), ethics/funding/competing-interests/author-contributions blocks.
- The LODO per-fold disclosure (now corrected for the 4-vs-3 degenerate-CI and the file-mixing once T1-2/T1-3 land).
- OXPHOS honestly scoped as fixed-effect-only (q=0.020 FE / 0.31 RE).
- DAM provenance correctly attributed to Keren-Shaul 2017 (not Schafer "developmental").
- Citation completeness (33/33 cited; refs 26/27 now present at L120).
- All six named data-availability files exist.

---

## 8. Recommended handling path

**Path C (wording-only + small additions + one doc regeneration) is viable and recommended** — this round is precision/integrity/branding polish for PLOS ONE. **Not** Path A (restructure) and **not** Path B (downgrade article type). No conclusion changes, no number changes (except the cosmetic 46.3→46.2 rounding standardisation), no new analysis is required. The only non-wording actions are: add two citation clusters (suzetrigine trial; SCN10A reconciliation), regenerate the compliance check, and rename/upload-clean the ScientificReports artifacts.

**Reframe note to the author (the skill's close):**
- **The strongest over-reach is partly your own and partly inherited.** The Abstract conclusion's categorical "rather than a CPSP-specific target" (T2-10) extends beyond a single incision arm and a non-significant p=0.14; soften it to match your own Discussion. The GSE265957 "twice the variance weight" sentence (T1-1) is a genuine misstatement you should correct — it does not weaken your real fragility argument (the bulk-only 54.3% overlap already carries that).
- **Your contribution you under-sell is the LODO nerve-injury-specificity.** Four of five folds separate nerve-injury perfectly under leakage control (T1-2/T1-3 fix the prose so this reads correctly), while the incision arm fails (0.677, CI includes chance). That is *direct, on-thesis evidence* that the axis is nerve-injury-specific rather than a universal pain signature — the paper's central claim — and it currently reads as if the classifier were weak. Lead with it.
- **Swapping emphasis converts a fragile signal into a stable structural finding** — with zero number changes, once T1-1/T1-2/T1-3/T2-10 land.

---

## 9. Process lessons (what the gates cannot catch, and new assertions)

- **A gate passing at 100% certifies arithmetic, not design or prose.** This round, the design-layer defects (GSE265957 false "twice-weight"; LODO 3-vs-4 degenerate-CI; LODO file-mixing) were *not* caught by any consistency gate — they are sentence-level accuracy issues a human recomputation finds. The value of the panel was the integrity/branding/prose layer (Zenodo wording, ScientificReports residues, stale compliance check, 46.3/46.2), which no numeric gate sees.
- **New gate assertions worth adding to `p7_consistency_gate.py`:**
  1. **Display-item self-consistency** — parse the "N figures + M tables" claim at L232 and assert the enumerated figures/tables actually count to N/M; flag the literal string "8-item cap" (Scientific Reports fingerprint) anywhere in the manuscript.
  2. **Zenodo wording** — flag the literal token "mirroring" (or "already"/"mirrors") when the DOI is the unresolved placeholder `XXXXXXX`; require fully prospective tense.
  3. **STROBE title check** — if the STROBE checklist asserts the title contains a design keyword (e.g. "meta-analysis"), assert that keyword actually appears in the manuscript title; else flag.
  4. **Reference count echo** — assert the compliance check document's reference count equals the manuscript's actual count (33); this would have caught T2-4 automatically.
- **Disclosure ≠ resolution, even for residuals.** The Round-8 T1-3 fix added future tense ("will be deposited … to be minted") but left the verb "mirroring" standing — a classic "second-occurrence staleness": the gate checked the first occurrence (presence of `XXXXXXX`) and passed, but the duplicate implication ("mirroring") went stale. **Rule:** grep every derived artifact for the *value/verb*, not just the expected location, and reduce to a single source of truth (one prospective Zenodo sentence).
- **The panel caught a *positive* under-reporting again** (LODO nerve-injury specificity) alongside the negatives — future rounds should explicitly ask: "what did the author bury that is actually their contribution?"
- **The compliance check is a verification artifact, not a certificate.** A stale check (26≠33 refs) is worse than no check because it can be read as a fabricated readiness claim. Regenerate it against the final file and treat its PASS list as advisory, not probative.
