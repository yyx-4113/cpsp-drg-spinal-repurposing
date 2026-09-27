# A1 (Domain: Computational Neurobiology / Pain Genomics) — Independent Peer Review

**Manuscript:** *Conserved nerve-injury-associated transcriptional response on the DRG–spinal axis: dorsal root ganglion analysis with spinal-cord localisation and honest repurposing null* (single author, submitted as Yang Y).
**Review type:** First-submission independent panel review. I have read `reports/MVP_PLOSONE_submission.md` (main), `reports/MVP_PLOSONE_supplementary.md`, and `reports/MVP_PLOSONE_cover_letter.md`. I verified every quantitative claim I cite against the source tables in `results/tables/` by re-deriving the numbers directly from those files. I did not read any prior review, response, or revision document.

---

## Overall assessment

This is a transparent, well-controlled computational reanalysis that is unusually honest about its own limits (random-effects shrinkage, non-circular translation test, full-library docking with reverse controls, explicit bootstrap stability, and an explicitly "honest null" framing). The core biological story — a nerve-injury-associated neuroimmune/complement programme with heterogeneity-sensitive membership, plus a docking null that is scoped as a methodological boundary — is, with the caveats below, supported by the data I could recompute. I found **no evidence of fabrication, no substantive contradiction between claims and tables, and no grounds for desk rejection**. The issues below are mostly (a) two genuine numeric/label errors, (b) framing honesty points around REG3B and the ion-channel undockability, and (c) a small number of missing citations and consistency clean-ups. None are fatal; several are easy paste-ready fixes.

I do **not** raise a DESK-REJECT flag. The manuscript is internally consistent, reproducible from the released tables, and appropriately hypothesis-generating.

---

## §1. What stands up (claims I suspected were wrong but found correct)

**1.1 — The canonical DRG injury markers are genuinely the strongest hubs, and the data back them.** I suspected the "ATF3/SPRR1A/NPY/GAL/ECEL1 are established DRG injury markers" claim might be asserted rather than supported. Recomputing from `META_DRG_axis_stouffer.csv`: ATF3 (meta_Z = 10.53, FDR = 1.0e-21, consistency 1.0, all 6/6 up), SPRR1A (8.18, 1.3e-13, 1.0), NPY (9.27, 4.9e-17, 1.0), GAL (10.34, 3.9e-21, 1.0), ECEL1 (9.54, 5.7e-18, 1.0) — all in the 4,055-gene core, all 6/6 directionally consistent and upregulated. These are exactly the genes the field expects (Xiao et al., 2002, PNAS, which the authors do cite). The "well-established markers" sentence in the Discussion (≈ line 122) is fully earned.

**1.2 — The SCN-channel down-regulation interpretation is biologically coherent and properly hedged.** The manuscript states bulk DRG SCN9A/10A/11A/8A are down-regulated in nerve injury but up-regulated in the incision model and in the translatome, and it explicitly flags the literature tension (Nav1.6/SCN8A up-regulated in some DRG models, Ding et al. 2019). I recomputed the bulk-only meta from `META_bulkonly_meta.csv`: SCN9A −2.925/0.0108, SCN10A −3.034/0.0080, SCN11A −3.408/0.0026, SCN8A −4.924/1.0e-5 (manuscript rounds to −2.92/0.011, −3.03/0.008, −3.41/0.003, −4.92/1e-5 — match). The six-input `META_DRG_axis_stouffer.csv` confirms n_up=1/n_dn=5 for all four (the single "up" is the incision arm). The authors correctly attribute the bulk down-regulation to neuronal atrophy/loss and immune/glial dilution (citing Cooper 2024) rather than to a neuronal sodium-channel mechanism, and they explicitly reject contradiction with the protein-level Nav1.6 literature. This is the rare case where an author resisted over-claiming a "channelopathy" story; it stands up.

**1.3 — The coordinated neuroimmune programme survives set-level correction, and the "DAM-like" qualifier is disciplined.** From `P3_geneset_stats.csv` (cross-checked against `results/tables/_R4_geneset_setlevel_bh.csv`): Neuroinflammation mean_Z 4.94, frac_up 1.00, perm_p 0.0005; DAM_microglia 3.88, frac_up 0.9375; Complement 3.44, frac_up 0.944; all q = 0.003 under set-level BH. OXPHOS mean_Z −2.37, frac_up 0.263 (i.e. 73.7% of members down), perm_p 0.004, and it correctly *fails* set-level BH under random effects (q = 0.31). The authors also check the canonical DAM hallmarks individually (`META_DRG_axis_stouffer.csv`): TYROBP FDR 8.8e-9, TREM2 1.3e-3, APOE 0.070 — and honestly note APOE does not reach the core, which is why they call the signal "DAM-*like*". This is careful and stands up.

**1.4 — The "honest repurposing null" scaffolding is real, not rhetorical.** The full-library breadth flip is verified: from `results/tables/P6_breadth_chembl_power.csv`, ADRA2A Tier-1 (620-drug) AUC = 0.6184, full-library (3,070-drug) AUC = 0.5325 (p = 0.118). Reverse controls from `P6_reverse_control.csv` (AXL 0.880, TNIK 0.824, ACVR1 0.797, MAPK14 0.779, SLC2A1 0.914, ADRA2A 0.532) and the MW-confounder table (`P6_enrichment_mw_confounder_check.csv`) reproduce exactly the manuscript's ΔAUC CI-contains-zero verdicts (AXL [−0.030, +0.104]; TNIK [−0.224, +0.193]). Face validity (`P6_face_validity.csv`): 0/64 known analgesics in Top-20, rank AUC 0.538 (p = 0.146), α2-agonists AUC 0.428 (p = 0.76). The multi-filter, reverse-control, MW-adjustment design is not just claimed — the numbers are in the tables and they agree.

**1.5 — The non-circular translation test is correctly executed and correctly self-critical.** From the supplementary S6 Panel B, the apparent 69.5% core→incision concordance collapses to 46.2% (2,266/4,899) under a fully non-circular build, vs a 47.1% background (6,779/14,390), risk difference −0.9 pp, permutation p = 0.14. This is a genuine, well-controlled negative and the authors lead with it rather than hiding it. Stands up.

**1.6 — Reproducibility is real.** I re-derived the headline counts directly: core 4,055 (FE) and 1,008 (RE) from `META_DRG_axis_CORE_signature.csv` and `_R4_random_effects_meta.csv`; 32/35 hubs in core from intersecting `P3_hub_genes.csv` with the core file; RE median I² = 38.8% across genes and 72.8% across the 35 hubs; 18/35 hubs retain FDR_RE < 0.05. All match the manuscript. The data and the prose agree throughout — this is the manuscript's strongest feature.

---

## §2. Questions for the authors (I do not guess the answers)

**Q1.** For REG3B: the internal meta makes it one of the most significant genes in the entire analysis (meta_Z = 8.28, FDR = 7.1e-14 from `META_DRG_axis_stouffer.csv`), and it is upregulated in all three nerve-injury contrasts that carry data (GSE212311, GSE278227, GSE241361), with the single opposing value being the incision arm. It is excluded from the core only because its direction consistency (0.75) falls below the ≥0.8 gate — largely because both GSE265957 translatome timepoints are blank for REG3B (K effectively 4, not 6). Given that the internal direction actually *agrees* with the external CRPS-I report (Nie et al. 2025), why is REG3B framed primarily as an "external motivational hypothesis, not an internal-supporting hub" rather than as an internally meta-significant, nerve-injury-upregulated gene that merely fails the consistency gate? Please clarify whether the framing is meant to convey "not in the core" (true) or "not supported by the internal data" (false).

**Q2.** The nerve-injury-specific ML signal rests, by the authors' own admission, "principally on GSE278227 (n = 28)" because GSE212311 (n = 6) is at the statistical floor (exact MW p = 0.10) and the two GSE241361 folds are same-animal. How should a reader weigh a "DRG-axis core" whose LODO discrimination in nerve injury is essentially carried by a single adequately powered study? Is the intent that the 35-hub set be treated purely as a hypothesis-generating candidate list for orthogonal validation, and if so is that stated strongly enough relative to the "core axis" language?

**Q3.** The docking null is explicitly scoped to "docking enrichment at library scale" and the Methods note the ion-channel class "was undockable" (line 167) and "could be revisited by blind/cavity-aware docking." But the entire ion-channel class includes essentially every clinically validated neuropathic/CPSP-relevant target in the manuscript's own `CPSP_literature` gene set (SCN9A/10A/11A, CACNA2D1/α2δ, GABRA1). When the Conclusions state the screen "found no target that cleared both filters," should this be read as "no *tractable* target" — and is the caveats paragraph sufficiently prominent relative to the headline "honest repurposing null"? Please confirm the intended reading.

**Q4.** In the bulk-only sensitivity, the manuscript reports "only 211 of the 4,055 primary-core genes are not bulk-significant at all." My recomputation (below, §3) finds 211 genes that *are present in the bulk meta but fail bulk FDR*, plus a further **102 primary-core genes that are entirely absent from the bulk meta file** (translatome-only), for 313 total. Is "not bulk-significant" intended to mean "present in the 4-bulk analysis yet non-significant," or should the 102 absent genes be counted as well? Please confirm the denominator you used.

**Q5.** For the LPL DAM-hallmark sentence (Results gene-set paragraph, ≈ line 48): the stated value "meta_Z −3.43, FDR 6.1×10⁻⁴" — my recomputation from `META_DRG_axis_stouffer.csv` gives meta_Z = −3.425 and **meta_FDR = 2.63×10⁻³**. The 6.1×10⁻⁴ value is exactly the uncorrected two-sided p for Z = −3.425 (Φ(−3.425)×2 ≈ 6.1e-4). Was the raw p mislabeled as FDR, and does the same apply elsewhere? This matters because the rest of the paper is scrupulous about FDR vs p.

**Q6.** The single-cell/spatial localisation is explicitly "directional hints" with 0 BH-significant genes at n = 2–3/group. Given that, how much weight do the authors intend readers to place on the DRG "injured/regenerating neuron" localisation (Fig. 3) versus the spinal dispersion (Fig. 4A) and the Visium baseline anatomy (Fig. 4B)? Is "axis-end specialisation" (DRG neuron programme → spinal multi-compartment dispersion) over-read from n = 2–3/group pseudobulk, or is it meant purely as a map of where hubs *could* act?

**Q7.** References 22 (Divito et al., *Cleveland Clinic Journal of Medicine* 93:94–98, 2026) and 23 (Bertoch et al., *Anesthesiology* 142:1085–1099, 2025) are cited for suzetrigine. The 2026 CCJM date is post-submission-window; can you confirm both DOIs resolve and the citation details are exact? (Flagged as "verify DOI" — see §5.)

---

## §3. What I actually checked (files read, values recomputed, discrepancies stated)

**Files read in full or part:** `reports/MVP_PLOSONE_submission.md`, `reports/MVP_PLOSONE_supplementary.md`, `reports/MVP_PLOSONE_cover_letter.md`.

**Tables recomputed directly (no script output trusted; values derived from the CSVs themselves):**
- `results/tables/META_DRG_axis_stouffer.csv` (16,552 rows) and `META_DRG_axis_CORE_signature.csv` (4,055 rows): core size = 4,055 (confirmed). DRG markers (ATF3, SPRR1A, NPY, GAL, ECEL1) all meta_Z > 8, FDR < 1e-16, consistency 1.0, in core (confirmed). SCN9A/10A/11A/8A six-input: n_up=1/n_dn=5 (confirmed down in nerve injury). REG3B: meta_Z 8.28, FDR 7.1e-14, consistency 0.75, excluded from core (confirmed); lfc shows 3 up (nerve-injury) / 1 down (incision), 2 translatome blank.
- `results/tables/META_bulkonly_meta.csv` (15,735 rows): bulk-only core (FDR<0.05 & consistency≥0.8) = 2,512 (confirmed); overlap with 6-input core = 2,202/4,055 = 54.3% (confirmed); SCN bulk meta_Z/FDR match Table 1b rounding.
- `results/tables/_R4_random_effects_meta.csv`: RE core (FDR_RE<0.05 & consistency≥0.8) = 1,008 (confirmed); median I² across all genes = 38.8% (confirmed); 41.9% of genes I²>50% (confirmed); 35-hub median I² = 72.8% (confirmed); 18/35 hubs retain FDR_RE<0.05 (confirmed).
- `results/tables/P3_hub_genes.csv`: 35 hubs; symbol-intersection with the core file = 32 in core, 3 out (REG3B, ANKRD1, MEGF11) (confirmed). Note the column is stored as boolean 'True'/'False', not 'Yes'/'No' as rendered in Table 2 — cosmetic only.
- `results/tables/P3_geneset_stats.csv` and `_R4_geneset_setlevel_bh.csv`: Neuroinflammation 4.94/1.00/0.0005; DAM 3.88/0.9375/0.0005; Complement 3.44/0.944/0.0005; OXPHOS −2.37/0.263 (73.7% down)/0.004 (confirmed); Neuropeptides 2.19/0.556/0.0105; P2RX_P2RY 0.85/0.583/0.440; Nav_SCN −1.37/0.214/0.180 (confirmed — no ion-channel coordination).
- `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`: GSE278227 AUC 1.0 (n=28), GSE267799 0.677 [0.374, 0.940] (n=20), GSE241361 DRG 1.0 (n=9), GSE241361 SC 1.0 (n=9), GSE212311 1.0 (n=6) — all match the manuscript.
- `results/tables/P6_breadth_chembl_power.csv`: ADRA2A Tier-1 AUC 0.6184 (620 ligands, 88 actives), full-library 0.5325 (p=0.118) — confirmed.
- `results/tables/P6_reverse_control.csv` and `P6_enrichment_mw_confounder_check.csv`: reverse-control AUCs and ΔAUC CI verdicts all match Table 3b / S4.
- `results/tables/P6_face_validity.csv`: 0/64 analgesics in Top-20; rank AUC 0.538 (p=0.146); α2-agonists 0.428 (p=0.76) — confirmed.
- `results/tables/P4_setlevel_test.json`: human miRNA set-level perm_p = 0.5101 (manuscript p = 0.51) — confirmed; nominal t_p = 0.0285 / wilcoxon_p = 0.035 vanish under permutation (confirming the authors' "failure to detect, not absence" framing).
- `results/tables/P5_GSE325938_hub_regionalization.csv` (via S2): 17/33 dorsal-horn assignments; all 17 have top_detection ≥ 0.05 (confirmed the "all 17 passed the 5% floor" claim).

**Discrepancies I found:**
- **D1 (numeric/label error):** LPL is reported as "meta_Z −3.43, **FDR 6.1×10⁻⁴**" but the table gives meta_FDR = 2.63×10⁻³; 6.1×10⁻⁴ is the uncorrected two-sided p. See §4 issue A.
- **D2 (denominator error):** "only 211 of the 4,055 primary-core genes are not bulk-significant at all" — recomputation gives 211 *present-but-non-significant* plus **102 absent from the bulk file** = 313 total not bulk-supported (7.7%). See §4 issue B / Q4.
- **D3 (terminology):** `P3_hub_genes.csv` stores `in_meta_core` as 'True'/'False' but Table 2 renders it 'Yes'/'No' — harmless but the raw column should match the rendered table for reproducibility audits.
- **D4 (table typo):** Supplementary Table S5b (≈ lines 190–191) contains a duplicated `Sigma1` row. Cosmetic but in a display item.
- **D5 (consistency):** The "35 hubs" count is applied unevenly across modalities (DRG scRNA: 34/35 present, CRISP3 absent; spinal snRNA: 33/35 present, CRISP3+REG3B absent; Visium: 33/35 detectable, CRISP3+LNP1 all-zero). This is platform-real, not contradictory, but the reader must track three different "35-minus-k" denominators; worth one clarifying sentence.

**No fabrication / no silent contradiction detected.** Every headline number I could recompute matched the tables.

---

## §4. Must-fix list (ranked, with severity)

Severity scale used: **T0** = blocks acceptance until fixed; **T1** = should fix before acceptance (affects a conclusion or its fairness); **T2** = important clarity/accuracy fix; **T3** = minor/typographical. No item below reaches T0 for this reviewer; I recommend the manuscript be accepted after T1/T2 fixes (no desk reject).

---

### Issue A — LPL "FDR 6.1×10⁻⁴" is actually the raw p; the corrected meta_FDR is 2.63×10⁻³
- 【Problem】 A citable number in the DAM-qualification sentence mislabels an uncorrected p as an FDR, over-stating the significance of the LPL down-regulation by ~4×.
- 【Evidence】 `results/tables/META_DRG_axis_stouffer.csv`, row LPL: `meta_Z = −3.425`, `meta_FDR = 2.628e-03`. The value 6.1×10⁻⁴ equals 2·Φ(−3.425) ≈ 6.1e-4 (uncorrected two-sided p). Manuscript states "meta_Z −3.43, FDR 6.1×10⁻⁴" in the gene-set paragraph (≈ line 48) and again in Discussion (≈ line 120). I recomputed by reading the CSV directly.
- 【Why it matters】 The LPL down-regulation is the pivot on which the authors qualify "DAM-like" → "not a complete DAM state." The *direction* (down) is unchanged and the conclusion holds, but a reviewer/reader who checks the FDR will see a 4× mismatch, which undermines trust in an otherwise rigorous multiple-testing presentation. It also slightly weakens the "we are scrupulous about FDR vs p" posture.
- 【Specific fix】 Replace the sentence (≈ line 48) with:
  > "Consistent with this qualification, LPL — a canonical DAM hallmark that is up-regulated in bona fide DAM — is itself down-regulated in the nerve-injury meta (meta_Z −3.43, meta_FDR 2.6×10⁻³; uncorrected p 6.1×10⁻⁴), so the 'DAM-like' label captures the complement/immune-activation pole of the programme and should not be read as a complete DAM state."

---

### Issue B — "Only 211 primary-core genes are not bulk-significant" undercounts the true unsupported fraction (313)
- 【Problem】 The bulk-only sensitivity states 211 primary-core genes are unsupported by the bulk analysis, but 102 additional primary-core genes are *absent from the bulk meta file entirely* (translatome-only), so 313/4,055 (7.7%) are not bulk-supported, not 211 (5.2%).
- 【Evidence】 `results/tables/META_DRG_axis_CORE_signature.csv` (4,055 symbols) vs `results/tables/META_bulkonly_meta.csv` (15,735 rows). Direct intersection: 3,953 of 4,055 core genes appear in the bulk file; of those, 211 have bulk `meta_FDR ≥ 0.05` (present but non-significant); **102 are absent from the bulk file**. 211 + 102 = 313. Manuscript bulk-only paragraph (≈ line 50) claims "only 211 … are not bulk-significant at all (the genuine translatome-specific contribution to membership)." I recomputed by set subtraction on the two CSVs.
- 【Why it matters】 The sentence frames the 211 as "the genuine translatome-specific contribution to membership," which is incorrect — the 102 absent genes are the *purest* translatome-only contribution, and the 211 are merely present-but-weak in bulk. The error makes the primary core look more bulk-robust than it is and mis-attributes the source of heterogeneity-sensitivity. It is a quantitative accuracy problem in a paragraph whose entire purpose is quantitative honesty.
- 【Specific fix】 Replace (≈ line 50) with:
  > "Of the 4,055 primary-core genes, 3,953 appear in the four-bulk meta; 211 are present there yet fail bulk FDR < 0.05, and a further 102 are absent from the bulk universe entirely (translatome-only), so 313 (7.7%) of the primary-core are not supported by the bulk-only analysis. The genuine translatome-specific contribution is therefore at least 313 genes, of which the 102 absent genes are the purest translatome-only members."

---

### Issue C — REG3B framing understates its internal support (meta-significant, nerve-injury-upregulated; excluded only on consistency)
- 【Problem】 REG3B is described as an "external motivational hypothesis, not an internal-supporting hub," which is technically true for core-membership but obscures that the internal meta makes REG3B one of the most significant genes overall and directionally consistent with the cited CRPS-I report.
- 【Evidence】 `META_DRG_axis_stouffer.csv`, REG3B: meta_Z = 8.28, meta_FDR = 7.1e-14 — far more significant than many genes *in* the core — but consistency = 0.75 (3 up / 1 down / 2 translatome blank), so it fails the ≥0.8 gate. The three contrasts with data are all nerve-injury and all up (GSE212311, GSE278227, GSE241361); the single down value is the incision arm. Manuscript "Hub plausibility" (≈ line 82) and Discussion (≈ line 122). I recomputed from the CSV.
- 【Why it matters】 A reader could reasonably infer REG3B was a null internally and is being imported from one external paper. In fact the internal data *agree* with Nie et al. (2025) directionally. This is not fabrication, but the asymmetry in framing (downplay internal significance while emphasising external motivation) is a fairness/honesty nuance. It also matters because REG3B is a neurite/regeneration-associated secreted factor whose upregulation in injured DRG is mechanistically plausible, so its exclusion should be transparently "consistency-gate + low DRG detection," not "external only."
- 【Specific fix】 Revise the REG3B sentence (≈ line 82) to:
  > "We stress that REG3B is an external motivational hypothesis, not an internal-supporting *core* hub: in this study REG3B was not in the meta core (it is meta-significant, FDR 7.1×10⁻¹⁴, but its direction consistency is 0.75 because both GSE265957 translatome timepoints are blank, and it is upregulated in all three nerve-injury contrasts that carry data), was not localisable in spinal snRNA, and showed only 1.7% detection in DRG; its 'established DRG neuroimmune hub' status derives additionally from a single CRPS-I (not CPSP, not nerve-transection) report (Nie et al., 2025) and must be tested prospectively before weight is attached."

---

### Issue D — The "honest repurposing null" headline should foreground that the ion-channel class (the clinically validated analgesic backbone) was structurally undockable
- 【Problem】 The Conclusions and Abstract lead with an "honest repurposing null" that, read quickly, implies the screen examined the relevant target space; in fact the entire ion-channel class — including SCN9A/10A/11A and CACNA2D1(α2δ)/GABRA1 that the authors themselves list in the `CPSP_literature` set and discuss as validated analgesics (gabapentinoids) — was excluded as undockable.
- 【Evidence】 Methods (≈ line 167): "ion-channel candidates (SCN9A/10A/11A/KCNQ2/CACNA2D1/GABRA1) have experimental structures but lack a ligand-anchored pocket appropriate for a defined docking box, and were therefore not docked." The 10 docked/referenced targets are GPCR (ADRA2A), kinases (MAPK14, TNIK, ACVR1, ITPKC), a transporter (SLC2A1), a serpin (SERPINE1), and AXL/VASH2/GALNS. None are ion channels. Verified from `P6_reverse_control.csv` / `P6_breadth_target_summary.csv` target lists.
- 【Why it matters】 The honest-null contribution is real *for the 10 tractable targets*. But the most clinically relevant neuropathic/CPSP targets in the authors' own literature set are ion channels that the method cannot assess. If the headline is "no target cleared both filters," a clinician reader may conclude "the axis yields no druggable ion-channel hypothesis," which the data cannot support or refute. This is the single most important framing boundary to state up front, not buried in Methods.
- 【Specific fix】 Add to the Conclusions (≈ line 134) and Abstract (≈ line 18/20) a one-line boundary:
  > "The docking null is scoped to the 10 structurally tractable targets; the ion-channel class — including the α2δ/CaV and NaV targets that anchor current neuropathic-pain pharmacotherapy and that appear in our own CPSP-literature set — was structurally undockable and remains untested by this screen (blind/cavity-aware docking is required before any null can be claimed for them)."

---

### Issue E — The "DRG–spinal axis core" is in fact a DRG-only meta core; the spinal dimension is supplied separately
- 【Problem】 Title and Abstract imply an integrated DRG–spinal axis signature, but the Stouffer meta core (4,055 genes) is built entirely from DRG / DRG-translatome inputs (all six contrasts are DRG). The spinal contribution is the LODO spinal fold and the Visium/spinal-snRNA localisation, not the meta core.
- 【Evidence】 Manuscript itself discloses this at ≈ line 44 ("the spinal-cord dimension of the titular axis is supplied independently by the LODO spinal fold and the Visium …"). The six inputs listed (line 144) are all DRG or DRG translatome. Verified: `META_DRG_axis_stouffer.csv` inputs are GSE267799_DRG, GSE212311_CCI_DRG, GSE278227_CCI_DRG, GSE241361_S1R_DRG, GSE265957_Xtail_DRG_Day4/Day63 — all DRG.
- 【Why it matters】 Not a contradiction (it is disclosed), but the phrase "DRG–spinal axis" in the title/abstract could over-promise an integrative cross-tissue signature. A one-sentence precision in the Abstract would prevent mis-reading and pre-empt a reviewer objection.
- 【Specific fix】 In the Abstract (≈ line 14) adjust to: "We integrated 12 GEO datasets by Stouffer meta-analysis of the DRG axis (all six meta contrasts are DRG/DRG-translatome), then localised hubs in independent spinal-cord single-cell and spatial transcriptomes and tested generalisation with a spinal leave-one-dataset-out fold."

---

### Issue F — The nerve-injury-specific ML signal is carried by a single adequately powered study; state this as a limitation
- 【Problem】 The authors note the conclusion "rests principally on GSE278227 (n = 28)" because GSE212311 (n = 6) is at the statistical floor and the two GSE241361 folds are same-animal. This is acknowledged but could be more prominent as a limitation.
- 【Evidence】 `P3_lodo_auc_ci_leakage_controlled.csv`: GSE278227 AUC 1.0 n=28; GSE212311 AUC 1.0 n=6 (exact MW p = 0.10, stated in text line 64); GSE241361 DRG/SC n=9 same-animal. Manuscript line 64.
- 【Why it matters】 A "core axis" whose LODO discrimination in nerve injury leans on one study (n=28) is thin support for the "nerve-injury-associated response" headline. It is consistent with hypothesis-generation framing, but the limitation should sit in the Discussion/Conclusions, not only inside the Results AUC paragraph.
- 【Specific fix】 Add to Limitations (Discussion, ≈ line 126): "The nerve-injury-specific ML signal, while leakage-controlled, is carried largely by a single adequately powered study (GSE278227, n=28); GSE212311 (n=6) is at the statistical floor and the two GSE241361 folds are same-animal, so the 35-hub set is a candidate list for orthogonal validation rather than a confirmed axis signature."

---

### Issue G — Supplementary Table S5b duplicated Sigma1 row (display-item typo)
- 【Problem】 The set-level BH table repeats the `Sigma1` row twice (≈ lines 190–191), the second instance redundant.
- 【Evidence】 `reports/MVP_PLOSONE_supplementary.md` lines 190–191. Verified by reading.
- 【Why it matters】 Minor, but it is a published display item; a duplicated row looks like a generation artefact and a reviewer may wonder if other rows are duplicated.
- 【Specific fix】 Delete the second `Sigma1` row (line 191).

---

### Issue H — `in_meta_core` column uses 'True'/'False' but Table 2 renders 'Yes'/'No'
- 【Problem】 `P3_hub_genes.csv` stores `in_meta_core` as boolean strings while Table 2 shows 'Yes'/'No'; a reproducibility auditor reading the raw CSV will see a different vocabulary than the table.
- 【Evidence】 `results/tables/P3_hub_genes.csv` header `in_meta_core` values `{'True','False'}`; Table 2 (manuscript) uses 'Yes'/'No'. Verified by reading both.
- 【Why it matters】 Cosmetic, but the manuscript stresses reproducibility; raw-table vocabulary should match the rendered table for scripted audits.
- 【Specific fix】 Either map the column to 'Yes'/'No' in the CSV or add a one-line note in the Table 2 caption that the source column is boolean.

---

### Issue I — Three different "35-minus-k" denominators across localisation panels need one clarifier
- 【Problem】 DRG scRNA: 34/35 present (CRISP3 absent); spinal snRNA: 33/35 (CRISP3+REG3B absent); Visium: 33/35 detectable (CRISP3+LNP1 all-zero). The "35 hubs" framing spans three different denominators without a single orienting sentence.
- 【Evidence】 Supplementary S1 (CRISP3 and REG3B "NotLocalisable"), S2 (CRISP3 and LNP1 all-zero, REG3B present but below floor), and main text lines 74–78. Verified by reading.
- 【Why it matters】 A reader tracing a single hub (e.g., REG3B: absent from spinal, below-floor in Visium, but meta-significant) could be confused about whether "35" is the same set in every panel.
- 【Specific fix】 Add one sentence at the start of the "Hubs are a multi-cellular DRG–spinal programme" section (≈ line 72): "Across the three localisation platforms the 35-hub set is pruned differently by detectability — DRG scRNA 34/35 (CRISP3 absent), spinal snRNA 33/35 (CRISP3 and REG3B absent), Visium 33/35 detectable (CRISP3 and LNP1 all-zero) — so panel denominators differ by platform, not by redefinition of the candidate set."

---

## §5. Must-cite literature the manuscript may have missed (confidence flagged)

The reference list is reasonable (Keren-Shaul 2017 for DAM; Tansley 2022 for spinal microglia DAM; Tsuda 2003 P2X4; Xiao 2002 for DRG injury markers; Haque 2024 for DRG OXPHOS; Irwin & Shoichet 2016 and Pushpakom 2019 for repurposing caveats). The following would strengthen the domain grounding; I mark confidence:

- **Usoskin et al., 2015, *Nature Neuroscience* 18:145–153 (DOI 10.1038/nn.3887)** — the canonical mouse DRG neuronal taxonomy (11 subtypes). Highly relevant to the "injured/regenerating neuron subtype" annotation in Fig. 3 / GSE216039, which used 8 non-hub markers. The authors should cite this as the reference classifier for DRG neuron subtypes. **Confident it exists.**
- **Renthal et al., 2019, *Science Translational Medicine* (DRG chromatin/epigenetic state after peripheral nerve injury)** — directly relevant to the "neuronal atrophy/loss and transcript dilution" explanation for bulk SCN down-regulation (currently supported only by Cooper 2024). **Verify DOI** — I am confident the paper exists but did not verify the exact volume/pages.
- **For the α2δ/CACNA2D1 (gabapentinoid) target that the docking screen cannot assess** — the clinical relevance should be anchored to a gabapentinoid-mechanism citation (e.g., the established α2δ-1 literature; the authors cite the broader neuropathic-pain triad, Scholz & Woolf 2007, which is adequate but predates the α2δ structural work). Optional.
- **For docking false-positive / enrichment caveats specific to GPCRs** — the manuscript cites Irwin & Shoichet 2016 (general) and Pushpakom 2019 (repurposing). A more targeted citation on GPCR docking bias would help justify why ADRA2A's weak signal is treated cautiously. **Verify DOI** — I would suggest the authors check a recent GPCR-docking benchmark rather than me naming one I cannot verify.
- **Suzetrigine references 22–23** (Divito 2026 CCJM; Bertoch 2025 *Anesthesiology* 142:1085–1099) — please confirm both DOIs resolve; the 2026 CCJM date is unusual for a submitted manuscript. **Verify DOI.**

I do **not** recommend citing additional papers to "pad" the neuroimmune or OXPHOS sections; those are adequately covered.

---

## §6. Minor notes (non-blocking)

- The manuscript's repeated "to our knowledge, to our knowledge" double-phrasing in the Introduction (≈ line 36) is a copy-edit artifact worth a single pass.
- The AI-use disclosure is appropriate and specific; no action needed.
- The STROBE checklist and compliance check were available to me but outside the domain scope; I note only that the manuscript's claims are consistent with them.

---

## Bottom line for the editor

Accept after minor revision. The biology is, on the data I could recompute, honestly reported; the two genuine errors (LPL FDR mislabel, the 211-vs-313 bulk-unsupported denominator) are simple fixable inaccuracies, not misconduct. The framing around REG3B and ion-channel undockability should be tightened so the "honest null" is not over-read as "no druggable hypothesis exists." No desk-reject flag. The manuscript's greatest strength — reproducibility and self-critical multiple-testing — is real and should be preserved through copy-editing.
