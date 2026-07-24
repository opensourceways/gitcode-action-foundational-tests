## 失败分诊 · SEC-PERM-01-004 · 默认状态下写操作被 403 拒绝

**判定结果**: FAIL
**失败断言**: assertions[0] (negative, run_logs) — must_not_contain "push_successful"，未出现（PASS）；assertions[1] (positive, run_logs) — 期望日志含 "push_denied_or_403"，实际 git commit 因未配置 user.email 失败，push 步骤从未执行，"push denied as expected" 从未被 echo

**根因初判**: 标记不匹配

**证据**:

- **Job 日志全量**（20 行）:
  ```
  === JOB: Test default write denied (status=FAILED) ===
  [2026/07/23 22:08:34.201 GMT+08:00] [INFO] Job(1529973523672211456_1529973523638657031) duration check: true
  No shell specified, using platform default: default-bash
  ::debug::Script file created: /home/slave1/runner/workers/0.0.4.4.version/_temp/c9fb60c5-345e-4ac3-aef2-01580421cf35.sh
  ::debug::Executing: bash -e /home/slave1/runner/workers/0.0.4.4.version/_temp/c9fb60c5-345e-4ac3-aef2-01580421cf35.sh
  Cloning into 'repo'...
  Author identity unknown

  *** Please tell me who you are.

  Run

    git config --global user.email "you@example.com"
    git config --global user.name "Your Name"

  to set your account's default identity.
  Omit --global to set the identity only in this repository.

  fatal: unable to auto-detect email address (got 'slave1@1529973523638657031-pod.(none)')
  ::error::Process exited with code 128
  ```
  脚本执行到 `git commit -m test` 时因 Runner 环境中未配置 git user.email/user.name 而失败（exit code 128）。`git push origin main || echo push denied as expected` 从未被执行到。因此 "push denied as expected"（脚本中空格分隔）从未输出到日志。断言关键词 "push_denied_or_403"（下划线复合词）与脚本中的 "push denied as expected" 在两方面不匹配：(1) 连接符不同（`_` vs ` `），(2) 词汇不同（"or_403" vs "as expected"）。

- **预期行为**（Phase 01 文本用例 `SEC-PERM-01-004`，优先级 P0，维度 security）:
  - 操作步骤 1: "提交一个未声明 permissions 的 workflow，尝试 push"
  - 操作步骤 2: "触发 workflow"
  - 预期结果: "push 操作返回权限拒绝；默认权限不包含未声明的写域"
  - 验证点: "[正向] 权限拒绝信息明确"

- **实际行为**:
  - git clone 成功（证明 repository:read 权限生效）
  - git commit 因缺少 user.email/user.name 配置而失败，push 操作从未被尝试
  - 权限拒绝（403）场景未被测试到——失败的原因是 git 环境配置不足，而非平台权限校验

- **失败传导链**: git clone 成功 → git commit -m test 失败（git config 缺失）→ exit 128 → Job FAILED → git push 和 `|| echo` 从未执行

- **测试 YAML 与规格精确对照**:
  - 测试 YAML 中 `default-write-denied` job 的 `Attempt push without permissions` 步骤:
    ```yaml
    - name: Attempt push without permissions
      run: |
        git clone https://x-access-token:${{ atomgit.token }}@atomgit.com/${{ atomgit.repository }}.git repo
        cd repo
        echo test > test.txt
        git add test.txt
        git commit -m test
        git push origin main || echo push denied as expected
    ```
  - 这对应 GitCode 规格 `security-permissions/token-permissions.md` 第 97-103 行的 permissions 与 ATOMGIT_TOKEN 关系表:
    ```
    | permissions 配置 | ATOMGIT_TOKEN 实际权限 |
    |------------------|----------------------|
    | 未声明 permissions | 使用仓库设置中定义的权限 |
    ```
    规格第 99 行承诺"未声明 permissions：使用仓库设置中定义的权限"。测试未声明 permissions，期望 git push 因缺少 repository:write 权限而被拒绝。但测试在 git commit 阶段就失败了（环境问题），权限校验逻辑未被触及。
  - 同时对应第 37-48 行的权限类型对照表，`repository: write` 行确认写权限为"推送/修改仓库"。文档确凿承诺了 permissions 控制推送权限的行为。

**置信度**: 高（日志确凿显示 git commit 因 git config 缺失失败，push 从未执行；断言关键词 push_denied_or_403（下划线）与 script 中 push denied as expected（空格）完全不匹配——同时包含下划线/空格系统性问题和环境配置问题）

**建议**:
- 在 script 中添加 `git config --global user.email "test@test.com"` 和 `git config --global user.name "test"` 确保 git commit 可以执行
- 断言关键词应与脚本 echo 输出一致（使用 `push denied as expected` 或 `push_denied_or_403` 并在 script 中显式 echo 匹配的标记）
- 在断言编译期做下划线/空格归一化
- 相关用例: SEC-PERM-01-003, SEC-RUN-01-001
