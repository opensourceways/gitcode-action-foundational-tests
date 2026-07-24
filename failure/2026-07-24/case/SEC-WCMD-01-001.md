## 失败分诊 · SEC-WCMD-01-001 · Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain_secret "API_KEY"，secret 原值未出现在日志中（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "mask_command_without_payload"，实际该关键词从未被脚本显式 echo 输出

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（仅 6 行）:
  ```
  === JOB: Test add-mask response (status=COMPLETED) ===
  [2026/07/23 22:10:58.623 GMT+08:00] [INFO] Job(1529974129308864512_1529974129283698695) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/d93eaaec-61d4-49e4-8d50-dad75070df4d.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/d93eaaec-61d4-49e4-8d50-dad75070df4d.sh
  ::add-mask::
  ```
  脚本 `echo "::add-mask::${{ secrets.API_KEY }}"` 执行后输出 `::add-mask::`——workflow 命令骨架被打印到日志中，但 `${{ secrets.API_KEY }}` 展开后值为空（`::` 后无 payload）。与 SEC-MASK-01-001 同模式：secret 值被替换为空字符串而非 `***`。关键安全结论：add-mask 命令的响应中**确实未泄露** secret 原值（negative 断言 PASS），但命令的输出格式暴露了命令调用本身（`::add-mask::`）。断言关键词 "mask_command_without_payload" 从未被脚本显式 echo——脚本仅输出了 `::add-mask::` 命令本身。

- **预期行为**（Phase 01 文本用例 `SEC-WCMD-01-001`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个 workflow，执行 add-mask 命令遮蔽 secret"
  - 操作步骤 2: "触发 workflow 并查看日志中命令的响应"
  - 预期结果: "workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值；命令执行日志应仅显示命令骨架，不含 payload"
  - 验证点: "[负向] workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值"

- **实际行为**:
  - Secret 原值确实未泄漏（`::add-mask::` 后的 payload 为空）
  - 平台的行为（空 payload）意味着 secret 值既未泄漏也未以 `***` 形式显示——与 SEC-MASK-01-001 的空字符串替换行为一致
  - 断言关键词 "mask_command_without_payload" 从未被脚本显式输出，无法被断言引擎匹配

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `add-mask-test` job 的 `Mask secret` 步骤:
    ```yaml
    - name: Mask secret
      run: |
        echo "::add-mask::${{ secrets.API_KEY }}"
    ```
  - 这对应 GitCode 规格 `syntax-reference/workflow-commands.md` 第 60-70 行的废弃命令格式表:
    ```
    | 废弃命令 | 替代方案 |
    |--------|--------|
    | echo "::set-output name=result::success" | echo "result=success" >> $ATOMGIT_OUTPUT |
    | echo "::set-env name=MY_VAR::my_value" | echo "MY_VAR=my_value" >> $ATOMGIT_ENV |
    ```
    以及第 70 行注："日志脱敏命令 `echo '::add-mask::$SECRET'` 见「使用脚本命令」页。"
    规格第 70 行注明确引用了 `::add-mask::` 命令，说明这是平台支持的日志脱敏工作流命令。测试验证的关键安全属性是：命令的响应本身是否在日志中泄露了 secret 原值（payload 部分）。当前行为是 payload 为空（secret 值被平台替换为空）。
  - 同时对应 `security-permissions/using-secrets.md` 第 66 行"Secret 值在日志中自动替换为 `***`"，但 add-mask 命令的响应显示为空而非 `***`。

**置信度**: 中（negative 断言 PASS 证明 secret 未通过 add-mask 命令泄漏；断言关键词 "mask_command_without_payload" 从未被脚本输出是测试设计缺陷——与 SEC-MASK 系列的断言标记缺失同模式）

**影响**:
- **阻塞性**: ⚪无影响 — `::add-mask::` 命令的响应中未泄露 secret 原值（payload 为空），安全属性满足；仅断言标记从未被脚本输出
- **静默性**: 🟢明确报错 — 日志输出 `::add-mask::`（命令骨架可见，payload 为空），行为可观测，不存在 secret 泄漏
- **影响面**: 🟢单用例 — 仅影响 SEC-WCMD-01-001 的 add-mask 命令响应测试
- **综合**: add-mask 命令安全属性正常（无 secret 泄露），FAIL 原因仅为断言关键词 "mask_command_without_payload" 从未被脚本显式 echo 输出
- **是否有规避手段**: 是 — 在脚本中添加显式标记输出或改用 `must_not_contain_secret` 作为唯一断言

**建议**:
- 在脚本中添加显式的断言标记输出（如 `echo "mask_command_without_payload"`）
- 或改用更精确的断言：`must_not_contain_secret: "API_KEY"` 单独成立即可（因为这也验证了"响应不含 payload"）
- 相关用例: SEC-WCMD-01-002, SEC-MASK-01-001
