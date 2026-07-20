用例 ID:   USE-CTXERR-01-001
维度标签:   [usability]
维度:      易用性
优先级:    P1
溯源意图:  INTENT-USE-006
标题:      上下文对象命名差异（github.* vs atomgit.*）的错误信息可诊断性

前置条件:
  - 仓库包含一个使用 `${{ github.* }}` 上下文引用的 workflow（GitHub 风格）
  - 分别测试 github.ref / github.event_name / github.workspace

操作步骤:
  1. 提交使用 `${{ github.ref }}` 的 workflow，触发 push
  2. 提交使用 `${{ github.event_name }}` 的 workflow，触发 push
  3. 提交使用 `${{ github.workspace }}` 的 workflow，触发 push
  4. 记录每次的报错消息，观察是否提示应使用 atomgit 替代

预期结果:
  - 平台必须报错（不应静默失败或返回空值）
  - 报错消息应明确指出 `github` 上下文不被识别
  - 理想情况下，报错消息应明确提示 GitCode 使用 `atomgit` 上下文替代

验证点:
  - [正-非功能] 使用 `github.ref` 时报错发生且含 `github` 不被识别的说明
  - [正-非功能] 使用 `github.event_name` 时报错同上述要求
  - [正-非功能] 使用 `github.workspace` 时报错同上述要求
  - [非功能] 消息是否暗示用户应将 github 替换为 atomgit（0=无提示, 1=需查文档, 2=消息直接说）

清理:      fixture
