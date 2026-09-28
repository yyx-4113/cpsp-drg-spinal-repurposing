# A4 — Venue & Reporting-standards audit (PLOS ONE, independent panel)

**Auditor role:** PLOS ONE handling-editor persona + STROBE reporting-checklist auditor.
**Manuscript under review:** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null* (single author, Yang Y).
**Mandate:** find PLOS ONE format hard-fails and reporting-honesty issues that would trigger a technical-check rejection or editorial return, and verify internal consistency of the submission package.

**Independence statement:** I did not read any sibling review/response/round files, the author's self-compliance document, the submission manifest, the reporting summary, or any archive/`.bak` file. Every judgement below comes from the artefacts I opened directly: the manuscript markdown, the supplementary markdown, the STROBE checklist markdown, the cover letter markdown, and the `Manuscript.docx` package (inspected as a zip, `word/media/` and `word/document.xml`), plus a live verification of the GitHub repository at tag `v1.6.0`.

---

## Executive verdict

The submission is, on the whole, exceptionally well-prepared for a PLOS ONE technical check: the Abstract is compliant, the five figures are genuinely embedded inline at 350 DPI, the Data Availability statement names a real, verified repository with no "available on request" wording and no fabricated Zenodo DOI, the AI-use disclosure is present and correct, and the competing-interests treatment of the pending ADRA2A grant is adequate. No reporting-honesty falsification was found; the "honest null" framing is internally consistent throughout.

**One genuine format hard-ish fail** was found: **the reference list is not numbered consecutively in the order of first citation**, which violates a stated PLOS ONE requirement and will generate a technical-check/editorial-return query (renumbering required). Two minor/verify items are also noted. None of these are grounds for outright rejection, but the reference-ordering item must be corrected before the manuscript can clear the technical check.

---

## Mandatory checks (PLOS ONE hard requirements)

| # | Check | Result |
|---|-------|--------|
| 1 | Abstract: single unstructured paragraph, ≤300 words, no labels | **PASS** |
| 2 | Author Summary present & accurate | **PASS** |
| 3 | Display-item count consistent (5 fig + 3 tbl) | **PASS** |
| 4 | Figures embedded in docx at ≥300 DPI | **PASS** |
| 5 | Data Availability: real URL, not "on request", no fabricated Zenodo, named files exist | **PASS** |
| 6 | CC BY stated | **PARTIAL** (declared in cover letter; absent from manuscript body — low risk) |
| 7 | References numbered, with titles + DOIs, callouts match | **PARTIAL** (all present & resolvable, but numbering order violated) |
| 8 | Competing interests / Ethics / Funding / Author contributions present & consistent | **PASS** |
| 9 | Cover letter ↔ manuscript consistency (v1.6.0, Author Summary mandatory, CC BY) | **PASS** |
| 10 | STROBE: all 22 items addressed or justified N/A | **PASS** |
| 11 | AI-use disclosure present; no AI authorship | **PASS** |

---

## Problems found

### P1 — References are not numbered in the order of first citation (format hard-fail / technical-check query)

【Problem】 The 40-item reference list is numbered by some internal order, not by the order in which each item is first cited in the text, contrary to PLOS ONE's required reference style.

【Evidence】 In the manuscript source (`reports/MVP_PLOSONE_submission.md`), first-appearance character offsets of the in-text citations (excluding the statistical "I²" symbol) are: ref **1** first cited at offset 4084 (Introduction: "healthcare cost¹"); ref **21** at 39747; ref **38** at 40300 ("…underlies gabapentinoid efficacy³⁸"); ref **40** at 40370 ("…SMIR-evoked hypersensitivity⁴⁰"); but ref **22** is not first cited until offset 47814 (Discussion: "…suzetrigine²²"). Thus refs 38 and 40 are first mentioned *before* refs 22–37. The computed first-appearance order is `[1…21, 38, 40, 22, 23, 26, 24, 25, 27…37, 39]`, which is not the consecutive sequence `1…40`.

【Why it matters】 PLOS ONE's instructions to authors state: *"References should be numbered consecutively in the order they are first mentioned in the text."* A violation triggers a technical-check/editorial-return query ("References are not in numerical order") and the manuscript cannot be accepted until the list is renumbered and all 40 in-text callouts are updated. It is a required fix, not a rejection, but it will block acceptance and forces a round-trip.

【Specific fix】 Renumber the reference list so that each number equals its rank of first appearance, and rewrite every in-text callout to match. The required current→new mapping (current number → new number) is:

```
1–21   → 1–21   (unchanged)
38     → 22
40     → 23
22     → 24
23     → 25
26     → 26
24     → 27
25     → 28
27     → 29
28     → 30
29     → 31
30     → 32
31     → 33
32     → 34
33     → 35
34     → 36
35     → 37
36     → 38
37     → 39
39     → 40
```

Concretely: the current ref 38 (Chen 2018, α2δ-1/gabapentinoid, *Cell Reports*) and current ref 40 (Flatters 2010, *Neuroscience Letters*) must become refs 22 and 23; current refs 22–37 shift down by two (current 22 → 24, …, current 37 → 39); current ref 39 (Flatters 2008) becomes 40. Apply the identical shift to every superscript callout in the body.

---

### P2 — Manuscript body does not itself state the CC BY license (minor / verify)

【Problem】 PLOS ONE requires the article to be published under CC BY, but the license is declared only in the cover letter, not echoed anywhere in the manuscript file.

【Evidence】 `MVP_PLOSONE_cover_letter.md:13` states *"upon acceptance will be published under the Creative Commons Attribution (CC BY) license."* A search of `reports/MVP_PLOSONE_submission.md` for "CC BY" / "Creative Commons" returns **no matches** (the manuscript has Ethics, Funding, Author contributions, Data availability, Competing interests, but no license line).

【Why it matters】 PLOS ONE captures the license selection in the submission system, so this is **not** a hard reject; however, some editorial offices expect the chosen license to be evident in the submission package. Leaving it only in the cover letter is a low-risk, easily-fixed gap.

【Specific fix】 Either (a) keep as-is (license is correctly asserted in the cover letter and will be set at acceptance), or (b) add a one-line statement to the manuscript, e.g. under "Additional Information": *"This article will be published under the Creative Commons Attribution (CC BY) license."* Option (b) removes any ambiguity.

---

### P3 — Author Summary slightly over-flattens the docking verdict vs the manuscript's ADRA2A nuance (minor consistency note)

【Problem】 The Author Summary states the screen "found no drug target that held up reliably," whereas the manuscript's own verdict is more carefully bounded: no target clears *both* filters, and ADRA2A is explicitly "inconclusive" because it *passes* the size-independent filter (BH q = 0.0025) while failing the full-library filter.

【Evidence】 `reports/MVP_PLOSONE_submission.md:20` (Author Summary): *"…found no drug target that held up reliably, a deliberately honest negative result…".* Contrast with `MVP_PLOSONE_submission.md:286` (Competing interests) and Table 3b (line 376): ADRA2A verdict = *"NS (only size-indep. passes BH; full-library AUC NS → inconclusive)"*; and `MVP_PLOSONE_submission.md:108` states the ADRA2A result is *"inconclusive, not a confirmed null."*

【Why it matters】 This is **not** a reporting-honesty violation — the lay summary is a fair rendering of the headline — but the flattening ("no target held up reliably") could be read as slightly stronger than the manuscript's own "no target clears both filters; ADRA2A inconclusive." At minimum it is a small internal-consistency roughness between the Author Summary and the body.

【Specific fix】 Tighten the Author Summary sentence to mirror the body, e.g.: *"…and found that no target cleared both enrichment filters we applied — an honestly negative result reported as a methodological boundary rather than a false lead."* This preserves the honest-null tone while matching the "both-filters" qualification that the manuscript uses throughout.

---

## § Stands up (verified correct)

1. **Abstract is fully compliant.** Exactly **266 words** (counted programmatically on the raw markdown, not the display-truncated view), a single continuous paragraph, with **no** Background/Methods/Results/Conclusions labels. The only superscript in the abstract is the statistical "I²" symbol (e.g. "median I² 41.8%"), which is *not* a citation. This is a frequent PLOS ONE technical-check rejection cause and it is satisfied here. (`MVP_PLOSONE_submission.md:12–14`.)

2. **All five figures are embedded inline in the docx at ≥300 DPI.** `submission_pack/Manuscript.docx` (`word/media/`) contains exactly **5** PNGs, each referenced by `<wp:inline>` (5 inline drawings) and each at **350 DPI** with pixel dimensions 2208–2834 px wide. This directly satisfies the PLOS ONE "figures embedded in the manuscript file, not merely listed" technical-check requirement. (Verified via zip+PIL inspection.)

3. **Data Availability is genuine, complete, and verified.** The statement (`MVP_PLOSONE_submission.md:278–283`) names a real GitHub URL, explicitly says data are *"not 'available on request'"*, and states *"no Zenodo snapshot has been deposited"* (confirmed: no `zenodo`/`10.5281` string anywhere in the manuscript). I independently queried the GitHub API: tag **v1.6.0** exists (commit `4813a28`), and every named file in the statement is present in `results/tables/` at that tag — `META_bulkonly_sensitivity_summary.json`, `P6_target_plausibility.json`, `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_meta.csv`, `_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap_resamples.csv`, `P3_geneset_stats.csv`, `_R4_geneset_setlevel_bh.csv` (among 142 files). No fabricated DOI, no unreachable data.

4. **AI-use disclosure is present and correct.** `MVP_PLOSONE_submission.md:176–177` ("Statistical discipline, causal scope and AI-use disclosure") discloses the use of Claude (Anthropic) for drafting/language polishing and explicitly states *"No AI tool satisfies authorship criteria."* This meets PLOS ONE's generative-AI disclosure policy.

5. **Competing interests adequately handle the pending ADRA2A grant.** `MVP_PLOSONE_submission.md:285–286` declares no *financial* competing interests and discloses the pending Fujian Natural Science Foundation application that lists ADRA2A, stating it did not fund or influence the analyses; it also explains why ADRA2A is discussed at greater length (the two-filter illustrative case). This is consistent with Funding (`MVP_PLOSONE_submission.md:272–273`, "no financial support") and with the cover letter (`MVP_PLOSONE_cover_letter.md:15`). No omission or contradiction.

6. **STROBE checklist covers all 22 items.** `MVP_STROBE_checklist.md:11–34` addresses every item 1–22; items outside the reanalysis's control (5 Setting, 6/13 participant flow/eligibility) are explicitly marked **N/A (primary deposition)** with a stated reason, and items 6 and 13 are additionally marked **Partial** with the reanalysis inclusion rule given. No item is left blank or contradictory to the manuscript.

7. **Cover letter ↔ manuscript consistency holds.** Cover letter asserts version **v1.6.0**, that the **Author Summary is mandatory** under PLOS ONE policy, and **CC BY** — all three match the manuscript (Data availability cites v1.6.0; Author Summary section present; license asserted in cover letter). No mismatch.

8. **Display-item count is internally consistent.** The manuscript enumerates **5 figures + 3 tables = 8** main items (`MVP_PLOSONE_submission.md:293`) and the docx contains **5 inline images** plus **5 `w:tbl` table objects** (Table 1 split into 1a/1b, Table 3 split into 3a/3b, Table 2 single = the 3 declared main tables, no duplication). The 7 supplementary tables (S1–S7) are correctly excluded from the main count and placed in the separate supplementary file.

9. **All 40 references are cited and carry resolvable DOIs.** Every reference number 1–40 appears at least once as an in-text callout (no uncited entries; no callout to a non-existent number). All 40 entries contain a `doi.org`/URL link (41 `doi.org` mentions; ref 38 carries two). Spot-checks resolved correctly: `10.1093/bja/aen099` → 200, `10.1038/s41597-024-04078-2` → 302, `10.1016/j.cell.2017.05.018` → 200, `10.3949/ccjm.93a.25087` → 200; the `10.1126/sciadv.adu4270` (ref 19) returned 403, which is a publisher bot-block, not a dead DOI — its prefix format matches the cited *Science Advances* article. No placeholder, duplicate, or missing DOI was found.

---

## § Questions for the authors

1. After renumbering references to first-citation order (P1), please confirm the renumbering was applied to **both** the list and every in-text callout, and that no callout was dropped or duplicated in the process.
2. The manuscript references `figures/Fig1_geneset_programme.png` etc. as source paths, but the docx embeds them as `image1.png`…`image5.png`. For the production submission, will the five PNGs also be uploaded as standalone files at ≥300 DPI (PLOS ONE accepts the embedded copies, but standalone uploads are the safer path)?
3. The STROBE checklist frames GSE158825 (n = 60) as the only primary human observational cohort, yet the human layer also reports GSE222979 (urine, n = 1,242, no pain phenotype) and GSE306403 (SH-SY5Y, not human tissue). Is the STROBE "by analogy" scope statement sufficient, or should the checklist more explicitly state that GSE222979/GSE306403 are *not* STROBE-indexed cohorts? (This is a clarity point, not a defect.)
4. The Author Summary (P3) could be tightened to the "both-filters" phrasing. Do you wish to keep the current stronger-sounding sentence, or adopt the more precise wording suggested?

---

## § What I actually checked

**Files opened (read in full or by section):**
- `reports/MVP_PLOSONE_submission.md` — full read (abstract, author summary, results, discussion, limitations, conclusions, methods, statements, display-item list, references).
- `reports/MVP_PLOSONE_supplementary.md` — full read (S1–S7; used to cross-check table content and the "35 hubs / 33 detectable" phrasing).
- `reports/MVP_STROBE_checklist.md` — full read (items 1–22).
- `reports/MVP_PLOSONE_cover_letter.md` — full read.
- `submission_pack/Manuscript.docx` — inspected as a zip: enumerated `word/media/` (5 PNGs), read `word/document.xml` (counts of `<wp:inline>`, `<w:tbl>`, figure/table citations).

**Checks run (programmatically, python3):**
- Abstract word count = 266; regex for Background/Methods/Results/Conclusions labels = none; superscript scan confirmed only "I²" (not citations).
- docx media: 5 PNGs, dimensions and DPI (all 350 DPI) via PIL.
- Reference integrity: 40 numbered entries, contiguous detection, all with doi.org links; in-text citation superscript extraction (I² excluded) → all 40 cited; first-appearance ordering computed → **not** consecutive (evidence for P1).
- Display items: docx `<wp:inline>` = 5, `<w:tbl>` = 5; manuscript enumeration 5 fig + 3 tbl; supplementary S1–S7 excluded — consistent.
- Data Availability: GitHub tag `v1.6.0` existence confirmed via API; 8 named files confirmed present in `results/tables/` at that tag (142 files total).
- License: manuscript body grep for "CC BY"/"Creative Commons" = none; cover letter asserts CC BY.
- AI-use disclosure: present, no-authorship clause confirmed.
- DOI spot-resolution: 4/4 reachable (200/302); 1 publisher bot-block (403) on a correctly-formatted prefix.
- Scan for forbidden tokens: `[truncated]`, round tokens, `_archive`, internal-version markers in the manuscript = **0** (the `[truncated]` strings seen during the initial display were line-truncation artefacts of the reader, not file content — confirmed by `grep -c`).

**Discrepancies / notes stated:**
- The reader initially truncated several long lines (showing `[truncated]`); the underlying file contains **no** such tokens. The abstract was therefore re-extracted from the raw file to obtain the true 266-word count and to confirm the only superscript is "I²".
- Reference numbering is the single substantive defect; everything else either passes or is a low-risk minor gap.
- I did **not** validate the scientific correctness of the statistical claims (meta-analysis, docking, etc.) — that is the remit of the scientific reviewers, not this venue/format audit.

---

*Prepared independently for the round-16 panel. Findings are based solely on the artefacts listed above.*
