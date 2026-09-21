#!/usr/bin/env python3
# p8_reference_renumber.py
# Fix the pre-existing reference-ordering defect surfaced by p7_consistency_gate.py:
#   in-text first-appearance order was [1-9,30,31,27,28,29,10-26], which violates
#   Nature Portfolio's "number references by first citation" rule.
# Derives old->new numbering from the CURRENT first-appearance order (asserting it
# matches the gate's sequence exactly), remaps EVERY superscript CITATION in the
# manuscript + 3 aux files with one consistent map, and reorders the list block.
# MATH-EXPONENT SAFEGUARD: a superscript run is treated as a citation UNLESS the
# character immediately before it is a superscript minus (⁻, U+207B), an en dash
# (–, U+2013), or an ASCII digit — those mark the tail of a math exponent such as
# Phi^-1 (Φ⁻¹) or a p-value (10⁻²⁰), which must NOT be renumbered.
import re, os

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
MS  = os.path.join(ROOT, "reports/MVP_ScientificReports_submission.md")
SUP = os.path.join(ROOT, "reports/MVP_ScientificReports_supplementary.md")
CL  = os.path.join(ROOT, "reports/MVP_ScientificReports_cover_letter.md")
RS  = os.path.join(ROOT, "reports/MVP_ScientificReports_reporting_summary.md")

M   = {d: c for d, c in zip('0123456789',
        ['\u2070','\u00b9','\u00b2','\u00b3','\u2074','\u2075','\u2076','\u2077','\u2078','\u2079'])}
REV = {c: d for d, c in M.items()}
SUPCHARS = ''.join(M.values())
rx = re.compile('[' + SUPCHARS + '][' + SUPCHARS + '\u207b\u2013]*')

def parse_one(s):
    return int(''.join(REV[c] for c in s))

def nums_in(run):           # expands RANGES fully -> for first-appearance tracking
    out = []
    for seg in run.split(','):
        if '\u207b' in seg or '\u2013' in seg:
            sep = '\u207b' if '\u207b' in seg else '\u2013'
            a, b = seg.split(sep)
            lo, hi = parse_one(a), parse_one(b)
            out += list(range(min(lo, hi), max(lo, hi) + 1))
        else:
            out.append(parse_one(seg))
    return out

def sup_of(n):
    return ''.join(M[d] for d in str(n))

def is_citation_run(m, text):
    s = m.start()
    if s == 0:
        return True
    prev = text[s-1]
    if prev in ('\u207b', '\u2013'):          # tail of a superscript-minus exponent
        return False
    if prev.isdigit():                        # tail of a 10^x style exponent
        return False
    return True

def remap_run(run, new_of):
    try:
        outp = []
        for p in run.split(','):
            if '\u207b' in p or '\u2013' in p:
                sep = '\u207b' if '\u207b' in p else '\u2013'
                a, b = p.split(sep)
                lo, hi = min(parse_one(a), parse_one(b)), max(parse_one(a), parse_one(b))
                members = list(range(lo, hi + 1))
                if not all(m in new_of for m in members):
                    return run
                nm = [new_of[m] for m in members]
                if nm == list(range(nm[0], nm[-1] + 1)):   # consecutive -> keep as range
                    outp.append(sup_of(nm[0]) + sep + sup_of(nm[-1]))
                else:                                      # non-consecutive -> individual
                    outp.append(','.join(sup_of(m) for m in nm))
            else:
                n = parse_one(p)
                if n not in new_of:
                    return run
                outp.append(sup_of(new_of[n]))
        return ','.join(outp)
    except (KeyError, ValueError):
        return run

def remap_text(text, new_of):
    return rx.sub(lambda m: remap_run(m.group(0), new_of) if is_citation_run(m, text) else m.group(0), text)

EXPECTED = [1,2,3,4,5,6,7,8,9,30,31,27,28,29,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26]

# ---- derive old->new map from CURRENT first-appearance (pre-References body) ----
ms = open(MS, encoding='utf-8').read()
body = ms.split('## References')[0]
firstseen = []
for m in rx.finditer(body):
    for n in nums_in(m.group(0)):
        if n not in firstseen:
            firstseen.append(n)
assert firstseen == EXPECTED, f"first-appearance mismatch:\n got={firstseen}"
new_of = {old: i for i, old in enumerate(firstseen, 1)}
old_of = {i: old for i, old in enumerate(firstseen, 1)}
print("first-appearance matches gate sequence:", firstseen)
print("sample map old->new:", {k: new_of[k] for k in (10,11,20,27,28,29,30,31)})

# ---- remap ENTIRE manuscript (all citations, before + after References) ----
ms_new = remap_text(ms, new_of)

# ---- guard: reference list block must contain NO superscript citations ----
ref_start = ms_new.index('## References')
ack_start = ms_new.index('## Acknowledgements')
ref_block = ms_new[ref_start:ack_start]
head_end  = ref_block.index('\n') + 1
header    = ref_block[:head_end]
list_block = ref_block[head_end:]
stray = rx.findall(list_block)
assert not stray, f"reference list block unexpectedly contains superscript runs: {stray}"

# ---- parse + reorder list entries ----
entry_starts = [m.start() for m in re.finditer(r'(?m)^(\d+)\. ', list_block)]
entries = {}
for idx, s in enumerate(entry_starts):
    e = list_block[s: entry_starts[idx+1] if idx+1 < len(entry_starts) else len(list_block)]
    oldnum = int(re.match(r'^(\d+)\. ', e).group(1))
    entries[oldnum] = e
assert len(entries) == 31, f"parsed {len(entries)} entries, expected 31"
new_list = ''
for i in range(1, 32):
    old = old_of[i]
    e = re.sub(r'^\d+\. ', f'{i}. ', entries[old], count=1)
    new_list += e
ms_new = ms_new[:ref_start] + header + new_list + ms_new[ack_start:]
open(MS, 'w', encoding='utf-8').write(ms_new)

# ---- remap aux files (they inherit the manuscript bibliography) ----
for f in (SUP, CL, RS):
    t = open(f, encoding='utf-8').read()
    open(f, 'w', encoding='utf-8').write(remap_text(t, new_of))

print("DONE: remapped manuscript + supplementary + cover_letter + reporting_summary (exponents preserved).")
