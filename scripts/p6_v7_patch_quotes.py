# -*- coding: utf-8 -*-
'''V7 收尾补丁：统一全文中文引号。

背景：文档历经 V4–V7 多轮生成，中文引语混用了 ASCII 双引号与全角引号。
提交前应统一为中文规范全角引号（U+201C / U+201D）。

安全性：仅处理满足以下全部条件的行
  ① 含 ASCII 双引号（U+0022）；
  ② ASCII 双引号个数为偶数（可完整配对）；
  ③ 该行不含任何已有全角引号（避免跨风格配对错位）。
配对的片段内若为纯英文而无汉字则跳过并报告（本文件实测为 0 条）。
'''
import io
import os
import re
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
P = os.path.join(BASE, 'results', 'P6_FJNSF_APPLICATION_SUBMISSION_V7.md')

DQ = '\u0022'
LQ = '\u201c'
RQ = '\u201d'

lines = io.open(P, encoding='utf-8').read().split('\n')
done, skip_odd, skip_mixed, skip_en = 0, [], [], []

for i, l in enumerate(lines):
    if DQ not in l:
        continue
    if LQ in l or RQ in l:
        skip_mixed.append(i + 1)
        continue
    pos = [m.start() for m in re.finditer(re.escape(DQ), l)]
    if len(pos) % 2:
        skip_odd.append(i + 1)
        continue
    pairs = list(zip(pos[0::2], pos[1::2]))
    bad = [l[a + 1:b] for a, b in pairs
           if re.search(r'[A-Za-z]{4,}', l[a + 1:b]) and not re.search(r'[\u4e00-\u9fff]', l[a + 1:b])]
    if bad:
        skip_en.append((i + 1, bad))
        continue
    new = []
    prev = 0
    for a, b in pairs:
        new.append(l[prev:a])
        new.append(LQ)
        new.append(l[a + 1:b])
        new.append(RQ)
        prev = b + 1
    new.append(l[prev:])
    lines[i] = ''.join(new)
    done += 1

out = '\n'.join(lines)
io.open(P, 'w', encoding='utf-8', newline='\n').write(out)

print('统一引号：处理 %d 行' % done)
print('跳过（奇数个引号）: %s' % (skip_odd or '无'))
print('跳过（与全角混用的行）: %s' % (skip_mixed or '无'))
print('跳过（英文引语）: %s' % (skip_en or '无'))
res = io.open(P, encoding='utf-8').read()
print('剩余 ASCII 双引号: %d 个；全角引号: %d / %d 个'
      % (res.count(DQ), res.count(LQ), res.count(RQ)))
if res.count(LQ) != res.count(RQ):
    print('!! 警告：全角左右引号数量不等，请人工复核')
    sys.exit(2)
print('OK')
