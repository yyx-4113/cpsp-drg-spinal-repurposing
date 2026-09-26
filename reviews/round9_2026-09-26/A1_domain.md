# EXPERT A1 — Domain Review: pain neurobiology / anesthesiology

**Role:** Domain / biological & clinical correctness reviewer, independent multi-expert panel (Round 9).
**Manuscript:** `reports/MVP_ScientificReports_submission.md` (283 lines) + `reports/MVP_ScientificReports_supplementary.md`.
**Target venue:** PLOS ONE.
**Independence statement:** Treated as a first submission. I read only the manuscript, its supplementary file, the panel brief, and the raw meta CSVs in `results/tables/`. I did not read any prior review, response, manifest, memory, or sibling report. Every quantitative claim below was re-derived by me from the cited source files.

---

## 1. The central "nerve-injury-specific, not CPSP-specific" claim is over-reached in the Abstract/Conclusions relative to the evidence and to the Discussion itself

【Problem】 The Abstract conclusion and L20 assert the axis is "rather than a CPSP-specific target," a categorical claim the evidence cannot sustain, while the Discussion (L120–121) correctly hedges it as "not shown."

【Evidence】
- L20 (Conclusions): "The axis is a nerve-injury-associated, heterogeneity-sensitive response rather than a CPSP-specific target; the docking null is a methodological boundary, not a false lead."
- L120 (Discussion): "The nerve-injury signature does not predict incision direction (46.3% versus a 47.1% background; difference −0.9 pp, p = 0.14), so **specificity of the axis to postsurgical versus nerve-injury pain is not shown by this meta-analysis.**" (emphasis added).
- The translation evidence: non-circular test 46.3% (2,266/4,899) vs 47.1% background (6,779/14,390), risk difference −0.9 pp, permutation p = 0.14 (L58; Supplementary Table S6 Panel B). A non-significant p = 0.14 is a failure to reject *no* difference, not evidence of *specificity*.
- Dataset imbalance: of the five DRG-axis studies, four are nerve-injury models and exactly one (GSE267799) is an incision/CPSP-closest model (L14, L36; Table 1b header L257). "Does not predict the single incision arm" cannot establish "nerve-injury-specific" — it can only establish "not demonstrated to translate."

【Why it matters】 For PLOS ONE the abstract and conclusions are the most quoted text. A categorical "not CPSP-specific" statement, derived from a single incision dataset and a non-significant (p = 0.14) translation test, invites being cited as if the study *ruled out* a CPSP component. This also creates an internal inconsistency between the confident Abstract and the careful Discussion that an editor or reviewer will immediately flag. The "nerve-injury-associated" framing is well supported; the "rather than CPSP-specific" extension is not.

【Specific fix】 L20: replace "rather than a CPSP-specific target" with "and is not shown by this meta-analysis to be CPSP-specific, because the nerve-injury signature does not predict the single incision arm (46.3% vs 47.1% background, p = 0.14)." Keep the Discussion wording as-is (it is correct).

---

## 2. The Nav1.8/suzetrigine clinical claim is anchored only to a 2026 secondary review, not to the pivotal trial(s)

【Problem】 The statement that "the more recent Nav1.8 inhibitor clinical programme shows that channel is druggable" (L52) — the single concrete clinical anchor of the entire Nav1.7/1.8 reconciliation — cites only a 2026 Cleveland Clinic Journal review (ref 20), not the primary phase-2/3 trial(s) that established suzetrigine's efficacy and approval.

【Evidence】
- L52: "…whereas the more recent Nav1.8 inhibitor clinical programme shows that channel is druggable without establishing injury-induced SCN10A up-regulation."
- L112: "consistent with the absence of a selective nonopioid analgesic signal such as suzetrigine²⁰ in this docking space…"
- Reference list (refs 1–33, L176–208): ref 20 = Divito, A. E. et al., *Cleveland Clinic Journal of Medicine* **93**, 94–98 (2026). No Jones et al. (N Engl J Med 2023, phase 2), no phase-3 NEJM publication, and no FDA-approval primary source appear anywhere in the list. I scanned all 33 references; suzetrigine is represented solely by a narrative review.

【Why it matters】 A clinical assertion about a drug's mechanism and regulatory status in a pain journal should rest on the registration trial, not a secondary review. Omitting the pivotal trial is a material citation gap: it is precisely the trial evidence that lets the authors claim Nav1.8 is "druggable," and a reviewer in this field will expect the primary source. It does not undermine the reconciliation (which is logically sound — see § Stands up), but it weakens the one externally verifiable clinical pillar.

【Specific fix】 Add the pivotal suzetrigine trial(s) to the reference list and cite at L52, e.g.: "…whereas the more recent Nav1.8 inhibitor suzetrigine, validated in phase-2/3 acute-pain trials (Jones et al., *N Engl J Med* 2023; …) and approved in 2025, shows the channel is druggable without establishing injury-induced SCN10A up-regulation." (Adjust the exact citation to the authors' preferred primary source.)

---

## 3. The SCN10A/Nav1.8 "down-regulated in axotomized IB4+ neurons" reconciliation is asserted without a primary citation — and so is the immune/glial-dilution argument

【Problem】 The mechanistic sentence that rescues the "all four nociceptor Na channels DOWN in nerve injury" finding from contradiction with the literature is presented with no reference, making the central ion-channel hedge unverifiable.

【Evidence】
- L52: "These bulk transcriptome-level down-regulations are consistent with, rather than contradictory to, the known biology of injured DRG: **SCN10A/Nav1.8 mRNA is down-regulated in axotomized IB4+ neurons, and bulk DRG signal is confounded by injury-induced neuronal atrophy/loss and by the dilution of neuronal transcripts by infiltrating immune and glial cells.**" — no superscript reference terminates this sentence.
- Contrast: the adjacent sentence ("Nav1.6 is transcriptionally up-regulated in DRG and contributes to neuropathic pain¹⁰") and the germline-channelopathy sentence ("germline SCN9A channelopathies¹¹,¹²,¹³…") *are* cited. Only the two factual claims that do the reconciliatory work are uncited.

【Why it matters】 This sentence is the linchpin of the manuscript's most scrutinised biological claim (the SCN direction reversal). If challenged, the authors currently have no primary source to point to for either (a) Nav1.8/SNS down-regulation after axotomy, or (b) DRG neuronal loss / IB4+ atrophy / immune-glial transcript dilution after nerve injury. Both are well established in the primary literature; leaving them uncited invites a "unsubstantiated assertion" critique and is inconsistent with the manuscript's otherwise careful citation discipline.

【Specific fix】 Append primary citations to the end of the L52 reconciliation sentence, e.g.: "…dilution of neuronal transcripts by infiltrating immune and glial cells (Black et al., *J Neurosci* 1999/2002; Dib-Hajj et al.; and Groves et al., 2005 / Hu & McLachlan on DRG neuronal loss after nerve injury)." (Authors should select the specific primary papers they rely on.)

---

## 4. The "Nav1.8 is down-regulated yet its inhibitor is an analgesic" paradox is resolved only implicitly and should be stated

【Problem】 A reader can perceive a contradiction between "SCN10A is down-regulated in nerve injury" (L52, Table 1b) and "suzetrigine, a Nav1.8 inhibitor, is a clinical analgesic" (L52, L112), even though the manuscript does resolve it.

【Evidence】
- L52 reports SCN10A bulk meta_Z −3.03 / FDR 0.008, direction DOWN in all nerve-injury contrasts (verified: six-input lfc G212311 −0.117, G278227 −0.569, G241361 −3.078, G265957 D4/D63 both negative; four-bulk meta_Z −3.034, FDR 0.00795 — see § What I actually checked).
- L112: "…suzetrigine acts on the expressed channel, so an mRNA-level signal is not expected to translate into docking affinity, and this is a scope limit rather than a discriminatory test."

【Why it matters】 The logic is correct (a blocker inhibits channel function regardless of transcript abundance, and Nav channels were not docked because they lack a ligand-anchored pocket — L160), but it is distributed across two paragraphs and never made explicit as "no paradox." A reviewer skimming L52 may raise a false "contradiction" objection that the authors then have to defend in rebuttal. One explicit sentence pre-empts this.

【Specific fix】 After the L52 reconciliation sentence (Issue 3 fix), add: "Because suzetrigine inhibits Nav1.8 channel function irrespective of baseline transcript abundance, the absence of injury-induced SCN10A up-regulation neither supports nor refutes its analgesic efficacy, and Nav channels were not docked here (no ligand-anchored pocket, L160)."

---

## 5. The "DAM-like" partial hedge is correctly provenanced, but the authors should confirm TREM2/APOE themselves sit in the up-regulated core

【Problem (minor, primarily a verification request)】 The DAM_microglia set as *defined* (Supplementary Table S5, L147) includes the TREM2/APOE/TYROBP axis, yet the text frames the captured programme as only "partially" DAM. The "partial" qualifier is correctly aimed at the pain-vs-neurodegeneration DAM distinction, but the reader cannot tell whether the *hallmark* Trem2/Apoe axis is actually up-regulated here.

【Evidence】
- L48: "DAM-like denotes the shared transcriptional programme, not a cell-type-resolved state."
- L84: "the absence of a P2RX/P2RY signal here implies that the DAM-like state captured is only partially the classic P2X4-driven microglial activation described in that literature…"
- L120: "…our DAM-like set follows that neurodegeneration-defined provenance — distinct from the developmental/homeostatic microglia described by Schafer et al.²⁴ — and is therefore described as DAM-like."
- Set definition (L147): DAM_microglia *includes* "TREM2/APOE/TYROBP axis, lysosomal (CTSD, LPL, CST7), phagocytic (MERTK, ITGAX, AXL), complement (C1QA/B/C), SPP1, GPNMB, CD68, CSF1R."
- Provenance check: Keren-Shaul et al. 2017 (ref 23, *Cell* 169:1276) is the correct origin of DAM; Schafer et al. 2012 (ref 24, *Neuron* 74:691) is correctly distinguished as the *homeostatic/developmental* microglia paper. This provenance is **correct** and is not the "Schafer developmental" definition.

【Why it matters】 Gene-set tests are aggregate; a significant DAM set (q = 0.003, L48/S5b) does not guarantee that TREM2/APOE/TYROBP themselves are in the up-regulated core. If they are *not*, the "DAM-like" label is even more partial than stated and the authors should say so; if they *are*, that strengthens the claim. Either way the manuscript should report the core membership of the canonical DAM markers.

【Specific fix】 In the Results or Discussion DAM paragraph, add one sentence: "Of the canonical DAM hallmark genes, TREM2, APOE and TYROBP [were/were not] themselves recovered in the up-regulated core (n = X/3), which is why we label the programme DAM-*like* rather than fully reconstituted DAM." (Fill from `META_DRG_axis_stouffer.csv` gene-level data.)

---

## 6. The human plasma-miRNA "blood-proxy boundary, not a failure" framing is clinically reasonable for n = 60 — keep it, but tighten one over-statement

【Problem (minor)】 The framing is sound, but L70 twice calls the result a "failure to detect, not evidence of absence" while also calling it (L68 heading) a "blood-proxy boundary, not a failure" — slightly mixed wording that a careful copy-edit should unify.

【Evidence】
- L70: "We stress that p = 0.51 is a failure to detect, not evidence of absence: with n = 60 plasma samples indexing 253 plasma-detectable miRNAs, the 5,000-permutation set-level test has limited power against a small-to-moderate association…"
- L68 heading: "The human layer is negative, a blood-proxy boundary, not a failure."

【Why it matters】 Low-stakes, but the same concept is labelled both "boundary" and "failure to detect" in adjacent paragraphs; unifying the phrasing prevents a reader from thinking the authors are contradicting themselves about whether it is a failure.

【Specific fix】 In L70, replace "p = 0.51 is a failure to detect, not evidence of absence" with "p = 0.51 is a non-significant result that demarcates a boundary for prospective validation, not evidence of absence."

---

# § Stands up (items I specifically checked and found CORRECT)

1. **SCN direction and magnitude claims are fully verified against raw source data and are internally consistent.** I recomputed the four-bulk meta from `META_bulkonly_meta.csv` and the six-input meta from `META_DRG_axis_stouffer.csv`:
   - Four-bulk (Table 1b source): SCN9A meta_Z −2.9247 / FDR 0.01078 → manuscript −2.92 / 0.011 ✓; SCN10A −3.0337 / 0.00795 → −3.03 / 0.008 ✓; SCN11A −3.4080 / 0.002638 → −3.41 / 0.003 ✓; SCN8A −4.9236 / 8.50e-7 → −4.92 / 1.0e-5 ✓.
   - Per-contrast log₂FCs match Table 1b exactly: incision (GSE267799) UP (+0.607 SCN9A, +0.987 SCN8A…), all four nerve-injury contrasts DOWN. Six-input consistency 0.833 (5/6 down); four-bulk consistency 0.75 (3/4 down). SCN8A is the most significant of the four in both the text (L52) and Table 1b (L259–262) — consistent.
   - L52 text values equal Table 1b rows exactly. No discrepancy.

2. **The Nav1.8/suzetrigine reconciliation is coherent and non-contradictory.** The manuscript correctly separates two distinct levels: (a) *channel-level druggability* — suzetrigine inhibits the expressed Nav1.8 protein; (b) *mRNA-level* — the bulk meta shows SCN10A down, which would *not* be expected to translate into docking affinity (and Nav channels were not docked, L160). Claiming the channel is "druggable without establishing injury-induced SCN10A up-regulation" (L52) is therefore logically consistent with the down-regulation finding. No contradiction with the rest of the paper.

3. **OXPHOS suppression is honestly scoped as fixed-effect-only.** Across L48, L120, Fig. 1 legend and Supplementary Table S5b, OXPHOS is reported as mean_Z −2.37, q = 0.020 under fixed effects and q = 0.31 (did NOT survive random-effects BH) — uniformly framed as "not reliable under between-contrast heterogeneity." No over-claim found. Verified against S5b (Mitochondria_OXPHOS perm p 0.004498 / BH q 0.02024 FE; 0.06897 / 0.3103 RE).

4. **The "DAM-like" provenance is correct.** Keren-Shaul 2017 (ref 23, *Cell*) is the true origin of the DAM definition; Schafer 2012 (ref 24, *Neuron*) is correctly cast as the *homeostatic/developmental* microglia paper and explicitly distinguished. The pain programme is hedged as only partially DAM via Tansley 2022 (ref 19, time- and sex-specific overlap). This is biologically defensible and not over-claimed.

5. **The purinergic self-negative is soundly interpreted.** P2RX/P2RY showed no coordinate change (perm p = 0.339 bulk-only, 0.440 six-input; L84, S5) and the authors correctly use this to qualify the DAM programme as "partially" the classic P2X4-driven microglial activation (Tsuda 2003, ref 18), rather than contradicting it. The interpretation is cautious and appropriate; it does not over-read a 12-member family null as "no purinergic role."

6. **Family-aggregate vs individual-channel distinction is handled correctly.** The four specific SCNs are individually significant and down-regulated, while the broader Nav_SCN family set (14 members) is not coordinately changed (q = 0.44, L48/S5b). The manuscript explicitly separates these (individual channels significant; family aggregate not), which is the correct reading and avoids a false "ion channels changed en bloc" claim.

7. **No clinically FALSE or misleading statement detected.** I specifically checked: (a) suzetrigine "acts on the expressed channel" — true (it is a Nav1.8 pore blocker); (b) "germline SCN9A channelopathies establish Nav1.7's necessity for human pain but are not evidence of injury-induced up-regulation" (L52) — accurate (gain-of-function → erythromelalgia/PEPD, loss-of-function → congenital indifference to pain); (c) "selective Nav1.7 inhibitors have repeatedly failed in the clinic" — supported by refs 14–16; (d) SCN8A = Nav1.6, correctly identified (L52). I found no statement that is clinically false or that misattributes channel vs mRNA-level effects.

---

# § Questions for the authors

1. **TREM2/APOE/TYROBP core membership (Issue 5).** Are TREM2, APOE and TYROBP themselves in the up-regulated meta core? This determines how literally "DAM-like" should be taken and should be stated explicitly.
2. **Four-bulk vs six-input headline numbers (clarification, not defect).** Table 1b and L52 report the *four-bulk* meta_Z/FDR (verified: −2.92/0.011 etc.), whereas the "primary 4,055-gene core" is the *six-input* meta (SCN9A six-input meta_Z = −3.475, FDR ≈ 0.0023). The channels are in both cores, so the biology is unchanged, but was this intentional? A one-line note that the SCN headline statistics are the four-bulk values (by design, to isolate nerve-injury bulk signal) would prevent confusion.
3. **SCN3A/Nav1.3.** L52 notes SCN3A/Nav1.3 "was not among the tested sets and should be examined in a revision." Since Nav1.3 is the channel most transcriptionally induced after injury, was it absent from the Nav_SCN gene set definition (S5: SCN1–7, SCN1B–4B) by oversight, or deliberately (it is not strictly "nociceptor-restricted")? Clarifying this would strengthen the ion-channel discussion.
4. **Human n = 60 power.** The set-level permutation p = 0.51 is framed as underpowered. Could the authors report the minimum effect size (e.g., number of plasma-detectable miRNAs that would need to associate) the 5,000-permutation test at n = 60 could have detected at, say, 80% power? This would make the "boundary" claim quantitative rather than qualitative.

---

# § What I actually checked

**Files read (allowed):**
- `reviews/round9_2026-09-26/_PANEL_BRIEF.md` — independence rules, environment trap list, scope.
- `reports/MVP_ScientificReports_submission.md` — full, two passes (lines 1–150, 151–284).
- `reports/MVP_ScientificReports_supplementary.md` — full (Tables S1–S7).
- `results/tables/META_DRG_axis_stouffer.csv` — SCN rows via targeted retrieval (six-input primary, 16,553 data rows).
- `results/tables/META_bulkonly_meta.csv` — SCN rows via targeted retrieval; confirmed header schema `symbol,K,meta_Z,meta_p,consistency,n_up,n_dn,lfc_GSE267799,lfc_GSE212311,lfc_GSE278227,lfc_GSE241361_DRG,meta_FDR`.

**Values I recomputed from raw source (vs manuscript):**
- SCN9A four-bulk: meta_Z = −2.924735, meta_FDR = 0.010780 → manuscript −2.92 / 0.011. MATCH.
- SCN10A four-bulk: meta_Z = −3.033675, meta_FDR = 0.007955 → manuscript −3.03 / 0.008. MATCH.
- SCN11A four-bulk: meta_Z = −3.407961, meta_FDR = 0.002638 → manuscript −3.41 / 0.003. MATCH.
- SCN8A four-bulk: meta_Z = −4.923567, meta_FDR = 8.498e-7 → manuscript −4.92 / 1.0e-5. MATCH.
- SCN9A six-input: meta_Z = −3.475391, meta_p = 5.10e-4, consistency = 0.833333, n_up = 1, n_dn = 5; per-contrast lfc: GSE267799 +0.6067 (UP), GSE212311 −0.0730 (DN), GSE278227 −0.2854 (DN), GSE241361 −2.7098 (DN), GSE265957 D4 −0.3035 (DN), D63 −0.5007 (DN). Directions match Table 1b L259 exactly (1 up, 5 down).
- SCN8A six-input: meta_Z = −5.112927, meta_p = 3.17e-7, consistency = 0.833333; per-contrast lfc: GSE267799 +0.9873 (UP), the four nerve-injury contrasts all negative. Matches Table 1b L262.
- Confirmed L52 text numbers (SCN9A −2.92/0.011, SCN10A −3.03/0.008, SCN11A −3.41/0.003, SCN8A −4.92/1.0e-5) are identical to Table 1b rows (L259–262) — internal consistency verified.
- Confirmed SCN8A is the most significant of the four in both text and table (lowest FDR 1.0e-5).

**Cross-checks against supplementary (not raw CSV, but authoritative as printed):**
- OXPHOS q = 0.020 (FE) / 0.31 (RE): S5b row Mitochondria_OXPHOS = perm p 0.004498 / BH q 0.02024 (FE), 0.06897 / 0.3103 (RE). Consistent with L48/L120/Fig 1.
- DAM/neuroinflammation/complement q = 0.003 each (FE and RE): S5b confirms. Consistent.
- ADRA2A two-filter logic (brief trap): full-library AUC 0.532, p = 0.118 (fails filter 1); size-independent BH q = 0.0025 (passes filter 2) → "inconclusive." Consistent with S4 Panel B and L112. I did not re-litigate this as a defect per the brief; I only confirmed the prose states it as inconclusive, not a confirmed hit.
- References 1–33 scanned: suzetrigine represented only by ref 20 (Divito 2026 review); Nav1.7 failure by refs 14–16; DAM/microglia-in-pain by refs 18–24, 28; DRG–spinal axis by refs 3–7, 31. No primary suzetrigine trial present (Issue 2).

**Forbidden files:** I did not open any `reviews/REVIEW_round*.md`, `reviews/round8*`, other `reviews/round9*` expert files, `.workbuddy/memory/**`, `SUBMISSION_MANIFEST.md`, `RESPONSE_*.md`, `REVISION_*.md`, prior expert outputs, or conversation history. No external web sources were used; all verdicts rest on the manuscript, its supplementary, and the two raw CSVs named above.

**Discrepancies found:** One (informational only, already disclosed by the authors at L264): the Table 1b "Bulk meta_Z/FDR" columns are four-bulk values, not the six-input primary-meta values; both are significant and same-direction, so no biological contradiction, but the headline SCN statistics are not the "primary 4,055-gene" numbers. See Question 2. No other numerical discrepancy between manuscript, tables, and raw CSV was found in the scope of this review.
