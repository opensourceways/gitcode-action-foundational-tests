用例 ID:   SEC-ISOL-01-002
维度标签:   [security]
维度:      安全性
优先级:    P1
溯源意图:  INTENT-SEC-033
标题:      并发 workflow 下的 token/secret 隔离

前置条件:
  - 仓库有两个独立的 workflow，可并发运行
  - 每个 workflow 绑定不同的 Secret（SECRET_A 和 SECRET_B）

操作步骤:
  1. 触发 workflow A（使用 SECRET_A）和 workflow B（使用 SECRET_B）同时运行
  2. job A 尝试读取 job B 可能写入共享位置的数据
  3. job A 尝试通过环境变量获取 job B 的信息
  4. 验证并发 job 之间 Secret 和 token 完全隔离

预期结果:
  - job A 无法从共享位置读取到 SECRET_B
  - job A 无法通过环境变量获取 job B 的 Secret
  - 并发 job 间的 Secret/token 完全隔离
  - 每个 job 的 ATOMGIT_TOKEN 独立且拥有各自的权限

验证点:
  - [负向] 并发 job A 不能读到 job B 的 Secret
  - [负向] 并发 job A 不能读到 job B 的环境变量
  - [正向] 每个 job 的 Secret 仅在该 job 内可用

清理:      full_instance
