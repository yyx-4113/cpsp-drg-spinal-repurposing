# A4 — PLOS ONE Venue Compliance / STROBE 2007 & Integrity Audit

**Role:** PLOS ONE journal editor + STROBE reporting-standard auditor (independent panel)
**Date:** 2026-09-26
**Manuscript under review:** `reports/MVP_ScientificReports_submission.md` (283 lines)
**Target venue:** PLOS ONE (SCIE)
**Independence:** Treated as a **first submission**. I read only the panel brief, the manuscript, the STROBE checklist, the PLOS ONE cover letter, and the PLOS ONE compliance check. I did **not** read any sibling review, prior round, memory, manifest, response, or conversation history. Every compliance claim below was re-verified against the actual manuscript text or the journal/standard requirement — nothing is assumed.

---

## Scope and method

I verified, from the manuscript's own text, that all PLOS ONE mandatory sections are present and non-empty; I recomputed the abstract word count, cross-checked the STROBE 2007 checklist item-by-item against the manuscript, and tested the Data Availability / AI-disclosure / Ethics / Competing-Interests statements against PLOS policy. Where the supplied `MVP_PLOSONE_compliance_check.md` makes a verifiable claim, I re-checked it against the manuscript and report any mismatch.

---

## Findings

### Issue 1 — STROBE Item 1: checklist misquotes the title, and the title omits "meta-analysis"

【Problem】 The STROBE checklist claims the title states "multi-dataset in-silico meta-analysis," but the actual title contains no such phrase and no word "meta-analysis" at all; STROBE 2007 Item 1 (title should indicate the study design) is therefore not demonstrably satisfied at the title level, and the checklist itself is inaccurate.

【Evidence】
- STROBE checklist L11: *"Title states 'multi-dataset in-silico meta-analysis'. Abstract (lines 7–21) states the design: 12 GEO datasets → Stouffer meta → dual-ML hub ID → docking."*
- Actual title (manuscript L1): *"Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"* — the string "meta-analysis" does **not** appear. The word "reanalysis" appears only in the metadata block (L8), not the title.
- STROBE 2007 Item 1: "Indicate the study design in the title and/or abstract." The design is indicated in the **abstract** (L14: "We reanalysed 12 public GEO datasets… Stouffer meta-analysis") but **not** in the title.

【Why it matters】 A checklist that misquotes the very text it audits is not a trustworthy verification document, and the title failing to signal "meta-analysis / reanalysis" weakens STROBE compliance and discoverability. This is a published-reporting defect that a meticulous STROBE-aware reviewer or editor will catch.

【Specific fix】 Pick one:
- (a) Amend the title to carry the design, e.g. *"…: a multi-dataset in-silico meta-analysis, non-predictive incision translation, and an honest repurposing null"*; **or**
- (b) Correct the checklist to an honest statement: *"Title does not name the design; design is stated in the Abstract (L14: 'We reanalysed 12 public GEO datasets… Stouffer meta-analysis') and in the manuscript metadata (L8). STROBE Item 1 satisfied via the abstract, not the title."* Do **not** leave the false "Title states 'multi-dataset in-silico meta-analysis'" claim standing.

---

### Issue 2 — Compliance check reference count (26) contradicts the manuscript (33); the check cannot be trusted as evidence of readiness

【Problem】 The PLOS ONE compliance check asserts "26 refs" and "23/26 DOIs verified," but the manuscript contains **33 numbered references** (L176–L208). A claim this easily verified is wrong, which means the check was not run against the final file and its other claims (DOI resolution, figure DPI, gate passes) are unsubstantiated.

【Evidence】
- Compliance check §1 item 6: *"References numbered in first-citation order (Vancouver) | ✅ PASS | 26 refs, order verified by `p7_consistency_gate` (0 errors)"*; §3: *"26/26 DOIs verified and appended."*
- Manuscript L176–L208: 33 references (1. Macrae … 33. Irwin). The in-text citations likewise run to ³³ (e.g., L128 cites ³³).
- The two artifacts disagree on the single most countable element of the manuscript.

【Why it matters】 Desk editors and the PLOS technical check use the compliance check to certify readiness. A check that miscounts references signals it was generated against an earlier draft; its "Content is PLOS ONE–ready" verdict and all downstream PASS claims (DOIs, 300-DPI gates, consistency gates) are therefore unverified. Submitting this check as supporting evidence is an integrity risk, not a cosmetic one — it could be read as a fabricated verification artifact.

【Specific fix】 Re-run the compliance/DOI scripts against the actual `MVP_ScientificReports_submission.md` and regenerate the document; confirm all 33 references carry a DOI where available (the 7 references beyond the check's "26" — refs 27–33, i.e. Kong, Scholz, Zhang Y, Luo, Xiao, Pushpakom, Irwin — must each be checked). Replace every "26" with "33" and remove the "Content is PLOS ONE–ready" verdict unless it is regenerated against the real file. If 7 references were added after the last check, re-verify those 7 specifically and state so.

---

### Issue 3 — STROBE checklist line citations are systematically offset from the manuscript (traceability failure)

【Problem】 Multiple STROBE checklist line citations do not point to the text they describe, so an editor tracing the checklist cannot locate the cited content. This corroborates Issue 2 (the checklist was not built against the final file).

【Evidence】
- STROBE item 22 (Funding) L32: *"Funding (line 211): no financial support; analyses conducted as preliminary foundation for a pending Fujian Natural Science Foundation grant…"* — but manuscript L211 is a horizontal separator; the Funding **header** is L215 and the text L216.
- STROBE item 1 L11: *"Abstract (lines 7–21)"* — the abstract is actually L12–L20.
- STROBE item 14 L24: *"Section 3.4, line 70"* for the human miRNA layer — the human-layer results are at L70, acceptable, but item 22's "line 211" is plainly wrong by ~4 lines and item 1's "lines 7–21" is wrong by ~5 lines, indicating a global offset.

【Why it matters】 A reporting checklist whose citations cannot be traced is useless as an audit trail and undermines confidence in every "Addressed" mark.

【Specific fix】 Re-derive all line numbers against the final manuscript (or, better, cite **section headings** rather than line numbers, which survive re-rendering). Minimum correction: change "Funding (line 211)" → "Funding (L215–216)"; "Abstract (lines 7–21)" → "Abstract (L12–L20)".

---

### Issue 4 — Data Availability: Zenodo placeholder DOI "to be minted at submission" is non-compliant wording at submission time

【Problem】 The Data Availability statement gives a placeholder Zenodo DOI (`10.5281/zenodo.XXXXXXX`) "to be minted at submission." PLOS requires data to be available without restriction; a placeholder with no real accession is not acceptable as the "permanent" archive, even though the GitHub repo is genuinely public.

【Evidence】
- Manuscript L222: *"A versioned Zenodo archive will be deposited at submission to provide a citable permanent DOI mirroring the GitHub release v1.0.0 (DOI: 10.5281/zenodo.XXXXXXX — to be minted at submission)."*
- PLOS Data Availability policy: data underlying the findings must be openly available to readers; "data will be deposited upon acceptance" is permitted **only** with a named repository and (ideally) a real accession. A fake `XXXXXXX` DOI satisfies neither.
- Mitigating fact: the same paragraph already points to a **real, public** GitHub repo (https://github.com/yyx-4113/cpsp-drg-spinal-repurposing, release v1.0.0) that contains all processed data, so the "available without restriction" bar is in fact met via GitHub.

【Why it matters】 PLOS's technical check will flag a placeholder DOI and may return the manuscript for correction or hold the data-availability sign-off. The risk is containable (GitHub already satisfies the core rule) but the wording must be fixed before upload.

【Specific fix】 Either:
- (a) **Mint the Zenodo DOI now** and insert the real one (preferred — gives a permanent, versioned mirror); **or**
- (b) Rephrase to remove the fake placeholder: *"All code, tables and figures are deposited in the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (release v1.0.0; integrity verifiable via MANIFEST.sha256). A versioned Zenodo archive mirroring this release will be deposited upon acceptance. Data are not 'available on request'."* Keep the explicit "not available on request" sentence (it is compliant and good).

---

### Issue 5 — Competing Interests vs ADRA2A emphasis: the "no target singled out" claim is undercut by the text

【Problem】 The Competing Interests statement asserts ADRA2A is discussed "uniformly" with all 10 targets and "no target is singled out," yet the manuscript foregrounds ADRA2A far more than any other target — and ADRA2A is a candidate target in the author's pending grant. This is a perceptible tension that weakens the credibility of the disclosure.

【Evidence】
- Competing Interests (L225): *"Biological-plausibility discussion is applied uniformly to all 10 docked targets (Table 3a) and no target is singled out for prioritisation, promotion, or exclusion."*
- Manuscript L112: a dedicated paragraph on the ADRA2A breadth flip (*"ADRA2A reached AUC 0.618 on the 620-drug CNS/analgesic-prior subset (Tier 1) but collapsed to 0.532 (p = 0.118…)"*).
- Manuscript L126: another dedicated ADRA2A paragraph (*"ADRA2A is neither prioritised nor excluded: it retains established α2A analgesic pharmacology and remains a plausible hypothesis…"*).
- Manuscript L90: *"the author has a pending grant in which ADRA2A is listed among candidate targets; this did not influence the present analyses."*
- The other 9 targets receive no comparable dedicated narrative; ADRA2A is the only target with its own exemplar paragraphs (the breadth flip and the composite-ranking discussion).

【Why it matters】 PLOS requires competing-interest disclosure to be credible. A statement that "no target is singled out" is directly contradicted by text that singles out exactly the pending-grant target. Even within an honest-null framing, this invites reviewer suspicion of undisclosed emphasis bias and may trigger an editor query.

【Specific fix】 Either:
- (a) Soften the competing-interests claim to be consistent with the text: *"ADRA2A is discussed at greater length than the other nine targets because it is the illustrative case for the two-filter rule (full-library AUC 0.532, p = 0.118, fails filter 1; size-independent BH q = 0.0025 passes filter 2 → inconclusive) and because the author's pending grant lists it as a candidate target. The author confirms this did not affect any analytical choice; all 10 targets were treated identically in the docking pipeline (Methods L160–L162; Table 3b).";* **or**
- (b) Reduce the ADRA2A narrative to parity with the other targets, keeping only the two-filter verdict as the worked example and moving the α2A-pharmacology commentary to a single sentence. The two-filter logic must be stated as the explicit reason for any emphasis.

---

### Issue 6 — No standalone "Conclusions" section (expected in PLOS ONE research-article structure)

【Problem】 The manuscript has a Discussion (L118–L129) but no separate "Conclusions" section heading. PLOS ONE's required research-article structure lists Conclusions as an expected section.

【Evidence】
- Manuscript section headings present: Introduction (L30), Results (L40), Discussion (L118), Methods (L132). No `## Conclusions` heading exists; the only "Conclusions" content is the abstract sub-heading (L20) and closing sentences of the Discussion.
- PLOS ONE author guidelines require a Conclusions section (it may be folded into Discussion, but a clearly identified conclusion is expected; the submission system's structural check looks for it).

【Why it matters】 Absence of a Conclusions section can trigger a formatting query or desk-level structural correction, delaying peer review. It is low-risk but trivially fixable.

【Specific fix】 Add a brief `## Conclusions` section (3–5 sentences) after Discussion, mirroring the abstract Conclusions (L20), e.g.:
> *"The DRG–spinal axis is a nerve-injury-associated, heterogeneity-sensitive transcriptional response rather than a CPSP-specific target; the full-library docking screen yields an honest null that defines a methodological boundary for repurposing in this field rather than a false lead. Prospective validation in human DRG/spinal or CSF biospecimens is the defined next step."*

---

### Issue 7 — The internal compliance check wrongly lists "Author Summary" as a required element

【Problem】 The PLOS ONE compliance check presents Author Summary as a mandatory manuscript element (✅ PASS), but PLOS ONE does **not** mandate an Author Summary — that is a PLOS Biology / Medicine / Computational Biology / Genetics item. The manuscript and cover letter correctly treat it as optional, so the error lives only in the compliance artifact, but it can mislead.

【Evidence】
- Compliance check §1 item 4: *"**Author Summary** (lay-audience summary) | ✅ PASS | Present, distinct from abstract, non-technical."* Listed among "Required manuscript elements."
- PLOS ONE submission guidelines: Author Summary is **optional**.
- Cover letter L13 (correct): *"The manuscript includes an Author Summary (optional under PLOS ONE policy), Data Availability, Ethics, Funding, Competing Interests, and Author Contributions statements."*

【Why it matters】 If the author/editor believes Author Summary is mandatory, they may over-invest in it or, conversely, fear a missing one is fatal. More importantly, this false "required" mark further erodes trust in the compliance check's other PASS claims (compounding Issues 2–3).

【Specific fix】 In the compliance check, change item 4 to: *"Author Summary (optional under PLOS ONE policy) — present; no action required."* Do not represent it as mandatory.

---

### Issue 8 — Residual "ScientificReports" branding in the manuscript body and the submission folder

【Problem】 Although the venue is PLOS ONE, the manuscript **body itself** still embeds a `MVP_ScientificReports_*` filename, and the project folder still contains multiple ScientificReports-named files (including a ScientificReports cover letter). This branding can confuse the editor or cause the wrong file to be uploaded.

【Evidence】
- Manuscript L283 (verified by search): *"**Supplementary Information** (separate file `MVP_ScientificReports_supplementary.md`; not counted toward the 8-item cap): …"* — the body references the supplementary file by its ScientificReports name.
- Folder search for "Scientific Reports"/"ScientificReports" returns, among others: `MVP_ScientificReports_submission.md`, `MVP_ScientificReports_supplementary.md`, `MVP_ScientificReports_cover_letter.md`, `MVP_ScientificReports_reporting_summary.md`, plus `_v14_source.md`, `_v15_source.md`, `P6_manuscript_draft.md`, and `MVP_PLOSONE_compliance_check.md` (which at L78 still names `reports/MVP_ScientificReports_submission.md`).
- The brief notes the pivot followed a Scientific Reports desk-reject; an editor receiving a file/screen branded "ScientificReports" may suspect parallel submission (which PLOS forbids) or carelessness.

【Why it matters】 PLOS explicitly forbids simultaneous submission and expects clean, venue-appropriate branding. A ScientificReports-named cover letter or body reference surviving in the PLOS ONE pack is a real desk-reject/query risk and an integrity smell.

【Specific fix】 Before upload: (1) rename source + generated files to `PLOSONE_submission.md` / `PLOSONE_supplementary.md` (and the docx to `Manuscript.docx` / `Supporting_Information.docx`); (2) update manuscript L283 to reference the renamed supplementary file; (3) remove or quarantine the ScientificReports-named cover letter, reporting summary, and `_v*_source.md`/`P6_manuscript_draft.md` from the upload set; (4) confirm the rendered docx contains no "Scientific Reports" string. The compliance check's "filename is cosmetic" reassurance (L78–L79) is inaccurate because the body (L283) embeds the name — so it is **not** purely cosmetic.

---

### Issue 9 — Ethics statement gives no IRB approval number; relies only on "documented in deposition"

【Problem】 The Ethics statement says GSE158825's IRB approval is "documented in deposition" but provides no approval/reference number. PLOS prefers the original ethics approval reference where available.

【Evidence】
- Manuscript L170: *"For the single human dataset reanalysed here, GSE158825 (human plasma miRNA, n = 60; lumbar surgery with pain outcome), the original deposition documents institutional review board (IRB) approval and informed consent, and the data were accessed in de-identified form; this secondary reanalysis required no further ethics approval."*
- No IRB committee name or approval number is given.
- PLOS ethics policy: for studies involving human participants, name the ethics committee and give the reference number; for secondary analyses of de-identified public data, state clearly that no further approval was required (which this does).

【Why it matters】 The statement is likely acceptable (secondary, de-identified), but its vagueness ("documented in deposition") may prompt an ethics-approval query during technical check. Citing the original approval reference removes the ambiguity.

【Specific fix】 Add the original study's ethics approval reference if retrievable from the GEO record, e.g.: *"GSE158825 was approved by [Institution] IRB (approval no. XXX) with written informed consent, as documented in the GEO deposition; this secondary reanalysis of de-identified data required no further ethics approval."* If the number is not retrievable, explicitly state: *"The original IRB approval is documented in the GSE158825 deposition; this reanalysis used de-identified data and required no additional approval."*

---

## § Stands up (things I suspected but found to be CORRECT)

1. **The structured abstract is compliant.** Recomputed word count of L14–L20 = **≈191 words** (the compliance check's "180 words" is slightly low but immaterial; both are well under PLOS's 300-word expectation). It uses the standard PLOS headings **Background / Methods / Results / Conclusions** (L14, L16, L18, L20) and contains **no citations** — fully compliant. (Verification: counted every token in L14–L20; confirmed no superscript/numbered reference in the abstract.)

2. **The AI-use disclosure is specific and compliant, in both places.** Manuscript L167 names the tool (*"A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing"*), states no AI generated/selected/interpreted data, and that no AI satisfies authorship. The cover letter L15 also discloses it (*"A large language model assisted language drafting; all scientific content is solely the author's"*). This meets PLOS's generative-AI disclosure policy.

3. **STROBE Item 14 is honestly handled.** The checklist (L24) correctly states the GSE158825 (n=60) human layer reports **only aggregate set-level permutation statistics**, that **no participant-level clinical descriptors are tabulated** because the deposition provides no per-participant covariates beyond case/control, and explicitly says participant-level descriptive tables are not applicable. It does **not** falsely claim participant-level descriptive stats exist. (Substance correct; only the status label "Addressed" could be tightened to "Addressed — aggregate genomic level; participant-level N/A," but it is not a false claim.)

4. **STROBE Item 5 (Setting) is correctly marked N/A with a real justification.** Checklist L15: marked "N/A (primary deposition)" with the reasoning that this is a secondary in-silico reanalysis with no physical site of its own. Appropriate and honest.

5. **All mandatory PLOS ONE sections are present and non-empty.** Verified in the manuscript: Title (L1), Author + affiliation + ORCID + email (L3–L6), Abstract (L12–L20), Introduction (L30), Methods (L132), Results (L40), Discussion (L118), References (L174–L209, 33 entries), Acknowledgements (L212), Funding (L215), Author Contributions (L218), Data Availability (L221), Competing Interests (L225), Ethics statement (L169). The GitHub Data Availability repo is real and public, satisfying "available without restriction," and the "not available on request" wording is present.

6. **Keywords are present and appropriate** (L28): chronic postsurgical pain, dorsal root ganglion, spinal cord, transcriptome meta-analysis, drug repurposing, single-cell transcriptomics, spatial transcriptomics, negative results — 8 well-chosen terms.

7. **The cover letter is otherwise sound:** it correctly labels Author Summary "optional" (L13), correctly states the article type as "Research Article" / "primary research" (L9), and matches the manuscript's negative framing (L11 emphasizes the honest docking null, not a positive finding). No over-claim of a positive result was found.

---

## § Questions for the authors

1. **Ethics:** What is the GSE158825 original IRB/ethics-committee approval number (and committee name), and can it be cited to strengthen L170? If not retrievable, confirm the stated "documented in deposition / no further approval required" position is the final one.
2. **Compliance check integrity:** The supplied `MVP_PLOSONE_compliance_check.md` counts 26 references while the manuscript has 33. Was the check run against an earlier draft? Can it be regenerated against the 33-reference file, and can the 7 references beyond its count (Kong, Scholz, Zhang Y, Luo, Xiao, Pushpakom, Irwin) each be confirmed for a DOI?
3. **Data Availability:** Will the Zenodo DOI be minted before submission (Issue 4a), or should the statement be rephrased to "upon acceptance" (Issue 4b)?
4. **Competing interests:** Confirm that ADRA2A's disproportionate narrative emphasis (L112, L126) is solely the two-filter illustrative example and that no analytical step — including the ADRA2A-specific composite-ranking metrics (L112) — was shaped by the pending grant. If so, is the softened disclosure in Issue 5(a) acceptable?
5. **Branding:** Confirm the `MVP_ScientificReports_*` files (including the separate `MVP_ScientificReports_cover_letter.md` and `MVP_ScientificReports_reporting_summary.md` found in the folder) will be excluded from the PLOS ONE upload set, and that L283 will be updated when the supplementary is renamed.

---

## § What I actually checked

**Files read (only these, per independence rules):**
- `reviews/round9_2026-09-26/_PANEL_BRIEF.md` (independence discipline, scope, output contract).
- `reports/MVP_ScientificReports_submission.md` — full read (L1–L150, then L150–L283).
- `reports/MVP_STROBE_checklist.md` — full read; cross-checked every item against the manuscript.
- `reports/MVP_PLOSONE_cover_letter.md` — full read.
- `reports/MVP_PLOSONE_compliance_check.md` — full read; its verifiable claims re-tested against the manuscript.

**Values recomputed / verified by me (not assumed):**
- **Abstract word count:** counted every token in L14–L20 = **≈191 words** (compliance check claimed 180; both < 300-word limit). Headings confirmed = Background/Methods/Results/Conclusions; no citations present.
- **Mandatory sections:** each located by line and confirmed non-empty (see § Stands up #5).
- **Reference count:** manually enumerated L176–L208 = **33 references** (compliance check claims 26 → mismatch, Issue 2).
- **STROBE Item 1:** searched the title (L1) for "meta-analysis" → **absent**; confirmed the checklist's quoted title phrase is not in the manuscript (Issue 1).
- **STROBE Item 14:** confirmed the checklist does **not** claim participant-level descriptive stats; it correctly limits GSE158825 to aggregate set-level statistics (Issue — none; stands up #3).
- **STROBE Item 5:** confirmed marked N/A with justification (stands up #4).
- **STROBE Item 22 / Funding:** confirmed content consistency but caught the wrong line citation "line 211" vs actual L215 (Issue 3).
- **Data Availability:** confirmed GitHub repo is real/public (satisfies "without restriction") and that the Zenodo DOI is a placeholder `XXXXXXX` (Issue 4).
- **AI disclosure:** confirmed present and specific in Methods L167 **and** cover letter L15 (stands up #2).
- **Competing Interests vs ADRA2A:** confirmed the "no target singled out" claim (L225) is contradicted by dedicated ADRA2A paragraphs at L112 and L126, with L90 noting the pending grant (Issue 5).
- **Branding:** searched the manuscript body for "Scientific Reports"/"ScientificReports" → **one hit, at L283**, the embedded supplementary filename `MVP_ScientificReports_supplementary.md`; folder search confirmed additional ScientificReports-named files including a separate cover letter (Issue 8).

**Discrepancies stated:**
- Compliance check reference count (26) vs manuscript (33) — unreconciled; the check appears stale/regenerated against an earlier draft.
- Compliance check line citations offset from the manuscript (Funding "211" vs 215; Abstract "7–21" vs 12–20).
- Compliance check item 4 mislabels Author Summary as required.
- Compliance check L78 still names `MVP_ScientificReports_submission.md`, contradicting its own "filename is cosmetic / PLOS-compliant" claim given the body embed at L283.

No other PLOS ONE mandatory elements were found missing. The manuscript is fundamentally venue-appropriate in content and framing (honest-negative, reproducible, well-sectioned); the defects above are correctable compliance/branding/integrity items, not substantive scientific flaws.
