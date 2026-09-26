# Reviewer A1 — Domain expert (chronic postsurgical pain / neuropathic pain / DRG–spinal-cord biology)

**Manuscript:** "A neuroimmune–metabolic programme defines the chronic postsurgical pain DRG–spinal axis with an honest repurposing null" (Scientific Reports, submission-ready v1.1, 2026-09-20)
**Review type:** Independent, fresh reading of the manuscript + supplementary + authoritative CSV outputs. This is treated as a first submission; I did not read the Round-1 review, the submission manifest, the project plan, or other reviewers' files.
**Scope of this review:** Biological defensibility of the "neuroimmune–metabolic axis" construct; novelty claim against the prior literature; correctness of specific biological claims (SCN9A/10A/11A, ADRA2A, MAPK14/p38, AXL, the annotation-outlier hubs); human-translatability framing of the negative miRNA layer; and the ADRA2A competing-interests tension.

---

## 1. Major issues

### 1A. The "neuroimmune–metabolic axis" is presented as CPSP-specific when the statistics only support a *generic* nerve-injury response

【Problem】 The title and Results/Discussion repeatedly frame the programme as *the* CPSP DRG–spinal axis, but the meta-analysis mixes incision, nerve-injury and tibial-nerve-injury models and the nerve-injury→incision translation was only 59.9% consistent, so the signature is better characterised as a conserved neuro-immune/metabolic injury response than a CPSP-specific axis.

【Evidence】 Manuscript line 1 (title) and line 30–33: the axis is "defined" by neuroinflammation mean_Z +4.94 (100% up), DAM microglia +3.88 (93.8% up), complement +3.44 (94.4% up) and OXPHOS −2.37 (73.7% down). I recomputed these four from `results/tables/P3_geneset_stats.csv`: Neuroinflammation mean_Z 4.9435, frac_up 1.000, n=19/19; DAM_microglia mean_Z 3.8838, frac_up 0.9375, n=16; Complement mean_Z 3.4409, frac_up 0.9444, n=18/22; Mitochondria_OXPHOS mean_Z −2.3728, frac_up 0.2632 → 73.7% down, n=19/20. All four perm_p values match the manuscript (0.0005/0.0005/0.0005/0.004). The *statistical* claims are correct. However, line 31 states nerve-injury→incision translation was directionally consistent in only 3,261/5,447 genes (59.9%, binomial p = 2.8e-48), and the six-dataset meta (line 32) deliberately spans incision + CCI + SNI + tibial-nerve models. DAM-microglia activation, complement upregulation and OXPHOS suppression are the canonical, near-universal transcriptional signature of *any* peripheral nerve injury / neuroinflammation (microglial–complement and metabolic dysfunction are reviewed as generic chronic-pain features in refs 6–8, 14–17 the authors themselves cite).

【Why it matters】 Scientific Reports readers will read the headline as a disease-specific mechanism. Over-claiming specificity from a pooled, model-heterogeneous meta-Z invites the "over-interpretation of meta-Z signs" critique and weakens the paper's central contribution: the value is the *integration and honest null*, not a newly-discovered CPSP-specific pathway. It also collides with the manuscript's own honesty posture elsewhere (the docking null, the human negative).

【Specific fix】 Replace disease-specific framing with mechanism-descriptive framing, e.g.: "Across CPSP-relevant incision, nerve-injury and tibial-nerve models, the DRG–spinal meta-signature is dominated by a conserved neuroimmune-activation (DAM microglia, complement) and OXPHOS-suppression programme — i.e., a generic maladaptive injury response rather than a CPSP-unique pathway." In the title consider "a neuroimmune–metabolic injury programme" instead of "defines the … axis". State explicitly in the Discussion that specificity to *postsurgical* (vs nerve-injury) pain is not demonstrated by these data.

---

### 1B. The "first CPSP study to integrate DRG and spinal-cord transcriptomes as a single axis" novelty claim is overstated and two directly relevant priors are not cited

【Problem】 The novelty claim is written broadly enough to imply the DRG+spinal-cord integration concept is itself new for CPSP, but (a) a multi-tissue CPSP transcriptomic study that already includes DRG exists, and (b) DRG↔spinal-cord cross-talk integration has already been published for neuropathic pain.

【Evidence】 Manuscript line 24: "To our knowledge this is the first CPSP study to integrate DRG and spinal-cord transcriptomes as a single axis via multi-dataset meta-analysis…". Literature check (WebSearch, 2026-09-20) returns two priors the manuscript does not cite:
- **Meng X-Y, Bu L, Shen L, Tao K-M. *Sci Data* 2024;11:1229 (PMID 39543146)** — "A transcriptome data set for comparing skin, muscle and dorsal root ganglion between acute and chronic postsurgical pain rats." This is a CPSP study that already performs multi-tissue (skin/muscle/**DRG**) transcriptomics across acute vs chronic postsurgical pain. It does *not* include spinal cord, so it does not invalidate the DRG+SC pairing, but it directly undercuts any implication that multi-tissue CPSP work including DRG is novel.
- **Dong F-L, Yu L, … Jiang B-C. *Commun Biol* 2025;8:70 (PMID 39820760)** — "An atlas of neuropathic pain-associated molecular pathological characteristics in the mouse spinal cord", which explicitly integrates spatial transcriptomics + snRNA-seq + bulk RNA-seq and reports "cross-talk omics between the DRG neurons and SC dorsal horn neurons and glial cells" after peripheral nerve injury. This shows DRG↔spinal-cord integration is an established *concept* (in neuropathic, not postsurgical, pain).

【Why it matters】 A broad "first … integrate DRG and spinal-cord" claim that omits these two papers is a straightforward novelty-overstatement that a careful reviewer (and the editor) will catch. It risks the paper being framed as claiming more than it delivers and detracts from the genuinely novel parts (12-dataset meta-analysis + LODO dual-ML + prospective full-library docking breadth applied to CPSP).

【Specific fix】 Narrow the claim to the combination/method and cite the priors, e.g.: "To our knowledge this is the first study to integrate DRG and spinal-cord transcriptomes as a single axis *for chronic postsurgical pain specifically via a 12-dataset Stouffer meta-analysis with leakage-controlled dual-ML hub locking and a prospectively specified full-library docking breadth screen*. Prior multi-tissue CPSP transcriptomics (Meng et al., *Sci Data* 2024) and DRG↔spinal cross-talk atlases in neuropathic pain (Dong et al., *Commun Biol* 2025) did not perform this meta-analytic + virtual-screening integration." Add both references to the Introduction.

---

### 1C. REG3B is wrongly flagged as an annotation outlier with "no established DRG- or pain-role" — it is an established DRG neuroimmune hub

【Problem】 The manuscript lists REG3B among six annotation outliers claimed to have "no established DRG- or pain-role," but REG3B/Reg3β is, in fact, a recently and directly demonstrated DRG-expressed, chronic-pain-relevant neuroimmune mediator; flagging it as a pure outlier is incorrect and under-sells a hub that actually *supports* the paper's neuroimmune-axis thesis.

【Evidence】 Manuscript line 49: "CDHR5 …, CRISP3 and REG3B (secretory/granule proteins) … have no established DRG- or pain-role." `results/tables/P3_hub_genes.csv` confirms REG3B is a hub (n_methods=2, in_meta_core=False). Literature check (WebSearch, 2026-09-20):
- **Nie H, Liu B, … Liu B. *Sci Adv* 2025;11(31):eadu4270 (PMID 40749060)** — "Neuronal Reg3β/macrophage TNF-α-mediated positive feedback signaling contributes to pain chronicity in a rat model of CRPS-I." This paper shows DRG *neurons* secrete Reg3β, which chemoattracts macrophages, forming a Reg3β–TNF-α positive-feedback loop driving chronic pain; Reg3β knockdown/neutralisation reduces macrophage infiltration and mechanical hypersensitivity. This is direct DRG + pain + neuroimmune evidence.
- **NCBI Gene (Reg3b, MGI:MGI:97478)** states Reg3b "Is expressed in central nervous system; **dorsal root ganglion**; hypoglossal nerve; and intestine."
- **Matsumoto S et al., *J Comp Neurol* 2011 (PMID 21681751)** shows Reg-IIIβ is expressed in specific subsets of primary sensory neurons.

【Why it matters】 Misclassifying REG3B as an outlier (a) is factually wrong, (b) makes the "annotation outlier" list look careless to domain readers, and (c) is self-defeating: REG3B is exactly the kind of neuron-derived immunoattractant that strengthens the neuroimmune-axis story the paper wants to tell. It also undermines the credibility of the other five outlier calls.

【Specific fix】 Remove REG3B from the annotation-outlier list. Reclassify it as an established DRG neuroimmune hub and cite Nie et al. 2025 and the NCBI/Gene expression annotation. Suggested sentence: "REG3B (Reg3β), a DRG-neuron-derived secreted immunoattractant shown to drive a neuronal Reg3β–macrophage TNF-α feedback loop in chronic pain (Nie et al., *Sci Adv* 2025), is a biologically coherent neuroimmune hub of this axis." The remaining five outliers (CDHR5, ANKRD1, FLNC, CRISP3, MEGF11) can stand, but see 2H on CRISP3.

---

### 1D. The ADRA2A defence is disproportionately elaborate relative to its (worst) docking performance, and the competing-interests disclosure is inadequate

【Problem】 ADRA2A carries a pending-grant competing interest yet receives the most sustained "biologically plausible" rescue narrative in the manuscript despite returning the *worst* reverse-control docking AUC of all ten targets (0.532, below chance); this asymmetry risks appearing to protect the grant narrative, and the disclosure omits the single most relevant fact — that this study's own screen did not prioritise the grant-listed target.

【Evidence】 Manuscript line 139 (Competing interests): "The author has a pending grant application (Fujian Natural Science Foundation) in which ADRA2A is listed among the candidate targets…" Yet ADRA2A is defended across Results line 54–58, Discussion line 64, 68 and 70. Key facts I verified:
- `results/tables/P3_hub_genes.csv`: ADRA2A is **not** one of the 35 hubs, so the defence is entirely extrinsic to the locked-hub set.
- `results/tables/META_DRG_axis_CORE_signature.csv`: ADRA2A is strongly up in the meta (meta_Z 4.837, consistency 1.0/6, FDR 1.5e-5) — so the biological-plausibility claim is *factually grounded* (see also § Stands up).
- `results/tables/P6_reverse_control.csv` / Supplementary Table S3: ADRA2A reverse-control AUC = **0.532** (n_known 115, reliable=0) — the only target *below* 0.5 and the weakest of all ten. Full-library AUC 0.532, p = 0.118 (NS). By contrast AXL (0.880), TNIK (0.824), ACVR1 (0.797), MAPK14 (0.779) have positive docking signal, yet they are mentioned far more briefly.
- The manuscript nonetheless asserts (line 58) ADRA2A is "biologically plausible, not-yet-docking-prioritised, hypothesis to be tested in vivo" and leans on its meta up-regulation + known α2A descending-analgesia pharmacology.

【Why it matters】 A reviewer (and a conflicts editor) will note that the one target with both a financial/grant interest *and* the worst enrichment gets the longest rescue paragraph, while better-performing targets are treated tersely. The disclosure statement's reassurance that the grant "did not influence… conclusions" is not sufficient when several paragraphs are devoted to preserving that exact target's credibility against a null result. This is the single largest credibility risk in the biology sections.

【Specific fix】 (1) Tone the ADRA2A language down to parity with other non-prioritised targets: one factual sentence, not a recurring defence. (2) Strengthen the Competing interests statement (line 139) to include the material fact: "ADRA2A is a candidate target in a pending Fujian Natural Science Foundation grant application. Notably, the present study's own prospectively specified full-library docking screen did *not* prioritise ADRA2A (full-library AUC 0.532, p = 0.118, NS; reverse-control AUC 0.532). The biological-plausibility argument below reflects the author's interpretation and is not a finding of this study." (3) In Discussion, state plainly that the docking null applies to ADRA2A no less than to the other targets and that no in-vivo claim is made here.

---

## 2. Secondary issues

### 2E. Visium "17/35 mapped to the dorsal horn" uses the wrong denominator; exclusions are inconsistent between the scRNA and Visium assays

【Problem】 The dorsal-horn fraction is reported over the full 35-hub candidate set although only 33 hubs are detectable in Visium, and the two "33/35" exclusions differ between the spinal snRNA and the Visium assays without being reconciled.

【Evidence】 Manuscript line 46 (spinal snRNA): "33/35 hubs were present (CRISP3, REG3B absent)". Manuscript line 51 (Visium): "33/35 were detectably expressed in mouse spinal cord (CRISP3 and LNP1 were below the detection threshold) and 17/35 mapped to the dorsal horn." I recomputed from `results/tables/P5_GSE325938_hub_regionalization.csv`: 35 rows total; top_region distribution = **17 DorsalHorn, 4 VentralHorn, 11 MeningealFibro, 2 Ependymal, 1 WhiteMatter** (sums to 35); the two "broad/low" (log2=0) hubs are CRISP3 and LNP1 (MeningealFibro). So the *count* 17/35 is arithmetically correct, but the honest denominator for "detectable hubs mapping to dorsal horn" is 33, not 35 (the two undetectable hubs cannot map to any region). Thus the figure should read **17/33** (51.5%) detectable, or be explicitly phrased as "17 of 35 candidate hubs (17 of 33 detectable)". Additionally the excluded members differ: scRNA drops {CRISP3, REG3B}, Visium drops {CRISP3, LNP1} — so the "35" denominator is held constant while the comparable sub-population silently changes.

【Why it matters】 Minor numerically, but it is a denominator-consistency issue a methods editor will flag, and the shifting exclusions make cross-assay comparison (scRNA vs Visium localisation) harder to parse. It also slightly inflates the apparent dorsal-horn fraction (17/35 = 48.6% vs 17/33 = 51.5%).

【Specific fix】 In line 51 report "17/33 detectable hubs (17/35 candidate hubs) mapped to the dorsal horn" and add one sentence noting the scRNA and Visium assays exclude different non-detected hubs (REG3B vs LNP1) so the two "33/35" denominators are not identical sub-sets. Apply the same denominator discipline in Table 2/Fig. 4B.

---

### 2F. "Only a minority of hubs are established DRG-injury/pain molecules" understates convergent validity

【Problem】 The manuscript restricts its "established" list to five genes (ATF3, SPRR1A, ECEL1, NPY, VIP) and implies the rest lack pain/DRG grounding, yet at least two other hubs the paper itself leans on (MAPK14/p38, AXL) have strong prior pain relevance, creating an internal inconsistency.

【Evidence】 Manuscript line 49 lists only ATF3, SPRR1A, ECEL1, NPY, VIP as established. But line 58 and Discussion line 64/68 treat MAPK14/p38 ("canonical inflammatory-pain kinase") and AXL ("microglial tyrosine kinase") as biologically plausible pain hubs — i.e., the authors *agree* these have established pain biology, yet exclude them from the "established" set. `results/tables/P3_hub_genes.csv` lists both MAPK14 (n_methods=2, in_meta_core=True) and AXL (n_methods=2, in_meta_core=True) as hubs. Domain knowledge: p38 MAPK (MAPK14) is a canonical inflammatory/neuropathic-pain kinase (ref 16, 17 cited by the authors); AXL is a TAM receptor well established in microglial/macrophage activation in pain and CNS injury.

【Why it matters】 The "minority established" framing is used to justify the large outlier/unknown set, but it is inconsistent with the paper's own later emphasis on MAPK14 and AXL. Readers may suspect the established set was kept artificially small to make the "honest outlier" narrative look stronger.

【Specific fix】 Either expand the "established/strongly-supported" category to include MAPK14 and AXL (with one-line justification each), or explicitly separate "established DRG-injury markers" (ATF3, SPRR1A, ECEL1, NPY, VIP, REG3B per 1C) from "established pain-pathway hubs not traditionally DRG-injury markers" (MAPK14/p38, AXL). Make the taxonomy explicit so the <50% "novel" claim is transparent rather than ambiguous.

---

### 2G. The human miRNA layer is framed as an "honest negative" but is more accurately an underpowered, non-significant finding

【Problem】 Reporting a set-level permutation p = 0.51 as an "honest negative boundary" oversells absence-of-evidence as evidence-of-absence and omits a power caveat appropriate to n = 60 plasma miRNA.

【Evidence】 Manuscript line 41 / abstract line 14: "The human miRNA layer was negative (set-level permutation p = 0.51)" and "We report the human layer as an honest negative boundary." `results/tables/P4_hub_miRNA_human_integration.csv` (33,394 rows) underlies the 33/35 hubs → predicted targeting miRNAs chain; `results/tables/P4_GSE158825_miRNA_LSSDS_vs_LSS.csv` is the n=60 human plasma set. The manuscript itself notes (line 41) that nominal hits "arose from miRNA non-independence and vanished under permutation" and that "direct human validation is absent." A p = 0.51 with n = 60 and a 35-hub-derived miRNA set is fully consistent with low power rather than a true null; the conclusion "no robust association" is defensible, but "negative result/boundary" implies a concluded absence.

【Why it matters】 Scientific Reports readers may interpret "honest negative" as a finding that human translation is absent, when it is really "not detected in an underpowered plasma miRNA cohort." This is the same over-claiming risk as 1A and could be read as overstating the rigour of the human boundary.

【Specific fix】 Rephrase as "no *detectable* association in an underpowered (n = 60) plasma-miRNA cohort (set-level permutation p = 0.51); this is inconclusive rather than a confirmed negative, and prospective qPCR/ELISA in accessible human biospecimens (PBMC, CSF, neuroma) is required." Add a one-line power caveat (e.g., post-hoc: with n = 60 and the observed effect, the set-level test is underpowered to exclude a small-to-moderate human signal).

---

### 2H. The CRISP3 outlier flag is defensible but rests on absence-of-evidence, not a strong negative

【Problem】 CRISP3 is flagged as an annotation outlier with no DRG/pain role; this is acceptable, but the literature search found no sensory-ganglion evidence either way, so the "outlier" label should be framed as "no current evidence" rather than confidently "no role."

【Evidence】 Manuscript line 49 groups CRISP3 with REG3B as secretory/granule proteins "with no established DRG- or pain-role." WebSearch (2026-09-20) on CRISP3/CRISP family returned only immune/secretory-tissue expression (B cells, neutrophils, eosinophils, prostate; snake-venom CRISPs as ion-channel modulators) — no DRG or sensory-neuron literature. So the absence of evidence is real, but unlike REG3B there is also no positive literature, and the CRISP family has not been systematically profiled in sensory ganglia. `results/tables/P3_hub_genes.csv`: CRISP3 is a hub (n_methods=2, in_meta_core=True) and in Visium (S2) it sits at MeningealFibro with log2=0 (broad/low), i.e., it is essentially undetectable in spinal tissue.

【Why it matters】 Low. But coupling CRISP3 with REG3B in one sentence ("CRISP3 and REG3B … have no established role") is now doubly problematic because REG3B (1C) *does* have an established role — the pair should be split. CRISP3 can remain an outlier, but the wording should not imply a confident negative.

【Specific fix】 Keep CRISP3 as an outlier but change the phrasing from "have no established DRG- or pain-role" to "lack current evidence for a DRG- or pain-related role (no sensory-ganglion literature identified)." Remove REG3B from this group entirely (see 1C).

---

## 3. § Stands up — items I checked that are correct / well-handled

1. **SCN9A/SCN10A/SCN11A down-regulation reframing is biologically correct.** The Tier-0 revision (line 33, abstract line 14) that these nociceptor sodium channels are *down*-regulated (meta_Z −3.6 to −3.1; FDR 1.7e-3–5.9e-3; 5/6 datasets down) is verified in `META_DRG_axis_CORE_signature.csv` (SCN9A meta_Z −3.475, FDR 2.25e-3; SCN10A −3.153, FDR 5.94e-3; SCN11A −3.558, FDR 1.73e-3; all consistency 0.833, 5/6 down). Transcriptomic down-regulation of Nav channels in injured DRG is the expected axotomy signature (loss of nociceptor identity in the injured cohort), so the reframing away from a naïve "ion-channel up" story is sound.

2. **Gene-set sizes are robust, not trivially small.** The prompt warns a "100% up" set of 3 genes is trivial. I confirmed from `P3_geneset_stats.csv` that Neuroinflammation is **19/19** members at 100% up (mean_Z 4.94), DAM_microglia **16/16** at 93.8% up, Complement **18/22** at 94.4% up — substantial curated sets, and the only single-member set (Sigma1, n=1) is correctly reported as non-significant (perm_p 0.466). The permutation calibration is therefore meaningful, not a small-set artefact.

3. **ADRA2A's biological-plausibility claim is factually grounded, not invented.** Although I object to the *disproportionate defence* (1D), the underlying facts are correct: `META_DRG_axis_CORE_signature.csv` shows ADRA2A strongly up (meta_Z 4.837, consistency 1.0, FDR 1.5e-5), and α2A-adrenoceptor-mediated descending noradrenergic analgesia is established pharmacology. So the rescue narrative is built on real signals — the problem is tone/asymmetry/disclosure, not fabrication.

4. **MAPK14/p38 and AXL biological-plausibility statements are correct.** p38 MAPK as a canonical inflammatory/neuropathic-pain kinase and AXL as a microglial TAM-receptor are both accurate and appropriately used (line 58, Discussion line 64). These are defensible and I do not dispute them.

5. **The "honest docking null" and prospective full-library breadth are a genuine methodological strength.** The Tier-1→full-library flip for ADRA2A (0.618 → 0.532, NS) and the 0/64 analgesics-in-Top-20 face-validity test are internally consistent with S3/S4 and represent real discipline; my concern (1D) is only about the ADRA2A-specific rescue language wrapped around an otherwise commendable null.

---

## 4. § Questions for the authors (do not guess — I need answers)

1. **On REG3B:** Do the per-dataset DEG tables (`results/tables/DEG_*.csv`) show REG3B up-regulated in the DRG bulk cohorts, and was it excluded from the "established" list before or after you became aware of the Nie et al. 2025 *Sci Adv* Reg3β–TNF-α loop? (I classify it as established per 1C, but want your read of the direction/strength in your own data.)

2. **On ADRA2A meta direction:** You cite meta_Z = 4.84, FDR 1.5e-5 for ADRA2A. Is ADRA2A's up-regulation driven by a specific model subset (e.g., the incision GSE267799 or the CCI cohorts), or uniform across all six? A stratified view would tell us whether the "biological plausibility" rests on a model-specific signal.

3. **On the "35" denominator:** For the scRNA (GSE328175) vs Visium (GSE325938) assays, why do the two non-detected hubs differ (REG3B absent in scRNA, LNP1 below-threshold in Visium)? Is LNP1 simply not expressed in spinal tissue, or a platform/annotation artefact? This determines whether "35" is the right constant denominator everywhere.

4. **On human power:** For the GSE158825 n=60 plasma-miRNA set-level test (p=0.51), what was the post-hoc power to detect a moderate effect (e.g., AUC 0.65–0.70) at the set level? I want to confirm my "underpowered/inconclusive" reading (2G) rather than assert it.

5. **On novelty scope:** Did you deliberately exclude Meng 2024 (*Sci Data* 39543146) and Dong 2025 (*Commun Biol* 39820760) from the Introduction, or were they missed? (See 1B — I believe the novelty claim must be narrowed and these cited regardless.)

---

## 5. § What I actually checked

**Files read (manuscript + supplementary only; did not open forbidden files):**
- `reports/MVP_ScientificReports_submission.md` (main manuscript, 169 lines).
- `reports/MVP_ScientificReports_supplementary.md` (Tables S1–S4).
- Authoritative CSVs in `results/tables/`: `P3_geneset_stats.csv`, `P3_hub_genes.csv`, `META_DRG_axis_CORE_signature.csv`, `P5_GSE325938_hub_regionalization.csv`, and (read-only, for cross-check) `P6_reverse_control.csv` values reproduced in S3.

**Recomputations performed:**
- **Gene-set signs/percentages (1A):** read directly from `P3_geneset_stats.csv`. Neuroinflammation mean_Z 4.9435 / frac_up 1.000 / n=19; DAM_microglia 3.8838 / 0.9375 / n=16; Complement 3.4409 / 0.9444 / n=18 of 22; Mitochondria_OXPHOS −2.3728 / frac_up 0.2632 (→73.7% down) / n=19 of 20. All four perm_p (0.0005, 0.0005, 0.0005, 0.004) match the manuscript exactly. ✔ No discrepancy.
- **Hub set & meta-core split (1C, 2F):** `P3_hub_genes.csv` contains exactly 35 hubs. `in_meta_core` is False for exactly three: REG3B, ANKRD1, MEGF11 → 32/35 in core, matching the manuscript's "32/35 (91%)". ✔ REG3B, ANKRD1, MEGF11 confirmed present as hubs; REG3B is the one with established DRG/pain literature (1C).
- **ADRA2A / SCN directions (1D, § Stands up 1&3):** from `META_DRG_axis_CORE_signature.csv`: ADRA2A meta_Z 4.837, consistency 1.0/6, FDR 1.509e-5 (UP); SCN9A −3.475/FDR 2.25e-3, SCN10A −3.153/FDR 5.94e-3, SCN11A −3.558/FDR 1.73e-3 (all DOWN, 5/6). All match the manuscript. ✔
- **Visium regionalisation (2E):** from `P5_GSE325938_hub_regionalization.csv`: 35 rows; top_region = 17 DorsalHorn + 4 VentralHorn + 11 MeningealFibro + 2 Ependymal + 1 WhiteMatter = 35. Two "broad/low" (log2=0) hubs = CRISP3 and LNP1. So 17/35 dorsal horn is arithmetically correct but the detectable denominator is 33. ✔ Count confirmed; denominator framing is the issue.

**Literature checks (WebSearch, 2026-09-20):**
- Meng X-Y et al., *Sci Data* 2024;11:1229 (PMID 39543146) — multi-tissue CPSP (skin/muscle/DRG) transcriptomics → novelty context (1B).
- Dong F-L et al., *Commun Biol* 2025;8:70 (PMID 39820760) — DRG↔spinal-cord cross-talk integration in neuropathic pain → novelty context (1B).
- Nie H et al., *Sci Adv* 2025;11(31):eadu4270 (PMID 40749060) — neuronal Reg3β–macrophage TNF-α loop in chronic pain; NCBI Gene Reg3b (DRG expression) → REG3B is established (1C).
- CRISP3/CRISP family literature → immune/secretory tissues only, no DRG evidence → outlier flag defensible (2H).

**Discrepancies / concerns surfaced (not arithmetic errors in the data, but in interpretation/framing):**
- 1A: meta-Z programme is generic injury response, not CPSP-specific (interpretation).
- 1B: novelty claim overstated; two uncited priors.
- 1C: REG3B misclassified as outlier (factual biological error).
- 1D: ADRA2A defence disproportionate + disclosure inadequate (competing-interests risk).
- 2E: Visium denominator should be 17/33, not 17/35; scRNA vs Visium exclusions differ.
- 2F: "minority established" understates MAPK14/AXL convergent validity.
- 2G: "honest negative" overstates an underpowered non-significant finding.
- 2H: CRISP3 outlier OK but should be "no current evidence," not "no role."

**No forbidden files were opened.** I did not read `REVIEW_round1_2026-09-20.md`, the submission manifest, `PROJECT_PLAN.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `README.md`, `CITATION.cff`, other reviewers' `reviews/round2_2026-09-20/*` files, or `scripts/gate_*.py`.
