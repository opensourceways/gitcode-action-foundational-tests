用例 ID:   SEC-SUPPLY-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-018
母意图:    —
标题:      第三方 action 引用未 pin 到 commit SHA 时有平台警告

前置条件:
  - 仓库中存在一个 workflow 文件
  - 准备多种 action 引用格式：`@v1`（tag 浮动）、`@main`（分支浮动）、`@<commit-sha>`（精确 SHA）

操作步骤:
  1. 提交 workflow A，使用 `uses: some-owner/some-action@main`（浮动分支引用）
  2. 提交 workflow B，使用 `uses: some-owner/some-action@v1`（浮动 tag 引用）
  3. 提交 workflow C，使用 `uses: some-owner/some-action@a1b2c3d4e5f6...`（完整 commit SHA）
  4. 观察提交时/workflow 初始化时是否有 lint/安全警告
  5. 验证同版本 tag 被覆盖指向新 commit 后，引用该 tag 的 workflow 抓取到的 action 代码是否更新

预期结果:
  - 使用浮动分支（@main）的引用在提交或解析时应有 lint 警告
  - 使用浮动 tag（@v1）的引用应有警告，推荐使用 commit SHA
  - 使用完整 commit SHA 的引用正常接受且不产生警告
  - tag 被覆盖后，引用该 tag 的 workflow 应拉取到最新指向的代码（验证可变性风险）

验证点:
  - [正向] `uses: action@<commit SHA>` 正常接受且执行
  - [负向] `uses: action@main`（浮动分支）→ 平台应产生 lint/安全警告
  - [负向] `uses: action@v1`（浮动 tag）→ 平台应产生 lint/安全警告
  - [负向] tag 被改写后引用该 tag 的 workflow 获取新代码（证明可变性风险存在）
  - [正向] commit SHA 引用的 action 不受 tag 改写影响

清理:      fixture
