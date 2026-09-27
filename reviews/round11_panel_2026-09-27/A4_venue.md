# A4 — Venue / Reporting-Standard Audit (PLOS ONE editor + STROBE checklist specialist)

**Role:** Independent peer-review panellist, venue-and-reporting lens.
**Manuscript under review:** *Conserved nerve-injury-associated transcriptional response on the DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null* (single author, Yang Y).
**Treatment:** First submission. I read only the five permitted reports, `scripts/build_sr_submission_pack.py`, `CITATION.cff`, and the data files referenced by the Data Availability statement. I did not read any prior-review, response, or revision artefacts.

---

## 0. Executive verdict

The manuscript is, on the whole, unusually disciplined for a computational reanalysis: it carries an explicit AI-use disclosure, an honest null, a real public GitHub repository, an IRB/exemption statement that matches the compliance note, and a complete (22/22) STROBE 2007 checklist. **However, one submission-blocking defect is present in the Data Availability statement — a literal placeholder Zenodo DOI (`10.5281/zenodo.XXXXXXX`) — and a second serious defect undermines the title single-source-of-truth: the build script and `CITATION.cff` still emit a *different, older* title than the manuscript/cover letter/compliance/supplementary/STROBE documents.** The build script in particular bakes the stale title into the `.docx` metadata, which is exactly the "gate only checks the first enumerated occurrence" trap.

I flag the data-availability placeholder as a **DESK-REJECT / T0 BLOCKER** per PLOS ONE's requirement of a real, immediately accessible repository, while noting that the underlying data *is* genuinely available via the public GitHub repo (verified live). The title divergence is ranked **T1**.

---

## 1. What stands up (with evidence)

**1.1 AI-use disclosure is explicit, names the tool, and correctly denies authorship — PLOS ONE policy met.**
- 【Evidence】 `reports/MVP_PLOSONE_submission.md:173` — *"A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing. The scientific design, all computational analyses, results and conclusions were conceived, executed and verified by the author; … No AI tool satisfies authorship criteria."* Cover letter `reports/MVP_PLOSONE_cover_letter.md:15` — *"A large language model assisted language drafting; all scientific content is solely the author's."* Compliance check item 15 (`reports/MVP_PLOSONE_compliance_check.md:27`) marks it PASS.
- 【Why it matters】 PLOS ONE requires authors to disclose AI assistance in manuscript preparation. This statement is complete: it names the specific model, scopes it to drafting/language polishing, affirms human ownership of content, and explicitly states no AI meets authorship criteria. This is a clean pass and need not be revised.

**1.2 Ethics / IRB statement is correctly framed for a public in-silico reanalysis and matches the compliance note.**
- 【Evidence】 `reports/MVP_PLOSONE_submission.md:175-176` — *"This study reanalysed publicly available, de-identified transcriptomics data from GEO. For the single human dataset … GSE158825 … the original deposition documents IRB approval and informed consent; … this secondary reanalysis required no further ethics approval."* Compliance §5 (`reports/MVP_PLOSONE_compliance_check.md:72-74`) repeats the GSE158825 IRB-in-deposition provenance verbatim.
- 【Why it matters】 For purely computational reanalysis of public, de-identified data, an IRB-exempt / "no new approval required" statement is appropriate, and the consistency between manuscript and compliance note is good. This satisfies PLOS ONE's ethics requirement and is not a blocker.

**1.3 Funding, Author Contributions, and Competing Interests are present, standalone, and consistent with single-authorship.**
- 【Evidence】 Funding (`submission.md:262-263`) — *"The author received no financial support for this work."* Author contributions (`:265-266`) — *"Y.Y. conceived the study, performed all computational analyses, interpreted the results, and wrote the manuscript."* Competing interests (`:275-276`) discloses the pending Fujian NSF grant that lists ADRA2A and states it did not influence the work.
- 【Why it matters】 The single-author contributions statement is honest about there being one author; the competing-interests disclosure of the pending grant is transparent and does not read as a conflict that taints the ADRA2A analysis (the manuscript explicitly holds ADRA2A to the same standard as the other nine targets). These elements pass PLOS ONE's structural requirements.

**1.4 Abstract structure, display-item count, and figure/table citations meet PLOS ONE format.**
- 【Evidence】 Abstract is explicitly sub-headed Background / Methods / Results / Conclusions (`submission.md:14-20`). Compliance items 3, 36-40 confirm 5 figures + 3 tables, all cited, legends present, PNG at 350 DPI. STROBE checklist is supplied as Supporting Information S8.
- 【Why it matters】 These are common format hard-fails; here they are satisfied. No action needed beyond the specific items in §4.

**1.5 The core data is genuinely available in a public repository (verified).**
- 【Evidence】 I resolved the repository URL live: `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` returns a public GitHub page ("Multi-dataset target lock-in and structure-based drug repurposing for chronic postsurgical pain (CPSP)"), MIT-licensed, with a full phase-by-phase script/table map. The Data Availability statement's listed derived tables (`META_bulkonly_meta.csv`, `META_bulkonly_sensitivity_summary.json`, `P6_target_plausibility.json`, `_R4_random_effects_meta.csv`, `_R4_nerveinjury_only_meta.csv`, `_R4_targetset_bootstrap.csv` and its companions) **all exist** in `results/tables/` (verified by directory listing). 
- 【Why it matters】 This is the substantive data-availability requirement: a real, accessible repository. It means the blocking issue in §4 (T0-1) is a *placeholder-DOI hygiene* problem, not a "data does not exist" problem — which materially narrows the fix (see T0-1 fix).

---

## 2. Questions for the authors

1. **On the Zenodo DOI:** At submission, will a real Zenodo DOI be minted and substituted into the Data Availability statement, or do you intend to rely solely on the public GitHub release for PLOS ONE's data-availability requirement? If the latter, the placeholder sentence must be deleted before upload.
2. **On the title:** Confirm which string is the canonical submission title — the "DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null" version used in the manuscript/cover/compliance/supplementary/STROBE, or the "dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null" version still hard-coded in `CITATION.cff` and `scripts/build_sr_submission_pack.py`. They must be made identical before the `.docx` is built.
3. **On the "not CPSP-specific" conclusion:** Given that the non-predictive incision result rests on a single, heterogeneous, underpowered incision arm (GSE267799 pools SMIR + LPI; day-32 SMIR samples are described as resolving), should the Conclusion be tempered from "rather than a CPSP-specific pathway" to "not demonstrated to be CPSP-specific by the available data"?
4. **On the 37/37 DOI claim:** Can you provide the machine-readable Crossref-resolution log behind the "37/37 references carry a verified DOI" assertion, given that the compliance check itself warns the legacy DOI scripts "must not be re-run"? An independent re-resolution would strengthen the claim.
5. **On the STROBE partial items:** Items 6, 13, and 14 are marked only "Partial"/"N/A (primary deposition)." For a reanalysis this is acceptable, but can you confirm a reviewer could still trace participant/eligibility flow for GSE158825 from the public deposition without ambiguity?

---

## 3. What I actually checked (files, greps, quotes, discrepancies)

**Files read (permitted):**
- `reports/MVP_PLOSONE_submission.md` (full, including the truncated-inline `[truncated]` markers which are part of the source text, not omissions on my side)
- `reports/MVP_PLOSONE_supplementary.md` (full)
- `reports/MVP_PLOSONE_cover_letter.md` (full)
- `reports/MVP_PLOSONE_compliance_check.md` (full)
- `reports/MVP_STROBE_checklist.md` (full)
- `CITATION.cff` (full)
- `scripts/build_sr_submission_pack.py` (full)
- Live resolution of `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing`

**Data-availability claims verified against `results/tables/`:** I listed the directory and grepped for every file named in the Data Availability statement (`META_bulkonly_meta.csv`, `META_bulkonly_sensitivity_summary.json`, `P6_target_plausibility.json`, `_R4_nerveinjury_only_meta.csv`, `_R4_random_effects_meta.csv`, `_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap.json`, `_R4_targetset_bootstrap_resamples.csv`). **All are present.** The data-availability statement is therefore truthful about *what exists*; the defect is the placeholder DOI, not missing files.

**Title string comparison (exact quotes):**

| Source | Title string (tail) |
|---|---|
| `submission.md:1` | *"...DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null"* |
| `cover_letter.md:3` | *"...DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null"* |
| `compliance_check.md:3` | *"...DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null"* |
| `supplementary.md:3` | *"...DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null"* |
| `STROBE_checklist.md:3` | *"...DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null"* |
| `CITATION.cff:3` | *"...dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"* |
| `build_sr_submission_pack.py:50-52` (`MS_TITLE`) | *"...dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"* |

**Discrepancy:** Five of seven artefacts carry Version A; `CITATION.cff` and the build script carry Version B (the older "non-predictive incision translation" phrasing). Critically, `build_sr_submission_pack.py:64` sets `cp.title = MS_TITLE`, so the *generated* `Manuscript.docx` core-property title will be Version B, while the visible H1 heading rendered from `submission.md:1` is Version A — and the cover letter (Version A) will be uploaded alongside it. A consistency gate that inspects only `submission.md` passes, while the artifact a reviewer/editor opens carries a mismatched metadata title.

**Zenodo placeholder grep:** `submission.md:271` contains the literal string `10.5281/zenodo.XXXXXXX`. `compliance_check.md:70` confirms it remains a placeholder: *"replace the `10.5281/zenodo.XXXXXXX` placeholder in the Data Availability statement with the minted DOI."* The cover letter contains no Zenodo DOI.

**Tense comparison (release/deposit):** Cover letter `:13` — *"released as version v1.0.0 with a MANIFEST.sha256 integrity manifest at submission"* (treated as done). Manuscript Data Availability `:269` — *"At submission the repository will be released as version v1.0.0"* (future). `:271` — *"A versioned Zenodo archive will be deposited at submission."* (future). The cover letter and the manuscript disagree on whether the release is complete or prospective.

---

## 4. Must-fix list (ranked; DESK-REJECT flag on the placeholder)

### T0 — BLOCKER (desk-reject risk)

**T0-1 · Data Availability statement contains a literal placeholder Zenodo DOI.**
- 【Problem】 The Data Availability statement presents a non-resolving DOI placeholder as the versioned archive, which is not an immediately accessible repository at submission.
- 【Evidence】 `reports/MVP_PLOSONE_submission.md:271` — *"A versioned Zenodo archive will be deposited at submission and will receive a citable DOI at that point (10.5281/zenodo.XXXXXXX, minted upon deposit)."* `reports/MVP_PLOSONE_compliance_check.md:70` — *"replace the `10.5281/zenodo.XXXXXXX` placeholder in the Data Availability statement with the minted DOI."* (command used: grep for `10.5281/zenodo` confined to the submission report; one hit at line 271.)
- 【Why it matters】 PLOS ONE requires data to be in a real, immediately accessible repository at submission. A placeholder DOI `10.5281/zenodo.XXXXXXX` does not resolve and must not appear in an uploaded manuscript; it is a honesty/blocking defect and, per the panel brief, triggers a DESK-REJECT flag. **Mitigating fact:** the public GitHub repo (verified live) already satisfies the substantive requirement, so this is a hygiene/placeholder problem rather than missing data.
- 【Specific fix】 Choose one of:
  - (a) Deposit the Zenodo snapshot, mint the real DOI, and replace `10.5281/zenodo.XXXXXXX` with the resolved `10.5281/zenodo.XXXXXX` (real) before upload; **or**
  - (b) Delete the Zenodo sentence entirely. The Data Availability statement already points to the public GitHub repo (`:269`), which is sufficient for PLOS ONE. Revised text for `:271`: *"The public GitHub repository (https://github.com/yyx-4113/cpsp-drg-spinal-repurposing) constitutes the versioned, citable archive of all code, tables, and figures at submission (release v1.0.0, MANIFEST.sha256). Data are not 'available on request'."* Either way, **no `XXXXXXX` placeholder may remain.**

### T1

**T1-1 · Title is not a single source of truth; build script and `CITATION.cff` emit a stale title into the artifact.**
- 【Problem】 Two different title strings circulate; the build script bakes the wrong (older) one into the `.docx` metadata, so the submitted Word file's title property will not match the manuscript body or the cover letter.
- 【Evidence】 See the table in §3. `CITATION.cff:3` and `build_sr_submission_pack.py:50-52` carry *"…dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"*; the five primary documents carry *"…DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null."* The build script `:64` assigns `cp.title = MS_TITLE` (the stale string).
- 【Why it matters】 PLOS ONE checks title consistency across metadata, manuscript, and cover letter. A `.docx` whose internal `core_properties.title` says "non-predictive incision translation" while its first heading and the cover letter say "dorsal root ganglion analysis with spinal-cord localisation" is an immediate editorial inconsistency and undermines the "consistency gate" that only inspects the `.md`.
- 【Specific fix】 Decide the canonical title (recommend the Version-A string already used by manuscript/cover/compliance/supplementary/STROBE). Then (i) set `MS_TITLE` in `scripts/build_sr_submission_pack.py:50-52` to that exact string; (ii) replace `CITATION.cff:3` `title:` with that exact string; (iii) rebuild `Manuscript.docx` and confirm `docx.core_properties.title` equals the body H1. Add a single canonical-title constant and reference it everywhere rather than re-typing the string.

### T2

**T2-1 · Tense conflict over "released/deposited at submission" between cover letter and manuscript.**
- 【Problem】 The cover letter presents the v1.0.0 release as already done "at submission," while the manuscript Data Availability statement presents both the GitHub release and the Zenodo deposit as future ("will be released"/"will be deposited").
- 【Evidence】 `cover_letter.md:13` — *"released as version v1.0.0 with a MANIFEST.sha256 integrity manifest at submission."* `submission.md:269` — *"At submission the repository will be released as version v1.0.0"*; `:271` — *"A versioned Zenodo archive will be deposited at submission."*
- 【Why it matters】 Inconsistent tense about whether the repository is publicly released creates ambiguity for the editor verifying data availability and for the version-lock the MANIFEST implies. It also interacts with T0-1 (if the deposit is genuinely future, the placeholder is even less defensible).
- 【Specific fix】 Align both documents to one factual tense. If the repo is public at submission, change `submission.md:269-271` to past/perfect ("released as v1.0.0 … A versioned Zenodo archive was deposited … DOI: 10.5281/zenodo.XXXXXX [real]"). If it is genuinely post-acceptance, change the cover letter to match and remove any implication of an existing v1.0.0 release.

**T2-2 · Title "DRG–spinal axis" overstates the meta core, which the manuscript itself concedes is DRG-only.**
- 【Problem】 The title and framing foreground a joint DRG–spinal "axis," but the manuscript explicitly states the Stouffer meta core is derived entirely from DRG (and DRG translatome) inputs, with the spinal component supplied by separate LODO/Visium analyses.
- 【Evidence】 `submission.md:44` — *"The Stouffer meta core is thus a DRG-axis product (all six inputs are DRG or DRG translatome); the spinal-cord dimension of the titular axis is supplied independently by the LODO spinal fold and the Visium…"*
- 【Why it matters】 Editors/readers scanning the title may expect a jointly-modelled DRG–spinal meta signature. The body correctly qualifies this, but the title leads with the stronger claim. This is an accuracy/honesty nuance, not a contradiction, yet it benefits from a hedged title or a one-line qualification near the title.
- 【Specific fix】 Either keep the title but ensure the first sentence of the Abstract/Introduction states the meta core is DRG-derived (it currently does at `:14`/`:44`), or adjust the title to "…on the DRG axis with spinal-cord localisation…" to avoid implying a joint meta. At minimum, do not let the title stand as the only statement of scope.

**T2-3 · The "not CPSP-specific" conclusion is drawn from a single, heterogeneous, underpowered incision comparison that the manuscript itself concedes is a weak test.**
- 【Problem】 Abstract and Conclusions assert the axis is "rather than a CPSP-specific pathway" based on the non-circular incision translation test, while the Methods concede this test is a single, heterogeneous, conservative bound.
- 【Evidence】 `submission.md:152` (Methods) — *"GSE267799 is a heterogeneous, two-model incision arm … the day-32 SMIR samples represent a resolving rather than established-chronic phenotype; … We therefore report the incision→nerve-injury translation as a conservative bound from a single, heterogeneous incision arm."* Contrast with `submission.md:20` (Abstract) and `:134` (Conclusions) — *"the DRG–spinal axis is a nerve-injury-associated … response rather than a CPSP-specific pathway."*
- 【Why it matters】 This is the closest the manuscript comes to the "limitation conceded in one place, strong claim left standing in another" pattern. The strong "rather than a CPSP-specific pathway" wording exceeds what a single, diluted incision comparison can support, even though the authors frame the test as conservative. A reviewer could reasonably object that the negative translation result is itself underpowered and therefore cannot establish absence of CPSP-specificity.
- 【Specific fix】 Soften the Conclusion/Abstract wording to match the conceded limitation, e.g. *"…the available data do not demonstrate CPSP-specificity; the nerve-injury signature did not predict the single incision arm examined (46.2% vs 47.1%, p = 0.14), a comparison limited by a single, heterogeneous incision dataset."* Keep the hedged phrasing; do not upgrade to a definitive negation.

### T3

**T3-1 · The "37/37 references carry a Crossref-verified DOI" claim is unverified by an independent, re-runnable check.**
- 【Problem】 The compliance check asserts all 37 references have verified DOIs, but it also states the legacy DOI/renumber scripts "must not be re-run," so the claim cannot be independently reproduced from the current source state.
- 【Evidence】 `compliance_check.md:5` — *"References: 37 / 37 carry a Crossref-verified DOI."* `:43-44` — *"All 37 references were matched against Crossref and verified against the real article metadata."* `:62` — *"the legacy `p7_renumber_refs.py` / `resolve_ref_dois.py` … must not be re-run after manual edits."*
- 【Why it matters】 Reference DOI accuracy is a PLOS ONE formatting requirement; an unverifiable "37/37" claim is a provenance risk. If even one DOI is stale or mis-matched, the journal's automated check will flag it.
- 【Specific fix】 Run an independent Crossref/DOI resolution over the final `submission.md` reference list (fresh script or manual spot-check of the 4 round-9/10 additions, especially the Cooper 2024 substitution at `:53` and Flatters 2008 at `:51`), and archive the resolution log. Do not rely on a script state that is declared non-rerunnable.

**T3-2 · STROBE Item 19 mislocates the "human DRG not directly measured" concession.**
- 【Problem】 The STROBE checklist cites "line 115 area" for the human-DRG-not-measured limitation, but the manuscript line ~115 is the docking section; the actual concession is in the Discussion.
- 【Evidence】 `STROBE_checklist.md:29` (Item 19) — *"human DRG not directly measured (line 115 area)."* `submission.md:128` (Discussion) — *"Direct DRG or spinal-cord biopsy is not clinically obtainable in CPSP patients…"* Line 115 of the manuscript is inside the docking eligibility paragraph, not the human-DRG point.
- 【Why it matters】 Minor, but a checklist cross-reference that points to the wrong line reduces the STROBE document's audit value and may prompt an editor to question whether limitations were carefully mapped.
- 【Specific fix】 Correct the Item 19 parenthetical to *"human DRG not directly measured (Discussion, line 128 area)"* (or the regenerated line number after final edits).

**T3-3 · Build script still identifies itself as a "Scientific Reports submission pack" builder.**
- 【Problem】 The PLOS ONE build script's docstring and comments describe a Scientific Reports / Anaesthesia pack, though it now emits PLOS ONE artefacts (`Cover_Letter_PLOSONE.docx`, `STROBE_Checklist.docx`).
- 【Evidence】 `build_sr_submission_pack.py:2` — *"Build the Scientific Reports submission pack from the v1.3 markdown sources."* `:5` — *"Changes for Scientific Reports / CPSP"*; `:382-387` mentions Nature 'Reporting Summary.' Yet `:356-369` builds `Cover_Letter_PLOSONE.docx` and `STROBE_Checklist.docx`.
- 【Why it matters】 Stale template identity raises the risk that a future build accidentally ships a Nature-style Reporting Summary or Scientific Reports page setup (Times New Roman 12 pt is actually PLOS-friendly, but the identity confusion is a process hazard).
- 【Specific fix】 Update the module docstring/comments to "PLOS ONE submission pack"; remove references to Scientific Reports / Anaesthesia / Nature Reporting Summary, or explicitly note they are not used.

**T3-4 · Repository README references a "repository DOI" that does not yet exist.**
- 【Problem】 The public GitHub README (verified live) says "Please cite both the article and the repository DOI," but no real repository DOI exists because the Data Availability statement still holds the Zenodo placeholder.
- 【Evidence】 Live GitHub README §8/§9: *"Please cite both the article and the repository DOI"*; manuscript `:271` placeholder. (README content observed during the §1.5 live check.)
- 【Why it matters】 A README promising a DOI that is only a placeholder is an external consistency hole; once T0-1 is fixed (real DOI or removed), ensure the README and the statement agree.
- 【Specific fix】 After resolving T0-1, either insert the real Zenodo DOI into the README or remove the "repository DOI" sentence so external and manuscript statements match.

**T3-5 · STROBE Items 6, 13, 14 are only "Partial"/"N/A (primary deposition)."**
- 【Problem】 These items lean on the primary GEO deposition for participant flow/eligibility/descriptive data; acceptable for a reanalysis but worth a confirm.
- 【Evidence】 `STROBE_checklist.md:16,23,24` mark Items 6, 13, 14 "Partial"/"N/A (primary deposition)."
- 【Why it matters】 For an in-silico reanalysis this is defensible, but an editor may ask for a short statement that the reanalysis inclusion rule (12 datasets decoded; two misclassifications corrected) is itself the "participants/eligibility" analogue. Low risk.
- 【Specific fix】 No change strictly required; optionally add one sentence under Methods clarifying that reanalysis eligibility = the 12-dataset decode rule, to pre-empt the "Partial" flag.

---

## 5. Internal-contradiction hunt (P0)

I searched for the pattern "a limitation conceded in one section while the original over-claim stands in another." Two side-by-side pairs are worth surfacing; both are *disclosed* in the text, so they are interpretive tensions rather than outright falsehoods, but they are the items most likely to draw an editor's "this is inconsistent" flag.

**Pair A — incision translation (T2-3 above), quoted side by side:**
- Conceded limitation — `submission.md:152`: *"GSE267799 is a heterogeneous, two-model incision arm … We therefore report the incision→nerve-injury translation as a conservative bound from a single, heterogeneous incision arm."*
- Standing claim — `submission.md:134` (Conclusions): *"the DRG–spinal axis is a nerve-injury-associated … response rather than a CPSP-specific pathway."*
- Assessment: The limitation concedes the test is a weak, single, heterogeneous bound; the Conclusion treats it as sufficient to characterise the axis as non-CPSP-specific. Not a logical contradiction (the wording is "rather than … specific," a comparative, and the test is described as conservative), but the strength of the Conclusion outruns the conceded evidence base. Fix as in T2-3.

**Pair B — "DRG–spinal axis" scope (T2-2 above), quoted side by side:**
- Conceded scope — `submission.md:44`: *"The Stouffer meta core is thus a DRG-axis product (all six inputs are DRG or DRG translatome); the spinal-cord dimension of the titular axis is supplied independently by the LODO spinal fold and the Visium…"*
- Standing title claim — `submission.md:1`: *"…on the DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null."*
- Assessment: The title advertises a joint DRG–spinal axis; the body clarifies the meta core is DRG-only with spinal input from separate analyses. This is reconciled in text but the title leads with the stronger framing. Fix as in T2-2.

**Explicitly checked and found NOT contradictory (to preclude re-litigation):**
- The "honest null" vs the Top-20 knowledge-informed retrieval: the manuscript repeatedly and explicitly scopes the Top-20 as "hypothesis-generating … not docking evidence" (`submission.md:124-126`). Consistent.
- OXPHOS "did not survive random-effects correction (q = 0.31)": stated identically in Abstract (`:18`), Results (`:48`), and Discussion (`:120`). Consistent.
- ADRA2A "inconclusive" vs "null": the manuscript labels it "inconclusive" (full-library AUC 0.532 NS; MW-adjusted 0.578, ΔAUC p≈0.0005) and explicitly distinguishes "NS" from "confirmed null" (`:112, :126`). The Abstract's single mention of ADRA2A quotes only the full-library p (`:18`), which is selective but not false; flagged only as T3-ish polish in T2-3's spirit.
- The docking "no target cleared both filters" claim coexists with "4/5 raw enrichment p-values remain significant after BH" in the supplementary (S4 reading, `supplementary.md:138`); the manuscript resolves this by defining the honest null as failure of the *size-independent* filter. Consistent and careful.

---

## 6. STROBE completeness assessment

The checklist addresses all 22 STROBE 2007 items (Items 1–22), with reanalysis-appropriate N/A markings for design/setting/recruitment items that belong to the primary GEO depositions. This is appropriate for a secondary in-silico reanalysis and meets the "complete" bar. Specific observations:
- **Item 1 (title/abstract design):** The checklist states the title does *not* name the design and that design is in the Abstract/metadata. The Abstract Background (`:14`) does say "We reanalysed 12 public GEO datasets," which is a reanalysis design statement — acceptable. No change required, but note the checklist's own phrasing should stay accurate (it currently is).
- **Items 6, 13, 14 (Partial/N/A):** Defensible for reanalysis; see T3-5.
- **Item 19 (Limitations):** Comprehensive and commendably honest (pseudoreplication avoided, translatome heterogeneity, ion channels undockable, human DRG not measured, translatome-dependence, causal scope disclaimed). The only defect is the mislocated cross-reference (T3-2).
- **Item 22 (Funding):** Addressed and consistent with the manuscript Funding section and the pending-grant competing-interests disclosure.

No STROBE item is missing; the checklist is submission-adequate once the T3-2 cross-reference is corrected.

---

## 7. Summary of ranking

| ID | Severity | Issue | Blocks submission? |
|---|---|---|---|
| T0-1 | **T0 / BLOCKER (DESK-REJECT flag)** | Placeholder Zenodo DOI `10.5281/zenodo.XXXXXXX` in Data Availability statement | Yes — must resolve |
| T1-1 | T1 | Title not single-source-of-truth; build script + `CITATION.cff` emit stale title into `.docx` metadata | Strongly advised pre-submission |
| T2-1 | T2 | Cover letter vs manuscript tense conflict on "released/deposited at submission" | Advised |
| T2-2 | T2 | Title "DRG–spinal axis" overstates DRG-only meta core (conceded in body) | Advised |
| T2-3 | T2 | "Not CPSP-specific" conclusion vs conceded single-heterogeneous-incision-arm limitation | Advised |
| T3-1 | T3 | "37/37 DOI" claim rests on non-rerunnable script; unverified | Polish |
| T3-2 | T3 | STROBE Item 19 mislocated line reference | Polish |
| T3-3 | T3 | Build script still self-identifies as Scientific Reports pack | Polish |
| T3-4 | T3 | README promises a repository DOI that is only a placeholder | Polish |
| T3-5 | T3 | STROBE Items 6/13/14 "Partial" — acceptable, optional clarification | Optional |

**Bottom line:** The manuscript is conceptually and reporting-strong, but **T0-1 is a desk-reject-class defect as submitted** and **T1-1 must be fixed before the `.docx` is built**. Everything in T2–T3 is achievable with targeted edits and does not, by itself, block submission once T0-1 and T1-1 are resolved.
