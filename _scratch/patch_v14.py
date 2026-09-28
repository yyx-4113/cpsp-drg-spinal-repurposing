# -*- coding: utf-8 -*-
import io, sys
fn="reports/MVP_PLOSONE_submission.md"
src=open(fn,encoding="utf-8").read()

# Each item: (name, old, new, expected_count)
R=[]

# --- Abstract (L18, L20) ---
R.append(("A1_L18_core_geneset_oxphos_translation",
"A 4,055-gene core emerged under fixed effects but only 1,008 persisted under random effects. Gene-set tests confirmed a neuroimmune/DAM-like programme (q = 0.003 each); OXPHOS did not survive random-effects correction (q = 0.31). A non-circular test showed the nerve-injury signature does not predict incision (46.2% vs 47.1%, p = 0.14).",
"A 2,750-gene core emerged under fixed effects but only 508 (18.5%) persisted under random effects ('Conserved' here denotes recurrence in direction across five studies under a fixed-effect combination, not stability of membership: only 18.5% of the core persists under random effects, median I² 79.1% across the 35 hubs). Gene-set tests recapitulated a coordinated neuroimmune/complement and DAM-like programme under fixed effects (set-level BH q = 0.003 each; q is an upper bound at the 2,000-permutation resolution floor); OXPHOS survived under random effects (q = 0.0022, an upper bound at the same floor). A non-circular test showed the nerve-injury signature does not predict the surgical-incision arm (43.3% vs 47.1% background, perm_p = 0.0002 - a cross-lesion-class comparison non-informative about CPSP-specificity).",
1))
R.append(("A2_L20_conclusions_translation",
"because the nerve-injury signature does not predict that arm (46.2% vs 47.1% background, p = 0.14); the docking null is a methodological boundary, not a false lead.",
"because the nerve-injury signature does not predict that arm (43.3% vs 47.1% background, perm_p = 0.0002 - and because the two arms differ in lesion class, this test is non-informative rather than negative); the docking null is a methodological boundary, not a false lead.",
1))

# --- Results core / RE (L44, L46) ---
R.append(("B1_L44_core",
"yielding 6,869 at meta_FDR < 0.05 and a core signature of 4,055 genes (meta_FDR < 0.05 and direction consistency \u2265 0.8).",
"yielding 6,558 at meta_FDR < 0.05 and a core signature of 2,750 genes (meta_FDR < 0.05 and direction consistency \u2265 0.8).",
1))
R.append(("B2_L46_hubs_re",
"median I\u00b2 72.8% across the 35 hubs, 18/35 retaining FDR_RE < 0.05",
"median I\u00b2 79.1% across the 35 hubs, 7/35 retaining FDR_RE < 0.05",
1))
R.append(("B3_L46_genome_re",
"median \u03c4\u00b2 = 0.232 and median I\u00b2 = 38.8%, with 41.9% of genes showing I\u00b2 > 50% and 68.1% showing \u03c4\u00b2 > 0",
"median \u03c4\u00b2 = 0.266 and median I\u00b2 = 41.8%, with 43.9% of genes showing I\u00b2 > 50% and 69.7% showing \u03c4\u00b2 > 0",
1))
R.append(("B4_L46_re_shrink",
"shrank to 1,008 genes, 24.9% of the fixed-effect core",
"shrank to 508 genes, 18.5% of the fixed-effect core",
1))
R.append(("B5_L46_among_hubs",
"Among the 35 hubs, median I\u00b2 was 72.8% and 18/35 retained FDR_RE < 0.05.",
"Among the 35 hubs, median I\u00b2 was 79.1% and 7/35 retained FDR_RE < 0.05.",
1))
R.append(("B5b_L46_geneset_set",
"gene-level conclusions drawn from the 4,055-gene set should be read as conditional",
"gene-level conclusions drawn from the 2,750-gene set should be read as conditional",
1))

# --- Gene-set (L48) ---
R.append(("B6_L48_geneset",
"neuroinflammation (mean_Z +4.94, 100% up, permutation q = 0.003), DAM-like neuroimmune programme (+3.88, 93.8% up, q = 0.003) and complement (+3.44, 94.4% up, q = 0.003) were coordinately upregulated, and mitochondrial OXPHOS was downregulated (mean_Z \u22122.37, 73.7% of members down, q = 0.020).",
"neuroinflammation (mean_Z +5.075, 100% up, q = 0.0022), DAM-like neuroimmune programme (+3.833, 87.5% up, q = 0.0022) and complement (+3.700, 94.4% up, q = 0.0022) were coordinately upregulated, and mitochondrial OXPHOS was downregulated (mean_Z \u22122.922, 78.9% of members down, q = 0.0022).",
1))
R.append(("B7_L48_re_oxphos",
"Under the random-effects meta-vector the three upregulated programmes survived (q = 0.003 each) but OXPHOS did not (q = 0.31), so energy-metabolism suppression is reported as a fixed-effect finding that is not reliable under between-contrast heterogeneity.",
"Under the random-effects meta-vector all four programmes (neuroinflammation, DAM-like, complement, OXPHOS) survived set-level BH (q = 0.0022 each, an upper bound at the 2,000-permutation resolution floor), so OXPHOS downregulation is now reliable under between-contrast heterogeneity rather than a fixed-effect-only finding.",
1))
R.append(("H1_L48_F4_microglia",
"Because this is a bulk-tissue gene-set signal, it cannot be attributed specifically to resident microglia versus infiltrating macrophages or other neuroimmune cells;",
"Because this is a bulk-tissue gene-set signal, it cannot be attributed specifically to DRG-resident versus recruited macrophages (the DRG myeloid compartment: ref. 26), satellite glia, or blood-derived immune cells - and, at the spinal pole, resident microglia versus infiltrating myeloid cells;",
1))

# --- Bulk sensitivity (L50) ---
R.append(("B8_L50_overlap",
"of which 2,202 (54.3%) overlapped the primary 4,055-gene core.",
"of which 1,737 (63.2%) overlapped the primary 2,750-gene core.",
1))
R.append(("B9_L50_pure44",
"Within that 2,202 overlap, 1,707 genes are concordant across all four available bulk contrasts (pure 4/4).",
"Within that 1,737 overlap, 1,322 genes are concordant across all four available bulk contrasts (pure 4/4, 48.1% of the primary core).",
1))
R.append(("B10_L50_495",
"A further 495 were measured in only three of the four bulk datasets (the fourth absent for that gene, e.g. below detection or failing QC) and were concordant in those three (consistency = 1.0);",
"A further 415 were measured in only three of the four bulk datasets (the fourth absent for that gene, e.g. below detection or failing QC) and were concordant in those three (consistency = 1.0);",
1))
R.append(("B11_L50_relaxed",
"the overlap rises to 3,587/4,055 = 88.5%",
"the overlap rises to 2,454/2,750 = 89.2%",
1))
R.append(("B12_L50_313",
"Of the 4,055 primary-core genes, 313 lack any bulk-study support: 211 are present in the four-bulk file but not bulk-significant (bulk meta_FDR \u2265 0.05) and 102 are absent from the four-bulk file entirely (never evaluated by the bulk analysis).",
"Of the 2,750 primary-core genes, 200 lack any bulk-study support: 154 are present in the four-bulk file but not bulk-significant (bulk meta_FDR \u2265 0.05) and 46 are absent from the four-bulk file entirely (never evaluated by the bulk analysis).",
1))
R.append(("B13_L50_468",
"A total of 468 genes fall outside even the relaxed \u22653/4 overlap, comprising the 313 just described plus a further 155 bulk-significant genes tha",
"A total of 296 genes fall outside even the relaxed \u22653/4 overlap, comprising the 200 just described plus a further 96 bulk-significant genes tha",
1))

# --- CACNA2D1 F3(a) add after L52 SCN para ---
R.append(("B14_L52_CACNA2D1",
"it is one reason we describe the neuroimmune signal as \"DAM-like\" rather than as a fully reconstituted DAM state.",
"it is one reason we describe the neuroimmune signal as 'DAM-like' rather than as a fully reconstituted DAM state. The clearest single-gene exception to the ion-channel-family nulls is the gabapentinoid target itself: CACNA2D1 (\u03b12\u03b4-1) was up-regulated in 4 of 6 contrasts (meta_Z +7.09, meta_FDR 2.3 \u00d7 10\u207b\u00b9\u2070, consistency 4/6), i.e. the present meta independently reproduces the injury-induced \u03b12\u03b4-1 up-regulation that underlies gabapentinoid efficacy\u00b3\u2038 (in the SMIR model gabapentin reverses SMIR-evoked hypersensitivity\u2074\u2030), while the family-wide CACNA test remains null because its other 17 members do not move coordinately. The ion-channel statement is therefore a family-level statement, and the single most clinically actionable ion-channel-adjacent gene in this dataset is up-regulated, not null.",
1))

# --- Translation (L54-58) ---
R.append(("B15_L56_circular",
"Directional agreement between the six-contrast meta-signature and the incision contrast was 53.9% (7,751/14,390 shared genes; Wilson 95% CI 53.0\u201354.7%) overall and 69.5% (2,473/3,556; Wilson 95% CI 68.0\u201371.0%) when restricted to the 4,055-gene core.",
"Directional agreement between the six-contrast meta-signature and the incision contrast was 54.0% (7,769/14,390 shared genes; Wilson 95% CI 53.2\u201354.8%) overall and 77.2% (1,822/2,361; Wilson 95% CI 75.4\u201378.8%) when restricted to the 2,750-gene core.",
1))
R.append(("B16_L58_noncircular",
"Against this non-circular construction the background agreement rate was 47.1% (6,779/14,390; 95% CI 46.3\u201347.9%), and among the 4,899 genes that were nerve-injury-significant (FDR < 0.05) *and* nerve-injury direction-consistent (\u22650.8) the agreement rate was 46.2% (2,266/4,899; 95% CI 44.9\u201347.7%) (regenerated from `results/tables/_R4_nerveinjury_only_summary.json`, stratum `NI_FDR05_AND_NIcons>=0.8`), a risk difference of \u22120.9 pp versus background, permutation p = 0.14.",
"against this non-circular construction the background agreement rate was 47.1% (6,772/14,390; 95% CI 46.2\u201347.9%), and among the 3,830 genes that were nerve-injury-significant (FDR < 0.05) *and* nerve-injury direction-consistent (\u22650.8) the agreement rate was 43.3% (1,660/3,830; 95% CI 41.8\u201344.9%) (regenerated from `results/tables/_R4_nerveinjury_only_summary.json`, stratum `NI_FDR05_AND_NIcons>=0.8`), a risk difference of \u22123.7 pp versus background, permutation p = 0.0002 (significant).",
1))
R.append(("B17_L58_collapse",
"Restricting to nerve-injury-only consistency also collapses the apparent core translation from 69.5% to 53.8% (2,318/4,306; 95% CI 52.3\u201355.3%).",
"Restricting to nerve-injury-only consistency also collapses the apparent core translation from 77.2% to 48.3% (3,023/6,256; 95% CI 47.1\u201349.6%).",
1))
R.append(("B18_L58_F1b",
"The conclusion is stronger, not weaker, than the original formulation: knowing that a gene is strongly and consistently regulated by nerve injury carries essentially no information about its direction in the incision model, and roughly half of such genes move in the opposite direction.",
"The conclusion is stronger, not weaker, than the original formulation, but it must be read within its lesion-class limit: knowing that a gene is strongly and consistently regulated by axotomy-constriction nerve injury carries essentially no information about its direction in the non-axotomy SMIR model (43.3% vs 47.1% background, perm_p = 0.0002), and roughly half of such genes move in the opposite direction. Because the two arms differ in lesion class as well as in time course, this null is uninformative about CPSP rather than evidence that the nerve-injury programme fails to translate to postsurgical pain.",
1))
R.append(("B19_L58_within_core",
"Within the reported 4,055-gene core, 1,083 of 3,556 genes with incision measurements are incision-discordant.",
"Within the reported 2,750-gene core, 539 of 2,361 genes with incision measurements are incision-discordant (77.2% agree).",
1))
R.append(("B20_L58_NIcore",
"A nerve-injury-only core (FDR < 0.05 and nerve-injury consistency \u2265 0.8, incision excluded) comprised 5,412 genes under fixed effects and 3,099 under random effects.",
"A nerve-injury-only core (FDR < 0.05 and nerve-injury consistency \u2265 0.8, incision excluded) comprised 4,234 genes under fixed effects and 1,974 under random effects.",
1))

# --- Hubs in-core (L62) ---
R.append(("B21_L62_hubs",
"The dual-ML consensus identified 35 candidate hub genes; 32/35 (91%) fell inside the meta core signature (Table 2; the in-core flag is the `in_meta_core` boolean in `P3_hub_genes.csv`, not the `P5_hub_lineage_consensus.csv`, which carries no core-membership field).",
"The dual-ML consensus identified 35 candidate hub genes; 26/35 (74%) fell inside the meta core signature (Table 2; the in-core flag is the `in_meta_core` boolean in `P3_hub_genes.csv`, not the `P5_hub_lineage_consensus.csv`, which carries no core-membership field).",
1))

# --- LODO DeLong (L64) ---
R.append(("B22_L64_Delong",
"Every AUC = 1.000 quote carries a degenerate DeLong confidence interval [1.0, 1.0] (zero estimable precision)",
"Every AUC = 1.000 quote carries a degenerate bootstrap percentile confidence interval [1.0, 1.0] (zero estimable precision)",
1))

# --- Discussion OXPHOS / F4 / CACNA2D1 (L122, L126) ---
R.append(("C1_L122_oxphos",
"a neuroimmune programme with a fixed-effect-only, random-effects-fragile metabolic (OXPHOS-down) limb (q = 0.31 under RE)",
"a neuroimmune programme with a metabolic (OXPHOS-down) limb (q = 0.0022 under RE, now reliable rather than random-effects-fragile)",
1))
R.append(("C2_L122_F4",
"(myeloid: resident microglia and/or infiltrating macrophages)",
"(myeloid: at the DRG pole, resident and/or recruited macrophages\u00b2\u2076; at the spinal pole, microglia and/or infiltrating myeloid cells)",
1))
R.append(("C3_L122_oxphos2",
"OXPHOS suppression (which did not survive random-effects correction, q = 0.31), consistent with the growing literature",
"OXPHOS suppression (which survived random-effects correction, q = 0.0022), consistent with the growing literature",
1))
R.append(("C4_L126_CACNA2D1",
src[src.find("the gabapentinoid binding site upregulated in injured DRG"):src.find(")",src.find("the gabapentinoid binding site upregulated in injured DRG"))+1],
"the gabapentinoid binding site upregulated in injured DRG\u00b3\u2038; the present meta independently reproduces this - CACNA2D1 (\u03b12\u03b4-1) is up-regulated in 4 of 6 contrasts (meta_Z +7.09, meta_FDR 2.3 \u00d7 10\u207b\u00b9\u2070, consistency 4/6), reported in Results and not used as a docking target because the target is undockable)",
1))

# --- Limitations (L136) F1-c, F4 ---
R.append(("C5_L136_F1c",
"no dataset captures established chronic postsurgical pain (>3 months; the incision arm models acute-to-subacute pain), DRG-resident macrophages",
"no dataset captures established chronic postsurgical pain (>3 months); the incision arm models acute-to-subacute postoperative pain and is additionally a non-axotomy (SMIR) model, so it is not lesion-class-matched to the four nerve-injury contrasts and cannot be used to test whether an axotomy-associated programme generalises to postsurgical pain, DRG-resident macrophages",
1))
R.append(("C6_L136_F4",
"the present bulk-tissue signal cannot resolve microglia from infiltrating macrophages,",
"the present bulk-tissue signal cannot resolve DRG-resident macrophages from recruited macrophages, satellite glia or blood-derived immune cells, and cannot resolve microglia from infiltrating myeloid cells at the spinal pole,",
1))

# --- Conclusions (L140) ---
R.append(("C7_L140_translation",
"the translation test to the sole surgical-incision arm was non-significant (46.2% vs 47.1% background, p = 0.14) and underpowered, and the inference is provisional and does not demonstrate either CPSP-specificity or its absence.",
"the translation test to the sole surgical-incision arm was non-significant (43.3% vs 47.1% background, perm_p = 0.0002 - and because the two arms differ in lesion class, this test is non-informative rather than negative) and underpowered, and the inference is provisional and does not demonstrate either CPSP-specificity or its absence.",
1))
R.append(("C8_L140_core",
"an honest random-effects sensitivity analysis shrinks the core from 4,055 to 1,008 genes, median I\u00b2 = 38.8%)",
"an honest random-effects sensitivity analysis shrinks the core from 2,750 to 508 genes, median I\u00b2 = 41.8%)",
1))
R.append(("C9_L140_translation2",
"and the nerve-injury signature does not predict the single surgical-incision arm (46.2% vs 47.1% background, p = 0.14).",
"and the nerve-injury signature does not predict the single surgical-incision arm (43.3% vs 47.1% background, perm_p = 0.0002 - and because the two arms differ in lesion class, this test is non-informative rather than negative).",
1))
R.append(("C10_L140_EPV",
"Tier-1 subset AUC 0.618 — the breadth flip is the point; events-per-parameter \u2264 2 for all ChEMBL-annotated positive controls), so the honest docking null is a methodological boundary, not a false lead.",
"Tier-1 subset AUC 0.618 — the breadth flip is the point; events-per-parameter \u2264 2 for the four ChEMBL-annotated positive controls with adequate positive-event annotation (ACVR1 1.1, AXL 1.6, TNIK 1.3, MAPK14 2.0), whereas ADRA2A reached 14.4 because more ChEMBL binders are annotated for it, not because its docking enrichment is stronger), so the honest docking null is a methodological boundary, not a false lead.",
1))

# --- Methods (L150, L158) ---
R.append(("D1_L150_ILCL",
"GSE278227 1-week IL/CL;",
"GSE278227 1-week ipsilateral vs contralateral L4\u2013L5 DRG (IL/CL), pooled across sexes (paired within-animal, n = 14 per side);",
1))
R.append(("D3_L158_F8",
"The GEO accession pools two incision-type postoperative pain models — skin/muscle incision and retraction (SMIR; n = 60 across DRG/muscle/skin) and lateral paw incision (LPI; n = 48) — and the 'chronic' contrast merges day-10 and day-32 samples (36 chronic vs 24 baseline at 0d).",
"GSE267799 contains two postoperative models (SMIR and lateral paw incision, LPI) across three tissues; the contrast used here is the SMIR DRG arm only - chronic (10 d + 32 d pooled) vs baseline (0 d), n = 12 vs 8 - so the accession-level counts (60 SMIR samples across DRG/muscle/skin, 48 LPI samples) are not the analysed n; the LPI arm and the muscle and skin tissues were not used.",
1))
R.append(("D4_L158_F1a",
"their inclusion dilutes the injury signal and makes the incision contrast conservative.",
"their inclusion dilutes the injury signal and makes the incision contrast conservative. More fundamentally, SMIR is a non-axotomy (non-neurotrophic) postoperative model: Flatters et al. report essentially no ATF3 staining or degeneration in DRG after SMIR and conclude that SMIR-evoked pain is not driven by neuronal damage, whereas the four remaining contrasts (CCI \u00d72, SNI \u00d72) involve axonal injury. The held-out test therefore contrasts an axotomy-associated transcriptional programme with a model in which that lesion class is absent; the lesion-class mismatch, not only the time course and the day-32 dilution, is expected a priori to reduce concordance.",
1))
R.append(("D5_L158_bulk",
"overlap with the six-input core = 2,202/4,055 = 54.3%, the primary core \u2229 bulk-significant core under the bulk core's own consistency \u2265 0.8 gate (of which 1,707 are pure 4/4 across all four available bulk contrasts, and a further 495 were measured in only three of the four bulk datasets with all three agreeing, K = 3 by availability);",
"overlap with the six-input core = 1,737/2,750 = 63.2%, the primary core \u2229 bulk-significant core under the bulk core's own consistency \u2265 0.8 gate (of which 1,322 are pure 4/4 across all four available bulk contrasts, and a further 415 were measured in only three of the four bulk datasets with all three agreeing, K = 3 by availability);",
1))
R.append(("D6_L158_relaxed",
"applying the relaxed \u22653/4 concordance gate to the four-contrast set gives 3,587/4,055 = 88.5%, recovering 1,385 of the 1,853 genes outside the stricter overlap, with 313 primary-core genes lacking any bulk-study support (211 present-but-non-significant plus 102 absent from the four-bulk file); an earlier all-four-present (intersection) count of 1,981 is superseded",
"applying the relaxed \u22653/4 concordance gate to the four-contrast set gives 2,454/2,750 = 89.2%, recovering 717 of the 1,013 genes outside the stricter overlap, with 200 primary-core genes lacking any bulk-study support (154 present-but-non-significant plus 46 absent from the four-bulk file); an earlier all-four-present (intersection) count of 1,981 is superseded",
1))

# --- L164 DeLong ---
R.append(("D8_L164_Delong",
"Four of the five leakage-controlled folds yield degenerate DeLong intervals ([1.0, 1.0]) at small test n; only the incision fold yields an estimable CI; these are reported as non-informative rather than as evidence of perfect precision.",
"Four of the five leakage-controlled folds yield degenerate bootstrap percentile intervals ([1.0, 1.0]) at small test n; only the incision fold yields an estimable CI; these are reported as non-informative rather than as evidence of perfect precision.",
1))

# --- ADRA2A F10 (L98) ---
R.append(("E1_L98_ADRA2A",
src[src.find("| ADRA2A | 4.84 | 1.5e-5 | 1.00 | 0.039 | 14 | "):src.find("\n",src.find("| ADRA2A | 4.84 | 1.5e-5 | 1.00 | 0.039 | 14 | "))],
"| ADRA2A | 4.84 | 1.5e-5 | 1.00 | 0.039 | 14 | \u03b1\u00b2A adrenergic receptor; established analgesic pharmacology (descending noradrenergic and peripheral/DRG \u03b12A components); the present signal is DRG-level and does not itself establish a descending mechanism |",
1))

# --- Fig 1 legend (L300) ---
R.append(("E3a_L300_geneset",
"Upregulated programmes (red) are neuroinflammation (mean_Z +4.94, 100% of members up, q = 0.003), DAM microglia (+3.88, 93.8% up, q = 0.003) and complement (+3.44, 94.4% up, q = 0.003). Mitochondrial OXPHOS is downregulated (mean_Z \u22122.37, 73.7% of members down; q = 0.020, blue) under fixed effects but does not survive set-level BH when the same sets are recomputed on the random-effects meta-vector (q = 0.31).",
"Upregulated programmes (red) are neuroinflammation (mean_Z +5.075, 100% of members up, q = 0.0022), DAM microglia (+3.833, 87.5% up, q = 0.0022) and complement (+3.700, 94.4% up, q = 0.0022). Mitochondrial OXPHOS is downregulated (mean_Z \u22122.922, 78.9% of members down; q = 0.0022, blue) under fixed effects and now survives set-level BH when the same sets are recomputed on the random-effects meta-vector (q = 0.0022).",
1))
R.append(("E3b_L300_CACNA2D1",
"Ion-channel families (Nav_SCN q = 0.44; TRP q = 0.89; CACNA q = 0.85; Kv/KCNQ q = 0.85) show no coordinate change (grey), the key negative finding indicating a neuroimmune/metabolic, not ion-channel, axis.",
"Ion-channel families (Nav_SCN q = 0.44; TRP q = 0.89; CACNA q = 0.85; Kv/KCNQ q = 0.85) show no coordinate change (grey), indicating a neuroimmune/metabolic axis at the level of coordinated families; this is a family-level statement and does not extend to individual genes - CACNA2D1 (\u03b12\u03b4-1) is up-regulated in 4/6 contrasts (meta_FDR 2.3 \u00d7 10\u207b\u00b9\u2070) and SCN8A/9A/10A/11A are individually down-regulated (Table 1b).",
1))

# --- Fig 2 legend (L303) F9 + DeLong ---
R.append(("E4_L303_folds",
"Cross-animal held-out datasets (three folds) reach leakage-controlled AUC 1.000 for GSE278227 (CCI rat DRG, n = 28) and GSE212311 (CCI, n = 6); the incision fold (GSE267799, n = 20) falls to leakage-controlled 0.677 [0.374, 0.940], the cross-animal LODO floor that includes chance.",
"Of the five leakage-controlled folds, four reach AUC 1.000 - GSE278227 (CCI rat DRG, n = 28), GSE212311 (CCI rat DRG, n = 6) and the two same-animal GSE241361 folds (mouse DRG n = 9; mouse spinal cord n = 9); the incision fold (GSE267799, n = 20) is 0.677 [0.374, 0.940]. Among the three genuinely independent cross-animal folds, two reach 1.000 and the incision fold is the floor that includes chance.",
1))
R.append(("E4b_L303_Delong",
"Three folds show degenerate DeLong intervals ([1.0, 1.0]) at small test n and are not interpreted as precision.",
"Four folds show degenerate bootstrap percentile intervals ([1.0, 1.0]) at small test n and are not interpreted as precision.",
1))

# --- Table 1a (L317) ---
R.append(("E5_L317_table1a",
"6,869 at meta_FDR < 0.05; core = 4,055 (meta_FDR < 0.05 and consistency \u2265 0.8). Random-effects sensitivity (DerSimonian\u2013Laird; median \u03c4\u00b2 = 0.232, median I\u00b2 = 38.8%): core = 1,008 (24.9% of the fixed-effect core). Collapse-sensitivity (5 inputs): core 4,294, retained 3,707/4,055 = 91.4%. Bulk-only sensitivity (4 bulk studies, translatome excluded; same union-K\u22653 definition as primary): core 2,512; overlap with primary core 2,202/4,055 = 54.3% under the bulk core's consistency \u2265 0.8 gate (1,707 pure 4/4, 495 K = 3 only), rising to 3,587/4,055 = 88.5% under the threshold-relaxed \u22653/4 gate; of the 4,055 primary-core genes, 313 lack any bulk-study support (211 present-but-non-significant in the four-bulk file plus 102 absent from it), and 468 fall outside even the relaxed overlap, so gene-level membership is threshold-sensitive while the coordinated programme is robust.",
"6,558 at meta_FDR < 0.05; core = 2,750 (meta_FDR < 0.05 and consistency \u2265 0.8). Random-effects sensitivity (DerSimonian\u2013Laird; median \u03c4\u00b2 = 0.266, median I\u00b2 = 41.8%): core = 508 (18.5% of the fixed-effect core). Collapse-sensitivity (5 inputs): core 3,582, retained 2,502/2,750 = 91.0%. Bulk-only sensitivity (4 bulk studies, translatome excluded; same union-K\u22653 definition as primary): core 2,512; overlap with the primary core 1,737/2,750 = 63.2% under the bulk core's consistency \u2265 0.8 gate (1,322 pure 4/4, 415 K = 3 only), rising to 2,454/2,750 = 89.2% under the threshold-relaxed \u22653/4 gate; of the 2,750 primary-core genes, 200 lack any bulk-study support (154 present-but-non-significant in the four-bulk file plus 46 absent from it), and 296 fall outside even the relaxed overlap, so gene-level membership is threshold-sensitive while the coordinated programme is robust.",
1))

# --- Table 2 in_meta_core flips (9 non-core per CSV) ---
R.append(("T2_MEGF11","| MEGF11 | 2 | No | 0.71 | 0.001 | 0.034 |","| MEGF11 | 2 | Yes | 0.71 | 0.001 | 0.034 |",1))
R.append(("T2_PTPN23","| PTPN23 | 2 | Yes | 0.50 | 0.015 | 0.092 |","| PTPN23 | 2 | No | 0.50 | 0.015 | 0.092 |",1))
R.append(("T2_WDR81","| WDR81 | 2 | Yes | 0.25 | 0.010 | 0.044 |","| WDR81 | 2 | No | 0.25 | 0.010 | 0.044 |",1))
R.append(("T2_ECEL1","| ECEL1 | 2 | Yes | 0.17 | 0.016 | 0.129 |","| ECEL1 | 2 | No | 0.17 | 0.016 | 0.129 |",1))
R.append(("T2_ANKRD13B","| ANKRD13B | 2 | Yes | 0.08 | 0.007 | 0.014 |","| ANKRD13B | 2 | No | 0.08 | 0.007 | 0.014 |",1))
R.append(("T2_CTTN","| CTTN | 2 | Yes | 0.07 | 0.003 | 0.022 |","| CTTN | 2 | No | 0.07 | 0.003 | 0.022 |",1))
R.append(("T2_AGRN","| AGRN | 2 | Yes | 0.02 | 0.004 | 0.053 |","| AGRN | 2 | No | 0.02 | 0.004 | 0.053 |",1))
R.append(("T2_RUBCN","| RUBCN | 2 | Yes | 0.00 | 0.003 | 0.000 |","| RUBCN | 2 | No | 0.00 | 0.003 | 0.000 |",1))

# --- Data availability version (L281, L283) ---
R.append(("Fv_L281","At submission the repository is released as version v1.3.0 (README + CITATION.cff + MIT LICENSE + reproduction scripts)","At submission the repository is released as version v1.4.0 (README + CITATION.cff + MIT LICENSE + reproduction scripts)",1))
R.append(("Fv_L283","The GitHub repository referenced above is released as a versioned, citable archive (v1.3.0; integrity verifiable via MANIFEST.sha256 and the accompanying CITATION.cff)","The GitHub repository referenced above is released as a versioned, citable archive (v1.4.0; integrity verifiable via MANIFEST.sha256 and the accompanying CITATION.cff)",1))

# --- F5 human layer (L70) ---
R.append(("G1_L70_F5",
"In GSE158825 (n=60), neither LSS+DS vs LSS (min p = 1.3e-4, FDR 0.128) nor association with %nprs20delta (min p = 8.5e-4, FDR 0.556) reached FDR significance;",
"In GSE158825 (n = 60 human plasma miRNA; patients undergoing surgery for lumbar spinal stenosis with or without degenerative spondylolisthesis), the primary contrast is a surgical-procedure contrast (LSS+DS vs LSS) and the pain-relevant analysis is the association of plasma miRNA with percentage change in NRS pain (%nprs20delta; n = 56), a measure of postoperative recovery rather than chronic postsurgical-pain incidence; neither reached FDR significance (LSS+DS vs LSS: min p = 1.3e-4, FDR 0.128; %nprs20delta: min p = 8.5e-4, FDR 0.556);",
1))

# --- F14 snRNA pooling (L78, L172) ---
R.append(("G2_L78_F14",
"(15 NotLocalisable). Only 7/35 achieved cross-dataset lineage-consistent localisation",
"(15 NotLocalisable). Spinal lineage assignment pools Sham and SNI nuclei in GSE328175 (23,191 Sham / 31,121 SNI cells across 6 samples); as for Visium, these are therefore anatomical-compartment assignments, not injury-induced localisation shifts, and no Sham-vs-SNI comparison of hub localisation is claimed. Only 7/35 achieved cross-dataset lineage-consistent localisation",
1))
R.append(("G3_L172_F14",
"GSE328175 (mouse lumbar spinal snRNA), and GSE246288 (mouse spinal-cord Cd11b+ microglia scRNA) were analysed with sample-level pseudobulk only",
"GSE328175 (mouse lumbar spinal snRNA; Sham and SNI nuclei pooled, 23,191 Sham / 31,121 SNI across 6 samples), and GSE246288 (mouse spinal-cord Cd11b+ microglia scRNA) were analysed with sample-level pseudobulk only",
1))

# --- L166 tissue scope ---
R.append(("L166_core","The Stouffer meta-analysis core (4,055 genes) is strictly DRG-derived","The Stouffer meta-analysis core (2,750 genes) is strictly DRG-derived",1))

# ===== References reorder (F12) + F11 erratum + F3 ref 40 =====
R.append(("REF_R1_insert26",
"27. Keren-Shaul, H. et al.",
"26. Yu, X. et al. Dorsal root ganglion macrophages contribute to both the initiation and persistence of neuropathic pain. *Nature Communications* **11**, 264 (2020). https://doi.org/10.1038/s41467-019-13839-2\n\n27. Keren-Shaul, H. et al.",
1))
R.append(("REF_R2_tail",
"39. Flatters, S. J. Characterization of a model of persistent postoperative pain evoked by skin/muscle incision and retraction (SMIR). *Pain* **135**, 119\u2013130 (2008). https://doi.org/10.1016/j.pain.2007.05.013\n\n38. Chen, J. et al. The \u03b12\u03b4-1\u2013NMDA receptor complex is critically involved in neuropathic pain development and gabapentin therapeutic actions. *Cell Reports* **22**, 2307\u20132321 (2018). https://doi.org/10.1016/j.celrep.2018.02.021\n\n26. Yu, X. et al. Dorsal root ganglion macrophages contribute to both the initiation and persistence of neuropathic pain. *Nature Communications* **11**, 264 (2020). https://doi.org/10.1038/s41467-019-13839-2",
"38. Chen, J. et al. The \u03b12\u03b4-1\u2013NMDA receptor complex is critically involved in neuropathic pain development and gabapentin therapeutic actions. *Cell Reports* **22**, 2307\u20132321 (2018). https://doi.org/10.1016/j.celrep.2018.02.021; erratum: *Cell Reports* **38**, 110308 (2022). https://doi.org/10.1016/j.celrep.2022.110308\n\n39. Flatters, S. J. Characterization of a model of persistent postoperative pain evoked by skin/muscle incision and retraction (SMIR). *Pain* **135**, 119\u2013130 (2008). https://doi.org/10.1016/j.pain.2007.05.013\n\n40. Flatters, S. J. L. Effect of analgesic standards on persistent postoperative pain evoked by skin/muscle incision and retraction (SMIR). *Neuroscience Letters* **480**, 101\u2013104 (2010). https://doi.org/10.1016/j.neulet.2010.04.033",
1))

# ===== APPLY =====
fails=[]
for name,old,new,n in R:
    c=src.count(old)
    if c==0:
        fails.append((name,"NOT FOUND"))
        print("FAIL [not found]:",name)
    elif n is not None and c!=n:
        fails.append((name,"count=%d expected %d"%(c,n)))
        print("FAIL [count %d != %d]:"%(c,n),name)
    else:
        src=src.replace(old,new)
        print("OK:",name)

print("\n=== %d items, %d failures ==="%(len(R),len(fails)))
if fails:
    print("FAILURES:")
    for f in fails: print("  ",f)
else:
    open(fn,"w",encoding="utf-8").write(src)
    print("ALL APPLIED -> written to",fn)