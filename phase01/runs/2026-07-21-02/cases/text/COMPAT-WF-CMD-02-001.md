用例 ID:   COMPAT-WF-CMD-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-034
母意图:    —
标题:      工作流日志命令差异——::group::/::error::/::warning::/::notice::/::add-mask:: 支持度

前置条件:
  - workflow 使用 GitHub 式日志命令

操作步骤:
  1. 在 run step 中输出 ::error::、::warning::、::group::、::notice::、::add-mask:: 命令
  2. 观察运行详情页是否识别并渲染这些命令

预期结果:
  - GitCode 应支持主流的日志命令
  - 不支持的命令应静默忽略而非报错

验证点:
  - [正向] 支持的命令在 UI 中可见
  - [负向] 不支持的命令不导致 step 失败

清理:      重置 fixture 仓库
