# REVIEW ROUND 8 — Independent Multi-Expert Panel Consolidation
**Manuscript:** `reports/MVP_ScientificReports_submission.md` (283 lines)
**Target venue this round:** PLOS ONE (SCIE; the authors' pivot after Scientific Reports desk-reject)
**Date:** 2026-09-26
**Editor:** consolidated by the panel coordinator (this report); all expert files in `reviews/round8_2026-09-26/`.

---

## 1. Independence statement (mechanism + evidence it worked)

**Mechanism.** Four experts were briefed from a shared `_PANEL_BRIEF.md` that (a) forbade reading any prior review (`REVIEW_round2…round7`, `reviews/round2…round7/*`), the project memory (`.workbuddy/memory/`), the conversation history, and each other's outputs; (b) required every claim to be verified from text or raw source data the expert read themselves; (c) demanded recomputation of every headline number from `results/tables/` raw CSV/JSON. Each expert wrote its own file and returned only a short summary.

**Evidence independence actually worked:**
- The four experts converged on the *same* concrete bibliographic/integrity defects — orphaned references 26/27 and the Zenodo placeholder — from four different angles (domain, provenance, venue). That clustering-on-a-real-defect is the diagnostic signature of genuine independence, not rubber-stamping.
- The design expert (A2) independently re-derived numbers and **initially misread** the ADRA2A BH row and the LODO per-fold disclosure, proposing a contradiction and a "hiding" claim that the editor's own recomputation **demoted** (see §3, §5). A re-reviewer carrying priors would not have invented a contradiction that does not exist — A2 formed a fresh (partly erroneous) judgement, exactly what independence is supposed to produce.

---

## 2. Verdict table

| Expert | Layer | Overall verdict | Highest severity raised | Conclusion-invalidating? |
|---|---|---|---|---|
| **A1** | Domain (pain neurobiology) | Minor–Moderate | Tier 1 (Nav1.8 contradiction) | No |
| **A2** | Design (meta-analysis / stats) | Moderate as filed, **mostly demoted on editor check** | Tier 2 residual (FE-primary justification) | No |
| **A3** | Implementation (provenance / recompute) | Minor (arithmetic sound) | Tier 1 (refs 26/27; Zenodo) | No |
| **A4** | Venue (PLOS ONE editor + STROBE) | Moderate (integrity risks) | Tier 1 (refs 26/27; Zenodo; STROBE-14) | No |

**Distribution:** Tier 0 = **0**. Tier 1 = 4 (all reword/add, none require new analysis). Tier 2 = 11 (wording/clarity). Tier 3 = 4 (housekeeping). No DESK-REJECT flag is warranted by itself.

---

## 3. Cross-verification table — headline numbers

Every number below was recomputed by A3 from raw sources; the editor independently re-derived the ADRA2A and LODO values. **No numeric discrepancy was found.**

| # | Manuscript location | Manuscript claims | Independently recomputed | Who checked | Verdict |
|---|---|---|---|---|---|
| 1 | Results (axis) | FE core 4,055; RE core 1,008 (τ²=0.232, I²=38.8%) | 4,055 / 1,008; τ²=0.232, I²=38.8% | A3, editor | ✅ exact |
| 2 | Results (robustness) | bulk-only core 2,512; overlap 2,202/4,055 = 54.3% | 2,512; 2,202/4,055 = 54.3% | A3 | ✅ exact |
| 3 | Results (gene-set) | q=0.003 (neuroimmune/DAM/complement); OXPHOS FE q=0.020 / RE q=0.31 | q=0.003 / 0.020 / 0.31 | A3 | ✅ exact |
| 4 | Results (translation) | 46.3% vs 47.1%, −0.9 pp, p=0.14 | 46.3% / 47.1%, p=0.14 | A3, A2 | ✅ exact |
| 5 | Results (ML) | leakage-controlled LODO AUC 0.677 [0.374, 0.940] | 0.677 [0.374, 0.940] (incision fold); other 4 folds = 1.000 | A3, **editor** | ✅ exact; per-fold disclosure present |
| 6 | Results (docking) | ADRA2A 0.618→0.532, p=0.118; MW ΔAUC p≈0.0005 | 0.532 (p=0.118); BH_q_size_indep=0.0025; ΔAUC p=0.0005 | A3, **editor** | ✅ exact; two-filter logic consistent (see §5) |
| 7 | Results (human) | p=0.51 (n=60) | p=0.51 | A3 | ✅ exact |
| 8 | Methods (scale) | 3,085 drugs; 30,850 poses; 30,687 scored; ~3,070/target | 3,085; 30,850; 30,687; ~3,070 | A3 | ✅ exact |
| 9 | Results (localisation) | 17/33 hubs dorsal horn | 17/33 | A3 | ✅ exact |

**Editor's independent confirmation (the two "severe" A2 claims):** I read `P6_BH_correction.csv` and `P3_lodo_auc_ci_leakage_controlled.csv` directly. ADRA2A has `BH_q_raw_enrich=0.118` (NOT significant) and `AUC=0.532, p=0.118` — it **fails** the full-library enrichment filter, so it does **not** clear *both* required filters; `BH_q_size_indep=0.0025` is real but irrelevant to the two-filter null. The manuscript's "inconclusive, not a confirmed null" is therefore **internally consistent** — A2's "contradiction" is **demoted**. For LODO, the manuscript (L64) already discloses that GSE278227 (n=28) and GSE212311 (n=6) reach AUC=1.000 and the incision fold is the cross-animal floor; the leakage-controlled 0.677 is explicitly the incision translation fold. A2's "hiding perfect folds" is **demoted** — the text is transparent.

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
**None.** All nine headline numbers reproduce exactly; no design defect invalidates a conclusion.

### Tier 1 — must fix before submission (reword / small add; no new analysis)
- **T1-1 · Nav1.8-inhibitor self-contradiction (A1-F1).** `L52` states "selective Nav1.7/Nav1.8 inhibitors have repeatedly failed clinically¹⁴,¹⁵,¹⁶," but `L112` and ref 20 (Divito 2026, *suzetrigine: a novel nonopioid systemic analgesic* — a Nav1.8 inhibitor approved 2025–2026) cite suzetrigine as an existing Nav1.8 analgesic. **【Fix】** qualify L52: "prior Nav1.7/Nav1.8 clinical programmes largely failed¹⁴⁻¹⁶; however, suzetrigine (a Nav1.8 inhibitor) was approved in 2025–2026²⁰ — it acts at the channel-protein level, so the mRNA-level down-regulation observed here is not expected to predict docking affinity (see Discussion)."
- **T1-2 · Orphaned references 26 & 27 (A3-F1, A4-FA).** References 26 (Yousefpour 2025, C1q/microglia synaptic removal) and 27 (Kong 2023, Lyn-glycolysis microglia) appear in the list but are **never cited in the body**; the sequence jumps 25→28. PLOS requires every reference to be cited. **【Fix】** either (a) cite 26 where complement/C1q is discussed (Results axis / Discussion) and 27 where microglial glycolysis/metabolic reprogramming is discussed, or (b) delete both and renumber. Option (a) is preferred (both are topically on-point).
- **T1-3 · Zenodo "mirrors" statement is premature (A3-F2, A4-FB).** `L222` says "A versioned Zenodo archive … mirrors the GitHub release v1.0.0 (DOI: 10.5281/zenodo.XXXXXXX — to be minted at submission)." The DOI is a placeholder, so the "mirrors" clause asserts an archive that does not yet exist. The GitHub URL is real and public, so data availability is satisfied — but the Zenodo clause must not imply existence. **【Fix】** reword: "All data are publicly available now via the GitHub repository above. A versioned Zenodo archival DOI will be minted at submission to provide a citable permanent record; the placeholder DOI is replaced at that time." Remove "mirrors … v1.0.0" until minted.
- **T1-4 · STROBE item 14 dishonest (A4-FC).** The STROBE checklist marks item 14 (descriptive statistics for participants) "Addressed," but the manuscript contains **no participant-level descriptive statistics** for the n=60 GSE158825 human layer (only gene-level results). **【Fix】** either add a small participant-characteristics table for GSE158825 (age/sex/pain-status distribution) and cite it, or re-mark item 14 as "N/A (no individual-level participant covariates analysed; aggregate miRNA only)" with a one-line justification. Do not leave "Addressed" unbacked.

### Tier 2 — wording / clarity (reword; strengthens acceptance)
- **T2-1 · FE-primary justification (A2-F1).** The manuscript uses fixed-effects for the primary "core" (4,055) and random-effects as sensitivity (1,008). With a median I²≈39% and 41.9% of genes I²>50%, a reader expects RE as primary. This is *defensible* here (the FE-vs-RE collapse **is** the paper's heterogeneity finding), but it must be stated, not implicit. **【Fix】** add one sentence in Methods/Meta-analysis: "We report the fixed-effects consensus core as the primary signature because the paper's thesis is heterogeneity-sensitivity; the random-effects set (1,008) is the conservative primary for persistence and is reported alongside."
- **T2-2 · GSE265957 weight-range wording (A2-F2, A3-F3).** `L38` states bulk contrast weights "1.00–7.02"; recomputed bulk w² = **1.50–7.00** (1.00 is the GSE265957 *per-timepoint* value, not a bulk contrast). **【Fix】** correct to "bulk-contrast w² = 1.50–7.00; the two GSE265957 timepoints each carry w=1.00, so that study contributes ≈2× the per-study effective weight, bounded by the bulk-only and collapse sensitivity analyses."
- **T2-3 · SCN3A "most induced" uncited (A1-F2).** `L52` calls SCN3A/Nav1.3 "the channel most transcriptionally induced after injury" without a citation. **【Fix】** add a primary citation for Nav1.3 up-regulation after nerve injury.
- **T2-4 · "axotomized IB4+ neurons" imprecision (A1-F3).** IB4 binding is *lost* in axotomized DRG neurons, so "down-regulated in axotomized IB4+ neurons" is imprecise. **【Fix】** reword to "down-regulated in injured DRG neurons (IB4+ nociceptor subpopulations are themselves depleted after axotomy)," or drop the IB4 qualifier.
- **T2-5 · "DAM-like" should flag the missing Trem2/Apoe axis (A1-F4).** The set lacks the hallmark Trem2/Apoe signature of true DAM. **【Fix】** add: "Our DAM-like set is enriched for complement and microglial-activation markers but does not capture the full Trem2–Apoe axis that defines canonical DAM, so 'DAM-like' is a partial, complement-weighted overlap, not a full DAM programme."
- **T2-6 · "NOT CPSP-specific" absolute negation (A1-F5).** The boundary rests on a single underpowered incision arm (p=0.14). The paper already frames it as "non-predictive incision translation," so the Conclusion's "rather than a CPSP-specific target" is acceptable but should stay hedged. **【Fix】** keep the hedged wording; do not strengthen to a definitive negation.
- **T2-7 · Make the ADRA2A two-filter logic explicit (editor, from A2-F4 demotion).** To prevent exactly the misreading A2 made, state once, plainly: "A target clears the screen only if it passes *both* the full-library enrichment filter (ADRA2A fails: 0.532, p=0.118) and the size-independent filter (ADRA2A passes: BH q=0.0025); because it fails the first, the docking null holds and ADRA2A is 'inconclusive' — not a confirmed hit, not a clean null." (No number changes.)
- **T2-8 · STROBE item 5 too generic (A4-FD).** "Setting" marked N/A with a one-line note; add the reanalysis-specific sentence already added to the checklist file (`MVP_STROBE_checklist.md`) and ensure it is the version shipped in the pack.
- **T2-9 · STROBE item 1 title wording (A4-FE).** The checklist says the title contains "meta-analysis"; the actual title does not. **【Fix】** align the checklist item-1 description to the real title.
- **T2-10 · Supporting files still branded "ScientificReports" (A4-F?).** Several supporting/doc artifacts carry "ScientificReports" naming while submitting to PLOS ONE. **【Fix】** rename the PLOS submission pack artifacts (and any "Scientific Reports" residual text) to PLOS ONE branding before upload.
- **T2-11 · Author Summary + cover letter (A4-FH).** PLOS ONE does **not** require an "Author Summary" (that is a *PLOS Biology/Medicine/Computational Biology* item). The `Cover_Letter_PLOSONE.docx` wrongly calls it required. **【Fix】** remove/relabel Author Summary as optional, and correct the cover letter claim.

### Tier 3 — housekeeping (low risk, do at the same time)
- **T3-1 · Superseded `_R4_translation_noncircular.csv` still ships** (53.7% / −11.8 pp, older merge) in `results/tables/` although the manuscript supersedes it in text (L58). **【Fix】** move to an `_archive/` or delete; keep only the authoritative `_R4_nerveinjury_only_summary.json`.
- **T3-2 · Collapse-sensitivity headline has no source artifact.** The "collapse (5-input) = 4,294 genes; 91.4%" figure cited in the manuscript has no corresponding CSV in `results/tables/`. **【Fix】** generate `META_collapse_meta.csv` (+ summary) so the number is reproducible, or cite the script that produces it.
- **T3-3 · Visium `present` column uniformly True.** `P5_GSE325938_hub_regionalization.csv` marks `present=True` for all 35 hubs despite only 33/35 being detectable. **【Fix】** recompute `present` from actual detection; this is a data-quality cosmetic, not a conclusion change.

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (across ≥2 experts, independent):**
- All nine headline numbers reproduce exactly (A3; editor-confirmed for ADRA2A/LODO).
- References 26/27 are orphaned (A3 + A4).
- The Zenodo placeholder statement is premature (A3 + A4).
- Structured abstract is compliant (4 headings, 185 words) and STROBE version is consistently 2007 across artifacts (A4).
- AI-use disclosure is specific (names Claude) (A4).

**Complementarity (each layer caught what others could not):**
- A1 (biology) caught the Nav1.8/suzetrigine self-contradiction and the DAM/Trem2 nuance.
- A3 (provenance) caught the orphaned references and the Zenodo false-ish clause via citation-scan + data-availability read.
- A4 (venue) caught STROBE item-14 dishonesty and the PLOS-branding/Author-Summary mismatches.
- A2 (design) supplied the FE-vs-RE and GSE265957 nuances (mostly defensible on editor check, but flagged the real T2-2 w-range error).

**Disagreement (preserved, with editor ruling):**
- **ADRA2A "contradiction" (A2 vs A3/editor).** A2 read `BH_q_size_indep=0.0025` as contradicting "inconclusive." **Ruling:** A3 and the editor are correct — the docking null requires *both* filters; ADRA2A fails the full-library filter, so the null holds. Adopt the stricter *clarity* fix (T2-7), not A2's "contradiction" framing.
- **LODO "hiding perfect folds" (A2 vs manuscript/editor).** A2 implied the manuscript hides that 4/5 folds are AUC=1.0. **Ruling:** the manuscript (L64) already discloses every fold explicitly. A2 misread; demoted. (See reframe in §8 — the paper *under*-emphasizes this strength, the opposite of hiding.)
- **FE-primary (A2 vs editor).** A2 graded it as a primary-analysis failure; the editor rules it defensible given the paper's heterogeneity thesis, but a one-sentence justification (T2-1) is mandatory so a reviewer cannot misread it as an error.

---

## 6. Priority must-fix list

**Must reword (no new analysis):** T1-1, T1-3, T1-4(clause), T2-1, T2-2, T2-3, T2-4, T2-5, T2-6, T2-7, T2-8, T2-9, T2-10, T2-11, T3-1, T3-3.
**Must add a small artifact:** T1-2 (cite or delete refs 26/27), T1-4 (participant table or honest N/A), T3-2 (collapse source CSV).

**DESK-REJECT flags:** **None** by themselves. However T1-3 (asserting a non-existent Zenodo mirror) and T1-4 (STROBE item 14 marked "Addressed" without the content) are **mandatory pre-submission integrity fixes** — a meticulous PLOS editor could return the manuscript for technical-compliance correction. Clear them before upload; they are cheap.

---

## 7. What stands up (do NOT change)

- All nine headline numbers (verified by A3 and the editor).
- The structured abstract (4 headings, 185 words) and the "honest null" framing.
- Consistency of title / STROBE 2007 version across manuscript, checklist, and cover letter.
- The specific AI-use disclosure (names Claude) and the ethics/funding/competing-interests/author-contributions blocks.
- The LODO per-fold disclosure (already honest — A2 misread it).
- The ADRA2A two-filter logic (already consistent — A2 misread it).
- DAM provenance correctly attributed to Keren-Shaul 2017 (not Schafer "developmental origin").
- The non-circular translation statistics (46.3% vs 47.1%, p=0.14) — recomputed exact.

---

## 8. Recommended handling path

**Path C (wording-only + two small additions) is viable and recommended** — this is unusual and worth stating plainly. No conclusion changes, no number changes, no new analysis is required. The manuscript is fundamentally sound; this round is precision/integrity polish for PLOS ONE. **Not** Path A (restructure) and **not** Path B (downgrade article type). The only non-wording actions are: cite/delete refs 26/27 (T1-2), add a participant table or honest N/A for STROBE-14 (T1-4), and generate the collapse-source CSV (T3-2).

**Reframe note to the author (the skill's close):**
- **The strongest over-reach is not your fault.** The absolute "NOT CPSP-specific" negation (resting on p=0.14) and the "Nav1.8 inhibitors repeatedly failed" claim (T1-1) both inherited the older Nav1.7-failure literature framing; suzetrigine's 2025–2026 approval simply post-dates that framing. Both are one-sentence qualifications, not structural flaws.
- **The contribution you buried is actually your strongest result.** The LODO classifier separates nerve-injury datasets *near-perfectly* (4 of 5 folds AUC=1.000 even under leakage control, n=6–28) but **fails to translate to the incision model** (0.677, CI includes 0.5). That is not a "weak/resampling-sensitive classifier" — it is direct, on-thesis evidence that *the axis is nerve-injury-specific rather than a universal pain signature*, which is exactly the paper's central claim. The manuscript currently headlines the 0.677 and under-sells the 4 perfect folds.
- **Swapping the emphasis converts a fragile signal into a stable structural finding.** Lead the ML paragraph with "the signature is nerve-injury-specific (4/5 cross-dataset folds separate perfectly under leakage control) yet does not generalize to the incision model (0.677, CI includes chance)," and relegate "resampling-sensitive candidate-generation tool" to the stability caveat. This turns the reviewer's instinct ("the classifier is weak") into the paper's thesis ("the axis is injury-specific"), with zero number changes.

---

## 9. Process lessons (what the gates cannot catch, and new assertions)

- **A gate passing at 100% certifies arithmetic, not design.** This round, the design-layer concerns (FE-primary, GSE265957) were *mostly defensible* — confirming that a gate-green paper can still be honest rather than hiding a defect. The value of the panel was catching the *prose* and *integrity* layer (orphaned refs, Zenodo clause, STROBE-14), which no numeric gate sees.
- **New gate assertion — reference citation completeness.** Every reference number in the list must appear as an in-text citation. Add to `p7_consistency_gate.py`: parse the `## References` block for numbers 1..N and assert each is referenced in the body (handle unicode superscripts ¹..³³, or switch in-text cites to ASCII for checkability). This would have caught T1-2 automatically.
- **New gate assertion — STROBE "Addressed" ↔ content exists.** If the checklist marks an item "Addressed," the manuscript must contain the corresponding content (item 14 ↔ participant-level stats). A lightweight keyword scan per item would catch T1-4.
- **Second-occurrence staleness.** The data-availability "Zenodo mirrors v1.0.0" claim is false until minted; the existing Zenodo placeholder check should WARN on the literal `XXXXXXX` and also flag the verb "mirrors"/"already" when the DOI is unresolved. (T1-3.)
- **Disclosure ≠ resolution, even for the *positive* result.** A2's misread of ADRA2A shows experts conflate "size-independent significant" with "hit." The fix is prose clarity (T2-7), not a number change — a gate cannot catch unclear two-filter logic. State the two-filter rule once, plainly.
- **The panel caught a *positive* under-reporting, not just negatives.** Most rounds hunt over-claims; this round's highest-value finding (T1-1 contradiction aside) is that the manuscript *under*-reports a genuinely strong, on-thesis result (LODO nerve-injury-specificity). Future rounds should explicitly ask: "what did the author bury that is actually their contribution?"
