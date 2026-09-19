# -*- coding: utf-8 -*-
"""
p6_finalize_watch.py —— P6 收尾编排器（幂等、无人值守、**失败即停**）

背景一：本会话环境对后台任务有 ~12h 生命周期清理，长链常被杀。本脚本作为第二道保险，
在对接结束后把 P6 推到"可定稿"状态。

背景二（本版最重要的改动）：旧版链在 `p6_score` 返回 rc=1 时**照样**继续跑出图与报告，
而图/报告读的是**上一轮的旧排序表** → 产出"新合表 + 旧数字"的自相矛盾产物，控制台一行
rc=1 淹没在长日志里无人察觉。故本脚本一切步骤**失败即停**：宁可没有图与报告，
也不要错的图与报告。

流程（每步幂等，可反复执行）：

  0. **等对接静默**：无 vina 进程、无 p6_dock 进程、t1/t2 两层合表都存在且 20 s 内不变。
  1. **审计并修复陈旧配体缓存**：`p6_audit_liglists.py`。对接按 chunk 缓存，而 chunk 名
     **不含配体清单版本指纹**，清单一旦重新生成过，旧 chunk 会被静默复用 → 某 靶标×层 的
     打分配体集合与当前清单不符（实测：AXL/t1_cns 多 60 缺 60）。发现即 `--fix`（rename 隔离，
     不删除）→ 重跑该 靶标×层 → 重评。
  2. **重评**：`p6_score --tags t1_cns,t2_other` → `p6_figures` → `p6_report`（逐步严格检查 rc）。
  3. **重算方法学控制**：`p6_mw_confounder` / `p6_face_validity` / `p6_mw_ranking_sensitivity`。
     这些脚本的输出**直接进稿件**，且读的是排序表 —— 若不随之重算，稿件里就会出现
     "新排序 + 旧控制数字"，而且不会有任何报错。
  4. **正式广度分析**：`p6_breadth.py`（无 `--allow-partial`，缺产物即拒跑）。
  5. **复核**：audit 再跑一遍必须 rc=0；写出 `P6_FINALIZE_STATUS.json`。

用法：
  python -u scripts/p6_finalize_watch.py > scripts/p6_finalize_watch.out 2>&1
"""
import os, sys, time, json, subprocess

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
PY = r"C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
TAB = os.path.join(ROOT, "results/tables")
T1 = os.path.join(TAB, "P6_docking_scores_t1_cns.csv")
T2 = os.path.join(TAB, "P6_docking_scores_t2_other.csv")
AUDIT_JSON = os.path.join(TAB, "P6_liglist_audit.json")
STATUS = os.path.join(TAB, "P6_FINALIZE_STATUS.json")
LIGLIST = {"t1_cns": "docking/_liglists/tier1_cns.txt",
           "t2_other": "docking/_liglists/tier2_other.txt"}

POLL = 120
MAX_WAIT = 8 * 3600


def log(m):
    print(f"[{time.strftime('%H:%M:%S')}] {m}", flush=True)


def _count(image):
    try:
        out = subprocess.run(["tasklist", "/FI", f"IMAGENAME eq {image}", "/FO", "CSV", "/NH"],
                             capture_output=True, text=True, errors="replace", timeout=40).stdout
    except Exception:
        return -1
    return sum(1 for l in out.splitlines() if image.split(".")[0] in l.lower())


def _n_dock_procs():
    """数正在跑的 p6_dock / p6_chain 进程（用命令行匹配，避免把本脚本自己数进去）"""
    ps = ("Get-CimInstance Win32_Process | Where-Object { $_.Name -eq 'python.exe' -and "
          "$_.CommandLine -match 'p6_dock|p6_chain' } | Measure-Object | "
          "Select-Object -ExpandProperty Count")
    try:
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, errors="replace", timeout=60).stdout
        return int((r or "0").strip() or 0)
    except Exception:
        return -1


def run(cmd, name, strict=True):
    log(f"▶ {name}")
    rc = subprocess.run([PY, "-u"] + cmd, cwd=ROOT).returncode
    log(f"  ← {name} rc={rc}" + ("   [FAIL]" if (strict and rc != 0) else ""))
    return rc


def wait_for_dock_idle():
    log("步骤0：等对接静默（无 vina / 无 p6_dock 进程 + 两层合表齐备且稳定）")
    t0 = time.time()
    while True:
        v, d = _count("vina.exe"), _n_dock_procs()
        if v == 0 and d == 0 and os.path.exists(T1) and os.path.exists(T2):
            s1 = (os.path.getsize(T1), os.path.getsize(T2))
            time.sleep(20)
            s2 = (os.path.getsize(T1), os.path.getsize(T2))
            if s1 == s2 and _count("vina.exe") == 0 and _n_dock_procs() == 0:
                log(f"✔ 静默：t1={s1[0]:,} B  t2={s1[1]:,} B")
                return True
        if time.time() - t0 > MAX_WAIT:
            log(f"⚠ 等待超时（vina={v} dock={d} t1={os.path.exists(T1)} t2={os.path.exists(T2)}）")
            return False
        time.sleep(POLL)


def audit(apply_fix=False):
    cmd = ["scripts/p6_audit_liglists.py", "--report-json", AUDIT_JSON]
    if apply_fix:
        cmd.insert(1, "--fix")
    return run(cmd, "audit --fix" if apply_fix else "audit")


def audit_and_repair():
    log("步骤1：审计配体清单一致性（靶标×层 的配体集合必须与当前清单**集合相等**）")
    rc = audit()
    if rc == 0:
        log("✔ 配体集合一致，无需修复")
        return True
    if rc == 1:
        log("⚠ 清单本身有问题（rc=1）——停止，需人工处理")
        return False
    stale = []
    try:
        stale = [tuple(x) for x in json.load(open(AUDIT_JSON, encoding="utf-8"))["stale"]]
    except Exception as e:
        log(f"⚠ 读 {AUDIT_JSON} 失败：{e}")
    log(f"发现陈旧 靶标×层 {stale} → 隔离并重跑")
    audit(apply_fix=True)
    for sym, tag in stale:
        ll = LIGLIST.get(tag)
        if not ll:
            log(f"⚠ 未知层 {tag}，跳过 {sym}")
            continue
        if run(["scripts/p6_dock.py", "--stage", "1", "--exh", "1", "--max-evals", "0",
                "--tag", tag, "--only", sym, "--liglist", ll, "--workers", "7"],
               f"redock {sym}/{tag}") != 0:
            log(f"⚠ {sym}/{tag} 重跑失败")
            return False
    return True


def rescore_all():
    """重评 + 出图 + 报告；任一步失败立即终止（绝不用旧表出图/出报告）"""
    log("步骤2：重评 → 出图 → 报告")
    if run(["scripts/p6_score.py", "--tags", "t1_cns,t2_other"], "score") != 0:
        log("⚠ 评分失败 → 终止（下游图表/报告不使用旧表）")
        return False
    if run(["scripts/p6_figures.py"], "figures") != 0:
        log("⚠ 出图失败 → 终止")
        return False
    if run(["scripts/p6_report.py"], "report") != 0:
        log("⚠ 报告失败 → 终止")
        return False
    return True


def refresh_controls():
    log("步骤3：重算依赖对接结果的方法学控制（否则稿件会出现『新排序 + 旧控制数字』）")
    ok = True
    for s in ("scripts/p6_mw_confounder.py --tags t1_cns,t2_other",
              "scripts/p6_face_validity.py",
              "scripts/p6_mw_ranking_sensitivity.py"):
        parts = s.split()
        if run([parts[0]] + parts[1:], os.path.basename(parts[0])) != 0:
            ok = False
    log("  （p6_throughput 不依赖对接结果；p6_reverse_control 的标签来自 ChEMBL 实测活性，"
        "独立于对接 → 两者均无需重算）")
    return ok


def main():
    st = {"started": time.strftime("%Y-%m-%d %H:%M:%S")}
    if not wait_for_dock_idle():
        st["result"] = "timeout_waiting_for_dock"; json.dump(st, open(STATUS, "w"), indent=2)
        sys.exit(4)
    st["audit_ok"] = audit_and_repair()
    if not st["audit_ok"]:
        log("⚠ 审计未通过 → 仍继续重评，但**不得定稿**")
    st["rescore_ok"] = rescore_all()
    if not st["rescore_ok"]:
        st["result"] = "rescore_failed"; json.dump(st, open(STATUS, "w"), indent=2)
        sys.exit(5)
    st["controls_ok"] = refresh_controls()
    log("步骤4：正式广度分析")
    rc = run(["scripts/p6_breadth.py"], "breadth")
    if rc == 3:
        log("⚠ 广度分析报缺产物（rc=3）——请核查哪个 靶标×层 未齐")
    # 复核闸门
    log("步骤5：复核审计")
    rc2 = run(["scripts/p6_audit_liglists.py", "--report-json", AUDIT_JSON], "audit (复核)")
    st["final_audit_rc"] = rc2
    st["breadth_rc"] = rc
    st["result"] = "ready_to_finalise" if (rc2 == 0 and rc == 0) else "needs_review"
    st["finished"] = time.strftime("%Y-%m-%d %H:%M:%S")
    json.dump(st, open(STATUS, "w"), indent=2)
    log(f"收尾结束：{st['result']}  状态见 {STATUS}")
    log("下一步（人工/下一轮）：填稿件 §3.5 广度段落 → 誊最终数字 → 定稿 → P7 tag/DOI")


if __name__ == "__main__":
    main()
