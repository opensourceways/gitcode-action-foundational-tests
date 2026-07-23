用例 ID:   COMPAT-MIGR-02-001
维度标签:   [compatibility, usability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-027
标题:      端到端迁移摩擦清单：从 GitHub workflow 到 GitCode workflow 的最小改写路线验证

前置条件:
  - 一个标准 GitHub workflow 文件（含 github.* 上下文、runs-on: ubuntu-latest、uses: actions/checkout@v4、permissions GitHub 命名、success() 函数语法、pull_request types GitHub 命名）
  - 将其放入 .gitcode/workflows/ 目录

操作步骤:
  1. 直接搬运不修改 → 验证报错列表（期望一次性暴露所有问题）
  2. 逐项修改：github.* → atomgit.*
  3. runs-on: ubuntu-latest → runs-on: {ubuntu-24,x64,small}
  4. permissions 块重写
  5. uses: actions/checkout@v4 → uses: checkout
  6. success()/failure() → success/failed
  7. pull_request.types 命名修改
  8. GITHUB_* 变量 → ATOMGIT_*
  9. 非 string inputs 类型改写
  10. concurrency 块重写

预期结果:
  - 每个摩擦点有对应错误信息指向正确写法
  - 按迁移清单逐项修改后 workflow 可正常触发
  - 每个未修改的差异点产生可理解错误（非 500）

验证点:
  - [正向] 按迁移清单逐项修改后 workflow 正常执行
  - [正向] 每个未修改的差异点产生可理解错误
  - [非功能] 迁移文档覆盖全部改写点

清理:      fixture
