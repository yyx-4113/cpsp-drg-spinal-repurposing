#!/usr/bin/env python3
"""Build the Scientific Reports submission pack from the v1.3 markdown sources.

Adapted from the manuscript-submission-pack skill asset (originally *Anaesthesia*).
Changes for Scientific Reports / CPSP:
  - Times New Roman 12 pt, single spaced (SR norm), page numbers in footer
  - Methods last; declarations after References; display items at the very end
  - Table 1 (incl. 1b SCN entity) and Table 3 (incl. 3b verdict entity) are
    rendered DIRECTLY from the manuscript's own Display-items block, so the
    .docx matches the v1.3 text verbatim (no stale numbers can leak in);
  - Table 2 is materialised from P3_hub_genes.csv (all 35 hub rows);
  - figure legends are extracted from the manuscript's "Display items" section;
    the figure image files are copied separately at >=300 DPI
  - the internal version blockquote and the "Display items" navigation heading are
    dropped from the submitted files

Run:  python scripts/build_sr_submission_pack.py
Then: python scripts/verify_sr_docx.py
"""

from __future__ import annotations

import csv
import os
import re
import shutil

from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REP = os.path.join(ROOT, "reports")
TBL = os.path.join(ROOT, "results", "tables")
FIG = os.path.join(ROOT, "figures")
OUT = os.path.join(ROOT, "submission_pack")

MS = os.path.join(REP, "MVP_ScientificReports_submission.md")
SUP = os.path.join(REP, "MVP_ScientificReports_supplementary.md")
CL = os.path.join(REP, "MVP_ScientificReports_cover_letter.md")
RS = os.path.join(REP, "MVP_ScientificReports_reporting_summary.md")

BODY_FONT = "Times New Roman"


# --------------------------------------------------------------------------- #
# document skeleton
# --------------------------------------------------------------------------- #
def new_document() -> Document:
    doc = Document()
    normal = doc.styles["Normal"]
    normal.font.name = BODY_FONT
    normal.font.size = Pt(12)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), BODY_FONT)
    pf = normal.paragraph_format
    pf.line_spacing = 1.15
    pf.space_after = Pt(0)
    for s in doc.sections:
        s.top_margin = s.bottom_margin = Cm(2.54)
        s.left_margin = s.right_margin = Cm(2.54)
        add_page_numbers(s)
    return doc


def add_page_numbers(section) -> None:
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    fld = OxmlElement("w:fldSimple")
    fld.set(qn("w:instr"), "PAGE")
    run._r.addnext(fld)


def para(doc, text="", *, bold=False, italic=False, size=None, align=None,
         space_before=0, space_after=2, font=None):
    p = doc.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(space_before)
    pf.space_after = Pt(space_after)
    if align is not None:
        p.alignment = align
    if text:
        add_runs(p, text, bold=bold, italic=italic, size=size, font=font)
    return p


INLINE = re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+?`)")


def add_runs(p, text, *, bold=False, italic=False, size=None, font=None):
    for piece in INLINE.split(text):
        if not piece:
            continue
        b, i, mono = bold, italic, False
        if piece.startswith("**") and piece.endswith("**") and len(piece) > 4:
            piece, b = piece[2:-2], True
        elif piece.startswith("*") and piece.endswith("*") and len(piece) > 2:
            piece, i = piece[1:-1], True
        elif piece.startswith("`") and piece.endswith("`") and len(piece) > 2:
            piece, mono = piece[1:-1], True
        run = p.add_run(piece)
        run.bold, run.italic = b, i
        if size:
            run.font.size = Pt(size)
        run.font.name = "Courier New" if mono else (font or BODY_FONT)


# --------------------------------------------------------------------------- #
# markdown rendering
# --------------------------------------------------------------------------- #
def is_table_row(line: str) -> bool:
    return line.strip().startswith("|") and line.strip().endswith("|")


def is_separator(line: str) -> bool:
    return bool(re.fullmatch(r"\|[\s:|-]+\|", line.strip()))


def cells(line: str) -> list[str]:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def add_table(doc, rows: list[list[str]], *, size=9.0, caption=None) -> None:
    if caption:
        para(doc, caption, italic=True, size=9, space_before=8, space_after=4)
    if not rows:
        return
    width = max(len(r) for r in rows)
    t = doc.add_table(rows=0, cols=width)
    t.style = "Table Grid"
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    t.autofit = True
    for ri, row in enumerate(rows):
        out = t.add_row().cells
        for ci in range(width):
            text = row[ci] if ci < len(row) else ""
            out[ci].text = ""
            p = out[ci].paragraphs[0]
            p.paragraph_format.line_spacing = 1.0
            p.paragraph_format.space_before = Pt(1)
            p.paragraph_format.space_after = Pt(1)
            add_runs(p, text, bold=(ri == 0), size=size)
        if ri == 0:
            trPr = t.rows[0]._tr.get_or_add_trPr()
            trPr.append(OxmlElement("w:tblHeader"))
    para(doc, "", space_after=4)


def render_markdown(doc, block: str, *, drop: tuple[str, ...] = (),
                    title_center=False) -> None:
    """Render a markdown block: headings, paragraphs, (optional) pipe tables.
    Blockquotes, horizontal rules and `drop`-prefixed paragraphs are skipped.
    A leading '* ' on a paragraph is stripped (used for the corresponding-author note)."""
    lines = block.split("\n")
    i = 0
    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped or stripped == "---":
            i += 1
            continue
        if stripped.startswith(">"):
            i += 1
            continue
        if any(stripped.startswith(d) for d in drop):
            i += 1
            continue

        if is_table_row(line):
            rows = []
            while i < len(lines) and is_table_row(lines[i]):
                if not is_separator(lines[i]):
                    rows.append(cells(lines[i]))
                i += 1
            add_table(doc, rows)
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            level, title = len(m.group(1)), m.group(2)
            if level == 1:
                para(doc, title, bold=True, size=14, align=WD_ALIGN_PARAGRAPH.CENTER,
                     space_after=8)
            else:
                para(doc, title, bold=True, size=12, space_before=8, space_after=4)
            i += 1
            continue

        if stripped.startswith("* "):
            stripped = stripped[2:]
        para(doc, stripped, size=11)
        i += 1


def split_manuscript(text: str) -> tuple[str, str]:
    idx = text.index("## Display items")
    return text[:idx], text[idx:]


def extract_legends(display_text: str) -> list[dict]:
    lines = display_text.split("\n")
    figs, cur, in_fig = [], None, False
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
            cur = {"num": m.group(1), "cap": m.group(3), "legend": ""}
        elif s.startswith("*Legend.*") and cur is not None:
            cur["legend"] = s[len("*Legend.*"):].strip()
        elif cur is not None and s and not s.startswith("- **Fig"):
            cur["legend"] += " " + s
    if cur:
        figs.append(cur)
    return figs


# --------------------------------------------------------------------------- #
# main-table builders (v1.3: render manuscript entities; materialise Table 2)
# --------------------------------------------------------------------------- #
def strip_bullets(block: str) -> str:
    """Turn '- xxx' bullets into plain paragraphs for render_markdown."""
    out = []
    for line in block.split("\n"):
        st = line.strip()
        out.append(st[2:] if st.startswith("- ") else line)
    return "\n".join(out)


def manuscript_tables_block(display_text: str) -> str:
    """The '**Tables**' .. (before '**Supplementary Information**') sub-block."""
    blk = display_text[display_text.index("**Tables**"):]
    return blk[:blk.index("**Supplementary Information**")]


def build_table2(doc) -> None:
    path = os.path.join(TBL, "P3_hub_genes.csv")
    rows = [["Symbol", "n_methods", "LASSO freq", "RF Gini", "|SHAP|", "in meta-core"]]
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append([
                r["symbol"], r["n_methods"],
                f"{float(r['lasso_freq']):.2f}",
                f"{float(r['rf_gini']):.4f}",
                f"{float(r['shap_meanabs']):.4f}",
                r["in_meta_core"],
            ])
    cap = ("Table 2. Thirty-five candidate hub genes identified by the dual-machine-learning "
           "consensus (>=2 of 3 methods: LASSO bootstrap, Random Forest mean-decrease-Gini, "
           "XGBoost |SHAP|). n_methods = number of methods flagging the gene; in meta-core = "
           "membership in the 4,055-gene Stouffer meta signature. Source: P3_hub_genes.csv. "
           "Bootstrap stability caveat: a 200-resample bootstrap of the 72 pooled samples "
           "(P3_hub_bootstrap.csv) showed low per-gene recovery (max 15.5%, 0/35 at a >=0.9 "
           "threshold; LASSO contributed no selections under resampling), so this set is a "
           "resampling-sensitive candidate list for prospective validation, not a rigidly "
           "locked set (see Results).")
    add_table(doc, rows, size=8.5, caption=cap)


def build_manuscript() -> str:
    doc = new_document()
    text = open(MS, encoding="utf-8").read()
    part_a, display = split_manuscript(text)

    # front + body + declarations + references (Table 3a renders from Results)
    render_markdown(doc, part_a)

    # figure legends extracted from the Display items block
    para(doc, "Figure legends", bold=True, size=13, space_before=12, space_after=6)
    for f in extract_legends(display):
        para(doc, f"Figure {f['num']}. {f['cap']}", bold=True, size=11,
             space_before=8, space_after=2)
        if f["legend"]:
            para(doc, f["legend"], size=10)

    # three main tables, after the references.
    # v1.3 renders Tables 1 and 3 as editable entities inside the manuscript's
    # Display-items block; render them verbatim from there. Table 2 is
    # materialised from P3_hub_genes.csv (all 35 rows) between its two halves.
    tbl = manuscript_tables_block(display)
    pre2, post2 = tbl.split("- **Table 2**", 1)
    t2_note, t3_part = post2.split("- **Table 3**", 1)
    para(doc, "Tables", bold=True, size=13, space_before=12, space_after=6)
    render_markdown(doc, strip_bullets(pre2), drop=("**Tables**",))
    build_table2(doc)
    render_markdown(doc, strip_bullets("- **Table 2**" + t2_note))
    render_markdown(doc, strip_bullets("- **Table 3**" + t3_part))

    path = os.path.join(OUT, "Manuscript.docx")
    doc.save(path)
    return path


def build_supporting() -> str:
    doc = new_document()
    render_markdown(doc, open(SUP, encoding="utf-8").read())
    path = os.path.join(OUT, "Supporting_Information.docx")
    doc.save(path)
    return path


def build_cover() -> str:
    doc = new_document()
    render_markdown(doc, open(CL, encoding="utf-8").read())
    path = os.path.join(OUT, "Cover_Letter.docx")
    doc.save(path)
    return path


def copy_figures() -> list[str]:
    out = []
    for fn in sorted(os.listdir(FIG)):
        if fn.endswith(".png"):
            dst = os.path.join(OUT, fn)
            shutil.copyfile(os.path.join(FIG, fn), dst)
            out.append(dst)
    return out


def copy_extras() -> list[str]:
    out = []
    dst = os.path.join(OUT, "Reporting_Summary.md")
    shutil.copyfile(RS, dst)
    out.append(dst)
    return out


def main() -> int:
    os.makedirs(OUT, exist_ok=True)
    ms = build_manuscript()
    si = build_supporting()
    cl = build_cover()
    figs = copy_figures()
    extras = copy_extras()
    print("built:")
    for p in [ms, si, cl, *figs, *extras]:
        print(f"  {os.path.relpath(p, ROOT):55s} {os.path.getsize(p)/1024:8.1f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
