# -*- coding: utf-8 -*-
'''
从 V12 留档版生成"提交版"（第四轮 A1 / B1 / B2 的处置，可复跑）。
规则：
  ① 保留标题，删除标题与首个 '---' 之间的全部 '>' 元信息块；
  ② **清扫指向被删章节的引用**（第四轮 A1：上版曾残留 2 处"见 §13"），并在生成后断言 §13 字样零残留；
  ③ 删除 §13 整节；
  ④ 删除文末作者脚注；
  ⑤ 在标题下插入一行最小"编者说明"（第四轮 B1/B2：交代图件文件名与交叉引用体例，不使用任何内部语言）。
待 2027 年度指南字数上限确认后，再按上限做压缩式裁剪。
'''
import io
import sys

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V12.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V12_提交版.md'

lines = io.open(SRC, encoding='utf-8').read().split('\n')

# ① 首个 '---' 之前只留标题
sep = lines.index('---')
title = lines[0].replace(' · 修订版 V12', '')
lines = [title] + lines[sep:]
text = '\n'.join(lines)

# ② 清扫指向被删章节（§13）的引用 —— 每处断言命中且仅命中 1 次
SWEEP = [
    ('，见 §13 待确认事项）', '）'),
    ('两种口径不得混用**（见 §13）', '两种口径不得混用**'),
]
for a, b in SWEEP:
    if text.count(a) != 1:
        print('!! FAIL 清扫片段命中 %d 次: %r' % (text.count(a), a))
        sys.exit(1)
    text = text.replace(a, b)

# ③ 去 §13 整节
lines = text.split('\n')
i13 = [i for i, l in enumerate(lines) if l.startswith('## 十三')]
assert len(i13) == 1
lines = lines[:i13[0]]
while lines and lines[-1].strip() in ('', '---'):
    lines.pop()

# ④ 去文末作者脚注（若仍在文末）
while lines and lines[-1].startswith('*本申请书由申请人杨永新撰写'):
    lines.pop()
while lines and lines[-1].strip() in ('', '---'):
    lines.pop()

# ⑤ 标题下插入最小"编者说明"
NOTE = [
    '> **编者说明**：① 交叉引用体例——`§1` = 第一节、`§8` = 第八节（标题使用中文序数），'
    '`§3.5(9)` 指 §3.5 内第 (9) 段。② 图件文件名对应——图 0 = `figures/P6_Fig0_technical_route.png`；'
    '图 1 = `figures/P6_Fig1_ADRA2A_forest.png`；图 2 = `figures/P6_Fig2_hub_LODO_AUC.png`；'
    '图 3 = `figures/P6_Fig3_human_translatability.png`（排版时按编号插入，并相应调整正文图号引用）。'
    '③ 文中的 `＿＿` 为须线下填写的表单字段（指南代码、接收函日期、签字盖章）。',
    '',
]
lines = [lines[0], ''] + NOTE + lines[1:]

out = '\n'.join(lines) + '\n'
io.open(DST, 'w', encoding='utf-8', newline='\n').write(out)

assert '§13' not in out, '提交版仍残留 §13 引用'
assert '十三、' not in out, '提交版仍残留 §13 节标题'
print('提交版已生成：%s' % DST)
print('行数：%d；§13 残留：0；含编者说明：%s' % (len(lines), '编者说明' in out))
