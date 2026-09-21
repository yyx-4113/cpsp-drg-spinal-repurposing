# -*- coding: utf-8 -*-
'''
P6 FJNSF 申请书 V9 -> V10 补丁（收口）
1) 头部块中的 ASCII 直引号改为全角引号（全文引号规范：ASCII 双引号须为 0）；
2) 头部块不再携带具体字数（避免"每次增删后立即过期"的复发），字数统一由 §13.2 第 16 条单一来源给出；
3) §13.2 第 16 条按 V10 实测值填写；
4) §13.1 第 58 条改写为"复核规则"，不再写具体数字，从机制上防止同类过期复发；
5) §13.1 第 53 条细化"八处"的构成。
'''
import io
import sys

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V10.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V10.md'

lines = io.open(SRC, encoding='utf-8').read().split('\n')
LOG = []


def find_one(pred, tag):
    idx = [i for i, l in enumerate(lines) if pred(l)]
    if len(idx) != 1:
        print('!! FAIL [%s] 命中 %d 次' % (tag, len(idx)))
        sys.exit(1)
    return idx[0]


def replace_line(pred, new, tag):
    i = find_one(pred, tag)
    old = lines[i]
    lines[i] = new
    LOG.append((tag, i + 1, old[:80], new[:80]))


def swap_in_line(pred, pairs, tag):
    i = find_one(pred, tag)
    s = lines[i]
    for a, b in pairs:
        if s.count(a) != 1:
            print('!! FAIL [%s] 片段命中 %d 次: %r' % (tag, s.count(a), a[:60]))
            sys.exit(1)
        s = s.replace(a, b)
    old = lines[i]
    lines[i] = s
    LOG.append((tag, i + 1, old[:80], s[:80]))


# 1. 引号规范
swap_in_line(lambda l: l.startswith('> §3.4、§3.5(11)(13)'),
             [('将"分选纯度"单列为', '将“分选纯度”单列为')], 'quote-h1')

# 2. 头部块去掉具体字数（单一来源原则）
replace_line(lambda l: l.startswith('> 篇幅/字数口径（1.47 万'),
             '> 篇幅/字数口径（原为早期版本的近似值，现改按实测重算，单一来源见 §13.2 第 16 条），'
             '并给 §11.1 的抗体清单补注“抗体用于组织化学与免疫荧光、',
             'header-nonum')
replace_line(lambda l: l.startswith('> "用于组织化学、不作活细胞分选标记"。逐条落点见'),
             '> 不作活细胞分选标记”。逐条落点见 `P6_V10_修订说明与遗留事项_2026-09-19.md`。',
             'header-nonum2')

# 3. §13.2 第 16 条按实测填写
replace_line(
    lambda l: l.startswith('| 16 | **2027 年度指南对正文的篇幅/字数限制**'),
    '| 16 | **2027 年度指南对正文的篇幅/字数限制** | 科研科 / 省科技厅 | 本稿实测（V10，2026-09-19）：'
    '正文（不含 §13、不含表格）约 **1.74 万汉字**；正文（不含 §13、含表格）约 **2.18 万汉字**；'
    '全文约 **2.52 万汉字 / 108 KB / 638 行**。V9 稿此处曾记为“1.47 万 / 2.03 万 / 89 KB”，属上版遗留的过期口径；'
    '**本节字数以本行为唯一来源，任何增删后须重跑统计并更新本行**。若指南设字数上限，须按上限裁剪，'
    '并按第 17 条拆分提交版 |',
    'pending16-v10')

# 4. §13.1 第 58 条改为复核规则
replace_line(
    lambda l: l.startswith('| 58 | §13.2 第 16 条的篇幅口径已按实测更正'),
    '| 58 | 篇幅口径的**复核规则**已建立：§13.2 第 16 条原有字数（1.47 万 / 2.03 万 / 89 KB）为早期版本遗留、'
    '已按实测更正为 V10 值，并在该行注明“本节字数以本行为唯一来源、任何增删后须重跑统计”。'
    '**本行不再重复列举数字，从机制上避免同类过期复发**；§11.1 抗体清单已补注“用于组织化学、'
    '不作活细胞分选标记”（与 §4.2 内容一(5) 的分选标记边界一致） | 已完成 |',
    'checklist58-fix')

# 5. §13.1 第 53 条细化
replace_line(
    lambda l: l.startswith('| 53 | 负责人**已被接收的国际期刊论文**已补入'),
    '| 53 | 负责人**已被接收的国际期刊论文**已补入 §10.2 代表性论著①（重排为论著列表第 1 条），'
    '并同步更新八处：头部定位、§3.4 创新点 3、§3.5(11)、§3.5(13)、§6.2、§9(1)、§10.2'
    '（内 3 处：研究方向栏、代表性论著栏、与本项目的关系）、§10.3 | 已完成 |',
    'checklist53-fix')

io.open(DST, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

print('=' * 78)
print('V10 补丁：%d 处，全部命中且仅命中 1 次' % len(LOG))
print('=' * 78)
for tag, ln, old, new in LOG:
    print('\n--- [%s] @ 行 %d ---' % (tag, ln))
    print('  - 旧: %s' % old)
    print('  + 新: %s' % new)
print('\n输出：%s' % DST)
