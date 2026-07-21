用例 ID:   COMP-PERM-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-015
标题:      验证 permissions 权限模型 6 个权限域与快捷语法
incorporates: TC-588/589 (permissions 快捷语法)

前置条件:
  - 配置各 permissions 组合

操作步骤:
  1. permissions: {} → 所有权限域 none（最小权限）
  2. permissions: { repository: read, pr: write } → 验证实际权限
  3. permissions: read-all / write-all 快捷语法
  4. 声明 pr: none 后尝试写 PR → 被拒绝
  5. 未声明 permissions 时的默认行为

预期结果:
  - 6 个权限域分别生效
  - 快捷语法正确展开
  - 权限声明与实际行为一致

验证点:
  - [正向] {} → 最小权限
  - [正向] read-all/write-all 正确
  - [负向] pr:none → 写被拒
  - [负向] 无 write 声明不应静默降级为 read

清理:      fixture
