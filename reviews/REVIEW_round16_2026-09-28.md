# REVIEW — Round 16 (2026-09-28) · PLOS ONE resubmission (v1.6.0)

**Manuscript:** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null* (single author; target: PLOS ONE).
**Version under review:** `v1.6.0` (tag `4813a28`, confirmed via `git ls-remote` by the editor).
**Panel:** 4 independent experts, **enforced-independence** (no access to prior review/response/compliance/archive files).
**Editor's role:** consolidate, and **independently re-verify every severe finding from raw data** (not trusting the subagents — see §3 "editor re-verified" and §7).

---

## 1. Independence declaration (mechanism + evidence)

**Mechanism.** Each expert received only `reports/MVP_PLOSONE_submission.md`, the authoritative `results/tables/*` files enumerated in `_PANEL_BRIEF.md`, and the PLOS ONE/STROBE artefacts they needed. The brief explicitly forbade reading `REVIEW_round*`, `round*_panel_*`, `RESPONSE_*`, `REVISION_*`, `MVP_PLOSONE_compliance_check.md`, `SUBMISSION_MANIFEST.md`, `Reporting_Summary.md`, sibling `A*` reports, and any `_archive/`/`.bak`. A fresh `round16_panel_2026-09-28/` directory was used; each subagent was a separate context with no memory of prior rounds.

**Evidence that independence held.**
- All four reports contain an explicit "Not read / Independence note" section listing the forbidden files they did **not** open.
- A1, A2, A3 each independently *recomputed* the same headline numbers and reached the same verdicts without coordination (e.g., A1 Check 2 and A2 Check 8 both flag the P6 verdict/AXL-TNIK contradiction from different angles).
- A4 performed a live GitHub tag check (`v1.6.0` → `4813a28`) that no other panel member used.
- No two reports cite the same "prior round said X" — they cite only the manuscript and the data.

**Editor's own re-verification (separate from the subagents).** I re-ran the five most severe findings directly from the raw CSV/JSON (column names `symbol`/`set`, not `gene`/`geneset`): see §3 and §7. Every severe finding below is marked **[editor re-verified]** where I personally confirmed it.

---

## 2. Verdict table

| Expert | Lens | Headline verdict | Blocking? | Key blocking / major items |
|---|---|---|---|---|
| **A1** Domain | pain neurobiology, neuroinflammation, DAM, DRG | **Revise** (minor-to-moderate) | No | MAJOR: Discussion DAM numbers wrong + "both in core" false for TREM2; P2RX/P2RY six-input p error; REG3B FDR; ADRA2A json drift; Nav1.8 mis-citation |
| **A2** Design/Stats | meta-analysis, heterogeneity, docking logic | **Minor revision** | No | Translation p floor-pinned; P6 verdict↔prose contradiction + TNIK p; resample artifacts not deposited; multivariate LR not in `results/tables`; K-H deferred |
| **A3** Impl/Provenance | reproducibility, version hygiene | **Safe on numeric grounds** | No | 0 numeric discrepancies; 4 hygiene items (MANIFEST.sha256 stray, .zenodo.json v1.0.0, release.yml, miRNA source citation) |
| **A4** Venue/STROBE | PLOS ONE format + reporting | **Technical-check query** | **Yes (mechanical)** | **Reference list not numbered by first citation** (hard-fail); CC BY only in cover letter; Author Summary over-flattened |

**Distribution:** 0 → reject / desk-reject; 0 → major revision (scientific); **4 → minor revision / revise**; 0 → accept.
**Round verdict: MINOR REVISION — NOT ACCEPT.** The scientific core is sound (all 10 mandatory counts recompute exactly), but one mechanical format hard-fail (reference ordering) and several numeric/discourse corrections must be cleared first.

---

## 3. Cross-verification table (manuscript claim vs independently recomputed)

Rows with a discrepancy are the actionable items. "Editor" = the consolidating editor re-ran the number from raw data.

| # | Manuscript location | Manuscript value | Independent recomputation (source) | Match | Verified by |
|---|---|---|---|---|---|
| 1 | Discussion (DAM hallmark) TYROBP | FDR 8.8e-9; 5/5 | 1.19e-7; 4/5 (six-input) / 2.48e-9; 3/3 (bulk) | ❌ | A1 + **editor** |
| 2 | Discussion TREM2 | FDR 1.3e-3; 5/6; "in core" | 3.04e-3; 4/6; **NOT in core** (cons 0.667 < 0.8) | ❌ | A1 + **editor** |
| 3 | Discussion APOE | FDR 0.070; 6/6 | 0.845; 4/6 (six-input) / 0.295; 4/4 (bulk) | ❌ | A1 + **editor** |
| 4 | P2RX/P2RY six-input perm-p | 0.440 | 0.5797 (`P3_geneset_stats.csv`) / 0.5607 (`_R4_geneset_setlevel_bh.csv` fixed) | ❌ | A1 + **editor** |
| 5 | P6 AXL/TNIK verdict (prose "failed size-indep") | "failed … p=0.141 / 0.579" | `verdict=PASS_size_independent`; TNIK deltaAUC_p = **0.4435** (not 0.579) | ❌ | A2 + **editor** |
| 6 | REG3B six-input FDR | 7.1e-14 | 1.38e-13 (`META_DRG_axis_stouffer.csv`) | ❌ | A1 + **editor** |
| 7 | ADRA2A `P6_target_plausibility.json` | 4.84 / 1.5e-5 / 1.0 | Table 3 / stouffer = 4.45 / 8.35e-5 / 0.833 (Table 3 canonical) | ⚠ traceability | A1 + **editor** |
| 8 | Translation perm-p | p = 0.0002 (point) | 0.00019996 = 1/5000 floor → report **p ≤ 0.0002** | ⚠ framing | A2 + **editor** |
| 9 | MANIFEST.sha256 | (compliance says "no MANIFEST exists") | File **exists** at root + `_manifest/` (15,598 / 28,392 B) | ❌ hygiene | A3 + **editor** |
| 10 | .zenodo.json version | — | `"version":"v1.0.0"` (stale; manuscript is v1.6.0) | ❌ hygiene | A3 + **editor** |
| 11 | Human-miRNA p = 0.51 source | (no cited file) | `P4_setlevel_test.json` perm_p = 0.5101, n = 253 (value correct; citation missing) | ⚠ provenance | A3 + **editor** |
| 12 | References numbered by first citation | 1…40 consecutive | First-appearance order = `[1…21,38,40,22,23,26,24,25,27…37,39]` | ❌ **format hard-fail** | A4 + **editor** |
| — | FE core | 2,750 | 2,750 (gate FDR<0.05 & cons≥0.8) | ✅ | A2/A3 + editor |
| — | RE core | 508 / 18.5% / I² 41.8% / τ² 0.266 | exactly reproduced | ✅ | A2/A3 + editor |
| — | Gene-set q | 0.0022 ×4 | 0.0022489 both FE & RE | ✅ | A2/A3 + editor |
| — | Non-circular | 43.3% / 47.1% / −3.7 pp | 1660/3830; 6772/14390; RD −3.7 pp | ✅ | A2/A3 + editor |
| — | Bulk-only | 2512; 63.2% (1322+415); 89.2%; 200 | reconciled exactly | ✅ | A2/A3 + editor |
| — | Collapse | 3582; 91.0% | 2502/2750 = 0.9102 | ✅ | A2/A3 + editor |
| — | Hubs / LODO / miRNA p / docking AUCs | as printed | all reproduced | ✅ | A1/A2/A3 + editor |
| — | Abstract | 266 words, unstructured | 266; single paragraph; no labels | ✅ | A4 + editor |
| — | Figures in docx | 5 inline ≥300 DPI | 5 PNG, 350 DPI, all inline | ✅ | A4 + editor |
| — | Data Availability | real GitHub v1.6.0, no Zenodo DOI | tag exists; named files present | ✅ | A4 + editor |

**Result:** 1 format hard-fail (ref ordering), 7 numeric/discourse errors (rows 1–7), 3 hygiene/provenance items (9–11), 1 framing fix (8). All other 13+ headline numbers reproduce exactly.

---

## 4. Graded problem list

### Tier 0 — Blocking (must fix before acceptance; mechanical, not scientific)
- **T0-1 · Reference ordering (A4 P1) — [editor re-verified].** PLOS ONE requires references numbered consecutively in order of first citation. Current first-appearance order is `[1…21, 38, 40, 22, 23, 26, 24, 25, 27…37, 39]`. Triggers a technical-check/editorial-return query and blocks acceptance. **Fix:** renumber the 40-item list to first-citation rank and rewrite every superscript callout. Mapping (current→new): `38→22, 40→23, 22→24, 23→25, 26→26, 24→27, 25→28, 27→29, 28→30, 29→31, 30→32, 31→33, 32→34, 33→35, 34→36, 35→37, 36→38, 37→39, 39→40` (1–21 unchanged). Apply identically to body callouts.

### Tier 1 — Must-fix before acceptance (scientific correctness / reproducibility)
- **T1-1 · DAM hallmark Discussion numbers (A1 Check 2) — [editor re-verified].** Replace the paragraph. Released-table values: TYROBP in core (FDR 1.2e-7; 4/5=0.80); TREM2 significant but **fails** core consistency (3.0e-3 six-input, 1.3e-3 bulk; 4/6=0.67 / 3/4=0.75); APOE not meta-significant (0.84 six-input, 0.30 bulk; 4/6=0.67). The "both TYROBP and TREM2 are within the core" claim is **false for TREM2** and must be deleted. (Corrected story — TYROBP in-core, TREM2 significant-but-inconsistent, APOE absent — is a *stronger* "partial DAM" argument.)
- **T1-2 · P2RX/P2RY six-input perm-p (A1 Check 7) — [editor re-verified].** Text says 0.440; both six-input tables give ~0.56–0.58. Change to "p = 0.56 in the six-input meta" (cite `P3_geneset_stats.csv` / `_R4_geneset_setlevel_bh.csv`). Conclusion unchanged (both ≫0.05).
- **T1-3 · P6 verdict vs prose contradiction + TNIK p (A2 Check 8) — [editor re-verified].** `P6_enrichment_mw_confounder_check.csv` labels AXL/TNIK `PASS_size_independent`, but the prose says they "failed the size-independent enrichment test" and gives TNIK p = 0.579 while the file gives **0.4435**. Reconcile: (a) relabel the `verdict` column to a single symmetric vocabulary (`PASS_BOTH`/`FAIL_FILTER1`/`FAIL_FILTER2`/`FAIL_BOTH`) so AXL/TNIK read `FAIL_FILTER2`; (b) define "inconclusive" = `FAIL_FILTER1 with size-indep signal` so ADRA2A uses the same rule; (c) correct TNIK p to 0.4435 (or cite BH-q 0.584, not 0.579).

### Tier 2 — Should-fix (traceability / hygiene; no conclusion change)
- **T2-1 · REG3B six-input FDR (A1 Check 6) — [editor re-verified].** 7.1e-14 → 1.38e-13 (keep cons 0.75, external-hypothesis framing).
- **T2-2 · ADRA2A json drift (A1 Check 5) — [editor re-verified].** Regenerate `P6_target_plausibility.json` from the same six-input Stouffer used for Table 3 (→ 4.45 / 8.35e-5 / 0.833), or add a one-line note that the json row was a different subset and Table 3 is canonical.
- **T2-3 · Translation p framing (A2 Check 4).** Report "p ≤ 0.0002 (5,000-permutation resolution floor, upper bound)"; keep "small, non-informative depletion" caveat.
- **T2-4 · MANIFEST.sha256 stray (A3 F-1) — [editor re-verified].** Either delete root + `_manifest/MANIFEST.sha256` and disable the release.yml step that regenerates it, or correct `MVP_PLOSONE_compliance_check.md` L95 to say it exists-but-unreferenced. (Option: delete — cleaner.)
- **T2-5 · .zenodo.json version (A3 F-2) — [editor re-verified].** Bump `"version"` to `"v1.6.0"`, or delete `.zenodo.json` entirely (manuscript states no Zenodo snapshot deposited).
- **T2-6 · release.yml (A3 F-3).** Update commented `v1.0.0` example to `v1.6.0`; remove/keep-align the MANIFEST-generation step per T2-4.
- **T2-7 · Human-miRNA source citation (A3 F-4).** Add `P4_setlevel_test.json` (perm_p 0.51, n = 253) to the Figure/Table source list. Value unchanged.

### Tier 3 — Minor / optional (clarify; no error)
- **T3-1 · CC BY in body (A4 P2).** Add a one-line license statement under "Additional Information" (currently only in cover letter; low risk).
- **T3-2 · Author Summary wording (A4 P3).** Tighten "no target held up reliably" → "no target cleared both enrichment filters" to match body nuance (ADRA2A inconclusive).
- **T3-3 · Nav1.8-axotomy mis-citation (A1 Check 3).** Ref 12 (Cooper 2024, neuronal subpopulation loss) does not directly state Nav1.8 down-regulation after axotomy; re-cite or soften.
- **T3-4 · Deposit resample-level bootstrap matrix (A2 Check 7).** Release the 200-resample hub-membership / target-recovery matrix (or the per-resample counts) so "median 43 hubs (IQR 41–46)", "median 8.70 of 17", "P(≥3 of 17)=1.000" are reproducible; separate per-gene median (0.465) from per-resample count (8.70).
- **T3-5 · Deposit multivariate physicochemical LR outputs (A2 Check 9).** Put the 5 LR p-values (AXL 2.6e-5, TNIK 7.3e-5, ACVR1 9.6e-4, MAPK14 0.066, ADRA2A 0.027) + EPV in `results/tables/` (or the script) so they are recomputable.
- **T3-6 · Knapp–Hartung for hubs/targets (A2 Check 10).** Recommended: apply K-H t-adjustment to the 35 hubs and 10 targets (K=3–7, hub median I² 79.1%); report new RE-significant counts (currently 7/35 hubs, 2/10 targets). Or keep deferred but name the subset explicitly.
- **T3-7 · Gene-set q=0.0022 clause (A1 Check 1).** Optional local reinforcement that the four identical q's are one floor-driven value (already stated later).

---

## 5. Consensus / complementary / divergent

**Consensus (all four).** The statistical design is unusually disciplined; the 10 mandatory counts reproduce exactly; the "honest null" framing is internally consistent and a strength; the abstract, figures, data availability, AI disclosure, and STROBE are compliant. No scientific rejection grounds.

**Complementary.** A1 (biology) and A2 (stats) independently converged on the P6 AXL/TNIK verdict↔prose contradiction from different angles (A1 via the docking discussion, A2 via the two-filter logic). A3's hygiene flags (MANIFEST, zenodo) are orthogonal to the science and were confirmed by the editor as real stray files.

**Divergent / resolved.** A4 rates reference ordering as the single blocking item; the three science reviewers rate their items as non-blocking. **Reconciliation:** reference ordering is a *mechanical* technical-check query, not a scientific defect — it is the only true acceptance gate, but it is cheap to fix. No scientific disagreement exists among the four.

---

## 6. Required-change list (acceptance gate)

| # | Item | Tier | Type | Blocker |
|---|---|---|---|---|
| 1 | Renumber references to first-citation order + rewrite all callouts | T0-1 | format | **YES** |
| 2 | Correct Discussion DAM numbers (TYROBP/TREM2/APOE) + drop "both in core" | T1-1 | numeric/discourse | yes (credibility) |
| 3 | Fix P2RX/P2RY six-input p 0.440 → 0.56 | T1-2 | numeric | yes |
| 4 | Reconcile P6 verdict column + TNIK p 0.579 → 0.4435 | T1-3 | data/manuscript | yes |
| 5 | REG3B FDR 7.1e-14 → 1.38e-13 | T2-1 | numeric | no |
| 6 | ADRA2A json → match Table 3 (or note) | T2-2 | traceability | no |
| 7 | Translation p → "p ≤ 0.0002" | T2-3 | framing | no |
| 8 | MANIFEST.sha256 stray cleanup | T2-4 | hygiene | no |
| 9 | .zenodo.json v1.0.0 → v1.6.0 / delete | T2-5 | hygiene | no |
| 10 | release.yml comment + MANIFEST step | T2-6 | hygiene | no |
| 11 | Cite P4_setlevel_test.json for miRNA p | T2-7 | provenance | no |
| 12 | CC BY line in body | T3-1 | minor | no |
| 13 | Author Summary wording | T3-2 | minor | no |
| 14 | Nav1.8 citation fix | T3-3 | minor | no |
| 15 | Deposit resample matrix | T3-4 | reproducibility | no |
| 16 | Deposit multivariate LR | T3-5 | reproducibility | no |
| 17 | K-H for hubs/targets (recommended) | T3-6 | robustness | no |

**No DESK-REJECT.** The blocking item is a renumbering + numeric-correction round, not a resubmission of substance.

---

## 7. What stands up (editor's independent confirmation)

I personally re-ran the five most severe findings from raw data and **confirm every one**:
- **DAM genes:** `META_DRG_axis_stouffer.csv` → TYROBP 1.19e-7/0.80; TREM2 3.04e-3/**0.667 (NOT in core)**; APOE 0.845/0.667. Manuscript's 8.8e-9/5-5, 1.3e-3/5-6, 0.070/6-6 are wrong, and "both in core" is false for TREM2. ✔ confirmed.
- **P2RX/P2RY six-input:** `P3_geneset_stats.csv` 0.5797; `_R4_geneset_setlevel_bh.csv` (fixed) 0.5607 — not 0.440. ✔ confirmed.
- **P6 verdict:** `P6_enrichment_mw_confounder_check.csv` → AXL/TNIK `PASS_size_independent`; TNIK `deltaAUC_vs_size_only_p_le0` = **0.4435** (not 0.579). ✔ confirmed contradiction.
- **MANIFEST.sha256:** exists at repo root (15,598 B) and `_manifest/` (28,392 B). ✔ confirmed stray.
- **Reference ordering:** Unicode-superscript parse → first-appearance `[1…21,38,40,22,23,26,24,25,27…37,39]` ≠ `1…40`. ✔ confirmed hard-fail.
- Plus: REG3B FDR 1.38e-13 (not 7.1e-14); ADRA2A json 4.84/1.5e-5/1.0 vs table 4.45/8.35e-5/0.833; .zenodo.json version "v1.0.0". ✔ all confirmed.

The **mathematical core is sound**: all 10 mandatory counts (FE 2750, RE 508/18.5%/I² 41.8%/τ² 0.266, q 0.0022×4, 43.3/47.1, bulk-only 2512/63.2/89.2/200/296, collapse 91.0%, LODO, miRNA 0.51, docking AUCs) reproduce exactly from the authoritative tables.

---

## 8. Recommended handling path

**Minor revision (not a resubmission; not a reject).** Two categories of fix:
1. **Mechanical / format:** T0-1 reference renumbering (the only true acceptance gate).
2. **Numeric & discourse corrections:** T1-1 (DAM Discussion), T1-2 (P2RX p), T1-3 (P6 verdict + TNIK p) — all change no conclusion; they make the paper's own strongest honesty claim ("data-supported, not metaphorical") actually reconcile with its tables.
3. **Hygiene (Tier 2):** cheap, do all before deposit.
4. **Optional (Tier 3):** recommended K-H extension and artefact deposits strengthen the "bounded hypothesis-generating" framing; not blocking.

After fixes: re-run the consistency gate, rebuild the docx (re-embed the 5 figures at 350 DPI), re-verify reference ordering programmatically, commit + tag **v1.7.0**, push, and `git ls-remote` confirm. Then re-panel (Round 17). The loop is expected to reach **accept** at Round 17 if T0-1 + T1-1..T1-3 + Tier-2 hygiene land cleanly, because no scientific objection remains.

---

## 9. Process lessons (honest, not dressed up as progress)

- **Gate still misses cross-file *discourse* numbers.** The consistency gate checks headline counts and stale tokens, but the Discussion DAM paragraph (TYROBP/TREM2/APOE) was hand-written prose that never traced to a single authoritative row — the gate could not catch it because no assertion existed to check. **Fix:** add a gate assertion that extracts the Discussion's DAM FDR/consistency triples and diffs them against `META_DRG_axis_stouffer.csv` / `META_bulkonly_meta.csv`.
- **Data-file `verdict` columns can contradict prose.** `P6_enrichment_mw_confounder_check.csv` says `PASS_size_independent` while the manuscript says "failed." A reader grepping the CSV will mis-cite a positive. **Fix:** gate-assert that every `verdict` in the docking CSV is consistent with the manuscript's two-filter wording, or relabel to a symmetric vocabulary.
- **Unicode superscript citations need an ordering assertion.** The reference-order violation hid behind Unicode superscripts (¹²³⁸⁴⁰), which a naive `[(\d+)\]` regex misses entirely — the editor's first attempt returned empty. **Fix:** add a Unicode-aware reference-ordering gate to the build so first-citation order is enforced automatically.
- **Stray release artefacts (MANIFEST.sha256, .zenodo.json v1.0.0) accumulate.** These are generated by the CI workflow and drift from the "no Zenodo / no MANIFEST referenced" design. **Fix:** either disable the generation step or assert version tokens == CITATION.cff in CI.
- **"Gate green" ≠ "review pass."** Four gates were green at v1.6.0, yet this independent panel found a format hard-fail and three numeric/discourse errors. The gate validates self-consistency, not correctness against the underlying biology tables. This round's value came from *independent recomputation of the Discussion prose against the CSVs*, which the gate does not do.

---

*Prepared by the consolidating editor from four independent panel reports (A1 domain, A2 design/stats, A3 implementation/provenance, A4 venue/STROBE) plus the editor's own raw-data re-verification. Enforced-independence confirmed. Round verdict: MINOR REVISION (not accept).*
