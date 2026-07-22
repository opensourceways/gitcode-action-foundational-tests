# 输入清单总表（INPUTS）

> Phase 02 脚本/agent 启动前必须确认所有输入到位。**缺输入不会让流程崩，但会阻断执行并回报缺失项。**

## 快速自检（跑 `/phase02-exec` 前）

| 输入 | 必需度 | 来源 | 放置位置 | 到位了吗 |
|---|---|---|---|---|
| 可执行 YAML 用例 | **必需** | Phase 01 `/phase01-gen` 产出 | `phase01/runs/<run-id>/cases/yaml/` | ☐ 待 Phase 01 DoD |
| API Access Token | **必需** | GitCode OAuth2.0 授权 | 环境变量 `GITCODE_ACCESS_TOKEN` | ☐ |
| Feature Parity Matrix | **必需** | Phase 01 L0 基线 | `phase01/baseline/parity-matrix.md` | ✅ (Phase 01) |
| 风险登记册 | **必需** | Phase 01 L0 基线 | `phase01/baseline/risk-register.md` | ✅ (Phase 01) |
| 质量门禁 | **必需** | Phase 01 L0 基线 | `phase01/baseline/quality-gate.md` | ✅ (Phase 01) |
| GitCode API 参考 | **必需** | Phase 01 inputs | `phase01/inputs/gitcode-api/api-reference.md` | ✅ (Phase 01) |
| GitCode Actions 规格 | **必需** | Phase 01 inputs | `phase01/inputs/gitcode-spec/` | ✅ (Phase 01) |
| 平台配置 | 建议 | 人工填写 | `phase01/inputs/platform-config/` | ☐ |
| Runner 访问凭证 | 条件必需 | 测试实例管理员 | 环境变量 `GITCODE_RUNNER_SSH_KEY` | ☐ |
| IaC 配置 | 条件必需 | `full_instance` 级重置需要 | `phase01/inputs/platform-config/` 或 IaC 仓库 | ☐ |

---

## 各类输入明细

### 1. 可执行 YAML 用例（必需）

- **来源**：Phase 01 通过 DoD 验收后，`runs/<run-id>/cases/yaml/*.yaml`
- **格式**：符合 `phase01/schema/executable-case.schema.yaml` 的 YAML 文件
- **消费方**：主链路（schema_check → run_case[preflight 检查+执行] → assertion_engine → report_builder）；yaml-checker 为**检查器**（合规检查，不编译）
- **缺失影响**：无输入则无法执行——这是 Phase 02 的唯一合法输入。
- **版本追踪**：执行时记录 Phase 01 run-id + YAML 文件 hash 清单 → `runs/<run-id>/run.md`

### 2. API Access Token（必需）

- **来源**：GitCode OAuth2.0 授权流程（`https://docs.gitcode.com/docs/apis/oauth`）
- **格式**：字符串，通过环境变量 `GITCODE_ACCESS_TOKEN` 注入
- **消费方**：api-client 脚本（所有 API 调用的认证凭据）
- **权限要求**：
  - `repo` 读写（创建/删除仓库、push workflow）
  - `actions` 读写（查看 run、下载日志、管理 artifacts）
  - `runner` 读取（查看 runner 状态）
- **缺失影响**：阻断执行。token 过期时需刷新。
- **安全要求**：token 只通过环境变量注入，不出现在日志/报告中。脚本中引用为 `$GITCODE_ACCESS_TOKEN`，不硬编码。

### 3. Feature Parity Matrix（必需）

- **来源**：Phase 01 的 L0 基线产物 `phase01/baseline/parity-matrix.md`
- **格式**：Markdown 表格（能力清单 × 支持状态）
- **消费方**：report-builder（报告分维度聚合的参照）、yaml-checker（兼容性检查的参照）
- **Phase 02 不修改此文件**

### 4. 风险登记册（必需）

- **来源**：Phase 01 的 L0 基线产物 `phase01/baseline/risk-register.md`
- **格式**：Markdown（风险项 × 影响 × 概率 × 维度 × 优先级）
- **消费方**：report-builder（P0/P1/P2 优先级来源）、harness-orchestrator（执行排序）
- **Phase 02 不修改此文件**

### 5. 质量门禁（必需）

- **来源**：Phase 01 的 L0 基线产物 `phase01/baseline/quality-gate.md`
- **格式**：Markdown（分维度阈值 + blocker 判定规则）
- **消费方**：report-builder（报告门禁判定的阈值依据）
- **Phase 02 不修改此文件**

### 6. GitCode API 参考（必需）

- **来源**：Phase 01 `inputs/gitcode-api/api-reference.md`（已补充，20 个 v8 Actions 端点）
- **格式**：Markdown
- **消费方**：api-client（API 调用参照）、yaml-checker（API 断言型用例）
- **Phase 02 直接引用 Phase 01 的文件，不复制一份。**

### 7. GitCode Actions 规格（必需）

- **来源**：Phase 01 `inputs/gitcode-spec/`（官方文档离线镜像）
- **格式**：Markdown
- **关键文件**（yaml-checker 尤其需要）：
  - `top-level-fields.md`（顶层字段定义）
  - `trigger-events.md`（触发器语法）
  - `core-concepts/workflow-job-step-action.md`（workflow 结构）
  - `core-concepts/variables-secrets-context-expressions.md`（secrets/表达式）
  - `COMPAT-NOTES.md`（已知兼容性差异）
  - `examples/`（官方示例）
- **消费方**：yaml-checker 检查器（合规检查的权威语法依据）、failure-analyst（对照规格判断产品缺陷）、run_case 的 preflight（VALIDATION-RULES 来源）
- **Phase 02 直接引用 Phase 01 的文件。**

### 8. 平台配置（建议）

- **来源**：人工填写（测试实例的实际配置参数）
- **格式**：Markdown / YAML
- **内容**：
  - GitCode 实例 Base URL（若不同于 `https://api.gitcode.com`）
  - Runner 标签与规格（CPU/内存/磁盘）
  - 可用 fixture 模板列表
  - 最大并发 workflow 数
  - Job/run 超时上限
  - Artifact/cache 大小限制
- **消费方**：env-manager（fixture 选择、环境配置）、workflow-runner（超时/并发控制）、yaml-checker（runner 标签映射）
- **缺失影响**：yaml-checker 使用默认 runner 标签（可能不可用），workflow-runner 使用默认超时。

### 9. Runner 访问凭证（条件必需）

- **条件**：需要做故障注入（`fault_injection`）的用例
- **来源**：测试实例管理员
- **格式**：SSH private key，通过环境变量 `GITCODE_RUNNER_SSH_KEY` 注入
- **消费方**：workflow-runner（故障注入时 SSH 到 runner 执行 kill/saturate/partition）
- **缺失影响**：故障注入类用例跳过执行（标记 `SKIPPED: no runner access`）

### 10. IaC 配置（条件必需）

- **条件**：需要 `full_instance` 级重置的用例
- **来源**：测试实例的 Terraform/Ansible 配置
- **格式**：IaC 文件（`.tf` / `.yml`）
- **消费方**：env-manager（`full_instance` 重置时 terraform destroy/apply）
- **缺失影响**：`full_instance` 级用例跳过执行（标记 `SKIPPED: no IaC config`）

---

## 环境变量一览

```bash
# 必需
export GITCODE_ACCESS_TOKEN="your_oauth_token"
export GITCODE_API_BASE_URL="https://api.gitcode.com"  # 默认值

# 条件必需
export GITCODE_RUNNER_SSH_KEY="/path/to/runner_key"     # 故障注入需要
export TF_VAR_gitcode_instance_id="test-instance-01"     # full_instance 重置需要

# 可选
export GITCODE_TEST_ORG="test-org"                       # 测试组织名（默认从 token 推断）
export PHASE02_CONCURRENCY=4                             # 最大并发执行数
export PHASE02_CASE_TIMEOUT=1800                         # 每条用例默认超时（秒）
```

## 放置约定

- Phase 02 的大部分输入**直接引用 Phase 01 的文件**（不复制）：API reference、GitCode spec、三份基线。
- 只有 Phase 02 专属的输入（如 API token、runner 凭证、IaC 配置）才通过环境变量或 `phase02/inputs/` 本地文件提供。
- 环境变量统一在 `.claude/settings.local.json` 或 `.env`（gitignore 中）配置。
- 敏感信息（token/key）**绝不入库**。
