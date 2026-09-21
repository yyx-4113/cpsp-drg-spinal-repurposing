# -*- coding: utf-8 -*-
'''
P6 V12 补丁 2 —— 反向抽查发现的"随内容变化的元数据未随正文走"

来源：results/P6_FJNSF_APPLICATION_SUBMISSION_V12.md（V12 留档版，原地更新）
产物：原地更新 V12 留档版；随后须重跑 p6_v12_make_submission_copy.py 重新生成提交版
断言：每处替换"命中且仅命中 1 次"，否则整体退出

病灶说明（合并违例）：
  · 第 22 条红线——随内容变化的元数据（计数）必须随正文走
  · 第 27 条红线——引入/删除/重编号条目后，须把相关"检索词"回全文扫一遍
  实测：V11 新增参考文献 [27]，更新了头部元信息块与 §13.1 第 12 项，
        但 §3.6 表尾"引用完整性说明"仍写"26 条"与"[13]、[25] 为预印本"，
        "预印本条目标识符提示"与 §13.2 第 7 条亦未同步。
'''
import io
import re
import sys

P = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V12.md'
text = io.open(P, encoding='utf-8').read()

EDITS = [
    # 1) §3.6 表尾：文献计数 26 → 27
    ('26 条全部在正文中有对应引用位置',
     '27 条全部在正文中有对应引用位置',
     '§3.6 表尾·计数'),

    # 2) §3.6 表尾：预印本清单补 [27]
    ('[13]、[25] 为预印本，已显式标注。',
     '[13]、[25]、[27] 为预印本，已显式标注。',
     '§3.6 表尾·预印本清单'),

    # 3) 标识符提示：补 [27]（Research Square 预印本无 PMID）
    ('[25] 为 bioRxiv 2023-07-25 上线）。',
     '[25] 为 bioRxiv 2023-07-25 上线）；[27] 为 Research Square 预印本、本身不含 PMID，'
     '故亦仅保留 DOI 与“预印本”标识。',
     '§3.6 标识符提示'),

    # 4) §13.2 第 7 条：[27] 一并纳入
    ('| 7 | 参考文献 [13][25] 是否已有正式见刊版本 | 申请人 | 若有，替换为正式出处 |',
     '| 7 | 参考文献 [13][25][27] 是否已有正式见刊版本 | 申请人 | 若有，替换为正式出处；'
     '[27] 为申请人本人预印本，其与已接收论文的对应关系见第 10 条 |',
     '§13.2 第 7 条'),

    # 5) §13.1 第 61 项：指向新增第 66 项
    ('`results/P6_FJNSF_REFERENCES.md` 已同步 | 已完成 |',
     '`results/P6_FJNSF_REFERENCES.md` 已同步；**表尾“引用完整性说明”的同步见第 66 项** | 已完成 |',
     '§13.1 第 61 项·补指向'),

    # 6) §13.1 新增第 66 项：如实记录本轮反向抽查的发现
    ('| 65 | **第四轮 A4**：§3.5(9) 已增加**术语约定**——明确“同源”在本稿只有“数据出处重叠”'
     '与“方法学/课题方向属于同一问题域”两类含义，二者**不构成互相印证**；“模型同源”属技术表述 | 已完成 |',
     '| 65 | **第四轮 A4**：§3.5(9) 已增加**术语约定**——明确“同源”在本稿只有“数据出处重叠”'
     '与“方法学/课题方向属于同一问题域”两类含义，二者**不构成互相印证**；“模型同源”属技术表述 | 已完成 |\n'
     '| 66 | **反向抽查发现并修正（本轮）**：§3.6 表尾“引用完整性说明”的计数与预印本清单未随 [27] 同步'
     '——仍写“26 条”与“[13]、[25] 为预印本”，本次更正为“**27 条**”与“**[13]、[25]、[27] 为预印本**”；'
     '同类未同步的“预印本条目标识符提示”（补 [27] 无 PMID 的说明）与 §13.2 第 7 条一并补齐。'
     '**该处属第 22 条红线（随内容变化的元数据须随正文走）与第 27 条红线（引入条目后须回全文扫）的合并违例**：'
     'V11 引入了 [27]，却未把“26”与“预印本清单”当作需要回扫的检索词 | 已完成 |',
     '§13.1 新增第 66 项'),

    # 7) 文末署名行：补记本轮反向抽查
    ('并保留 V10/V11 各轮改动）。',
     '并保留 V10/V11 各轮改动；另据反向抽查修正 §3.6 表尾过期的文献计数与预印本清单，'
     '见 §13.1 第 66 项）。',
     '文末署名行'),
]

n_ok = 0
for old, new, tag in EDITS:
    c = text.count(old)
    if c != 1:
        print('!! FAIL [%s] 命中 %d 次（须为 1）' % (tag, c))
        sys.exit(1)
    text = text.replace(old, new, 1)
    n_ok += 1
    print('OK   [%s]' % tag)

print('--- V12 补丁2：%d 处，全部命中且仅命中 1 次 ---' % n_ok)


# ---------- 第 8 步：按实测重算 §13.2 第 16 条的字数（不动点迭代） ----------
def measure(t):
    body = t.split('## 十三、')[0]
    lines = body.split('\n')
    no_tbl = [l for l in lines if not l.strip().startswith('|')]
    han_all = len(re.findall(r'[\u4e00-\u9fff]', body))
    han_no_tbl = len(re.findall(r'[\u4e00-\u9fff]', '\n'.join(no_tbl)))
    full_han = len(re.findall(r'[\u4e00-\u9fff]', t))
    full_lines = t.count('\n') + 1
    full_kb = len(t.encode('utf-8')) / 1024.0
    return han_all, han_no_tbl, full_han, full_lines, full_kb


item16_pat = re.compile(r'\| 16 \| \*\*2027 年度指南对正文的篇幅/字数限制\*\*.*?\n')

for _ in range(6):
    han_all, han_no_tbl, full_han, full_lines, full_kb = measure(text)
    new16 = (
        '| 16 | **2027 年度指南对正文的篇幅/字数限制** | 科研科 / 省科技厅 | '
        '本稿实测（V12 定稿，2026-09-19，含本轮补丁）：正文（不含 §13、不含表格）约 **%.2f 万汉字**；'
        '正文（不含 §13、含表格）约 **%.2f 万汉字**；全文约 **%.2f 万汉字 / %.0f KB / %d 行**。'
        'V9 稿此处曾记为“1.47 万 / 2.03 万 / 89 KB”，属上版遗留的过期口径；'
        '**本节字数以本行为唯一来源，任何增删后须重跑统计并更新本行**。'
        '若指南设字数上限，须按上限裁剪，并按第 17、21 条生成与复核提交版 |\n'
        % (han_no_tbl / 10000.0, han_all / 10000.0, full_han / 10000.0, full_kb, full_lines)
    )
    m = item16_pat.search(text)
    if not m:
        print('!! FAIL 未匹配到 §13.2 第 16 条')
        sys.exit(1)
    if m.group(0) == new16:
        break
    text = text[:m.start()] + new16 + text[m.end():]

han_all, han_no_tbl, full_han, full_lines, full_kb = measure(text)
print('§13.2 第 16 条已按实测重算：正文不含表格 %.2f 万 / 含表格 %.2f 万 / 全文 %.2f 万汉字 / %.0f KB / %d 行'
      % (han_no_tbl / 10000.0, han_all / 10000.0, full_han / 10000.0, full_kb, full_lines))

# ---------- 定稿校验 ----------
# 注意：§13.1 第 66 项为"如实记录"，其中引用了旧措辞（26 条 / [13][25]），
#       故此处不能做全库否定断言，改为断言 §3.6 表尾那一行本身已正确。
assert '27 条全部在正文中有对应引用位置' in text, '§3.6 表尾计数未同步'
assert '27 条全部在正文中有对应引用位置，' in text, '§3.6 表尾计数未同步'
assert '[13]、[25]、[27] 为预印本，已显式标注。' in text, '§3.6 表尾预印本清单未同步'
tail = [l for l in text.split('\n') if l.startswith('> 引用完整性说明')]
assert len(tail) == 1, '§3.6 表尾说明行数异常：%d' % len(tail)
assert '26 条' not in tail[0] and '[13]、[25] 为预印本' not in tail[0], '§3.6 表尾仍含旧口径'
han = len(re.findall(r'[\u4e00-\u9fff]', text))
assert text.count('\u201c') == text.count('\u201d'), '全角引号不配对：%d / %d' % (
    text.count('\u201c'), text.count('\u201d'))
assert text.count('"') == 0, '仍存在 ASCII 双引号'
print('定稿校验：§3.6 表尾已同步 / ASCII 双引号 0 / 全角引号 %d:%d 配对 / 汉字 %d / 行 %d'
      % (text.count('\u201c'), text.count('\u201d'), han, text.count('\n') + 1))

io.open(P, 'w', encoding='utf-8').write(text)
print('已写入 %s' % P)
