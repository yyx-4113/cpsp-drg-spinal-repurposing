# -*- coding: utf-8 -*-
'''
P6 FJNSF 申请书 V7 -> V8 定点修订脚本（第五轮）
用户第 5 轮输入（四项事实澄清）：
  1) 杨代和：履历"硕士"与官网"教授、博士研究生导师"不冲突——硕士是学历，教授/博导是职称与学术资格。
  2) 杨代和进修：为两段独立经历（北京大学人民医院疼痛科进修；2014-2015 美国 Thomas Jefferson 大学医院访问学者）。
  3) 黄文职称：副主任医师（以履历原件为准）。
  4) 双单位：论文中 Yang Daihe 署名 "Department of Pain" 与 "Department of Anesthesiology" 指向同一科室同一人
     （本院麻醉科与疼痛科为同一批人员的两块牌子），非不同人员。

设计原则：只做行级定点替换，每处断言"命中且仅命中 1 次"；未命中即整体报错退出，绝不静默漏改。
'''
import io
import sys

SRC = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V7.md'
DST = 'results/P6_FJNSF_APPLICATION_SUBMISSION_V8.md'

text = io.open(SRC, encoding='utf-8').read()
lines = text.split('\n')

LOG = []


def find_one(pred, tag):
    idx = [i for i, l in enumerate(lines) if pred(l)]
    if len(idx) != 1:
        print('!! FAIL [%s] 命中 %d 次（须为 1 次）' % (tag, len(idx)))
        sys.exit(1)
    return idx[0]


def replace_line(pred, new, tag):
    i = find_one(pred, tag)
    old = lines[i]
    lines[i] = new
    LOG.append(('replace_line', tag, i + 1, old, new))


def swap_in_line(pred, pairs, tag):
    i = find_one(pred, tag)
    old = lines[i]
    s = old
    for a, b in pairs:
        n = s.count(a)
        if n != 1:
            print('!! FAIL [%s] 片段命中 %d 次: %r' % (tag, n, a[:50]))
            sys.exit(1)
        s = s.replace(a, b)
    lines[i] = s
    LOG.append(('swap_in_line', tag, i + 1, old, s))


def insert_after(pred, newlines, tag, offset=1):
    i = find_one(pred, tag)
    for k, nl in enumerate(newlines):
        lines.insert(i + offset + k, nl)
    LOG.append(('insert_after', tag, i + 1, lines[i], '\n'.join(newlines)))


# ---------------------------------------------------------------- 1. 版本号
replace_line(lambda l: l.startswith('# 福建省自然科学基金（面上项目）申请书'),
             '# 福建省自然科学基金（面上项目）申请书 · 修订版 V8', 'title')

# ---------------------------------------------------------------- 2. 两张表的列头：学位 → 学位（学历）
replace_line(lambda l: l.startswith('| 姓名 | 职称 / 学位 |') and '单位与科室' in l,
             '| 姓名 | 职称 / 学位（学历） | 单位与科室 | 项目分工 |', 'header_group')
replace_line(lambda l: l.startswith('| 姓名 | 职称 / 学位 |') and '与本项目相关' in l,
             '| 姓名 | 职称 / 学位（学历） | 与本项目相关的工作基础 | 分工 |', 'header_members')

# ---------------------------------------------------------------- 3. §1 项目组组成表：杨代和 / 黄文
replace_line(lambda l: l.startswith('| 杨代和 |') and '项目分工' not in l and '研究内容一、二的实验质量' in l,
             '| 杨代和 | 主任医师、教授、博士研究生导师 / 硕士（学历）；麻醉科主任（兼疼痛科主任） | 同上 | '
             '主要参加者：疼痛模型与机制设计把关，研究内容一、二的实验质量与统计分析监督；'
             '提供疼痛科与电针镇痛交叉机制视角 |', 'group_yangdaihe')

replace_line(lambda l: l.startswith('| 黄文 |') and 'qPCR 检测的实施与质量控制' in l,
             '| 黄文 | 副主任医师 / 硕士（学历） | 同上 | '
             '主要参加者：神经–免疫交互机制解析，免疫组化、蛋白印迹与 qPCR 检测的实施与质量控制 |',
             'group_huangwen')

# ---------------------------------------------------------------- 4. §1 表后加注（学历与职称/导师资格关系 + 科室口径）
insert_after(lambda l: l.startswith('| 在读硕士研究生 2 名 |') and '分子检测辅助、数据整理与统计分析' in l,
             ['',
              '> 注：表中“学位（学历）”栏为学历层次，“博士研究生导师”为学术资格（导师资格），二者不构成对应关系；'
              '杨代和同志的学历为硕士研究生，其主任医师职称与博士研究生导师资格均按临床与科研业绩取得。'
              '本院**麻醉科与疼痛科为同一科室（同一批人员、两块牌子）**，表中“单位与科室”统一表述为“麻醉科（疼痛科）”。'],
             'group_note')

# ---------------------------------------------------------------- 5. §10.3 成员表：杨代和（学历 + 两段进修）
swap_in_line(
    lambda l: l.startswith('| 杨代和 | 主任医师 / 教授、博士研究生导师；麻醉科主任') and 'Cell Biochem Funct' in l,
    [('| 杨代和 | 主任医师 / 教授、博士研究生导师；麻醉科主任（兼疼痛科主任） |',
      '| 杨代和 | 主任医师、教授、博士研究生导师 / 硕士（学历）；麻醉科主任（兼疼痛科主任） |'),
     ('；实用新型专利 4 项、发明专利 1 项；2014–2015 年美国 Thomas Jefferson 大学医院访问学者 |',
      '；实用新型专利 4 项、发明专利 1 项；**硕士研究生学历**（其主任医师职称与博士研究生导师资格按临床与科研业绩取得）；'
      '两段进修与访学经历——**曾于北京大学人民医院疼痛科进修**、**2014–2015 年美国 Thomas Jefferson 大学医院访问学者** |')],
    'members_yangdaihe')

# ---------------------------------------------------------------- 6. §10.3 成员表：黄文职称口径确认
swap_in_line(
    lambda l: l.startswith('| 黄文 | 副主任医师 / 硕士 |') and 'Chin J Integr Med' in l,
    [('| 黄文 | 副主任医师 / 硕士 |', '| 黄文 | 副主任医师 / 硕士（学历） |')],
    'members_huangwen')

# ---------------------------------------------------------------- 7. §10.3 表后加注：署名单位口径
insert_after(
    lambda l: l.startswith('> **团队既有协同的书面证据**'),
    ['> **关于署名单位的说明**：本院麻醉科与疼痛科为同一科室、同一批人员的两块牌子。杨代和主任同时担任'
     '麻醉科主任与疼痛科主任，其论文在不同时期分别以 “Department of Anesthesiology” 与 “Department of Pain” '
     '署名，指向**同一科室、同一人员**，属署名习惯差异，而非不同人员。本申请书统一以“麻醉科（疼痛科）”表述。'],
    'signature_note')

# ---------------------------------------------------------------- 8. §13.1 新增已核实项 38–40
insert_after(
    lambda l: l.startswith('| 37 | 已如实说明该文为'),
    ['| 38 | 团队成员学历与职称口径已明确：杨代和同志的学历为硕士研究生，其“主任医师、教授、博士研究生导师”'
     '为职称与导师资格，**二者不构成对应关系、并非矛盾**；§1 与 §10.3 两表列头已改为“职称 / 学位（学历）”并加注 | 已完成 |',
     '| 39 | 杨代和同志的两段进修与访学经历已**并列**写入 §10.3：曾于北京大学人民医院疼痛科进修；'
     '2014–2015 年美国 Thomas Jefferson 大学医院访问学者（此前仅写入修订说明、正文漏载，本轮修正） | 已完成 |',
     '| 40 | 黄文同志职称按履历原件确认为**副主任医师**；已加注说明本院麻醉科与疼痛科为同一科室，'
     '论文署名 “Department of Anesthesiology” 与 “Department of Pain” 指向同一人 | 已完成 |'],
    'checklist_new')

# ---------------------------------------------------------------- 9. §13.2 新增待确认项 15
insert_after(
    lambda l: l.startswith('| 14 | **ADRA2A 抗体特异性**'),
    ['| 15 | 杨代和同志北京大学人民医院疼痛科进修的起止年月 | 项目组 | 履历原件未载明时间，正文按事实写“曾于”而不虚构年份；'
     '若系统简历栏要求填时间，请据实补入 |'],
    'pending_new')

# ---------------------------------------------------------------- 10. 尾注
replace_line(
    lambda l: l.startswith('*本申请书由申请人杨永新撰写，2026-09-19 修订为 V7 版'),
    '*本申请书由申请人杨永新撰写，2026-09-19 修订为 V8 版（第五轮：明确团队成员学历与职称口径、'
    '补全杨代和同志两段进修与访学经历、加注科室与论文署名单位口径）。'
    '配套文件：`P6_V8_修订说明与遗留事项_2026-09-19.md`。*', 'footer')

io.open(DST, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))

print('=' * 78)
print('V8 定点修订：%d 处，全部命中且仅命中 1 次' % len(LOG))
print('=' * 78)
for kind, tag, ln, old, new in LOG:
    print('\n--- [%s] %s @ 行 %d ---' % (kind, tag, ln))
    print('  - 旧: %s' % (old[:150].replace('\n', ' ')))
    print('  + 新: %s' % (new[:150].replace('\n', ' ')))
print('\n输出：%s' % DST)
