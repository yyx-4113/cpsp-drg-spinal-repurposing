# Round 8 — Independent domain review (pain neurobiology / neuroimmunology)

**Reviewer:** A1 (domain: DRG–spinal pain axis, sodium-channel biology, neuroimmune–metabolic signalling)
**Manuscript:** `MVP_ScientificReports_submission.md` (reanalysis of 12 GEO datasets + 3,085-drug docking screen)
**Independence note:** This is treated as a first submission; no prior-round reviews, author responses, or panel memos were read.

---

## Executive summary

The manuscript is, from a neurobiological standpoint, unusually careful for a computational reanalysis. Most of the claims I approached skeptically — the bulk-DRG Nav-channel down-regulation being a neuronal-loss/immune-dilution artefact rather than true channel suppression, the honest Keren-Shaul (not Schafer) provenance of "DAM-like", and the circularity-controlled non-predictive incision translation — are correctly framed and honestly bounded. Three issues need correction before acceptance: (1) the blanket "Nav1.8 inhibitors have repeatedly failed clinically" is contradicted by the authors' own citation of the approved Nav1.8 inhibitor suzetrigine; (2) the SCN3A/Nav1.3 "most induced after injury" claim is defensible but uncited and over-absolute; (3) the "DAM-like" label should be more explicitly qualified as a partial, complement-weighted overlap rather than a reconstituted DAM state. The central "nerve-injury-associated, NOT CPSP-specific" boundary is defensible but rests on a single, underpowered incision arm whose CPSP-adjacency is source-asserted, not verified.

---

## § Stands up (things I suspected were wrong but found correct)

1. **Bulk DRG Nav-channel down-regulation is honestly attributed to neuronal loss / immune dilution, not claimed as true channel suppression.** I expected the authors to over-read the bulk down-regulation of SCN9A/SCN10A/SCN11A/SCN8A as biologically meaningful channel loss. Instead, `manuscript:52` explicitly states "bulk DRG signal is confounded by injury-induced neuronal atrophy/loss and by the dilution of neuronal transcripts by infiltrating immune and glial cells." This matches the established literature (axotomy reduces DRG neuron number and enriches macrophage/glia transcripts, masking true per-neuron channel states). Correct and well-bounded.

2. **DAM provenance is correctly attributed to Keren-Shaul 2017, explicitly separated from Schafer's developmental microglia.** I expected a generic "DAM = pain microglia" overclaim. Instead, `manuscript:120` writes "the DAM programme was first defined in neurodegeneration by Keren-Shaul et al.²³ … distinct from the developmental/homeostatic microglia described by Schafer et al.²⁴ — and is therefore described as DAM-like," and `manuscript:48` notes the bulk signal "cannot be attributed specifically to resident microglia versus infiltrating macrophages." Accurate provenance and honest qualifier.

3. **The non-circular translation test is genuinely circularity-controlled and does not overclaim.** I expected the authors to present the 53.9%/69.5% directional-agreement numbers as translation evidence. Instead, `manuscript:56` correctly identifies both as circular (the pooled consistency filter and meta_Z include the incision contrast) and refuses to test them against a 50% null; `manuscript:58` builds a nerve-injury-only signature and uses incision once as held-out (46.3% vs 47.1% background, p = 0.14). The negative conclusion is stronger and honestly derived. This is the manuscript's strongest methodological display.

4. **The Nav1.7 necessity-vs-injury-upregulation distinction is correct.** `manuscript:52` correctly states that germline SCN9A channelopathies (refs 11–13) establish Nav1.7 *necessity* for human pain but are *not* evidence of injury-induced up-regulation, and that selective Nav1.7 inhibitors failed clinically (refs 14,16). This is biologically accurate: Nav1.7 protein is largely unchanged in injured DRG, so loss-of-function CIP/IEM genetics do not license a "Nav1.7 is upregulated in neuropathic pain" story.

5. **SCN3A/Nav1.3 is flagged as untested and deferred, rather than silently omitted.** `manuscript:52` admits "the channel most transcriptionally induced after injury, SCN3A/Nav1.3, was not among the tested sets and should be examined in a revision." Honest self-auditing of a coverage gap.

---

## § Substantive issues (each with Problem / Evidence / Why it matters / Specific fix)

### Issue 1 — "Nav1.8 inhibitors have repeatedly failed clinically" is internally contradicted by the authors' own suzetrigine citation

- 【Problem】 The blanket claim that selective Nav1.8 inhibitors have "repeatedly failed clinically" is outdated and contradicts the manuscript's own reference 20 to suzetrigine, a Nav1.8 inhibitor approved for acute pain.
- 【Evidence】 `manuscript:52` states "selective Nav1.7/Nav1.8 inhibitors have repeatedly failed clinically¹⁴,¹⁵,¹⁶"; yet `manuscript:112` and `references:20` cite Divito 2026 describing "Suzetrigine: a novel nonopioid systemic analgesic," and the Discussion (`manuscript:128`) notes "such as suzetrigine²⁰." Suzetrigine (VX-548 / Journavx) is a Nav1.8 (SCN10A) inhibitor approved by the FDA in 2025 — i.e., a Nav1.8 inhibitor that *succeeded*.
- 【Why it matters】 A domain reader will immediately see the internal contradiction: the same paragraph invokes suzetrigine as a real Nav1.8 drug while asserting Nav1.8 inhibitors "repeatedly failed." This undermines the credibility of an otherwise careful sodium-channel discussion and could be seized on by reviewers as carelessness.
- 【Specific fix】 Replace with: "Selective Nav1.7 blockers have repeatedly failed in neuropathic-pain trials¹⁴,¹⁶; Nav1.8 inhibition was long unsuccessful in neuropathic indications (e.g. vixotrigine¹⁵) until the 2025 approval of the Nav1.8 inhibitor suzetrigine for acute pain²⁰, so the Nav1.8 clinical track record is mixed rather than uniformly negative, and neither channel's failure licenses a CPSP-specific up-regulation narrative."

### Issue 2 — SCN3A/Nav1.3 "most transcriptionally induced after injury" is uncited and over-absolute

- 【Problem】 The claim that SCN3A/Nav1.3 is "the channel most transcriptionally induced after injury" is biologically defensible but stated without a primary citation and in absolute terms that over-reach relative to the literature.
- 【Evidence】 `manuscript:52`: "Notably, the channel most transcriptionally induced after injury, SCN3A/Nav1.3, was not among the tested sets and should be examined in a revision." No citation anchors the "most induced" assertion.
- 【Why it matters】 Among voltage-gated sodium channels SCN3A/Nav1.3 is indeed the most robustly *up*-regulated after peripheral axotomy (small DRG neurons), but the absolute superlative invites challenge and is unsourced. A domain reviewer expects the primary axotomy literature (Black/Waxman/Dib-Hajj) to be cited; its absence looks like a literature gap.
- 【Specific fix】 Replace with: "Among voltage-gated sodium channels, SCN3A/Nav1.3 is the most strongly and consistently transcriptionally induced after peripheral axotomy (Black et al. 1999/2001; Dib-Hajj & Waxman 2007) and was not among the tested sets; it should be examined in a revision."

### Issue 3 — "axotomized IB4+ neurons" is an imprecise locus for the Nav1.8 down-regulation

- 【Problem】 Describing SCN10A/Nav1.8 down-regulation as occurring in "axotomized IB4+ neurons" is biologically imprecise because axotomized DRG neurons down-regulate IB4 binding, so the surviving Nav1.8+ population is not cleanly IB4+.
- 【Evidence】 `manuscript:52`: "SCN10A/Nav1.8 mRNA is down-regulated in axotomized IB4+ neurons." The IB4+ (non-peptidergic) subclass largely loses its IB4/GDNF-receptor phenotype after axotomy, so "IB4+" is a pre-injury descriptor.
- 【Why it matters】 A neurobiology reader will flag the cell-type label as technically loose; it does not invalidate the down-regulation claim (Nav1.8 is indeed reduced in small DRG neurons after axotomy) but exposes the sentence to a trivial correction that distracts from the substantive point.
- 【Specific fix】 Replace with: "SCN10A/Nav1.8 mRNA is down-regulated in axotomized small/non-peptidergic DRG neurons (which largely lose IB4 binding after injury), and bulk DRG signal is confounded by injury-induced neuronal atrophy/loss and by dilution of neuronal transcripts by infiltrating immune and glial cells."

### Issue 4 — "DAM-like" should be more explicitly qualified as a partial, complement-weighted overlap, not a reconstituted DAM state

- 【Problem】 The "DAM-like" label risks implying a Trem2/Apoe-dependent disease-associated-microglia state, but the authors' set is dominated by complement (C1QA/B/C) and cytokines that are also in generic neuroinflammation, and bulk tissue cannot resolve microglia from infiltrating macrophages.
- 【Evidence】 `manuscript:48` notes "C1QA/B/C appear in both complement and the DAM-like set, and cytokines such as IL6/TNF/CCL2 in both neuroinflammation and DAM-like," and `manuscript:120` states the DAM-like set "follows that neurodegeneration-defined provenance." True DAM (Keren-Shaul) requires the Trem2–Tyrobp–Apoe axis; no Trem2/Apoe evidence is shown in this bulk signal.
- 【Why it matters】 Calling a complement/cytokine-enriched bulk signature "DAM-like" is acceptable as a homology label, but without stating that it lacks the defining Trem2/Apoe axis it overstates microglial-state specificity and could be read as claiming a verified DAM reprogramming in pain — which the data cannot support.
- 【Specific fix】 Add to `manuscript:120` after the DAM-like sentence: "We note that true DAM requires the Trem2–Tyrobp–Apoe axis, which is not resolved in our bulk signal; the present programme is therefore a complement- and cytokine-weighted neuroimmune activation that resembles DAM only partially, and we retain the 'DAM-like' qualifier to avoid implying a reconstituted microglial state."

### Issue 5 — The negative incision translation is underpowered and should not bear the full weight of the "NOT CPSP-specific" boundary

- 【Problem】 The conclusion that the axis is "nerve-injury-associated, NOT CPSP-specific" leans on a single incision arm whose CPSP-adjacency is source-asserted and whose negative translation is statistically weak (p = 0.14, one dataset).
- 【Evidence】 `manuscript:58` reports 46.3% vs 47.1% background, p = 0.14; `manuscript:146` states "the exact chronic harvest day is not stated in the deposited metadata … could not be verified … the incision→nerve-injury translation is reported as a conservative bound from a single incision arm"; `manuscript:14` notes "only one is a surgical-incision model."
- 【Why it matters】 The boundary claim is the manuscript's headline contribution. A single, unverified, underpowered incision dataset cannot *establish* absence of CPSP-specificity; it can only fail to demonstrate prediction. Over-reading it as proof of the boundary invites rejection on biological-grounds that the authors partly anticipate but do not fully hedge in the Abstract/Conclusions (`manuscript:20`).
- 【Specific fix】 In `manuscript:20` (Conclusions) and `manuscript:120`, soften to: "In the single available incision arm — whose CPSP-adjacency is source-asserted and unverified and which is underpowered (p = 0.14) — the nerve-injury signature did not predict incision direction; this supports, but does not prove, a nerve-injury-associated rather than CPSP-specific axis and should be read as a conservative bound pending additional postsurgical datasets."

### Issue 6 — OXPHOS "down-regulation" framing should cite the mechanistic (not merely correlative) mitochondrial-pain literature

- 【Problem】 The metabolic claim is honestly bounded as fixed-effect-only (q = 0.31 under random effects), which is good, but the Discussion cites only correlative/metabolic-dysfunction literature and omits the causal DRG mitochondrial-pain work that would strengthen the biological plausibility.
- 【Evidence】 `manuscript:120` cites Haque 2024 and Kong 2023 for "energy-metabolism dysfunction in chronic and neuropathic pain"; `manuscript:48` reports OXPHOS mean_Z −2.37 (fixed) not surviving random effects (q = 0.31).
- 【Why it matters】 The hedging is correct, but the biological interpretation would be stronger and more current if it acknowledged that DRG mitochondrial pyruvate-oxidation disruption *causes* nociceptor sensitization (mechanistic), not just "dysfunction associates with pain." Minor, but it tightens the metabolic claim.
- 【Specific fix】 In `manuscript:120`, append: "with causal evidence that disrupting DRG mitochondrial pyruvate oxidation drives persistent nociceptor sensitization (Haque et al. 2024), the fixed-effect OXPHOS signal is biologically plausible even though it is not reliable under between-contrast heterogeneity."

---

## § Questions for the authors (do not guess; I need to know)

1. **DAM member composition.** What are the actual members of the "DAM-like" set (Supplementary Table S5)? Do they include Trem2, Tyrobp, Apoe, Cst7, Lpl — the defining Keren-Shaul axis genes — or is the set essentially complement (C1qa/b/c) + cytokines? This determines whether "DAM-like" is a homology label or an overclaim.
2. **Cellular resolution of the neuroimmune signal.** Bulk DRG/spinal RNA cannot separate resident microglia from infiltrating macrophages. Do the single-cell data (GSE216039/GSE328175) permit any estimate of what fraction of the DAM-like/complement signal is microglial vs macrophage? If not, the "DAM-like" label rests entirely on bulk homology.
3. **SCN per-neuron validation.** The bulk Nav down-regulation is attributed to neuronal loss/immune dilution. Is there any single-neuron or snRNA evidence in the reanalysed data (GSE216039) for the true per-neuron direction of SCN9A/SCN10A/SCN11A after injury, to support the bulk-confound explanation?
4. **Incision model details.** For GSE267799, can the chronic harvest day be recovered from the original publication (not just GEO metadata)? The CPSP-adjacency of the entire translation argument hinges on this.
5. **Suzetrigine scope.** Was suzetrigine approved for *acute* (not chronic/CPSP) pain, and do the authors intend the Nav1.8 "mixed track record" fix to reflect that acute-vs-chronic distinction? (I assume yes; please confirm in the revision.)

---

## § What I actually checked

- **Files read:** only `reports/MVP_ScientificReports_submission.md` (full text, lines 1–283). No prior-round reviews, RESPONSE/REVISION memos, author-verification statements, `.workbuddy/memory/`, or other panellists' files were opened, per the independence embargo.
- **Primary-literature claims verified against domain knowledge (not re-run scripts):**
  - SCN9A germline channelopathies (IEM/PEPD/CIP) establish necessity, not injury up-regulation — correct (Yang 2004; Cox 2006; Fertleman 2006).
  - Selective Nav1.7 blockers failed neuropathic trials — correct (PF-05089771, McDonnell 2018; Eagles 2022). Nav1.8: vixotrigine failed (Faber 2023) BUT suzetrigine approved 2025 — the blanket "failed" is outdated (Issue 1).
  - SCN10A/Nav1.8 down after axotomy — correct; "IB4+" locus imprecise post-axotomy (Issue 3).
  - SCN3A/Nav1.3 strongly up after axotomy — correct, but uncited (Issue 2).
  - DAM provenance = Keren-Shaul 2017, not Schafer 2012 — correct (Issue 4 nuance).
  - Complement C1qa/b/c in neuropathic pain — correct; CXCL12/SDF-1 dorsal-horn — correct (Luo 2016; Zhang 2017).
  - ADRA2A α2A descending anti-nociception — correct and well established.
  - OXPHOS/metabolic down-regulation bounded as fixed-effect-only — correct and honest (Issue 6).
- **Statistical/biological logic I did NOT re-verify (out of domain scope):** the Stouffer/RD meta weights, the permutation resolution floor, the docking MW-correction AUCs, and the bootstrap stability numbers. These are methods claims, not domain-correctness claims, and I accept them as reported pending the methods reviewers.

---

## § Must-cite literature the authors should add (would change or sharpen a claim)

1. **SCN3A/Nav1.3 axotomy up-regulation** — Black JA, Liu S, Hinson AW, Waxman SG. *Nature Neuroscience* 1999/2001 (or Dib-Hajj & Waxman, 2007, on Nav1.3 in injured DRG). Required to support the Issue-2 sentence.
2. **Mechanistic DRG mitochondrial–pain link** — Haque et al. 2024 is already cited; if a stronger causal paper is intended, cite e.g. the Kim/Pain 2012–2016 mitochondrial-DRG series. (Minor; addresses Issue 6.)
3. **Suzetrigine approval** — already cited (Divito 2026, ref 20); the Issue-1 fix simply reconciles the text with it.
4. **Trem2/Apoe DAM-axis definition** — Keren-Shaul 2017 (ref 23) already cited; the Issue-4 fix adds the explicit "lacks Trem2/Apoe axis" qualifier using the same reference.

No clinically or biologically FALSE statement was found that would require retraction of a conclusion; Issues 1–5 are accuracy/bounding corrections that strengthen an already careful manuscript.
