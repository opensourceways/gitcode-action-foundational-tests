用例 ID:   COMP-ENV-01-001
维度标签:   [completeness]
维度:      功能完备性
优先级:    P1
溯源意图:  INTENT-COMP-011
标题:      验证环境变量四级优先级链: step > job > workflow > vars > ATOMGIT_*
前置条件:  仓库配置了项目级 vars
操作步骤:
  1. 设置 workflow/job/step 三级同名 env 变量
  2. 验证 step env 覆盖 job env，job env 覆盖 workflow env
  3. 验证 ${{ env.VAR }} 和 $VAR 读取到相同值
  4. 验证 vars 在 env 未定义时生效
预期结果: 优先级链 step > job > workflow > vars > ATOMGIT_* 正确生效
验证点:
  - [正向] step env 覆盖 job env
  - [正向] job env 覆盖 workflow env
  - [正向] env > vars 优先级成立
清理:      fixture
