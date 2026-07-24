## 失败分诊 · USE-INPT-01-002 · 使用 boolean 类型 input 时报错应提示仅支持 string

**判定结果**: FAIL
**失败断言**:
- negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 boolean 类型）
- nonfunctional/error_message: rubric "报错信息必须包含 GitCode 仅支持 string 类型或等效说明" — 无任何报错

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: test boolean input error (status=COMPLETED) ===
  [2026/07/23 22:43:37.866 GMT+08:00] [INFO] Job(1529982346910896128_1529982346885730311) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/23180564-e297-4a8e-8070-f5b7e2d4ee7c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/23180564-e297-4a8e-8070-f5b7e2d4ee7c.sh
  dry_run=false
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 文件位于 .gitcode/workflows/
  - 操作步骤: 声明 workflow_dispatch inputs 的 type: boolean
  - 预期结果: YAML 校验报错，明确说明 GitCode 仅支持 string 类型，并给出转换指引

- **实际行为**:
  - 平台**静默接受** `type: boolean`，将其值作为字符串 `"false"` 处理并正常执行
  - **失败传导链**: 平台 → 跳过 inputs type 校验 → boolean 静默降级为 string → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `workflow_dispatch.inputs` 段:
    ```yaml
    on:
      workflow_dispatch:
        inputs:
          dry_run:
            description: dry run flag
            type: boolean
            required: false
            default: false
    ```
  - **GitCode 规格** `running-pipelines/manually-trigger-pipeline.md` 第54-67行:
    ```markdown
    AtomGit Action 的 `inputs` 仅支持 `string` 类型参数。
    
    | type | 说明 |
    |------|------|
    | `string` | 文本输入 |
    
    - `type`：输入类型，当前仅支持 `string`
    ```
  - **逐项映射**:
    - 测试 `type: boolean` → 规格声明 "仅支持 `string` 类型"，boolean 为非法类型值
    - 测试 `default: false` → 如规格所述仅支持 string，default 也应为字符串 `"false"`
    - 平台行为：boolean 类型被静默接受并降级处理为 string（输出 `false` 而非报错）
    - 差异：期望 YAML 校验报错，实际平台对非法 type 值采取静默降级策略

- **环境前置条件验证**: workflow_dispatch 触发，params 为空，input type 为 boolean

**置信度**: 高（日志直接证明 boolean 类型被静默接受；规格明确仅支持 string 类型）

**影响**:
- **阻塞性**: 🟡 使用 boolean 类型的 workflow 可以运行但语义可能与预期不同（boolean 值被当作字符串）
- **静默性**: 🔴 完全静默 — 无任何类型校验警告
- **影响面**: 🟡 从 GitHub Actions 迁移的 workflow（GitHub 支持 boolean、choice、environment 等多种类型）
- **综合**: 用户使用 `type: boolean` 无报错，但条件判断 `${{ inputs.dry_run == true }}` 永远不成立（因为值是字符串 "false" 而非布尔 false）
- **是否有规避手段**: 是（手动将所有 input type 改为 string，并在条件表达式中用 `== 'true'` 字符串比较；但用户无法在无提示的情况下知晓需要此转换）

**建议**:
- 平台方应在 YAML 校验阶段检测 inputs 的 `type` 字段值，非 `string` 时报错并提示仅支持 string
- 报错信息应包含："当前仅支持 string 类型。如需 boolean 语义，请将 type 设为 string，并在步骤中使用 `${{ inputs.dry_run == 'true' }}` 进行字符串比较"
