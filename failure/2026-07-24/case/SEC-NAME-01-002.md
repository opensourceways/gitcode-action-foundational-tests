## 失败分诊 · SEC-NAME-01-002 · 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain_secret "API_KEY"，secret 原值未出现在日志中（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "masked_or_not_found"，实际 grep 输出缺失，该下划线复合词从未被脚本显式输出

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（13 行）:
  ```
  === JOB: Test printenv masking (status=COMPLETED) ===
  [2026/07/23 22:08:01.828 GMT+08:00] [INFO] Job(1529973387885940736_1529973387860774919) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ae3abea2-e99c-454c-b1d0-f8f15055d985.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ae3abea2-e99c-454c-b1d0-f8f15055d985.sh
  INPUT_SCHEDULER_ACTION_PARAMS={"pluginInfo":"{\"uses\":\"official_shell@1.0.0\",\"pluginName\":\"official_shell\",\"pluginVersion\":\"1.0.0\"}","script":"printenv | grep API_KEY || echo not found\n","shell":"","working-directory":""}
  INPUT_SCRIPT=printenv | grep API_KEY || echo not found

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1b0ba4fc-bfca-4786-80d3-1930013a1173.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1b0ba4fc-bfca-4786-80d3-1930013a1173.sh
  INPUT_SCHEDULER_ACTION_PARAMS={"working-directory":"","script":"cat /proc/self/environ | tr '\\0' '\\n' | grep API_KEY || echo not found\n","shell":"","pluginInfo":"{\"uses\":\"official_shell@1.0.0\",\"pluginName\":\"official_shell\",\"pluginVersion\":\"1.0.0\"}"}
  INPUT_SCRIPT=cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found

  ```
  日志仅输出 Runner 内部的 INPUT_SCHEDULER_ACTION_PARAMS 和 INPUT_SCRIPT 变量值，无 grep 的实际执行结果。grep 的输出（匹配行或 "not found"）未出现在 run_logs 中。脚本使用 `echo not found`（空格分隔），断言期望的关键词是 "masked_or_not_found"（下划线复合词），两者完全不匹配——无论是词汇中单词间的连接符（`_` vs ` `）还是语义（"masked_or" vs 仅 "not found"）都不对应。

- **预期行为**（Phase 01 文本用例 `SEC-NAME-01-002`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，执行 printenv 或读取 /proc/self/environ"
  - 操作步骤 2: "触发 workflow 并查看运行日志"
  - 预期结果: "printenv 输出到日志时，secret 值必须被脱敏；即使通过 env | grep 过滤，过滤后的值也应被脱敏"
  - 验证点: "[负向] printenv 输出到日志时，secret 值必须被脱敏，绝不应保留原值"

- **实际行为**:
  - grep/printenv 的实际输出未被记录到 run_logs 中——Runner 内部日志仅记录了脚本参数而非执行输出
  - 脚本的 `echo not found` 输出也未出现在日志中
  - 断言关键词 "masked_or_not_found" 是测试设计者设想的验证锚点，但脚本中从未显式 echo 该字符串

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `printenv-test` job 的两个步骤:
    ```yaml
    - name: Run printenv
      run: |
        printenv | grep API_KEY || echo not found
    - name: Read proc environ
      run: |
        cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found
    ```
  - 这对应 GitCode 规格 `security-permissions/using-secrets.md` 第 62-69 行的 Secret 安全机制表:
    ```
    | 安全措施 | 说明 |
    |--------|------|
    | 日志遮掩 | Secret 值在日志中自动替换为 *** |
    ```
    规格第 66 行承诺日志遮掩。printenv 和 /proc/self/environ 是常见的绕过简单 echo 脱敏的攻击手法——如果 secret 在环境变量中以明文存在，printenv 可能输出原值。但当前日志中 grep 输出完全缺失，无法判断脱敏是否在工作。
  - 测试 YAML 巧用 `runs-on: [self-hosted,arch=arm]` 来尝试在不同 Runner 环境中测试脱敏行为。

**置信度**: 高（日志确凿显示 grep 输出缺失，断言关键词 "masked_or_not_found"（下划线）与脚本中 "not found"（空格）完全不匹配——这是下划线/空格差异的系统性 标记不匹配）

**建议**:
- 在 script 中显式 echo 断言锚点（如 `echo "masked_or_not_found"`）而非依赖 grep 的未定义输出
- 断言关键词应与脚本实际输出的字符串精确一致（或用空格和下划线归一化处理）
- 相关用例: SEC-NAME-01-001, USE-SECNAME-01-001
