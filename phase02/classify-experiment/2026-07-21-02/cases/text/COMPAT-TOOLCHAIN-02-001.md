用例 ID:   COMPAT-TOOLCHAIN-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P2
溯源意图:  INTENT-COMPAT-038
母意图:    —
标题:      预装工具链版本差异——GitHub runner image 与 GitCode ubuntu-latest 预装软件差集

前置条件:
  - runner 标签为 ubuntu-latest

操作步骤:
  1. 在 workflow 中检查常见预装工具（git、node、python、docker、jq）的版本
  2. 与 GitHub ubuntu-latest 的标准列表对比

预期结果:
  - 核心工具（git、bash、curl）应存在
  - 版本差异应被文档化

验证点:
  - [正向] git、bash、curl 可用
  - [nonfunctional] 缺失工具的报错可理解

清理:      重置 fixture 仓库
