## 失败分诊 · USE-EXPR-01-001 · 引用不存在的上下文属性时报错应包含原始表达式与错误类型

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_status) — 期望 run_status 不为 COMPLETED（即表达式求值应报错），实际 COMPLETED；assertions[1] (nonfunctional, error_message) — 期望报错含原始表达式和错误类型说明，实际无任何报错

**根因初判**: 产品bug

**证据**:

- **Job 日志全量**（6 行）:
  ```
  === JOB: undefined context property (status=COMPLETED) ===
  [2026/07/23 22:43:16.941 GMT+08:00] [INFO] Job(1529982259069460480_1529982259035906055) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/6a7813a6-cf11-4a67-a9e5-9b5d034cce44.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/6a7813a6-cf11-4a67-a9e5-9b5d034cce44.sh
  val=
  ```
  `${{ atomgit.nonexistent_property }}` 表达式被静默求值为空字符串 `""`（输出 `val=`），Job 以 COMPLETED 完成。平台未因引用不存在的上下文属性而报错，也未给出任何关于"未知上下文属性"或"请检查拼写"的错误提示。

- **预期行为**（Phase 01 文本用例 `USE-EXPR-01-001`，优先级 P1，维度 usability/compatibility）:
  - 操作步骤 1: "在 run 步骤中使用 ${{ atomgit.nonexistent_property }}"
  - 预期结果: "报错包含原始表达式字符串和错误类型说明（undefined property / unknown context）"
  - 验证点: "[负向] 不应静默求值为空字符串"；"[非功能] 报错中是否包含原始表达式和错误位置"

- **实际行为**:
  - 平台对 `atomgit.nonexistent_property` 表达式执行了求值，结果为空字符串（`val=`），Job 正常结束。触发了"静默求值为空字符串"这一负向验证点描述的禁止行为。用户无法判断表达式是否存在错误或拼写问题。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `bad` job 的步骤:
    ```yaml
    steps:
      - name: bad expression
        run: |
          echo "val=${{ atomgit.nonexistent_property }}"
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/syntax-reference/context.md` 第 27-48 行的 `atomgit` 上下文完整属性表，其中定义了 19 个合法属性（如 `atomgit.ref`、`atomgit.sha`、`atomgit.event_name` 等），不包含 `nonexistent_property`。文档第 5 行声明"每个上下文是一个 JSON 对象，可通过表达式 `${{ context.property }}` 访问"，暗含了属性应在上下文中存在的前提。平台应在引用不存在的属性时产生诊断信息。

**置信度**: 高（日志第 6 行 `val=` 证实表达式被求值为空字符串，Job COMPLETED 无任何报错，直接违反"不应静默求值为空字符串"的负向验证点）

**建议**:
- 平台表达式引擎应在求值阶段检测上下文属性的存在性，对 `atomgit.<不存在的属性>` 抛出明确错误（含原始表达式和"undefined property"类型说明）
- 最少应产生一个警告级别的诊断信息，避免用户因拼写错误导致静默空值传播
- 相关用例: USE-EXPR-01-002（同一意图 INTENT-USE-024 sibling）
