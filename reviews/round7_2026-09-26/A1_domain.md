# A1 — Domain Review (Pain / Neuroscience / Computational Biology)

**Manuscript:** *Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null* (single-author reanalysis; PLOS ONE / Scientific Reports target)
**Reviewer role:** Domain reviewer (A1) — independent, first-submission framing. No prior review history assumed.

---

## 1. Overall assessment

This is an unusually self-critical computational manuscript. The author repeatedly disclaims causal claims, flags circularity, reports resampling fragility, and turns the docking screen into an explicit "honest null." That discipline is a genuine strength and rare in the virtual-screening repurposing literature. My job here is the domain lane: does the *biology* hold up, and does the CPSP/nerve-injury framing survive a pain-specialist read?

**Headline verdict:** Major-points-tier revision. The analytical honesty is real, but three domain claims need correction before acceptance: (i) the sodium-channel "does not contradict neuronal up-regulation" hedge misuses its own citations and omits the channel that actually defines the injury transcriptome (Nav1.3/SCN3A); (ii) "DAM-microglia" is over-specific as a headline for a bulk, largely non-microglial DRG/spinal signal; (iii) the "honest null" is honestly scoped in the body but over-generalized in the Abstract, where the ion-channel exclusion (the entire class of canonical pain targets) is invisible. None of these are fatal; all are fixable with text and a few citations.

I recomputed every number I cite below from the deposited `results/tables/` files. Details in §7.

---

## 2. Mandatory verification — recomputed values

| Claim in manuscript | Source file | My recomputation | Verdict |
|---|---|---|---|
| Neuroinflammation / Complement / DAM q = 0.003 (fixed) | `_R4_geneset_setlevel_bh.csv` | perm_q = 0.0029985 for all three | **Verified** |
| OXPHOS q = 0.020 (fixed) | same | perm_q = 0.02024 | **Verified** |
| OXPHOS q = 0.31 (random effects) | same | perm_q = 0.31034 | **Verified** |
| 17/33 hubs in dorsal horn | `P5_GSE325938_hub_regionalization.csv` | exactly 17 of 35 rows have `top_region = DorsalHorn`; CRISP3 & LNP1 have `top_detection = 0.0` (not detected) → 33/35 detectably expressed; 17/33 = 51.5% | **Verified** |
| Human miRNA p = 0.51 | `P4_setlevel_test.json` | perm_p = 0.51010 | **Verified** |
| Non-circular: 47.1% background, 46.3% stratum, −0.9 pp, p = 0.14 | `_R4_nerveinjury_only_summary.json` | all_measured 6779/14390 = 0.4711; NI_FDR05_AND_NIcons≥0.8 2266/4899 = 0.4625; strong_vs_background_pp = −0.9; perm_p = 0.1396 | **Verified** |
| Bulk-only core 2,512; overlap 2,202/4,055 = 54.3% | `META_bulkonly_sensitivity_summary.json` | bulk_only_core_size 2512; overlap 2202; overlap_pct 54.32% | **Verified** |
| SCN bulk meta_Z/FDR (4 channels) | `META_bulkonly_sensitivity_summary.json` → scn_tab | SCN9A −2.925 / 0.0108; SCN10A −3.034 / 0.0080; SCN11A −3.408 / 0.0026; SCN8A −4.924 / 1.0e-5 | **Verified** (matches Table 1b) |
| 35 hubs; 32/35 in meta-core; 5 full 3-method consensus | `P3_hub_genes.csv` | in_meta_core=False for REG3B, ANKRD1, MEGF11 → 32/35; n_methods=3 for SPRR1A, ATF3, TFE3, CDHR5, GALNS → 5 | **Verified** |
| Bootstrap: 0/35 ≥ 0.9 stability | `P3_hub_bootstrap.csv` | max hub_freq = 0.155 (CDHR5); no row ≥ 0.90 | **Verified** |
| ADRA2A full-library AUC 0.532, p = 0.118 | `P6_breadth_chembl_power.csv` | full_library auc = 0.53247, p_auc_mwu_onesided = 0.1184 | **Verified** |

**Discrepancy worth flagging (see F5 and §7):** the task brief named `P4_GSE249746_hub_celltype.csv` as the 17/33 source. That file does **not** contain dorsal-horn data — it is a human-DRG single-nucleus cluster table (`peak_annotation` = pain_relevant / nonpain(LTMR/proprio), with a `spearman_vs_painScore` column) from a study, **GSE249746, that is not listed among the 12 curated datasets in the Methods** (grep returns 0 mentions). The real 17/33 source is `P5_GSE325938_hub_regionalization.csv`. The GSE249746 file is an orphan and must be reconciled.

---

## 3. Findings

### F1 — The sodium-channel "does not contradict neuronal up-regulation" hedge misuses its citations and omits Nav1.3/SCN3A

【Problem】 The manuscript defends bulk SCN9A/10A/11A/8A down-regulation by appealing to "established neuronal up-regulation of Nav1.7/1.8/1.9 at the protein and functional level in injured DRG nociceptors" and to human SCN9A mutations, but two of those three supports are citation-category errors and the third (Nav1.8) is contradicted by the bulk signal the manuscript actually sees.

【Evidence】 Manuscript line 46: *"These bulk transcriptome-level down-regulations do not contradict the established neuronal up-regulation of Nav1.7/1.8/1.9 at the protein and functional level in injured DRG nociceptors, nor the human SCN9A mutations that causally link the channel to human pain¹¹,¹²,¹³."* Refs 11–13 (Yang 2004, Cox 2006, Fertleman 2006) are **germline SCN9A channelopathies** — they establish that Nav1.7 is *necessary and sufficient* for human pain perception, **not** that Nav1.7 is up-regulated after nerve injury. Citing them as evidence of injury-induced neuronal up-regulation is a category error. For Nav1.8/SCN10A specifically, the canonical axotomy/CCI literature (e.g., injury-induced *down*-regulation of Nav1.8 mRNA in IB4+ DRG neurons) actually *agrees* with the bulk down-regulation the manuscript reports (SCN10A bulk_meta_Z −3.03, FDR 0.008; verified in `META_bulkonly_sensitivity_summary.json`), so there is no contradiction to "resolve" — the hedge papers over a non-problem. Finally, the manuscript discusses **only** SCN9A/10A/11A/8A and never mentions **SCN3A/Nav1.3**, which is the sodium channel most robustly and consistently *up*-regulated at the transcript level after peripheral nerve injury (axotomy, SNI, CCI) in DRG neurons. In a pain transcriptomics paper, a sodium-channel discussion that omits Nav1.3 is incomplete; had SCN3A been tested, the "sodium channels are down-regulated" narrative could invert.

【Why it matters】 This is the single most biologically load-bearing hedge in the paper, and it is doing rhetorical work to reassure the reader that a surprising bulk signal is "not contradictory." Because the supporting citations do not support the claim as written, the hedge reads as defensive rather than explanatory and will be challenged by any pain electrophysiologist. The omission of Nav1.3 leaves the sodium-channel section looking like a partial inventory.

【Specific fix】 Replace lines 46's channel paragraph with a biologically precise version, e.g.:
> "The four tested nociceptor sodium channels (SCN9A/10A/11A/8A) are bulk-down-regulated in nerve injury. This is consistent with, rather than contradictory to, the known biology of injured DRG: SCN10A/Nav1.8 mRNA is down-regulated in axotomized IB4+ neurons, and bulk DRG signal is confounded by injury-induced neuronal atrophy/loss and by the dilution of neuronal transcripts by infiltrating immune and glial cells. The germline SCN9A channelopathies (Yang 2004; Cox 2006; Fertleman 2006) establish Nav1.7's necessity for human pain but are not evidence of injury-induced up-regulation; likewise, selective Nav1.7/1.8 inhibitors have repeatedly failed clinically (McDonnell 2018; Faber 2023; Eagles 2022). Notably, the channel most transcriptionally induced after injury, SCN3A/Nav1.3, was not among the tested sets and should be examined in a revision. We therefore describe these channels as nerve-injury-down-regulated in this collection and explicitly hedge any CPSP-specific claim."

---

### F2 — "DAM-microglia" is over-specific as a headline for a bulk DRG/spinal signal

【Problem】 The manuscript headlines "DAM-microglia" activation, but the signal is a bulk-tissue gene-set enrichment in tissues where resident microglia are sparse (especially DRG), and the cited Schafer provenance is mischaracterized.

【Evidence】 Abstract (line 14) and Results (line 42) lead with "DAM-microglia ... q = 0.003." The manuscript does correctly hedge at line 42 (*"this is a bulk-tissue gene-set signal, it cannot be attributed specifically to resident microglia versus infiltrating macrophages"*) and at Discussion line 114 (*"DAM-like"*). But two problems remain. (a) **Cellular resolution:** DRG is not CNS parenchyma; it contains very few resident microglia, so a "DAM-*microglia*" label for the DRG pole is biologically imprecise — the neuroimmune signal there is far more likely driven by infiltrating macrophages, satellite-glia activation, and the neurons themselves. Using "DAM-microglia" in the Abstract/Results headline, then retreating to "DAM-like" in the Discussion, is inconsistent emphasis. (b) **Citation characterization:** line 114 states *"Schafer et al.²⁴ describe its developmental origin, and our DAM set follows that provenance."* Schafer 2012 (Neuron 74:691) is about microglia sculpting **developing** synapses via complement-dependent pruning (C1q/C3/CX3CR1), and is the conceptual *complement* link to DAM — it does **not** describe the "developmental origin" of the DAM state (the yolk-sac progenitor origin of microglia is a different literature; Keren-Shaul 2017 defines DAM as an injury-response state). The phrase "developmental origin" is a misstatement of what Schafer 2012 shows.

【Why it matters】 The DAM label is evocative and will be read as a mechanistic microglial claim. In a DRG-centric axis it over-reaches, and the imprecise Schafer attribution is the kind of detail a careful reviewer (and the DAM-field readers) will flag. The manuscript's own honesty apparatus already supplies the correct "DAM-like / bulk-tissue" framing; it just needs to be applied consistently from the Abstract up.

【Specific fix】 (i) In the Abstract and Results, change "DAM microglia" to "DAM-like neuroimmune programme" everywhere it refers to the bulk signal, reserving "DAM" only for the gene-set name. (ii) Replace line 114's Schafer sentence with: *"The DAM programme was first defined in neurodegeneration (Keren-Shaul et al. 2017); its complement-dependent microglial phenotype connects conceptually to Schafer et al. (2012) on complement-mediated synaptic pruning. Because this is a bulk-tissue signal in tissues with sparse resident microglia (especially DRG), 'DAM-like' denotes a shared transcriptional programme, not a cell-type-resolved microglial state, and the DRG-pole signal may be driven as much by infiltrating macrophages and glial activation as by microglia."*

---

### F3 — CPSP framing is honestly hedged but the Abstract/Introduction overweight CPSP relative to the data

【Problem】 The manuscript is genuinely candid that 4/5 studies are nerve-injury and only 1 is incision, but the Abstract and Introduction still front-load CPSP (10–50% prevalence, "druggable targets on the DRG–spinal-cord axis remain undefined" for CPSP), creating a mismatch with a dataset that is ~83% nerve-injury.

【Evidence】 Abstract line 14: *"Because four of five axis studies are nerve-injury models and one is a surgical-incision model, we frame the axis as a nerve-injury-associated transcriptional response (not CPSP-specific)."* This is commendably explicit. However, the same Abstract opens with CPSP prevalence and the Introduction (lines 26–30) builds the entire motivation around CPSP. The title is "nerve-injury-associated" (honest), but the framing is "CPSP-adjacent." The decisive internal evidence is the translation test itself: the nerve-injury signature does **not** predict incision direction (46.3% vs 47.1% background, −0.9 pp, p = 0.14; verified §2), i.e. the manuscript's own data show that the CPSP-relevant (incision) model is *not* captured by the nerve-injury programme. That is a stronger reason to de-emphasize CPSP than the 4/5 caveat alone, and it is under-exploited as a framing argument.

【Why it matters】 If a reader scans only the Abstract/Introduction, they will conclude this is a CPSP mechanisms paper. The body then walks that back. The mismatch invites reviewer accusations of title/abstract baiting even though the body is honest. Tightening the front matter to match the body's discipline protects the paper.

【Specific fix】 In the Abstract, lead with the nerve-injury framing before any CPSP statistic, e.g.: *"We integrated 12 GEO datasets spanning the DRG–spinal axis. Because four of five axis studies are nerve-injury (SNI/CCI/tibial-nerve) models and only one is surgical incision, we frame the axis as a nerve-injury-associated transcriptional response and treat the single incision arm as a held-out translation test — not as a CPSP-specific mechanism. (CPSP affects 10–50% of surgical patients; the incision arm is the closest CPSP proxy available, and, as we show, it is not predicted by the nerve-injury signature.)"*

---

### F4 — The "honest null" is over-generalized in the Abstract; canonical pain targets (ion channels) were never docked

【Problem】 The docking conclusion is honestly scoped in the body ("Ion-channel targets ... lacked ligand-anchored holo structures ... were thus not docked", line 106/154) but the Abstract states a global null ("Full-library docking of 3,085 drugs found no target clearing both filters") that is in fact limited to 10 structurally tractable, non-ion-channel targets.

【Evidence】 Abstract line 14 vs Results line 106/154: the manuscript itself lists the excluded ion channels explicitly — "SCN9A/10A/11A/KCNQ2/CACNA2D1/GABRA1 have experimental structures but lack a ligand-anchored pocket ... were therefore not docked." So **33 of the original 43 candidate targets (the entire ion-channel class, which includes the very sodium channels analysed in Table 1b and the canonical pain targets P2X4/TRPV1) were never screened.** The honest-null conclusion — "no drug target held up" — is true *only* for the 10 tractable targets (ADRA2A, MAPK14, AXL, TNIK, ACVR1, SERPINE1, SLC2A1, GALNS, VASH2, ITPKC). The Abstract's global phrasing lets a reader conclude "virtual screening found no repurposable pain target," which is unsupported: it found no repurposable target *among 10 non-ion-channel proteins*.

【Why it matters】 This is precisely the kind of over-generalization the manuscript's own Methods warn against (it builds the whole paper around not over-claiming). The docking null is a real and useful methodological boundary — but it cannot speak to ion-channel repurposing, which is where most mechanistic pain pharmacology lives. The Abstract must carry the same scope limitation the body does.

【Specific fix】 Abstract: replace *"Full-library docking of 3,085 drugs found no target clearing both the full-library and size-independent enrichment filters"* with *"Full-library docking of 3,085 drugs against the 10 structurally tractable targets found none clearing both the full-library and size-independent enrichment filters; the ion-channel class (including the SCN channels analysed here) could not be docked for lack of ligand-anchored holo structures and remains untested."*

---

### F5 — The 17/33 dorsal-horn count is correct, but "assigned to the dorsal horn" overstates specificity, and GSE249746 is an orphan dataset

【Problem】 The 17/33 spatial figure is arithmetically correct, but it is a *peak-expression-region-on-baseline-tissue* count, not evidence of dorsal-horn enrichment/recruitment, and several of the 17 sit barely above the 5% detection floor; simultaneously, a results file from an undeclared dataset (GSE249746) exists and is unaccounted for.

【Evidence】 `P5_GSE325938_hub_regionalization.csv` (verified §2): 17 rows have `top_region = DorsalHorn`. But `top_detection` (fraction of dorsal-horn spots where the gene is detected) is low for several: GALNS 0.105, SRRM4 0.182, ITPKC 0.123, VASH2 0.189, TFE3 0.302 — i.e., these hubs are detected in only ~10–30% of dorsal-horn spots and are assigned to dorsal horn simply because it is the *highest* of seven regions. The manuscript does caveat this as "constitutive baseline anatomy, not injury-induced recruitment" (line 72), which is correct, but the body and Fig 4 legend still say "assigned to the dorsal horn," which a reader will read as anatomical localization. A count of "peak region = dorsal horn" is weaker than "localized to dorsal horn." Separately, `P4_GSE249746_hub_celltype.csv` contains 36 hub/ADRA2A rows with human-DRG cluster annotations (`pain_relevant` / `nonpain(LTMR/proprio)`) and a `spearman_vs_painScore` column, from **GSE249746 — a dataset absent from the Methods' 12-dataset list** (grep = 0). This is either an undeclared analysis or a leftover file; either way it is a transparency/STROBE gap and the brief's premise that it is the 17/33 source is wrong.

【Why it matters】 Spatial claims are visually persuasive; over-reading a peak-region count on uninjured tissue as "dorsal-horn localization" is the kind of claim that draws "over-interpretation" criticisms. The GSE249746 orphan file is a concrete audit defect: a reviewer must be able to map every deposited table to a declared dataset.

【Specific fix】 (i) Reword line 72 / Fig 4: *"17 of 33 detectably expressed hubs had their highest mean expression in the dorsal horn on Sham tissue (range of dorsal-horn detection fraction 10–80%); this is a constitutive baseline peak-expression assignment, not evidence of enrichment or injury recruitment."* (ii) Add a STROBE/Data-availability note reconciling `P4_GSE249746_hub_celltype.csv`: either declare GSE249746 as an additional (exploratory, non-core) human-DRG dataset with its own methods line, or remove the file from the release and state it was a discarded pilot. Do not leave an undocumented dataset in the supplementary tables.

---

### F6 — ADRA2A verdict labeling is internally inconsistent with the paper's own thresholds

【Problem】 The ADRA2A docking result is presented as "inconclusive, not a confirmed null," yet both its Tier-1 and its MW-adjusted full-library tests are statistically significant, while the paper treats weaker signals for the control targets as informative — an asymmetry worth making explicit.

【Evidence】 `P6_breadth_chembl_power.csv` (verified): ADRA2A Tier-1 (620-drug) AUC = 0.618, **p = 0.00019** (significant); full-library AUC = 0.532, p = 0.118 (NS); MW-adjusted full-library AUC = 0.578, **p ≈ 0.0005** (significant). The manuscript (Abstract line 14; Results line 106) emphasizes the NS full-library AUC and calls the result "inconclusive." Meanwhile, for AXL/TNIK the paper reports size-independent recovery via a *multivariate* control as informative. The paper's pre-specified rule (Table 3b) is "must clear BOTH raw full-library and size-independent filters" — under that rule ADRA2A correctly fails (full-library NS), so the verdict is defensible. But the significant Tier-1 (p=0.00019) and significant MW-adjusted (p=0.0005) signals are strong enough that "inconclusive" under-states them, and the asymmetry (strict for ADRA2A, lenient for controls) should be acknowledged rather than left implicit — especially because ADRA2A is the external add-on that is also the author's pending-grant target (competing-interest declared, line 219).

【Why it matters】 A reader could reasonably read "inconclusive" as "no signal," which is not what the table shows. Given the declared competing interest, the ADRA2A handling is the most scrutiny-prone part of the docking section; the asymmetry in verdict standards should be stated outright to pre-empt a bias critique.

【Specific fix】 In Results line 106, append: *"We apply one rule to all targets (both filters must clear); under it ADRA2A fails because its unadjusted full-library AUC is NS. We note, for transparency, that ADRA2A's Tier-1 (p=0.00019) and MW-adjusted full-library (p≈0.0005) tests are significant, so 'inconclusive' means 'fails the dual-filter bar,' not 'no signal.' Because ADRA2A is the author's externally motivated, pending-grant target, we report this without emphasis."*

---

### F7 — Missing MUST-CITE literature for the sodium-channel and neuroimmune sections

【Problem】 The sodium-channel discussion omits the defining injury-induced channel (Nav1.3/SCN3A) and the neuronal-loss confound; the neuroimmune section would be strengthened by citing the spinal-microglia time/sex-specific DAM literature it gestures at.

【Evidence】 (a) SCN3A/Nav1.3: the most consistently *up*-regulated sodium channel transcript after peripheral nerve injury in DRG neurons is absent from the manuscript. Its omission is the central gap in F1. (b) Neuronal loss/atrophy confound for bulk DRG: the manuscript mentions "neuronal loss or atrophy" (line 46) but cites no literature; this is a well-established confound for bulk DRG transcriptomics and should be cited. (c) The Discussion (line 114) cites Tansley 2022 for "only partial and time- and sex-specific overlap with the canonical DAM programme" — good — but the axotomy-induced Nav1.8 down-regulation (the literature that actually explains the bulk SCN10A signal) and the Nav1.3 induction literature are not cited. (d) For the DAM/complement claim in DRG, the macrophage-vs-microglia ambiguity (F2) would be sharpened by citing the DRG-resident vs infiltrating immune literature.

【Why it matters】 A domain reviewer expects the canonical sodium-channel and neuroimmune references; their absence makes the channel section look under-read and weakens the "we know our biology" credibility that the rest of the paper earns through its statistical honesty.

【Specific fix】 Add citations (examples the author should verify for fit): for Nav1.3/SCN3A induction after injury — Waxman / Dib-Hajj / Black lineage (e.g., studies showing SCN3A induction in axotomized DRG neurons); for Nav1.8 down-regulation after axotomy — Lai et al., *J Neurosci* 2004, and the Waxman-lab axotomy series; for DRG neuronal loss/atrophy confound — the relevant DRG-neuron-degeneration literature; for macrophage vs microglia in injured DRG — the Schwann/satellite/immune infiltration literature.

---

### F8 — "CXCL12/SDF-1 implicated specifically in CPSP" overstates the cited rodent evidence

【Problem】 The Discussion cites CXCL12/CXCR4 as "implicated specifically in CPSP" on the basis of two rodent studies that are mostly neuropathic/postsurgical models, not human CPSP.

【Evidence】 Line 114: *"Chemokine signalling at the spinal dorsal horn, in particular the CXCL12/SDF-1 axis, has also been implicated specifically in CPSP²⁹,³⁰."* Ref 29 (Zhang 2017) is rat *postsurgical* pain; ref 30 (Luo 2016) is *neuropathic* pain. Neither establishes CXCL12 as *CPSP-specific* in humans. The word "specifically" is not supported.

【Why it matters】 Minor, but "specifically in CPSP" is a stronger claim than the citations support and compounds the CPSP-overweighting concern in F3.

【Specific fix】 Replace with: *"Chemokine signalling at the spinal dorsal horn, including the CXCL12/CXCR4 axis, has been implicated in rodent postsurgical and neuropathic pain models (Zhang 2017; Luo 2016), consistent with the neuroimmune component of the axis identified here."*

---

### F9 — Descriptive-vs-causal handling is a strength, but one verb slips ("converges on")

【Problem】 The manuscript's causal-scope discipline is excellent, but the Discussion opens with "The DRG–spinal axis converges on a neuroimmune–metabolic programme," which implies coordination/directionality the design cannot support.

【Evidence】 Discussion line 114: *"The DRG–spinal axis converges on a neuroimmune–metabolic programme..."* The manuscript's own Causal-scope paragraph (line 161) correctly states all findings are associations and "response/programme" are descriptive. "Converges on" gently implies a shared driver. This is a one-word tone issue, not a substantive error.

【Why it matters】 Low; noted for consistency with the paper's own (admirable) discipline. A single verb that implies coordination undercuts the careful causal hedging elsewhere.

【Specific fix】 Change "converges on" to "is recurrently characterized by" or "shows a recurrent neuroimmune–metabolic signature."

---

## 4. § Stands up (things the manuscript gets right — domain view)

1. **The non-circular translation test is methodologically exemplary.** Building the signature on nerve-injury contrasts only and holding the incision contrast out as a test, then reporting 46.3% vs 47.1% background (p=0.14, verified), is exactly how this should be done. The authors even expose their own earlier circular numbers (53.9%/69.5%) and discard them. This is the paper's strongest contribution and is biologically honest: the incision (CPSP-proxy) model is *not* predicted by the nerve-injury programme.

2. **Set-level BH correction and the random-effects sensitivity are correctly applied and reported.** I verified q = 0.003 / 0.020 / 0.31 from `_R4_geneset_setlevel_bh.csv`. Applying BH across the 18 multi-member sets, and reporting OXPHOS as a fixed-effect-only finding that fails under random effects (q=0.31), is the right level of caution and is not over-claimed.

3. **The "DAM-like / bulk-tissue" and "DAM not fully reconstituted" hedges are biologically correct.** Lines 42, 78, and 114 correctly distinguish a shared transcriptional programme from a cell-type-resolved microglial state, and the self-negative on P2RX/P2RY (perm p = 0.339) honestly bounds the DAM interpretation. The purinergic self-negative is a genuine strength.

4. **The docking honest-null framework is sound and pre-specified.** Prospective full-library breadth, reverse positive controls, and MW correction are real methodological safeguards; the bulk-only and bootstrap fragility analyses (45.7% of the core is translatome-dependent; 0/35 hubs ≥ 0.9 bootstrap stability, verified) show the author understands resampling limits. The decision to report the null as a *methodological boundary* rather than a positive hit is defensible and useful.

5. **Causal-scope and AI-use disclosure are model examples.** The dedicated Causal-scope paragraph (line 161) and the explicit AI-drafting disclosure meet the bar that most computational manuscripts fail to reach.

---

## 5. § Questions for the authors

1. **GSE249746:** `P4_GSE249746_hub_celltype.csv` is present in the release but GSE249746 is not in your 12-dataset Methods list. Is this an exploratory human-DRG analysis you forgot to declare, or a discarded pilot file that should be removed? Either way it must be reconciled for STROBE compliance.

2. **SCN3A/Nav1.3:** Did you test SCN3A? Given it is the most injury-induced sodium channel transcript in DRG, its absence reverses the "sodium channels are down-regulated" narrative. If it was in the meta universe, report its direction; if not, explain why it was excluded from the channel sets.

3. **Dorsal-horn detection fractions:** For the 17 dorsal-horn-assigned hubs, could you report the actual dorsal-horn `top_detection` fractions (not just the peak-region call) in the supplementary table, so readers can see that several sit at 10–19% detection?

4. **ADRA2A asymmetry:** Given ADRA2A is your externally motivated, pending-grant target (declared competing interest), do you agree the verdict standard applied to it should be stated explicitly as identical to the controls, and the significant Tier-1/MW-adjusted p-values reported alongside the "inconclusive" label?

5. **Bulk DRG neuronal confound:** For the SCN down-regulation, have you attempted any neuronal-fraction correction (e.g., using neuronal marker load as a covariate) to separate true per-neuron channel change from neuronal loss/atrophy? If not, is this flagged as a known limitation rather than resolved by the current hedge?

6. **Translatome mixing:** The primary six-input meta mixes a ribosome-profiling translatome (GSE265957) with four bulk transcriptomes. Even though the bulk-only sensitivity (54.3% overlap) is reported, do you consider the primary six-input core or the bulk-only core as the analysis you would defend as primary in a revision?

---

## 6. Recommendations to the editor (priority order)

- **Major (must fix):** F1 (sodium-channel citation/logic + SCN3A omission), F2 (DAM-microglia headline precision + Schafer attribution), F4 (Abstract over-generalization of the docking null; ion-channel exclusion invisible).
- **Minor-but-required:** F3 (front-matter CPSP weighting), F5 (17/33 wording + GSE249746 orphan), F6 (ADRA2A verdict transparency), F8 (CXCL12 "specifically"), F9 (one verb).
- **Strengthen:** F7 (add the missing canonical citations).

None of the major points require new computation; they are text/citation corrections plus one dataset-reconciliation step. The analytical core of the paper is sound and, on its own terms, commendably honest.

---

## 7. § What I actually checked

**Files read (manuscript + source tables):**
- `reports/MVP_ScientificReports_submission.md` (full, 277 lines).
- `results/tables/P3_geneset_stats.csv` — gene-set raw stats.
- `results/tables/_R4_geneset_setlevel_bh.csv` — set-level BH q-values (fixed + random). **Used to verify q = 0.003 / 0.020 / 0.31.**
- `results/tables/P5_GSE325938_hub_regionalization.csv` — Visium hub regionalization. **Used to verify 17/33 dorsal-horn** (17 rows with `top_region = DorsalHorn`; CRISP3 & LNP1 `top_detection = 0.0`).
- `results/tables/P4_setlevel_test.json` — human-miRNA set-level permutation. **Used to verify p = 0.5101.**
- `results/tables/_R4_nerveinjury_only_summary.json` — non-circular strata. **Used to verify 6779/14390, 2266/4899, −0.9 pp, perm_p 0.1396.**
- `results/tables/META_bulkonly_sensitivity_summary.json` — bulk-only core + SCN table. **Used to verify core 2512, overlap 2202/4055 = 54.32%, and SCN bulk meta_Z/FDR.**
- `results/tables/P3_hub_genes.csv` — 35 hubs, meta-core membership, method consensus. **Used to verify 32/35 in core, 5 three-method.**
- `results/tables/P3_hub_bootstrap.csv` — bootstrap stability. **Used to verify max hub_freq 0.155, 0/35 ≥ 0.9.**
- `results/tables/P6_breadth_chembl_power.csv` — ADRA2A/others breadth AUCs. **Used to verify ADRA2A full-library 0.532 (p=0.118) and Tier-1 0.618 (p=0.00019).**
- `results/tables/P4_GSE249746_hub_celltype.csv` — read to check the 17/33 source named in the brief; found it is a **different** (human-DRG cluster) dataset, GSE249746, **not referenced in the manuscript** (confirmed via grep: 0 mentions).

**Values recomputed (not merely transcribed):**
- 17/33: counted `top_region == "DorsalHorn"` rows in the 35-row Visium file = 17; confirmed 2 zero-detection rows → denominator 33. Matches manuscript 51.5%.
- Gene-set q: read perm_q from the BH file directly (0.0029985, 0.02024, 0.31034) rather than relying on the manuscript's rounded 0.003/0.020/0.31 — all match.
- Non-circular rates: 6779/14390 = 0.4711; 2266/4899 = 0.4625; risk diff −0.9 pp; perm_p 0.1396 — all match.
- SCN bulk meta from the json scn_tab: SCN9A −2.925/0.0108, SCN10A −3.034/0.0080, SCN11A −3.408/0.0026, SCN8A −4.924/1.0e-5 — match Table 1b.

**Discrepancies / things I could not verify:**
- I did not re-run the per-contrast Welch tests or the Stouffer meta from raw counts (DEG_*.csv are multi-GB); I verified the *reported* aggregate numbers against the deposited summary json/csv, which is the appropriate level for a review.
- The `P4_GSE249746_hub_celltype.csv` discrepancy (orphan, undeclared dataset) is the one transparency defect I could not resolve from the manuscript alone — hence Q1.
- I did not assess the docking PDB/pose mechanics (ρ ≈ 0.78 fidelity, exhaustiveness-1 choice); those are computational-methodology matters outside the strict domain lane, though their consequence (ion-channel exclusion) is captured in F4.

**Independence note:** I treated the manuscript as a first submission and did not consult any other review, response, or source-file version outside `results/tables/` and the manuscript itself.
