# A4 — Venue / Reporting-Standard Audit (PLOS ONE editor + STROBE)

**Manuscript:** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null* (v1.2.0)
**Assigned role:** A4 — Venue / reporting-standard auditor (PLOS ONE editorial criteria + STROBE 2007 checklist)
**Review basis:** First-submission review. I did not read any prior review, response, revision, gate script, or manifest. All judgements are from the artefacts listed in the panel brief and from independent recomputation of the source PNG/docx files.
**Artefacts read:** `reports/MVP_PLOSONE_submission.md`, `reports/MVP_PLOSONE_supplementary.md`, `reports/MVP_STROBE_checklist.md`, `reports/MVP_PLOSONE_cover_letter.md`, `reports/MVP_PLOSONE_compliance_check.md`, `submission_pack/Manuscript.docx` (+ `Supporting_Information.docx`, `STROBE_Checklist.docx`, `Cover_Letter_PLOSONE.docx`), source PNGs in `figures/` and `submission_pack/`.

---

## Executive summary

The manuscript is, in substance, close to PLOS ONE–ready and is honestly positioned as a negative/null computational study — which is exactly the category PLOS ONE explicitly welcomes. The STROBE honesty reframing of the 45.7% "translatome-dependence" is correctly done. The hard-fail elements I could verify directly (abstract length, figure embedding, DPI, AI disclosure, data-availability/no-fabricated-DOI, competing interests, ethics, title length, journal-name/scope/version consistency in the cover letter) are all *present and correct*.

However, the **`MVP_PLOSONE_compliance_check.md` is not as accurate as its "Content is PLOS ONE–ready" verdict implies**. It contains at least one materially wrong number (abstract word count: it states 180; the source contains 256), one mislabelled figure/result in the STROBE checklist (Item 16 conflates Tier-1 AUC 0.618 with the full-library AUC 0.532 for ADRA2A), a stale instruction referencing a Zenodo placeholder that does **not** exist in the current manuscript, an internally unreliable DPI justification (it credits a "gate" that cannot measure DPI from a docx), and several imprecise numeric assertions (title char count 166 vs actual 143). None of these is individually a desk-reject, but they undermine the compliance document's authority and a few should be corrected before submission.

The only genuine *soft* desk-review risk is data-availability: the manuscript relies solely on a GitHub release (v1.2.0) and explicitly states "no Zenodo snapshot has been deposited." PLOS ONE prefers a DOI-minting, recognised public repository; GitHub-only is usually accepted but can draw an editor query. I recommend depositing a versioned Zenodo/figshare archive.

---

## 1. STROBE honesty — Item 19 and the 45.7% reframing

### 1.1 The 45.7% "translatome-dependence" is correctly reframed as a threshold/concordance artefact (PASS)

**【Problem】** The brief asked whether STROBE Item 19 still implies a biological finding the manuscript has retracted. It does **not** — the 45.7% figure is explicitly reframed as a counting/threshold artefact.

**【Evidence】** `reports/MVP_PLOSONE_submission.md` line 50 (Results, bulk-only sensitivity): *"the apparent 45.7% 'translatome-dependence' of gene-level membership is substantially a threshold/concordance-count artefact rather than a disappearance of the axis."* The same reframing is recorded in `reports/MVP_STROBE_checklist.md` Item 19: *"the apparent 45.7% 'translatome-dependence' of core membership reframed as a threshold/concordance-count artefact (Methods, Meta-analysis)."* I recomputed the arithmetic: primary core = 4,055; strict-gate bulk overlap = 2,202; non-overlap = 1,853; 1,853 / 4,055 = 0.45697 ≈ 45.7% — so the number is real, and the manuscript immediately qualifies it by noting the relaxed ≥3/4 gate recovers 3,587/4,055 = 88.5%.

**【Why it matters】** This is the exact trap the panel flagged: a retracted "biology" claim lingering in a reporting checklist. Here the checklist and the manuscript agree that 45.7% is a counting artefact, not a finding. No desk-reject or mis-reporting risk.

**【Specific fix】** No fix required. Optional polish: the noun "translatome-dependence" is a slight misnomer (the 45.7% is really "not confirmed by bulk under the strict gate," not literal dependence on the translatome). Since it already appears in scare quotes in both documents and is walked back, leave as-is or change to *"apparent translatome-only membership"* for precision.

### 1.2 Other STROBE items do not imply a retracted biology claim (PASS)

**【Problem】** Beyond Item 19, I checked whether any other STROBE answer smuggles in a retracted claim. None does.

**【Evidence】** Item 9 correctly records the *non-circular* translation test (incision held out) and the GSE265957 non-independence; Item 18 records the incision arm as a translation test, not as confirmation; Item 14 treats the human-miRNA layer as a null. The circular 69.5%/53.9% numbers are explicitly disowned in the manuscript (line 56) and the checklist does not present them as positive findings.

**【Why it matters】** Confirms the reporting checklist is aligned with the manuscript's honesty reframing throughout, not just at Item 19.

**【Specific fix】** None.

---

## 2. PLOS ONE hard-fail checks

### 2.1 Abstract word count: compliance_check says 180; source contains 256 (no hard fail, but compliance_check is wrong)

**【Problem】** `MVP_PLOSONE_compliance_check.md` §1 item 3 states the abstract is "180 words"; my independent count from the source markdown is **256 words**.

**【Evidence】** I extracted the block between `## Abstract` and `## Author Summary` in `reports/MVP_PLOSONE_submission.md`, stripped markdown bold markers, and tokenised: **256 words** (structured headings Background/Methods/Results/Conclusions included). The compliance_check's "180 words" is therefore inaccurate. However, PLOS ONE's abstract ceiling is ≤300 words, so 256 is still compliant — this is **not** a desk-reject and not a hard fail, but the compliance document's numeric claim is demonstrably wrong.

**【Why it matters】** A "final compliance check" that mis-states the abstract length by ~30% damages confidence in its other assertions (see §4). The manuscript itself is fine; only the compliance document needs correction.

**【Specific fix】** In `MVP_PLOSONE_compliance_check.md` §1 item 3, replace *"180 words"* with *"256 words"* (verified against the source markdown; ≤300, compliant).

### 2.2 Figure legends complete (PASS)

**【Problem】** Confirm whether every figure has a complete legend.

**【Evidence】** `reports/MVP_PLOSONE_submission.md` "Display items" (lines 287–302) provides a full legend for Fig. 1–5, each describing all panels (Fig. 2 A/B, Fig. 4 A/B, Fig. 5 A/B/C) and citing source files. No panel is left unexplained.

**【Why it matters】** Incomplete legends are a common PLOS ONE desk-query; here they are complete.

**【Specific fix】** None.

### 2.3 Figure resolution ≥300 DPI: source PNGs are 350.012 DPI — verdict TRUE, but compliance_check's evidence is unsound

**【Problem】** The compliance_check claims "All 5 figures = 350.012 DPI (gate_word ALL PASS)." The panel brief correctly notes a docx does **not** store DPI, so a gate reading the docx cannot verify DPI. I therefore verified the *source PNGs* directly.

**【Evidence】** Reading the PNG metadata in `figures/` (and `submission_pack/`):
- Fig1_geneset_programme.png → dpi (350.012, 350.012), 2516×1517 px
- Fig2_hub_convergence.png → dpi (350.012, 350.012), 2834×1679 px
- Fig3_DRG_neuron_subtype_localisation.png → dpi (350.012, 350.012), 2208×2109 px
- Fig4_spinal_lineage_visium.png → dpi (350.012, 350.012), 2814×1691 px
- Fig5_docking_honest_null.png → dpi (350.012, 350.012), 2472×1622 px

All five are genuinely 350.012 DPI, comfortably above the 300-DPI floor (and above PLOS ONE's preferred 300). The *conclusion* of the compliance_check is therefore correct against the real artefacts.

**【Why it matters】** The DPI hard-fail is satisfied. But the compliance_check credits "gate_word ALL PASS" as the evidence — and per the panel brief a gate on a docx cannot measure DPI; the only valid evidence is the PNG metadata, which I confirmed. The compliance_check's reasoning is unsound even though its number happens to be right.

**【Specific fix】** In `MVP_PLOSONE_compliance_check.md` §2, change the DPI evidence note from *"(gate_word ALL PASS)"* to *"(verified on source PNG metadata: 350.012 DPI for all five figures; docx does not store DPI, so the PNGs — not the docx — are the source of record)."*

### 2.4 Figures embedded in the docx (PASS)

**【Problem】** Confirm the five figures are actually embedded (not merely referenced) in `Manuscript.docx`.

**【Evidence】** `python-docx` on `submission_pack/Manuscript.docx`: `len(d.inline_shapes) == 5`. This matches "5 figures + 3 tables" and the manuscript's Fig. 1–5. So all five are embedded as inline shapes.

**【Why it matters】** A docx with figure *references* but no embedded images would fail PLOS ONE's "figures embedded" expectation (and the separate-file upload requirement). Here the embedding is confirmed.

**【Specific fix】** None. (Separately, remember PLOS ONE's upload system wants the five PNGs as individual files — `submission_pack/` already contains them; rename to `Fig1.png`…`Fig5.png` at upload, as the compliance_check §2 already notes.)

### 2.5 AI-use disclosure present and correctly placed (PASS)

**【Problem】** PLOS ONE requires an AI-use statement; verify presence and placement.

**【Evidence】** `Manuscript.docx` text contains *"A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing"* (under Methods → "Statistical discipline, causal scope and AI-use disclosure"), plus the explicit statement that no AI tool satisfies authorship criteria. The cover letter likewise discloses it ("A large language model assisted language drafting; all scientific content is solely the author's"). The disclosure names the specific model and reaffirms human authorship — which exceeds PLOS ONE's minimum.

**【Why it matters】** AI-use non-disclosure is a policy violation at PLOS ONE; here it is present, specific, and correctly placed (Methods, not buried).

**【Specific fix】** None.

### 2.6 Data-availability: GitHub v1.2.0, NO fabricated DOI (PASS on the no-fabrication test; soft risk on repository type)

**【Problem】** Verify the data-availability statement points to GitHub v1.2.0 with no fabricated DOI, and assess PLOS ONE acceptability.

**【Evidence】** `reports/MVP_PLOSONE_submission.md` Data Availability (lines 270–275): repository `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`, released as **v1.2.0**; explicitly *"no Zenodo snapshot has been deposited. Data are therefore available from the versioned GitHub release, not on request"* and *"Data are not 'available on request'."* The 12 GEO accessions are public. There is **no** `10.5281/zenodo.XXXXXXX` placeholder anywhere in the manuscript — I grepped the whole file. So the "no fabricated DOI" test is satisfied.

**【Why it matters】** A fabricated/placeholder DOI would be a serious integrity red flag; none exists. The softer risk: PLOS ONE's data policy prefers deposit in a recognised, DOI-minting public repository; a GitHub release alone is usually accepted but can prompt an editor query, especially because the manuscript itself advertises the absence of a Zenodo snapshot. This is not a desk-reject but a likely "minor revision / clarification" request.

**【Specific fix】** Strongly recommended: deposit a versioned Zenodo (or figshare/OSF) archive of the v1.2.0 release and cite its real DOI in the Data Availability statement; OR, if staying GitHub-only, add one sentence justifying GitHub as the permanent public archive and confirming the release tag is immutable. Do **not** introduce a `10.5281/zenodo.XXXXXXX` placeholder — the compliance_check §4 still tells you to "replace the placeholder," but no placeholder exists in the current text (see §4.3).

### 2.7 Competing-interests statement present and consistent (PASS)

**【Problem】** Verify a competing-interests statement exists and is internally consistent.

**【Evidence】** `reports/MVP_PLOSONE_submission.md` "Competing interests" (lines 277–278): declares no financial competing interests; discloses a pending Fujian Natural Science Foundation grant in which ADRA2A is listed among candidate targets, and states it did not fund/influence the analysis. The cover letter repeats this. The disclosure is consistent with the Results/Discussion, where ADRA2A is discussed at greater length precisely because it is the illustrative two-filter case *and* a grant-listed target.

**【Why it matters】** Missing or contradictory competing-interests statements are PLOS ONE policy violations; here it is present, specific, and non-contradictory.

**【Specific fix】** None.

### 2.8 Ethics statement: public GEO data, human/animal declarations correct and non-contradictory (PASS)

**【Problem】** Verify the ethics statement correctly covers the single human dataset (GSE158825) and the animal datasets, and contains no contradiction.

**【Evidence】** `reports/MVP_PLOSONE_submission.md` Ethics statement (lines 177–178): for GSE158825 (human plasma miRNA, n = 60) it states IRB approval and informed consent are documented in the original GEO deposition and that the secondary reanalysis required no further approval; for the nine animal/in-vitro datasets it states IACUC approvals are documented in the original depositions and no new animal data were generated. The STROBE checklist (Item 5, Item 22) echoes the same. There is no claim of new human/animal data, no contradiction between "public de-identified data" and "IRB documented," and no overstatement of local approval.

**【Why it matters】** PLOS ONE has a mandatory ethics statement; an incorrect or contradictory one (e.g., claiming IRB approval the authors themselves hold for *reanalysed* public data) would be a problem. Here the statement correctly delegates primary approval to the depositors and asserts only the secondary-analysis exemption.

**【Specific fix】** None. (Optional: the manuscript does not print the GSE158825 IRB identifier, which is fine because it resides in the deposit; no change needed.)

---

## 3. Cover letter vs manuscript

### 3.1 Journal name, scope claim, and version are all consistent (PASS)

**【Problem】** Desk-reject risk if the cover letter names the wrong venue, mis-states scope, or disagrees on version.

**【Evidence】** Cover letter (`reports/MVP_PLOSONE_cover_letter.md`) addresses *"the Editorial Board of PLOS ONE"* (line 7) and proposes *"Research Article"*; the manuscript title and Data Availability match. Scope claim (line 11): *"PLOS ONE's editorial criteria evaluate scientific rigour and reproducibility rather than perceived novelty or impact, and the journal explicitly welcomes transparent negative and null results"* — this is an accurate description of PLOS ONE policy. Version: cover letter line 13 states the repo is released as **v1.2.0**; the manuscript Data Availability also states **v1.2.0**. ADRA2A numbers in the cover letter ("Tier-1 AUC 0.618 collapses to 0.532, p = 0.118") match the manuscript exactly.

**【Why it matters】** No venue/scope/version mismatch → no desk-reject on these grounds.

**【Specific fix】** None.

### 3.2 Cover letter correctly states ADRA2A numbers — unlike the STROBE checklist (see §6.1)

**【Problem】** The cover letter gets the ADRA2A Tier-1 vs full-library AUC right, which the STROBE checklist (Item 16) does not.

**【Evidence】** Cover letter line 11: *"ADRA2A Tier-1 AUC 0.618 collapses to 0.532, p = 0.118."* Correct. Contrast with STROBE Item 16 (§6.1), which mislabels 0.532 (full-library) as "Tier-1."

**【Why it matters】** Confirms the manuscript itself is internally consistent on this point; only the STROBE checklist entry is wrong.

**【Specific fix】** None for the cover letter; fix the STROBE checklist per §6.1.

---

## 4. `MVP_PLOSONE_compliance_check.md` accuracy

### 4.1 Abstract word count is wrong (180 vs 256) — already covered in §2.1

See §2.1. The "Content is PLOS ONE–ready" headline is undercut by this demonstrable error.

### 4.2 Title character count is wrong (166 vs 143)

**【Problem】** The compliance_check §1 item 1 states the title is "166 chars"; my count is **143 characters**.

**【Evidence】** Title (line 1 of the manuscript): *"Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null"* — character length (including spaces) = **143**. It is still ≤250, so no failure, but the compliance_check's number is off.

**【Why it matters】** Reinforces that the compliance_check's numeric assertions were not recomputed against the current file; lowers trust in its other "PASS" ratings.

**【Specific fix】** Change *"166 chars"* to *"143 chars"* in §1 item 1.

### 4.3 Stale Zenodo instruction references a placeholder that does not exist

**【Problem】** `MVP_PLOSONE_compliance_check.md` §4 instructs: *"replace the 10.5281/zenodo.XXXXXXX placeholder in the Data Availability statement with the minted DOI."* No such placeholder exists in the current manuscript.

**【Evidence】** I searched `reports/MVP_PLOSONE_submission.md` for "zenodo"/"10.5281"; the only occurrences are the Data Availability statement's explicit *"no Zenodo snapshot has been deposited"* (line 273) and the compliance_check's own §4. There is no `10.5281/zenodo.XXXXXXX` string anywhere in the manuscript.

**【Why it matters】** The compliance_check describes a manuscript state that is not the current one. An editor or author following §4 literally would hunt for a placeholder that was already removed — a sign the compliance document was not regenerated against the final text.

**【Specific fix】** Replace the §4 bullet with an accurate instruction: *"Optional but recommended: deposit a versioned Zenodo/figshare archive of v1.2.0 and add its real DOI to the Data Availability statement. The current manuscript intentionally relies on the immutable GitHub v1.2.0 release and states no Zenodo snapshot exists; do NOT introduce a placeholder DOI."*

### 4.4 DPI justification credits an incapable gate (covered in §2.3)

See §2.3 — the DPI *conclusion* is correct (verified on PNGs) but the cited *evidence* ("gate_word ALL PASS") cannot measure DPI from a docx.

### 4.5 "37/37 Crossref-verified DOI" — credible on spot-check, but dated and should be re-verified

**【Problem】** The compliance_check asserts all 37 references carry a Crossref-verified DOI and admits this verification dates to Round 9.

**【Evidence】** The reference list indeed contains 37 entries, each with a `https://doi.org/...` URL, and I independently spot-checked three of the most recent/suspicious DOIs via web search:
- Ref 22 — Divito AE et al., *Cleveland Clinic Journal of Medicine* **93**(2):94–98 (2026), doi:10.3949/ccjm.93a.25087 → **real, matches**.
- Ref 23 — Bertoch T et al., *Anesthesiology* **142**(6):1085–1099 (2025), doi:10.1097/ALN.0000000000005460 → **real, matches**.
- Ref 7 — Dong FL et al., *Communications Biology* **8**:70 (2025), doi:10.1038/s42003-025-07506-0 → **real, matches**.

All three resolve to the exact articles cited, so the 37/37 claim is, at minimum, credible for the sampled items. The compliance_check's own provenance note (§3) says the verification is "validated as of [Round 9] and should be re-verified only if the reference list is subsequently edited; no reference was added or removed in the present T2/T3 pass." That caveat is honest, but because the compliance_check is being used as the submission gate, a fresh independent check is warranted.

**【Why it matters】** A single dead/wrong DOI would not be a desk-reject but would trigger a correction request; the claim's age (Round 9) means it should be re-confirmed against the final reference list.

**【Specific fix】** Before submission, re-run a Crossref batch check on all 37 DOIs and confirm none 404; record the date. No change to the manuscript is needed unless a DOI fails.

### 4.6 Reference journal names and Vancouver ordering — verified acceptable

**【Problem】** Whether all journal names are full (no abbreviations) and references are numbered in first-citation order.

**【Evidence】** I scanned all 37 references in `reports/MVP_PLOSONE_submission.md`; every journal name is spelled out in full PLOS style (e.g., *Proceedings of the National Academy of Sciences of the United States of America*, not PNAS; *British Journal of Anaesthesia*, not BJA). Inline citation order in the Introduction runs ¹→²→³→⁴→⁵→⁶→⁷→⁸→⁹, then ¹⁰–¹⁸ first appear together in Results in ascending order, consistent with Vancouver numbering. No obvious out-of-order citation was found.

**【Why it matters】** Abbreviated journal names or mis-ordered references are routine PLOS ONE formatting queries; here they appear clean.

**【Specific fix】** None (re-confirm during the DOI re-check in §4.5).

---

## 5. Title / abstract / keywords alignment with PLOS ONE scope

### 5.1 Honest null positioning is consistent with PLOS ONE's explicit welcome of negative results (PASS)

**【Problem】** Whether the manuscript is over-claimed or honestly positioned for a venue that welcomes null results.

**【Evidence】** The title contains *"an honest repurposing null"*; the abstract's Conclusions state *"the docking null is a methodological boundary, not a false lead"*; the keyword list (line 28) includes *"negative results"*; the Discussion repeatedly declines to recommend any drug and disclaims causal/clinical claims. The manuscript never asserts CPSP-specificity (it explicitly says the axis is *not shown* to be CPSP-specific and that this rests on a single heterogeneous incision arm). This is exactly the transparent negative-result framing PLOS ONE solicits.

**【Why it matters】** Over-claiming (e.g., implying a drug target or a CPSP mechanism) would be the main scope mismatch; the manuscript avoids it. Alignment with venue scope is strong.

**【Specific fix】** None. (Maintain this discipline; do not let the "35 hubs" or "dorsal-horn localisation" language drift into therapeutic implication — the Discussion already guards this.)

### 5.2 Keywords present and appropriate (PASS)

**【Problem】** Verify keywords exist and are relevant.

**【Evidence】** Line 28 lists 8 keywords: *chronic postsurgical pain, dorsal root ganglion, spinal cord, transcriptome meta-analysis, drug repurposing, single-cell transcriptomics, spatial transcriptomics, negative results.* All relevant; "negative results" appropriately signals the manuscript's contribution type.

**【Why it matters】** Missing/irrelevant keywords are a minor indexing issue; here they are fine.

**【Specific fix】** None.

---

## 6. Reporting-checklist mis-ticks / contradictions

### 6.1 STROBE Item 16 mislabels ADRA2A's AUC (Tier-1 0.618 vs full-library 0.532) — ERROR

**【Problem】** STROBE Item 16 states *"full-library docking null (ADRA2A Tier-1 AUC 0.532, p = 0.118 NS)"*, conflating the Tier-1 subset AUC with the full-library AUC.

**【Evidence】** `reports/MVP_STROBE_checklist.md` Item 16 (line 26) writes *"ADRA2A Tier-1 AUC 0.532, p = 0.118 NS."* But the manuscript is explicit and consistent that Tier-1 = **0.618** and full-library = **0.532** (p = 0.118): see `reports/MVP_PLOSONE_submission.md` line 114 (*"ADRA2A reached AUC 0.618 on the 620-drug CNS/analgesic-prior subset (Tier 1) but collapsed to 0.532 (p = 0.118, NS) across all 3,085 drugs"*) and Table 3b (line 368, ADRA2A row: "Full-library AUC 0.532"). The cover letter (§3.2) also gets it right. So the STROBE checklist's Item 16 sentence is factually wrong: 0.532 is the **full-library** AUC, not the Tier-1 AUC.

**【Why it matters】** A reporting-checklist entry that contradicts the manuscript on a headline result is exactly the "mis-ticked item" the panel asked me to catch. It would mislead an editor skimming the STROBE answers and undermines the checklist's reliability.

**【Specific fix】** In `MVP_STROBE_checklist.md` Item 16, replace *"full-library docking null (ADRA2A Tier-1 AUC 0.532, p = 0.118 NS)"* with: *"full-library docking null (ADRA2A full-library AUC 0.532, p = 0.118 NS; Tier-1 subset AUC 0.618 — the breadth flip is the point)."*

### 6.2 STROBE checklist line-citations are systematically offset from the manuscript (reliability concern)

**【Problem】** Many STROBE items cite "line N" locators that do not match the manuscript's actual line numbers, suggesting the checklist was written against an older layout.

**【Evidence】** Examples:
- Item 8 cites *"12 codes listed line 129"* — in the current manuscript the 12 GEO accessions appear in the Data curation paragraph (≈ line 143), not 129.
- Item 15 cites the human-miRNA outcome at *"line 149"* — the human miRNA layer is in Methods at ≈ line 162–163, not 149; line 149 is inside the fixed-effect meta-analysis Methods.
- Item 22 (Funding) cites *"line 211"* — the Funding section is at ≈ line 264.
- Item 5 (Setting) cites the Ethics statement at *"line 164"* — it is at ≈ line 178.
- Item 1 cites metadata at *"line 8"* — this one is correct (line 8 is the metadata block).

The pattern (several citations ~14–50 lines off) indicates the checklist was not re-anchored to the final manuscript. None of these is a scientific error, but they reduce the checklist's value as a navigational aid for editors/reviewers.

**【Why it matters】** A STROBE checklist whose internal line pointers are wrong looks unmaintained and can hide a genuine mis-tick (as in §6.1). It should be regenerated against the final file.

**【Specific fix】** Either (a) re-number all "line N" references against the final `MVP_PLOSONE_submission.md`, or (b) replace specific line pointers with section names (e.g., "Methods → Data curation", "Ethics statement") which are layout-stable. Option (b) is lower-maintenance.

### 6.3 STROBE is a stretch for a purely in-silico reanalysis; the choice should be justified

**【Problem】** STROBE 2007 is designed for primary observational studies (cohort/case-control/cross-sectional). This manuscript is a computational meta-analysis/reanalysis of public transcriptomes with no primary "participants," "setting," "recruitment," or "follow-up" in the observational sense; several items (5, 6, 13, 14) are marked N/A by delegating to "primary deposition."

**【Evidence】** `reports/MVP_STROBE_checklist.md` lines 5–7 and Items 5/6/13/14 explicitly mark design/recruitment/flow/descriptive-participant items N/A (primary deposition). The checklist's own header acknowledges this is a "secondary, in-silico reanalysis."

**【Why it matters】** Using STROBE for an in-silico transcriptome meta-analysis is defensible but imperfect; an editor or EQUATOR-minded reviewer may ask why STROBE (rather than a meta-analysis or transcriptomics reporting standard) was chosen, and whether the N/A delegations are appropriate. It is not a hard fail, but the rationale should be stated up front so the N/A items are not read as evasions.

**【Specific fix】** Add one sentence to the STROBE checklist's introductory paragraph: *"STROBE is applied here by analogy as the observational-reporting checklist closest to this reanalysis of a single human observational cohort (GSE158825); items concerning primary study design/recruitment/follow-up are marked N/A (primary deposition) because they are not under the control of a secondary reanalysis of de-identified public data."* Optionally note that no EQUATOR checklist is mandated for computational studies by PLOS ONE.

---

## 7. Additional minor venue notes (non-blocking)

### 7.1 Manuscript metadata block vs PLOS ONE "Author Summary" convention

**【Problem】** The manuscript includes an "Author Summary" (line 24) and a separate keyword line (line 28); PLOS ONE treats Author Summary as optional and keywords as required. Both are present and correctly placed. No action.

### 7.2 "Display items" count language

**【Problem】** The manuscript declares "5 figures + 3 tables = 8 enumerated main display items." PLOS ONE does not cap display items, so this is fine; the "enumerated" framing is clear.

### 7.3 Supplementary material labelling

**【Problem】** The supplementary document is a set of seven tables (S1–S7) plus the STROBE as S8. PLOS ONE requires each supplementary file to be labelled S1, S2, … The compliance_check §4 notes uploading as S1…S8. Confirm at upload that the STROBE checklist is indeed designated S8 and the seven tables S1–S7, matching the in-manuscript cross-references (e.g., "Supplementary Table S2"). No discrepancy found in the text.

---

## § Stands up (things I suspected were wrong but found correct)

1. **The 45.7% "translatome-dependence" is NOT presented as biology in the STROBE checklist.** I expected a lingering retracted claim; instead Item 19 explicitly reframes it as a threshold/concordance-count artefact, matching the manuscript. (Evidence: `MVP_STROBE_checklist.md` Item 19; `MVP_PLOSONE_submission.md` line 50.)
2. **Figure DPI genuinely meets the 300 floor.** I expected the "350 DPI" claim to be unverifiable (docx doesn't store DPI) and possibly false; direct PNG-metadata inspection shows all five are 350.012 DPI. (Evidence: PNG `dpi` tuples in `figures/`.)
3. **All five figures are actually embedded in the docx** (5 inline shapes), not just referenced. (Evidence: `len(d.inline_shapes) == 5` on `Manuscript.docx`.)
4. **The AI-use disclosure is present, specific (names Claude/Anthropic), and correctly placed in Methods**, exceeding PLOS ONE's minimum — no non-disclosure risk. (Evidence: `Manuscript.docx` text; cover letter.)
5. **No fabricated/placeholder DOI in the Data Availability statement** — the repository is a real GitHub v1.2.0 release, and the manuscript explicitly states no Zenodo snapshot exists. (Evidence: grep of `MVP_PLOSONE_submission.md`; no `10.5281/zenodo.XXXXXXX` string.)
6. **The single human-dataset ethics declaration is correct and non-contradictory** (IRB/consent in original GEO deposit; secondary-reanalysis exemption asserted; no new human/animal data). (Evidence: Ethics statement lines 177–178; STROBE Items 5/22.)
7. **Cover letter is consistent with the manuscript** on journal name (PLOS ONE), scope claim (welcomes null results — true), version (v1.2.0), and ADRA2A numbers. (Evidence: cover letter lines 7, 11, 13 vs manuscript.)
8. **Three spot-checked recent reference DOIs (refs 7, 22, 23) resolve to the exact cited articles**, supporting the compliance_check's 37/37 claim. (Evidence: web verification of doi:10.1038/s42003-025-07506-0, doi:10.3949/ccjm.93a.25087, doi:10.1097/ALN.0000000000005460.)

---

## § Questions for the authors (I do not guess the answers)

1. **STROBE applicability:** Do you intend STROBE as the definitive reporting guideline, or would you prefer to also cite/justify a transcriptomics/meta-analysis standard? (Relevant to §6.3.)
2. **Data repository:** Will you deposit a DOI-minting archive (Zenodo/figshare/OSF) of the v1.2.0 release before submission, or deliberately remain GitHub-only? (Relevant to §2.6 / §4.3.) If GitHub-only, can you confirm the v1.2.0 release tag is immutable?
3. **STROBE Item 16 correction:** Will you correct the ADRA2A AUC mislabel (Tier-1 0.618 vs full-library 0.532) in the checklist? (Relevant to §6.1.)
4. **Line re-anchoring:** Can the STROBE checklist's "line N" pointers be re-derived against the final manuscript, or converted to section names? (Relevant to §6.2.)
5. **Reference DOI re-verification:** Has the 37-reference DOI set been re-checked against Crossref since Round 9, given the compliance_check itself dates that verification? (Relevant to §4.5.)

---

## § What I actually checked

**Files read (full):**
- `reports/MVP_PLOSONE_submission.md` (375 lines; abstract/results/methods/tables/display items/statements)
- `reports/MVP_PLOSONE_supplementary.md` (302 lines; S1–S7)
- `reports/MVP_STROBE_checklist.md` (34 lines; Items 1–22)
- `reports/MVP_PLOSONE_cover_letter.md` (25 lines)
- `reports/MVP_PLOSONE_compliance_check.md` (86 lines)
- `submission_pack/Manuscript.docx` (inspected via python-docx: inline shapes, full text search for AI-disclosure keywords)
- Source PNGs in `figures/` and `submission_pack/` (DPI + pixel dimensions)

**Commands / recomputations run (independent of any gate script):**
- Extracted the abstract block from the markdown and tokenised → **256 words** (compliance_check claims 180). Both ≤300; no hard fail, but the compliance_check number is wrong.
- Counted the title length → **143 characters** (compliance_check claims 166).
- Read PNG `dpi` metadata for all five figures → all **350.012 DPI** (verified independently of the docx, which cannot store DPI).
- Counted `inline_shapes` in `Manuscript.docx` → **5** (all five figures embedded).
- Searched `Manuscript.docx` text for AI-disclosure keywords → "generative AI", "Claude", "Anthropic", "AI language" all present.
- Grepped `MVP_PLOSONE_submission.md` for "zenodo"/"10.5281" → only the explicit "no Zenodo snapshot has been deposited" sentence; **no placeholder exists** (contradicting compliance_check §4).
- Verified the ADRA2A AUC numbers in the manuscript (Tier-1 0.618, full-library 0.532, p = 0.118) against the abstract, Results line 114, Table 3b line 368, and the cover letter → manuscript/cover letter consistent; **STROBE Item 16 mislabels 0.532 as "Tier-1."**
- Recomputed the 45.7% arithmetic: 4,055 − 2,202 = 1,853; 1,853 / 4,055 = 0.45697 → confirms the number and its artefactual reframing.
- Spot-checked three recent reference DOIs (refs 7, 22, 23) via web search → all resolve to the exact cited articles.

**Discrepancies found vs the compliance_check / artefacts:**
- Abstract word count: compliance_check "180" vs my "256" (manuscript compliant either way).
- Title char count: compliance_check "166" vs my "143" (compliant either way).
- DPI evidence: compliance_check credits "gate_word" (incapable of measuring DPI from a docx); my PNG check confirms the 350.012 DPI conclusion is still true.
- Zenodo placeholder: compliance_check §4 tells you to replace a placeholder that does not exist in the manuscript.
- STROBE Item 16: mislabels ADRA2A's full-library AUC (0.532) as "Tier-1."
- STROBE line-citations: systematically offset from the final manuscript (e.g., Item 8 "line 129" for the 12 accessions; Item 22 "line 211" for Funding; Item 5 "line 164" for Ethics) → checklist not re-anchored to final layout.

**No discrepancy found** on: journal name / scope / version consistency between cover letter and manuscript; AI-disclosure presence and placement; no-fabricated-DOI data availability; competing-interests statement; ethics statement correctness; figure-legend completeness; reference journal-name spelling (all full); overall honest-null positioning vs PLOS ONE scope.

---

*Prepared as reviewer A4 on 2026-09-27. Independence maintained: no prior review, response, revision, gate output, manifest, or sibling round-12 file was read.*
