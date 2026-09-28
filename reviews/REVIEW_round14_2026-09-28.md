# MVP PLOS ONE — Round 14 Review & Disposition (2026-09-28)

**Manuscript:** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null* (single-author, Y.Y.)
**Process:** Enforced-independence four-panel review (A1 domain · A2 design/statistics · A3 code-provenance/recomputation · A4 venue compliance) **+ independent recomputation of every headline number from authoritative products** (trust-but-verify discipline), then targeted revision, pack rebuild, gates, and versioned release.
**Outcome of this round:** All panel-raised and self-discovered items resolved; both consistency gates green; version **v1.5.0** committed, tagged, and pushed over SSH (verified by `git ls-remote`).

---

## 1. Four-panel conclusions (summary)

| Panel | Verdict | Headline |
| --- | --- | --- |
| **A1 Domain** | No scientific-design rejection. Flagged wording/quantitative precision items only. | Set-level q wording (F2); REG3B FDR precision (F5); hub "28/35 NI-consistency" claim needs a denominator check. |
| **A2 Design/Stats** | No methodological rejection. Flagged two numbers that must match the meta product. | Abstract set-level q must equal the computed BH q (F6); median-I² self-inconsistency (F5). |
| **A3 Implementation** | No computation-correctness rejection after recomputation. Flagged one genuine stale count (32/35 → 26/35, F1) and stale set-level q (F4). | Confirmed the meta/RE/S6 numbers now trace to `_R4_*.csv` / `META_*.csv`; the "46.2%/p=0.14" Discussion figure was already corrected in the working tree. |
| **A4 Venue (PLOS ONE)** | Compliant. Flagged a caption wording + a STROBE/table-caption core-size string. | Table-2 caption "4,055-gene signature" must read the current 2,750-gene core; STROBE item 15 same. |

**No panel recommended rejection.** The consensus path was "same-article-type revise" (A) — close the quantitative-precision and stale-number items, do not change the scientific claims.

---

## 2. Item-by-item disposition

| # | Item (source) | Classification | Action in v1.5.0 |
| --- | --- | --- | --- |
| 1 | Abstract set-level q = 0.003 (A1 F2 / A2 F6 / A3 F4) | **Real bug** (stale geneset q) | → **0.0022** (authoritative `_R4_geneset_setlevel_bh.csv`, all four core sets FE & RE). |
| 2 | Body L46 "median I² ≈39%" contradicts "median I² = 41.8%" in same paragraph | **Real bug** (self-inconsistency) | → **41.8%** (recomputed median I² across 16,552 genes = 41.77%). |
| 3 | Body L48 contradictory "q = 0.003" paragraph vs its own "q = 0.0022" listing | **Real bug** (leftover from a prior half-fix) | Rewritten: OXPHOS now **survives set-level BH under random effects (q = 0.0022)**; the "fixed-effect only" framing removed. |
| 4 | Body L124 "32/35, 91%" in meta core | **Real bug** (stale count) | → **26/35 (74%)**; added clarifying note: all 35 satisfy meta_FDR < 0.05, only 26/35 clear consistency ≥ 0.8. |
| 5 | Supplementary S5b — entire set-level BH table | **Real bug** (stale perm_p + BH q; OXPHOS mislabelled "fixed-effect only") | Rebuilt row-by-row from `_R4_geneset_setlevel_bh.csv`; OXPHOS now **yes (FE & RE)**. |
| 6 | Supplementary S6 Panel A — core size, τ², I², hubs | **Real bug** (all 4,055-era values) | → 2,750 / 508 (18.5%) / τ² 0.266 / I² 41.8% / I²>50% 43.9% / τ²>0 69.7% / hubs RE 7/35. |
| 7 | Supplementary S6 Panel B — 46.2% / p=0.14 vs body 43.3%/p=0.0002 | **Real bug** (orphaned loose stratum contradicting the authoritative strict test) | Rebuilt around the strict stratum `NI_FDR05_AND_NIcons>=0.8` = 1,660/3,830 (43.3%) vs background 6,772/14,390 (47.1%), −3.7 pp, p = 0.0002. Orphaned 46.2%/4,899 row removed. |
| 8 | Supplementary S6 Panel C — 4,055-era consistency split | **Real bug** | → 2,361 measured / 1,822 (77.2%) concordant / 539 (22.8%) discordant / 2,590/2,750 (94.2%) / 1,663 both / mean NI consistency 0.914. |
| 9 | Build script Table-2 caption "4,055-gene signature" (A4) | **Real bug** | → **2,750-gene core (meta_FDR < 0.05 and consistency ≥ 0.8)**. |
| 10 | STROBE checklist item 15 "locked 4,055-gene core" (A4) | **Real bug** | → **2,750-gene core**. |
| 11 | Data availability "released as version v1.4.0" | **Real bug** (version drift) | → **v1.5.0** (both occurrences). |
| 12 | Fig. 1 legend ion-channel family q (Nav_SCN/TRP/CACNA/Kv) | **Real bug** (stale FE q) | → **0.62 / 0.92 / 0.92 / 0.91** (authoritative FE BH q). Qualitative "grey = not significant" unchanged. |
| 13 | REG3B FDR 7.1×10⁻¹⁴ (A1 F5) | **Real bug** (stale precision) | → **1.38×10⁻¹³** (authoritative `META_DRG_axis_stouffer.csv`), with consistency-failing framing retained. |
| 14 | `gate_consistency.py` hardcoded 4055 / 32/35 | **Real bug** (gate drift) | → 2750 / 26/35. |
| 15 | `gate_consistency.py` 9 further stale hardcoded assertions (SCN range, geneset mean_Z, 53.9%/69.5%/7,751, ref=39) | **Gate bug, not manuscript bug** | SCN check was reading the **full** 6-contrast meta while the manuscript cites the **bulk-only** meta (`META_bulkonly_meta.csv`); corrected the source file. Other assertions updated to current authoritative values. Manuscript L52 (SCN9A −2.92/0.011 etc.) was **verified correct** against the bulk-only product. |
| 16 | A3 F2 (significance wording) / A3 F3 (46.2% in Discussion) | **Already fixed in working tree** (not a new bug) | Verified present; no further change. |

**Total genuine manuscript/supplementary/pack edits this round: 13 numbers/tables (items 1–13) + 1 gate (14).** The deep recomputation surfaced **12+ stale locations** — substantially more than the panel's nominal ~5 items, because the panel read line-by-line while the consistency gates had never covered the supplementary tables, the build caption, STROBE, the data-availability block, or the figure legend.

---

## 3. Trust-but-verify record (recomputed from authoritative products)

Every value written in v1.5.0 was independently recomputed from:
- `_R4_geneset_setlevel_bh.csv` → S5b table, abstract/body q = 0.0022.
- `_R4_random_effects_meta.csv` → S6 Panel A (median I² 41.77%, τ² 0.266, %I²>50% 43.9%, %τ²>0 69.7%, FE core 2,750, RE core 508, hubs RE 7/35) and Panel C (2,361 / 1,822 / 539 / 2,590 / 1,663 / 0.914).
- `_R4_nerveinjury_only_summary.json` → S6 Panel B strict stratum (1,660/3,830 = 43.3%, background 6,772/14,390 = 47.1%, −3.7 pp, p = 0.0002).
- `META_DRG_axis_stouffer.csv` (FE core 2,750) and `P3_hub_genes.csv` (26/35 meta-core; 7/35 RE FDR<0.05) → L124, Table 2.
- `META_bulkonly_meta.csv` → L52 SCN channels (SCN9A −2.92/0.0108, SCN10A −3.03/0.0080, SCN11A −3.41/0.0026, SCN8A −4.92/1.0e-5) — **confirmed the manuscript's stated bulk meta values are correct**; the earlier "failure" was a gate reading the wrong (full-meta) file.

**No value was changed on the panel's word alone.** Where the panel quoted a line that had already been fixed in the working tree (A3 F2/F3), the fix was verified rather than re-applied.

---

## 4. Honest limitations retained (not "strengthened")

Per the manuscript's integrity, these deliberately negative / bounded statements were preserved verbatim:
- Random-effects core collapse (2,750 → 508, 18.5%).
- Non-predictive incision translation (43.3% vs 47.1%, p = 0.0002 — significant *depletion*, non-informative about CPSP specificity).
- Honest full-library docking null (no target clears both filters; ion-channel class undockable, so the null cannot speak to those targets).
- REG3B carried as a consistency-failing external hypothesis, not an internal hub.
- Zenodo placeholder removed in v1.2.0; data availability = GitHub **v1.5.0** versioned release (no pseudo-DOI).

---

## 5. Gates & build

| Gate | Result |
| --- | --- |
| `p7_consistency_gate.py` (authoritative) | **0 failure, 49 checks passed** |
| `gate_consistency.py` (deprecated, fixed this round) | **57 pass, 0 fail** |
| `build_sr_submission_pack.py` | Manuscript.docx / Supporting_Information.docx / Cover_Letter*.docx rebuilt; DPI ≥300. |
| docx numeric audit | New numbers present (2,750, 508, 41.8%, 43.3%, 26/35, v1.5.0, 0.0022, 18.5%, 77.2%, 94.2%, 0.914); stale numbers absent (4,055, 1,008, 32/35, 0.003-as-geneset-q, v1.4.0, 46.2%, 38.8%, 72.8%, 0.002999, "fixed-effect only"). Residual `0.003`/`0.31` substrings are legitimate per-gene statistics (Table 2 hub p-values; SCN11A bulk FDR; MAPK14 0.310; reference DOIs 10.3109…), not the stale geneset q. |

---

## 6. Release

- Commit (Round 14 revision set) → `git tag v1.5.0` → SSH push `main` + `v1.5.0` → **`git ls-remote` verified the tag and branch are present on origin** (no fabricated success).

---

## 7. Round 15 plan (close the structural blind spot)

1. **Extend `p7_consistency_gate.py`** to cover the supplementary tables (S5b set-level BH q, S6 Panel A/B/C headline numbers) and the data-availability version string against the authoritative CSVs/JSON — the blind spot that let these stale numbers persist v1.0→v1.4 must be closed so it cannot recur.
2. Final independent re-read of the full v1.5.0 manuscript + supplementary for any remaining prose/number drift.
3. If clean → submit to PLOS ONE (target journal already selected: SCIE, IF 2.8, Q2, explicitly accepts negative/null results).

---

*Prepared 2026-09-28 by the research-assistant agent. Review panels: `reviews/round14_panel_2026-09-28/{A1_domain,A2_design_stats,A3_implementation,A4_venue}.md`.*
