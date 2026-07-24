用例 ID:   COMP-VARREF-01-083
维度标签:   [completeness]
维度:      完备性
优先级:    P1
溯源意图:  KEEP-TC-438~440
母意图:    —
标题:      YAML 表达式与 Shell 环境变量引用方式验证

前置条件:
  - 仓库已启用 AtomGit Action

操作步骤:
  1. 在 env 和 run 中分别使用 ${{ }} 表达式和 $VAR 环境变量方式引用
  2. 验证两种方式结果一致

预期结果:
  - ${{ env.VAR }} 与 $VAR 引用同一变量时值一致，${{ atomgit.sha }} 与 $ATOMGIT_SHA 值一致

验证点:
  - [正向] 表达式引用与环境变量引用结果相同
  - [正向] atomgit 上下文与 ATOMGIT_* 环境变量值一致

清理:      重置 fixture 仓库
