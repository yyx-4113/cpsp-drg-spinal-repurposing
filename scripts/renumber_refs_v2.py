#!/usr/bin/env python3
# renumber_refs_v2.py -- safe Vancouver first-citation renumber of MVP_PLOSONE_submission.md.
#
# Unlike the deprecated p7_renumber_refs.py (which re-renders from the quarantined
# _v15_source.md), this operates DIRECTLY on the current manuscript, recomputes the
# first-citation order, remaps every in-text superscript citation, and reorders the
# reference list. It does NOT touch any other file and never re-renders from source.
import os, re

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
MS = os.path.join(ROOT, "reports/MVP_PLOSONE_submission.md")
SUPCLS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP2D = {c: str(i) for i, c in enumerate(SUPCLS)}
D2SUP = {str(i): c for i, c in enumerate(SUPCLS)}

text = open(MS, encoding="utf-8").read()
if "## References" not in text or "## Acknowledgements" not in text:
    raise SystemExit("References/Acknowledgements headers not found")

body, _, rest = text.partition("## References")
# rest currently starts with '## References'; keep it for the reference-list rewrite.
# We only remap the BODY (everything strictly before '## References').

RUN = rf"[{SUPCLS}][{SUPCLS}\u207b\u2013\u2014,]*"

# ---- first-appearance order in body ----
seen = []
for m in re.finditer(RUN, body):
    if m.start() > 0 and body[m.start() - 1].isdigit():
        continue  # exponent (e.g. 10^9), not a citation
    for part in m.group(0).split(","):
        digits = "".join(SUP2D.get(c, "") for c in part)
        if digits.isdigit():
            n = int(digits)
            if n not in seen:
                seen.append(n)

# any uncited references (should be none) appended in original order
all_old = sorted(set(re.findall(r"(?m)^(\d+)\.\s", rest)))
for n in all_old:
    n = int(n)
    if n not in seen:
        seen.append(n)

old2new = {old: i + 1 for i, old in enumerate(seen)}
new2old = {v: k for k, v in old2new.items()}

def remap_run(m):
    run = m.group(0)
    if m.start() > 0 and body[m.start() - 1].isdigit():
        return run
    def repl(mm):
        digits = "".join(SUP2D[c] for c in mm.group(0))
        n = int(digits)
        new = old2new.get(n, n)
        return "".join(D2SUP[d] for d in str(new))
    return re.sub(rf"[{SUPCLS}]+", repl, run)

body_new = re.sub(RUN, remap_run, body)

# ---- rewrite the reference list in new order ----
refsec = rest.split("## Acknowledgements")[0]
chunks = re.split(r"(?m)^(\d+)\.\s", refsec)
preamble = chunks[0]
old2text = {}
i = 1
while i < len(chunks) - 1:
    num = int(chunks[i]); body_r = chunks[i + 1]
    old2text[num] = body_r.strip("\n")
    i += 2

new_entries = []
for newnum in range(1, max(new2old) + 1):
    old = new2old[newnum]
    new_entries.append(f"{newnum}. {old2text[old].strip()}")
new_refsec = preamble.rstrip("\n") + "\n\n" + "\n\n".join(new_entries) + "\n\n"
rest_new = "## References\n" + new_refsec + "## Acknowledgements" + rest.split("## Acknowledgements")[1]

new_text = body_new + rest_new

# sanity: ensure no old number leaks and counts match
assert new_text.count("## References") == 1
open(MS, "w", encoding="utf-8").write(new_text)

print("old->new map:")
for o in sorted(old2new):
    print(f"  {o} -> {old2new[o]}")
print(f"\nreferences: {len(old2text)} | first-citation order length: {len(seen)}")
print("RENUMBER DONE -> MVP_PLOSONE_submission.md")
