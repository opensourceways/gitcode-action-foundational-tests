## 失败分诊 · USE-ENV-01-002 · 引用 GITHUB_SHA 时日志应给出环境变量映射提示

**判定结果**: FAIL
**失败断言**:
- nonfunctional/error_message: rubric "日志警告是否足够醒目且包含有效指引：应提示 GITHUB_* 环境变量在 GitCode 中对应为 ATOMGIT_*" — 实际仅输出 shell 层面的 "unbound variable" 错误，无任何 ATOMGIT 映射提示

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: test GITHUB env var hint (status=FAILED) ===
  [2026/07/23 22:43:06.329 GMT+08:00] [INFO] Job(1529982214710374400_1529982214693597191) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c7c5c50c-e929-41f0-8d21-b4dac04536b0.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c7c5c50c-e929-41f0-8d21-b4dac04536b0.sh
  /home/slave1/runner/workers/0.0.4.4.version/_temp/c7c5c50c-e929-41f0-8d21-b4dac04536b0.sh: line 2: GITHUB_SHA: unbound variable
  ::error::Process exited with code 1
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 在 GitCode Runner 上执行
  - 操作步骤: 在 run 步骤中输出 $GITHUB_SHA
  - 预期结果: 日志中应出现关于 GITHUB 变量不存在或建议使用 ATOMGIT 的提示

- **实际行为**:
  - Shell 层面因 `set -u` 检测到 `GITHUB_SHA` 未定义，报 "unbound variable" 后退出
  - **无任何 GitCode/AtoMGit 平台层面的环境变量映射提示**
  - **失败传导链**: 平台 → 环境中无 `GITHUB_SHA` 变量 → `set -u` 触发 bash 错误 → 进程退出码 1 → job FAILED → 测试断言 error_message rubric 不满足

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `bad-env` job 的 `echo GITHUB_SHA` step:
    ```yaml
    steps:
      - name: echo GITHUB_SHA
        run: |
          set -u
          echo "sha=$GITHUB_SHA"
    ```
  - **GitCode 规格** `writing-pipelines/using-variables-secrets.md` 第124-138行:
    ```markdown
    AtomGit Action 的系统变量使用 `ATOMGIT_*` 前缀：
    
    | 系统变量 | 说明 |
    |---------|------|
    | `ATOMGIT_SHA` | 当前提交 SHA |
    | `ATOMGIT_REF` | 当前分支或 Tag 引用 |
    | `ATOMGIT_TOKEN` | 自动生成的 workflow token |
    ```
    不存在 `GITHUB_*` 前缀的系统变量
  - **逐项映射**:
    - 测试 `$GITHUB_SHA` (shell 变量) → 规格无 `GITHUB_*` 系统变量，对应为 `ATOMGIT_SHA`
    - 测试中 `set -u` → 测试主动启用了 "unset 变量即报错" 的 bash 严格模式
    - 平台行为：未在环境中注入 `GITHUB_SHA`，也未产生任何映射提示
    - 差异：期望平台在检测到 `GITHUB_*` 变量引用时输出映射提示，实际仅获得 bash 原生错误

- **环境前置条件验证**: GitCode Runner 环境，系统变量仅含 `ATOMGIT_*` 前缀，不含 `GITHUB_*`

**置信度**: 高（日志仅含 bash 级的 "unbound variable" 错误；规格中明确所有系统变量为 ATOMGIT_* 前缀）

**影响**:
- **阻塞性**: 🟡 使用 `$GITHUB_SHA` 等 GitHub 变量名的脚本会失败，但用户可看到 bash 错误
- **静默性**: 🟡 脚本因 `set -u` 终止有明确错误输出，但完全无平台层面的指引
- **影响面**: 🟡 从 GitHub Actions 迁移的 workflow（`$GITHUB_SHA`、`$GITHUB_REF`、`$GITHUB_WORKSPACE` 等极高频）
- **综合**: 用户使用 GitHub 环境变量名会被 bash 报错但没有平台层映射提示，迁移体验差
- **是否有规避手段**: 是（手动替换 `GITHUB_*` → `ATOMGIT_*`；但用户需要从文档中主动发现这个差异）

**建议**:
- 平台方应增加 Runner 启动时的环境变量兼容层：当检测到脚本引用了 `GITHUB_*` 变量但不存在时，输出 WARNING 级日志提示对应替换
- 在 workflow YAML 校验阶段检测 `GITHUB_*` 环境变量引用，给出迁移指引
