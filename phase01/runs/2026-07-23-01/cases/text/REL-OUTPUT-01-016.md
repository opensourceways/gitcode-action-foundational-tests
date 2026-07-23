用例 ID:   REL-OUTPUT-01-016
维度标签:   [reliability]
维度:      稳定性
优先级:    P1
溯源意图:  INTENT-REL-016
母意图:    —
标题:      step output 边界值——ATOMGIT_OUTPUT 写入 1 MB 参数应成功传递

前置条件:
  - 仓库具备 workflow 运行权限

操作步骤:
  1. job 的 step A 向 ATOMGIT_OUTPUT 写入恰好 1 MB 参数
  2. step B 读取该参数

预期结果:
  - step B 读取到完整 1 MB 内容
  - MD5 校验通过

验证点:
  - [正向] 下游读取内容长度=1,048,576 bytes
  - [负向] 不应截断或丢失

清理:      无需特殊清理
