# REVIEW Round 11 (2026-09-27) — Independent Panel Consolidation

**Manuscript:** `reports/MVP_PLOSONE_submission.md` (+ supplementary, cover letter, compliance, STROBE) — CPSP DRG–spinal-axis in-silico meta-analysis + ML + single-cell + spatial + virtual screening; PLOS ONE target.
**Editor:** consolidated by the coordinating agent from four independent expert reports.
**Panel files:** `reviews/round11_panel_2026-09-27/A1_domain.md`, `A2_design.md`, `A3_provenance.md`, `A4_venue.md`.

---

## 1. Independence statement (and evidence it worked)

Each expert received a self-contained brief (`_PANEL_BRIEF.md`) and was **forbidden** from reading any `REVIEW_*.md` / `RESPONSE_*.md` / `REVISION_*.md`, task-status files, project-overview, deposit SOP, `author_verification_statement.md`, or any peer's output file in the panel directory. Every expert recomputed the key numbers from raw `results/tables/*.csv|json` with their own script. **No reviewer had access to another's draft or to prior rounds.**

**Evidence independence actually worked** (the diagnostic the skill requires):
- The **211-denominator defect** was hit independently by **two** reviewers from different angles — A2 via complement arithmetic (primary − relaxed = 468) and A1 via the present-but-NS + absent partition (313); the editor reproduced 313 from raw sources.
- The **stale-title defect** was hit independently by **two** reviewers from different layers — A3 (provenance: `CITATION.cff:3` + `build_sr_submission_pack.py:50` emit the old title into `.docx` metadata) and A4 (venue: same files + single-source-of-truth rule).
- Findings *cluster* on already-known themes (the DRG-only-meta-core vs "DRG–spinal axis" title tension, the translatome-dependence denominator) — this is expected for a mature manuscript and indicates the panel read the *current state*, not a delta.

No evidence that any reviewer re-litigated a prior-round fix or accepted the manuscript's own framing uncritically.

---

## 2. Verdict table

| Expert | Layer | Overall verdict | DESK-REJECT? | Headline |
|---|---|---|---|---|
| A1 | Domain (pain genomics) | Accept after minor revision | No | Biology honestly reported; 2 genuine numeric errors (LPL FDR, 211 denominator) |
| A2 | Design / Statistics | Do not reject; 4 T1 must-fix | No | 211 miscount, 4/4 mislabel, zero-precision CI conclusion, undeclared EPV |
| A3 | Implementation / Provenance | No desk-reject; fix T1/T2 before acceptance | No | Numbers fully traceable; title-in-CITATION.cff + SR-legacy gate are the real defects |
| A4 | Venue / Reporting (PLOS ONE + STROBE) | **T0 BLOCKER** (Zenodo placeholder) + T1 title | Flagged T0 on DA statement | Placeholder DOI blocks submission; title not single-source-of-truth |

**Distribution:** 0 recommend rejection; 1 flags a submission-blocking (T0) hygiene defect; 3 flag T1 numeric/structural must-fixes. **No scientific fabrication or unreproducible number was found** — all headline figures recomputed to the raw sources and matched.

---

## 3. Cross-verification table (manuscript claim vs independent recompute)

| # | Manuscript location | Claim | Independently recomputed | Who checked | Verdict |
|---|---|---|---|---|---|
| 1 | L44 / core def | primary core = 4,055 | 4,055 (all FDR<0.05 & consistency≥0.8) | A2, A3, Editor | ✅ consistent |
| 2 | L50 | bulk-only core 2,512; overlap 2,202/4,055 = 54.3% | 2,512; 2,202 = 54.3% | A2, A3 | ✅ consistent |
| 3 | L50 | relaxed ≥3/4 overlap 3,587/4,055 = 88.5% | 3,587 = 88.5% | A2, A3 | ✅ consistent |
| 4 | L50 | "only **211** … not bulk-significant at all" | 211 = present-but-NS; **+102 absent from bulk file = 313** lacking bulk support; primary−relaxed = **468** | A1 (313), A2 (468), **Editor (313, from raw)** | ❌ **INCONSISTENT — T1** |
| 5 | L50 | strict overlap "all four bulk contrasts concordant, 4/4" | of 2,202 overlap, **495 (22.5%) are K=3 only**; pure 4/4 = **1,707** | A2 | ❌ **MISLABELLED — T1** |
| 6 | L62 | 32/35 hubs in meta core | 32/35 (from `P3_hub_genes.csv` `in_meta_core`) | A2, A3 | ✅ consistent |
| 7 | L64 / Fig2A | LODO incision AUC 0.677 [0.374,0.940]; NI folds = 1.000 | matches `P3_lodo_auc_ci_leakage_controlled.csv` | A2, A3 | ✅ consistent (but see #8) |
| 8 | L64 / Conclusion | axis is "nerve-injury-specific (not incision)" | GSE278227 n=28 CI ≈ [1.0,1.0] zero-precision; n=6 floor; AUC=1.0 on 139–164 feats = overfit fingerprint | A2 | ⚠️ **OVERSTATED — T1** |
| 9 | L66 | bootstrap median 43 / Jaccard 0.304 / 8.70 / P≥3=1.000 | matches `_R4_targetset_bootstrap.*` | A2, A3 | ✅ consistent |
| 10 | L48 | neuroimmune/DAM/complement q=0.003 | q is BH-adjusted permutation resolution floor (upper bound), not precise q | A2 | ⚠️ **UNLABELLED UPPER BOUND — T2** |
| 11 | L1 (title) | new title "DRG–spinal axis: dorsal root ganglion analysis…" | `CITATION.cff:3` + `build_sr_submission_pack.py:50` emit **OLD** title into `.docx` metadata | A3, A4, **Editor** | ❌ **INCONSISTENT — T1** |
| 12 | L271 (DA statement) | Zenodo DOI `10.5281/zenodo.XXXXXXX` (placeholder) | placeholder confirmed; data genuinely on public GitHub | A4, **Editor** | ❌ **SUBMISSION BLOCKER — T0** |
| 13 | L44 vs L1 | "DRG–spinal axis" title vs body conceding meta core is DRG-only | conceded at L44; title leads with stronger framing | A2, A4, A1 | ⚠️ **RESIDUAL OVERSTATEMENT — T2** |
| 14 | STROBE | 22/22 items complete | confirmed complete, reanalysis-appropriate N/A | A4 | ✅ consistent |
| 15 | AI disclosure / IRB / Funding | explicit, correct | explicit (names Claude/Anthropic, denies authorship); IRB correctly exempt-for-reanalysis | A4 | ✅ consistent |

---

## 4. Graded consolidated issue list

### T0 — submission-blocking (DESK-REJECT class as submitted)
**T0-1 · Zenodo placeholder DOI in Data Availability statement (L271).** `10.5281/zenodo.XXXXXXX` is a literal placeholder. PLOS ONE requires a real, immediately-accessible repository. **Mitigating:** the underlying data IS genuinely available — the public GitHub repo (MIT, CITATION.cff, MANIFEST.sha256) was confirmed live and every table named in the statement exists in `results/tables/`. **Fix (either):** (a) mint the real Zenodo DOI and backfill, or (b) honestly cite the GitHub repository + version tag v1.0.0 as the data source (PLOS ONE accepts GitHub when properly described). Until the placeholder is replaced, the statement is false and the manuscript cannot be submitted. *(Flagged by A4; editor-verified. Note: user has deferred Zenodo — this must be closed before submission.)*

### T1 — must fix before acceptance
**T1-1 · "211 not bulk-significant at all" is arithmetically inconsistent (L50).** Editor-verified from raw sources: of 4,055 core genes, 102 are **absent from the bulk file entirely** (never tested in bulk) and 211 are present-but-NON-significant (FDR≥0.05). The true count lacking bulk-support evidence = **313**, not 211; A2's stricter reading (primary − relaxed overlap) = **468**. The "211" silently excludes the 102 never-bulk-tested genes, understating the translatome-specific contribution. **Fix:** publish one canonical partition — "211 present-but-NS + 102 absent-from-bulk = 313 lacking bulk evidence; 468 outside the relaxed ≥3/4 overlap" — with explicit definitions. *(A1=313, A2=468, Editor=313; adopt 313 as the defensible correction, note A2's 468.)*

**T1-2 · "strict 4/4" overlap mislabelled (L50).** Of the 2,202 overlap, 495 (22.5%) are K=3 only (3/4 concordant); pure 4/4 = 1,707. Calling it "all four bulk contrasts concordant, 4/4" is false for 22.5% of the set. **Fix:** relabel "≥4/4 or 3/3" or report the pure 4/4 (1,707) separately. *(A2 F2; editor-verified K-distribution.)*

**T1-3 · "nerve-injury-specific" conclusion rests on zero-precision CIs (L64/Conclusion).** The conclusion that the axis is nerve-injury-specific (not incision) rests on GSE278227 n=28 (AUC=1.0, CI ≈ [1.0,1.0], zero precision) plus the n=6 design floor, while AUC=1.0 on 139–164 features vs n=6–28 test sets is an overfitting fingerprint. **Fix:** downgrade to "a candidate nerve-injury-enriched signal" and declare the precision limitation explicitly. *(A2 F3.)*

**T1-4 · EPV never declared (Methods/L64).** LODO uses 139–164 selected features against n=6–28 test sets (EPV ≪ 1), never stated. **Fix:** add "these classifiers are severely under-parameterised and are used as candidate-generation screens, not calibrated precision estimates." *(A2 F4.)*

**T1-5 · Title not a single source of truth (CITATION.cff:3, build script:50).** The manuscript (L1) uses the NEW title; `CITATION.cff` line 3 and `scripts/build_sr_submission_pack.py` line 50 hard-code the OLD title ("…non-predictive incision translation…"); the build script writes that stale string into the `.docx` metadata (`cp.title = MS_TITLE`, line 64). A reviewer opening the Word file sees a title that mismatches the heading and cover letter. **Fix:** make the title canonical in one place and reference it; correct both `CITATION.cff` and the build script before the `.docx` is built. *(A3 T1-A, A4 T1-1; editor-verified.)*

**T1-6 · LPL FDR mislabel (Table 1a / L50 area).** Manuscript states LPL "FDR 6.1e-4" but the table gives `meta_FDR` 2.63e-3; 6.1e-4 is the *uncorrected* p. **Fix:** correct the cited value or its label. *(A1.)*

**T1-7 · REG3B framed as purely "external hypothesis" while meta-significant (L82/L122).** REG3B is meta-significant (FDR ≈ 7e-14) and up in all 3 nerve-injury contrasts, yet framed as an external motivational hypothesis. **Fix:** tighten the framing so the external-evidence point is not over-read as "not an internal hit." *(A1.)*

### T2 — should fix (wording / framing)
- **T2-1** · Cover letter vs manuscript tense conflict: "released at submission" (cover) vs "will be released/deposited" (manuscript). Reconcile. *(A4.)*
- **T2-2** · Residual title overstatement "DRG–spinal axis": the six-input meta core is DRG-only; spinal is supplied separately (conceded L44). Soften the title or move "–spinal" to a subtitle. *(A2 F5, A4 Pair B, A1.)*
- **T2-3** · "Not CPSP-specific" Conclusion rests on the conceded single-heterogeneous-incision-arm limitation (L152 vs L134). Soften the strength. *(A4 Pair A.)*
- **T2-4** · Primary FE meta_Z SE marginally anti-conservative because the two same-animal translatome timepoints are treated as independent (11.4% weight). Declare. *(A2 F6.)*
- **T2-5** · q=0.003 is a BH-adjusted permutation resolution lower bound (upper bound), not a precise q. Label it. *(A2 F7.)*
- **T2-6** · Hub–core overlap (32/35) source is `P3_hub_genes.csv` `in_meta_core`, NOT `P5_hub_lineage_consensus.csv` (which has no core flag). Clarify in Methods. *(A2 F8.)*
- **T2-7** · Three different "35-minus-k" denominators across localisation platforms (DRG 34/35, spinal 33/35, Visium 33/35). Add one orienting sentence. *(A1 Issue I.)*
- **T2-8** · "honest null" should foreground that the entire ion-channel class (α2δ / NaV — the clinically validated analgesic backbone, and in the authors' own CPSP literature set) was structurally undockable, so the null cannot speak to them. *(A1.)*
- **T2-9** · Refresh stale gate artifact `scripts/_gate_out.txt` (shows source 1981 / 0.79 / references=26) after recompute. *(A3 T2-A.)*

### T3 — format / polish (non-blocking)
- **T3-1** · Supplementary S5b has a duplicated Sigma1 row (`:190-191`). Delete one. *(A3 T2-B.)*
- **T3-2** · Supplementary S2 "Present" column is same-name/different-meaning vs source `present` field (CRISP3/LNP1 show Present=1 but source `present=False`). Rename column (e.g., `In_35hub_set`). *(A3 T2-D.)*
- **T3-3** · "37/37 DOI" claim rests on a script the compliance check says must not be re-run (unverifiable). Verify or qualify. *(A4 T3-1.)*
- **T3-4** · STROBE Item 19 mislocated line reference. *(A4 T3-2.)*
- **T3-5** · Build script still self-identifies as a "Scientific Reports" pack. Rename. *(A4 T3-3.)*
- **T3-6** · README promises a repository DOI that does not yet exist. *(A4 T3-4.)*
- **T3-7** · `P3_hub_genes.csv` stores `in_meta_core` as boolean while Table 2 shows Yes/No — align vocabulary. *(A1.)*
- **T3-8** · Deprecate the Scientific-Reports-legacy hardcoded gate `scripts/gate_consistency.py` (lines 92/199-200/214 write 0.917, 53.9%, references=37); it cannot catch number errors and is wrong-context for PLOS ONE. Keep only `p7_consistency_gate.py` (derives expected values from source). *(A3 T1-B.)*
- **T3-9** · Minor copy-edit: "to our knowledge, to our knowledge" double-phrasing (L36). *(A1.)*

---

## 5. Consensus / Complementarity / Disagreement

**Consensus (all four):** (a) no scientific fabrication — every headline number traces to a correct raw source; (b) the honest-null + self-critical multiple-testing discipline is the paper's real strength; (c) T0-1 (Zenodo) and T1-5 (stale title) are real blockers; (d) T1-1 (211) and T1-2 (4/4) are real numeric inconsistencies; (e) STROBE 22/22 complete, AI disclosure and IRB statements correct.

**Complementarity (each layer caught what others could not):** A1 caught domain framing errors (REG3B, ion-channel undockability, LPL FDR); A2 caught the design-layer statistics (211, 4/4, zero-precision CI, EPV, anti-conservative SE); A3 caught provenance/code defects (title-in-CITATION.cff, SR-legacy gate, S2 column collision, Sigma1 dup); A4 caught venue/reporting blockers (Zenodo placeholder, title single-source, STROBE cross-ref). This is exactly the intended payoff of a multi-layer panel.

**Disagreements (adjudicated, not averaged):**
- **Severity of the 211 issue:** A1 computed the unsupported complement as **313** (211 present-but-NS + 102 absent); A2 as **468** (primary − relaxed overlap). These are *different valid definitions*, not a contradiction. **Ruling:** adopt **313** as the defensible correction (it is the literal "lacking bulk evidence" count, editor-verified), and require the author to publish ONE canonical partition with explicit definitions (211 / 102 / 313 / 468 all stated).
- **Overall verdict:** A1 returned "accept after minor revision" (lenient) while A2/A4 returned T1/T0 flags. A1's leniency certifies the *biology layer*, not the whole manuscript. **Ruling:** adopt the stricter verdict for the manuscript as a whole — the lenient domain verdict does not cover the design-layer and venue-layer defects.
- **Article type:** the manuscript's strongest real finding (the honest null + method self-criticism) is being *buried* while the weakest (the nerve-injury-specific ML signal resting on zero-precision CIs) is headlined. **Ruling:** this is a reframing opportunity, not a downgrade (see §8).

---

## 6. Priority must-fix list

**DESK-REJECT flags:** T0-1 only (Zenodo placeholder) — mitigable by minting a real DOI or honestly citing the public GitHub repo. No scientific DESK-REJECT.

**Must add analysis / recompute (not wording-only):**
1. T1-1 — publish canonical bulk-support partition (211 / 102 / 313 / 468).
2. T1-2 — report pure 4/4 overlap (1,707) or relabel.
3. T1-3 + T1-4 — declare EPV and downgrade the nerve-injury-specific conclusion to a candidate signal.

**Must reword / fix structure:**
4. T0-1 — replace Zenodo placeholder (real DOI or GitHub citation).
5. T1-5 — single-source the title (fix `CITATION.cff` + build script).
6. T1-6 — correct LPL FDR value/label.
7. T1-7 — tighten REG3B framing.
8. T2-2/T2-3 — soften title/scope and "not CPSP-specific" strength.
9. T2-4/T2-5 — declare anti-conservative SE and q upper-bound.
10. T2-6/T2-7 — clarify hub-core source file and platform denominators.
11. T3-* — supplementary table fixes (Sigma1 dup, S2 column, gate deprecation, script renames).

**"Wording-only is not viable" for T1 items:** T1-1/T1-2/T1-3/T1-4 require numeric/structural correction, not prose; a wording-only revision would not close them.

---

## 7. What stands up (do NOT change)

- Core 4,055; bulk-only 2,512; strict overlap 54.3% (2,202); relaxed 88.5% (3,587); collapse 91.4% — all recomputed and correct.
- 32/35 hub–core overlap; bootstrap median 43 / Jaccard 0.304 / dock_eligible_17 mean 8.70 / P(≥3)=1.000 — correct.
- LODO leakage-controlled AUCs (NI folds 1.000; incision 0.677 [0.374,0.940]) — correct; DeLong collapse at AUC=1.0 correctly flagged non-informative.
- Circularity correctly handled: non-circular translation test 46.2% vs 47.1%, p=0.14 (recomputed, matches).
- Docking honest-null three-piece (ADRA2A 0.618→0.532, p=0.118; reverse/MW controls) — real, not decorative.
- OXPHOS honestly fails random-effects (q=0.31), stated identically in Abstract/Results/Discussion.
- AI-use disclosure (explicit, names Claude/Anthropic, denies authorship); IRB/ethics (correctly exempt for reanalysis); Funding; author-contributions (honest single-author); STROBE 22/22 complete.

---

## 8. Recommended handling paths

**A) Restructure-and-resubmit as the SAME article type (original research) — recommended.** The honest-null + method self-criticism is a legitimate original-research contribution. After closing T0-1 + T1-1…T1-7, the manuscript is acceptable.
**B) Downgrade article type — NOT recommended.** The contribution is substantive (a reproducible negative + a self-critical method paper), not a mere letter/correspondence.
**C) Wording-only — NOT viable.** T1-1/T1-2/T1-3/T1-4 are numeric/structural; a prose-only pass cannot close them.

**Reframe note to the author:** the strongest claim that does *not* fully hold is the "nerve-injury-specific axis" headline (T1-3) — its failure is *not your fault*: it is driven by small-n structural opacity and the AUC=1.0-overfitting fingerprint, not by a mistake you made. The finding you *buried* — the honest repurposing null plus the multi-layer self-critical multiple-testing discipline — is actually your contribution. Swapping the emphasis (lead with the honest null + reproducibility; present the ML signal as a candidate-generating screen with declared EPV) converts the paper from a fragile signal into a stable methodological/negative-result contribution that PLOS ONE explicitly welcomes.

---

## 9. Process lessons (what gates could NOT have caught)

- **A gate passing at 100% proves arithmetic, not design.** The 211-denominator and 4/4-mislabel defects are design-layer; no string-gate detected them. Only hypothesis-generating human-style review found them.
- **A consistency gate only checks enumerated first occurrences.** The title appears in the manuscript, `CITATION.cff`, and the build script; the gate covered the manuscript occurrence and silently passed the stale duplicates. **Rule:** grep every derived artefact for the *value*, require a single source of truth.
- **"Counted as present-but-NS" ≠ "counted as absent-from-bulk."** The 211-vs-313-vs-468 ambiguity is a reporting-precision trap. Require the author to publish one canonical matrix with explicit definitions.
- **New gate assertions to extend coverage to the design layer:** (a) recompute the bulk-support partition and assert it equals the presented number; (b) fail if any Data-Availability DOI string is a placeholder (`XXXXXXX`); (c) grep the title across all artefacts and assert a single canonical string; (d) deprecate the SR-legacy hardcoded gate (`gate_consistency.py`) — it encodes expected values and cannot catch errors.

---

*Editor's personal verification: the single worst scientific claim (the "211" denominator, T1-1) was reproduced from raw `META_DRG_axis_CORE_signature.csv` (4,055) and `META_bulkonly_meta.csv` (15,735): 102 core genes are absent from the bulk file, 211 are present-but-NON-significant, so 313 — not 211 — lack bulk support. This is recorded as confirmed. The two submission-blocking findings (T0-1 Zenodo placeholder; T1-5 stale title in CITATION.cff/build script) were also confirmed by direct file inspection.*
