#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_reverse_control.py -- 用 ChEMBL 实测活性构造"已知结合"阳性集（反向阳性对照的燃料）

【为什么必须补这一层】
PROJECT_PLAN.md §6.5 要求做反向阳性对照：拿已知镇痛药-靶点配对当探针，验证流程能召回它们。
但只靠 DRH 的 `target` 注释 + 人工 PAIN_PRIOR 标注，阳性集会**几乎全部落在 ADRA2A 一个靶标上**：

    ADRA2A   48 个库内阳性药
    其余 9 个靶标   0 个

原因是**真实的**：MAPK14 在 DRH 里有 38 个注释药物，但全是临床前/Ph1-3 的 p38 抑制剂，
没有一个是已批准药（我们的库是 ChEMBL max_phase=4 的已批准药），所以交集为 0。
AXL/ACVR1/SLC2A1/SERPINE1 同理。于是"逐靶标 AUC"这个用于给每个靶标结论定
可信度权重（D4）的机制，实际上只剩 1 个靶标可用 → D4 退化成常数 0.5，形同虚设。

本脚本改用**与对接打分完全独立的实验数据来源**：ChEMBL 实测活性（pChEMBL）。
  · 标签（阳性）来自实验测定 → 预测（对接打分）来自物理模拟 → **无二重蘸取**
  · 这是一次标准的 retrospective enrichment / 反向对照设计
  · 阈值 pchembl_value >= 6（即 ≤1 µM）记为该靶标的"已验证结合分子"

产出：results/tables/P6_reverse_control_positives.csv
      symbol, chembl_id, pref_name, pchembl_max, n_act, chembl_target, source

【可靠性说明 · 务必读】
EBI 的 ChEMBL REST 接口在本次会话中**反复整体性 5xx**（连 `/activity.json?limit=1` 这种
无过滤查询都会 500，且返回的是 EMBL-EBI 的 HTML 错误页而非 ChEMBL 的 JSON 错误）。
因此本脚本按"可重跑、可断点续跑"设计：每个靶标的原始 JSON 都落盘缓存，
重跑时直接命中缓存；失败不抛异常，只记 `status=FAILED`，最后由 p6_score.py 自行降级。
"""
import os, sys, json, time, argparse, urllib.request, urllib.error
import pandas as pd

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
TAB = os.path.join(ROOT, "results/tables")
RAW = os.path.join(ROOT, "data/raw")
CACHE = os.path.join(RAW, "chembl_rc_cache")
os.makedirs(CACHE, exist_ok=True)

UA = "cpsp-p6-reverse-control/1.0 (academic use)"
PCHEMBL_MIN = 6.0            # <=1 uM
MAX_RETRY = 6
BACKOFF = [5, 10, 20, 40, 60, 60]


def _get(url, timeout=45):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": UA})
    with urllib.request.urlopen(req, timeout=timeout) as f:
        return f.read()


def get_json_cached(url, cache_key, force=False):
    """带落盘缓存 + 指数退避重试的 GET。

    【踩过的坑】EBI/ChEMBL 的 5xx 是**间歇性**的：上一分钟 `activity.json?limit=1` 还能返回
    24,527,044 条总数，下一分钟同样的 URL 就 500 并返回 EBI 的 HTML 错误页。
    所以必须：① 重试不能少（6 次）；② 退避要够长（最长 60s）；③ 结果必须落盘，
    一次成功的抓取不能被后续失败浪费。三者缺一，长跑必然半途而废。
    """
    p = os.path.join(CACHE, cache_key)
    if os.path.exists(p) and not force:
        try:
            return json.load(open(p, encoding="utf-8")), True
        except Exception:
            pass
    last = ""
    for i in range(MAX_RETRY):
        try:
            raw = _get(url)
            d = json.loads(raw.decode("utf-8"))
            json.dump(d, open(p, "w", encoding="utf-8"))
            return d, False
        except urllib.error.HTTPError as e:
            body = b""
            try:
                body = e.read()[:120]
            except Exception:
                pass
            last = f"HTTP {e.code} {body!r}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        if i < MAX_RETRY - 1:
            wait = BACKOFF[min(i, len(BACKOFF) - 1)]
            print(f"      retry {i+1}/{MAX_RETRY} ({last}) ，等 {wait}s", flush=True)
            time.sleep(wait)
    return None, last


def uniprot_to_chembl(acc, force=False):
    """UniProt → ChEMBL target id，走 UniProt 官方交叉引用。

    【踩过的坑】不要用 ChEMBL 自己的 `?target_components__accession=<acc>` 过滤 ——
    该过滤在当前 ChEMBL 部署上稳定返回 HTTP 500。UniProt 的
    `uniProtKBCrossReferences` 里直接带 ChEMBL id，稳定且权威。
    """
    url = f"https://rest.uniprot.org/uniprotkb/{acc}.json"
    d, cached = get_json_cached(url, f"uniprot_{acc}.json", force)
    if d is None:
        return [], cached
    ids = [x["id"] for x in d.get("uniProtKBCrossReferences", [])
           if x.get("database") == "ChEMBL" and x.get("id")]
    return sorted(set(ids)), cached


def fetch_activities(tid, force=False):
    """拉取该 ChEMBL target 上所有 pchembl>=PCHEMBL_MIN 的活性（分页）。"""
    acts, offset, total = [], 0, None
    while True:
        url = (f"https://www.ebi.ac.uk/chembl/api/data/activity.json?"
               f"target_chembl_id={tid}&pchembl_value__gte={PCHEMBL_MIN}"
               f"&limit=1000&offset={offset}")
        d, cached = get_json_cached(url, f"act_{tid}_{offset}.json", force)
        if d is None:
            # 允许部分成功：前几页拿到多少算多少
            print(f"      [warn] {tid} offset={offset} 抓取失败，已有 {len(acts)} 条", flush=True)
            break
        if total is None:
            total = d["page_meta"]["total_count"]
        got = d.get("activities", [])
        acts.extend(got)
        offset += len(got)
        if cached:
            print(f"      缓存命中 {tid} offset={offset}/{total}", flush=True)
        if not got or offset >= (total or 0):
            break
        time.sleep(0.4)          # 对 EBI 客气一点，降低被限流概率
    return acts, total


def probe_chembl():
    """起步前的可用性探针。

    【踩过的坑】不做探针的话，EBI 侧故障时会**逐个靶标白烧重试时间**：
    每个靶标 6 次重试、退避合计 195s，10 个靶标 ≈ 33 分钟全部浪费在没有希望的等待上，
    最后还写出一份空阳性表。探针用最廉价的查询先确认端点活着，不行就立刻退出。
    """
    url = "https://www.ebi.ac.uk/chembl/api/data/activity.json?limit=1"
    for i in range(3):
        try:
            raw = _get(url, timeout=30)
            json.loads(raw.decode("utf-8"))
            return True, "OK"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
        except Exception as e:
            last = f"{type(e).__name__}: {e}"
        if i < 2:
            time.sleep(4)
    return False, last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="忽略缓存重抓")
    ap.add_argument("--only", default=None, help="逗号分隔靶标符号")
    ap.add_argument("--skip-probe", action="store_true", help="跳过起始探针（缓存充足时用）")
    a = ap.parse_args()

    outp = os.path.join(TAB, "P6_reverse_control_positives.csv")
    n_old = 0
    if os.path.exists(outp):
        try:
            n_old = len(pd.read_csv(outp))
        except Exception:
            n_old = 0

    if not a.skip_probe:
        okc, note = probe_chembl()
        print(f"ChEMBL 探针: {'可用' if okc else '不可用（' + note + '）'}", flush=True)
        if not okc:
            print("  端点不可用 → 立即退出，不进入逐靶标重试（避免白烧 30+ 分钟）。")
            print("  已有阳性表行数：", n_old)
            print("  稍后 EBI 恢复时重跑本脚本即可（无过滤参数的缓存仍有效）。")
            raise SystemExit(2)

    R = pd.read_csv(os.path.join(TAB, "P6_receptors.csv"))
    T = pd.read_csv(os.path.join(TAB, "P6_target_selection.csv"))
    targets = sorted(R[R.status == "OK"].symbol.str.upper().unique())
    if a.only:
        want = {x.strip().upper() for x in a.only.split(",")}
        targets = [t for t in targets if t in want]
    acc = dict(zip(T.symbol.str.upper(), T.uniprot))

    L = pd.read_csv(os.path.join(TAB, "P6_ligand_library.csv"))
    L = L[L["pass"] == True].copy()
    L["chembl_id"] = L.chembl_id.astype(str)
    lib = set(L.chembl_id)
    print(f"库内可用配体 {len(lib)} 个 | 待查靶标 {len(targets)} 个")

    rows, stat = [], []
    for sym in targets:
        u = acc.get(sym)
        print(f"\n[{sym}] UniProt={u}", flush=True)
        if not u or pd.isna(u):
            stat.append({"symbol": sym, "status": "NO_UNIPROT", "n_chembl_targets": 0,
                         "n_activities": 0, "n_lib_positives": 0}); continue
        tids, note = uniprot_to_chembl(u, a.force)
        if not tids:
            print(f"  未拿到 ChEMBL target id（{note}）", flush=True)
            stat.append({"symbol": sym, "status": f"NO_CHEMBL_TARGET:{note}",
                         "n_chembl_targets": 0, "n_activities": 0, "n_lib_positives": 0}); continue
        print(f"  ChEMBL targets: {tids}", flush=True)

        n_act, best = 0, {}
        for tid in tids:
            acts, total = fetch_activities(tid, a.force)
            n_act += len(acts)
            print(f"    {tid}: {len(acts)} 条活性（报告总数 {total}）", flush=True)
            for x in acts:
                cid = x.get("molecule_chembl_id")
                pv = x.get("pchembl_value")
                if not cid or cid not in lib or pv in (None, ""):
                    continue
                try:
                    pv = float(pv)
                except (TypeError, ValueError):
                    continue
                if cid not in best or pv > best[cid][0]:
                    best[cid] = (pv, x.get("standard_type"), tid)
        for cid, (pv, st, tid) in best.items():
            rows.append({"symbol": sym, "chembl_id": cid, "pchembl_max": round(pv, 2),
                         "standard_type": st or "", "chembl_target": tid, "source": "ChEMBL_activity"})
        print(f"  -> 库内阳性 {len(best)} 个", flush=True)
        stat.append({"symbol": sym, "status": "OK", "n_chembl_targets": len(tids),
                     "n_activities": n_act, "n_lib_positives": len(best)})

    # 合并药物名，便于人工核对
    P = pd.DataFrame(rows)
    if len(P):
        P = P.merge(L[["chembl_id", "pref_name", "atc", "pain_prior"]], on="chembl_id", how="left")
        P = P.sort_values(["symbol", "pchembl_max"], ascending=[True, False])

    # 【护栏 · 必须保留】绝不用空结果覆盖已有的非空阳性表。
    # 本项目已经踩过一次同类事故：配体库脚本因解释器用错而把结果 CSV 覆盖成 0 行成功，
    # 好在 PDBQT 文件因存在性检查幸存。反向对照的阳性表是**不可再生**的（依赖外部 API
    # 的当时状态），一旦被空表覆盖，后续 p6_score.py 会静默退化成"无阳性"。
    if len(P) == 0 and n_old > 0:
        print(f"\n[护栏] 本次抓取 0 行，但已有 {n_old} 行的旧阳性表 → "
              f"拒绝覆盖，保留旧表。")
        ST = pd.DataFrame(stat)
        ST.to_csv(os.path.join(TAB, "P6_reverse_control_positives_status.csv"), index=False)
        print(ST.to_string(index=False))
        raise SystemExit(3)

    P.to_csv(outp, index=False)
    ST = pd.DataFrame(stat)
    ST.to_csv(os.path.join(TAB, "P6_reverse_control_positives_status.csv"), index=False)

    print("\n=== 抓取状态 ===")
    print(ST.to_string(index=False))
    print("\n=== 各靶标库内阳性数 ===")
    if len(P):
        print(P.groupby("symbol").agg(n_pos=("chembl_id", "nunique"),
                                      pchembl_max=("pchembl_max", "max")).to_string())
    else:
        print("  （无）")
    print(f"\n表 -> P6_reverse_control_positives.csv（{len(P)} 行）")


if __name__ == "__main__":
    main()
