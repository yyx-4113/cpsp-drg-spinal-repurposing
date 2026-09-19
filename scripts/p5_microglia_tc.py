#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p5_microglia_tc.py -- GSE246288 脊髓 Cd11b+ 小胶质 hub 基因时间序列（描述性）

为什么必须单独处理本数据集：
  GSE246288 是 **Cd11b+ FACS 分选** 的脊髓背角（SCDH, L4-L6）细胞，只含小胶质/巨噬细胞。
  但 p5_sc.py 的无监督聚类在本集里还"找到"了 Neuron / Oligodendrocyte / OPC / Pericyte /
  Ependymal / Astrocyte 等簇——这是 **ambient RNA 造的伪簇**（本集 HVG top 是
  S100A8 / S100A9 / RETNLG / MKI67 / TOP2A / HIST1H1B，纯髓系+增殖特征；且这些"其它细胞"
  的 marker 得分 margin 普遍 < 0.5）。因此本集的**跨细胞类型定位结论全部作废**，
  只能做一件事：**小胶质内部的表达与时间趋势**。

采样设计：SA = Sham，PID 0；3A / 7A / 14A = SNI，PID 3 / 7 / 14。每时间点 **n = 1 只**，
所以本表**只报告描述性数值（不做任何检验）**——n=1 无法给出统计推断，这是伪重复的反面：
不是重复被夸大，而是根本不存在重复。

输出：results/tables/P5_GSE246288_microglia_timecourse.csv
用法：python p5_microglia_tc.py
"""
import os
import numpy as np, pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")

pb = pd.read_csv(os.path.join(TAB, "P5_GSE246288_SC_pseudobulk_celltype.csv"))
hub = pd.read_csv(os.path.join(TAB, "P3_hub_genes.csv"))
hub["symbol"] = hub["symbol"].str.upper()
nm = dict(zip(hub.symbol, hub.n_methods))
hubs = [g for g in hub.symbol.tolist() if g in pb.columns]

mg = pb[pb.celltype == "Microglia"].copy()
mg["tp"] = mg["sample"].astype(str).str.replace("GSM7866244_SA", "PID0", regex=False) \
    .str.replace("GSM7866245_3A", "PID3", regex=False) \
    .str.replace("GSM7866246_7A", "PID7", regex=False) \
    .str.replace("GSM7866247_14A", "PID14", regex=False)
order = ["PID0", "PID3", "PID7", "PID14"]
mg = mg.set_index("tp").reindex(order)

ncells = mg["n_cells"].to_dict()
print("Microglia+ n_cells by timepoint:", {k: int(v) for k, v in ncells.items()}, "| each timepoint = 1 mouse")

M = mg[hubs].T
M.columns = [f"{c}_mean_lognorm" for c in order]
df = M.reset_index().rename(columns={"index": "symbol"})
df["n_methods"] = df.symbol.map(nm)
df["n_cells_PID0"], df["n_cells_PID3"] = int(ncells["PID0"]), int(ncells["PID3"])
df["n_cells_PID7"], df["n_cells_PID14"] = int(ncells["PID7"]), int(ncells["PID14"])
df["delta_PID0_to_14"] = df.PID14_mean_lognorm - df.PID0_mean_lognorm
df["detected_any"] = (df[[f"{t}_mean_lognorm" for t in order]].max(axis=1) > 0.05)

# 单调性：Spearman 秩相关（仅描述趋势强度，不做 p 值推断——4 个时间点、每点 n=1 只）
# 直接实现（rank -> Pearson），避免 scipy 版本间 spearmanr 的 numpy 兼容问题
def _spearman(x, y):
    x, y = np.asarray(x, float), np.asarray(y, float)
    rx = pd.Series(x).rank().to_numpy()
    ry = pd.Series(y).rank().to_numpy()
    rx, ry = rx - rx.mean(), ry - ry.mean()
    d = np.sqrt((rx ** 2).sum() * (ry ** 2).sum())
    return float((rx * ry).sum() / d) if d > 0 else np.nan

xs = np.arange(4)
df["spearman_rho_trend"] = [float(_spearman(xs, r[[f"{t}_mean_lognorm" for t in order]].to_numpy(float)))
                            for _, r in df.iterrows()]
df["trend"] = np.where(~df.detected_any, "not_detected",
                       np.where(df.delta_PID0_to_14 > 0.10, "up",
                                np.where(df.delta_PID0_to_14 < -0.10, "down", "flat")))
df = df.sort_values(["n_methods", "delta_PID0_to_14"], ascending=[False, False])
cols = (["symbol", "n_methods", "detected_any", "trend", "delta_PID0_to_14", "spearman_rho_trend"]
        + [f"{t}_mean_lognorm" for t in order]
        + ["n_cells_PID0", "n_cells_PID3", "n_cells_PID7", "n_cells_PID14"])
df[cols].to_csv(os.path.join(TAB, "P5_GSE246288_microglia_timecourse.csv"), index=False)

det = df[df.detected_any]
print(f"\nhub 基因在脊髓小胶质中可检出: {len(det)}/{len(df)}")
print("时间趋势 counts:", det.trend.value_counts().to_dict())
print("\n上调最明显的 12 个（PID14 - PID0）:")
print(det.head(12)[["symbol", "n_methods", "delta_PID0_to_14", "spearman_rho_trend",
                    "PID0_mean_lognorm", "PID3_mean_lognorm", "PID7_mean_lognorm",
                    "PID14_mean_lognorm", "trend"]].to_string(index=False, float_format=lambda v: f"{v:.3f}"))
print("\n表 -> results/tables/P5_GSE246288_microglia_timecourse.csv")
