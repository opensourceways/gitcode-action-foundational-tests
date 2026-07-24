用例 ID:   COMP-BOUND-01-088
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-240~246
母意图:    —
标题:      工作流命令 set-env add-path 与文件写入边界验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 run 中通过 ATOMGIT_ENV / ATOMGIT_PATH / ATOMGIT_OUTPUT 写入
  2. 验证后续步骤可读取

预期结果:
  - ATOMGIT_ENV 写入的变量在当前 job 后续 step 中可用，ATOMGIT_PATH 添加的目录在 PATH 中，ATOMGIT_OUTPUT 写入的键值可被引用

验证点:
  - [正向] ATOMGIT_ENV 写入后后续 step 可读取
  - [正向] ATOMGIT_PATH 添加后目录在 PATH
  - [正向] ATOMGIT_OUTPUT 写入后 outputs 可引用

清理:      重置 fixture 仓库
