## 失败分诊 · USE-ENV-01-002 · 引用 GITHUB_SHA 时日志应给出环境变量映射提示

**判定结果**: FAIL
**失败断言**: assertions[0] (nonfunctional, error_message, eval=llm_assisted) — 期望日志中出现 ATOMGIT_* 前缀环境变量的映射指引，实际日志仅含 bash 级 `GITHUB_SHA: unbound variable` 错误，无平台级环境变量映射提示；断言退化至 run_status 检查时 Job 为 FAILED

**根因初判**: 产品bug（错误提示缺失）+ 用例问题（断言 eval=llm_assisted 导致编译退化）

**证据**:

- **Job 日志全量**（7 行）:
  ```
  === JOB: test GITHUB env var hint (status=FAILED) ===
  [2026/07/23 22:43:06.329 GMT+08:00] [INFO] Job(1529982214710374400_1529982214693597191) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c7c5c50c-e929-41f0-8d21-b4dac04536b0.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c7c5c50c-e929-41f0-8d21-b4dac04536b0.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/c7c5c50c-e929-41f0-8d21-b4dac04536b0.sh: line 2: GITHUB_SHA: unbound variable
  ::error::Process exited with code 1
  ```
  用户使用 `$GITHUB_SHA` 环境变量，由于 GitCode 环境中不存在该变量且脚本启用了 `set -u`，bash 抛出 `unbound variable` 错误并退出码 1。日志中无任何关于 `GITHUB_*` 应替换为 `ATOMGIT_*` 的平台级指引或警告信息。

- **预期行为**（Phase 01 文本用例 `USE-ENV-01-002`，优先级 P1，维度 usability/compatibility）:
  - 操作步骤 1: "在 run 步骤中输出 $GITHUB_SHA"
  - 预期结果: "日志中应出现关于 GITHUB 变量不存在或建议使用 ATOMGIT 的提示"
  - 验证点: "[负向] 不应静默输出空值后继续"；"[非功能] 日志中是否出现 ATOMGIT 前缀的环境变量指引"

- **实际行为**:
  - 用户引用 `$GITHUB_SHA` 后脚本因 `set -u` 退出码 1，Job FAILED。平台正确阻止了静默继续（满足"不应静默输出空值后继续"），但错误源是 bash 自身，并非平台级别的环境变量兼容层给出的带有 ATOMGIT_* 映射指引的友好报错。用户看到的是晦涩的 `unbound variable` 而非"GITHUB_SHA 在 GitCode 中对应 ATOMGIT_SHA"。

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `bad-env` job 的步骤:
    ```yaml
    steps:
      - name: echo GITHUB_SHA
        run: |
          set -u
          echo "sha=$GITHUB_SHA"
    ```
  - 这对应 GitCode 规格 `phase01/inputs/gitcode-spec/running-pipelines/view-job-logs.md` 第 50-61 行的 ATOMGIT_* 系统变量表:
    ```
    | `ATOMGIT_SHA` | 触发提交 SHA |
    ```
    文档明确声明 Runner 环境中注入了 `ATOMGIT_SHA`（第 57 行），但未声明 `GITHUB_SHA` 的存在或兼容映射关系。根据第 48 行"除 `${{ }}` 表达式外，Runner 环境中还注入了 `ATOMGIT_*` 系统环境变量"，平台仅保证 `ATOMGIT_*` 变量可用。

**置信度**: 中（平台正确拦截了未定义变量，Job FAILED 非静默通过；但缺少映射指引属于编译缺口——断言 `eval=llm_assisted` 需要 LLM 判断"日志警告是否醒目"，编译期无法处理此 target 导致退化至 run_status 检查）

**影响**:
- **阻塞性**: 🟡非阻塞 — bash 报错 `unbound variable` 导致 Job FAILED，用户可看到错误但缺少平台级迁移指引
- **静默性**: 🟢明确报错 — bash 明确输出 `GITHUB_SHA: unbound variable` 错误，错误信息清晰可定位
- **影响面**: 🟡同维度 — 所有引用 GITHUB_* 环境变量（非表达式）的 workflow 均会在此处失败
- **综合**: bash 报错明确但缺少平台级 GITHUB_* → ATOMGIT_* 迁移指引，所有引用 GitHub 环境变量的 workflow 均受影响
- **是否有规避手段**: 是 — 用户可直接将 `$GITHUB_SHA` 替换为 `$ATOMGIT_SHA`

**建议**:
- 平台可在 Runner 环境中设置 GITHUB_* → ATOMGIT_* 的兼容 alias，或在引用未定义的 GITHUB_* 变量时在 stderr 注入提示信息（如 "GITHUB_SHA is not set. Use ATOMGIT_SHA instead."）
- 测试 YAML 断言 `eval: llm_assisted` 需要 LLM 运行时评估，建议增加一个 `positive: run_logs contains "ATOMGIT_SHA"` 作为确定性 fallback
- 相关用例: USE-ENV-01-001（同一意图 INTENT-USE-003 sibling）
