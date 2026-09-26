# A4 — VENUE / REPORTING-STANDARDS AUDIT

**Reviewer codename:** A4 (PLOS ONE handling-editor + reporting-guidelines auditor)
**Date:** 2026-09-27
**Manuscript:** *Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null*
**Venue under audit:** resubmission to **PLOS ONE** (SCIE), single-author, in-silico re-analysis

**Independence statement.** I reviewed this as a first submission I had never seen. I did not read
`reviews/REVIEW_*.md`, `reviews/RESPONSE_*.md`, `reviews/round2_*`…`round9_*`, `.workbuddy/memory/**`,
`SUBMISSION_MANIFEST.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, nor any other
reviewer's output in `reviews/round10_2026-09-26/`. I did not run `scripts/p7_renumber_refs.py` or
`scripts/resolve_ref_dois.py`. No file was modified.

**Bottom line.** The science reporting is unusually self-critical and the reference list is clean, but
the submission will **not** survive administrative/technical check in its present form: five of the eight
main display items are never cited in the text, one of the three main tables has no table content, the
Data Availability statement makes three claims that the repository does not support, and the manuscript
body still carries an internal revision changelog and a placeholder Zenodo DOI. One item
(**A4-05**) is a **DESK-REJECT risk** on PLOS ONE's data-availability policy.

---

## §1. PLOS ONE hard-format requirements

### A4-01 — Five of the eight main display items are never cited anywhere in the narrative text (MAJOR, administrative-return risk)

**【Problem】** Figures 2–5 and Tables 2 and 3 are listed in the "Display items" block but are never called
out in Results, Discussion or Methods; only Fig. 1 and Table 1b are cited in text.

**【Evidence】** Full-text scan of `reports/MVP_PLOSONE_submission.md` (332 lines) for the strings
`Fig. 1`…`Fig. 5`, `Table 1`…`Table 3`:

| Token | Lines containing it |
|---|---|
| `Fig. 1` | 48 (Results), 285 (display-item list) |
| `Fig. 2` | 288 only (display-item list) |
| `Fig. 3` | 291 only |
| `Fig. 4` | 294 only |
| `Fig. 5` | 297 only |
| `Table 1` | 8 (metadata), 52 (Results), 302, 313 |
| `Table 2` | 315 only (display-item list) |
| `Table 3` | 274 (Competing Interests), 318 (display-item list) |

So the only in-narrative display-item citation in the entire Results/Discussion is
`reports/MVP_PLOSONE_submission.md:52` — "**SCN-channel directions are model-dependent (Table 1b).**".
`Table 3` is cited only inside the Competing Interests paragraph (line 274), never in the Results section
that it belongs to.

**【Why it matters】** PLOS ONE's initial technical/formatting check requires that every figure and table
be cited in the main text, in numerical order. A submission in which 5 of 8 display items appear only in
an end-matter list is returned to the author before editorial triage, and — worse for credibility — it
tells the handling editor that the display items were bolted on after the fact rather than used to
present the results.

**【Specific fix】** Insert these exact sentences (they replace the existing opening sentence of the
paragraph at the cited line):

At `reports/MVP_PLOSONE_submission.md:62`, replace
`The dual-ML consensus identified 35 candidate hub genes; 32/35 (91%) fell inside the meta core signature.`
with:
`The dual-ML consensus identified 35 candidate hub genes (Table 2; Fig. 2); 32/35 (91%) fell inside the meta core signature.`

At `reports/MVP_PLOSONE_submission.md:74`, replace
`On the DRG side (GSE216039), 34/35 hubs were present (CRISP3 absent) and 25 passed detection; 20/25 localised to the injured/regenerating neuron subtype.`
with:
`On the DRG side (GSE216039), 34/35 hubs were present (CRISP3 absent) and 25 passed detection (Fig. 3); 20/25 localised to the injured/regenerating neuron subtype.`

At `reports/MVP_PLOSONE_submission.md:76`, replace
`On the spinal side (GSE328175), 33/35 hubs were present (CRISP3, REG3B absent), 24 detectable (mean pseudobulk expression > 0 in ≥1 lineage), and 20 were localisable across neuron/microglia/astrocyte/OPC (15 NotLocalisable).`
with:
`On the spinal side (GSE328175), 33/35 hubs were present (CRISP3, REG3B absent), 24 detectable (mean pseudobulk expression > 0 in ≥1 lineage), and 20 were localisable across neuron/microglia/astrocyte/OPC (15 NotLocalisable) (Fig. 4A).`

At `reports/MVP_PLOSONE_submission.md:78`, replace
`Visium spatial mapping (GSE325938) gave the 35 hubs their first spatial coordinates: 33/35 were detectably expressed in mouse spinal cord (CRISP3 and LNP1 were below the detection threshold), and 17 of 33 detectably expressed hubs (51.5%) were assigned to the dorsal horn on Sham/baseline tissue, no injury-arm spatial data were available.`
with:
`Visium spatial mapping (GSE325938) gave the 35 hubs their first spatial coordinates (Fig. 4B): 33/35 were detectably expressed in mouse spinal cord (CRISP3 and LNP1 were below the detection threshold), and 17 of 33 detectably expressed hubs (51.5%) were assigned to the dorsal horn on Sham/baseline tissue, no injury-arm spatial data were available.`

At `reports/MVP_PLOSONE_submission.md:88`, replace the opening clause
`We docked 3,085 dockable drugs (≈3,070 scored per target) against 10 tractable targets`
with:
`We docked 3,085 dockable drugs (≈3,070 scored per target) against 10 tractable targets (Fig. 5; Table 3)`

At `reports/MVP_PLOSONE_submission.md:92`, replace `*Panel A — biological candidates (n = 7):*` with
`*Table 3a, Panel A — biological candidates (n = 7):*`
and at line 104 replace
`*Panel B — accessibility / negative controls (n = 3; included only because a ligand-anchored holo PDB made them dockable):*`
with
`*Table 3a, Panel B — accessibility / negative controls (n = 3; included only because a ligand-anchored holo PDB made them dockable):*`

---

### A4-02 — The two target tables in Results carry no table number or caption (MAJOR)

**【Problem】** Two full markdown tables sit inside the Results narrative (Panel A, 7 rows; Panel B, 3 rows)
with no "Table" label and no caption, so they either read as unnumbered floating tables or are miscounted
as a 4th and 5th table.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:94` and `:106` are table header rows
(`| Target | meta_Z | meta_FDR | consistency | FDR_RE | n_holo_PDB | Known biological/pharmacological link |`).
The file contains exactly four markdown table separator rows — at lines **95, 107, 307, 323**. Lines 95
and 107 are the Panel A/Panel B tables; 307 is Table 1b; 323 is Table 3b. The display-item block says
Table 3a is "rendered in the Results 'Drug repurposing' section above"
(`reports/MVP_PLOSONE_submission.md:319`), but the tables themselves are not labelled `Table 3a`.

**【Why it matters】** PLOS ONE requires each table to carry a numbered caption directly above it. A
copy-editor will either strip the tables or renumber them, changing the declared "8 display items" to 10
and breaking the caption numbering. It also means the reader cannot tell that the Panel A/Panel B tables
*are* Table 3a.

**【Specific fix】** Insert the caption lines immediately above the tables:

At `reports/MVP_PLOSONE_submission.md:92`, replace the whole line with:
`**Table 3a. The ten tractable docking targets with meta-analytic support, structural tractability and biological plausibility.** *Panel A — biological candidates (n = 7):*`

At `reports/MVP_PLOSONE_submission.md:104`, replace the whole line with:
`*Table 3a, Panel B — accessibility / negative controls (n = 3; included only because a ligand-anchored holo PDB made them dockable):*`

---

### A4-03 — "Table 2" (a main display item) contains no table at all (MAJOR)

**【Problem】** Table 2 is declared as one of three main tables but its entire content is a prose
description plus a pointer to an external CSV; the 35 hub rows are not in the manuscript.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:315-316`:
`- **Table 2** 35 hub genes with method consensus and meta-core membership.`
`- 35 hubs; full three-method consensus (n_methods = 3): SPRR1A, ATF3, TFE3, CDHR5, GALNS (5/35). Exactly two-method consensus (n_methods = 2): the remaining 30. In meta core (32/35): all except REG3B, ANKRD1, MEGF11. Full per-gene table in `results/tables/P3_hub_genes.csv` …`
There is no table block under it (confirmed: table separator rows occur only at lines 95, 107, 307, 323).

**【Why it matters】** PLOS ONE requires main tables to be supplied in the manuscript file as editable
tables. A "table" that is a filename is treated as a missing display item; the submission is either
returned or the table is silently demoted, which then makes the "5 + 3 = 8" count wrong.

**【Specific fix】** Insert the full 35-row table under line 316. Spec: columns
`Symbol | n_methods | in_meta_core | bootstrap_recovery` ; rows in the same order as
`reports/MVP_PLOSONE_supplementary.md:15-49` (S1), with `bootstrap_recovery` taken from
`results/tables/P3_hub_bootstrap.csv`. Caption to place immediately above:
`**Table 2. The 35 candidate hub genes: dual-machine-learning consensus, meta-core membership and bootstrap recovery frequency.**`

---

### A4-04 — The manuscript body still carries an internal revision changelog (MAJOR)

**【Problem】** A blockquote immediately under the author line documents what "this version adds" — a
revision trail that must not appear in a submitted manuscript.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:8`:
`> **Manuscript metadata.** Reanalysis of public transcriptomes; no new wet-lab data were generated. This version adds a random-effects (DerSimonian–Laird) sensitivity meta-analysis with τ²/I² heterogeneity, set-level Benjamini–Hochberg correction across gene sets, a non-circular test of nerve-injury-to-incision translation, a bootstrap stability assessment of the docking target set, correction of three printed values (bulk-only OXPHOS polarity, human-miRNA pair count, spinal localisable count) and relabelling of Table 1b magnitudes as Z-statistics alongside the true log₂ fold-changes. This is preliminary research foundation for a pending grant; no grant number, no fund acknowledgement.`

**【Why it matters】** To a first-submission handling editor this reads as (a) evidence of prior review
rounds at another journal and (b) an admission that three printed values were previously wrong. Both are
handled, correctly and invisibly, by the internal response document — not by the manuscript. It also
duplicates the Competing Interests and Funding sections, where the grant point is already made
(lines 261, 274).

**【Specific fix】** Delete line 8 in its entirety. If the "preliminary foundation for a pending grant"
point must survive, it already does, correctly, at `reports/MVP_PLOSONE_submission.md:261`
(Funding) and `:274` (Competing Interests).

---

### A4-05 — Data Availability makes three claims the repository does not support (MAJOR — **DESK-REJECT RISK**)

**【Problem】** The Data Availability statement asserts that the pinned release v1.0.0 already contains
the headline Round-9 outputs, that file integrity is verifiable via `MANIFEST.sha256`, and that "all
code, tables and figures" are deposited. Verification against the repository shows: the only tag in the
repository, `v1.0.0`, contains **zero** `_R4_*` files; `MANIFEST.sha256` exists only in an
**untracked** `_manifest/` directory; and no real Zenodo DOI exists anywhere in the repository.

**【Evidence】**

1. `reports/MVP_PLOSONE_submission.md:267`:
   `All code, tables and figures are deposited in the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (version v1.0.0; README + CITATION.cff + MIT LICENSE + reproduction scripts; integrity verifiable via MANIFEST.sha256). The GitHub repository already contains all processed data (… the random-effects and non-circular translation outputs `_R4_random_effects_meta.csv` and `_R4_nerveinjury_only_meta.csv`, and the target-set bootstrap `_R4_targetset_bootstrap.csv` with its per-resample recovery sets `_R4_targetset_bootstrap_resamples.csv`).`
   Repository check: `git tag -l` returns only `v1.0.0`; `git rev-list --count v1.0.0..HEAD` = **4**
   (the tag points at commit `5cfa2fb`, four commits behind HEAD);
   `git ls-tree --name-only v1.0.0 results/tables/ | grep -c '_R4_'` = **0**;
   `git ls-tree --name-only HEAD results/tables/ | grep '_R4_'` = **13 files**.
   So the three named `_R4_` artefacts exist only **after** the pinned release.
2. `MANIFEST.sha256`: `git ls-files _manifest` returns **nothing** (untracked); the only copy is
   `_manifest/MANIFEST.sha256`. It is therefore absent from the GitHub repository, and a reader
   following the stated URL cannot verify integrity.
3. Zenodo: a repository-wide scan for the pattern `10\.5281/zenodo\.[0-9]+` returns **0 matches**. The
   only Zenodo string in the whole tree is the placeholder at
   `reports/MVP_PLOSONE_submission.md:269`.

**【Why it matters】** PLOS ONE's data-availability policy requires that the underlying data be available
**at submission**, and the journal treats an availability statement that does not match reality as an
editorial-integrity issue rather than a copy-editing issue. Three independently false assertions in one
paragraph — including the specific claim that the pinned release contains the files that carry the
paper's headline results (random-effects shrinkage, set-level BH, non-circular translation) — is the
single most likely trigger for a desk rejection or an immediate "return to author" in this submission.

**【Specific fix】** Three edits:

(a) Cut the release v1.0.0 from the current HEAD (or create `v1.1.0` including `results/tables/_R4_*`), then
replace the first two sentences of `reports/MVP_PLOSONE_submission.md:267` with:
`All code, tables and figures are deposited in the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (release v1.1.0, commit <40-hex SHA>; README + CITATION.cff + MIT LICENSE + reproduction scripts). The repository at that release already contains all processed data underpinning the reported numbers, including the random-effects and non-circular translation outputs (results/tables/_R4_random_effects_meta.csv, _R4_nerveinjury_only_meta.csv) and the target-set bootstrap (_R4_targetset_bootstrap.csv with _R4_targetset_bootstrap_resamples.csv).`

(b) Move `_manifest/MANIFEST.sha256` to the repository root and `git add` it, or delete the parenthetical
`; integrity verifiable via MANIFEST.sha256` from line 267 and from
`reports/MVP_PLOSONE_cover_letter.md:13`.

(c) Replace `reports/MVP_PLOSONE_submission.md:269` (see A4-06).

---

### A4-06 — Placeholder Zenodo DOI (`10.5281/zenodo.XXXXXXX`) inside the manuscript text (MAJOR)

**【Problem】** The manuscript contains an un-minted DOI placeholder and a description of Zenodo's
workflow that is not how Zenodo works.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:269`:
`A versioned Zenodo archive will be deposited at submission; upon acceptance it will receive a citable permanent DOI (10.5281/zenodo.XXXXXXX, to be minted) that archives the GitHub release v1.0.0.`
The same placeholder is present in the built artefact: `submission_pack/Manuscript.docx` contains
`zenodo.XXXXXXX` ×1 and `10.5281` ×1 (verified by extracting `word/document.xml`).

**【Why it matters】** (i) A placeholder DOI in the manuscript body is a technical-check failure — it will
be typeset verbatim if the paper is accepted unchanged. (ii) "will be deposited at submission … upon
acceptance it will receive a DOI" is internally contradictory and factually wrong: Zenodo mints the DOI
at deposit/publish time, not at journal acceptance; an editor who knows this will read the sentence as an
unfounded promise. (iii) It compounds A4-05 by promising to archive a release (v1.0.0) that lacks the
headline outputs.

**【Specific fix】** Deposit to Zenodo **before** upload, then replace line 269 with (substituting the real
DOI):
`A versioned snapshot of the repository is archived at Zenodo (https://doi.org/10.5281/zenodo.<real-DOI>), which archives GitHub release v1.1.0 and mints an immutable, citable DOI for the exact files analysed here.`
If the deposit genuinely cannot be made before upload, delete line 269 entirely and rely on the GitHub
release; do **not** print a placeholder.

---

### A4-07 — Supplementary items S1, S3, S7 and "S5b" are never cited, and "S5b" is not a PLOS label (MINOR)

**【Problem】** Four of the eight supplementary tables are not referenced in the manuscript text, and the
SI uses a non-standard "S5b" label.

**【Evidence】** In-text supplementary citations in `reports/MVP_PLOSONE_submission.md` occur only at
lines 78, 124, 128, 148, 155, 164, 167, 295, 298, 332 and cover only **S2, S4, S5, S6**. There is no
in-text citation for **S1**, **S3**, **S7**, or **S5b**. `reports/MVP_PLOSONE_supplementary.md:166`
introduces `## Supplementary Table S5b.`; the manuscript's SI list
(`reports/MVP_PLOSONE_submission.md:332`) enumerates only **S1–S7** and never mentions S5b, while
`reports/MVP_PLOSONE_supplementary.md:7` states "seven supplementary tables (S1–S7)". PLOS naming is
`S1 Table` / `S1 Fig`, not "Supplementary Table S1".

**【Why it matters】** PLOS ONE requires every Supporting Information file to be cited in the text by its
`S#` label and listed with a one-line caption. An uncited S-file is flagged at technical check, and an
`S5b` label breaks the upload mapping (`S1`…`S8`).

**【Specific fix】**
1. Renumber `Supplementary Table S5b` → `Supplementary Table S6` and shift the existing S6 → S7, S7 → S8.
2. Cite the three uncited items in the text. Paste-ready insertions:
   - After `reports/MVP_PLOSONE_submission.md:74` (DRG localisation paragraph), append:
     `Per-hub cross-dataset lineage calls are tabulated in S1 Table, and per-hub spinal regionalisation in S2 Table.`
   - After `reports/MVP_PLOSONE_submission.md:88` (docking paragraph), append:
     `Full reverse-control counts and known-binder lists are given in S3 Table.`
   - After `reports/MVP_PLOSONE_submission.md:66` (bootstrap paragraph), append:
     `Set-level and per-gene bootstrap recovery frequencies are given in S7 Table.`
3. Rewrite the SI list at `reports/MVP_PLOSONE_submission.md:332` to use `S1 Table` … `S8 Table`
   captions and to include the renumbered gene-set-BH table.

---

### A4-08 — In-text citations are bare superscripts, not PLOS-style bracketed numbers (MINOR)

**【Problem】** The manuscript cites as `¹`, `²`, `¹³,¹⁴,¹⁵` — PLOS ONE's Vancouver style is bracketed
numbers in the running text.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:32`: `…imposing a substantial and under-served burden on quality of life and healthcare cost¹.`;
`reports/MVP_PLOSONE_submission.md:52`: `…contributes to neuropathic pain¹⁰;`. No `[` `]` citation
delimiters occur anywhere in the reference-calling text.

**【Why it matters】** Cosmetic at production (PLOS typesets citations), but it is one of the items PLOS's
initial formatting screen looks at, and it costs nothing to fix before upload.

**【Specific fix】** Convert every superscript run to bracketed form, e.g. `…healthcare cost¹.` →
`…healthcare cost [1].` and `…neuropathic pain¹⁰;` → `…neuropathic pain [10];`, `¹³,¹⁴,¹⁵` → `[13–15]`.

---

### A4-09 — "## Additional Information" is a *Scientific Reports* section heading (MINOR)

**【Problem】** A leftover non-PLOS section heading survives in the manuscript.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:276-277`:
`## Additional Information`
`This manuscript is a reanalysis of public transcriptomes and is hypothesis-generating rather than causal. No wet-lab data were generated. Competing interests are declared above under the stand-alone heading. The STROBE checklist for this observational reanalysis is provided as Supporting Information (`MVP_STROBE_checklist.md`).`
"Additional Information" is a *Scientific Reports* convention; PLOS ONE has no such section. The block
also sits **after** Competing Interests and **before** the Display items block, so the file ends with
figure legends after the declarations — unusual ordering for PLOS ONE.

**【Why it matters】** Signals an unadapted transfer from the previously desk-rejected venue; a handling
editor who recognises it will look harder for other unadapted remnants (and will find them, see A4-04).

**【Specific fix】** Delete the heading and move its one substantive sentence into the Methods. Replace
lines 276–277 with:
`## Supporting Information`
`The STROBE checklist for this observational reanalysis is provided as Supporting Information (S8 Checklist).`

---

### A4-10 — Discussion contains a sentence fragment in a load-bearing position (MINOR)

**【Problem】** The sentence that conveys the OXPHOS finding in the Discussion has no finite verb.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:120` contains:
`In the fixed-effect analysis only, OXPHOS suppression (which did not survive random-effects correction, q = 0.31), consistent with the growing literature on microglial–complement and energy-metabolism dysfunction in chronic and neuropathic pain²⁴,²⁵,²⁸,²⁹,³⁰,³¹, and with prior multi-tissue CPSP resources including a DRG-containing dataset⁶ and a spinal-cord neuropathic-pain atlas⁷.`

**【Why it matters】** This is the Discussion's statement of one of the two gene-set findings; a fragment
here is read as carelessness in exactly the paragraph where the hedging ("fixed-effect analysis only")
matters most, and it invites a copy-editor to "fix" the hedge away.

**【Specific fix】** Replace with:
`OXPHOS suppression was significant in the fixed-effect analysis only (it did not survive random-effects correction, q = 0.31), a direction consistent with the growing literature on microglial–complement and energy-metabolism dysfunction in chronic and neuropathic pain²⁴,²⁵,²⁸,²⁹,³⁰,³¹ and with prior multi-tissue CPSP resources including a DRG-containing dataset⁶ and a spinal-cord neuropathic-pain atlas⁷.`

---

### A4-11 — Duplicated phrase "to our knowledge" inside a single sentence (COSMETIC)

**【Problem】** The same hedge appears twice in one sentence and a third time in the same sentence.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:36`: `To our knowledge, this is, to our knowledge, among the first CPSP-adjacent studies … and, to our knowledge, among the first to identify hubs …`

**【Why it matters】** A duplicated hedge in the priority claim draws attention to the claim itself, which
is the one sentence an editor reads for novelty.

**【Specific fix】** Replace with:
`To our knowledge, this is among the first CPSP-adjacent studies to integrate DRG and spinal-cord transcriptomes as a single axis via multi-dataset meta-analysis (recent single-tissue resources include a multi-tissue CPSP DRG dataset⁶ and a spinal-cord neuropathic-pain atlas⁷), and among the first to identify hubs by a dual-ML consensus under LODO leakage control and to report a prospectively specified full-library FDA repurposing screen that, despite reverse controls, yielded no reliable enrichment, turning an honest null into an explicit methodological boundary.`

---

### A4-12 — "Data are not 'available on request'." is a meta-commentary sentence (COSMETIC)

**【Problem】** The Data Availability section ends with a sentence addressed to the journal's compliance
software rather than to the reader.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:271`: `Data are not "available on request".`

**【Why it matters】** Reads as defensive; the absence of an "on request" statement is already obvious.
Minor credibility cost with no benefit.

**【Specific fix】** Delete line 271.

---

## §2. STROBE checklist honesty

### A4-13 — Every line pointer in the STROBE checklist is misaligned with the submitted manuscript (MAJOR)

**【Problem】** The checklist justifies each item by citing manuscript line numbers; I spot-checked the
pointers and **none** of them lands on the content it claims. A reporting-guidelines auditor cannot
verify a single row.

**【Evidence】** `reports/MVP_STROBE_checklist.md` vs `reports/MVP_PLOSONE_submission.md` (332 lines):

| Checklist row | Claimed location | Actual content at that line |
|---|---|---|
| Item 2 (line 12) | `Introduction/Abstract (lines 7–13, 38–43)` | line 7 blank, 13 blank, 38 `---`, 43 blank. Abstract is at 14–21; Introduction at 30–36. |
| Item 5 (line 15) | `Ethics statement (line 164)` | line 164 is `### Single-cell & spatial localisation`. Ethics statement is at **175–176**. |
| Item 6 (line 16) | `Methods, Data curation (line 129)` | line 129 blank. Data curation is at **140**. |
| Item 10 (line 20) | `16,552 genes tested … (line 249)` | line 249 is reference **33 (Luo)**. The figure is at **44** and **303**. |
| Item 12 (line 22) | `Software/scripts in public repo (line 217)` | line 217 is reference **17 (Faber)**. Data availability is at **267**. |
| Item 22 (line 32) | `Funding (line 211)` / `Competing interests (line 220)` | line 211 is reference **14 (Cox)**; line 220 is blank. Funding is at **260–261**; Competing Interests at **273–274**. |

**【Why it matters】** A checklist whose cross-references are all wrong is worse than no checklist: the
editor's first move is to open the cited line, find the wrong content, and conclude the "Addressed"
statuses were not actually checked. For a paper whose central selling point is honesty, this lands badly.

**【Specific fix】** Regenerate the checklist with page/line numbers taken from the **final** submission
file, or replace every line pointer with a section name plus a short verbatim quote, e.g. for Item 22:
`Addressed. "## Funding" — "The author received no financial support for this work."`

---

### A4-14 — Item 16 states a number that contradicts the manuscript (MAJOR)

**【Problem】** The "Main results" row of the checklist misreports the ADRA2A Tier-1 AUC as 0.532.

**【Evidence】** `reports/MVP_STROBE_checklist.md:26`:
`Addressed. Results (lines 42–52): coordinated neuroimmune/DAM/complement↑ and OXPHOS↓; 35 hubs; full-library docking null (ADRA2A Tier-1 AUC 0.532, p = 0.118 NS).`
Manuscript `reports/MVP_PLOSONE_submission.md:112`: `ADRA2A reached AUC 0.618 on the 620-drug CNS/analgesic-prior subset (Tier 1) but collapsed to 0.532 (p = 0.118, NS) across all 3,085 drugs`.
0.618 is the Tier-1 value; 0.532 is the full-library value.

**【Why it matters】** This is the exact confusion the manuscript exists to prevent (Tier-1 subset vs
full library). Finding it inside the reporting checklist destroys the document's credibility as an audit
trail, and a reviewer who sees "Tier-1 AUC 0.532" may suspect the headline "breadth flip" was
retrofitted.

**【Specific fix】** Replace the parenthetical with:
`full-library docking null: ADRA2A Tier-1 (620-drug subset) AUC 0.618 collapsed to full-library (3,085-drug) AUC 0.532, p = 0.118, NS`

---

### A4-15 — Item 14 justifies the absence of participant descriptors with a statement the manuscript contradicts (MAJOR)

**【Problem】** The checklist claims the GSE158825 deposition provides "no per-participant covariates
beyond case/control status"; the manuscript itself analyses a continuous per-participant pain outcome.

**【Evidence】** `reports/MVP_STROBE_checklist.md:24`:
`… no participant-level clinical descriptors are tabulated because the public deposition provides no per-participant covariates beyond case/control status, so item 14 is addressed for the genomic summaries and explicitly not applicable to a participant-level descriptive table.`
Manuscript `reports/MVP_PLOSONE_submission.md:161`:
`GSE158825 (n=60 human plasma miRNA; lumbar surgery + pain outcome %nprs20delta) was tested by Welch+BH and Spearman+BH.`
Manuscript `reports/MVP_PLOSONE_submission.md:70`: `neither LSS+DS vs LSS (min p = 1.3e-4, FDR 0.128) nor association with %nprs20delta (min p = 8.5e-4, FDR 0.556) reached FDR significance`.

**【Why it matters】** STROBE Item 14 (descriptive data) is the item a PLOS editor checks first when a
human cohort is present, because missing participant descriptors are the classic reason to request a
revision. Asserting the covariates do not exist when the paper reports an analysis *on* one is a factual
error in a compliance document — and it forecloses the cheaper fix (tabulate what the deposition does
provide).

**【Specific fix】** Replace the justification clause with:
`The deposition provides the pain-outcome variable %nprs20delta and case/control status but no age/sex or comorbidity covariates; because the deposition is de-identified and supplies no demographic covariates, item 14 is met for the genomic summaries and for the available phenotype variable, and a participant-level descriptive table of demographics cannot be produced from the public data.`
And add to the manuscript, after `reports/MVP_PLOSONE_submission.md:70`, the sentence:
`The GSE158825 deposition provides no age, sex or comorbidity covariates, so no participant-level descriptive table can be reported; the only participant-level variables available to this reanalysis were group status (LSS+DS vs LSS) and the continuous pain outcome %nprs20delta.`

---

### A4-16 — Item 9 (Bias) is marked "Addressed" but contains no study-level risk-of-bias or publication-bias assessment (MAJOR)

**【Problem】** The checklist's Item 9 lists technical harmonisation steps as bias control; it does not
report any risk-of-bias assessment of the 12 included datasets, any small-study/publication-bias
assessment across the five meta-analysed studies, or any assessment of the animal studies' randomisation
and blinding.

**【Evidence】** `reports/MVP_STROBE_checklist.md:19`:
`Addressed. Key bias controls: cross-species upper-case harmonisation; direction-consistency filter (K≥3, lines 134); non-circular translation test using the incision contrast as held-out (line 138); pseudoreplication avoided by sample-level pseudobulk only (line 152); docking reverse positive controls + MW-confounder correction (line 155); GSE265957 non-independence disclosed (lines 131, 140).`
Every item in that list is an analytic-bias control *within* this reanalysis. The manuscript contains no
risk-of-bias table for the source studies, no funnel-plot/Egger-type small-study assessment across the
five studies (n per group ranges from 2/2 to 14/14), and no statement about blinding or randomisation in
the animal depositions.

**【Why it matters】** For a meta-analysis with per-group n as low as 2 (`GSE265957 D4 2/2 and D63 2/2`,
`reports/MVP_PLOSONE_submission.md:146`), the dominant bias is at the level of the *source* studies, not
the reanalysis. Marking Item 9 "Addressed" on the strength of internal controls invites the reviewer to
ask why the source-level bias was never assessed, and it is precisely the kind of over-claim that turns a
Major revision into a second round.

**【Specific fix】** Change the status to `Partial` and add:
`Partial. Within-reanalysis analytic biases are controlled (see list). Bias arising from the source studies is not assessed: no risk-of-bias tool was applied to the 12 depositions, no randomisation/blinding information was extracted, and no small-study or publication-bias assessment (e.g., funnel-plot asymmetry, Egger test) was performed across the five meta-analysed studies, which is not feasible with five contrasts, two of which come from the same animals at n = 2 per group.`
Add the corresponding sentence to the manuscript's Limitations (after `reports/MVP_PLOSONE_submission.md:128`):
`We did not apply a formal risk-of-bias tool to the source depositions and did not assess small-study or publication bias across the five meta-analysed studies; with five contrasts, two of them from the same animals at n = 2 per group, such an assessment would not be informative.`

---

### A4-17 — Item 1 concedes the title does not name the design, but the design term is also absent from the title's own framing (MINOR)

**【Problem】** STROBE Item 1 asks for the design in the **title or the abstract**; the checklist relies on
the abstract, but the abstract's design term ("Stouffer meta-analysis") is applied to 12 datasets, only 5
of which were meta-analysed (see A4-20), so the design statement is itself inaccurate where it is made.

**【Evidence】** `reports/MVP_STROBE_checklist.md:11`:
`Addressed. The title does **not** name the design; the design is stated in the Abstract (Background/Methods: 12 GEO datasets → Stouffer meta → dual-ML hub ID → docking) …`

**【Why it matters】** Acceptable in principle (STROBE permits design-in-abstract), but the abstract design
sentence is wrong (A4-20), so the item cannot be marked Addressed until A4-20 is fixed.

**【Specific fix】** Fix A4-20, then keep Item 1 as `Addressed via the abstract (STROBE Item 1 permits design in the title or the abstract)`. Optionally add "in-silico" to the title: `…: an in-silico multi-dataset reanalysis`.

---

### A4-18 — STROBE is the wrong reporting guideline for this design, and the manuscript does not say so (MINOR)

**【Problem】** STROBE governs cohort/case-control/cross-sectional epidemiological studies. This is a
transcriptome meta-analysis plus a docking screen with one small human miRNA layer; the checklist's
"Addressed" statuses are largely about genomic aggregates.

**【Evidence】** `reports/MVP_STROBE_checklist.md:5` declares `STROBE 2007` and restricts the
STROBE-indexed cohort to GSE158825, yet items 7, 8, 11, 12, 15, 16, 17 are answered with genomic content.
`reports/MVP_PLOSONE_compliance_check.md:65` itself concedes: `computational/observational study — no specific EQUATOR checklist mandated`.

**【Why it matters】** An editor who sees a STROBE checklist on a bioinformatics paper may read it as
guideline-shopping — an attempt to borrow epidemiological authority for an in-silico study. Naming the
limitation yourself removes the suspicion.

**【Specific fix】** Add to the top of the checklist, before the table:
`Guideline-scope note: STROBE (2007) is designed for cohort, case-control and cross-sectional epidemiological studies. It is supplied here because one reanalysed dataset (GSE158825, n = 60) is a human observational cohort with a pain outcome; for the eleven animal/in-vitro transcriptomes and for the docking screen it is applied by analogy, and items that presuppose primary recruitment, exposure ascertainment, follow-up or participant-level descriptive data are marked N/A (primary deposition) or Partial rather than Addressed.`

---

## §3. AI-use disclosure

### A4-19 — The AI disclosure is absent from the cover letter and does not name the tool there (MAJOR)

**【Problem】** PLOS ONE requires generative-AI use to be disclosed in the cover letter. The cover letter
discloses "a large language model" without naming it, while the manuscript names "Claude, Anthropic" —
the two documents disagree on specificity.

**【Evidence】**
- Manuscript `reports/MVP_PLOSONE_submission.md:173`: `A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing. The scientific design, all computational analyses, results and conclusions were conceived, executed and verified by the author; every AI-generated or AI-edited sentence was checked by the author against the result tables and scripts and corrected where needed, and no AI tool was used to generate, select or interpret data. No AI tool satisfies authorship criteria.`
- Cover letter `reports/MVP_PLOSONE_cover_letter.md:15`: `A large language model assisted language drafting; all scientific content is solely the author's.`
- The same weak sentence is in the built artefact `submission_pack/Cover_Letter_PLOSONE.docx` (`large language model` ×1, verified in `word/document.xml`).

**【Why it matters】** The cover letter is the document the handling editor reads first and the one PLOS
points at for AI disclosure. "A large language model assisted language drafting" is not a named tool, does
not say who verified the output, and does not state that the tool is not an author — all three of which
the manuscript version *does* say. A mismatch between the two disclosures is itself a red flag.

**【Specific fix】** Replace the final sentence of `reports/MVP_PLOSONE_cover_letter.md:15` with:
`Generative-AI disclosure: a generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing only. The scientific design, all computational analyses, results and conclusions were conceived, executed and verified by the author alone; every AI-generated or AI-edited sentence was checked by the author against the result tables and scripts and corrected where needed. No AI tool was used to generate, select or interpret data, and no AI tool meets PLOS's authorship criteria.`

---

### A4-20 — The manuscript AI disclosure is well-formed but incompletely scoped and unversioned (MINOR)

**【Problem】** The in-manuscript disclosure names the tool, states what it was used for, who verified, and
that it is not an author — but it is silent on model version/date and on whether AI was used to write or
debug the analysis code, and it is buried inside a Methods sub-section whose title is
"Statistical discipline, causal scope and AI-use disclosure".

**【Evidence】** `reports/MVP_PLOSONE_submission.md:172` heading and `:173` sentence (quoted in A4-19).
There is no version ("Claude" only), no date, and no statement about code generation. The repository
contains AI-authored-looking helper scripts (e.g. `_zenodo_deposit_local.py`, `_api_push.py`) which the
disclosure does not address.

**【Why it matters】** PLOS ONE's policy asks for "how the tool was used". "Manuscript drafting and
language polishing" is a complete answer only if code generation is excluded; the manuscript claims
`all computational analyses … were … executed by the author`, which does not exclude AI assistance in
writing the scripts. An editor who asks and gets a different answer than the printed one has an
integrity problem on their hands.

**【Specific fix】** Replace the first sentence of `reports/MVP_PLOSONE_submission.md:173` with:
`Generative-AI disclosure: a generative AI language model (Claude, Anthropic; accessed 2026, model version as provided by the vendor at the time of use) was used to assist manuscript drafting, language polishing and the editing of analysis scripts; it was not used to design the study, to generate, select or interpret data, or to produce any reported number.`

---

## §4. Ethics statement

### A4-21 — Ethics statement: correct attribution, no implied new approval — this stands up (see § Stands up, item 6)

Nothing to fix; recorded for completeness. The one actionable improvement is below.

### A4-22 — IRB name and approval identifier are withheld without saying why (MINOR)

**【Problem】** The statement says the IRB and its identifier are "not independently reproduced here" but
does not say whether they were even retrievable, so a reader cannot tell whether the author verified them
or never looked.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:176`: `… the approving IRB and its approval identifier are recorded in the GSE158825 data deposit (accession GSE158825) and are not independently reproduced here, and the data were accessed in de-identified form; this secondary reanalysis required no further ethics approval.`

**【Why it matters】** PLOS ONE's human-subjects policy expects the ethics committee and reference number
where they exist. "Not reproduced" is honest but incomplete: the editor cannot distinguish
"verified but not copied" from "not verified".

**【Specific fix】** Append:
`The IRB of record and its approval identifier were read from the GSE158825 deposition during data curation and are not reprinted here because this reanalysis holds no approval of its own; the deposition-level provenance can be inspected at the accession. Written informed consent for the original sample collection is documented in the same deposition.`
(Delete the consent clause if the deposition does not in fact state written consent; see § Questions.)

---

## §5. Cross-document consistency

### A4-23 — The compliance document misnumbers three references it claims to have added (MAJOR)

**【Problem】** `MVP_PLOSONE_compliance_check.md` §3.1 assigns reference numbers 34/35/36 to papers that
are numbered 23/11/12 in the manuscript.

**【Evidence】** `reports/MVP_PLOSONE_compliance_check.md:47-50`:
`- **34.** Bertoch, T. et al. … doi:10.1097/ALN.0000000000005460`
`- **35.** Yin, R. et al. … doi:10.3109/00207454.2015.1004172`
`- **36.** Cooper, A. H. et al. … doi:10.1097/j.pain.0000000000003321`
Actual numbering in `reports/MVP_PLOSONE_submission.md`: **23** = Bertoch, **11** = Yin, **12** = Cooper;
**34** = Xiao, **35** = Pushpakom, **36** = Irwin (verified: 36 entries, numbers 1–36 in order).
`reports/MVP_PLOSONE_compliance_check.md:52` compounds it: `it was **replaced by Cooper et al. 2024**` —
Cooper is [12], not [36].

**【Why it matters】** The document that certifies "Reference DOIs — resolved" cannot itself keep the
reference numbers straight. If it travels with the submission (it is listed in the submission set), the
editor sees an internal document contradicting the manuscript on the very item it is certifying.

**【Specific fix】** Replace the three bullets with:
`- **23.** Bertoch, T. et al. … doi:10.1097/ALN.0000000000005460`
`- **11.** Yin, R. et al. … doi:10.3109/00207454.2015.1004172`
`- **12.** Cooper, A. H. et al. … doi:10.1097/j.pain.0000000000003321`
and change line 52 to `… it was **replaced by Cooper et al. 2024 (reference 12)** …`.

---

### A4-24 — The compliance document misquotes the Funding statement, the AI statement, the STROBE filename and the abstract length (MINOR)

**【Problem】** Four quoted/verified values in the compliance document do not match the manuscript.

**【Evidence】**

| Compliance doc | Claim | Manuscript actual |
|---|---|---|
| line 13 (row 3) | `Abstract … 180 words` | **218 words** including the four bold sub-heading labels (**214** excluding them); I counted the block at lines 14–21. |
| line 23 (row 11) | `"The author received no specific funding for this work."` | line 261: `The author received no financial support for this work.` |
| line 27 (row 15) | `"A large language model (LLM) was used to assist manuscript drafting and language polishing"` | line 173: `A generative AI language model (Claude, Anthropic) was used to assist manuscript drafting and language polishing.` |
| line 30 (row 18) | `` `reports/MVP_PLOSONE_STROBE_checklist.md` `` | The file on disk is `reports/MVP_STROBE_checklist.md`. The named path does not exist. |

**【Why it matters】** Each mismatch is small; together they show the compliance document was written
against an earlier draft and never re-verified. Its "Verdict: Content is PLOS ONE–ready" (line 5) is
therefore not evidence of anything, and the submission set should not rely on it.

**【Specific fix】** Re-derive all four values from `reports/MVP_PLOSONE_submission.md` and correct
lines 13, 23, 27, 30; correct the filename to `reports/MVP_STROBE_checklist.md`.

---

### A4-25 — Fig. 2 legend and Results/Methods disagree on which LODO numbers are reported and on how many folds are degenerate (MAJOR)

**【Problem】** The Fig. 2 legend reports raw (non-leakage) AUCs without labelling them as raw, and states
that **three** folds have degenerate DeLong intervals; Results and Methods both state **four**.

**【Evidence】**
- Fig. 2 legend, `reports/MVP_PLOSONE_submission.md:289`: `Cross-animal held-out datasets (three folds) reach AUC 1.000 for GSE278227 (CCI rat DRG, n = 28) and GSE212311 (CCI, n = 6), and 0.917 [0.729, 1.000] for GSE267799 (incision rat DRG, n = 20), the cross-animal LODO floor. … Three folds show degenerate DeLong intervals ([1.0, 1.0]) at small test n and are not interpreted as precision.`
- Results, `reports/MVP_PLOSONE_submission.md:64`: `A leakage-controlled re-estimation (feature selection recomputed out-of-fold; `P3_lodo_auc_ci_leakage_controlled.csv`) confirms the four nerve-injury folds at AUC 1.000 and the incision fold at 0.677 [0.374, 0.940]` … `Four of the five leakage-controlled folds have degenerate CIs [1.0,1.0] (the four AUC = 1.0 nerve-injury folds); only the incision fold yields an estimable CI`.
- Methods, `reports/MVP_PLOSONE_submission.md:158`: `Four of the five leakage-controlled folds yield degenerate DeLong intervals ([1.0, 1.0]) at small test n; only the incision fold yields an estimable CI`.

So the legend's 0.917 (incision) is the raw value, while 0.677 is the leakage-controlled value the text
declares authoritative; and the legend says three degenerate folds where the text says four.

**【Why it matters】** The figure is where most readers look first. A legend that prints the number the
text has explicitly deprecated (0.917) while the text reports 0.677, plus a 3-vs-4 count disagreement in
the same file, is exactly the kind of inconsistency that makes a reviewer distrust every other number.

**【Specific fix】** Replace the first two sentences of the Fig. 2 legend at
`reports/MVP_PLOSONE_submission.md:289` with:
`Two panels. (A) Leakage-controlled leave-one-dataset-out (LODO) cross-validation AUC with 95% confidence intervals for the dual-ML hub classifier (feature selection recomputed out-of-fold). The four nerve-injury folds reach AUC 1.000 (GSE278227 CCI rat DRG, n = 28; GSE212311 CCI, n = 6; and the two same-animal GSE241361 folds, mouse DRG n = 9 and spinal cord n = 9, plotted separately and excluded from the cross-animal mean), and the incision fold GSE267799 (n = 20) falls to 0.677 [0.374, 0.940]. Raw (non-leakage-controlled) LODO AUCs, reported for comparison only, were 1.000, 1.000, 1.000, 0.950 [0.709, 1.000] and 0.917 [0.729, 1.000] respectively. Four of the five leakage-controlled folds (all four AUC = 1.0 nerve-injury folds) have degenerate DeLong intervals ([1.0, 1.0]) at small test n and are not interpreted as precision.`

---

### A4-26 — Non-circular translation confidence interval is printed as 47.7% in the manuscript and 47.6% in the supplementary (MINOR)

**【Problem】** One digit of the headline CI differs between the two documents.

**【Evidence】**
- `reports/MVP_PLOSONE_submission.md:58`: `the agreement rate was 46.2% (2,266/4,899; 95% CI 44.9–47.7%)`
- `reports/MVP_PLOSONE_supplementary.md:220`: `| **Non-circular test: NI FDR < 0.05 and NI consistency ≥ 0.8** | 2,266/4,899 | **46.2%** | 44.9–47.6% | 0.14 | no |`
- Authoritative source `results/tables/_R4_nerveinjury_only_summary.json`, stratum
  `NI_FDR05_AND_NIcons>=0.8`: `"k": 2266, "n": 4899, "rate": 0.4625, "ci": [0.4486, 0.4765]` — i.e. the
  upper bound is 47.65%, which rounds to **47.7%** (half-up) and truncates to **47.6%**.

**【Why it matters】** The number is quoted in the Abstract, Results, Discussion, Conclusions and the cover
letter. Two different printings of the same CI in the same submission set is precisely what an auditor
looks for, and it forces a question about which one was computed.

**【Specific fix】** Change `reports/MVP_PLOSONE_supplementary.md:220` upper bound from `44.9–47.6%` to
`44.9–47.7%`, and state the rule once: add to the S6 footnote
(`reports/MVP_PLOSONE_supplementary.md:223`) the clause `All Wilson intervals are rounded half-up to one decimal place.`

---

### A4-27 — Supplementary Table S5b contains a duplicated Sigma1 row (MINOR)

**【Problem】** The set-level BH table prints the Sigma1 row twice, giving 20 rows for 19 gene sets.

**【Evidence】** `reports/MVP_PLOSONE_supplementary.md:190` and `:191` are byte-identical:
`| Sigma1 | 1 | — | **—** | — | — | no |`

**【Why it matters】** A duplicated row in a table that is the evidence for "BH correction across the 18
multi-member sets" invites the reader to wonder whether the correction was run over 18 or 19 sets.

**【Specific fix】** Delete `reports/MVP_PLOSONE_supplementary.md:191`.

---

### A4-28 — A cited result file does not exist in the working tree (MINOR)

**【Problem】** `_R4_translation_noncircular.csv` is cited twice as a source but is deleted.

**【Evidence】** `reports/MVP_PLOSONE_submission.md:58` refers to
`the exploratory `_R4_translation_noncircular.csv``; `reports/MVP_PLOSONE_supplementary.md:212` lists it
under "Sources". Working-tree check: `results/tables/_R4_translation_noncircular.csv` = **missing**
(23 of 24 claimed result files verified present; this one is absent, and
`results/tables/_R4_reference_map.json` is also deleted).

**【Why it matters】** Both citations describe the file as superseded, so the science is unaffected, but a
reviewer who tries to open the cited artefact and cannot will treat every other file citation as
unverified.

**【Specific fix】** Restore the file (it is present in the HEAD tree: `git checkout HEAD -- results/tables/_R4_translation_noncircular.csv results/tables/_R4_reference_map.json`), or delete both citations and replace the S6 "Sources" entry with `results/tables/_R4_nerveinjury_only_summary.json` only.

---

### A4-29 — The compliance document leaks internal round/venue tokens (MINOR)

**【Problem】** If the compliance document travels with the submission, it discloses the prior review
history and the previous venue.

**【Evidence】** `reports/MVP_PLOSONE_compliance_check.md:4` `**Checked:** 2026-09-26 (Round 9)`;
`:40` `no Scientific Reports–era cap phrase remains`; `:46` `### 3.1 Round-9 additions`;
`:61` and `:82` `scripts/build_sr_submission_pack.py` ("sr" = Scientific Reports);
`:75` `## 6. What was changed in this pass (Round 9, 2026-09-26)`;
`:52` `This substitution is disclosed to the author.`

**【Why it matters】** A document that narrates nine review rounds at another venue undermines the
"first submission to PLOS ONE" framing of the cover letter and hands the editor the prior-round context
you would rather they did not have (and which you are entitled to withhold only if it is not attached).

**【Specific fix】** Do not upload `MVP_PLOSONE_compliance_check.md`. If it must be retained, delete
lines 4, 46, 52, 75, 81, 82 and replace `build_sr_submission_pack.py` with the actual build script name.

---

### A4-30 — Duplicate and backup artefacts in `submission_pack/` (COSMETIC)

**【Problem】** Two identical cover letters and a `.bak` manuscript sit in the upload folder.

**【Evidence】** `submission_pack/Cover_Letter.docx` and `submission_pack/Cover_Letter_PLOSONE.docx`
are byte-size identical (39,804 bytes each, same mtime 22:20); `submission_pack/Manuscript.docx.bak`
(75,700 bytes, 21-09-23) is a stale backup.

**【Why it matters】** Uploading the wrong cover letter (the un-rebranded one) is a real, avoidable error.

**【Specific fix】** Delete `submission_pack/Cover_Letter.docx` and `submission_pack/Manuscript.docx.bak`
before upload; keep only `Cover_Letter_PLOSONE.docx`.

---

## §6. Disclosure ≠ resolution

For each limitation conceded in the body, I searched the **Abstract**, the **Conclusions** section and
the **cover letter** for an unqualified restatement.

### A4-31 — "Spatial mapping placed 17/33 hubs in the dorsal horn" (Abstract) vs "constitutive baseline anatomy" (body) — MAJOR

**【Problem】** The Abstract reports dorsal-horn localisation without the qualifier the body insists on,
so the abstract claim reads as injury-related localisation.

**【Evidence, side by side】**
- Abstract, `reports/MVP_PLOSONE_submission.md:18`: `Spatial mapping placed 17/33 hubs in the dorsal horn; the human blood miRNA layer was negative (p = 0.51).`
- Body, `reports/MVP_PLOSONE_submission.md:78`: `17 of 33 detectably expressed hubs (51.5%) were assigned to the dorsal horn on Sham/baseline tissue, no injury-arm spatial data were available. Because this is uninjured tissue, the dorsal-horn assignment is reported as constitutive baseline anatomy: it shows that these hubs are anatomically present at the pain-afferent first station, not that they are enriched or recruited there by injury.`

**【Why it matters】** The Abstract is the only part most readers and all indexing services see. The body
concedes the single most important scope limit of the spatial layer — there is no injury arm — and the
Abstract drops it. Reviewers routinely quote the abstract back at authors as evidence of over-claiming.

**【Specific fix】** Replace the Abstract clause with:
`Spatial mapping on uninjured (Sham) tissue placed 17 of 33 detectably expressed hubs in the dorsal horn — constitutive baseline anatomy, not injury-induced recruitment; the human blood miRNA layer was negative (p = 0.51).`
(Word count after edit: 228, still under 300.)

---

### A4-32 — "Conserved" in the title vs "the single most important fragility of the signature" in the body — MAJOR

**【Problem】** The title's first word asserts conservation; the body concedes that 75.1% of the core
disappears under random effects and 45.7% is not recovered without the translatome study.

**【Evidence, side by side】**
- Title, `reports/MVP_PLOSONE_submission.md:1`: `Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null`
- Body, `reports/MVP_PLOSONE_submission.md:46`: `Under random effects the core (FDR_RE < 0.05 and consistency ≥ 0.8) shrank to 1,008 genes, 24.9% of the fixed-effect core.`
- Body, `reports/MVP_PLOSONE_submission.md:50`: `45.7% of the primary core was not recovered without the translatome study, the single most important fragility of the signature, and one we therefore lead with rather than report as a secondary sensitivity.`
- Cover letter, `reports/MVP_PLOSONE_cover_letter.md:11`: `a DerSimonian–Laird random-effects sensitivity analysis shows the core signature shrinks from 4,055 to 1,008 genes (median I² = 38.8%)` — the cover letter discloses it; the title does not.

**【Why it matters】** The title is the strongest claim in the paper and is the one thing an editor judges
before reading. "Conserved" is not supported on the paper's own numbers for the majority of the core.

**【Specific fix】** Replace the title with:
`Heterogeneity-sensitive nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null`
(170 characters; still within PLOS ONE's limit.)

---

### A4-33 — "We integrated 12 GEO datasets by Stouffer meta-analysis" (Abstract) vs five studies/six contrasts (Methods) — MAJOR

**【Problem】** The Abstract's Methods sentence implies all 12 datasets entered the Stouffer meta-analysis;
only five studies (six contrasts) did.

**【Evidence, side by side】**
- Abstract, `reports/MVP_PLOSONE_submission.md:16`: `We integrated 12 GEO datasets by Stouffer meta-analysis, set-level BH-corrected gene-set tests, dual-ML hub identification under leakage-controlled leave-one-dataset-out, and a full-library (3,085-drug) docking screen with reverse positive controls.`
- Methods, `reports/MVP_PLOSONE_submission.md:144`: `For the DRG-axis meta-analysis, five independent studies are represented by six contrasts …`
- Methods, `reports/MVP_PLOSONE_submission.md:141`: `Twelve GEO datasets were decoded per-dataset for species, model, tissue and true grouping …` — the other seven datasets are scRNA/snRNA/Visium/human-plasma-miRNA/SH-SY5Y, which cannot be Stouffer-combined with bulk contrasts.

**【Why it matters】** An abstract that overstates the meta-analysis denominator by 2.4× is the first thing
a methodology reviewer catches; it also makes the Abstract internally inconsistent with its own
Background sentence, which says "12 public GEO datasets (four nerve-injury, one incision)" — 4 + 1 = 5,
not 12 (`reports/MVP_PLOSONE_submission.md:14`), leaving the reader to guess what the other seven did.

**【Specific fix】** Two edits:
`reports/MVP_PLOSONE_submission.md:14`: replace `We reanalysed 12 public GEO datasets (four nerve-injury, one incision),` with
`We reanalysed 12 public GEO datasets, five of which (four nerve-injury, one incision) entered the DRG-axis meta-analysis,`
`reports/MVP_PLOSONE_submission.md:16`: replace `We integrated 12 GEO datasets by Stouffer meta-analysis,` with
`We combined five studies (six contrasts) by Stouffer meta-analysis,`

---

### A4-34 — Cover letter claims prospective registration the manuscript does not document — MAJOR

**【Problem】** The cover letter says the analysis "was pre-specified and registered in the public
repository before reporting"; the manuscript documents prospective specification inside code but no
registration of any kind.

**【Evidence, side by side】**
- Cover letter, `reports/MVP_PLOSONE_cover_letter.md:11`: `The analysis was pre-specified and registered in the public repository before reporting: the repurposing screen was defined as a full-library breadth analysis with reverse positive controls before any enrichment was computed.`
- Manuscript, `reports/MVP_PLOSONE_submission.md:166` heading: `### Structure-based repurposing (prospectively specified)`; `:167`: `The ligand library was ChEMBL max_phase=4 … → 3,085 pdbqt files`. No registration identifier (no OSF, no PROSPERO, no clinical-trials number) appears anywhere in the manuscript, supplementary, or repository metadata (`CITATION.cff`, `.zenodo.json`).

**【Why it matters】** "Registered" is a term of art. Claiming registration without an identifier is an
unsupported claim in the one document the editor reads first, and it over-answers a question PLOS ONE is
not asking (PLOS ONE does not require registration for non-clinical studies). If challenged, the author
must retreat from a written statement.

**【Specific fix】** Replace the clause with:
`The analysis code was prospectively specified and version-controlled in the public repository before the results were written up: the repurposing screen was defined as a full-library breadth analysis with reverse positive controls before any enrichment was computed.`

---

### A4-35 — "no target clears both filters" (Conclusions/Abstract) vs "ADRA2A … inconclusive, not a confirmed null" (Results) — MINOR

**【Problem】** The headline "both filters" framing is technically correct but is silent about the fact
that ADRA2A *did* clear the second filter, which the Results concedes.

**【Evidence, side by side】**
- Abstract, `reports/MVP_PLOSONE_submission.md:18`: `Full-library docking of 3,085 drugs against the 10 tractable targets found none clearing both the full-library and size-independent enrichment filters (ADRA2A 0.618 → 0.532, p = 0.118)`
- Conclusions, `reports/MVP_PLOSONE_submission.md:134`: `a prospectively specified, full-library docking screen of the FDA-approved catalogue found no target that cleared both the full-library and size-independent enrichment filters (ADRA2A Tier-1 AUC 0.618 collapses to 0.532, p = 0.118; events-per-parameter ≤ 2 for all ChEMBL-annotated positive controls)`
- Results, `reports/MVP_PLOSONE_submission.md:112`: `after MW adjustment the AUC was 0.578 with a weak but significant ΔAUC (p ≈ 0.0005), so the ADRA2A docking result is inconclusive, not a confirmed null.`
- Table 3b, `reports/MVP_PLOSONE_submission.md:325`: `ADRA2A | 0.532 | No | 0.0005 | 0.118 | 0.0025 | 0.532 | NS (only size-indep. passes BH; full-library AUC NS → inconclusive)`

**【Why it matters】** A reader who checks Table 3b sees ADRA2A's size-independent BH q = 0.0025 (a pass)
and may conclude the Abstract's "none clearing both filters" is spin. Saying it explicitly costs one
clause and removes the objection.

**【Specific fix】** Append to the Abstract sentence:
`… found none clearing both the full-library and size-independent enrichment filters (ADRA2A 0.618 → 0.532, p = 0.118; ADRA2A cleared the size-independent filter alone, q = 0.0025, and is therefore inconclusive rather than null)`

---

### A4-36 — Abstract's dataset arithmetic: "12 public GEO datasets (four nerve-injury, one incision)" — MINOR

Covered inside A4-33 (same sentence, same fix). Listed separately because it is an internal
inconsistency in the Abstract itself even after A4-33's Methods fix is applied to line 16; the fix for
line 14 in A4-33 resolves it.

---

## § Stands up

Things I suspected, checked, and found **correct**.

1. **Abstract structure and length pass.** `reports/MVP_PLOSONE_submission.md:14-21` carries all four
   required sub-headings — `**Background.**`, `**Methods.**`, `**Results.**`, `**Conclusions.**` — in that
   order. I counted the block: **218 words** including the four bold labels, **214** excluding them,
   against PLOS ONE's 300-word limit. I also checked for citations inside the abstract
   (`(\d{4})`, `[\d+]`, `[^`)`: **zero** — PLOS ONE forbids references in the abstract. PASS.

2. **The reference list is clean on every dimension I tested.** 36 entries
   (`reports/MVP_PLOSONE_submission.md:183-256`, numbers 1–36, no gaps, no duplicates). I parsed the
   superscript citation stream in the pre-References text: all 36 numbers are cited, **none** is cited
   before its own number (zero first-citation-order violations), and **every** one of the 36 entries ends
   with a `https://doi.org/…` link — 36/36, no PMID-only stub. This independently confirms
   `MVP_PLOSONE_compliance_check.md:5` (`References: 36 / 36`) and `:18` on the counts, even though that
   document's *numbering* of individual refs is wrong (A4-23).

3. **Display-item arithmetic is correct.** `reports/MVP_PLOSONE_submission.md:281` declares
   "5 figures + 3 tables = 8 enumerated main display items". I enumerated the entries: `- **Fig. 1**`
   (285), `Fig. 2` (288), `Fig. 3` (291), `Fig. 4` (294), `Fig. 5` (297) = **5**; `- **Table 1**` (302),
   `Table 2` (315), `Table 3` (318) = **3**. 5 + 3 = 8 ✔. The stated count is not a bluff.

4. **Figure legends exist for all five figures and all are within the ≤350-word target the manuscript sets
   for itself.** Word counts: Fig. 1 = 172 (line 286), Fig. 2 = 155 (289), Fig. 3 = 107 (292),
   Fig. 4 = 152 (295), Fig. 5 = 154 (298). Each names the source result file.

5. **Title length and tone.** `reports/MVP_PLOSONE_submission.md:1` = **166 characters**, matching
   `MVP_PLOSONE_compliance_check.md:13`, well under PLOS ONE's limit, and it contains no "novel",
   "first", "superior" or other unsubstantiated superlative. (The *substance* of "Conserved" is a separate
   problem — A4-32 — but the formatting requirement is met.)

6. **The ethics statement correctly attributes IRB approval to the original deposition and does not imply
   a new approval.** `reports/MVP_PLOSONE_submission.md:176`: `the original deposition documents
   institutional review board (IRB) approval and informed consent; the approving IRB and its approval
   identifier are recorded in the GSE158825 data deposit … and are not independently reproduced here …
   this secondary reanalysis required no further ethics approval.` The same paragraph separately states
   that the nine animal datasets carry IACUC approval in their depositions and that no new animal data
   were generated. This is the correct and honest formulation for a secondary analysis; nothing in the
   manuscript, supplementary or cover letter claims a new approval.

7. **The GitHub URL is real, not fabricated.** The repository's configured remote is
   `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing.git` (both fetch and push), matching the URL
   in `reports/MVP_PLOSONE_submission.md:267`, `reports/MVP_PLOSONE_cover_letter.md:13`,
   `reports/MVP_PLOSONE_supplementary.md:7`, `CITATION.cff` and `README.md`. The claimed tag
   `v1.0.0` exists. (What is *in* that tag is a separate problem — A4-05.)

8. **The competing-interests disclosure of the pending grant is made twice and is specific.**
   `reports/MVP_PLOSONE_submission.md:261` (Funding) and `:274` (Competing Interests) both state that the
   Fujian Natural Science Foundation application lists ADRA2A among candidate targets, that it did not
   fund and did not influence the analyses, and `:90` repeats it at the point of use: `the author has a
   pending grant in which ADRA2A is listed among the candidate targets; this did not influence the present
   analyses`. An editor cannot accuse the author of burying it.

9. **Two numeric cross-checks between manuscript and supplementary agree.** (a) Supplementary
   `reports/MVP_PLOSONE_supplementary.md:251` states that only 4 of 10 targets retain RE FDR < 0.05 and
   names SLC2A1, TNIK, ADRA2A, GALNS; the manuscript's Panel A/B tables
   (`reports/MVP_PLOSONE_submission.md:96-110`) list exactly those four with FDR_RE < 0.05 (0.0000, 0.021,
   0.039, 0.025) and six above it. (b) Supplementary S1
   (`reports/MVP_PLOSONE_supplementary.md:15-49`) has exactly 5 rows with `n_methods = 3` and 30 with
   `n_methods = 2`, matching "5/35 reached full three-method consensus … the remaining 30 agreed by exactly
   two methods" (`reports/MVP_PLOSONE_submission.md:62`) — 35 rows total.

10. **The supplementary correctly flags the two below-floor spatial hubs sets and the manuscript agrees.**
    `reports/MVP_PLOSONE_supplementary.md:53` lists CDHR5, SERPINE1, CRISP3, LNP1, VIP, REG3B, ANKRD1 as
    below-floor; `reports/MVP_PLOSONE_submission.md:164` names the identical seven. Consistent.

---

## § Questions for the authors

1. **Which commit was GitHub release `v1.0.0` cut from?** The only tag in the repository points at
   `5cfa2fb`, four commits behind HEAD, and at that commit `results/tables/` contains **zero** `_R4_*`
   files. If the release was cut from a later commit, please give the SHA; if not, A4-05 stands and the
   manuscript's claim that v1.0.0 "already contains" `_R4_random_effects_meta.csv`,
   `_R4_nerveinjury_only_meta.csv` and `_R4_targetset_bootstrap.csv` is false.
2. **Where can a reviewer find `MANIFEST.sha256`?** The only copy is `_manifest/MANIFEST.sha256`, which is
   untracked (`git ls-files _manifest` is empty) and therefore absent from the repository.
3. **Has the Zenodo deposit actually been made?** I found no `10.5281/zenodo.<digits>` anywhere in the
   repository. If it has, what is the DOI? If not, when will it be made, and will the placeholder be
   removed from the manuscript before upload?
4. **Was any generative-AI tool used to write, debug or refactor the analysis scripts** (as opposed to
   prose)? The disclosure at line 173 covers "manuscript drafting and language polishing" only, but the
   repository contains AI-shaped helper scripts. Which model, which version, which dates?
5. **Does GSE158825 provide any participant-level covariates beyond group status and `%nprs20delta`**
   (age, sex, BMI, surgical level)? The STROBE checklist says none exist; the manuscript analyses
   `%nprs20delta`, which is one. If age/sex are available in the deposition, please tabulate them.
6. **Is there any registration record for the "pre-specified" screen** — an OSF DOI, a PROSPERO ID, a
   dated pre-analysis plan in the repository? The cover letter says "registered"; the manuscript shows
   only a prospectively specified code path.
7. **Which LODO numbers does Fig. 2 actually plot** — raw or leakage-controlled? The legend prints 0.917
   for the incision fold and 0.950 for the spinal-cord fold (raw), while the text declares the
   leakage-controlled 0.677 authoritative.
8. **Are the Panel A / Panel B tables in the Results meant to *be* Table 3a**, and where is Table 2's
   actual 35-row content? I cannot find either in the manuscript.
9. **What is the article type you will select in the submission system?** A pure in-silico re-analysis of
   public data can be triaged as a Research Article, but the editor needs the argument in one sentence;
   the cover letter's current argument (line 9) rests on novelty ("a novel integrative signature"), which
   is not PLOS ONE's criterion.
10. **Was the GSE158825 consent documented as written or oral** in the original deposition? The ethics
    statement says "informed consent" without the form.

---

## § What I actually checked

**Files read in full (not skimmed):**
- `reports/MVP_PLOSONE_submission.md` (332 lines) — read line by line, including every long line that
  required separate extraction (lines 44, 48, 52, 58, 64, 88, 112, 120, 128, 167, 267, 269, 274, 277,
  286, 289, 292, 295, 298, 303, 304, 313, 316, 319, 320, 330, 332).
- `reports/MVP_PLOSONE_supplementary.md` (303 lines, all of S1–S7 incl. S5b).
- `reports/MVP_STROBE_checklist.md` (34 lines, all 22 items).
- `reports/MVP_PLOSONE_cover_letter.md` (24 lines).
- `reports/MVP_PLOSONE_compliance_check.md` (82 lines).
- `submission_pack/Manuscript.docx`, `Cover_Letter_PLOSONE.docx`, `Supporting_Information.docx`,
  `STROBE_Checklist.docx` — text extracted from `word/document.xml` and searched for the strings
  `Scientific Reports`, `zenodo.XXXXXXX`, `10.5281`, `Table 2`, `Additional Information`, `Claude`,
  `large language model`.

**Repository facts verified (not assumed):**
- `git tag -l` → `v1.0.0` only; `git rev-list --count v1.0.0..HEAD` → 4; `git log -1 v1.0.0` → `5cfa2fb`.
- `git ls-tree v1.0.0 results/tables/ | grep -c '_R4_'` → **0**; same at HEAD → **13**.
- `git ls-files _manifest` → empty; `MANIFEST.sha256` exists only at `_manifest/MANIFEST.sha256`.
- Repository-wide regex scan for `10\.5281/zenodo\.[0-9]+` → **0 matches**.
- `git remote -v` → `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing.git` (matches the manuscript URL).
- Existence check on 24 result files named in the manuscript/supplementary → 22 present,
  `_R4_translation_noncircular.csv` and `_R4_reference_map.json` missing.
- `results/tables/_R4_nerveinjury_only_summary.json` read directly: stratum `NI_FDR05_AND_NIcons>=0.8`
  → `k=2266, n=4899, rate=0.4625, ci=[0.4486, 0.4765], perm_p=0.1396` (this is the source of the 46.2%
  figure and the 44.9–47.7 vs 47.6 CI discrepancy).

**Counts I verified myself:**
- Title: 166 characters.
- Abstract: 218 words with sub-heading labels / 214 without; 0 references inside.
- References: 36 entries; 36/36 cited; 0 first-citation-order violations; 36/36 end with a DOI.
- Display items: 5 `Fig.` entries + 3 `Table` entries = 8 (matches the stated count).
- Figure legends: 5 present; 172 / 155 / 107 / 152 / 154 words (all ≤ 350).
- Markdown table blocks in the manuscript: 4 (lines 95, 107, 307, 323) — two of them unlabelled.
- In-text citations of display items: `Fig. 1` ×2 (one in Results), `Fig. 2`–`Fig. 5` ×1 each
  (display-item list only), `Table 1` ×4 (one in Results), `Table 2` ×1 (display-item list only),
  `Table 3` ×2 (Competing Interests + display-item list).
- In-text citations of supplementary items: S2, S4, S5, S6 only; S1, S3, S7, S5b uncited.
- Keywords: 8, present after the Author Summary.

**Discrepancies I found (stated explicitly, all cross-referenced above):** A4-23 (reference numbers 34/35/36
in the compliance doc vs 23/11/12 in the manuscript); A4-24 (abstract 180 vs 214 words; two misquoted
sentences; one non-existent filename); A4-25 (Fig. 2 legend 0.917/three folds vs text 0.677/four folds);
A4-26 (CI 47.7% vs 47.6%); A4-14 (Tier-1 AUC 0.532 vs 0.618); A4-15 ("no per-participant covariates" vs
`%nprs20delta`); A4-13 (all STROBE line pointers misaligned); A4-05/A4-06 (repository claims vs
repository contents); A4-27 (duplicated Sigma1 row); A4-28 (two cited files missing).

**Not checked (out of scope or unverifiable from here):** whether the GitHub repository is publicly
visible and whether the `v1.0.0` release object on GitHub was cut from a different commit than the local
tag (question 1); whether the 36 DOIs resolve to the cited articles at Crossref (I verified presence and
format only); the statistical correctness of the meta-analysis, ML and docking pipelines (other
reviewers' remit).

---

## § Must-fix list (ordered by severity)

| # | Item | Severity | Desk-reject risk |
|---|---|---|---|
| A4-05 | Data Availability claims v1.0.0 contains the `_R4_*` outputs (it contains 0), that integrity is verifiable via `MANIFEST.sha256` (untracked, absent from repo), and that all figures are deposited | **Major** | **YES — highest risk in this submission** |
| A4-01 | Fig. 2–5, Table 2 and Table 3 are never cited in the narrative text (only Fig. 1 and Table 1b are) | **Major** | High (administrative return before triage) |
| A4-03 | Table 2, a declared main display item, contains no table — only prose plus a CSV path | **Major** | High (missing display item) |
| A4-02 | Panel A / Panel B tables in Results carry no table number or caption | **Major** | Moderate |
| A4-06 | Placeholder DOI `10.5281/zenodo.XXXXXXX` printed in the manuscript and present in `Manuscript.docx`; "upon acceptance it will receive a DOI" misdescribes Zenodo | **Major** | Moderate–high |
| A4-04 | Internal revision changelog ("This version adds…", "correction of three printed values") printed as a blockquote under the title | **Major** | Moderate |
| A4-13 | Every line pointer in the STROBE checklist is misaligned with the submitted manuscript | **Major** | Moderate |
| A4-14 | STROBE Item 16 reports "ADRA2A Tier-1 AUC 0.532" — the Tier-1 value is 0.618 | **Major** | Moderate |
| A4-15 | STROBE Item 14 asserts no per-participant covariates exist; the manuscript analyses `%nprs20delta` | **Major** | Moderate |
| A4-16 | STROBE Item 9 marked "Addressed" with no source-study risk-of-bias or publication-bias assessment | **Major** | Moderate |
| A4-19 | Cover letter's AI disclosure names no tool and omits verification/authorship statements present in the manuscript | **Major** | Moderate |
| A4-23 | Compliance document misnumbers three references (34/35/36 vs actual 23/11/12) | **Major** | Low (if not uploaded) |
| A4-25 | Fig. 2 legend prints raw LODO AUCs (0.917, 0.950) unlabelled and says three degenerate folds; text says four | **Major** | Low |
| A4-31 | Abstract omits "uninjured/Sham tissue" from the dorsal-horn claim the body explicitly qualifies | **Major** | Low |
| A4-32 | Title's "Conserved" vs body's 24.9% RE retention and 45.7% translatome dependence | **Major** | Low |
| A4-33 | Abstract says "12 GEO datasets by Stouffer meta-analysis"; only five studies/six contrasts were combined | **Major** | Low |
| A4-34 | Cover letter claims the analysis was "registered"; no registration record exists | **Major** | Low |
| A4-07 | S1, S3, S7 and S5b uncited; "S5b" is not a valid PLOS SI label | Minor | Low |
| A4-08 | Bare superscript citations instead of PLOS bracketed numbers | Minor | Low |
| A4-09 | "## Additional Information" — a *Scientific Reports* section heading | Minor | Low |
| A4-10 | Sentence fragment in the Discussion's OXPHOS statement | Minor | Low |
| A4-20 | AI disclosure silent on model version and on AI assistance with analysis code | Minor | Low |
| A4-22 | IRB name/identifier withheld without stating whether they were verified | Minor | Low |
| A4-24 | Compliance doc misquotes Funding, AI sentence, STROBE filename, abstract word count | Minor | Low |
| A4-26 | CI printed as 44.9–47.7% in the manuscript and 44.9–47.6% in the supplementary | Minor | Low |
| A4-27 | Duplicated Sigma1 row in Supplementary Table S5b | Minor | Low |
| A4-28 | Two cited result files deleted from the working tree | Minor | Low |
| A4-29 | Compliance doc leaks "Round 9" and "Scientific Reports" tokens | Minor | Low |
| A4-35 | "None clearing both filters" does not say ADRA2A cleared the second | Minor | Low |
| A4-11 | "To our knowledge … to our knowledge" duplicated in one sentence | Cosmetic | — |
| A4-12 | "Data are not 'available on request'." meta-sentence | Cosmetic | — |
| A4-30 | Duplicate `Cover_Letter.docx` and stale `Manuscript.docx.bak` in the upload folder | Cosmetic | — |

**Recommended action:** do not upload until A4-01 through A4-06 are fixed. A4-05 alone is sufficient
grounds for a PLOS ONE desk rejection on data-availability grounds, and A4-01/A4-03 alone are sufficient
grounds for an administrative return before editorial triage.
