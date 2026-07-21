# Agents 设计

本目录定义 Phase 01「测试用例设计」团队的 agent。团队不直接按产品模块拆分，而是按测试责任维度分工：先并行发现风险和测试意图（intent），再集中评审，最后生成可交付的用例。这使覆盖度、优先级和用例数量都可被审计，而不是由单个 agent 一次性决定。

完整流程见 [`../process.md`](../process.md)，全局约束见 [`../rules.md`](../rules.md)。本目录中的每个 `CLAUDE.md` 是对应角色的执行说明和行为契约。

## 设计目标

- **意图先行**：分析角色只回答「测什么、为什么测、预期什么」，不直接编写执行细节；只有通过门禁的 intent 才能展开为用例。
- **责任分离**：发现风险、管理覆盖度、审批准入、编写用例分别由不同角色承担，避免自审自批。
- **以证据为依据**：优先级来自风险登记册，期望结果（oracle）来自 GitCode 规格、GitHub Actions 语义或已声明差异。
- **可追溯和可复现**：每条产物应能形成“能力/风险项 → intent → 文本用例 → YAML”的链路；过程产物保存在对应 `runs/<run-id>/` 中。
- **文本稳定、YAML 可再生**：文本用例是评审和归档的 source of truth；可执行 YAML 是依据当前平台规范生成的派生物。

## 角色划分

| Agent | 职责 | 主要产出 |
|---|---|---|
| [`spec-analyst/`](spec-analyst/) | 将 GitCode 规格整理为带出处、约束、默认值和置信度的能力清单 | `intents/spec.md` |
| [`compat-diff/`](compat-diff/) | 对照 GitHub Actions 与 GitCode，发现兼容性疑点并明确 oracle 对齐方向 | `intents/compat.md` |
| [`security/`](security/) | 从信任边界和 CI/CD 攻击面出发，设计防御性负向验收目标 | `intents/security.md` |
| [`reliability/`](reliability/) | 覆盖配额边界、并发、故障注入与恢复行为 | `intents/reliability.md` |
| [`usability/`](usability/) | 从迁移开发者视角检查报错、文档、调试和迁移摩擦 | `intents/usability.md` |
| [`orchestrator/`](orchestrator/) | 维护全局覆盖坐标系，汇总、聚类、排序 intent 并暴露盲区 | `intent-library.md`、`gate-log.md` |
| [`review-gate/`](review-gate/) | 独立审计 intent 的重复性、可测性、优先级和维度覆盖，决定是否准入 | 准入/打回/盲区记录 |
| [`case-writer/`](case-writer/) | 将准入 intent 展开为文本用例，并按 GitCode 规范编译为 YAML | `cases/text/`、`cases/yaml/`、`case-manifest.md` |

其中前五个角色是**维度分析 agent**。它们可在阶段 A 并行工作；`orchestrator` 与 `review-gate` 是收敛与治理角色；`case-writer` 是唯一可以创建交付用例的角色。

## 协作流

```text
inputs/ + baseline/
        │
        ▼
阶段 A：五个维度分析 agent 并行产生 intent
        │
        ▼
orchestrator 汇总、去重、风险映射、覆盖度建模
        │
        ▼
review-gate 审计并输出准入清单 ── STOP①：人工确认
        │
        ▼
case-writer：intent → 文本用例 → 可执行 YAML
        │
        ▼
coverage.md + DoD ──────────────────── STOP②：交付确认
```

阶段之间通过落盘文件协作，而不是依赖隐式会话状态。这样既允许阶段 A 并行，又让任意一次 run 都能在之后复核、重跑或增量更新。

## 关键边界与护栏

- 维度分析 agent 停在 intent 层；不得越过门禁自行展开用例，也不应把 GitCode YAML 语法写入 intent。
- `orchestrator` 负责全局排序和盲区呈现，但不自造风险项或优先级；缺少依据时应回写为待确认事项。
- `review-gate` 只决定准入，不为凑齐覆盖度而隐瞒盲区；每个 blocker 风险要么被准入 intent 覆盖，要么明确记录为盲区。
- `case-writer` 只处理已准入的 intent，并必须复用历史基底、仅生成差异，避免跨 run 重复造用例。
- 安全角色及所有下游产物仅描述防御性验收目标；不得包含真实密钥、攻击 payload、可利用 exploit 或绕过步骤。
- 破坏性场景仅面向隔离且可重置的测试环境，并声明恢复预期和 `teardown.reset` 级别。

## 产物与溯源

每次运行以 `runs/<run-id>/` 为边界。agent 的最小交接链为：

```text
Parity Matrix / 风险登记册
  → INTENT-<DIM>-<N>
  → <DIM>-<TOPIC>-<RUN>-<N>.md
  → 同 ID 的 .yaml
```

文本用例必须保留 `intent_ref`、维度、优先级、预期结果和可确定性验证点；YAML 必须以同一 ID 引用 intent，并通过 [`../schema/`](../schema/) 校验。安全用例还必须在文本和 YAML 中体现“**不应发生**”的负向断言。

## 新增或修改角色

新增 agent 时，应新建 `<agent-name>/CLAUDE.md`，并至少定义：角色边界、输入、工作步骤、输出位置、质量清单和护栏。若角色会影响 intent 格式、门禁、命名、优先级或溯源链，也必须同步更新 [`../process.md`](../process.md)、[`../rules.md`](../rules.md) 和相关模板；不要仅通过提示词引入未记录的流程约定。
