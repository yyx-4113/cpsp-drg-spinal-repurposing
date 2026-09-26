# REVIEW — Round 2 (independent panel) · CPSP DRG–Spinal Axis manuscript v1.1

**Manuscript:** "A neuroimmune–metabolic programme defines the chronic postsurgical pain DRG–spinal axis with an honest repurposing null" (target: *Scientific Reports*, Article)
**Review date:** 2026-09-20
**Editor:** 小团 (consolidating editor; acted as journal editor organising the panel)
**Panel:** 4 independent experts — A1 Domain (CPSP/neuropathic-pain biology), A2 Design/Statistics/ML, A3 Implementation/Provenance auditor, A4 Venue/Editorial & reporting-standard.

---

## 1. Independence statement (mechanism + evidence it worked)

The panel was convened under a strict independence discipline: each expert was forbidden from reading `reports/REVIEW_round1_2026-09-20.md`, the submission manifest, `PROJECT_PLAN.md`, `GITHUB_DEPOSIT_SOP.md`, `author_verification_statement.md`, `README.md`/`CITATION.cff`, other reviewers' files, and the gate scripts. Every expert recomputed headline numbers from raw CSVs rather than trusting the automated gates.

**Evidence the discipline worked — the diagnostic signature is present:** several experts, with zero knowledge of each other, converged independently on the *same* defects from different angles:
- **Orphan references 5/11/12** — caught independently by A3 (provenance) *and* A4 (venue). Both grepped the manuscript and found no superscript ⁵/¹¹/¹².
- **ADRA2A disproportionate defence vs the disclosed pending grant** — caught independently by A1 (domain) *and* A4 (venue), each from its own layer.
- **"neuroimmune–metabolic axis" over-specificity + novelty overclaim + REG3B misclassification** — surfaced by A1 from biology; the permutation-floor / CV-leakage / GSE265957 / SPRR1A / ACVR1 issues were new, design-layer findings invisible to the compliance gate.

Conversely, the cluster did **not** merely re-litigate prior-round points: the bulk of Tier-1 items below are *fresh* design/compliance findings the prior Round-1 did not surface (orphan refs, Nature-style, permutation floor, ACVR1 LR/Wald, GSE265957 over-representation, SPRR1A labeling, 253-definition, pooled-CV impossible dispersion, REG3B, novelty priors, Visium denominator, Reporting-Summary missing CI, Supplementary repo URL). This is the behaviour the independence rule is designed to produce.

**Editor's own verification (do not forward a finding unconfirmed):** I personally re-checked the four most consequential claims against raw sources:
1. **GSE265957 "Tier-0 same-animal double-counting" → REFUTED.** The GEO record (GSE265957) states RFP + bulk mRNA were sequenced at "day 4 or day 63 time points … each condition had two biological replicates." Ribosome profiling is destructive, so D4 and D63 are independent cohorts, not same-animal longitudinal. The structural facts (two meta-entries, `w=1.0` hardcoded, n=2/arm, one study = 2 of 6 meta inputs) are real but the conclusion-invalidating component is absent. **Demoted from Tier-0 to Tier-1.**
2. **ACVR1 LR-vs-Wald contradiction (A2-F6) → CONFIRMED.** `P6_multivariate_physchem_control.csv`: ACVR1 `LR_dock_residual_p` = 9.6e-4 (significant) but `Wald_neg_aff_p` = 0.172 (NS). One of the three "validated" targets fails its own coefficient test.
3. **ADRA2A Tier-1 AUC 0.618 "not in any CSV" (A3-D4) → REFUTED as a data gap.** It is in `P6_breadth_chembl_power.csv` (ADRA2A `t1_only` auc = 0.61837). Only a *figure-source citation* gap remains (Fig 5C cites `P6_reverse_control.csv` + `P6_enrichment_mw_confounder_check.csv`, not the breadth file).
4. **SPRR1A "17.4× arithmetic error" (A2-F9 / A3-D2) → REFUTED as arithmetic.** 17.4× = `specificity` = top_mean/others_mean = 3.0912/0.1777 = 17.39 (correct expression ratio). The detection ratio is 98.1/16.8 = 5.84×. The defect is purely *labeling* — the Results line juxtaposes a detection percentage against an unrelated expression ratio, which a reader misreads. Demoted from "critical arithmetic error" to Tier-2 wording.

---

## 2. Verdict table

| Reviewer | Layer | Overall verdict | Tier-0 | Tier-1 | Tier-2 | Tier-3 |
|---|---|---|---|---|---|---|
| A1 Domain | Biology / literature / claims | Major revision | 0 | 4 (1A,1B,1C,1D) | 4 (2E,2F,2G,2H) | 0 |
| A2 Design | Statistics / ML / leakage | Major revision | 0 (candidate refuted) | 6 (F2,F3,F4,F5,F6,F8) | 4 (F1,F7,F9,F10) | 0 |
| A3 Audit | Provenance / recompute | Major revision | 0 | 3 (D1; D2 demoted to T2; D4→citation) | 5 (D3,D5,D6; D2; D4-citation) | 0 |
| A4 Venue | Format / disclosure / cross-doc | Major revision | 0 | 4 (F1,F2,F3,F4) | 4 (F5,F6,F7,F8) | 0 |

**Distribution:** 0 Tier-0 (no conclusion-invalidating defect confirmed). ~17 Tier-1/2 items, of which the compliance cluster (Nature-style refs, 3 orphan refs, Reporting-Summary missing Competing Interests) is a *must-fix-before-submission* group that the manuscript's own "format compliant" self-declaration fails. The scientific conclusion — a reproducible "honest docking null" — survived every recomputation.

---

## 3. Cross-verification table (manuscript claim vs independently recomputed)

| # | Manuscript location | Manuscript claims | Independently recomputed | Checked by | Verdict |
|---|---|---|---|---|---|
| 1 | L31 | Core 4,055 genes; 16,552 tested; 6,869 FDR<0.05 | 4,055 / 16,552 / 6,869 exact | A3, editor | ✅ PASS |
| 2 | L33/Fig1 | Neuroinflammation +4.94/100% up; DAM +3.88/93.8%; complement +3.44/94.4%; OXPHOS −2.37/73.7% down | exact (perm p 0.0005/0.0005/0.0005/0.004) | A1, A3 | ✅ PASS (but see F1 floor) |
| 3 | L33/64/Abstract | SCN9A/10A/11A meta_Z −3.6 to −3.1; FDR 1.7e-3–5.9e-3 | FDR exact; range is **−3.56 to −3.15** | A3 | ⚠️ wording slip (D5) |
| 4 | L36 | 32/35 hubs in meta core | exact | A3 | ✅ PASS |
| 5 | L38 | LODO GSE267799 0.917 [0.729,1.000] | exact | A3 | ✅ PASS |
| 6 | L44/Fig3 | DRG 20/25; SPRR1A 98.1% vs 16.8% detection (17.4×); ECEL1 25.7×; NPY 10.0×; FLNC 10.2× | counts exact; **17.4× = expression ratio (specificity 17.39); detection ratio = 5.84×** | A2, A3, editor | ⚠️ labeling (Tier-2) |
| 7 | L46 | 7/35 confident spinal lineage | exact | A3 | ✅ PASS |
| 8 | L51/Fig4B | Visium 33/35 detectable; 17/35 dorsal horn | counts exact; denominator framing | A1, A3 | ⚠️ minor (Tier-2) |
| 9 | L54/56 | ADRA2A full-library AUC 0.532; p 0.118; MW-adj 0.578 | exact | A3 | ✅ PASS |
| 10 | L56 | precision@10 0.700; lift ×18.69; p 9.4e-9; precision@20 0.450; p 1.3e-8 | exact | A3 | ✅ PASS |
| 11 | L54/S4 | Multivariate LR p: AXL 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4, ADRA2A 0.027, MAPK14 0.066 | exact | A3 | ✅ PASS — **but ACVR1 Wald p = 0.172 (contradiction, F6)** |
| 12 | L41 | Human set-level perm p = 0.51; "253 … human plasma" | p exact; **253 = (hub,plasma-miRNA) pairs, not hubs** | A3 | ⚠️ wording (Tier-2) |
| 13 | L14/L56 | Tier-1 ADRA2A AUC 0.618 → 0.532 | 0.618 in `P6_breadth_chembl_power.csv`; only citation gap | A3, editor | ⚠️ citation (Tier-2) |
| 14 | L38 | Pooled 5×20 CV AUC 0.999 ± 0.004 | 0.999209; +SD = **1.0032 > 1.0 (impossible)** | A2, editor | ❌ Tier-1 (F3) |
| 15 | L80/Script | GSE265957 D4 + D63 as two meta datasets, w=1.0, n=2/arm | structural confirmed; **same-animal longitudinal REFUTED** (GEO: independent cohorts) | A2, editor | ⚠️ Tier-1 (F2, demoted) |
| 16 | L107–125 | References in Nature style; all 18 cited | **Vancouver/AMA style, not Nature**; **orphans {5,11,12}** | A3, A4 | ❌ Tier-1 (F1/F2) |
| 17 | RS §AI | Reporting Summary has Competing Interests block | **absent** (present in MS + cover letter) | A4 | ❌ Tier-1 (F3) |

---

## 4. Graded consolidated issue list

### Tier 0 — conclusion-invalidating
**None confirmed.** The candidate (GSE265957 same-animal double-counting) was refuted by the editor against the GEO design statement. The "honest docking null" and the meta/ML backbone recomputed exactly across all four auditors.

### Tier 1 — substantive (analyses to add / reword; must address before submission)
- **T1-1 · GSE265957 is one study represented as two of six meta inputs, n=2/arm, with undisclosed relatedness and measurement heterogeneity (A2-F2, editor-refuted Tier-0).** Disclose that GSE265957 contributes two timepoints (D4 acute, D63 chronic) from one tibial-nerve-injury study, each contrast n=2/group; note the "six-dataset" meta is five studies; acknowledge that GSE265957's DRG input is *translatome* (Xtail ribosome-profiling log2FC) mixed with bulk-transcriptome meta_Z from other studies — a measurement-heterogeneity limitation. Add a sensitivity meta-analysis collapsing GSE265957 to one contrast and report whether the 4,055-gene core survives. **Severity: moderate — over-states independence of the meta core.**
- **T1-2 · Pooled CV AUC = 0.999 ± 0.004 is leakage-inflated and prints an impossible dispersion (A2-F3, editor-confirmed).** The ± implies AUC > 1.0. Report LODO (mean 0.973; range 0.917–1.000) as the primary generalisation metric; demote the pooled within-dataset CV to "optimistic, leakage-prone" or replace with dataset-stratified CV; never print a CI crossing 1.0.
- **T1-3 · "Docking adds signal beyond chemotype" for AXL/TNIK/ACVR1 is contradicted internally (A2-F6, editor-confirmed).** `Wald_neg_aff_p` for ACVR1 = 0.172 while `LR_dock_residual_p` = 9.6e-4; single-variable size-independent ΔAUC 95% CI contains zero for AXL/TNIK/ACVR1/MAPK14. The LR "significance" rests on only 9–13 positive events and large total n. Soften to "a small, event-poor, n-inflated increment that does not survive the simpler size-independent test"; report n_pos, the docking-coefficient Wald p, and the AUC deltas. **This does not overturn the honest null but undercuts the "protocol-validating" sub-claim.**
- **T1-4 · Three orphan references (5, 11, 12) — never cited (A3-D1 / A4-F2, editor-confirmed).** Refs 11 (Suzetrigine nonopioid analgesic) and 12 (Nav1.7/SCN9A blocker) are directly on-topic for the analgesic-enrichment-null and SCN reframing claims. Either cite them at L53–56 / L64 or delete. **Compliance hard-fail on the manuscript's own "all references cited" expectation.**
- **T1-5 · References are not in Nature style (A4-F1).** All 18 use Vancouver/AMA template; Scientific Reports requires Nature style (surname-comma-initials, `&` before last author, italic-abbreviated journal with periods, **bold volume**, year in parentheses). Reformat all 18.
- **T1-6 · Reporting Summary omits the Competing Interests block (A4-F3).** Present in manuscript (L139) and cover letter (L17) but absent from the Reporting Summary. Add it verbatim.
- **T1-7 · ADRA2A defence is disproportionately elaborate vs its (worst) docking performance and the disclosed pending grant (A1-1D / A4-F4).** ADRA2A (full-library AUC 0.532, the only target below chance) gets the longest "biologically plausible" rescue while being a candidate in the author's own pending FJNSF grant — directly contradicting the manuscript's own "assessed uniformly, not an ADRA2A-specific rescue" sentence (L58). Either generalise the biological-plausibility discussion to all 10 targets, or add an explicit conflict-of-interest guard and soften "biologically plausible" to "a biologically plausible hypothesis to be tested." **Perceived-bias risk — credibility, not mechanics.**
- **T1-8 · Novelty claim overstated; two directly relevant priors uncited (A1-1B).** Meng 2024 (*Sci Data* 39543146, multi-tissue CPSP incl. DRG) and Dong 2025 (*Commun Biol* 39820760, DRG↔spinal cross-talk atlas in neuropathic pain) are not cited. Narrow the "first … integrate DRG and spinal-cord" claim to the method combination and cite both.
- **T1-9 · "neuroimmune–metabolic axis" presented as CPSP-specific when statistics support a generic nerve-injury response (A1-1A).** The meta pools incision + CCI + SNI + tibial-nerve models; nerve-injury→incision translation was only 59.9% consistent. Reframe as a *conserved* maladaptive injury programme, not a CPSP-unique pathway; state explicitly that specificity to *postsurgical* (vs nerve-injury) pain is not demonstrated.
- **T1-10 · REG3B wrongly flagged as an annotation outlier (A1-1C).** Nie et al. 2025 (*Sci Adv* PMID 40749060) shows DRG-neuron Reg3β drives a macrophage TNF-α feedback loop in chronic pain; NCBI Gene lists DRG expression. Remove REG3B from the outlier list and reclassify as an established DRG neuroimmune hub (strengthens, not weakens, the thesis).
- **T1-11 · Human miRNA layer framed as "honest negative" but is underpowered/inconclusive (A1-2G).** p = 0.51 with n=60 plasma miRNA is consistent with low power, not a confirmed absence. Rephrase as "no *detectable* association in an underpowered n=60 cohort; inconclusive, prospective qPCR/ELISA required."
- **T1-12 · Hub stability not demonstrated (A2-F5).** λ.1se = 1 gene; the 35 hubs ride RF/XGBoost over a univariate Top-800 pre-screen of 13,208 genes with n=72. Add a bootstrap (≥200 resamples) reporting per-gene selection-frequency CIs and demote any hub near the consensus threshold.
- **T1-13 · GSE241361 LODO tests are same-animal, presented on par with independent ones (A2-F4).** Label the two GSE241361 tests "same-animal, within-study (not cross-dataset)" and report the cross-animal LODO summary (GSE278227/GSE212311/GSE267799) separately; state the honest floor as "cross-animal LODO down to 0.917."
- **T1-14 · "three filters" collapses to two (A2-F8).** Raw and full-library p are the same quantity; the distinct filters are only (i) raw/full-library MW p and (ii) size-independent MW-adjusted p. Rephrase; drop the redundant third term.
- **T1-15 · precision@10 circularity unverified (A2-F7).** The composite "blends docking with pharmacological-prior terms" and is scored against ADRA2A ChEMBL binders; if the prior terms encode the same labels, precision@10 is tautological. Demonstrate the prior component uses a disjoint ChEMBL subset (leave-the-target-out), or relabel precision@10 as "knowledge-informed retrieval, circularity acknowledged" and drop the hypergeometric p as a validity claim.

### Tier 2 — wording / labeling (must fix; fast)
- **T2-1 · SPRR1A "17.4×" labeling (A2-F9 / A3-D2, editor-refuted arithmetic-error).** Keep 17.4× (correct expression ratio) but decouple from the detection percentage: "SPRR1A detected in 98.1% vs 16.8% (detection-ratio 5.8×) with mean-expression enrichment 17.4×." State that all "×" values are mean-expression folds (specificity), distinct from detection fractions.
- **T2-2 · "253" = (hub, plasma-miRNA) pairs, not hubs (A3-D3).** Reword L41: "253 high-confidence hub→miRNA pairs detectable in human plasma (of 608 high-confidence pairs; spanning 33 of 35 hubs)."
- **T2-3 · Visium denominator 17/35 vs 17/33 (A1-2E / A3-D6).** Write "17/35 hubs (of the 33 detectably expressed, i.e. 17/33 = 51.5%) mapped to the dorsal horn"; note scRNA and Visium exclude different non-detected hubs (REG3B vs LNP1).
- **T2-4 · SCN meta_Z range (A3-D5).** Change "−3.6 to −3.1" to "−3.6 to −3.2 (range −3.56 to −3.15)."
- **T2-5 · Permutation floor (A2-F1).** Report p = 0.0005 as a *ceiling* ("≤ 0.0005, resolution floor of 2,000 permutations; programmes not rankable against each other; ordering from Stouffer Z"), not an equality.
- **T2-6 · Fig 5C source note must cite `P6_breadth_chembl_power.csv` (A3-D4 corrected).** The Tier-1 0.618 is traceable there; the figure source currently omits it.
- **T2-7 · Ref #8 preprint correction remark (A4-F5).** Trim "original citation to Brain 2026 was incorrect" to a clean preprint citation.
- **T2-8 · "first …" novelty unbundled/hedged (A4-F6).** Apply "To our knowledge" consistently in abstract and introduction; drop or reframe the third "first" (full-library screen is methodological, not intrinsically novel).
- **T2-9 · "honest null" vs candidate shortlist framing (A4-F7).** Scope the null explicitly to *docking enrichment* in the abstract; acknowledge the separate knowledge-informed Top-20 as prospectively testable, not docking evidence.
- **T2-10 · Over-precise n=2–3/group ratios (A2-F10).** Keep qualitative localisation in main text; move decimal-precise ratios (SPRR1A 17.4× etc.) into a bounded "exploratory/directional hints" subsection or supplementary, with the n=2–3/group caveat adjacent and binomial CIs shown.

### Tier 3 — format / cross-document
- **T3-1 · Supplementary missing repo URL (A4-F8).** Print `https://github.com/yyx-4113/cpsp-drg-spinal-repurposing` once in the Supplementary for self-contained cross-document consistency.

---

## 5. Consensus / complementarity / disagreement

**Consensus (all four, independently):** (a) the quantitative backbone and the honest docking null are reproducible and scientifically valuable; (b) ADRA2A receives disproportionate, grant-linked advocacy that contradicts the paper's own "uniform" statement; (c) references are not Nature-style and three are orphaned; (d) the axis is over-claimed as CPSP-specific and the novelty claim is over-bundled.

**Complementarity:** A1 supplied the biological/literature corrections (REG3B, novelty priors, human-layer framing) that the other layers could not; A2 supplied the design-layer defects invisible to gates (GSE265957, CV leakage, ACVR1 LR/Wald, permutation floor); A3 supplied the provenance/recompute confirmation; A4 supplied the venue compliance cluster. Each layer caught defects the others did not.

**Disagreement (adjudicated by the editor):**
- **GSE265957 severity (A2 called it potential Tier-0; editor refuted the same-animal component):** adopted the stricter structural finding (over-representation + underpower + translatome mixing + asymmetric disclosure) but rejected the conclusion-invalidating double-counting. A2's own "solid regardless of same-animal status" framing is correct.
- **SPRR1A 17.4× (A2/A3 called it a critical arithmetic error; editor: correct value, labeling-only defect):** adopted Tier-2 wording, not Tier-1 arithmetic. The reviewers' instinct was right that the *line* misleads; the "×" itself is correct.
- **Tier-1 0.618 provenance (A3 called it "not in any CSV"; editor found it in `P6_breadth_chembl_power.csv`):** adopted Tier-2 citation gap, not a missing-data gap. A3's audit missed the breadth file.
- **ADRA2A biological plausibility (A1 objects to the *defence*; A1's own "Stands up" confirms the underlying signal is real):** the facts are correct, the *asymmetry/tone* is the defect — kept as T1-7.

---

## 6. Priority must-fix list

**Pre-submission compliance cluster (do these before uploading — the manuscript's "format compliant" self-declaration currently fails):**
- ⮑ T1-4 orphan refs 5/11/12 (cite or delete)
- ⮑ T1-5 reformat all 18 refs to Nature style
- ⮑ T1-6 add Competing Interests to Reporting Summary
- ⮑ T3-1 print repo URL in Supplementary

**Scientific credibility cluster (revision required; not strict desk-reject but a careful editor will query):**
- ⮑ T1-1 GSE265957 disclosure + sensitivity meta-analysis
- ⮑ T1-2 CV leakage / impossible dispersion
- ⮑ T1-3 ACVR1 LR/Wald contradiction + soften "protocol-validating"
- ⮑ T1-7 ADRA2A advocacy vs disclosed grant
- ⮑ T1-8 / T1-9 novelty + axis-specificity reframing
- ⮑ T1-10 REG3B reclassification

**No DESK-REJECT flag is warranted** — there is no Tier-0 conclusion-invalidating defect, and the docking null recomputes exactly. However, the compliance cluster above, if shipped as-is, will trigger an editorial "formatting required" return and undermines the "format compliant" claim; address it before submission.

**Must-add-analysis vs must-reword split:**
- *Must add:* T1-1 sensitivity meta-analysis (collapse GSE265957); T1-12 hub-stability bootstrap; T1-15/M1-2 dataset-stratified CV + LODO permutation null; T1-15 leave-the-target-out precision@10 (T1-15).
- *Must reword (no new data):* everything else — all are restatements, citations, or reframings.

---

## 7. What stands up (do NOT change)

Carried forward from the experts and the editor's own checks — these survived independent recomputation and should be preserved:
1. **Core meta-signature** (4,055 genes; 16,552 tested; ATF3 positive control meta_Z 10.53/FDR 1e-21) recomputes exactly.
2. **Gene-set programme** (neuroinflammation +4.94/100% up; DAM +3.88/93.8%; complement +3.44/94.4%; OXPHOS −2.37/73.7% down) — substantial curated sets, not small-set artefacts.
3. **SCN9A/10A/11A down-regulation reframing** is biologically correct (expected axotomy signature).
4. **32/35 hub-convergence, LODO GSE267799 0.917 [0.729,1.000], 7/35 confident lineage, 20/25 DRG localisation, 17/35 Visium dorsal horn** — all exact.
5. **The honest docking null itself** — ADRA2A 0.532/0.118/0.578, multivariate LR p-values, BH-q, precision@10=0.700/lift 18.69/p 9.4e-9, precision@20=0.450 — recompute end-to-end. The "no target clears the filters; honest null" conclusion is the right call.
6. **BH correction arithmetic** is exact (A2 verified).
7. **Lift denominator** for precision@10 is correctly the per-target known-binder prevalence, not a library-wide rate.
8. **ADRA2A's biological-plausibility facts** (meta_Z 4.84, FDR 1.5e-5; α2A descending-analgesia pharmacology) are real — only the *asymmetry of the defence* is the problem (T1-7).
9. **Format items verified clean:** title 15 words; abstract 179 words, 0 citations; display items 8; figures ~320 DPI; Methods last; mandatory declarations present; AI disclosure in Methods + Reporting Summary; real repo URL + "not available on request" consistent across docs.

---

## 8. Recommended handling path

**A) Restructure-and-resubmit as the same Article type — recommended.** The work is sound, reproducible, and the negative/honest reporting is a genuine strength that fits Scientific Reports' reproducibility mandate. All Tier-1 items are restatements or one sensitivity analysis + one bootstrap, not new experiments. The paper does **not** need to be downgraded (e.g., to a "matters arising" or a methods note); it needs the compliance cluster fixed and the framing tightened.

**B) Do NOT downgrade article type.** The prospective full-library docking breadth + dual-ML LODO + 12-dataset meta is a complete original-research story.

**C) Wording-only is not viable** for the design layer — T1-1 (GSE265957 sensitivity meta-analysis) and T1-12 (hub stability) are genuine analyses, and T1-2/T1-3 require re-framing the validation claims, not just polish.

**Reframe, don't just criticise (editor's direct note to the author):**
- **The strongest claim that does not hold** is that this is a *CPSP-specific* neuroimmune–metabolic axis discovered here. It is in fact a *conserved, generic* nerve-injury programme (59.9% translation to the incision model; pools CCI/SNI/tibial-nerve). This is **not your fault** — it is a structural property of pooling heterogeneous injury models — but the title/abstract/intro over-state specificity.
- **The buried contribution that is actually your paper** is the *methodological* one: a prospectively specified, full-library, reverse-controlled docking screen that turns an apparent Tier-1 hit (ADRA2A 0.618) into an honest null (0.532, NS), demonstrates how filtering/double-dipping manufactures false positives, and couples that to leakage-controlled ML and rigorous negative reporting. **Swapping the headline from "we found a CPSP axis" to "we show how repurposing screens go wrong and report an honest null" converts a fragile signal into a stable, reusable methodological boundary** — which is what Scientific Reports explicitly publishes.

---

## 9. Process lessons (what the gates could not catch, and how to extend coverage)

1. **A gate passing at 100% proves arithmetic, not design.** `gate_consistency.py` verified 46/46 numbers, yet the panel found ~17 design/compliance defects. The gate only checks the strings it enumerates; the *second occurrence* and the *framing* are where it goes stale. Recommendation: extend the gate to (a) grep every derived artefact for the *value* not the location (catch the duplicate 17/35 denominator, the un-cited refs via superscript parse), and (b) add a "permutation-floor" assertion and a "no AUC CI crossing 1.0" assertion.
2. **"Counted N events" ≠ "N patients" / "one study as K datasets."** GSE265957 (one study → 2 meta entries, n=2/arm) and the pooled-CV leakage are design-layer defects no recompute-gate flags. Add a manifest of meta-dataset → GEO-accession → n/group → relatedness, and assert independence.
3. **Internal statistical contradiction (LR vs Wald)** slipped through because the gate checked the LR p but not the Wald p in the same row. Add a "coherence" check across columns of the multivariate CSV.
4. **Citation completeness** (orphan refs) is a venue gate that should be mechanical: parse superscripts, expand ranges, assert every reference is cited and every citation is listed. This is cheap and currently missing.
5. **The independence discipline caught new design-layer defects** (GSE265957, CV leakage, ACVR1 LR/Wald, permutation floor) that Round-1 and the gates missed — confirming the value of re-reviewing the *current state* rather than the *delta*.

---

*Expert files (audit trail): `reviews/round2_2026-09-20/A1_domain.md`, `A2_design.md`, `A3_audit.md`, `A4_venue.md`. Shared brief: `_PANEL_BRIEF.md`. Editor verification scripts run directly against `results/tables/*.csv` and the GEO record for GSE265957.*
