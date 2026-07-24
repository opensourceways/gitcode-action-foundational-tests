## 失败分诊 · SEC-MASK-01-002 · Secret 值在 step summary 和错误堆栈中必须被脱敏

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, step_summary) — must_not_contain_secret "API_KEY"，断言目标 step_summary 不被断言引擎支持；assertions[1] (negative, error_stack) — must_not_contain_secret "API_KEY"，断言目标 error_stack 不被断言引擎支持

**根因初判**: 编译缺口

**证据**:

- **Job 日志全量**（11 行）:
  ```
  === JOB: Test summary masking (status=FAILED) ===
  [2026/07/23 22:06:57.709 GMT+08:00] [INFO] Job(1529973118867476480_1529973118842310663) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/11ffd625-7ee1-4a2b-8f49-3b4fddc20001.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/11ffd625-7ee1-4a2b-8f49-3b4fddc20001.sh

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/9cb3636a-c161-490a-95cb-ab53c2167329.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/9cb3636a-c161-490a-95cb-ab53c2167329.sh
  Failing with key 
  ::error::Process exited with code 1
  ```
  日志包含两个步骤：第 1 步（Write secret to summary）将 secret 写入 `$ATOMGIT_STEP_SUMMARY` 但无标准输出；第 2 步（Intentionally fail）输出 `Failing with key ` 后 secret 值为空并 exit 1。断言声明的 target `step_summary` 和 `error_stack` 是断言引擎不支持的合约目标类型——引擎仅支持 `run_logs`、`run_status`、`cache_restore` 等已实现的目标。两个断言均退化为 `kind:status` 的 coarse 评估。

- **预期行为**（Phase 01 文本用例 `SEC-MASK-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，将 secrets.API_KEY 写入 ATOMGIT_STEP_SUMMARY"
  - 操作步骤 2: "触发 workflow 并查看 step summary 与日志"
  - 预期结果: "step summary 中 API_KEY 的原值被替换为 `***`；若步骤失败产生堆栈，堆栈中亦不应出现原值"
  - 验证点: "[负向] step summary 不含 API_KEY 原值；[负向] 错误堆栈不含 API_KEY 原值"

- **实际行为**:
  - 第 1 步 `echo "Key: ${{ secrets.API_KEY }}" >> $ATOMGIT_STEP_SUMMARY` 无标准输出，step summary 内容写入了 ATOMGIT_STEP_SUMMARY 文件但不在 run_logs 中
  - 第 2 步故意失败 `exit 1`，输出 "Failing with key "（秘密值被掩码为空）
  - 断言引擎无法读取 `step_summary` 和 `error_stack` 目标，导致断言实际退化为 job status 检查

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `summary-mask` job 的两个步骤:
    ```yaml
    - name: Write secret to summary
      run: |
        echo "Key: ${{ secrets.API_KEY }}" >> $ATOMGIT_STEP_SUMMARY
    - name: Intentionally fail
      run: |
        echo "Failing with key ${{ secrets.API_KEY }}"
        exit 1
    ```
  - 这对应 GitCode 规格 `security-permissions/using-secrets.md` 第 62-69 行的 Secret 安全机制表:
    ```
    | 安全措施 | 说明 |
    |--------|------|
    | 日志遮掩 | Secret 值在日志中自动替换为 *** |
    ```
    规格第 66 行承诺日志遮掩，但未单独对 `ATOMGIT_STEP_SUMMARY` 或错误堆栈中的 secret 脱敏行为做出承诺。
  - 同时对应 `syntax-reference/workflow-commands.md` 第 50-58 行的 `ATOMGIT_STEP_SUMMARY` 用法:
    ```
    将 Markdown 内容写入工作流运行摘要，显示在 AtomGit 工作流运行详情页面。
    echo "## 构建结果" >> $ATOMGIT_STEP_SUMMARY
    ```
    规格第 54 行演示了向 step summary 写入内容的标准方法，测试 YAML 完全遵循此写法。但工作流命令文档未说明 summary 中是否自动脱敏 secret。

- **失败传导链**: step_1 (Write secret to summary) 成功但无可见输出 → step_2 (Intentionally fail) 故意 exit 1 导致 job FAILED → 断言 target `step_summary` 和 `error_stack` 不被引擎支持，断言评估退化为 coarse status 检查

**置信度**: 中（断言引擎不支持 `step_summary`/`error_stack` 目标是编译期缺口，同时 secret 值在日志中为空而非 `***` 再次印证 SEC-MASK-01-001 的掩码缺陷）

**影响**:
- **阻塞性**: ⚪无影响 — 断言引擎不支持 `step_summary` 和 `error_stack` 目标类型是测试基础设施的编译期缺口，非平台安全缺陷；secret 脱敏行为本身（空字符串）与 SEC-MASK-01-001 同根因
- **静默性**: 🟡可察觉 — job status FAILED 可被观测，但步骤 1（Write secret to summary）无标准输出，需推断步骤执行结果
- **影响面**: 🟢单用例 — 仅影响依赖 `step_summary`/`error_stack` 断言目标的测试用例（当前仅 SEC-MASK-01-002）
- **综合**: 断言引擎编译期无法读取 step_summary/error_stack 目标，叠加 secret 空字符串脱敏问题，非 step summary 特有的安全缺陷
- **是否有规避手段**: 是 — 将断言 target 改为 run_logs 并通过 echo 输出验证标记；或在断言引擎中增加 step_summary/error_stack 读取支持

**建议**:
- 在断言引擎中增加 `step_summary` 和 `error_stack` 目标的读取支持
- 若无条件支持，将断言的 target 改为 `run_logs` 并通过 echo 输出验证标记
- 相关用例: SEC-MASK-01-001, SEC-MASK-01-003, SEC-MASK-01-004, SEC-MASK-01-005
