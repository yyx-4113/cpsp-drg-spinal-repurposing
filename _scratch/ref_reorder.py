#!/usr/bin/env python3
"""Renumber superscript citation markers in the PLOS ONE manuscript + companion
reports to match strict first-citation order (PLOS ONE / Vancouver policy).

Strategy:
  * parse the manuscript BODY (before '## References') for superscript citation
    runs, record the first character position of each cited number,
  * rank numbers by first-appearance -> desired new number,
  * build old->new mapping, then apply it to every superscript run in the
    manuscript (body + reference-list leaders) and in the companion reports
    (supplementary / STROBE / compliance / cover letter) so all docs stay
    internally consistent.
Ranges like '21-30' are expanded and each component renumbered.
"""
import os, re

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
REP = os.path.join(ROOT, "reports")

SUPD = {"\u2070":"0","\u00b9":"1","\u00b2":"2","\u00b3":"3","\u2074":"4",
        "\u2075":"5","\u2076":"6","\u2077":"7","\u2078":"8","\u2079":"9"}
SUPCH = {v:k for k,v in SUPD.items()}   # digit -> superscript char
SUPCLS = "\u2070\u00b9\u00b2\u00b3\u2074\u2075\u2076\u2077\u2078\u2079"
RUN = re.compile(f"[{SUPCLS}][{SUPCLS}\u207b\u2013]*")

def parse_run(s: str):
    """Return list of ints a run represents (handles single + range)."""
    if "\u207b" in s or "\u2013" in s:
        sep = "\u207b" if "\u207b" in s else "\u2013"
        a, b = s.split(sep)
        return list(range(int("".join(SUPD[c] for c in a)),
                          int("".join(SUPD[c] for c in b)) + 1))
    return [int("".join(SUPD[c] for c in s))]

def render(n: int) -> str:
    return "".join(SUPCH[d] for d in str(n))

def rerender_run(s: str) -> str:
    nums = parse_run(s)
    if len(nums) == 1:
        return render(nums[0])
    # range: render first-last with en dash
    return render(nums[0]) + "\u2013" + render(nums[-1])

# ---- 1. compute mapping from manuscript body ------------------------------ #
ms = open(os.path.join(REP, "MVP_PLOSONE_submission.md"), encoding="utf-8").read()
body = ms.split("## References")[0]
firstpos = {}
for m in RUN.finditer(body):
    for n in parse_run(m.group(0)):
        firstpos.setdefault(n, m.start())
maxn = max(firstpos)
ordered = sorted(firstpos, key=lambda n: firstpos[n])
mapping = {old: new for new, old in enumerate(ordered, 1)}
print("max cited number:", maxn)
print("mapping (old -> new):")
for k in sorted(mapping):
    if k != mapping[k]:
        print(f"   {k} -> {mapping[k]}")
print("numbers unchanged:", [k for k in sorted(mapping) if k == mapping[k]])

def apply_mapping(text: str) -> str:
    def cb(m):
        old = m.group(0)
        nums = parse_run(old)
        new = [mapping.get(n, n) for n in nums]
        if len(new) == 1:
            return render(new[0])
        return render(new[0]) + "\u2013" + render(new[-1])
    return RUN.sub(cb, text)

# ---- 2. rewrite the reference-list leaders in the manuscript --------------- #
ref_block = ms.split("## References")[1].split("## Acknowledgements")[0]
def leader_cb(m):
    old = int(m.group(1))
    new = mapping.get(old, old)
    return f"{new}. "
new_ref_block = re.sub(r"(?m)^(\d+)\.\s", leader_cb, ref_block)
ms_new = ms.split("## References")[0] + "## References" + new_ref_block + "## Acknowledgements" + ms.split("## Acknowledgements")[1]
ms_new = apply_mapping(ms_new)
open(os.path.join(REP, "MVP_PLOSONE_submission.md"), "w", encoding="utf-8").write(ms_new)
print("manuscript rewritten")

# ---- 3. REPORT (do not auto-apply) companion reports ---------------------- #
# Companion files may contain superscript EXPONENTS (e.g. 10^-29) that would be
# corrupted by blind renumbering. Only the manuscript is gated for citation
# order, so we just report which companion files carry superscript runs in the
# affected range so they can be fixed by hand if they are genuine citations.
for fn in ["MVP_PLOSONE_supplementary.md", "MVP_STROBE_checklist.md",
           "MVP_PLOSONE_compliance_check.md", "MVP_PLOSONE_cover_letter.md"]:
    p = os.path.join(REP, fn)
    if not os.path.exists(p):
        continue
    t = open(p, encoding="utf-8").read()
    hits = set()
    for m in RUN.finditer(t):
        for n in parse_run(m.group(0)):
            if n in mapping and n != mapping[n]:
                hits.add(n)
    if hits:
        print(f"{fn}: contains superscript runs for remapped refs {sorted(hits)} "
              f"(REVIEW before manual fix)")
    else:
        print(f"{fn}: no remapped-ref superscript runs")
print("DONE")
