## 失败分诊 · USE-INPT-01-002 · 使用 boolean 类型 input 时报错应提示仅支持 string

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即 YAML 校验应拒绝 `type: boolean`），实际 COMPLETED；assertions[1] (nonfunctional, error_message) — 期望报错含"仅支持 string"及类型转换指引，实际无任何报错

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: test boolean input error (status=COMPLETED) ===
  [2026/07/23 22:43:37.866 GMT+08:00] [INFO] Job(1529982346910896128_1529982346885730311) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/23180564-e297-4a8e-8070-f5b7e2d4ee7c.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/23180564-e297-4a8e-8070-f5b7e2d4ee7c.sh
  dry_run=false
  ```
  `type: boolean` 被平台静默接受，workflow 正常调度执行至 COMPLETED，输出 `dry_run=false`。日志中无任何 YAML 校验错误，无关于"仅支持 string 类型"的提示或报错信息。

- **预期行为**（Phase 01 文本用例 `USE-INPT-01-002`，优先级 P1，维度 usability/compatibility）:
  - 操作步骤 1: "声明 workflow_dispatch inputs 的 type: boolean"
  - 预期结果: "YAML 校验报错，明确说明 GitCode 仅支持 string 类型，并给出转换指引"
  - 验证点: "[负向] 不应静默降级为 string"；"[非功能] 报错中应包含 string 与类型转换相关提示"

- **实际行为**:
  - 平台对 `type: boolean` 的 input 声明静默接受并执行转换，`boolean`→`string` 降级为 `"false"` 输出。触发了"不应静默降级为 string"这一负向验证点描述的禁止行为。用户无法知晓 GitCode 仅支持 `string` 类型。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `bad-input` job 的 workflow_dispatch inputs 定义:
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
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/writing-pipelines/configure-triggers.md` 第 56-67 行和第 103 行的 inputs 字段类型说明:
    ```
    | type | 说明 | 示例 |
    |------|------|------|
    | `string` | 文本输入 | 版本号、镜像名、环境名 |
    ```
    以及第 103 行："AtomGit Action 的 `workflow_dispatch.inputs` 仅支持 `string` 类型参数。" 测试 YAML 使用了文档未声明的 `type: boolean`，平台应按规格在 YAML 校验阶段拒绝该配置并提示仅支持 `string`。

**置信度**: 高（日志第 6 行 `dry_run=false` 证实 boolean 类型被静默降级为 string，Job COMPLETED 无校验错误，与 spec configure-triggers.md 第 103 行"仅支持 string"声明直接矛盾）

**影响**:
- **阻塞性**: 🟡非阻塞 — type:boolean 被静默降级为 string，workflow 仍正常完成，不阻塞执行
- **静默性**: 🔴静默错误 — boolean 类型被静默接受并降级为 string，无任何校验错误或警告
- **影响面**: 🟡同维度 — 所有使用非 string 类型 input 的 workflow_dispatch 均受影响，任何非 string 类型都会被静默降级
- **综合**: boolean 类型 input 被静默降级为 string 且无任何提示，所有使用非 string 类型 input 的 workflow_dispatch 均受影响
- **是否有规避手段**: 否 — 用户无法从平台获得任何关于类型限制的提示

**建议**:
- 平台 YAML 校验器需拒绝 `type` 字段的非 `string` 值，在 API 返回/UI 展示中明确报出"inputs 仅支持 string 类型，如需布尔语义请在步骤中使用表达式转换"的错误信息
- 相关用例: USE-INPT-01-001（同一意图 INTENT-USE-008 sibling）
