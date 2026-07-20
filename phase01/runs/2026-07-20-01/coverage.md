# Coverage Report · Run 2026-07-20-01

> 对照 Phase 01 L0 基线（Parity Matrix + 风险登记册）的覆盖度分析。

## 1. 产出统计

| 维度 | Intent | 文本用例 | YAML | P0 | P1 |
|---|---|---|---|---|---|
| completeness | 24 | 25 | 25 | 1 | 24 |
| compatibility | 29 | 29 | 29 | 2 | 27 |
| security | 36 | 36 | 36 | 16 | 20 |
| reliability | 29 | 30 | 30 | 1 | 29 |
| usability | 23 | 22 | 22 | 1 | 21 |
| **合计** | **141** | **142** | **142** | **21** | **121** |

> 注：REL 多 1 条是因 REL-024 (needs→matrix 父级失败) 从 REL-022 拆分为独立用例。

## 2. Parity Matrix 覆盖

当前 Parity Matrix 仅 8 行模板数据（全部 ❓），逐一覆盖：

| 能力项 | 覆盖用例 | 状态 |
|---|---|---|
| `push` 触发 + branches 过滤 | COMP-TRIG-01-001, COMP-FILTER-01-001 | ✅ |
| `pull_request_target` | COMPAT-PRTGT-01-001, SEC-FORK-01-* (4) | ✅ |
| `${{ contains() }}` | COMP-EXPR-01-001, COMP-EXPRFN-01-001, COMPAT-EXPRBR-01-001 | ✅ |
| `concurrency` + cancel-in-progress | COMP-CONCUR-01-001, REL-CONCUR-01-* (4) | ✅ |
| 默认 `permissions` | COMP-PERM-01-001, SEC-PERM-01-* (3), COMPAT-PERMN-01-001 | ✅ |
| secret 日志 masking | SEC-MASK-01-* (6) | ✅ |
| `actions/checkout` 等价实现 | COMP-ACTION-01-001, COMPAT-BACTREF-01-001 | ✅ |
| `runs-on` 标签 | COMP-RUNNER-01-001, COMPAT-RUNON-01-001 | ✅ |

**结论**：Parity Matrix 当前 8 行全量覆盖。但 Matrix 本身仅模板数据，需人工补全真实能力项后做二次覆盖审计。

## 3. 风险登记册覆盖

| 风险项 | 优先级 | 覆盖用例 | 状态 |
|---|---|---|---|
| RISK-SEC-01 (fork PR 读到 secrets) | P0 | SEC-FORK-01-* (4), SEC-CACHE-01-001, SEC-ISOL-01-* (2), SEC-TOKEN-01-* (2) | ✅ |
| RISK-SEC-02 (不可信输入注入) | P0 | SEC-INJECT-01-* (7), SEC-PERM-01-* (3), SEC-EXPR-01-001 | ✅ |
| RISK-COMPAT-01 (兼容性差异) | P1 | 29 COMPAT 用例全覆盖 | ✅ |
| RISK-REL-01 (稳定性) | P1 | 30 REL 用例全覆盖 | ✅ |
| RISK-USE-01 (易用性/迁移摩擦) | P1 | 22 USE 用例全覆盖 | ✅ |

**结论**：5 个风险项全量覆盖。但风险登记册仅 5 行模板数据，建议补全。

## 4. testing-focus.md 12 章节覆盖

| 章节 | 覆盖 | 缺口 |
|---|---|---|
| §1 语法解析 | ✅ COMP-PARSE-01-001 | — |
| §2 触发器语义 | ✅ COMP-TRIG, COMPAT-PRTYPES, COMPAT-SCHED | — |
| §3 执行模型 | ✅ COMP-DAG/STAGES/MATRIX/POST/CONCUR | — |
| §4 Runner 环境隔离 | ⚠️ | 网络出站策略、预装工具链版本确认、容器逃逸 (盲区-E1) |
| §5 Secrets 与权限 | ✅ SEC-FORK/SEC-PERM/SEC-MASK | — |
| §6 表达式注入 | ✅ SEC-INJECT (7) | — |
| §7 复用与供应链 | ✅ SEC-SUPPLY, COMP-WFCALL, COMP-ACTION | Dependabot 等价机制未知 (盲区-E2) |
| §8 Artifact/Cache | ✅ COMP-ARTIFACT/CACHE, SEC-CACHE | — |
| §9 可观测性 | ✅ USE-STATE/USE-WFCMD/USE-SYSVAR | — |
| §10 兼容性差异 7 类 | ✅ 29 COMPAT 全类覆盖 | — |
| §11 迁移摩擦 | ✅ USE-MIGR/USE-MIGDOC/USE-INTYPE | — |
| §12 稳定性专项 | ⚠️ | CPU 饱和注入 (盲区-E3)，自托管 runner 离线恢复 (盲区-E4) |

## 5. 已知覆盖盲区（8 项）

| 盲区 ID | 描述 | 严重度 | 建议维度 | 状态 |
|---|---|---|---|---|
| E1 | 网络出站策略/预装工具链/容器逃逸 | P1 | reliability | 📋 后续补 |
| E2 | Dependabot 等价机制 | P1 | security | 📋 后续补 |
| E3 | CPU 饱和注入 | P1 | reliability | 📋 后续补 |
| E4 | 自托管 runner 离线恢复 | P1 | reliability | 📋 后续补 |
| E5 | OIDC / 短时凭据 | P0 | security | 📋 后续补 |
| E6 | `container.image` 支持 | P1 | completeness | 📋 后续补 |
| E7 | `environment` 字段 YAML 语法 | P1 | completeness | 📋 后续补 |
| E8 | `services:` 服务容器 | P1 | compatibility | 📋 后续补 |

**处置**：全部标记为「后续 `/phase01-update` 补」——已由人工在 STOP① 裁决。

## 6. 输入缺失影响

| 缺失输入 | 影响维度 | 降级程度 | 盲区关联 |
|---|---|---|---|
| `workflow-samples/` | compat, usability | 中等 | 迁移摩擦无真实负载验证 |
| `security-knowledge/` | security | 中等偏高 | E1/E2/E5 无针对性知识 |
| `platform-config/` | reliability | 中等 | 边界值测试用推断值 |
| `business-context/` | usability, risk | 低中等 | 优先级缺少实证锚点 |

---

*覆盖度报告生成时间：2026-07-20*
*对照基线：phase01/baseline/parity-matrix.md · risk-register.md · quality-gate.md*
