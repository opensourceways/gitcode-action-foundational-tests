用例 ID:   COMP-RUNNER-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-017
标题:      验证 runner 标签匹配三段式标签、default 等效、自托管全匹配

前置条件:
  - 配置各 runs-on 标签格式

操作步骤:
  1. runs-on: {ubuntu-24,x64,small} → 分配 small x64 Ubuntu
  2. runs-on: default → 等价 [ubuntu-latest, x64, small]
  3. runs-on: [self-hosted, linux, gpu] → 全匹配
  4. ${{ matrix.os }},${{ matrix.arch }},small 动态标签
  5. 无匹配 runner → 排队或超时失败

预期结果:
  - 三段式标签正确匹配
  - 自托管全匹配
  - 无匹配时不随机分配

验证点:
  - [正向] 官方三段式标签正确
  - [正向] default 等价
  - [正向] 自托管全匹配
  - [负向] 无匹配不随机分配

清理:      fixture
