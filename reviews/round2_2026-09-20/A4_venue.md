# Reviewer A4 — Venue / editorial & reporting-standard audit
**Manuscript:** "A neuroimmune–metabolic programme defines the chronic postsurgical pain DRG–spinal axis with an honest repurposing null"
**Venue:** *Scientific Reports* (Nature Portfolio), Article
**Review date:** 2026-09-20 (Round 2, independent first-read)
**My layer:** journal hard-limits, formatting, cross-document consistency, disclosure honesty. I did not read any other reviewer's file, the round-1 review, the submission manifest, project/plan/SOP files, or gate scripts — compliance below is verified directly from the four submitted documents.

---

## Overall verdict
**Major revision required before the "format-compliant / submission-ready" claim can stand.** The manuscript clears the bulk of *Scientific Reports* hard-limits (title length, abstract length, display-item count, figure DPI, Methods placement, mandatory declarations, AI disclosure, data-availability language). However, three items are genuine compliance gaps that an editor will catch on first pass: (1) references are **not** in Nature style; (2) three references are orphans; (3) the Reporting Summary omits the Competing Interests block that the manuscript and cover letter both carry. A fourth, more serious item is a **framing/perceived-bias** problem: the repeatedly favorable ADRA2A advocacy sits awkwardly against the disclosed pending grant that lists ADRA2A as a candidate target, and it contradicts the paper's own "assessed uniformly" statement. None of these is individually a guaranteed desk-reject, but together they invalidate the manuscript's own "Format compliant with Scientific Reports Author Instructions" statement (submission.md:8).

---

## F1 — References are not in Nature style (systematic, all 18)
【Problem】 Every reference uses a Vancouver/AMA-style template (`Surname Initials. Title. *Journal*. Year;Vol(Issue):Pages. DOI`) instead of the Nature-style template (`Surname, A. A. & Last, B. B. Title. *Journal* **vol**, pages (year).`), so the manuscript's claim of Nature-style compliance is false.

【Evidence】 submission.md:107–125. Concrete deviations on the first entry (submission.md:107):
- Author order: `Macrae WA.` → Nature requires `Macrae, W. A.` (comma after surname, spaced initials with periods).
- Multi-author joiners: submission.md:108 `Xu R, Wang J, Nie H, Wang L, Xiao X, Luo M.` → Nature requires `Xu, R., Wang, J., Nie, H., Wang, L., Xiao, X. & Luo, M.` (comma after every author, `&` before the last).
- Journal: `Br J Anaesth` (no periods) → `Br. J. Anaesth.`; similarly `J Pain Res`→`J. Pain Res.`, `Commun Biol`→`Commun. Biol.`, `Nat Med`→`Nat. Med.`, `Acta Pharmacol Sin`→`Acta Pharmacol. Sin.`, `Cleveland Clin J Med`→`Clevel. Clin. J. Med.`, `Mol Pain`→`Mol. Pain.`, etc.
- Volume/year/pages: `2017;119(Suppl 1):i3–i4.` → `**119**, i3–i4 (2017).` (bold volume, year in parentheses, no semicolon/colon/issue-in-parentheses construction).
- Preprint (submission.md:114): Nature form is `Bhuiyan, S. A. et al. A Reference Atlas of the Human Dorsal Root Ganglion. Preprint at bioRxiv https://doi.org/10.1101/2025.11.05.686654 (2025).`

【Why it matters】 *Scientific Reports* Author Instructions explicitly request Nature-style references. A manuscript that asserts "Format compliant … Nature style" (submission.md:8) while delivering a different style is a hard-fail on its own self-declaration; production/editors will return it for reformatting, and it erodes trust in the other compliance claims. Not a desk-reject by itself, but a guaranteed post-acceptance rework and a credibility flag now.

【Specific fix】 Reformat all 18 entries to Nature style. Canonical target for #1:
`Macrae, W. A. Chronic postsurgical pain: 10 years on. *Br. J. Anaesth.* **119**, i3–i4 (2017).`
Apply uniformly: surname-first with comma + spaced initials; comma after each author and `&` before the final author; italic journal abbreviated with periods; **bold volume**; pages; year in parentheses; DOI retained at end. Treat #8 as the preprint form above.

---

## F2 — Three orphan references (5, 11, 12 listed but never cited)
【Problem】 References 5, 11 and 12 appear only in the reference list; they are never cited anywhere in the body text.

【Evidence】 Cited reference numbers parsed from the text = {1, 2, 3, 4, 6, 7, 8, 9, 10, 13, 14, 15, 16, 17, 18} (refs 7/15/16 occur only inside the ranges `⁶⁻⁸` and `¹⁴⁻¹⁷`, so they are legitimately cited). Orphans = {5, 11, 12}:
- submission.md:111 — #5 Sapio MR … *J Pain* 2020 (dynorphin/enkephalin in DRG/spinal cord) — never cited.
- submission.md:117 — #11 Divito AE … Suzetrigine *Cleveland Clin J Med* 2026 — never cited.
- submission.md:118 — #12 McDonnell A … PF-05089771 Nav1.7 blocker *Pain* 2018 — never cited.
A text search for "Sapio", "Dynorphin", "Suzetrigine", "PF-05089771" returns only the reference rows themselves, confirming zero in-text use.

【Why it matters】 Nature/SciRep expect every listed reference to be cited (and every citation to be listed). Orphans are a classic marker of incomplete editing or reference padding; they will draw an editor/reviewer query and make the stated "18 references" look uncoordinated. They also waste the reference budget (≤60 is fine, but coherence matters).

【Specific fix】 Either cite each where genuinely relevant (e.g., #5 dynorphin/enkephalin in the DRG-neuron or peptidergic discussion at submission.md:44/49; #11/#12 in the "known analgesics / Nav-blocking strategies do not address this" context at submission.md:64) **or** delete them. Given they are tangential, deletion is the cleaner option and keeps the list tight.

---

## F3 — Reporting Summary missing the Competing Interests section
【Problem】 The Nature Portfolio Reporting Summary supplied with the manuscript has no Competing Interests disclosure, even though the manuscript (submission.md:139) and the cover letter (cover_letter.md:17) both disclose the pending Fujian Natural Science Foundation grant that lists ADRA2A as a candidate target.

【Evidence】 reporting_summary.md sections run Statistics → Software and code → Data → Human participants → Animal research → Field-specific reporting → Specific materials/systems → AI disclosure (reporting_summary.md:50–51). There is no "Competing interests" block. By contrast, submission.md:139 and cover_letter.md:17 both carry the ADRA2A/pending-grant statement. The Reporting Summary *does* include an AI-disclosure block (reporting_summary.md:50–51) but not the competing-interests one.

【Why it matters】 Cross-document inconsistency: an editor reconciling the three files will see the disclosure in two places and its absence in the third, which both breaks the "disclosures agree across documents" expectation and leaves the Reporting Summary incomplete against the Nature Portfolio template (which asks for competing interests). It also undercuts the manuscript's claim of complete, consistent declaration.

【Specific fix】 Add a "Competing interests" entry to reporting_summary.md that mirrors submission.md:139 verbatim, e.g.:
`The author declares no financial competing interests. The author has a pending grant application (Fujian Natural Science Foundation) in which ADRA2A is listed among the candidate targets; this application did not fund and did not influence the present analyses, results, or conclusions, and the manuscript was written independently of the grant.`

---

## F4 — ADRA2A framing vs the disclosed pending-grant interest (perceived-bias risk)
【Problem】 The disclosure itself meets the journal's *minimum* standard (it names ADRA2A and the grant and states no influence), but the manuscript repeatedly gives ADRA2A a uniquely favorable biological-plausibility advocacy that (a) contradicts its own "assessed uniformly, not an ADRA2A-specific rescue" sentence and (b) favors the *weakest* docking target, creating a perceived-bias problem given the author's disclosed interest in ADRA2A.

【Evidence】
- Disclosure present and adequately specific: submission.md:139 ("pending grant application (Fujian Natural Science Foundation) in which ADRA2A is listed among the candidate targets") and cover_letter.md:17 (consistent wording).
- Contradiction: submission.md:58 opens "Target-specific biological plausibility is assessed uniformly across all 10 tractable targets, not as an ADRA2A-specific rescue." The very next sentences defend **only** ADRA2A at length ("established α2A norepinephrine-mediated descending analgesia and meta direction-consistency, meta_Z = 4.84, FDR = 1.5e-5; … ADRA2A docking is therefore non-informative—neither supporting nor refuting the target" … "biologically plausible, not-yet-docking-prioritised, hypothesis to be tested in vivo"). No parallel biological-plausibility defense is given for the other nine targets.
- ADRA2A is the *worst* performer: full-library AUC 0.532, p = 0.118 (NS) — the lowest of the 10 targets (submission.md:54, 56, 159–160); yet it is singled out for advocacy at submission.md:56, 58, 68.
- The favorable framing recurs in Discussion: submission.md:68 ("ADRA2A's meta direction-consistency and known α2A analgesic pharmacology keep it a biologically plausible … hypothesis to be tested in vivo").

【Why it matters】 Disclosure satisfies the literal policy, but venue perception is the issue: when an author with a *disclosed* interest in target X repeatedly argues X is "biologically plausible" despite X being the weakest docking result and explicitly claims the treatment is "uniform," reviewers/editors can reasonably read the advocacy as not independent. This is exactly the kind of framing that triggers a "please justify/neutralize" editorial request and, combined with F3, makes the disclosure look incomplete in spirit. It is a credibility risk for the venue, not a mechanical pass/fail.

【Specific fix】 Pick one of two clean resolutions:
- (a) Make the claim true: genuinely treat all 10 targets uniformly — replace the ADRA2A-only paragraph with a short table/summary of biological plausibility for every tractable target (or none), and delete the "assessed uniformly … not ADRA2A-specific rescue" sentence if it cannot be honored.
- (b) Keep the ADRA2A discussion but add an explicit guard sentence: "Because ADRA2A is a candidate target in the author's pending grant (disclosed in Competing Interests), its favorable framing herein was independently verified against the docking evidence and the conclusion is docking-null-independent." Then soften the absolute "biologically plausible" to "a biologically plausible hypothesis to be tested," matching the honest-null tone.

---

## F5 — Reference #8 bioRxiv preprint: acceptable, but the inline correction remark should go
【Problem】 #8 (a human DRG atlas) is correctly cited as a preprint, which Nature policy permits; however the parenthetical "original citation to *Brain* 2026 was incorrect and has been corrected" is an editorial artifact that should not survive into a finished reference list.

【Evidence】 submission.md:114 — `*bioRxiv*. 2025. https://doi.org/10.1101/2025.11.05.686654 *(Preprint; not yet a journal article — original citation to *Brain* 2026 was incorrect and has been corrected.)*`

【Why it matters】 Citing a preprint as anatomical support is fine *because* it is clearly labelled "(Preprint …)"; that satisfies Nature's preprint policy. But the "Brain 2026 was incorrect" note signals reference churn and reads unprofessionally to an editor; it also hints the citation was unstable. The reference is used inside the range `⁶⁻⁸` (submission.md:64), so the paper is not *solely* leaning on a preprint — acceptable. Still, tidy it.

【Specific fix】 Reduce to: `Bhuiyan, S. A. et al. A Reference Atlas of the Human Dorsal Root Ganglion. Preprint at bioRxiv https://doi.org/10.1101/2025.11.05.686654 (2025).` Drop the Brain 2026 remark. Optionally add the word "preprint" once in-text at submission.md:64 where the range is first used, so a reader skimming does not mistake it for a peer-reviewed anatomical citation.

---

## F6 — "First …" novelty claim is over-bundled and unevenly hedged (framing risk)
【Problem】 The abstract and introduction assert, as essentially factual, three bundled "firsts" for a CPSP study, but the hedging is inconsistent between the two sections.

【Evidence】
- submission.md:24 (Introduction): "To our knowledge this is the first CPSP study to integrate DRG and spinal-cord transcriptomes as a single axis via multi-dataset meta-analysis, lock hubs by dual-ML consensus under LODO leakage control, and report a prospectively specified full-library FDA repurposing screen …"
- submission.md:14 (Abstract): states the contribution more flatly ("We report all results transparently …"), and submission.md:24 later repeats the claim without the "To our knowledge" qualifier in its summation ("It is a reanalysis … hypothesis-generating").

【Why it matters】 *Scientific Reports* does not require novelty for acceptance, so this is not a venue blocker — but a false or over-strong "first" is a *framing* liability the domain reviewer (A1) or editor can demolish. If any prior DRG+spinal CPSP meta-analysis exists, the unqualified claim collapses and drags down the paper's credibility on every other assertion. The inconsistent hedging (qualified in Intro, flat in Abstract) is itself a polish defect.

【Specific fix】 Use "To our knowledge" consistently in **both** the abstract and the introduction, and tighten the scope so each "first" is precisely bounded, e.g.: "To our knowledge, the first CPSP study to combine DRG and spinal-cord transcriptomes as a single axis via Stouffer meta-analysis *and* to lock hubs by a LODO-controlled dual-ML consensus." Drop the third "first" (full-library FDA screen) or phrase it as a methodological contribution rather than a novelty claim, since prospective full-library screens are not intrinsically novel.

---

## F7 — "Honest null" headline vs the body's candidate shortlist (framing tension)
【Problem】 The title and abstract foreground an "honest repurposing null," yet the Results/Discussion also present a prioritized Top-20 candidate set (precision@10 = 0.700, lift ×18.69) and advocate ADRA2A, producing an ambivalent central claim for the venue.

【Evidence】
- Title (submission.md:1) and abstract (submission.md:14): "honest repurposing null" / "honest full-library repurposing does not yet support a specific analgesic."
- submission.md:56: "composite (knowledge-informed) ranking showed precision@10 = 0.700 (lift ×18.69, p = 9.4e-9) … this score blends docking with pharmacological-prior terms, so it is a knowledge-informed prioritisation metric rather than docking evidence."
- submission.md:58 and 68: ADRA2A advocacy (see F4).

【Why it matters】 A "null" headline paired with a ranked candidate shortlist and target advocacy can read as hedged or contradictory to an editor deciding "what is this paper's claim?" The docking null and the knowledge-informed shortlist are genuinely different things, but the manuscript does not cleanly separate them in the abstract, which is the venue's shop window.

【Specific fix】 In the abstract, scope the "null" explicitly to docking enrichment and acknowledge the separate candidate shortlist: e.g., "the structure-based docking screen yielded an honest null (no target cleared all three filters), whereas a knowledge-informed composite ranking produced a separate, prospectively testable Top-20 candidate set." Keep "null" tied to docking throughout.

---

## F8 — Minor cross-document note: Supplementary does not repeat the repository URL
【Problem】 The Supplementary Information references "the reproduction repository (see Data availability)" (supplementary.md:7, 89) but does not print the actual URL, unlike the manuscript, cover letter, and Reporting Summary which all state `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`.

【Evidence】 supplementary.md:7 and :89 say "the reproduction repository (see Data availability)" / "the reproduction repository" without the URL; manuscript submission.md:136, cover_letter.md:15, reporting_summary.md:22/25 all carry the full URL.

【Why it matters】 Low severity — the Supplementary explicitly points to the Data Availability section, so a reader can find it. But for strict cross-document consistency (the brief requires the repo URL to agree across all four docs), the URL should appear verbatim at least once in the Supplementary too, so the file is self-contained.

【Specific fix】 Add the full URL once in supplementary.md (e.g., in the opening paragraph): `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`.

---

## § Stands up (verified compliant)
1. **Title length.** 15 words (`A neuroimmune–metabolic programme defines the chronic postsurgical pain DRG–spinal axis with an honest repurposing null`, submission.md:1). Limit ≤ 18 — **pass** (counted: A / neuroimmune–metabolic / programme / defines / the / chronic / postsurgical / pain / DRG–spinal / axis / with / an / honest / repurposing / null).
2. **Abstract length and citation-free.** 179 words, with **zero** superscript/citation markers (submission.md:14). Limit ≤ 200 and no references — **pass**.
3. **Display items ≤ 8.** Exactly 5 figures + 3 tables = 8 (submission.md:143, 162–166). Limit ≤ 8 — **pass**. Figure legends word-counted at 135 / 120 / 91 / 119 / 150 words, all well under the 350-word cap — **pass**.
4. **Figures supplied as separate ≥300 DPI PNGs.** All five PNGs exist in `figures/` (Fig1–Fig5) and each carries a pHYs chunk of ~320 DPI (Fig1 3526×1345, Fig2 2604×1375, Fig3 2049×1888, Fig4 2470×1447, Fig5 2204×1342) — **pass** on the DPI hard-limit.
5. **Methods placed last (after Discussion).** Document order is Title → Abstract → Introduction → Results → Discussion → Methods → References → back matter (submission.md:62 Discussion, :74 Methods) — **pass**.
6. **Mandatory declarations present and complete.** Author Contributions (submission.md:132–133), Data Availability (submission.md:135–136), Competing Interests (submission.md:139) all present — **pass**.
7. **AI-use disclosure in both Methods and Reporting Summary; no generative-AI imagery.** Methods (submission.md:98): "A large language model (LLM) was used to assist manuscript drafting and language polishing; … no LLM satisfies authorship criteria." Reporting Summary (reporting_summary.md:50–51): "An LLM assisted manuscript drafting/language polishing; … No LLM is an author." All figures are matplotlib plots (no generative-AI images) — **pass**.
8. **Data availability: real URL + "not available on request."** Manuscript (submission.md:136), Reporting Summary (reporting_summary.md:25), and cover letter (cover_letter.md:15) all give the identical real repo URL `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` (not a placeholder) and explicitly state data are "not available on request" — **pass** on cross-document agreement.
9. **Reference count ≤ 60.** Exactly 18 references (submission.md:107–125) — **pass**; and the reference count agrees across documents (no document asserts a different number).
10. **Competing-interests disclosure names the target and grant.** Both the manuscript and the cover letter disclose ADRA2A + Fujian Natural Science Foundation + "did not fund/did not influence" (submission.md:139, cover_letter.md:17) — meets the **minimum** standard (see F4 for the framing caveat).

---

## § Questions for the authors
1. **Orphan references.** Refs 5, 11, 12 are never cited in the text. Will you cite them where genuinely relevant, or delete them? (See F2.)
2. **ADRA2A bias guard.** Because ADRA2A is a listed candidate in your *own* pending grant (disclosed at submission.md:139), were the repeatedly favorable ADRA2A statements independently verified? Will you (a) generalize the biological-plausibility discussion to all 10 targets, or (b) add an explicit conflict-of-interest guard sentence and soften the "biologically plausible" language? (See F4.)
3. **Preprint reliance.** Is ref #8 intended as a key anatomical reference, and is the "Brain 2026 was incorrect" remark intentional, or should it be trimmed to a clean preprint citation? (See F5.)
4. **Novelty claim.** Can you confirm with a literature check that no prior DRG+spinal CPSP meta-analysis exists, and will you apply "To our knowledge" consistently in abstract and introduction and unbundle the three "firsts"? (See F6.)
5. **Reporting Summary completeness.** Will you add the Competing Interests block to the Reporting Summary so it matches the manuscript and cover letter? (See F3.)
6. **Repo URL in Supplementary.** Will you print the full repository URL once in the Supplementary for self-contained cross-document consistency? (See F8.)

---

## § What I actually checked
**Files read (only the four permitted):**
- `reports/MVP_ScientificReports_submission.md` (main manuscript; sections, references, display items, declarations).
- `reports/MVP_ScientificReports_supplementary.md` (S1–S4; title and repo references).
- `reports/MVP_ScientificReports_reporting_summary.md` (Nature Portfolio Reporting Summary; AI disclosure; absence of competing-interests block).
- `reports/MVP_ScientificReports_cover_letter.md` (title, repo URL, declarations, pre-upload checklist).

**Counts / checks run (verified from the files themselves):**
- Title word count = **15** (limit 18) — pass.
- Abstract word count = **179** (limit 200) and **0** citation/superscript markers — pass.
- Figure-legend word counts = **135 / 120 / 91 / 119 / 150** (limit 350 each) — pass.
- Display items = **5 figures + 3 tables = 8** (limit 8) — pass.
- Figure DPI: parsed the pHYs chunk of all five PNGs in `figures/` → ~**320 DPI** each (limit ≥300) — pass.
- References enumerated = **18** (limit 60) — pass.
- Cited reference numbers parsed from superscripts/ranges = {1,2,3,4,6,7,8,9,10,13,14,15,16,17,18}; **orphans = {5, 11, 12}** (refs 7/15/16 occur only inside the ranges `⁶⁻⁸` and `¹⁴⁻¹⁷`, hence legitimately cited).
- Methods-after-Discussion ordering confirmed by section sequence.
- Mandatory declarations (Author Contributions / Data Availability / Competing Interests) confirmed present at submission.md:132–139.
- AI-use disclosure confirmed in both Methods (submission.md:98) and Reporting Summary (reporting_summary.md:50–51); figures confirmed matplotlib (no generative-AI imagery).
- Repo URL `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` confirmed identical across manuscript, cover letter, Reporting Summary; "not available on request" confirmed.
- Cross-document title match confirmed (manuscript, supplementary, cover letter).
- Competing-interests disclosure present in manuscript + cover letter but **absent** from Reporting Summary (discrepancy → F3).
- ADRA2A favorable-framing passages located (submission.md:56, 58, 68) and checked against the "assessed uniformly" sentence (submission.md:58) and the disclosure (submission.md:139) → perceived-bias finding (F4).

**Discrepancies / gaps found:** Nature-style reference format mismatch (F1); 3 orphan references (F2); Reporting Summary missing Competing Interests (F3); ADRA2A framing vs disclosed interest (F4); preprint correction remark (F5); over-bundled/unhedged "first" claim (F6); "null" vs candidate-shortlist tension (F7); Supplementary omits repo URL (F8).

**Not flagged as defects (verified clean):** title/abstract limits, display-item count, figure DPI, Methods placement, mandatory declarations, AI disclosure, data-availability language, reference count ≤ 60, repo-URL agreement.

**Independence note:** I did not open the round-1 review, the submission manifest, PROJECT_PLAN, GITHUB_DEPOSIT_SOP, author_verification_statement, README, CITATION.cff, any other Round-2 reviewer file, or any gate script. All compliance judgments above are derived solely from the four documents listed and the figure files in `figures/`.
