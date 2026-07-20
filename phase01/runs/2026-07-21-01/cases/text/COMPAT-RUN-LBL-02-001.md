用例 ID:   COMPAT-RUN-LBL-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-010
标题:      验证 runs-on 三段式标签格式差异与 GitHub 单标签不兼容

前置条件:
  - 使用 GitCode 三段式和 GitHub 单标签

操作步骤:
  1. runs-on: {ubuntu-24,x64,small} → 正确匹配
  2. runs-on: default → 等价默认规格
  3. runs-on: [self-hosted, linux, x64] → 全匹配
  4. runs-on: ubuntu-latest（GitHub 格式）→ 验证报错

预期结果:
  - 三段式标签正确匹配
  - GitHub 格式明确报错

验证点:
  - [正向] 三段式正确匹配 runner
  - [正向] default 等价
  - [负向] ubuntu-latest 应明确报错

清理:      fixture
