## 失败分诊 · SEC-SUPPLY-01-002 · commit hash 不匹配时第三方 Action 应被拒绝执行

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_status) — must_not_equal "success"，实际 run_status=FAILED ≠ "success"（PASS，平台正确拒绝了无效 action）；assertions[1] (positive, run_logs) — 期望日志含 "action_not_found_or_sha_mismatch"，实际 0 字节有效日志无任何诊断输出

**根因初判**: 平台缺陷（兼用例问题）

**证据**:

- **Job 日志全量**（仅 2 行）:
  ```
  === JOB: Test hash mismatch rejection (status=FAILED) ===
  [2026/07/23 22:10:37.801 GMT+08:00] [INFO] Job(1529974041978880000_1529974041945325575) duration check: true

  ```
  日志仅包含 job header 和 duration check 行，与 SEC-SUPPLY-01-001 完全相同的模式。平台在遇到全零 hash action 引用（`uses: docker/build-push-action@0000000000000000000000000000000000000000`）时，job 直接 FAILED 无任何步骤执行、无任何诊断输出。负面断言 PASS（平台正确拒绝了无效 action 引用——job 未执行），但缺乏可观测的错误信息使正向断言无法验证。

- **预期行为**（Phase 01 文本用例 `SEC-SUPPLY-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，使用一个不存在的 commit SHA 引用 Action"
  - 操作步骤 2: "触发 workflow"
  - 预期结果: "job 进入失败状态或明确拒绝执行；系统不应静默回退到分支 HEAD"
  - 验证点: "[正向] 返回明确的 Action 未找到或 SHA 不匹配错误"

- **实际行为**:
  - 平台正确拒绝了无效的 action 引用：job FAILED，未执行任何步骤
  - 但平台上缺失任何错误诊断输出——"静默失败"违反了"不应静默回退"的要求
  - 从安全角度，平台行为正确（未执行不可信代码），但从可观测性角度，缺乏诊断是不合格的

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `hash-mismatch` job 的 `Use invalid hash action` 步骤:
    ```yaml
    - name: Use invalid hash action
      uses: docker/build-push-action@0000000000000000000000000000000000000000
    ```
  - 这对应 GitCode 规格 `action-development/plugin-security-specification.md` 第 43-52 行的输入参数安全验证表:
    ```
    | 参数类型 | 验证规则 | 示例 |
    |---------|--------|------|
    | 字符串 | 长度限制、格式校验 | 邮箱格式、URL 格式 |
    | 数字 | 范围检查、类型检查 | 正数、负数范围限制 |
    | 文件 | 路径安全检查 | 防止路径遍历攻击 |
    ```
    规格第 49 行要求字符串参数需做"长度限制、格式校验"。action 引用中的 commit hash 作为特殊格式的字符串，应被校验——但平台的行为是直接 FAILED 无错误信息，既是安全策略（拒绝执行）也是可观测性缺陷（无错误消息）。
  - 同时对应规格第 18-24 行的处理原则（禁止硬编码、使用安全输入、最小化暴露），这些原则隐含了对不可信输入（无效 hash）的安全处理要求。

**置信度**: 中（平台确凿拒绝了无效 action 引用——negative 断言 PASS；但 0 字节有效日志使得正向断言因无诊断输出而 FAIL，属于平台可观测性缺陷与断言关键词 mismatch 的叠加）

**影响**:
- **阻塞性**: 🟡非阻塞 — 平台正确拒绝了无效的全零 hash action 引用（job FAILED，未执行步骤），安全策略生效；但缺乏诊断输出
- **静默性**: 🔴静默错误 — job FAILED 但 0 字节有效日志，无 `::error::` 注释、无 "action not found" 或 "sha mismatch" 诊断，与 SEC-SUPPLY-01-001 同模式
- **影响面**: 🟡同维度 — 影响所有不合法的 action hash 引用场景（SEC-SUPPLY 系列），不可信的无效引用均缺乏诊断输出
- **综合**: 安全策略正确（拒绝执行无效 action），但 0 字节日志形成诊断盲区，违反"不应静默回退"的文档要求
- **是否有规避手段**: 否 — 当前平台无内置诊断输出，用户无法自行获取无效 action 引用被拒绝的具体原因

**建议**:
- 平台应输出明确错误信息：如 `::error:: Action not found: docker/build-push-action@0000000... (SHA not found in registry)`
- 断言可简化为仅依赖 negative/must_not_equal（当前 SEC-SUPPLY-01-002 的 negative 断言已经正确验证了行为）
- 相关用例: SEC-SUPPLY-01-001
