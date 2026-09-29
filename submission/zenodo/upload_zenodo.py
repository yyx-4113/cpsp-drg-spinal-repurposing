#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
upload_zenodo.py -- one-command Zenodo deposit for the CPSP DRG-spinal-axis /
FDA drug-repurposing reproducibility package (v1.8.0).

Adapted from D:\\dca_pocd_pipeline\\submission\\SciReports_preprint\\upload_zenodo.py
(the reference project that already holds a published Zenodo concept DOI). It uses
the CURRENT Zenodo InvenioRDM REST API (/api/records), NOT the retired legacy
/api/deposit/depositions endpoint.

Verified gotchas (both hit for real on other projects, fixed here):
  * sending a top-level "pids" block when creating the draft -> HTTP 500.
  * omitting metadata.publisher -> publish fails HTTP 400
    ("Missing publisher field required for DOI registration").

Usage
-----
  # rehearsal on the sandbox (needs a separate sandbox token)
  python upload_zenodo.py --sandbox --token <SANDBOX_TOKEN> --publish

  # production: create draft, upload the deposit zip, publish, then backfill the
  # repository (manuscript Data Availability, CITATION.cff, README, rebuild .docx)
  python upload_zenodo.py --token <PROD_TOKEN> --publish --fill-doi

  # show exactly what would be sent, without touching the network
  python upload_zenodo.py --dry-run

Token resolution order: --token  >  env ZENODO_TOKEN  >  ./zenodo_token.txt
Never echo the token.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
import time
import http.client
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent  # project root (script lives in submission/zenodo/)
PROD_BASE = "https://zenodo.org"
SANDBOX_BASE = "https://sandbox.zenodo.org"

DEFAULT_FILES = ["cpsp_drg_repurposing_deposit.zip"]
TOKEN_FILE = HERE / "zenodo_token.txt"

# Repository files touched by --fill-doi
MANUSCRIPT = REPO / "reports" / "MVP_PLOSONE_submission.md"
BUILDER = REPO / "scripts" / "build_sr_submission_pack.py"
README = REPO / "README.md"
CITATION = REPO / "CITATION.cff"
REPORTING = REPO / "submission_pack" / "Reporting_Summary.md"
DOI_PLACEHOLDER = "10.5281/zenodo.XXXXXXX"

# ---------------------------------------------------------------------------
# Metadata (CPSP v1.8.0)
# ---------------------------------------------------------------------------
TITLE = (
    "CPSP DRG-spinal-axis target locking and FDA drug-repurposing virtual "
    "screening: a reproducibility package (v1.8.0)"
)
AFFILIATION = (
    "The Second Affiliated Hospital of Fujian University of Traditional Chinese "
    "Medicine, Fuzhou, Fujian 350003, China"
)
ORCID = "0009-0004-9698-6552"
VERSION = "v1.8.0"

DESCRIPTION = (
    "Reproducibility package for the chronic postsurgical pain (CPSP) "
    "DRG–spinal-cord-axis target-locking and FDA-approved drug-repurposing "
    "virtual-screening study (single-author; P1–P6).<br><br>"
    "<b>What it contains.</b> The manuscript and its submission pack (Manuscript.docx "
    "with 5 embedded figures ≥300 DPI, Supporting Information, cover letter, STROBE "
    "checklist, reporting summary), all consolidated result tables (cross-dataset "
    "Stouffer meta-analysis, gene-set statistics with set-level correction, dual "
    "machine-learning hub-gene lists, per-dataset DEG tables, single-cell / spatial "
    "localisation tables, bulk-only sensitivity, target plausibility, random-effects "
    "and nerve-injury-only meta, and the target-set bootstrap), the Figure 1–5 "
    "source PNGs, the reproduction + build scripts, and a SHA-256 manifest "
    "(MANIFEST.sha256).<br><br>"
    "<b>Honest repurposing null.</b> The structure-based virtual screen of the ChEMBL "
    "max_phase=4 approved-drug library (3,085 unique drugs) against ten tractable hub "
    "targets produced no robust enrichment (full-library AUC 0.532, p = 0.118, NS). "
    "This is the reported, intended result. The control-based validation framework "
    "— docking-parameter fidelity, independently labelled (ChEMBL) enrichment, "
    "molecular-weight confounder control (size-only and 2D-physicochemical baselines "
    "with paired ΔAUC confidence intervals), and a reportable face-validity test "
    "— is what makes the null informative rather than a methodological failure. "
    "Every number in the manuscript traces to the files here; nothing was fabricated.<br><br>"
    "<b>Excluded by design.</b> The ~11 GB raw GEO counts (data/) and the prepared "
    "receptor/ligand structures (docking/) are not bundled: they are regenerable from "
    "the 12 public GEO accessions, the documented RCSB PDB IDs and ChEMBL SMILES. The "
    "consolidated docking-score table (P6_docking_scores_merged.csv) is included as the "
    "screen output of record. The canonical source is the versioned GitHub release "
    "v1.8.0.<br><br>"
    "<b>File layout.</b> This deposit is published as sequential split volumes "
    "(cpsp_drg_repurposing_deposit.zip.001, .002, …) because the upload egress stalls on "
    "single transfers larger than ~2 MiB. Download all volumes into one folder and "
    "recombine with <code>cat cpsp_drg_repurposing_deposit.zip.* &gt; "
    "cpsp_drg_repurposing_deposit.zip</code> (Linux/macOS/WSL) or the equivalent "
    "PowerShell/<code>split</code>-tool command (see 00_REASSEMBLE.txt); the recombined "
    "file is byte-identical to the original zip. Unzip it to obtain the manuscript, "
    "submission pack, derived_tables, figures, code and MANIFEST.sha256."
)

KEYWORDS = [
    "chronic postsurgical pain",
    "dorsal root ganglion",
    "spinal cord",
    "drug repurposing",
    "virtual screening",
    "AutoDock Vina",
    "transcriptomics",
    "machine learning",
    "reproducibility",
    "null results",
]

RELATED = [{
    "relation_type": {"id": "isderivedfrom"},
    "scheme": "url",
    "identifier": "https://github.com/yyx-4113/cpsp-drg-spinal-repurposing/releases/tag/v1.8.0",
}]


def build_metadata() -> dict:
    today = _dt.date.today().isoformat()
    return {
        "metadata": {
            "title": TITLE,
            "description": DESCRIPTION,
            "publication_date": today,
            "resource_type": {"id": "software"},
            "creators": [
                {
                    "person_or_org": {
                        "type": "personal",
                        "name": "Yang, Yongxin",
                        "given_name": "Yongxin",
                        "family_name": "Yang",
                        "identifiers": [{"scheme": "orcid", "identifier": ORCID}],
                    },
                    "affiliations": [{"name": AFFILIATION}],
                    "role": {"id": "researcher"},
                }
            ],
            "rights": [{"id": "mit"}],
            "languages": [{"id": "eng"}],
            "keywords": KEYWORDS,
            "related_identifiers": RELATED,
            "publisher": "Zenodo",
            "version": VERSION,
        }
    }


# ---------------------------------------------------------------------------
# Thin HTTP helper
# ---------------------------------------------------------------------------
def _req(base, path, token, method="GET", json_body=None, raw_body=None,
         content_type=None, timeout=300, extra_headers=None):
    url = path if str(path).startswith("http") else base + path
    headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
    if extra_headers:
        headers.update(extra_headers)
    data = None
    if raw_body is not None:
        data = raw_body
        headers["Content-Type"] = content_type or "application/octet-stream"
    elif json_body is not None:
        data = json.dumps(json_body).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            payload = resp.read()
            if not payload:
                return resp.status, {}
            try:
                return resp.status, json.loads(payload)
            except Exception:
                return resp.status, {"_raw": payload[:800].decode("utf-8", "replace")}
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "replace")
        try:
            return e.code, json.loads(body)
        except Exception:
            return e.code, {"error": body[:1500]}
    except (urllib.error.URLError, OSError, http.client.HTTPException) as e:
        # Covers transient egress-proxy drops (RemoteDisconnected / ConnectionReset),
        # which urllib raises as http.client.HTTPException rather than URLError.
        return 0, {"error": f"network unreachable: {e!r}"}


def _fail(msg, payload=None):
    print(f"  \u2717 {msg}", file=sys.stderr)
    if payload is not None:
        print(f"    response: {json.dumps(payload)[:1500]}", file=sys.stderr)
    sys.exit(1)


def extract_version_doi(rec):
    if not isinstance(rec, dict):
        return None
    pids = rec.get("pids") or {}
    d = pids.get("doi") or {}
    if d.get("identifier"):
        return d["identifier"]
    if rec.get("doi"):
        return rec["doi"]
    l = (rec.get("links") or {}).get("doi")
    if l:
        return l.rstrip("/").split("doi.org/")[-1]
    return None


def extract_concept_doi(rec):
    if not isinstance(rec, dict):
        return None
    links = rec.get("links") or {}
    if links.get("parent_doi"):
        return links["parent_doi"].rstrip("/").split("doi.org/")[-1]
    parent = rec.get("parent") or {}
    pd = (parent.get("pids") or {}).get("doi") or {}
    if pd.get("identifier"):
        return pd["identifier"]
    if rec.get("conceptdoi"):
        return rec["conceptdoi"]
    if links.get("conceptdoi"):
        return links["conceptdoi"].rstrip("/").split("doi.org/")[-1]
    return None


# ---------------------------------------------------------------------------
# Steps
# ---------------------------------------------------------------------------
def create_draft(base, token):
    print("[1/6] creating empty draft record ...")
    body = {
        "access": {"record": "public", "files": "public"},
        "files": {"enabled": True},
        **build_metadata(),
    }
    status, resp = _req(base, "/api/records", token, method="POST", json_body=body)
    if status not in (200, 201):
        _fail(f"draft creation failed (HTTP {status})", resp)
    rid = resp.get("id")
    print(f"  \u2713 draft id={rid}  edit at {(resp.get('links') or {}).get('self_html', '')}")
    return resp


def draft_committed_keys(base, token, rid):
    """Return the set of file keys already present AND completed in the draft.

    Retries the listing GET on transient network drops so a single proxy blip at
    startup does not force a full re-upload of everything already committed.
    """
    for attempt in range(1, 5):
        status, resp = _req(base, f"/api/records/{rid}/draft/files", token, method="GET")
        if status == 200:
            ents = resp.get("entries", []) if isinstance(resp, dict) else (resp if isinstance(resp, list) else [])
            done = set()
            for f in ents:
                if f.get("status") == "completed":
                    done.add(f.get("key"))
            return done
        print(f"  ! committed-keys GET attempt {attempt} HTTP {status}; "
              f"retrying in {min(2 ** attempt, 30)}s")
        time.sleep(min(2 ** attempt, 30))
    return set()


def upload_files(base, token, draft, paths, skip_existing=True):
    """Upload each file via single PUT (proven reliable for <=~2 MiB on this egress).

    Resumable: files already committed in the draft are skipped. If a file fails
    after retries (flaky proxy), it is recorded and the loop continues so already
    uploaded files are not lost -- the caller publishes only once EVERY file is
    present. Returns the list of keys that failed this run.
    """
    rid = draft["id"]
    done = draft_committed_keys(base, token, rid) if skip_existing else set()
    failed = []
    for i, p in enumerate(paths, 1):
        p = Path(p)
        if not p.exists():
            _fail(f"file not found: {p}")
        if skip_existing and p.name in done:
            print(f"[3/6] file {i}/{len(paths)}: {p.name} already committed -- skip")
            continue
        size = p.stat().st_size
        print(f"[3/6] registering file {i}/{len(paths)}: {p.name} ({size:,} bytes) ...")
        # Register the file key, retrying on transient proxy glitches (e.g. HTTP 400
        # injected by the egress proxy). Only proceed to content upload once the key
        # actually exists -- a failed registration makes the PUT 404 ("no file").
        # 409 = already registered (resume); treat as success.
        registered = False
        for attempt in range(1, 6):
            status, resp = _req(base, f"/api/records/{rid}/draft/files", token,
                                method="POST", json_body=[{"key": p.name}])
            if status in (200, 201, 409):
                registered = True
                break
            print(f"    ! registration attempt {attempt} HTTP {status}: "
                  f"{str(resp)[:80]}; retrying in {min(2 ** attempt, 30)}s")
            time.sleep(min(2 ** attempt, 30))
        if not registered:
            print(f"  \u2717 {p.name} registration FAILED this run; will retry on next run")
            failed.append(p.name)
            continue
        content_url = f"/api/records/{rid}/draft/files/{p.name}/content"
        print(f"        uploading bytes (single PUT, retry on network reset) ...")
        data = p.read_bytes()
        ok = False
        for attempt in range(1, 6):
            status, resp = _req(base, content_url, token, method="PUT",
                                raw_body=data, content_type="application/octet-stream",
                                timeout=900)
            if status in (200, 201):
                ok = True
                break
            print(f"    ! single PUT attempt {attempt} HTTP {status}: "
                  f"{str(resp)[:100]}; retrying in {min(2 ** attempt, 30)}s")
            time.sleep(min(2 ** attempt, 30))
        if not ok:
            print(f"  \u2717 {p.name} FAILED this run (HTTP {status}); will retry on next run")
            failed.append(p.name)
            continue
        print(f"        committing ...")
        status, resp = _req(base, f"/api/records/{rid}/draft/files/{p.name}/commit",
                            token, method="POST")
        if status not in (200, 201, 202):
            print(f"  \u2717 {p.name} commit FAILED this run (HTTP {status}); will retry on next run")
            failed.append(p.name)
            continue
        print(f"  \u2713 {p.name} uploaded and committed")
        time.sleep(1)  # gentle pause so the egress proxy is not saturated
    return failed


def update_draft_metadata(base, token, draft):
    """PUT the full (corrected) metadata onto the existing draft before publishing,
    so any schema fixes (e.g. related_identifiers.relation_type) are applied to the
    resumed draft rather than only to freshly-created ones."""
    rid = draft["id"]
    print("[5/6] updating draft metadata (re-PUT corrected schema) ...")
    status, resp = _req(base, f"/api/records/{rid}/draft", token, method="PUT",
                        json_body=build_metadata())
    if status not in (200, 201):
        _fail(f"draft metadata update failed (HTTP {status})", resp)
    print(f"  \u2713 draft metadata updated")
    return resp


def publish(base, token, draft):
    rid = draft["id"]
    print("[6/6] publishing ...")
    status, resp = _req(base, f"/api/records/{rid}/draft/actions/publish",
                        token, method="POST")
    if status not in (200, 202):
        _fail(f"publish failed (HTTP {status})", resp)
    # The 202 publish body is NOT the record; fetch it to read the minted DOI.
    st2, rec = _req(base, f"/api/records/{rid}", token, method="GET")
    if st2 not in (200,):
        rec = resp
    vdoi = extract_version_doi(rec)
    cdoi = extract_concept_doi(rec)
    html = (rec.get("links") or {}).get("self_html") or (rec.get("links") or {}).get("record_html")
    print(f"  \u2713 published: {html}")
    if cdoi:
        print(f"  \u2713 concept DOI : {cdoi}")
    if vdoi:
        print(f"  \u2713 version DOI : {vdoi}")
    return rec, vdoi, cdoi


def new_version(base, token, old_id, paths):
    print(f"[new-version] creating new version of record {old_id} ...")
    st, r = _req(base, f"/api/records/{old_id}/versions", token, method="POST")
    if st not in (200, 201):
        _fail(f"new-version creation failed (HTTP {st})", r)
    new_id = r.get("id")
    print(f"  \u2713 new draft id={new_id}")
    st, r = _req(base, f"/api/records/{new_id}/draft", token, method="PUT",
                 json_body=build_metadata())
    if st not in (200, 201):
        _fail(f"new-version metadata update failed (HTTP {st})", r)
    upload_files(base, token, {"id": new_id}, paths)
    rec, vdoi, cdoi = publish(base, token, {"id": new_id})
    return rec, vdoi, cdoi


# ---------------------------------------------------------------------------
# Post-publish repository backfill (--fill-doi)
# ---------------------------------------------------------------------------
def _bake_manuscript_da(txt, doi):
    old = ("no Zenodo snapshot has been deposited. Data are therefore available "
           "from the versioned GitHub release, not on request.")
    new = (f"a Zenodo snapshot of this reproducibility package is deposited under "
           f"DOI {doi} (https://doi.org/{doi}); the data are additionally available "
           f"from the Zenodo archive and the versioned GitHub release, not on request.")
    if old in txt:
        return txt.replace(old, new), True
    return txt, False


def fill_doi_in_repo(doi, rebuild_docx=True):
    print(f"[fill-doi] backfilling DOI {doi} into the repository ...")
    changed = []

    # 1) manuscript Data Availability statement
    if MANUSCRIPT.exists():
        txt = MANUSCRIPT.read_text(encoding="utf-8")
        new_txt, ok = _bake_manuscript_da(txt, doi)
        if ok:
            MANUSCRIPT.write_text(new_txt, encoding="utf-8")
            changed.append("reports/MVP_PLOSONE_submission.md Data Availability -> DOI")
        else:
            print("  ! manuscript DA placeholder not found; left unchanged")

    # 2) rebuild the .docx from the updated markdown
    if rebuild_docx and BUILDER.exists():
        print(f"  rebuilding Manuscript.docx via {BUILDER.name} ...")
        r = subprocess.run([sys.executable, str(BUILDER)], cwd=str(REPO))
        changed.append(f"submission_pack/Manuscript.docx rebuilt (rc={r.returncode})")

    # 3) CITATION.cff -- add an identifiers: doi block (idempotent)
    if CITATION.exists():
        s = CITATION.read_text(encoding="utf-8")
        if doi not in s and "identifiers:" not in s:
            block = (
                "identifiers:\n"
                "  - type: doi\n"
                f"    value: {doi}\n"
                "    description: Concept DOI resolving to the versioned "
                "reproducibility deposit on Zenodo.\n"
            )
            s = s.replace("version: v1.8.0\n", "version: v1.8.0\n" + block, 1)
            CITATION.write_text(s, encoding="utf-8")
            changed.append("CITATION.cff identifiers: doi added")
        else:
            print("  ! CITATION.cff already carries the DOI; left unchanged")

    # 4) README.md -- add a Zenodo badge (idempotent)
    if README.exists():
        s = README.read_text(encoding="utf-8")
        if doi not in s:
            badge = (f"[![DOI](https://zenodo.org/badge/DOI/{doi}.svg)]"
                     f"(https://doi.org/{doi})\n")
            s = re.sub(r"^(# .*)$", r"\1\n\n" + badge, s, count=1, flags=re.M)
            README.write_text(s, encoding="utf-8")
            changed.append("README.md Zenodo badge added")
        else:
            print("  ! README.md already carries the DOI; left unchanged")

    # 5) Reporting_Summary.md -- swap the acceptance placeholder if present
    if REPORTING.exists():
        s = REPORTING.read_text(encoding="utf-8")
        if "Zenodo DOI on acceptance" in s:
            s = s.replace("Zenodo DOI on acceptance",
                          f"Zenodo DOI: {doi} (assigned at submission)")
            REPORTING.write_text(s, encoding="utf-8")
            changed.append("submission_pack/Reporting_Summary.md DOI filled")
        else:
            print("  ! Reporting_Summary.md has no 'on acceptance' placeholder; left unchanged")

    for c in changed:
        print(f"  \u2713 {c}")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def resolve_token(args):
    if args.token:
        return args.token.strip()
    if os.environ.get("ZENODO_TOKEN"):
        return os.environ["ZENODO_TOKEN"].strip()
    if TOKEN_FILE.exists():
        return TOKEN_FILE.read_text(encoding="utf-8").strip()
    return None


def main():
    ap = argparse.ArgumentParser(
        description="One-command Zenodo deposit for the CPSP reproducibility package.")
    ap.add_argument("--token", help="Zenodo personal access token (deposit:write + deposit:actions). "
                                   "Falls back to $ZENODO_TOKEN or ./zenodo_token.txt")
    ap.add_argument("--sandbox", action="store_true",
                    help="use https://sandbox.zenodo.org (needs a separate sandbox token)")
    ap.add_argument("--files", nargs="+", default=DEFAULT_FILES,
                    help="deposit file(s) (default: the built zip)")
    ap.add_argument("--publish", action="store_true",
                    help="publish after upload (without it, the record stays a draft)")
    ap.add_argument("--new-version", metavar="RECORD_ID", type=int,
                    help="create a NEW VERSION of an existing record, upload --files, and "
                         "publish (used to re-deposit a DOI-baked zip after --fill-doi)")
    ap.add_argument("--resume", metavar="DRAFT_ID", type=int,
                    help="resume an EXISTING draft (skip create_draft); used to recover from "
                         "a network drop mid-upload without spawning a new orphan draft")
    ap.add_argument("--fill-doi", action="store_true",
                    help="after publishing, backfill the DOI into the manuscript DA, "
                         "CITATION.cff, README and rebuild the .docx")
    ap.add_argument("--patch-doi", metavar="DOI",
                    help="ONLY backfill the DOI into the repo and rebuild the PDF/docx "
                         "(no network, no token needed)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the exact payload and plan without touching the network")
    ap.add_argument("--no-proxy", action="store_true",
                    help="disable the egress HTTP proxy (clear *_proxy env vars) and connect "
                         "directly to Zenodo; use when the proxy MITMs TLS with a mismatched cert")
    args = ap.parse_args()

    if args.no_proxy:
        for _k in ("http_proxy", "https_proxy", "HTTP_PROXY", "HTTPS_PROXY",
                   "all_proxy", "ALL_PROXY"):
            os.environ.pop(_k, None)
        print("[no-proxy] egress HTTP proxy disabled; connecting directly to Zenodo")

    if args.patch_doi:
        fill_doi_in_repo(args.patch_doi.strip())
        return

    base = SANDBOX_BASE if args.sandbox else PROD_BASE
    # Default (no --files override): publish the sequential split volumes produced by
    # make_deposit.py, plus the reassembly helper, so each PUT stays under the proxy limit.
    if args.files == DEFAULT_FILES:
        parts = sorted(HERE.glob("cpsp_drg_repurposing_deposit.zip.[0-9][0-9][0-9]"))
        reasm = HERE / "00_REASSEMBLE.txt"
        files = [str(p) for p in parts]
        if reasm.exists():
            files.append(str(reasm))
        if not parts:
            _fail("no split volumes found in submission/zenodo/; run make_deposit.py first")
    else:
        files = [str((HERE / f) if not Path(f).is_absolute() else Path(f)) for f in args.files]

    print("=" * 72)
    print("Zenodo deposit -- CPSP reproducibility package")
    print(f"  host    : {base}{'   (SANDBOX)' if args.sandbox else '   (PRODUCTION)'}")
    print(f"  files   : {', '.join(Path(f).name for f in files)}")
    print(f"  publish : {args.publish}   fill-doi: {args.fill_doi}   "
          f"new-version: {args.new_version or '-'}")
    print("=" * 72)

    if args.dry_run:
        print("[dry-run] metadata payload that would be POSTed to /api/records:")
        print(json.dumps(build_metadata(), indent=2, ensure_ascii=False))
        print("\n[dry-run] planned calls:")
        print(f"  POST {base}/api/records")
        for f in files:
            print(f"  POST {base}/api/records/<id>/draft/files   key={Path(f).name}")
            print(f"  PUT  {base}/api/records/<id>/draft/files/{Path(f).name}/content   "
                  f"({Path(f).stat().st_size if Path(f).exists() else '?'} bytes)")
            print(f"  POST {base}/api/records/<id>/draft/files/{Path(f).name}/commit")
        if args.publish:
            print(f"  POST {base}/api/records/<id>/draft/actions/publish")
        return

    token = resolve_token(args)
    if not token:
        _fail("no token. Pass --token, set $ZENODO_TOKEN, or create ./zenodo_token.txt")

    if args.new_version:
        rec, vdoi, cdoi = new_version(base, token, args.new_version, files)
        doi = cdoi or vdoi
        if args.fill_doi and doi:
            fill_doi_in_repo(doi)
    else:
        draft_id = args.resume
        if draft_id:
            draft = {"id": draft_id}
            print(f"[resume] reusing existing draft id={draft_id}")
        else:
            draft = create_draft(base, token)
            draft_id = draft["id"]
        print(f"[info] draft id={draft_id} -- upload is resumable: volumes already "
              f"committed in the draft are skipped automatically")
        # Single pass, resumable. upload_files returns the keys that failed THIS
        # pass (flaky proxy); we publish ONLY when every planned file is committed.
        failed = upload_files(base, token, draft, files)
        if failed:
            print()
            print("=" * 72)
            print(f"UPLOAD INCOMPLETE: {len(failed)}/{len(files)} volumes not yet "
                  f"committed on draft {draft_id}:")
            for k in failed:
                print(f"  - {k}")
            print("Re-run the SAME command with --resume "
                  f"{draft_id} to continue; committed volumes are skipped.")
            print("=" * 72)
            doi = None
        else:
            if args.publish:
                update_draft_metadata(base, token, draft)
                rec, vdoi, cdoi = publish(base, token, draft)
                doi = cdoi or vdoi
                if args.fill_doi and doi:
                    fill_doi_in_repo(doi)
            else:
                print(f"[done] draft left unpublished. Review and publish at: "
                      f"{(draft.get('links') or {}).get('self_html')}")
                doi = None

    print()
    print("=" * 72)
    if doi:
        print(f"RESULT_DOI={doi}")
        print(f"RESULT_URL=https://doi.org/{doi}")
    else:
        print("RESULT_DOI=(none yet - record not published)")
    print("=" * 72)


if __name__ == "__main__":
    main()
