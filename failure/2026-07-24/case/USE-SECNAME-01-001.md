## 失败分诊 · USE-SECNAME-01-001 · Secret 名称以 ATOMGIT_ 开头时应给出命名规则错误

**判定结果**: FAIL
**失败断言**:
- negative/run_status: expected ≠ COMPLETED, actual = COMPLETED（平台未拒绝 `ATOMGIT_TOKEN` 作为 secret 名称）
- nonfunctional/error_message: rubric "报错信息必须包含 Secret 名称规则或命名格式相关说明" — 无任何报错

**根因初判**: 产品bug
**责任人**: 平台方

**证据**:

- **Job 日志全量**:
  ```
  === JOB: secret name rule violation (status=COMPLETED) ===
  [2026/07/23 22:45:47.794 GMT+08:00] [INFO] Job(1529982887808339968_1529982887787368455) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/4e769d45-9244-4dc5-85e0-23c1f9739b2e.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/4e769d45-9244-4dc5-85e0-23c1f9739b2e.sh
  token=***
  ```

- **预期行为**（Phase 01 文本用例）:
  - 前置条件: workflow 文件位于 .gitcode/workflows/
  - 操作步骤: 在 workflow 中引用 ${{ secrets.ATOMGIT_TOKEN }}
  - 预期结果: 系统在校验或运行时给出明确的命名规则提示，区分名称违规与未配置

- **实际行为**:
  - 平台**静默接受** `ATOMGIT_TOKEN` secret 引用，输出 `***`（脱敏后的值，说明该 secret 确实存在或被映射到了系统 token）
  - **失败传导链**: 平台 → `ATOMGIT_TOKEN` 未被拒绝 → 系统 token 值被注入 → job 正常完成 → 测试断言 negative/run_status ≠ COMPLETED 失败

- **测试 YAML 与规格精确对照**:
  - **测试 YAML** 中 `bad` job 的 `use reserved prefix secret` step:
    ```yaml
    steps:
      - name: use reserved prefix secret
        run: |
          echo "token=${{ secrets.ATOMGIT_TOKEN }}"
    ```
  - **GitCode 规格** `security-permissions/using-secrets.md` 第43-47行:
    ```markdown
    Secret 名称规则：
    
    - 仅允许大写字母、数字和下划线
    - 不得以 `ATOMGIT_` 开头（与系统变量冲突）
    - 不得以数字开头
    ```
  - **逐项映射**:
    - 测试 `${{ secrets.ATOMGIT_TOKEN }}` → 规格声明 "不得以 ATOMGIT_ 开头"
    - `ATOMGIT_TOKEN` 前缀匹配 `ATOMGIT_`，属于违规命名
    - 平台行为：`ATOMGIT_TOKEN` 被当作系统保留 secret（自动生成的会话 Token），未触发命名违规错误
    - 差异：期望报错并提示命名规则，实际直接返回系统 token 值（脱敏后显示 `***`）

- **环境前置条件验证**: workflow_dispatch 触发，Runner [dedicate-hosted, x64, large]，`ATOMGIT_TOKEN` 为系统级自动注入 token

**置信度**: 高（日志显示 secret 值被脱敏输出 `***` 说明系统将其识别为系统 token；规格明确禁止 ATOMGIT_ 前缀）

**影响**:
- **阻塞性**: 🟡 用户自己创建名为 `ATOMGIT_TOKEN` 的 secret 会与系统 token 冲突，获得的是系统 token 而非自定义 secret
- **静默性**: 🔴 完全静默 — workflow 正常运行，但使用的 secret 值可能不是用户预期的
- **影响面**: 🟡 所有使用了 ATOMGIT_ 前缀自定义 secret 的项目（安全敏感场景）
- **综合**: 用户使用 ATOMGIT_ 前缀的 secret 名称会被静默替换为系统值，无任何安全警告
- **是否有规避手段**: 否（用户不知道自己的 secret 被系统值覆盖，且无反馈）

**建议**:
- 平台方应在 YAML 校验或运行时对 `${{ secrets.ATOMGIT_* }}` 引用进行拦截，报错内容包含：
  - "Secret 名称不得以 ATOMGIT_ 开头（为系统保留前缀）"
  - 完整命名规则：仅大写字母、数字、下划线；不得以数字开头
  - 区分 "名称违规" 与 "Secret 未配置" 两类错误
- 在 AtomGit 界面创建 Secret 时也应拦截以 `ATOMGIT_` 开头的名称
