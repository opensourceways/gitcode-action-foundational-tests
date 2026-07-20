用例 ID:   COMP-ACT-03-012
维度标签:   [completeness, security]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-ACT-012
母意图:    —
标题:      k8s_deploy 部署完整链路——kubeconfig 认证/namespace/资源清单/日志脱敏

前置条件:
  - 仓库配置了 K8s 部署 workflow
  - 配置了有效的 kubeconfig（通过 secret 传入）
  - 集群 API server 网络可达

操作步骤:
  1. 配置 workflow 使用 `uses: official_k8s_deploy`，提供有效 kubeconfig
  2. 部署一个 Deployment 资源清单
  3. 指定 namespace 部署，再在不指定 namespace 时部署（验证默认行为）
  4. 指定不存在的 namespace，观察报错
  5. 部署格式错误的资源清单（如缺少必填字段），观察报错
  6. 使用无效 kubeconfig，观察认证失败的报错
  7. 检查日志中 kubeconfig 内容是否被脱敏

预期结果:
  - 有效 kubeconfig 可正常连接集群并部署资源
  - namespace 正确应用，不指定时使用 default
  - 不存在的 namespace 时给出明确报错
  - 格式错误清单给出具体错误位置
  - 无效 kubeconfig 时认证失败报错清晰
  - 日志中 kubeconfig 凭证被脱敏

验证点:
  - [正向] 有效 kubeconfig 部署成功，资源在集群中可见
  - [正向] namespace 行为符合预期
  - [负向] 无效 kubeconfig 报错不含密钥明文
  - [负向] 日志中 kubeconfig 凭证被脱敏
  - [状态] 若集群 API server 不可达——标记为 blocked-by-platform

清理: fixture
