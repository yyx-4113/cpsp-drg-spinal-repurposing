# A1 — Domain review (neuropathic / chronic postsurgical pain; DRG–spinal neurobiology; neuroinflammation, microglial DAM, complement-mediated synapse pruning)

**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null" (v1.4, treated as a first submission).
**Lens:** biological / clinical plausibility of every claim; literature grounding; internal consistency of the honest-null framing; coherence of the hub-localisation endpoint.

I read the main text, supplementary, cover letter and reporting summary, and re-ran / cross-checked the numbers I cite against `results/tables/` (OXPHOS frac_down, SCN meta-stats, the non-circular concordance, the ADRA2A size-independent test, the DRG finetype table). Details in § "What I actually checked."

---

## 1. MAJOR — The honest-null headline contradicts the paper's own tables on ADRA2A

【Problem】 The Abstract and cover letter state that full-library docking found "no size-independent enrichment for any of 10 tractable targets," but the manuscript's own Table 3b and Supplementary Table S4 show ADRA2A's size-independent increment is significant (ΔAUC p = 0.0005; BH q = 0.0025), and the Discussion itself calls ADRA2A "inconclusive," not a clean null.

【Evidence】 submission.md:14 (Abstract, final sentence: "Full-library docking of 3,085 drugs found no size-independent enrichment for any of 10 tractable targets (ADRA2A Tier-1 0.618 → full-library 0.532, p = 0.118)"). Same claim in cover_letter.md:11. This directly contradicts submission.md:245 (Table 3b: ADRA2A row, "Size-indep. BH q = 0.0025") and supplementary.md:130–134 (S4 Panel B: ADRA2A size-independent p = 0.0005, BH q = 0.0025), and the Discussion at submission.md:107 ("ADRA2A … its docking result is inconclusive (full-library AUC 0.532, NS; MW-adjusted 0.578)").

【Why it matters】 This is exactly the failure mode the brief warned about: an over-claim surviving in the headline after the caveat was buried elsewhere. A reader who trusts the Abstract concludes ADRA2A has zero size-independent signal, while the paper's own tables show it clears one of the two pre-specified filters (it only fails the full-library filter). The contradiction sits inside the manuscript's central methodological claim and is the single most likely thing for a third reviewer to pounce on as "your null is overstated." It also weakly undercuts the "we draw no therapeutic priority" conclusion, because ADRA2A is the one target that does show a (single-filter) significant size-independent signal.

【Specific fix】 Replace the Abstract sentence with:
> "Full-library docking of 3,085 drugs found that no target cleared both pre-specified filters — the raw/full-library MW-corrected enrichment p and the size-independent (MW-adjusted) p; ADRA2A's size-independent increment was significant (ΔAUC p = 0.0005, BH q = 0.0025) but its full-library AUC was non-significant (0.532, p = 0.118), so the ADRA2A result is inconclusive rather than a clean null."
Apply the same correction to cover_letter.md:11. The Discussion (submission.md:107) is already consistent and needs no change.

---

## 2. MODERATE — Discussion presents OXPHOS suppression as a confirmed axis component, contradicting the Abstract/gene-set tables

【Problem】 The Discussion writes OXPHOS suppression as a robust, literature-consistent part of the axis ("consistent with the growing literature on microglial–complement and energy-metabolism dysfunction in chronic and neuropathic pain"), but the Abstract and Supplementary Table S5b report it as a fixed-effect-only finding that fails random-effects set-level BH (q = 0.31).

【Evidence】 submission.md:101 (Discussion: "coordinated DAM-like microglial and complement activation plus, in the fixed-effect analysis, OXPHOS suppression, consistent with the growing literature on microglial–complement and energy-metabolism dysfunction …"). Contradicts submission.md:14 (Abstract: "OXPHOS suppression did not survive random-effects correction (q = 0.31)") and supplementary.md:173,191 (S5b: OXPHOS BH q = 0.31 under RE, "fixed-effect only"). The bulk-only OXPHOS figure (72.2% down, perm p ≤ 0.0005, submission.md:38 / META_bulkonly_sensitivity_summary.json) is real, but the random-effects failure stands.

【Why it matters】 The reader meets two different epistemic statuses for OXPHOS within one paper. The brief explicitly asks to hunt "an over-claim [that] survives somewhere (title, abstract, conclusion) after caveats were added elsewhere" — and this is it, in the Discussion. It makes the energy-metabolism claim look more settled than the authors' own sensitivity analysis supports, and invites the objection that the "neuroimmune–metabolic axis" is really a "neuroimmune axis" (metabolic limb heterogeneity-sensitive).

【Specific fix】 In submission.md:101, after "OXPHOS suppression," insert: "OXPHOS suppression is reported as a fixed-effect finding that did not survive the random-effects sensitivity analysis (set-level BH q = 0.31) and is therefore heterogeneity-sensitive rather than a confirmed axis component; we nonetheless note its direction is consistent with the established nerve-injury-induced metabolic shift toward aerobic glycolysis in DRG neurons."

---

## 3. MODERATE — "Conserved" in the title is justified only at the programme level; gene-level conservation is 24.9%

【Problem】 The title calls the response "conserved," but under the random-effects sensitivity analysis only 1,008/4,055 genes (24.9%) persist, so the *gene-level* signature is highly heterogeneity-sensitive; only the three programme-level signals (neuroinflammation/DAM/complement) are robustly conserved.

【Evidence】 submission.md:34 ("core … shrank to 1,008 genes — 24.9% of the fixed-effect core"); supplementary.md:198–208 (S6 Panel A). Title at submission.md:1. The programme-level conservation (neuroinflammation/DAM/complement q = 0.003 each under both FE and RE) is verified at supplementary.md:170–172.

【Why it matters】 "Conserved" read at the gene level overstates robustness and could be read as contradicting the authors' own 24.9% figure. Read at the programme level it is defensible and actually the stronger claim.

【Specific fix】 Either (a) keep "conserved" and add one clause in the Abstract: "the conserved component is the coordinated neuroimmune programme (neuroinflammation, DAM-microglia, complement), whereas exact gene membership is heterogeneity-sensitive (24.9% persists under random effects)"; or (b) re-title as "A nerve-injury-associated neuroimmune transcriptional response on the DRG–spinal axis …". I prefer (a) — it preserves the authors' point while pre-empting the obvious reviewer pushback.

---

## 4. MODERATE — Must-cite foundational literature is omitted for the DRG injury programme and the complement-pruning mechanism

【Problem】 The manuscript validates its DRG injury/regeneration positive controls (ATF3, SPRR1A, GAL, ECEL1, NPY, FLRT3, SOCS3) and its DAM + complement axis without citing the foundational papers that established those as the canonical nerve-injury DRG programme and the complement(C1q/C3)-mediated synaptic-pruning mechanism the axis invokes.

【Evidence】 submission.md:32 lists ATF3/SPRR1A/GAL/ECEL1/NPY/FLRT3/SOCS3 as "classic DRG injury/pain molecules" but cites only Qu 2024 (ref 4) and Pokhilko 2020 (ref 5) for the DRG programme. submission.md:101 invokes "microglial–complement … dysfunction" citing refs 15–20, none of which is the canonical complement-pruning reference (Yousefpour 2025, ref 16, is recent and good, but the mechanistic anchor — C1q/C3 microglial synaptic elimination — is un-cited). The DAM set provenance (Keren-Shaul 2017, ref 21) is cited, which is correct.

【Why it matters】 For a *Scientific Reports* mechanism paper, anchoring the positive controls and the complement-pruning claim to the primary literature is expected; omission makes the "conserved programme" look under-contextualised and weakens the novelty/robustness narrative. These are not competitive citations — they strengthen the authors' case.

【Specific fix】 Add to the Introduction or Discussion:
- Costigan, M. et al. "Replicate high-density rat genome oligonucleotide microarrays reveal hundreds of regulated genes in the dorsal root ganglion after peripheral nerve injury." *Proc. Natl. Acad. Sci. USA* **99**, 15598–15603 (2002) — the canonical DRG nerve-injury transcriptome defining the ATF3/SPRR1A/GAL/ECEL1/NPY regeneration programme now used as positive controls.
- Schafer, D. P. et al. "Microglia phagocytose live developing synapses via C1q." *Neuron* **74**, 691–705 (2012) — the foundational complement (C1q/C3)-mediated synaptic-pruning mechanism invoked by the DAM + complement axis.
- Optionally Usoskin, D. et al. "Unbiased classification of sensory neuron types …" *Nat. Neurosci.* **18**, 145–153 (2015) for DRG neuronal subtypes, and a direct spinal-complement-in-pain citation alongside Yousefpour 2025 if a pre-2025 one exists in the authors' library.
Also: the OXPHOS↓ direction should be tied to the established DRG aerobic-glycolysis switch (the authors already cite Haque 2024, ref 15, and Kong 2023, ref 17; add one foundational "DRG neuronal metabolic reprogramming toward aerobic glycolysis after nerve injury" reference if available).

---

## 5. MODERATE — CDHR5 is biologically implausible as a DRG/pain hub and should be flagged for contamination/orthology, not presented alongside true injury markers

【Problem】 CDHR5 (intestinal epithelial cadherin) is a top full-three-method-consensus hub and the single most stable dock-eligible hub (15.5% bootstrap recovery), yet it has no DRG or pain role and its DRG upregulation after nerve injury is biologically implausible; the manuscript flags it as a "candidate pending orthogonal confirmation" but does not consider a contamination or orthology explanation.

【Evidence】 submission.md:54,70 (CDHR5 "intestinal epithelial cadherin … no DRG or pain role … candidate pending orthogonal confirmation"); supplementary.md:274 (CDHR5 recovery 0.155, highest of the dock-eligible set); submission.md:70 states it is "consistently up-regulated in all four bulk contrasts (log₂FC +0.07 to +2.62)."

【Why it matters】 A gut-epithelial cadherin lighting up in bulk DRG after nerve injury is the kind of signal that, absent an explanation, reads as tissue/contaminant or orthology artifact (e.g., gut-derived immune infiltrate, or a mis-annotated ortholog). Presenting CDHR5 next to ATF3/SPRR1A inflates the candidate set's credibility and could misdirect the prospective-validation plan.

【Specific fix】 In submission.md:70, after "treated as a candidate pending orthogonal confirmation rather than as a finding," add: "Given its intestinal-epithelial annotation, we additionally consider contamination (e.g., gut-derived immune infiltrate in the injured DRG) or orthology mis-assignment as plausible explanations for the DRG signal, and recommend excluding CDHR5 from the primary prospective-validation list unless orthogonal RNAscope/qPCR confirms DRG-specific expression."

---

## 6. MODERATE — The SCN block is presented as a uniform "nerve-injury-down-regulated" finding, under-stating the Nav1.6/SCN8A literature tension

【Problem】 The manuscript reports SCN8A (Nav1.6) as nerve-injury-down-regulated (meta_Z −4.92) while citing Ding 2019 (ref 10) that Nav1.6 is transcriptionally UP-regulated in DRG after nerve injury, and frames the four SCN channels as a coherent "nerve-injury-down-regulated" block; the discrepancy is hedged only as "bulk vs protein/single-neuron level."

【Evidence】 submission.md:40 (SCN8A −4.92 / 1.0e-5, "opposite to that reported for Nav1.6/SCN8A in nerve-injury models … should not be read as contradicting that work at the protein or single-neuron level"); submission.md:101 ("the specific nociceptor sodium channels SCN9A, SCN10A, SCN11A and SCN8A were individually significant and down-regulated in nerve-injury models (SCN8A most significant …)"). The per-contrast bulk meta-stats were re-verified (META_bulkonly_sensitivity_summary.json: SCN8A bulk_meta_Z −4.9236, FDR 1.009e-5).

【Why it matters】 Nav1.6/SCN8A up-regulation in injured DRG neurons is replicated beyond Ding 2019; a bulk DRG meta-Z down-regulation of SCN8A most plausibly reflects glial/non-neuronal contributions, species, or timepoint effects, not a neuronal Nav-channel programme. Presenting all four SCN channels as a uniform "down-regulated" block, then using it to comment on "Nav-blocking strategies," risks a false mechanistic inference.

【Specific fix】 In submission.md:101, after "but inverted to up-regulation in the single incision model," add: "and the SCN8A (Nav1.6) nerve-injury down-regulation here contrasts with multiple reports of Nav1.6 up-regulation in injured DRG neurons; we therefore attribute the bulk SCN8A signal to population/species/timepoint effects and do not infer a uniform neuronal Nav-channel down-regulation programme from the bulk meta-Z." (Retain the existing incision-inversion hedge.)

---

## 7. MINOR–MODERATE — DRG "injured/regenerating neuron" co-localisation is expected programmatic convergence, not independent evidence

【Problem】 Twenty of 25 detected hubs are assigned to an "Injured_RegenNeuron" subtype, but that subtype is itself defined by classical regeneration markers (GAL, GAP43, SOX11, VGF, MMP16, CDK5R1, SCG2, NCAM1 — submission.md:62,139), so co-localising the injury hubs (SPRR1A/ATF3/ECEL1/NPY) to it partly restates that both the subtype and the hubs are the regeneration programme.

【Evidence】 supplementary.md:17–49 (S1) and the finetype table (many hubs top_finetype = Injured_RegenNeuron). submission.md:62 notes the eight annotating markers are "non-hub markers" (zero overlap with hubs) — true, so annotation circularity is correctly avoided; but the markers are themselves regeneration-associated, so convergence is expected, not discovered. The 20/25 figure was re-verified against P5_GSE216039_DRG_hub_finetype_top.csv (25 detected=True; 20 of those top_finetype = Injured_RegenNeuron).

【Why it matters】 A reviewer may read "20/25 localise to injured/regenerating neurons" as strong independent support for a DRG-neuron programme, when it is largely convergent validation. Not wrong, but should be framed as such to avoid over-interpretation.

【Specific fix】 In submission.md:62, after "20/25 localised to the injured/regenerating neuron subtype," add: "Because the injured/regenerating neuron subtype is itself defined by classical regeneration-associated markers (GAL, GAP43, SOX11, VGF, MMP16, CDK5R1, SCG2, NCAM1), the co-localisation of the injury hubs is expected programmatic convergence rather than independent anatomical evidence, and is reported as such."

---

## 8. MINOR — The dorsal-horn "pain-afferent first station" narrative overstates laminar specificity

【Problem】 The Visium result is framed as hubs being "anatomically present at the pain-afferent first station [dorsal horn]," but the two strongest DRG injury markers (SPRR1A, ECEL1) are assigned to the VENTRAL horn in Visium, and the dorsal-horn set is a subset (17/33).

【Evidence】 supplementary.md:55–66 (S2): SPRR1A top_region = VentralHorn (2.540), ECEL1 top_region = VentralHorn (1.559); both crossmodal = divergent. submission.md:66 ("anatomically present at the pain-afferent first station"). The 17/33 dorsal-horn count is correct (supplementary.md:51–92).

【Why it matters】 "Dorsal horn as the pain-afferent first station" overstates laminar restriction; these hubs are distributed across spinal laminae and the strongest DRG markers are ventral. A false anatomical claim is the kind of thing a neuroanatomy-aware reviewer flags.

【Specific fix】 In submission.md:66, replace "it shows that these hubs are anatomically present at the pain-afferent first station" with: "it shows that these hubs are anatomically present across spinal laminae, including the dorsal horn, at baseline — not that they are restricted to or enriched in the pain-afferent first station (the two strongest DRG injury markers, SPRR1A and ECEL1, localise to the ventral horn in this dataset)."

---

## 9. MINOR — Non-circular concordance figure is mis-rounded (46.3% should be 46.2%)

【Problem】 The non-circular test agreement is reported as 46.3% in the Abstract and Results, but 2,266/4,899 = 46.23%, and the manuscript's own Supplementary Table S6 reports 46.2%; the consistent figure is 46.2%.

【Evidence】 submission.md:14 (Abstract "46.3%") and submission.md:46 (Results "46.3% (2,266/4,899 …)"). Recomputed: 2,266 ÷ 4,899 = 0.46234 → 46.2%. supplementary.md:218 (S6 Panel B: "46.2%"). The background 6,779/14,390 = 47.1% is correct (recomputed 0.47103).

【Why it matters】 Numerically trivial, but a reviewer comparing the Abstract to Table S6 will see a 0.1 pp mismatch, and this manuscript's central result is a concordance proportion — internal numeric consistency matters for credibility.

【Specific fix】 Change "46.3%" to "46.2%" at submission.md:14 and submission.md:46; keep the denominator 2,266/4,899 and the Wilson CI 44.9–47.6% as in S6 (the Results currently gives 44.9–47.7%, which should also be aligned to 44.9–47.6%).

---

## 10. (Process note, not a science claim) — Fig. 3 should display only the 25 detected hubs

【Problem】 The DRG finetype table includes hubs with detected = False (e.g., GALNS, MEGF11, ANKRD1, REG3B, VIP, LNP1, SERPINE1, CCDC160, CDHR5) yet assigns them a "top_finetype"; the claim "20/25 localised" correctly counts only detected hubs, but a figure built from the full finetype table could silently include undetected hubs.

【Evidence】 P5_GSE216039_DRG_hub_finetype_top.csv (detected column); submission.md:62 ("25 passed detection; 20/25 localised"). Fig. 3 legend (submission.md:212) cites P5_GSE216039_DRG_hub_finetype_top.csv.

【Why it matters】 Minor reproducibility/clarity point — the figure must filter to detected = True so the 20/25 claim is visually faithful.

【Specific fix】 In the Fig. 3 source filter, restrict to `detected == True` (n = 25) before computing the "20/25" bar set; state the filter in the legend.

---

## § Stands up (things I suspected but found correct)

1. **Non-circular translation test is genuinely well executed and the "null" is real.** I expected the 46.3%-vs-47.1% concordance to be a soft result, but it is a correctly powered, non-circular, permutation-calibrated test: building the signature on the five nerve-injury contrasts only and holding the incision contrast out once gives 2,266/4,899 = 46.2% agreement vs a 47.1% background, permutation p = 0.14 (recomputed; supplementary.md:218). The conclusion — "knowing a gene is strongly nerve-injury-regulated carries essentially no information about its incision direction" — is defensible and is the paper's strongest, most honest contribution.

2. **The OXPHOS direction and the bulk-only fragility are correctly reported and internally consistent at the data level.** META_bulkonly_sensitivity_summary.json gives OXPHOS frac_up = 0.2778 → 72.2% down (mean_Z −2.80), exactly as submission.md:38 states. The primary meta (P3_geneset_stats.csv) gives OXPHOS frac_up = 0.2632 → 73.7% down (mean_Z −2.37), matching submission.md:36. The random-effects failure (q = 0.31) is correctly carried into the Abstract. The data support the authors' circumspection; only the Discussion wording (item 2) over-reaches.

3. **The DAM-plus-complement signal is robust and the "DAM-like" qualifier is appropriate.** Neuroinflammation/DAM/complement survive set-level BH under both fixed and random effects (q = 0.003 each; supplementary.md:170–172, re-verified). The authors' self-negative on P2RX/P2RY (perm p = 0.339/0.440) is correctly interpreted as evidence the captured state is only partially the classic P2X4-driven microglial activation — and crucially the DAM gene set (Keren-Shaul) does not include P2rx4, so the absence of a purinergic signal does not contradict the DAM set. This nuance is handled correctly and should be kept.

4. **Hub→docking-eligibility rule is decoupled from hub stability, as claimed.** The bootstrap shows 0/35 hubs reach ≥0.9 stability and the target set recovers a median of 1/17 dock-eligible hubs per resample (supplementary.md:252–301, re-read). The decision to justify the docking target list by structural tractability (n_holo_PDB ≥ 1) rather than hub rank is coherent and is the right call; the manuscript does not over-sell the docking targets as a validated ranking.

5. **SCN meta-stats are accurately transcribed.** From META_bulkonly_sensitivity_summary.json: SCN9A −2.9247/0.0108, SCN10A −3.0337/0.00795, SCN11A −3.408/0.00264, SCN8A −4.9236/1.009e-5 — matching submission.md:40 within rounding. The incision inversion (all four UP in GSE267799) is real in the data.

6. **The DRG 20/25 injured-neuron localisation is reproducible from the source table** (P5_GSE216039_DRG_hub_finetype_top.csv: 25 detected, 20 Injured_RegenNeuron), and the annotation-marker leave-one-out consistency (92–100%, ρ 0.965–0.996; P5_GSE216039_DRG_subtype_marker_LOO.csv) is genuinely high, so the subtype call is not circular at the marker level.

---

## § Questions for the authors (I am not guessing the answers)

1. **What is the actual condition/model of GSE216039, and how was the "Injured_RegenNeuron" subtype defined?** Is GSE216039 a naive DRG atlas, or does it include an injury/axotomy arm? Is "Injured_RegenNeuron" an a-priori annotated cell state or a data-driven cluster that merely expresses regeneration markers? (If the latter, item 7's "expected convergence" point is even stronger and should be stated.) I could not verify the dataset's condition from the files provided.

2. **Is GSE325938 genuinely uninjured/sham spinal cord, and how were the seven spinal regions (DorsalHorn, VentralHorn, MeningealFibro, Ependymal, WhiteMatter, etc.) anatomically annotated?** The paper flags the Ependymal region (28% of spots) as "likely a central-gray mislabel" and ATF3 as meninges — I want to know the annotation provenance before trusting the 17/33 dorsal-horn count as "anatomy."

3. **For CDHR5 (item 5):** do the authors have any orthogonal evidence (RNAscope, a second DRG dataset, or a non-gut tissue source) that CDHR5 is genuinely expressed in DRG neurons after injury, or is the all-four-contrasts upregulation consistent with a batch/contrast effect? I could not resolve this from the bulk meta alone.

4. **ADRA2A size-independent significance (item 1):** was the size-independent ΔAUC test pre-specified as a primary filter alongside the full-library filter, or added post hoc? The manuscript says the two-filter rule was pre-specified, but the reader needs to see that the size-independent filter was not retrofitted to explain ADRA2A's ambiguous result. Clarification in Methods would settle the contradiction in item 1.

5. **Human miRNA pair counts (submission.md:58, corrected values 3,511 / 752 / 328 / 253):** I did not re-verify these against P4_hub_miRNA_human_integration.csv and P4_hub_targeting_miRNAs.csv (large CSVs, not fully read). Please confirm the 3,511→752→328→253 cascade is reproducible from the deposited tables, since it is the only human-layer number I could not independently recompute.

---

## § What I actually checked

**Files read (manuscript + sources):**
- `reports/MVP_ScientificReports_submission.md` (main text) — full.
- `reports/MVP_ScientificReports_supplementary.md` — full (S1–S7).
- `reports/MVP_ScientificReports_cover_letter.md` — full.
- `reports/MVP_ScientificReports_reporting_summary.md` — full.
- `results/tables/META_bulkonly_sensitivity_summary.json` — full (OXPHOS frac_up 0.2778 → 72.2% down; SCN bulk meta_Z/FDR per gene).
- `results/tables/P3_geneset_stats.csv` — full (OXPHOS frac_up 0.2632 → 73.7% down; neuroinflammation/DAM/complement frac_up 1.0/0.9375/0.9444).
- `results/tables/P4_setlevel_test.json` — full (perm_p 0.5101 for the human miRNA layer → "p = 0.51").
- `results/tables/P5_GSE216039_DRG_hub_finetype_top.csv` — full (25 detected; 20 Injured_RegenNeuron; log2 enrich values match the 17.4×/25.7×/10.0×/10.2× in the text).
- `results/tables/P5_GSE216039_DRG_cluster_annotation.csv` — full.
- `results/tables/P5_GSE216039_DRG_subtype_marker_LOO.csv` — full (frac_same 0.92–1.0, spearman 0.965–0.996).

**Values recomputed vs the manuscript (no discrepancy unless noted):**
- OXPHOS bulk-only frac_down: source 1 − 0.2778 = 0.7222 → 72.2% (manuscript 72.2%, ✓).
- OXPHOS primary frac_down: 1 − 0.2632 = 0.7368 → 73.7% (manuscript 73.7%, ✓).
- Neuroinflammation/DAM/complement % up: 100% / 93.8% / 94.4% from frac_up 1.0/0.9375/0.9444 (✓).
- SCN bulk meta_Z/FDR: SCN9A −2.9247/0.0108, SCN10A −3.0337/0.00795, SCN11A −3.4079/0.00264, SCN8A −4.9236/1.009e-5 (manuscript −2.92/0.011, −3.03/0.008, −3.41/0.003, −4.92/1.0e-5, ✓ within rounding).
- Non-circular concordance: 2,266/4,899 = 46.23% (manuscript says 46.3% in Abstract+Results, S6 says 46.2% → manuscript mis-rounds; flagged item 9). Background 6,779/14,390 = 47.10% (✓).
- Bulk-only core overlap: 1,732/4,055 = 42.71% (manuscript 42.7%; "57.3% not recovered" = 1 − 0.4271, ✓).
- ADRA2A size-independent test: S4 Panel B / Table 3b give p = 0.0005, BH q = 0.0025 — **significant**, contradicting the Abstract/cover-letter "no size-independent enrichment" claim (item 1, the core finding).
- DRG 20/25 Injured_RegenNeuron: recomputed from finetype table (✓).
- Visium 17/33 dorsal horn: recomputed from S2 (✓); SPRR1A/ECEL1 = VentralHorn confirmed (item 8).

**Not verified (stated explicitly):** the human miRNA cascade 3,511/752/328/253 (large CSVs not fully read — see Q5); the per-resample docking-target bootstrap medians/Jaccard (taken from S7, not re-run); the GSE216039 and GSE325938 dataset conditions (no GEO metadata in the provided files — see Q1, Q2). No command failed; all cited numbers come from files I could read.
