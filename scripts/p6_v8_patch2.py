# -*- coding: utf-8 -*-
'''
P6 FJNSF 申请书 V8 收尾补丁：
  1) 消除 §10.3 杨代和行内的重复表述（列头已标“硕士（学历）”）；
  2) 清理 §10.3 加注中全角引号前的多余空格。
行级定点替换，断言“命中且仅命中 1 次”。
'''
import io
import sys

P = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V8.md'
lines = io.open(P, encoding='utf-8').read().split('\n')

JOBS = [
    # (定位谓词, [(旧片段, 新片段), ...], 标签)
    (lambda l: l.startswith('| 杨代和 |') and 'Cell Biochem Funct' in l,
     [('；**硕士研究生学历**（其主任医师职称与博士研究生导师资格按临床与科研业绩取得）；两段进修与访学经历——',
       '；学历为硕士研究生，主任医师职称与博士研究生导师资格均按临床与科研业绩取得；另有**两段进修与访学经历**——')],
     'members_yangdaihe_dedup'),

    (lambda l: l.startswith('> **关于署名单位的说明**'),
     [('其论文在不同时期分别以 “Department of Anesthesiology” 与 “Department of Pain” 署名',
       '其论文在不同时期分别以“Department of Anesthesiology”与“Department of Pain”署名')],
     'signature_note_spacing'),
]

for pred, pairs, tag in JOBS:
    idx = [i for i, l in enumerate(lines) if pred(l)]
    if len(idx) != 1:
        print('!! FAIL [%s] 命中 %d 次' % (tag, len(idx)))
        sys.exit(1)
    i = idx[0]
    s = lines[i]
    for a, b in pairs:
        n = s.count(a)
        if n != 1:
            print('!! FAIL [%s] 片段命中 %d 次: %r' % (tag, n, a[:60]))
            sys.exit(1)
        s = s.replace(a, b)
    lines[i] = s
    print('[OK] %s @ 行 %d' % (tag, i + 1))

io.open(P, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('补丁完成；体量 %d 行 / %d 字节' % (len(lines), len('\n'.join(lines).encode('utf-8'))))
