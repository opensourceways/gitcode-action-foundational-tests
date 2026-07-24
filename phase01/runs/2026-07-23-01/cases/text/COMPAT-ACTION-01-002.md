用例 ID:   COMPAT-ACTION-01-002
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-024
参照来源:  inputs/gitcode-spec/action-development/top-level-fields.md
母意图:    COMPAT-ACTION-01-001
标题:      checkout 短名等价性——path 参数支持

前置条件:
  - 仓库存在默认分支 main

操作步骤:
  1. 在工作流中使用 `uses: checkout` 并传入 `path: subdir/checkout-path` 参数
  2. 触发工作流，观察 checkout 行为
  3. 在后续步骤中验证代码是否被检出到指定子目录

预期结果:
  - `uses: checkout` 配合 path 参数可将代码检出到指定子目录
  - 裸插件名写法与 GitHub 全名写法在行为上等价
  - 后续步骤可在指定子目录中访问仓库文件

验证点:
  - [正向] checkout 步骤成功完成，无报错
  - [正向] 指定子目录下存在仓库文件
  - [负向] 不应因使用裸插件名而解析失败
  - [负向] 不应将代码检出到默认工作目录以外的意外位置

清理:      fixture
