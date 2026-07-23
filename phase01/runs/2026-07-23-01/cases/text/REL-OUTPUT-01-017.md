用例 ID:   REL-OUTPUT-01-017
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-017
母意图:    —
标题:      step output 越界值——ATOMGIT_OUTPUT 写入 1 MB+1 byte 应被拒绝或报错

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. job 的 step 向 ATOMGIT_OUTPUT 写入 1,048,577 bytes

预期结果:
  - 系统报错或截断并给出警告
  - 不应静默截断

验证点:
  - [正向] step 状态=failure 或日志含 1MB/超出限制
  - [负向] 不应静默截断且无提示

清理:      无需特殊清理
