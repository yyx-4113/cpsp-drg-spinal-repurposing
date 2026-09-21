# -*- coding: utf-8 -*-
'''
从 V10 留档版生成"提交版"（第三轮专家组第 2、3 项待办：拆分留档版 / 提交版）。
规则（机械化、可复跑）：
  1) 保留标题，删除标题与首个 '---' 之间的全部 '>' 元信息块（版本沿革、写作纪律、图件与参考文献说明、历轮修订要点）；
  2) 删除 §13「提交前自查与待确认事项」整节（内部自查与待办清单，不得随稿提交）；
  3) 删除文末作者脚注行。
说明：字数上限尚待 2027 年度指南确认，故提交版暂只做"结构性去除"，
      不做压缩式改写；待指南字数明确后再按上限裁剪。
'''
import io

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V10.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V10_提交版.md'

lines = io.open(SRC, encoding='utf-8').read().split('\n')

# 1) 首个 '---' 之前只留标题
sep = lines.index('---')
head = [lines[0].replace(' · 修订版 V10', ''), '']
lines = head + lines[sep:]

# 2) 去 §13 整节
i13 = [i for i, l in enumerate(lines) if l.startswith('## 十三')]
assert len(i13) == 1
i13 = i13[0]
# 保留 §13 之前的内容，去掉 §13 与紧随其后的分隔线与脚注
lines = lines[:i13]
while lines and lines[-1].strip() in ('', '---'):
    lines.pop()

io.open(DST, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')

print('提交版已生成：%s' % DST)
print('留档版：%d 行 → 提交版：%d 行' % (len(io.open(SRC, encoding='utf-8').read().split('\n')), len(lines)))
