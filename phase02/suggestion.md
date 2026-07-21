# Phase 02 run-case.sh 用例分类与扩展建议

## 背景

当前 `run-case.sh` 是一个单体脚本，处理所有 249 个用例的执行。随着用例类型增多，脚本的断言引擎（146-166 行）硬编码了 `step-value`、`ATOMGIT_WORKSPACE`、`TEST_VAR` 三个具体字符串，扩展性差。

## 用例分类

基于对 249 个 YAML 用例的完整分析，建议按 **执行剖面（Execution Profile）** 分为 5 大类：

| 类别 | 名称 | 数量 | 占比 | 核心差异点 |
|---|---|---|---|---|
| **A** | 标准推送 | ~196 | 78.7% | push 触发 + deterministic 断言 + fixture 清理 |
| **B** | PR/Fork 隔离 | ~42 | 16.9% | 需要创建 PR/Fork，untrusted 角色，安全断言 |
| **C** | 故障注入 | ~11 | 4.4% | fault_injection 编排 + full_instance 清理 |
| **D** | API 触发 | ~10 | 4.0% | workflow_dispatch/manual/schedule，需 API 调用触发 |
| **E** | LLM 辅助判定 | ~30 | 12% | eval=llm_assisted，需 AI 判定（与 A-D 正交叠加） |

---

### A 类 — 标准推送（Standard Push）

**特征：**
- `trigger.event`: `push`
- `trigger.as`: `maintainer`
- `fault_injection`: `null`
- `teardown.reset`: `fixture`
- `assertions.eval`: `deterministic`

**脚本行为：** 当前 `run-case.sh` 已完整支持。部署 workflow → git push → 轮询 → 收集日志 → 确定性断言 → 写结果。

**断言子类型（需插件化）：**

| 断言 target | 数量 | 判定逻辑 |
|---|---|---|
| `run_logs` | 293 | 日志内容 grep/正则匹配 |
| `step_logs` | 132 | 步骤级日志匹配（需先按 step 切分） |
| `run_status` | 126 | conclusion 值比对 |
| `error_message` | 15 | 错误信息匹配 |
| `job_status` | 6 | job 级状态检查 |

---

### B 类 — PR/Fork 隔离（Cross-Repo Security）

**特征：**
- `trigger.event`: `fork_pr` / `pull_request` / `pull_request_target` / `pr`
- `trigger.as`: `untrusted_contributor`
- `setup.repo_fixture`: `with-fork*`
- `assertions.type`: 以 `negative` 为主

**脚本差异：** 需要额外步骤——创建 fork 仓库 → 在 fork 上创建 PR → 触发 CI → 验证隔离行为（如 artifact 不可访问、secret 不泄露）。

---

### C 类 — 故障注入（Fault Injection / Chaos）

**特征：**
- `fault_injection`: 非 null（`kill_runner` / `network_partition` / `disk_full` / `cpu_saturate` / `concurrent_flood`）
- `fault_injection.at`: `pre_job` / `mid_job` / `post_job`
- `teardown.reset`: 多为 `full_instance`

**脚本差异：** 需要在 job 执行到特定阶段时注入故障 → 验证 `recovery_expectation` → 完整环境重建。

---

### D 类 — API 触发（Manual / Scheduled）

**特征：**
- `trigger.event`: `workflow_dispatch` / `manual` / `schedule` / `issue_comment` / `pull_request_comment`

**脚本差异：** 不能靠 git push 触发，需要调用 GitCode API 的 `CreateWorkflowDispatchEvent` 端点，或等待 schedule 触发。

---

### E 类 — LLM 辅助判定（正交叠加）

**特征：**
- `assertions.eval`: `llm_assisted`（30 条）
- 有 `rubric` 字段作为判定标准

**脚本差异：** 断言阶段不执行确定性规则，而是将日志 + rubric 发送给 LLM 判定。E 类与 A-D 正交（任何类都可能包含 LLM 断言）。

---

## 建议的脚本重构方向

```
phase02/scripts/
├── run-case.sh              # 主入口，按类别分发
├── lib/
│   ├── trigger/
│   │   ├── push.sh          # A 类：git push 触发
│   │   ├── fork-pr.sh       # B 类：fork + PR 触发
│   │   └── api-dispatch.sh  # D 类：API 触发
│   ├── assert/
│   │   ├── run-logs.sh      # target=run_logs
│   │   ├── step-logs.sh     # target=step_logs
│   │   ├── run-status.sh    # target=run_status
│   │   ├── error-msg.sh     # target=error_message
│   │   └── llm-judge.sh     # E 类：LLM 判定
│   ├── fault-inject.sh      # C 类：故障注入编排
│   └── teardown.sh          # fixture / full_instance / none
```

**核心原则：** 按 **触发方式**（A/B/C/D）决定部署和轮询策略，按 **断言 target**（run_logs/step_logs/run_status/...）决定判定策略，E 类（LLM）作为断言策略的一种正交叠加。这样新增一种断言 target 只需加一个 `assert/xxx.sh`，不影响其他逻辑。

---

## 全局统计数据

### trigger.event 分布

| 事件类型 | 数量 | 占比 |
|---|---|---|
| `push` | 196 | 78.7% |
| `fork_pr` | 23 | 9.2% |
| `pull_request` | 9 | 3.6% |
| `pull_request_target` | 7 | 2.8% |
| `manual` | 4 | 1.6% |
| `workflow_dispatch` | 3 | 1.2% |
| `schedule` | 3 | 1.2% |
| `pr` | 2 | 0.8% |
| `pull_request_comment` | 1 | 0.4% |
| `issue_comment` | 1 | 0.4% |

### assertions.target 分布

| target 类型 | 数量 |
|---|---|
| `run_logs` | 293 |
| `step_logs` | 132 |
| `run_status` | 126 |
| `error_message` | 15 |
| `yaml_validation` | 6 |
| `job_status` | 6 |
| `summary_ui` | 3 |
| `step_status` | 2 |
| `pod_count` | 2 |
| `trigger_behavior` | 1 |
| `step_list` | 1 |
| `queue_ui` | 1 |

### teardown.reset 分布

| reset 类型 | 数量 | 占比 |
|---|---|---|
| `fixture` | 203 | 81.5% |
| `none` | 36 | 14.5% |
| `full_instance` | 10 | 4.0% |
