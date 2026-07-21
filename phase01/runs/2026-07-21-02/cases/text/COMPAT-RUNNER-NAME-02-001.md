用例 ID:   COMPAT-RUNNER-NAME-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-033
母意图:    —
标题:      RUNNER_OS/ARCH 双命名混乱——RUNNER_* vs ATOMGIT_RUNNER_* 及 GitHub 对齐

前置条件:
  - runner 正常可用

操作步骤:
  1. 在 shell 中输出 RUNNER_OS、ATOMGIT_RUNNER_OS、RUNNER_ARCH、ATOMGIT_RUNNER_ARCH
  2. 比较四者的值与存在性

预期结果:
  - 至少一套命名应返回正确的 os/arch 值
  - 两套命名若并存，其值应一致

验证点:
  - [正向] 至少一个 OS 变量返回非空值
  - [正向] 至少一个 ARCH 变量返回非空值
  - [负向] 无同时为空

清理:      重置 fixture 仓库
