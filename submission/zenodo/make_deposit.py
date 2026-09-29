#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
make_deposit.py -- assemble a Zenodo-ready reproducibility deposit package for the
CPSP DRG-spinal-axis / FDA drug-repurposing study (v1.8.0).

Adapted from D:\\dca_pocd_pipeline\\submission\\SciReports_preprint\\make_deposit.py
(the reference project that already holds a published Zenodo concept DOI).

This script ONLY packages files locally (no network, no token). The author (or the
companion upload_zenodo.py) then deposits the zip to Zenodo.

Exclusions (per the manuscript's own Data Availability statement and the integrity
policy): the 11 GB raw GEO counts (data/) and the prepared receptor/ligand
structures (docking/) are NOT bundled -- they are regenerable from the documented
GEO accessions, RCSB PDB IDs and ChEMBL SMILES. The consolidated docking-score
table (P6_docking_scores_merged.csv, in results/tables) is the screen output of
record and IS included.

Pass --doi to bake a Zenodo DOI into the manuscript copy and DEPOSIT_README so the
archived snapshot is self-consistent (run this AFTER upload_zenodo.py has
backfilled the repository with the DOI, then use --new-version to re-deposit).
"""
from __future__ import annotations

import argparse
import math
import zipfile
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent  # project root (script lives in submission/zenodo/)

OUT = HERE / "cpsp_drg_repurposing_deposit.zip"

# The sandbox egress proxy stalls / resets single PUTs larger than ~2 MiB, so the
# deposit is published as sequential split volumes (each well under that limit).
# Zenodo lists them as separate files; reassemble locally with:
#   cat cpsp_drg_repurposing_deposit.zip.* > cpsp_drg_repurposing_deposit.zip
DEFAULT_PART_SIZE = 1572864  # 1.5 MiB

# Optional: a Zenodo DOI (concept or version) to bake into the archived copy.
DEPOSIT_DOI = ""

# (source_path, archive_path, description)
ITEMS: list[tuple[Path, str, str]] = []


def add(src: Path, arc: str, desc: str) -> None:
    ITEMS.append((src, arc, desc))


def build_item_list() -> None:
    # ---- manuscript + reporting docs ----
    add(REPO / "reports" / "MVP_PLOSONE_submission.md",
        "manuscript/MVP_PLOSONE_submission.md",
        "Main manuscript source (markdown; the submitted text).")
    add(REPO / "reports" / "MVP_PLOSONE_supplementary.md",
        "manuscript/MVP_PLOSONE_supplementary.md",
        "Supporting Information source (markdown).")
    add(REPO / "reports" / "MVP_STROBE_checklist.md",
        "manuscript/MVP_STROBE_checklist.md",
        "STROBE checklist for this observational reanalysis.")
    add(REPO / "reports" / "MVP_PLOSONE_cover_letter.md",
        "manuscript/MVP_PLOSONE_cover_letter.md",
        "Cover letter.")
    add(REPO / "reports" / "MVP_PLOSONE_compliance_check.md",
        "manuscript/MVP_PLOSONE_compliance_check.md",
        "Pre-submission compliance / venue check log.")

    # ---- submission-pack artefacts (the actual journal files) ----
    add(REPO / "submission_pack" / "Manuscript.docx",
        "submission_pack/Manuscript.docx",
        "Manuscript as submitted to PLOS ONE (5 figures embedded >=300 DPI).")
    add(REPO / "submission_pack" / "Supporting_Information.docx",
        "submission_pack/Supporting_Information.docx",
        "Supporting Information .docx.")
    add(REPO / "submission_pack" / "Cover_Letter_PLOSONE.docx",
        "submission_pack/Cover_Letter_PLOSONE.docx",
        "Cover letter .docx.")
    add(REPO / "submission_pack" / "STROBE_Checklist.docx",
        "submission_pack/STROBE_Checklist.docx",
        "STROBE checklist .docx.")
    add(REPO / "submission_pack" / "Reporting_Summary.md",
        "submission_pack/Reporting_Summary.md",
        "PLOS ONE reporting summary.")
    add(REPO / "submission_pack" / "SUBMISSION_MANIFEST.md",
        "submission_pack/SUBMISSION_MANIFEST.md",
        "Submission manifest (file inventory for the journal upload).")

    # ---- repository metadata ----
    add(REPO / "README.md", "README.md",
        "Project README: file map, reproduction commands, caveats, software versions.")
    add(REPO / "CITATION.cff", "CITATION.cff",
        "CITATION.cff (version v1.8.0, with Zenodo DOI identifier once backfilled).")
    add(REPO / "LICENSE", "LICENSE", "MIT license.")
    add(REPO / ".zenodo.json", ".zenodo.json",
        "Zenodo metadata hint (for optional GitHub-Zenodo integration).")
    add(REPO / "MANIFEST.sha256", "MANIFEST.sha256",
        "SHA-256 manifest of derived artefact files (integrity verification).")

    # ---- derived tables (the analytical output of record) ----
    tables_dir = REPO / "results" / "tables"
    if tables_dir.is_dir():
        for p in sorted(tables_dir.glob("*.csv")) + sorted(tables_dir.glob("*.json")) \
                + sorted(tables_dir.glob("*.csv.gz")):
            if p.is_file():
                add(p, f"derived_tables/{p.name}",
                    f"Derived table: {p.name}.")
    # results notes / provenance
    for p in sorted((REPO / "results").glob("*.md")):
        add(p, f"derived_tables/{p.name}", f"Analysis note: {p.name}.")

    # ---- figures ----
    figdir = REPO / "figures"
    if figdir.is_dir():
        for p in sorted(figdir.glob("*.png")):
            add(p, f"figures/{p.name}", f"Figure source: {p.name}.")

    # ---- analysis + build scripts (exclude scratch / cache) ----
    scripts_dir = REPO / "scripts"
    if scripts_dir.is_dir():
        for p in sorted(scripts_dir.glob("*.py")):
            if p.name.startswith("_"):
                continue  # dev scratch / one-off fix scripts
            add(p, f"code/{p.name}", f"Analysis / build script: {p.name}.")
    # also include the deprecated dir's genuinely useful scripts? No -- keep it out.


def deposit_readme(doi: str) -> str:
    lines = [
        "CPSP DRG-spinal-axis target locking + FDA drug-repurposing -- deposit package",
        "=============================================================================",
        "",
        "Manuscript: 'Conserved nerve-injury-associated transcriptional response of the",
        "dorsal root ganglion: spinal-cord localisation and an honest repurposing null'",
        "Author: Yongxin Yang (single author), ORCID 0009-0004-9698-6552",
        "Version: v1.8.0   License: MIT",
        "",
        "Contents",
        "--------",
        "- manuscript/      main text (.md), Supporting Information (.md), STROBE",
        "                  checklist, cover letter, compliance log",
        "- submission_pack/ the actual journal files (Manuscript.docx with 5 embedded",
        "                  figures >=300 DPI, Supporting_Information.docx, cover letter",
        "                  .docx, STROBE .docx, reporting summary, submission manifest)",
        "- derived_tables/  all consolidated result tables (meta-analysis, gene-set",
        "                  statistics, hub lists, DEG tables, single-cell / spatial",
        "                  localisation, bulk-only sensitivity, target plausibility,",
        "                  random-effects & nerve-injury-only meta, target-set bootstrap)",
        "- figures/         Figure 1-5 source PNGs (>=300 DPI)",
        "- code/           reproduction + build scripts (p1_* through p9_*, make_*,",
        "                  gate_*, common_map, build_sr_submission_pack, verify_sr_docx)",
        "- README.md, CITATION.cff, LICENSE, .zenodo.json, MANIFEST.sha256",
        "",
        "Data-integrity notes",
        "--------------------",
        "- This is an HONEST REPURPOSING NULL. The structure-based virtual screen of the",
        "  ChEMBL max_phase=4 approved-drug library (3,085 unique drugs) against ten",
        "  tractable hub targets produced no robust enrichment (full-library AUC 0.532,",
        "  p=0.118, NS); this is the reported, intended result. The control-based",
        "  validation framework (docking-parameter fidelity, independently labelled",
        "  ChEMBL enrichment, molecular-weight confounder control with paired delta-AUC",
        "  confidence intervals, and a reportable face-validity test) is what makes the",
        "  null informative rather than a methodological failure.",
        "- All numbers in the manuscript are traceable to the files in derived_tables/",
        "  and code/; no p-values or effect sizes were fabricated. See MANIFEST.sha256.",
        "- Raw GEO counts (data/, ~11 GB) and prepared receptor/ligand structures",
        "  (docking/) are intentionally excluded: they are regenerable from the 12",
        "  public GEO accessions, the documented RCSB PDB IDs and ChEMBL SMILES. The",
        "  consolidated docking-score table (P6_docking_scores_merged.csv) is included",
        "  as the screen output of record.",
        "",
    ]
    if doi:
        lines += [
            "This record",
            "-----------",
            f"Zenodo DOI {doi}  (https://doi.org/{doi})",
            "The manuscript copy in manuscript/ already cites this DOI in its Data",
            "Availability statement.",
            "",
        ]
    else:
        lines += [
            "This record",
            "-----------",
            "The Zenodo DOI is assigned on first publish and is shown on the record",
            "landing page. The manuscript copy here is the pre-DOI snapshot; the",
            "versioned GitHub release carries the DOI-cited Data Availability text.",
            "",
        ]
    lines += [
        "Reproduce",
        "--------",
        "1) pip install numpy pandas scipy scikit-learn mygene matplotlib python-docx",
        "2) python code/p1_build.py            # -> transcriptomic matrices",
        "3) python code/p3_ml.py              # -> hub-gene prioritisation",
        "4) python code/p6_dock.py            # -> virtual-screen scores (needs ChEMBL",
        "                                       SMILES + RCSB PDB, see manuscript Methods)",
        "5) python code/build_sr_submission_pack.py   # -> submission_pack/Manuscript.docx",
        "",
        "Deposit helper",
        "--------------",
        "upload_zenodo.py (in this deposit package / project) creates this Zenodo record",
        "via the current InvenioRDM /api/records API. Re-running it needs a personal",
        "access token with deposit:write + deposit:actions. See --help.",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="Build the CPSP Zenodo deposit zip (offline).")
    ap.add_argument("--doi", default="", help="Zenodo DOI to bake into the manuscript "
                                            "copy + DEPOSIT_README (run after repo backfill).")
    ap.add_argument("--part-size", type=int, default=DEFAULT_PART_SIZE,
                    help=f"split-volume size in bytes (default {DEFAULT_PART_SIZE} = 1.5 MiB). "
                         f"The egress proxy stalls single PUTs >~2 MiB, so the deposit is "
                         f"published as split volumes for reliable upload.")
    args = ap.parse_args()
    doi = (args.doi or DEPOSIT_DOI).strip()

    build_item_list()

    missing = [src for src, _, _ in ITEMS if not src.exists()]
    if missing:
        print("MISSING SOURCE FILES:")
        for m in missing:
            print(f"  {m}")
        return 1

    # Safety: never package anything that looks like a credential.
    leaks = [str(src) for src, _, _ in ITEMS if "token" in src.name.lower()
             or "secret" in src.name.lower() or src.name.lower().endswith(".env")]
    if leaks:
        print("REFUSING TO PACKAGE CREDENTIAL-LIKE FILE(S):")
        for l in leaks:
            print(f"  {l}")
        return 2

    manifest_lines = ["file\tdescription", ""]
    with zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED) as z:
        for src, arc, desc in ITEMS:
            # Special-case the main manuscript: bake the DOI into its Data
            # Availability text if a DOI was supplied (keeps the archived copy
            # self-consistent without touching the repository file here).
            if doi and arc == "manuscript/MVP_PLOSONE_submission.md":
                txt = src.read_text(encoding="utf-8")
                txt = _bake_doi(txt, doi)
                z.writestr(arc, txt)
            else:
                z.write(src, arc)
            manifest_lines.append(f"{arc}\t{desc}")
        z.writestr("DEPOSIT_README.md", deposit_readme(doi))
        manifest_lines.append("DEPOSIT_README.md\tThis file: package overview + integrity notes + reproduce steps.")
        z.writestr("MANIFEST.tsv", "\n".join(manifest_lines))

    size = OUT.stat().st_size
    print(f"Deposit package written: {OUT}")
    print(f"  files: {len(ITEMS) + 2}  ({size:,} bytes, "
          f"{size/1024/1024:.1f} MiB)")
    print(f"  generated: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    if doi:
        print(f"  DOI baked: {doi}")

    # ---- split into sequential volumes for reliable egress upload ----
    parts = split_zip(OUT, args.part_size)
    print(f"Split into {len(parts)} volume(s) of <= {args.part_size:,} bytes each:")
    for p in parts:
        print(f"  {p.name}  ({p.stat().st_size:,} bytes)")
    return 0


def split_zip(zip_path: Path, part_size: int) -> list[Path]:
    """Split the deposit zip into zero-padded sequential volumes (cpsp_...zip.001,
    .002, ...). Lexical sort equals numeric order so `cat *.zip.*` reassembles
    correctly. Existing volumes are removed first to avoid stale leftovers."""
    stem = zip_path.name
    for old in HERE.glob(f"{stem}.*"):
        if old.is_file() and old.suffix[1:].isdigit():
            old.unlink()
    size = zip_path.stat().st_size
    nparts = max(1, math.ceil(size / part_size))
    parts = []
    with zip_path.open("rb") as fh:
        for i in range(1, nparts + 1):
            part = HERE / f"{stem}.{i:03d}"
            chunk = fh.read(part_size)
            if not chunk:
                break
            part.write_bytes(chunk)
            parts.append(part)
    # reassembly helper (uploaded alongside the volumes)
    reasm = HERE / "00_REASSEMBLE.txt"
    reasm.write_text(
        "Reassemble the split deposit volumes\n"
        "=====================================\n\n"
        "Zenodo stores this deposit as sequential split volumes named\n"
        f"  {stem}.001, {stem}.002, ... ({nparts} parts)\n"
        "because the upload egress stalls on single transfers >~2 MiB.\n\n"
        "Download all parts into one folder, then recombine:\n\n"
        "  Linux / macOS / WSL:\n"
        f"    cat {stem}.* > {stem}\n\n"
        "  Windows (PowerShell):\n"
        f"    Get-Content {stem}.* -Raw | Set-Content -Encoding Byte {stem}\n\n"
        "  (or any 'split/join' tool, e.g. 7-Zip / HJSplit)\n\n"
        "Then unzip the recombined archive:\n"
        f"    unzip {stem}\n\n"
        "The recombined file is byte-identical to the original deposit zip.\n",
        encoding="utf-8")
    return parts


def _bake_doi(txt: str, doi: str) -> str:
    old = ("no Zenodo snapshot has been deposited. Data are therefore available "
           "from the versioned GitHub release, not on request.")
    new = (f"a Zenodo snapshot of this reproducibility package is deposited under "
           f"DOI {doi} (https://doi.org/{doi}); the data are additionally available "
           f"from the Zenodo archive and the versioned GitHub release, not on request.")
    if old in txt:
        return txt.replace(old, new)
    return txt


if __name__ == "__main__":
    raise SystemExit(main())
