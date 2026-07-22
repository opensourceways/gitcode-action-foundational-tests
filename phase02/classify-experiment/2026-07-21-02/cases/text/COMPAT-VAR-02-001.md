用例 ID:   COMPAT-VAR-02-001
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-062
母意图:    —
标题:      RUNNER_* / ATOMGIT_* 系统变量 Shell 真实注入回归验证

前置条件:
  - 仓库已启用 workflow 触发
  - Runner 环境已就绪

操作步骤:
  1. 在 workflow step 的 shell 中依次 echo 以下变量：
     `$RUNNER_OS`、`$RUNNER_ARCH`、`$RUNNER_NAME`、`$RUNNER_TEMP`、
     `$RUNNER_TOOL_CACHE`、`$RUNNER_ENVIRONMENT`、
     `$ATOMGIT_RUNNER_OS`、`$ATOMGIT_RUNNER_ARCH`、`$ATOMGIT_REPOSITORY_OWNER`
  2. 比对输出是否非空且值符合预期 runner 实际规格

预期结果:
  - 所有列出的 RUNNER_* 与 ATOMGIT_* 系统变量在 shell 中均可读取到非空值
  - 值与 runner 实际规格一致（如 RUNNER_OS 应为 Linux 而非 linux 或空串）
  - 双命名并存时至少有一套命名稳定可用

验证点:
  - [正向] step shell 中 echo 所列变量，输出非空且值正确
  - [负向] 不应出现「变量存在但值为空串」或「变量未定义」（历史 TC-441/442/206）
  - [非功能] 若 ATOMGIT_RUNNER_OS 与 RUNNER_OS 并存，文档应明确权威命名

清理:      无
