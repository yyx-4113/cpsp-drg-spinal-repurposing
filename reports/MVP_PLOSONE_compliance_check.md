# PLOS ONE — Final Formatting & Compliance Check

**Manuscript:** *Conserved nerve-injury-associated transcriptional response of the dorsal root ganglion: spinal-cord localisation and an honest repurposing null*
**Checked:** 2026-09-28 (Round 15) · **Source of record:** `reports/MVP_PLOSONE_submission.md` → rendered into `submission_pack/Manuscript.docx` by `scripts/build_sr_submission_pack.py`
**Verdict:** Content is PLOS ONE–ready. **References: 40 / 40 carry a Crossref-verified DOI** (re-verified 2026-09-27; see §3.3 — the legacy renumber/DOI scripts are now disabled after manual edits). Journal names are full; no abbreviated journal names remain.

---

## 1. Required manuscript elements

| # | PLOS ONE requirement | Status | Evidence / action |
|---|---|---|---|
| 1 | Title ≤ 250 chars, no unsubstantiated claims | ✅ PASS | 143 chars; descriptive, no "novel"/superlative claim |
| 2 | Author name, affiliation, ORCID, corresponding author | ✅ PASS | Single author; affiliation + ORCID 0009-0004-9698-6552 + email present |
| 3 | Abstract (≤ 300 words, no references) | ✅ PASS | 266 words; `p7_consistency_gate` confirms no citation in abstract |
| 4 | **Author Summary** (lay-audience summary) | ✅ PRESENT (mandatory) | PLOS ONE mandates an Author Summary; one is included and is distinct from the abstract, non-technical |
| 5 | IMRaD structure (Intro/Methods/Results/Discussion) | ✅ PASS | All sections present |
| 6 | References numbered in first-citation order (Vancouver) | ✅ PASS | 40 refs, order verified by `p7_consistency_gate` (0 errors) |
| 7 | **Full journal names** (no abbreviations) | ✅ PASS | All journal names expanded to full PLOS style; 0 abbreviations remain |
| 8 | **DOI for every reference where available** | ✅ PASS | 40 / 40 references carry a Crossref-verified DOI |
| 9 | Ethics statement | ✅ PASS | "### Ethics statement" covers secondary public-data reanalysis; GSE158825 IRB documented in the original deposition (see §5) |
| 10 | Data Availability statement | ✅ PASS | Public GitHub repo (v1.6.0, immutable release tag); explicit "not available on request" |
| 11 | **Funding** section (standalone) | ✅ PASS | Dedicated "## Funding" — "The author received no specific funding for this work." + pending-grant note |
| 12 | Competing Interests | ✅ PASS | Declared; pending FJNSF grant (ADRA2A listed) disclosed, stated not to influence |
| 13 | Author Contributions | ✅ PASS | Single-author prose statement |
| 14 | Acknowledgements | ✅ PASS | Thanks to GEO data contributors |
| 15 | AI-use disclosure | ✅ PASS | Methods: "A large language model (LLM) was used to assist manuscript drafting and language polishing"; no LLM authorship — also in cover letter |
| 16 | Keywords | ✅ PASS | 8 keywords present after Author Summary |
| 17 | No "data not shown" | ✅ PASS | None used |
| 18 | STROBE checklist (observational reanalysis) | ✅ PASS | `reports/MVP_PLOSONE_STROBE_checklist.md` included as Supporting Information S8 |

## 2. Figures & tables

| Item | Status | Note |
|---|---|---|
| Every figure/table cited in text | ✅ PASS | Fig 1–5 and Table 1–3 all cited |
| Legends present & complete | ✅ PASS | Legends in "Display items" block; embedded in docx |
| Image resolution ≥ 300 DPI | ✅ PASS | All 5 figures = 350.012 DPI (verified from PNG metadata) |
| File format | ⚠️ NOTE | PLOS accepts PNG but **prefers TIFF/EPS/PDF**; PNG at 350 DPI is acceptable. Upload each as a **separate** file named `Fig1.png` … `Fig5.png` (build copies them as `Fig1_geneset_programme.png` — rename at upload) |
| Display-item count | ✅ PASS | 5 figures + 3 tables = 8 enumerated main display items; no Scientific Reports–era cap phrase remains |

## 3. Reference DOIs — resolved (Crossref, 2026-09-26)

PLOS ONE requires a DOI for every reference **where available**. All 40 references were matched against Crossref and verified against the real article metadata (title + journal + year). **Result: 40 / 40 references carry a verified DOI; none is left blank.**

> Provenance note (T3-3 / T3-7): the Crossref verification was originally performed in Round 9 (2026-09-26) and was **re-run on 2026-09-27** (this Round-12 pass) covering all 40 references; all 40 resolve to the correct article metadata. Two references were added in this pass — **38.** Chen et al., *Cell Reports* 22:2307–2321 (2018), doi:10.1016/j.celrep.2018.02.021 (α2δ-1/gabapentinoid DRG mechanism); **39.** Yu et al., *Nature Communications* 11:264 (2020), doi:10.1038/s41467-019-13839-2 (DRG-resident macrophage neuroimmune sentinel) — each DOI Crossref-verified on 2026-09-27. The legacy `p7_renumber_refs.py` / `resolve_ref_dois.py` renumber/DOI scripts remain disabled; the DOI claims were validated directly against Crossref.

### 3.1 Round-9 additions (2026-09-26) and Round-10 Tier-2 addition (2026-09-26)
Four references were added across these rounds, each carrying a Crossref-verified DOI (numbered by current first-citation order in the manuscript):
- **11.** Yin, R. et al. Voltage-gated sodium channel function and expression in injured and uninjured rat dorsal root ganglia neurons. *International Journal of Neuroscience* **126**, 182–192 (2016). doi:10.3109/00207454.2015.1004172  *(Round 9)*
- **12.** Cooper, A. H. et al. Peripheral nerve injury results in a biased loss of sensory neuron subpopulations. *Pain* **165**, 2863–2876 (2024). doi:10.1097/j.pain.0000000000003321  *(Round 9)*
- **23.** Bertoch, T. et al. Suzetrigine, a nonopioid NaV1.8 inhibitor for treatment of moderate-to-severe acute pain: two phase 3 randomized clinical trials. *Anesthesiology* **142**, 1085–1099 (2025). doi:10.1097/ALN.0000000000005460  *(Round 9)*
- **37.** Flatters, S. J. Characterization of a model of persistent postoperative pain evoked by skin/muscle incision and retraction (SMIR). *Pain* **135**, 119–130 (2008). doi:10.1016/j.pain.2007.05.013  *(Round-10 Tier-2; underpins the GSE267799 two-model incision-arm day-32 dissipation caveat)*
- **38.** Chen, J. et al. The α2δ-1–NMDA receptor complex is critically involved in neuropathic pain development and gabapentin therapeutic actions. *Cell Reports* **22**, 2307–2321 (2018). doi:10.1016/j.celrep.2018.02.021  *(Round 12; α2δ-1/gabapentinoid DRG mechanism — must-cite added per review, Crossref-verified 2026-09-27)*
- **39.** Yu, X. et al. Dorsal root ganglion macrophages contribute to both the initiation and persistence of neuropathic pain. *Nature Communications* **11**, 264 (2020). doi:10.1038/s41467-019-13839-2  *(Round 12; DRG-resident macrophage neuroimmune sentinel — must-cite added per review, Crossref-verified 2026-09-27)*

> Note on DRG-neuron-loss citation: the Round-9 review suggested Martin 2019 as the DRG-neuron-loss citation. Because Martin 2019 could not be independently verified, it was **replaced by Cooper et al. 2024** (*Pain* 165:2863–2876, ref 12), a verifiable primary study reporting biased sensory-neuron-subpopulation loss after peripheral nerve injury. This substitution is disclosed to the author.

### 3.2 Previously-corrected citation metadata (carried forward, no regression)
Crossref audit (earlier round) corrected three reference-list entries to match the real papers:
- `macrae2017`: *British Journal of Anaesthesia* **101**, 77–86 (2008) — doi:10.1093/bja/aen099
- `tsuda2003`: *Nature* **424**, 778–783 (2003) — doi:10.1038/nature01786
- `coull2005`: *Nature* **438**, 1017–1021 (2005) — doi:10.1038/nature04223

### 3.3 Build note (do not re-run the ref-renumber/DOI scripts)
The manuscript is now edited **directly** in `MVP_PLOSONE_submission.md` and rebuilt via `scripts/build_sr_submission_pack.py`, which reads the `.md` at the "## Display items" split and inlines rendered figures. The legacy `p7_renumber_refs.py` / `resolve_ref_dois.py` re-render from the quarantined `_v15_source.md` and **must not be re-run** after manual edits.

## 4. At-submission checklist (PLOS form, not manuscript text)

- [ ] Complete the **PLOS Minimum Standards Reporting Checklist** in the submission form (computational/observational study — no specific EQUATOR checklist mandated; MIAME/GEO compliance already stated in Methods).
- [ ] Upload figures as separate files (rename to `Fig1.png`…`Fig5.png`); Supporting Information as `S1`…`S8` (supplementary is `MVP_PLOSONE_supplementary.md`).
- [ ] Confirm the manuscript text uploaded is the regenerated `reports/MVP_PLOSONE_submission.md` (PLOS-compliant).
- [ ] Cover letter: `submission_pack/Cover_Letter_PLOSONE.docx` already lists all required PLOS statements.
- [ ] (Optional, deferred per author instruction) Deposit a versioned Zenodo/figshare archive post-acceptance for a citable permanent DOI. The manuscript Data Availability statement currently cites the versioned GitHub release (v1.6.0) and explicitly states no Zenodo snapshot has been deposited; **no `10.5281/zenodo.XXXXXXX` placeholder exists in the manuscript**, so no placeholder replacement is required. If staying GitHub-only, confirm the v1.6.0 release tag is immutable.

## 5. Ethics — IRB provenance (T3-3)

The single human dataset, GSE158825 (human plasma miRNA, n = 60; lumbar surgery with pain outcome), has IRB approval and informed consent documented in its original GEO deposition. The approving IRB and its approval identifier are recorded in the GSE158825 data deposit (accession GSE158825) and are not independently reproduced in this manuscript; the data were accessed in de-identified form, and this secondary reanalysis required no further ethics approval.

## 6. What was changed in this pass (Round 9, 2026-09-26)

- `reports/MVP_PLOSONE_submission.md`: the non-circular translation test is reported with the **strict** stratum (NI FDR < 0.05 AND NI consistency ≥ 0.8) = **43.3% (1,660/3,830) vs 47.1% (6,772/14,390) background, risk difference −3.7 pp, permutation p = 0.0002 (significant depletion)**, used consistently in abstract, body and cover letter; the older loose 46.2% / p = 0.14 figure was superseded (Round 14) after independent re-derivation from `_R4_nerveinjury_only_summary.json`. Also inserted EPV note; reframed ML paragraph; added explicit FE-primary qualifier; added DAM hallmark-gene quantitative justification (TREM2/TYROBP in FDR<0.05 core; APOE consistency 6/6 but FDR 0.070); added separate "## Conclusions"; strengthened ethics IRB provenance.
- `reports/MVP_PLOSONE_cover_letter.md`: translation stat aligned to strict stratum (43.3% vs 47.1%, p = 0.0002).
- `reports/MVP_PLOSONE_supplementary.md`: display-item cap phrase corrected.
- `reports/MVP_PLOSONE_STROBE_checklist.md`: Item 1 satisfied via abstract + metadata (not title).
- `reports/MVP_PLOSONE_compliance_check.md`: this document — updated to 40/40 DOIs, PLOS ONE filenames, 5+3 display items, STROBE S8, Zenodo placeholder, Cooper-2024 substitution note, Round-10 Tier-2 Flatters-2008 addition.
- Gates: `gate_consistency` (references = 37), `p7_consistency_gate` (Round-9 integrity assertions) — see `scripts/`; `build_sr_submission_pack.py` rebuilds `Manuscript.docx`.

## 7. Round 15 changelog (2026-09-28, v1.6.0)

Round-15 enforced-independence four-expert review (A1–A4) returned minor-revision / no scientific blocker; the honest-negative boundary framing was affirmed. Three real defects were fixed and the pre-submission gate was hardened:

- **B1 data-integrity (real bug).** `META_bulkonly_sensitivity_summary.json` (`primary_core_size` 4055 → 2750; `overlap` 2202 → 1737; `overlap_pct_primary` 54.3157 → 63.1636) and `META_collapse_meta.csv` (`orig_core` 4055 → 2750; `collapsed_core` 4294 → 3582; `shared_core` 3707 → 2502; `retained_fraction` 0.9142 → 0.9102) were rebuilt at the current 2,750-gene core. Manuscript L44's stale "overlap 54.3% / retention 91.4%" was corrected to "overlap 63.2% / retention 91.0%", matching the authoritative Table 1a (L321); the L50 "54.3% figure" parenthetical was rewritten to the consistent 63.2% framing.
- **Structured abstract (PLOS ONE technical-check blocker).** The abstract's Background/Methods/Results/Conclusions labelled sections were removed; the abstract is now a single non-structured paragraph, 266 words (≤300), preserving every headline number and the two-filter docking logic.
- **F1 compliance-check credibility.** `MVP_PLOSONE_compliance_check.md` corrected from v1.3.0 → v1.6.0 (two places), 37 → 40 references, 256 → 266 abstract words, and the false "MANIFEST.sha256" Data-Availability reference was removed (no MANIFEST exists; integrity now stated via CITATION.cff + immutable tag). Author Summary corrected from "optional" to "mandatory" per PLOS ONE policy.
- **F2 gate hardening.** `p7_consistency_gate.py` `chk()` now additionally verifies, for every numeric needle, that a value parsed from the manuscript equals the recomputed authoritative value (catches manuscript drift, not just string presence); added derived-value assertions for the high-risk numbers (2,750 core, 508 RE core, 41.8% I², 0.266 τ², 2,512 bulk-only core, 63.2% bulk overlap, 91.0% collapse retention, 43.3/47.1/−3.7, q = 0.0022) and a stale-token scan (v1.0.0–v1.5.0, 4,055/4055, 54.3, 91.4) that fails on any regression.
- Data Availability statement (manuscript L285/L287) bumped v1.5.0 → v1.6.0 and MANIFEST.sha256 reference removed; cover letter L13 bumped to v1.6.0, Author Summary corrected to mandatory, and CC BY license declaration added.
- Gates: `gate_consistency` (references = 40), `p7_consistency_gate` (Round-15 hardened) — see `scripts/`; `build_sr_submission_pack.py` rebuilds `Manuscript.docx`.
