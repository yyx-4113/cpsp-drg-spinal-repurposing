#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
De-AI polish pass for the CPSP MVP manuscript source (_v15_source.md).

Three deterministic, number-safe transformations:
  1. Em-dash (—, U+2014) -> comma/colon.  En-dash (–, U+2013) is preserved
     (it is the standard range / gene-axis hyphen in scientific prose).
  2. Decorative inline bold removed; structural bold (author, Keywords,
     figure/table labels, paragraph lead-ins) preserved via an allow-list.
  3. Conservative AI-tell word substitutions (no number / citation touched).

The script rewrites reports/_v15_source.md in place. A backup should already
exist as _v15_source.md.bak.
"""
import re
import sys

SRC = "reports/_v15_source.md"

# ---------------------------------------------------------------------------
# 1. EM-DASH normalisation
# ---------------------------------------------------------------------------
def fix_emdashes(text: str) -> str:
    # Figure / table legend descriptions: backtick `path` — Desc  ->  `path: Desc
    text = re.sub(r"`\s*—\s*", "` : ", text)
    # Everything else: em-dash (with any surrounding whitespace) -> ", "
    text = re.sub(r"\s*—\s*", ", ", text)
    return text


# ---------------------------------------------------------------------------
# 2. BOLD allow-list (structural only)
# ---------------------------------------------------------------------------
KEEP_BOLD = {
    "Yang Y",
    "Manuscript metadata.",
    "Keywords:",
    "Random-effects sensitivity analysis and heterogeneity.",
    "Bulk-only sensitivity meta-analysis (translatome excluded), the primary robustness check.",
    "SCN-channel directions are model-dependent (Table 1b).",
    "Reverse positive controls",
    "Target-specific biological plausibility is assessed uniformly across all 10 tractable targets",
    "The prospectively specified full-library breadth overturned the Tier-1 signal",
    "Face-validity testing refuted analgesic enrichment",
    "Hub→target eligibility rule (explicit).",
    "We therefore draw no therapeutic priority from this screen.",
    "Fixed-effect (primary).",
    "Random-effects sensitivity (DerSimonian–Laird).",
    "Consistency split and non-circular translation test.",
    "Sensitivity analyses.",
    "GSE267799 harvest-day caveat:",
    "Parameter-fidelity validation was performed before screening",
    "molecular-weight confounder correction",
    "Causal scope:",
    "Figures",
    "Fig. 1", "Fig. 2", "Fig. 3", "Fig. 4", "Fig. 5",
    "Tables", "Table 1", "Table 2", "Table 3",
    "Supplementary Information",
    "S1", "S2", "S3", "S4", "S5", "S6", "S7",
}


def strip_decorative_bold(text: str) -> str:
    def repl(m):
        inner = m.group(1)
        if inner in KEEP_BOLD:
            return "**" + inner + "**"
        return inner
    # non-greedy, non-spanning
    return re.sub(r"\*\*(.+?)\*\*", repl, text)


# ---------------------------------------------------------------------------
# 3. AI-tell word substitutions (number / citation safe)
# ---------------------------------------------------------------------------
def fix_ai_words(text: str) -> str:
    # robustly -> reliably  (do before robust)
    text = text.replace("robustly", "reliably")
    # "robust to" -> "reliable under"  (before generic robust)
    text = re.sub(r"robust to", "reliable under", text)
    # standalone robust -> reliable
    text = re.sub(r"\brobust\b", "reliable", text)
    # demonstrate / demonstrates / demonstrated -> show / shows / shown
    text = re.sub(r"demonstrat(ed|es|e)\b",
                  lambda m: {"ed": "shown", "es": "shows", "e": "show"}[m.group(1)],
                  text)
    text = text.replace("in order to", "to")
    text = re.sub(r"\badditionally\b", "also", text)
    text = re.sub(r"\bnotably\b", "in particular", text)
    text = re.sub(r"\bhighlight\b", "note", text)
    return text


# ---------------------------------------------------------------------------
def main():
    with open(SRC, encoding="utf-8") as fh:
        text = fh.read()

    before_dash = text.count("—")
    before_bold = text.count("**") // 2

    text = fix_emdashes(text)
    text = strip_decorative_bold(text)
    text = fix_ai_words(text)

    after_dash = text.count("—")
    after_bold = text.count("**") // 2

    with open(SRC, "w", encoding="utf-8") as fh:
        fh.write(text)

    print(f"em-dash  : {before_dash} -> {after_dash}")
    print(f"bold(**) : {before_bold} -> {after_bold}")
    # guard: any reference markers / numeric integrity sanity
    print("has {{ref}} markers:", "{{" in text)
    print("done.")


if __name__ == "__main__":
    main()
