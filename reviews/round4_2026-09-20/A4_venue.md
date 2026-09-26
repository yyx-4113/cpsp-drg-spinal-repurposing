# Reviewer A4 — Venue & Reporting-Standards Audit
**Manuscript:** `reports/MVP_ScientificReports_submission.md` (v1.3, 2026-09-20) + `MVP_ScientificReports_supplementary.md`
**Target venue:** *Scientific Reports* (Nature Portfolio), Article type, single author (Yang Y)
**My remit (venue / reporting-standards only):** title & abstract length, display-item count & legend length, reporting-checklist honesty, data-availability integrity, competing-interests consistency, "honest null" framing consistency, "first/among the first" defensibility, article-type suitability, AI-use disclosure, and format hard-fails (reference ordering, truncation, cover-letter vs manuscript mismatches, statistical-sidedness statement).

**Independence statement.** I read only the files permitted to this round: the manuscript, the supplementary file, `reports/MVP_ScientificReports_reporting_summary.md`, `reports/MVP_ScientificReports_cover_letter.md`, the `_PANEL_BRIEF.md`, and raw/processed data under `results/tables/`, `data/`, `docking/`, `scripts/`. I did **not** read any prior-review, response, or project-status file. Every number I cite as "verified" was recomputed by me from the source CSVs/JSONs listed in § "What I actually checked."

---

## Editorial verdict (headline)

The quantitative reporting that I could independently recompute is **honest and internally consistent** (concordance fractions, core size, hub counts, LODO values, and bulk-only sensitivity all reproduce exactly). However, the manuscript has **two format hard-fails that block acceptance as-submitted** (a literal `[truncated]` inside Methods, and references not numbered by first citation), **one self-contradiction** (an "honest null" in Abstract/Results that the Discussion converts into specific repurposing "priorities"), and **one competing-interests consistency gap** (ADRA2A is benchmarked and singled out despite a statement that it receives "no privileged treatment"). These are correctable but must be fixed before the manuscript can proceed to production.

---

## Venue compliance scorecard (Scientific Reports checklist → this review)

| Requirement | Status | Finding |
|---|---|---|
| Title ≤ 20 words | PASS | 19 words (recomputed) |
| Abstract ≤ 200 words, no refs | PASS | 195 words (recomputed) |
| Display items ≤ cap; legends ≤ 350 words | PASS | 8 items (5 figs + 3 tables); max legend 163 words |
| Tables editable (not "see file X") | PASS | Tables 1–3 rendered as markdown |
| Reporting Summary completed & consistent | PASS* | Consistent with manuscript stats; minor "CV" mislabel noted |
| Data availability w/ real repo + no "on request" | PARTIAL | Local files exist; GitHub URL unverifiable; internal `_R3_` names (F7) |
| Competing interests declared | PARTIAL | Disclosed, but behavior contradicts "no privilege" (F5) |
| AI-use disclosed in Methods | PASS | Adequate (see below) |
| References numbered by first citation | FAIL | F2 |
| No truncation / placeholder in text | FAIL | F1 |
| Honest, non-overstated claims | PARTIAL | Discussion overstates (F4, F5, F8) |
| "Novelty/impact" not required | N/A | Venue has no such bar; "first" claims are unnecessary (F3) |

*PASS = verified; PARTIAL = present but with a fix needed; FAIL = blocks acceptance.

---

## Findings (each with the four-part contract)

### F1 — Methods section ends mid-sentence with a literal `[truncated]` marker
- **【Problem】** The Methods "Structure-based repurposing" paragraph is cut off mid-sentence by a verbatim placeholder, leaving the docking BH-enrichment method description incomplete.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:122` — the paragraph closes with: *"…but its full-library AUC remains ... [truncated]."* This is the final sentence before the next sub-section ("Statistical discipline and AI-use disclosure"); the `scripts/build_sr_submission_pack.py` / `make_sr_figures.py` pipeline evidently injected an unfilled placeholder. A scan of the whole file found exactly **one** `[truncated]` occurrence.
- **【Why it matters】** A truncated Methods paragraph means the editor and reviewers cannot verify how the Benjamini–Hochberg correction across the five targets was actually computed, nor the final enrichment verdict. For a journal that requires "adherence to field standards" and a complete Methods, this is a desk-reject/major-revision trigger on its own. It also signals that the submission file was assembled by an automated packer without human proofreading of the output.
- **【Specific fix】** Replace the truncated tail with the finished sentence drawn from the supplementary Panel B logic, e.g.:
  > "Benjamini–Hochberg correction across the five targets was applied to both the raw full-library enrichment p-values and the size-independent (MW-adjusted) p-values (Supplementary Table S4): 4/5 raw p-values survive BH (AXL, MAPK14, TNIK, ACVR1) whereas only ADRA2A's weak size-independent p survives BH (q = 0.0025); ADRA2A's full-library AUC (0.532, p = 0.118) remains non-significant, so no target clears both filters and the honest-null conclusion is unchanged."

### F2 — References are not numbered in order of first citation (Nature/Scientific Reports format rule)
- **【Problem】** The reference list is numbered 1–22 sequentially, but citations in the text do not appear in that order, violating Scientific Reports' requirement that references be numbered by order of first appearance.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:20` cites `¹` (Macrae) then `⁵` (Sapio) before `²`,`³`,`⁴` appear at lines 22. My script's first-citation order is `[1, 5, 2, 3, 4, 9, 6, 7, 8, 20, 15, 10, 11, 13, 14, 19, 22, 12, 17, 18, 16]` whereas the list is numbered `[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22]`. Concretely, Sapio (assigned #5) is the **second** reference cited in the text and should be #2; Xu (assigned #2) is the **third** cited and should be #3.
- **【Why it matters】** Scientific Reports follows Nature house style: "References are numbered in the order they appear in the text." A mis-ordered list forces the reader to hunt for citations, fails technical compliance, and is a common reason for a formatting reject at the production gate. (All 22 entries are themselves present and cited — no orphan or missing reference — so this is a re-numbering fix, not a content gap.)
- **【Specific fix】** Renumber the reference list to match first-appearance order. The verified correct assignment is:
  1 Macrae, 2 Sapio, 3 Xu, 4 Qu, 5 Pokhilko, 6 Meng, 7 Dong, 8 Gan, 9 Pham, 10 Nie, 11 Tsuda, 12 Divito, 13 Haque, 14 Yousefpour, 15 Kong, 16 Taves, 17 Scholz, 18 Keren-Shaul, 19 Sun, 20 Luo, 21 McDonnell, 22 Coull. (Re-run the citation renumbering across the whole text via the submission pack, not by hand, to avoid introducing new mismatches.)

### F3 — "the first to …" absolute priority claim is inconsistent with the cover letter and unverifiable
- **【Problem】** The Introduction asserts an absolute "first" for two contributions, but the cover letter hedges the same items to "among the first," and an unqualified "first" is neither verifiable nor required by the venue.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:24`: *"…and the first to identify hubs by a dual-ML consensus under LODO leakage control and to report a prospectively specified full-library FDA repurposing screen that—despite reverse controls—yielded no robust enrichment…"* Contrast `reports/MVP_ScientificReports_cover_letter.md:13`, which states *"among the first CPSP-adjacent studies to (i) … (ii) identify candidate hub genes by dual-ML consensus under cross-dataset leakage control (LODO), and (iii) report a prospectively specified full-library FDA repurposing screen…"* — i.e., the cover letter uses "among the first" for all three, while the manuscript uses "the first" for (ii)/(iii). This is a cover-letter-vs-manuscript mismatch.
- **【Why it matters】** Scientific Reports has **no novelty or impact bar**, so an absolute "first" claim is both unnecessary and risky: it invites a "show me the literature search proving no predecessor" objection and undermines the otherwise careful, humility-signalling tone of the paper. The internal inconsistency between cover letter and manuscript also fails the editor's "consistency" check. Note also that the hub set is itself described as resampling-sensitive (0/35 stable; `:44`), which sits oddly with claiming to have "first identified" a definitive hub set.
- **【Specific fix】** Make the two documents agree and soften to a defensible phrasing; change `submission.md:24` to:
  > "…and, to our knowledge, among the first CPSP-adjacent studies to identify candidate hubs by a dual-ML consensus under LODO leakage control and to report a prospectively specified full-library FDA repurposing screen that—despite reverse controls—yielded no robust enrichment…"
  (Keep the "among the first" framing for the DRG–spinal axis meta-analysis, which is already hedged by citing refs 6 and 9.)

### F4 — "Honest null" in Abstract/Results is contradicted by Discussion "repurposing priorities"
- **【Problem】** The Discussion designates specific targets as repurposing "priorities," directly contradicting the honestly-null conclusion stated in the Abstract and Results.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:14` (Abstract): *"Honest full-library repurposing does not yet support a specific analgesic."* `:83` (Results): *"no target clears both filters… the honest null applies to the absence of a robust, size-independent candidate hit."* But `:91` (Discussion): *"The clinically relevant reframing therefore redirects repurposing toward neuroimmune/glial and metabolic hubs (e.g., MAPK14, AXL, TFE3) as priorities…"* Table 3b (`submission.md:222`–`223`) shows MAPK14 size-independent p = 0.579 (NS) and AXL size-independent p = 0.141 (NS) — i.e., both **failed** the size-independent filter. TFE3 was **never docked** (it is not among the 10 tractable targets; it is a hub gene). So none of the three "priorities" is supported by the docking evidence the paper itself reports.
- **【Why it matters】** This is the clearest headline-vs-caveat contradiction in the manuscript. It converts a methodologically honest null into a translational recommendation the data do not support, which is exactly the overstatement Scientific Reports' "honest reporting" mandate is meant to prevent. It also dilutes the paper's strongest selling point — its candid "honest null."
- **【Specific fix】** Either (a) delete the word "priorities" and reframe as hypothesis-generating, e.g.:
  > "The clinically relevant reframing therefore *suggests* that neuroimmune/glial and metabolic hubs (e.g., MAPK14, AXL, TFE3) are *candidate* directions for future, prospectively validated repurposing work — noting that none cleared the size-independent enrichment filter in the present screen."
  or (b) move any such directional suggestion into the explicit "Stretch / future work" sentence already present at `:97` and keep the Discussion null-consistent.

### F5 — ADRA2A is benchmarked and singled out, contradicting the "no privileged treatment" statement
- **【Problem】** Although the Competing Interests section asserts ADRA2A receives no privileged treatment, the manuscript uses ADRA2A as the retrieval gold-standard and singles it out for in-vivo testing.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:169` (Competing Interests): *"ADRA2A receives no privileged treatment, and no prior-ablation or promotional language singles it out."* Yet:
  - `:83`: the knowledge-informed composite ranking is benchmarked *"against the ADRA2A ChEMBL binder set"* (precision@10 = 0.700, lift ×18.69) — i.e., ADRA2A is the reference standard for the retrieval metric, a form of privileging.
  - `:95` (Discussion): *"ADRA2A (established α2A analgesic pharmacology and meta direction-consistency) remaining a biologically plausible, not-yet-docking-prioritised, hypothesis to be tested in vivo"* — singles ADRA2A out as the one target to test in vivo.
  - `:68`: the "weakest of the ten on meta-evidence" defense is immediately followed by Discussion re-privileging, so the defense and the behavior are inconsistent. (I verified from `_R3_plausibility.json` that ADRA2A has the lowest meta_Z, 4.84, of the ten — so "weakest on meta-evidence" is literally true, which makes the later singling-out more, not less, conspicuous.)
- **【Why it matters】** The pending Fujian Natural Science Foundation grant lists ADRA2A (disclosed at `:168`–`169`, `cover_letter.md:17`, `reporting_summary.md:50`–`52`). Even though the disclosure itself is adequate, the manuscript's *behavior* undercuts the "no privileged treatment" assertion and creates the appearance the competing-interests statement is trying to preclude. This is precisely the kind of subtle inconsistency a venue/reporting reviewer must surface.
- **【Specific fix】** Make the text match the declaration. Two minimal changes:
  1. At `:83`, state the benchmark choice neutrally: *"The composite ranking was benchmarked against the ADRA2A ChEMBL binder set as a representative established analgesic target; these are knowledge-informed retrieval metrics, not independent docking evidence…"*
  2. At `:95`, remove the singling-out: replace *"with ADRA2A … remaining a biologically plausible … hypothesis to be tested in vivo"* with *"with the established α2A analgesic target ADRA2A remaining, like the other nine, a biologically plausible but docking-unprioritised hypothesis for future in-vivo testing."*

### F6 — Internal round-specific shorthand retained, contradicting the manuscript's own "removed internal revision shorthand" claim
- **【Problem】** The manuscript still carries round-specific revision shorthand ("Round-3 independent-panel revision", version string `v1.3`) even though its own version note claims this shorthand was removed.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:8`: *"…v1.3, 2026-09-20; Round-3 independent-panel revision). This revision … removes internal revision shorthand…"* — the note asserts removal while simultaneously containing the shorthand it claims to have removed (self-contradiction). The same string recurs at `MVP_ScientificReports_supplementary.md:7` (*"v1.3, 2026-09-20; Round-3 independent-panel revision"*). A scan found 1 "Round-3 independent-panel" hit and the version token `v1.3` in the manuscript.
- **【Why it matters】** Internal round labels in a file submitted to a journal look unprofessional and suggest the "final" manuscript was not actually finalized by the author; it also undermines confidence that other internal artifacts (see F7) were cleaned.
- **【Specific fix】** Delete "Round-3 independent-panel revision" from both `submission.md:8` and `supplementary.md:7`; replace the version token with a static descriptor such as *"Scientific Reports submission-ready manuscript (2026-09-20)"*. Remove the ", v1.3" token.

### F7 — Data-availability statement cites internal `_R3_` filenames; public GitHub deposit unverifiable by this review
- **【Problem】** The Data Availability statement points to a GitHub URL I cannot verify and embeds round-specific internal filenames (`_R3_bulkonly_meta_summary.json`, `_R3_plausibility.json`) that should not appear in a public deposit.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:166` (Data availability): *"…the bulk-only sensitivity outputs `_R3_bulkonly_meta_summary.json` and `_R3_plausibility.json`)."* The same `_R3_` names appear at `:208` (Table 1b source). My local check confirms these two files **do** exist in `results/tables/` (verified by reading both JSONs), and every other processed file cited in the Display Items (e.g., `META_DRG_axis_stouffer.csv`, `P3_geneset_stats.csv`, `P3_lodo_auc_ci.csv`, `P3_hub_genes.csv`, `P5_GSE216039_DRG_hub_finetype_top.csv`, `P5_hub_lineage_consensus.csv`, `P5_GSE325938_hub_regionalization.csv`, `P4_hub_miRNA_human_integration.csv`, `P3_hub_bootstrap.csv`, `P6_reverse_control.csv`, `P6_enrichment_mw_confounder_check.csv`, `P6_BH_correction.csv`, `P6_breadth_chembl_power.csv`) exists locally, as do `figures/Fig1–Fig5_*.png`. So the *local* data underpinning is present and the "not available on request" stance is internally consistent with a real deposit. **However**, I cannot open `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` to confirm the repo actually contains these files; that is an editor-side verification step.
- **【Why it matters】** Scientific Reports requires a working, populated Data Availability statement. The `_R3_` prefixes are round-3 artifact names that should be renamed to neutral names (e.g., `bulkonly_meta_summary.json`, `plausibility.json`) before any public deposit, because a reader cloning the repo should not see internal round labels. The unverifiable URL is not a defect per se, but the editor must confirm the repo is populated and that the cited filenames match.
- **【Specific fix】** (1) Rename the two JSONs in both the repo and the manuscript to drop `_R3_`; update `submission.md:166` and `:208` accordingly. (2) Editor action: open the GitHub URL and confirm `results/tables/`, `docking/out/`, `figures/`, and `data/processed/` are present and that the cited CSV/JSON/PNG names match exactly before acceptance.

### F8 — Article type is acceptable, but translational language overreaches the honest-null framing
- **【Problem】** "Article" is the correct Scientific Reports type for this computational reanalysis, but several translational phrasings imply causal/therapeutic certainty the data do not support.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:91` ("redirects repurposing toward … as priorities" — see F4) and `:95` ("ADRA2A … hypothesis to be tested in vivo" — see F5). Elsewhere the framing is appropriately hedged (`:24` "hypothesis-generating rather than causal"; `:97` "no single drug is advocated"). The inconsistency is between the hedged stance and the two overstated clauses.
- **【Why it matters】** Scientific Reports does **not** require a "Computational Study" reclassification here — Article is fine for a rigorous reanalysis. But an Article implies a contribution with boundaries, and the overstated translational clauses risk misleading readers into thinking specific targets are validated repurposing leads. This is a tone/compliance issue, not a type error.
- **【Specific fix】** Keep "Article." Apply the F4/F5 wording fixes so every translational statement is explicitly hypothesis-generating and null-consistent; no target should be described as a "priority" or singled out for in-vivo testing without the size-independent evidence the paper itself says is absent.

### F9 (minor) — Title/Abstract/legend limits are met, but the Abstract is near the ceiling and the cover-letter "first" softener must propagate
- **【Problem】** All length limits are satisfied, but the Abstract sits at 195/200 words (little headroom) and the cover letter's "among the first" softening (F3) must be mirrored in the manuscript.
- **【Evidence】** Recomputed counts (see § "What I actually checked"): Title = 19 words (≤20 ✓); Abstract = 195 words (≤200 ✓); Fig 1 legend = 135, Fig 2 = 163, Fig 3 = 87, Fig 4 = 138, Fig 5 = 162 words (all ≤350 ✓). Display items = 5 figures + 3 tables = 8 (within the generous Scientific Reports cap ✓); Tables 1–3 are rendered as editable markdown entities, not "see file X" placeholders ✓.
- **【Why it matters】** No limit is breached, so this is not a blocker; I flag it only so the author does not later add text that pushes the Abstract over 200 words during revision, and so the F3 cover/manuscript wording is kept consistent.
- **【Specific fix】** No change required now; keep the Abstract ≤200 words through any revision and align the "first/among the first" wording across manuscript and cover letter per F3.

### F10 — GSE267799 "harvest-day" caveat is honestly scoped, but the "CPSP-closest" framing near it is not fully reconciled
- **【Problem】** The incision-model harvest-day caveat is disclosed, but the manuscript continues to call the incision model the "CPSP-closest" model in the same breath, without flagging that this adjacency is source-asserted, not verified here.
- **【Evidence】** `reports/MVP_ScientificReports_submission.md:107` (Methods) discloses: *"the exact chronic harvest day is not stated in the deposited metadata and could not be verified … so the incision model's CPSP-adjacency is asserted by the source, not independently verified here."* This is honest. However, `:32` and `:91` repeatedly call incision "the (CPSP-closest) model" without repeating that the CPSP-adjacency itself is unverified. The 53.9% translation figure is therefore computed against a model whose CPSP-relevance is borrowed from the source GEO annotation.
- **【Why it matters】** The caveat is present and adequate for MIAME/transparency purposes (good — this is a "stands up" on scoping), but the recurring "CPSP-closest" label could be read as the authors' own endorsement of the adjacency. A one-line reinforcement at first use would close the loop.
- **【Specific fix】** At the first appearance of "CPSP-closest" (`:32`), append: *"(CPSP-adjacency per the source GEO annotation; the chronic harvest day was not verifiable from the deposited metadata — see Methods)."* This keeps the honest caveat attached to the claim it qualifies.

### F11 — Single-cell / spatial MIAME-style disclosure is honestly handled (positive; noted for balance)
- **【Problem】** None — this is a compliance strength, logged so the editor knows it was checked.
- **【Evidence】** `submission.md:118`–`119`: single-cell analysis uses sample-level pseudobulk only (n = 2–3/group), explicitly to avoid pseudoreplication; all single-cell calls are labelled "directional hints"; `:56` states Visium mapping is on Sham/baseline tissue with "no injury-arm spatial data were available"; `:54` notes ambient-RNA downgrades for ATF3/AXL; `:119` applies a 5% detection floor and excludes below-floor hubs from biological interpretation. These are exactly the MIAME/ARRIVE-aligned negatives the Reporting Summary promises (`reporting_summary.md:35`–`43`).
- **【Why it matters】** This is the kind of reporting honesty Scientific Reports rewards; it is logged here to confirm the scoping of the GSE267799 caveat (F10) and the single-cell limitations is adequate and not a blocker.
- **【Specific fix】** No change required.

### F12 — Figure DPI / format claim cannot be verified by text review (editor action)
- **【Problem】** The manuscript claims all figures are supplied as PNG at ≥300 DPI, but DPI is a file property not visible in the markdown.
- **【Evidence】** `submission.md:178`: *"all supplied as PNG at ≥300 DPI; legends ≤350 words each."* The five PNGs exist in `figures/` (`Fig1_geneset_programme.png`, `Fig2_hub_convergence.png`, `Fig3_DRG_neuron_subtype_localisation.png`, `Fig4_spinal_lineage_visium.png`, `Fig5_docking_honest_null.png`), and legend word counts are all ≤350 (verified). DPI itself is not checkable from text.
- **【Why it matters】** DPI compliance is a production-gate requirement; the editor/production must confirm the actual PNG resolution during file check, not just trust the claim.
- **【Specific fix】** Editor action: verify each PNG's effective DPI (pixel dimensions ÷ intended print size) meets ≥300 DPI before acceptance. If any figure is below threshold, request vector (SVG/PDF) or high-res replacement.

### F13 — Cover-letter vs manuscript title/claim match (PASS; closes item 10)
- **【Problem】** None blocking; logged to confirm the cover letter and manuscript are mutually consistent on title and headline claim.
- **【Evidence】** `reports/MVP_ScientificReports_cover_letter.md:3` title = *"Conserved maladaptive nerve-injury response on the dorsal root ganglion–spinal axis, with incomplete incision translation and an honest repurposing null"* — character-identical to `submission.md:1`. No title mismatch. The cover letter's "Novelty and significance" paragraph (`:13`) correctly softens all three contributions to "among the first," which is the version that should propagate into the manuscript per F3. The cover letter's compliance checklist (`:25`) also restates the same limits I verified (Title ≤20, Abstract ≤200, display items ≤8, refs Nature style ≤60 — note: the manuscript has 22 refs, well under 60).
- **【Why it matters】** A cover-letter/manuscript title mismatch is a classic desk-reject trigger; here there is none, which is good. The only residual cover-vs-manuscript inconsistency is the "first/among the first" wording (F3), already captured.
- **【Specific fix】** No change to the cover letter; apply F3 to the manuscript so the two documents use identical wording.

### F14 — Statistical discipline statement (one-sided AUC p / two-sided permutation p) is internally consistent (PASS; closes item 11)
- **【Problem】** None blocking; logged to confirm the sidedness statement is applied consistently across manuscript, Reporting Summary, and Methods.
- **【Evidence】** `submission.md:125`: *"AUC-based enrichment p-values are one-sided; permutation-calibration p-values are two-sided, as stated in the Reporting Summary."* `reporting_summary.md:11`: *"…one-sample t and 2,000/5,000 same-size permutation tests (two-sided); … AUC with one-sided enrichment p."* The ADRA2A full-library AUC p = 0.118 (NS) is reported as a one-sided enrichment p throughout (`:83`, `:95`, Table 3b), consistent with the declared sidedness. No passage reports a permutation p as one-sided or an AUC p as two-sided.
- **【Why it matters】** Sidedness errors are a frequent reporting-checklist failure; here the declaration matches the usage, so there is no conflict to raise. This is logged as cleared.
- **【Specific fix】** No change required.

---

## Pre-decision editor checklist (must-fix vs should-fix)

**MUST FIX before acceptance (hard-fails / contradictions):**
1. F1 — remove the literal `[truncated]` and complete the Methods BH-enrichment sentence.
2. F2 — renumber references by first-appearance order (script-verified mismatch).
3. F4 — reconcile Discussion "repurposing priorities" with the honestly-null conclusion (delete/reframe "priorities").
4. F5 — align ADRA2A treatment with the "no privileged treatment" statement (neutralize benchmark wording + in-vivo singling-out).

**SHOULD FIX (consistency / hygiene):**
5. F3 — propagate "among the first" into the manuscript; drop absolute "first."
6. F6 — delete "Round-3 independent-panel revision" / version token from manuscript and supplementary.
7. F7 — rename internal `_R3_*.json` to neutral names in repo + manuscript; editor verifies the GitHub repo is populated.
8. F8 — keep Article type; temper translational language to match null.
9. F10 — re-tie "CPSP-closest" label to its own harvest-day caveat at first use.
10. F12 — editor verifies all five PNGs meet ≥300 DPI at print width.

**VERIFIED CLEAN (no action):**
- Title 19 words, Abstract 195 words, all figure legends ≤350 words, 8 display items, editable tables (F9).
- All recomputed numbers (concordance, core, hubs, LODO, bulk-only, plausibility) reproduce exactly.
- Reporting Summary statistically consistent with manuscript; AI-use disclosure adequate; single-cell MIAME-style disclosures honest (F11, F14).
- All cited processed-data files exist locally; supplementary S1–S5 present and populated.

---

## § Stands up (verified correct — delivery, not filler)

1. **Translation concordance numbers reproduce exactly.** From `results/tables/META_DRG_axis_stouffer.csv` I recomputed shared = 14,390 genes with a numeric `incision_lfc`, of which 7,751 are directionally concordant → **53.9%** (manuscript `:32` "7,751/14,390"). Restricting to the core (meta_FDR < 0.05 & consistency ≥ 0.8) gives 3,556 shared, 2,473 concordant → **69.5%** (manuscript "2,473/3,556"). Both match to the decimal.
2. **Core signature and hub-set counts reproduce exactly.** `META_DRG_axis_CORE_signature.csv` = **4,055** rows (manuscript "4,055-gene core" ✓). `P3_hub_genes.csv` = **35** hubs, **5** with `n_methods == 3` (SPRR1A, ATF3, TFE3, CDHR5, GALNS — matches manuscript `:42`), and **32/35** with `in_meta_core == True` (matches "32/35 (91%)" ✓).
3. **Bulk-only sensitivity analysis reproduces exactly.** From `results/tables/_R3_bulkonly_meta_summary.json`: `bulk_only_core_size` = **1,981**, `primary_core_size` = **4,055**, `overlap` = **1,732**, `overlap_pct_primary` = **42.71%** (manuscript `:36` "1,981", "1,732/4,055 = 42.7%" ✓). SCN-tab and set-call values (e.g., Nav_SCN bulk perm_p = 0.268) also match the manuscript's reported bulk-only set statistics.
4. **LODO values reproduce exactly.** `P3_lodo_auc_ci.csv` gives GSE278227 AUC 1.000 (n=28), GSE267799 0.917 [0.729, 1.000] (n=20), GSE241361 DRG 1.000 (n=9), GSE241361 SC 0.950 [0.709, 1.000] (n=9), GSE212311 1.000 (n=6) — exactly as reported at `submission.md:44`. The cross-animal floor (0.917) and same-animal caveat are honest.
5. **10-target plausibility table reproduces exactly.** From `results/tables/_R3_plausibility.json`, every target's `meta_Z / meta_FDR / consistency / n_pdb_holo / decision` matches Table 3a (`:70`–`81`): e.g., ADRA2A meta_Z 4.84 / FDR 1.5e-5 / consistency 1.0 / n_holo 14; TNIK 8.00 / 4.3e-13 / 1.0 / 10; etc. The "ADRA2A weakest on meta-evidence" claim (`:68`) is literally true (lowest meta_Z of the ten).
6. **Display-item inventory and legend lengths comply.** 5 figures + 3 tables = 8 (manuscript `:176` claim verified); all five PNGs exist in `figures/`; all legends ≤350 words (max 163). Tables 1–3 are editable markdown, not external pointers — satisfies the "editable tables" requirement.
7. **Title (19 words) and Abstract (195 words) are within Scientific Reports limits** (recomputed, not trusted).
8. **Reporting Summary is statistically consistent with the manuscript.** One-sided AUC enrichment p vs two-sided permutation p (`:125` ↔ `reporting_summary.md:11`); sample sizes (GSE267799 12/8, GSE278227 14/14, GSE241361 4/5 DRG, GSE158825 n=60) match `reporting_summary.md:9` ↔ `submission.md:107`; permutation calibration 2,000 (gene-set) / 5,000 (miRNA) matches `reporting_summary.md:11` ↔ `:110,116`; CIs for LODO AUC reported as claimed. No numerical conflict found between the two documents. (Minor note: `reporting_summary.md:14` writes "mean ± SD (CV 0.999 ± 0.004)" — "CV" is a slight mislabel for the repeated-CV AUC; harmless but could be reworded to "repeated-CV AUC 0.999 ± 0.004".)
9. **AI-use disclosure is adequate and placed correctly.** `submission.md:124`–`125` (Methods): LLM assisted drafting/language polishing; author conceived/verified all science; no LLM meets authorship criteria. Mirrored in `cover_letter.md:15` and `reporting_summary.md:54`–`55`. No figure appears AI-generated; all five figures derive from data scripts. This satisfies Nature's AI policy.
10. **Every processed data file cited in the Display Items exists locally**, which supports (but does not prove) the Data Availability claim; the "not available on request" stance is internally consistent with a real deposit.
11. **Supplementary Tables S1–S5 are present and populated** in `MVP_ScientificReports_supplementary.md`: S1 (35-row lineage consensus), S2 (35-row Visium regionalisation with 7 below-floor flags), S3 (10-target reverse-control AUCs), S4 (multivariate physicochemical control + BH correction, Panels A/B), S5 (19 a priori gene-set members and provenance). All five are referenced from the main text and are not counted toward the 8-item cap (correct).

---

## § Questions for the authors

1. **GitHub verification:** Can you confirm the public repo `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` currently contains the exact CSV/JSON/PNG files cited (including the renamed `bulkonly_meta_summary.json` / `plausibility.json`)? The reviewer could not open the URL.
2. **Truncation origin:** The Methods `[truncated]` at `:122` — what is the intended closing sentence, and was the submission pack generated without a final human read of the rendered Methods?
3. **ADRA2A benchmark rationale:** Why was the composite ranking benchmarked specifically against the ADRA2A ChEMBL binder set rather than a target-agnostic or all-targets benchmark, given the pending grant lists ADRA2A? (This is to document that the choice was methodological, not preferential.)
4. **"Priorities" evidence:** For the Discussion's MAPK14/AXL/TFE3 "priorities" — do you intend these as casual hypotheses (in which case the wording should change per F4) or as claims carrying the size-independent enrichment evidence (which the paper says is absent)?
5. **Reference renumbering:** Will you regenerate the reference list by first-appearance order (F2) via the packer rather than hand-editing, to avoid introducing new citation mismatches?
6. **Figure DPI:** Can you confirm each of the five PNGs meets ≥300 DPI at its intended print width? (Production-gate check, F12.)

---

## § What I actually checked

**Files read (permitted only):**
- `reports/MVP_ScientificReports_submission.md` (full, 228 lines) — primary manuscript.
- `reports/MVP_ScientificReports_supplementary.md` (full, 163 lines) — S1–S5.
- `reports/MVP_ScientificReports_reporting_summary.md` (full, 56 lines).
- `reports/MVP_ScientificReports_cover_letter.md` (full, 26 lines).
- `reviews/round4_2026-09-20/_PANEL_BRIEF.md` (full).
- `results/tables/*.csv` and `*.json` (selected for recomputation).
- `figures/` directory listing; `docking/out/` listing; `data/processed/` listing.

**Commands run / values recomputed (Python 3.13 managed venv):**
- `META_DRG_axis_stouffer.csv`: columns inspected; rows with numeric `incision_lfc` = 14,390; directional concordance = 7,751 → **53.9%** (matches `:32`). Core subset (meta_FDR<0.05 & consistency≥0.8): 3,556 shared, 2,473 concordant → **69.5%** (matches `:32`). **No discrepancy.**
- `META_DRG_axis_CORE_signature.csv`: row count = **4,055** (matches `:32`, Table 1a). **No discrepancy.**
- `P3_hub_genes.csv`: 35 rows; `n_methods==3` → 5 (SPRR1A, ATF3, TFE3, CDHR5, GALNS); `in_meta_core==True` → 32. Matches `:42`, Table 2. **No discrepancy.**
- `P3_lodo_auc_ci.csv`: 5 folds; values match `:44` exactly. **No discrepancy.**
- `_R3_bulkonly_meta_summary.json`: `bulk_only_core_size`=1,981, `primary_core_size`=4,055, `overlap`=1,732, `overlap_pct_primary`=42.71%. Matches `:36`. **No discrepancy.**
- `_R3_plausibility.json`: 10 targets; `meta_Z/meta_FDR/consistency/n_pdb_holo/decision` match Table 3a (`:70`–`81`). **No discrepancy.**
- Title/Abstract/legend word counts via regex tokenizer: Title 19; Abstract 195; Fig1 135, Fig2 163, Fig3 87, Fig4 138, Fig5 162. All within limits. **No discrepancy.**
- Reference first-citation order via superscript-position scan: `[1,5,2,3,4,9,6,7,8,20,15,10,11,13,14,19,22,12,17,18,16]` vs list numbering `[1..22]`. **Mismatch confirmed (F2).**
- Placeholder scan of `submission.md`: found 1 `[truncated]` (`:122`), 3 `_R3_` tokens (`:166`×2, `:208`×1), 1 `Round-3 independent-panel` (`:8`), version token `v1.3` (`:8`). The `v1.7`/"v6.0" hits were false positives ("Nav1.7", "miRDB v6.0").

**Discrepancies / conflicts identified:**
- `[truncated]` literal in Methods → F1.
- Reference numbering not by first citation → F2.
- "the first to…" (manuscript `:24`) vs "among the first" (cover letter `:13`) → F3.
- Discussion "priorities" (`:91`) contradicts honest null (`:14`,`:83`) → F4.
- ADRA2A benchmark + in-vivo singling-out (`:83`,`:95`) contradicts "no privileged treatment" (`:169`) → F5.
- Retained "Round-3 independent-panel revision" (`:8`, supplementary `:7`) despite claim to have removed it → F6.
- Internal `_R3_` filenames in Data Availability (`:166`,`:208`) → F7.
- Article-type acceptable; translational overstatement (`:91`,`:95`) → F8.
- "CPSP-closest" label not re-tied to its own harvest-day caveat → F10.
- Figure DPI claim not text-verifiable → F12 (editor action).

**Discrepancies NOT found (explicitly cleared):**
- All cited processed-data filenames exist locally (no missing file).
- Reporting Summary vs manuscript statistics (sidedness, sample sizes, permutation resolution, CIs) — no conflict.
- AI-use disclosure — present and adequate in all three required locations.
- Display-item count (8) and editable-table rendering — compliant.
- Core/hub/LODO/concordance/bulk-only/plausibility numbers — all reproduce exactly.
- Supplementary Tables S1–S5 — present and populated.

**Files I did NOT read (independence discipline):** any `REVIEW_*.md`, `RESPONSE_*.md`, `REVISION_*.md`, the `reviews/round2_*` and `REVIEW_PANEL*` directories, `PROJECT_PLAN.md`, `README.md`, `CITATION.cff`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `submission_pack/`, `.workbuddy/`, and any `*_R3_*.json` interpretation notes. No prior-round context informed this review.
