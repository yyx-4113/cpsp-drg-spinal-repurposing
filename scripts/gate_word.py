#!/usr/bin/env python
"""Word gate for MVP_ScientificReports v1.1 (Scientific Reports limits)."""
import re, os, struct

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
MS = open(os.path.join(ROOT, "reports", "MVP_ScientificReports_submission.md"), encoding="utf-8").read()

def wcount(s):
    """Journal-style word count (MS Word convention): whitespace-delimited
    tokens containing at least one alphanumeric character. The previous
    regex tokenizer split on punctuation inside numbers, inflating counts
    (e.g. '7,751/14,390' counted as 4 words instead of 1)."""
    return len([t for t in s.split() if re.search(r"[A-Za-z0-9]", t)])

title = re.search(r'^# (.+)$', MS, re.M).group(1)
abs_m = re.search(r"## Abstract\s*\n(.*?)\n---", MS, re.S)
abs_text = abs_m.group(1).strip()
nref = len(re.findall(r'^\d+\.', MS, re.M))
nfig = MS.count("**Fig.")
ntab = MS.count("**Table ")
display = nfig + ntab
total_words = wcount(MS)

# Scientific Reports also limits the abstract to no references; check none in abstract.
# NOTE: statistical exponents such as I^2 (heterogeneity) or R^2 use the same superscript glyphs
# as citation markers, so letter-adjacent superscripts are stripped before the reference scan.
abs_noexp = re.sub(r'[A-Za-z][\u00B2\u00B3\u2070-\u2079]', '', abs_text)
abs_has_ref = bool(re.search(r'[\u00B9\u00B2-\u00B3\u2070-\u2079]', abs_noexp)) or 'et al' in abs_text.lower() or bool(re.search(r'\(\w[\w ,]*\d{4}\)', abs_text))

# DPI check (pHYs chunk)
def png_dpi(path):
    with open(path, 'rb') as f:
        data = f.read()
    i = 8
    while i + 8 <= len(data):
        ln = struct.unpack('>I', data[i:i+4])[0]
        typ = data[i+4:i+8]
        if typ == b'pHYs':
            x, y, unit = struct.unpack('>IIB', data[i+8:i+17])
            return (x / 39.3701) if unit == 1 else None
        i += 12 + ln
    return None

print("=== WORD GATE (Scientific Reports) ===")
checks = []
def chk(name, ok, val=""):
    checks.append(ok); print(f"[{'PASS' if ok else 'FAIL'}] {name}" + (f"  {val}" if val else ""))

chk("Title <= 20 words (Round-3-confirmed SR norm)", wcount(title) <= 20, f"{wcount(title)} words")
chk("Abstract <= 200 words", wcount(abs_text) <= 200, f"{wcount(abs_text)} words")
chk("Abstract has no refs", not abs_has_ref, "ref-like tokens" if abs_has_ref else "clean")
chk("References <= 60", nref <= 60, f"{nref} refs")
chk("Display items <= 8", display <= 8, f"{display} ({nfig} fig + {ntab} tab)")
chk("Figures == 5", nfig == 5, f"{nfig}")
chk("Tables == 3", ntab == 3, f"{ntab}")
print(f"[INFO] Total manuscript words (incl. refs/display): {total_words}")

print("\n=== FIGURE DPI (Science Reports requires >=300) ===")
figdir = os.path.join(ROOT, "figures")
dpi_ok = True
for fn in sorted(os.listdir(figdir)):
    if fn.endswith('.png'):
        d = png_dpi(os.path.join(figdir, fn))
        ok = (d is not None and d >= 300)
        dpi_ok = dpi_ok and ok
        print(f"[{'PASS' if ok else 'WARN'}] {fn}: {d:.3f} DPI" if d is not None else f"[WARN] {fn}: DPI metadata absent")
chk("All figures >= 300 DPI", dpi_ok, "")

print("\n=== SUMMARY ===")
print(f"WORD GATE: {'ALL PASS' if all(checks) and dpi_ok else 'SEE WARNINGS'}")
