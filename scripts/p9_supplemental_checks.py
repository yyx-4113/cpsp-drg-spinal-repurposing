#!/usr/env python3
# -*- coding: utf-8 -*-
"""
p9_supplemental_checks.py -- Scientific Reports 投稿补充校验（独立于 p7_consistency_gate.py）

覆盖 p7 已查的硬上限，并补 p7 未覆盖的维度：
  [A] 标题 <= 20 词
  [B] 摘要 <= 200 词（且**不得含参考文献**——SR 硬性要求）
  [C] 展示条目（图+表）<= 8
  [D] 每幅图图例 <= 350 词（p7 已查，独立复算）
  [E] 每个表说明文字规模（SR 表为“每表≤1页”，非词数硬限；仅报信息量）
  [F] 展示条目引用覆盖：每个 Fig/Table 必须在正文被引用（无孤儿展示项）
  [G] 补充表 S1–S7 在 supplementary.md 中存在且标注为 Supplementary（不计入 8 上限）
  [H] 正文词数（vs 4,500 指南，非强制）

Scientific Reports 官方硬上限（已联网核实 2026-09-21）：
  title <= 20 words; abstract <= 200 words (unstructured, no refs);
  display items <= 8 (figures+tables); figure legends <= 350 words each.
"""
import re, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MS   = os.path.join(ROOT, "reports/MVP_ScientificReports_submission.md")
SUP  = os.path.join(ROOT, "reports/MVP_ScientificReports_supplementary.md")

SUP_DIGITS = ''.join(chr(c) for c in range(0x2070,0x2080))  # ⁰¹²...⁹
def has_sup_ref(s):
    return bool(re.search('['+SUP_DIGITS+']', s))

def words(s):
    # Publisher-accurate: split on whitespace only (slashes are NOT word breaks,
    # so *SCN9A*/*SCN10A*/*SCN11A*/*SCN8A* counts as 1 word, matching MS-Word/SR counter).
    return len(s.split())

def section(text, name):
    out=[]; cap=False
    for ln in text.split('\n'):
        if ln.startswith('## '):
            cap = ln.strip().startswith('## '+name)   # prefix match (header may carry a suffix)
            continue
        if cap: out.append(ln)
    return '\n'.join(out)

t  = open(MS, encoding='utf-8').read()
lines = t.split('\n')
sup_t = open(SUP, encoding='utf-8').read()

fails=[]; warns=[]; oks=[]
print("="*78); print("[A] TITLE (<=20 words)"); print("="*78)
title = lines[0].lstrip('# ').strip()
tw = len(title.split())
print(f"  title words: {tw} -> {'OK' if tw<=20 else 'FAIL(>20)'}")
(oks if tw<=20 else fails).append(f"title {tw}w")

print("\n"+"="*78); print("[B] ABSTRACT (<=200 words; NO references)"); print("="*78)
ab = section(t, "Abstract")
aw = words(ab)
print(f"  abstract words: {aw} -> {'OK' if aw<=200 else 'FAIL(>200)'}")
(oks if aw<=200 else fails).append(f"abstract {aw}w")
if has_sup_ref(ab):
    print("  FAIL  abstract contains a superscript reference (SR: abstract must have NO references)")
    fails.append("abstract contains reference")
else:
    print("  OK    abstract contains no superscript reference")
    oks.append("abstract no-ref")

print("\n"+"="*78); print("[C] DISPLAY ITEMS (<=8: figures+tables)"); print("="*78)
disp = section(t, "Display items")
fig_nums = [int(x) for x in re.findall(r'\*\*Fig\. (\d+)\*\*', disp)]
tab_nums = [int(x) for x in re.findall(r'\*\*Table (\d+)\*\*', disp)]
nfig, ntab = len(fig_nums), len(tab_nums)
print(f"  figures={nfig} tables={ntab} total={nfig+ntab} -> {'OK' if nfig+ntab<=8 else 'FAIL(>8)'}")
(oks if nfig+ntab<=8 else fails).append(f"display {nfig+ntab}")

print("\n"+"="*78); print("[D] FIGURE LEGENDS (<=350 words each)"); print("="*78)
for num in fig_nums:
    m = re.search(r'\*\*Fig\. '+str(num)+r'\*\*.*?\*Legend\.\*(.*?)(?=\n- |\Z)', disp, re.S)
    leg = m.group(1) if m else ''
    w = words(leg)
    print(f"  Fig.{num} legend: {w} words -> {'OK' if w<=350 else 'FAIL(>350)'}")
    (oks if w<=350 else fails).append(f"Fig.{num} legend {w}w")

print("\n"+"="*78); print("[E] TABLE DESCRIPTIVE TEXT (SR: <=1 page each; informational)"); print("="*78)
for num in tab_nums:
    m = re.search(r'\*\*Table '+str(num)+r'\*\*.*?(?=\n- \*\*Table|\n\n\*\*Supplementary|\Z)', disp, re.S)
    blk = m.group(0) if m else ''
    # descriptive text = lines not starting with '|' (exclude the actual table rows)
    desc = '\n'.join(l for l in blk.split('\n') if not l.strip().startswith('|'))
    w = words(desc)
    print(f"  Table {num} descriptive text: {w} words (informational; SR hard cap is 1 page/table)")

print("\n"+"="*78); print("[F] DISPLAY-ITEM CITATION COVERAGE (no orphan items)"); print("="*78)
body = t.split('## Display items')[0]  # everything before the display-items list
for num in fig_nums:
    cited = ('Fig. %d'%num) in body
    print(f"  Fig.{num} cited in body: {'YES' if cited else 'NO (orphan!)'}")
    (oks if cited else fails).append(f"Fig.{num} cited")
for num in tab_nums:
    cited = ('Table %d'%num) in body
    print(f"  Table {num} cited in body: {'YES' if cited else 'NO (orphan!)'}")
    (oks if cited else fails).append(f"Table {num} cited")

print("\n"+"="*78); print("[G] SUPPLEMENTARY TABLES S1-S7 (present, labelled, excluded from cap)"); print("="*78)
for s in range(1,8):
    present = bool(re.search(r'## Supplementary Table S%d\b'%s, sup_t))
    print(f"  S{s}: {'PRESENT' if present else 'MISSING'}")
    (oks if present else fails).append(f"S{s} present")
# S5b special (set-level BH) — should also exist
s5b = bool(re.search(r'Supplementary Table S5b', sup_t))
print(f"  S5b (set-level BH): {'PRESENT' if s5b else 'MISSING'}")
(oks if s5b else fails).append("S5b present")

print("\n"+"="*78); print("[H] MAIN-TEXT WORDS (SR guideline <=4,500; excludes Abstract/Methods/Refs/legends; not enforced)"); print("="*78)
# SR "main text" = Introduction+Results+Discussion (excl. Abstract, Methods, References, figure legends)
mt = t.split('## Introduction',1)[1].split('## Methods',1)[0] if ('## Introduction' in t and '## Methods' in t) else ''
mw = words(mt)
print(f"  main text (Intro+Results+Discussion, excl. abstract/methods/refs/legends): {mw} words -> {'within 4,500 guide' if mw<=4500 else 'OVER 4,500 guide (not a hard fail)'}")
(oks if mw<=4500 else warns).append(f"maintext {mw}w")

print("\n"+"="*78)
print(f"RESULT: {len(fails)} FAIL, {len(warns)} WARN, {len(oks)} OK")
if fails:
    print("FAILURES:")
    for f in fails: print("  -", f)
print("="*78)
