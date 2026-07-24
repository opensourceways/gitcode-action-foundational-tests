## 失败分诊 · USE-EXPR-01-001 · 引用不存在的上下文属性时报错应包含原始表达式与错误类型

**判定结果**: FAIL
**失败断言**:
- negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝未定义属性）
- nonfunctional/error_message: rubric "报错信息必须包含出错的原始表达式和错误类型说明" — 无任何报错

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: undefined context property (status=COMPLETED) ===
  [2026/07/23 22:43:16.941 GMT+08:00] [INFO] Job(1529982259069460480_1529982259035906055) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6a7813a6-cf11-4a67-a9e5-9b5d034cce44.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6a7813a6-cf11-4a67-a9e5-9b5d034cce44.sh
  val=
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 文件位于 .gitcode/workflows/
  - 操作步骤: 在 run 步骤中使用 ${{ atomgit.nonexistent_property }}
  - 预期结果: 报错包含原始表达式字符串和错误类型说明（undefined property / unknown context）

- **实际行为**:
  - 表达式 `${{ atomgit.nonexistent_property }}` **静默求值为空字符串**
  - Job 成功完成（COMPLETED），无任何错误、警告或提示
  - **失败传导链**: 平台 → `atomgit.nonexistent_property` 静默求值为 `""` → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `bad` job 的 `bad expression` step:
    ```yaml
    steps:
      - name: bad expression
        run: |
          echo "val=${{ atomgit.nonexistent_property }}"
    ```
  - **GitCode 规格** `syntax-reference/context.md` 第25-48行:
    ```markdown
    ## 2.2 atomgit 上下文完整属性
    
    | 属性 | 类型 | 说明 |
    |------|------|------|
    | `atomgit.event_name` | string | 当前触发事件名称 |
    | `atomgit.sha` | string | 触发提交的 SHA |
    | `atomgit.ref` | string | 触发引用 |
    | ... |
    ```
    `atomgit` 上下文的合法属性列表中**不存在** `nonexistent_property`
  - **逐项映射**:
    - 测试 `atomgit.nonexistent_property` → 规格中 `atomgit` 无此属性，属性名不合法
    - 平台行为：未定义属性静默展开为空字符串，无报错
    - 差异：应产生包含原始表达式 `${{ atomgit.nonexistent_property }}` 和 "undefined property" 类型的报错

- **环境前置条件验证**: workflow_dispatch 触发，Runner [dedicate-hosted, x64, large]，表达式语法 `${{ }}` 正确

**置信度**: 高（日志直接证明 undefined property 静默求值为空；规格明确列出 atomgit 的合法属性集合）

**影响**:
- **阻塞性**: 🔴 用户使用不存在的上下文属性（拼写错误、迁移遗留等）不会得到任何反馈，静默使用空值
- **静默性**: 🔴 完全静默 — 无任何错误、警告
- **影响面**: 🔴 所有 workflow — 对任何上下文属性的拼写错误都无校验
- **综合**: 用户可能因拼写错误（如 `atomgit.shaa`）导致脚本逻辑错误，排障极端困难
- **是否有规避手段**: 否（用户无法区分"属性不存在返回空"和"属性值为空"）

**建议**:
- 平台方应在表达式求值阶段对未定义的上下文属性进行检测，报错内容须包含：
  - 原始表达式字符串（或前50字符）
  - 错误类型（undefined property / unknown context）
  - 建议检查上下文名称和属性名拼写
- 建议同时校验其他上下文（runner、env、vars 等）的属性合法性
