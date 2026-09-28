# A1 — Independent Domain Review (Pain Neurobiology / DRG–Spinal-Axis Transcriptomics)

**Reviewer:** A1 (domain expert, DRG–spinal-axis nerve-injury transcriptomics)
**Manuscript:** "Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null" (single-author PLOS ONE resubmission; reviewed *as a first submission*)
**Evidence base:** `reports/MVP_PLOSONE_submission.md`; `results/tables/META_DRG_axis_stouffer.csv`, `META_DRG_axis_CORE_signature.csv`, `P3_hub_genes.csv`, `_R4_nerveinjury_only_summary.json`, `_R4_supplementary_summary.json`, `_R4_translation_noncircular.json`.
**Reproducibility stance:** every number cited below was re-read/recomputed from the raw CSV/JSON, not from the manuscript transcription.

---

## FINDING 1 — CRITICAL. Table 3a target meta-values are not reproducible from the cited source CSV

【Problem】 The ten-target biological-plausibility table (Results "Panel A/B", and the Table 3a display item) reports `meta_Z`, `meta_FDR`, and `consistency` values that disagree, often substantially, with the file the manuscript itself names as the source (`META_DRG_axis_stouffer.csv`, cited at Methods and Data Availability).

【Evidence】 Comparing the manuscript (lines 98–112) with the two provided source CSVs (which agree with each other exactly):

| Target | MS meta_Z | CSV meta_Z | MS meta_FDR | CSV meta_FDR | MS cons | CSV cons |
|---|---|---|---|---|---|---|
| ADRA2A | 4.84 | 4.4487 | 1.5e‑5 | 8.35e‑5 | 1.00 | 0.8333 |
| MAPK14 | 6.09 | 5.1220 | 3.9e‑8 | 5.39e‑6 | 1.00 | 0.8333 |
| ITPKC | 7.18 | 6.7616 | 8.1e‑11 | 1.56e‑9 | 1.00 | 0.8333 |
| SLC2A1 | 6.83 | 5.5854 | 6.3e‑10 | 6.57e‑7 | 1.00 | 0.8333 |
| TNIK | 8.00 | 8.0000 | 4.3e‑13 | 8.59e‑13 | 1.00 | 0.8333 |
| ACVR1 | 6.95 | 6.9458 | 3.2e‑10 | 5.42e‑10 | 1.00 | 1.00 |
| SERPINE1 | 6.92 | 6.9199 | 3.7e‑10 | 6.34e‑10 | 1.00 | 1.00 |
| AXL | 6.14 | 6.1424 | 2.9e‑8 | 4.04e‑8 | 1.00 | 1.00 |
| GALNS | 5.79 | 6.0836 | 1.8e‑7 | 5.53e‑8 | 0.83 | 0.8333 |
| VASH2 | 6.00 | 5.9419 | 6.4e‑8 | 1.13e‑7 | 0.83 | 0.8333 |

The `consistency` column is reported as **1.00 for ADRA2A, MAPK14, ITPKC, SLC2A1, TNIK** in the manuscript, but the CSV shows **0.8333** for all five. `meta_Z` is off by 0.39–1.25 (SLC2A1: 5.59→6.83; MAPK14: 5.12→6.09; ITPKC: 6.76→7.18; ADRA2A: 4.45→4.84). `meta_FDR` differs by factors of 5.6× (ADRA2A) to ~1000× (SLC2A1). AXL/ACVR1/SERPINE1 are internally consistent (their six-input consistency is genuinely 1.00), which confirms the CSV is the intended source and the other rows are simply wrong.

【Why it matters】 This is a data-integrity problem, not a rounding artefact. The ten-target table is the quantitative backbone of the entire "honest docking null" narrative and the only place the reader sees per-target meta-evidence. If the table cannot be regenerated from the deposited source, every downstream claim that leans on these numbers (e.g., "ADRA2A has the smallest |meta_Z| of the ten (4.84)", line 92; the Panel A/B prioritisation) is unverifiable. It will not survive editorial/reviewer recomputation and is the single most damaging issue for acceptance.

【Specific fix】 Regenerate Table 3a directly from a single declared source file (the six-input `META_DRG_axis_stouffer.csv` is appropriate and is already cited) and re-paste every cell. If the table was intended to reflect the bulk-only (translatome-excluded) meta, state that explicitly and cite `META_bulkonly_meta.csv`, but then the `meta_Z`/`meta_FDR` must also come from that file — they currently match neither. Add a script (`scripts/...`) that emits Table 3a verbatim from the CSV so reviewers can reproduce it.

---

## FINDING 2 — MAJOR. Internal contradiction on the gene-set q-value (0.0022 vs 0.003)

【Problem】 The coordinated gene-set programme is reported with two different q-values that cannot both be correct, and the contradiction appears *within the same Results paragraph* as well as between Abstract and body.

【Evidence】 Abstract (line 18): "q = 0.003 each, an upper bound at the 2,000-permutation floor." Results (line 48, first sentence): "neuroinflammation … q = 0.0022, DAM-like … q = 0.0022 and complement … q = 0.0022." Same Results paragraph, later sentence (line 48): "The reported q = 0.003 for neuroinflammation, DAM-like and complement is the BH-adjusted value of this 1/2001 permutation floor and is therefore an upper bound." Fig. 1 legend (line 302) and Discussion (line 122) both use **0.0022**. So across the paper the value is reported as 0.0022 (Results/Fig/Discussion) and 0.003 (Abstract + a Results sentence) interchangeably.

【Why it matters】 A reader (and the meta-analytic reviewer) cannot tell which q is the operative one. If 0.003 is the BH-adjusted floor-derived upper bound, then the 0.0022 figures elsewhere are misreported; if 0.0022 is the operative value, the Abstract's "0.003" understates it. Either way the headline significance of the central biological claim (the neuroimmune/complement axis) is presented inconsistently, which undermines confidence in the statistical reporting.

【Specific fix】 Decide on one number and use it everywhere (Abstract, Results line 48, Fig. 1 legend, Discussion line 122). Explicitly state the relationship: e.g., "BH-adjusted q across the 18 multi-member sets = 0.0022; because this sits at the 2,000-permutation resolution floor (1/2001 ≈ 0.0005), we report it as an upper bound." Then remove the conflicting "0.003" sentence.

---

## FINDING 3 — MODERATE. CACNA2D1 platform-dependence is disclosed in count but its measurement-modality meaning is buried

【Problem】 CACNA2D1 (α2δ-1) is presented as the clearest single-gene validation of injury-induced α2δ-1 up-regulation, but the manuscript does not surface that the *only* discordant contrasts are the two GSE265957 **translatome** (ribosome-profiling) timepoints, i.e., the discordance is a transcript-vs-translatome modality split, not a biology split across independent studies.

【Evidence】 From `META_DRG_axis_stouffer.csv`, CACNA2D1: meta_Z 7.08797 (MS 7.09 ✓), meta_FDR 2.322e‑10 (MS 2.3e‑10 ✓), consistency 0.6667 = 4/6. Per-contrast log₂FC: GSE267799 +0.225, GSE212311 +1.156, GSE278227 +2.019, GSE241361 +1.871 (all UP), but **GSE265957 Xtail D4 −0.159 and D63 −0.0091 (both DOWN)**. So 4/6 up = the four bulk/mixed-bulk inputs up; both ribosome-profiling inputs down. Two further points: (a) consistency 0.667 is **below the 0.8 core gate, so CACNA2D1 is NOT a member of the 2,750-gene core** — the manuscript never states this explicitly; (b) the same modality split explains Finding 1: ADRA2A, MAPK14, ITPKC, SLC2A1 each have their single discordant contrast at GSE265957 Xtail D4 (down), and TNIK's "discordance" is Xtail D4 = exactly 0.000 (flat, not down). In other words, **every one of these targets is unanimously UP in all four bulk studies and only the translatome disagrees.**

【Why it matters】 This is actually a *supportive* observation for the authors' own "heterogeneity-sensitive / measurement-heterogeneity" thesis, but by misreporting these targets' consistency as 1.00 (Finding 1) and by not highlighting the bulk-up / translatome-down pattern, the manuscript (i) hides a real transcript–translatome decoupling that deserves discussion, and (ii) weakens its own honesty narrative. The "independently reproduces α2δ-1 up-regulation" claim (lines 86, 126, 302) is defensible *for the bulk mRNA signal* but should be qualified by the translatome disagreement rather than left as a clean reproduction.

【Specific fix】 Add a sentence in the CACNA2D1 paragraph (and a note in Table 3a once corrected): "All four bulk studies up-regulate CACNA2D1 (α2δ-1); the two discordant contrasts are the GSE265957 ribosome-profiling timepoints (down), so the injury-induced up-regulation is a bulk-transcript signal whose translational-level concordance is unconfirmed. CACNA2D1 (consistency 4/6 = 0.667) does not meet the 0.8 core-consistency gate and is therefore not in the 2,750-gene core." Extend this to ADRA2A/MAPK14/ITPKC/SLC2A1 (same pattern).

---

## FINDING 4 — MODERATE. "Dual-ML consensus" is overstated for a substantial subset of hubs

【Problem】 The manuscript frames the 35 hubs as convergence "across independent computational routes under leakage control" (Discussion line 124), but for ~10 hubs one of the three methods (LASSO) contributed essentially zero, so the "consensus" is effectively RF + SHAP only.

【Evidence】 From `P3_hub_genes.csv`, LASSO resampling frequency (`lasso_freq`) for several hubs that still carry the "2/3 methods" label: VASH2 0.00, ACVR1 0.00, NPY 0.00, RUBCN 0.00, TNS3 0.02, SERPINE1 0.02, MAPK14 0.01, WBP1L 0.00, CRISP3 0.02, REG3B 0.02, ITPKC 0.11, TNIK 0.11. The ≥2/3 rule admits a gene selected by RF and SHAP with LASSO frequency ≈0; for 12 of 35 hubs LASSO frequency is ≤0.11. The "convergence across independent routes" claim is therefore true for the 5 full-consensus hubs (SPRR1A, ATF3, TFE3, CDHR5, GALNS) and a handful of others, but not for the low-LASSO subset.

【Why it matters】 It affects how strongly the hub list can be sold. The bootstrap (200 resamples) is the right corrective and the manuscript does report it, but the *primary* "dual-ML consensus" descriptor overstates independence for a third of the list. Reviewers will read "dual-ML consensus under leakage control" as three independent routes agreeing; for many hubs it is two.

【Specific fix】 Reword the hub-construction description: "Hubs required agreement of ≥2 of 3 selectors; for 12/35 hubs LASSO contributed ≤0.11 selection frequency, so their consensus is effectively Random Forest + XGBoost rather than three independent routes. We therefore describe the set as a candidate convergence of RF and SHAP, with three-route agreement reserved for the 5 full-consensus genes." This preserves the honesty while removing the overstatement.

---

## FINDING 5 — MINOR. REG3B six-input FDR transcription mismatch

【Problem】 The REG3B six-input Stouffer FDR is reported as 7.1×10⁻¹⁴ but the source CSV lists 1.38×10⁻¹³.

【Evidence】 `META_DRG_axis_stouffer.csv` REG3B row: meta_FDR = 1.379×10⁻¹³ (manuscript line 84: "six-input Stouffer FDR 7.1×10⁻¹⁴"). This is a ~1.9× discrepancy, smaller than Finding 1 but still a transcribed-number error in a gene the manuscript discusses at length (and correctly flags as consistency-failing: 0.75, down in 1 of 4). The "nerve-injury-only FDR 2.1×10⁻²⁰" cannot be checked against the files provided (NI-only meta CSV not in the read set) and should be verified separately.

【Why it matters】 Low stakes individually, but it compounds the impression (with Findings 1–2) that transcribed numbers were not regenerated from the deposited tables. PLOS ONE will recompute.

【Specific fix】 Correct 7.1×10⁻¹⁴ → 1.38×10⁻¹³ (or regenerate from the CSV). Verify the NI-only 2.1×10⁻²⁰ against `_R4_nerveinjury_only_meta.csv` and cite that file explicitly.

---

## FINDING 6 — FRAMING. Asymmetric treatment of a significant vs a non-significant null

【Problem】 The manuscript frames a *significant* result (translation test, perm_p = 0.0002) as "non-informative," while framing a *non-significant* result (docking, p = 0.118) as an "honest null" — both are cautious, but the asymmetry in how significance is weighted is worth making explicit.

【Evidence】 Translation: background agreement 47.1% (6,772/14,390), strong stratum 43.3% (1,660/3,830), risk difference −3.7 pp, perm_p = 0.0002 (recomputed exactly from `_R4_nerveinjury_only_summary.json`: k=6772/n=14390→0.4706; k=1660/n=3830→0.4334; `strong_vs_background_pp` = −3.7). The manuscript calls this "non-informative rather than negative" (Abstract line 20; Conclusion line 140). Docking: ADRA2A full-library AUC 0.532, p = 0.118 NS, called "honest null" (heading line 88; but body line 114 calls it "inconclusive"). Note that *all four* NI strata in the JSON fall below the 47.1% background (44.4%, 43.3%, 45.8%, 41.9% under RE) — i.e., the nerve-injury direction is *consistently slightly opposed* to the incision direction, which is stronger than pure noise and is more than "non-informative."

【Why it matters】 Not a contradiction per se, but the reader could perceive selective caution: significance is discounted where it complicates the "no translation" story, and non-significance is elevated to a "null" where it supports the docking story. Both framings are defensible given the lesion-class difference and the MW-adjusted ADRA2A p=0.0005, but the asymmetry should be acknowledged head-on.

【Specific fix】 In the translation paragraph, state plainly: "The −3.7 pp deficit is statistically significant (perm_p = 0.0002) but small in magnitude and confounded by the incision/nerve-injury lesion-class difference, so we interpret it as evidence of directional non-transfer, not as a precise estimate of CPSP-specificity." This keeps the honest framing while conceding the significance rather than burying it. Similarly, resolve the "null" vs "inconclusive" wording for ADRA2A (use "inconclusive" throughout, since the MW-adjusted size-independent q = 0.0025 passes one filter).

---

## FINDING 7 — CITATIONS. Two high-value omissions in the DRG-injury / neuroinflammation space

【Problem】 The biological story rests on two literatures that are under-cited given how central they are to the claims.

【Evidence】
1. **DRG sensory-neuron single-cell classification underpinning the localisation claim.** The entire DRG neuron-subtype localisation (Fig. 3, "injured/regenerating neuron," markers GAL/GAP43/SOX11/VGF/MMP16/CDK5R1/SCG2/NCAM1) depends on an established DRG scRNA taxonomy, but no foundational DRG-classification reference is cited (e.g., the sensory-neuron subtype atlases that define the injured/regenerating state). The authors use GSE216039 but cite no primary DRG-scRNA methodology. Without it, the "20/25 hubs localise to the injured/regenerating neuron" claim floats.
2. **Pain-specific complement / microglial C1q-C3 synaptic-pruning literature.** The complement programme is a headline axis claim, yet the only pain-side complement citation is a single 2025 paper (Yousefpour). The spinal dorsal horn C1q/C3-dependent microglial synapse elimination after nerve injury has a substantial prior literature that would anchor the "complement" axis beyond the neurodegeneration-derived DAM provenance (Keren-Shaul 2017, already cited) and Tansley 2022.

【Why it matters】 These are not decorative; they are the evidentiary scaffolding for the two most novel biological claims (spatial localisation and the complement/DAM axis). Missing them makes the biological narrative look less grounded than it is and invites "why didn't you cite X" from a domain reviewer.

【Specific fix】 Add (a) a citation to the DRG sensory-neuron subclassification / injured-state scRNA literature used to define the annotated subtypes, and (b) 1–2 pain-specific complement/microglial-pruning references (spinal dorsal horn C1q/C3-dependent synapse elimination in neuropathic pain). The α2δ-1/CACNA2D1 translational claim is already anchored by Chen 2018 (ref 38), so no additional citation is required there.

---

## § Stands up (things I suspected but verified as correct)

1. **The non-circular translation numbers are exactly reproducible and honestly framed.** 6,772/14,390 = 47.1% background; 1,660/3,830 = 43.3% strong stratum; risk difference −3.7 pp; perm_p = 0.0002 — all match `_R4_nerveinjury_only_summary.json` exactly. The explicit disclosure that GSE278227 is a within-animal paired design (ipsilateral vs contralateral from the same 14 rats) and that the only genuinely cross-animal nerve-injury fold is GSE212311 (n=6) (lines 64, 158, 305) is appropriate and not over-claimed.
2. **CACNA2D1 headline numbers are correct.** meta_Z 7.088, meta_FDR 2.32e‑10, 4/6 up — match the CSV precisely (line 86). The manuscript does disclose "4 of 6" and does not claim it is in the core.
3. **The honest docking null is presented as a methodological boundary, not a false lead.** Reverse positive controls, MW correction, the breadth flip (0.618→0.532, p=0.118), and the explicit "no target is privileged or excluded" statement (lines 88–116, 126, 128) are appropriate for PLOS ONE's negative-findings policy. The Table 3b verdicts (all five ChEMBL targets FAIL the combined filters) are internally consistent.
4. **Heterogeneity is honestly reported.** Core shrinks 2,750→508 under random effects (508/2,750 = 18.5%, arithmetic correct); median I² 41.8% genome-wide and 79.1% among the 35 hubs (line 46) is stated plainly, and the bulk-only/collapse sensitivity suite is thorough.
5. **Annotation outliers are flagged, not concealed.** CDHR5, GALNS, FLNC, CRISP3, ANKRD1, MEGF11 are explicitly carried as watch-list/non-candidates (lines 62, 84), which is exactly the right behaviour for a hypothesis-generating computational study.
6. **The DAM-axis validation via TYROBP/TREM2/APOE** (Discussion line 122: TYROBP meta_FDR 8.8e‑9, TREM2 1.3e‑3, APOE 0.070) is a genuine, data-supported qualification of the "DAM-like" descriptor rather than a metaphor.

---

## § Questions for the authors

1. **Table 3a source.** Was Table 3a generated from the six-input `META_DRG_axis_stouffer.csv`, the bulk-only `META_bulkonly_meta.csv`, or an intermediate draft? The deposited six-input CSV gives ADRA2A meta_Z 4.45 / FDR 8.35e‑5 / consistency 0.8333, not the 4.84 / 1.5e‑5 / 1.00 in the text — please regenerate and reconcile.
2. **Transcript–translatome decoupling.** Given that ADRA2A, MAPK14, ITPKC, SLC2A1, CACNA2D1 are unanimously UP in all four bulk studies and only the GSE265957 ribosome-profiling timepoints disagree, do you intend to discuss this as a measurement-modality effect (and does it change how you present the "consistency" of these targets)?
3. **LPL.** The review brief lists LPL among the hub genes, but LPL is absent from `P3_hub_genes.csv` (the 35-hub list) and is not meta-significant (meta_Z −1.679, meta_FDR 0.174 in the stouffer CSV). Is LPL intended to appear anywhere as a hub, or is that a mislabel?
4. **NI-only FDR for REG3B.** The "nerve-injury-only FDR 2.1×10⁻²⁰" could not be verified against the provided files; please cite the exact source file and confirm.
5. **Gene-set q.** Which is the operative value, 0.0022 or 0.003, and can you provide the BH-across-18-sets computation that yields it?

---

## § What I actually checked

**Files read (full or in part):**
- `reports/MVP_PLOSONE_submission.md` (387 lines, full)
- `results/tables/META_DRG_axis_stouffer.csv` (16,553 lines — queried by gene)
- `results/tables/META_DRG_axis_CORE_signature.csv` (queried by gene)
- `results/tables/P3_hub_genes.csv` (full, 37 lines incl. header)
- `results/tables/_R4_nerveinjury_only_summary.json` (full)
- `results/tables/_R4_supplementary_summary.json` (not separately needed; translation JSON sufficed)
- `results/tables/_R4_translation_noncircular.json` (referenced; the non-circular statistics were taken from `_R4_nerveinjury_only_summary.json` as the manuscript directs)

**Values recomputed and compared to the manuscript:**
- Background translation rate: 6772/14390 = 0.4706 → MS 47.1% ✓
- Strong stratum: 1660/3830 = 0.4334 → MS 43.3% ✓
- Risk difference: 43.34 − 47.06 = −3.72 pp → MS −3.7 pp ✓; perm_p 0.0002 ✓
- CACNA2D1: meta_Z 7.08797 (MS 7.09 ✓), meta_FDR 2.322e‑10 (MS 2.3e‑10 ✓), consistency 0.6667=4/6 (MS "4/6" ✓); per-contrast lfc confirms 4 bulk UP, 2 Xtail DOWN.
- REG3B: meta_FDR 1.379e‑13 (MS 7.1e‑14 ✗, ~1.9× off).
- Ten target-table rows: 5 show consistency 1.00 in MS vs 0.8333 in CSV (ADRA2A, MAPK14, ITPKC, SLC2A1, TNIK); meta_Z off by 0.39–1.25 and meta_FDR by 5.6×–~1000× for the same five; AXL/ACVR1/SERPINE1 consistent.
- Per-contrast direction of the 5 consistency-discordant targets: the single discordant contrast is GSE265957 Xtail D4 (down) for ADRA2A, MAPK14, ITPKC, SLC2A1; TNIK's "discordance" is Xtail D4 = 0.000 (flat). ADRA2A's discordant contrast is Xtail D63 (−0.263).
- 2,750→508 RE core: 508/2750 = 0.1847 = 18.5% ✓ (arithmetic).

**Discrepancies stated:**
- Table 3a meta_Z/meta_FDR/consistency not reproducible from the cited source CSV (Finding 1) — the dominant issue.
- Gene-set q reported as both 0.0022 and 0.003 (Finding 2).
- REG3B six-input FDR 7.1e‑14 vs CSV 1.38e‑13 (Finding 5).
- CACNA2D1 consistency 0.667 < 0.8 → not in core, not stated (Finding 3).
- "Dual-ML consensus" overstated for ~12/35 hubs with LASSO freq ≤0.11 (Finding 4).

**Specifically NOT found problematic:** the non-circular translation framing and its disclosed paired-design limitation; the honest docking-null presentation; the heterogeneity reporting; the outlier flagging; the DAM hallmark validation.

---

*Overall verdict for the domain editor: the biological narrative is fundamentally sound and, where checked, more honest than most computational repurposing papers. However, Finding 1 (unreproducible Table 3a) is a blocking data-integrity defect that must be corrected before any further scientific assessment can be trusted, and Findings 2–3 should be fixed in the same revision. The manuscript should be returned for a major revision specifically to regenerate all transcribed numbers from the deposited CSVs/JSONs and to resolve the q-value and consistency contradictions.*
