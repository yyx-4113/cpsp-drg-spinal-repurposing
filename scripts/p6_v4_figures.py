# -*- coding: utf-8 -*-
"""生成 P6 标书所需图件（V4 建立，V5/V6 沿用并同步更新）：
  Fig0 技术路线图（双色：已完成 / 拟开展）
  Fig1 ADRA2A 跨 6 对比效应森林图
  Fig2 35-hub 留一数据集（LODO）泛化 AUC
  Fig3 人源可译性证据矩阵（35-hub 四层 + 4055 核心签名层 + 细胞相关性）
所有数值在运行时从 results/ 产物文件读取，不硬编码（Fig2/Fig3 的统计量来自 P3/P4 结果 md，
以常量表形式集中声明并标注出处行）。

版本同步记录：
  - V5：主模型由足底切口痛改为 SMIR → 同步 Fig0 措辞。
  - V6：V5 新增的「人源 4055 核心签名层」结果补入 Fig3（消除图文不一致）。
"""
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TAB = os.path.join(BASE, "results", "tables")
OUT = os.path.join(BASE, "results", "figures")
os.makedirs(OUT, exist_ok=True)

plt.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
plt.rcParams["savefig.dpi"] = 200
plt.rcParams["figure.facecolor"] = "white"

RED = "#C0392B"      # 上调（中国习惯：红涨）
GREEN = "#1E8449"    # 下调
BLUE = "#1F4E79"
ORANGE = "#B9770E"
GREY = "#5D6D7E"

# ---------------------------------------------------------------- Fig 0 技术路线图
def fig0():
    fig, ax = plt.subplots(figsize=(11.5, 9.6))
    ax.set_xlim(0, 100); ax.set_ylim(0, 110); ax.axis("off")

    def box(x, y, w, h, text, fc, ec, fs=9.3, bold=False, lw=1.3):
        ax.add_patch(FancyBboxPatch((x, y - h / 2), w, h,
                                    boxstyle="round,pad=0.5,rounding_size=1.4",
                                    linewidth=lw, facecolor=fc, edgecolor=ec))
        ax.text(x + w / 2, y, text, ha="center", va="center", fontsize=fs,
                color="#20303F", fontweight="bold" if bold else "normal", linespacing=1.55)

    def arrow(x1, y1, x2, y2, color=GREY, ls="-", lw=1.5):
        ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="-|>",
                                     mutation_scale=13, linewidth=lw, color=color,
                                     linestyle=ls, shrinkA=0, shrinkB=0))

    FC_D = "#EAF2FA"; EC_D = BLUE
    FC_P = "#FDF3E7"; EC_P = ORANGE

    # 阶段横幅
    box(2, 106, 96, 5.2, "第一阶段（申报前已完成）　计算锁靶 —— 计算假说生成",
        "#D6E4F0", BLUE, fs=11.8, bold=True)
    box(2, 38, 96, 4.8, "第二阶段（本项目拟开展）　体内验证 —— 假说检验与范式闭环",
        "#FCE9D6", ORANGE, fs=11.8, bold=True)

    # 已完成链（左列）
    x1, w1 = 3, 43
    x2, w2 = 54, 43
    ys = [96, 84, 72, 60]
    t1 = ["8 套 GEO 多组学数据集\n（bulk RNA-seq / snRNA-seq / 血浆 miRNA）",
          "DRG 轴 Stouffer 元分析\n5 套 · 6 对比 → 4055 基因核心签名\n（切口模型同向 59.9%，p = 2.8e-48）",
          "双机器学习锁靶\nLASSO + RF + SHAP → 35 个 hub 基因程序\n（留一数据集 AUC 0.917–1.000）",
          "全库药物重定位虚拟筛选\n已批准药物库 3,085 个配体 × 10 个靶标\n完成 30,850 次分子对接"]
    t2 = ["4 层人源可译性评估（分层结论，如实报告）\nGSE249746 强阳性 / GSE107181 弱 /\nSPARC476 未复制 / Pennsieve480 非神经元趋势",
          "空间与细胞归属定位\nGSE325938（小鼠脊髓 Visium）35/35 定位成功\n背角 17 · 脑膜纤维 11 · 腹角 4 · 其它 3",
          "靶点取舍分析\nAXL / TNIK 均缺乏已上市镇痛药物\nADRA2A 具备三重可转化条件",
          "形成优先假说：ADRA2A\n核心签名成员（方向一致性 100%，6/6）\nmeta_Z = 4.84，meta_FDR = 1.5e-5"]
    for y, ta, tb in zip(ys, t1, t2):
        box(x1, y, w1, 10.6, ta, FC_D, EC_D)
        box(x2, y, w2, 10.6, tb, FC_D, EC_D)
    for i in range(len(ys) - 1):
        arrow(x1 + w1 / 2, ys[i] - 5.3, x1 + w1 / 2, ys[i + 1] + 5.5, color=EC_D)
        arrow(x2 + w2 / 2, ys[i] - 5.3, x2 + w2 / 2, ys[i + 1] + 5.5, color=EC_D)
    arrow(x1 + w1 + 1, ys[0], x2 - 1, ys[0], color=EC_D)

    # 收口 → 假说
    box(23, 48, 54, 8.4,
        "优先假说：CPSP 中 ADRA2A（α2A 肾上腺素能受体）及其所属 DRG–脊髓轴分子程序的\n表达水平与细胞归属发生改变，构成可靶向的干预出口",
        "#FFF6CC", "#B7950B", fs=10, bold=True, lw=1.6)
    arrow(x1 + w1 / 2, 54.7, x1 + w1 / 2, 52.4, color=GREY)
    arrow(x2 + w2 / 2, 54.7, x2 + w2 / 2, 52.4, color=GREY)
    arrow(50, 43.6, 50, 40.6, color=GREY)

    # 拟开展：研究内容一 / 二
    box(3, 27.5, 43, 11.4,
        "研究内容一　表达定位与细胞归属\nC57BL/6J 雄鼠 · SMIR（主）/ SNI（辅）模型\nqPCR + IHC/WB + 神经元–非神经元分选\n时间点 d3 / d7 / d14 / d28，n = 8–10/组",
        FC_P, EC_P)
    box(54, 27.5, 43, 11.4,
        "研究内容二　体内功能药理验证\n右美托咪定 / 可乐定 · 鞘内 + 系统给药\n3–4 点剂量–反应 → 亚最大有效剂量\natipamezole / BRL-44408 特异性阻断",
        FC_P, EC_P)
    arrow(46.6, 27.5, 53.4, 27.5, color=EC_P)
    arrow(24.5, 35.6, 24.5, 33.4, color=GREY)
    arrow(75.5, 35.6, 75.5, 33.4, color=GREY)

    # 判读出口
    box(3, 15, 20, 8.6, "判读 A\nADRA2A 上调主要发生在\n伤害感受神经元", "#F2F3F4", GREY, fs=8.6)
    box(25, 15, 21, 8.6, "判读 B\n主要发生在非神经元/\n基质（呼应人 DRG 趋势）", "#F2F3F4", GREY, fs=8.6)
    box(54, 15, 43, 8.6, "判读 C\n镇痛效应可被 α2A 选择性拮抗剂阻断\n→ 支持 ADRA2A 为可成药干预出口（预防 + 逆转双场景）",
        "#F2F3F4", GREY, fs=8.6)
    arrow(12, 21.5, 12, 19.5, color=GREY)
    arrow(35, 21.5, 35, 19.5, color=GREY)
    arrow(75.5, 21.5, 75.5, 19.5, color=GREY)

    # 研究内容三
    box(16, 5, 68, 7.2,
        "研究内容三　方法学闭环与资源整合\n结论反哺计算框架，输出“计算锁靶 → 表达定位 → 功能验证”可复用流程与候选靶点优先级资源",
        FC_P, EC_P, fs=9)
    arrow(12, 10.6, 24, 8.8, color=GREY, ls=":")
    arrow(35, 10.6, 42, 8.8, color=GREY, ls=":")
    arrow(75.5, 10.6, 68, 8.8, color=GREY, ls=":")

    fig.savefig(os.path.join(OUT, "P6_Fig0_technical_route.png"), bbox_inches="tight")
    plt.close(fig)
    print("Fig0 ok")


# ---------------------------------------------------------------- Fig 1 森林图
LABELS = {
    "lfc_GSE267799_SMIR_DRG": "GSE267799　大鼠 DRG　切口模型\n（chronic vs baseline）",
    "lfc_GSE212311_CCI_DRG": "GSE212311　大鼠 DRG　CCI",
    "lfc_GSE278227_CCI_DRG": "GSE278227　CCI 1W（IL vs CL）",
    "lfc_GSE241361_S1R_DRG": "GSE241361　小鼠 DRG　SNI（WT）",
    "lfc_GSE265957_Xtail_DRG_Day4": "GSE265957　DRG　术后 D4",
    "lfc_GSE265957_Xtail_DRG_Day63": "GSE265957　DRG　术后 D63",
}


def fig1():
    df = pd.read_csv(os.path.join(TAB, "META_DRG_axis_stouffer.csv"))
    row = df[df["symbol"].astype(str).str.upper() == "ADRA2A"].iloc[0]
    cols = list(LABELS.keys())
    vals = [float(row[c]) for c in cols]
    order = np.argsort(vals)
    vals = [vals[i] for i in order]
    labs = [LABELS[cols[i]] for i in order]

    fig, ax = plt.subplots(figsize=(9.6, 5.2))
    y = np.arange(len(vals))
    ax.hlines(y, 0, vals, color=RED, linewidth=2.4, alpha=0.75)
    ax.plot(vals, y, "o", color=RED, markersize=8, zorder=3)
    for yi, v in zip(y, vals):
        ax.text(v + 0.012, yi, f"{v:+.3f}", va="center", fontsize=9.2, color="#20303F")
    ax.axvline(0, color="#7F8C8D", linewidth=1.1, linestyle="--")
    ax.set_yticks(y); ax.set_yticklabels(labs, fontsize=8.8)
    ax.set_xlabel("各数据集 Welch-t 导出的 log2 倍数变化（ADRA2A）", fontsize=10)
    ax.set_xlim(-0.04, max(vals) * 1.28)
    ax.set_title("图 1　ADRA2A 在 DRG 轴 Stouffer 元分析全部 6 个对比中方向一致（6/6 同向）\n"
                 f"meta_Z = {float(row['meta_Z']):.2f}　meta_FDR = {float(row['meta_FDR']):.2e}　"
                 f"方向一致性 consistency = {float(row['consistency']):.2f}（K = {int(row['K'])}）",
                 fontsize=10.5, fontweight="bold", color=BLUE, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", linestyle=":", alpha=0.4)
    fig.text(0.5, -0.02,
             "数据来源：results/tables/META_DRG_axis_stouffer.csv（ADRA2A 行，K=6、n_up=6、n_dn=0、"
             "concordant_incision=True）；红色 = 上调方向。",
             ha="center", fontsize=7.8, color=GREY)
    fig.savefig(os.path.join(OUT, "P6_Fig1_ADRA2A_forest.png"), bbox_inches="tight")
    plt.close(fig)
    print("Fig1 ok")


# ---------------------------------------------------------------- Fig 2 LODO AUC
LODO = [
    ("GSE278227　CCI 大鼠 DRG", 1.000, 1.000, 1.000, 28, "训练信号最强"),
    ("GSE267799　切口 大鼠 DRG", 0.917, 0.729, 1.000, 20, "完全不同模型\n且训练时被排除"),
    ("GSE241361　小鼠 DRG", 1.000, 1.000, 1.000, 9, "跨物种"),
    ("GSE241361　小鼠脊髓", 0.950, 0.709, 1.000, 9, "跨组织"),
    ("GSE212311　CCI 大鼠 DRG", 1.000, 1.000, 1.000, 6, "n 极小"),
]


def fig2():
    fig, ax = plt.subplots(figsize=(9.6, 4.4))
    y = np.arange(len(LODO))[::-1]
    for yi, (name, auc, lo, hi, n, note) in zip(y, LODO):
        ax.hlines(yi, lo, hi, color=BLUE, linewidth=2.6, alpha=0.55)
        ax.plot([auc], [yi], "o", color=BLUE, markersize=9, zorder=3)
        ax.text(1.015, yi, f"AUC {auc:.3f}  [{lo:.3f}, {hi:.3f}]　n={n}", va="center",
                fontsize=8.8, color="#20303F", transform=ax.get_yaxis_transform())
        ax.text(0.475, yi + 0.32, note, va="center", fontsize=7.8, color=GREY, style="italic")
    ax.axvline(0.5, color="#7F8C8D", linestyle="--", linewidth=1.1)
    ax.text(0.512, -0.52, "随机水平 0.5", fontsize=8, color=GREY)
    ax.set_yticks(y); ax.set_yticklabels([x[0] for x in LODO], fontsize=9)
    ax.set_xlim(0.45, 1.02); ax.set_ylim(-0.9, len(LODO) - 0.4)
    ax.set_xlabel("留一数据集（LODO）泛化 AUC（35-hub 签名，95% CI）", fontsize=10)
    ax.set_title("图 2　35-hub 签名的留一数据集泛化性能\n"
                 "合并 5×20 重复分层 CV AUC = 0.999 ± 0.004；标签置换零假设 AUC = 0.490 ± 0.085",
                 fontsize=10.5, fontweight="bold", color=BLUE, pad=12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="x", linestyle=":", alpha=0.4)
    fig.text(0.5, -0.05,
             "数据来源：results/P3_RESULTS.md §3（results/tables/P3_lodo_auc_ci.csv）。"
             "局限：AUC≈1.0 部分源于各模型共享的强损伤签名；GSE241361 的 DRG 与脊髓取自同一批动物，LODO 非完全独立。",
             ha="center", fontsize=7.6, color=GREY)
    fig.savefig(os.path.join(OUT, "P6_Fig2_hub_LODO_AUC.png"), bbox_inches="tight")
    plt.close(fig)
    print("Fig2 ok")


# ---------------------------------------------------------------- Fig 3 人源四层
HUMAN = [
    ("GSE249746\n人 DRG 单细胞图谱", "35 hub + ADRA2A 全检出", "26/35 峰值落\n伤害感受样神经元簇\nADRA2A → 簇 C14（ρ=+0.12）", "强阳性"),
    ("GSE107181\n人 iPS-DRG 发育对比", "33 hub 可评估", "18/33 神经元上调\n二项检验 p = 0.73", "弱（NS）"),
    ("SPARC 476\n人 C2-DRG Visium（n=8）", "34 hub 可映射", "set-mean t = 0.236\n置换 p = 0.765", "未复制"),
    ("Pennsieve 480\n人 DRG snRNA-seq（40 供体）", "33 hub 可映射", "set-mean t = 0.480（p=0.109）\n与神经元标记 ρ = −0.473（p=0.002）", "非神经元趋势"),
]
TAG_COLOR = {"强阳性": RED, "弱（NS）": "#B7950B", "未复制": GREEN, "非神经元趋势": ORANGE}

# 4055 核心签名层（ADRA2A 即其中成员）：V5 正文补入，V6 在图 3 中一并呈现
# 数值来源：results/tables/P4_SPARC476_geneset_test.csv、results/tables/P4b_Pennsieve480_geneset_test.csv
CORE_SIG = [
    ("SPARC 476（人 DRG Visium）", "3,921", "2,167 (55.3%)", "4.5e-11", "0.846 (NS)"),
    ("Pennsieve 480（人 DRG snRNA）", "3,839", "2,212 (57.6%)", "3.6e-21", "0.174 (NS)"),
]


def fig3():
    fig = plt.figure(figsize=(10.6, 8.0))
    gs = fig.add_gridspec(3, 1, height_ratios=[2.05, 1.05, 1.00], hspace=0.30)

    # ---------------- panel A：35-hub 四层
    ax = fig.add_subplot(gs[0]); ax.axis("off")
    ax.set_xlim(0, 100); ax.set_ylim(0, 100)
    ax.text(50, 100, "图 3　人源可译性证据矩阵（分层、混合结论，如实报告）",
            ha="center", va="top", fontsize=10.8, fontweight="bold", color=BLUE)
    ax.text(50, 91.0, "A　35-hub 分子程序在四层人源数据中的可译性",
            ha="center", va="top", fontsize=9.3, fontweight="bold", color="#20303F")
    hdr = ["人源数据集", "hub 覆盖", "关键统计量", "判读"]
    xs = [2, 34, 52, 88]; ws = [31, 17, 35, 12]
    hdr_bottom, hdr_h, row_h = 73, 8, 16.5
    for x, w, h in zip(xs, ws, hdr):
        ax.add_patch(FancyBboxPatch((x, hdr_bottom), w, hdr_h,
                                    boxstyle="round,pad=0.3,rounding_size=1.2",
                                    facecolor="#D6E4F0", edgecolor=BLUE, linewidth=1))
        ax.text(x + w / 2, hdr_bottom + hdr_h / 2, h, ha="center", va="center",
                fontsize=9.2, fontweight="bold", color=BLUE)
    for i, (ds, cov, stat, tag) in enumerate(HUMAN):
        y0 = hdr_bottom - row_h * (i + 1)
        bh = row_h - 1.4
        for x, w, t in zip(xs, ws, [ds, cov, stat, ""]):
            fc = "#FFFFFF" if i % 2 == 0 else "#F7F9FB"
            ax.add_patch(FancyBboxPatch((x, y0), w, bh,
                                        boxstyle="round,pad=0.3,rounding_size=1.2",
                                        facecolor=fc, edgecolor="#C8D2DC", linewidth=0.9))
            if t:
                ax.text(x + w / 2, y0 + bh / 2, t, ha="center", va="center",
                        fontsize=8.2, color="#20303F", linespacing=1.4)
        ax.text(xs[3] + ws[3] / 2, y0 + bh / 2, tag, ha="center", va="center",
                fontsize=8.8, fontweight="bold", color=TAG_COLOR[tag])
    ax.set_xlim(0, 100); ax.set_ylim(0, 100); ax.set_autoscale_on(False)

    # ---------------- panel B：4055 核心签名层
    axb = fig.add_subplot(gs[1]); axb.axis("off")
    axb.text(50, 100, "B　同层面的 4055 核心签名（ADRA2A 即其成员）：方向一致性层面已复制、集合均值层面未复制",
             ha="center", va="top", fontsize=9.0, fontweight="bold", color=BLUE)
    hdrb = ["数据集", "可映射", "方向为正", "二项检验 p\n方向一致性", "均值置换 p\n效应量"]
    xsb = [2, 34, 47, 62, 82]; wsb = [31, 12, 14, 19, 16]
    hdrb_bottom, hdrb_h, rowb_h = 66, 20, 20
    for x, w, h in zip(xsb, wsb, hdrb):
        axb.add_patch(FancyBboxPatch((x, hdrb_bottom), w, hdrb_h,
                                     boxstyle="round,pad=0.3,rounding_size=1.2",
                                     facecolor="#D6E4F0", edgecolor=BLUE, linewidth=1))
        axb.text(x + w / 2, hdrb_bottom + hdrb_h / 2, h, ha="center", va="center",
                 fontsize=8.3, fontweight="bold", color=BLUE, linespacing=1.3)
    for i, (ds, nmap, pos, binp, permp) in enumerate(CORE_SIG):
        y0 = hdrb_bottom - rowb_h * (i + 1)
        bh = rowb_h - 1.6
        for x, w, t in zip(xsb, wsb, [ds, nmap, pos, binp, permp]):
            fc = "#FFFFFF" if i % 2 == 0 else "#F7F9FB"
            axb.add_patch(FancyBboxPatch((x, y0), w, bh,
                                         boxstyle="round,pad=0.3,rounding_size=1.2",
                                         facecolor=fc, edgecolor="#C8D2DC", linewidth=0.9))
            strong = (x == xsb[3])
            axb.text(x + w / 2, y0 + bh / 2, t, ha="center", va="center",
                     fontsize=8.0, color=(RED if strong else "#20303F"),
                     fontweight="bold" if strong else "normal", linespacing=1.35)
    axb.text(50, 13, "读法（与小鼠切口模型用同一把尺子）：广谱、低幅度、方向高度一致的偏移——"
                     "方向一致性极显著，而集合均值效应量不显著。",
             ha="center", va="center", fontsize=8.0, color=GREY)
    axb.set_xlim(0, 100); axb.set_ylim(0, 100); axb.set_autoscale_on(False)

    # ---------------- panel C：细胞类型相关性
    ax2 = fig.add_subplot(gs[2])
    labs = ["与神经元标记\n（ρ = −0.473, p = 0.002）", "与成纤维/基质标记\n（ρ = +0.399, p = 0.011）"]
    vals = [-0.4732, 0.399]
    cols = [BLUE, RED]
    bars = ax2.barh([1, 0], vals, color=cols, height=0.5, alpha=0.85)
    ax2.axvline(0, color="#7F8C8D", linewidth=1.1)
    for b, v in zip(bars, vals):
        ax2.text(v + (0.03 if v > 0 else -0.03), b.get_y() + b.get_height() / 2,
                 f"{v:+.3f}", va="center", ha="left" if v > 0 else "right",
                 fontsize=9.2, color="#20303F")
    ax2.set_yticks([1, 0]); ax2.set_yticklabels(labs, fontsize=8.8)
    ax2.set_xlim(-0.62, 0.62)
    ax2.set_xlabel("C　Pennsieve 480（人 DRG snRNA-seq, 40 供体）：35-hub 程序均值与细胞类型标记的相关性（Spearman ρ）",
                   fontsize=8.8)
    ax2.spines[["top", "right"]].set_visible(False)
    ax2.grid(axis="x", linestyle=":", alpha=0.4)
    fig.text(0.5, 0.005,
             "数据来源：results/P4_HUMAN_REANALYSIS_RESULTS.md、P4_SPARC476_results.md、"
             "P4b_Pennsieve480_results.md 及其对应的 tables/*_geneset_test.csv。"
             "各层结论互不一致，提示人源可译性分层依赖，不构成对动物水平验证的替代。",
             ha="center", fontsize=7.6, color=GREY)
    fig.savefig(os.path.join(OUT, "P6_Fig3_human_translatability.png"), bbox_inches="tight")
    plt.close(fig)
    print("Fig3 ok")


if __name__ == "__main__":
    fig0(); fig1(); fig2(); fig3()
    print("OUT =", OUT)
