用例 ID:   REL-RUNNER-ORG-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-029
标题:      自托管 runner 组织级注册后授权项目可正确调度——历史 #37

前置条件:
  - 组织级 runner 授权给项目 A
  - 项目 B 未授权

操作步骤:
  1. 项目 A 触发 workflow (runs-on 指向组织 runner group)
  2. 观察项目 A job 是否正常调度到组织 runner
  3. 项目 B 触发相同 workflow 验证是否被拒绝

预期结果:
  - 授权项目 A 可正常调度组织 runner
  - 未授权项目 B 无法使用组织 runner

验证点:
  - [正向] 授权项目 job 成功执行
  - [负向] 未授权项目无法使用组织 runner

清理:      fixture
