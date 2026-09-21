# -*- coding: utf-8 -*-
'''
从 V14 留档版生成"提交版"（同 V12 的分版规则，可复跑）。
规则：
  ① 保留标题，删除标题与首个 '---' 之间的全部 '>' 元信息块；
  ② **清扫指向被删章节的引用**（第四轮 A1：上版曾残留 2 处"见 §13"），并在生成后断言 §13 字样零残留；
  ③ 删除 §13 整节；
  ④ 删除文末作者脚注；
  ⑤ 在标题下插入一行最小"编者说明"（第四轮 B1/B2：交代图件文件名与交叉引用体例，不使用任何内部语言）。
待 2027 年度指南字数上限确认后，再按上限做压缩式裁剪。
'''
import io
import re
import sys

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V14.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V14_提交版.md'

lines = io.open(SRC, encoding='utf-8').read().split('\n')

# ① 首个 '---' 之前只留标题
sep = lines.index('---')
title = lines[0].replace(' · 修订版 V14', '')
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

# ---------- 生成后断言（带定位，便于排查） ----------
for bad in ('§13', '十三、', '待确认事项'):
    hits = [i + 1 for i, l in enumerate(lines) if bad in l]
    if hits:
        print('!! FAIL 提交版残留 %r，行号：%s' % (bad, hits))
        for i in hits[:5]:
            print('   L%d: %s' % (i, lines[i - 1][:160]))
        sys.exit(1)
assert out.count('"') == 0, '提交版仍存在 ASCII 双引号'
assert out.count('\u201c') == out.count('\u201d'), '提交版全角引号不配对'
refs = [int(x) for x in re.findall(r'^\*\*\[(\d+)\]\*\*', out, re.M)]
assert refs == list(range(1, len(refs) + 1)), '提交版参考文献编号不连续'
# 本轮新增内容必须在提交版里生效（§10.2 ① 属于 §10，不会被删）
assert '未被 JCR 收录、无 JCR 影响因子、亦未进入中科院 SCI 期刊分区表' in out, '期刊层级改写未进入提交版'
assert '非北京大学《中文核心期刊要目总览》来源期刊、非中国科技核心期刊（统计源）' in out, '中文期刊层级披露未进入提交版'

print('提交版已生成：%s' % DST)
print('行数：%d；§13 残留：0；含编者说明：%s；参考文献 %d 条连续'
      % (len(lines), '编者说明' in out, len(refs)))
