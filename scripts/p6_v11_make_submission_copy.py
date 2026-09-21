# -*- coding: utf-8 -*-
'''
从 V11 留档版生成"提交版"（沿用 V10 的结构性去除规则，可复跑）。
规则：① 保留标题，删除标题与首个 '---' 之间的全部 '>' 元信息块；
      ② 删除 §13 整节；③ 删除文末作者脚注。
待 2027 年度指南字数上限确认后，再按上限做压缩式裁剪。
'''
import io

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V11.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V11_提交版.md'

lines = io.open(SRC, encoding='utf-8').read().split('\n')

sep = lines.index('---')
lines = [lines[0].replace(' · 修订版 V11', ''), ''] + lines[sep:]

i13 = [i for i, l in enumerate(lines) if l.startswith('## 十三')]
assert len(i13) == 1
lines = lines[:i13[0]]
while lines and lines[-1].strip() in ('', '---'):
    lines.pop()

io.open(DST, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

print('提交版已生成：%s' % DST)
print('行数：%d' % len(lines))
