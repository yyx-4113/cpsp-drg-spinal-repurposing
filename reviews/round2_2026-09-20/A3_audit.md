# Reviewer A3 — Implementation & provenance / recompute audit
**Manuscript:** *A neuroimmune–metabolic programme defines the chronic postsurgical pain DRG–spinal axis with an honest repurposing null* (Scientific Reports, Article)
**Role:** Independent recompute auditor. I treated this as a first submission, read the main + supplementary manuscripts, and recomputed every headline number directly from the authoritative CSV outputs in `results/tables/` using `python 3.13.12`. I did **not** read the Round-1 review, the submission manifest, project-plan/README/CITATION files, other reviewers' files, or the gate scripts; the gate PASS was not taken as verification.
**Bottom line:** The quantitative backbone is, with a few important exceptions, reproducible from raw CSVs. I found **one major citation-completeness failure (3 orphan references, two of them directly on-topic), one metric-ambiguity that alters the plain reading of a headline enrichment (SPRR1A "17.4×"), one provenance gap (the Tier-1 ADRA2A AUC 0.618 is not in any authoritative CSV), and several minor internal inconsistencies.** None invalidate the core "honest null" conclusion, but the flagged items must be corrected before acceptance because they are exactly the kind of number/label mismatches a computational-methods reviewer should catch.

---

## § What I actually checked (recomputed value vs manuscript, discrepancy stated)

| # | Claim (manuscript) | Recomputed from CSV | Verdict |
|---|---|---|---|
| 1 | Core signature **4,055** genes; genes tested **16,552**; meta_FDR<0.05 = 6,869 (L31) | `META_DRG_axis_CORE_signature.csv` = 4,055 rows, all FDR<0.05 & consistency≥0.8; `META_DRG_axis_stouffer.csv` = 16,552 rows; 6,869 have meta_FDR<0.05 | ✅ exact |
| 1b | ATF3 meta_Z **10.53**, FDR **1.0e-21**, consistency **1.00** (L31) | 10.533 / 1.00e-21 / 1.00 | ✅ exact |
| 2 | Neuroinflammation mean_Z **+4.94 / 100% up**; DAM **+3.88 / 93.8% up**; complement **+3.44 / 94.4% up**; OXPHOS **−2.37 / 73.7% down** (L33, Fig1) | `P3_geneset_stats.csv`: 4.9435/1.000; 3.8838/0.9375; 3.4409/0.9444; −2.3728/0.7368 (frac_down=1−0.2632) | ✅ exact (93.75→93.8, 94.44→94.4, 73.68→73.7 rounding) |
| 3 | SCN9A/10A/11A meta_Z **−3.6 to −3.1**; FDR **1.7e-3–5.9e-3**; 5/6 down (L33,64, Abstract) | `META…stouffer.csv`: SCN11A −3.558/FDR 1.73e-3; SCN9A −3.475/2.26e-3; SCN10A −3.153/5.94e-3; all consistency 0.83, n_dn=5,n_up=1 | ⚠️ FDR range exact; meta_Z range should be **−3.56 to −3.15**, not −3.6 to −3.1 (see D5) |
| 4 | **32/35** hubs in meta core (L36) | `P3_hub_genes.csv` `in_meta_core=True` = 32; False = REG3B, ANKRD1, MEGF11 | ✅ exact |
| 5 | LODO GSE267799 **0.917 [0.729, 1.000]** (L38) | `P3_lodo_auc_ci.csv`: 0.9167, lo 0.7291, hi 1.0, n=20 | ✅ exact |
| 6 | DRG **20/25** localise to injured/regenerating neuron; SPRR1A 98.1% vs 16.8% detection (**17.4×**); ECEL1 25.7×; NPY 10.0×; FLNC 10.2× (L44) | `P5_GSE216039_DRG_hub_finetype_top.csv`: 20/25 with top_finetype=Injured_RegenNeuron & detected; SPRR1A top_pct 0.981/others_pct 0.168 → detection ratio **5.84×**, `specificity` col=17.39; ECEL1 25.69; NPY 10.04; FLNC 10.21 | ⚠️ counts exact; **"17.4×" is the mean-expression ratio (specificity), NOT the detection ratio (5.84×)** — see D2 |
| 7 | Spinal **7/35** confident (≥2 datasets) (L46) | `P5_hub_lineage_consensus.csv` `confident==True` = 7 (TFE3, ANKRD13B, CHL1, CTTN, PTPN23, SRRM4, VASH2) | ✅ exact |
| 8 | Visium **33/35** detectable; **17/35** dorsal horn (L51, Fig4B) | `P5_GSE325938_hub_regionalization.csv`: CRISP3 & LNP1 have top_label_log2=0 (broad/low) → 33 detectable; top_region==DorsalHorn = 17 | ✅ counts exact; ⚠️ denominator framing — see D6 |
| 9 | ADRA2A full-library AUC **0.532**, raw p **0.118**, MW-adjusted **0.578** (L54,56) | `P6_reverse_control.csv` auc 0.5325; `P6_enrichment_mw_confounder_check.csv` p_mannwhitney 0.1184, AUC_MW_adjusted 0.578 | ✅ exact |
| 10 | precision@10 = **0.700**, lift **×18.69**, p **9.4e-9**; precision@20 = **0.450**, p **1.3e-8** (L56) | `P6_mw_ranking_summary.csv`: prec@10_raw 0.7, hyper_p@10 9.45e-9, lift@10 18.69; prec@20_raw 0.45, hyper_p@20 1.26e-8 | ✅ exact |
| 11 | Multivariate LR p: AXL **2.6e-5**, TNIK **7.3e-5**, ACVR1 **9.6e-4**, ADRA2A **0.027**, MAPK14 **0.066**; BH q (S4) | `P6_multivariate_physchem_control.csv` LR_dock_residual_p: 2.55e-5/7.26e-5/9.57e-4/0.0269/0.0662; `P6_BH_correction.csv` BH_q matches S4 | ✅ exact |
| 12 | Human layer set-level permutation **p = 0.51**; **253** hubs-with-plasma-miRNAs (L41) | `P4_setlevel_test.json` perm_p 0.5101, n=253; `P4_hub_targeting_miRNAs.csv` = 3,511 (hub,miRNA) pairs over only **33** distinct hubs, no plasma column | ⚠️ p exact; **"253" = number of (hub, plasma-detectable miRNA) pairs, not 253 hubs** — see D3 |
| 13 | Every reference 1–18 cited in-text | Citations found: {1,2,3,4,6,7,8,9,10,13,14,15,16,17,18}; **orphans = {5, 11, 12}** | ❌ 3 orphan references — see D1 |
| 14 | Abstract vs body: ADRA2A 0.618→0.532 p=0.118; SCN FDR 1.7e-3–5.9e-3; human miRNA p=0.51 | Abstract (L14) and body (L41,56) agree on all three; but **Tier-1 0.618 has no authoritative CSV** (see D4) | ⚠️ abstract↔body consistent; D4 provenance gap |

---

## § Specific discrepancies (four-part contract)

### D1 — Three listed references (5, 11, 12) are never cited in-text  ❌ MAJOR
【Problem】 Three of the 18 bibliography entries are orphaned: they appear in the References section but are never referenced by an in-text superscript.
【Evidence】 Automated extraction of superscript citations from `MVP_ScientificReports_submission.md` (with range-expansion of `⁶⁻⁸` and `¹⁴⁻¹⁷`) yields cited set {1,2,3,4,6,7,8,9,10,13,14,15,16,17,18}; missing = **5, 11, 12**. Direct grep confirms `⁵`, `¹¹`, `¹²` are absent from the body. The orphaned entries are: **5** Sapio et al. (dynorphin/enkephalin opioid peptides in spinal cord & DRG), **11** Divito et al. (Suzetrigine, a novel nonopioid systemic analgesic), **12** McDonnell et al. (Nav1.7/SCN9A blocker PF-05089771 in painful diabetic neuropathy).
【Why it matters】 Scientific Reports requires that every reference be cited (and the Reporting Summary / reference-manager checks typically enforce this). More substantively, refs 11 and 12 are *directly on-topic*: the manuscript's whole repurposing narrative pivots on (a) analgesics not being enriched and (b) SCN9A/10A/11A being down-regulated yet undockable. A nonopioid analgesic (Suzetrigine, ref 11) and a Nav1.7 blocker (ref 12) are the two most natural comparators for those exact claims and their omission looks like a gap, not a styling slip. Ref 5 (opioid peptides in the DRG–spinal axis) is relevant to the neuroimmune/opioid discussion in L64.
【Specific fix】 Either (i) insert the citations where the science demands them — e.g. L53–56 (analgesic-enrichment null) → cite ref 11 (Suzetrigine) and ref 12 (Nav1.7/SCN9A blocker) as the concrete "known analgesics / Nav-blocking strategies" the study says it does *not* address; L64 (opioid/DRG–spinal axis) → cite ref 5 — or (ii) delete the three entries from the bibliography if they are genuinely unused. Do not ship a manuscript with orphan references; the gate will block it.

### D2 — SPRR1A "17.4×" is the mean-expression ratio, not the detection-fraction ratio (5.84×)  ⚠️ MAJOR / critical
【Problem】 The headline "SPRR1A 98.1% vs 16.8% detection (17.4×)" presents 17.4× as if it were the detection-fraction ratio, but 98.1/16.8 = **5.84×**, and 17.4× is in fact the mean log2-expression fold (`specificity` = top_mean/others_mean).
【Evidence】 `P5_GSE216039_DRG_hub_finetype_top.csv`, SPRR1A row: `top_pct`=0.981, `others_pct`=0.168 ⇒ **detection ratio = 0.981/0.168 = 5.84×**; `top_mean`=3.0912, `others_mean`=0.1777 ⇒ **expression ratio = 17.39×** (the `specificity` column = 17.39); `log2_enrich_pct`=2.54 ⇒ 2^2.54 = 5.84×, i.e. the log2 column encodes the *detection* ratio, while the `specificity` column encodes the *expression* ratio. Body L44 writes "SPRR1A 98.1% vs 16.8% detection (17.4×)". Fig 3 legend (L154) is internally consistent — it correctly states the bars are the *mean log2 expression ratio* and lists "SPRR1A 17.4× (98.1% vs 16.8% detection)" — but the **body prose** reads as if 17.4× follows the detection percentages, implying a detection ratio. Recomputed equivalents for the other three: ECEL1 specificity 25.69 (stated 25.7×), detection ratio 2^4.0≈16×; NPY 10.04 vs detection ratio 2^3.51≈11.5×; FLNC 10.21 vs detection ratio 2^3.46≈11×. So **all four "×" values are expression ratios, not detection ratios**, yet only the SPRR1A line juxtaposes them against detection percentages, creating the false implication.
【Why it matters】 A reader (and a meta-analyst) who takes "98.1% vs 16.8% detection (17.4×)" at face value will conclude the *detection* is 17.4-fold enriched, when it is only 5.84-fold; the 17.4× describes how much *higher the mean expression* is in injured vs other neurons. These are different biological statements (detection prevalence vs expression magnitude) and the conflation can be lifted verbatim into a review or press summary. This is precisely the "metric ambiguity the automated gates cannot see."
【Specific fix】 In L44, decouple the two metrics explicitly, e.g.: *"SPRR1A was detected in 98.1% of injured/regenerating neurons vs 16.8% of other subtypes (detection-ratio 5.8×), with a mean-expression enrichment of 17.4×; ECEL1 25.7×, NPY 10.0×, FLNC 10.2× (all mean-expression fold = injured/regenerating ÷ other subtypes)."* Add one clause that the "×" enrichment values throughout are **mean-expression** folds (specificity = top_mean/others_mean), distinct from detection-fraction ratios, so the Fig 3 legend and body agree unambiguously.

### D3 — "253 hubs" is actually 253 (hub, plasma-detectable miRNA) pairs  ⚠️ MAJOR (definition)
【Problem】 The number 253 is described as hubs ("253 hubs with human-plasma-detectable targeting miRNAs", L41/Methods) but is physically impossible as a hub count and is in fact the count of high-confidence (hub→miRNA) pairs used in the set-level permutation.
【Evidence】 `P4_setlevel_test.json`: `{"n": 253, "perm_p": 0.5101, ...}` — the permutation permutes 253 items. `P4_hub_targeting_miRNAs.csv`: 3,511 (hub,miRNA) rows, but only **33 distinct hub symbols** (out of 35 hubs) and **no plasma-detection column at all** — so 253 cannot be a hub count (there are only 35 hubs; 33 have any predicted targeting miRNA). The only authoritative source of "253" is the permutation's `n`. The manuscript L41 text "33/35 hubs had predicted targeting miRNAs (608 high-confidence), 253 detectable in human plasma" reads most naturally as 253 *pairs* (of the 608 high-confidence pairs, 253 are plasma-detectable), which is consistent with `n=253`; but the parallel phrase "253 hubs with human-plasma-detectable targeting miRNAs" mislabels them as hubs.
【Why it matters】 Calling 253 items "hubs" is arithmetically impossible and, if a reader cross-checks against the 35-hub set, undermines confidence in the human layer. The honest-negative conclusion (perm_p = 0.51) is unaffected, but the wording must be exact.
【Specific fix】 Replace "253 hubs with human-plasma-detectable targeting miRNAs" with "253 high-confidence hub→miRNA pairs detectable in human plasma (of 608 high-confidence predicted pairs; spanning 33 of 35 hubs)". State plainly in Methods that the set-level permutation (perm_p = 0.51) was run over the 253 plasma-detectable pairs.

### D4 — The Tier-1 ADRA2A AUC 0.618 is not reproducible from any authoritative CSV  ⚠️ MAJOR (provenance)
【Problem】 The pivotal "Tier-1 AUC 0.618 → full-library 0.532" flip is stated identically in Abstract (L14) and body (L56), but the value 0.618 does not exist in any `results/tables/*.csv`; it survives only in narrative markdown outside the tables folder.
【Evidence】 Grep for "0.618" across `results/` returns only narrative files (`P6_breadth_note.md`, `P6_FJNSF_APPLICATION_SUBMISSION*.md`, etc.) — none of which are the authoritative `results/tables/` CSVs. The breadth file `P6_breadth_target_summary.csv` confirms `n_t1 = 620` for ADRA2A (the 620-drug CNS/analgesic subset is real) and contains median/quantile affinities but **no AUC column**, so the 0.618 cannot be recomputed from the provided CSVs. The full-library 0.532 / p 0.118 / MW-adjusted 0.578 (D9) *are* fully reproducible. So the abstract↔body agreement on 0.618 is internally consistent, but the number itself is not provenance-anchored to a table the reviewer can recompute.
【Why it matters】 As the recompute auditor, I can verify 0.532 but not 0.618. A headline "the Tier-1 signal was overturned" rests on a number I cannot trace to a CSV; if the Tier-1 AUC script is not archived or its CSV is missing, the most newsworthy claim in the docking section is unverifiable. This is exactly the provenance gap the brief asks me to surface.
【Specific fix】 Add a CSV — e.g. `P6_breadth_tier1_auc.csv` (one row per target: AUC_dock_Tier1, n_t1, p, CI) — containing ADRA2A Tier-1 AUC = 0.618 and its p/CI, and cite it in L56 / Table 3. Until that file exists, annotate L56 with the script that produced 0.618 so the value is recomputable.

### D5 — SCN meta_Z range stated as −3.6 to −3.1 but recomputed −3.56 to −3.15  ⚠️ MINOR
【Problem】 The abstract/body state the three SCN channels span meta_Z −3.6 to −3.1, but the actual range is −3.56 (SCN11A) to −3.15 (SCN10A).
【Evidence】 `META_DRG_axis_stouffer.csv`: SCN11A −3.558, SCN9A −3.475, SCN10A −3.153. Rounded to one decimal the range is −3.2 to −3.6; the stated upper bound −3.1 is off by ~0.05 from the true maximum (−3.15). FDR range (1.7e-3–5.9e-3) is exact.
【Why it matters】 Cosmetic, but a methods reviewer will recompute and notice the bounds don't match; it weakens the "down-regulated −3.6 to −3.1" phrasing.
【Specific fix】 Change "meta_Z −3.6 to −3.1" to "meta_Z −3.6 to −3.2 (range −3.56 to −3.15)".

### D6 — Visium "33/35 detectable" vs "17/35 mapped to dorsal horn" denominator framing  ⚠️ MINOR
【Problem】 Two fractions in L51 use the same denominator (35) but describe partially overlapping populations, which can be misread as 17/33.
【Evidence】 `P5_GSE325938_hub_regionalization.csv`: 33/35 hubs are detectably expressed (CRISP3 & LNP1 have log2=0, tier broad/low); of all 35 hubs, 17 have top_region = DorsalHorn (CRISP3/LNP1 map to MeningealFibro, so they are "mapped" but not "detectable"). The Supplementary (S2 header, L7) already clarifies "33/35 … resolvable; 35 hubs = full set". So 17/35 is *defensible* (17 of the full 35-hub set localise to dorsal horn), but the adjacent "33/35 detectable" invites a reader to read "17/33 dorsal horn."
【Why it matters】 Low risk, but the honest-null/localisation framing is a selling point; denominators should be unambiguous.
【Specific fix】 In L51 write "17/35 hubs (of the 33 detectably expressed, i.e. 17/33 = 51.5%) mapped to the dorsal horn" so the two denominators are explicit, matching the S2 clarification.

### D7 (coherence note, not a contradiction) — ATF3 counted in DRG "20/25" yet flagged ambient elsewhere
【Problem】 ATF3 is included in the 20/25 DRG injured-neuron localisation (its `top_finetype` = Injured_RegenNeuron, detected True) while the manuscript separately flags ATF3's *spinal* assignment as ambient-downgraded (L46, L51).
【Evidence】 `P5_GSE216039_DRG_hub_finetype_top.csv` ATF3 row: top_finetype Injured_RegenNeuron, detected True → counts toward 20/25. `P5_hub_lineage_consensus.csv` ATF3: NotLocalisable (confident False). These are different tissues (DRG neuron subtype vs spinal lineage consensus), so there is no arithmetic contradiction, but a reader could conflate "ATF3 localises to injured neuron" (DRG) with "ATF3 not localisable" (spinal).
【Why it matters】 Prevents a reviewer/reader from inferring an internal contradiction where none exists.
【Specific fix】 Add one sentence in L44 clarifying the 20/25 is DRG-neuron-subtype localisation and is independent of the spinal lineage-consensus calls in L46.

---

## § Stands up (verified, with evidence)

1. **Core meta-signature is exactly reproducible.** `META_DRG_axis_CORE_signature.csv` contains precisely 4,055 genes all satisfying meta_FDR<0.05 & consistency≥0.8; `META_DRG_axis_stouffer.csv` contains exactly 16,552 tested genes and 6,869 at meta_FDR<0.05 (L31). The ATF3 positive control (meta_Z 10.53, FDR 1.0e-21, consistency 1.00) recomputes exactly — strong internal validation.
2. **Gene-set programme numbers are exact.** All four a priori sets in `P3_geneset_stats.csv` match to the stated decimals (neuroinflammation +4.94/100% up; DAM +3.88/93.8% up; complement +3.44/94.4% up; OXPHOS −2.37/73.7% down). The permutation p-values (0.0005 / 0.004) and the ion-channel non-coordination (Nav_SCN perm p = 0.180) also check out.
3. **The honest docking null is fully anchored.** ADRA2A full-library AUC 0.532, raw p 0.118, MW-adjusted 0.578 (D9); the multivariate LR p-values (AXL 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4, ADRA2A 0.027, MAPK14 0.066) and the S4 BH-q table all recompute exactly from `P6_multivariate_physchem_control.csv` and `P6_BH_correction.csv`. The knowledge-informed ranking precision@10 = 0.700 (lift ×18.69, p 9.4e-9) and precision@20 = 0.450 (p 1.3e-8) match `P6_mw_ranking_summary.csv`. The negative conclusion is therefore reproducible end-to-end.
4. **Hub convergence and cross-modal counts are exact.** 32/35 in meta core (D4), LODO GSE267799 0.917 [0.729, 1.000] (D5), 7/35 confident spinal lineage (D7), 20/25 DRG injured-neuron localisation and 17/35 Visium dorsal horn (D6/D8) all recompute exactly from their CSVs.

---

## § Questions for the authors

1. **Citations.** Will you insert refs 11 (Suzetrigine) and 12 (Nav1.7/SCN9A blocker) at L53–56 where you discuss analgesics-not-enriched and Nav-blocking strategies-not-addressed, and ref 5 at L64? Or are these three references genuinely unused and slated for deletion? (D1)
2. **SPRR1A metric.** Do you agree the body L44 "17.4×" is the mean-expression ratio and not the 5.84× detection ratio, and will you relabel it as proposed (D2)? Should the other three "×" values (ECEL1/NPY/FLNC) carry the same "mean-expression fold" qualifier throughout?
3. **Tier-1 AUC provenance.** Where is the 0.618 ADRA2A Tier-1 AUC computed, and can you add the backing CSV to `results/tables/` so it is recomputable (D4)? Is the 620-drug CNS/analgesic subset definition (n_t1=620 in `P6_breadth_target_summary.csv`) the exact subset that produced 0.618?
4. **"253" unit.** Confirm that 253 denotes high-confidence hub→miRNA *pairs* detectable in plasma (over 33 of 35 hubs), and not 253 hubs; will you reword L41/Methods accordingly (D3)?
5. **Human-layer denominator.** The human miRNA layer is honestly negative (perm_p = 0.51). Given only 33/35 hubs have any predicted targeting miRNA and the set-level test permutes 253 pairs, is the "33/35 hubs had predicted targeting miRNAs (608 high-confidence)" count (608) also derivable from a CSV we can recompute, or is it narrative-only?
6. **SCN range.** Accept the −3.6 to −3.2 rewording (D5), or do you intend a different rounding convention?

---

## § Recap of mandated checks (items 1–14)

- **1. Core 4,055 / tested 16,552 / 6,869 FDR<0.05** — ✅ exact (CSV).
- **2. Geneset stats** — ✅ exact (CSV).
- **3. SCN9A/10A/11A** — meta_Z FDR exact; range wording −3.6…−3.1 → should be −3.56…−3.15 (D5).
- **4. 32/35 in meta core** — ✅ exact (CSV).
- **5. LODO GSE267799 0.917 [0.729,1.000]** — ✅ exact (CSV).
- **6. DRG 20/25; SPRR1A 98.1/16.8 detection; "×" values** — counts ✅; **17.4× is expression ratio, detection ratio is 5.84×** (D2, critical).
- **7. 7/35 confident** — ✅ exact (CSV).
- **8. Visium 33/35 detectable; 17/35 dorsal horn** — ✅ counts; denominator framing flagged (D6).
- **9. ADRA2A 0.532 / p 0.118 / MW-adj 0.578** — ✅ exact (CSV).
- **10. precision@10 0.700 / lift ×18.69 / p 9.4e-9; precision@20 0.450 / p 1.3e-8** — ✅ exact (CSV).
- **11. Multivariate LR p + BH q** — ✅ exact (CSV).
- **12. Human perm p = 0.51; 253** — p ✅; "253" = pairs not hubs (D3).
- **13. Reference completeness** — ❌ orphans {5, 11, 12} (D1).
- **14. Abstract vs body** — ADRA2A 0.618→0.532 p=0.118, SCN FDR 1.7e-3–5.9e-3, human p=0.51 all agree between Abstract (L14) and body; but Tier-1 0.618 unanchored to a CSV (D4).

**Net:** 11 of 14 checks are fully reproducible; 1 (SCN range) is a rounding/wording slip; 2 (D2 metric ambiguity, D4 Tier-1 provenance) are substantive; and 1 cross-cutting citation failure (D1) must be fixed. The docking "honest null" and the meta/ML backbone are solid and reproducible — the corrections are about labelling precision, citation hygiene, and one missing provenance CSV, not about the scientific conclusion.
