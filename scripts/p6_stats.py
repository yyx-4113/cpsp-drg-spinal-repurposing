# -*- coding: utf-8 -*-
"""
p6_stats.py —— P6 的**唯一**统计口径模块（富集检验 / 尺寸控制 / 裁决）

【为什么要单独抽出来】
同一批数字（对接 AUC、仅 MW 基线、MW 校正后 AUC）在 `p6_mw_confounder.py` 与
`p6_breadth.py` 里**各写了一套裁决规则**，而且两套规则对同一个靶标给出**相反结论**：

    AXL：对接 0.879 / 仅 MW 0.839 / 校正 0.751
      · 旧 mw_confounder 规则（对接>0.5 且 校正>0.5 且 对接>仅MW）→ **PASS**
      · 旧 breadth     规则（校正>0.5 且 校正>仅MW）        → **FAIL**

两套规则都不是笔误，是**判据设计不同**；但同一份稿件里出现两个互相矛盾的裁决，
是不可接受的（且不会有任何报错）。故抽出本模块，全局**只有一个** `enrichment_verdict()`。

【哪个规则是对的：两条规则错在哪】
· breadth 旧规则要求 `校正后 AUC > 仅 MW 基线` —— **口径错配**。校正后 AUC 是"扣掉尺寸趋势后
  的残差"的判别力，仅 MW 基线是"原始尺寸本身"的判别力，两者不同量纲、不可直接比大小。
  扣掉尺寸必然带走尺寸贡献的那部分判别力，所以该条件对"阳性天然偏大"的靶标近乎不可能满足
  —— 它会**系统性冤枉**所有真实信号。
· mw_confounder 旧规则方向对（比的是"对接原始 AUC vs 仅 MW 原始 AUC"，同口径），
  但**漏了显著性**：AUC 0.532 / p=0.118 也会被判 PASS，等于把噪声说成信号。

【本模块采用的规范判据（按优先级短路）】
    0. 阳性数 < MIN_POS（或数值非有限）          → n/a_insufficient_positives
    1. 仅 MW 基线 AUC ≥ 对接 AUC                 → FAIL_size_only_matches
       （一个"按分子量排序"的一行式启发式就够好 → 对接没提供额外信息）
    2. 对接 AUC 的 Mann-Whitney p ≥ 0.05         → NS_not_significant
       （有方向但达不到显著 → 只能说"趋势"，不能说"富集"）
    3. 校正后 AUC > 0.5                          → PASS_size_independent
       （对接优于尺寸启发式，且扣掉尺寸趋势后仍有判别力）
    4. 否则                                      → WEAK_residual_below_chance

规范判据同时满足三条实质要求：**优于平凡基线**（1）+ **统计显著**（2）+ **非尺寸伪影**（3）。

【额外的第二道平凡基线：2D 理化性质**
仅 MW 是"最弱"的平凡基线，审稿人更可能追问"5 个常见理化描述符的 logistic 回归能不能打平对接"。
故提供 `physchem_baseline_auc()`：用 MW/logP/TPSA/HBD/HBA/可旋转键 做**交叉验证**的
logistic 回归 AUC（小样本必须交叉验证，否则基线会被过拟合高估）。这不是替代判据，
而是**并列报告**的更强对照组 —— 若对接 AUC 不高于它，同样不能说对接有增量价值。

【方向约定（极易搞反，务必遵守）】
所有传入 `auc()` 的 score 一律 **越大越像阳性**：对接用 `-affinity`，MW 用 `mw`，
残差用 `pred - (-affinity)`（即"优于同尺寸预期"）。任何 AUC 都在此约定下解读。
"""
import numpy as np
from scipy import stats

MIN_POS = 5          # 富集检验的最少阳性数
PHYSCHEM = ["mw", "logp", "tpsa", "hbd", "hba", "rotb"]


# ---------------------------------------------------------------- 基础量
def auc(y, score):
    """AUC（Mann-Whitney U）；score **越大越像阳性**。返回 nan 表示无法计算。"""
    y = np.asarray(y)
    score = np.asarray(score, dtype=float)
    m = ~np.isnan(score)
    y, score = y[m], score[m]
    if len(set(y)) < 2:
        return np.nan
    a, b = score[y == 1], score[y == 0]
    if len(a) == 0 or len(b) == 0:
        return np.nan
    return float(stats.mannwhitneyu(a, b, alternative="two-sided").statistic) / (len(a) * len(b))


def auc_from_pos_neg(pos, neg):
    """秩公式 AUC = P(pos>neg) + 0.5·P(tie)，与 p6_score.py 口径一致。"""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if len(pos) == 0 or len(neg) == 0:
        return np.nan
    r = stats.rankdata(np.concatenate([pos, neg]))
    rp = r[:len(pos)].sum()
    u = rp - len(pos) * (len(pos) + 1) / 2.0
    return float(u) / (len(pos) * len(neg))


def auc_p(pos, neg):
    """单侧 p：阳性是否**显著更优**（score 更大）。"""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if len(pos) < 2 or len(neg) < 2:
        return np.nan
    return float(stats.mannwhitneyu(pos, neg, alternative="greater").pvalue)


def auc_boot_ci(pos, neg, n_boot=2000, seed=0):
    """Bootstrap 95% CI —— 小样本（n_pos 9–16）下 AUC 的不确定度必须报出来，
    否则 0.879 vs 0.839 这种差距会被读成"显著优于基线"，而实际 CI 大幅重叠。"""
    pos, neg = np.asarray(pos, float), np.asarray(neg, float)
    pos, neg = pos[~np.isnan(pos)], neg[~np.isnan(neg)]
    if len(pos) < 2 or len(neg) < 2:
        return (np.nan, np.nan)
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        a = rng.choice(pos, len(pos), replace=True)
        b = rng.choice(neg, len(neg), replace=True)
        v = auc_from_pos_neg(a, b)
        if np.isfinite(v):
            vals.append(v)
    if len(vals) < 50:
        return (np.nan, np.nan)
    return (float(np.percentile(vals, 2.5)), float(np.percentile(vals, 97.5)))


def residualise(x, z):
    """x 对 z 做一元线性拟合后取残差（去掉 z 的线性贡献）。"""
    x = np.asarray(x, dtype=float)
    z = np.asarray(z, dtype=float)
    return x - np.polyval(np.polyfit(z, x, 1), z)


def mw_adjust_auc(aff, mw, is_pos):
    """
    尺寸控制三件套。约定：score = -affinity（越大越好），残差 = 优于同尺寸预期的程度。
    返回 (auc_adj, auc_size_only, auc_dock, slope)
      auc_dock       : 原始对接 AUC（-affinity）
      auc_size_only  : 仅用 MW 的 AUC（平凡基线的**原始**判别力）
      auc_adj        : (-affinity) 扣掉 MW 线性趋势后的残差 AUC
      slope          : (-affinity) 对 MW 的回归斜率（负值=大分子被打得更负）
    """
    aff = np.asarray(aff, float)
    mw = np.asarray(mw, float)
    is_pos = np.asarray(is_pos).astype(bool)
    ok = (~np.isnan(aff)) & (~np.isnan(mw))
    neg_aff = -aff
    if ok.sum() < 4:
        return (np.nan, np.nan, np.nan, np.nan)
    a_dock = auc(is_pos[ok], neg_aff[ok])
    a_size = auc(is_pos[ok], mw[ok])
    slope = np.nan
    try:
        slope, _ = np.polyfit(mw[ok], neg_aff[ok], 1)
    except Exception:
        pass
    resid = residualise(neg_aff[ok], mw[ok])
    a_adj = auc(is_pos[ok], resid)
    return (a_adj, a_size, a_dock, slope)


def physchem_baseline_auc(X, y, seed=0):
    """
    2D 理化性质 logistic 回归的**交叉验证** AUC —— 比"仅 MW"更强的平凡基线。
    小样本必须交叉验证：训练集内 AUC 会被过拟合抬高，导致基线被高估、对接被冤枉。
    X: DataFrame/list（列需含 PHYSCHEM 中可用者）；y: 0/1。
    返回 (auc_cv, n_features)；不可计算时 (nan, k)。
    """
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict
    from sklearn.metrics import roc_auc_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    X = pd.DataFrame(X)
    y = np.asarray(y).astype(int)
    cols = [c for c in PHYSCHEM if c in X.columns]
    if not cols:
        return (np.nan, 0)
    D = X[cols].astype(float)
    keep = D.notna().all(axis=1).to_numpy()
    Xv, yv = D[keep].to_numpy(), y[keep]
    n_pos, n_neg = int((yv == 1).sum()), int((yv == 0).sum())
    if n_pos < MIN_POS or n_neg < 10:
        return (np.nan, len(cols))
    n_splits = int(min(5, n_pos))
    if n_splits < 2:
        return (np.nan, len(cols))
    clf = make_pipeline(StandardScaler(),
                        LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced"))
    cv = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=seed)
    try:
        pr = cross_val_predict(clf, Xv, yv, cv=cv, method="predict_proba")[:, 1]
        return (float(roc_auc_score(yv, pr)), len(cols))
    except Exception:
        return (np.nan, len(cols))


def physchem_in_sample_score(X, y):
    """
    2D 理化性质 logistic 的**样本内**打分（概率），用于配对比较 ΔAUC。
    注意：样本内拟合会**高估**基线 → 该基线偏强 → 对"对接更好"这一主张是**保守**方向。
    """
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    from sklearn.preprocessing import StandardScaler

    X = pd.DataFrame(X)
    y = np.asarray(y).astype(int)
    cols = [c for c in PHYSCHEM if c in X.columns]
    if not cols:
        return None
    D = X[cols].astype(float)
    keep = D.notna().all(axis=1).to_numpy()
    if int((y[keep] == 1).sum()) < MIN_POS or int((y[keep] == 0).sum()) < 10:
        return None
    sc = StandardScaler().fit(D[keep].to_numpy())
    clf = LogisticRegression(C=1.0, max_iter=5000, class_weight="balanced")
    clf.fit(sc.transform(D[keep].to_numpy()), y[keep])
    out = np.full(len(X), np.nan)
    out[keep] = clf.predict_proba(sc.transform(D[keep].to_numpy()))[:, 1]
    return out


def delta_auc_paired_ci(score_a, score_b, y, n_boot=2000, seed=0):
    """
    **同一批配体**上两个打分器的 AUC 之差 ΔAUC = AUC(a) − AUC(b) 的 bootstrap 95% CI，
    以及单侧 p（重采样中 Δ≤0 的比例）。

    这是回答"对接是否**优于**平凡基线"的**决定性统计量**：
    单看"对接 AUC 0.879 > 尺寸基线 0.841"不足以声称增量 —— 两个 AUC 各自有不确定度，
    小样本（n_pos 9–16）下其差值的 CI 往往**跨 0**。CI 含 0 ⇒ 不能说对接提供了增量信息。
    score_a / score_b 都须满足"越大越像阳性"。
    """
    a = np.asarray(score_a, float)
    b = np.asarray(score_b, float)
    y = np.asarray(y).astype(int)
    m = np.isfinite(a) & np.isfinite(b)
    a, b, y = a[m], b[m], y[m]
    if len(set(y)) < 2 or int(y.sum()) < 2:
        return (np.nan, np.nan, np.nan)
    d0 = auc(y, a) - auc(y, b)
    rng = np.random.default_rng(seed)
    n = len(y)
    ds = []
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        yy = y[idx]
        if len(set(yy)) < 2:
            continue
        v = auc(yy, a[idx]) - auc(yy, b[idx])
        if np.isfinite(v):
            ds.append(v)
    if len(ds) < 50:
        return (float(d0), np.nan, np.nan)
    ds = np.asarray(ds)
    return (float(d0), float(np.percentile(ds, 2.5)), float(np.percentile(ds, 97.5)))


def delta_auc_p_le0(ds_a, ds_b, y, n_boot=2000, seed=0):
    """ΔAUC 的单侧 p = P(Δ ≤ 0)（bootstrap）。"""
    a = np.asarray(ds_a, float)
    b = np.asarray(ds_b, float)
    y = np.asarray(y).astype(int)
    m = np.isfinite(a) & np.isfinite(b)
    a, b, y = a[m], b[m], y[m]
    if len(set(y)) < 2 or int(y.sum()) < 2:
        return np.nan
    rng = np.random.default_rng(seed)
    n, cnt, tot = len(y), 0, 0
    for _ in range(n_boot):
        idx = rng.integers(0, n, n)
        yy = y[idx]
        if len(set(yy)) < 2:
            continue
        v = auc(yy, a[idx]) - auc(yy, b[idx])
        if np.isfinite(v):
            tot += 1
            cnt += int(v <= 0)
    return float(cnt / tot) if tot else np.nan


# ---------------------------------------------------------------- 规范裁决
def enrichment_verdict(n_pos, auc_dock, auc_size_only, auc_adj, p_dock,
                       auc_physchem=np.nan, min_pos=MIN_POS,
                       delta_vs_size_ci=(np.nan, np.nan),
                       delta_vs_physchem_ci=(np.nan, np.nan)):
    """
    全局唯一的富集裁决（判据见模块 docstring）。返回 (verdict, reason_zh)。
    verdict ∈ {n/a_insufficient_positives, FAIL_size_only_matches, NS_not_significant,
               PASS_size_independent, WEAK_residual_below_chance}
    """
    if (n_pos is None or n_pos < min_pos or not np.isfinite(auc_dock)
            or not np.isfinite(auc_size_only) or not np.isfinite(auc_adj)):
        return ("n/a_insufficient_positives", f"阳性数 {n_pos} 不足 {min_pos} 或数值不可用")
    if auc_size_only >= auc_dock:
        return ("FAIL_size_only_matches",
                f"仅分子量基线 AUC {auc_size_only:.3f} ≥ 对接 AUC {auc_dock:.3f}："
                "一行式尺寸启发式就够好，对接未提供增量信息")
    if not (np.isfinite(p_dock) and p_dock < 0.05):
        pv = "nan" if not np.isfinite(p_dock) else f"{p_dock:.3g}"
        return ("NS_not_significant",
                f"对接 AUC {auc_dock:.3f} 方向正确但 p={pv} ≥ 0.05：只能称趋势，不能称富集")
    if auc_adj > 0.5:
        notes = []
        if np.isfinite(auc_physchem) and auc_dock <= auc_physchem:
            notes.append(f"2D 理化基线 AUC {auc_physchem:.3f} ≥ 对接 {auc_dock:.3f}")
        lo_s, hi_s = delta_vs_size_ci
        if np.isfinite(lo_s) and lo_s <= 0:
            notes.append(f"ΔAUC(vs 尺寸基线) 的 95% CI [{lo_s:+.3f}, {hi_s:+.3f}] **含 0** → 增量不显著")
        lo_p, hi_p = delta_vs_physchem_ci
        if np.isfinite(lo_p) and lo_p <= 0:
            notes.append(f"ΔAUC(vs 2D 理化基线) 的 95% CI [{lo_p:+.3f}, {hi_p:+.3f}] **含 0** → 增量不显著")
        extra = ("；但注意：" + "；".join(notes)) if notes else ""
        return ("PASS_size_independent",
                f"对接 AUC {auc_dock:.3f} > 尺寸基线 {auc_size_only:.3f}、p={p_dock:.2g}、"
                f"校正后 {auc_adj:.3f} > 0.5{extra}")
    return ("WEAK_residual_below_chance",
            f"扣掉尺寸趋势后 AUC {auc_adj:.3f} ≤ 0.5：残差已无判别力")
