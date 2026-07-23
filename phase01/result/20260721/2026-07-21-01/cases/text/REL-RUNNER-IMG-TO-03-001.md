用例 ID:   REL-RUNNER-IMG-TO-03-001
维度标签:   [reliability]
维度:      可靠性
优先级:    P1
溯源意图:  INTENT-REL-026
标题:      自托管 runner + 自定义 image：镜像拉取超时应有明确错误——历史 #7/#52/#54

前置条件:
  - 自托管 runner 使用不存在的自定义镜像

操作步骤:
  1. 配置 container.image=nonexistent-registry.example.com/nonexistent:99
  2. 触发 workflow
  3. 观察 job 在 10min 内的行为和日志

预期结果:
  - 镜像拉取失败/超时时 10min 内 Run failed
  - 日志含镜像拉取错误（镜像名 + 失败原因）
  - 不应 pending 1h 后才失败且日志仅 1 行

验证点:
  - [正向] 10min 内 Run failed
  - [正向] 日志含 image pull 错误和镜像名
  - [负向] 日志不只有 1 行

清理:      fixture
