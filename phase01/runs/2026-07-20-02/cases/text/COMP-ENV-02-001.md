用例 ID:   COMP-ENV-02-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-011
标题:      验证环境变量四级优先级链 step > job > workflow > vars > ATOMGIT_*
incorporates: TC-001~004 (env 定义与优先级), TC-533 (job env 未注入 Shell)

前置条件:
  - 配置四级同名环境变量
  - 使用 ${{ env.VAR }} 和 $VAR 引用

操作步骤:
  1. step env 覆盖 job env（同名变量取 step 值）
  2. job env 覆盖 workflow env
  3. 验证 ${{ env.VAR }} 和 $VAR 读取同值
  4. 验证项目级 vars 覆盖组织级
  5. 验证 env > vars 优先级成立

预期结果:
  - 四级优先级链正确
  - 表达式和 Shell 引用一致
  - Job env 注入 Runner Shell 有效（修复 TC-533）

验证点:
  - [正向] step env 覆盖 job env
  - [正向] job env 覆盖 workflow env
  - [正向] ${{ env.VAR }} 和 $VAR 同值
  - [负向] $VAR 不为 UNSET（TC-533 问题修复确认）

清理:      fixture
