## 失败分诊 · USE-DISP-01-002 · workflow_dispatch 未提供参数但存在 default 时应使用默认值运行

**判定结果**: FAIL
**失败断言**:
- positive/run_logs: contains `"env=staging"` — job 在 step 执行前已失败，日志不含任何表达式输出

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: default input value (status=FAILED) ===
  [2026/07/23 22:42:44.561 GMT+08:00] [INFO] Job(1529982123488710656_1529982123467739143) duration check: true
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 配置了一个有 default 值的 input
  - 操作步骤: 手动触发 workflow 不提供该参数
  - 预期结果: workflow 使用默认值成功运行

- **实际行为**:
  - Job status 直接为 FAILED，**未进入任何 step 执行**
  - 日志仅有一行 job info，无 shell 创建、无脚本执行、无输出
  - **失败传导链**: 平台 → workflow_dispatch 触发时未传 params → inputs 解析失败 → job 在 setup 阶段直接标记 FAILED → 测试断言 positive/run_logs 无匹配

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `test-default` job 及 trigger 段:
    ```yaml
    on:
      workflow_dispatch:
        inputs:
          environment:
            description: target environment
            type: string
            required: false
            default: staging
    jobs:
      test-default:
        name: default input value
        runs-on: [dedicate-hosted, x64, large]
        steps:
          - name: echo env
            run: |
              echo "env=${{ inputs.environment }}"
    trigger:
      event: workflow_dispatch
      as: maintainer
      params: {}
    ```
  - **GitCode 规格** `running-pipelines/manually-trigger-pipeline.md` 第54-67行:
    ```markdown
    | type | 说明 |
    |------|------|
    | `string` | 文本输入 |
    
    - `description`：输入项说明文字
    - `required`：是否必填（`true`/`false`）
    - `default`：默认值
    - `type`：输入类型，当前仅支持 `string`
    ```
  - **逐项映射**:
    - 测试 `inputs.environment` + `default: staging` + `required: false` → 规格声明 `default` 为默认值，`required: false` 表示可选
    - 测试 `params: {}`（手动触发不传参） → 规格描述的"默认值"行为预期启用
    - 平台行为：`params: {}` 触发时 job 直接 FAILED，未使用 default 值
    - 差异：规格要求默认值回退，实际平台未正确注入默认值

- **环境前置条件验证**: workflow_dispatch 事件，params 为空对象，input 配置有 default 值

**置信度**: 高（job 直接 FAILED 未进入任何 step；日志极度短小；规格明确声明 default 行为）

**影响**:
- **阻塞性**: 🔴 所有包含有 default 值 input 的 workflow_dispatch 工作流在手动触发不填参数时直接失败
- **静默性**: 🟡 job 状态为 FAILED 可见，但无任何错误消息说明原因
- **影响面**: 🔴 所有使用 workflow_dispatch inputs + default 组合的工作流
- **综合**: 手动触发工作流不填可选参数（有默认值）时 job 直接失败，完全阻塞手动触发场景
- **是否有规避手段**: 是（手动触发时总是显式传入所有 input 参数值；但这违背了 default 的设计目的）

**建议**:
- 平台方应修复 workflow_dispatch 触发时 inputs 默认值的注入逻辑
- 建议在 job setup 失败时输出更详细的错误信息（如"input environment 未提供值且无默认值"）
