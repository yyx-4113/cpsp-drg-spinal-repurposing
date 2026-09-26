# REVIEW_round4_2026-09-20 — Editorial Consolidation Report

**Target venue:** *Scientific Reports* (Nature Portfolio), Article type, single author (Yang Y / 杨永新)
**Manuscript:** `reports/MVP_ScientificReports_submission.md` (v1.3, 2026-09-20) + `MVP_ScientificReports_supplementary.md`
**Acting editor:** 小团 (journal-editor role for this round)
**Independence date:** 2026-09-20 — treated as a **first submission**; four reviewers (A1 domain, A2 design/statistics, A3 implementation/provenance, A4 venue/reporting) worked independently and were forbidden from reading any prior-round review, response, or project-status file.
**Panel outputs (this round):** `reviews/round4_2026-09-20/A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`.

---

## 0. Independence declaration

This round was run as a clean first-submission review. The four reviewers each read only the manuscript, the supplementary file, and the raw/processed data under `results/tables/`, `data/`, `docking/`, and `scripts/`. None read `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, `PROJECT_PLAN.md`, `README.md`, `CITATION.cff`, `submission_pack/`, or other reviewers' outputs. Every quantitative claim in the panel reports was recomputed by the reviewer from raw sources — the editor re-verified the single most severe finding with an independent script (§1) reading only raw sources.

---

## 1. Editor's decision

**Recommendation: Major revision (not reject).**

Two independent reasons make this not a reject: (a) the computational pipeline is sound and the headline numbers reproduce exactly (§4, §6); (b) the manuscript's central honesty devices — the *conserved nerve-injury reframing* and the *docking honest-null* — are genuine methodological strengths, not spun weaknesses.

**However, the manuscript as-submitted contains TWO format hard-fails that individually risk a desk-reject / production-gate rejection at *Scientific Reports*:**
- **D1 (hard-fail).** Methods ends mid-sentence with a literal `[truncated]` placeholder (`submission.md:122`). A truncated Methods paragraph is a completeness failure on its own.
- **D2 (hard-fail).** References are not numbered by first citation (Nature house style: "numbered in the order they appear in the text"); the list is numbered sequentially but the text cites `⁵` (Sapio) before `²,³,⁴` (submission.md:20–22).

**Plus one internal numerical contradiction that must be corrected before the docking honest-null narrative is credible:**
- **D3.** The ACVR1 single-variable size-independent p is stated as **0.172** in the Results prose (`submission.md:66`) but **0.584** in Table 3b, S4, and both raw source files. This is the manuscript's own central "honest contradiction" example, and the prose number is simply wrong.

> **Independently confirmed by the editor.** Reading only `results/tables/P6_BH_correction.csv` and `results/tables/P6_enrichment_mw_confounder_check.csv`, ACVR1 `deltaAUC_vs_size_only_p_le0` = **0.584** in both files (also `BH_q_size_indep` = 0.584). No source file contains 0.172. The text value is a stale draft number. The editor additionally re-verified two further defects from raw sources: (i) bulk-only OXPHOS `frac_up` = 0.2778 in `_R3_bulkonly_meta_summary.json::setcalls.Mitochondria_OXPHOS` ⇒ **72.2% down**, not the "27.8% down" printed at `submission.md:36`; (ii) Table 1b per-contrast magnitudes equal the Z-statistics in `_R3_bulkonly_meta_summary.json::scn_tab` (e.g. SCN8A GSE278227 Z = −6.728) and **not** the Stouffer logFC (−0.746), confirming the Z-as-logFC mislabel at `submission.md:201–206`.

---

## 2. Cross-verification table (every recomputed number)

Compiled from A1–A4 independent recomputations plus the editor's own script. "Verified by" = which reviewer(s) recomputed from raw sources; "Editor" = editor re-ran an independent script.

| # | Claim | Manuscript value | Source value | Verdict | Verified by |
|---|-------|-----------------|-------------|---------|-------------|
| 1 | Core signature size | 4,055 / 16,552 | 4,055 (recomputed `meta_FDR<0.05 & consistency≥0.8`) | **MATCH** | A1, A2, A3 |
| 2 | Incision translation concordance | 53.9% (7,751/14,390); 69.5% (2,473/3,556) | 0.5386; 0.6954 | **MATCH** (framing disputed) | A1, A2, A3, A4 |
| 3 | Bulk-only core | 1,981; overlap 1,732/4,055 = 42.7% | 1,981; 1,732; 42.71% | **MATCH** | A2, A3, A4 |
| 4 | Gene-set (primary): Neuroinf / DAM / Complement / OXPHOS | +4.94/100%up; +3.88/93.8%up; +3.44/94.4%up; −2.37/73.7%down | identical (P3_geneset_stats.csv) | **MATCH** | A1, A3 |
| 5 | Bulk-only OXPHOS polarity | "27.8% down" | `frac_up`=0.2778 ⇒ **72.2% down** | **MISMATCH (inverted)** | A3, **Editor** |
| 6 | SCN bulk meta_Z/FDR | −2.92/0.011 … −4.92/1.0e-5 | identical (json scn_tab) | **MATCH** | A1, A3, A4 |
| 7 | Table 1b per-contrast magnitudes | "DN(−6.73)" etc. | = Z-values (−6.728), **not** logFC (−0.746) | **MISLABEL (Z as logFC)** | A1, A3, **Editor** |
| 8 | Hub set | 35; 32/35 in core; 5/35 three-method | identical (P3_hub_genes.csv) | **MATCH** | A1, A2, A3, A4 |
| 9 | LODO AUC/CI | 1.000 / 0.917[0.729,1.0] / 0.95 | identical (P3_lodo_auc_ci.csv) | **MATCH (CI-honesty caveat)** | A2, A3, A4 |
| 10 | Bootstrap stability | 0/35 ≥0.9; max 15.5% | identical (P3_hub_bootstrap.csv) | **MATCH** | A2, A3 |
| 11 | Human miRNA | "253 … pairs" | 253 = distinct miRNAs; **328 high-confidence pairs** | **MISMATCH (units)** | A3, **Editor** |
| 12 | Spinal "16 localisable" | 16 | 15 NotLocalisable ⇒ **20 localisable** | **MISMATCH** | A3, **Editor** |
| 13 | Visium | 33 detectable; 17/33 dorsal horn | identical (P5_GSE325938_*) | **MATCH** | A3, A4 |
| 14 | Docking AUCs / breadth flip | ADRA2A 0.618→0.532 p=0.118; BH q ADRA2A 0.0025 | identical (P6_*.csv) | **MATCH** | A3, A4 |
| 15 | ACVR1 single-variable size-indep p | **0.172** (prose) | **0.584** (Table 3b, S4, P6_BH, P6_MW) | **MISMATCH (internal)** | A2, A3, **Editor** |
| 16 | Docking "10 of the 17 eligible docked" | "10 … actually docked" | 9 of 17 hubs + ADRA2A (non-hub); TFE3 eligible, not docked | **MISMATCH (subset logic)** | A3, **Editor** |
| 17 | ADRA2A `reliable=False` w/ 115 pairs | reliable=False | violates ≥3 rule (should be True) | **LOGIC BREAK** | A1 |
| 18 | AXL size-independent verdict | Table 3b/S4 p=0.141 (CI⊃0); breadth PASS 0.880 | two constructions disagree | **INCONSISTENT** | A1 |
| 19 | Title length | 19 words | 19 | **MATCH** | A3, A4 |
| 20 | Abstract length | ≤200 words | 195 | **MATCH** | A3, A4 |
| 21 | References order | list 1–22; text cites 1,5,2,3,4… | first-citation order differs | **FAIL (format)** | A4 |
| 22 | Display items | 8 (5 fig + 3 tab) | 8 | **MATCH** | A4 |
| 23 | Methods `[truncated]` | literal placeholder at :122 | — | **FAIL (completeness)** | A4 |

**Takeaway:** every *count* the manuscript reports traces to a real source file and is arithmetically correct (Items 1–4, 6, 8–10, 13–14, 19–20, 22). The defects are **mislabels / unit errors / stale values / internal contradictions / format failures** (Items 5, 7, 11–12, 15–18, 21, 23) — not fabricated statistics. This is why the decision is Major revision, not reject.

---

## 3. Graded problem list (T0–T3)

### T0 — Blockers (must fix before acceptance; D1–D3 above)
- **T0-1 (D1).** Remove the literal `[truncated]` at `:122` and complete the Methods BH-enrichment sentence from S4 logic (paste-ready text in A4 F1).
- **T0-2 (D2).** Renumber references by first-appearance order via the submission packer (verified correct assignment in A4 F2); do not hand-edit.
- **T0-3 (D3).** Change ACVR1 "p = 0.172" → "p = 0.584" at `:66` (and anywhere else). The multivariate-vs-size-independent contrast is still valid (9.6e-4 vs 0.584); only the quoted single-variable number is wrong.

### T1 — Major (correct before acceptance)
- **T1-1.** Table 1b: rebuild the per-contrast column as actual log₂FC (from `META_DRG_axis_stouffer.csv` `lfc_*`), move Z to a separately labelled column, and footnote that parentheticals are Z not logFC. (A1 Item 2, A3 F5; inflates fold-change ~9–20×.)
- **T1-2.** Discussion `:91` "redirects repurposing toward … MAPK14, AXL, TFE3 as priorities" contradicts the honest-null. Reframe as hypothesis-generating, explicitly noting none cleared the size-independent filter. (A1 Item 8, A4 F4.)
- **T1-3.** Competing Interests `:169` "ADRA2A receives no privileged treatment" is contradicted by (a) ADRA2A as the composite-ranking gold standard `:83` and (b) ADRA2A singled out for in-vivo testing `:95`. Neutralize both phrasings. (A4 F5.)
- **T1-4.** Bulk-only OXPHOS polarity `:36` — "27.8% down" → "72.2% down". (A3 F1; editor verified.)
- **T1-5.** Human-miRNA `:48`/abstract `:14` — "253 … pairs" → "253 distinct plasma-detectable miRNAs (328 of the 752 high-confidence pairs)". (A3 F2.)
- **T1-6.** Docking subset `:85` — "10 … actually docked" → "9 of the 17 eligible hubs + ADRA2A (added as a known analgesic target); TFE3 was eligible but not docked." (A3 F6; editor verified.)
- **T1-7.** Fixed-effects Stouffer over heterogeneous contrasts with no τ²/I²; and the "degenerate equal weight" characterization is wrong (the weight is the correct effective-n weight). Add a random-effects (DerSimonian–Laird) alternative + heterogeneity stats; re-state the core under RE. (A2 Item 1.)
- **T1-8.** Translation binomial p≈10⁻²⁰ is n-driven on a +3.9 pp effect; the 50% null is inappropriate. Lead with effect size + Wilson CI + permutation null, drop the standalone p. (A1 Item 1, A2 Item 2.)
- **T1-9.** Direction-consistency ≥0.8 pools incision with nerve-injury/translatome, so a gene can be "core-consistent" while incision disagrees. Report `nerve_injury_consistency` and `incision_agreement` as separate annotations. (A2 Item 3.)
- **T1-10.** 19 gene sets tested with no set-level BH; the three floor-pinned sets are tied and only ordered by Stouffer Z. Add BH/q across sets (or max-T). (A2 Item 4.)
- **T1-11.** LODO: the two same-animal GSE241361 folds inflate the mean and must be excluded from the cross-animal mean; the "cross-animal floor 0.917" is a single wide-CI set; 0/35 bootstrap-stable contradicts the "35 candidate hub genes" headline. Soften the hub headline and report the bootstrap-stability of the *docking-target set* itself. (A2 Item 5, A1 Item 16.)
- **T1-12.** Small-n fragility: 57.3% of the primary core is absent from the bulk-only core (translatome-dependent); n=2/2 translatome weighted 1.00. Lead with the bulk-only sensitivity as the primary robustness check, not the 91.4% collapse. (A2 Item 8, Item 10.)
- **T1-13.** Causal language: "conserved maladaptive nerve-injury *response* / *programme*" implies mechanism; design is purely observational. Replace with associational language and add a causal-limit sentence to Methods. (A2 Item 9.)

### T2 — Should fix / strengthen
- **T2-1.** AXL size-correction contradiction (breadth PASS vs S4 p=0.141). Declare one authoritative method or explicitly reconcile. (A1 Item 9.)
- **T2-2.** ADRA2A `reliable=False` despite 115 known pairs — rename to `control_passed` or set True and report the chance-level AUC as the real result. (A1 Item 10.)
- **T2-3.** Human-miRNA null is blood-based and underpowered — narrow the claim to "a blood-proxy null, uninformative about the CNS axis." (A1 Item 12.)
- **T2-4.** Visium 17/33 dorsal horn is constitutive baseline anatomy — reframe as "anatomically present at baseline," not "pain-afferent first station" enrichment. (A1 Item 11.)
- **T2-5.** OXPHOS claim lacks cell-type resolution — add deconvolution or soften to "bulk meta signal, cellular locus unresolved." (A1 Item 15.)
- **T2-6.** CDHR5 reaching three-method consensus is biologically implausible (gut cadherin) — investigate which study drives it; downgrade until resolved. (A1 Item 5.)
- **T2-7.** Literature anchoring gaps: Nav1.6/SCN8A in pain, incision-Nav direction, pain-specific DAM/microglial-state, suzetrigine mRNA-vs-function dissociation, P2X4/DAM partial state, REG3B softening. (A1 Items 3, 6, 7, 13, 17, 18.)
- **T2-8.** Single incision arm (GSE267799, rat, ~day-10) supports the SCN inversion — bound as one-study evidence. (A1 Item 4.)
- **T2-9.** Multiple-testing registry across the five analytical families; composite hypergeometric p is a restatement of the prior term, not docking evidence. (A2 Item 7.)

### T3 — Clarify / honesty
- **T3-1.** Spinal "16 localisable" → 20 (reconcile with Fig. 4 "NotLocalisable n=15"). (A3 F3; editor verified.)
- **T3-2.** LODO degenerate CIs [1.0,1.0] for n=6/9/28 unreported — add the DeLong-collapse caveat. (A3 F4.)
- **T3-3.** Abstract "honest null" vs Results "inconclusive" ADRA2A — align nuance. (A3 F8.)
- **T3-4.** Title/abstract "first" (`submission.md:24`) vs "among the first" (cover letter, intro `:23`) — propagate "among the first." (A4 F3.)
- **T3-5.** Retained "Round-3 independent-panel revision" / v1.3 token (`submission.md:8`, supplementary `:7`) — delete; replace with neutral descriptor. (A4 F6.)
- **T3-6.** Internal `_R3_*.json` filenames in Data Availability (`:166`, `:208`) — rename to neutral names before public deposit; editor must confirm the GitHub repo is populated. (A4 F7.)
- **T3-7.** "CPSP-closest" label not re-tied to its own harvest-day caveat at first use. (A4 F10.)
- **T3-8.** Figure ≥300 DPI claim not text-verifiable — editor/production must check pixel dimensions at print width. (A4 F12.)

---

## 4. Consensus / complementary / disagreement

**Strong consensus (three or four reviewers, independently):** the ACVR1 0.172/0.584 internal contradiction (A2+A3+Editor); the Table 1b Z-as-logFC mislabel (A1+A3+Editor); the Discussion "priorities" contradicting the honest-null (A1+A4); the bulk-only OXPHOS polarity inversion (A3+Editor); the docking 10-of-17 subset error (A3+Editor); the `[truncated]` and reference-ordering hard-fails (A4). The fact that independent reviewers converged on the same defects without reading each other is the strongest signal that these are real, not reviewer noise.

**Complementary (different reviewers, different angles, all valid):**
- A2 (design/statistics) added the structural critique the domain/implementation reviewers did not: fixed-effects-no-τ², set-level BH, causal language, 57.3% small-n fragility, LODO same-animal inflation.
- A1 (domain) added the biological/clinical reading: CDHR5 implausibility, DAM pain-specific citation, Nav1.6 literature, incision single-study bound, REG3B softening, P2X4/DAM partial state.
- A3 (implementation) is the provenance backbone: every headline count traced to a source file and marked MATCH; the five numeric mismatches (F1–F3, F6, F7) are the audit's core deliverable.
- A4 (venue) caught the two acceptance-blocking format failures and the competing-interests consistency gap that the other three did not foreground.

**Disagreements / adjudication:** there are no material *factual* disagreements. The only tension is severity grading — e.g., A1 grades the discussion "priorities" contradiction as a Major coherence issue while A4 grades it a must-fix format/contradiction. **Editor's adjudication:** it is both — a must-fix contradiction (T1-2) because it undermines the manuscript's own headline honesty device. On the ACVR1 number, A2 wanted to know whether 0.172 might be a different (univariate Wald) test; the editor's raw-source check resolves this — 0.172 appears in no file, so it is a stale value, not an alternative test. On AXL size-correction, the editor sides with A1: declare one authoritative construction rather than leaving both verdicts standing (T2-1).

---

## 5. Must-fix list (with DESK-REJECT flags)

**DESK-REJECT-risk if not fixed before resubmission:**
1. `[truncated]` in Methods (T0-1) — *add analysis, not just wording.*
2. References not numbered by first citation (T0-2).
3. ACVR1 0.172→0.584 internal contradiction (T0-3).

**Must fix (acceptance-blockers, not desk-reject):**
4. Table 1b Z/ logFC relabel (T1-1).
5. Discussion "priorities" ↔ honest-null reconciliation (T1-2).
6. ADRA2A "no privileged treatment" ↔ behavior reconciliation (T1-3).
7. Bulk-only OXPHOS polarity (T1-4).
8. Human-miRNA 253/328 units (T1-5).
9. Docking 10-of-17 subset (T1-6).
10. Fixed-effects → add random-effects + τ²/I²; drop "degenerate equal weight" claim (T1-7).
11. Translation effect-size-led framing (T1-8).
12. Consistency incision vs nerve-injury split (T1-9).
13. Set-level BH across 19 gene sets (T1-10).
14. LODO same-animal exclusion + hub-stability softening + target-set bootstrap (T1-11).
15. Bulk-only as primary sensitivity; 57.3% fragility stated (T1-12).
16. Associational language + causal-limit sentence (T1-13).

**Split: "须加分析" vs "须改措辞"**
- *须加分析 (new computation):* T1-7 (RE meta + τ²/I²), T1-9 (separate NI/incision consistency), T1-10 (set-level BH), T1-11 (target-set bootstrap stability), T2-5 (cell-type deconvolution).
- *须改措辞 (rewording only, numbers already correct):* T0-1 (complete sentence), T0-2 (renumber), T0-3 (0.172→0.584), T1-1 (relabel column), T1-2/1-3 (reconcile contradictions), T1-4/1-5/1-6 (correct printed numbers), T1-8 (effect-size framing), T1-12 (reorder sensitivities), T1-13 (causal wording), all T2/T3 hygiene.

---

## 6. § Stands up (verified correct — delivered, not filler)

The following were suspected by the editor/panel but confirmed exact against raw sources — the manuscript's quantitative spine is sound:
1. Core 4,055 / 16,552 — exact; definition reproduces the file.
2. Translation 53.9% (7,751/14,390) and 69.5% (2,473/3,556) — exact; binomial p real arithmetically.
3. Bulk-only 1,981 / 1,732 / 42.7% — exact.
4. Gene-set programme (Neuroinf +4.94/100%up; DAM +3.88/93.8%; Complement +3.44/94.4%; OXPHOS −2.37/73.7%down) — exact in the primary meta.
5. SCN bulk meta_Z/FDR and directions — exact; SCN8A most significant is correct; the inversion holds across species (not a rat/mouse confound).
6. Hub set 35 / 32 in core / 5 three-method — exact; bootstrap 0/35 stable is faithfully reported.
7. LODO values and CIs — exact; cross-animal floor 0.917 honest.
8. Docking AUCs, breadth flip 0.618→0.532 (p=0.118), BH q-values — exact; the honest-null narrative is internally consistent with its data and is a genuine strength.
9. Title 19 words, Abstract 195 words, 8 display items, editable tables, AI-use disclosure, Reporting-Summary consistency — all compliant.
10. Every processed-data file cited in the display items exists locally.

---

## 7. Processing path (recommended)

**A — Reframe + resubmit (recommended).** The study's contribution (meta-defined conserved nerve-injury axis + honest docking null + transparency about negative layers) is intact and, once the T0/T1 items are fixed, is a strong *Scientific Reports* Article. The required changes are mostly correction and re-framing, not new wet-lab data.

**B — Demote (not needed).** None of the defects require demoting the study to a "methodology note" or withdrawing the honest-null claim; the null is the paper's strength.

**C — Wording-only (insufficient alone).** Pure rewording cannot close T0-1 (incomplete Methods), T0-3 (wrong number), or the T1 *须加分析* items (RE meta, set-level BH, target-set bootstrap, cell-type deconvolution). Those require computation.

**Priority order for the author:** (1) fix the three T0 blockers; (2) fix the T1 *须改措辞* number corrections (cheap, high-impact); (3) run the four T1 *须加分析* computations; (4) sweep the T2/T3 hygiene items. Estimated effort: T0+T1-措辞 ≈ 1 focused revision pass; T1-分析 ≈ 2–3 days of recomputation.

---

## 8. Reframe note (required by the panel brief)

The single most consequential reframing the editor endorses is **decoupling the "honest null" from the Discussion's translational "priorities."** The manuscript's strongest asset is its candid docking null; the Discussion currently spends that credibility by re-prioritizing MAPK14/AXL/TFE3 — two of which failed the size-independent filter and one of which was never docked. Once the Discussion is made null-consistent (T1-2) and the ADRA2A treatment is reconciled with the competing-interests statement (T1-3), the paper reads as the disciplined, hypothesis-generating reanalysis it actually is. The second reframing is **honest fragility reporting**: the 4,055-gene core is 57.3% translatome-dependent and the 35 hubs are bootstrap-unstable; presenting these as known rather than as sensitivity boundaries strengthens, not weakens, the manuscript. Neither reframing requires new data — only disciplined wording and three small recomputations.

---

## 9. Process lesson (for the author's workflow)

The defects that cost this round are **internal-consistency defects introduced in the revision pass**, not pipeline errors: a stale ACVR1 number, a truncated Methods sentence, mis-ordered references, and a Z-column left unrelabelled. They are exactly the class of error a final automated "consistency gate" would catch — and the project already runs consistency/word/docx gates for the *Anaesthesia* manuscript. **Recommendation:** add a pre-submission gate that (i) greps the manuscript for any `[truncated]` / `vX.Y` / `Round-N` token, (ii) recomputes every in-text number against its source CSV/JSON and fails on mismatch, and (iii) verifies reference first-citation order against the numbered list. This would have prevented T0-1, T0-2, T0-3, T1-4, T1-5, T1-6, and T3-5 at zero new analysis cost.

---

*Report only — no manuscript file was modified. Panel outputs: `reviews/round4_2026-09-20/A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`. Editor's independent recomputation script read only `results/tables/P6_BH_correction.csv`, `P6_enrichment_mw_confounder_check.csv`, `_R3_bulkonly_meta_summary.json`, `META_DRG_axis_stouffer.csv`, `P4_hub_targeting_miRNAs.csv`, `P4_hub_miRNA_human_integration.csv`, `P5_hub_lineage_consensus.csv`.*
