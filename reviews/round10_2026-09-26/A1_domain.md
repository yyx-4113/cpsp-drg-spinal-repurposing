# A1 — Domain review (pain neurobiology / translational neuroscience)

**Reviewer codename:** A1
**Manuscript:** "Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null"
**Venue:** PLOS ONE (resubmission), single-author in-silico re-analysis
**Review mode:** independent first-read. I read only the manuscript, its supporting reports, and the source result tables / GEO metadata. I did not read any prior review round.

**Bottom line.** The statistical self-auditing in this paper is unusually thorough, and the numbers I recomputed from `results/tables/` reproduce the manuscript's claims almost without exception. The biology, however, is described through a framing that the data and the primary literature do not support at three critical points: (i) the "DRG–spinal axis" meta-analysis contains **no spinal-cord contrast at all**; (ii) the single "incision arm" is **two different surgical models pooled**, with a "chronic" group that mixes a pain-present (day 10) and a pain-resolved (day 32) timepoint; and (iii) the "DAM-like" label is applied to a **peripheral DRG** bulk signal using a CNS-microglial gene set whose canonical directionality is violated by the authors' own numbers. Each of these is fixable by re-scoping the claims rather than by new computation, but all three sit in the title, abstract and cover letter, so they must be fixed before acceptance.

---

## 【D1 — Major】The "DRG–spinal axis" meta-analysis contains zero spinal-cord contrasts

**【Problem】** Every one of the six meta-analysis inputs is a DRG contrast; the paper's central "axis" result is a DRG-only meta-analysis.

**【Evidence】**
- `scripts/p2_deg_meta.py:128-134`, the `primary` dictionary that defines the meta inputs:
  `GSE267799_SMIR_DRG__chronic_vs_baseline`, `GSE212311_CCI_DRG__CCI_vs_Sham`, `GSE278227_CCI_DRG__1W_IL_vs_CL_pooled`, `GSE241361_S1R_DRG__SNI_vs_Naive_WT`, plus `GSE265957_Xtail_DRG_Day4`, `GSE265957_Xtail_DRG_Day63`. All six are DRG.
- A spinal contrast **does** exist in the pipeline — `scripts/p2_deg_meta.py:103-106` computes `GSE241361_S1R_SC__SNI_vs_Naive_WT_SC` with `r["axis"]="SC"` — but it is not in `primary` and never enters the meta.
- `results/tables/META_DRG_axis_stouffer.csv` header: all six per-contrast columns are `lfc_GSE267799_SMIR_DRG`, `lfc_GSE212311_CCI_DRG`, `lfc_GSE278227_CCI_DRG`, `lfc_GSE241361_S1R_DRG`, `lfc_GSE265957_Xtail_DRG_Day4`, `lfc_GSE265957_Xtail_DRG_Day63`. No `lfc_*_SC`.
- Spinal translatome data for the same study are on disk and unused: `data/processed/GSE265957_Xtail_SC_Day4_SNI_vs_SHM.csv`, `GSE265957_Xtail_SC_Day63_SNI_vs_SHM.csv`.
- The spinal pole therefore enters only through (a) one mouse spinal fold in the ML hub step, drawn from **the same animals** as the DRG fold (manuscript, Results "35 candidate hub genes"), and (b) single-cell/spatial localisation that the manuscript itself labels "directional hints" (n = 2–3/group, 0 BH-significant genes at sample level).

**【Why it matters】** The title, the Abstract ("Conserved … response on the dorsal root ganglion–spinal axis"), the Introduction ("viewing the DRG and spinal cord not as separate tissues but as a single peripheral–central axis"), the Discussion and the cover letter all assert an axis-level result. A DRG-only meta-analysis cannot support an axis claim. This is the single largest threat to acceptance: any pain neuroscientist on the editorial board will open `META_DRG_axis_stouffer.csv`, see six DRG columns, and treat the axis framing as mislabelled. It also makes the "axis-end specialisation" discussion paragraph (Results, spinal section: "This is not a localisation failure but evidence of axis-end specialisation") uninterpretable, because the DRG pole carries the entire quantitative weight.

**【Specific fix】** Two options; pick one and apply it everywhere.

*Option A (recommended — no new computation).* Re-scope the claim to DRG and state that the spinal pole is localisation-only. Replace the title with:

> "Conserved nerve-injury-associated transcriptional response in the dorsal root ganglion: non-predictive incision translation and an honest repurposing null"

Replace Abstract Background sentence 1 with:

> "Chronic postsurgical pain affects 10–50% of surgical patients, yet DRG-level targets remain undefined. We reanalysed 12 public GEO datasets (four DRG nerve-injury contrasts and one DRG surgical-incision contrast in the meta-analysis; the remaining datasets provide single-cell, spatial, human miRNA and in-vitro layers), framing the meta-signature as a nerve-injury-associated DRG response and the incision arm as a held-out translation test."

Add to the end of the Methods "Meta-analysis" paragraph:

> "All six meta-analysis contrasts are dorsal-root-ganglion contrasts. The spinal-cord pole is represented in this study only by the GSE241361 spinal-cord fold of the hub classifier (same animals as the DRG fold) and by the single-cell and spatial localisation layers; no spinal-cord contrast enters the meta-analysis, and the meta-signature is therefore a DRG signature, not an axis-wide signature. The deposited GSE265957 spinal-cord translatome (Day 4 and Day 63) and the GSE241361 spinal-cord contrast were not included because they would leave only one or two spinal studies, below the K ≥ 3 inclusion rule."

*Option B.* Add the two GSE265957 spinal translatome contrasts and the GSE241361 spinal contrast as a seventh/eighth input and re-run. This changes every headline number and is a much larger revision; it is the only route to keep the word "axis" in the title.

---

## 【D2 — Major】The "single incision arm" is two different surgical models pooled, and the "chronic" group mixes a pain-present with a pain-resolved timepoint

**【Problem】** GSE267799 is not one model: it contains **SMIR** and **LPI** animals, and the manuscript's "chronic_vs_baseline" contrast pools both models and two harvest days, one of which is a timepoint at which the SMIR pain phenotype has resolved.

**【Evidence】**
- `data/processed/GSE267799_series_matrix.txt.gz_samples.csv`, parsed `characteristics_ch1`, DRG only:
  `('DRG','LPI','0 day') 4; ('DRG','LPI','10 day') 4; ('DRG','LPI','2 days') 4; ('DRG','LPI','6 hours') 4; ('DRG','SMIR','0 day') 4; ('DRG','SMIR','10 day') 4; ('DRG','SMIR','2 days') 4; ('DRG','SMIR','32 days') 4; ('DRG','SMIR','6 hours') 4.`
  → two models, and LPI has **no** 32-day timepoint while SMIR does.
- `data/processed/GSE267799_DRG_sampletable.csv`: `model` column = SMIR 20, LPI 16; `time_group` = acute 16, chronic 12, baseline 8.
- `data/processed/GSE267799_DRG_symbol_count.csv` column names include both `SMIR_DRG_10d_*`/`SMIR_DRG_32d_*` and `LPI_DRG_10d_*`; `scripts/p2_deg_meta.py:66-69` groups by `time_group` only, with no model term.
- `results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`: `n_case = 12`, `n_ctrl = 8` → chronic = 4 SMIR-10d + 4 SMIR-32d + 4 LPI-10d; baseline = 4 SMIR-0d + 4 LPI-0d. The manuscript reports exactly these n (Methods: "GSE267799 12/8 → 2.19"), confirming the pooling.
- The manuscript never mentions LPI anywhere (grep of `reports/MVP_PLOSONE_submission.md`: no occurrence of "LPI").
- Flatters SJL, *Pain* 2008;135(1-2):119-130, doi:10.1016/j.pain.2007.05.013 — I read the abstract: SMIR-evoked mechanical hypersensitivity "was observed by postoperative day 3, most prominent between postoperative days 10-13, persisted until at least postoperative day 22 and **had dissipated by postoperative day 32**."

**【Why it matters】** Two consequences, both biological. First, the model × time design is confounded: 8 of 12 "chronic" samples are SMIR (including the 4 at day 32) and 4 of 12 are LPI (day 10 only), so the "chronic postsurgical pain" contrast is partly a model contrast and partly a resolved-pain contrast. Second — and worse for the CPSP framing — one third of the "chronic" group (4/12) is harvested at a day when the defining behavioural phenotype of SMIR has dissipated. A "chronic postsurgical pain" transcriptome that includes pain-resolved animals is not a chronic-pain transcriptome. This directly undermines the cover letter's "reproducible benchmark for the chronic postsurgical pain … axis" and the manuscript's claim that GSE267799 is "CPSP-closest".

**【Specific fix】** Add to Methods, immediately after the sentence "GSE267799 chronic vs baseline":

> "GSE267799 contains two surgical models rather than one: skin/muscle incision and retraction (SMIR; 20 DRG libraries, timepoints 0 d, 6 h, 2 d, 10 d, 32 d) and a second incisional model annotated 'LPI' in the deposition (16 DRG libraries; 0 d, 6 h, 2 d, 10 d — no 32 d timepoint). The primary 'chronic vs baseline' contrast (n = 12 vs 8) therefore pools both models and both the 10-day and 32-day harvests, because stratifying by model leaves n = 4 per cell. We report it as a pooled postsurgical-incision contrast and do not attribute it to either model individually. In SMIR, mechanical hypersensitivity is reported to be maximal at postoperative days 10–13 and to have dissipated by postoperative day 32 (Flatters 2008), so the four day-32 libraries are from animals in which the pain phenotype is expected to have resolved; a sensitivity contrast restricted to day 10 (n = 8 vs 8) is reported in Supplementary Table S6 and all incision-arm conclusions are unchanged / [state which change, if any]."

And run and report the day-10-only and the SMIR-only contrasts. If the authors cannot run them, delete every occurrence of "chronic" in connection with GSE267799 and rename the arm "pooled postsurgical-incision (day 10 and day 32, two models)".

---

## 【D3 — Major】The manuscript's own harvest-day caveat is factually wrong

**【Problem】** The manuscript states the chronic harvest day "is not stated in the deposited metadata and could not be verified"; it is stated.

**【Evidence】** Manuscript Methods, "GSE267799 harvest-day caveat" (line 152): "the source GEO annotates acute and chronic incision timepoints; the exact chronic harvest day is not stated in the deposited metadata and could not be verified from the reanalysed matrix". Against this: `GSE267799_series_matrix.txt.gz_samples.csv` carries `time: 10 day` and `time: 32 days` in `characteristics_ch1` for every sample, and the repository's own `GSE267799_DRG_sampletable.csv` carries `time_label` = `0d/6h/2d/10d/32d`.

**【Why it matters】** A reader who checks GEO will find the caveat false, and a false "unverifiable" claim costs more credibility than the underlying uncertainty would have. It also conceals the day-32 problem in D2.

**【Specific fix】** Delete the sentence and replace with:

> "The deposited GSE267799 metadata annotate five harvest points (0 d, 6 h, 2 d, 10 d and 32 d) for SMIR and four (0 d, 6 h, 2 d, 10 d) for LPI. We pooled 10 d and 32 d into the 'chronic' stratum (see above); the 32 d timepoint lies beyond the window in which SMIR-evoked hypersensitivity is reported to persist (Flatters 2008)."

---

## 【D4 — Major】The incision arm's defining biological property — absence of neuronal damage — is never stated, and it largely explains the "non-predictive translation" headline

**【Problem】** The meta core is an axotomy/regeneration programme; the incision model used as the held-out test is, by construction, a model in which DRG neurons are not damaged. The failure to translate is therefore close to a foregone consequence of model choice, not a discovery about CPSP biology.

**【Evidence】**
- The manuscript's own positive controls are the canonical regeneration-associated genes (RAGs) of axotomised DRG: ATF3, SPRR1A, GAL, ECEL1, NPY, FLRT3, SOCS3 (manuscript Results, first paragraph). ATF3, SPRR1A, GAL, NPY are textbook markers of the axotomy response, not of pain per se.
- Recomputed per-contrast log₂FC from `META_DRG_axis_stouffer.csv` (incision | CCI-212311 | CCI-278227 | SNI-241361):

| Gene | incision | GSE212311 | GSE278227 | GSE241361 |
|---|---|---|---|---|
| ATF3 | +0.80 | +2.92 | +4.93 | +5.89 |
| SPRR1A | +0.50 | +1.84 | +3.32 | +9.04 |
| GAL | +0.57 | +3.93 | +4.67 | +6.47 |
| ECEL1 | +0.50 | +0.94 | +3.37 | +6.25 |
| NPY | +0.30 | +5.18 | +7.31 | +6.94 |

  The incision arm mounts 4–18× smaller inductions of every one of these genes.
- Flatters 2008 (doi:10.1016/j.pain.2007.05.013), abstract: "In addition, very little to no degeneration was detected with ATF3 staining in DRG from SMIR-operated rats. These data suggest that prolonged retraction of superficial tissue evokes a persistent pain syndrome that is not driven by neuronal damage."

**【Why it matters】** The paper's headline — "non-predictive incision translation" (in the title) — is presented as a substantive negative finding about CPSP relevance. In fact, comparing an axotomy-driven transcriptional programme against a non-axotomising model is close to guaranteed to fail. Without stating this, the paper risks being read as evidence that nerve-injury biology is irrelevant to postsurgical pain, which the data cannot support and which is not what the authors intend. Conversely, stating it makes the paper stronger: the failure becomes a well-explained boundary rather than an unexplained one.

**【Specific fix】** Insert into the "Translation to the incision model" section, after the non-circular result:

> "This negative translation result has a straightforward mechanistic explanation that we state explicitly so that it is not over-read. The meta core is dominated by the axotomy/regeneration programme of injured sensory neurons (ATF3, SPRR1A, GAL, ECEL1, NPY, FLRT3, SOCS3), and the incision arm is a skin/muscle incision-and-retraction model in which DRG neurons are reported not to degenerate: ATF3 staining in DRG of SMIR-operated rats is minimal and the model is explicitly described as a persistent pain state 'not driven by neuronal damage' (Flatters 2008). Consistently, the incision contrast induces each of these genes 4–18-fold more weakly than the nerve-injury contrasts (ATF3 +0.80 vs +5.89 log₂; SPRR1A +0.50 vs +9.04; NPY +0.30 vs +7.31). The non-predictive result is therefore partly a consequence of comparing an axotomy programme against a non-axotomising model, and it should not be read as evidence that nerve-injury biology is irrelevant to postsurgical pain, nor as a positive demonstration of CPSP specificity."

And add to the Abstract Conclusions:

> "…the nerve-injury signature does not predict the single surgical-incision arm (46.2% vs 47.1% background, p = 0.14), a result that is partly expected because the core is an axotomy/regeneration programme while the incision model does not damage DRG neurons."

---

## 【D5 — Major】"DAM-like" is over-claimed: the canonical DAM directionality is violated by the authors' own numbers, and a microglial gene set is being applied to a ganglion that contains no microglia

**【Problem】** The manuscript's Discussion quotes only three DAM genes (TYROBP, TREM2, APOE) and concludes the DAM descriptor is "data-supported"; recomputing the full 16-member DAM set and the canonical homeostatic arm shows the programme is substantially anti-DAM, and the tissue is peripheral ganglion, not CNS.

**【Evidence】** All values recomputed from `results/tables/META_DRG_axis_stouffer.csv` (six-input primary meta). The manuscript's three quoted genes reproduce exactly (TYROBP FDR 8.807e-9, K = 5, 5 up / 0 down; TREM2 FDR 1.299e-3, K = 6, 5 up / 1 down; APOE FDR 6.973e-2, 6 up / 0 down) — this part is correct.

Full `DAM_microglia` set (`results/tables/_R4_geneset_members.json`: TREM2, APOE, TYROBP, CST7, LPL, CTSD, SPP1, GPNMB, ITGAX, AXL, MERTK, CD68, CSF1R, C1QA, C1QB, C1QC), core = FDR < 0.05 and consistency ≥ 0.8:

| Member | meta_Z | meta_FDR | up/down | core? |
|---|---|---|---|---|
| TREM2 | +3.65 | 1.3e-3 | 5/1 | up-core |
| APOE | +2.16 | 7.0e-2 | 6/0 | **no (FDR)** |
| TYROBP | +6.36 | 8.8e-9 | 5/0 | up-core |
| CST7 | +3.39 | 3.0e-3 | 3/1 | **no (cons 0.75)** |
| **LPL** | **−3.43** | **2.6e-3** | **1/5** | **DOWN-core** |
| CTSD | +1.24 | 3.3e-1 | 4/2 | no |
| SPP1 | +4.38 | 9.7e-5 | 3/3 | no (cons 0.50) |
| GPNMB | +2.71 | 2.0e-2 | 4/2 | no (cons 0.67) |
| ITGAX | +4.90 | 1.2e-5 | 5/1 | up-core |
| AXL | +6.14 | 2.9e-8 | 6/0 | up-core |
| MERTK | +2.03 | 8.9e-2 | 4/2 | no |
| CD68 | +4.92 | 1.0e-5 | 5/1 | up-core |
| CSF1R | +4.60 | 4.1e-5 | 5/1 | up-core |
| C1QA | +5.85 | 1.4e-7 | 5/1 | up-core |
| C1QB | +6.22 | 1.9e-8 | 6/0 | up-core |
| C1QC | +7.03 | 1.9e-10 | 5/0 | up-core |

→ 9/16 up-and-core; **1/16 significantly DOWN** (LPL, FDR 0.0026, 5 of 6 contrasts down); 6/16 not core.

The canonical DAM/MGnD transition is defined as *down*-regulation of the homeostatic module with *up*-regulation of APOE, CTSD, LPL, TYROBP, TREM2 (Krasemann et al., *Immunity* 2017;47(3):566-581.e9, doi:10.1016/j.immuni.2017.08.008; Deczkowska et al., *Cell* 2018;173(5):1073-1081, doi:10.1016/j.cell.2018.05.003 — homeostatic genes listed there are *P2ry12, P2ry13, Cx3cr1, CD33, Tmem119*). In this data every one of these is **up**, not down:

| Homeostatic gene | meta_Z | meta_FDR | up/down |
|---|---|---|---|
| CX3CR1 | +6.48 | 4.7e-9 | **6/0 up** |
| CD33 | +4.84 | 1.5e-5 | 5/1 up |
| TMEM119 | +3.63 | 1.4e-3 | 5/1 up |
| P2RY12 | +3.23 | 4.7e-3 | 3/3 |

And the canonical DAM-up gene **CD9** (not in the authors' set) is also down: meta_Z −2.01, 2 up / 4 down.

Finally, the tissue: all six meta contrasts are DRG (see D1). DRG contains macrophages and monocytes, not microglia. The canonical paper for the DRG myeloid compartment is Yu X, Liu H, Hamel KA, Morvan MG, Yu S, Leff J, Guan Z, Braz JM, Basbaum AI. "Dorsal root ganglion macrophages contribute to both the initiation and persistence of neuropathic pain." *Nature Communications* 2020;11(1):264. doi:10.1038/s41467-019-13839-2 — **not cited anywhere in the manuscript**.

**【Why it matters】** As written, the paper tells a pain audience that nerve injury recruits a "DAM-like microglial programme" in the DRG–spinal axis. A reader who checks the genes will find that the homeostatic arm that defines DAM moves in the wrong direction, that a canonical DAM-up gene (LPL) is significantly down, and that the tissue has no microglia. The claim is defensible only as "a TREM2/TYROBP/C1Q-positive myeloid-macrophage programme in the DRG", which is a different and more accurate statement. The manuscript's own hedge ("cannot be attributed specifically to resident microglia versus infiltrating macrophages") is immediately undercut by the Discussion sentence that follows (see D9c).

**【Specific fix】**
1. Rename the gene set `DAM_microglia` → `DAM_like_myeloid` in `Results`, Fig. 1 legend, and Supplementary Table S5, and add `P2RY12, P2RY13, CX3CR1, TMEM119, CD33, CD9, CTSD` reporting.
2. Replace the Discussion sentence beginning "To quantify the 'DAM-like' qualifier…" with:

> "To quantify the 'DAM-like' qualifier we checked all 16 members of the set, not only the three hallmarks, against the Stouffer meta vector, and we checked the homeostatic arm that defines the DAM/MGnD switch. Nine of sixteen members are up-regulated and core-significant (TYROBP, TREM2, ITGAX, AXL, CD68, CSF1R, C1QA, C1QB, C1QC); six are not (APOE meta_FDR 0.070; CST7 consistency 0.75; CTSD FDR 0.33; SPP1 consistency 0.50; GPNMB 0.67; MERTK FDR 0.089); and one canonical DAM-up member, LPL, is significantly **down**-regulated (meta_Z −3.43, FDR 0.0026, 5 of 6 contrasts down). The homeostatic module that DAM is defined by suppressing is coordinately **up**-regulated here, not down (CX3CR1 meta_Z +6.48, 6/6 contrasts up, FDR 4.7e-9; CD33 +4.84; TMEM119 +3.63; P2RY12 +3.23, 3 up/3 down). The programme captured here is therefore a TREM2/TYROBP/C1Q-positive myeloid activation with only partial and partly inverted correspondence to the neurodegeneration-defined DAM/MGnD state, and we use 'DAM-like' strictly in that qualified sense. Because all six meta contrasts are dorsal-root-ganglion contrasts, the most likely cellular source is the injury-expanded DRG macrophage/monocyte compartment rather than microglia, which are absent from the ganglion; we therefore do not describe this as a microglial state."

3. Cite Yu et al. 2020 (doi:10.1038/s41467-019-13839-2) and Krasemann et al. 2017 and Deczkowska et al. 2018 alongside Keren-Shaul et al. 2017 wherever "DAM-like" appears.

---

## 【D6 — Major】GSE265957 is described as "tibial-nerve-injury"; it is spared nerve injury (SNI)

**【Problem】** A wrong model label, repeated in the Results and the Methods, that also creates a phantom third model class in the Introduction.

**【Evidence】**
- Manuscript Results line 44: "one tibial-nerve-injury study, GSE265957"; Methods line 144: "one tibial-nerve-injury study, GSE265957"; Introduction line 36: "spanning incision, nerve-injury and tibial-nerve-injury models in rat, mouse and human."
- `data/processed/GSE265957-GPL21103_series_matrix.txt.gz_samples.csv`, `treatment_protocol_ch1`: "**Spared nerver injury** or sham surgery was performed on mice and was followed by eithanization and dissection of tissue at day 4 for early time point and at day 60 or day 63 for late time point." Sample titles: `DRG_D04_SNI_101_mRNA`, `SC_D04_SNI_201_mRNA`, etc. Deposited files: `GSE265957_Xtail_DRG_Day4_SNI_vs_SHM.csv`. `organism_ch1` = *Mus musculus*, growth protocol = female C57BL/6.
- SNI (Decosterd & Woolf, spared nerve injury: tibial + common peroneal ligated/transected, sural spared) and TNI (tibial nerve injury/cut) are different models with different injury severities; the deposition says SNI.

**【Why it matters】** Model identity is the primary biological metadata of the paper. Mislabelling SNI as "tibial-nerve-injury" will be caught immediately, and it inflates the apparent model diversity ("three classes") that the paper uses to justify the meta-analysis.

**【Specific fix】**
- Results line 44: replace "one tibial-nerve-injury study, GSE265957" with "one spared-nerve-injury (SNI) study, GSE265957".
- Methods line 144: same replacement.
- Introduction line 36: replace "spanning incision, nerve-injury and tibial-nerve-injury models in rat, mouse and human" with "spanning surgical incision, chronic constriction injury (CCI) and spared nerve injury (SNI) in rat and mouse, plus human plasma miRNA and human cell-line layers".
- Add to the Methods dataset list: "GSE265957: mouse (female C57BL/6) spared nerve injury, DRG and spinal-cord ribosome profiling at day 4 and day 63; only the DRG contrasts enter the meta-analysis."

---

## 【D7 — Major】Reference 11 is misattributed, and the SCN3A claim in the next sentence is both uncited and factually wrong about the authors' own gene set

**【Problem】** Three linked errors in one paragraph: ref 11 does not say what it is cited for; the SCN3A sentence cites nothing (although ref 11 is exactly the right citation); and the claim that SCN3A "was not among the tested sets" is false.

**【Evidence】**
- Manuscript Results "SCN-channel directions" (line 52): "SCN10A/Nav1.8 mRNA is down-regulated in axotomized IB4+ neurons¹¹". Reference 11 = Yin R, Liu D, Chhoa M, Li CM, Luo Y, Zhang M, Lehto SG, Immke DC, Moyer BD. *Int J Neurosci* 2016;126(2):182-192, doi:10.3109/00207454.2015.1004172 (verified). Its abstract: "experiments were performed to elucidate the contribution of Nav channels to sodium currents in rat DRG neurons following the **L5/L6 spinal nerve ligation (SNL)** model… **Scn10a (Nav1.8) and Scn11a (Nav1.9) expression was twenty- to thirty-fold lower**, while among Nav transcripts encoding TTX-S channels, **Scn3a (Nav1.3) expression was four-fold higher** in injured compared to uninjured DRG **by qRT-PCR analysis**." There is no IB4⁺ sorting and no IB4⁺ attribution anywhere in that paper; the comparison is injured vs contralateral whole DRG.
- Same paragraph, next sentence: "Notably, the channel most transcriptionally induced after injury, SCN3A/Nav1.3, was not among the tested sets and should be examined in a revision." Two errors. (a) `results/tables/_R4_geneset_members.json` → `Nav_SCN` = [SCN1A, SCN2A, SCN3A, SCN4A, SCN5A, SCN7A, SCN8A, SCN9A, SCN10A, SCN11A, SCN1B, SCN2B, SCN3B, SCN4B] — **SCN3A is a member of the tested Nav set**. (b) In this dataset SCN3A is not the most induced channel: `META_DRG_axis_stouffer.csv` gives SCN3A meta_Z +3.95, FDR 4.70e-4, 4 up / 2 down, and it is **down** (−0.884 log₂) in the GSE241361 SNI contrast. The most consistently down-regulated channel here is SCN8A (meta_Z −4.92).
- Ref 11 is in fact the correct citation for the SCN3A sentence.

**【Why it matters】** A misattributed citation in the one paragraph where the paper engages directly with sodium-channel biology is exactly what a pain-pharmacology reviewer will check first. And the SCN3A sentence is self-contradictory: the authors say a gene is missing from their gene sets when it is listed in them.

**【Specific fix】** Replace the two sentences with:

> "These bulk transcriptome-level down-regulations are consistent with, rather than contradictory to, the known biology of injured DRG: in the L5/L6 spinal nerve ligation model, *Scn10a* (Nav1.8) and *Scn11a* (Nav1.9) transcripts are 20–30-fold lower and *Scn3a* (Nav1.3) is 4-fold higher in injured versus contralateral DRG by qRT-PCR¹¹, and bulk DRG signal is additionally confounded by injury-induced sensory-neuron loss¹² and by dilution of neuronal transcripts by infiltrating immune and glial cells. We did not resolve these channels by neuronal subpopulation (for example IB4-positive non-peptidergic nociceptors), so the present result is a whole-ganglion average and cannot be attributed to a specific neuronal class. Notably, SCN3A/Nav1.3 — the channel reported as transcriptionally *induced* after axotomy¹¹ — is a member of our Nav_SCN set and behaves differently again in this collection (meta_Z +3.95, meta_FDR 4.7e-4, up in 4 of 6 contrasts but down 0.884 log₂ in the SNI contrast), so the direction of the Nav family is channel- and model-specific rather than uniform."

---

## 【D8 — Major】Must-cite literature is missing, including the paper that defines the incision model the whole translation test rests on

**【Problem】** The manuscript reanalyses a skin/muscle incision-and-retraction dataset without ever citing the paper that defines it, applies a myeloid DAM programme to DRG without citing the DRG-macrophage literature, and cites only one source (Macrae 2008) for a CPSP epidemiology figure that belongs to Kehlet, Jensen & Woolf 2006.

**【Evidence / exact citations】** All verified by me this session unless marked "verify".

Missing and required:
1. **Flatters SJL.** "Characterization of a model of persistent postoperative pain evoked by skin/muscle incision and retraction (SMIR)." *Pain* 2008;135(1-2):119-130. **doi:10.1016/j.pain.2007.05.013** — verified (PubMed 17590272). Must be cited at first mention of GSE267799 / the incision arm; it is also the source of the day-32 resolution and the no-neuronal-damage facts used in D2 and D4.
2. **Yu X, Liu H, Hamel KA, Morvan MG, Yu S, Leff J, Guan Z, Braz JM, Basbaum AI.** "Dorsal root ganglion macrophages contribute to both the initiation and persistence of neuropathic pain." *Nature Communications* 2020;11(1):264. **doi:10.1038/s41467-019-13839-2** — verified (PMID 31937758). Must be cited wherever TREM2/APOE/C1Q/CSF1R/AXL are interpreted in DRG.
3. **Krasemann S, Madore C, Cialic R, et al.** "The TREM2-APOE Pathway Drives the Transcriptional Phenotype of Dysfunctional Microglia in Neurodegenerative Diseases." *Immunity* 2017;47(3):566-581.e9. **doi:10.1016/j.immuni.2017.08.008** — verified. The TREM2–APOE axis paper; directly relevant because the authors use TREM2/APOE/TYROBP as their DAM hallmarks.
4. **Deczkowska A, Keren-Shaul H, Weiner A, Colonna M, Schwartz M, Amit I.** "Disease-Associated Microglia: A Universal Immune Sensor of Neurodegeneration." *Cell* 2018;173(5):1073-1081. **doi:10.1016/j.cell.2018.05.003** — verified. The canonical DAM review; the manuscript cites only the 2017 primary paper.
5. **Kehlet H, Jensen TS, Woolf CJ.** "Persistent postsurgical pain: risk factors and prevention." *Lancet* 2006;367(9522):1618-1625. **doi:10.1016/S0140-6736(06)68700-X** — verified (PMID 16698416). This is the canonical source of the "10–50%" figure the manuscript attributes solely to Macrae 2008, and it is the standard CPSP citation. Must be added to Introduction sentence 1.
6. **Osteen JD, Immani S, Tapley TL, et al.** "Pharmacology and mechanism of action of suzetrigine, a potent and selective NaV1.8 pain signal inhibitor for the treatment of moderate to severe pain." *Pain Ther* 2025;14:655-674 (PMID 39775738) — the primary pharmacology paper for suzetrigine; the manuscript cites only a phase-3 report and a 2026 review.
7. **Brennan TJ, Vandermeulen EP, Gebhart GF.** "Characterization of a rat model of incisional pain." *Pain* 1996;64(3):493-501 — the canonical incisional-pain model and the likely identity of the "LPI" arm. **Verify volume/pages/DOI before use.**
8. **Werner MU, Kongsgaard UE / Perkins FM & Kehlet H** ("Persistent pain after surgery"; *Anesthesiology* 2000;93:1123-1133) — cited inside Flatters 2008 as the source of CPSP incidence ranges. *Verify before use.*

Also conspicuously absent from a paper about neuroimmune activation in neuropathy: **Ji RR, Chamessian A, Zhang YQ.** "Pain regulation by non-neuronal cells and inflammation." *Science* 2016;354(6312):572-577 (doi:10.1126/science.aaf8924 — *verify DOI*) and **Grace PM, Hutchinson MR, Maier SF, Watkins LR.** "Pathological pain and the neuroimmune interface." *Nature Reviews Immunology* 2014;14(4):217-231 (*verify*). And for early DRG nerve-injury transcriptomics, alongside the cited Xiao 2002 PNAS: **Costigan M, Befort K, Karchewski L, et al.** "Replicate high-density rat genome oligonucleotide microarrays reveal hundreds of regulated genes in the dorsal root ganglion after peripheral nerve injury." *BMC Neuroscience* 2002;3:16 (*verify*).

**【Why it matters】** PLOS ONE reviewers routinely check whether the primary literature for the models and the programmes used is cited. The absence of Flatters 2008 is the most damaging, because the entire "incision" half of the paper rests on a model the manuscript never defines or credits; a referee will read that as the authors not knowing what model they reanalysed — which, given D2 and D3, is a fair reading.

**【Specific fix】** Add to Introduction sentence 1:

> "Chronic postsurgical pain (CPSP) develops in 10–50% of surgical patients¹,⁵⁰ and persists beyond the normal healing window…"

with new reference 50 = Kehlet/Jensen/Woolf 2006. Add to Introduction sentence 2 (after "DRG-centred studies cluster in nerve-injury or constriction models rather than surgical incision⁴,⁵"):

> "…rather than surgical incision⁴,⁵; the incision models used here — skin/muscle incision and retraction (SMIR)⁵¹ and plantar incision⁵² — were developed specifically to reproduce persistent postsurgical pain without transecting a nerve."

with 51 = Flatters 2008, 52 = Brennan 1996. Add Yu 2020, Krasemann 2017 and Deczkowska 2018 to the Discussion DAM paragraph (see D5 fix). Add Osteen 2025 next to references 22–23.

---

## 【D9 — Major】Disclosure ≠ resolution: five places where a conceded limitation is still asserted elsewhere in unqualified form

Each row gives the conceded (hedged) text and the unqualified text, both from the manuscript as submitted.

**(a) "Nerve-injury-specific" is *established* from a non-significant result.**
- Conceded (Results, translation section, line 58): "Specificity of the axis to postsurgical versus nerve-injury pain is therefore not shown by this meta-analysis, and the axis is described as a nerve-injury-associated response throughout."
- Unqualified (Results, hub section, line 64): "the pivotal incision fold (GSE267799 n = 20) falls to a leakage-controlled 0.677 [0.374, 0.940], a confidence interval that includes chance, **establishing that the axis is a nerve-injury-specific response rather than a universal pain signature**."
- Also (same paragraph): "Honest evaluation confirmed a **nerve-injury-specific — not universally generalisable** — LODO signal."

**【Why it matters】** The word "establishing" converts a null (AUC CI spanning 0.374–0.940) into a positive claim, and it contradicts the paper's own translation section and its Abstract. A null cannot establish specificity.

**【Specific fix】** Replace "a confidence interval that includes chance, establishing that the axis is a nerve-injury-specific response rather than a universal pain signature" with:

> "a confidence interval that includes chance; the incision fold is therefore non-informative, and we do not claim that the axis is nerve-injury-specific on this evidence — we report only that generalisation to the incision model is not established."

Replace "Honest evaluation confirmed a nerve-injury-specific — not universally generalisable — LODO signal" with:

> "Honest evaluation shows that the LODO signal is confined to held-out nerve-injury datasets and does not extend to the incision dataset."

**(b) Neuronal-loss dilution is invoked for sodium channels only, then ignored for OXPHOS and synaptic genes.**
- Conceded (Results, SCN paragraph, line 52): "bulk DRG signal is confounded by injury-induced neuronal atrophy/loss¹² and by the dilution of neuronal transcripts by infiltrating immune and glial cells."
- Unqualified (Results, gene-set paragraph, line 48): "mitochondrial OXPHOS was downregulated (mean_Z −2.37, 73.7% of members down, q = 0.020)" — reported with no cell-composition caveat; and (Discussion, line 120) "OXPHOS suppression … consistent with the growing literature on microglial–complement and **energy-metabolism dysfunction** in chronic and neuropathic pain²⁴,²⁵,²⁸,²⁹,³⁰,³¹."
- Recomputed: the `Synaptic` set is also coordinately down (mean_Z −1.41, 45% up) and the strongest single OXPHOS members are uniformly down (NDUFS1 −6.55, 0 up / 6 down; SDHA −5.48, 0/6; ATP5F1B −5.09, 0/4; ATP5MC1 −4.05, 0/4; UQCRC2 −4.74).

**【Why it matters】** Loss of neurons and dilution by immune cells *mechanically* lowers the neuronal transcript fraction, and neurons are the most mitochondria-dense cells in the ganglion. The OXPHOS result and the synaptic result are the two most likely to be entirely compositional. Presenting one confounder for the SCN genes and not for the metabolic genes is selective.

**【Specific fix】** Append to the OXPHOS sentence in Results:

> "Because the same injury-induced sensory-neuron loss and immune-cell dilution that we invoke below for sodium channels also reduces the neuronal (mitochondria-rich) fraction of the ganglion, the OXPHOS and synaptic (mean_Z −1.41) suppressions are compositional as well as regulatory in origin and cannot be interpreted as a cell-intrinsic metabolic switch without cell-type-resolved or neuron-count-normalised data."

**(c) "Not attributable to microglia vs macrophages" is conceded, then six microglial papers are cited for the same signal.**
- Conceded (Results, line 48): "Because this is a bulk-tissue gene-set signal, it cannot be attributed specifically to resident microglia versus infiltrating macrophages or other neuroimmune cells; 'DAM-like' denotes the shared transcriptional programme, not a cell-type-resolved state."
- Unqualified (Discussion, line 120): "coordinated **DAM-like neuroimmune** and complement activation²¹,²⁴,²⁵ … consistent with the growing literature on **microglial**–complement and energy-metabolism dysfunction in chronic and neuropathic pain²⁴,²⁵,²⁸,²⁹,³⁰,³¹" — and Fig. 1 legend and Supplementary S5 both label the set "DAM **microglia**".

**【Specific fix】** See D5 fix 2 (the replacement paragraph states the macrophage source explicitly). In addition, change the set label to "DAM-like myeloid" in Fig. 1, the Fig. 1 legend and Supplementary Table S5.

**(d) OXPHOS does not survive random effects — but is still narrated as a finding in the Discussion.**
- Conceded (Results, line 48): "OXPHOS did not survive random-effects correction (q = 0.31), so energy-metabolism suppression is reported as a fixed-effect finding that is not reliable under between-contrast heterogeneity."
- Unqualified (Discussion, line 120): "In the fixed-effect analysis only, OXPHOS suppression (which did not survive random-effects correction, q = 0.31), **consistent with the growing literature on … energy-metabolism dysfunction in chronic and neuropathic pain**²⁴,²⁵,²⁸,²⁹,³⁰,³¹" — the hedge is a parenthesis around an affirmative claim of consistency with six papers. Abstract line 18 is cleaner ("OXPHOS did not survive random-effects correction (q = 0.31)").

**【Specific fix】** Replace the Discussion clause with:

> "OXPHOS suppression was present under fixed effects only and did not survive random-effects correction (q = 0.31); we therefore do not claim it, and we note only that, were it real, it would be compatible with reports of metabolic dysfunction in chronic and neuropathic pain²⁴,²⁵,²⁸,²⁹,³⁰,³¹ — a conditional statement, not a finding."

Also note that reference 30 (Kong et al. 2023) reports microglial **glycolysis enhancement**, not OXPHOS suppression, so it is not supporting evidence for the direction reported here; either drop it from that citation list or say so.

**(e) "Not a localisation failure" converts a localisation null into a positive finding.**
- Conceded (Results, spinal section, line 76): "Only 7/35 achieved cross-dataset lineage-consistent localisation (…) 15 NotLocalisable."
- Unqualified (same sentence): "**This is not a localisation failure but evidence of axis-end specialisation**: the DRG pole is an injured-neuron programme, the spinal pole disperses across neuronal/glial/immune compartments."

**【Why it matters】** 15 of 35 hubs could not be localised at all, and sample-level pseudobulk gave 0 BH-significant genes in both single-cell datasets (n = 2–3/group). "Specialisation" is one of several explanations for non-localisation; others include dropout, ambient RNA and power. Asserting one is an interpretive upgrade of a null.

**【Specific fix】** Replace with:

> "Fifteen of 35 hubs were not localisable in either spinal dataset and only 7/35 were lineage-consistent across datasets. Axis-end dispersion is one explanation for this pattern; non-detection at this sequencing depth, ambient RNA and the small per-group n are equally compatible, and sample-level pseudobulk gave 0 BH-significant genes in both datasets (n = 2–3/group). We therefore record the 7 lineage-consistent hubs as the only spinal localisation we would act on, and treat dispersion as a hypothesis, not a demonstrated property of the axis."

---

## 【D10 — Major】The spatial result is selectively reported: the second-largest regional block (meningeal/fibroblast, 11/35) is never quantified

**【Problem】** The manuscript headlines 17/33 hubs "assigned to the dorsal horn" but never reports that 11 hubs have their maximal expression in the meninges/fibroblast region — a block nearly as large, and biologically implausible for a DRG-neuron-derived programme.

**【Evidence】** `results/tables/P5_GSE325938_hub_regionalization.csv`, `top_region` counts over all 35 hubs: `DorsalHorn 17, MeningealFibro 11, VentralHorn 4, Ependymal 2, WhiteMatter 1`. The manuscript mentions the meningeal block only for ATF3 (Results, spatial section: "ATF3 localised to meninges (not dorsal-horn neuron), consistent with its ambient downgrade") and dismisses the ependymal block as a likely mislabel, but never reports the 11/35 count.

**【Why it matters】** A reader who sees "17/33 (51.5%) in the dorsal horn" will read it as dorsal-horn enrichment. The countervailing fact — that a third of the hubs peak in a meningeal/fibroblast compartment — is the expected signature of ambient or dissection-derived contamination for a programme derived from dissociated DRG neurons, and it materially weakens the dorsal-horn claim.

**【Specific fix】** Add to the spatial paragraph:

> "Of the 35 hubs, 17 had their maximal regional expression in the dorsal horn, but 11 had it in the meningeal/fibroblast compartment, 4 in the ventral horn, 2 in the ependymal region and 1 in white matter. The size of the meningeal/fibroblast block (11/35), together with the ambient-RNA flags on ATF3 and AXL, is compatible with a substantial ambient/dissection contribution to the spatial assignment, so we report the dorsal-horn count as an anatomical observation on uninjured tissue and not as enrichment."

---

## 【D11 — Minor-to-Major】Suzetrigine is described incompletely, and one sentence about it is not a test

**【Problem】** The manuscript calls suzetrigine a "Nav1.8 inhibitor clinical programme" and "phase 3"; it is in fact FDA-approved (30 January 2025) for moderate-to-severe **acute** pain in adults with a 14-day maximum, and its neuropathic-pain evidence is phase 2. Separately, "consistent with the absence of a selective nonopioid analgesic signal such as suzetrigine in this docking space" is not an observation about the docking space at all, because ion channels were never docked.

**【Evidence】**
- Manuscript Results line 52: "the more recent Nav1.8 inhibitor clinical programme shows that channel is druggable without establishing injury-induced SCN10A up-regulation." Introduction/Results line 112: "consistent with the absence of a selective nonopioid analgesic signal such as suzetrigine²²,²³ in this docking space".
- References 22 and 23 are real and correctly described: Divito AE, Sharobeem M, Bajracharya GR, Abdelmalak BB, *Cleve Clin J Med* 2026;93(2):94-98, doi:10.3949/ccjm.93a.25087 (verified); Bertoch T et al., *Anesthesiology* 2025;142(5):1085-1099, doi:10.1097/ALN.0000000000005460 (two phase-3 RCTs in abdominoplasty and bunionectomy — consistent with the approved indication).
- FDA approval: 30 January 2025, Journavx (suzetrigine), selective NaV1.8 inhibitor, adults, moderate-to-severe acute pain, maximum 14 days.

**【Why it matters】** In a paper whose subject is nerve injury, saying only "phase 3, druggable" invites the reader to generalise an acute-postsurgical-pain approval to nerve-injury indications. That would be an over-read the authors themselves would not endorse, and it sits one sentence away from a claim about CPSP.

**【Specific fix】** Replace Results line 52 clause with:

> "whereas the recent Nav1.8 programme has produced the first FDA-approved selective NaV1.8 inhibitor (suzetrigine; approved January 2025 for moderate-to-severe acute pain in adults, maximum 14 days), which establishes that the channel is druggable in acute postsurgical pain but does not establish efficacy in neuropathic or nerve-injury pain and says nothing about injury-induced SCN10A regulation."

Replace "consistent with the absence of a selective nonopioid analgesic signal such as suzetrigine²²,²³ in this docking space" with:

> "Ion-channel targets were not docked at all in this screen, so suzetrigine and other NaV-directed analgesics²²,²³ are outside the assessed chemical space by construction rather than by failure; this is a scope limit, not a finding."

---

## 【D12 — Minor】"Face-validity testing refuted analgesic enrichment" overstates a null

**【Problem】** 0 of 64 observed versus ≈0.4 expected with p > 0.14 is an underpowered absence of enrichment, not a refutation.

**【Evidence】** Manuscript Results line 112: "**Face-validity testing refuted analgesic enrichment**: 0 of 64 known analgesics appeared in the Top-20 (≈0.4 expected), rank AUC ≈ 0.54 (p > 0.14)". With 0.4 expected events, the test has essentially no power to detect absence.

**【Specific fix】** Replace with:

> "Face-validity testing found no analgesic enrichment, but with only ~0.4 expected analgesics in the top 20 the test is uninformative rather than refuting: 0 of 64 known analgesics appeared in the top 20 (rank AUC ≈ 0.54, p > 0.14), and α2-agonists scored at chance after MW correction (AUC 0.428, p = 0.76)."

---

## 【D13 — Minor】"Neuroinflammation" is a misnomer for this gene set, and GFAP is being read as an astrocyte marker in a ganglion

**【Problem】** The `Neuroinflammation` set mixes true cytokines with neuronal injury-associated transcription factors and a satellite-glia marker; its mean_Z is largely driven by the axotomy programme.

**【Evidence】** `results/tables/_R4_geneset_members.json` → `Neuroinflammation` = IL1B, IL6, TNF, CCL2, CXCL1, IL10, TLR2, TLR4, MYD88, NFKB1, NFKB2, STAT3, SOCS3, CD68, AIF1, GFAP, **ATF3, JUN, FOS**. Recomputed from `META_DRG_axis_stouffer.csv`: ATF3 Z +10.53, SOCS3 +8.78, JUN +8.17, STAT3 +7.33, GFAP +7.37, IL6 +7.15 — so six of the largest contributors are a neuronal regeneration/immediate-early programme plus GFAP, while the canonical inflammatory cytokines are weak or non-significant (TNF Z +1.45, FDR 0.24; NFKB1 FDR 0.089; NFKB2 FDR 0.14; CCL2 consistency 0.67). In DRG, GFAP marks **satellite glial cells**, not astrocytes.

**【Why it matters】** Calling this "neuroinflammation" and then citing microglial BDNF/p38 literature for it (Discussion, refs 24, 25) misattributes a regeneration/gliosis signal to an inflammatory mechanism.

**【Specific fix】** Rename the set to `Injury_inflammation_mixed` in Fig. 1, the legend and Supplementary S5, and add to the Results gene-set paragraph:

> "The set we label 'neuroinflammation' is heterogeneous: its largest contributors are the neuronal injury/regeneration factors ATF3 (+10.53), SOCS3 (+8.78), JUN (+8.17) and STAT3 (+7.33) and the satellite-glia marker GFAP (+7.37), whereas the canonical cytokines are weak or non-significant in this collection (TNF meta_Z +1.45, FDR 0.24; NFKB1 FDR 0.089; NFKB2 FDR 0.14). We therefore treat it as a mixed injury–inflammation–gliosis module and do not interpret it as a microglial inflammatory mechanism."

---

## 【D14 — Minor】Reference 12 is used for "atrophy/loss" but documents loss only, and only after severe axotomy

**【Problem】** The citation is slightly over-extended and one-sided.

**【Evidence】** Cooper AH, Barry AM, Chrysostomidou P, Lolignier R, Wang J, Redondo Canales M, Titterton HF, Bennett DL, Weir GA. "Peripheral nerve injury results in a biased loss of sensory neuron subpopulations." *Pain* 2024;165(12):2863-2876, doi:10.1097/j.pain.0000000000003321 — verified (PMID 39158319). Its abstract: loss is documented after **spared nerve injury** (near-complete loss of Mrgprd⁺ non-peptidergic nociceptors) and **sciatic nerve crush** (~50%), and the paper states that "the extent or even presence of neuron loss following injury has recently been challenged." It documents cell loss, not atrophy.

**【Why it matters】** The manuscript says "injury-induced neuronal **atrophy/loss**¹²" and applies it as a general confounder of bulk DRG signal across CCI, SNI and incision models. Cooper et al. cover SNI and crush; CCI is not examined, and no incision model is. The qualifier "atrophy" is not supported by that reference.

**【Specific fix】** Replace "bulk DRG signal is confounded by injury-induced neuronal atrophy/loss¹²" with:

> "bulk DRG signal is confounded by injury-induced sensory-neuron loss, which after spared nerve injury removes almost the whole Mrgprd⁺ non-peptidergic population and after sciatic crush roughly half of it¹² — although the extent of such loss is itself contested, and it has not been quantified in the CCI or incision models used here."

---

## 【D15 — Minor】Abstract dataset description is arithmetically confusing

**【Problem】** "12 public GEO datasets (four nerve-injury, one incision)" reads as if 12 = 4 + 1.

**【Evidence】** Abstract line 14: "We reanalysed 12 public GEO datasets (four nerve-injury, one incision), framing the axis as a nerve-injury-associated response and the incision arm as a held-out translation test." In fact five datasets feed the meta-analysis (four nerve-injury + one incision); the other seven are single-cell (GSE216039, GSE328175, GSE246288), spatial (GSE325938), human plasma miRNA (GSE158825), cross-fluid miRNA (GSE222979) and an SH-SY5Y cell line (GSE306403).

**【Specific fix】** Replace with:

> "We reanalysed 12 public GEO datasets, of which five (four nerve-injury, one surgical incision) contribute dorsal-root-ganglion contrasts to the meta-analysis and seven provide single-cell, spatial, human plasma miRNA and in-vitro layers."

---

## § Stands up

Things I suspected, checked against the source tables or the primary literature, and found **correct**.

1. **The positive-control biology is right and the numbers reproduce.** ATF3 is the correct top-ranked positive control for a nerve-injury DRG meta-analysis, and `META_DRG_axis_stouffer.csv` gives exactly the printed values: ATF3 meta_Z 10.533, meta_FDR 1.005e-21, K = 6, 6 up / 0 down; followed by GAL (10.339), ECEL1 (9.544), NPY (9.275), FLRT3 (9.252). ATF3, SPRR1A, GAL, NPY and SOCS3 are indeed the canonical injury/regeneration-associated genes of axotomised DRG.
2. **The TREM2 / APOE / TYROBP honesty check is genuine, not cosmetic.** The Discussion reports TYROBP meta_FDR 8.8e-9 (consistency 5/5), TREM2 1.3e-3 (5/6) and APOE 0.070 (6/6, up but sub-threshold). Recomputation gives 8.807e-9 (K = 5, 5 up / 0 dn), 1.299e-3 (K = 6, 5 up / 1 dn) and 6.973e-2 (6 up / 0 dn) — exact. Reporting that the third canonical DAM hallmark fails the FDR threshold, rather than quietly dropping it, is the right behaviour. (My D5 objection is about what is *omitted around* these three numbers, not about these three numbers.)
3. **Table 1b reproduces exactly, on both the per-contrast log₂FC and the bulk meta_Z/FDR.** SCN9A: incision +0.607 (printed +0.61), −0.073, −0.285, −2.710, bulk Z −2.925 / FDR 0.0108 (printed −2.92 / 0.011). SCN10A +0.986 / −3.034 / 0.0080. SCN11A +0.899 / −3.408 / 0.0026. SCN8A +0.987 / −4.924 / 1.009e-5. All four incision-up / nerve-injury-down directions are real in the data, and the decision to print Z alongside log₂FC (so that |Z| is not mistaken for effect size) is correct and well explained.
4. **The core-signature counts and the circular-concordance number reproduce.** From `META_DRG_axis_stouffer.csv`: 16,552 genes tested; 6,869 at meta_FDR < 0.05; 4,055 at FDR < 0.05 and consistency ≥ 0.8; 3,556 of the core have incision measurements, of which 2,473 are concordant = 69.5% — exactly as printed (69.5%, 2,473/3,556). The K distribution (K = 6: 9,834; K = 4: 3,229; K = 5: 1,782; K = 3: 1,707) shows that the "≥ 0.8 consistency" threshold is being applied at mixed K, which the manuscript does disclose.
5. **The gene-set statistics reproduce and the direction claims are right.** `P3_geneset_stats.csv`: neuroinflammation mean_Z +4.943, frac_up 1.000; DAM_microglia +3.884, 0.938 (printed 93.8%); complement +3.441, 0.944 (printed 94.4%); OXPHOS −2.373, frac_up 0.263 (printed "73.7% of members down"). Complement up-regulation and C1Q up-regulation after peripheral nerve injury are consistent with current knowledge (including the recent C1q/microglial-synaptic-removal work the authors cite as ref 29).
6. **The SCN8A contradiction with the Nav1.6 literature is appropriately hedged.** Nav1.6/SCN8A *is* reported as transcriptionally up-regulated in DRG after nerve injury (the cited L5-VRT TNF-α/STAT3 paper, ref 10, is a real and appropriate citation), and the manuscript's statement that its own down-regulation "should not be read as contradicting that work at the protein or single-neuron level" is the correct response to a genuine conflict between bulk mRNA and the channel literature.
7. **The suzetrigine references are real and correctly characterised as Nav1.8.** Ref 22 (Divito et al., CCJM 2026;93(2):94-98, doi:10.3949/ccjm.93a.25087) and ref 23 (Bertoch et al., Anesthesiology 2025;142:1085-1099, two phase-3 RCTs) both exist and both describe a Nav1.8 inhibitor. My D11 objection is about completeness (approval status and indication scope), not about accuracy of what is written.
8. **The Visium dorsal-horn count reproduces.** `P5_GSE325938_hub_regionalization.csv` gives 17 hubs with `top_region = DorsalHorn`, matching "17 of 33 detectably expressed hubs (51.5%)". The decision to place a 5% detection floor on regional specificity ratios, and to report the dorsal-horn assignment as constitutive baseline anatomy rather than injury-induced recruitment (only Sham tissue was available), is correct.
9. **REG3B is handled honestly.** The manuscript flags REG3B as an external motivational hypothesis from a CRPS-I (not CPSP, not nerve-transection) report and states it was not in the meta core, not localisable in spinal snRNA, and detected in only 1.7% of DRG cells. `P3_hub_genes.csv` confirms `REG3B … in_meta_core = False`, and `META_DRG_axis_stouffer.csv` gives REG3B K = 4, 3 up / 1 down (consistency 0.75 < 0.8). That is the right way to carry a prior hypothesis that the data do not support.

---

## § Questions for the authors

I am not guessing at the answers to any of these.

1. **Spinal representation.** Is any spinal-cord contrast in the meta-analysis? If not, on what basis is the axis framing retained? Would you accept Option A of D1 (re-scope to DRG, keep the spinal pole as a localisation layer)?
2. **Unused spinal data.** `data/processed/GSE265957_Xtail_SC_Day4_SNI_vs_SHM.csv`, `GSE265957_Xtail_SC_Day63_SNI_vs_SHM.csv` and `results/tables/DEG_GSE241361_S1R_SC__SNI_vs_Naive_WT_SC.csv` all exist. Why were they excluded — the K ≥ 3 rule, or something else? Please state the reason in the Methods either way.
3. **SMIR + LPI.** Does the GSE267799 "chronic_vs_baseline" contrast pool both models (my reading of the sample table says yes: 4 SMIR-10d + 4 SMIR-32d + 4 LPI-10d vs 4 SMIR-0d + 4 LPI-0d)? Was model ever included as a covariate or as a stratification? If it can be stratified, what happens to the 46.2% / 47.1% translation result?
4. **Day 32.** Given that SMIR-evoked hypersensitivity is reported to have dissipated by postoperative day 32, will you re-run the incision arm as day-10-only (n = 8 vs 8) and report it? If the result changes, the "non-predictive" headline needs restating.
5. **Pain phenotype confirmation.** Do any of GSE212311, GSE278227, GSE241361 or GSE265957 report behavioural confirmation (mechanical/thermal thresholds) that the injured animals were actually hypersensitive at the harvest timepoint? The manuscript never confirms this, and a transcriptional "pain signature" from tissue with no verified pain phenotype is an assumption.
6. **Sex.** GSE265957 and GSE241361 are female C57BL/6; GSE212311 is male Sprague-Dawley; GSE278227 has both sexes but the meta uses the pooled 1-week contrast. Sex is a documented determinant of whether the microglial or the macrophage compartment drives nerve-injury hypersensitivity. Was sex considered? If it cannot be (n = 2–4 per cell), please say so.
7. **LPL.** LPL is a member of your own DAM set and is significantly down (meta_Z −3.43, FDR 0.0026, 5/6 contrasts). Do you agree this needs to be reported alongside TREM2/TYROBP/APOE?
8. **Reference 6 and GSE267799.** Is GSE267799 the dataset described by Meng X, Bu L, Shen L, Tao KM (*Scientific Data* 2024;11:1229, doi:10.1038/s41597-024-04078-2)? The deposited design (rat; skin, muscle and DRG; two surgical models; acute vs chronic postsurgical pain; public October 2024) matches that descriptor closely. If it is the same dataset, reference 6 is currently cited as an external comparator resource when it is in fact the source of the incision arm you analyse, and it must be cited as such. Please confirm or correct.
9. **Ref 11 and IB4.** Which paper do you actually mean for "SCN10A/Nav1.8 mRNA is down-regulated in axotomized IB4+ neurons"? Yin 2016 does not report IB4⁺ sorting. If the intended claim is just "Nav1.8 mRNA is down after axotomy", Yin 2016 supports it and should be cited that way.
10. **Tissue of the human layer.** GSE158825 is plasma miRNA from lumbar-surgery patients. Do you have any information on whether %nprs20delta is a CPSP endpoint or an acute pain-change endpoint? The manuscript calls it "pain outcome" throughout; whether it indexes chronic postsurgical pain determines whether the null is a CPSP null at all.

---

## § What I actually checked

**Files read (manuscript and supporting):**
`reports/MVP_PLOSONE_submission.md` (all 332 lines, including the long lines that render truncated in a paged read — I printed lines 44, 48, 52, 58, 64, 88, 112, 120, 128, 167 in full); `reports/MVP_PLOSONE_cover_letter.md` (all 25 lines); `reports/MVP_PLOSONE_supplementary.md` (lines 1–61 and the two CPSP gene-set rows at 161 and 185); `reports/MVP_STROBE_checklist.md` and `reports/MVP_PLOSONE_compliance_check.md` (skimmed).

**Source tables read and recomputed:**
- `results/tables/META_DRG_axis_stouffer.csv` — 16,552 rows × 16 columns. Queried ~80 genes individually (DAM members, complement, OXPHOS, Nav family, neuroinflammation members, homeostatic microglial genes, all 10 docking targets, all 35 hubs). Recomputed total N, FDR < 0.05 count, core count, K distribution, core-with-incision count and concordance.
- `results/tables/META_bulkonly_meta.csv` — verified the four bulk SCN meta_Z/FDR values printed in Table 1b and the bulk-only TREM2/APOE/TYROBP values.
- `results/tables/P3_geneset_stats.csv` — all 19 sets.
- `results/tables/_R4_geneset_members.json` — membership of all 19 sets (this is where I found SCN3A inside Nav_SCN).
- `results/tables/P3_hub_genes.csv` — all 35 hubs with n_methods, lasso_freq, rf_gini, shap_meanabs, in_meta_core.
- `results/tables/P5_GSE325938_hub_regionalization.csv` — top_region counts.
- `results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv` — n_case = 12, n_ctrl = 8.
- `results/tables/_R4_ref_DOIs.json` — the authors' own DOI registry (26 of 36 references; refs 11–18, 22–23 and 19 are not in it).

**Scripts read:** `scripts/p2_deg_meta.py` (lines 1–200 — this is where I established both that the meta is DRG-only and that GSE267799 is grouped by `time_group` only).

**GEO metadata read:** `data/processed/GSE267799_series_matrix.txt.gz_samples.csv` (108 samples; parsed tissue × treatment × time), `data/processed/GSE267799_DRG_sampletable.csv`, `data/processed/GSE267799_all_sampletable.csv`, `data/processed/GSE267799_DRG_symbol_count.csv` (column headers), `data/processed/GSE265957-GPL21103_series_matrix.txt.gz_samples.csv`, `data/processed/GSE212311_series_matrix.txt.gz_samples.csv`.

**Literature verified this session (DOI or PMID confirmed):** Flatters 2008 (PMID 17590272, doi:10.1016/j.pain.2007.05.013); Yu et al. 2020 (PMID 31937758, doi:10.1038/s41467-019-13839-2); Kehlet/Jensen/Woolf 2006 (PMID 16698416, doi:10.1016/S0140-6736(06)68700-X); Krasemann et al. 2017 (doi:10.1016/j.immuni.2017.08.008); Deczkowska et al. 2018 (doi:10.1016/j.cell.2018.05.003); Cooper et al. 2024 (PMID 39158319, doi:10.1097/j.pain.0000000000003321); Yin et al. 2016 (PMID 25562420, doi:10.3109/00207454.2015.1004172, abstract read in full); Divito et al. 2026 (doi:10.3949/ccjm.93a.25087); suzetrigine FDA approval 30 Jan 2025, Journavx, NaV1.8, acute pain, max 14 days; Osteen et al., Pain Ther 2025;14:655-674 (PMID 39775738).

**Discrepancies between manuscript and source data — stated explicitly:**
- Every number I recomputed from `META_DRG_axis_stouffer.csv`, `P3_geneset_stats.csv`, `P5_GSE325938_hub_regionalization.csv` and `META_bulkonly_meta.csv` **matched** the manuscript (ATF3, SCN Table 1b, core counts 16,552 / 6,869 / 4,055 / 3,556 / 69.5%, gene-set mean_Z and frac_up, 17 dorsal-horn hubs, CDHR5 log₂FC range, TREM2/TYROBP/APOE FDRs). I found **no** fabricated or mis-transcribed quantitative value in the submitted tables.
- Discrepancies found are all of *label, scope, attribution and omission*, not of arithmetic: meta is DRG-only (D1); incision arm pools SMIR + LPI and day 10 + day 32 (D2); harvest-day caveat contradicts the deposition (D3); SCN3A is in the tested Nav set and is not the most induced channel here (D7); ref 11 does not support the IB4⁺ attribution (D7); GSE265957 is SNI not tibial-nerve injury (D6); LPL direction and the homeostatic-arm direction are unreported (D5); 11/35 meningeal assignments are unreported (D10); "establishing … nerve-injury-specific" contradicts the paper's own hedged statement (D9a); the cover letter asserts a CPSP axis the Abstract disclaims (see Must-fix).

**Not checked (outside my remit):** the docking pipeline and enrichment statistics, the ML leakage-control implementation, the permutation machinery, the DerSimonian–Laird algebra, reference numbering/PLOS formatting. Those belong to the other panel members.

---

## § Must-fix list (ordered by severity)

| # | Item | Severity |
|---|---|---|
| 1 | **D1** — The meta-analysis is DRG-only; the title, Abstract, Introduction, Discussion and cover letter all claim a DRG–spinal axis. Re-scope to DRG (Option A) or add the spinal contrasts and re-run. | **Major** |
| 2 | **D2** — Incision arm pools two surgical models (SMIR + LPI) and two harvest days (10 d, 32 d); the day-32 samples are from animals whose SMIR hypersensitivity has resolved. Stratify or relabel, and report the day-10-only sensitivity contrast. | **Major** |
| 3 | **D4** — State explicitly that the core is an axotomy/regeneration programme while the incision model does not damage DRG neurons, so the "non-predictive translation" headline is partly expected by design. | **Major** |
| 4 | **D5** — Report all 16 DAM members plus the homeostatic arm; report LPL as significantly down; stop calling the DRG signal microglial; rename the set; cite Yu 2020, Krasemann 2017, Deczkowska 2018. | **Major** |
| 5 | **D8** — Add Flatters 2008 (defines the incision arm), Yu 2020, Kehlet 2006, Krasemann 2017, Deczkowska 2018, Osteen 2025, Brennan 1996. | **Major** |
| 6 | **D9a** — Remove "establishing that the axis is a nerve-injury-specific response"; a non-significant AUC cannot establish specificity. | **Major** |
| 7 | **D3** — Correct the false "harvest day not stated in the deposited metadata" caveat; the deposition states 0 d / 6 h / 2 d / 10 d / 32 d. | **Major** |
| 8 | **D6** — GSE265957 is spared nerve injury (SNI), not "tibial-nerve-injury"; correct in Results, Methods and Introduction. | **Major** |
| 9 | **D7** — Correct the ref-11 IB4⁺ misattribution; cite Yin 2016 for SCN3A; correct the false "SCN3A was not among the tested sets". | **Major** |
| 10 | **D9b/c/d** — Apply the neuronal-loss/dilution confounder to the OXPHOS and synaptic results; stop citing microglial papers for a DRG macrophage signal; make the OXPHOS Discussion sentence conditional. | **Major** |
| 11 | **Cover letter, line 9** — "reproducible benchmark for the chronic postsurgical pain (CPSP) dorsal root ganglion–spinal (DRG–spinal) axis" contradicts the Abstract's "not shown by this meta-analysis to be CPSP-specific". Replace with: "a reproducible benchmark for the dorsal root ganglion transcriptional response to peripheral nerve injury, with a held-out and non-predictive surgical-incision translation test". | **Major** |
| 12 | **D10** — Report the 11/35 meningeal/fibroblast regional assignment alongside the 17/33 dorsal-horn figure. | **Major** |
| 13 | **D11** — State suzetrigine's approval status (FDA, Jan 2025) and indication scope (acute pain, ≤14 days); rewrite the "absence … in this docking space" sentence as a scope limit. | **Minor** |
| 14 | **D9e** — Downgrade "axis-end specialisation" from a demonstrated property to a hypothesis, given 15/35 NotLocalisable and 0 BH-significant pseudobulk genes. | **Minor** |
| 15 | **D12** — "Refuted analgesic enrichment" → "no enrichment found; test uninformative". | **Minor** |
| 16 | **D13** — Rename the "neuroinflammation" set; disclose that ATF3/JUN/FOS/SOCS3/STAT3/GFAP dominate it and that TNF/NFKB are non-significant; note GFAP = satellite glia in DRG. | **Minor** |
| 17 | **D14** — Ref 12 documents loss (SNI, crush), not atrophy, and not in CCI or incision models; qualify. | **Minor** |
| 18 | **D15** — Fix "12 public GEO datasets (four nerve-injury, one incision)" so it does not read as 12 = 5. | **Cosmetic** |
| 19 | Drop ref 30 (Kong 2023) from the OXPHOS-support citation list, or note that it reports glycolytic *enhancement*, not OXPHOS suppression. | **Cosmetic** |
