用例 ID:   SEC-ISOLATE-03-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-044
母意图:    —
标题:      多项目共享 runner 环境下的跨项目数据隔离

前置条件:
  - 两个不同项目共享同一批 runner 资源
  - 项目 A 的 workflow 在 runner 写入文件、env、secret

操作步骤:
  1. 项目 A 的 job 在 runner workspace 创建 ${PROJ}_SECRET_DATA 文件
  2. 项目 A 的 job 上传 artifact 含敏感数据
  3. 项目 A 的 job 结束后，项目 B 的 job 在同一 runner 上执行
  4. 检查项目 B 是否能访问项目 A 残留数据

预期结果:
  - 项目 B job 不应能看到项目 A 的残留文件、环境变量、进程
  - 项目 B 不应能下载项目 A 的 artifact
  - 项目 A 的 Secret 在项目 B 中不可访问

验证点:
  - [负向] 项目 B 的 `ls $WORKSPACE` 不含项目 A 残留文件
  - [负向] 项目 B 的 `env` 不含项目 A 残留环境变量
  - [负向] 项目 B 的 API 调用返回的 artifact 列表不含项目 A 条目
  - [负向] 项目 B 不可引用项目 A 的 Secret

清理: full_instance
