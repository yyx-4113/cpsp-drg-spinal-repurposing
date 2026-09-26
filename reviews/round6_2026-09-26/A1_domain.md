# Independent Domain Review — Pain / Neuroscience clinician-scientist

**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
**Venue under consideration:** PLOS ONE (Research Article)
**Review type:** First-submission-style independent review. I read the manuscript and the three named data tables myself and verified a subset of references against the primary literature. I did not read any prior review/response/revision documents or the project plan, and treated this as a fresh submission.

**Overall assessment:** The analytical discipline of this paper is genuinely strong — the random-effects sensitivity analysis, the non-circular translation test, the bootstrap stability audit, and the prospectively specified full-library docking null are exactly the controls this field usually omits. My concerns are concentrated in the *biological/clinical framing* of the results, the engagement with the sodium-channel literature (the single most literature-contrary and clinically load-bearing finding), and reference hygiene. None are fatal; several are straightforward fixes. I recommend **Major Revision**.

---

## FINDING 1 — Residual CPSP-specific over-framing in the Abstract and Author Summary

**【Problem】** The title and the Results/Discussion correctly reframe the axis as "nerve-injury-associated, not CPSP-specific," but the Abstract and Author Summary still lead and land as a CPSP study, creating a consistency gap a careful PLOS ONE editor will flag.

**【Evidence】** Title (manuscript line 1) and Discussion (lines 107, 115) and Methods metadata (line 8) all use "nerve-injury-associated … not a CPSP-specific mechanism." Yet the Abstract opens "Chronic postsurgical pain (CPSP) affects 10–50% of surgical patients, yet druggable targets on the DRG–spinal-cord axis remain undefined" (line 14) with no reframing caveat, and the Author Summary (lines 18–22) repeatedly says "CPSP" / "surgical-incision pain models" and never states the nerve-injury reframing that the body relies on. The reframing caveat only appears in the third paragraph of the Introduction (line 30) and in Discussion.

**【Why it matters】** For PLOS ONE the disease claim in the Abstract must match the body. A reader who stops at the Abstract will take away "this is a CPSP signature," which the non-circular translation test (46.3% vs 47.1%, p = 0.14; line 52, 107) explicitly refutes. This is the exact over-claim Scientific Reports flagged as "not sufficiently valid."

**【Specific fix】** Replace the Abstract opening sentence and add the caveat verbatim:
> "We integrated 12 GEO datasets spanning nerve-injury, tibial-nerve-injury and surgical-incision models in rat, mouse and human to define the transcriptional architecture of the dorsal root ganglion–spinal axis in persistent pain. Because four of the five axis studies are nerve-injury models and only one is an incision model, we frame the axis as a nerve-injury-associated transcriptional response rather than a CPSP-specific mechanism; the incision arm is analysed separately as a translation test."
And in the Author Summary, insert after the first sentence: "We deliberately frame the axis as nerve-injury-associated rather than CPSP-specific, because four of the five studies are nerve-injury models and the single incision model does not recapitulate the signature."

---

## FINDING 2 — The "neuroimmune–metabolic" label over-weights OXPHOS, and the DAM cellular identity is unresolved

**【Problem】** The headline programme is called "neuroimmune–metabolic," but the metabolic (OXPHOS) arm is a fixed-effect-only finding that did not survive random-effects correction, and the "DAM microglial" signal cannot be assigned to microglia specifically from bulk tissue.

**【Evidence】** OXPHOS suppression is reported as upregulated-programme-coordinated but "did not survive random-effects correction (q = 0.31)" (line 42, repeated line 107). The random-effects core shrank to 24.9% of the fixed-effect core (line 40). The DAM microglia set is the Keren-Shaul neurodegeneration signature (ref 22) applied to pooled bulk DRG + spinal tissue; the manuscript states the "cellular locus of the OXPHOS signal … is unresolved" (line 44) but does **not** extend that caveat to the DAM signal. Single-cell only confirmed TFE3 as a cross-dataset *immune* lineage hub, and only 7/35 hubs achieved cross-dataset lineage-consistent localisation (line 70). ATF3 and AXL were ambient-RNA downgraded (line 70). So the DAM gene-set is a bulk inference that cannot distinguish resident microglia from infiltrating monocytes/macrophages — and in peripheral nerve injury the DAM-like programme is in fact driven substantially by recruited macrophages (ref 13, Tansley 2022, which the manuscript itself cites).

**【Why it matters】** Calling it "DAM-like microglial" (line 107, twice) over-specifies the cellular source. Resident microglia vs infiltrating macrophages are therapeutically distinct (the manuscript's own purinergic self-negative, line 78, already gestures at this). The "metabolic" label also implies a robust arm that is in fact heterogeneity-fragile.

**【Specific fix】** (a) In Discussion line 107, replace "a neuroimmune–metabolic programme … coordinated DAM-like microglial and complement activation¹⁵ plus, in the fixed-effect analysis only, OXPHOS suppression" with:
> "a neuroimmune programme (with a fixed-effect-only, heterogeneity-fragile metabolic/OXPHOS component that did not survive random-effects correction, q = 0.31) — coordinated DAM-like neuroimmune and complement activation¹³,¹⁹,²⁰ plus OXPHOS suppression under fixed effects only."
(b) Add one sentence: "The DAM-like gene-set signal is a bulk-tissue inference; because the axis pools DRG and spinal tissue containing both resident microglia and infiltrating monocytes/macrophages, we cannot assign it to resident microglia specifically, and we use 'DAM-like neuroimmune' rather than 'DAM-like microglial' throughout."

---

## FINDING 3 — The sodium-channel direction inversion is under-discussed relative to its clinical consequence

**【Problem】** The down-regulation of SCN9A/SCN10A/SCN11A/SCN8A in nerve injury (and inversion to up in the single incision model) is the most literature-contrary and clinically loaded finding, yet it is hedged with a single citation (Ding 2019, Nav1.6) and omits the entire Nav1.7/Nav1.8 human-genetics and clinical-failure literature; the in-hand single-cell resource was not used to resolve neuronal vs non-neuronal direction.

**【Evidence】** SCN8A is the most significant of the four (meta_Z −4.92, FDR 1.0e-5; line 46, 107, Table 1b) and all four invert to up in the one incision model (Table 1b, lines 239–242). The only cited reconciliation is Ding 2019 (ref 10) on Nav1.6 up-regulation. The manuscript does **not** cite or discuss (i) the large body of work showing Nav1.7/Nav1.8/Nav1.9 are *up*-regulated at the protein/functional level in injured DRG nociceptors, (ii) human SCN9A gain-of-function mutations causing pain (Yang 2004; Cox 2006; Fertleman 2006/2007), or (iii) the repeated clinical failure of selective Nav1.7/Nav1.8 blockers — despite Reference 25 (McDonnell 2018, the PF-05089771 Nav1.7 phase-II failure) being in the reference list yet never cited (see F7). The DRG single-cell dataset GSE216039 (line 68) is already analysed for hub localisation but the SCN per-celltype direction is never reported, leaving the central question — do neurons or non-neuronal cells drive the bulk down-signal? — unanswered.

**【Why it matters】** Bulk DRG contains many cell types; a bulk SCN down-signal can reflect neuronal loss/atrophy, non-neuronal down-regulation, or transcript–protein decoupling rather than a negation of the well-established neuronal Nav up-regulation that motivates most analgesic sodium-channel programmes. Without this reconciliation the reader is left with an apparent contradiction that the manuscript only partially defuses. This is precisely the kind of claim that draws "not valid" desk-rejections.

**【Specific fix】** Insert after the Ding 2019 sentence (line 46) the following paragraph:
> "This bulk down-regulation of SCN9A/SCN10A/SCN11A/SCN8A contrasts with the extensive literature showing Nav1.7/Nav1.8/Nav1.9 up-regulation at the protein and functional level in injured DRG nociceptors, with human SCN9A gain-of-function mutations that cause pain, and with the repeated clinical failure of selective Nav1.7 (e.g., PF-05089771; McDonnell 2018, ref 25) and Nav1.8 (e.g., vixotrigine) blockers in neuropathic-pain trials. We therefore interpret the present direction as a bulk-tissue average that likely reflects non-neuronal compartments, neuronal loss/atrophy, or transcript–protein decoupling, rather than a negation of neuronal Nav up-regulation; we did not resolve the per-cell-type direction in the available DRG single-cell resource (GSE216039), which is a limitation."

---

## FINDING 4 — The "honest null" target list mixes biologically irrelevant proteins with real candidates on equal footing

**【Problem】** Four of the ten docked targets (SLC2A1, GALNS, VASH2, ITPKC) have no established analgesic rationale and were included only because a ligand-anchored holo PDB structure existed; presenting them in a single uniform table risks readers over-reading them as candidate pain targets.

**【Evidence】** Table 3a (lines 86–97) and P6_target_plausibility.json both tag SLC2A1 ("glucose transporter (no analgesic link)"), GALNS ("lysosomal sulfatase (no analgesic link)"), VASH2 ("vasohibin (no analgesic link)"), ITPKC ("inositol kinase (no analgesic link)") — i.e., the manuscript itself states they have no analgesic link. Yet the Results state "Target-specific biological plausibility is assessed uniformly across all 10 tractable targets" (line 84) and the Discussion names MAPK14/AXL/TFE3 as the strongest priors (line 113) only in prose, not in the table structure. The hub→target eligibility rule is explicitly "≥1 ligand-anchored holo PDB structure" (line 101), confirming these were included for tractability, not biology.

**【Why it matters】** A uniform 10-target table is honest about each target's "no analgesic link" text but still implies co-equality. A scanning reader will treat GALNS (Morquio A enzyme) or VASH2 (angiogenesis vasohibin) as if they were analgesic candidates, which dilutes the methodological message and invites reviewer scepticism about target selection.

**【Specific fix】** Split Table 3a into two sub-tables with an explicit header:
> "Ten tractable targets: six biologically plausible candidates (ADRA2A, MAPK14, AXL, TNIK, ACVR1, SERPINE1; SLC2A1 additionally has an emerging DRG-metabolic rationale, ref 16) and four tractability/negative-control targets with no established analgesic rationale (GALNS, VASH2, ITPKC — included solely because a ligand-anchored holo PDB structure existed, not as a priori candidates). The honest-null conclusion applies to all ten; only the six biologically plausible targets should be read as hypothesis generators."
Retitle the surrounding section from "Target-specific biological plausibility is assessed uniformly across all 10 tractable targets" to "Ten tractable targets: six plausible candidates and four tractability negative controls."

---

## FINDING 5 — CDHR5 is presented as a co-equal candidate despite being the most likely technical/biological false-positive

**【Problem】** CDHR5 (an intestinal epithelial cadherin with no DRG/pain role) reached full three-method consensus and is the single most bootstrap-stable dock-eligible hub, yet it is listed alongside established markers as a "candidate," under-weighting how suspicious its biology is.

**【Evidence】** CDHR5 is one of the five full three-method-consensus hubs (line 56: "SPRR1A, ATF3, TFE3, CDHR5, GALNS") and is "consistently up-regulated in all four bulk contrasts (log₂FC +0.07 to +2.62, the largest contribution coming from GSE278227)" (line 76). The bootstrap audit states "The single most stable dock-eligible hub was CDHR5 (15.5%)" (line 60). P3_hub_genes.csv confirms CDHR5 n_methods = 3, lasso_freq 0.79. So a protein with no neuronal/DRG biology is both consensus-strong and the most stable hub — the classic signature of a batch/technical or cell-type-contamination artifact, not a discovery.

**【Why it matters】** Listing CDHR5 as a peer of ATF3 and SPRR1A implies equivalence. If it is (as is likely) an artifact, retaining it as a "candidate" in the 35-hub set and as the most stable dock-eligible hub undermines confidence in the whole hub list and in the docking target set that is "determined by structural tractability, not by hub rank" (line 101) — because structural tractability here inherits CDHR5.

**【Specific fix】** Replace the CDHR5 clause (line 76) with:
> "CDHR5 is the strongest single illustration: it reached full three-method consensus and is consistently up-regulated in all four bulk contrasts (log₂FC +0.07 to +2.62, the largest contribution from GSE278227), so it is not a single-study artefact; however, because its annotated biology is intestinal-epithelial with no DRG or pain role, and because it is simultaneously the single most bootstrap-stable dock-eligible hub (15.5%) despite this biological distance, we flag it as the top technical/biological watch-list outlier rather than as a co-equal candidate, and recommend it be excluded from the candidate hub shortlist and from the dock-eligible set pending orthogonal confirmation."

---

## FINDING 6 — Translational roadmap over-states blood accessibility and under-bounds the rodent→human gap

**【Problem】** The "blood-accessible hubs" list includes nuclear transcription factors and microglial markers that are weak or non-blood biomarkers, and the rodent DRG–spinal signature is presented as if plasma qPCR/ELISA validation is a natural next step without enough emphasis that blood is a low-yield surrogate.

**【Evidence】** Line 115 lists "blood-accessible hubs (e.g., NPY, VIP, SERPINE1, AXL, MAPK14, TFE3)" as "addressable in the planned plasma qPCR/ELISA work." TFE3 is a nuclear transcription factor (measured only as PBMC mRNA, not a soluble/secreted biomarker); AXL is microglial/immune and likewise PBMC-mRNA only. The human miRNA layer (line 64) was already negative (p = 0.51) — itself evidence that blood proxies of this axis are weak. The manuscript does state "the 35 hubs constitute a rodent axis signature that must be confirmed in human tissue before any therapeutic claim" (line 115), which is correct, but the enthusiasm for plasma qPCR/ELISA is not balanced by stating that CSF (still indirect) or human DRG/neuroma tissue is the only mechanism-concordant validation.

**【Why it matters】** PLOS ONE reviewers will ask whether the proposed validation is even capable of confirming the axis. Presenting TFE3 as "blood-accessible" over-states feasibility and could be read as over-claiming the translational path.

**【Specific fix】** Replace the hub-accessibility clause (line 115) with:
> "only hubs measurable as mRNA in peripheral-blood PBMC or as soluble/secreted factors are addressable in the planned qPCR/ELISA work; among the 35, secreted/soluble candidates (e.g., NPY and VIP as neuropeptides, SERPINE1/PAI-1 as a secreted serpin) are the most blood-appropriate, whereas nuclear transcription factors such as TFE3 and microglial markers such as AXL are at best PBMC-mRNA measurable and are weak blood biomarkers. Cerebrospinal fluid, and where surgically available human DRG/neuroma or scar-nerve tissue, remain the only mechanism-concordant validation and should be the primary validation target; plasma is a low-yield surrogate whose limits are already illustrated by the negative human miRNA layer (p = 0.51)."

---

## FINDING 7 (MANDATORY MUST-CITE / MIS-CITATION) — Reference 25 is uncited; Nav1.7/Nav1.8 and docking-confound literatures omitted

**【Problem】** Reference 25 (McDonnell 2018, the PF-05089771 Nav1.7 phase-II failure) is present in the reference list but never cited in the body — a floating reference that violates PLOS ONE's cite-all / cite-none rule — and the broader Nav1.7/Nav1.8 human-genetics and clinical-failure literature, plus the "repurposing panacea"/docking-confound critique that this study's own result exemplifies, are entirely absent.

**【Evidence】** I grepped the manuscript body for "[25]" / "²⁵" / "McDonnell" and found the citation marker only on the reference-list line (line 187); no inline use exists. The sodium-channel and repurposing discussions (lines 46, 80–113) cite only Ding 2019 (ref 10), Gan 2023 & Pham 2025 (refs 8–9, which are tool/method papers, not critiques), and Divito 2026 (ref 14, suzetrigine). I verified externally that (a) McDonnell 2018 (Pain 159:1465–1476) is real and reports PF-05089771 failure in painful DPN; (b) vixotrigine also failed its phase-II small-fibre-neuropathy primary endpoint (Faber/CONVEY, Lancet EClinicalMedicine 2023); (c) Divito 2026 (CCJM 93(2):94–98, PMID 41629062, doi 10.3949/ccjm.93a.25087) is real and correctly attributed, as is Nie 2025 (Sci Adv 11(31):eadu4270, PMID 40749060) — both correctly used. The omission is therefore substantive, not a factual error in the listed items.

**【Why it matters】** A sodium-channel pain paper that finds Nav channels down-regulated and then runs a docking screen must engage (i) why neuronal Nav up-regulation is the dominant literature and (ii) why Nav1.7/Nav1.8 blockers have failed clinically — otherwise the sodium-channel and repurposing sections read as disconnected from the field. The docking MW-confound result (ADRA2A full-library AUC 0.532 vs Tier-1 0.618; lines 99, 255–256) is a direct empirical demonstration of the "repurposing panacea" critique, yet that critique literature is not cited, weakening the paper's positioning.

**【Specific fix】**
1. Cite ref 25 where it belongs — in the F3-added paragraph above, append "(McDonnell 2018, ref 25)" after "PF-05089771." This removes the floating reference.
2. Add to the sodium-channel discussion the human-genetics/clinical-failure context, e.g.: "Selective Nav1.7/Nav1.8 blockers have repeatedly stalled in Phase II despite strong genetic validation (e.g., Yang et al. 2004 Nat Genet; Cox et al. 2006 J Clin Invest; Fertleman et al. 2006 Nat Neurosci; Eagles et al. 2022 Br J Pharmacol; Faber et al. 2023 Lancet EClinicalMedicine on vixotrigine)."
3. In the repurposing Discussion (line 111, "corrects the 'repurposing panacea' narrative"), add a real critique citation, e.g.: "This corrects the 'repurposing panacea' narrative (Pushpakom et al. 2019 Nat Rev Drug Discov; and the well-documented physicochemical/MW confounding of structure-based enrichment, e.g., the virtual-screening false-positive literature such as Irwin & Shoichet 2016, and contemporary docking-reproducibility critiques)."
4. Anchor the DAM/complement-in-pain claim (line 107, currently ref 15 Schafer 2012, a *developmental* microglia paper) primarily on refs 13/19/20 (Tansley 2022; Inoue 2018; Coull 2005), keeping ref 15 as developmental context only.

---

## FINDING 8 (minor) — The Discussion sodium-channel paragraph is incomplete as written

**【Problem】** The Discussion sentence "Because the channels we find down-regulated are the same ones targeted by conventiona…" (line 107) is cut off, and the manuscript never completes the translational paradox — that the channels conventionally up-regulated/targeted in pain appear down-regulated here.

**【Evidence】** Line 107 ends mid-word at "conventiona…"; the intended completion (likely "...conventional analgesic sodium-channel programmes") is missing, so the paragraph's clinical punchline is absent.

**【Why it matters】** An unfinished sentence in the Discussion is a presentation defect that undermines the careful hedging elsewhere and leaves the most important clinical reconciliation dangling.

**【Specific fix】** Complete the sentence:
> "Because the channels we find down-regulated in bulk nerve-injury tissue are the same Nav isoforms (Nav1.6/1.7/1.8/1.9) that conventional analgesic programmes target and that are typically up-regulated at the neuronal protein level, the present bulk direction should not be interpreted as evidence against those targets; it is a tissue-composition and model-dependent average that the single-cell and incision analyses (above) show is non-predictive of the postsurgical setting."

---

## § Stands up — things I suspected were wrong but found correct

1. **The non-circular translation test is genuine, not a fig leaf.** I expected the "incision does not predict nerve injury" claim to be a circular artefact. It is not: the authors rebuilt the signature on the five nerve-injury contrasts only and used incision once as held-out test, getting 46.3% vs a 47.1% background (difference −0.9 pp, p = 0.14; line 52, 107). The circular 69.5% number is explicitly disowned (line 50). This is exactly the discipline the field lacks.

2. **The honest docking null is real and well-controlled.** I expected the "null" to be softened somewhere. It is not: reverse positive controls pass as *method validation only* (AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779; P6_reverse_control.csv), ADRA2A's Tier-1 signal collapses from AUC 0.618 to 0.532 (p = 0.118) at full-library scale (lines 99, 255–256), known analgesics are not enriched (0/64 in Top-20), and no target clears *both* the raw/full-library and the size-independent filters. The composite Top-20 is explicitly framed as knowledge-informed retrieval, not docking evidence (line 99). Internally consistent.

3. **The fragility of the core is led with, not buried.** The bulk-only sensitivity showing 1,732/4,055 = 42.7% overlap (57.3% of the primary core is translatome-dependent; line 44) is presented as "the single most important fragility of the signature, and one we therefore lead with" (line 44). Genuine epistemic honesty.

4. **OXPHOS is correctly NOT claimed under random effects.** Despite being in the programme name, the authors report q = 0.31 for OXPHOS under the random-effects vector and scope it to fixed-effect only (lines 42, 107). Appropriate restraint.

5. **Hub outliers are flagged, not concealed.** ANKRD1, FLNC, CRISP3, MEGF11 are explicitly named as having no DRG/pain role (line 76); P3_hub_genes.csv confirms REG3B, ANKRD1, MEGF11 are out of the meta core. REG3B is correctly demoted to an external hypothesis with model-mismatched (CRPS-I, not CPSP) evidence (lines 76, 109), and I verified Nie 2025 (Sci Adv 11(31):eadu4270) is real and that its CPIP model is indeed a CRPS-I ischemia-reperfusion model — so the "model-mismatched" caveat is accurate.

6. **The bootstrap instability is openly reported.** "0/35 hubs reached ≥0.9 resampling stability" and "λ.1se = 1 gene" (line 60) are stated plainly. The target set is then justified by structural tractability, not hub stability (line 101) — a coherent logical chain.

7. **References 14 (Divito 2026) and 11 (Nie 2025) are real and correctly attributed** — I verified both against the primary sources (CCJM 93(2):94–98, PMID 41629062; Sci Adv 11(31):eadu4270, PMID 40749060). The suzetrigine citation is correctly used as an example of a nonopioid analgesic.

---

## § Questions for the authors (I do not guess the answers)

1. In GSE216039 (DRG scRNA), what is the per-celltype direction of SCN9A/SCN10A/SCN11A/SCN8A? Was neuronal vs non-neuronal direction tested, and if so, what did it show? This is the single most important missing analysis for the sodium-channel claim.
2. TFE3 is a full three-method-consensus hub and is named (line 113) among the "strongest prior biological rationale" targets, yet it was not docked ("no appropriately ligand-anchored cavity," line 101). Is TFE3 biologically a tractable analgesic target at all, or is its inclusion in the "strongest priors" list itself questionable?
3. For CDHR5 — do you have any hypothesis for why an intestinal epithelial cadherin is up in all four bulk contrasts (largest effect from GSE278227)? Could it reflect a cell-type composition difference, a batch effect, or a genuine but unexpected DRG signal?
4. The incision model GSE267799 harvest day is "not stated in the deposited metadata" (line 133). What day does the source publication state, if any? This bounds the CPSP-adjacency claim.
5. Is a CSF sample, or human DRG/neuroma/scar-nerve tissue, actually obtainable for the planned qPCR/ELISA validation, or is the plasma-PBMC plan the only feasible one? This determines whether the validation is mechanism-concordant or a surrogate.

---

## § What I actually checked

**Files read (this round):**
- `reports/MVP_ScientificReports_submission.md` — full manuscript (263 lines; noted truncation of the Discussion sodium-channel sentence at line 107 "conventiona…" and the Results docking sentence at line 99 "structure-b…", which are display artifacts of long lines, not missing content I needed).
- `results/tables/P3_hub_genes.csv` — confirmed 35 hubs; 5 with n_methods = 3 (SPRR1A, ATF3, TFE3, CDHR5, GALNS); in_meta_core = False for REG3B, ANKRD1, MEGF11; CDHR5 lasso_freq 0.79.
- `results/tables/P6_target_plausibility.json` — confirmed 10 targets with meta_Z/meta_FDR/consistency/n_holo_PDB matching Table 3a; all in_meta_core = True; SLC2A1/GALNS/VASH2/ITPKC tagged "no analgesic link."
- `results/tables/P6_reverse_control.csv` — confirmed reverse-control AUCs: AXL 0.8798, TNIK 0.8242, ACVR1 0.7970, MAPK14 0.7785, SLC2A1 0.9142 (single known pair), ADRA2A 0.5325 (reliable = False); GALNS/ITPKC/SERPINE1/VASH2 have 0 known pairs.

**Numbers recomputed / directly read and cited:**
- OXPHOS q = 0.31 under random effects (manuscript lines 42, 107).
- SCN8A most significant: meta_Z −4.92, FDR 1.0e-5 (lines 46, 107; Table 1b lines 239–242).
- Non-circular translation: 46.3% vs 47.1% background, −0.9 pp, p = 0.14 (lines 52, 107).
- Bulk-only core 1,981; overlap 1,732/4,055 = 42.7%; 57.3% translatome-dependent (line 44).
- Random-effects core = 1,008 = 24.9% of fixed-effect core (line 40).
- 4/10 targets retain random-effects significance: SLC2A1 (0.0000), TNIK (0.021), GALNS (0.025), ADRA2A (0.039) (line 84; Table 3a FDR_RE column).
- ADRA2A full-library AUC 0.532, p = 0.118; MW-adjusted 0.578, ΔAUC p ≈ 0.0005 (lines 99, 255–256).
- Human miRNA set-level p = 0.51 (line 64).
- ATF3 positive control meta_Z 10.53, FDR 1.0e-21, consistency 1.00 (line 38).

**Reference verification (external):**
- Ref 14 Divito 2026 — verified real: Cleveland Clinic Journal of Medicine 93(2):94–98, doi 10.3949/ccjm.93a.25087, PMID 41629062. Correctly attributed.
- Ref 11 Nie 2025 — verified real: Science Advances 11(31):eadu4270, doi 10.1126/sciadv.adu4270, PMID 40749060. Correctly attributed; CPIP is a CRPS-I ischemia-reperfusion rat model, so the manuscript's "model-mismatched (CRPS-I, not CPSP)" caveat is accurate.
- Ref 25 McDonnell 2018 — verified real (Pain 159:1465–1476, PF-05089771 failed phase-II DPN) but confirmed **uncited** in the manuscript body (no inline [25] marker found).
- Nav1.7/Nav1.8 clinical failures — confirmed via literature: PF-05089771 (McDonnell 2018) and vixotrigine (Faber/CONVEY, Lancet EClinicalMedicine 2023) both failed phase-II pain endpoints; this literature is absent from the manuscript.

**Discrepancy stated:** Reference 25 is listed but never cited inline (floating reference). The sodium-channel and repurposing discussions cite only Ding 2019, the Gan/Pham tool papers, and Divito 2026 — none of the Nav1.7/Nav1.8 human-genetics, clinical-failure, or docking-confound-critique literatures that this study's own results most directly engage.

**Independence discipline observed:** I did not open any REVIEW_*.md, RESPONSE_*.md, REVISION_*.md, or files under reviews/round2_2026-09-20, reviews/round4_2026-09-20, reviews/round5_2026-09-21; I did not read PROJECT_PLAN.md, SUBMISSION_MANIFEST.md, GITHUB_DEPOSIT_SOP.md, or author_verification_statement.md, and did not read any other reviewer's file in this round. All judgements above derive solely from the manuscript text, the three named data tables, and the external reference checks reported here.
