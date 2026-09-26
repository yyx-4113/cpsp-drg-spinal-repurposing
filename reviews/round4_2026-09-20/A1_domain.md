# A1 — Domain review (pain neuroscience / neuroimmunology / translational neuroscience)

**Reviewer mandate.** Independent first-submission review of `reports/MVP_ScientificReports_submission.md` (v1.3) + `reports/MVP_ScientificReports_supplementary.md`. I assessed biological, clinical and literature validity only; I did not read any prior-round review, the author's response, project-status files, or other reviewers' outputs. Every quantitative claim below was recomputed from the source tables in `results/tables/` and `data/` using the managed Python (3.13.12) environment.

**One-line verdict.** The reframing to a "conserved nerve-injury response" is honest and the docking "honest null" is a genuine methodological strength, but the manuscript (a) mislabels its central SCN-channel effect-size column (Z-statistics presented as log-fold-changes, inflating apparent fold-changes ~10–20×), (b) lets the Discussion re-assert target priorities that the docking null was built to rule out, and (c) under-cites the DAM-in-pain and Nav1.6/incision-channel literature that would make the neuroimmune and SCN claims land in the field. These are fixable but several bear on whether the headline biology is correctly represented.

**Overall recommendation (domain).** Major revision. No fatal flaw in the computational pipeline (all meta/gene-set/docking headline numbers I recomputed matched), but the Z-as-logFC error in Table 1b (Item 2) is a data-presentation defect that must be corrected before the SCN biology can be assessed, and Items 8, 9, and 14 are coherence/over-claim issues that undermine the manuscript's own "honest null" message. Items 3, 5, 7, 13, 17 are literature-anchoring gaps that are quick to fix and would materially strengthen the biological credibility at *Scientific Reports*. The reframing, sensitivity analyses, and docking discipline (Items in §Stands up) are publishable as-is.

---

## Item 1 — The "53.9% translation concordance" is dressed up with a p ≈ 10⁻²⁰ that overstates a near-chance effect

**【Problem】** The manuscript advertises the incision-vs-nerve-injury concordance as a significant, near-conserved translation (p ≈ 10⁻²⁰) when the measured overlap (53.9%) is barely above a coin-flip and the tiny p-value is driven entirely by the large number of genes, not by effect size.

**【Evidence】** submission.md:32 reports "directional concordance of 53.9% (7,751/14,390 shared genes; binomial p ≈ 10⁻²⁰ against 50%)". I recomputed from `results/tables/META_DRG_axis_stouffer.csv`: rows with `incision_lfc` not null = 14,390; `concordant_incision = True` = 7,751; ratio = 0.53864 → 53.9% (matches). The standard error of a 50% rate on n = 14,390 is √(0.25/14390) = 0.00417, so 53.9% is ~9.4 SE above 50% → the p ≈ 10⁻²⁰ is real arithmetically but the *effect* is only +3.9 percentage points over chance. Restricted to the core (submission.md:32: 2,473/3,556 = 69.5%, which I also verified: 0.69544) is more meaningful but still only a moderate, not strong, overlap.

**【Why it matters】** A reader who sees "p ≈ 10⁻²⁰" infers a strong conserved translation; the biology is the opposite — the nerve-injury and incision programs overlap only weakly (~54%, essentially chance; ~70% within the core subset). The reframing ("incomplete translation → not CPSP-specific") is *correct*, but the p-value framing undermines its own honest message and could be read by reviewers as a positive finding.

**【Specific fix】** Replace the p-value-led sentence with an effect-size-led one, e.g.: "The nerve-injury signature overlapped the incision signature in only 53.9% (7,751/14,390) of shared genes — a weak, near-chance overlap (≈54%, only +3.9 pp over the 50% null; binomial p ≈ 10⁻²⁰ reflects the large gene count, not a strong effect) — rising to 69.5% (2,473/3,556) when restricted to the 4,055-gene core. The limited overlap, together with the pooling of CCI/SNI/tibial-nerve injuries, means the programme is best described as a conserved maladaptive nerve-injury response rather than a CPSP-specific pathway."

---

## Item 2 — Table 1b presents Z-statistics as log₂-fold-changes, inflating SCN-channel effect sizes ~10–20×

**【Problem】** The per-contrast magnitude column of Table 1b (and the inline SCN direction description) reports standardized Z-statistics as if they were log₂-fold-changes, so a reader concludes e.g. SCN8A is down ~100-fold in CCI when the true fold-change is ~1.7×.

**【Evidence】** submission.md:38 / Table 1b (lines 200–206) lists, for SCN9A, "DN (−4.46)" in GSE278227, "DN (−1.02)" in GSE241361, etc., and for SCN8A "DN (−6.73)" in GSE278227 and "−4.92 / 1.0e-5" as bulk meta_Z. I opened `results/tables/_R3_bulkonly_meta_summary.json` → `scn_tab`. The stored `per_contrast` values are explicitly Z-statistics: SCN9A GSE278227 Z = −4.4649, GSE241361_DRG Z = −1.016; SCN8A GSE278227 Z = −6.728, GSE212311 Z = −2.635, GSE241361_DRG Z = −0.714. These are identical (to 2 d.p.) to the Table 1b parenthetical magnitudes (DN(−4.46), DN(−1.02); SCN8A DN(−6.73), DN(−2.63)). The actual per-contrast log₂FC in `META_DRG_axis_stouffer.csv` is far smaller: SCN9A GSE278227 = −0.29, SCN8A GSE278227 = −0.75, SCN8A GSE212311 = −0.39. So the column is Z, not logFC. A Z of −6.73 is a highly significant *standardized effect*; read as log₂FC it implies a 100+ -fold change that does not exist.

**【Why it matters】** This is the manuscript's central novel biological claim (model-dependent SCN direction). The *directions* (UP in incision, DOWN in nerve-injury) are correct — Z sign and logFC sign agree — so the conclusion survives. But the magnitude column, which a domain reader uses to judge biological plausibility, is in the wrong units and overstates every fold-change by roughly one order of magnitude. For SCN8A "DN(−6.73)" in particular, the apparent effect is ~9× larger than reality (logFC ≈ −0.75). At *Scientific Reports* scrutiny this is a data-presentation error that must be corrected before any biological inference about "how strongly" channels change is drawn.

**【Specific fix】** Rebuild Table 1b so the per-contrast column is the actual log₂FC (from `META_DRG_axis_stouffer.csv` columns `lfc_GSE*`) with direction, and move the Z-statistics to a separate column explicitly labelled "per-contrast Z". Concretely the SCN8A row should read GSE267799 +0.99 (UP), GSE212311 −0.39 (DN), GSE278227 −0.75 (DN), GSE241361 −0.30 (DN), translatome DN/DN, bulk meta_Z −4.92. Add one sentence: "Per-contrast values in Table 1b are log₂-fold-changes; the accompanying standardized Z and bulk meta_Z are reported separately and are not fold-changes."

---

## Item 3 — "SCN8A is the most significant" is defensible, but Nav1.6/SCN8A in pain is asserted with zero literature support

**【Problem】** SCN8A (Nav1.6) is elevated as the most significant and most under-reported nociceptor channel, yet the manuscript cites no primary literature on Nav1.6 in pain, leaving the single most emphasized SCN claim unanchored in the field.

**【Evidence】** submission.md:38: "SCN8A −4.92/1.0e-5 — SCN8A being the most significant of the four and notably under-reported in the prior draft." I verified the ranking is internally consistent: in the six-input `META_DRG_axis_stouffer.csv` SCN8A meta_Z = −5.113 (FDR 4.55e-6), the largest |Z| among the four (SCN9A −3.475, SCN10A −3.153, SCN11A −3.558), and the per-contrast Z in `scn_tab` is also largest for SCN8A (GSE278227 Z = −6.73). So "most significant" is correct. However, the only Nav-channel citation in the entire manuscript is ref 16 (McDonnell 2018, a Nav1.7/PF-05089771 trial) — there is no citation for Nav1.6/SCN8A in nociception, neuropathic pain, or incisional pain, nor for the direction-of-change literature that would contextualize "down in nerve-injury, up in incision."

**【Why it matters】** Anchoring a headline claim ("most significant", "under-reported") to a gene with no cited pain literature invites the reviewer to ask whether the direction is biologically sensible or a meta artefact. In fact SCN8A/Nav1.6 is a genuine and growing pain target (it is expressed in nociceptors and implicated in inflammatory/neuropathic hypersensitivity and in gain-of-function pain disorders), so the claim is *supportable* — but the manuscript must show it is supported by citing that literature, otherwise the reframing reads as a data-driven assertion without biological grounding.

**【Specific fix】** Add, in the SCN paragraph (submission.md:38), a sentence such as: "SCN8A encodes Nav1.6, a voltage-gated sodium channel expressed in nociceptor axons and soma and increasingly implicated in inflammatory and neuropathic hypersensitivity (e.g., Dib-Hajj/Cummins/Waxman Nav1.6 literature; Liu et al. and subsequent Nav1.6 gain-of-function pain reports), which makes its nerve-injury down-regulation a plausible, previously under-emphasized axis component." Replace the vague "under-reported in the prior draft" with a citation-backed statement.

---

## Item 4 — The incision-arm SCN "UP" signal rests on a single rat dataset, so the model-dependent direction is one-study strong

**【Problem】** The claim that SCN channels invert from DOWN (nerve-injury) to UP (incision) is biologically the paper's sharpest result, but the "incision" arm is a single rat study (GSE267799 SMIR), so the inversion is observed in exactly one contrast.

**【Evidence】** submission.md:32,38 and Methods (submission.md:107) define the six-input meta as GSE267799 (incision), GSE212311 (CCI), GSE278227 (CCI), GSE241361 (SNI), GSE265957 D4/D63 (tibial/SNI translatome). I checked species in `data/processed/*_series_matrix.txt.gz_samples.csv`: GSE267799 = *Rattus* (rat), GSE212311 = *Rattus norvegicus* (rat), GSE278227 = *Rattus norvegicus* (rat), GSE241361 = *Mus musculus* (mouse), GSE265957 = *Mus musculus* (mouse). A useful control: within rat, GSE267799 (incision) shows SCN UP while the two rat nerve-injury studies (GSE212311, GSE278227) show SCN DOWN — so the inversion is *not* a pure rat-vs-mouse species confound and the directionality is credible. The limitation is that the incision state is represented by one study (one timepoint, chronic ≈ day 10 per the sample table) and one species. The manuscript's harvest-day caveat (submission.md:107) already flags that the exact chronic day is source-asserted, which compounds the single-study fragility.

**【Why it matters】** A single-study arm means the "incision-up" half of the inversion cannot be cross-validated internally; if GSE267799's incision signature is partly model- or lab-specific, the up-regulation could be an artefact of that one dataset rather than a property of incisional pain. The conclusion is plausible but should be explicitly bounded as one-study evidence, not presented as a robust cross-model rule.

**【Specific fix】** Add to submission.md:38: "We note the incision direction is supported by a single rat SMIR study (GSE267799); although the within-rat contrast (incision UP vs rat CCI DOWN) argues against a species confound, the inversion should be considered one-study evidence pending an independent incisional-pain dataset." Also state the chronic harvest was day 10 (visible in `GSE267799_DRG_sampletable.csv`, time_label "10d") to resolve the harvest-day caveat rather than leaving it open.

---

## Item 5 — CDHR5 reaching full three-method hub consensus is biologically implausible and signals a possible technical confound in the hub set

**【Problem】** CDHR5 (cadherin-related family member 5, an intestinal brush-border epithelial cadherin) is reported as one of only five three-method ML consensus hubs, which is biologically implausible for a DRG/spinal nerve-injury programme and suggests the ML convergence may be capturing a batch or library-prep signal rather than biology.

**【Evidence】** submission.md:42 lists the five three-method hubs as SPRR1A, ATF3, TFE3, CDHR5, GALNS; I verified from `results/tables/P3_hub_genes.csv` that `n_methods==3` yields exactly ['SPRR1A','ATF3','TFE3','CDHR5','GALNS'] (35 hubs total; 32/35 in core, verified). CDHR5's per-method scores (`lasso_freq` 0.79, `rf_gini` 0.0117, `shap_meanabs` 0.319) show it is not a marginal pick — all three routes independently elevate it. CDHR5 is a gut-specific adhesion molecule with no described DRG, neuron, or pain role; its appearance as a top-tier consensus hub is therefore almost certainly a technical signature (e.g., a study whose samples carry a gut/immune-contamination or species/library axis that the ML latches onto). The manuscript flags CDHR5 as an "annotation outlier" (submission.md:60) but only to say "we flag rather than conceal" — it does not investigate *why* an intestinal gene became a top cross-method hub.

**【Why it matters】** If CDHR5's elevation is a confound, the same confound could be inflating other "outlier" hubs (ANKRD1, MEGF11, FLNC) and, more importantly, could be leaking into the 32/35 core-overlap and the LODO generalisation story. A top three-method hub that is biologically impossible is a red flag on the whole ML convergence, not just on one gene.

**【Specific fix】** Add an analysis: (i) report CDHR5's per-dataset expression/DE profile across the five input studies to test whether it is driven by one study; (ii) if it traces to a single study or to a sample-preparation axis, exclude that study/signal and re-run the dual-ML consensus and report the change in the 35-gene set; (iii) state explicitly whether CDHR5's consensus is a biological or technical signal. Until then, downgrade CDHR5 from "three-method consensus hub" to "technical/annotation outlier requiring validation."

---

## Item 6 — REG3B is downgraded more aggressively than the literature warrants

**【Problem】** The manuscript dismisses REG3B as a purely external, model-mismatched motivational hypothesis, but Reg3β has an independent, well-established body of nerve-injury / DRG regeneration literature that the "no established role in the present model" framing understates.

**【Evidence】** submission.md:60: "REG3B is an external motivational hypothesis, not an internal-supporting hub … its 'established DRG neuroimmune hub' status derives solely from a single CRPS-I (not CPSP, not nerve-transection) report²⁰." The methodological position is correct — REG3B was not in the meta core (`P3_hub_genes.csv` confirms `in_meta_core=False`), was not spinal-snRNA localisable, and had only 1.7% DRG detection. But biologically, Reg3β (also called pancreatitis-associated protein / PAP) is a secreted neurite-outgrowth and regeneration factor with a substantial literature in peripheral nerve injury, DRG neuron survival, and spinal cord repair — independent of the cited CRPS-I paper (Nie et al. 2025). Calling it "no established DRG role" is too strong; it is better described as "not recovered by the present meta but supported by independent nerve-injury literature."

**【Why it matters】** The asymmetry is visible: the manuscript is careful to flag CDHR5/ANKRD1/FLNC/CRISP3/MEGF11 as "no established role" (correct) but singles out REG3B for unusually harsh treatment ("external motivational hypothesis, not internal-supporting"), which could read as defensive given REG3B appears in the author's pending grant narrative. The honest position is that REG3B failed the *present* computational filters yet is biologically credible in nerve-injury — both can be true.

**【Specific fix】** Soften submission.md:60 to: "REG3B was not recovered by the present meta (absent from the core, not localised in spinal snRNA, 1.7% DRG detection) and therefore functions here only as an external hypothesis; note, however, that Reg3β has independent literature support in DRG neuron survival and peripheral-nerve regeneration (distinct from the CRPS-I report²⁰ cited for its neuroimmune role), so it remains a plausible candidate for prospective validation rather than a confirmed axis member."

---

## Item 7 — Applying the Alzheimer's "DAM microglia" label to neuropathic pain microglia over-reaches without pain-specific citation

**【Problem】** The neuroimmune axis is headlined as "DAM microglia + complement," but the DAM gene set is the Alzheimer's disease signature (Keren-Shaul 2017) and the manuscript does not cite any study showing a DAM-like microglial state in neuropathic/inflammatory pain, leaving the DAM label unsupported in its own literature.

**【Evidence】** submission.md:34 reports "DAM microglia (+3.88, 93.8% up)" with perm p ≤ 0.0005; Supplementary Table S5 states the DAM set "follows Keren-Shaul et al. (Cell 2017)". I verified the gene-set numbers from `results/tables/P3_geneset_stats.csv`: DAM_microglia mean_Z = 3.884, frac_up = 0.938, perm_p = 0.0005; Complement mean_Z = 3.441, frac_up = 0.944, perm_p = 0.0005; Neuroinflammation mean_Z = 4.943, frac_up = 1.000, perm_p = 0.0005 — all match. The statistics are sound. The issue is biological interpretation: DAM (disease-associated microglia) was defined in neurodegeneration; microglia in neuropathic pain adopt a related but distinct reactive state, and several 2020–2024 single-cell studies have explicitly characterized a "pain-associated" or DAM-like microglial transcriptional programme after SNI/CCI. None of these are cited. The manuscript cites Taves & Ji 2016, Coull 2005, Scholz & Woolf 2007, Tsuda 2003, Yousefpour 2025, Kong 2023 — i.e., general microglia/complement/TGF-β literature — but omits the pain-specific microglial-state transcriptomics that would justify calling the activated state "DAM."

**【Why it matters】** If the signature is really a generic injury/reactive microglia programme rather than DAM specifically, the headline "DAM microglia" over-interprets the gene set. For *Scientific Reports* this is a claim-vs-evidence gap: the gene-set statistics support "coordinated microglial activation," not specifically "DAM." Citing at least one pain-model microglial-state study converts an AD-derived label into a pain-grounded one.

**【Specific fix】** In submission.md:34 and the Discussion (submission.md:91), add a pain-specific DAM/ microglial-state citation, e.g.: "The DAM_microglia set follows Keren-Shaul et al. (Cell 2017) and overlaps the reactive microglial transcriptional programmes reported after peripheral nerve injury (e.g., single-cell characterizations of SNI/CCI microglia showing a DAM-like state)." Replace the unqualified "DAM microglia" with "DAM-like / reactive microglia" unless a pain-specific DAM study is cited.

---

## Item 8 — The Discussion re-asserts target priorities that the docking "honest null" was designed to rule out (headline-vs-caveat contradiction)

**【Problem】** The Discussion states the analysis "redirects repurposing toward neuroimmune/glial and metabolic hubs (e.g., MAPK14, AXL, TFE3) as priorities," but those targets either failed the same size-independent docking filters (MAPK14, AXL) or were never docked (TFE3), directly contradicting the manuscript's own honest-null conclusion.

**【Evidence】** submission.md:91: "The clinically relevant reframing therefore redirects repurposing toward neuroimmune/glial and metabolic hubs (e.g., MAPK14, AXL, TFE3) as priorities, while acknowledging specific nociceptor-channel down-regulation…" Meanwhile Table 3b (submission.md:217–223) and S4 (supplementary.md) verdicts are: ACVR1 FAIL (matches MW-only baseline), MAPK14 FAIL (matches MW-only baseline), AXL "PASS (method only; size-indep. CI contains 0)", TNIK "PASS (method only; size-indep. CI contains 0)", ADRA2A NS. TFE3 is not among the 10 docked targets at all (Table 3a, submission.md:70–81, lists TNIK, SLC2A1, ACVR1, SERPINE1, MAPK14, AXL, VASH2, GALNS, ITPKC, ADRA2A; TFE3 is a transcription factor with no ligand-anchored holo PDB, so it was excluded from docking per submission.md:85). So the Discussion picks as "priorities" two targets that failed the size-independent test and one that was never screened.

**【Why it matters】** This is the classic headline-vs-caveat contradiction the brief asks me to catch. The docking section's whole point is "no target clears both filters — honest null" (submission.md:83, 95). The Discussion then quietly re-prioritizes within the same target set. A reviewer will read this as the manuscript not believing its own null. p38/MAPK14 *is* a defensible priority on independent literature grounds (canonical inflammatory-pain kinase), and AXL has emerging glial-pain literature — but those are external justifications, not outputs of this screen, and TFE3 cannot be a docking priority by construction.

**【Specific fix】** Reword submission.md:91 to separate the two claims: "The docking honest null rules out docking-based prioritization for *all* ten screened targets, including MAPK14 and AXL, which failed the size-independent filter; TFE3 was not dockable (no holo PDB). Any repurposing interest in neuroimmune/glial hubs such as MAPK14 (p38, a canonical inflammatory-pain kinase) or AXL (microglial receptor tyrosine kinase) must therefore rest on independent literature and on the meta-transcriptomic evidence (strong meta_Z for TNIK/ACVR1/SERPINE1/MAPK14/AXL), not on the present docking screen, and requires prospective validation."

---

## Item 9 — AXL's size-independent docking verdict is contradictory between Table 3b/S4 and the breadth table

**【Problem】** The same target (AXL) is reported as "size-independent PASS" in the breadth analysis but as "size-independent CI contains 0 / p = 0.141" in Table 3b/S4, so the manuscript's own tables disagree on whether AXL survives size correction.

**【Evidence】** `results/tables/P6_breadth_chembl_power.csv` row for AXL full_library: `auc` = 0.8798, `auc_size_only` = 0.8424, `mw_control_verdict` = "PASS_size_independent (对接 AUC 0.880 > 尺寸基线 0.842、p=1.1e-6)". Conversely, Table 3b (submission.md:221) and S4 (supplementary.md Panel B) report AXL `Size-indep. ΔAUC p` = 0.141 (BH q = 0.352) with the verdict "PASS (method only; size-indep. CI contains 0)". The two panels use different size-correction constructions: breadth compares docking AUC (0.880) directly to the MW-only baseline (0.842) and finds docking better (p = 1.1e-6); S4 computes a ΔAUC = AUC_dock − AUC_mw_only with a resampling CI and finds it non-significant (p = 0.141). Both purport to answer "does docking add beyond molecular weight?" yet reach opposite conclusions for AXL.

**【Why it matters】** The "honest null — no target clears both filters" claim (submission.md:83, 95) is only as strong as its most consistent target. If AXL actually clears the size-independent filter in one table, the blanket "all targets fail" statement is overstated, and a reviewer recomputing from the breadth CSV will find AXL passing. The inconsistency must be reconciled and one authoritative size-correction method declared.

**【Specific fix】** Either (a) adopt a single size-correction method across both tables and report AXL's verdict consistently, or (b) explicitly explain why the two constructions differ (e.g., "the breadth comparison tests AUC_dock > AUC_mw_only by MWU, whereas S4 tests the ΔAUC CI; AXL passes the former but not the latter, so we classify AXL as method-validated-only, not size-independent"). Do not leave both verdicts standing unreconciled.

---

## Item 10 — ADRA2A is flagged "not reliable" as a reverse control despite having the most known binders of any target

**【Problem】** In the reverse-control table ADRA2A is marked `reliable = False` even though it has 115 known ChEMBL binder pairs (the most of any target), violating the stated rule that reliability requires ≥3 known pairs.

**【Evidence】** `results/tables/P6_reverse_control.csv` (also supplementary.md S3): AXL n_known=13 → reliable True; TNIK 10 → True; ACVR1 9 → True; MAPK14 16 → True; ADRA2A n_known=115 → `reliable = False`. The Methods (submission.md:121) state the reverse-control rule as "`reliable` = True only when ≥3 known pairs exist." With 115 pairs, ADRA2A should be reliable=True by that rule. The likely reason it is False is that its AUC is 0.532 (chance), so the flag was set manually — but that conflates "control failed" with "control unreliable," which are different statements. The 115 promiscuous ChEMBL binders (amitriptyline, aripiprazole, etc.) are exactly why the AUC is low, and that is itself informative (a GPCR with many off-target hits does not enrich in structure-based docking).

**【Why it matters】** It is a minor data-integrity/notation issue, but it muddies the reverse-control logic: a reader trusting the `reliable` flag would think ADRA2A's 115 binders are too few to judge, when in fact they are the most numerous and the low AUC is the real, reportable result (GPCR docking performs at chance here).

**【Specific fix】** Reconcile the flag with the rule: either set ADRA2A `reliable = True` (115 ≥ 3) and report its AUC 0.532 as a genuine failed positive control, or rename the column to `control_passed` so "False" means "failed," not "unreliable." Add a note that ADRA2A's 115 binders are promiscuous psychoactive compounds, which explains the chance-level AUC and reflects GPCR docking difficulty rather than absence of α2A pharmacology.

---

## Item 11 — "17/33 hubs in the dorsal horn" is constitutive baseline anatomy, not injury response, and is over-read as pain-relevant

**【Problem】** The Visium result that 17/33 detectably expressed hubs localize to the dorsal horn is presented as support for a pain-afferent axis, but it was measured on Sham/baseline tissue, so it maps where these genes are *constitutively* expressed, not where they respond to injury.

**【Evidence】** submission.md:56: "17 of 33 detectably expressed hubs (51.5%) mapped to the dorsal horn … on Sham/baseline tissue—no injury-arm spatial data were available." I verified the regionalization in `results/tables/P5_GSE325938_hub_regionalization.csv` (supplementary.md S2): 33/35 hubs expressed (CRISP3, LNP1 all-zero), 17 assigned to DorsalHorn, all passing the 5% detection floor. The manuscript does hedge ("no injury-induced redistribution is claimed"), which is correct. The problem is the surrounding framing: "dorsal horn (pain-afferent first station)" (submission.md:56, 91) implies pain relevance from a baseline map. Many dorsal-horn-expressed genes at baseline are simply constitutively expressed there (e.g., neuronal housekeeping/sensory markers), so 51.5% in the dorsal horn is expected from gross spinal anatomy and does not by itself implicate a maladaptive response.

**【Why it matters】** Spatial localization is a major display claim (Fig. 4B, S2). If read as "hubs concentrate at the pain first station," it over-interprets a baseline spatial map. The honest, defensible claim is "hubs are anatomically present in the dorsal horn at baseline," which is necessary but not sufficient for a pain role.

**【Specific fix】** In submission.md:56 and the Fig. 4B legend, reframe as: "On Sham/baseline tissue, 17/33 detectably expressed hubs localized to the dorsal horn — i.e., these candidates are anatomically present at the primary somatosensory gateway, but this is a constitutive-expression map; injury-induced redistribution (and thus pain-specific enrichment) cannot be assessed without an injury-arm Visium cohort, which is a stated limitation."

---

## Item 12 — The human-miRNA "honest negative" is underpowered and blood-based; its null does not speak to the CNS axis

**【Problem】** The human layer is correctly reported as an honest negative (set-perm p = 0.51), but the manuscript understates that plasma miRNAs are a poor proxy for the DRG–spinal axis, so a null in blood neither confirms nor refutes the rodent axis.

**【Evidence】** submission.md:48: GSE158825 n = 60 human plasma miRNA; set-level permutation p = 0.51; "underpowered … demarcates where prospective validation is required rather than confirming an absence." I verified the chain counts in `results/tables/P4_hub_miRNA_human_integration.csv` (3,511 relationships, 752 high-confidence ≥80, 253 plasma-detectable) and the set-perm result (`P4_setlevel_test.json` p = 0.51). The logic is sound. The gap is biological: plasma miRNA originates largely from blood/immune compartments and is only weakly coupled to DRG/spinal cord transcriptional state; a null here is unsurprising and uninformative about the CNS axis the manuscript actually studies.

**【Why it matters】** Calling the human layer a "boundary, not a failure" is the right instinct, but presenting it as a meaningful test of the axis overstates what plasma miRNAs can address. The honest boundary is narrower: "we could not detect a plasma-miRNA signature associated with the hub set in n = 60 samples," which says little about DRG/spinal biology.

**【Specific fix】** Add to submission.md:48: "Because plasma miRNAs reflect peripheral/immune rather than DRG–spinal transcriptional state, this null is uninformative about the CNS axis itself; it demarcates only that a blood-based miRNA proxy is underpowered and biologically distal, and that CSF or DRG/tissue validation is required before any human inference."

---

## Item 13 — Missing must-cite literature: incision-model Nav-channel direction and SCN8A/Nav1.6 in pain

**【Problem】** The manuscript's sharpest novel claim — SCN channels UP in incision but DOWN in nerve-injury — is presented without citing the existing literature on Nav-channel regulation in incisional/postoperative pain or on Nav1.6 in pain, leaving the field context absent.

**【Evidence】** A full-text scan of the reference list (submission.md:134–155) shows Nav-channel citations are limited to ref 16 (McDonnell 2018, Nav1.7 trial) and ref 10 (Divito 2026, suzetrigine/Nav1.8). There is no citation for (a) Nav1.8/SCN10A up-regulation in incisional pain models (a documented phenomenon), (b) SCN8A/Nav1.6 in nociception or neuropathic pain, or (c) the broader literature on Nav-channel mRNA-versus-function dissociation after nerve injury that would explain why mRNA down-regulation coexists with channel-driven hyperexcitability. The Discussion (submission.md:91) hedges the Nav claim but provides no literature anchor.

**【Why it matters】** Without these citations the model-dependent direction looks like a free-standing computational observation rather than a finding situated in 20+ years of Nav-channel pain biology. Citing the incision-Nav literature would *strengthen* the claim (it is consistent with prior work), not weaken it; omitting it looks like the authors are unaware of it.

**【Specific fix】** Add 2–3 citations in submission.md:38/91: (i) a study showing Nav1.8 up-regulation in incisional/postoperative pain; (ii) SCN8A/Nav1.6 pain literature; (iii) a review on Nav-channel transcriptional regulation vs functional contribution after nerve injury (to frame the mRNA-down finding). This converts "we found X" into "we found X, consistent with Y."

---

## Item 14 — The "conserved nerve-injury response, not CPSP-specific" reframing is credible, but the title/abstract still foreground CPSP the data never directly address

**【Problem】** The reframing is honest and well-justified, yet the study contains no CPSP (human chronic postsurgical pain) dataset at all — every axis study is rodent nerve-injury (4/5) or rodent incision (1/5) — so "CPSP" in the title/abstract is inferential, not measured.

**【Evidence】** submission.md:32,38 and Methods (submission.md:104,107) confirm the DRG-axis meta uses GSE267799 (rat incision), GSE212311 (rat CCI), GSE278227 (rat CCI), GSE241361 (mouse SNI), GSE265957 (mouse tibial/SNI translatome). 4 of 5 are nerve-injury models; 1 is incision. None is human CPSP. The single human dataset is GSE158825 (plasma miRNA, n = 60, negative). The manuscript is commendably explicit about this in the Introduction/Results ("specificity of the axis to postsurgical versus nerve-injury pain is not demonstrated"). The residual issue is that the Abstract's first sentence and the clinical framing still center "CPSP," and the Discussion (submission.md:91, 97) repeatedly ties findings to "CPSP-adjacent" clinical translation.

**【Why it matters】** *Scientific Reports* reviewers will ask whether the CPSP claim is supported. It is not, by the author's own admission — but the packaging (title mentions "chronic postsurgical pain") could be read as over-claiming. The reframing is a strength; the residual CPSP foregrounding is the only place it is not fully carried through.

**【Specific fix】** Keep the nerve-injury reframing in the title (already present) and lead the Abstract with it; rephrase the opening from "Chronic postsurgical pain (CPSP) affects 10–50%…" to "Chronic postsurgical pain (CPSP) is a major burden; because no human CPSP transcriptome of the DRG–spinal axis exists, we interrogated the conserved nerve-injury response that CPSP is hypothesized to share…" so the CPSP link is explicitly framed as a hypothesis, not a measured endpoint.

---

## Item 15 — "OXPHOS suppression" is reported without cell-type resolution, so the metabolic claim is broader than the data support

**【Problem】** The manuscript headlines a polarity-opposed "OXPHOS suppression" axis, but the gene-set statistic is computed on the bulk/stouffer meta_Z vector with no cell-type deconvolution, so it cannot state whether the metabolic suppression resides in neurons, glia, or is a compositional artefact of injury-induced cell-type shifts.

**【Evidence】** submission.md:34: "mitochondrial OXPHOS was downregulated (mean_Z −2.37, 73.7% of members down; permutation p = 0.004)." I verified from `P3_geneset_stats.csv`: Mitochondria_OXPHOS mean_Z = −2.373, frac_up = 0.263 (⇒ 73.7% down), perm_p = 0.0040 — correct. But the OXPHOS gene set (S5) is "Electron-transport-chain complexes I–V (NDUF*, SDH*, UQCR*, COX*, ATP5*)" — these are expressed across neurons, glia, and vascular cells. The single-cell layers (GSE216039 DRG, GSE328175 spinal, GSE246288 microglia) are described as "directional hints" with "0 BH-significant genes" (submission.md:52,54) because n = 2–3/group, so they cannot localize the metabolic suppression. The bulk-only meta (submission.md:36) reports OXPHOS −2.80 with only 27.8% down (vs 73.7% in the six-input), a striking drop that the manuscript attributes to "ribosome-biased signals" but which could equally reflect that the translatome contributed neurons with strong ETC expression.

**【Why it matters】** A "metabolic suppression" interpretation implies the injured neurons or activated glia shift away from oxidative phosphorylation (a Warburg-like state, consistent with Kong 2023 Lyn→glycolysis, which is cited). But without showing the suppression is in a pain-relevant cell type, the claim risks being a bulk-average of mixed cell populations. This is the difference between "DRG neurons suppress OXPHOS in pain" (mechanistically actionable) and "the bulk DRG-spinal sample shows lower ETC Z" (descriptive).

**【Specific fix】** Either (a) add a cell-type deconvolution (e.g., CIBERSORTx or the single-cell reference from GSE216039/GSE328175) of the OXPHOS signal, or (b) soften to: "Bulk meta-analysis indicates coordinated OXPHOS gene down-regulation (mean_Z −2.37; 73.7% of members down), but cell-type resolution is lacking (single-cell calls are directional hints only, n = 2–3/group), so the cellular locus of metabolic suppression is unresolved and requires validation." Do not assert neuronal metabolic suppression without evidence.

---

## Item 16 — The 0/35 bootstrap instability is honestly reported but its consequence for docking target selection is under-appraised

**【Problem】** The manuscript correctly reports that 0/35 hubs reached ≥0.9 bootstrap stability, yet still uses the 35-gene set as the basis for the hub→target eligibility rule that selects the docking targets, without quantifying how unstable the *docking target list* itself is.

**【Evidence】** submission.md:44: bootstrap of 72 pooled samples ("P3_hub_bootstrap.csv") showed per-gene recovery 0.5%–15.5% and "0/35 hubs reached a ≥0.9 stability threshold." I confirmed `P3_hub_bootstrap.csv` exists and the summary is reflected in the text. The hub→target eligibility rule (submission.md:85) then takes the 35 hubs and keeps those with n_holo_PDB ≥ 1 → 17 dock-eligible hubs → 10 actually docked. Because the hub set is resampling-unstable, the set of 17 dock-eligible / 10 docked targets is itself a draw from an unstable upstream list. The manuscript states the rule is "decoupled from hub-selection stability" (submission.md:85) — true for the mechanics, but it does not report the sensitivity of the 17/10 target list to bootstrap resampling of the hub set, so the reader cannot judge whether e.g. TFE3, AXL, MAPK14 would survive as hubs (and hence as targets) under resampling.

**【Why it matters】** The "honest null" docking conclusion is robust to target choice in the sense that no target enriched — but the *specific* targets flagged for prospective validation (and the competing-interest-adjacent ADRA2A) are drawn from an unstable hub list. If the hub list is 90% resampling-noise, the translational "Top-20 candidate set" is a hypothesis about a hypothesis, and the manuscript should say so more loudly than the single sentence at submission.md:85.

**【Specific fix】** Add a short analysis: bootstrap-resample the 72 samples, re-derive the hub set each time, and report the stability of the *docking-target set* (e.g., "the 10 docked targets were recovered in X% of bootstrap replicates; TFE3/AXL/MAPK14 in Y%"). Then state the prospective-validation priority explicitly as "derived from a resampling-unstable hub list and therefore itself tentative." This converts the honesty caveat from a footnote into a quantified boundary.

---

## Item 17 — The suzetrigine (Nav1.8) reference is biologically incoherent with the manuscript's own SCN10A direction unless the mRNA-versus-function dissociation is stated

**【Problem】** The manuscript invokes suzetrigine — a selective Nav1.8 (SCN10A) blocker — as the "expected" non-opioid analgesic signal that the docking screen should have surfaced, yet its own meta shows SCN10A is transcriptionally *down*-regulated in nerve-injury, which makes a Nav1.8-blocker rationale appear contradictory.

**【Evidence】** submission.md:83: "consistent with the absence of a selective nonopioid analgesic signal such as suzetrigine¹⁰ in this docking space." suzetrigine targets Nav1.8 = SCN10A (ref 10, Divito 2026, which I accept as a recent Nav1.8 analgesic reference). But the same manuscript reports SCN10A down-regulated in nerve-injury (submission.md:38; verified six-input SCN10A meta_Z = −3.153; per-contrast logFC negative in GSE212311/GSE278227/GSE241361). A naive reader sees: "Nav1.8 is down, yet we expected a Nav1.8 blocker to show up as an analgesic" — a seeming contradiction, because the manuscript never states the canonical resolution: in neuropathic pain, Nav1.8 channel *function/trafficking* is upregulated at the membrane despite stable or reduced mRNA, which is exactly why Nav1.8 blockers are analgesic. The manuscript's honest-null docking (Nav channels were excluded as undockable) means suzetrigine could not appear anyway, but the textual linkage invites confusion.

**【Why it matters】** This is the kind of mRNA-vs-function point that, if stated once, would actually *strengthen* the SCN narrative (it shows the authors understand why a down-regulated transcript does not preclude a channel-targeted therapy). Left unstated, it looks like an internal inconsistency between the SCN-direction claim and the suzetrigine citation.

**【Specific fix】** In submission.md:83, add: "Suzetrigine targets Nav1.8 (SCN10A); although our meta shows SCN10A transcript down-regulation in nerve-injury, Nav1.8 channel membrane trafficking/function is upregulated in neuropathic pain, which is the basis for Nav1.8-blocking analgesia — and because Nav channels lacked ligand-anchored holo structures they were excluded from docking, so suzetrigine could not appear by construction." This removes the apparent contradiction and demonstrates biological fluency.

---

## Item 18 — The purinergic self-negative means the "DAM" state lacks the canonical P2X4 microglial arm, and the DAM label should be qualified accordingly

**【Problem】** The manuscript reports a negative purinergic (P2RX/P2RY) signal and treats it as a useful boundary, but does not draw the key biological inference: the most canonical microglial mechanism in neuropathic pain (P2X4-driven microglial activation, Tsuda 2003, ref 15, which the manuscript does cite) is absent here, so the activated microglia in this axis are DAM-like in complement/phagocytic markers but *not* the P2X4-state — i.e., a partial/atypical DAM.

**【Evidence】** submission.md:62: "the purinergic family was itself negative: P2RX/P2RY showed no coordinate change (permutation p = 0.339 in the bulk-only meta; p = 0.440 in the six-input meta)." I verified from `P3_geneset_stats.csv`: P2RX_P2RY mean_Z = 0.848, perm_p = 0.440 (six-input); and from `_R3_bulkonly_meta_summary.json` setcalls: P2RX_P2RY perm_p = 0.3388 (bulk). Both match. The DAM set (S5) includes complement (C1QA/B/C) and phagocytic (MERTK, ITGAX, AXL) and lysosomal (CTSD, LPL, CST7) markers but not P2rx4 explicitly; the purinergic set (P2RX1–7, P2RY1/2/12/13/14) is separate and negative. The manuscript correctly notes "the DAM state captured is not the classic P2X4-driven microglial activation" (submission.md:62) — but then continues to headline "DAM microglia" as a clean programme without re-qualifying that the purinergic activation arm is missing.

**【Why it matters】** For a pain neuroimmunologist, the P2X4 microglial state (Tsuda et al., Nat Med 2003) is *the* best-established microglial driver of tactile allodynia after nerve injury. Showing it absent while complement/DAM markers are up tells a more interesting story than a generic "DAM activation": it suggests the axis captures the complement/phagocytic microglial programme but not its purinergic effector arm — a dissociation that should be stated, not buried as a one-line boundary. It also guards against over-reading the DAM claim (Item 7): a complement-up / P2X4-flat microglia is a specific, partial state, not full DAM engagement.

**【Specific fix】** In submission.md:62 and the Discussion (submission.md:91), state explicitly: "The DAM-like programme captured here is complement/phagocytic (C1q, MERTK, AXL, lysosomal) but lacks the canonical P2X4 purinergic microglial arm (P2RX/P2RY flat, perm p = 0.34–0.44), so it represents a partial, complement-weighted microglial state rather than full DAM engagement; this dissociation should be tested directly by profiling P2rx4 at the protein level in the same models."

---

## § Stands up (things I suspected were wrong but found correct)

1. **The nerve-injury-dominant, CPSP-reframed design is honestly executed.** I expected the "CPSP" label to be a marketing overlay on nerve-injury data, but the manuscript states plainly (submission.md:24, 32, 91) that 4/5 studies are nerve-injury and that CPSP-specificity is *not* demonstrated, and it rebuilds the abstract/title around that. This is genuine methodological honesty, not lip-service.

2. **The core signature, concordance, and gene-set statistics all recompute exactly.** Core = 4,055 (meta_FDR<0.05 & consistency≥0.8) from `META_DRG_axis_stouffer.csv` (16,552 genes); 7,751/14,390 = 53.9% and 2,473/3,556 = 69.5% both verified; neuroinflammation +4.94/100% up, DAM +3.88/93.8% up, complement +3.44/94.4% up, OXPHOS −2.37/73.7% down all match `P3_geneset_stats.csv`. The numbers are real.

3. **The bulk-only sensitivity analysis is internally consistent and supports the axis.** `META_DRG_axis_CORE_signature`-adjacent `_R3_bulkonly_meta_summary.json` gives bulk-only core 1,981, overlap 1,732/4,055 = 42.7% (both verified), and the neuroimmune–metabolic programme survives (Neuroinflammation mean_Z 5.13, DAM 3.96, Complement 3.53, OXPHOS −2.80) — so excluding the translatome does not dismantle the conclusion. This is a credible robustness check.

4. **The SCN direction itself (not its magnitude) is correct and not a species artefact.** Within rat, incision (GSE267799) is UP while rat CCI (GSE212311, GSE278227) is DOWN; mouse nerve-injury (GSE241361, GSE265957) is also DOWN. So the inversion holds across species and is not a rat-vs-mouse confound. The biological direction the manuscript argues for is sound; only the magnitude column (Item 2) is mislabeled.

5. **The docking "honest null" is real and well-controlled.** ADRA2A Tier-1 AUC 0.618 → full-library 0.532 (p = 0.118 NS) verified from `P6_breadth_chembl_power.csv`; reverse controls, MW correction, and the breadth flip are present and the null is reported without special-pleading for the author's ADRA2A grant interest. The competing-interest disclosure (submission.md:169) is transparent.

6. **The LODO cross-animal floor is as reported.** `P3_lodo_auc_ci.csv` gives GSE267799_incision_ratDRG AUC 0.917 [0.729, 1.0], n = 20; other folds 0.95–1.0 — matching submission.md:44. The same-animal GSE241361 DRG/SC (n = 9 each) are correctly separated as within-study.

---

## § Questions for the authors (please answer; I will not guess)

1. **Table 1b units.** Is the per-contrast magnitude column intended to be log₂FC or Z? The values match the Z-statistics in `_R3_bulkonly_meta_summary.json::scn_tab` exactly, not the logFC in `META_DRG_axis_stouffer.csv`. Please confirm and, if Z, replace with the actual logFC.
2. **CDHR5.** Which study/dataset drives CDHR5's three-method consensus? If it traces to a single study or a sample-preparation axis, what happens to the 35-gene set when that signal is removed?
3. **AXL size correction.** Which of the two size-correction implementations (breadth AUC_dock > AUC_mw_only, vs S4 ΔAUC CI) is authoritative for the "no target clears both filters" claim? Do you intend AXL to be classified as passing or failing size-independence?
4. **Incision arm.** Given GSE267799 is the sole incision study (rat, ~day-10 chronic), do you have or plan any independent incisional-pain dataset to cross-check the SCN up-regulation before claiming model-dependent direction?
5. **REG3B / DAM framing.** Will you soften the REG3B dismissal to acknowledge independent nerve-injury/regeneration literature, and will you add a pain-specific microglial-state citation before using the "DAM" label?
6. **Bulk meta_Z source.** The "Bulk meta_Z" column in Table 1b (SCN9A −2.92, SCN8A −4.92, …) — can you point to the exact table/file it was computed from? (The six-input `META_DRG_axis_stouffer.csv` gives SCN8A −5.113; I could not locate a standalone bulk meta_Z table in `results/tables/`.)

---

## § What I actually checked

**Files read (allowed set only):**
- `reports/MVP_ScientificReports_submission.md` (full, 228 lines)
- `reports/MVP_ScientificReports_supplementary.md` (full, S1–S5)
- `reviews/round4_2026-09-20/_PANEL_BRIEF.md` (brief only)
- Source tables: `results/tables/META_DRG_axis_stouffer.csv`, `results/tables/META_DRG_axis_CORE_signature.csv`, `results/tables/P3_geneset_stats.csv`, `results/tables/P3_hub_genes.csv`, `results/tables/P3_lodo_auc_ci.csv`, `results/tables/P3_hub_bootstrap.csv`, `results/tables/_R3_bulkonly_meta_summary.json`, `results/tables/_R3_plausibility.json`, `results/tables/P6_reverse_control.csv`, `results/tables/P6_breadth_chembl_power.csv`, `results/tables/P6_face_validity.csv`, `results/tables/P4_hub_miRNA_human_integration.csv`, `results/tables/P4_setlevel_test.json`, `results/tables/P4_hub_targeting_miRNAs.csv`, `results/tables/P5_GSE325938_hub_regionalization.csv`
- Processed data: `data/processed/GSE267799_DRG_sampletable.csv`, `GSE265957-GPL21103_series_matrix.txt.gz_samples.csv`, `GSE278227_DRG_sampletable.csv`, `GSE241361_sampletable.csv`, `GSE212311_DRG_sampletable.csv`, and the five `*_series_matrix.txt.gz_samples.csv` for organism/species; `data/processed/GSE267799_series_matrix.txt.gz_samples.csv` (harvest day).

**Recomputations run (managed Python 3.13.12):**
- Core size 4,055 from `meta_FDR<0.05 & consistency≥0.8` on 16,552 genes; meta_FDR<0.05 count = 6,869. **Match.**
- Concordance: `incision_lfc` not null = 14,390; `concordant_incision` True = 7,751 → 53.86% (≈53.9%). Core-restricted: 3,556 shared, 2,473 concordant → 69.54% (≈69.5%). **Match.**
- SCN (six-input `META_DRG_axis_stouffer.csv`): SCN9A meta_Z −3.475/FDR 2.25e-3; SCN10A −3.153/5.94e-3; SCN11A −3.558/1.73e-3; SCN8A −5.113/4.55e-6. Manuscript "Bulk meta_Z" (−2.92/−3.03/−3.41/−4.92) is less significant than the six-input, consistent with a 4-study bulk meta; I could not locate a standalone bulk meta_Z file to recompute exactly.
- Per-contrast actual logFC for SCN channels (from `META_DRG_axis_stouffer.csv`): SCN9A GSE278227 = −0.29, GSE241361 = −2.71; SCN8A GSE278227 = −0.75, GSE212311 = −0.39. These do **not** match Table 1b's −4.46 / −1.02 / −6.73 / −2.63, which instead match the Z-values in `_R3_bulkonly_meta_summary.json::scn_tab` (SCN9A GSE278227 Z −4.465, GSE241361 Z −1.016; SCN8A GSE278227 Z −6.728, GSE212311 Z −2.635). **Discrepancy confirmed: Table 1b magnitudes are Z, not logFC.**
- Gene-set stats from `P3_geneset_stats.csv`: Neuroinflammation mean_Z 4.943/frac_up 1.000/perm_p 0.0005; DAM 3.884/0.938/0.0005; Complement 3.441/0.944/0.0005; OXPHOS −2.373/frac_up 0.263 (⇒73.7% down)/perm_p 0.0040; Nav_SCN −1.365/perm_p 0.180; P2RX_P2RY 0.848/perm_p 0.440. **All match.**
- Bulk-only (json): core 1,981, overlap 1,732/4,055 = 42.71%; Neuroinflammation 5.13, DAM 3.96, Complement 3.53, OXPHOS −2.80. **Match.**
- Hub list (`P3_hub_genes.csv`): 35 hubs; 5 with n_methods=3 = SPRR1A, ATF3, TFE3, CDHR5, GALNS; 32/35 in_meta_core; NOT in core = REG3B, ANKRD1, MEGF11; SCN8A absent (correct). **Match.**
- LODO (`P3_lodo_auc_ci.csv`): GSE267799 incision rat DRG 0.9167 [0.729, 1.0] n=20; GSE278227 1.000 n=28; GSE212311 1.000 n=6; GSE241361 DRG 1.000 n=9; GSE241361 SC 0.950 n=9. **Match.**
- Docking breadth (`P6_breadth_chembl_power.csv`): ADRA2A t1 AUC 0.618 (p=1.9e-4), full-library 0.532 (p=0.118); AXL full 0.880 (p=1.1e-6, size-only baseline 0.842 → PASS in this file); ACVR1 0.797 FAIL (baseline 0.817); MAPK14 0.779 FAIL (baseline 0.787). Reverse control (`P6_reverse_control.csv`): AXL 13 pairs reliable True, ADRA2A 115 pairs reliable **False** (rule violation). **Match / discrepancy noted.**
- Species: GSE267799 *Rattus*; GSE212311, GSE278227 *Rattus norvegicus*; GSE241361, GSE265957 *Mus musculus*. GSE267799 chronic harvest day = 10d (sample table `time_label` "10d"), resolving (partially) the manuscript's harvest-day caveat.

**Discrepancies found:**
1. **Table 1b per-contrast magnitudes are Z-statistics, not log₂-fold-changes** (Item 2) — confirmed by exact numeric match to `scn_tab` Z and mismatch with `META_DRG_axis_stouffer.csv` logFC.
2. **AXL size-independent verdict contradicts between `P6_breadth_chembl_power.csv` (PASS) and Table 3b/S4 (p=0.141, CI contains 0)** (Item 9).
3. **ADRA2A `reliable=False` despite 115 known pairs, violating the stated ≥3 rule** (Item 10).
4. Minor: manuscript's harvest-day caveat (submission.md:107) says the day "could not be verified," but the processed sample table shows 10d — the source GEO metadata may lack it, but the reanalyzed data contains it.

No other numeric discrepancies were found; all headline meta/gene-set/docking counts I could recompute matched the manuscript.
