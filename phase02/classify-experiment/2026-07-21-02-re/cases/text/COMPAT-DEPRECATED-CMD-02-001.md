用例 ID:   COMPAT-DEPRECATED-CMD-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-045
母意图:    —
标题:      废弃命令处理差异——::set-output/::set-env/::add-path 在 GitCode 的降级

前置条件:
  - workflow 使用废弃的 ::set-output、::set-env、::add-path 命令

操作步骤:
  1. 在 run step 中使用废弃命令
  2. 观察平台处理行为与日志输出

预期结果:
  - 废弃命令不应导致 step 失败
  - 应给出废弃警告或自动映射到新命令

验证点:
  - [正向] run 状态仍为成功
  - [nonfunctional] 出现废弃警告或自动映射提示

清理:      重置 fixture 仓库
