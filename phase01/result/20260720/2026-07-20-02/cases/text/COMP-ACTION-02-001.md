用例 ID:   COMP-ACTION-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-022
标题:      验证 Action 引用方式官方短名、第三方全路径、本地相对路径
incorporates: TC-310 (setup-java 不存在), TC-502 (CLI 工具缺失)

前置条件:
  - 使用三种 action 引用方式

操作步骤:
  1. uses: checkout → 使用官方 action
  2. uses: setup-node with { node-version: 20 } → 安装 node
  3. uses: docker/build-push-action@v6 → 第三方 action
  4. uses: ./.gitcode/actions/my-action → 本地 action
  5. @v4 tag / @sha commit 引用解析
  6. 引用不存在的 action → 验证报错

预期结果:
  - 三种引用方式均正确解析
  - tag/SHA 引用正确
  - 不存在的 action 明确报错
  - setup-java 应存在（TC-310 问题确认）

验证点:
  - [正向] 官方短名 checkout/setup-node 可用
  - [正向] 第三方全路径引用可用
  - [正向] 本地 relative path 可用
  - [负向] 不存在的 action 报错
  - [负向] setup-java 应存在（追踪 TC-310）

清理:      fixture
