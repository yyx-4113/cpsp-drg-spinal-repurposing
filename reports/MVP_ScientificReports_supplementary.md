# Supplementary Information

**Title.** Conserved nerve-injury-associated transcriptional response on the dorsal root ganglion–spinal axis: non-predictive incision translation and an honest repurposing null

**Author.** Yang Y

This Supplementary Information accompanies the *Scientific Reports* submission. It contains seven supplementary tables (S1–S7) that are **not** counted toward the 8 main display-item cap (5 figures + 3 tables). All tables are reproduced programmatically from the authoritative CSV/JSON outputs in `results/tables/` and are fully reproducible from the public GitHub repository at https://github.com/yyx-4113/cpsp-drg-spinal-repurposing (MIT LICENSE, CITATION.cff; the raw CSVs are the source of record). `NA` = not applicable / blank in source. Note: in GSE325938 Visium, 33/35 hubs were detectably expressed (CRISP3 and LNP1 were below the detection threshold); "35 hubs" refers to the full candidate set, of which 33 are spatially resolvable.

## Supplementary Table S1. Cross-dataset hub lineage consensus (P5)

Consensus across three single-cell/nucleus datasets: GSE216039 (mouse DRG neuron-enriched scRNA), GSE328175 (mouse lumbar spinal snRNA), GSE246288 (mouse spinal-cord Cd11b+ microglia scRNA). `n_methods` = number of ML routes (of 3) that flagged the gene as a hub; `n_datasets` = number of datasets in which the hub was localisable; `consensus_lineage` =  Neuronal / Immune / Glial / Mixed / NotLocalisable; `confident` = True only when localisation agreed across ≥2 datasets; `mean_enrich` = mean log2 enrichment of the hub in its assigned cell type vs others; `tiers` / `lineages` list per-dataset calls.

| Symbol | n_methods | n_datasets | Cell types | Consensus lineage | Confident | Mean enrich | Tiers | Lineages |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| ATF3 | 3 |  |  | NotLocalisable | 0 |  |  |  |
| CDHR5 | 3 |  |  | NotLocalisable | 0 |  |  |  |
| GALNS | 3 | 1 | Neuron | Neuronal | 0 | 1.570 | restricted | Neuronal |
| SPRR1A | 3 | 1 | Neuron | Neuronal | 0 | 2.460 | restricted | Neuronal |
| TFE3 | 3 | 2 | Immune|Microglia | Immune | 1 | 1.795 | enriched|restricted | Immune |
| ACVR1 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| AGRN | 2 |  |  | NotLocalisable | 0 |  |  |  |
| ANKRD1 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| ANKRD13B | 2 | 2 | Neuron | Neuronal | 1 | 1.850 | restricted | Neuronal |
| AXL | 2 | 1 | Immune | Immune | 0 | 2.330 | restricted | Immune |
| CCDC160 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| CHL1 | 2 | 2 | Astrocyte|SatelliteGlia | Glial | 1 | 1.910 | enriched|restricted | Glial |
| CRISP3 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| CTTN | 2 | 2 | Neuron | Neuronal | 1 | 0.840 | enriched | Neuronal |
| ECEL1 | 2 | 1 | Neuron | Neuronal | 0 | 2.950 | restricted | Neuronal |
| FLNC | 2 |  |  | NotLocalisable | 0 |  |  |  |
| FLRT3 | 2 | 2 | Neuron|OPC | Mixed | 0 | 1.465 | restricted | Glial|Neuronal |
| ITPKC | 2 |  |  | NotLocalisable | 0 |  |  |  |
| LNP1 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| MAPK14 | 2 | 2 | Microglia|Schwann | Mixed | 0 | 1.035 | enriched|restricted | Glial|Immune |
| MEGF11 | 2 | 1 | OPC | Glial | 0 | 4.670 | restricted | Glial |
| NPY | 2 |  |  | NotLocalisable | 0 |  |  |  |
| PTPN23 | 2 | 2 | Neuron | Neuronal | 1 | 0.885 | enriched | Neuronal |
| REG3B | 2 |  |  | NotLocalisable | 0 |  |  |  |
| RNF19B | 2 | 2 | Microglia|Neuron | Mixed | 0 | 1.495 | restricted | Immune|Neuronal |
| RUBCN | 2 | 2 | Neuron|OPC | Mixed | 0 | 0.755 | enriched | Glial|Neuronal |
| SERPINE1 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| SLC2A1 | 2 |  |  | NotLocalisable | 0 |  |  |  |
| SRRM4 | 2 | 2 | Neuron | Neuronal | 1 | 2.625 | restricted | Neuronal |
| TNIK | 2 | 2 | Astrocyte|Neuron | Mixed | 0 | 1.330 | restricted | Glial|Neuronal |
| TNS3 | 2 | 1 | SatelliteGlia | Glial | 0 | 2.080 | restricted | Glial |
| VASH2 | 2 | 2 | Neuron | Neuronal | 1 | 2.245 | restricted | Neuronal |
| VIP | 2 |  |  | NotLocalisable | 0 |  |  |  |
| WBP1L | 2 | 1 | Microglia | Immune | 0 | 0.930 | enriched | Immune |
| WDR81 | 2 | 1 | Microglia | Immune | 0 | 2.020 | restricted | Immune |

## Supplementary Table S2. Visium GSE325938 spatial regionalisation of the 35 hubs (P5)

Spatial regionalisation of the 35 hubs across seven spinal-cord regions in Visium GSE325938 (mouse spinal cord, Sham/baseline tissue). 33/35 hubs were detectably expressed (CRISP3 and LNP1 were below the detection threshold, tier "broad/low", all log2 = 0). `top_region` = region of maximal mean log2 expression; `top_label_log2` = that region's label log2 value; `top_detection` = detection fraction in the top region; `tier` = restricted / enriched / broad-low; `snRNA_lineage` = lineage assigned by snRNA (blank = not localisable); `crossmodal` = consistent / divergent / n/a between Visium top region and snRNA lineage. **Detection floor (below-floor flag, marked \*):** hubs whose `top_detection` < 5% in their top region — CDHR5, SERPINE1, CRISP3, LNP1, VIP, REG3B and ANKRD1 — are flagged below-floor; their regional specificity ratios are driven by near-zero detection fractions and are therefore excluded from biological interpretation (see Methods). All 17 dorsal-horn assignments passed the 5% floor. The full per-region breakdown (`log2_all_regions`) is retained in `results/tables/P5_GSE325938_hub_regionalization.csv`.

| Symbol | Present | Top region | Top log2 | Top detect | Global mean | Global detect | Tier | snRNA lineage | Crossmodal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SPRR1A | 1 | VentralHorn | 2.540 | 0.098 | 0.089 | 0.018 | restricted | Neuronal | divergent |
| ATF3 | 1 | MeningealFibro | 2.243 | 0.077 | 0.067 | 0.015 | restricted |  |  |
| TFE3 | 1 | DorsalHorn | 0.864 | 0.302 | 0.675 | 0.151 | enriched | Immune | divergent |
| CDHR5\* | 1 | WhiteMatter | 3.109 | 0.006 | 0.004 | 0.001 | restricted |  |  |
| GALNS | 1 | DorsalHorn | 1.374 | 0.105 | 0.163 | 0.038 | restricted | Neuronal | consistent |
| CHL1 | 1 | DorsalHorn | 1.619 | 0.804 | 1.229 | 0.263 | restricted | Glial | divergent |
| FLNC | 1 | MeningealFibro | 2.327 | 0.250 | 0.236 | 0.047 | restricted |  |  |
| RNF19B | 1 | DorsalHorn | 1.022 | 0.435 | 0.886 | 0.197 | restricted | Immune|Neuronal |  |
| SRRM4 | 1 | DorsalHorn | 1.856 | 0.182 | 0.199 | 0.048 | restricted | Neuronal | consistent |
| ECEL1 | 1 | VentralHorn | 1.559 | 0.422 | 0.681 | 0.147 | restricted | Neuronal | divergent |
| FLRT3 | 1 | DorsalHorn | 2.018 | 0.277 | 0.280 | 0.066 | restricted | Glial|Neuronal |  |
| PTPN23 | 1 | DorsalHorn | 1.209 | 0.495 | 0.904 | 0.199 | restricted | Neuronal | consistent |
| MAPK14 | 1 | DorsalHorn | 1.254 | 0.667 | 1.239 | 0.268 | restricted | Glial|Immune |  |
| VASH2 | 1 | DorsalHorn | 1.875 | 0.189 | 0.209 | 0.050 | restricted | Neuronal | consistent |
| TNIK | 1 | DorsalHorn | 1.231 | 0.572 | 1.085 | 0.237 | restricted | Glial|Neuronal |  |
| WDR81 | 1 | VentralHorn | 0.952 | 0.236 | 0.502 | 0.112 | enriched | Immune | divergent |
| CCDC160 | 1 | Ependymal | 1.063 | 0.075 | 0.145 | 0.034 | restricted |  |  |
| SLC2A1 | 1 | MeningealFibro | 0.861 | 0.856 | 2.761 | 0.526 | enriched |  |  |
| ANKRD13B | 1 | DorsalHorn | 1.164 | 0.435 | 0.836 | 0.182 | restricted | Neuronal | consistent |
| NPY | 1 | DorsalHorn | 2.591 | 0.775 | 0.637 | 0.132 | restricted |  |  |
| AXL | 1 | MeningealFibro | 1.078 | 0.587 | 1.331 | 0.283 | restricted | Immune | divergent |
| SERPINE1\* | 1 | MeningealFibro | 3.827 | 0.038 | 0.015 | 0.003 | restricted |  |  |
| CRISP3\* | 1 | MeningealFibro | 0 | 0 | 0 | 0 | broad/low |  |  |
| WBP1L | 1 | MeningealFibro | 1.039 | 0.385 | 0.881 | 0.189 | restricted | Immune | divergent |
| ITPKC | 1 | DorsalHorn | 1.523 | 0.123 | 0.171 | 0.039 | restricted |  |  |
| ACVR1 | 1 | DorsalHorn | 1.067 | 0.270 | 0.517 | 0.118 | restricted |  |  |
| LNP1\* | 1 | MeningealFibro | 0 | 0 | 0 | 0 | broad/low |  |  |
| AGRN | 1 | DorsalHorn | 1.017 | 0.691 | 1.539 | 0.324 | restricted |  |  |
| VIP\* | 1 | Ependymal | 1.332 | 0.036 | 0.059 | 0.014 | restricted |  |  |
| REG3B\* | 1 | MeningealFibro | 2.468 | 0.010 | 0.007 | 0.002 | restricted |  |  |
| TNS3 | 1 | MeningealFibro | 0.778 | 0.596 | 1.671 | 0.341 | enriched | Glial | divergent |
| ANKRD1\* | 1 | MeningealFibro | 2.578 | 0.010 | 0.006 | 0.001 | restricted |  |  |
| CTTN | 1 | DorsalHorn | 0.756 | 0.621 | 1.638 | 0.345 | enriched | Neuronal | consistent |
| RUBCN | 1 | DorsalHorn | 0.753 | 0.484 | 1.213 | 0.259 | enriched | Glial|Neuronal |  |
| MEGF11 | 1 | VentralHorn | 0.917 | 0.172 | 0.377 | 0.085 | enriched | Glial | divergent |

\* Below detection floor: `top_detection` < 5% in the hub's top region (CRISP3 and LNP1 are all-zero). Regional specificity ratios computed on such near-zero detection fractions are noise-driven (e.g., ratios exceeding 10³) and are not biologically interpreted.

## Supplementary Table S3. Reverse positive-control docking AUCs (P6)

Reverse positive controls for the structure-based repurposing screen. `n_known_pairs` = number of ChEMBL binding-type pairs (pChEMBL ≥ 6) for the target; `n_ligands` = number of docked FDA drugs scored; `known_median_aff` / `all_median_aff` = median Vina affinity (kcal/mol, more negative = tighter) of known binders vs the full library; `known_median_pct` = percentile of known-binder median affinity within the library; `auc_known_vs_rest` = ROC-AUC separating known binders from the rest; `control_evaluable` = True when ≥3 ChEMBL known pairs exist, i.e. the control can be computed at all; `control_passed` = True only when the resulting AUC separates known binders and is reported as method validation. These are **different questions**, and conflating them previously produced a coding error: ADRA2A (115 known pairs) was flagged `reliable = 0` although it comfortably exceeds the ≥3 threshold. ADRA2A is therefore **control-evaluable but did not pass** — its chance-level AUC (0.532, p = 0.118) is the real result, and no target should be credited with method validation on the basis of pair count alone. Targets with 0 known pairs (GALNS, ITPKC, SERPINE1, VASH2) are neither evaluable nor interpretable and are shown for completeness. `known_drugs` lists the ChEMBL binding-type compounds used as positive controls. Because a valid positive control requires ≥3 known pairs, SLC2A1 (n_known = 1, AUC 0.914) is *not* a method-validation control and is excluded from any claim that the screen can separate known binders.

| Target | n_known | n_ligands | Known med aff | All med aff | Known pct | AUC | Control evaluable (≥3 pairs) | Control passed | Known drugs (ChEMBL) |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| AXL | 13 | 3071 | -8.021 | -6.511 | 88.261 | 0.880 | 1 | 1 | AXITINIB;BOSUTINIB;CABOZANTINIB;CRIZOTINIB;ENTRECTINIB;FEDRATINIB;GILTERITINIB;MIDOSTAURIN |
| TNIK | 10 | 3063 | -8.700 | -6.688 | 91.691 | 0.824 | 1 | 1 | AXITINIB;BOSUTINIB;LENVATINIB;NERATINIB;NINTEDANIB;PACRITINIB;PAZOPANIB;PONATINIB |
| ACVR1 | 9 | 3075 | -8.951 | -7.706 | 83.203 | 0.797 | 1 | 1 | CRIZOTINIB;DASATINIB;FEDRATINIB;GILTERITINIB;LORLATINIB;MOMELOTINIB;NINTEDANIB;PACRITINIB |
| MAPK14 | 16 | 3068 | -7.758 | -6.597 | 83.686 | 0.779 | 1 | 1 | BITHIONOL;CELECOXIB;DASATINIB;DASATINIB ANHYDROUS;ETORICOXIB;GEFITINIB;HEXACHLOROPHENE;LENVATINIB |
| SLC2A1 | 1 | 3066 | -10.240 | -8.005 | 91.422 | 0.914 | 0 | 0 | EMETINE |
| ADRA2A | 115 | 3070 | -7.719 | -7.500 | 55.065 | 0.532 | 1 | 0 | AMIODARONE;AMITRIPTYLINE;AMLODIPINE;AMOXAPINE;APRACLONIDINE;ARIPIPRAZOLE;ASENAPINE;AZELASTINE |
| GALNS | 0 | 3064 |  | -6.496 |  |  | 0 | 0 |  |
| ITPKC | 0 | 3065 |  | -5.060 |  |  | 0 | 0 |  |
| SERPINE1 | 0 | 3075 |  | -5.820 |  |  | 0 | 0 |  |
| VASH2 | 0 | 3070 |  | -6.631 |  |  | 0 | 0 |  |

## Supplementary Table S4. Multivariate physicochemical control and Benjamini–Hochberg correction (P6)

Two post-hoc controls added in response to review (T2-11 and T2-14). Panel A: for each ChEMBL-annotated target, a logistic regression of known-binder status on six physicochemical descriptors (MW, logP, TPSA, HBD, HBA, rotB) plus docking affinity was fit; `AUC_phys` = physicochemical-only model, `AUC_dock` = docking-affinity-only model, `AUC_combined` = both; `LR_dock_residual_p` = likelihood-ratio test for whether docking affinity adds discrimination beyond chemotype. Panel B: Benjamini–Hochberg (BH) correction across the five targets of (i) the raw full-library enrichment p (`p_mannwhitney`) and (ii) the size-independent p (`deltaAUC_vs_size_only_p_le0`). Source: `results/tables/P6_multivariate_physchem_control.csv`, `P6_BH_correction.csv`.

**Panel A — multivariate physicochemical control.**

| Target | n | n known binders | AUC_phys | AUC_dock | AUC_combined | LR docking-residual p |
| --- | --- | --- | --- | --- | --- | --- |
| ACVR1 | 3075 | 9 | 0.8983 | 0.7970 | 0.9308 | 9.6e-4 |
| ADRA2A | 3070 | 115 | 0.7910 | 0.5325 | 0.7967 | 0.027 |
| AXL | 3071 | 13 | 0.8953 | 0.8798 | 0.9267 | 2.6e-5 |
| MAPK14 | 3068 | 16 | 0.8971 | 0.7785 | 0.9135 | 0.066 |
| TNIK | 3063 | 10 | 0.8516 | 0.8242 | 0.8978 | 7.3e-5 |

*Panel A is a post-hoc physicochemical control; its likelihood-ratio tests are reported descriptively and are explicitly not counted among the corrected inferential tests (see manuscript Methods, multiple-testing registry).*

**Panel B — Benjamini–Hochberg correction across five targets.**

| Target | AUC_dock | raw p | BH q (raw) | size-independent p | BH q (size-independent) |
| --- | --- | --- | --- | --- | --- |
| ACVR1 | 0.797 | 1.03e-3 | 1.29e-3 | 0.584 | 0.584 |
| ADRA2A | 0.532 | 0.118 | 0.118 | 0.0005 | 0.0025 |
| AXL | 0.880 | 1.11e-6 | 5.55e-6 | 0.141 | 0.352 |
| MAPK14 | 0.779 | 5.94e-5 | 1.48e-4 | 0.579 | 0.584 |
| TNIK | 0.824 | 1.96e-4 | 3.27e-4 | 0.444 | 0.584 |

*Reading:* After BH, 4/5 raw enrichment p-values remain significant (AXL, MAPK14, TNIK, ACVR1) but only ADRA2A's weak size-independent p survives BH (q = 0.0025), and ADRA2A's overall full-library enrichment is non-significant (AUC 0.532, p = 0.118). No target clears both filters we applied—the raw/full-library MW-corrected enrichment p and the size-independent (MW-adjusted) p—so the honest-null conclusion is unchanged. The multivariate control (Panel A) shows the three strongest positive controls (AXL, TNIK, ACVR1) retain docking signal beyond chemotype, partially validating the docking protocol rather than discrediting it; ADRA2A remains weak/non-informative.

## Supplementary Table S5. A priori gene-set members and provenance (P3)

Nineteen a priori gene sets were defined before analysis and tested on the six-input Stouffer meta_Z vector (2,000-permutation calibration; resolution floor 1/2001 ≈ 0.0005). `n_members` = genes in the set definition; `n_present` = members present in the meta_Z vector; `mean_Z` / `perm_p` are from `results/tables/P3_geneset_stats.csv`. Sigma-1 is a single-gene marker (SIGMAR1) and is reported as such, not as a set-level test. The DAM_microglia set follows Keren-Shaul et al. (Cell 169:1276–1290.e17, 2017).

| Gene set | n_members | n_present | mean_Z | perm_p | Provenance / definition |
| --- | --- | --- | --- | --- | --- |
| Neuroinflammation | 19 | 19 | 4.94 | 0.0005 | Cytokines/TLR/NF-κB axis (IL1B, IL6, TNF, CCL2, CXCL1, IL10, TLR2, TLR4, MYD88, NFKB1, NFKB2, STAT3, SOCS3), myeloid markers (CD68, AIF1/IBA1), astrocyte GFAP, injury markers (ATF3, JUN, FOS) — general neuroimmune activation inventory |
| DAM_microglia | 16 | 16 | 3.88 | 0.0005 | Disease-associated microglia signature (Keren-Shaul et al., Cell 2017): TREM2/APOE/TYROBP axis, lysosomal (CTSD, LPL, CST7), phagocytic (MERTK, ITGAX, AXL), complement (C1QA/B/C), SPP1, GPNMB, CD68, CSF1R |
| Complement | 22 | 18 | 3.44 | 0.0005 | Classical/alternative/terminal complement cascade + regulators: C1QA/B/C, C2, C3, C4A/B, CFB, CFH, CFI, SERPING1, CR1/2, C5, C5AR1, C6, C7, C8A, C9, CD46, CD55, CD59 |
| Mitochondria_OXPHOS | 20 | 19 | −2.37 | 0.004 | Electron-transport-chain complexes I–V (NDUF*, SDH*, UQCR*, COX*, ATP5*) — energy-metabolism suppression |
| Neuropeptides_pain | 19 | 18 | 2.19 | 0.010 | Pain-related neuropeptides/receptors: NPY, GAL, VGF, ADCYAP1, CALCA/B, TAC1/TACR1, SST, CCK/CCKBR, GRP, NMB, NPB/NPW, PROK2, NTS/NTSR1/2 |
| Synaptic | 20 | 20 | −1.41 | 0.112 | Pre/postsynaptic and excitatory/inhibitory synaptic proteins (SYN1, SNAP25, GRIA1–4, GRIN1/2A/B, GABRA1, GABRB2, DLG4, SHANK1–3, NLGN1, SLC17A6/7, GAD1/2) |
| Nav_SCN | 14 | 14 | −1.37 | 0.180 | Voltage-gated sodium channels (nociceptor Nav1.7/1.8/1.9 = SCN9A/10A/11A; SCN8A; plus SCN1–7, SCN1B–4B) — canonical pain ion channels |
| P2RX_P2RY | 12 | 12 | 0.85 | 0.440 | Purinergic receptors (P2RX1–7, P2RY1/2/12/13/14); microglial P2X4 implicated in neuropathic pain (Tsuda et al., Nat Med 2003) — self-negative in this meta |
| MAPK_kinase | 15 | 15 | 0.77 | 0.465 | MAPK/ERK/p38/JNK cascade + MAP2K + MAP3K + DUSP phosphatases |
| Sigma1 | 1 | 1 | 2.06 | 0.466 | Single member SIGMAR1 — reported as a single-gene marker, not a set-level test |
| Opioid_GPCR | 8 | 8 | −0.85 | 0.500 | Opioid receptors (OPRM1, OPRD1, OPRK1, OPRL1) + opioid peptide system (POMC, PENK, PDYN, PNOC) |
| ASIC | 8 | 4 | −0.97 | 0.517 | Acid-sensing ion channels (ASIC1–4, ACCN1–4) |
| Myelin_OL | 14 | 13 | 0.70 | 0.524 | Oligodendrocyte/myelin markers (MBP, PLP1, MAG, MOG, CNP, MOBP, CLDN11, OPALIN, MAL, SOX10, OLIG1/2, MYRF, CNTN2) |
| K2P_KCNK | 15 | 14 | 0.66 | 0.544 | Two-pore-domain potassium channels (KCNK1–18) |
| Autophagy_mitophagy | 11 | 11 | 0.60 | 0.606 | Autophagy/mitophagy machinery (MAP1LC3B, ATG5/7, BECN1, BNIP3, PINK1, PRKN, SQSTM1, OPTN, TFEB, GABARAP) |
| CPSP_literature | 24 | 24 | 0.52 | 0.613 | Genes curated from the CPSP/neuropathic-pain literature as a positive-control set (SCN9A/10A/11A, CACNA2D1–3, GCH1, OPRM1, COMT, DRD2, TRPV1, P2RX7, IL6, TNF, BDNF, NGF, NTRK1, KCNS1, HCN2, GRIN2B, CACNG2, ATP1A3, KCNQ2/3) |
| Kv_KCNQ_KCNH | 13 | 13 | 0.33 | 0.754 | Voltage-gated / KCNQ / KCNH potassium channels (KCNQ1–5, KCNH1–8) |
| CACNA | 18 | 18 | 0.24 | 0.828 | Voltage-gated calcium channels (CACNA1A/B/C/D/E/F/G/H/I/S, CACNB1–4, CACNA2D1–4) |
| TRP_channels | 12 | 12 | −0.17 | 0.888 | Transient receptor potential channels (TRPV1–4, TRPA1, TRPM2/3/8, TRPC1/3/5/6) — canonical nociceptor/thermosensor families |

## Supplementary Table S5b. Set-level Benjamini–Hochberg correction across gene sets (P3)

The 19 a priori gene sets were previously reported with permutation p-values but **without** correction across sets, which left the three floor-pinned sets (permutation p at the 1/2001 resolution floor) tied and ordered only by Stouffer Z. Benjamini–Hochberg correction is applied here across the **18 multi-member sets**; Sigma-1 is a single-gene marker (SIGMAR1), is reported as such, and is excluded from set-level inference and ordering. Columns are given for the fixed-effect meta_Z vector (primary) and for the random-effects meta_Z vector (sensitivity). Source: `results/tables/_R4_geneset_setlevel_bh.csv`.

| Gene set | n_present | perm p (FE) | **BH q (FE)** | perm p (RE) | **BH q (RE)** | Survives set-level BH |
| --- | --- | --- | --- | --- | --- | --- |
| Neuroinflammation | 19 | 0.0004998 | **0.002999** | 0.0004998 | 0.002999 | yes |
| Complement | 18 | 0.0004998 | **0.002999** | 0.0004998 | 0.002999 | yes |
| DAM_microglia | 16 | 0.0004998 | **0.002999** | 0.0004998 | 0.002999 | yes |
| Mitochondria_OXPHOS | 19 | 0.004498 | **0.02024** | 0.06897 | 0.3103 | fixed-effect only |
| Neuropeptides_pain | 18 | 0.01299 | **0.04678** | 0.4898 | 0.7948 | fixed-effect only |
| Synaptic | 20 | 0.1059 | **0.3178** | 0.6182 | 0.7948 | no |
| Nav_SCN | 14 | 0.1724 | **0.4433** | 0.2354 | 0.5047 | no |
| P2RX_P2RY | 12 | 0.4383 | **0.7736** | 0.2524 | 0.5047 | no |
| MAPK_kinase | 15 | 0.4458 | **0.7736** | 0.1064 | 0.3193 | no |
| Opioid_GPCR | 8 | 0.4893 | **0.7736** | 0.5522 | 0.7948 | no |
| ASIC | 4 | 0.5262 | **0.7736** | 0.901 | 0.9541 | no |
| K2P_KCNK | 14 | 0.5517 | **0.7736** | 0.09445 | 0.3193 | no |
| Autophagy_mitophagy | 11 | 0.5877 | **0.7736** | 0.6172 | 0.7948 | no |
| CPSP_literature | 24 | 0.6357 | **0.7736** | 0.6912 | 0.8294 | no |
| Myelin_OL | 14 | 0.6447 | **0.7736** | 0.1284 | 0.3303 | no |
| Kv_KCNQ_KCNH | 13 | 0.7671 | **0.8488** | 0.5697 | 0.7948 | no |
| CACNA | 18 | 0.8016 | **0.8488** | 0.8751 | 0.9541 | no |
| TRP_channels | 12 | 0.8881 | **0.8881** | 0.961 | 0.961 | no |
| Sigma1 | 1 | — | **—** | — | — | no |
| Sigma1 | 1 | — | **—** | — | — | no |

*Reading.* Under the fixed-effect meta-vector, neuroinflammation, complement, DAM microglia (q = 0.003 each) and mitochondrial OXPHOS (q = 0.0202) survive set-level BH; neuropeptides are borderline (q = 0.0468). Under the random-effects meta-vector the three upregulated programmes survive unchanged (q = 0.003) but **OXPHOS does not (q = 0.31)**, so energy-metabolism suppression is reported as a fixed-effect finding that is not robust to between-contrast heterogeneity. No ion-channel family survives under either model.


## Supplementary Table S6. Random-effects sensitivity, heterogeneity, and the non-circular translation test

**Panel A — heterogeneity and core stability.** The primary meta-analysis is a fixed-effect (inverse-variance / Stouffer) combination. Panel A reports a DerSimonian–Laird random-effects alternative computed on the same per-contrast Z-values, with τ² and I² per gene. Source: `results/tables/_R4_random_effects_meta.csv`, `_R4_supplementary_summary.json`.

| Quantity | Fixed effect | Random effects |
| --- | --- | --- |
| Genes tested | 16,552 | 16,552 |
| Core (FDR < 0.05 and consistency ≥ 0.8) | **4,055** | **1,008** (24.9% of the fixed-effect core) |
| Median τ² | — (assumed 0) | 0.232 |
| Median I² | — (assumed 0) | 38.8% |
| Genes with I² > 50% | — | 41.9% |
| Genes with τ² > 0 | — | 68.1% |
| 35 hubs retaining FDR < 0.05 | 35/35 | 18/35 |

*Reading.* Between-contrast heterogeneity is moderate overall (median I² = 38.8%) and high among the hubs (median I² = 72.8%), and the core is heterogeneity-sensitive: only 24.9% of the fixed-effect core persists under random effects. The fixed-effect core is reported as the primary result with the random-effects core as its sensitivity bound.

**Panel B — nerve-injury-to-incision translation, circular versus non-circular.** The originally reported concordance figures were produced by a circular design: both the meta_Z and the pooled consistency filter (≥0.8 across all six contrasts) **include the incision contrast**, so a gene could enter the core partly because it already agreed with the incision direction. Panel B reports (i) those circular figures for reference only, (ii) the same test with consistency restricted to the five nerve-injury contrasts, and (iii) the fully non-circular test in which the signature is built on the five nerve-injury contrasts only and the incision contrast is used once, as a held-out test. Wilson 95% confidence intervals and a 5,000-draw label-permutation null against the measured background are given in place of a binomial test against 50%, which is not the correct reference for a contrast with a global directional skew. Sources: `results/tables/_R4_translation_concordance_effectsize.csv`, `_R4_translation_noncircular.csv`, `_R4_nerveinjury_only_meta.csv`.

| Stratum | k / n | Agreement | Wilson 95% CI | Permutation p vs background | Circular? |
| --- | --- | --- | --- | --- | --- |
| Circular: all measured genes (6-contrast meta_Z) | 7,751/14,390 | 53.9% | 53.0–54.7% | — | yes |
| Circular: core (pooled consistency ≥ 0.8) | 2,473/3,556 | 69.5% | 68.0–71.0% | 0.0002 | yes |
| Semi-corrected: meta FDR < 0.05 and nerve-injury consistency ≥ 0.8 | 2,318/4,306 | 53.8% | 52.3–55.3% | 0.79 | partial (FDR still 6-contrast) |
| **Non-circular background (all measured)** | 6,779/14,390 | **47.1%** | 46.3–47.9% | 1.00 | no |
| **Non-circular test: NI FDR < 0.05 and NI consistency ≥ 0.8** | 2,266/4,899 | **46.2%** | 44.9–47.6% | 0.14 | no |
| Non-circular comparator: NI FDR < 0.05 and NI consistency < 0.8 | 978/2,185 | 44.8% | 42.7–46.9% | 0.0148 | no |

*Reading.* The apparent core "translation" of 69.5% collapses to 53.8% once consistency is restricted to nerve-injury contrasts and to **46.2%** under the fully non-circular test, versus a **47.1%** background — a risk difference of **-0.9 pp** (permutation p = 0.14). Knowing that a gene is strongly and consistently regulated by nerve injury therefore carries essentially no information about its direction in the incision model. A nerve-injury-only core (incision excluded) comprised 5,412 genes under fixed effects and 3,099 under random effects.

**Panel C — consistency split for the reported 4,055-gene core.** `nerve_injury_consistency` is computed across the five nerve-injury contrasts only; `incision_agreement` is the indicator that the incision log₂FC has the same sign as the meta Z. Source: `results/tables/_R4_random_effects_meta.csv`.

| Quantity | Value |
| --- | --- |
| Core genes with an incision measurement | 3,556 |
| ... incision-concordant | 2,473 (69.5%) |
| ... incision-**discordant** (core-consistent yet incision-opposed) | 1,083 (30.5%) |
| Core genes with nerve-injury consistency ≥ 0.8 | 3,889/4,055 (95.9%) |
| Core genes both NI-consistent ≥ 0.8 **and** incision-concordant | 2,308 |
| Mean nerve-injury consistency in the core | 0.938 (pooled consistency 0.903) |

**Panel D — the ten docking targets under fixed versus random effects.** Source: `results/tables/_R4_targets_fixed_vs_random.csv`.

| Target | Z (FE) | FDR (FE) | Z (RE) | FDR (RE) | I² (%) | τ² | Retains RE significance |
| --- | --- | --- | --- | --- | --- | --- | --- |
| TNIK | 8.00 | 4.3e-13 | 3.34 | 0.0212 | 68.9 | 0.86 | yes |
| SLC2A1 | 6.83 | 6.3e-10 | 6.83 | 7.02e-08 | 0.0 | 0.00 | yes |
| ACVR1 | 6.95 | 3.2e-10 | 2.15 | 0.188 | 82.0 | 1.77 | no |
| SERPINE1 | 6.92 | 3.7e-10 | 2.87 | 0.0596 | 72.8 | 1.04 | no |
| MAPK14 | 6.09 | 3.9e-08 | 2.43 | 0.126 | 75.1 | 1.17 | no |
| AXL | 6.14 | 2.9e-08 | 2.79 | 0.0677 | 66.8 | 0.78 | no |
| VASH2 | 6.00 | 6.4e-08 | 2.15 | 0.186 | 74.9 | 1.16 | no |
| GALNS | 5.79 | 1.8e-07 | 3.27 | 0.0251 | 45.8 | 0.33 | yes |
| ITPKC | 7.18 | 8.1e-11 | 1.77 | 0.296 | 84.4 | 2.10 | no |
| ADRA2A | 4.84 | 1.5e-05 | 3.08 | 0.0386 | 44.3 | 0.31 | yes |

*Reading.* Only 4 of the 10 targets retain FDR < 0.05 under random effects (SLC2A1, TNIK, ADRA2A, GALNS), so target ranking is model-dependent and no target is either privileged or excluded by the meta-analysis on this basis.


## Supplementary Table S7. Bootstrap stability of the docking target set (P3/P6)

The published bootstrap (`P3_hub_bootstrap.csv`) reported per-gene hub-recovery frequency only and could not answer whether the **docking target set** is reproducible. This table re-runs the identical three-method bootstrap (B = 200, SEED = 42; LASSO λ.min, Random-Forest MDGini top-80, XGBoost |SHAP| top-80; hub = ≥2/3 methods) and additionally records the full recovered hub set on every resample. Source: `results/tables/_R4_targetset_bootstrap.csv`, `_R4_targetset_bootstrap.json`.

**Panel A — set-level reproducibility.**

| Quantity | Dock-eligible hubs (17) | Actually docked hubs (9) |
| --- | --- | --- |
| Members present in the ML feature pool | 17/17 | 9/9 |
| Mean number recovered per resample | 0.79 | 0.35 |
| Median (min–max) | 1 (0–4) | 0 (0–3) |
| P(≥1 recovered) | 0.57 | 0.32 |
| P(≥3 recovered) | 0.04 | 0.005 |
| P(≥5 recovered) | 0.0 | 0.0 |
| P(all recovered) | 0.0 | 0.0 |

Resampled hub sets had a median size of 6 genes (IQR 5–8) and a median Jaccard overlap of **0.026** (IQR 0.024–0.051) with the published 35-gene set.

**Panel B — per-gene recovery frequency within the dock-eligible set.**

| Symbol | Set | Recovery frequency |
| --- | --- | --- |
| CDHR5 | dock-eligible (17) | 0.155 |
| GALNS | dock-eligible (17) | 0.100 |
| TFE3 | dock-eligible (17) | 0.070 |
| PTPN23 | dock-eligible (17) | 0.065 |
| ITPKC | dock-eligible (17) | 0.050 |
| NPY | dock-eligible (17) | 0.050 |
| SLC2A1 | dock-eligible (17) | 0.050 |
| AXL | dock-eligible (17) | 0.045 |
| FLRT3 | dock-eligible (17) | 0.040 |
| VASH2 | dock-eligible (17) | 0.035 |
| MAPK14 | dock-eligible (17) | 0.030 |
| FLNC | dock-eligible (17) | 0.025 |
| RUBCN | dock-eligible (17) | 0.020 |
| TNIK | dock-eligible (17) | 0.020 |
| SERPINE1 | dock-eligible (17) | 0.015 |
| CTTN | dock-eligible (17) | 0.010 |
| ACVR1 | dock-eligible (17) | 0.005 |
| GALNS | docked (9) | 0.100 |
| ITPKC | docked (9) | 0.050 |
| SLC2A1 | docked (9) | 0.050 |
| AXL | docked (9) | 0.045 |
| VASH2 | docked (9) | 0.035 |
| MAPK14 | docked (9) | 0.030 |
| TNIK | docked (9) | 0.020 |
| SERPINE1 | docked (9) | 0.015 |
| ACVR1 | docked (9) | 0.005 |

*Reading.* The docking target set is **not statistically reproducible**: a median of 1 of the 17 dock-eligible hubs (and 0 of the 9 actually docked hubs) is recovered per resample, P(≥3 of 17) = 0.04, and the most stable single hub (CDHR5) reaches only 15.5%. This is consistent with the 0/35 hubs reaching ≥0.9 stability in the published per-gene bootstrap. The docking target list is therefore justified by **structural tractability (n_holo_PDB ≥ 1), not by statistical stability of hub selection**, and the docking results should be read as a screen of structurally tractable candidates rather than as a validated ranking of the 35 hubs.
