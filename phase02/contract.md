# 接口契约 · Phase 01 ↔ Phase 02 对齐文档

> 本文档定义 Phase 01（用例设计）与 Phase 02（执行与报告）之间的**唯一合法交接面**。
> 两份手册（`phase01.md` §7 与 `phase02.md` §2）以此文档为权威引用。

---

## 1. 交接物清单

Phase 01 交付给 Phase 02 的完整产物：

| 产物 | 路径 | 是否必需 | 说明 |
|---|---|---|---|
| 可执行 YAML 用例 | `phase01/runs/<run-id>/cases/yaml/*.yaml` | **必需** | 每条通过 schema 校验，字段遵循 `phase01/schema/executable-case.schema.yaml` |
| Feature Parity Matrix | `phase01/baseline/parity-matrix.md` | **必需** | 报告分维度聚合的参照 |
| 风险登记册 | `phase01/baseline/risk-register.md` | **必需** | P0/P1/P2 优先级来源 |
| 质量门禁 | `phase01/baseline/quality-gate.md` | **必需** | 报告判定「能否上线」的阈值依据 |
| 文本用例 | `phase01/runs/<run-id>/cases/text/*.md` | 参考 | 失败分析时回溯意图层描述，非执行输入 |

---

## 2. 合法输入定义

Phase 02 的 **唯一合法输入** 是可执行 YAML 用例，必须满足：

1. 文件位于 `phase01/runs/<run-id>/cases/yaml/`，扩展名 `.yaml` 或 `.yml`
2. 通过 `phase01/schema/executable-case.schema.yaml` 的完整校验
3. 字段含义与约束见下方 §3

Phase 02 **不接受的输入**：
- 未经 schema 校验的 YAML
- 直接手写的 workflow YAML（未经 Phase 01 意图→文本→编译链路）
- 非 Phase 01 产出的第三方用例

---

## 3. 可执行 YAML 契约（转述，以 schema 为准）

```yaml
id: SEC-FORK-01-001                 # 全局唯一，与文本用例共用同一 ID
dimensions: [security]              # 维度标签数组
dimension: security                 # 主维度
priority: P0                        # 取自风险登记册
title: fork PR 不应读取到仓库 secrets
intent_ref: INTENT-SEC-014          # 溯源到 Phase 01 意图库

setup:                              # 前置状态，Phase 02 harness 布置
  repo_fixture: with-secrets
  secrets: [DEPLOY_TOKEN]
  variables: {}
  branch_protection: default

workflow: |                         # ★ 被测 workflow 内联定义
  on: [pull_request_target]         #    Phase 02 yaml-compiler 据此编译 GitCode YAML
  jobs:
    echo:
      runs-on: default
      steps:
        - run: echo "$DEPLOY_TOKEN"

trigger:                            # Phase 02 workflow-runner 据此触发
  event: fork_pr
  as: untrusted_contributor
  params: {}

fault_injection: null               # 非 null 时 Phase 02 执行注入

assertions:                         # Phase 02 assertion-engine 据此判定
  - type: negative
    target: run_logs
    must_not_contain_secret: DEPLOY_TOKEN
  - type: positive
    target: run_status
    equals: blocked_or_no_secret_access

teardown:                           # Phase 02 env-manager 据此清理
  reset: fixture
```

---

## 4. 校验与拒收协议

### 4.1 Phase 02 启动校验（`/phase02-schema-check`）

Phase 02 执行前**必须**先对所有输入 YAML 逐条做 schema 校验：

- **通过**：进入执行队列
- **不通过**：拒收，生成《拒收清单》回报 Phase 01

### 4.2 拒收清单格式

```markdown
## 拒收清单 · 2026-07-20 执行批次

| 文件 | 错误字段 | 错误类型 | 说明 |
|---|---|---|---|
| SEC-FORK-01-001.yaml | assertions[0].type | enum violation | 值 `negativ` 不在 [positive, negative, nonfunctional] 中 |
| COMP-MATRIX-01-003.yaml | trigger | missing required | 缺少必填字段 `event` |
```

拒收清单抄送 Phase 01 的 orchestrator / review-gate，由 Phase 01 修复后重新编译 YAML。

### 4.3 纪律

- **绝不「尽力执行」残缺用例**：schema 校验不通过 = 不执行。这是保证边界干净的纪律。
- Phase 01 重编译 YAML（`/phase01-compile`）后，Phase 02 重新运行 `/phase02-schema-check`，消费新版。

---

## 5. 溯源链（不可断）

Phase 01 维护的溯源链延伸到 Phase 02：

```
风险项/能力项 → INTENT-xxx → 文本用例 ID → 派生 YAML(intent_ref) → Phase 02 执行结果(id)
```

- Phase 02 每条执行结果通过 `id` 回绑 Phase 01 文本用例。
- Phase 02 报告中的失败项可沿此链追溯到原始意图与风险项。
- 报告分维度聚合时，以 YAML 的 `dimension`/`dimensions` 字段为分组键。

---

## 6. 规范变更时的协作

当 GitCode Actions 规范变更时：

1. Phase 01 运行 `/phase01-compile`，从文本用例重新生成 YAML（文本用例基本不动）
2. Phase 02 运行 `/phase02-schema-check` 校验新版 YAML
3. Phase 02 重新执行受影响的用例（增量，非全量）
4. Phase 02 更新报告

**关键**：Phase 02 的脚本（api-client / assertion-engine 等）**不因规范变更而改动**——只有 YAML 编译 agent 需要适配新规范。这正是两层表示（文本←→YAML）的设计收益。

---

## 7. Phase 02 产出物 → Phase 01 回流传导

| Phase 02 产出 | 回流对象 | 作用 |
|---|---|---|
| 拒收清单 | Phase 01 review-gate | 修复 YAML 再编译 |
| 失败用例 + LLM 根因初判 | Phase 01 orchestrator | 定位用例问题 / 补充意图 |
| LLM 衍生用例建议 | Phase 01 review-gate | 评审后纳入意图库 |
| Flaky 标记 | Phase 01 reliability agent | 审查稳定性用例质量 |
| 易用性 LLM 评分 | Phase 01 usability agent | 校准「可理解性」判据 |

---

## 8. 版本记录

| 日期 | 变更 | 发起方 |
|---|---|---|
| 2026-07-20 | 初始版本 | Phase 02 创建 |
