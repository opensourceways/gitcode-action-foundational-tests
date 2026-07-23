用例 ID:   COMPAT-ACTION-01-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-024
母意图:    —
标题:      checkout 短名等价性——ref 参数支持

前置条件:
  - 仓库存在默认分支 main
  - 存在一个可 checkout 的 feature 分支

操作步骤:
  1. 在工作流中使用 `uses: checkout` 并传入 `ref: main` 参数
  2. 触发工作流，观察 checkout 行为
  3. 再传入 `ref: feature-branch` 参数重复触发

预期结果:
  - `uses: checkout` 配合 ref 参数可正确检出指定分支
  - 裸插件名写法与 GitHub 全名写法在行为上等价
  - 检出后的工作目录包含指定分支代码

验证点:
  - [正向] checkout 步骤成功完成，无报错
  - [正向] 检出后的代码与指定分支一致
  - [负向] 不应因使用裸插件名而解析失败

清理:      fixture
