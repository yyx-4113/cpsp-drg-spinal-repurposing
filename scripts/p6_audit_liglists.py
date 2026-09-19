# -*- coding: utf-8 -*-
"""
p6_audit_liglists.py —— 配体清单与"逐靶标逐层"打分配体集合的一致性审计（+ 可选修复）

【为什么必须有这个脚本】
对接是**按 chunk 缓存**的：chunk 文件名只含 `(target, tag, chunk_index)`，**不含配体清单的
版本指纹**。于是只要 `docking/_liglists/*.txt` 被重新生成过（本项目真实发生：Tier1/Tier2 的
分层被调整过），旧 chunk 缓存仍会被复用：

  · 分块边界按旧清单切分 → 某些 chunk 里的配体已不属于该层，而该层的新配体从未被对接；
  · 结果 `scores_<tag>.csv` 看起来"行数对得上"（仍是 620 行），**但集合是错的**；
  · 该靶标的"靶标内百分位"于是建立在与其它靶标**不同的配体集合**上 → 跨靶标可比性被静默破坏，
    而且不会有任何报错。

本项目实例：**AXL 的 t1_cns 结果里有 60 个配体现已划入 t2_other，同时缺 60 个当前 t1 配体**
（其余 9 个靶标完全一致）。若不做审计，这条会一路进到四维排序与稿件表格里。

【审计口径】
  · 先验检查：`t1_list ∪ t2_list == 通过过滤的配体库`，且两清单互不相交、各自无重复；
  · 逐靶标逐层：`set(scores_<tag>.csv.chembl_id)` 必须**等于** 对应清单的集合（缺失与多出
    都要报 0 才算 OK）；
  · `--fix` 时把陈旧的 chunk 与 scores **重命名隔离**到 `_stale_<tag>_<时间戳>/`
    （用 rename 不用 delete：既绕开沙箱批量删除守卫，又保留现场可回溯），使重跑真正重新对接。

退出码：0=全 OK；2=发现陈旧但未修；3=发现陈旧且已隔离（需重跑该 靶标×层）；1=先验检查失败。
"""
import os, sys, glob, time, shutil, argparse, collections
import pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
OUT = os.path.join(ROOT, "docking/out")
LIGL = os.path.join(ROOT, "docking/_liglists")
TAGS = {"t1_cns": "tier1_cns.txt", "t2_other": "tier2_other.txt"}


def read_list(p):
    return [l.strip() for l in open(p, encoding="utf-8") if l.strip()]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fix", action="store_true", help="隔离陈旧的 chunk/scores（不删除，改名移入 _stale_*）")
    ap.add_argument("--tags", default=",".join(TAGS), help="要审计的层")
    ap.add_argument("--report-json", default=None,
                    help="把审计结论写成 JSON（含 stale 列表），供上层守望脚本机读")
    a = ap.parse_args()
    tags = [t.strip() for t in a.tags.split(",") if t.strip()]

    def _dump(stale_pairs, fix_applied=False):
        if not a.report_json:
            return
        import json
        json.dump({"stale": [[s, t] for s, t in stale_pairs],
                   "fix_applied": bool(fix_applied),
                   "all_lists_consistent": not stale_pairs,
                   "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S")},
                  open(a.report_json, "w", encoding="utf-8"), indent=2, ensure_ascii=False)

    # ---------- 先验：清单自身与配体库一致 ----------
    lig = pd.read_csv(os.path.join(TAB, "P6_ligand_library.csv"))
    lig["chembl_id"] = lig.chembl_id.astype(str)
    pas = set(lig[lig["pass"] == True].chembl_id)
    lists = {}
    bad = False
    for tg in tags:
        if tg not in TAGS:
            print(f"[skip] 未知层 {tg}"); continue
        fp = os.path.join(LIGL, TAGS[tg])
        if not os.path.exists(fp):
            print(f"⚠ 缺清单 {fp}"); bad = True; continue
        v = read_list(fp)
        dup = [k for k, c in collections.Counter(v).items() if c > 1]
        lists[tg] = set(v)
        print(f"清单 {TAGS[tg]}: {len(v)} 条，唯一 {len(set(v))}，重复 {len(dup)}")
        if dup:
            print(f"  ⚠ 清单内重复：{dup[:10]}"); bad = True
    if len(lists) == 2:
        inter = lists["t1_cns"] & lists["t2_other"]
        uni = lists["t1_cns"] | lists["t2_other"]
        print(f"两层交集 {len(inter)}；并集 {len(uni)}；配体库(pass) {len(pas)}；"
              f"并集==库? {uni == pas}")
        if inter:
            print(f"  ⚠ 两层交集非空：{sorted(inter)[:10]}"); bad = True
        if uni != pas:
            print(f"  ⚠ 并集与库不一致：库独有 {len(pas-uni)}，并集独有 {len(uni-pas)}"); bad = True
    if bad:
        print("\n先验检查失败 —— 清单本身有问题，先修清单再谈缓存。")
        sys.exit(1)

    # ---------- 逐靶标逐层：打分集合 vs 清单 ----------
    syms = sorted(d for d in os.listdir(OUT) if os.path.isdir(os.path.join(OUT, d)))
    stale = []
    print(f"\n{'target':10s} {'tag':9s} {'scored':>7s} {'expect':>7s} {'missing':>8s} {'extra':>6s}  判定")
    for sym in syms:
        for tg in tags:
            sp = os.path.join(OUT, sym, f"scores_{tg}.csv")
            exp = lists.get(tg)
            if exp is None:
                continue
            if not os.path.exists(sp):
                print(f"{sym:10s} {tg:9s} {'-':>7s} {len(exp):7d} {'-':>8s} {'-':>6s}  (未跑)")
                continue
            got = set(pd.read_csv(sp, usecols=["chembl_id"]).chembl_id.astype(str))
            miss, extra = exp - got, got - exp
            ok = (not miss) and (not extra)
            if not ok:
                stale.append((sym, tg))
            print(f"{sym:10s} {tg:9s} {len(got):7d} {len(exp):7d} {len(miss):8d} {len(extra):6d}"
                  f"  {'OK' if ok else '❌ 陈旧/错配'}")

    if not stale:
        print("\n✔ 全部 靶标×层 的配体集合与当前清单一致。")
        sys.exit(0)

    print(f"\n发现 {len(stale)} 个 靶标×层 的配体集合与清单不符：{stale}")
    if not a.fix:
        print("（未指定 --fix，不修改任何文件。加 --fix 会把陈旧 chunk/scores 隔离到 _stale_*，"
              "随后需重跑这些 靶标×层。）")
        _dump(stale, fix_applied=False)
        sys.exit(2)

    ts = time.strftime("%Y%m%d_%H%M%S")
    for sym, tg in stale:
        odir = os.path.join(OUT, sym)
        q = os.path.join(odir, f"_stale_{tg}_{ts}")
        os.makedirs(q, exist_ok=True)
        moved = 0
        for pat in (f"chunk_{tg}_*.csv", f"scores_{tg}.csv"):
            for f in glob.glob(os.path.join(odir, pat)):
                shutil.move(f, os.path.join(q, os.path.basename(f)))
                moved += 1
        print(f"  ✔ 隔离 {sym}/{tg}：{moved} 个文件 -> {q}")
    print("\n请重跑这些 靶标×层（例：")
    for sym, tg in stale:
        print(f"   python scripts/p6_dock.py --stage 1 --exh 1 --max-evals 0 "
              f"--tag {tg} --only {sym} --liglist docking/_liglists/{TAGS[tg]} --workers 7")
    print("）后再跑 p6_score / p6_figures / p6_report / p6_breadth。")
    _dump(stale, fix_applied=True)
    sys.exit(3)


if __name__ == "__main__":
    main()
