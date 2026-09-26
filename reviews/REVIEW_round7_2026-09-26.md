# Round 7 — Consolidated Independent Review (CPSP / DRG–spinal-axis meta + repurposing)

**Date:** 2026-09-26
**Manuscript:** `reports/MVP_ScientificReports_submission.md` (PLOS ONE target; single author, B.M. only)
**Panel:** 4 independent experts — A1 Domain, A2 Design/Statistics, A3 Implementation/Provenance, A4 Venue/Reporting
**Method:** Fresh panel, enforced independence (no access to REVIEW_round*.md, RESPONSE*, _v14/_v15 source, compliance check, other reviewers). Each expert recomputed the manuscript's numbers from raw `results/tables/*` sources.
**Editor verification:** The single most severe finding (A2-F2, ML leakage-controlled AUC) was independently re-checked by the editor from raw CSVs before consolidation.

---

## 1. Independence statement

Four experts reviewed the manuscript as a *first submission*, forbidden from reading any prior-round review, the stale render source, the prior compliance check, or each other's outputs. 

**Evidence independence worked:**
- The four converged on the **same thematic defect from different angles** — the gap between the manuscript's headline ("conserved", "real not overfit signal", CPSP framing) and the fragility its own data shows (core 4,055→1,008 under RE; 45.7% core translatome-dependent; leakage-controlled incision AUC 0.677 with CI including 0.5). A1-F3 (CPSP front-loading), A2-F2 (ML leakage AUC), A4-F19 (title "Conserved" overstates fragility) all hit this independently.
- Each expert found *distinct* defects in their lane: A1 the sodium-channel citation-category errors; A2 the leakage-controlled AUC and the I² mislabel; A3 the missing ref-31 DOI and orphan GSE249746 file; A4 the unstructured abstract and STROBE title/version mismatch. No finding is unique-only-to-one in a way that signals diffusion; the cluster is on the headline-vs-fragility tension plus lane-specific format issues.

---

## 2. Verdict table

| Expert | Primary lane | Headline verdict | Notable |
|---|---|---|---|
| A1 Domain | Clinical/neuro/pain biology | REVISE — science honest but several citation-accuracy and framing issues | Sodium-channel defence misuses 2 of 3 citations; "DAM-microglia" over-specific for bulk DRG; CPSP over-front-loaded vs ~83% nerve-injury data |
| A2 Design | Meta-analysis statistics | REVISE — 2 design-layer defects the gates cannot catch | ML headline uses non-leakage-controlled AUC (0.917) while own table shows 0.677 (CI⊃0.5); I²=38.8% mislabelled "substantial" |
| A3 Implementation | Provenance/recompute | REVISE (minor) — all 18 headline numbers reproduce; 2 format/provenance defects | Ref 31 (Xiao 2002) missing its DOI; orphan `GSE249746` table file |
| A4 Venue | PLOS ONE + STROBE | REVISE — no desk-reject; fixable format/consistency | Structured abstract required; STROBE title/version mismatch; Zenodo DOI placeholder |

**Distribution:** 0 desk-reject; 4 × REVISE. No expert found a conclusion-invalidating error in the core meta-analysis (all headline numbers reproduced exactly — see §3).

---

## 3. Cross-verification table (manuscript claim → independently recomputed → verdict)

| # | Manuscript location | Manuscript claims | Independently recomputed (expert) | Who | Verdict |
|---|---|---|---|---|---|
| 1 | Results/Methods | 16,552 genes tested; 6,869 meta_FDR<0.05; core 4,055 | 16,552 / 6,869 / 4,055 from `META_DRG_axis_stouffer.csv` | A3, A2 | ✅ exact |
| 2 | Abstract/Methods | Random-effects core 1,008 (24.9%); median τ²=0.232, I²=38.8% | 1,008; τ²=0.2324, I²=38.79% | A2, A3 | ✅ exact |
| 3 | Methods/Table 1b | Bulk-only core 2,512; overlap 2,202/4,055=54.3% | 2,512; 2,202/4,055=54.3% from `META_bulkonly_meta.csv` + JSON | A2, A3 | ✅ exact (reconciled from 1,981 this round) |
| 4 | Results | Gene-set q=0.003 (neuroinflammation/DAM/complement); OXPHOS q=0.31 | q≈0.00299 each; OXPHOS RE q=0.31034 from `P3_geneset_stats.csv` | A1, A2 | ✅ exact |
| 5 | Results | 35 hubs; 17/33 in dorsal horn | 35 from `P3_hub_genes.csv`; 17/33 from `P5_GSE325938_hub_regionalization.csv` | A1, A3 | ✅ exact (source = GSE325938, disclosed) |
| 6 | Results | Human miRNA p=0.51 | perm_p=0.5101 from `P4_setlevel_test.json` | A1, A3 | ✅ exact |
| 7 | Results | Translation 46.3% vs 47.1%, −0.9pp, p=0.14 | 2266/4899=46.3%; 6779/14390=47.1%; perm p=0.1396 | A2, A3 | ✅ exact |
| 8 | Discussion | ADRA2A 0.618→0.532, p=0.118; "no target clears both filters" | 0.618 (Tier-1) / 0.532 (full-library) p=0.118 from `P6_*` | A3 | ✅ exact |
| 9 | **Results L58/L234** | Incision LODO AUC **0.917** [0.729,1.0] = "most persuasive evidence"; "real, not overfit signal" | Own `P3_lodo_auc_ci_leakage_controlled.csv` → **0.677** [0.374,0.940] (CI⊃0.5); 0.917 is the standard (non-leakage-controlled) LODO | **A2; editor-confirmed** | ⚠ **OMISSION** — leakage-controlled value undisclosed; contradicts "real signal" claim |
| 10 | References L200 | Ref 31 (Xiao 2002) — no DOI | Genuine DOI `10.1073/pnas.122231899` (PMID 12060780) exists in `_R4_ref_DOIs.json` but was NOT printed | A3; editor-confirmed | ⚠ **MISSING DOI** (prior round mis-removed it from ref 33 instead of adding to ref 31) |
| 11 | STROBE / L277 | Manuscript: "**STROBE 2023**"; checklist title = old SR title | Checklist header: "**STROBE 2007**" + old SR-era title | A4; editor-confirmed | ⚠ **MISMATCH** |

No headline number *failed to reproduce*. The three ⚠ rows are **omissions/inconsistencies**, not arithmetic errors.

---

## 4. Graded consolidated issue list

### Tier 0 — submission-blocking format / admin gates
- **A4-F1 (format hard-fail).** PLOS ONE requires a **structured abstract** (Background / Methods / Results / Conclusions headings). The current abstract is one unbroken paragraph. *Fix:* add the four bold subheadings; keep ≤200 words (currently exactly 200, so reformat, do not expand). *Why:* PLOS returns non-compliant manuscripts for technical correction before peer review.
- **A4-F12 (to complete at submission).** Zenodo DOI is a literal placeholder `10.5281/zenodo.XXXXXXX — to be minted at submission`. *Fix:* mint the Zenodo DOI at upload and replace the placeholder in ms L216 + cover letter. Not a defect now, but must be closed before/at submission.

### Tier 1 — analyses/framing that change interpretation
- **A2-F2 (editor-confirmed, highest-value design defect).** The manuscript headlines the incision LODO AUC **0.917 [0.729, 1.000]** as "the most persuasive evidence" and states "Honest evaluation confirmed a real, not overfit, classifier signal" (L58, L234). Its *own* leakage-controlled table (`P3_lodo_auc_ci_leakage_controlled.csv`, LC-LODO) gives the same fold at **0.677 [0.374, 0.940]** — a confidence interval that **includes 0.5**. The 0.917 is the legitimate cross-animal LODO (not the 0.999 within-dataset leakage-inflated number, which the manuscript already correctly discounts), but the leakage-controlled re-estimate is never disclosed. *Fix:* in L58/L234, after the 0.917 figure, add: "A leakage-controlled re-estimation (feature selection recomputed out-of-fold; `P3_lodo_auc_ci_leakage_controlled.csv`) gives 0.677 [0.374, 0.940] for this fold, a confidence interval that includes chance, so we report the classifier signal as a resampling-sensitive candidate-generation tool rather than as a validated cross-model generalisation." Replace "real, not overfit, classifier signal" with "a cross-animal LODO signal whose leakage-controlled estimate is not distinguishable from chance for the pivotal incision fold." *Why:* this is an internal contradiction the manuscript's own data reveals; disclosing it *strengthens* the paper's honest-null thesis and pre-empts a reviewer who will find the 0.677 table.
- **A2-F1 (residual design transparency).** GSE265957's two timepoints (same animals) enter the 6-input primary as two independent contrasts each at w=1.00, so the translatome study carries double a single bulk study's effective variance weight. The manuscript already *leads with* the bulk-only (45.7% core translatome-dependent) and collapse sensitivities, so this is bounded — but the weight assignment is not stated as a residual limitation. *Fix:* add one sentence in L38 or L140: "Because GSE265957 contributes two meta-inputs at equal weight, the translatome study's effective variance weight in the six-input primary is double that of a single bulk study; the bulk-only (4-input) and collapse (5-input) sensitivities bound this and are reported as the primary robustness checks." *Why:* makes the double-counting explicit rather than implicit.
- **A1-F1 (domain accuracy — sodium-channel defence).** L46 defends bulk SCN down-regulation by citing (i) neuronal Nav1.7/1.8/1.9 protein up-regulation, (ii) human SCN9A mutations, (iii) Nav1.8 inhibitor-clinical-failure. Citation-category errors: refs 11–13 (human SCN9A mutations) establish *necessity for pain*, not *injury-induced up-regulation*; Nav1.8 down-regulation after axotomy actually *agrees* with the bulk down-signal (the manuscript frames it as a contradiction); and the defining injury-induced channel **Nav1.3/SCN3A** is omitted. *Fix:* rephrase L46 to (a) state the human SCN9A mutations show the channel is *required* for human pain, not that it is up-regulated here; (b) note Nav1.8/Nav1.9 down-regulation post-axotomy is consistent with the bulk signal; (c) add the omitted Nav1.3/SCN3A injury-induction literature and the neuronal-loss/atrophy confound. *Why:* the sodium-channel paragraph is the most clinically-loaded passage; mischaracterising the citations invites a domain reviewer to reject the hedge.

### Tier 2 — wording / precision
- **A2-F3.** "substantial heterogeneity" for median I²=38.8% is inaccurate (Higgins–Thompson: 25% low, 50% moderate, 75% high → ~39% is low-to-moderate). *Fix:* replace "substantial" with "low-to-moderate but non-negligible" or drop the adjective; keep the empirically correct 1,008/4,055 shrinkage. (Check the Discussion for any "substantial" wording; the abstract L14 currently says only "heterogeneity-sensitive" — acceptable.)
- **A2-F4.** Neuroinflammation/DAM/Complement reported as three independent "q=0.003" programmes, but they share many members (one neuroimmune axis triple-counted). *Fix:* state explicitly that the three sets overlap and the effective number of independent discoveries is ~1; report the three q-values but frame as "one coordinated neuroimmune–complement axis."
- **A1-F2.** "DAM-microglia" is over-specific for a bulk DRG/spinal signal (DRG has sparse microglia; the programme is shared with macrophages). The manuscript's own L42 hedge ("DAM-like denotes the shared transcriptional programme, not a cell-type-resolved state") already mitigates this — *strengthen* by using "DAM-like neuroimmune" consistently and correcting the Schafer provenance (Schafer 2015 describes *development*, not the Keren-Shaul 2017 DAM definition the manuscript cites as the origin).
- **A1-F3 / A4-F19.** Title's lead word "Conserved" and the Abstract/Introduction CPSP front-loading (10–50% prevalence, "druggable targets … remain undefined *for CPSP*") mismatch a dataset that is ~83% nerve-injury. The paper's own non-predictive-incision result is the stronger, more honest contribution. *Fix:* keep the nerve-injury-associated framing already in L14/L38; soften title if desired (optional) but at minimum ensure the Conclusion retracts any "conserved CPSP mechanism" language and foregrounds the honest-null/methodological-boundary contribution.
- **A1-F4.** Abstract's global docking null ("found no target clearing both filters") is scoped in the body to 10 structurally tractable, *non-ion-channel* targets; the ion-channel class (canonical pain targets) was never docked. *Fix:* in the Abstract, add the qualifier "among 10 structurally tractable non-ion-channel targets" so the global-null claim is not over-read.
- **A1-F7.** Missing must-cite: Nav1.3/SCN3A injury-induction; spinal-microglia time/sex-specific DAM literature.
- **A1-F8.** CXCL12/CXCR4 "implicated specifically in CPSP" rests on rodent neuropathic/postsurgical studies, not human CPSP. *Fix:* drop "specifically in CPSP"; say "in nerve-injury and postsurgical pain models."
- **A2-F6 / A1-F6.** ADRA2A verdict asymmetry: both its Tier-1 and MW-adjusted full-library tests are statistically significant, yet the paper calls it "inconclusive, not a confirmed null," while treating weaker signals for controls as informative. *Fix:* make the asymmetry explicit — "ADRA2A retains a weak MW-adjusted signal (p≈0.0005) but its full-library AUC 0.532 is NS, so we classify it inconclusive; this is stricter than the control targets, none of which survive size-independent correction."
- **A2-F7.** Human-miRNA p=0.51 with n=60 and 253 plasma miRNAs cannot distinguish a true null from a modest real association. *Fix:* state this as a power limitation (the manuscript already scopes it as underpowered — keep/extend).

### Tier 3 — format / provenance / housekeeping
- **A3-F1 / A4-F7 (ref 31 DOI).** Ref 31 (Xiao 2002, L200) lacks a DOI; the genuine `10.1073/pnas.122231899` (PMID 12060780) was mistakenly removed from ref 33 in the prior round instead of being added here. *Fix:* append `https://doi.org/10.1073/pnas.122231899` to ref 31. Confirm ref 33 keeps only `10.1021/acs.jmedchem.5b02008`.
- **A3-F2 (orphan GSE249746).** `results/tables/P4_GSE249746_hub_celltype.csv` exists but GSE249746 is **not** in the manuscript's disclosed 12-dataset list (the 17/33 correctly comes from disclosed GSE325938). *Fix:* delete the unused GSE249746 artifact, or if it was an exploratory precursor, note it is superseded by GSE325938 and not cited.
- **A3-F3 (drug-count wording).** "3,085 drugs" treated as the tested N; per-target scored N ≈ 3,070. *Fix:* "3,085 dockable drugs (≈3,070 scored per target)."
- **A3-F4 (stale map).** `results/tables/_R4_reference_map.json` is a pre-renumbering map. *Fix:* regenerate or delete; the manuscript itself is internally consistent, so this is housekeeping only.
- **A4-F3 (STROBE title).** STROBE checklist header carries the old ScientificReports title. *Fix:* replace with the current PLOS title.
- **A4-F4 (STROBE version).** Manuscript L277 says "STROBE 2023"; checklist says "STROBE 2007" (the actual STROBE statement, von Elm et al. 2007). *Fix:* change manuscript to "STROBE checklist (von Elm et al., 2007)" to match; "STROBE 2023" is not a real version.
- **A4-F18 (display-items count).** Manuscript L226 says "5 figures + 3 tables = 8" but the docx has 5 figure + 5 table objects. *Fix:* correct to "5 figures + 5 tables = 10" (or recount the main display items precisely).
- **A4-F9 (docx metadata).** `Manuscript.docx` core properties carry the python-docx generator default as author/title. *Fix:* set core metadata author="Yang Y", title=manuscript title in the build script.
- **A4-F20 (priority claims).** "among the first" claims sit in mild tension with the honest-null emphasis. *Fix:* temper to "to our knowledge, one of the first …".

---

## 5. Consensus / complementarity / disagreement

**Consensus (all 4):** the science is honestly framed and the core meta-analysis numbers are reproducible; the manuscript's strongest real contribution is the *honest null + methodological-boundary* thesis (docking, translation non-predictive, heterogeneity sensitivity), and this should be the headline rather than "conserved CPSP mechanism." No expert disputes the bulk-only reconciliation (2,512) or the random-effects shrinkage.

**Complementarity:** A1 supplied the domain citation-accuracy defects; A2 the design-layer omissions (leakage AUC, I², overlapping sets); A3 the provenance/format defects (ref DOI, orphan file); A4 the PLOS/STROBE format gates. Together they cover all four layers; no layer is unguarded.

**Disagreement / adjudication:**
- *Severity of A2-F2 (ML AUC):* A2 rated it Major (it undercuts "real signal"). A3, auditing only arithmetic, would rate it Minor (the 0.917 is correctly the cross-animal LODO). **Adjudication:** adopt A2's stricter reading — the omission of the leakage-controlled 0.677 is a genuine internal contradiction the manuscript's own table reveals, and the "real, not overfit signal" claim is not supported for the pivotal fold. This is Tier 1, not Minor.
- *A1-F5 (GSE249746):* A1 flagged it as an "undisclosed dataset." A3 showed the 17/33 actually derives from disclosed GSE325938 and GSE249746 is merely an unused stale file. **Adjudication:** downgrade to Tier 3 housekeeping (delete unused file); no hidden-dataset defect.
- *Abstract structure (A4-F1):* A4 rates it a format hard-fail. This is correct per PLOS ONE's structured-abstract requirement but is a trivial reformatting, not a scientific defect — keep as Tier 0 format, not DESK-REJECT.

---

## 6. Priority must-fix list

**Must fix before submission (Tier 0 + Tier 1):**
1. Structured abstract (A4-F1) — add Background/Methods/Results/Conclusions.
2. Disclose leakage-controlled AUC 0.677 + temper "real signal" claim (A2-F2, editor-confirmed).
3. Add ref 31 DOI (A3-F1).
4. Fix STROBE title + version mismatch (A4-F3/F4).
5. Sodium-channel citation rephrase (A1-F1) — highest domain-risk passage.

**Must reword (Tier 2):** I² "substantial"→low-to-moderate; overlapping-set framing; DAM-like consistency; CPSP-front-load softening; ADRA2A asymmetry; CXCL12 "specifically CPSP" drop; docking global-null qualifier.

**Must reword/housekeep (Tier 3):** GSE249746 file delete; 3,085→≈3,070; stale _R4_reference_map.json; display-items count; docx metadata; priority-claim tempering.

**DESK-REJECT flags:** none. The manuscript is scientifically honest and the defects are fixable in one revision pass.

---

## 7. What stands up (do NOT change)

Carried from the experts' § Stands up:
- The **non-circular translation test** (46.3% vs 47.1%, p=0.14) is correctly designed and the permutation test is the right choice over a 2-proportion binomial.
- **Set-level BH + random-effects caution** — exemplary; the manuscript does not over-claim the core.
- **Bulk-only reconciliation** (2,512) and the explicit lead-with-fragility framing (45.7% translatome-dependent).
- **The honest-null docking framework** (prospective full-library breadth, reverse controls, MW correction) — the paper's genuine contribution.
- **Causal-scope / AI-use discipline** — no causal claim; AI disclosure names the tool and states it was not used for data selection/interpretation.
- **Author-degree integrity** — no "Dr./MD/PhD" anywhere (A4 hard check passed).
- **Data Availability** uses a real GitHub URL, not "available on request."
- All 18 recomputed headline numbers reproduce exactly.

---

## 8. Recommended handling path

**Path A — revise and resubmit to PLOS ONE as the same article type (recommended).** All defects are fixable in one pass; the science is honest and the evidence level matches PLOS ONE's scope (it explicitly welcomes null/negative results). No article-type downgrade is warranted. The revision should *swap the headline*: lead with the honest-null/methodological-boundary contribution (which the data robustly support) and demote "conserved CPSP mechanism" to a descriptive, heterogeneity-sensitive observation.

---

## 9. Process lessons (what the automated gates could not catch)

- The consistency gate (`p7_consistency_gate.py`) verifies arithmetic and string matches; it **cannot** ask "is the ML signal claim supported by the leakage-controlled table the author also deposited?" That design-layer omission (A2-F2) passed every gate. **New gate artefact proposed:** a script that diffs every AUC/statistic cited in the manuscript against *all* tables in `results/tables/`, flagging any cited value whose leakage-controlled or sensitivity counterpart is undisclosed.
- The gate checks the reference *numbering* but not *whether every reference has a resolvable DOI* (A3-F1) or whether the STROBE checklist title matches the manuscript (A4-F3). **New gate assertions:** (a) every reference entry ends with a `https://doi.org/...` or PMID; (b) the STROBE checklist title string equals the manuscript title string.
- The prior round's "bogus DOI" fix was mis-applied (removed from ref 33 instead of added to ref 31) — a direct consequence of editing the rendered manuscript rather than the `{{key}}` source. **Lesson:** renumbering/DOI edits must be done by script with a verification pass, not by hand.

---

## Editor's closing note to the author

Your strongest claim — "a conserved CPSP mechanism on the DRG–spinal axis" — does not hold as strongly as the word "conserved" implies, and *that is not your fault*: at K=5–6 the random-effects core collapses 4,055→1,008 and 45.7% of it is translatome-dependent, and the incision arm (your only CPSP-adjacent model) is non-predictive. The finding you buried — that the docking screen, the translation test, and the heterogeneity analysis together constitute a *rigorous, honest null* that exposes where repurposing approaches in this field are fragile — is actually your contribution, and it is exactly what PLOS ONE says it wants. Swapping the two (headline the honest null, demote "conserved") converts the paper from a fragile-signal story into a stable methodological one. The leakage-controlled AUC (0.677, CI⊃0.5) is your friend here, not an embarrassment: disclosing it shows you already did the rigorous thing and makes the honest-null thesis unassailable.

*Panel files: `reviews/round7_2026-09-26/A1_domain.md`, `A2_design.md`, `A3_implementation.md`, `A4_venue.md`. Shared brief: `_PANEL_BRIEF.md`.*
