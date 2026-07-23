用例 ID:   COMP-ACTION-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-022
标题:      验证 Action 引用方式: 官方短名、第三方全路径、本地相对路径
前置条件:  仓库存在本地 action（.gitcode/actions/my-action/action.yml）
操作步骤:
  1. uses: checkout（官方短名）
  2. uses: setup-node with node-version:'20'
  3. uses: docker/build-push-action@v6（全路径）
  4. uses: ./.gitcode/actions/my-action（本地相对路径）
  5. @v4 tag vs @sha commit 引用
预期结果: 三种引用方式均正确解析和执行；不存在的 action 明确报错
验证点:
  - [正向] 官方短名 checkout 正确拉取
  - [正向] 第三方全路径引用成功
  - [正向] 本地相对路径引用成功
  - [负向] 引用不存在的 action 明确报错
清理:      fixture
