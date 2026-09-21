# -*- coding: utf-8 -*-
'''
P6 FJNSF 申请书 V10 -> V11 定点修订（第八轮 / V10 补录）
用户第 8 轮输入（Research Square 通知原文）：负责人的预印本
  "Cells are not replicates: permutation calibration of the unit-of-analysis error in a pooled sleep
   single-cell design (GSE137665)" 已发布，DOI 10.21203/rs.3.rs-11022757/v1

本轮把该预印本据实补录，并同步更新参考文献表：
  1) 头部定位块改为 V11 四项改动，并把预印本独立成第 ② 项；
  2) §3.5(11)、(13) 补引 [27]，并把预印本中的量化结果（经验 I 类错误率 37.7% vs 库级 3.0%）写出；
  3) §3.6 新增 [27]（预印本，含可核验 DOI）；
  4) §10.2 代表性论著栏插入 ②（预印本，独立作者）并整体重排为 ①–⑦；说明段与 §10.3 同步；
  5) §13.1 新增已核实项 59–61；§13.2 第 10 条按新事实改写（DOI 问题已解决）；
  6) 参考文献总数 26 -> 27，同步修正两处计数表述。

核验记录（写作前已完成）：
  Crossref API `https://api.crossref.org/works/10.21203/rs.3.rs-11022757/v1`
    - type = posted-content / subtype = preprint（确为预印本，非期刊论文）
    - posted = 2026-09-15；group-title = "In Review"（Research Square 的 "In Review" 系列）
    - author = 永新 杨，affiliation = The Second Affiliated Hospital of Fujian University of
      Traditional Chinese Medicine（单位与本单位一致；**独立作者**）
    - abstract 内含：nine libraries，each a suspension pooled from three animals；
      df = 29,566（细胞级）vs n = 9 / df = 4（库级）；216 assignments；
      经验 I 类错误率 37.7%（细胞级）vs 3.0%（库级）
'''
import io
import sys

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V10.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V11.md'

lines = io.open(SRC, encoding='utf-8').read().split('\n')
LOG = []

PP_TITLE = ('Cells are not replicates: permutation calibration of the unit-of-analysis error in a pooled '
            'sleep single-cell design (GSE137665)')
PP_DOI = '10.21203/rs.3.rs-11022757/v1'


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
            print('!! FAIL [%s] 片段命中 %d 次: %r' % (tag, s.count(a), a[:70]))
            sys.exit(1)
        s = s.replace(a, b)
    old = lines[i]
    lines[i] = s
    LOG.append((tag, i + 1, old[:80], s[:80]))


def insert_after(pred, newlines, tag, offset=1):
    i = find_one(pred, tag)
    for k, nl in enumerate(newlines):
        lines.insert(i + offset + k, nl)
    LOG.append((tag, i + 1, lines[i][:80], '\n'.join(newlines)[:200]))


def replace_block(start_pred, end_pred, newlines, tag):
    i = find_one(start_pred, tag + '-s')
    j = find_one(end_pred, tag + '-e')
    lines[i:j + 1] = newlines
    LOG.append((tag, i + 1, '（%d 行）' % (j - i + 1), '\n'.join(newlines)[:200]))


# ================================================================ 1. 标题与头部定位块
replace_line(lambda l: l.startswith('# 福建省自然科学基金（面上项目）申请书 · 修订版 V10'),
             '# 福建省自然科学基金（面上项目）申请书 · 修订版 V11', 'title')

replace_block(
    lambda l: l.startswith('> **本稿（V10）三项改动**'),
    lambda l: l.startswith('> 不作活细胞分选标记”。逐条落点见'),
    ['> **本稿（V11）四项改动**：① 据实补入负责人**已被接收**的国际期刊论文（*Neurobiology of Sleep and Circadian Rhythms*，'
     'Elsevier 出版；独立作者数据评论，',
     '> 主题为单细胞转录组中的伪重复与数据泄漏——与本项目**方法学层**直接同源），同步更新 §3.4、§3.5(11)(13)、§6.2、'
     '§9(1)、§10.2（内 3 处）、',
     '> §10.3 共八处；② 补录负责人**独立作者**的预印本（*Cells are not replicates: permutation calibration of the '
     'unit-of-analysis error in a pooled sleep',
     '> single-cell design (GSE137665)*，Research Square，2026-09-15 公开，doi:10.21203/rs.3.rs-11022757/v1），'
     '并列入参考文献 **[27]**；',
     '> ③ 收口第三轮专家组**保留意见**——在 §5.3 将“分选纯度”单列为一条风险，给出交叉污染预设阈值与三级退守路径，'
     '§6.4 补第 8 条局限；',
     '> ④ 横向一致性自审——修正 §13.2 第 16 条已过期的篇幅/字数口径（改按实测重算，单一来源见该行），'
     '并给 §11.1 的抗体清单补注',
     '> “抗体用于组织化学与免疫荧光、不作活细胞分选标记”。逐条落点见 `P6_V11_修订说明与遗留事项_2026-09-19.md`。'],
    'header')

replace_line(lambda l: l.startswith('> **参考文献**：26 条全部内嵌于 §3.6'),
             '> **参考文献**：**27 条**全部内嵌于 §3.6，编号与 `results/P6_FJNSF_REFERENCES.md` 一致，'
             '均含可核验 DOI/PMID；其中 **[27] 为申请人独立作者的预印本**（已显式标注）。',
             'ref-note')

# ================================================================ 2. §3.5(11) 补引 [27]
swap_in_line(
    lambda l: l.startswith('**（11）抗伪重复的方法学纪律。**'),
    [('并给出置换校准与“以动物数报告样本量”的可操作建议。',
      '并给出置换校准与“以动物数报告样本量”的可操作建议。该分析的完整版本与量化结果——'
      '因原研究在**捕获前合并了 3 只动物**的细胞悬液、动物标签被销毁，细胞级检验（df = 29,566）在名义 α = 0.05 下'
      '的经验 I 类错误率高达 **37.7%**，而库级检验（n = 9）为 **3.0%**——已以预印本公开 [27]。')],
    'basis11-pp')

# ================================================================ 3. §3.5(13) 补录预印本
swap_in_line(
    lambda l: l.startswith('**（13）学术延续性之二（方法学层）'),
    [('本申请书仅据其方法学价值引用，不作课题方向上的等同表述。',
      '本申请书仅据其方法学价值引用，不作课题方向上的等同表述。'
      '该条方法学线另有**可公开查验的预印本记录**（同以 GSE137665 为分析对象，负责人独立作者）[27]：'
      '在原研究中，9 个文库各由 3 只动物的细胞悬液**合并**后上机，动物标签被销毁，'
      '**动物间方差分量不可估计**；该文以细胞级（df = 29,566）与库级（n = 9，df = 4）两个单位拟合同一模型、'
      '并以 216 次条件标签置换做校准，测得细胞级检验的经验 I 类错误率为 **37.7%**，库级为 **3.0%**；'
      '在库级口径下无一基因通过 FDR < 0.1 或 Bonferroni 校正。上述数字均可在该预印本中逐条核验，'
      '其结论对本项目的直接含义是：**“可得的细胞数”不等于“可用的样本量”**——'
      '这正是本项目在单细胞/空间层一律按样本/供体聚合、并在动物实验设计中以个体为统计单元的原因。')],
    'basis13-pp')

# ================================================================ 4. §3.6 新增 [27]
insert_after(
    lambda l: l.startswith('**[26]** DenAdel A'),
    ['',
     '**[27]** Yang Y. ' + PP_TITLE + '. *Research Square [预印本].* 2026. doi:' + PP_DOI +
     '（**申请人独立作者**；2026-09-15 公开，Research Square “In Review” 系列，**未经同行评议**）'],
    'ref27')

# ================================================================ 5. §10.2 论著栏：插入 ② 并重排
swap_in_line(
    lambda l: l.startswith('| **代表性论著** |'),
    [('<br>**⑥** 本项目前期计算管线的公开代码仓库', '<br>**⑦** 本项目前期计算管线的公开代码仓库'),
     ('<br>**⑤** 主持福建省教育厅中青年教师教育科研项目结题成果',
      '<br>**⑥** 主持福建省教育厅中青年教师教育科研项目结题成果'),
     ('**④（第四作者）**', '**⑤（第四作者）**'),
     ('**③（第三作者）**', '**④（第三作者）**'),
     ('<br>**②（第一作者）** 杨永新',
      '<br>**②（预印本，独立作者）** ' + PP_TITLE + '. *Research Square [预印本].* 2026. doi:' + PP_DOI +
      '（**负责人为独立作者**，署名单位为“福建中医药大学附属第二人民医院”，与本单位一致；2026-09-15 公开，'
      '属 Research Square “In Review” 系列，**未经同行评议**）。'
      '**内容**：对公开数据集 GSE137665（小鼠脑干、皮层与下丘脑单细胞，正常睡眠 / 12 h 睡眠剥夺 / 恢复睡眠）'
      '做单位分析错误（unit-of-analysis error）的置换校准——原研究的 9 个文库各由 3 只动物的细胞悬液**合并**后上机，'
      '**动物标签被销毁、动物间方差分量不可估计**；该文以细胞级（df = 29,566）与库级（n = 9，df = 4）两个单位'
      '拟合同一模型、并以 216 次条件标签置换校准，测得细胞级检验的经验 I 类错误率为 **37.7%**（名义 α = 0.05），'
      '库级为 **3.0%**，并审计了原研究的 RNAscope 验证层与其自带的差异表达输出。'
      '**与本项目的关系**：与本节 ① 同属“单细胞统计判读纪律”这一条方法学线，同为**方法学同源、'
      '非课题方向重复**；其“合并建库后动物水平推断不可恢复”的结论，正是本项目对单细胞/空间层数据一律采用'
      '样本/供体级聚合、并在动物实验中以个体为统计单元的依据（见 §3.5(11)(13)）<br>'
      '**③（第一作者）** 杨永新')],
    'cv-pubs-pp')

# ================================================================ 6. §10.2 说明段
swap_in_line(
    lambda l: l.startswith('| **代表性论著** |'),
    [('申请人的发表记录包含国际期刊论文 1 篇（独立完成，方法学数据评论，**已被接收**）与中文期刊论文 3 篇'
      '（第一作者 1 篇，第三、第四作者各 1 篇）。',
      '申请人的发表记录包含国际期刊论文 1 篇（独立完成，方法学数据评论，**已被接收**）、预印本 1 篇'
      '（独立完成，已获 DOI，与前者同属“单细胞统计判读纪律”这条方法学线）与中文期刊论文 3 篇'
      '（第一作者 1 篇，第三、第四作者各 1 篇）。'),
     ('**上述三项——在体疼痛模型的第一作者研究经验、可完整复现的计算管线、以及已获国际期刊接收的方法学论证能力'
      '——构成本项目可行性的主要依据。**',
      '**上述四项——在体疼痛模型的第一作者研究经验、可完整复现的计算管线、已获国际期刊接收的方法学论证能力、'
      '以及已公开可引用的预印本记录——构成本项目可行性的主要依据。**')],
    'cv-pubs-sum')

# ================================================================ 7. §10.3 团队表负责人行
swap_in_line(
    lambda l: l.startswith('| 杨永新 | 主治医师 / 学士 | 主持完成福建省教育厅课题 1 项'),
    [('单细胞转录组伪重复与数据泄漏的方法学数据评论，待刊出**；',
      '单细胞转录组伪重复与数据泄漏的方法学数据评论，待刊出**；'
      '**预印本（独立作者，已获 DOI）：' + PP_TITLE + '，*Research Square*，2026，doi:' + PP_DOI + '**；')],
    'team-lead-pp')

# ================================================================ 8. §13.1 新增 59–61
insert_after(
    lambda l: l.startswith('| 58 | 篇幅口径的**复核规则**已建立'),
    ['| 59 | 负责人**独立作者**的预印本已补录：*Cells are not replicates: permutation calibration of the '
     'unit-of-analysis error in a pooled sleep single-cell design (GSE137665)*，Research Square，2026-09-15 公开，'
     'doi:10.21203/rs.3.rs-11022757/v1；落点：头部定位块、§3.5(11)、§3.5(13)、§3.6 [27]、§10.2 论著栏②、'
     '§10.2 说明段、§10.3 | 已完成 |',
     '| 60 | 该预印本元数据已据实核验（Crossref API 逐字段）：`type = posted-content / subtype = preprint`'
     '（确为预印本、非期刊论文）；`posted = 2026-09-15`；作者栏仅 **Yongxin Yang** 一人，'
     '单位 “The Second Affiliated Hospital of Fujian University of Traditional Chinese Medicine”'
     '**与本单位一致**；平台标注为 Research Square “In Review” 系列。'
     '故正文按“**预印本、未经同行评议、独立作者**”表述，**不并入期刊论文计数** | 已完成 |',
     '| 61 | 参考文献表已由 **26 条扩为 27 条**（新增 [27] 预印本，含可核验 DOI），'
     '并同步修正 §3.6 前注释与 §13.1 第 12 项的计数表述；`results/P6_FJNSF_REFERENCES.md` 已同步 | 已完成 |'],
    'checklist_new2')

replace_line(lambda l: l.startswith('| 12 | 参考文献 26 条全部内嵌'),
             '| 12 | 参考文献 **27 条**全部内嵌；[14][15][16] 已补引用位置（新增 [27] 为申请人独立作者的预印本） | 已完成 |',
             'checklist12')

# ================================================================ 9. §13.2 第 10 条改写
replace_line(
    lambda l: l.startswith('| 10 | **代表性论著的完整性'),
    '| 10 | **代表性论著的完整性（本轮已解决主体部分）** | 申请人 | 已补入负责人**已被接收**的国际期刊论文'
    '（Elsevier，独立完成，方法学数据评论）与其**独立作者**的 Research Square 预印本（已获 DOI），'
    '原“记录以中文期刊为主”的短板已补强。仍需申请人确认三点：'
    '① 已接收论文的作者署名与接收函署名页一致，并补入接收函日期与见刊后的 DOI 与卷期页码；'
    '② 该预印本与已被接收的数据评论是**同一工作的两个版本**，还是**两项独立工作**——'
    '若为同一工作，建议在论著栏标注“预印本 → 见刊”的对应关系以体现过程透明；若为两项独立工作，'
    '请在系统填报时分别列出，并注意向接收期刊如实披露预印本存在（Research Square 页面标注为 “In Review” 系列）；'
    '③ 中文期刊论文是否标注教育厅项目编号，若有请在系统填报时同步注明 |',
    'pending10-v11')

# ================================================================ 10. 尾注
replace_line(
    lambda l: l.startswith('*本申请书由申请人杨永新撰写，2026-09-19 修订为 V10 版'),
    '*本申请书由申请人杨永新撰写，2026-09-19 修订为 V11 版（第八轮：① 补录负责人独立作者的 Research Square '
    '预印本（doi:10.21203/rs.3.rs-11022757/v1）并列入参考文献 [27]，同步更新 §3.5(11)(13)、§10.2、§10.3；'
    '② 保留 V10 的三项改动：补入已被接收的国际期刊论文、收口“分选纯度”保留意见、横向一致性自审）。'
    '配套文件：`P6_标书评审意见书_专家组_第三轮_2026-09-19.md`、`P6_标书第三轮修改对照表_2026-09-19.md`、'
    '`P6_V10_修订说明与遗留事项_2026-09-19.md`、`P6_V11_修订说明与遗留事项_2026-09-19.md`。*',
    'footer')

io.open(DST, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

print('=' * 78)
print('V11 定点修订：%d 处，全部命中且仅命中 1 次' % len(LOG))
print('=' * 78)
for tag, ln, old, new in LOG:
    print('\n--- [%s] @ 行 %d ---' % (tag, ln))
    print('  - 旧: %s' % old)
    print('  + 新: %s' % new)
print('\n输出：%s' % DST)
