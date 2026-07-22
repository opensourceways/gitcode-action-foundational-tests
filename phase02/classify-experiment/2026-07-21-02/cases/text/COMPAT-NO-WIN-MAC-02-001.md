用例 ID:   COMPAT-NO-WIN-MAC-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-039
母意图:    —
标题:      无 Windows/macOS runner——GitHub 三平台 vs GitCode 仅 Linux 的迁移降级

前置条件:
  - workflow 声明了 windows-latest 或 macos-latest

操作步骤:
  1. 提交包含 windows-latest 或 macos-latest 的 workflow
  2. 观察平台调度行为

预期结果:
  - 不应静默挂起或无提示失败
  - 应给出明确的「不支持该平台」报错

验证点:
  - [负向] 不静默挂起超过 300 秒
  - [nonfunctional] 报错信息包含平台不支持提示

清理:      重置 fixture 仓库
