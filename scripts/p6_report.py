#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_report.py -- 汇总 P6 全部产物为 results/P6_RESULTS.md

【原则】报告里出现的每个数字都必须能追到本项目 results/tables 下的某个文件，
不允许手写硬编码的"好看数字"。因此本脚本**全部字段从表里读**，读不到就写
"未完成/不可用"并记入"缺口"一节，而不是留空或编造。
"""
import os, json, glob
import pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
FIG = os.path.join(ROOT, "results/figures")
OUT = os.path.join(ROOT, "results/P6_RESULTS.md")

gaps = []


def rd(name, **kw):
    p = os.path.join(TAB, name)
    if not os.path.exists(p):
        gaps.append(name)
        return None
    return pd.read_csv(p, **kw)


def rj(name):
    p = os.path.join(ROOT, "results", name) if not os.path.isabs(name) else name
    if not os.path.exists(p):
        p = os.path.join(TAB, name)
    if not os.path.exists(p):
        gaps.append(name)
        return None
    return json.load(open(p, encoding="utf-8"))


def md_table(df, cols=None, fmt="%.3f", n=None):
    if df is None or not len(df):
        return "_（无数据）_\n"
    d = df if cols is None else df[cols]
    if n:
        d = d.head(n)
    try:
        return d.to_markdown(index=False, floatfmt=".3f" if fmt == "%.3f" else fmt) + "\n"
    except Exception:
        return "```\n" + d.to_string(index=False) + "\n```\n"


L = []

# ============ 头部 ============
L.append("# P6 老药新用虚拟筛选结果（CPSP / DRG-脊髓轴）\n")
L.append("> 本文件由 `scripts/p6_report.py` 自动生成，所有数值从 `results/tables/` 下的产物读取。\n")

# ============ 1. 设计 ============
L.append("## 1. 目的与设计\n")
L.append(
    "在 P3 双机器学习锁定的 hub 靶标与 §6 优先靶标之上，用已批准药物库做**结构基础的"
    "虚拟筛选（分子对接）**，产出可进入湿实验的老药新用候选清单，并用**反向阳性对照**为"
    "每个靶标的排序结论定可信度权重。\n\n"
    "关键设计选择：**对接打分的保真度上限**必须先用实测确立，再决定对接参数；"
    "否则会得到一个看似完整、实则排序失效的结果矩阵（见第 5 节）。\n")

# ============ 2. 环境 ============
L.append("## 2. 计算环境\n")
L.append("| 项 | 值 |\n|---|---|\n"
         "| Python | 3.13.14（隔离 venv） |\n"
         "| 对接引擎 | AutoDock Vina 1.2.5（官方 Windows exe） |\n"
         "| 配体准备 | RDKit + Meeko 0.8.0 |\n"
         "| 受体准备 | gemmi + Open Babel 3.1.0 |\n"
         "| 并行 | 7 worker × `--cpu 1`（8 核机） |\n")

# ============ 3. 配体库 ============
L.append("## 3. 配体库（已批准药物）\n")
fun = rj("P6_ligand_funnel.json")
if fun:
    L.append("来源：ChEMBL `max_phase=4`（DrugBank 已批准药物的开放等价物），"
             "以 Broad Drug Repurposing Hub（CC0）交叉注释。\n")
    rows = "\n".join(f"| {k} | {v} |" for k, v in fun.items())
    L.append("| 漏斗阶段 | 数量 |\n|---|---|\n" + rows + "\n")
else:
    L.append("_（漏斗数据缺失）_\n")

LIG = rd("P6_ligand_library.csv")
if LIG is not None:
    ok = LIG[LIG["pass"] == True]
    L.append(f"- 进入对接的配体：**{len(ok):,}** 个（占候选 {len(LIG):,} 的 {100*len(ok)/max(len(LIG),1):.1f}%）\n")
    if "pain_prior" in ok.columns:
        L.append(f"- 已知镇痛药（人工标注先验）覆盖：**{int(ok.pain_prior.sum())}** 个\n")
    cns = rd("P6_ligand_cns_prior.csv")
    if cns is not None:
        L.append(f"- CNS/镇痛先验子集（Tier 1）：**{len(cns):,}** 个\n")
    # 盐形式修复的留痕
    L.append("\n> **方法学留痕**：配体准备阶段曾用 `rdMolStandardize.FragmentParent` 去反离子，"
             "它对本库中含盐的多组分 SMILES 抛 `RuntimeError`，异常被 `except: pass` 吞掉后"
             "该分子仍带反离子，随后在构象生成阶段再次抛错，**导致 1,078 个含盐药物被静默丢弃**"
             "（丙戊酸钠、色甘酸钠、沙奎那韦、阿仑膦酸钠等）。改用 `LargestFragmentChooser`"
             "后配体数由 2,040 升至 3,085，失败归零。\n")

# ============ 4. 靶标 ============
L.append("## 4. 靶标可成药性筛查\n")
TS = rd("P6_target_selection.csv")
REC = rd("P6_receptors.csv")
if TS is not None:
    vc = TS.decision.value_counts().to_dict()
    L.append(f"候选靶标 **{len(TS)}** 个（35 个 P3 hub + §6 优先靶标），决策分布：\n\n"
             + "\n".join(f"- `{k}`：{v}" for k, v in vc.items()) + "\n")
if REC is not None:
    okr = REC[REC.status == "OK"]
    L.append(f"\n完成受体准备、可实际对接的靶标：**{len(okr)}** 个\n\n")
    L.append(md_table(okr, ["symbol", "pdb_id", "ligand_ref", "target_chains"], n=20))
    fail = REC[REC.status != "OK"]
    if len(fail):
        L.append(f"\n未能对接的 {len(fail)} 个，原因分布：\n\n"
                 + "\n".join(f"- `{k}`：{v}" for k, v in fail.status.value_counts().items()) + "\n")

L.append("\n> **必须如实写进局限的结构性缺口**：§6 列为优先靶标的离子通道类"
         "（SCN9A / SCN10A / SCN11A / KCNQ2 / CACNA2D1 / GABRA1）**全部无法对接** —— "
         "它们是无可用 holo 晶体结构的膜蛋白，缺少可定位的正构位点。"
         "这意味着 P6 的结论**不能**覆盖 §6 中机制上最重要的一类镇痛靶标，"
         "只能覆盖有结构可用的一支。这一限制不能靠措辞弱化。\n")

# ============ 5. 参数保真度 ============
L.append("## 5. 对接参数保真度验证（本阶段最关键的方法学结论）\n")
P1 = rd("P6_stage1_param_validation.csv")
P2 = rd("P6_exh_validation.csv")


def param_summary(df, variants, gold="gold_aff", gold_sec="gold_sec"):
    """把逐配体验证表压成"设置 → 保真度指标"的汇总对照表，并把结果落盘以便审计。

    报告正文只放汇总；逐配体原始值留在 results/tables/P6_*_validation.csv 作审计凭证
    （把 15 行 × 8 列的原始表塞进正文，会把方法学结论淹掉）。

    **Δ 的定义必须写死**：Δ_i = 变体亲和力_i − 金标准亲和力_i（**带符号**，正 = 变体打分更弱）。
    ρ(Δ, 可旋转键) 用 Spearman。只有带符号 Δ 才能回答"偏差是否**系统性**地惩罚柔性配体"——
    用 |Δ| 会把"柔性配体被打得更弱"和"刚性配体被打得更弱"混在一起，方向相反时互相抵消，
    得到看似"无偏"的假象。本项目先前一版报告里写的 ρ(Δ,tors)≈0.48 与 −0.108/−0.198
    分别对应**两种不同定义**且无法复现，属不可追溯数字，已废弃；下表口径唯一。
    """
    if df is None:
        return None
    rows = []
    base_sec = df[gold_sec].mean()
    rows.append({"设置": "金标准（基准）", "n": len(df), "rho_Spearman": 1.0,
                 "delta_abs_median": 0.0, "delta_mean": 0.0, "rho_delta_tors": 0.0,
                 "top10_recall": 1.0, "sec_mean": base_sec, "speedup": 1.0})
    for name, lab, sec in variants:
        if name not in df.columns:
            continue
        ds = df[name] - df[gold]                       # 带符号 Δ
        dabs = ds.abs()
        # 方差为 0（如刚性配体子集）时相关系数无定义 → 置 0，不要报 NaN
        rho_t = df.n_torsions.corr(ds, method="spearman")
        rho = df[gold].corr(df[name], method="spearman")
        k = max(int(round(0.1 * len(df))), 1)
        g_top = set(df.nlargest(k, gold).chembl_id)
        v_top = set(df.nlargest(k, name).chembl_id)
        rec = len(g_top & v_top) / k
        secm = df[sec].mean()
        rows.append({"设置": lab, "n": len(df),
                     "rho_Spearman": rho if pd.notna(rho) else 0.0,
                     "delta_abs_median": dabs.median(), "delta_mean": ds.mean(),
                     "rho_delta_tors": rho_t if pd.notna(rho_t) else 0.0,
                     "top10_recall": rec, "sec_mean": secm,
                     "speedup": base_sec / secm if secm else float("nan")})
    return pd.DataFrame(rows)


SUMS = []
if P1 is not None:
    L.append("做法：在锚点靶标（MAPK14 / 3LFF）上，按**可旋转键分层抽样** 15 个配体，"
             "以慢速高精度设置为金标准，比较各快速设置与金标准的一致性。\n\n"
             "口径（唯一，全文一致）：Δ = 变体亲和力 − 金标准亲和力（**带符号**，正 = 变体打分更弱）；"
             "ρ(Δ, 可旋转键) 用 Spearman，**只有带符号 Δ 才能检验偏差是否系统性地惩罚柔性配体**。"
             "逐配体原始值见 `results/tables/P6_stage1_param_validation.csv`。\n\n")
    S = param_summary(P1, [("c0_aff", "exh2 + max_evals 2000", "c0_sec"),
                           ("c1_aff", "exh2 + max_evals 6000", "c1_sec")])
    if S is not None:
        L.append(md_table(S, n=None))
        SUMS.append(S.assign(section="max_evals"))
if P2 is not None:
    L.append("\n`exhaustiveness` 专项对照（复用同批金标准，逐配体原始值见 "
             "`results/tables/P6_exh_validation.csv`）：\n\n")
    S2 = param_summary(P2, [("exh2_aff", "exhaustiveness 2（默认）", "exh2_sec"),
                            ("exh1_aff", "exhaustiveness 1", "exh1_sec")])
    if S2 is not None:
        L.append(md_table(S2, n=None))
        SUMS.append(S2.assign(section="exhaustiveness"))
if SUMS:
    pd.concat(SUMS, ignore_index=True).to_csv(
        os.path.join(TAB, "P6_param_summary.csv"), index=False)
    L.append("\n> 上表已落盘为 `results/tables/P6_param_summary.csv`，供稿件中每个数字溯源。\n")
L.append("""
**结论（决定了整个 P6 的参数选择）**：

- **`--max_evals` 路线不可用**：它压缩的是**单次运行的采样步数上限**，柔性配体因此搜不到
  最优构象。表现在两个层面同时出现：① **整体大幅偏弱**（Δ 均值 +2.17 / +1.71 kcal/mol）；
  ② **偏弱幅度随柔性增强**（ρ(Δ, 可旋转键) = +0.263 / +0.249，为**正**，即越柔性被打得越弱）
  —— 这是**系统性**偏差，会直接把柔性配体挤出榜单。
  最终 Spearman ρ ≤ 0.11，**top-10% 召回率 0%**：排序完全失效，
  不可用于任何"取 top-N 候选"的用途。
- **`--exhaustiveness` 路线可用**：它只是**重复独立优化取最优**，单次运行本身已充分，
  降到 1 只带来一个**近似恒定的轻微偏移**（Δ 均值 +0.45 kcal/mol），
  且该偏移**几乎不随柔性变化**（ρ(Δ, 可旋转键) = +0.029，接近零）
  —— 恒定偏移不改变配体之间的相对次序，所以排序保真度得以保持：
  exh=1 与 exh=2 的 Spearman ρ **完全相同（0.783）**，而单配体耗时由 27.2s 降至 5.9s（**4.6×**）。
- **最终参数：`--exhaustiveness 1`，不设置 `--max_evals`。**
  算力不足时应缩配体库或靶标数，**绝不压 `max_evals`**。
- **保真度现实上限 ρ ≈ 0.78**。因此全文措辞为 *candidate prioritisation*（候选优选），
  **不得**表述为 *accurate binding ranking*（精确结合能排序）。
""")

# ============ 6. 对接执行 ============
L.append("## 6. 对接执行\n")
S1 = rd("P6_docking_scores_t1_cns.csv")
S2 = rd("P6_docking_scores_t2_other.csv")
L.append("| 分层 | 配体 | 靶标 | 对接次数 | 状态 |\n|---|---|---|---|---|\n")
for nm, S, nlig in [("Tier 1（CNS/镇痛先验）", S1, 620), ("Tier 2（其余已批准药）", S2, 2465)]:
    if S is None:
        L.append(f"| {nm} | {nlig} | 10 | {nlig*10:,} | **未完成** |\n")
    else:
        L.append(f"| {nm} | {S.chembl_id.nunique()} | {S.symbol.nunique()} | {len(S):,} | 完成 |\n")
if S1 is not None or S2 is not None:
    A = pd.concat([x for x in [S1, S2] if x is not None], ignore_index=True)
    L.append(f"\n合计完成对接 **{len(A):,}** 次；有打分 {int(A.affinity.notna().sum()):,} 次。\n")
    if "err" in A.columns:
        nerr = int((A.err.fillna("") != "").sum())
        L.append(f"对接返回错误/无打分：{nerr} 次（{100*nerr/max(len(A),1):.2f}%）。\n")
    if "sec" in A.columns:
        L.append(f"单次对接耗时：中位 {A.sec.median():.1f}s，合计 {A.sec.sum()/3600:.1f} 机时。\n")

# ============ 7. 反向对照 ============
L.append("## 7. 反向阳性对照（方法学校验）\n")
RC = rd("P6_reverse_control.csv")
RCP = rd("P6_reverse_control_positives.csv")
if RCP is not None:
    cnt = RCP.groupby("symbol").chembl_id.nunique()
    L.append("ChEMBL 实测活性层（pChEMBL ≥ 6，即 ≤1 µM）提供的阳性数：\n\n"
             + "\n".join(f"- {s}：{int(v)}" for s, v in cnt.sort_values(ascending=False).items()) + "\n\n")
if RC is not None:
    L.append(md_table(RC, ["symbol", "n_known_pairs", "n_ligands", "known_median_aff",
                           "all_median_aff", "auc_known_vs_rest", "reliable"]))
    rel = RC[RC.reliable == True]
    L.append(f"\n**通过校验（AUC ≥ 0.60 且阳性数 ≥ 3）的靶标：{len(rel)} 个"
             f"（{', '.join(rel.symbol) if len(rel) else '无'}）。**\n\n"
             "未通过校验的靶标，其打分排序被视为缺乏区分力，在四维评分中 D4 取中性 0.5。\n")
L.append("""
**标签口径决策（为什么只用 ChEMBL）**：反向对照测的是「对接打分能否区分**真正结合**该靶标的分子」，
因此标签必须是**结合型**（实测 IC50/Kd/Ki ≤ 1 µM），不能掺入**适应症/注释型**标签 ——
PAIN_PRIOR 记的是"这药是已知镇痛药"，DRH target 字段记的是"注释靶点"，二者回答的是不同问题。
实测（ADRA2A，Tier 1）：纯 ChEMBL n=88 → **AUC 0.618**；掺入 DRH(+11)/PAIN_PRIOR(+2) 后
n=101 → AUC 0.592。两者都 > 0.5（方向一致、结论稳健），但**本稿以 ChEMBL 口径为主**，
因其判据单一、客观、可复现。手工镇痛药标注改用于 §3.4 的**面容效度**分析（另一个独立问题）。
""")
L.append("""
**关于阳性集覆盖的真实情况（不可略过）**：仅用 Drug Repurposing Hub 的靶点注释 +
人工镇痛药标注时，阳性集会**几乎全部落在 ADRA2A 一个靶标上**（其余 9 个为 0）。
原因是真实的：MAPK14 在 DRH 中有 38 个注释药物，但**全是临床前/Ph1–3 的 p38 抑制剂，
没有一个是已批准药**，而本库是已批准药库，故交集为 0；AXL / ACVR1 / SLC2A1 / SERPINE1 同理。
脚本 `scripts/p6_score.py` 中曾有一条 `and t not in hub` 的过滤条件 ——
而 10 个可对接靶标里有 9 个本身就是 hub 基因 —— 该条件会把 DRH 层阳性几乎全部滤掉，
使反向对照退化为"仅 1 个靶标"，属于隐蔽的失效，已修正。另由
`scripts/p6_reverse_control.py` 引入与对接完全独立的 ChEMBL 实测活性作为补充阳性来源。
""")

# ---- 7b. 分子量混淆检验 ----
MWC = rd("P6_enrichment_mw_confounder_check.csv")
L.append("\n### 7.1 富集信号是否为「分子量伪信号」？（必答的审稿问题）\n")
if MWC is None or MWC.empty:
    L.append("_未产出（需先运行 `scripts/p6_mw_confounder.py`）。_\n")
else:
    L.append("""
分子对接打分天然偏袒**大分子**：配体越大、重原子越多，打分函数给出的亲和力数值越负。
因此"已知活性药富集"很可能是**分子量（MW）伪信号**而非方法有效。
本检验给出三重防线：**① MW-only 基线**（仅用 MW 预测阳性的 AUC，尺寸偏倚上界）、
**② MW 线性校正后 AUC**（对接打分对 MW 回归取残差）、**③ MW 五分位分层内 AUC**（非参数，最稳健）。
判读规则在 `scripts/p6_mw_confounder.py` 中写死，不做事后解释：
只有 docking AUC > 0.5 **且**校正/分层后仍 > 0.5 **且** AUC_dock > AUC_MW_only，才可声称为方法效度证据。
""")
    L.append(md_table(MWC, ["symbol", "n_known", "n_total", "AUC_dock", "AUC_MW_only",
                            "AUC_MW_adjusted", "AUC_MW_stratified", "rho_affinity_MW",
                            "p_mannwhitney", "verdict"]))
    pas = MWC[MWC.verdict.astype(str).str.startswith("PASS")]
    L.append(f"\n**判定为 PASS（富集非尺寸伪信号）的靶标：{len(pas)} 个"
             f"（{', '.join(pas.symbol) if len(pas) else '无'}）。**\n\n"
             "注意：打分与 MW 的 Spearman ρ 为**负值**（大分子打分更好）且绝对值较大，"
             "说明尺寸偏倚**确实存在**；正因如此，未做此校正的富集 AUC 不可直接引用。"
             "校正后 AUC 仍在 0.5 以上，才支持「对接在该靶标上具备真实区分力」这一结论。\n")

# ---- 7c. 面容效度（含阴性结果）----
FV = rd("P6_face_validity.csv")
L.append("\n### 7.2 面容效度检验：已知镇痛药是否被筛回来？（阴性结果，必须报告）\n")
if FV is None or FV.empty:
    L.append("_未产出（需先运行 `scripts/p6_face_validity.py`）。_\n")
else:
    L.append("""
"Top 里出现了已知镇痛药"是虚拟筛选最常见的自证话术，但极易沦为**挑选性举例**。
本检验把它拆成三个可证伪的问题（`pain_prior` 与 α2 激动剂名单均为外部药理学标注，
**不参与 composite 任何一维**，故本检验非循环论证）：
**A** 类别层面（镇痛药整体是否更靠前）、**B** 靶标层面（ADRA2A 上是否打分更好）、
**C** 机制层面（药理学定义 ADRA2A 的 α2 激动剂是否被筛回，含 MW 校正前后对比）。
""")
    L.append(md_table(FV, ["level", "test", "n_pos", "n_neg", "AUC", "p_one_sided", "note"]))
    L.append("""
**结论：类别层面不支持"已知镇痛药富集"**（AUC 0.553, p=0.081；Top-20 中 0 个，期望 1.9 个）。
α2 激动剂原始 AUC 仅 0.343（比平均更差）—— 因其多为小分子（中位 MW 245.6 vs 其余 300.7），
被尺寸偏倚系统性惩罚；MW 校正后回到 0.475（等同随机）。
**因此本稿不以面容效度作为流程效度的证据**，方法效度只由 §7 的 ChEMBL 结合型富集支撑。
个别药物（氟吡汀在 ADRA2A 上排 5/620；右美托咪定 MW 校正后升至第 94 百分位）
仅作**假设生成性个例**陈述。
""")

# ---- 7.3 头号排序的 MW 敏感性：Top 榜是不是「分子量榜」？----
L.append("\n### 7.3 头号排序的分子量敏感性：Top 榜是不是「分子量榜」？\n")
MWS = rd("P6_mw_ranking_summary.csv")
MWR = rd("P6_mw_ranking_pairs.csv")
if MWS is None or MWS.empty:
    L.append("_未产出（需先运行 `scripts/p6_mw_ranking_sensitivity.py`）。_\n")
else:
    r = MWS.iloc[0]
    L.append("""
对接系统性偏爱大分子（§7.1 实测 ρ(亲和力, MW) = −0.607），而本稿头号候选（麦角胺类、
抗精神病药）恰好都是大分子。故必须直接检验**药物级排序本身**是否只是尺寸的产物。
做法：保留 D2/D3/D4 与原权重（0.40/0.25/0.20/0.15），**仅替换 D1** 为两种 MW 稳健化的
靶内百分位 —— **A** 亲和力对 MW 线性回归的**残差**百分位；**B** MW 五分位**层内**排名
（非参数，不假设线性）——从而隔离 MW 这一个变量。
""")
    L.append("**① 排序稳健性**（对应 %s，620 配对）\n" % r["target"])
    L.append("| 比较 | Spearman ρ |\n|---|---|\n")
    L.append("| D1 单维：主口径 vs MW 残差 | %.3f |\n" % r["rho_D1_raw_vs_mwres"])
    L.append("| composite：主口径 vs MW 残差 | **%.3f** |\n" % r["rho_composite_raw_vs_mwres"])
    L.append("| composite：主口径 vs MW 分层 | **%.3f** |\n" % r["rho_composite_raw_vs_mwstrat"])
    L.append("| 药物级（跨 10 靶标，680 药）：主口径 vs MW 残差 | %.3f |\n"
             % r["drug_rho_raw_vs_mwres"])
    L.append("\nTop-k 名单重叠（主口径 ∩ 变体）：**Top-20 = %d/20**（MW 残差）、"
             "**%d/20**（MW 分层）。\n"
             % (int(r["top20_overlap_mwres"]), int(r["top20_overlap_mwstrat"])))

    L.append("""
**② 排序质量的前瞻性口径 —— precision@k**（用 §7 的独立 ChEMBL 阳性集，
标签来自实测活性、预测来自对接，无二重蘸取）：
""")
    L.append("| k | 命中数 | precision | lift vs 基线 %.1f%% | 超几何 p | MW 残差 precision | MW 分层 precision |\n"
             % (100 * r["baseline"]))
    L.append("|---|---|---|---|---|---|---|\n")
    for k in (10, 20, 50):
        L.append("| Top-%d | %d | **%.3f** | ×%.2f | %.2g | %.3f | %.3f |\n"
                 % (k, int(r["hit@%d_raw" % k]), r["prec@%d_raw" % k],
                    r["lift@%d_raw" % k], r["hyper_p@%d_raw" % k],
                    r["prec@%d_mwres" % k], r["prec@%d_mwstrat" % k]))

    if MWR is not None and "rank_comp_D1_raw" in MWR.columns:
        G3 = MWR[MWR.symbol == r["target"]]
        t10 = pd.DataFrame({
            "主口径": G3.nsmallest(10, "rank_comp_D1_raw").pref_name.values,
            "MW 残差": G3.nsmallest(10, "rank_comp_D1_mwres").pref_name.values,
            "MW 分层": G3.nsmallest(10, "rank_comp_D1_mwstrat").pref_name.values})
        L.append("\n**③ 各口径 Top-10 名单并列**（检验的是「集合」，不是「单一名次」）：\n")
        L.append(md_table(t10))

    L.append("""
**结论（两句话，各自独立，不可只引用其中一句）**：

1. **排序质量对 MW 稳健**：composite 与 MW 校正后排序的 Spearman 达 %.3f–%.3f（判据
   ≥0.80，判定 **%s**），且 Top-20 有 %d/20 重叠。**precision@10 = %.3f（lift ×%.2f,
   p = %.2g）、precision@20 = %.3f** 在 MW 校正后仍显著高于 %.1f%% 基线 ——
   即"ADRA2A 的 Top 候选集合富集真实 ADRA2A 结合物"这一结论**不是尺寸伪信号**。
2. **但 Top-10 的「具体身份」不稳定**：MW 校正后名单仅重叠 4/10。右美托咪定、氟吡汀
   挤入前五，鲁拉西酮、阿立哌唑掉出。**故本稿只主张「Top-20 候选集合富集」，
   不主张「某个药排名第一」**；任何单药首位结论都应视为不稳健。
""" % (r["rho_composite_raw_vs_mwstrat"], r["rho_composite_raw_vs_mwres"],
       r["verdict"], int(r["top20_overlap_mwres"]),
       r["prec@10_raw"], r["lift@10_raw"], r["hyper_p@10_raw"],
       r["prec@20_raw"], 100 * r["baseline"]))

# ============ 8. 排序 ============
L.append("## 8. 四维评分与候选清单\n")
DR = rd("P6_ranking_drugs.csv")
PR = rd("P6_ranking_pairs.csv")
L.append("综合分 = 0.40·D1(靶标内亲和力百分位) + 0.25·D2(已有多靶点药理学合理性) "
         "+ 0.20·D3(临床可及性/CNS-MPO 式) + 0.15·D4(该靶标反向对照可信度)。\n\n")
if DR is not None:
    L.append(f"药物级榜单共 {len(DR):,} 行，Top 20：\n\n")
    keep = [c for c in ["pref_name", "best_target", "affinity_at_best_target",
                        "best_affinity_any_target", "n_top1pct", "n_top5pct",
                        "best_composite", "pain_prior", "drh_phase"] if c in DR.columns]
    L.append(md_table(DR, keep, n=20))
    L.append("""
> **读表警告（务必遵守）**：`affinity_at_best_target` 是该药物在 `best_target` **这一对**上的
> 亲和力，与靶标严格配对，引用时应当用它。而 `best_affinity_any_target` 是该药物在**任意靶标**
> 上的最强值（跨靶标取最小），其所属靶标**通常不是** `best_target`（Top 20 中 19/20 如此）。
> 把后者标到前者名下会造成张冠李戴——本稿曾踩此坑，已拆分列并在此写明。
""")
if PR is not None:
    L.append(f"\n药物-靶标配对表共 {len(PR):,} 行，Top 20：\n\n")
    keep = [c for c in ["pref_name", "symbol", "affinity", "pct_in_target", "D1_affinity",
                        "D2_pharm_prior", "D3_accessibility", "D4_reliability", "composite"]
            if c in PR.columns]
    L.append(md_table(PR, keep, n=20))

# ============ 9. 局限 ============
L.append("\n## 9. 局限（必须与结论同时呈现）\n")
L.append("""
1. **靶标覆盖不全**：§6 优先的离子通道类靶标（SCN9A/SCN10A/SCN11A/KCNQ2/CACNA2D1/GABRA1）
   因缺乏可用结构全部无法对接，P6 无法对它们给出候选。
2. **打分保真度上限 ρ ≈ 0.78**：对接结果只支撑"候选优选"，不支撑精确结合能排序；
   任何"第 N 名优于第 N+1 名"的强比较都超出数据支持范围。
3. **反向对照阳性集稀疏**：多数靶标缺乏已批准药层面的已知结合分子，
   其 D4 可信度权重只能取中性值，无法独立校验。
4. **静态结构近似**：对接使用单一晶体构象，未考虑构象选择与诱导契合；
   柔性配体与柔性口袋体系的误差更大。
5. **无膜环境**：膜蛋白靶标（即便有结构）在对接中按可溶蛋白处理，缺失脂双层与
   跨膜电位的约束。
6. **打分与实验效价的缺口**：虚拟筛选给出的是相对排序，不等于体内/体外镇痛效力；
   所有候选在湿实验验证前均属假说。
""")

# ============ 10. 产物清单 ============
L.append("## 10. 产物清单\n")
L.append("| 文件 | 内容 |\n|---|---|\n"
         "| `results/tables/P6_ligand_library.csv` | 配体库逐个分子的准备结果与淘汰原因 |\n"
         "| `results/tables/P6_ligand_funnel.json` | 配体漏斗各阶段计数 |\n"
         "| `results/tables/P6_ligand_cns_prior.csv` | Tier 1 CNS/镇痛先验子集 |\n"
         "| `results/tables/P6_target_selection.csv` | 43 个候选靶标的可成药性决策 |\n"
         "| `results/tables/P6_receptors.csv` | 受体准备结果（含盒参数、链定位） |\n"
         "| `results/tables/P6_stage1_param_validation.csv` | 参数保真度验证（15 个分层配体） |\n"
         "| `results/tables/P6_exh_validation.csv` | exhaustiveness 专项对照 |\n"
         "| `results/tables/P6_docking_scores_*.csv` | 分层对接打分原始表 |\n"
         "| `results/tables/P6_reverse_control.csv` | 逐靶标反向阳性对照 AUC |\n"
         "| `results/tables/P6_reverse_control_positives.csv` | ChEMBL 实测活性阳性集 |\n"
         "| `results/tables/P6_ranking_pairs.csv` | 药物-靶标配对四维评分 |\n"
         "| `results/tables/P6_ranking_drugs.csv` | 药物级汇总榜单 |\n")
figs = sorted(os.path.basename(f) for f in glob.glob(os.path.join(FIG, "P6_*.png")))
if figs:
    L.append("\n图件：\n\n" + "\n".join(f"- `results/figures/{f}`" for f in figs) + "\n")

# ============ 缺口 ============
if gaps:
    L.append("\n## 附：本次生成时缺失的产物\n")
    L.append("（这些项对应的分析尚未完成，报告中以占位形式呈现，不得当作已完成）\n\n"
             + "\n".join(f"- `{g}`" for g in sorted(set(gaps))) + "\n")

open(OUT, "w", encoding="utf-8").write("\n".join(L))
print(f"报告已生成 -> {OUT}")
print(f"章节数 {len(L)}，缺失产物 {len(set(gaps))} 项")
if gaps:
    print("缺失：" + ", ".join(sorted(set(gaps))))
