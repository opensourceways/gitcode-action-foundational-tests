```
用例 ID:   COMPAT-PERM-01-001
维度标签:   [compatibility, security]
维度:      兼容性
优先级:    P0
溯源意图:  INTENT-COMPAT-002
母意图:    —
标题:      未声明 permissions 时默认 TOKEN 读操作权限范围

前置条件:
  - 仓库为私有或内部仓库，默认需要认证才能读取
  - 仓库已启用 GitCode Action
  - 未在 workflow 中显式声明 permissions 块

操作步骤:
  1. 提交一个不包含 permissions 块的 workflow
  2. 在该 workflow 中执行读操作（如 checkout、查看仓库文件）
  3. 手动触发该 workflow

预期结果:
  - 系统在 workflow 未声明 permissions 时，仍赋予默认 TOKEN 足够的读权限
  - checkout 和文件读取操作成功执行

验证点:
  - [正向] checkout step 成功完成
  - [正向] 读操作（如 cat README）成功返回内容
  - [负向] 读操作不应因权限不足而失败

清理:      重置 fixture 仓库
```
