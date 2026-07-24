## 失败分诊 · SEC-NAME-01-002 · 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

**判定结果**: FAIL
**失败断言**:
  - 负向 `run_logs` `must_not_contain_secret: "API_KEY"` — **PASS**: 日志中 API_KEY 原值未出现
  - 正向 `run_logs` `equals: "masked_or_not_found"` — **PASS**: printenv 和 /proc/environ 结果中均无 API_KEY 原值

**根因初判**: 环境问题（secret 未注入，非脱敏生效）
**责任人**: Phase 02

**证据**:

- **Job 日志全量**:
  ```
  === JOB: Test printenv masking (status=COMPLETED) ===
  [2026/07/23 22:08:01.828 GMT+08:00] [INFO] Job(1529973387885940736_1529973387860774919) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/ae3abea2-e99c-454c-b1d0-f8f15055d985.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/ae3abea2-e99c-454c-b1d0-f8f15055d985.sh
  INPUT_SCHEDULER_ACTION_PARAMS={"pluginInfo":"...","script":"printenv | grep API_KEY || echo not found\n",...}
  INPUT_SCRIPT=printenv | grep API_KEY || echo not found

  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/1b0ba4fc-bfca-4786-80d3-1930013a1173.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/1b0ba4fc-bfca-4786-80d3-1930013a1173.sh
  INPUT_SCHEDULER_ACTION_PARAMS={"pluginInfo":"...","script":"cat /proc/self/environ | tr '\\0' '\\n' | grep API_KEY || echo not found\n",...}
  INPUT_SCRIPT=cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: 仓库配置了 secret API_KEY
  - 操作步骤: 1. 提交 workflow，执行 printenv 或读取 /proc/self/environ；2. 查看运行日志
  - 预期结果: printenv 输出到日志时，secret 值必须被脱敏；即使通过 env | grep 过滤，过滤后的值也应被脱敏

- **实际行为**:
  - 日志显示了 INPUT_SCHEDULER_ACTION_PARAMS 中的脚本内容（含 printenv 和 grep API_KEY 命令），说明日志记录了输入的脚本
  - 但 printenv 和 /proc/self/environ 的**输出结果未出现在日志中** — grep 可能未匹配、输出被脱敏引擎过滤、或 secret 未注入
  - 无法从日志中确认 API_KEY 原本存在但被脱敏为 `***`
  - **失败传导链**: printenv | grep API_KEY 执行 → 输出被日志系统捕获 → 日志中仅显示 input 参数脚本，grep 结果未显示 → 缺少"masked_or_not_found"的显式证据

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `printenv-test` 的 `Run printenv` 和 `Read proc environ`:
    ```yaml
    steps:
      - name: Run printenv
        run: |
          printenv | grep API_KEY || echo not found
      - name: Read proc environ
        run: |
          cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found
    ```
  - **GitCode 规格** `core-concepts/variables-secrets-context-expressions.md` 第 25-39 行:
    ```
    ## Context
    | `env` | Environment variables | `env.VAR_NAME` |
    |
    | `runner` | Runner information | `runner.os`, `runner.arch` |
    ```
  - **逐项映射**:
    - `printenv | grep API_KEY || echo not found`: 测试 YAML 枚举环境变量并过滤 secret 名 — 未直接引用 `${{ secrets.API_KEY }}`
    - 规格定义 Context 体系但未描述 printenv 场景下 secret 的脱敏机制
    - 测试 YAML 通过 shell 命令间接访问环境变量，而非通过 `${{ }}` 表达式

- **环境前置条件验证**: 未发现 API_KEY 原值泄露，但 printenv 输出结果未出现在日志中，无法确认 secret 是否存在。符合"Secret/token empty + no config_probe → 环境问题 (Phase 02)"

**置信度**: 中（日志中 printenv 结果被过滤或 secret 未注入，两种可能均无法排除）

**影响**:
- **阻塞性**: 低 — 未发现 secret 泄露
- **静默性**: 中 — 若脱敏引擎正常但日志采集丢弃了脱敏后的输出，测试无法得到正面证据
- **影响面**: 低 — 与其他 secret 系列共享环境问题
- **综合**: printenv 和 /proc/environ 操作执行但输出结果未在日志中出现，无法验证脱敏效果
- **是否有规避手段**: 是 — 增加显式的 `echo "found"` 或 `echo "not found"` 输出，而非仅依赖 grep 的输出

**建议**:
- Phase 02: 与其他 MASK 系列一样，确保 API_KEY secret 已配置
- Phase 01: 修改脚本为 `printenv | grep API_KEY && echo "FOUND RAW SECRET" || echo "secret masked or absent"`，确保日志中总是有显式判定输出
