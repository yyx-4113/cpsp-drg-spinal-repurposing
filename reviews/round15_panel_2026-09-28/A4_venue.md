# A4 — Journal Venue & Compliance Review (Round 15)

**Manuscript (v1.5.0, git tag `v1.5.0` present):** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null*
**Target venue:** PLOS ONE (SCIE, IF ≈2.8, Q2; accepts negative/null)
**Reviewer discipline:** Judged solely from the products listed in the Round-15 brief. Prior rounds (≤14) were **not** read. PLOS ONE policy details cross-checked via WebSearch on 2026-09-28 (sources cited).

---

## 1. PLOS ONE hard-requirement table (PASS / FAIL with evidence)

| # | PLOS ONE requirement | Verdict | Evidence (from actual files) |
|---|---|---|---|
| 1 | **Abstract ≤ 300 words** | ✅ PASS (length) | `MVP_PLOSONE_submission.md` abstract = **279 words** (whitespace, markdown stripped). Under the 300 cap. |
| 2 | Abstract **unstructured** (no labelled subsections, no citations) | ❌ **FAIL** | Abstract contains bold labels **Background. / Methods. / Results. / Conclusions.** (lines 14–20). PLOS ONE mandates a single unstructured paragraph. **Must reformat.** |
| 3 | **Title ≤ 250 characters** (PLOS rule; task framed as "≤20 words") | ✅ PASS | Title = **143 chars / 16 words**. Within both the 250-char hard rule and the task's 20-word proxy. |
| 4 | **≤ 8 display items** (figures + tables) | ✅ PASS (at boundary) | `## Display items` header: **5 figures + 3 tables = 8**. Note: current PLOS ONE has *no* hard cap on figures/tables (verified 2026-09-28); the task's ≤8 framing is a legacy artifact, but 8 is safely within it. |
| 5 | **All figures embedded** in manuscript docx | ✅ PASS | `Manuscript.docx` contains **5 embedded PNGs** (`word/media/image1–5.png`), **5 `<a:blip>` + 5 `<w:drawing>`** inline, and all 5 figure captions (Fig. 1–5) present. The prior Scientific Reports "missing figures" cause is **fixed**. |
| 6 | **Data Availability** statement, no "available on request" | ✅ PASS | `## Data availability` (line 284) cites versioned GitHub release **v1.5.0**, states "not on request", and "no Zenodo snapshot has been deposited". No `10.5281/zenodo.XXXXXXX` placeholder. |
| 7 | **Ethics statement** | ✅ PASS | `### Ethics statement` present (line 185); secondary de-identified public-data reanalysis; GSE158825 IRB/consent per original deposition. |
| 8 | **Funding** (standalone) | ✅ PASS | `## Funding` (line 278): "no specific funding"; pending-grant note disclosed. |
| 9 | **Competing Interests** | ✅ PASS | `## Competing interests` (line 291): pending FJNSF grant lists ADRA2A, stated not to influence. |
| 10 | **Author Contributions** | ✅ PASS | `## Author contributions` (line 281): single-author prose statement. |
| 11 | **Author Summary** (PLOS ONE *mandatory*) | ✅ PASS (present) ⚠️ length | Present (lines 24–27) = **237 words**. PLOS guidance is ~200 words; **trim toward ≤200** is recommended but not a hard blocker. (Compliance check wrongly labels it *optional* — see §4.) |
| 12 | **AI-use disclosure** (PLOS policy, 2023/2024) | ✅ PASS | Methods (line 182 area): "A large language model (LLM) was used to assist manuscript drafting and language polishing"; no LLM authorship. Also in cover letter. Meets PLOS disclosure requirement. |
| 13 | **CC BY license** | ⚠️ N/A in text | Not stated in manuscript or cover letter. PLOS CC BY is agreed at the submission license step, not in manuscript text — **not a manuscript blocker**, but add a one-line "content will be published under CC BY" to the cover letter for completeness. |
| 14 | **Reporting guideline checklist** supplied | ✅ PASS (weak fit) | STROBE checklist supplied (`STROBE_Checklist.docx` = S8). See §3 for fit concern. |
| 15 | **References** numbered, full journal names, DOIs | ✅ PASS (present) | **40 references**, all 40 carry a `doi.org` string (0 missing). Vancouver order. (Note outdated "37 refs" claim in compliance check — §4.) |
| 16 | No `[truncated]` / round / internal-version tokens | ✅ PASS | Manuscript, supplementary, STROBE: no literal `[truncated]`. (Apparent match in cover letter is only the checklist instruction "No `[truncated]`…", not an artifact.) |

---

## 2. Technical-check assessment (would the pack pass PLOS ONE's automated check?)

- **Embedded figures — FIXED.** The single issue that caused the prior *Scientific Reports* editorial rejection ("missing figures") is resolved: `Manuscript.docx` embeds all 5 figures inline (5 media PNGs, 5 inline drawings, captions Fig.1–5). This is the central technical-check item and it now passes.
- **Abstract structure — would trigger a formatting bounce.** PLOS ONE's technical/formatting check expects an *unstructured* abstract; the labelled Background/Methods/Results/Conclusions layout (item 2, §1) will generate a revision query. Mechanical fix.
- **Display-item count** (8) is within limits; no cap breach.
- **File integrity:** Manuscript/Supporting/Cover/STROBE docx all present in `submission_pack/`; separate `Fig1–5` PNGs also supplied for upload.
- **No phantom Zenodo DOI**, no "on request" wording. Git tag `v1.5.0` matches the Data Availability version. ✅

**Verdict on technical check:** Passable after the abstract is un-structured; the historically fatal "missing figures" defect is gone.

---

## 3. Reporting-guideline appropriateness (STROBE vs alternative)

The study is an **in-silico meta-analysis of 5 transcriptomic studies + docking screen**, not a primary human observational cohort. PLOS ONE's checklist menu (CONSORT / ARRIVE / STROBE / PRISMA) accepts STROBE, but STROBE 2007 was written for *primary observational epidemiology*. The supplied `MVP_STROBE_checklist.md` itself concedes (lines 5–9) it is applied **"by analogy"** because only 1 of 12 datasets (GSE158825, n=60, a negative human-plasma sub-analysis) is an observational cohort; core items "Setting / Participants / Study size (human)" are marked **N/A (primary deposition)**.

**Assessment:** STROBE is *permissible* but a **weak fit**. The manuscript is explicitly framed as a *meta-analysis*, for which **PRISMA** (or PRISMA-style for -omics synthesis) is the canonical EQUATOR guideline, complemented by **MIAME/MINSEQE (GEO) data-reporting** which the manuscript already cites. 

**Recommendation:** Either (a) switch the supplied checklist to **PRISMA** (better maps to "search → eligibility → synthesis → bias" of the 12-dataset curation), or (b) keep STROBE but add an explicit justification paragraph that the reanalysis is computational and STROBE is applied by analogy, with GEO/MIAME compliance as the data-reporting backbone. This is a *soft* compliance point (PLOS accepts STROBE), but a reviewer/editor may question the mismatch — worth pre-empting.

---

## 4. Verification of the author's self-check (`MVP_PLOSONE_compliance_check.md`) — NOT blindly trusted

The compliance check is **stale and internally inconsistent**; its claims must not be taken at face value:

| Compliance-check claim | Reality in v1.5.0 files | Verdict |
|---|---|---|
| "Data Availability … v1.3.0" (lines 22, 74) | Manuscript + cover letter say **v1.5.0** | ❌ **STALE** — check not regenerated for v1.5.0 |
| "37 refs" (lines 6, 18) | Manuscript has **40 references** | ❌ **STALE/inconsistent** |
| "40 / 40 references carry a Crossref-verified DOI" (lines 5, 8, 44) | All 40 entries contain a `doi.org` string (verified); Crossref re-resolution last run Round 12, not re-run for v1.5.0 | ⚠️ **Plausible but unverified for current file** — DOIs *present*, full re-resolution not independently confirmed by me |
| "Author Summary (optional)" (line 16) | PLOS ONE **mandates** an Author Summary | ❌ **Misclassification** (item present, so no blocker) |
| "Figures embedded … 350.012 DPI" (line 38) | 5 PNGs embedded; DPI claim not re-verified by me | ⚠️ Unverified |
| "Checked 2026-09-26 (Round 9)" | Current version is Round 14/15 → v1.5.0 | ❌ **Out of date** |

**Action:** The compliance check must be **regenerated against v1.5.0** (correct version, 40 refs, fix the 37/40 and v1.3.0/v1.5.0 inconsistencies, reclassify Author Summary as mandatory) before submission. Its "Content is PLOS ONE–ready" conclusion is **not** supported by its own stale content.

---

## 5. Formatting / compliance blockers that could prevent acceptance

1. **(BLOCKER — must fix)** Structured abstract → convert to a single unstructured paragraph (keep ≤300 words; 279 available). 
2. **(BLOCKER — metadata)** Regenerate `MVP_PLOSONE_compliance_check.md` to v1.5.0; resolve the 37-vs-40 ref and v1.3.0-vs-v1.5.0 discrepancies.
3. **(SHOULD FIX)** Reporting guideline: prefer PRISMA over STROBE (or justify STROBE-by-analogy + GEO/MIAME).
4. **(MINOR)** Author Summary 237 words → trim toward ~200.
5. **(MINOR)** Add CC BY license statement to cover letter (submission-form agreement otherwise).
6. **(MINOR)** Provide a short title (≤100 chars) at submission (form field, not in docx).

---

## 6. Verdict

**MINOR REVISION.** No scientific defect blocks PLOS ONE; the previously fatal "missing figures" technical failure is fixed (figures embedded, 5/5). Two *mechanical* must-fixes remain before submission: (1) un-structure the abstract, (2) regenerate the stale compliance check to v1.5.0. A reporting-guideline upgrade (PRISMA) and a couple of minor trims are recommended to pre-empt editor/reviewer queries. With those fixes the pack should clear PLOS ONE's technical check.

---

### Sources (WebSearch, 2026-09-28)
- PLOS ONE formatting: abstract **unstructured, ≤300 words**; title **≤250 characters**; figures **embedded at first mention**; Data Availability **mandatory**; Author Summary **required** — confirmed via PLOS submission-guideline summaries (manusights.com 2026-03-24; casrai.org PLOS ONE guide; checkmymanuscript.com PLOS checker).
- PLOS AI-tools policy (2023/2024): AI use **disclosed in Methods or Acknowledgements**, no AI authorship — PLOS Ethical Publishing Practice / PLOS Blog 2024-09; Columbia ReaDI program synthesis of publisher AI policies.
