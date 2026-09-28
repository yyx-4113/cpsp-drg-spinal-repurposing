# A1 · Domain review (pain neuroscience / CPSP) — round 13 panel, 2026-09-28

**Reviewer lane:** biological / domain validity only (statistics = A2, code/reproducibility = A3, journal compliance = A4). Cross-cutting issues seen from my lane are flagged as such and deferred to the owning reviewer.

**Independence statement.** I read only: `reports/MVP_PLOSONE_submission.md` (full, 385 lines), `reports/MVP_PLOSONE_supplementary.md` (full), result files under `results/tables/` and `results/*.md`, and `data/processed/GSE158825_*`, `GSE267799_*`. I did **not** read `reviews/` (no prior-round files), and did not read `MVP_STROBE_checklist.md` or `MVP_PLOSONE_compliance_check.md`. I did not modify any manuscript, supplement, or script; this file is my only write.

---

## Recommendation: **MAJOR REVISION**

**Justification.** The manuscript is unusually honest by the standards of this literature: the negative full-library docking screen, the non-circular translation test, the permutation-floor disclosure on the gene-set q-values, the ambient-RNA voiding, the LODO degeneracy caveats and the resampling-sensitive candidate-set framing are all correct in spirit and, on the numbers I checked, correct in fact (see *Independently verified*). Nothing I found is fabricated, and I found **no T0 (submission-blocking)** item.

I nevertheless recommend major revision because three domain defects distort interpretation of the paper's central results:

1. The held-out "translation test" compares an **axotomy-derived transcriptional programme against a deliberately non-axotomy model** (SMIR), and the manuscript never states this lesion-class mismatch. The null is therefore predicted a priori and cannot carry the weight the Abstract/Conclusions place on it ("not shown to be CPSP-specific"). The finding is not wrong — it is under-specified to the point of being non-informative, and a pain-literate reader will read it as confounded (F1).
2. The "nerve-injury-**enriched** — not specific" downgrade is applied consistently in most places but **leaks back** in one sentence, where a resampling-fragile classifier is described as having "nerve-injury specificity" as its "robust finding" — a claim the only relevant test (incision fold, AUC 0.677 [0.374, 0.940]) cannot support (F2).
3. The single most clinically actionable gene in the entire dataset — **CACNA2D1 / α2δ-1, the gabapentinoid target** — is meta-significant, direction-concordant 6/6 and among the strongest up-regulated genes, yet is reported only as "undockable". Its omission makes the "neuroimmune/metabolic, not ion-channel" summary misleading and forfeits the internal positive control that the manuscript's own reference-38 argument needs (F3).

All three are fixable by adding/replacing sentences, not by re-running analyses. With F1–F3 addressed plus the T2/T3 items, I would expect to recommend minor revision or accept.

---

## Findings

### T1 — major

---

#### F1 (T1) · The incision arm is a non-axotomy model; the held-out translation test is confounded by lesion class, and the manuscript never says so

**Location.** Results "Translation to the incision model is incomplete and, tested non-circularly, non-predictive" (lines 54–58); Methods "Sensitivity analyses" (line 158, the paragraph beginning "**GSE267799 is a heterogeneous, two-model incision arm.**"); Limitations (line 136); Abstract Conclusions (line 20) and Conclusions (line 140).

**What is wrong.** The incision arm is the SMIR arm of GSE267799 (confirmed: `results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`, `data/processed/GSE267799_DRG_sampletable.csv`, model column = SMIR). SMIR is the one postoperative model in this panel that is explicitly **not** a nerve-injury model: Flatters et al. (2008, *Pain* 135:119–130 — ref 39) report essentially **no** neuronal damage in SMIR DRG ("very little to no degeneration was detected with ATF3 staining in DRG from SMIR-operated rats… not driven by neuronal damage"), alongside the dissipation of hypersensitivity by POD 32 that the manuscript already cites correctly.

The manuscript's own meta, however, is an **axotomy/constriction-injury programme**: its two strongest hubs are ATF3 (meta_Z +10.53, FDR 1.0e-21, 6/6 up) and SPRR1A (+8.18, 6/6 up) — the canonical neuronal-injury/regeneration markers — and 4 of the 5 nerve-injury contrasts are CCI/SNI (axonal injury). So the test as constructed asks: "does an axotomy-induced regeneration/inflammation programme predict direction in a model with no axotomy?" The observed 46.2% vs 47.1% background is the a-priori-expected answer. Reporting it as an informative negative about CPSP (and as the evidentiary basis for "CPSP-specificity is not shown") over-reads the design. The manuscript does flag the arm as heterogeneous and day-32 as resolving — that is good — but it attributes the mismatch to **time course** ("acute-to-subacute") and **model pooling**, and never to the decisive difference: **lesion class (axotomy vs non-axotomy)**.

**Why it matters.** This is the paper's central translational claim and it appears in the Abstract, Author Summary, Discussion and Conclusions. In its present form a CPSP reviewer will judge the negative translation test as confounded, which weakens the whole "honest null" framing rather than strengthening it. Stating the confound explicitly *strengthens* the paper: it converts a weak negative into a correctly scoped non-informative result and it is fully consistent with the paper's honesty posture.

**Concrete fix.** (a) In Methods line 158, after the Flatters sentence, insert:

> "More fundamentally, SMIR is a **non-axotomy (non-neurotmetic) postoperative model**: Flatters et al. report essentially no ATF3 staining or degeneration in DRG after SMIR and conclude that SMIR-evoked pain is not driven by neuronal damage, whereas the four remaining contrasts (CCI ×2, SNI ×2) involve axonal injury. The held-out test therefore contrasts an axotomy-associated transcriptional programme with a model in which that lesion class is absent; the lesion-class mismatch, not only the time course and the day-32 dilution, is expected a priori to reduce concordance."

(b) In Results, replace the sentence "The conclusion is stronger, not weaker, than the original formulation: knowing that a gene is strongly and consistently regulated by nerve injury carries essentially no information about its direction in the incision model, and roughly half of such genes move in the opposite direction." with:

> "The conclusion is stronger, not weaker, than the original formulation, but it must be read within its lesion-class limit: knowing that a gene is strongly and consistently regulated by axotomy-constriction nerve injury carries essentially no information about its direction in the non-axotomy SMIR model (46.2% vs 47.1% background, p = 0.14), and roughly half of such genes move in the opposite direction. Because the two arms differ in lesion class as well as in time course, this null is **uninformative about CPSP** rather than evidence that the nerve-injury programme fails to translate to postsurgical pain."

(c) In Limitations (line 136) replace "no dataset captures established chronic postsurgical pain (>3 months; the incision arm models acute-to-subacute pain)" with:

> "no dataset captures established chronic postsurgical pain (>3 months); the incision arm models acute-to-subacute postoperative pain and is additionally a non-axotomy (SMIR) model, so it is not lesion-class-matched to the four nerve-injury contrasts and cannot be used to test whether an axotomy-associated programme generalises to postsurgical pain."

(d) In Abstract Conclusions and Conclusions, add "— and because the two arms differ in lesion class, this test is non-informative rather than negative" after the 46.2%/47.1%/p = 0.14 clause.

---

#### F2 (T1) · "nerve-injury specificity" leaks back in, and is not supported by the only test that could support it

**Location.** Results, "35 candidate hub genes, with explicitly bounded stability", line 64: "we present the classifier as a candidate-generation tool whose **nerve-injury specificity** is the robust finding and whose incision generalisation is not established."

**What is wrong.** Two problems. (i) Wording: this is the one place where the "nerve-injury-enriched, not specific" downgrade is abandoned; everywhere else ("candidate nerve-injury-enriched — not universally generalisable", "not shown by this meta-analysis to be CPSP-specific") the manuscript is careful. (ii) Substance: "specificity" would require the classifier to *fail* on non-nerve-injury states; the single non-nerve-injury fold is GSE267799 at AUC 0.677, 95% CI [0.374, 0.940] (verified in `P3_lodo_auc_ci_leakage_controlled.csv`), a CI that includes chance. A test that cannot distinguish 0.677 from 0.5 cannot establish specificity. What the LODO panel shows is *cross-dataset generalisation within nerve-injury models* (GSE278227 AUC 1.000, n = 28; GSE212311 AUC 1.000, n = 6), which is a weaker and different claim — and one the manuscript itself correctly describes elsewhere as resting on a single n = 28 fold.

**Why it matters.** This sentence is the only place where the word "specificity" is used as a positive claim about the axis, and it sits in the Results paragraph that reviewers will read as the hub-validation statement. It directly contradicts the paper's central downgrade and invites the "over-claims relative to null results" criticism the manuscript otherwise avoids.

**Concrete fix.** Replace the clause with:

> "we present the classifier as a candidate-generation tool whose **cross-dataset generalisation within nerve-injury models** is the robust finding (two independent cross-animal folds, GSE278227 n = 28 and GSE212311 n = 6, both AUC 1.000; the n = 6 fold is at its design floor), whose behaviour outside nerve injury is **unresolved** (incision fold 0.677, 95% CI [0.374, 0.940], inclusive of chance) and which therefore establishes **no nerve-injury specificity**."

Optionally add the same qualifier to the Author Summary sentence "we frame the axis as a nerve-injury-associated transcriptional response rather than a CPSP-specific mechanism" — that sentence is already correct and needs no change.

---

#### F3 (T1) · CACNA2D1 (α2δ-1, the gabapentinoid target) is one of the strongest, fully concordant up-regulated genes in the meta and is never reported as such

**Location.** Fig. 1 legend (line 300: "Ion-channel families (Nav_SCN q = 0.44; TRP q = 0.89; CACNA q = 0.85; Kv/KCNQ q = 0.85) show no coordinate change (grey), the key negative finding indicating a **neuroimmune/metabolic, not ion-channel, axis**"); Results "SCN-channel directions are model-dependent" (line 52); Discussion (line 126, the α2δ-1 / gabapentinoid paragraph). CACNA2D1 appears in the manuscript only in the list of undockable structures (Methods line 175) and inside the CPSP_literature gene set (Supplementary Table S5).

**What is wrong.** In the primary six-input meta (`META_DRG_axis_stouffer.csv`, verified) CACNA2D1 has **meta_Z = +7.96, meta_FDR = 5.95e-13, consistency = 1.00, 6/6 contrasts up** (log₂FC +0.22 SMIR, +1.16 GSE212311, +2.02 GSE278227, +1.87 GSE241361, +1.10 D4, +0.22 D63). That makes it, by |meta_Z|, one of the most significant genes among all the pain-relevant genes discussed in this paper — stronger than any of the ten docking targets except TNIK, and stronger than ADRA2A (+4.84, the illustrative case). It is also precisely the gene the manuscript invokes from outside the data in Discussion ("α2δ-1, the gabapentinoid binding site upregulated in injured DRG³⁸"). The report therefore cites Chen et al. (2018) for an observation its own meta already makes, while simultaneously telling the reader that the axis is "not ion-channel".

The set-level CACNA null (18 members, q = 0.85) does not contradict this: a family-wide test is insensitive to one strongly moving member, exactly as the manuscript itself argues for SCN8A/9A/10A/11A (where it correctly says "this is not a pure ion-channel-null story").

**Why it matters.** (i) It is a reporting omission of the most pharmacologically actionable gene in the dataset, and it makes a headline claim ("not ion-channel") misleading at the gene level. (ii) It removes the one available internal positive control: reporting that the meta independently reproduces α2δ-1 up-regulation is what makes the ref-38/gabapentinoid argument evidentiary rather than rhetorical. (iii) It strengthens the paper's own Limitations argument that "absence of docking enrichment is not evidence against gabapentinoid action" — an argument that currently rests only on the undockability of the target.

**Concrete fix.** (a) In Results line 52 (after the SCN paragraph), add:

> "The clearest single-gene exception to the ion-channel-family nulls is the gabapentinoid target itself: **CACNA2D1 (α2δ-1) was up-regulated in all six contrasts (meta_Z +7.96, meta_FDR 5.9 × 10⁻¹³, consistency 6/6)**, i.e. the present meta independently reproduces the injury-induced α2δ-1 up-regulation that underlies gabapentinoid efficacy³⁸ (in the SMIR model SMIR-evoked hypersensitivity is gabapentin-reversible⁴⁰), while the family-wide CACNA test remains null because its other 17 members do not move coordinately. The ion-channel statement is therefore a **family-level** statement, and the single most clinically actionable ion-channel-adjacent gene in this dataset is up-regulated, not null."

(b) In the Fig. 1 legend, change "indicating a neuroimmune/metabolic, not ion-channel, axis" to:

> "indicating a neuroimmune/metabolic axis at the level of coordinated families; this is a family-level statement and does not extend to individual genes — CACNA2D1 (α2δ-1) is up-regulated in 6/6 contrasts (meta_FDR 5.9 × 10⁻¹³) and SCN8A/9A/10A/11A are individually down-regulated (Table 1b)."

(c) In Discussion line 126, after "…upregulated in injured DRG³⁸", add "(independently reproduced in the present meta: CACNA2D1 up in 6/6 contrasts, meta_FDR 5.9 × 10⁻¹³ — reported in Results and not used as a docking target, because the target is undockable)".

(d) Add Flatters 2010 (*Neuroscience Letters*; gabapentin reverses SMIR-evoked hypersensitivity — PubMed 20417687) as reference 40, or cite the same fact from the existing ref 39 if the author prefers. This is the cleanest available evidence that gabapentinoid biology is alive in the very arm the docking screen cannot address.

---

### T2 — moderate

---

#### F4 (T2) · "Resident microglia versus infiltrating macrophages" is the wrong dichotomy for a DRG-derived signature

**Location.** Results line 48 ("Because this is a bulk-tissue gene-set signal, it cannot be attributed specifically to resident microglia versus infiltrating macrophages or other neuroimmune cells; 'DAM-like' denotes the shared transcriptional programme, not a cell-type-resolved state"); Discussion line 122 ("coordinated DAM-like (myeloid: resident microglia and/or infiltrating macrophages) neuroimmune and complement activation"); Limitations line 136 ("cannot resolve microglia from infiltrating macrophages").

**What is wrong.** The meta core is strictly DRG-derived (the manuscript says so correctly in Methods, "Tissue scope of the hub set"), and DRG is outside the CNS parenchyma: the myeloid compartment of an injured DRG is **resident plus recruited macrophages** (Yu et al. 2020, ref 26, verified: "expansion and proliferation of macrophages around injured sensory neurons in DRG", explicitly paralleled with — and distinguished from — dorsal horn microglia, "the resident macrophages of the CNS"). Microglia are the correct comparator for the *spinal pole* (which contributes only localisation, not the meta signal), not for the DRG pole that generated the numbers. As written, the sentence lists microglia as a plausible source of a DRG-derived signal, which is a cell-biology error that a pain reviewer will catch immediately. The Yu 2020 reference is cited in Limitations but the distinction is not carried into the Results/Discussion wording.

**Why it matters.** It misattributes the cellular source of the paper's main positive finding, and it blunts the paper's otherwise careful DAM-like caveat. The DAM programme itself is defined in CNS microglia (Keren-Shaul 2017, ref 27, correctly acknowledged), so the "DAM-like" hedge needs the macrophage framing to be biologically coherent.

**Concrete fix.** In Results line 48, replace "resident microglia versus infiltrating macrophages or other neuroimmune cells" with:

> "DRG-resident versus recruited macrophages (the DRG myeloid compartment: ref. 26), satellite glia, or blood-derived immune cells — and, at the spinal pole, resident microglia versus infiltrating myeloid cells".

In Discussion line 122, replace "(myeloid: resident microglia and/or infiltrating macrophages)" with:

> "(myeloid: at the DRG pole, resident and/or recruited macrophages²⁶; at the spinal pole, microglia and/or infiltrating myeloid cells), recognising that the gene-set signal is generated by DRG tissue and that the spinal contribution enters only through localisation".

In Limitations line 136, replace "cannot resolve microglia from infiltrating macrophages" with "cannot resolve DRG-resident macrophages from recruited macrophages, satellite glia or blood-derived immune cells, and cannot resolve microglia from infiltrating myeloid cells at the spinal pole".

---

#### F5 (T2) · The human layer is under-specified: the outcome timepoint is never stated and the primary contrast is a surgical-procedure contrast, not a pain-state contrast

**Location.** Results, "The human layer is negative, a blood-proxy boundary, not a failure" (line 70); Methods "Human miRNA layer" (line 169); Limitations/Conclusions ("no analysed dataset captures established chronic postsurgical pain (>3 months)").

**What is wrong.** (i) GSE158825 is a **lumbar spinal stenosis surgery** cohort (LSS vs LSS+DS; verified in `data/processed/GSE158825_sampletable.csv`, diagnosis column, and `GSE158825_series_matrix.txt.gz_samples.csv`). The primary differential (LSS+DS vs LSS) is a **surgical-procedure / radiographic-group contrast**, not a pain-versus-no-pain contrast; the pain-relevant analysis is the secondary Spearman correlation with `%nprs20delta`, which is a *percentage improvement* in NRS (median ≈ 59 in the available n = 56), i.e. a construct of postoperative *recovery*, not of CPSP *development*. (ii) The follow-up timepoint at which `%nprs20delta` was measured is not stated anywhere in the manuscript, the supplement, or the result files I read. (iii) These two facts sit awkwardly beside the blanket statement "no analysed dataset captures established chronic postsurgical pain (>3 months)": if the NRS change was ascertained at ≥3 months (typical for spine surgery), the human layer *is* a ≥3-month postsurgical pain cohort and the blanket statement is wrong; if it was ascertained earlier, the manuscript must say so.

**Why it matters.** The human layer is one of the paper's three honest nulls. Scoping it as "a blood-proxy null" is necessary but not sufficient: a reader cannot judge the null without knowing what phenotype and timepoint were tested, and the current wording allows the human layer to be read as a CPSP test when it is (at best) a postoperative-recovery test in a degenerative-spine cohort.

**Concrete fix.** Replace the opening sentence of Results line 70 with:

> "In GSE158825 (n = 60 human plasma miRNA; patients undergoing surgery for lumbar spinal stenosis with or without degenerative spondylolisthesis), the primary contrast is a **surgical-procedure contrast** (LSS+DS vs LSS) and the pain-relevant analysis is the association of plasma miRNA with the percentage change in NRS pain (`%nprs20delta`; n = 56; median 59) measured at [STATE FOLLOW-UP INTERVAL — and, if <3 months, say so explicitly]. Neither reached FDR significance (LSS+DS vs LSS: min p = 1.3 × 10⁻⁴, FDR 0.128; %nprs20delta: min p = 8.5 × 10⁻⁴, FDR 0.556)."

and add to the same paragraph: "Accordingly, this null is scoped as a plasma-proxy null in a degenerative lumbar-spine surgical cohort tested against postoperative pain *improvement*, not as a test of CPSP incidence; if the outcome was ascertained before 3 months it does not address established CPSP, and if after 3 months it addresses pain improvement after decompressive surgery rather than persistent postsurgical pain."

---

#### F6 (T2) · Title claim "Conserved" is not supported by the heterogeneity the manuscript reports

**Location.** Title (line 1); the word recurs implicitly in Abstract ("A 4,055-gene core emerged") and Discussion.

**What is wrong.** "Conserved" is the strongest available claim about cross-model/cross-species stability, and the manuscript's own numbers contradict it: the random-effects core is 1,008 genes (24.9% of the fixed-effect core), median I² = 38.8% genome-wide and **72.8% across the hubs**, with only 18/35 hubs retaining FDR_RE < 0.05. The manuscript is scrupulous about this everywhere else ("heterogeneity-sensitive", "FE-conditional"). The title is the one place where the hedge is dropped.

**Fix.** Either change "Conserved" to "Recurrent" or "Concordant" (suggested title: "*A nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null*"), or retain "Conserved" and add to the Abstract's first Results sentence: "'Conserved' here denotes recurrence in direction across five studies under a fixed-effect combination, not stability of membership: only 24.9% of the core persists under random effects (median I² across hubs 72.8%)."

---

#### F7 (T2) · "Gene-set tests **confirmed** a neuroimmune/DAM-like programme" over-claims a reanalysis result

**Location.** Abstract, Results (line 18).

**What is wrong.** "Confirmed" implies a pre-specified hypothesis was verified. In a bulk-tissue reanalysis whose set-level q (0.003) is explicitly an upper bound pinned at the 2,000-permutation resolution floor (1/2001), and whose OXPHOS limb dies under random effects (q = 0.31), "confirmed" is stronger than the design supports. The rest of the manuscript uses correctly hedged language ("revealed", "identified", "recapitulated"); the Abstract word is out of register with it.

**Fix.** Replace "Gene-set tests confirmed a neuroimmune/DAM-like programme (q = 0.003 each)" with "Gene-set tests recapitulated a coordinated neuroimmune/complement and DAM-like programme under fixed effects (set-level BH q = 0.003 each; the q is an upper bound at the 2,000-permutation resolution floor)".

---

#### F8 (T2) · Methods states that the analysed GSE267799 contrast pools two models and 36 vs 24 samples; the analysed contrast is SMIR-DRG only, 12 vs 8

**Location.** Methods, "Sensitivity analyses", line 158: "GSE267799 pools two incision-type postoperative pain models — SMIR (n = 60 across DRG/muscle/skin) and lateral paw incision (LPI; n = 48) — and the 'chronic' contrast merges day-10 and day-32 samples (36 chronic vs 24 baseline at 0d)."

**What is wrong.** Per the processed data, the contrast actually entering the meta is **SMIR DRG only, chronic (10 d + 32 d) vs baseline (0 d), n = 12 vs 8** (`results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`, n_case = 12, n_ctrl = 8; `results/P2_RESULTS.md`; and the meta weight 2.19 = √(12·8/20) quoted in Methods line 152). The LPI arm and the muscle/skin tissues are in the accession but not in the analysed contrast. As written, the sentence implies the analysed contrast contains both models and 60 samples, which will not reproduce for anyone checking the tables. (This is also squarely in A3's lane — flagged cross-cutting.)

**Fix.** Replace with: "GSE267799 contains two postoperative models (SMIR and lateral paw incision, LPI) across three tissues; **the contrast used here is the SMIR DRG arm only — chronic (10 d + 32 d pooled) vs baseline (0 d), n = 12 vs 8** — so the accession-level counts (60 SMIR samples across DRG/muscle/skin, 48 LPI samples) are not the analysed n; the LPI arm and the muscle and skin tissues were not used."

---

#### F9 (T2) · Fig. 2 legend misstates the cross-animal folds

**Location.** Fig. 2 legend (line 302–303): "Cross-animal held-out datasets (**three folds**) reach leakage-controlled AUC 1.000 for GSE278227 (CCI rat DRG, n = 28) and GSE212311 (CCI, n = 6); the incision fold (GSE267799, n = 20) falls to leakage-controlled 0.677 [0.374, 0.940], the cross-animal LODO floor that includes chance."

**What is wrong.** Verified against `results/tables/P3_lodo_auc_ci_leakage_controlled.csv`: five leakage-controlled folds — GSE278227 1.000 (n = 28), GSE267799 incision 0.677 (n = 20), GSE241361 mouse DRG 1.000 (n = 9), GSE241361 mouse SC 1.000 (n = 9), GSE212311 1.000 (n = 6). There are three *cross-animal* folds (rat: 278227, 212311, 267799-incision) but only **two** of them reach 1.000; the third is 0.677. As written, the sentence says three folds reach 1.000 and then describes only two. (Cross-cutting: A2 owns the statistics; I flag it because I read the source file.)

**Fix.** Replace with: "Of the five leakage-controlled folds, four reach AUC 1.000 — GSE278227 (CCI rat DRG, n = 28), GSE212311 (CCI rat DRG, n = 6) and the two same-animal GSE241361 folds (mouse DRG n = 9; mouse spinal cord n = 9); the incision fold (GSE267799, n = 20) is 0.677 [0.374, 0.940]. Among the three genuinely independent cross-animal folds, two reach 1.000 and the incision fold is the floor that includes chance."

---

### T3 — minor

---

#### F10 (T3) · ADRA2A's biological link is described as "descending anti-nociception" for a DRG-derived signal

**Location.** Table 3a Panel A (line 98): "α2A adrenergic receptor; established descending anti-nociception."

**What is wrong.** α2A-mediated analgesia is classically described as descending (locus coeruleus → spinal dorsal horn) — but the gene here is measured in DRG, i.e. the peripheral pole, where α2A acts on primary afferents (and where systemic/clonidine-like agonism also reduces afferent excitability). Attributing a descending mechanism to a DRG-derived up-regulation is a small tissue-attribution slip of exactly the kind the manuscript is otherwise careful about. (The up-regulation itself is verified: meta_Z +4.84, 6/6 up.)

**Fix.** Change the cell to: "α2A adrenergic receptor; established analgesic pharmacology (descending noradrenergic and peripheral/DRG α2A components); the present signal is DRG-level and does not itself establish a descending mechanism."

---

#### F11 (T3) · Reference 38 (Chen et al. 2018) has a published Erratum that should be cited

**Location.** References, line 267.

**What is wrong.** Chen et al., *Cell Reports* 22:2307–2321 (2018) carries an Erratum: Chen J. et al., *Cell Reports* 38(4):110308 (2022). Not citing it is a minor reference-fidelity issue. (The substance of the citation is correct — I verified that the paper identifies α2δ-1 as "a binding site of gabapentinoids" and shows nerve-injury-dependent α2δ-1–NMDAR trafficking, so the manuscript's α2δ-1 claim is accurate.)

**Fix.** Append "; erratum: *Cell Reports* **38**, 110308 (2022). https://doi.org/10.1016/j.celrep.2022.110308" to reference 38.

---

#### F12 (T3) · Reference list is out of numerical order around the entries most relevant to this lane

**Location.** References, lines 239–269: order runs …24, 25, **27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 39, 38, 26**.

**What is wrong.** Reference 26 (Yu 2020, DRG macrophages — the citation that carries the F4 fix) appears last, after 39 and 38. Mechanical, but it affects exactly the four references (26, 38, 39, plus the new 40 requested in F3) that carry this review's domain corrections, and it will be read as sloppy by a pain-literate reviewer. (Cross-cutting: A4 owns reference formatting; flagged because it touches my lane's citations.)

**Fix.** Renumber so the list is monotonic (…24, 25, 26, 27…37, 38, 39) and update the in-text markers accordingly; note that ref 26 currently appears only in the Discussion/Limitations and ref 39 only in Methods, so the renumbering is small.

---

#### F13 (T3) · "IL/CL" is never expanded

**Location.** Throughout (e.g. Methods line 150 "GSE278227 1-week IL/CL"; Table 1a source notes; DEG filenames).

**Fix.** Define at first use: "ipsilateral vs contralateral L4–L5 DRG (IL/CL), pooled across sexes". Note also that contralateral DRG is the control here, which is worth one clause: contralateral tissue is not an uninjured reference in the strict sense.

---

#### F14 (T3) · Spinal snRNA localisation does not state which condition the cells came from

**Location.** Results, "Hubs are a multi-cellular DRG-centred, spinal-localised programme" (line 78) and Methods "Single-cell & spatial localisation" (line 172).

**What is wrong.** GSE328175 contains both Sham and SNI cells (verified: `P5_GSE328175_SC_ShamSNI_qc_summary.csv`, groups Sham 23,191 cells / SNI 31,121 cells, 6 samples), but the manuscript does not say whether the lineage-assignment denominators pool Sham+SNI, use Sham only, or use SNI only — which matters because the same section is scrupulous about stating that the Visium tissue is Sham-only. Since the paper's whole localisation claim is "constitutive baseline anatomy, not injury-induced recruitment", the reader needs the matching statement for the snRNA layer.

**Fix.** Add: "Spinal lineage assignment pools Sham and SNI nuclei in GSE328175 (23,191 Sham / 31,121 SNI cells across 6 samples); as for Visium, these are therefore anatomical/anatomical-compartment assignments, not injury-induced localisation shifts, and no Sham-vs-SNI comparison of hub localisation is claimed."

---

## Independently verified

All numbers below were read directly from the source files; every figure quoted in the manuscript matched the source unless stated otherwise.

| # | Claim in manuscript | Value I read | Source file |
|---|---|---|---|
| 1 | ADRA2A full-library docking AUC 0.532, p = 0.118 (NS) | `auc = 0.5324652`, `p_auc_mwu_onesided = 0.1184085` | `results/tables/P6_breadth_chembl_power.csv` (row symbol=ADRA2A, set=full_library, n=3070, n_actives=115) |
| 2 | ADRA2A Tier-1 (620-drug) AUC 0.618 | `auc = 0.6183677` (set=t1_only, n=620, n_actives=88) | same file |
| 3 | ADRA2A MW-adjusted AUC 0.578 | `auc_mw_adjusted = 0.5783138` (vs size-only baseline 0.4618) | same file |
| 4 | ADRA2A size-independent BH q = 0.0025; raw BH q = 0.118 | `BH_q_size_indep = 0.0025`, `BH_q_raw_enrich = 0.1184` | `results/tables/P6_BH_correction.csv` |
| 5 | OXPHOS gene set: FE q = 0.020, RE q = 0.31 | FE `perm_q = 0.0202399`; RE `perm_q = 0.3103448` (RE mean_Z −0.934 vs FE −2.373) | `results/tables/_R4_geneset_setlevel_bh.csv` |
| 6 | Neuroinflammation / complement / DAM q = 0.003 under both FE and RE | FE and RE `perm_q = 0.0029985` for all three (RE mean_Z 2.00/1.88/2.07 vs FE 4.94/3.44/3.88 — effect sizes roughly halved but still at the permutation floor) | same file |
| 7 | ADRA2A meta_Z 4.84, meta_FDR 1.5e-5, consistency 1.00 | `meta_Z = +4.83699`, `meta_FDR = 1.5089e-05`, consistency 1.0, 6/6 up | `results/tables/META_DRG_axis_stouffer.csv` |
| 8 | Table 1b bulk SCN meta_Z/FDR: SCN9A −2.92/0.011, SCN10A −3.03/0.008, SCN11A −3.41/0.003, SCN8A −4.92/1.0e-5 | −2.9247/0.01078; −3.0337/0.00795; −3.40796/0.00264; −4.92357/1.009e-05 (all four: 3/4 down, incision up) | `results/tables/META_bulkonly_meta.csv` |
| 9 | Table 1b per-contrast SCN directions (incision up; CCI/SNI down) | e.g. SCN9A incision +0.607, GSE212311 −0.073, GSE278227 −0.285, GSE241361 −2.710 | `results/tables/META_DRG_axis_stouffer.csv` (lfc columns) |
| 10 | DAM hallmarks: TYROBP FDR 8.8e-9 (5/5), TREM2 FDR 1.3e-3 (5/6), APOE consistency 6/6 with FDR 0.070 (not significant) | TYROBP K=5, consistency 1.0, FDR 8.807e-09; TREM2 K=6, consistency 0.833, FDR 1.299e-03; APOE K=6, consistency 1.0, FDR 0.0697 | `results/tables/META_DRG_axis_stouffer.csv` |
| 11 | 32/35 hubs in meta core; REG3B, MEGF11, ANKRD1 out | `in_meta_core` False for exactly REG3B, ANKRD1, MEGF11 | `results/tables/P3_hub_genes.csv` |
| 12 | CDHR5 up in all four bulk contrasts, log₂FC +0.07 to +2.62 | K=4, consistency 1.0, lfc +0.430 / +0.736 / +2.620 / +0.066 | `results/tables/META_DRG_axis_stouffer.csv` |
| 13 | ATF3 and SPRR1A up in 6/6 | ATF3 meta_Z +10.53, SPRR1A +8.18, both consistency 1.0, 6 up | same file |
| 14 | **Not reported in the manuscript:** CACNA2D1 | meta_Z **+7.96**, meta_FDR **5.95e-13**, consistency 1.0, 6/6 up | `results/tables/META_DRG_axis_stouffer.csv` (basis of F3) |
| 15 | LODO: 4/5 folds AUC 1.000; incision 0.677 [0.374, 0.940]; two same-animal GSE241361 folds | 1.000 (n=28), 0.677419 [0.37354, 0.94049] (n=20), 1.000 (n=9), 1.000 (n=9), 1.000 (n=6) | `results/tables/P3_lodo_auc_ci_leakage_controlled.csv` (basis of F2, F9) |
| 16 | SMIR hypersensitivity "dissipated by postoperative day 32" (ref 39, used to justify the day-32 dilution argument) | Verbatim from Flatters 2008 abstract: "persisted until at least postoperative day 22 and had dissipated by postoperative day 32" — **citation correct**; same paper: "very little to no degeneration was detected with ATF3 staining in DRG from SMIR-operated rats… not driven by neuronal damage" (basis of F1) | Flatters SJL, *Pain* 135:119–130 (2008), PMID 17590272, PMC2278124 |
| 17 | "α2δ-1 … gabapentinoid binding site" (ref 38) | Verbatim: "α2δ-1, commonly known as a voltage-activated Ca²⁺ channel subunit, is a binding site of gabapentinoids"; gabapentinoids act by inhibiting forward trafficking of α2δ-1–NMDAR complexes — **citation correct**; erratum exists (Cell Rep 38:110308, 2022) | Chen J et al., *Cell Reports* 22:2307–2321 (2018), PMID 29490268 (basis of F11) |
| 18 | "DRG macrophages … neuroimmune sentinel after nerve injury" (ref 26) | Verbatim: "significant expansion and proliferation of macrophages around injured sensory neurons in DRG"; contribution to initiation **and maintenance**; DRG macrophages explicitly distinguished from dorsal horn microglia ("the resident macrophages of the CNS") — **citation correct** (basis of F4) | Yu X et al., *Nat Commun* 11:264 (2020), PMID 31937758 |
| 19 | 17/33 hubs assigned to dorsal horn in Visium; Sham-only, no mouse injury arm | 17 DorsalHorn rows in S2; `P5_GSE325938_note.md`: "该 Visium 无鼠 SNI 臂" (samples Mouse_Sham1–4 + human xenograft) — **correct** | `reports/MVP_PLOSONE_supplementary.md` S2; `results/P5_GSE325938_note.md`; `results/tables/P5_GSE325938_region_annotation.csv` |
| 20 | Analysed incision contrast is SMIR DRG 12 vs 8 (vs Methods' "36 chronic vs 24 baseline") | `n_case = 12`, `n_ctrl = 8`, dataset `GSE267799_SMIR_DRG`, contrast `chronic_vs_baseline`; sample table model column = SMIR (LPI present in the accession but not in this contrast) — **discrepancy** (basis of F8) | `results/tables/DEG_GSE267799_SMIR_DRG__chronic_vs_baseline.csv`; `data/processed/GSE267799_DRG_sampletable.csv` |
| 21 | GSE158825 = human plasma miRNA, n = 60, lumbar surgery + pain outcome | Sample table: 60 samples, diagnosis LSS / LSS+DS, `nprs20delta` available (n = 56); series matrix confirms plasma miRNA, LSS cohort — **no follow-up timepoint stated anywhere** (basis of F5) | `data/processed/GSE158825_sampletable.csv`; `GSE158825_series_matrix.txt.gz_samples.csv`; `results/P4_RESULTS.md` |
| 22 | GSE328175 snRNA has Sham and SNI cells | groups: SNI 31,121 / Sham 23,191 cells, 6 samples (basis of F14) | `results/tables/P5_GSE328175_SC_ShamSNI_qc_summary.csv` |

---

## Lane-boundary notes (for the orchestrator)

- **F8 and F12** are primarily A3/A4 items (reproducibility of stated n; reference formatting); I report them because they surfaced while verifying domain claims about the incision arm and refs 26/38/39.
- **F9** is primarily A2 (result-statement consistency); reported because I read the authoritative CSV.
- I did not assess: the Stouffer weighting algebra, the permutation/BH machinery, the DeLong intervals, the docking parameter fidelity, or the Vina protocol — all A2/A3.
- I did not read any prior-round review file, and I did not read the STROBE or compliance checklists.
