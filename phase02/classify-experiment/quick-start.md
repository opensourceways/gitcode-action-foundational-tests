# Phase 02 Classify-Experiment — 快速上手

## 背景

`phase01/runs/2026-07-21-02/cases/` 下有 197 个 case（YAML + Markdown）。
目标是逐个分析每个 case 的 **trigger + setup + fault_injection + 断言**，判断能否被 Phase 02 的执行器 (`workflow_runner.py` + `assertion_engine.py`) 全自动执行。

## 目录文件

### 分类脚本

| 文件 | 说明 |
|------|------|
| `classify_cases.py` | v1 — 只按断言分类（trigger/setup/fault 未考虑） |
| `classify_cases_v2.py` | **v2（推荐）** — 全维度分类：trigger + setup + fault_injection + 断言 |
| `api_gap_analysis.py` | v1 API 缺口分析（有 bug，已废弃） |
| `api_gap_analysis_v2.py` | v2 API 缺口分析 |

### 分类结果

| 文件 | 说明 |
|------|------|
| `classification_report.md` | v1 逐 case 明细报告 |
| `classification_v2_report.md` | **v2 逐 case 明细报告（2791行）** |
| `classification_v2.csv` | **v2 CSV 表格（推荐直接看这个）** |
| `classification_v2_detail.json` | v2 机器可读 JSON |

### 操作工具

| 文件 | 说明 |
|------|------|
| `actions_ctl.py` | **GitCode Actions dispatch / stop CLI 工具** |
| `run-case.sh` | Phase 02 最小闭环执行脚本（单 case 部署+跑+断言） |

## 快速上手

### 1. 生成分类报告

```bash
cd phase02/classify-experiment
python3 classify_cases_v2.py
# 输出: classification_v2_report.md, classification_v2.csv, classification_v2_detail.json
```

### 2. 查看分类结果（推荐先看 CSV）

```bash
# 看总体统计
head -20 classification_v2_report.md

# 只看 full_scriptable 的 case
grep full_scriptable classification_v2.csv

# 只看 not_scriptable 的 case
grep not_scriptable classification_v2.csv
```

### 3. 使用 actions_ctl 操作 workflow

**前置条件**：从浏览器 F12 抓包获取 `GITCODE_COOKIE`，写入 `.env`：

```bash
cd phase02          # 项目根目录（.env 在这里）
echo 'GITCODE_COOKIE=<your-cookie>' >> .env
echo 'GITCODE_ACCESS_TOKEN=<your-token>' >> .env   # v8 API 轮询用
```

```bash
# 列出某个项目的所有 workflow
python3 classify-experiment/actions_ctl.py list -p ComputingActionTest/foundational-tests

# 手动触发
python3 classify-experiment/actions_ctl.py dispatch -p ComputingActionTest/foundational-tests -w PILOT-BASIC

# 触发 + 等待完成
python3 classify-experiment/actions_ctl.py dispatch -p ComputingActionTest/foundational-tests -w PILOT-BASIC --wait

# 带 inputs 触发
python3 classify-experiment/actions_ctl.py dispatch -p ComputingActionTest/foundational-tests \
  -w some-workflow -i '{"key":"value"}' --wait

# 停止运行中的 run
python3 classify-experiment/actions_ctl.py stop -p ComputingActionTest/foundational-tests -r <workflow_run_id>
```

### 4. 执行单个 case（全体）

```bash
export GITCODE_ACCESS_TOKEN=<token>
export GITCODE_EXECUTOR=<你的 GitCode 用户名>

# 执行一个 case
./classify-experiment/run-case.sh phase01/runs/2026-07-21-02/cases/yaml/COMP-ENV-02-001.yaml test-run-01
```

## 核心结论

### 分类结果（197 case 总计）

| 分类 | 数量 | 含义 |
|------|------|------|
| `full_scriptable` | 107 (54.3%) | trigger=push + 全部断言可映射 + 无阻断 |
| `partial_scriptable` | 59 (29.9%) | trigger=push 但存在 LLM/新 target/未知 fixture 阻断 |
| `not_scriptable` | 31 (15.7%) | trigger 非 push（fork_pr/manual/schedule/pr） |

### 按维度

| 维度 | full | partial | not | 主要阻断原因 |
|------|------|---------|-----|-------------|
| completeness | 21 | 6 | 2 | 未知 fixture |
| compatibility | 39 | 16 | 6 | pr/manual trigger |
| reliability | 25 | 10 | 5 | fault_injection + schedule |
| security | 17 | 8 | 15 | fork_pr + untrusted_contributor |
| usability | 5 | 19 | 3 | llm_assisted + error_message |

### API 状态（所有阻断项对应的 API 均已确认存在）

| 端点 | 状态 |
|------|------|
| `POST web-api.gitcode.com/api/v2/.../actions/workflows/{id}/dispatch` | ✅ `actions_ctl.py` 已验证 |
| `POST web-api.gitcode.com/api/v2/.../actions/workflow-runs/{id}/stop` | ✅ `actions_ctl.py` 已验证 |
| `POST api.gitcode.com/api/v5/repos/{o}/{r}/pulls` | ✅ 文档已收录 |
| `POST api.gitcode.com/api/v5/repos/{o}/{r}/forks` | ✅ 文档已收录 |
| `POST api.gitcode.com/api/v5/repos/{o}/{r}/pulls/{n}/comments` | ✅ 文档已收录 |

### 非 API 问题（需其他方案）

| 阻断 | 数量 | 方案 |
|------|------|------|
| `eval=llm_assisted` | 44 | LLM 集成到 assertion_engine |
| `trigger.as=untrusted_contributor` | 17 | 第二 GitCode 账号 |
| `schedule` trigger | 5 | 改为 push + 手动设 `ATOMGIT_EVENT_NAME=schedule` |
| `target=run_ui / pr_ui` | 4 | Playwright 浏览器自动化 |
| `fault_injection` | 5 | runner kill / network_partition infra |
| 未知 `repo_fixture` | ~18 | 预先创建配置好的测试仓 |
