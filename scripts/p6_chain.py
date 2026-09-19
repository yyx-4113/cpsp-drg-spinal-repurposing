#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
p6_chain.py -- P6 自驱动流水线链（Tier1 → Tier2 → 评分 → 出图 → 报告）

【设计动机】
P6 的对接总量是 3,085 配体 × 10 靶标 = 30,850 次 Vina 调用，按实测速度要十几个小时。
人工盯着跑、跑完再手动敲下一条命令，既慢又容易在中断处卡住。本脚本把整条链固化成
**可中断、可续跑、幂等** 的一条命令，把"持续进行的步骤"落到工程上：

  1. 等 Tier 1（若已在跑）→ 跑完落 `P6_docking_scores_t1_cns.csv`
  2. Tier 2 全库其余配体
  3. p6_score.py --tags t1_cns,t2_other（反向对照 + 四维排序）
  4. p6_figures.py（补齐剩余 3 张图）
  5. p6_report.py（生成 results/P6_RESULTS.md）

【幂等与自愈】
每个步骤先查产物是否存在，存在即跳过。
检测"Tier 1 是否还在跑"用 `vina.exe` 进程数： docking 期间必然有 vina 进程，
一个都没有而产物又缺失 → 说明上一个进程被会话清理杀掉了 → 本脚本**自己重启该阶段**。
因为 p6_dock.py 以 chunk 为单位落盘缓存，重启只会重跑未完成的块，不浪费已完成算力。
"""
import os, sys, time, subprocess, glob, argparse

ROOT = "D:/2026.9/极速交付9月会员日优惠套路/01_AI生信-虚拟多重筛药/慢性疼痛"
PY = r"C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
TAB = os.path.join(ROOT, "results/tables")
LOG = os.path.join(ROOT, "scripts/p6_chain.out")


def log(msg):
    line = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def n_vina():
    """在跑的 vina 进程数。返回 -1 表示查询失败（当作"未知"，不误判为掉线）。"""
    try:
        r = subprocess.run(["tasklist"], capture_output=True)
        txt = r.stdout.decode("utf-8", "replace").lower()
        return txt.count("vina.exe")
    except Exception:
        return -1


def run(cmd, tag):
    log(f"▶ 启动 {tag}\n    {' '.join(str(c) for c in cmd)}")
    t0 = time.time()
    with open(os.path.join(ROOT, f"scripts/p6_chain_{tag}.out"), "a", encoding="utf-8") as f:
        p = subprocess.run(cmd, cwd=ROOT, stdout=f, stderr=subprocess.STDOUT)
    log(f"✔ {tag} 结束 rc={p.returncode}  用时 {time.time()-t0:.0f}s")
    return p.returncode


def wait_for_completion(product, poll=90, max_hours=24.0):
    """等 product 出现；若发现 vina 全停而 product 仍未出现，返回 False 让调用方重启阶段。"""
    t_start = time.time()
    while True:
        if os.path.exists(product):
            return True
        el = time.time() - t_start
        if el > max_hours * 3600:
            log(f"⚠ 等待 {product} 超过 {max_hours}h，放弃等待")
            return False
        nv = n_vina()
        if nv == 0:
            log(f"  检测到 0 个 vina 进程且 {os.path.basename(product)} 仍缺失 → 判定上一进程已中断")
            return False
        if int(el) % (poll * 8) < poll:            # 每 ~8 次轮询打一条心跳
            log(f"  等待中… vina 进程 {nv} 个，已等 {el/60:.1f} 分钟")
        time.sleep(poll)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from", dest="start_at", default="1",
                    choices=["1", "2", "3", "4", "5"], help="从第几步开始")
    ap.add_argument("--workers", type=int, default=7)
    ap.add_argument("--chunk", type=int, default=30)
    a = ap.parse_args()
    start = int(a.start_at)

    log("=" * 78)
    log(f"P6 流水线链启动（从步骤 {start} 开始）")

    # ---- 步骤 1：Tier 1（CNS/镇痛先验层，620 配体 × 10 靶标）----
    # 【修复】旧逻辑在 Tier 1 重启失败后会"误判完成"并推进到步骤 2，导致 t1 合表永远
    # 缺失、下游评分用到残缺数据。现改为：循环拉起 Tier 1 直到合表真实存在（最多 10 次），
    # 仍失败则直接终止流水线，绝不带着残缺 t1 进入评分。
    t1 = os.path.join(TAB, "P6_docking_scores_t1_cns.csv")
    if start <= 1 and not os.path.exists(t1):
        log("步骤 1/5：Tier 1 对接")
        T1_CMD = [PY, "-u", "scripts/p6_dock.py", "--stage", "1", "--exh", "1",
                  "--max-evals", "0", "--tag", "t1_cns", "--workers", str(a.workers),
                  "--liglist", "docking/_liglists/tier1_cns.txt", "--chunk", str(a.chunk)]
        attempt = 0
        while not os.path.exists(t1):
            attempt += 1
            if attempt > 10:
                log("⚠ Tier 1 重试 10 次仍无合表产物，终止流水线（不污染后续评分）")
                sys.exit(1)
            if n_vina() > 0:
                log(f"  [尝试 {attempt}] Tier 1 已在运行，等待其完成（中断则自动续跑）")
                if wait_for_completion(t1):
                    break
                # 0 个 vina 且产物仍缺失 → 下面重新拉起
            log(f"  [尝试 {attempt}] 拉起 Tier 1（chunk 缓存会自动跳过已完成部分）")
            run(T1_CMD, "t1")
            # run() 阻塞到 p6_dock 结束；若合表已出则跳出，否则下一轮重拉
        if not os.path.exists(t1):
            log("⚠ Tier 1 合表仍未生成，终止流水线（不污染后续评分）")
            sys.exit(1)
        log("  ✔ Tier 1 合表已生成")
    else:
        log("步骤 1/5：Tier 1 产物已存在，跳过")

    # ---- 步骤 2：Tier 2（其余 2,465 配体 × 10 靶标）----
    # 【修复】旧逻辑只 `run()` 一次，p6_dock 子进程一旦被会话清理杀掉就静默带着缺失的
    # t2 进入评分。现改为：循环拉起 Tier 2 直到合表真实存在（最多 10 次），中途靠 chunk
    # 缓存续跑、不重算；仍失败则终止，绝不带着残缺 t2 进评分。
    t2 = os.path.join(TAB, "P6_docking_scores_t2_other.csv")
    if start <= 2 and not os.path.exists(t2):
        log("步骤 2/5：Tier 2 对接（全库其余配体）")
        T2_CMD = [PY, "-u", "scripts/p6_dock.py", "--stage", "1", "--exh", "1", "--max-evals", "0",
                  "--tag", "t2_other", "--workers", str(a.workers),
                  "--liglist", "docking/_liglists/tier2_other.txt", "--chunk", str(a.chunk)]
        attempt = 0
        while not os.path.exists(t2):
            attempt += 1
            if attempt > 10:
                log("⚠ Tier 2 重试 10 次仍无合表产物，终止流水线（不污染后续评分）")
                sys.exit(1)
            if n_vina() > 0:
                log(f"  [尝试 {attempt}] Tier 2 已在运行，等待其完成（中断则自动续跑）")
                if wait_for_completion(t2):
                    break
            log(f"  [尝试 {attempt}] 拉起 Tier 2（chunk 缓存会自动跳过已完成部分）")
            run(T2_CMD, "t2")
        if not os.path.exists(t2):
            log("⚠ Tier 2 合表仍未生成，终止流水线（不污染后续评分）")
            sys.exit(1)
        log("  ✔ Tier 2 合表已生成")
    else:
        log("步骤 2/5：Tier 2 产物已存在，跳过")

    # ---- 步骤 3：评分（多层合并 + 反向对照 + 四维排序）----
    if start <= 3:
        # 3a. 先尝试补 ChEMBL 实测活性阳性集（可选层，端点不可用则跳过）。
        #     rc==2 表示 EBI 端点探针失败，rc==3 表示"拒绝用空结果覆盖旧表"，
        #     两者都属预期内的降级，不是错误 → 继续走评分。
        rcp = os.path.join(TAB, "P6_reverse_control_positives.csv")
        if not os.path.exists(rcp):
            log("步骤 3a：抓取 ChEMBL 实测活性阳性集（可选增强层）")
            rc = run([PY, "-u", "scripts/p6_reverse_control.py"], "rc")
            if rc in (2, 3):
                log(f"  ChEMBL 层未取得（rc={rc}），按预期降级；评分改用 PAIN_PRIOR + DRH 两层")
            elif rc != 0:
                log(f"  ChEMBL 层异常 rc={rc}，同样降级继续")
        else:
            log("步骤 3a：ChEMBL 阳性表已存在，跳过")
        log("步骤 3b：四维评分与反向对照")
        # 【踩过的坑 · 已修 2026-09-19】旧写法无条件往下走，于是评分 rc=1 时链**照样**跑出图与报告
        # ——而图/报告读的是**上一轮的旧排序表**，产出"新合表 + 旧数字"的自相矛盾产物，且控制台
        # 一行 rc=1 淹没在长日志里，无人察觉（实测真发生过：Tier 2 合表落盘后评分崩，figs/report 照跑）。
        # 正确行为：**任一步失败即终止**，宁可没有图与报告，也不要错的图与报告。
        if run([PY, "-u", "scripts/p6_score.py", "--tags", "t1_cns,t2_other"], "score") != 0:
            log("⚠ 评分失败 → 终止流水线（不用旧表出图/出报告）")
            sys.exit(1)
    else:
        log("步骤 3/5：跳过")

    # ---- 步骤 4：出图 ----
    if start <= 4:
        log("步骤 4/5：生成图表")
        if run([PY, "-u", "scripts/p6_figures.py"], "figs") != 0:
            log("⚠ 出图失败 → 终止流水线")
            sys.exit(1)
    else:
        log("步骤 4/5：跳过")

    # ---- 步骤 5：报告 ----
    if start <= 5:
        log("步骤 5/5：生成 results/P6_RESULTS.md")
        if run([PY, "-u", "scripts/p6_report.py"], "report") != 0:
            log("⚠ 报告失败 → 终止流水线")
            sys.exit(1)
    else:
        log("步骤 5/5：跳过")

    log("P6 流水线链全部结束")


if __name__ == "__main__":
    main()
