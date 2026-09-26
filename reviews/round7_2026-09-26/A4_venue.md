# A4 — Venue / Reporting-Standards Editor Report
**Journal under review:** PLOS ONE (SCIE, IF ≈ 2.8, Q2, fully OA; explicit "null/negative results welcome" policy)
**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
**Author:** Yang Y (single author)
**Reviewer lane:** A4 — Venue / Reporting-Standards (independence enforced; treated as a first submission)
**Date:** 2026-09-26

---

## 0. Reviewer's scope note and overall recommendation

I reviewed the manuscript strictly from the **venue / reporting-standards** perspective: PLOS ONE's submission requirements, the author-degree integrity, STROBE honesty, cross-artefact reporting consistency, and format hard-fails. I did **not** re-derive any computational result; I verified that the manuscript *reports* its methods and disclosures in a way that survives PLOS ONE's editorial gate. I read the manuscript `.md`, the STROBE checklist `.md`, the cover-letter `.md`, and the three submission-pack `.docx` files (Manuscript, Supporting Information, Cover Letter) directly; I did not consult any prior review, response, or self-compliance file.

**Overall recommendation: REVISE (major, but not a desk-reject).** The science is honestly framed and the disclosures are substantially present, but there are **two PLOS ONE format hard-fails** (structured abstract; reference DOI completeness) and **two cross-artefact consistency defects** (STROBE title mismatch; STROBE 2007-vs-2023 label conflict) that must be fixed before the manuscript can pass technical checks. None of these are fatal to the science; all are fixable in a single revision pass.

---

## 1. Findings (each with Problem / Evidence / Why it matters / Specific fix)

### F1. Abstract is a single paragraph — PLOS ONE requires a *structured* abstract.
- **【Problem】** The Abstract is submitted as one unbroken paragraph and contains none of PLOS ONE's required bold section headings (Background, Methods, Results, Conclusions).
- **【Evidence】** `Manuscript.docx` paragraph [5] (Abstract body) is one continuous block; a regex scan for `Background|Methods|Results|Conclusions|Objectives` inside the abstract text returned **NONE**. Same single-paragraph text at `MVP_ScientificReports_submission.md:14` (and mirrored in `Manuscript.docx`). The cover letter's pre-upload checklist (`MVP_PLOSONE_cover_letter.md:24`) self-checks "Abstract" but does not assert structure.
- **【Why it matters】** PLOS ONE mandates a structured abstract (Background / Methods / Results / Conclusions) for Research Articles. A non-structured abstract is a **technical-check rejection trigger** at the initial submission stage — editors routinely bounce it back before peer review. This is a hard format fail, not a stylistic preference.
- **【Specific fix】** Reformat the existing abstract text into four bold sub-sections. Paste-ready skeleton:

  > **Background.** Chronic postsurgical pain (CPSP) affects 10–50% of surgical patients, yet druggable targets on the DRG–spinal-cord axis remain undefined, and most transcriptomic work is single-tissue/single-model.
  > **Methods.** We reanalysed 12 public GEO datasets (5 studies, 6 contrasts) via Stouffer meta-analysis, set-level BH-corrected gene-set tests, dual-ML hub identification under leave-one-dataset-out leakage control, single-cell/spatial localisation, and a prospectively specified full-library (3,085-drug) structure-based repurposing screen with reverse positive controls.
  > **Results.** Under fixed effects a 4,055-gene core emerged, but only 1,008 persisted under random effects (median I² = 38.8%). Gene-set tests confirmed neuroimmune/DAM/complement activation (q = 0.003 each); OXPHOS did not survive random-effects correction (q = 0.31). A non-circular test showed the nerve-injury signature does not predict incision direction (46.3% vs 47.1% background, p = 0.14). The full-library docking screen found no target clearing both enrichment filters (ADRA2A 0.618 → 0.532, p = 0.118).
  > **Conclusions.** The axis is best framed as a nerve-injury-associated, heterogeneity-sensitive transcriptional response rather than a CPSP-specific target; the docking null is reported as a methodological boundary, not a false lead.

  Keep each section's word count balanced; the total must stay within the word ceiling (see F2).

### F2. Abstract word count sits exactly at the stated 200-word ceiling.
- **【Problem】** The abstract is 200 words exactly, at the absolute limit of the ≤200-word target, leaving no margin for PLOS's own word-count parser or for the structural reformatting in F1.
- **【Evidence】** `MVP_ScientificReports_submission.md:14` → `wc -w` = **200**. (PLOS ONE's general abstract limit is 300 words, so the manuscript is also within PLOS's larger limit; but the self-imposed ≤200 bar is met only marginally.)
- **【Why it matters】** Margin protects against (a) word-count tools that treat hyphenated compounds or parentheticals differently, and (b) the added headings words from F1 pushing the count over. A count that is exactly at the limit is fragile.
- **【Specific fix】** Trim ~10–15 words during the F1 reformat (e.g., drop "yet druggable targets on the DRG–spinal-cord axis remain undefined" → fold into Background; compress "set-level BH-corrected gene-set tests confirmed coordinated neuroinflammation, DAM-microglia and complement activation" → "set-level tests confirmed neuroimmune/DAM/complement activation"). Target ≤ 190 words after restructuring.

### F3. STROBE checklist title does NOT match the manuscript / cover-letter / docx title.
- **【Problem】** The STROBE checklist carries a *different* (older, ScientificReports-era) manuscript title than the one used everywhere else.
- **【Evidence】** `MVP_STROBE_checklist.md:3` title = *"Coordinated neuroimmune and metabolic reprogramming of the dorsal-root-ganglion–spinal axis in chronic postsurgical pain: a multi-dataset in-silico meta-analysis and structure-based repurposing screen"*. By contrast, `MVP_ScientificReports_submission.md:1`, `Manuscript.docx` paragraph [0], and `MVP_PLOSONE_cover_letter.md:3` / `Cover_Letter_PLOSONE.docx` all read *"Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"*.
- **【Why it matters】** PLOS ONE cross-checks that the title is identical across the manuscript, cover letter, and supporting checklists. A mismatched title on a mandatory reporting-guideline file signals a stale artefact and triggers a technical-check query; it also undermines the "reporting consistency" the author claims to value.
- **【Specific fix】** Replace the title string in `MVP_STROBE_checklist.md:3` with the current PLOS ONE title, verbatim: *"Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"*. Then regenerate `Supporting_Information.docx` (which embeds the checklist) so the embedded copy matches.

### F4. STROBE version label conflict: manuscript says "STROBE 2023", checklist says "STROBE 2007".
- **【Problem】** The manuscript cites the *STROBE 2023* checklist, but the supplied checklist file identifies itself as *STROBE 2007*.
- **【Evidence】** `MVP_ScientificReports_submission.md:277` — *"The completed **STROBE 2023** checklist for this observational reanalysis is provided as a separate Supporting Information file"*. `MVP_STROBE_checklist.md:4` — *"**STROBE statement version:** STROBE 2007 (von Elm et al., Lancet 2007;370:1453–1457)"*.
- **【Why it matters】** PLOS ONE asks authors to use the current version of the relevant reporting guideline. The 22-item structure is conserved between 2007 and 2023, so the *content* is still usable, but the label contradiction is a factual inconsistency a meticulous editor will flag, and it suggests the checklist was not re-issued for this submission.
- **【Specific fix】** Either (a) adopt the STROBE 2023 checklist (ELife 2023;12:e85928) and update the header at `MVP_STROBE_checklist.md:4`, keeping the manuscript's "STROBE 2023" reference; **or** (b) if retaining the 2007 checklist, change the manuscript's `:277` reference from "STROBE 2023" to "STROBE 2007". Option (a) is preferred for currency. Re-embed in `Supporting_Information.docx`.

### F5. STROBE item 5 (Setting) marked N/A — defensible but should be explicitly justified at the reanalysis level.
- **【Problem】** The author marks STROBE item 5 (Setting) as N/A (primary deposition) and leans entirely on the general transparency note, without describing the *reanalysis* setting.
- **【Evidence】** `MVP_STROBE_checklist.md:15` — *"5 | Setting | N/A (primary deposition)…"*; the transparency note at `:7` justifies N/A generically. Items 6 and 13 are likewise partially/fully N/A (`:16`, `:23`).
- **【Why it matters】** For a secondary in-silico reanalysis, marking the *original* study setting N/A is acceptable, but STROBE reviewers expect the *reanalysis* context (public GEO, computational environment, no new recruitment) to be stated somewhere. Leaving it wholly N/A risks a reviewer noting the reanalysis "setting" (in-silico, public-data) is itself reportable under item 4/5.
- **【Specific fix】** Add one sentence to item 5's entry: *"Reanalysis setting: fully computational, secondary reanalysis of de-identified public transcriptomes deposited in GEO; no new data collection, recruitment, or laboratory setting."* This preserves the N/A for the *primary* setting while satisfying the reanalysis-reporting expectation. (Items 6 and 13 are acceptable as-is given the transparency note.)

### F6. STROBE items 7, 12, 18, 22 are correctly ADDRESSED (not wrongly N/A) — positive verification.
- **【Problem】** (None — this is a verification note.) The brief flagged items 7 (Variables), 12 (Statistical methods), 18 (Key results), and 22 (Funding) as possible incorrect N/A; on inspection the author *correctly* addressed all four.
- **【Evidence】** `MVP_STROBE_checklist.md:17` (Variables — Addressed), `:22` (Statistical methods — Addressed in detail), `:28` (Key results — Addressed), `:32` (Funding — Addressed). None are marked N/A.
- **【Why it matters】** Confirms the author did not under-report on the items most prone to lazy N/A marking; this strengthens the STROBE submission.
- **【Specific fix】** No change required. Keep these as "Addressed" with their current section pointers.

### F7. Reference 31 (Xiao et al., 2002, PNAS) is missing a DOI / PubMed ID.
- **【Problem】** One reference lacks any DOI or PubMed ID, violating PLOS ONE's requirement that every reference carry a resolvable identifier where one exists.
- **【Evidence】** `MVP_ScientificReports_submission.md:200` — *"31. Xiao, H. S. et al. Identification of gene expression profile of dorsal root ganglion in the rat peripheral axotomy model of neuropathic pain. Proceedings of the National Academy of Sciences of the United States of America 99, 8360–8365 (2002)."* — no `https://doi.org/...` suffix, unlike all other 32 references.
- **【Why it matters】** PLOS ONE requires a DOI (or PMID/URL) for every reference for which one is available; PNAS articles from 2002 carry DOIs (e.g., 10.1073/pnas.122716399). A missing identifier is a technical-check defect and contradicts the cover letter's own pre-upload claim that references are "PLOS style (… DOIs)" (`MVP_PLOSONE_cover_letter.md:24`).
- **【Specific fix】** Append the DOI to reference 31, e.g.: *"… 99, 8360–8365 (2002). https://doi.org/10.1073/pnas.122716399"* (verify the exact DOI against the source before finalising). Re-embed in `Manuscript.docx`.

### F8. Reference DOIs are correctly formatted as full `https://doi.org/...` URLs — positive verification.
- **【Problem】** (None.) All other 32 references use full `https://doi.org/…` URLs, satisfying PLOS's Vancouver + full-URL requirement.
- **【Evidence】** Sampled across `MVP_ScientificReports_submission.md:170–202`: refs 1–30, 32, 33 each close with `https://doi.org/10.x…`. No bare `doi:10.x` or truncated forms found.
- **【Why it matters】** Confirms the reference-format backbone is compliant; only F7 needs remediation.
- **【Specific fix】** No change beyond F7.

### F9. Word document core metadata is the generator default (`python-docx`), not the author.
- **【Problem】** The `.docx` files' core properties carry the python-docx library default as author and an empty title, which is inconsistent with the byline and can confuse editorial systems that read metadata.
- **【Evidence】** `Manuscript.docx`, `Supporting_Information.docx`, `Cover_Letter_PLOSONE.docx` core properties: `author = 'python-docx'`, `title = ''` (verified via `python-docx` core-properties read). The *visible* byline in all three is correct ("Yang Y"), so this is a metadata (not visible-text) defect.
- **【Why it matters】** Some submission systems ingest docx metadata; a byline of "python-docx" could trigger a metadata/byline mismatch query or be carried into the typeset proof if not cleaned. It also looks unpolished.
- **【Specific fix】** Before final upload, set the document core properties: `author = "Yang Y"`, `title = "<the PLOS ONE title>"`, and `last_modified_by = "Yang Y"` in all three `.docx` files (e.g., via a properties step in the render pipeline). This is a one-line fix per file.

### F10. Author-degree integrity verified clean — no "Dr.", "MD", or "PhD" anywhere (hard check passed).
- **【Problem】** (None — this is the required hard-error check, and it PASSES.) The single author is presented as "Yang Y" with no honorific or doctoral attribution in any artefact.
- **【Evidence】** Regex scans for `\bDr\.|\bMD\b|\bPhD\b|Prof\.|M\.D\.|Ph\.D` across `MVP_ScientificReports_submission.md`, `MVP_PLOSONE_cover_letter.md`, and the full text of all three `.docx` files (including tables) returned **no honorific hits** (the only string matches for "MD" were the `.md` file-extension tokens in paths, not degrees). Byline: `Manuscript.docx` paragraph [1] = "Yang Y¹*"; `Cover_Letter_PLOSONE.docx` = "Corresponding author: Yang Y".
- **【Why it matters】** A Bachelor-of-Medicine-only author must not be accorded "Dr./MD/PhD" — this was flagged as a potential hard error. It is **not present**; the manuscript is compliant on this point.
- **【Specific fix】** No change required. (Note only the F9 metadata default is unrelated to degree and must still be cleaned.)

### F11. Ethics statement is present and adequate for a secondary reanalysis.
- **【Problem】** (None.) The manuscript includes a stand-alone Ethics statement covering both the human dataset (IRB + consent) and the animal/in-vitro datasets (IACUC), and correctly states no new data were generated.
- **【Evidence】** `MVP_ScientificReports_submission.md:163–164` ("Ethics statement" section) — GSE158825 IRB/consent documented by depositor; animal datasets IACUC-documented; no new animal data. Mirrored in `Manuscript.docx`. Cover letter `MVP_PLOSONE_cover_letter.md:15` affirms the ethics statement.
- **【Why it matters】** PLOS ONE requires an explicit ethics statement for any human-subjects component; the secondary-reanalysis framing ("required no further ethics approval") is appropriate and defensible.
- **【Specific fix】** No change required. Keep verbatim.

### F12. Data Availability uses a real repository URL, but the Zenodo DOI is a placeholder.
- **【Problem】** The primary data-availability route (public GitHub) is real and explicit (not "available on request"), which is good; however the citable Zenodo DOI is a literal placeholder `10.5281/zenodo.XXXXXXX — to be minted at submission`.
- **【Evidence】** `MVP_ScientificReports_submission.md:216` — GitHub repo `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` (v1.0.0) is real; the Zenodo line reads *"A versioned Zenodo archive … (DOI: 10.5281/zenodo.XXXXXXX — to be minted at submission)"*. Cover letter `:13` references the GitHub repo only.
- **【Why it matters】** PLOS ONE requires that data underlying the results be available at acceptance. A placeholder DOI is acceptable *if* minted before acceptance, but an unresolved placeholder left in the final PDF is a technical-check fail. The GitHub repo alone satisfies "not available on request," so the risk is contained, but the placeholder must be resolved or removed.
- **【Specific fix】** Either (a) mint the Zenodo DOI and replace `XXXXXXX` with the real one before acceptance, or (b) if not minting, delete the Zenodo sentence and keep the GitHub repo as the sole (sufficient) availability statement. Do not leave the literal `XXXXXXX` in the submitted PDF.

### F13. Funding statement is consistent and correctly denies a grant — no false grant claim.
- **【Problem】** (None.) The Funding section states "no financial support" and frames the pending grant correctly as *non-funding* (preliminary foundation only), with no grant number asserted.
- **【Evidence】** `MVP_ScientificReports_submission.md:210` — *"The author received no financial support for this work… preliminary foundation for a pending Fujian Natural Science Foundation grant application; the grant did not fund and did not influence the present analyses."* Cover letter `MVP_PLOSONE_cover_letter.md:15` — *"No funding was received for this work (… no grant number)."* No grant number appears anywhere.
- **【Why it matters】** Confirms the brief's concern (a grant claimed that wasn't awarded) is **not** present; the pending grant is transparently disclosed in Competing Interests, not misrepresented as funding.
- **【Specific fix】** No change required.

### F14. Competing interests declared and consistent across artefacts.
- **【Problem】** (None.) A stand-alone Competing Interests section exists, discloses the pending ADRA2A-containing grant, and attests uniform treatment of all 10 targets.
- **【Evidence】** `MVP_ScientificReports_submission.md:218–219`; echoed in Discussion `:84` and `:120`; cover letter `:15`. Consistent wording on "did not fund / did not influence."
- **【Why it matters】** PLOS ONE requires an explicit, stand-alone Competing Interests statement; present and coherent.
- **【Specific fix】** No change required.

### F15. AI-use disclosure is present, names the tool, and states AI was NOT used for data selection/interpretation — consistent.
- **【Problem】** (None.) The manuscript contains a proper AI-use statement; the cover letter's shorter version is consistent with it.
- **【Evidence】** `MVP_ScientificReports_submission.md:161` — *"A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing… no AI tool was used to generate, select or interpret data. No AI tool satisfies authorship criteria."* Cover letter `MVP_PLOSONE_cover_letter.md:15` — *"A large language model assisted language drafting; all scientific content is solely the author's."*
- **【Why it matters】** PLOS ONE *requires* an AI-use disclosure naming the tool and clarifying it was not used for data/analysis decisions. Both criteria are met and the two artefacts agree.
- **【Specific fix】** No change required. (Optional: align the cover-letter phrasing slightly toward the manuscript's explicit "not used to generate, select or interpret data" wording for maximal consistency.)

### F16. ORCID and complete affiliation are present.
- **【Problem】** (None.) The corresponding author provides a valid ORCID and a complete institutional affiliation.
- **【Evidence】** `MVP_ScientificReports_submission.md:3–6` — affiliation "The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine, Fuzhou, Fujian 350003, China"; ORCID 0009-0004-9698-6552; email. Mirrored in `Manuscript.docx` [1–3] and `Cover_Letter_PLOSONE.docx`.
- **【Why it matters】** PLOS ONE requires ORCID for all authors and a complete affiliation; satisfied.
- **【Specific fix】** No change required.

### F17. Figures and tables are embedded (not merely referenced) — verified.
- **【Problem】** (None.) The `Manuscript.docx` embeds all five figures as PNG images and contains five table objects; the `Supporting_Information.docx` embeds 13 supplementary tables.
- **【Evidence】** `Manuscript.docx` zip archive contains `word/media/image1.png … image5.png` (5 images) and `len(tables) = 5`. The manuscript text references Fig. 1–5 and Tables 1–3 (with sub-parts). `Supporting_Information.docx` has 13 tables, 0 images. The PNGs are also present as standalone files in `submission_pack/`.
- **【Why it matters】** PLOS ONE requires display items to be embedded in the manuscript file (not "available on request" / separate-only). This is satisfied.
- **【Specific fix】** No change required. Confirm at upload that the five embedded figures meet the ≥300 DPI spec (the standalone PNGs are sized appropriately; ensure the embedded copies are not downscaled by the render step).

### F18. "Display items" count claim ("3 tables") undercounts the 5 rendered tables — internal inconsistency.
- **【Problem】** The manuscript's display-items header says "5 figures + 3 tables = 8 main display items," but the `Manuscript.docx` actually contains **5** table objects (Table 1b, Table 2, Table 3a Panel A, Table 3a Panel B, Table 3b).
- **【Evidence】** `MVP_ScientificReports_submission.md:226` — *"## Display items (5 figures + 3 tables = 8 main display items)"*; but `Manuscript.docx` table inventory = 5 tables. The "3" conflates logical tables (1, 2, 3) with the 5 physical table objects produced by the render (Table 1 was split into 1a-prose + 1b-table; Table 3 into 3a-A, 3a-B, 3b).
- **【Why it matters】** Low severity, but a reviewer counting display items will notice 5 tables vs the stated 3; it reads as a stale artefact from the ScientificReports template.
- **【Specific fix】** Either relabel the header to "5 figures + 5 tables" (counting physical objects) or re-merge the split tables so the count reads "3 tables" truthfully. Recommended: update the header text to reflect the rendered count to avoid any mismatch.

### F19. Editorial framing: the title's lead adjective "Conserved" overstates a result the paper itself shows is fragile.
- **【Problem】** The title and several lead sentences present a "conserved" axis "response" as the headline finding, while the paper's own evidence shows the core is heterogeneity-sensitive (4,055 → 1,008 genes under random effects; 45.7% of the core is translatome-dependent) and the docking result is an explicit null.
- **【Evidence】** Title `MVP_ScientificReports_submission.md:1` leads with "Conserved nerve-injury-associated transcriptional response." Yet `:40` reports the random-effects core shrinks to 1,008 (24.9%); `:44` reports 45.7% of the primary core is translatome-dependent; `:82`/`:106` report the honest docking null. Introduction `:30` also claims *"among the first CPSP-adjacent studies to integrate DRG and spinal-cord transcriptomes as a single axis"* — a priority claim.
- **【Why it matters】** PLOS ONE evaluates rigour over novelty, and the manuscript's *strongest, most defensible* contribution is the honest-negative/methodological-boundary (the "repurposing panacea" correction, the non-circular translation null, the bootstrap instability). Leading with "Conserved" creates a self-contradiction: the headline implies a robust positive finding that the body qualifies heavily. This is exactly the "over-claim a finding when the real contribution is the honest negative" trap the brief warned about. It will draw reviewer pushback on tone even though the substance is honest.
- **【Specific fix】** Soften the lead framing so it matches the demonstrated evidence. Options: (a) change "Conserved … transcriptional response" → "A nerve-injury-associated, heterogeneity-sensitive transcriptional response," or (b) keep "nerve-injury-associated" (already present mid-title) and drop "Conserved." In the Conclusion/Discussion close, explicitly restate that the paper's contribution is the *methodological benchmark and the honest nulls*, not a conserved CPSP target — i.e., let the Conclusion **retract** the discovery-language rather than merely qualifying it in a sub-section. The Discussion already hedges (`:114`, `:120`); make the final paragraph state this outright.

### F20. The novelty/priority claim ("among the first …") is acceptable at PLOS ONE but should be tempered.
- **【Problem】** The Introduction asserts multiple "among the first" priority claims that sit in mild tension with the manuscript's honest-null emphasis.
- **【Evidence】** `MVP_ScientificReports_submission.md:30` — *"To our knowledge, this is among the first CPSP-adjacent studies to integrate DRG and spinal-cord transcriptomes as a single axis via multi-dataset meta-analysis … and among the first to identify hubs by a dual-ML consensus under LODO leakage control and to report a prospectively specified full-library FDA repurposing screen…"*
- **【Why it matters】** PLOS ONE does not require novelty, so priority claims are not mandatory and will not be rejected on that basis; but over-stated priority invites "is this really first?" scrutiny and dilutes the manuscript's genuine selling point (transparency/null-results welcome). Better to foreground the methodological-honesty angle the journal explicitly welcomes.
- **【Specific fix】** Recast from "among the first to…" to "we provide, to our knowledge, the first explicitly heterogeneity-bounded and non-circularly tested DRG–spinal-axis reanalysis with a prospectively specified full-library docking null." This keeps the contribution claim truthful and aligned with PLOS ONE's stated editorial preferences.

---

## 2. § Stands up (verified compliant — at least 3)

1. **Author-degree integrity (hard check) passes.** No "Dr.", "MD", "PhD", or "Prof." attribution appears in the manuscript `.md`, the cover letter `.md`, or the full text of any of the three `.docx` files. The single author "Yang Y" is presented without any doctoral honorific. (Only the unrelated F9 docx-metadata generator default needs cleaning.) This was a flagged hard error and it is **not** present.

2. **AI-use disclosure satisfies PLOS ONE.** The Methods section (`MVP_ScientificReports_submission.md:161`) names the specific tool (Claude, Anthropic), states its limited role (drafting/language polishing), and explicitly affirms AI was **not** used to generate, select, or interpret data, and does not satisfy authorship criteria. The cover letter's shorter version is consistent. PLOS ONE's mandatory AI-disclosure criteria are fully met.

3. **Funding / "no grant" stance is consistent and honest.** The Funding section (`:210`) states "no financial support," correctly frames the pending Fujian NSF grant as non-funding preliminary foundation, and asserts no grant number. The cover letter (`:15`) matches word-for-word on "No funding was received… no grant number." No fabricated/asserted-but-unawarded grant appears — the brief's worst-case concern is absent.

4. **Ethics, Data Availability, ORCID, affiliation, Competing Interests all present and adequate.** IRB/IACUC ethics statement (`:163–164`); real GitHub repository (not "available on request") for data/code (`:216`); valid ORCID 0009-0004-9698-6552 with complete affiliation (`:3–6`); stand-alone Competing Interests (`:218–219`). These are the PLOS ONE administrative gate items and they pass.

5. **STROBE items 7/12/18/22 are correctly addressed, not wrongly N/A.** Verification against the brief's suspicion list shows the author properly reported Variables, Statistical methods, Key results, and Funding rather than lazily marking them N/A.

6. **Figures/tables are genuinely embedded.** `Manuscript.docx` embeds 5 PNG figures and 5 table objects; `Supporting_Information.docx` embeds 13 supplementary tables. No display item is reference-only.

---

## 3. § Questions for the authors

1. **STROBE version:** Will you adopt the STROBE 2023 checklist (preferred) or revert the manuscript's "STROBE 2023" reference to "2007"? The current file asserts both simultaneously (F4).
2. **Zenodo DOI:** Is the `10.5281/zenodo.XXXXXXX` placeholder going to be minted before acceptance, or should the sentence be removed and GitHub left as the sole availability route (F12)?
3. **"Conserved" framing:** Given the random-effects core collapses to 1,008/4,055 genes and 45.7% of the primary core is translatome-dependent, are you willing to drop or qualify "Conserved" in the title so the headline matches the demonstrated fragility (F19)?
4. **Reference 31 DOI:** Can you supply the correct DOI for Xiao et al. 2002 PNAS so the reference list is fully identifier-complete (F7)?
5. **Table count:** The display-items header says "3 tables" but 5 table objects render — do you intend to re-merge them or update the count (F18)?
6. **Docx metadata:** Will the render pipeline set author/title core properties to "Yang Y" / the real title instead of the `python-docx` default before upload (F9)?

---

## 4. § What I actually checked (artefacts read; discrepancies found)

**Artefacts read (independently, no prior-review contamination):**
- `reports/MVP_ScientificReports_submission.md` (full, 278 lines) — primary manuscript source.
- `reports/MVP_STROBE_checklist.md` (full, 35 lines) — STROBE 22-item self-map.
- `reports/MVP_PLOSONE_cover_letter.md` (full, 25 lines) — cover letter source.
- `submission_pack/Manuscript.docx` — extracted core properties, embedded image inventory (5), table inventory (5), full text, abstract structure.
- `submission_pack/Supporting_Information.docx` — extracted table inventory (13), image inventory (0), text.
- `submission_pack/Cover_Letter_PLOSONE.docx` — extracted text, title, honorific scan.

**Automated/independent verification performed:**
- Regex scan for degree honorifics (`Dr.`, `MD`, `PhD`, `Prof.`, `M.D.`, `Ph.D.`) across all three `.md` and all three `.docx` texts+`docx` tables → **no hits** (only `.md` path tokens matched "MD").
- Abstract word count (`wc -w` on the abstract line) = **200**; structured-heading regex inside the abstract = **none**.
- DOI presence scan across all 33 references → 32 carry full `https://doi.org/…`; **reference 31 missing**.
- Title string comparison across manuscript `.md` (:1), `Manuscript.docx` ([0]), cover-letter `.md` (:3), `Cover_Letter_PLOSONE.docx`, and STROBE checklist (:3) → **3 of 4 match; STROBE checklist uses a different (old) title**.
- STROBE version label cross-check → manuscript (:277) says "2023"; checklist (:4) says "2007".
- Docx core-property read → `author='python-docx'`, `title=''`.

**Discrepancies / defects found (summary):**
- **Format hard-fail 1:** Abstract not structured (F1). → REVISE.
- **Format hard-fail 2:** Reference 31 missing DOI (F7). → REVISE.
- **Consistency defect 1:** STROBE checklist title ≠ manuscript/cover/docx title (F3). → REVISE.
- **Consistency defect 2:** STROBE 2023 (manuscript) vs STROBE 2007 (checklist) label conflict (F4). → REVISE.
- **Minor:** Abstract at exact 200-word ceiling (F2); docx metadata default (F9); "3 tables" vs 5 rendered (F18); "Conserved"/priority framing tension (F19/F20); Zenodo placeholder DOI (F12).
- **Verified clean / compliant:** author degree (F10), AI disclosure (F15), Funding/no-grant (F13), Ethics (F11), ORCID+affiliation (F16), Competing interests (F14), embedded figures/tables (F17), STROBE 7/12/18/22 addressed (F6), DOIs format (F8).

**Independence discipline:** I did not open any `reviews/REVIEW_round*.md`, `reviews/round*/*`, `RESPONSE*.md`, `REVISION*.md`, `_v14_source.md`, `_v15_source.md`, `MVP_PLOSONE_compliance_check.md`, `SUBMISSION_MANIFEST.md`, other reviewers' files in `reviews/round7_2026-09-26/`, any `*.bak`, or `author_verification_statement.md`. The manuscript was assessed as a first submission.

---

*End of A4 venue / reporting-standards report.*
