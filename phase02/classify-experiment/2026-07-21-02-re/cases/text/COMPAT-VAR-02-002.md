用例 ID:   COMPAT-VAR-02-002
维度标签:   [compatibility, reliability]
维度:      兼容性
优先级:    P1
溯源意图:  INTENT-COMPAT-063
母意图:    —
标题:      env > vars 优先级链在 Shell 中的真实覆盖回归验证

前置条件:
  - 仓库已启用 workflow 触发
  - 平台已在 vars 中设置 ENV_LEVEL=vars（不通过 env 映射）

操作步骤:
  1. 在 workflow 级定义 env ENV_LEVEL=workflow
  2. 在 job 级定义 env ENV_LEVEL=job
  3. 在 step 级定义 env ENV_LEVEL=step，step shell 中 echo $ENV_LEVEL
  4. 在同一 job 的另一个 step 中不做 env 映射，直接 echo $ENV_LEVEL
  5. 观测 shell 中实际读到的值

预期结果:
  - 含 step env 的 step 中，$ENV_LEVEL 输出为 step（最内层生效）
  - 不含 step env 映射的 step 中，$ENV_LEVEL 输出为 job（vars 不直接介入 shell 覆盖）
  - 不应出现「step env 定义但 shell 中读不到」或「vars 静默覆盖 env」的情况

验证点:
  - [正向] workflow/job/step 三级同名 env，step 读取 $ENV_LEVEL 验证最内层生效
  - [负向] 不应出现「step env 定义但 shell 中读不到」（历史 TC-533）；不应出现「vars 与 env 同名时 vars 静默覆盖 env 使 shell 读到 vars 值」
  - [非功能] 优先级链文档表述与实测一致；vars 如何进入 shell 环境（显式映射 vs 自动合并）清晰

清理:      无
