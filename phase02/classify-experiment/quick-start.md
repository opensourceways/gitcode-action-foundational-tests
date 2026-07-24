# Phase 02 Classify-Experiment — 快速上手

## 背景

对每个 case YAML 的 **trigger + setup + fault_injection + 断言** 做可脚本化分析，
判断能否被 `workflow_runner.py` + `assertion_engine.py` 全自动执行。

---

## 一、完整工作流

### Step 1: 校验（validate）

将 case YAML 批量提交到平台 API 校验，按结果分组到 `VALID/`、`INVALID/`、`SKIP/`。

```bash
cd phase02/classify-experiment/2026-07-23
python3 batch_validate.py
# 输入: phase01/runs/2026-07-23-01/cases/yaml/ (369 cases)
# 输出: VALID/ INVALID/ SKIP/ + validation-results.json
```

### Step 2: 可脚本化分类（classify）

只对 `VALID/` 中的 case 做 trigger + assertion 自动化可行性分析。

```bash
python3 classify_20260723.py
# 输入: VALID/ (289 cases)
# 输出: classification_report.md
```

### Step 3: 无效案例分析（failure triage）

为 INVALID/ERROR 案例生成故障分析报告。

```bash
python3 failure/2026-07-24/gen_invalid_reports.py
# 输入: validation-results.json
# 输出: failure/2026-07-24/analysis/validation-invalid-74-cases.md
#       failure/2026-07-24/case/{CASE_ID}.md (74 per-case reports)
```

### Step 4: 分发/执行（dispatch）

对 `scriptable` 分类的 case，通过 API 触发执行。

```bash
python3 actions_ctl.py dispatch -w <workflow-name> --wait
# 或 python3 phase02/scripts/run_batch.py
```

---

## 二、最新批次结果（369 cases → 2026-07-23-01）

| 阶段 | 数量 | 占比 | 输出文件 |
|------|------|------|---------|
| 总输入 | 369 | 100% | `phase01/runs/2026-07-23-01/cases/yaml/` |
| VALID | 297 | 80.5% | `VALID/` (含 8 个 WAF 拦截但人工验证通过的 case) |
| INVALID | 66 | 17.9% | `INVALID/` + `failure/2026-07-24/` |
| SKIP (无 workflow) | 6 | 1.6% | `SKIP/` |

> **注意**: 8 个 case 在 API 校验时被 WAF 拦截（HTTP 418），经人工验证确认为合法 workflow，
> 已从 `ERROR_WAF/` 手动提升至 `VALID/`。这些 YAML 触发 WAF 的原因可能是：
> `${}` 表达式、反引号、URI 编码样式字符串等，需排查 WAF 规则。
>
> | case_id | 维度 | WAF 提升原因 |
> |---------|------|-------------|
> | COMP-ATOMGIT-01-049 | completeness | atomgit 边界格式校验 |
> | COMP-SCRIPT-01-082 | completeness | 脚本权限设置 |
> | COMPAT-TOKEN-01-001 | compatibility | ATOMGIT_TOKEN 有效性 |
> | COMPAT-TOKEN-01-002 | compatibility | GITHUB_TOKEN 空值映射 |
> | REL-LOG-01-040 | reliability | 100MB 超长日志 |
> | REL-OUTPUT-01-017 | reliability | step output 1MB+ 越界 |
> | SEC-NAME-01-002 | security | printenv 脱敏验证 |
> | USE-MASK-01-001 | usability | secret 脱敏文档描述 |

### 可脚本化分类（297 VALID → 分类报告）

| 分类 | 数量 | 占比 | 含义 |
|------|------|------|------|
| `scriptable` | 13 | 4.4% | push trigger + 全部断言可映射 |
| `api_blocked` | 35 | 11.8% | API 可行，平台不触发 |
| `untested` | 243 | 81.8% | workflow_dispatch 等未验证 |
| `fixture_gap` | 2 | 0.7% | 缺 repo fixture |
| `assertion_gap` | 4 | 1.3% | 断言需新 kind |

### INVALID 主要根因

| 类别 | 数量 | 典型错误 |
|------|------|---------|
| 未知字段 | 21 | `post.steps`, `run-name`, `environment`, `permissions` 等字段平台不支持 |
| concurrency | 12 | `exceed-action` 为空, `max < 1`, `preemption.events` 值非法 |
| cron 表达式 | 8 | 平台 cron 语法与标准不兼容 |
| if 表达式 | 8 | `failure()` 函数不识别（应用 `failed` 关键字） |

---

## 三、分类规则（基于 demo 实测）

### Trigger 层

| 触发事件 | API 调用链 | 平台是否触发 | 分类结论 |
|----------|-----------|-------------|---------|
| `push` | git push | ✅ | `scriptable` |
| `pull_request` | `POST /pulls` | ❌ | `api_blocked` — API 可行，平台不触发 |
| `pull_request_target` | `POST /pulls` (fork) | ❌ | `api_blocked` |
| `fork_pr` | `POST /forks` + `POST /pulls` | ❌ | `api_blocked` |
| `issue_comment` | `POST /issues` + `POST /comments` | ❌ | `api_blocked` |
| `pull_request_comment` | `POST /comments` (PR) | ❌ | `api_blocked` |
| `schedule` | push cron + wait | ⚠️ | `api_blocked` — 变通可行但不稳定 |
| `manual` / `workflow_dispatch` | dispatch API | ❓ | `untested` — 未验证 |
| `tag` | git tag + push | ❓ | `untested` — 未验证 |

### 分类标签

| 标签 | 含义 | 示例 |
|------|------|------|
| `scriptable` | trigger=push + 全部断言可映射 + 无 setup/fault 阻断 | 标准 push workflow |
| `api_blocked` | API 调用链已打通，但平台不触发 workflow | 所有 PR/issue_comment/schedule 事件 |
| `untested` | API 尚未验证（如 workflow_dispatch） | manual/tag 触发 |
| `fixture_gap` | trigger 可触发但缺 repo fixture | `with-cache`, `with-artifacts` |
| `fault_gap` | 需要故障注入基础设施 | `kill_runner`, `network_partition` |
| `assertion_gap` | trigger 可触发但断言需要新 kind | `artifact_download`, `pr_ui`, LLM |

### 断言层映射

| 断言 kind | 状态 | 说明 |
|----------|------|------|
| `status` | ✅ 已实现 | 所有 job/step 为绿 |
| `run_status` | ✅ 已实现 | conclusion 比对 |
| `value` | ✅ 已实现 | 日志包含期望值 |
| `leak` | ✅ 已实现 | 日志不包含明文 secret |
| `mask` | ✅ 已实现 | *** 命中 + 明文 0 命中 |
| `config_probe` | ✅ 已实现 | 前置资源探测 |
| `artifact_download` | ⚠️ 模式已证明 | API 已确认，待写入 engine |
| `cache_pollution` / `cache_restore` | ⚠️ 模式已证明 | 日志扫描 CACHE_HIT/CACHE_MISS |
| `pr_ui` / `run_ui` | ⚠️ 需 Playwright | 浏览器截图 + LLM 判定 |
| `eval=llm_assisted` | ⚠️ 需 LLM 集成 | 非确定性判定 |
| 其他新 target | ⚠️ 需新 kind | `runner_schedulable`, `error_message` 等 |

### Actor 层

| actor | 需要 | 状态 |
|-------|------|------|
| `maintainer` | bot token | ✅ 已配置 |
| `untrusted_contributor` | `CONTRIBUTOR_GITCODE_TOKEN` | ✅ 已配置，fork API 已验证 |

## 分类命令

```bash
cd phase02/classify-experiment/2026-07-23
python3 classify_20260723.py
# 输出: classification_report.md
```

## 运行案例 demo

```bash
cd phase02/classify-experiment/demo
python3 demo_artifact_assertion.py   # artifact 上传 → 下载 → 校验
python3 demo_cache_assertion.py     # cache 写 → 读 → 验证隔离
python3 demo_pr_trigger.py          # same-repo PR 创建
python3 demo_fork_pr.py             # fork → PR 全流程
python3 demo_issue_comment.py       # issue + comment 触发
python3 demo_schedule.py            # cron 触发等待
python3 demo_pull_request_target.py  # PR target 触发
```

## 核心结论（197 case 旧批次）

| 分类 | 旧标签 | 新标签 | 说明 |
|------|--------|--------|------|
| 107 | `full_scriptable` | `scriptable` | push trigger + 全部断言可映射 |
| 59 | `partial_scriptable` | `assertion_gap` / `fixture_gap` | trigger 可行但断言/环境缺 |
| 31 | `not_scriptable` | `api_blocked` | API 可行，平台不触发 |

## 目录结构

```
phase02/classify-experiment/
├── quick-start.md              ← 本文件
├── actions_ctl.py              ← dispatch/list/stop CLI
├── 2026-07-23/                 ← 批次目录
│   ├── batch_validate.py       ← 批量校验脚本
│   ├── classify_20260723.py    ← 分类脚本
│   ├── classification_report.md ← 分类报告输出
│   ├── validation-results.json ← 原始校验结果
│   ├── VALID/                  ← 通过校验的 case YAML
│   ├── INVALID/                ← 校验失败的 case YAML
│   ├── ERROR_WAF/              ← WAF 拦截的 case YAML (HTTP 418)
│   └── SKIP/                   ← 无 workflow 字段的 case YAML
├── demo/                       ← Demo 验证脚本
│   ├── demo_pr_trigger.py
│   ├── demo_fork_pr.py
│   ├── demo_schedule.py
│   ├── demo_issue_comment.py
│   ├── demo_pull_request_target.py
│   ├── demo_artifact_assertion.py
│   ├── demo_cache_assertion.py
│   └── demo_pr_ui_assertion.py
└── output/                     ← 旧批次报告

failure/2026-07-24/
├── analysis/
│   ├── failure-analysis-96-cases.md       ← 96 条运行失败交叉分析
│   └── validation-invalid-74-cases.md     ← 74 条校验失败分析
├── case/                       ← 逐 case 分诊报告
│   ├── COMP-ARTIFACT-01-002.md
│   ├── COMP-BOUND-01-085.md
│   └── ... (96+74 cases)
└── *.log                       ← 原始 job 日志
```

## Demo 验证结论（2026-07-24）

- `push` — 唯一平台会触发的 trigger
- `pull_request` / `pull_request_target` / `issue_comment` / `schedule` — API 全打通，平台均不触发
- `fork_pr` — 双账号 fork→PR 全流程自动化可行，平台不触发
- `workflow_dispatch` / `tag` / `manual` — 未验证
