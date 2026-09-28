# A1 — Domain / Clinical-Scientific Reviewer Report
**Round:** 15 (enforced independence — no prior review files read)
**Manuscript:** "Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null"
**Version under review:** v1.5.0 (git tag v1.5.0, commit a5c610a)
**Target journal:** PLOS ONE (SCIE, Q2, accepts negative/null results)
**Author:** Yongxxin Yang (BMed; no MD/PhD/MS titles ascribed anywhere — verified)

---

## 1. Verdict
**MINOR-REVISION** — science and framing are sound and well-suited to PLOS ONE, but one **real, verifiable inconsistency** must be fixed before acceptance: the bulk-only and collapse *sensitivity-analysis companion files* (and two stale percentages carried in the manuscript text) were **not regenerated after the Round-13 core change (4,055 → 2,750 genes)**. The fix is mechanical and does not affect the reported conclusions or the core gene-set evidence. This is a hard gate, not optional polish.

---

## 2. Independent recomputation (audit of raw product files)
I recomputed the numbers the paper leans on most:

1. **Set-level BH q for the four core gene sets** — from `results/tables/_R4_geneset_setlevel_bh.csv`.
   - The four core sets (Neuroinflammation, Complement, Mitochondria_OXPHOS, DAM_microglia) each show `perm_q = 0.0022488755622188904` under **both** fixed and random effects.
   - This equals the BH-corrected q across the 18 multi-member sets: the four tied floor p-values (1/2001 ≈ 0.0004997501) occupy ranks 1–4, so `q = 0.0004997501 × 18 / 4 = 0.002248875…` ✓ exactly matches. **Verdict: reported q = 0.0022 is correct and correctly applied under random effects too** (OXPHOS surviving RE is genuine).

2. **Strict non-circular stratum** — from `results/tables/_R4_nerveinjury_only_summary.json`, stratum `NI_FDR05_AND_NIcons>=0.8`:
   - k = 1,660 / n = 3,830 → **43.3%**; background `all_measured` k = 6,772 / n = 14,390 → **47.1%**; `perm_p = 0.00019996 ≈ 0.0002`. I confirmed 1660/3830 = 43.3% and 6772/14390 = 47.1%. ✓ **Matches the manuscript exactly.**

3. **Core size** — `results/tables/META_DRG_axis_CORE_signature.csv` contains **2,750 data rows** ✓ matches the abstract/results/methods "2,750-gene core". The 508-gene RE core (508/2750 = 18.5%) is consistent with `supplementary line 202`.

4. **Abstract word count** — 286 whitespace words ✓ ≤ 300 (PLOS ONE limit).

5. **ADRA2A P6 source** — `results/tables/P6_BH_correction.csv` ADRA2A row: `0.532, 0.118, …, 0.0025` ✓ matches supplementary Table S4 Panel B (AUC 0.532, raw p = 0.118, size-independent BH q = 0.0025). The AUC 0.618 (Tier-1 subset) appears in text and pack — consistent.

**Conclusion of audit:** the headline mechanism evidence (q = 0.0022) and the honest-negative translation statistic (43.3% vs 47.1%, p = 0.0002) are accurate and reproducible. The deposited derived tables that broke are the *sensitivity-analysis companions*, not the primary gene-set/core files.

---

## 3. A1 Focus Assessment

### (1) Hub-gene neuroinflammation / DAM / complement↑ · OXPHOS↓ mechanism — COHERENT, not overclaimed
The four programmes are genuinely coordinated and polarity-opposed (neuroimmune/complement/DAM up; OXPHOS down), all at set-level BH q = 0.0022, **under both fixed and random effects** (verified). The paper correctly notes these sets share many members (C1QA/B/C, IL6/TNF/CCL2) so the *effective number of independent discoveries is ≈1*, and explicitly re-describes them as **one coordinated neuroimmune–complement axis** rather than three independent hits. This is appropriate restraint. The DAM qualifier is justified biologically (TYROBP/TREM2 in the FDR<0.05 core; APOE directional but FDR 0.070) rather than metaphorical. **No overclaim.**

### (2) Honest-negative framing — CANDID, NON-DEFENSIVE, a genuine strength
- Human plasma miRNA layer: p = 0.51, explicitly "failure to detect, not evidence of absence," scoped as a blood-proxy boundary (n = 60, underpowered).
- Single-cell: 0 BH-significant genes; all calls labelled "directional hints."
- Full-library docking: no target clears both filters; ion-channel class undockable so the null "cannot speak to those targets."
- ADRA2A downgraded (see #3).
The negatives are framed as **methodological boundaries**, not failures, and are integrated into the paper's contribution narrative. This is exactly the rigor PLOS ONE's negative-results policy rewards. **No undermining of contribution.**

### (3) ADRA2A downgrade — INTERNALLY CONSISTENT (with one minor watch)
- Abstract: ADRA2A is cited only as the *example of the failed filter* (0.618 → 0.532, p = 0.118), never as a finding.
- Main text: "We hold ADRA2A to the same single standard as the other nine targets… neither prioritised nor excluded"; "ADRA2A remains weak and non-informative." Correctly distinguished from the main line.
- Supplementary S3/S4: "control-evaluable but did not pass"; "ADRA2A remains weak/non-informative."
- STROBE/Compliance: listed only as illustration of the breadth flip; competing-interest disclosure (pending grant lists ADRA2A) present.
**Minor watch:** S4 Panel B notes "only ADRA2A's weak size-independent p survives BH (q = 0.0025)." This is technically true (MW-adjusted ΔAUC p = 0.0005 → q = 0.0025 across the 5 targets) but could be cherry-picked by a careless reader as a "significant" ADRA2A signal. The manuscript pre-empts this well ("the MW-adjusted ΔAUC does not override the failed full-library enrichment 0.532, p = 0.118"), so it is a *watch*, not a defect. No change strictly required; consider one bolded caveat in S4.

### (4) Contribution argument for PLOS ONE — CLEAR and convincing
The paper's value is (a) a rigorously bounded, heterogeneity-honest DRG–spinal-axis meta-analysis, and (b) a prospectively specified full-library repurposing screen whose null is methodologically informative. Both are explicitly positioned against the field's "Tier-1 double-dipping" habit and PLOS ONE's stated appetite for negative results. The contribution is argued, not asserted.

### (5) Clinical/biological plausibility of hubs and the DRG–spinal axis — PLAUSIBLE
- Established DRG-injury/pain markers recovered: ATF3 (rank 1, meta_Z 10.53), SPRR1A, NPY, VIP, ECEL1, GAL, FLRT3, SOCS3 — strong face validity.
- **CACNA2D1 (α2δ-1, the gabapentinoid target)** reproduced as up-regulated (meta_Z +7.09, FDR 2.3e-10) — an independently validating, clinically congruent signal; the ion-channel undockability is honestly scoped.
- Annotation outliers (CDHR5, ANKRD1, FLNC, CRISP3, MEGF11) are flagged, not concealed; CDHR5 is correctly demoted to a watch-list.
- DRG→spinal localisation (17/33 hubs in dorsal horn at baseline) is appropriately caveated as constitutive anatomy, not injury recruitment.
The axis for CPSP is correctly framed as **nerve-injury-associated, not CPSP-specific** (single heterogeneous incision arm). Plausible and honest.

### (6) Title & abstract — accurate, no hype, within word limit
- Title: "…an honest repurposing null" — matches content.
- Abstract: 286 words (≤300), no hidden positives, no puffery; the honest negatives (43.3% vs 47.1% depletion; p = 0.51; 0.532 NS; undockable ion channels) are all present.
- **Minor:** the word "Conserved" in the title is slightly optimistic given the RE collapse to 508 (18.5%) and the explicit "recurrence in direction, not stability of membership" definition. The abstract disambiguates, so this is a low-severity stylistic note, not a block.

### (7) Overclaiming / underclaiming / gaps that would block acceptance
- **Real bug (the one gate):** see §4, "REAL-BUG" item B1. The sensitivity-analysis companion files contradict the manuscript's own 2,750-gene core.
- No other blocking gaps found. Causal scope is explicitly disclaimed; AI-use is disclosed; ethics/data-availability are complete (GitHub v1.5.0, MANIFEST.sha256, no phantom Zenodo DOI — verified 0 occurrences of `10.5281/zenodo`).

---

## 4. Issues — categorised

### REAL-BUG (must fix before acceptance)
**B1. Stale core size in sensitivity-analysis companions + residual stale percentages in text.**
- `results/tables/META_bulkonly_sensitivity_summary.json`: `primary_core_size: 4055`, `overlap: 2202`, `overlap_pct_primary: 54.3157`. This is the **pre-Round-13 4,055-gene core**; the current primary core is **2,750** (verified in `META_DRG_axis_CORE_signature.csv`, 2,750 rows). 2202/4055 = **54.3%** — i.e. the very "54.3%" overlap the manuscript still cites.
- `results/tables/META_collapse_meta.csv`: `orig_core: 4055.0`, `retained_fraction: 0.9142` — the **91.4%** collapse retention is likewise computed on the stale 4,055 core.
- Manuscript text still carries both stale figures: line 44 "bounded by the bulk-only (overlap 54.3%) and collapse (retention 91.4%)"; line 50 "The 54.3% figure is the conservative, threshold-strict overlap…" — **in the same paragraph it also states the correct 1,737/2,750 = 63.2%**, an open internal contradiction.
- The Data Availability statement lists these JSON/CSV as authoritative derived tables, so a reviewer pulling them sees the conflict immediately.
- **Fix:** (i) regenerate `META_bulkonly_sensitivity_summary.json` and `META_collapse_meta.csv` against the current 2,750-gene core; (ii) in lines 44 & 50 replace the stale "54.3%" / "91.4%" with the regenerated, core-consistent figures (or, if 63.2% is the intended bulk-only overlap, delete the 54.3%/91.4% references entirely). The round-14 commit claimed a "stale-number sweep" — this corner was missed.

### ALREADY-FIXED (verified, no action)
- F1. Core size corrected 4,055 → 2,750 (Round 13) — confirmed in the actual core CSV (2,750 rows) and throughout abstract/results/methods.
- F2. ADRA2A downgraded to control/baseline — consistent in abstract, text, S3/S4, STROBE, compliance.
- F3. No phantom Zenodo DOI — 0 occurrences; DA correctly cites versioned GitHub v1.5.0.
- F4. Abstract within 300-word limit (286).
- F5. Gene-set BH q = 0.0022 verified correct under both FE and RE.

### REVIEWER-MISREAD (none) / clarifications
- C1. The supplementary "ADRA2A size-independent q = 0.0025 survives BH" is **not** a misclaim — it is the MW-adjusted ΔAUC, and the manuscript correctly subordinates it to the failed raw full-library enrichment (0.532, p = 0.118). Not a defect; listed only as a watch in §3(3).
- C2. "median I² 79.1%" in the abstract attaches to the 508/RE-hub context; the manuscript clarifies (line 46) it is the hub-subset I², with genome-wide median I² = 41.8%. Consistent, not an error.

---

## 5. Recommendations (priority order)
1. **[GATE]** Regenerate the two stale sensitivity companions (B1) and purge the 54.3%/91.4% figures from lines 44/50. Re-run the gate check.
2. Add a one-line bolded caveat in supplementary S4 next to the ADRA2A q = 0.0025 row: "size-independent MW-adjusted p only; raw full-library enrichment non-significant (0.532, p = 0.118), so ADRA2A remains inconclusive/baseline."
3. [Optional, low severity] Soften or footnote the title's "Conserved" (e.g., "recurrently coordinated") to avoid over-reading given the 18.5% RE persistence; the abstract already qualifies it.
4. [Doc nit] The compliance checklist (line 74) still describes the DA statement as citing "v1.3.0"; the manuscript now correctly says v1.5.0. Update the checklist text to avoid confusion.

---

## 6. Summary statement (for editorial triage)
**Verdict: MINOR-REVISION.** The sanctioned neuroimmune/DAM/complement↑·OXPHOS↓ mechanism is coherent, BH-corrected (q = 0.0022, verified under both fixed and random effects), and not overclaimed. The honest-negative results (human p = 0.51; 0 single-cell BH hits; no target clears both docking filters; ADRA2A downgraded to baseline) are candid, non-defensive, and constitute a genuine PLOS ONE-fit contribution. ADRA2A is consistently treated as control, never lead. Title/abstract are accurate and within the 300-word limit. One real, mechanical defect blocks acceptance: the bulk-only and collapse *sensitivity-analysis companion files* (and two residual "54.3%"/"91.4%" text references) were not regenerated after the Round-13 core change (4,055 → 2,750 genes) and now contradict the manuscript's own 2,750-gene core. Fixing these files and the two stale percentages is the single required action.
