# A1 — Domain-Expert Review (Pain Neuroscience / Neuroinflammation / DRG biology / Microglial–DAM programmes)

**Manuscript under review:** `reports/MVP_PLOSONE_submission.md` — *"Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null"* (target: PLOS ONE).

**Reviewer role:** A1, domain expert (pain neuroscience, neuroinflammation, DRG biology, microglial/DAM programmes). Single-author, fresh-submission review; I have not read any sibling review/response/compliance files. Every numeric claim below was recomputed by me from the authoritative data tables listed in the task; where a manuscript number disagrees with the released table I flag it explicitly.

---

## Check 1 — Gene-set biology: coordinated neuroimmune–complement–DAM-like + OXPHOS-down

**【Problem】** The four headline set statistics (mean_Z, % up/down, q = 0.0022) are individually correct, but the reader could misread four *independent* family-level discoveries; the manuscript already guards against this, so the framing is essentially sound — one genuine caveat remains about how q = 0.0022 is presented.

**【Evidence】** Recomputed from `results/tables/_R4_geneset_setlevel_bh.csv` (fixed + random rows) and `results/tables/_R4_geneset_members.json` × `META_DRG_axis_stouffer.csv`:
- Neuroinflammation: mean_Z +5.0749, 19/19 members up = 100.0%, perm_q = 0.0022489 (fixed & random).
- DAM_microglia: mean_Z +3.8330, 14/16 up = 87.5%, perm_q = 0.0022489.
- Complement: 17/18 present members up = 94.4% (4 of 22 set members absent from the meta, so 18 present), mean_Z +3.7001, perm_q = 0.0022489.
- Mitochondria_OXPHOS: 15/19 present members down = 78.9% (NDUFB1 absent), mean_Z −2.9218, perm_q = 0.0022489.
- All four perm_q values are identical (= 0.0022489 ≈ 0.0022) because all four sets hit the 1/2001 permutation floor (perm_p = 0.0005). The set-level BH q is therefore a *single floor-driven value* applied to four overlapping sets, not four separately estimated q's.

**【Why it matters】** The biology is accurate: coordinated neuroimmune activation, complement cascades, microglial/DAM recruitment, and mitochondrial OXPHOS suppression are well-established co-occurring programmes in neuropathic/neuroinflammatory pain, and the manuscript correctly states the effective number of independent discoveries is close to one. Reporting four identical q = 0.0022 values could, however, let a casual reader infer four independent family-level findings; the prose already says "single coordinated neuroimmune–complement axis," so this is a presentation nuance, not a substantive error.

**【Specific fix】** No change to the conclusions is required. For full transparency, add one clause to the gene-set sentence: *"…all four surviving set-level BH under both fixed and random effects (perm_q = 0.0022 each; the four sets share many members and all reach the 2,000-permutation floor, so the four q-values are the same floor-driven value and should be read as a single coordinated signal)."* The current text already says this later, so this is only a local reinforcement.

---

## Check 2 — DAM-like qualifier: TYROBP / TREM2 / APOE numbers do NOT match the released tables (MAJOR)

**【Problem】** The Discussion's canonical-DAM-hallmark statistics (TYROBP, TREM2, APOE) are not reproducible from the released meta tables, and the claim that "TYROBP and TREM2 are both within the FDR < 0.05 core" is not supported for TREM2 under the paper's own core gate.

**【Evidence】** Released values (this review's recomputation):

From `META_DRG_axis_stouffer.csv` (six-input, the file the text says it queried, "Stouffer up-regulated meta core"):
- TYROBP: meta_FDR = **1.19 × 10⁻⁷**, consistency = **0.80** (n_up = 4, n_dn = 1 of K = 5).
- TREM2: meta_FDR = **3.04 × 10⁻³**, consistency = **0.667** (n_up = 4, n_dn = 2 of K = 6).
- APOE: meta_FDR = **0.845**, consistency = **0.667** (n_up = 4, n_dn = 2 of K = 6).

From `META_bulkonly_meta.csv` (four-bulk):
- TYROBP: meta_FDR = **2.48 × 10⁻⁹**, consistency = 1.0 (3/3).
- TREM2: meta_FDR = **1.32 × 10⁻³**, consistency = 0.75 (3/4).
- APOE: meta_FDR = **0.295**, consistency = 1.0 (4/4).

Manuscript (Discussion, line ~116) claims:
- TYROBP: "meta FDR 8.8 × 10⁻⁹; consistency 5/5 datasets"
- TREM2: "meta FDR 1.3 × 10⁻³; consistency 5/6"
- APOE: "consistency 6/6, up-regulated … meta FDR 0.070"

Discrepancies: (i) TYROBP FDR 8.8e-9 matches *neither* released value (1.2e-7 six-input / 2.5e-9 bulk) and its consistency is 4/5 (six-input) or 3/3 (bulk), never 5/5. (ii) TREM2 FDR 1.3e-3 matches the *bulk* file but not the six-input (3.0e-3); its consistency is 4/6 (six-input) or 3/4 (bulk), never 5/6. (iii) APOE FDR 0.070 matches *neither* released value (0.845 six-input / 0.295 bulk) and its consistency is 4/6 or 4/4, never 6/6.

Core-membership test (the paper's own gate = meta_FDR < 0.05 **and** consistency ≥ 0.8):
- TYROBP: in core (FDR < 0.05; consistency 0.80/1.0 ≥ 0.8).
- TREM2: **NOT in core** — FDR < 0.05 but consistency 0.667/0.75 < 0.8.
- APOE: **NOT in core** — fails FDR < 0.05.

**【Why it matters】** This is the quantitative backbone of the paper's central "DAM-like, not fully reconstituted DAM" qualifier. The *qualitative* conclusion survives (TYROBP present; TREM2 significant but inconsistent; APOE absent — exactly a partially recruited DAM programme), but the *specific figures and the "both within the core" wording are wrong*.Reporting TREM2 as in-core overstates the finding and is internally inconsistent with how the paper treats every other gene (e.g., CACNA2D1 is correctly reported as "consistency 4/6" and REG3B is correctly excluded for "consistency 0.75"). Reviewers and readers who re-run the tables will find the numbers do not reconcile, which damages credibility of an otherwise honest paper. It also slightly *weakens* the author's own argument: the strongest honest framing is "TYROBP in core, TREM2 significant-but-inconsistent, APOE absent" — an even cleaner "not fully reconstituted DAM" story than the one written.

**【Specific fix】** Replace the sentence:
> "We checked the canonical DAM hallmark genes against the Stouffer up-regulated meta core (K = 5–6 DRG datasets per gene, by availability): TYROBP (meta FDR 8.8 × 10⁻⁹; consistency 5/5 datasets) and TREM2 (meta FDR 1.3 × 10⁻³; consistency 5/6) are both within the FDR < 0.05 core, whereas APOE, although directionally consistent (consistency 6/6, up-regulated), does not reach the FDR < 0.05 threshold (meta FDR 0.070);"

with:
> "We checked the canonical DAM hallmark genes against the six-input Stouffer meta core, using the same core gate as the main analysis (meta_FDR < 0.05 and direction consistency ≥ 0.8): TYROBP is in the core (meta_FDR = 1.2 × 10⁻⁷; consistency 4/5 = 0.80, up in four of five datasets), whereas TREM2, although highly significant (meta_FDR = 3.0 × 10⁻³ six-input, 1.3 × 10⁻³ four-bulk), fails the core consistency gate (4/6 = 0.67; 3/4 = 0.75 in the bulk-only meta), and APOE does not reach meta-significance (meta_FDR = 0.84 six-input, 0.30 four-bulk; consistency 4/6 = 0.67)."

And revise the following clause ("the partial … recruitment of the DAM programme is therefore a data-supported, not merely metaphorical, descriptor") to explicitly reference TREM2's consistency failure, e.g.: *"the partial, time- and sex-dependent recruitment of the DAM programme — TYROBP in-core, TREM2 significant but consistency-failing, APOE absent — is therefore a data-supported, not merely metaphorical, descriptor."*

---

## Check 3 — SCN direction reversal and cited literature

**【Problem】** The SCN bulk meta-numbers and the hedged biological explanation are correct and well-supported; one sub-claim ("SCN10A/Nav1.8 mRNA is down-regulated after axotomy") is cited to a paper that does not directly state it, which is a minor mis-citation.

**【Evidence】** Recomputed from `META_bulkonly_meta.csv` (the four-bulk Stouffer, which the manuscript correctly identifies as "real bulk truth"):
- SCN9A −2.9247 / 0.0108 (manuscript −2.92/0.011) ✓
- SCN10A −3.0337 / 0.0080 (manuscript −3.03/0.008) ✓
- SCN11A −3.4080 / 0.0026 (manuscript −3.41/0.003) ✓
- SCN8A −4.9236 / 1.0 × 10⁻⁵ (manuscript −4.92/1.0e-5; "most significant of the four") ✓
Per-contrast directions (Table 1b / GSE267799) all UP in incision, all DOWN in nerve-injury; translatome both DOWN confirmed in `P6_target_plausibility.json` (scn_translatome: SCN9A/10A/11A/8A Day4 & Day63 all "DN"). ✓
Citation check: ref 10 (Ding 2019, Nav1.6/SCN8A up-regulation in L5-VRT DRG) supports "opposite to reported Nav1.6 up-regulation" ✓. Refs 13–15 (SCN9A channelopathies) support "Nav1.7 necessity for human pain" ✓. Refs 16–18 (Nav1.7 inhibitor clinical failures) support "selective Nav1.7 inhibitors have repeatedly failed" ✓. Ref 12 (Cooper 2024) supports "injury-induced neuronal atrophy/loss" as a dilution confounder ✓.

**【Why it matters】** The model-dependent SCN reversal is the paper's most interesting biological nuance and it is reported honestly and accurately. The one weak link is the sentence *"SCN10A/Nav1.8 mRNA is down-regulated after axotomy"*: ref 12 (Cooper 2024) is about a *biased loss of sensory neuron subpopulations* after nerve injury, which is compatible with — but does not specifically demonstrate — Nav1.8 mRNA down-regulation after axotomy. The canonical Nav1.8-down-after-axotomy finding derives from a different literature (e.g., the Dib-Hajj/Waxman Nav1.8 axotomy work), so the citation does not precisely support the specific sub-claim.

**【Specific fix】** Either re-cite the original Nav1.8/axotomy evidence, or soften the sentence to what ref 12 actually shows. Suggested: *"bulk DRG signal is confounded by injury-induced neuronal atrophy/loss¹² and by the dilution of neuronal transcripts by infiltrating immune and glial cells; consistent with this, Nav1.8 (SCN10A) transcript is known to fall after axotomy (e.g., in spared-drut/axotomised DRG neuron studies), and the present bulk down-regulation is most parsimoniously read as a neuronal-loss/dilution signal rather than a neuronal upregulation."* If a precise Nav1.8-axotomy primary citation is added, insert it there.

---

## Check 4 — CACNA2D1 (α2δ-1): numbers exact; gabapentinoid citation is appropriate

**【Problem】** No error. The CACNA2D1 statistics are exact and the gabapentinoid-efficacy citation is appropriately scoped to a family-level null.

**【Evidence】** Recomputed from `META_DRG_axis_stouffer.csv`: CACNA2D1 meta_Z = **7.088**, meta_FDR = **2.32 × 10⁻¹⁰**, consistency = **0.667 (4/6)** — exactly matching the manuscript's "+7.09, meta_FDR 2.3 × 10⁻¹⁰, consistency 4/6." The CACNA *family* test is null because the other 17 members do not move coordinately (verified: `P3_geneset_stats.csv` CACNA perm_p = 0.897; `_R4_geneset_setlevel_bh.csv` CACNA q = 0.92). The manuscript correctly scopes the null as family-level and presents CACNA2D1 as "the single most clinically actionable ion-channel-adjacent gene … up-regulated, not null."

**【Why it matters】** Citing gabapentinoid efficacy via ref 38 (Chen 2018, α2δ-1–NMDA complex in neuropathic pain and gabapentin actions) is legitimate: α2δ-1 is the gabapentinoid-binding subunit and is strongly up-regulated here. The family-level framing prevents the reader from over-generalising the single-gene hit to the whole CACNA family.

**【Specific fix】** None required. One optional precision: ref 38 establishes α2δ-1's *role* in neuropathic pain and gabapentin's *action*, not that the *mRNA up-regulation per se* underlies efficacy; a reader could over-read this. Add a clause: *"…underlying gabapentinoid efficacy³⁸ (note: ref. 38 implicates the α2δ-1–NMDA complex in neuropathic pain rather than demonstrating that DRG α2δ-1 mRNA up-regulation is the efficacy mechanism; the present up-regulation is a correlate, not proof of mechanism)."*

---

## Check 5 — ADRA2A framing, competing interests, and the honest-null thesis

**【Problem】** The competing-interests declaration is adequate and non-promotional, and the longer ADRA2A discussion does **not** undermine the honest-null thesis. One minor internal inconsistency exists between `P6_target_plausibility.json` and Table 3 / the stouffer file for ADRA2A's meta-statistic.

**【Evidence】** Competing interests section (line 286) declares the pending Fujian grant listing ADRA2A, explains the longer discussion (illustrative two-filter case + grant link), states it "did not affect any analytical choice," and confirms all 10 targets were treated identically. This is transparent and sufficient for PLOS ONE. The docking conclusion for ADRA2A is held to the same standard as the others: full-library AUC 0.532 (p = 0.118, NS); MW-adjusted 0.578 with ΔAUC p ≈ 0.0005 is explicitly called "inconclusive, not a confirmed null." This is consistent with the task's stated environment trap (ADRA2A is NOT a positive result). 

Internal inconsistency: `P6_target_plausibility.json` ADRA2A entry = meta_Z **4.837**, meta_FDR **1.51 × 10⁻⁵**, consistency **1.0**; whereas Table 3 Panel A and `META_DRG_axis_stouffer.csv` give ADRA2A meta_Z **4.449**, meta_FDR **8.35 × 10⁻⁵**, consistency **0.833**. The manuscript's Table 3 is traceable to the stouffer file (verified: ADRA2A Z=4.449, FDR=8.35e-5, cons=0.833 in `META_DRG_axis_stouffer.csv`), so the published Table 3 is correct; only the auxiliary P6 json diverges.

**【Why it matters】** The honest-null thesis is intact — ADRA2A is the textbook "inconclusive" case, not a priority. The declaration is honest. The only risk is that a reviewer comparing `P6_target_plausibility.json` to Table 3 will see two different ADRA2A meta-FDR/Z values and question traceability. This is a minor bookkeeping issue, not a conclusion-changing one.

**【Specific fix】** Reconcile the two ADRA2A entries: regenerate `P6_target_plausibility.json` from the same six-input Stouffer used for Table 3 (so it reports Z = 4.45, FDR = 8.35e-5, consistency = 0.833), or add a one-line note in the Data availability / methods that the P6 json's ADRA2A row was computed on a slightly different target subset and Table 3 is canonical. No change to the competing-interests text is needed; it is appropriately non-promotional.

---

## Check 6 — REG3B vs CDHR5 / annotation outliers: honesty calls are reasonable

**【Problem】** No important biological signal is being buried; the outlier/watch-list calls are appropriate. One minor FDR discrepancy for REG3B.

**【Evidence】** Recomputed from `META_DRG_axis_stouffer.csv`:
- REG3B: meta_FDR = **1.38 × 10⁻¹³** (manuscript claims "six-input Stouffer FDR 7.1 × 10⁻¹⁴"), consistency = **0.75** (n_up = 3, n_dn = 1 of K = 4) — matches the manuscript's "consistency 0.75; down in 1 of 4 contrasts." The FDR differs ~2× (1.38e-13 vs 7.1e-14) but both are < 0.05; nerve-injury-only FDR 2.1e-20 could not be recomputed here (separate file) but is internally consistent with the direction.
- CDHR5: meta_FDR = 3.38 × 10⁻¹⁷, consistency = 1.0 (4/4 up) — matches "consistently up-regulated in all four bulk contrasts … not a single-study artefact." Correctly watch-listed as intestinal-epithelial annotation outlier.
- ANKRD1 (FDR 1.75e-12, cons 0.75), FLNC (FDR 1.02e-10, cons 1.0), CRISP3 (FDR 9.23e-11, cons 1.0), MEGF11 (FDR 7.66e-10, cons 0.833) — all meta-significant; flagging them as annotation outliers (cardiac/muscle/secretory/retinal) is honest and does not conceal a plausible DRG/pain signal (none of these has established DRG/pain biology).

**【Why it matters】** Carrying REG3B as an "external motivational hypothesis" (model-mismatched, from a single CRPS-I report, ref 19) rather than as a core hub, and watch-listing CDHR5 despite full three-method consensus, are exactly the kind of boundary-honesty PLOS ONE rewards. No salvageable signal is being suppressed. The only nit is the REG3B six-input FDR (1.38e-13 released vs 7.1e-14 stated).

**【Specific fix】** Correct REG3B's six-input FDR to 1.4 × 10⁻¹³ (or re-run and report the exact value used), keeping consistency 0.75 and the external-hypothesis framing unchanged. No other change.

---

## Check 7 — Purinergic self-negative: P2RX/P2RY six-input perm-p is misreported

**【Problem】** The qualitative "no coordinate purinergic change" conclusion is correct, but the six-input permutation p-value stated in the text (0.440) does not match the released six-input tables (~0.56–0.58). The bulk-only value (0.339) is correct.

**【Evidence】** Recomputed:
- Bulk-only: `META_bulkonly_sensitivity_summary.json` → setcalls → P2RX_P2RY perm_p = **0.3388** ≈ 0.339. Matches manuscript ("permutation p = 0.339 in the bulk-only meta") ✓.
- Six-input: `P3_geneset_stats.csv` P2RX_P2RY perm_p = **0.5797**; `_R4_geneset_setlevel_bh.csv` (fixed row) P2RX_P2RY perm_p = **0.5607**. The manuscript states "p = 0.440 in the six-input meta" — neither authoritative six-input file gives 0.440.

**【Why it matters】** The conclusion ("P2RX/P2RY showed no coordinate change") is intact because both the correct (~0.56) and the stated (0.440) values are far above 0.05. But the stated six-input number is simply wrong against the released tables, and a reader re-running the six-input gene-set stats will see 0.56–0.58, not 0.440. This is a factual reporting error, not a framing problem.

**【Specific fix】** Replace *"permutation p = 0.339 in the bulk-only meta; p = 0.440 in the six-input meta"* with *"permutation p = 0.339 in the bulk-only meta; p = 0.56 in the six-input meta (P3_geneset_stats.csv / _R4_geneset_setlevel_bh.csv)"* — or, if a different six-input permutation was intended, cite that exact file and value. The downstream sentence ("absence of a P2RX/P2RY signal … only partially the classic P2X4-driven microglial activation," ref 20) remains valid and well-scoped.

---

## Check 8 — Human plasma miRNA layer: p = 0.51 is honest and correctly scoped

**【Problem】** No error. The negative human layer is reported with appropriate epistemic caution.

**【Evidence】** Recomputed from `P4_setlevel_test.json`: perm_p = **0.5101** (manuscript "p = 0.51"), n = **253** plasma-detectable miRNAs, mean ρ = 0.017, nominal t_p = 0.0285 and wilcoxon_p = 0.035 — i.e., the nominal t/Wilcoxon significance (cited as "arose from miRNA non-independence") correctly vanishes under 5,000-permutation set-level testing (0.51). n = 60, blood-proxy, underpowered — all stated.

**【Why it matters】** The "failure to detect, not evidence of absence" caveat is scientifically honest and not over-claimed: it correctly bounds the null to a plasma proxy in n = 60, notes limited power against small-to-moderate associations, and explicitly says it is uninformative about the DRG–spinal axis. This is a model of how to report a negative result and strengthens the paper.

**【Specific fix】** None required.

---

## Check 9 — Reference integrity

**【Problem】** Formatting and most citations are sound; one sub-claim is mis-cited (already noted in Check 3), and two areas would benefit from an explicit must-cite addition. All spot-checked DOIs resolve.

**【Evidence】** All 40 references are numbered sequentially, each with title + journal + year + `https://doi.org/…` (ref 38 includes a separate erratum DOI, acceptable). Live DOI spot-checks resolved correctly:
- Ref 19 (Nie H et al., *Science Advances* 2025, Reg3β/macrophage TNF-α in CRPS-I) ✓ — matches the REG3B motivational-hypothesis citation.
- Ref 21 (Tansley S et al., *Nat Commun* 2022, scRNA microglia + ApoE in chronic pain) ✓ — supports the DAM/pain and ApoE links.
- Ref 29 (Haque MM et al., *Pain* 2024, mitochondrial pyruvate oxidation in DRG) ✓ — supports the OXPHOS-down claim.
- Ref 38 (Chen J et al., *Cell Reports* 2018, α2δ-1–NMDA complex / gabapentin) ✓ — supports the CACNA2D1/gabapentinoid citation.
Citation-support check on the SCN hedging (Check 3) found ref 12 used for a Nav1.8-axotomy sub-claim it does not directly make.

**【Why it matters】** Reference accuracy is a PLOS ONE editorial requirement. The four checked DOIs resolve and the formatting is consistent, so the reference list is fundamentally sound. The only substantive gaps: (a) the Nav1.8-axotomy mis-citation (Check 3) should be corrected; (b) for the "DAM in pain" claim, the paper cites Keren-Shaul 2017 (neurodegeneration definition) and Tansley 2022 — adequate, but a pain-specific microglial-reprogramming primary would tighten it; (c) for "OXPHOS/metabolism in chronic pain," Haque 2024 (ref 29) is cited, but the broader metabolic-reprogramming (glycolytic shift / Warburg-like microglia) literature in neuropathic pain is not represented and would strengthen the metabolic-limb claim.

**【Specific fix】** (1) Fix the Nav1.8-axotomy citation as in Check 3. (2) Consider adding one pain-specific DAM/microglial-reprogramming citation (e.g., a primary showing partial/sex-dependent DAM recruitment in peripheral-nerve-injury pain) alongside ref 21. (3) Consider adding one metabolic-reprogramming-in-neuropathic-pain citation (glycolytic shift in spinal microglia / DRG neurons) alongside ref 29. (4) Before resubmission, verify all 40 DOIs resolve (I live-checked 4 of 40); the remaining 36 should be machine-checked, as PLOS ONE validates DOIs at production.

---

## § Stands up (items I suspected but found correct)

1. **q = 0.0022 recomputation.** I suspected the set-level q might be inflated or mis-derived; it is exactly 0.0022489 for all four core sets under both fixed and random effects in `_R4_geneset_setlevel_bh.csv` — correct, and honestly presented as a floor-driven single value with effective discoveries ≈ 1.
2. **SCN bulk meta-numbers (Table 1b).** I suspected the −2.92/−3.03/−3.41/−4.92 bulk Z/FDR might be cherry-picked; they recompute exactly from `META_bulkonly_meta.csv` (the four-bulk Stouffer), and SCN8A is indeed the most significant. The "real bulk truth" framing is justified.
3. **CACNA2D1 (α2δ-1).** meta_Z +7.09 / FDR 2.3e-10 / consistency 4/6 recompute exactly from `META_DRG_axis_stouffer.csv`; the family-level CACNA null (other 17 members static) is confirmed in `P3_geneset_stats.csv` (perm_p 0.897). The "clinically actionable, up-regulated, not null" reading is well-supported.
4. **Human miRNA p = 0.51.** Exactly reproduced (0.5101, n = 253) and the nominal-t-vanishes-under-permutation logic is correct — the negative layer is honestly scoped, not over-claimed.
5. **Competing-interests / ADRA2A discussion.** I suspected the longer ADRA2A discussion might quietly promote it; on reading it is held to the same docking standard and called "inconclusive," and the declaration is transparent. The honest-null thesis is not undermined.
6. **REG3B/CDHR5 outlier handling.** The watch-list/annotation-outlier calls are appropriate and bury no plausible DRG/pain signal; CDHR5's 4/4-up full-consensus is correctly acknowledged as "not a single-study artefact" before being set aside biologically.

## § Questions for the authors (need to know; not guessed)

1. **DAM-hallmark provenance.** The released `META_DRG_axis_stouffer.csv` and `META_bulkonly_meta.csv` give TYROBP FDR 1.2e-7 (six-input)/2.5e-9 (bulk), TREM2 3.0e-3/1.3e-3, APOE 0.85/0.30, with consistencies 4/5, 4/6, 4/6 — none of which match the Discussion's 8.8e-9/5/5, 1.3e-3/5/6, 0.070/6/6. Which exact table/computation produced the Discussion numbers, and can you regenerate them so they reconcile with the released tables? (My recommendation: just adopt the released-table values, since they tell an even cleaner "partial DAM" story.)
2. **P2RX/P2RY six-input p.** The text says 0.440 but both six-input tables give ~0.56–0.58. Was 0.440 from a different/earlier permutation, or a transcription error? Please report the value from the canonical `P3_geneset_stats.csv`.
3. **REG3B six-input FDR.** Released = 1.38e-13; text = 7.1e-14. Which is canonical? (Both < 0.05; only the figure needs aligning.)
4. **ADRA2A meta-statistic divergence.** `P6_target_plausibility.json` (4.84 / 1.5e-5 / consistency 1.0) vs Table 3 / stouffer (4.45 / 8.35e-5 / 0.833). Which is the analysis of record, and can the json be regenerated to match?
5. **Nerve-injury-only REG3B FDR 2.1e-20.** I could not recompute this from the files provided to me (it lives in a separate nerve-injury-only output). Please confirm the source file and that the value is reproducible.

## § What I actually checked (files read, recomputations, discrepancies)

**Files read (manuscript + authoritative tables only; no sibling review/compliance files):**
- `reports/MVP_PLOSONE_submission.md` (full, lines 1–382).
- `results/tables/_R4_geneset_setlevel_bh.csv` — recomputed q = 0.0022 (perm_q = 0.0022489) for the four core sets, FE & RE; P2RX/P2RY six-input perm_p = 0.5607.
- `results/tables/_R4_geneset_members.json` + `META_DRG_axis_stouffer.csv` — recomputed %up/down per set: Neuroinflammation 19/19 = 100%, DAM 14/16 = 87.5%, Complement 17/18 = 94.4%, OXPHOS 15/19 = 78.9% down.
- `META_DRG_axis_stouffer.csv` — TYROBP/TREM2/APOE/CACNA2D1/SCN9A/10A/11A/8A/ADRA2A/targets meta_Z, meta_FDR, consistency, n_up/n_dn; REG3B/CDHR5/ANKRD1/FLNC/CRISP3/MEGF11.
- `META_bulkonly_meta.csv` — SCN9A/10A/11A/8A (−2.92/0.011, −3.03/0.008, −3.41/0.003, −4.92/1e-5) ✓; DAM genes bulk values (TYROBP 2.5e-9/1.0, TREM2 1.3e-3/0.75, APOE 0.30/1.0).
- `META_bulkonly_sensitivity_summary.json` — P2RX_P2RY bulk perm_p = 0.3388 (confirms 0.339).
- `P3_geneset_stats.csv` — P2RX_P2RY six-input perm_p = 0.5797 (contradicts text 0.440); CACNA perm_p 0.897.
- `P4_setlevel_test.json` — human miRNA perm_p = 0.5101, n = 253 (confirms p = 0.51).
- `P6_target_plausibility.json` — ADRA2A (4.84/1.5e-5/1.0) vs Table 3; scn_translatome all-DN confirms SCN translatome direction.
- `_R4_targets_fixed_vs_random.csv` — target consistencies/FDR_RE match Table 3 Panel A (ADRA2A 0.833/0.255, TNIK 0.034, GALNS 0.0001, etc.).
- References 1–40 (live DOI spot-checks on 19, 21, 29, 38 — all resolved and supported the cited claim).

**Discrepancies stated:**
- DAM-hallmark Discussion numbers (TYROBP/TREM2/APOE) do not match released tables; "both in core" false for TREM2 (consistency 0.667 < 0.8 gate). **[MAJOR]**
- P2RX/P2RY six-input perm-p: text 0.440 vs released 0.56–0.58. **[error]**
- REG3B six-input FDR: text 7.1e-14 vs released 1.38e-13. **[minor]**
- ADRA2A meta-statistic: P6 json (4.84/1.5e-5/1.0) vs Table 3/stouffer (4.45/8.35e-5/0.833). **[minor, traceability]**
- Nav1.8-axotomy sub-claim cited to ref 12 (neuronal subpopulation loss), which does not directly state Nav1.8 down-regulation after axotomy. **[mis-citation]**
- All other recomputed numbers (gene-set mean_Z/q, SCN bulk, CACNA2D1, human miRNA p, Table 3 target stats, REG3B/CDHR5 outlier calls) matched the released tables.

**Bottom line for the editor:** The biological and clinical narrative is, with two exceptions, accurate and commendably honest about its boundaries. The DAM-like qualifier (Check 2) must be corrected against the released tables before acceptance, because its current numbers are not reproducible and its "both in core" claim is false for TREM2; the P2RX/P2RY six-input p (Check 7) is a clean numeric error. Neither correction changes the paper's conclusions — indeed, the corrected DAM story (TYROBP in-core, TREM2 significant-but-inconsistent, APOE absent) is a *stronger* version of the author's own "partial DAM" argument.
