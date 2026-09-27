# A1 — Domain review (clinician-scientist: chronic postsurgical pain / DRG neuroimmune signalling / neuroinflammation)

**Reviewer codename:** A1
**Role:** Domain expert
**Manuscript version reviewed:** v1.2.0 (treated as a first submission; no prior review read)
**Manuscript:** `reports/MVP_PLOSONE_submission.md` + `reports/MVP_PLOSONE_supplementary.md`
**Title under review:** "Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null"

---

## 1. Endpoint mechanistic coherence (neuroinflammation–DAM-like–complement ↑, OXPHOS ↓)

### Item 1 — The endpoint is coherent with *neuropathic* pain literature, but the leap to CPSP is by analogy, not evidence
【Problem】 The neuroimmune–DAM–complement-up / OXPHOS-down endpoint is well supported in nerve-injury/neuropathic models, but the manuscript frames it inside a "CPSP" title/abstract while none of the primary evidence is CPSP tissue.
【Evidence】 Gene-set endpoint values are internally consistent and match the supplementary: neuroinflammation mean_Z +4.94 (q=0.003), DAM_microglia +3.88 (q=0.003), complement +3.44 (q=0.003), mitochondria_OXPHOS −2.37 (q=0.020 fixed-effect, 0.31 random-effects) — `MVP_PLOSONE_supplementary.md` S5/S5b lines 146–192. The cited support is neuropathic/nerve-injury work: Tsuda et al. Nat Med 2003 (spinal microglial P2X4), Inoue & Tsuda Nat Rev Neurosci 2018, Tansley et al. Nat Commun 2022 (pain microglia scRNA), Haque et al. Pain 2024 (DRG mitochondrial pyruvate oxidation), Scholz & Woolf Nat Neurosci 2007 (triad). Of the five axis bulk studies, four are nerve-injury (CCI/SNI/translatome) and only one is incision — `MVP_PLOSONE_submission.md` line 36, 122.
【Why it matters】 Mechanism transfers from neuropathic (SNI/CCI) to chronic postsurgical pain (CPSP) are plausible but not automatic; CPSP has distinct temporal, immune and central-sensitisation features. Calling the endpoint a "CPSP" endpoint overstates what the data show and is at odds with the paper's own "nerve-injury-associated, not CPSP-specific" conclusion.
【Specific fix】 Add an explicit boundary sentence in the Abstract/Discussion: "The neuroimmune–DAM–complement and OXPHOS endpoints are established here in nerve-injury/neuropathic models and extrapolated to CPSP by mechanistic analogy; they are not demonstrated in CPSP (chronic postsurgical) tissue." This aligns the endpoint claim with the reframe rather than contradicting it.

### Item 2 — OXPHOS-down limb collapses under random effects; the "metabolic" half of the endpoint is fragile and should be demoted in summary claims
【Problem】 The "neuroimmune–*metabolic* axis" headline depends on an OXPHOS-down signal that does not survive random-effects correction (q=0.31) and is therefore RE-fragile, yet the Discussion still calls it a robust "neuroimmune–metabolic programme."
【Evidence】 S5b (`MVP_PLOSONE_supplementary.md` lines 175, 192): Mitochondria_OXPHOS perm p 0.0045 → BH q 0.0202 (fixed-effect) but q 0.3103 (random-effects), "OXPHOS does not (q = 0.31) ... reported as a fixed-effect finding that is not reliable under between-contrast heterogeneity." Random-effects heterogeneity is high: median I² 38.8% genome-wide, 72.8% across the 35 hubs (`MVP_PLOSONE_supplementary.md` lines 204, 209; `MVP_PLOSONE_submission.md` line 46). Discussion line 122: "The DRG–spinal axis is recurrently characterized by a neuroimmune–metabolic programme…" and "In the fixed-effect analysis only, OXPHOS suppression… consistent with the growing literature…"
【Why it matters】 A domain reader expects "metabolic suppression" to be a reproducible, mechanistically central limb. Its disappearance under RE (median I² 72.8% in hubs) means the metabolic limb is the weakest part of the endpoint; leaving "metabolic" unqualified in the Discussion overstates robustness.
【Specific fix】 Replace "neuroimmune–metabolic programme" (Discussion line 122) with "neuroimmune programme with a fixed-effect-only, random-effects-fragile metabolic (OXPHOS-down) limb (q=0.31 under RE)." Keep the Abstract as-is (it already says "neuroimmune/DAM-like programme" without "metabolic" — good).

### Item 3 — "DAM-like"/"microglial" label over-extrapolates a bulk DRG signal
【Problem】 The endpoint is repeatedly described as "microglial DAM," but it is a bulk DRG gene-set signal that cannot distinguish resident microglia from infiltrating macrophages or other myeloid cells — and in DRG after peripheral nerve injury the dominant immune population is infiltrating macrophages/satellite glia, not CNS microglia.
【Evidence】 `MVP_PLOSONE_submission.md` line 48 (honest): "this is a bulk-tissue gene-set signal, it cannot be attributed specifically to resident microglia versus infiltrating macrophages or other neuroimmune cells." Yet Discussion lines 122, 124, 126 repeatedly say "DAM-like neuroimmune and complement activation," "microglial DAM in pain," "the classic P2X4-driven microglial activation." DRG is a peripheral ganglion; its post-injury immune infiltrate is largely haematogenous macrophages (the DAM gene set — TREM2/APOE/TYROBP, CTSD, CST7, MERTK, ITGAX, AXL, C1QA/B/C — is expressed by both microglia and infiltrating macrophages).
【Why it matters】 Assigning a bulk DRG DAM signal specifically to microglia is an extrapolation that could misdirect mechanistic follow-up (e.g., microglia-specific vs macrophage-specific targeting). It also compounds the P2RX self-negative below.
【Specific fix】 Consistently phrase as "DAM-like neuroimmune programme of myeloid (resident microglia and/or infiltrating macrophage) origin" wherever the endpoint is summarised, until single-cell deconvolution (which the authors already have in GSE216039/GSE246288) is used to attribute the DAM genes to a specific cell type.

### Item 4 — The P2RX/P2RY self-negative (good honesty) further weakens the "DAM" qualifier and should be kept prominent
【Problem】 The absence of a purinergic (P2X4) signal means the captured state is only "partially" the canonical microglial DAM programme; this is honestly noted but is easy to under-weight.
【Evidence】 `MVP_PLOSONE_submission.md` line 86: "P2RX/P2RY showed no coordinate change (permutation p = 0.339 in the bulk-only meta; p = 0.440 in the six-input meta)… the DAM-like state captured is only partially the classic P2X4-driven microglial activation… we describe the neuroimmune signal as 'DAM-like' rather than as a fully reconstituted DAM state." This matches the cited Tansley et al. 2022 (time-/sex-specific partial overlap).
【Why it matters】 This is a genuine strength (the authors did not hide a negative), but it means the "DAM" descriptor is doubly qualified: (a) bulk cannot assign cell type (Item 3), and (b) the canonical P2X4 DAM marker is absent. The reader should not read "DAM" as "full Alzheimer-type microglial programme."
【Specific fix】 No change required; I flag it as a stand-up item and recommend the authors keep this paragraph in the main body (not only Discussion) so it is not lost.

---

## 2. Title reframe ("DRG-only") consistency

### Item 5 — "DRG–spinal axis" wording contradicts the DRG-only title reframe in ≥4 places
【Problem】 The title reframes to "dorsal root ganglion … spinal-cord localisation," i.e. DRG-only with spinal as localisation, but the body repeatedly invokes a "DRG–spinal axis" that was never meta-analysed.
【Evidence】 Title line 1 is DRG-only; however: Abstract line 14 "DRG–spinal-axis targets remain undefined"; Introduction line 32 "viewing the dorsal root ganglion (DRG) and spinal cord not as separate tissues but as a single peripheral–central axis"; Introduction line 36 "dissect the DRG–spinal axis computationally"; Author Summary line 26 "across this DRG–spinal axis"; Discussion line 122 "The DRG–spinal axis is recurrently characterized by…". The meta-analysis itself is DRG-only: six contrasts from five studies, all DRG (`MVP_PLOSONE_submission.md` line 146: GSE267799, GSE212311, GSE278227, GSE241361 DRG, GSE265957 D4/D63 — all DRG). No spinal-cord bulk meta was computed.
【Why it matters】 A reviewer/reader will infer a computed DRG↔spinal meta-axis. None exists; spinal is only single-cell/spatial localisation. This is a real internal inconsistency that the title reframe was meant to fix but the body did not follow through.
【Specific fix】 Replace every "DRG–spinal axis" / "peripheral–central axis" with "DRG-centred nerve-injury response with spinal-cord localisation," and add one Methods sentence: "No spinal-cord bulk transcriptome was included in the Stouffer meta-analysis; spinal-cord datasets (GSE241361 spinal, GSE328175, GSE246288, GSE325938) were used for hub localisation and the ML cross-dataset fold only, not for the DRG meta-core."

### Item 6 — Spinal-cord data entered the *hub-definition* ML, contradicting "spinal = localisation only"
【Problem】 The 35 hubs were derived from an ML pool that includes a spinal-cord dataset fold, so spinal expression informed hub selection — yet the reframe says spinal is "localisation only."
【Evidence】 Methods line 159: "Five DRG-axis datasets (GSE278227, GSE267799, GSE241361 mouse DRG, GSE241361 mouse spinal cord, GSE212311) were intra-dataset gene-z-scored, intersected to 13,208 common genes, and pooled into 72 samples." Fig. 2 legend line 293 lists the "GSE241361 mouse spinal cord" fold. So GSE241361 spinal is a training/test fold for the dual-ML hub classifier, not merely a localisation dataset.
【Why it matters】 If spinal expression contributes to hub selection, the hub set is not strictly DRG-only, and the "DRG-only" reframe is internally inconsistent. More importantly, the two GSE241361 folds come from the same animals (line 64), so including the spinal fold also imports the same-animal non-independence into hub definition, not just into LODO reporting.
【Specific fix】 Either (a) remove GSE241361 spinal from the ML pooling, re-derive the 35 hubs DRG-only, and re-run docking eligibility on the revised set; or (b) if spinal is retained, drop the "DRG-only / spinal = localisation only" absolutism from title/abstract and state that spinal-cord expression contributed to hub convergence. Option (a) is cleaner and preserves the reframe.

---

## 3. "Not CPSP-specific" defensibility

### Item 7 — No analysed dataset captures *established* CPSP; the incision arm is acute/postoperative, not chronic CPSP
【Problem】 The entire "CPSP-specific vs nerve-injury" question is built on a proxy: the incision arm models acute-to-subacute postoperative pain, not chronic postsurgical pain (pain persisting >3 months), and the "chronic" contrast itself mixes resolving samples.
【Evidence】 Methods line 143/154: GSE267799 "chronic vs baseline" but line 154 "merges day-10 and day-32 samples (36 chronic vs 24 baseline at 0d)… day-32 SMIR samples represent a resolving rather than established-chronic phenotype." CPSP is conventionally defined as pain >3 months after surgery (Macrae 2008, ref 1, is cited for the 10–50% incidence but the datasets do not reach that timeframe). All 12 accessions are rodent acute/subacute models or human plasma miRNA (GSE158825) — none model established human CPSP.
【Why it matters】 The conclusion "not CPSP-specific" is therefore doubly provisional: it rests on (i) a single heterogeneous incision arm and (ii) an arm that is not actually CPSP. Treating a non-significant acute-incision translation test as informative about CPSP specificity over-reaches.
【Specific fix】 Add: "No analysed dataset captures established chronic postsurgical pain (pain persisting >3 months); the incision arm models acute-to-subacute postoperative pain and is used as a translational proxy, so the CPSP-specificity question is necessarily provisional and is not answered by this study."

### Item 8 — "Not CPSP-specific" is inferred from a non-significant test (p=0.14); the conclusion should not be stated as affirmative
【Problem】 The non-circular translation test (46.2% vs 47.1%, p=0.14) fails to reject the null of no relationship; from a non-significant result one cannot affirmatively conclude the signature is non-specific (or specific). Yet Conclusions line 136 states it as a positive claim.
【Evidence】 Results lines 54–58: non-circular test agreement 46.2% (2,266/4,899) vs background 47.1% (6,779/14,390), risk difference −0.9 pp, permutation p=0.14. Conclusions line 136: "the DRG–spinal axis is a nerve-injury-associated… transcriptional response rather than a CPSP-specific pathway on the available evidence (this conclusion rests on a single, heterogeneous incision arm and is provisional)." The parenthetical hedge is good, but the main clause states it as a settled contrast ("rather than a CPSP-specific pathway").
【Why it matters】 Stating a conclusion "rather than X" from a p=0.14 null commits the error of interpreting a failed test as evidence of absence of translation; it is methodologically the weakest link in the reframe.
【Specific fix】 Rephrase Conclusions line 136 to: "on available evidence the nerve-injury signature is not established as CPSP-specific — the translation test to the sole incision arm was non-significant (p=0.14) and underpowered, and the inference is provisional and does not demonstrate either CPSP-specificity or its absence." Attach the provisional qualifier to the conclusion itself, not only the parenthesis.

---

## 4. Ion-channel "honest null" framing

### Item 9 — The ion-channel "honest null" is transparent but should state the excluded class contains the *only* clinically validated non-opioid analgesic targets
【Problem】 The "honest null" headline risks being read as a broad negative on structure-based repurposing, whereas the most clinically relevant analgesic mechanisms (gabapentinoid α2δ, NaV1.8) were excluded by a structural-database limitation, so the null is *silent*, not *negative*, on them.
【Evidence】 Methods line 168: ion-channel candidates "SCN9A/10A/11A/KCNQ2/CACNA2D1/GABRA1 have experimental structures but lack a ligand-anchored pocket appropriate for a defined docking box, and were therefore not docked (they could be revisited by blind/cavity-aware docking)." Results line 126: "the entire ion-channel analgesic class — α2δ subunits and NaV channels, including the clinically validated gabapentinoid and NaV1.7/NaV1.8 targets — was structurally undockable and never screened, so the null deliberately cannot speak to those mechanisms." This disclosure is present and is good.
【Why it matters】 α2δ-1 (gabapentinoids) and NaV1.8 (suzetrigine) are the only mechanism-level validated non-opioid analgesics discussed; excluding them by design means the docking null cannot speak to the targets most relevant to CPSP pharmacotherapy. Left unstated, a reader may generalise "no target cleared both filters" to "repurposing of these classes is exhausted."
【Specific fix】 Add one sentence after Results line 126: "Because the excluded ion-channel class contains the only mechanism-level validated non-opioid analgesics (gabapentinoids via α2δ-1 and NaV1.8 inhibitors), the docking null is silent — not contradictory — regarding these targets; revisiting them requires cavity-aware/blind docking or ligand-based approaches outside this study's structure-based scope."

### Item 10 — "Undockable ≠ biologically irrelevant" is acknowledged but could be stated more forcefully as a methodological boundary
【Problem】 The framing already says the null "deliberately cannot speak to those mechanisms" (line 126), which is honest, but the abstract's "honest repurposing null" and Conclusions "methodological boundary, not a false lead" could be misread as a validated negative across all analgesic mechanisms.
【Evidence】 Abstract line 18: "the ion-channel class was undockable, so the null deliberately cannot speak to those targets." Conclusions line 136: "the honest docking null is a methodological boundary, not a false lead." Both correct.
【Why it matters】 The brief explicitly asks whether this masks a real methodological gap. It does not *mask* it (it is disclosed), but the gap — inability to dock the only validated analgesic classes — is the single largest limitation of the repurposing claim and deserves to be the *first* limitation, not buried in the docking section.
【Specific fix】 Promote the ion-channel exclusion to the head of the Limitations paragraph (currently embedded in the docking Discussion) and state plainly: "The principal boundary of this repurposing screen is that the ion-channel analgesic class — the only clinically validated non-opioid analgesic mechanisms — was structurally undockable and therefore never screened; the docking null is silent on these targets by construction."

---

## 5. Missing must-cite papers

### Item 11 — Missing must-cite: gabapentinoid / α2δ-1 DRG mechanism
【Problem】 The single most-prescribed CPSP-relevant drug class (gabapentinoids) is named in the Introduction (line 32) but its mechanism — α2δ-1 subunit up-regulation in DRG after nerve injury and reduction of presynaptic Ca²⁺ influx — is never cited, and the CPSP_literature gene set (S5) lists CACNA2D1–3 without an α2δ-1 DRG reference.
【Evidence】 Introduction line 32 "Current pharmacotherapy, gabapentinoids, NSAIDs and opioids…" — no mechanism citation. S5 CPSP_literature set (line 161) includes CACNA2D1–3 but no α2δ-1 DRG-upregulation paper. The only α2δ mention is the undockable exclusion (Methods line 168, Results line 126).
【Why it matters】 The contextual anchor for why α2δ is a "clinically validated" target (Results line 98, 126) is unsupported; a domain reviewer expects the canonical α2δ-1 nerve-injury-upregulation / gabapentinoid mechanism to be cited when the class is central to the "honest null" argument.
【Specific fix】 Add a citation such as: "the α2δ-1 subunit is up-regulated in DRG after peripheral nerve injury and mediates gabapentin/pregabalin analgesia (e.g., Li et al., J Neurosci 2004/2006 on α2δ-1 up-regulation; Taylor & Garrido 2001 or the α2δ-1 pain-mechanism reviews)." **Verify the exact reference/DOI before insertion** — I am citing this from memory and have not verified the DOI.

### Item 12 — Missing must-cite: DRG-resident / infiltrating myeloid neuroimmune sentinel literature
【Problem】 The neuroimmune endpoint is attributed to DRG, but the cited neuroimmune refs are spinal-cord microglial (Tsuda 2003, Tansley 2022) or general (Scholz & Woolf 2007); a DRG-specific myeloid/neuroimmune sentinel reference is absent, despite DRG being the tissue of the meta-core.
【Evidence】 Cited immune refs: Tsuda 2003 (spinal microglial P2X4), Inoue & Tsuda 2018 (review), Tansley 2022 (spinal cord microglia), Coull 2005 (spinal BDNF). None is a DRG myeloid sentinel primary. Yet the meta-core and hubs are DRG-derived (`MVP_PLOSONE_submission.md` line 146; Table 2).
【Why it matters】 In DRG after peripheral nerve injury the immune response is dominated by infiltrating macrophages, T-cells and satellite-glia activation, not CNS microglia; anchoring the endpoint to DRG-specific neuroimmune work is required to support the "DAM-like" claim (Item 3) and to avoid mis-assigning the signal to microglia.
【Specific fix】 Add a DRG neuroimmune sentinel citation (e.g., a primary paper or review on macrophage/cytokine signalling in injured DRG, or the Ji-lab neuroimmune-in-DRG body of work). **Verify the exact reference before insertion** — cited from memory, DOI not verified.

### Item 13 — Microglial DAM in *pain* is reasonably covered, but a second pain-DAM primary would strengthen Item 3
【Problem】 The DAM-in-pain literature beyond Keren-Shaul 2017 (Alzheimer-defined) and Tansley 2022 is thinly cited; the authors lean on Tansley 2022 for the "partial, time-/sex-dependent" qualifier, which is appropriate but singular.
【Evidence】 Discussion line 122 cites Keren-Shaul 2017 (ref 26) and Tansley 2022 (ref 21) for the DAM-in-pain claim; the remainder of the immune refs are neuropathic-pain general (Inoue & Tsuda 2018, Coull 2005, Scholz & Woolf 2007).
【Why it matters】 A second, independent pain-DAM primary (e.g., a spinal/sensory-ganglion single-cell or bulk DAM-in-neuropathic-pain study) would make the "DAM-like" qualifier more robust and less dependent on one citation.
【Specific fix】 Add one independent pain-DAM reference (verify before insertion; from memory, candidates include additional 2020–2024 spinal/sensory-ganglion microglia single-cell studies). Optional, not blocking.

---

## 6. Clinical / pain-mechanism narrative over-reach

### Item 14 — The paper mostly avoids therapeutic over-reach (good), but "MAPK14/AXL/TFE3 have the strongest prior biological rationale" edges toward implicit prioritisation
【Problem】 The manuscript explicitly says "We therefore draw no therapeutic priority from this screen" (line 128) and "no single drug is advocated" (line 130) — both correct and commendable. However, line 128 also names "MAPK14, AXL and TFE3 have the strongest prior biological rationale among the tractable targets," which, combined with TFE3 being a stable hub (bootstrap 0.885, S7), could be read as soft prioritisation.
【Evidence】 `MVP_PLOSONE_submission.md` line 128: "MAPK14, AXL and TFE3 have the strongest prior biological rationale among the tractable targets, but on our own pre-specified criteria none of them can be advanced… they are recorded as hypotheses for which the present screen provides no positive docking evidence." S7 line 275: TFE3 recovery 0.885 (most stable dock-eligible hub).
【Why it matters】 Naming three "strongest rationale" targets, even while disclaiming advancement, risks implying a rank the docking data do not support (only 4/10 retain RE significance; TFE3 was never docked). The paper is otherwise exemplary in avoiding over-reach, so this is a minor consistency tightening.
【Specific fix】 Rephrase to: "Among the tractable targets, MAPK14, AXL and TFE3 carry the most prior biological literature, but on our pre-specified criteria none can be advanced and TFE3 was never docked; they are recorded as hypotheses for which the present screen provides no positive docking evidence, and any ranking is unstable (only 4/10 retain random-effects significance)."

### Item 15 — Translational "next-step" biospecimen guidance is appropriate and not over-reaching
【Problem】 None — this is a stand-up item. The Discussion (line 130) correctly scopes human validation: neuron/glia-restricted hubs require CSF/tissue, only NPY/VIP/SERPINE1 are blood-suitable, and "plasma remains a low-yield proxy." This is honest translational guidance, not a therapeutic claim.
【Evidence】 `MVP_PLOSONE_submission.md` line 130; consistent with the honestly negative human miRNA layer (p=0.51, line 70).
【Why it matters】 Confirms the authors do not imply therapeutic guidance from an in-silico null — the brief's specific concern is addressed.
【Specific fix】 No change.

---

## § Stands up (things I suspected were wrong but found correct)

1. **Ion-channel exclusion is genuinely transparent, not hidden.** I suspected the "honest null" might bury the undockable ion-channel class. It does not: Methods line 168 and Results line 126 explicitly list the excluded targets (SCN9A/10A/11A/KCNQ2/CACNA2D1/GABRA1) and state they were "never screened" and "the null deliberately cannot speak to those mechanisms." This is the right kind of honesty.
2. **The "DAM-like" qualifier is data-supported, not metaphorical.** Discussion line 122 quantifies it: TYROBP (FDR 8.8e-9, 5/5), TREM2 (FDR 1.3e-3, 5/6) in the core, APOE directional but FDR 0.070 — so the "partial DAM" descriptor is grounded in the actual meta-core, not hand-waving.
3. **Single-cell calls are honestly bounded as "directional hints."** Lines 76–78 report 0 BH-significant genes at n=2–3/group and label all single-cell assignments "directional hints," with ambient-RNA downgrades (ATF3, AXL) and voided non-microglial clusters. No pseudoreplication over-claim.
4. **The non-circular translation test is methodologically sound and the circular numbers are not presented as evidence.** Lines 54–58 explicitly refuse to report the circular 69.5% as translation and replace it with the non-circular 46.2% vs 47.1% (p=0.14). The circular/non-circular distinction is real and well executed.
5. **Causal-scope disclosure is explicit and appropriate.** Line 175 states all findings are associations, "response"/"programme" are descriptive, and no causal/targeting claim is made. This directly answers the brief's over-reach concern.
6. **The "not CPSP-specific" conclusion is already hedged as provisional** in the Conclusions (line 136), even though I recommend tightening it (Item 8). The authors did not assert CPSP-specificity as proven.
7. **GSE267799 heterogeneity is correctly identified and disclosed** (Methods line 154: SMIR + LPI pooled, day-32 SMIR resolving), supporting the "single, heterogeneous incision arm" caveat the authors themselves use.

---

## § Questions for the authors

1. **Hub ML pooling:** Is GSE241361 mouse *spinal cord* included in the 72-sample ML pool used to define the 35 hubs (Methods line 159)? If yes, does removing it and re-deriving hubs DRG-only change the 35-gene set or the 17/9 dock-eligible split (re Item 6)?
2. **CPSP models:** Did any of the 12 accessions capture *established* chronic postsurgical pain (>3 months)? Or are all incision/nerve-injury models acute/subacute proxies (re Item 7)?
3. **OXPHOS limb:** Given random-effects q=0.31 and hub median I² 72.8%, do you intend to keep "metabolic" in the endpoint summary, or demote it to fixed-effect-only (re Item 2)?
4. **Incision arm robustness:** The day-32 SMIR samples are described as "resolving" (line 154). Did you test the non-circular translation excluding day-32 (or SMIR-only vs LPI-only) to check whether the heterogeneous/underpowered arm is what drives the p=0.14 null (re Item 7/8)?
5. **α2δ citation:** Will you supply the exact α2δ-1/gabapentinoid DRG-mechanism reference you would accept for Item 11, or should the editor propose one?
6. **Cell-type attribution:** Can the existing GSE216039 (DRG neuron-enriched) and GSE246288 (Cd11b+ microglia) data attribute the DAM genes (TYROBP/TREM2/C1QA/B/C) to neurons vs microglia vs infiltrating macrophages in DRG, to support or qualify the "microglial DAM" language (re Item 3)?

---

## § What I actually checked

**Files read (full):**
- `reviews/round12_panel_2026-09-27/_PANEL_BRIEF.md` (independence rules, output contract, per-layer checks).
- `reports/MVP_PLOSONE_submission.md` (375 lines, read in full across two passes; lines 1–200 and 200–376).
- `reports/MVP_PLOSONE_supplementary.md` (302 lines, read in full).

**Independent checks performed by reading source tables (no gate files read):**
- Endpoint gene-set values: re-read S5 (lines 146–164) and S5b (lines 170–192) and confirmed neuroinflammation mean_Z +4.94 / q 0.003; DAM +3.88 / q 0.003; complement +3.44 / q 0.003; OXPHOS −2.37 / q 0.020 (FE) / 0.31 (RE). **No discrepancy** with the main text (lines 48, 290).
- GSE267799 heterogeneity claim: confirmed against Methods line 154 (SMIR n=60 + LPI n=48 pooled; day-10/day-32 merged; day-32 SMIR "resolving"). **Matches** the Abstract/Conclusions "single, heterogeneous incision arm" caveat.
- Ion-channel exclusion: confirmed Methods line 168 list (SCN9A/10A/11A/KCNQ2/CACNA2D1/GABRA1) and Results line 126 "never screened" statement are consistent with each other and with the abstract.
- "DRG–spinal axis" occurrences: located by reading at Abstract line 14, Introduction lines 32 & 36, Author Summary line 26, Discussion line 122. Confirmed the meta-analysis is DRG-only (line 146, six DRG contrasts). This supports Item 5.
- Hub ML pooling: confirmed GSE241361 spinal cord is in the 72-sample ML pool (Methods line 159) and appears in Fig. 2 legend (line 293). Supports Item 6.
- "DAM-like" data support: confirmed Discussion line 122 quantifies TYROBP/TREM2/APOE status against the meta-core. Supports stand-up #2.
- Translation test numbers: confirmed non-circular 46.2% vs 47.1%, p=0.14 (lines 54–58) and circular 69.5% is explicitly disavowed. Supports stand-up #4.

**Citations — memory vs verified:**
- Verified-by-reading-within-manuscript (internal): all endpoint, heterogeneity, exclusion, and "axis" claims above.
- Known-from-domain-knowledge (not re-verified by web lookup during this review): Tsuda 2003 (P2X4 microglia, Nat Med), Inoue & Tsuda 2018 (Nat Rev Neurosci), Tansley 2022 (Nat Commun pain microglia), Keren-Shaul 2017 (Cell DAM), Scholz & Woolf 2007 (neuropathic triad), Coull 2005 (Nat Med BDNF), Haque 2024 (Pain DRG mitochondria), Macrae 2008 (BJA CPSP incidence). These are cited in the manuscript and I recognise them as real; I did **not** re-check their DOIs in this pass.
- From-memory, DOI-NOT-verified (recommended additions, Items 11–13): the α2δ-1 DRG up-regulation / gabapentinoid mechanism paper(s) and a DRG myeloid neuroimmune sentinel reference. These must be verified against the actual literature before insertion; I flag them as memory-based suggestions, not verified citations.

**Recomputation note:** The A1 domain brief does not require recomputation of the Stouffer/ML/docking statistics (those are A2/A3). I confined verification to (a) internal consistency between text and the supplementary source tables the manuscript points to, and (b) mechanistic coherence against domain literature. I did not run any scripts or open the CSV/JSON raw files; the endpoint and heterogeneity numbers I cite were cross-checked against the supplementary tables the manuscript itself reproduces, and I found no discrepancy.
