用例 ID:   COMPAT-PR-TYPES-02-001
维度标签:   [compatibility]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-007
标题:      验证 pull_request types 命名差异 open vs opened / update vs synchronize
incorporates: TC-064 (PR state 返回 opened), TC-234 (PR update 未触发), TC-561 (merge 未触发)

前置条件:
  - 配置各 types 值组合

操作步骤:
  1. types: [open] → PR 创建时触发
  2. types: [update] → PR 源分支新提交触发
  3. types: [reopen] → PR 重新打开触发
  4. types: [merge] → PR 合并触发
  5. types: [opened, synchronize, reopened]（GitHub 命名）→ 验证报错/兼容

预期结果:
  - GitCode types 命名正确生效
  - GitHub 命名应有明确报错
  - merge 事件可靠触发（TC-561 修复确认）

验证点:
  - [正向] open/update/reopen/merge 正确触发
  - [负向] GitHub 命名不应静默忽略

清理:      fixture
