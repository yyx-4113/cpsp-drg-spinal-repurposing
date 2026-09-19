# GitHub 存缴操作手册（中文）· `cpsp-drg-spinal-repurposing`

> 目的：把本工作目录**平铺**为仓库根，一次性推上 GitHub，并建立"打 tag → 自动 Release → Zenodo 取 DOI"的可引用链路。
> 平铺纪律：仓库根 = 工作目录 `D:\2026.9\极速交付9月会员日优惠套路\01_AI生信-虚拟多重筛药\慢性疼痛`。
> **账号纪律：科研仓库一律用 `yyx-4113`。** 早年课程作业账号 `yongxinyang` 与本项目无关，**不得**在任何稿件或仓库中出现。

---

## 0. 前置检查（推送前必做）

- [ ] `README.md` 的文件地图与 `scripts/` 实际文件名一致（改过脚本名就要同步改 README）
- [ ] `CITATION.cff` 的 ORCID / 单位 / 邮箱正确
- [ ] `.gitignore` 已排除 `data/`、`docking/out/`、`docking/ligands/`、`docking/receptors/`、`scripts/*.out`、`scripts/*.err`
- [ ] **数据可用性声明写的是实名仓库 URL，不是 "available on request"**
- [ ] 稿件里每个数字都能在 `results/tables/` 找到出处；`results/*_RESULTS.md` 已重新生成到最新
- [ ] 中间/合成产物已隔离（本项目的合成自检产物统一带 `_SYNTHETIC_` 或 `_QC_` 前缀，**不得**被当作正式结果引用）

快速自检命令：

```bash
# 1) 确认没有大文件混进暂存区（>10 MB 就该是排除对象）
git ls-files -z | xargs -0 du -h 2>/dev/null | sort -hr | head -20

# 2) 确认关键文件都在
for f in README.md PROJECT_PLAN.md CITATION.cff LICENSE .gitignore \
         .github/workflows/release.yml GITHUB_DEPOSIT_SOP.md author_verification_statement.md; do
  [ -f "$f" ] && echo "OK  $f" || echo "MISSING  $f"
done

# 3) 确认脚本目录里没有日志/临时文件被纳入
git status --short | grep -E '\.(out|err)$' && echo "⚠ 有日志文件待提交，检查 .gitignore" || echo "OK  无日志文件"
```

---

## 1. 首次建仓与推送

```bash
# 1.1 初始化（若目录尚未是 git 仓库）
git init -b main

# 1.2 配置身份（仅本仓库；不要设成全局以免影响其他账号）
git config user.name  "Yongxin Yang"
git config user.email "960856791@qq.com"

# 1.3 查看将被提交的内容（务必人工过一眼，确认大文件已被排除）
git add -A
git status --short | head -50
git ls-files | wc -l

# 1.4 首次提交
git commit -m "CPSP DRG-spinal-axis target lock-in and approved-drug repurposing: code, derived tables, figures"

# 1.5 在 GitHub 网页端用 yyx-4113 账号新建**空**仓库 cpsp-drg-spinal-repurposing
#     （不要勾选 README / .gitignore / LICENSE，避免与本地冲突）
git remote add origin https://github.com/yyx-4113/cpsp-drg-spinal-repurposing.git

# 1.6 推送
git push -u origin main
```

若 1.5 之前已误建了带 README 的仓库：

```bash
git remote add origin https://github.com/yyx-4113/cpsp-drg-spinal-repurposing.git
git fetch origin
git rebase origin/main     # 或 git pull --rebase origin main
git push -u origin main
```

---

## 2. 打 tag 触发自动 Release

`.github/workflows/release.yml` 会在 `v*.*.*` tag 推送时自动：
1. 生成 `MANIFEST.sha256`（`results/tables`、`results/figures`、`results/*.md` 的 SHA-256 清单）；
2. 创建 Release 并附上该清单 + GitHub 自动生成的源码压缩包。

```bash
git tag -a v1.0.0 -m "Manuscript submission snapshot v1.0.0"
git push origin v1.0.0
```

之后在仓库 **Actions** 页确认 workflow 成功，在 **Releases** 页确认 `v1.0.0` 出现且含 `MANIFEST.sha256`。

> 本地校验清单（评审人视角）：
> ```bash
> sha256sum -c MANIFEST.sha256     # 在 results/ 同级目录执行
> ```

---

## 3. Zenodo 取 DOI（InvenioRDM 新接口）

1. 用 **GitHub 账号 `yyx-4113`** 登录 <https://zenodo.org> → Settings → GitHub → 打开 `cpsp-drg-spinal-repurposing` 的开关。
2. 回到 GitHub，**重新推一个新 tag**（如 `v1.0.1`）——Zenodo 只在授权后的**新** release 上建记录，已存在的 `v1.0.0` 不会被追溯。
3. Zenodo 会自动生成 DOI（形如 `10.5281/zenodo.XXXXXXX`），在 Zenodo 记录页把 metadata（作者 ORCID、单位、关键词、License=MIT）补全。
4. 若走 **InvenioRDM 新接口**手工上传（不经 GitHub 联动），流程为：创建 draft record → 注册文件 → 上传文件 → 发布取 DOI。注意 draft 与 published 是两套 URL，稿件里引用 **published** 的那个。

**拿到 DOI 后必须回填的三处：**

| 位置 | 回填内容 |
|---|---|
| `README.md` §7 Data availability | `mirrored to Zenodo with DOI 10.5281/zenodo.XXXXXXX` |
| `CITATION.cff` | 追加 `doi:` 与 `version:`（并让 version 与 tag 一致） |
| 稿件 Data availability | 实名仓库 URL + Zenodo DOI（**禁止** "available on request"） |

---

## 4. 后续更新（改结果 / 改脚本）

```bash
git add -A
git commit -m "Update P6 scoring tables after Tier-2 completion"
git push

# 有实质变更时递增版本号（语义化：修数字=patch，加分析=minor）
git tag -a v1.0.1 -m "Sync tables to final Tier-2 results"
git push origin v1.0.1
```

> **铁律**：稿件引用的版本一经投稿就不覆盖。任何重新跑出来的数字若要替换，一律**新 tag**，
> 并在稿件 Data availability 里把 DOI 改成新的那个；不要 force-push 已发布的 tag。

---

## 5. 常见坑

| 现象 | 原因 | 处理 |
|---|---|---|
| push 被拒 `file is 118 MB; exceeds GitHub's file size limit` | 大文件（`.pdbqt` / 矩阵 / gz）混进了提交 | `git rm --cached <path>` → 补进 `.gitignore` → 若已在历史里则用 `git filter-repo` 清理后重推 |
| Release workflow 没触发 | tag 不是 `v*.*.*` 形式，或 workflow 文件不在 `main` 上 | 用 `v1.0.0` 这类 tag；确认 workflow 已 push 到默认分支 |
| Zenodo 没生成 DOI | 授权开关是在 release **之后**才打开的 | 推一个**新** tag（如 `v1.0.1`）触发 |
| 稿件数字与仓库对不上 | 先生成稿件数字、后跑脚本，或反之 | 定稿流程固定为：**跑完 → 重生成 `results/*_RESULTS.md` → 再誊数字进稿件**（本项目铁律："跑完再定稿"） |
| README 链接 404 | 文件改名/移动后 README 未同步 | 每次改脚本名，同时 `grep -n` 一遍 README 与 `PROJECT_PLAN.md` 里的引用 |
