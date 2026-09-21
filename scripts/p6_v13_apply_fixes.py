# -*- coding: utf-8 -*-
'''
P6 V13 —— 期刊层级复核（申请人提问触发：*Neurobiology of Sleep and Circadian Rhythms* 是否 SCI？）

来源：results/P6_FJNSF_APPLICATION_SUBMISSION_V12.md
产物：results/P6_FJNSF_APPLICATION_SUBMISSION_V13.md（新建，V12 留档对照）
断言：每处替换"命中且仅命中 1 次"，否则整体退出

核验结论（2026-09-20，五源交叉）：
  该刊**不是 SCI / SCIE 期刊**：
    · Elsevier 官方 ScienceDirect 期刊页"期刊对比表"——Impact Factor 栏为 "-"（空），CiteScore 4.2
    · LetPub（繁体版）——"According to the latest JCR data, this journal is not indexed in the JCR"；
      WOS Quartile: Q0 N/A；"五年IF 0"、"实时影响因子 -"、"h-index 暂无"
    · 刊鹿选刊——影响因子 0.00；JCR 分区 Q0（未被收录）；收录数据库标注
      "Scopus收录 / DOAJ开放期刊 / 未被最新的JCR收录"
    · 艾思科蓝——中科院 SCI 期刊分区（2025年3月升级版）未检索到；
      《新锐期刊分区表》（2026年3月发布）未检索到；SCI 收录 coverage 仅 Scopus + DOAJ
    · 爱科学——中科院 JCR 分区 2025年3月升级版 未收录；2023年12月升级版 未收录
  存疑待核实：是否被 WoS 核心合集的 **ESCI**（Emerging Sources Citation Index）收录。
    researcher.life / Editage 标注 "Indexed in ... Web of Science"，但这两家是聚合站、
    未指明具体索引，而 Clarivate Master Journal List 为 JS 页面无法抓取。
    → 交由申请人以 mjl.clarivate.com（输入 ISSN 2451-9944）逐条核实后回填。
    → 即便确认为 ESCI，仍**不得**写为 "SCI 论文"（ESCI 与 SCIE 是 WoS 内两个不同索引）。
  维普给出的"影响因子(2025版) 1.963"为维普自算值（非 JCR IF），**不能作为 SCI 依据**。
'''
import io
import re
import sys

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V12.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V13.md'
text = io.open(SRC, encoding='utf-8').read()

# ---------- 1) 标题 ----------
EDITS = [
    ('# 福建省自然科学基金（面上项目）申请书 · 修订版 V12',
     '# 福建省自然科学基金（面上项目）申请书 · 修订版 V13',
     '标题版本号'),

    # ---------- 2) 头部：新增第 ⑥ 项改动 ----------
    ('B 类 3 项已落实/已裁定。第四轮综合评分 **4.0/5**，逐条落点见 `P6_标书第四轮修改对照表_2026-09-19.md`。',
     'B 类 3 项已落实/已裁定。第四轮综合评分 **4.0/5**，逐条落点见 `P6_标书第四轮修改对照表_2026-09-19.md`。\n'
     '> **⑥ 期刊层级复核（2026-09-20，申请人提问触发）**：对 §10.2 代表性论著① 所在期刊 '
     '*Neurobiology of Sleep and Circadian Rhythms* 的收录层级作五源交叉核验，确认其**未被 JCR 收录、'
     '无 JCR 影响因子、未进入中科院 SCI 期刊分区表**，故本稿**维持“国际同行评议期刊”表述、'
     '不按“SCI 论文”表述**；核验实录见 §13.1 第 67 项，提交前复核方法见 §13.2 第 22 条。',
     '头部·新增第⑥项'),

    # ---------- 3) §10.2 ①：期刊层级表述精确化 ----------
    ('该刊未进入 JCR 影响因子体系，**故本栏不列影响因子、亦不按“SCI 论文”表述**。',
     '该刊**未被 JCR 收录、无 JCR 影响因子、亦未进入中科院 SCI 期刊分区表**'
     # 注意：此处**不得**写"见 §13.1 第 67 项"——§13 是内部自查节，提交版会整节删除，
     #      写了就形成悬空交叉引用（第四轮 A1 的同型复发）。核验实录只留在留档版 §13.1。
     '（2026-09-20 经出版方期刊页与四家中文期刊数据库交叉核验），'
     '**故本栏不列影响因子、亦不按“SCI 论文”表述**；该刊是否被 Web of Science 核心合集的 '
     'Emerging Sources Citation Index（ESCI）收录尚待以 Clarivate Master Journal List 逐条核实，'
     '若确认收录则本栏据实补入“被 Web of Science 核心合集收录”，但**仍不按“SCI 论文”表述**。'
     '**上述层级以出版方与科睿唯安官方数据为准，若后续收录状态变化，本栏据实更新。**',
     '§10.2 ①·期刊层级'),

    # ---------- 4) §13.1 新增第 67 项（核验实录） ----------
    ('V11 引入了 [27]，却未把“26”与“预印本清单”当作需要回扫的检索词 | 已完成 |',
     'V11 引入了 [27]，却未把“26”与“预印本清单”当作需要回扫的检索词 | 已完成 |\n'
     '| 67 | **期刊层级复核（2026-09-20，申请人提问触发）**：对 *Neurobiology of Sleep and Circadian Rhythms* '
     '（ISSN 2451-9944，Elsevier，开放获取）是否为 SCI 期刊作五源交叉核验——'
     '① **Elsevier 官方 ScienceDirect 期刊页**"期刊对比表"Impact Factor 栏为 **"-"（空）**、CiteScore **4.2**；'
     '② **LetPub**（含繁体版）:"According to the latest JCR data, this journal is **not indexed in the JCR**"，'
     'WOS Quartile **Q0 N/A**、五年 IF **0**、实时影响因子 **-**；'
     '③ **刊鹿选刊**：影响因子 **0.00**、JCR 分区 **Q0（未被收录）**，收录数据库标注'
     '"Scopus 收录 / DOAJ 开放期刊 / **未被最新的 JCR 收录**"；'
     '④ **艾思科蓝**：中科院 SCI 期刊分区（2025 年 3 月升级版）**未检索到**，'
     '《新锐期刊分区表》（2026 年 3 月发布）**未检索到**；'
     '⑤ **爱科学**：中科院 JCR 分区 2025 年 3 月升级版与 2023 年 12 月升级版均**未收录**。'
     '**结论：该刊不是 SCI / SCIE 期刊**，本稿维持"国际同行评议期刊"表述、不按"SCI 论文"表述（§10.2 ①）。'
     '**一并排除两条误判来源**：researcher.life / Editage 标注的"Indexed in ... Web of Science"未指明具体索引'
     '（若为 ESCI 则仍**不等于** SCIE）；维普所载"影响因子(2025 版) 1.963"为维普自算值、非 JCR IF，'
     '**均不能作为 SCI 依据** | 已完成 |',
     '§13.1 新增第 67 项'),

    # ---------- 5) §13.2 新增第 22 条（提交前复核方法） ----------
    ('④ 分版后须复构图件编号（第 19 条） |',
     '④ 分版后须复构图件编号（第 19 条） |\n'
     '| 22 | **期刊收录层级的提交前复核（2026-09-20 新增）** | 申请人 | '
     '§10.2 代表性论著① 所在期刊现经五源核验确认**未被 JCR 收录、无影响因子**（见 §13.1 第 67 项），'
     '本稿据此不按"SCI 论文"表述。**提交前请再核一次**：'
     '① 打开 Clarivate Master Journal List（mjl.clarivate.com），输入 **ISSN 2451-9944**，'
     '查看 "Web of Science Coverage" 一栏——若列 **Science Citation Index Expanded (SCIE)** 则属 SCI，'
     '须同步修改 §10.2 ①、§13.1 第 54 项与 §9(1) 的表述；'
     '若列 **Emerging Sources Citation Index (ESCI)** 则**仍不是 SCI**，可据实补入'
     '"被 Web of Science 核心合集收录"，但不得写成"SCI 论文"；'
     '② **CiteScore / SJR / SNIP 每年更新**（本稿所载 CiteScore 4.2 为 2026 年 6 月最新版），'
     '若正文引用具体数值，须与当年最新值一致或改用不带数值的表述；'
     '③ 若该刊日后进入 SCIE，**必须逐一回扫**所有涉及"不按 SCI 表述"的句子（§9(1)、§10.2 ①、§13.1 第 54 项） |',
     '§13.2 新增第 22 条'),

    # ---------- 6) 文末署名行 ----------
    ('见 §13.1 第 66 项）。',
     '见 §13.1 第 66 项）；V13（第十轮）：据申请人提问复核 §10.2 代表性论著① 所在期刊的收录层级，'
     '确认其未被 JCR 收录、无影响因子、未进入中科院 SCI 分区表，维持"国际同行评议期刊"表述，'
     '并新增 §13.1 第 67 项（核验实录）与 §13.2 第 22 条（提交前复核方法）。',
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

print('--- V13：%d 处，全部命中且仅命中 1 次 ---' % n_ok)


# ---------- 7) 按实测重算 §13.2 第 16 条字数（不动点迭代） ----------
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
        '本稿实测（V13 定稿，2026-09-20）：正文（不含 §13、不含表格）约 **%.2f 万汉字**；'
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

# ---------- 8) 引号统一：本次新增文本里的 ASCII 双引号转为全角（本文件约定：ASCII 双引号归零） ----------
_n = text.count('"')
if _n % 2 != 0:
    print('!! FAIL ASCII 双引号个数为奇数，无法配对：%d' % _n)
    sys.exit(1)
buf = []
i = 0
for ch in text:
    if ch == '"':
        buf.append('\u201c' if i % 2 == 0 else '\u201d')
        i += 1
    else:
        buf.append(ch)
text = ''.join(buf)
print('引号统一：ASCII 双引号 %d 个已转为全角（左 %d / 右 %d）' % (_n, _n // 2, _n // 2))

# ---------- 定稿校验（定点断言，避免"自指陷阱"） ----------
assert '修订版 V13' in text, '标题版本号未更新'
assert '未被 JCR 收录、无 JCR 影响因子、亦未进入中科院 SCI 期刊分区表' in text, '§10.2 ① 未改写'
assert text.count('\u201c') == text.count('\u201d'), '全角引号不配对：%d / %d' % (
    text.count('\u201c'), text.count('\u201d'))
assert text.count('"') == 0, '仍存在 ASCII 双引号'
refs = [int(x) for x in re.findall(r'^\*\*\[(\d+)\]\*\*', text, re.M)]
assert refs == list(range(1, len(refs) + 1)), '参考文献编号不连续'
print('定稿校验：ASCII 双引号 0 / 全角引号 %d:%d 配对 / 参考文献 %d 条连续 / 行 %d'
      % (text.count('\u201c'), text.count('\u201d'), len(refs), text.count('\n') + 1))

io.open(DST, 'w', encoding='utf-8', newline='\n').write(text)
print('已写入 %s' % DST)
