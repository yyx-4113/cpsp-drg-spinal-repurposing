#!/usr/bin/env python3
"""Verify the Scientific Reports .docx pack lost nothing in conversion.

Proof strategy (loss-free transformation of the *authored* text):
  1. FORWARD numeric-token check: every numeric token in the exported markdown
     (manuscript body+legends, supplementary prose, cover letter) is present in
     the corresponding .docx paragraph text -> nothing was dropped/altered.
     (The three main tables are materialised from CSVs, so the reverse
     "no invented numbers" check is replaced by explicit CSV cross-checks.)
  2. No Chinese (CJK) text reaches any submitted file.
  3. Mandatory strings survive (repo URL, ORCID, AI disclosure, competing
     interests, reference anchors, S1-S4 pointers, cover-letter anchors).
  4. Table counts: Manuscript == 4 (3a plausibility + 1b SCN + Table 2 hubs +
     3b verdicts), Supplementary >= 4, Cover Letter == 0.
  5. No placeholder markers remain.
  6. Generated-table cross-checks against the v1.3 manuscript entities:
     3a = 10 targets, 1b = 4 SCN channels (SCN8A -4.92 / 1.0e-5),
     Table 2 = 35 hub rows, 3b = 5 targets (ADRA2A 0.532 / q 0.0025).
  7. Figure DPI >= 300 (pHYs chunk).

Exit 0 = pass.
"""

from __future__ import annotations

import os
import re
import struct
import sys

from docx import Document

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "reports")
TBL = os.path.join(ROOT, "results", "tables")
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "submission_pack")

MS = os.path.join(REP, "MVP_ScientificReports_submission.md")
SUP = os.path.join(REP, "MVP_ScientificReports_supplementary.md")
CL = os.path.join(REP, "MVP_ScientificReports_cover_letter.md")

NUM = re.compile(r"\d[\d,]*(?:\.\d+)?")
OK, BAD = [], []


def chk(label, got, exp=True):
    (OK if got == exp else BAD).append(f"{label}: got={got!r} exp={exp!r}")


def tokens(text: str) -> set[str]:
    # strip markdown emphasis markers so the tokenisation matches the rendered
    # .docx (render_markdown drops ** / * ; plaintext must mirror that), and
    # avoid the comma in \d[\d,]* swallowing a trailing "," that only exists
    # in the rendered text (e.g. Nature-style "... *Pain* **159**, 1465").
    return set(NUM.findall(text.replace("`", "").replace("*", "")))


def docx_para_text(path: str) -> str:
    """Only paragraph text (excludes table cells) — used for the forward check."""
    d = Document(path)
    return "\n".join(p.text for p in d.paragraphs)


def docx_full_text(path: str) -> str:
    d = Document(path)
    parts = [p.text for p in d.paragraphs]
    for t in d.tables:
        for r in t.rows:
            for c in r.cells:
                parts.append(c.text)
    return "\n".join(parts)


def docx_table_count(path: str) -> int:
    return len(Document(path).tables)


def docx_tables_rows(path: str) -> list[list[list[str]]]:
    d = Document(path)
    return [[[c.text for c in r.cells] for r in t.rows] for t in d.tables]


def plaintext(block: str) -> str:
    """Mirror what render_markdown emits as paragraph text (no table cells)."""
    out = []
    for raw in block.split("\n"):
        s = raw.strip()
        if not s or s == "---":
            continue
        if s.startswith(">"):
            continue
        if is_table_row(s):
            continue
        if s.startswith("* "):
            s = s[2:]
        out.append(s)
    return "\n".join(out)


def is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def split_manuscript(text: str) -> tuple[str, str]:
    idx = text.index("## Display items")
    return text[:idx], text[idx:]


def extract_legend_text(display_text: str) -> str:
    lines = display_text.split("\n")
    figs, cur, in_fig, buf = [], None, False, []
    for raw in lines:
        s = raw.strip()
        if s.startswith("**Figures**"):
            in_fig = True
            continue
        if s.startswith("**Tables**") or s.startswith("**Supplementary"):
            in_fig = False
            if cur:
                figs.append(cur)
                cur = None
            continue
        if not in_fig:
            continue
        m = re.match(r"^- \*\*Fig\. (\d+)\*\*\s+`([^`]+)`\s+—\s+(.+)$", s)
        if m:
            if cur:
                figs.append(cur)
            cur = f"Figure {m.group(1)}. {m.group(3)}"
        elif s.startswith("*Legend.*") and cur is not None:
            cur += " " + s[len("*Legend.*"):].strip()
        elif cur is not None and s and not s.startswith("- **Fig"):
            cur += " " + s
    if cur:
        figs.append(cur)
    return "\n".join(figs)


def png_dpi(path):
    with open(path, "rb") as f:
        data = f.read()
    i = 8
    while i + 8 <= len(data):
        ln = struct.unpack(">I", data[i:i + 4])[0]
        typ = data[i + 4:i + 8]
        if typ == b"pHYs":
            x, _y, unit = struct.unpack(">IIB", data[i + 8:i + 17])
            return (x / 39.3701) if unit == 1 else None
        i += 12 + ln
    return None


def main() -> int:
    ms = os.path.join(OUT, "Manuscript.docx")
    si = os.path.join(OUT, "Supporting_Information.docx")
    cl = os.path.join(OUT, "Cover_Letter.docx")
    for p in (ms, si, cl):
        chk(f"file exists {os.path.basename(p)}", os.path.exists(p))

    # ---- expected (authored text) ---------------------------------------- #
    mt = open(MS, encoding="utf-8").read()
    part_a, display = split_manuscript(mt)
    # the Tables sub-block of Display items is rendered verbatim by the builder
    tbl_blk = display[display.index("**Tables**"):]
    tbl_blk = tbl_blk[:tbl_blk.index("**Supplementary Information**")]
    expected_main = (plaintext(part_a) + "\n" + extract_legend_text(display)
                     + "\n" + plaintext(tbl_blk))
    expected_supp = plaintext(open(SUP, encoding="utf-8").read())
    expected_cl = plaintext(open(CL, encoding="utf-8").read())

    ms_para = docx_para_text(ms)
    si_para = docx_para_text(si)
    cl_para = docx_para_text(cl)

    # 1. forward numeric tokens
    for label, md_src, dx_text in [("Manuscript", expected_main, ms_para),
                                   ("Supporting", expected_supp, si_para),
                                   ("CoverLetter", expected_cl, cl_para)]:
        a = tokens(md_src)
        b = tokens(dx_text)
        missing = sorted(a - b)
        chk(f"[{label}] no dropped numbers", missing, [])

    # 2. no Chinese
    for label, t in [("Manuscript", docx_full_text(ms)),
                     ("Supporting", docx_full_text(si)),
                     ("CoverLetter", docx_full_text(cl))]:
        chk(f"[{label}] no Chinese", re.findall(r"[\u4e00-\u9fff]", t), [])

    # 3. mandatory strings
    chk("Manuscript has repo URL",
        "https://github.com/yyx-4113/cpsp-drg-spinal-repurposing" in ms_para)
    chk("Manuscript has ORCID", "0009-0004-9698-6552" in ms_para)
    chk("Manuscript has AI disclosure", "large language model" in ms_para.lower())
    chk("Manuscript has Competing interests", "Competing interests" in ms_para)
    chk("Manuscript has ref1 (Macrae)", "Macrae" in ms_para)
    chk("Manuscript has ref18 (Luo/Mol Pain 2016)", "1744806916636385" in ms_para)
    chk("CoverLetter has repo URL",
        "https://github.com/yyx-4113/cpsp-drg-spinal-repurposing" in cl_para)
    chk("CoverLetter has ORCID", "0009-0004-9698-6552" in cl_para)
    chk("CoverLetter names Scientific Reports", "Scientific Reports" in cl_para)
    for s in ["Table S1", "Table S2", "Table S3", "Table S4", "Table S5"]:
        chk(f"Supporting has {s}", s in docx_full_text(si))

    # 4. table counts (v1.3: 4 docx tables in the manuscript)
    chk("Manuscript table count == 4", docx_table_count(ms), 4)
    chk("Supporting table count >= 4", docx_table_count(si) >= 4, True)
    chk("CoverLetter table count == 0", docx_table_count(cl), 0)

    # 5. no placeholders
    for label, t in [("Manuscript", docx_full_text(ms)),
                     ("Supporting", docx_full_text(si)),
                     ("CoverLetter", docx_full_text(cl))]:
        left = [m for m in ["[[", "TODO", "TBD", "XXX",
                             "COMPLETE BEFORE SUBMISSION", "PLACEHOLDER"]
                if m in t]
        chk(f"[{label}] no placeholders", left, [])

    # 6. generated-table cross-checks (v1.3 entities, content-keyed)
    tables = docx_tables_rows(ms)
    t_txt = lambda t: "\n".join(" ".join(r) for r in t)

    t_plaus = next((t for t in tables
                    if any("n_holo_PDB" in c for c in t[0])), None)
    chk("Table 3a (plausibility) found", t_plaus is not None)
    if t_plaus:
        chk("Table 3a = 10 target rows", len(t_plaus) - 1, 10)
        chk("Table 3a has TNIK + ADRA2A",
            "TNIK" in t_txt(t_plaus) and "ADRA2A" in t_txt(t_plaus))

    t_scn = next((t for t in tables
                  if t and t[0] and t[0][0].strip() == "Gene"), None)
    chk("Table 1b (SCN directions) found", t_scn is not None)
    if t_scn:
        chk("Table 1b = 4 channel rows", len(t_scn) - 1, 4)
        chk("Table 1b SCN8A -4.92 / 1.0e-5",
            "4.92" in t_txt(t_scn) and "1.0e-5" in t_txt(t_scn))
        chk("Table 1b shows incision UP",
            t_txt(t_scn).count("UP") >= 4)

    t_hubs = next((t for t in tables if len(t) == 36), None)
    chk("Table 2 = 35 hub rows", t_hubs is not None and len(t_hubs) - 1, 35)
    if t_hubs:
        chk("Table 2 has SPRR1A", "SPRR1A" in t_txt(t_hubs))
        chk("Table 2 has MEGF11", "MEGF11" in t_txt(t_hubs))

    t_verd = next((t for t in tables
                   if any("Reverse-control" in c for c in t[0])), None)
    chk("Table 3b (verdicts) found", t_verd is not None)
    if t_verd:
        chk("Table 3b = 5 target rows", len(t_verd) - 1, 5)
        chk("Table 3b ADRA2A 0.532 / size-indep q 0.0025",
            "ADRA2A" in t_txt(t_verd) and "0.532" in t_txt(t_verd)
            and "0.0025" in t_txt(t_verd))

    # 7. figure DPI
    dpi_all_ok = True
    for fn in sorted(os.listdir(FIG)):
        if fn.endswith(".png"):
            d = png_dpi(os.path.join(FIG, fn))
            ok = d is not None and d >= 300
            dpi_all_ok = dpi_all_ok and ok
            print(f"[{'PASS' if ok else 'FAIL'}] {fn}: "
                  + (f"{d:.3f} DPI" if d is not None else "no DPI metadata"))
    chk("All figures >= 300 DPI", dpi_all_ok, True)

    print(f"\n==== PASS {len(OK)} / FAIL {len(BAD)} ====")
    for b in BAD:
        print("  [X]", b)
    return 1 if BAD else 0


if __name__ == "__main__":
    sys.exit(main())
