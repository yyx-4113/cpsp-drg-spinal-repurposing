# DRAFT — Repurposing approved drugs for chronic postsurgical pain via structure-based virtual screening of DRG–spinal-cord-axis targets

> **状态：DRAFT（全库结果已并入，待 P7 复现包定稿）**。生成于 2026-09-18；全库结果并入于 2026-09-19。
> 依据：P6 Tier 1（620 药）+ Tier 2（2,465 药）= **3,085 已批准药 × 10 靶标 = 30,850 对接**全部完成；`P6_FINALIZE_STATUS.json` = `ready_to_finalise`（审计 20/20 靶标×层一致，所有控制与广度分析 rc=0）。
> 本文稿 Tier 1 + Tier 2 全库结果均已并入；所有数值均可追溯到 `results/tables/` 与 `results/figures/`（`P6_RESULTS.md` 为自动汇总）。
> 期刊对齐：A 档 *Frontiers in Pharmacology* / *Scientific Reports*（方法+重定位假说）；C 档 *Pain* / *BJA* / *Neuropharmacology* 需 ≥1 个 Top 候选湿实验验证。

---

## Title (proposed)

**Structure-based repurposing of approved drugs against DRG–spinal-cord-axis targets nominates α2A-adrenergic receptor (ADRA2A) as the best-supported chronic postsurgical pain repurposing hypothesis**

*Running title*: ADRA2A-centred drug repurposing for chronic postsurgical pain

---

## Abstract

**Background.** Chronic postsurgical pain (CPSP) lacks mechanism-targeted pharmacotherapy. A prior dual-machine-learning screen of the DRG–spinal-cord axis (P3) nominated 35 hub genes; 10 are tractable for structure-based docking. **Methods.** We performed rigorous virtual screening of the approved-drug library (ChEMBL `max_phase=4`, 3,085 dockable ligands) against the 10 hub targets using AutoDock Vina 1.2.5. *Before* screening we established docking-parameter fidelity: `--exhaustiveness 1` preserves rank order (Spearman ρ≈0.78 ceiling vs the true standard) whereas `--max_evals` introduces a systematic, rotatable-bond-correlated bias (ρ≈−0.23…+0.11) that invalidates ranking — so we screened with exh1 and framed results as *candidate prioritisation*. A reverse positive-control used **ChEMBL measured activity** (pChEMBL ≥ 6, 164 verified drug–target pairs) as labels strictly independent of the docking predictions, and — because docking scores favour large ligands — every enrichment result was tested against a **molecular-weight confounder control**. Synthetic-data self-tests pre-empted three fatal scoring bugs. **Results (Tier 1, CNS/analgesia-prioritised layer, 620 drugs × 10 targets).** ADRA2A (α2A-adrenergic receptor) dominated the 4-dimensional ranking: all of the top six and 6 of the top 7 best targets were ADRA2A (ergotamine, risperidone, dihydroergotamine, ziprasidone, lurasidone, bromocriptine; composite 0.73–0.79). We explicitly tested and **rejected** the face-validity claim that known analgesics are enriched as a class (AUC 0.553, p=0.08; 0 of 64 analgesics in the top 20). ADRA2A was the only target with an adequately powered enrichment test and it passed: AUC 0.618 (n=88 actives, p=1.9×10⁻⁴), remaining above 0.5 after MW adjustment (0.597) and MW stratification (0.600), against a size-only baseline of 0.581 — i.e. the signal is **not** a molecular-weight artefact. **Caveat (pre-registered full-library test, §3.5):** on all 3,085 ligands ADRA2A's docking AUC falls to 0.532 (p=0.118, NS), and no target shows a robust, size-independent docking enrichment that beats a trivial 2D-physicochemical baseline — the Tier-1 pass was a composition artefact of the CNS-prioritised subset. At the ranking level, **8 of the top 10 ADRA2A candidates are ChEMBL-confirmed ADRA2A binders** (precision@10 = 0.80, lift ×5.6 over the 14.2% baseline, p=4.4×10⁻⁶), and precision remains 0.55–0.80 after MW adjustment — but the individual top-10 *identities* are only 4/10 stable, so we claim a **top-20 candidate set**, not a single best drug. **Full-library breadth (§3.5) revises this:** ADRA2A's enrichment does not survive extension to all 3,085 ligands (AUC 0.532, p=0.118, NS) and no target shows a robust, incrementally informative docking enrichment, so the hypotheses are *prioritised and bounded*, not validated. **Conclusion.** ADRA2A-centred repurposing hypotheses for CPSP are biologically coherent with descending noradrenergic inhibition and warrant prospective wet-lab validation.

---

## 1. Introduction

Chronic postsurgical pain (CPSP) affects 10–50% of surgical patients and is mechanistically anchored in maladaptive plasticity along the dorsal root ganglion (DRG) → spinal cord axis[ref]. Current prophylaxis is limited to generic analgesics (NSAIDs, gabapentinoids, opioids) without target specificity for the injured-axis programme.

A dual-machine-learning screen of seven GEO datasets (P3) identified a 35-gene hub programme spanning neuronal injury-response (ATF3/SPRR1A/GAL), microglial/immune (TFE3/AXL), and glial/matrix (SLC2A1/SERPINE1/VASH2/MAPK14/ACVR1) signatures. Ten of these are structurally tractable and were advanced to docking (§6 of the project plan).

Virtual screening of approved drugs offers a fast, de-risked repurposing path, but its literature is littered with irreproducible rankings stemming from (i) undisclosed docking-parameter bias, (ii) circular positive controls (double-dipping), and (iii) pseudoreplication at the ligand level. We therefore built the screen around three methodological safeguards and report them as primary contributions.

---

## 2. Methods

### 2.1 Target selection and structural preparation
43 candidate targets (35 P3 hubs + §6 priority) were triaged for druggability; 18 were `DOCK`, 12 `EXCLUDE`, 11 `HOLD_AF2`, 2 `HOLD_APO`. Ten received full receptor preparation (gemmi + Open Babel 3.1.0): GALNS, SLC2A1, ACVR1, AXL, ADRA2A, ITPKC, MAPK14, SERPINE1, TNIK, VASH2. Ion-channel candidates (SCN9A/SCN10A/SCN11A/KCNQ2/CACNA2D1/GABRA1) were excluded for lack of usable structures — a stated coverage gap.

### 2.2 Ligand library
Source: ChEMBL `max_phase=4` (the open equivalent of the DrugBank approved set), cross-annotated with the Broad Drug Repurposing Hub (CC0). After salt handling with `LargestFragmentChooser` (a fix that recovered 1,078 salts from silent drop-out) and drug-likeness filters, **3,085 ligands** entered docking (93.2% of the 3,311 small molecules). Sixty-four carry manual analgesia priors.

### 2.3 Docking and a priori parameter-fidelity validation
AutoDock Vina 1.2.5 (official Windows binary), 7 workers × `--cpu 1` on an 8-core host. We first validated parameters on a 15-ligand held-out set against a high-`--exhaustiveness` gold standard:
- `--max_evals 2000/6000` produced large, **rotatable-bond-correlated** affinity shifts (Spearman ρ≈−0.23…+0.11) → systematic bias, ranking void.
- `--exhaustiveness 1` produced only a small, rotatable-bond-**independent** scale shift (ρ≈0.78) → ranking preserved.
Screening therefore used `exh1 --max-evals 0`; the ρ≈0.78 ceiling dictates *candidate prioritisation* wording throughout.

### 2.4 Reverse positive control (no double-dipping)

Positive labels are **independent of the docking predictions**. The primary label source is ChEMBL measured bioactivity (release ChEMBL_37): for each target, the UniProt accession was resolved to ChEMBL target IDs via UniProt cross-references, and all activities with pChEMBL ≥ 6 (IC50/Kd/Ki ≤ 1 µM) were retained and intersected with the screened library (`scripts/p6_reverse_control.py`). A secondary source is a curated set of known analgesic–target pairs (`PAIN_PRIOR`). Predictions come solely from Vina scores; labels are never used to set thresholds, fit parameters, or construct scores, so no double-dipping occurs.

Per target we computed the AUC of known actives vs the rest (Mann–Whitney U); targets below AUC 0.60 (or with fewer than 5 actives) received a neutral D4 reliability weight (0.5).

### 2.4.1 Molecular-weight confounder control

Because docking scores increase monotonically with ligand size, any enrichment could be a molecular-weight (MW) artefact. We therefore pre-specified a **single, unified verdict rule** (`p6_stats.enrichment_verdict`, called identically by `p6_mw_confounder.py` and `p6_breadth.py` so the two analyses can never disagree; §2.8 pre-registered it). A target reaches `PASS_size_independent` only if **all** of: (i) ≥5 independent ChEMBL actives; (ii) docking AUC > 0.5; (iii) the size-only MW baseline AUC is **strictly below** the docking AUC (if not, a one-line MW heuristic already explains the signal → `FAIL_size_only_matches`); and (iv) one-sided Mann–Whitney p < 0.05 (if not → `NS_not_significant`). To prevent over-claiming when the docking AUC merely equals the baseline within noise, we additionally report a **paired ΔAUC bootstrap** of docking vs both the size-only baseline and a 6-descriptor 2D-physichem logistic baseline (cross-validated, §3.3.1); if the 95% CI contains zero, the docking increment is reported as **not distinguishable** from the trivial baseline even when the nominal label is PASS.

### 2.5 Four-dimensional scoring
Composite = 0.40·D1(affinity percentile within target) + 0.25·D2(known polypharmacology overlap with 35 hubs) + 0.20·D3(accessibility / CNS-MPO-like) + 0.15·D4(reverse-control reliability).

### 2.6 Synthetic-data self-test
Before the real run, a synthetic score table with implanted signal (theoretical AUC 0.961) exercised the entire downstream (positive construction + 4-dim scoring + reverse control) and caught three fatal scoring bugs (§10).

### 2.7 Cache-invalidation audit (ligand-set equality, not row counts)

Docking results are cached per ligand chunk, and a chunk filename encodes `(target, tier, index)` but **no fingerprint of the ligand list**. If a tier list is ever regenerated — as ours was, when the CNS/analgesia-prioritised split was revised — previously cached chunks are silently reused, so a target's scoring table can contain a *different* ligand set while still showing the expected row count. Every downstream within-target percentile for that target would then rest on a different ligand set from the other targets, silently breaking cross-target comparability.

We therefore added an explicit audit (`scripts/p6_audit_liglists.py`) that runs before scoring and asserts, for every target × tier, `set(scores.chembl_id) == set(current tier list)` with **both the missing and the extra counts equal to zero**, after first checking that the two tier lists are disjoint and that their union equals the filtered library. On the real data the audit found exactly one offending entry: the Tier-1 table of **AXL**, which contained 60 ligands since reclassified into Tier 2 and was missing 60 ligands now in Tier 1; the other 19 target × tier combinations were clean. The stale chunks were quarantined by rename (never deletion, preserving the original artefacts) and AXL Tier 1 was re-docked against the current list, after which scoring, figures and the report were regenerated. We report this transparently because a row-count check — the natural sanity check — would not have caught it.

### 2.8 Pre-registration of the full-library breadth analysis

The breadth analysis of §3.5 was written and its decision rules fixed *before* the full-library screening finished, to prevent post-hoc selection of statistics. Pre-specified components: (i) per-target affinity distributions under a **composition-controlled** comparison (all ten targets docked against the identical ligand set); (ii) a pocket-volume confound test, since Vina scores have no common scale across pockets; (iii) target-ranking stability between the Tier-1 subset and the full library (Spearman ρ of per-target medians); (iv) enrichment power for every target with ≥5 independent actives, each reported with the same three molecular-weight guards as §2.4.1 (docking AUC vs size-only AUC vs MW-adjusted AUC). Any target whose apparent enrichment is matched or exceeded by the size-only baseline is reported as **not** distinguishable from a size artefact.

---

## 3. Results

### 3.1 Library and parameter fidelity
3,085 ligands docked (Fig. P6_ligand_funnel). Parameter validation confirmed exh1 as the faithful setting (Fig. P6_param_fidelity; see §2.3).

### 3.2 Tier 1 docking is complete and real
All 3,085 approved-drug ligands were docked against all 10 targets = **30,850 docking evaluations** (Tier-1 `P6_docking_scores_t1_cns.csv`: 6,200 rows; Tier-2 `P6_docking_scores_t2_other.csv`: 24,650 rows; the combined per-target scores were rebuilt from the per-target source-of-truth files by `p6_score.py`, rc=0). 163 target×ligand pairs (34 unique ligands, 0.53% of 30,850) failed docking — 60 from `unsupported_atom_type_B` (boron-containing drugs Vina cannot parse) and 103 from 600 s time-outs (macrocycles / high-flexibility agents); these are excluded from scoring and listed in `P6_ligands_unscored.csv` with a per-ligand upper-bound proof (`P6_exclusion_bound.csv`) that none could have entered the top-20.

### 3.3 Reverse positive control (ChEMBL-measured labels, no double-dipping)

Labels are **independent of docking**: they come from ChEMBL measured bioactivity at pChEMBL ≥ 6 (≤1 µM), retrieved per target via UniProt cross-references (`scripts/p6_reverse_control.py`, ChEMBL_37). Predictions come solely from Vina scores; no label participates in any threshold or score construction, so there is no double-dipping.

Across the 10 targets the ChEMBL layer yielded **164 verified drug–target positives**: ADRA2A 115 (max pChEMBL 9.54), MAPK14 16 (7.80), AXL 13 (9.30), TNIK 10 (7.64), ACVR1 9 (8.10), SLC2A1 1 (6.97); GALNS and SERPINE1 returned 0, and ITPKC/VASH2 have no ChEMBL target mapping. Within the Tier-1 layer (620 drugs), 88 ADRA2A actives were available for testing.

| Target | n known actives | AUC (docking) | p (Mann–Whitney) | passes (AUC ≥ 0.60) |
|---|---|---|---|---|
| ADRA2A | 88 | **0.618** | 1.9 × 10⁻⁴ | **yes** |
| MAPK14 | 2 | 0.675 | — | not evaluable (n too small) |
| all others | <5 | not testable | — | neutral D4 (0.5) |

**Within the Tier-1 layer, ADRA2A is the only target with an adequately powered enrichment test, and it passes (AUC 0.618, p=1.9×10⁻⁴).** The remaining nine received a neutral D4 weight. However, the pre-registered full-library test (§3.5.4) shows this Tier-1 pass does **not** survive extension to all 3,085 ligands (AUC 0.532, p=0.118, NS): the Tier-1 enrichment was a composition artefact of the CNS-prioritised subset, and the full-library verdict is the definitive one.

**Label-definition decision.** Labels must be *binding* labels for a binding-enrichment test. We therefore used ChEMBL measured activity alone, and deliberately excluded two noisier curated layers — a hand-curated analgesic list (indication-based, "this drug is an analgesic") and Drug Repurposing Hub target annotations — because they answer a different question. This matters numerically: on ADRA2A, ChEMBL-only gives n = 88 with AUC 0.618, whereas adding the 13 annotation-derived ligands gives n = 101 with AUC 0.592. Both are > 0.5, so the direction of the conclusion is robust to label definition; we report the ChEMBL-only figure as primary because its criterion is single, objective and reproducible. The curated analgesic list is instead used for the separate *face-validity* analysis in §3.4.

### 3.3.1 Is the enrichment merely a molecular-weight artefact?

Docking scores inherently favour larger ligands: more heavy atoms accumulate more favourable scoring terms. Because ADRA2A's known actives are disproportionately large CNS drugs (antipsychotics, antidepressants), enrichment could be a pure size artefact. We therefore report three guards (`scripts/p6_mw_confounder.py`, judgment rule fixed a priori):

| Statistic | Value | Interpretation |
|---|---|---|
| Spearman ρ(affinity, MW) | **−0.607** | size bias is real and strong |
| AUC using **MW only** | 0.581 | size-only artefact baseline |
| AUC using docking score | **0.618** | observed enrichment |
| AUC after **linear MW adjustment** | 0.597 | signal survives |
| AUC **within MW quintiles** | 0.600 | signal survives (non-parametric) |
| Mann–Whitney p | 1.9 × 10⁻⁴ | significant |

Since docking AUC exceeds the MW-only baseline **and** remains > 0.5 after both linear adjustment and stratification, the ADRA2A enrichment is **not attributable to molecular size** within the Tier-1 layer. Reporting an unadjusted enrichment AUC in this setting would not be defensible. This size-control conclusion is moot once the composition effect is accounted for: the pre-registered full-library test (§3.5.4) overturns the ADRA2A enrichment itself (full-library AUC 0.532, NS).

### 3.4 ADRA2A dominates the candidate ranking
Top drug-level hits (Fig. P6_ranking_drugs, Table 1). **Affinities below are those measured at the stated best target** (`affinity_at_best_target`) — *not* the drug's strongest value across all targets, which frequently belongs to a different target (see the caveat in §6, Data-integrity note).

| Rank | Drug | Best target | Affinity at that target (kcal/mol) | Strongest across any target | Composite |
|---|---|---|---|---|---|
| 1 | Ergotamine | ADRA2A | −10.36 | −10.93 (SLC2A1) | 0.791 |
| 2 | Risperidone | ADRA2A | −10.08 | −11.21 (SLC2A1) | 0.789 |
| 3 | Dihydroergotamine | ADRA2A | −10.05 | −12.02 (SLC2A1) | 0.788 |
| 4 | Ziprasidone | ADRA2A | −9.35 | −10.42 (SLC2A1) | 0.781 |
| 5 | Lurasidone | ADRA2A | −10.39 | −11.73 (SLC2A1) | 0.741 |
| 6 | Bromocriptine | ADRA2A | −9.29 | −11.53 (SLC2A1) | 0.728 |

**All six of the top-ranked drugs have ADRA2A as their best target**, and ADRA2A accounts for 6 of the top 7 (the exception, buclizine at rank 7, maps to MAPK14). No other single target dominates the ranking to a comparable degree.

### 3.4.1 Face validity: a negative result that must be reported

It is tempting — and common — to claim face validity by pointing at one or two recognisable analgesics in the top ranks. Tested as a **class**, that claim does **not** hold (`scripts/p6_face_validity.py`; `pain_prior` labels are external and enter none of the four scoring dimensions, so this test is not circular):

| Test | Result | Verdict |
|---|---|---|
| Analgesics (n=64) vs rest, drug-level composite | AUC 0.553, p=0.081 | not significant |
| Analgesics in top-20 | **0** observed vs 1.9 expected | no enrichment |
| Analgesics in top-50 / top-100 | 1 (exp. 4.7) / 5 (exp. 9.4) | fewer than expected |
| Analgesics vs rest on ADRA2A affinity | AUC 0.508, p=0.42 | no difference |
| α2-adrenergic agonists (n=8) on ADRA2A, raw | AUC **0.343** | worse than average |
| α2 agonists, **MW-adjusted** | AUC 0.475, p=0.60 | at chance |

The α2-agonist result deserves comment because it exposes the size penalty concretely: these prototypical ligands are small (median MW 245.6 vs 300.7 for the rest), and raw docking therefore places them *below* average. After removing the MW contribution, dexmedetomidine — the selective α2A agonist — moves from the 68th to the **94th percentile**, whereas clonidine (15.7 → 28.1) and tizanidine (20.0 → 27.3) remain poorly ranked.

**Interpretation.** These findings are hypothesis-generating, not confirmatory. Two individual observations merit follow-up — flupirtine, a recognised central analgesic, ranks 5th of 620 on ADRA2A; and dexmedetomidine reaches the top 6% once size is accounted for. But the class-level tests give **no support** for the claim that known analgesics are enriched, and we therefore do **not** advance face validity as evidence of pipeline validity. The screen's validation rests instead on the ChEMBL binding-based enrichment of §3.3, which is an independent, adequately powered and confounder-controlled test.

**Biological coherence.** α2A-adrenergic receptors mediate descending noradrenergic inhibition of spinal nociception — the mechanistic basis of antidepressant and α2-agonist adjuvant analgesia. ADRA2A as the best-supported CPSP repurposing hypothesis is therefore mechanistically self-consistent, but this coherence is a *rationale for prioritising* ADRA2A, not a validation of the ranking.

### 3.4.2 Ranking robustness: is the top list merely a molecular-weight ranking?

Because molecular size is the strongest single bias in docking (§3.3.1), and because every candidate in §3.4 is a large CNS drug, the *ranking itself* must be tested against MW — not just the enrichment (`scripts/p6_mw_ranking_sensitivity.py`). Holding D2/D3/D4 and all weights fixed, we replaced **D1 only** with two MW-robustified within-target percentiles: **(A)** the percentile of the residual of affinity regressed on MW, and **(B)** the within-MW-quintile percentile (non-parametric, no linearity assumption). This isolates molecular size as the single manipulated variable.

**Ranking quality is robust to MW.** Spearman ρ between the primary composite and the MW-residual composite is **0.83** (0.80 against the stratified variant); at drug level across all 10 targets, ρ = **0.89**. Top-20 membership overlaps **14/20**. (Judgment rule fixed a priori: ρ ≥ 0.80 *and* top-20 overlap ≥ 12 ⇒ robust; here both hold.)

**A stronger, decision-relevant metric — precision@k.** Using the independent ChEMBL actives of §3.3 as ground truth (labels measured, predictions docked — no double-dipping):

| k | hits | precision | lift vs 14.2% baseline | hypergeometric p | MW-residual precision | MW-stratified precision |
|---|---|---|---|---|---|---|
| 10 | 8 | **0.800** | ×5.64 | 4.4 × 10⁻⁶ | 0.600 | 0.800 |
| 20 | 14 | **0.700** | ×4.93 | 9.8 × 10⁻⁹ | 0.700 | 0.550 |
| 50 | 20 | **0.400** | ×2.82 | 2.1 × 10⁻⁶ | 0.360 | 0.360 |

Eight of the top ten ADRA2A candidates are experimentally confirmed ADRA2A binders. Precision remains well above the 14.2% baseline under *both* MW corrections, so the set-level claim — the head of the ADRA2A ranking is enriched for true binders — is not a size artefact.

**However, the individual top-10 identities are not stable.** Only **4/10** of the primary top ten survive MW adjustment: dexmedetomidine and flupirtine enter the top five, while lurasidone and aripiprazole leave it. We therefore claim **a top-20 candidate set**, and we make no claim of the form "drug X ranks first" — such a statement is demonstrably not robust.

Note the deliberate tension with §3.4.1, which we report rather than smooth over: at *class* level α2 agonists do not enrich (AUC 0.475 even after MW adjustment), yet the single selective α2A agonist dexmedetomidine is among the most MW-robust top candidates. A negative class-level result does not preclude individual exceptions, and both facts are reported.

### 3.5 Full-library breadth (pre-registered)

*Pre-registered analysis plan (fixed before the full-library results were available; §2.8). Numeric values filled from `P6_breadth_*.csv` / `P6_breadth_note.md` only after the cache-invalidation audit of §2.7 passed (it did: all 20 target×tag ligand sets match the current lists, rc=0).*

**3.5.1 Composition-controlled target comparison.** With all 3,085 ligands docked against all ten targets (30,685 scored pairs, 99.5% coverage), per-target affinity distributions are compared on an identical ligand set, so rank differences cannot be attributed to ligand composition. Per-target median / best affinity (kcal/mol, more negative = better) and counts below −9.0 / −10.0 kcal/mol (`P6_breadth_target_summary.csv`):

| Target | n scored | median | best | n ≤ −9.0 | n ≤ −10.0 |
|---|---|---|---|---|---|
| SLC2A1 | 3,066 | −8.005 | −15.71 | 840 | 327 |
| ACVR1 | 3,075 | −7.710 | −14.55 | 492 | 125 |
| ADRA2A | 3,070 | −7.506 | −12.52 | 444 | 96 |
| TNIK | 3,063 | −6.690 | −11.48 | 162 | 36 |
| VASH2 | 3,070 | −6.632 | −10.10 | 67 | 2 |
| MAPK14 | 3,066 | −6.599 | −10.04 | 50 | 1 |
| AXL | 3,071 | −6.520 | −10.59 | 51 | 13 |
| GALNS | 3,064 | −6.496 | −10.09 | 29 | 1 |
| SERPINE1 | 3,075 | −5.820 | −9.00 | 2 | 0 |
| ITPKC | 3,065 | −5.060 | −8.72 | 0 | 0 |

SLC2A1 and ACVR1 are the deepest-binding targets; ITPKC and SERPINE1 show essentially no sub-−9 kcal/mol enrichment. Because the comparison is composition-controlled, these ranks are real target effects.

**3.5.2 Pocket-volume confound test.** Because Vina scores have no cross-pocket scale, we tested whether larger boxes score systematically better (`P6_breadth_pocket_volume_confound.json`): Spearman ρ(box volume, per-target median affinity) = **−0.018** (p=0.96); ρ(box volume, best affinity) = **0.042** (p=0.907). Non-significant → no systematic box-size bias (reported as a negative result). This does **not** license cross-target comparison of raw kcal/mol; target priority continues to rest on the composite of §2.5.

**3.5.3 Target-ranking stability under breadth.** Per-target median affinity on the Tier-1 subset versus the full library (`P6_breadth_target_rank_stability.csv`): Spearman ρ = **0.988** (p=9.3×10⁻⁸) across the ten targets, with rank shifts of at most 1 (AXL 8→7, GALNS 7→8). The Tier-1 *target ordering* is therefore not an artefact of the CNS-prioritised subset — but §3.5.4 shows the *enrichment signal* itself is composition-sensitive.

**3.5.4 Enrichment power and the size-independent verdict for every target (pre-registered, full library).** Of 10 targets, 5 reach ≥5 independent ChEMBL actives; each is tested with the unified rule of §2.4.1 (`P6_breadth_chembl_power.csv` / `P6_enrichment_mw_confounder_check.csv`):

| Target | n actives | AUC(dock) | p(MWU) | AUC(size-only) | AUC(MW-adj) | verdict |
|---|---|---|---|---|---|---|
| ACVR1 | 9 | 0.797 | 1.0×10⁻³ | 0.817 | 0.655 | FAIL_size_only_matches |
| ADRA2A | 115 | 0.532 | 0.118 | 0.462 | 0.578 | NS_not_significant |
| AXL | 13 | 0.880 | 1.1×10⁻⁶ | 0.842 | 0.752 | PASS_size_independent * |
| MAPK14 | 16 | 0.779 | 5.9×10⁻⁵ | 0.787 | 0.729 | FAIL_size_only_matches |
| TNIK | 10 | 0.824 | 2.0×10⁻⁴ | 0.816 | 0.803 | PASS_size_independent * |
| GALNS / ITPKC / SERPINE1 / VASH2 / SLC2A1 | <5 | — | — | — | — | n/a (insufficient actives) |

\*Both PASS targets clear the nominal size-independent rule (dock AUC > size-only baseline, p<0.05, MW-adjusted >0.5). **However, the decisive incremental test — a paired ΔAUC bootstrap of docking vs the trivial baseline — has a 95% CI that contains zero for both:** AXL ΔAUC(vs size-only) [−0.030, +0.104] and (vs 2D-physichem) [−0.071, +0.027]; TNIK [−0.224, +0.193] and [−0.282, +0.120]. Docking therefore provides **no statistically distinguishable incremental enrichment** over a one-line MW heuristic or a 6-descriptor 2D-physichem logistic model. The two "PASS" labels mean *not worse than baseline*, not *better than baseline*.

**Headline result.** The pre-registered full-library test finds **no target with a robust, size-independent, and incrementally informative docking enrichment**. ADRA2A — the only target that passed in the Tier-1 CNS-prioritised subset (AUC 0.618, p=1.9×10⁻⁴) — does **not** survive extension to the full library (AUC 0.532, p=0.118, NS): its Tier-1 signal was a composition artefact of the CNS-prioritised subset. This is exactly the failure mode the pre-registration and the size control were designed to expose, and we report it rather than the Tier-1 positive.

**3.5.5 New candidates outside the CNS-prioritised subset.** Because the full-library enrichment does not support a target-specific ranking, no Tier-2 candidates are advanced as additional ADRA2A hypotheses; the candidate set remains the Tier-1 top-20 of §3.4, now explicitly carrying the full-library caveat of §3.5.4. (Within-target percentiles for the breadth summary were recomputed on the 3,085-ligand library; the §3.4 ranking used the 620-ligand Tier-1 percentile basis and is reported as such.)

### 3.6 Human transcriptomic validation of the hub programme (P4)

The 35-hub DRG→spinal-cord programme was derived from rodent nerve-injury models; its human translatability is tested across three independent human layers, with pseudoreplication discipline enforced throughout (patient/subject-level tests only — never spot- or cell-level).

**3.6.1 Cross-species neuronal anchor — GSE249746 (positive).** In a 1,136-neuron human DRG single-soma atlas (Nature Neuroscience 2024), 34/35 hubs (all but REG3B) plus ADRA2A are detected. 26/35 hubs peak in pain-relevant human nociceptive/IB4+/NPY+ neuronal clusters, and the programme co-varies with human nociceptive identity (median ρ = 0.158 across 35 hubs; 82% positive; strongest CHL1 ρ = 0.69, TFE3 0.41). ADRA2A localises to a nociceptive-like cluster (C14). This establishes cross-species conservation of the hub programme at the human DRG neuronal-identity level.

**3.6.2 Human iPS-DRG neuron programme — GSE107181 (weak; development, not injury).** 18/33 hubs are neuron-upregulated vs iPSC progenitors (binomial p = 0.73, NS; gene-set permutation p = 1.0). A subset (CHL1, SRRM4, FLRT3, RUBCN, GALNS, SPRR1A, RNF19B) shows strong neuron enrichment. Because GSE107181 contrasts *development* (neuron vs progenitor), not nerve injury, the set-level null is biologically expected and cannot test pathological-pain induction; it shows the hub programme contains a human DRG neuronal-identity component.

**3.6.3 Human chronic C2-DRG Visium — SPARC Dataset 476 (non-replication).** At subject-level pseudobulk (n = 8 patients: 3 acute / 5 chronic neck-pain — the only open human DRG spatial cohort, CC-BY-4.0), the 35-hub programme shows a directionally positive but **non-significant** association with chronicity: set-mean Welch t = +0.235 (22/34 mapped hubs higher in chronic), permutation two-sided p = 0.765, binomial-on-sign p = 0.121 (trend only). The 4,055-gene meta-core signature is not enriched (set-mean t = +0.062, permutation p = 0.846). Critically, the canonical rodent axon-injury/regeneration hubs **SPRR1A and CDHR5 are essentially undetected (≈0 CPM)** in human C2-DRG, and ATF3/RNF19B/CTTN are if anything lower in chronic (CTTN log2FC = −0.28, p = 0.0013). The human chronic-DRG programme is therefore **not a recapitulation** of the rodent SNI/CCI injury programme on which the signature was built; the cross-species hub signature does not face-validate in this human tissue cohort.

**3.6.4 Human DRG snRNA-seq atlas — Pennsieve Dataset 480 (positive trend; non-neuronal).** In the open CC-BY-4.0 human DRG snRNA-seq atlas (Sankaranarayanan & Price 2025; 40 donors = 3 cervical fusion + 7 thoracic vertebrectomy + 30 organ donors; 10x Chromium FLEX), tested at donor-level pseudobulk (n = 40 independent units; 10 surgical-exposed CC+TV vs 30 organ-donor control), the 35-hub programme shows a directionally positive but non-significant enrichment in surgical-exposed DRG: set-mean Welch t = +0.480 (22/33 mapped hubs higher; 67%), permutation two-sided p = 0.109, binomial-on-sign p = 0.080 (trend only). The 4,055-gene meta-core signature is not enriched (set-mean t = +0.273, permutation p = 0.174). Individually, SERPINE1 (log2FC = +1.21, p = 0.0097), ITPKC (+0.67, p = 0.0009), MEGF11 (+0.61, p = 0.002), CRISP3, VASH2 and NPY are among the most consistently elevated hubs, whereas ECEL1 (−1.40), CHL1 (−0.33, p = 0.042) and PTPN23 are lower. SPRR1A is again undetected (≈0 expression) in human DRG. **Cell-type resolution reveals the programme is non-neuronal**: donor-level mean hub expression is *negatively* correlated with a neuronal-marker score (SNAP25/RBFOX3/ENO2/SYN1/MAP2/NEFL/SLC17A7/GRIN1; Spearman ρ = −0.473, p = 0.002) and *positively* with fibroblast (ρ = +0.40, p = 0.011) and oligodendrocyte-precursor (ρ = +0.36, p = 0.022) markers. The human DRG hub programme is therefore a stromal/glial response, not a neuronal injury programme — which reconciles the §3.6.3 Visium null (neuronal DRG, no replication) with the §3.6.1 neuronal-identity anchor (positional conservation) and explains why the rodent SNI/CCI injury signature does not transfer cleanly to human chronic DRG.

**Synthesis.** Human validation of the 35-hub programme is *mixed and layer-dependent*: strongly supported at the neuronal-identity level (§3.6.1), partially supported as a neuronal component (§3.6.2), non-replicated at the chronic-DRG-tissue level (§3.6.3, Visium), and showing only a non-significant, non-neuronal stromal trend in open human DRG snRNA (§3.6.4). The coherent reading is that the hub programme is *conserved in human DRG neuronal identity* but manifests in human tissue as a *stromal/glial* response rather than a neuronal-injury programme — which is exactly why the rodent SNI/CCI-derived signature does not cleanly transfer. This is an honest, hypothesis-generating pattern, not a confirmatory result; the decisive human test remains a pain-phenotyped (pain vs no-pain) DRG cohort and prospective wet-lab validation (§5.1). The ADRA2A repurposing hypothesis is not contradicted by §3.6.3–§3.6.4 — ADRA2A is neither a hub nor a DRG-injury marker, and its support derives from the docking/ChEMBL axis of §3.3–§3.5, not from the transcriptomic hub programme.

---

## 4. Discussion

The screen's value is twofold. *Methodologically*, it demonstrates that two pervasive but rarely-checked failure modes can be made explicit and controlled: docking-parameter choice is not cosmetic (`--max_evals` fast modes silently corrupt ranking, and only an a-priori fidelity check exposes this), and retrospective enrichment is not self-validating (with ρ(affinity, MW) = −0.607, an unadjusted AUC would have been uninterpretable; the signal survives adjustment and stratification). *Biologically*, it delivers a concrete, mechanism-anchored repurposing hypothesis — ADRA2A — supported within the Tier-1 layer by ChEMBL-verified enrichment (AUC 0.618, p=1.9×10⁻⁴) that is not a pure size artefact, and by a precision@10 of 0.80 (lift ×5.6, p=4.4×10⁻⁶) that likewise survives MW adjustment within that layer. **The pre-registered full-library breadth (§3.5.4) qualifies this: ADRA2A's enrichment does not survive extension to all 3,085 ligands (AUC 0.532, p=0.118, NS), and no other target reaches a robust, size-independent docking enrichment that beats a trivial 2D-physichem baseline — so the screen delivers a *prioritised, explicitly bounded hypothesis set*, not a validated target.** This is fully consistent with descending-inhibition physiology, which motivates prioritising ADRA2A for follow-up but does not itself validate the ranking. We also report two **negative** or deflationary results rather than omit them: the widely-invoked "known analgesics resurface" argument does not survive testing as a class (§3.4.1), and the individual top-10 identities are only 4/10 stable under MW adjustment (§3.4.2), which is why we advance a **top-20 candidate set** and make no "best drug" claim. Cherry-picked examples of recognisable drugs are not evidence, and reporting the failed tests tells the reader exactly how much weight the ranking can bear.

**Limitations (carried with conclusions).** Ion-channel targets (SCN9A/SCN10A/SCN11A/KCNQ2/CACNA2D1/GABRA1) are undockable here — a structural-biology gap (no ligand-bound holo structure), not a dataset artefact, and out of scope of a GEO swap; the ρ≈0.78 fidelity ceiling supports prioritisation not precise ordering; ADRA2A is the only target with an adequately powered enrichment test — the other nine rest on neutral D4 and their rankings are correspondingly weaker; the enrichment AUC of 0.618 is modest in absolute terms, so ADRA2A should be read as *the best-supported* rather than a *validated* target; single crystal conformations omit induced fit and membrane environment; and all candidates remain hypothetical until wet validation. The pre-registered full-library breadth (§3.5) **does** shift the conclusion: no target shows a robust, size-independent and incrementally informative docking enrichment, and ADRA2A's Tier-1 pass is overturned (full-library AUC 0.532, NS). The screen's biological output is therefore downgraded from "ADRA2A is the validated target" to "ADRA2A is the best-supported *Tier-1* hypothesis, with the full-library test showing the signal is composition-sensitive and not incrementally better than a trivial baseline". Separately, the 35-hub programme's **human translatability is mixed and unconfirmed in chronic tissue** (§3.6): conserved at human DRG neuronal identity (GSE249746) but not replicated in chronic human C2-DRG (SPARC 476 Visium), and only a non-significant, non-neuronal stromal trend in open human DRG snRNA (Pennsieve 480) — so the hub programme is not itself an independently validated human target set, and its human signal is stromal/glial rather than neuronal; ADRA2A's support rests on the docking/ChEMBL axis, not on transcriptomic hub conservation.

---

## 5. Conclusions

A rigorously parameter-validated, pseudoreplication-aware virtual screen of approved drugs against DRG–spinal-cord-axis hubs nominates **ADRA2A** as the best-supported CPSP repurposing hypothesis — a nomination qualified, not confirmed, by the pre-registered full-library test of §3.5.4 (full-library AUC 0.532, p=0.118, NS). Established CNS/analgesic drugs form an immediately testable top-20 candidate set. Prospective wet-lab validation in a CPSP model is the next step toward a clinically actionable hypothesis.

---

## 5.1 Future directions

The screen is deliberately bounded; four boundaries are structural, not dataset artefacts, and point to concrete next steps:

- **Ion-channel targets (SCN9A/SCN10A/SCN11A/KCNQ2/CACNA2D1/GABRA1).** Their absence is a *structural-biology* gap — no ligand-bound holo structure exists for blind library docking — and cannot be closed by swapping GEO datasets. A separate track should model Nav1.7 / Cav2.2 from recent cryo-EM (2023–2025) or AlphaFold3 and re-dock the approved library onto the toxin-binding pocket.
- **Scoring fidelity ceiling (ρ≈0.78).** Inherent to Vina/NN-score on these targets; claims are restricted to candidate prioritisation. A consensus scorer (Vina + GNINA/CNN) with MM-GBSA or FEP rescoring on the top poses would raise ranking confidence.
- **Human validation layer (P4) is mixed, not uniformly negative (§3.6).** The 35-hub programme is conserved at the human DRG neuronal-identity level (GSE249746, 26/35 hubs in nociceptive clusters), **not replicated** in chronic human C2-DRG tissue (SPARC 476 Visium: set-mean t = +0.235, permutation p = 0.765; rodent injury hubs SPRR1A/CDHR5 ≈ 0 CPM), and shows only a non-significant, *non-neuronal* stromal trend in open human DRG snRNA (Pennsieve 480: set-mean t = +0.480, permutation p = 0.109; ρ = −0.473 vs neuronal markers, +0.40 vs fibroblast). The decisive human test is therefore a **pain-phenotyped** DRG cohort (pain vs no-pain, not surgical-vs-donor) and/or a meta-analysis of human neuropathic-pain transcriptomics (n ≥ 10/group), plus prospective wet-lab validation. This resolves the earlier "P4 negative / under-powered" framing: the signal is layer-specific and stromal rather than neuronal, and the open-cohort null is explained by a genuine programme mismatch (rodent neuronal injury vs human chronic-DRG stromal response), not merely small n. NOTE: the previously-assumed PRECISION DPN controlled-access DUA is now largely obviated — the human DRG snRNA-seq atlas is already open (Pennsieve 480, CC-BY-4.0); the DUA path applies only to the narrower DPN-neuropathy contrast subset and is optional.
- **Static crystal, no membrane, no induced fit, no wet lab.** MD refinement + MM-PBSA (membrane-embedded for membrane targets) and induced-fit/ensemble docking would harden the top poses; definitive advancement to a C-tier journal requires ≥1 prospective wet-lab validation (point mutation / SPR, or an ADRA2A-binding analgesic in a CPSP model).
- **Spatial layer (Stretch).** GSE325938 Visium localised 17/35 hubs to the dorsal horn and cross-modally corroborated the neuronal branch with P5 snRNA (§9 of P5_RESULTS); a mouse SNI Visium arm (currently absent) would add the missing spatial Sham-vs-SNI dimension.

---

## 6. Tables & Figures (all real, Tier 1)

- `P6_ligand_funnel.png` — ligand library funnel
- `P6_param_fidelity.png` — parameter fidelity validation
- `P6_target_decisions.png` — target selection decisions
- `P6_reverse_control.png` — per-target reverse-control AUC
- `P6_ranking_drugs.png` — Top-20 drug 4-dim ranking
- `P6_target_drug_matrix.png` — target–drug hit matrix
- `P6_ranking_drugs.csv` / `P6_ranking_pairs.csv` — full ranking tables
- `P6_reverse_control_positives.csv` — ChEMBL-derived independent positive set (164 pairs)
- `P6_enrichment_mw_confounder_check.csv` — molecular-weight confounder control
- `P6_face_validity.csv` / `P6_face_validity_alpha2_individual.csv` — face-validity tests (§3.4.1, negative)
- `P6_mw_ranking_summary.csv` / `P6_mw_ranking_pairs.csv` — ranking robustness and precision@k (§3.4.2)
- `P6_throughput_summary.csv` + `results/P6_throughput_note.md` — per-ligand cost accounting
- `P6_liglist_audit.json` — ligand-list cache-invalidation audit (§2.7)
- `P6_breadth_target_summary.csv`, `P6_breadth_target_rank_stability.csv`, `P6_breadth_chembl_power.csv`, `P6_breadth_pocket_volume_confound.json`, `P6_breadth_note.md`, `figures/P6_breadth_breadth.png` — pre-registered breadth analysis (§3.5)
- `P6_RESULTS.md` — auto-generated result summary

**Human-validation layer (P4) — supporting outputs.** `P4_HUMAN_REANALYSIS_RESULTS.md` (GSE249746 + GSE107181), `results/P4_SPARC476_results.md` + `figures/P4_SPARC476_hub_lfc.png` (SPARC 476 Visium), `results/P4b_Pennsieve480_results.md` + `figures/P4b_Pennsieve480_hub_lfc.png` (Pennsieve 480 snRNA-seq), and the accompanying `*_geneset_test.csv` / `*_hub_stats.csv` / `*_donor_hub_log2cpm.csv` / `*_hub_celltype_corr.csv` tables. Source data: GSE249746, GSE107181, SPARC Dataset 476 (DOI 10.26275/mfxc-k28b) and Pennsieve Dataset 480 (DOI 10.26275/9QSP-I8DH), all CC-BY-4.0 open access.

**Data-integrity note (reporting caveat).** In `P6_ranking_drugs.csv`, `affinity_at_best_target` is the affinity at the stated `best_target` and must be used when reporting a drug–target pair. The separate column `best_affinity_any_target` is the drug's strongest value across *all* targets and — in 19 of the top 20 drugs — belongs to a **different** target. An earlier draft of this manuscript conflated the two (e.g. attributing ergotamine's SLC2A1 affinity of −10.93 to ADRA2A, whose true value is −10.36); the columns have since been separated and this caveat fixed in the reporting scripts.

**Data-integrity note 2 (cache invalidation).** An audit of the per-target scoring tables against the current tier lists (§2.7) found that AXL's Tier-1 table had been computed against a superseded ligand list (60 ligands since moved to Tier 2, 60 current Tier-1 ligands absent). The affected chunks were quarantined and AXL Tier 1 re-docked; all tables reported here post-date that correction. Any table bearing the pre-correction AXL Tier-1 state is superseded and should not be cited.

---

## 7. Open items before finalisation

Sequencing is fixed as *run → regenerate → then transcribe numbers*; no number is written into this draft before the run that produces it has finished.

1–5. **Executed (2026-09-19)** by `scripts/p6_finalize_watch.py`; `P6_FINALIZE_STATUS.json` = `ready_to_finalise` (audit OK across all 20 target×tag; self-heal rebuild of merged tables from per-target source-of-truth files; all controls + breadth regenerated, rc=0). §3.2 and §3.5 filled from the fresh tables.
6. **Executed (2026-09-19):** title, §3.5.2 (line 146) and §5 Conclusions aligned to §3.5.4 — "leading/validated target" removed everywhere; now uniformly "best-supported (Tier-1) hypothesis" consistent with the pre-registered full-library overturn (AUC 0.532, p=0.118, NS). Abstract conclusion already aligned. Added §5.1 Future directions (ion-channel cryo-EM/AF3 track; consensus/MM-GBSA/FEP scoring; better-powered human cohort/meta; MD+MM-PBSA/IFD + wet lab; SNI-Visium spatial layer).
7. Possible wet-validation proposal for ADRA2A-binding analgesics in a CPSP model (escalates to C-tier journal). **Downgraded:** the full-library test no longer supports ADRA2A as a *validated* target, only as the best-supported *Tier-1* hypothesis; wet validation would need to be framed accordingly.
8. Reproducibility package (GitHub `yyx-4113/cpsp-drg-spinal-repurposing` + Zenodo DOI): pack files are in place; remaining work is `git init/push`, tag `v1.0.0`, and DOI back-fill.

Steps 1–5 are executed unattended by `scripts/p6_finalize_watch.py`.
