<!-- auto-generated from gitcode-pipeline-test-cases.xlsx | generated: 2026-07-20 -->

# GitCode 流水线第一版测试用例清单

> 来源: `phase01/inputs/existing-cases/gitcode-pipeline-test-cases.xlsx`
> 本文为 agent 预处理版本，agent 应**直接读取本 Markdown**，无需再解析 Excel。
> 共 5 个 sheet：问题、测试用例清单、输入、按章节统计、按分类统计。

---

## 问题

**22 条记录**

| 用例ID | 预期和问题现象 | 严重等级 | 提出人 |
|---|---|---|---|
| TC-064 | 预期：PR 状态应返回 open。<br>现象：GitCode 返回 opened，导致断言失败。 | P2 | 李超然 |
| TC-234 | 预期：配置 types: [open,reopen,update] 后，匹配类型的 PR 事件应触发独立 Job。<br>现象：PR 更新提交后没有对应 workflow 运行。 | P1 | 李超然 |
| TC-236 | 预期：修改 tc-tests/api/** 路径的 PR 应触发独立 Job。<br>现象：满足 paths 条件的 PR 变更没有对应 workflow 运行。 | P1 | 李超然 |
| TC-461 | 预期：PR open 应触发 pull_request_target 的独立 Job。<br>现象：PR open 未触发；同名运行来自 PUSH，且在 Job 创建前失败。 | P1 | 李超然 |
| TC-463 | 预期：未指定 types 时，pull_request_target 的默认 open/reopen/update 类型应触发。<br>现象：PR open 没有创建对应 workflow 运行。 | P1 | 李超然 |
| TC-561 | 预期：合并 PR 应触发 pull_request 的 merge 独立 Job。<br>现象：合并后只出现 PUSH 运行，且运行在 Job 创建前失败 | P1 | 李超然 |
| TC-502 | 预期：Action 中使用 GitCode 工具调用 API，发布 PR 检查结果评论。<br>现象：runner 未提供类似 gh 的 GitCode CLI/API 工具，gitcode pr comment 报 command not found。 | P2 | 李超然 |
| TC-310 | setup-java 插件不存在 | P2 | 陈琦 |
| TC-499 | python -m build 构建失败 | P2 | 陈琦 |
| TC-486/481/499 | needs: 指向 matrix 父 job 导致"任务初始化错误" | P1 | 陈琦 |
| TC-163 | 使用字面量整数 | P3 | 李洋行 |
| TC-137/138 | 在Action中使用runner上下文<br>runner.os 返回 linux，文档应为 Linux（大小写错误） | P3 | 李洋行 |
| TC-095 | runner.arch 返回 x86_64，文档应为 X64（格式错误） | P3 | 李洋行 |
| TC-317-321 | 条件执行函数问题 | P2 | 李洋行 |
| TC-206 | 系统变量 ATOMGIT_REPOSITORY_OWNER 未注入 Runner | P2 | 李洋行 |
| S3 × 24 + TC-391 | Scheduler 不工作：两个仓库、多次 cron 配置，从未产生 Schedule Run。文档声明的定时触发、cron 运算符、UTC 时区、默认分支、最小间隔等全部无法验证 | P1 | 尹昱林 |
| TC-533 | Runner 不注入 Job env 到 Shell：表达式层 ${{ env.VAR }} 正常但 Bash $VAR 恒为 UNSET。违反文档声明"变量注入 Runner"和"env > vars"优先级链 | P1 | 尹昱林 |
| TC-220 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS 默认值缺失 | P2 | 尹昱林 |
| TC-273 | Job 容器不可用：文档声明的 container.image 能力无法使用 | P2 | 尹昱林 |
| TC-010 | environment 字段不被平台识别：语法检查报 unknown property。文档仅描述环境 Secret 审批功能，未提供环境绑定 YAML 语法 | P2 | 尹昱林 |
| TC-534 | vars > ATOMGIT_* 优先级无法验证：平台禁止创建 ATOMGIT_ 前缀的项目 Variable（与系统变量冲突） | P2 | 尹昱林 |
| TC-390 | Docker 构建能力无法验证：缺少 Docker Registry 和镜像推送资源 | P3 | 尹昱林 |
---

## 测试用例清单

**629 条用例**（21 列）

| 用例ID | 文档章节 | 测试分类 | 测试对象 | 类型 | 引用语法 | 测试内容 | 预期结果 | YAML示例片段 | 触发事件 | 备注 | 可验API字段 | JSON路径 | 预期规则 | 真测可达性 | 测试结果 | 失败原因/备注 | 测试会话 | 责任人 | 用例不当 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| TC-001 | core-concepts/variables-secrets-context-expressions | env变量 | env(workflow级) | 变量定义 | ${{env.VAR}} | workflow顶层env定义GLOBAL_VAR | Runner中$GLOBAL_VAR可读 | env:<br>  GLOBAL_VAR: v | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-002 | core-concepts/variables-secrets-context-expressions | env变量 | env(job级) | 变量定义 | ${{env.VAR}} | job内env定义JOB_VAR | 该job可读$JOB_VAR | jobs:<br>  b:<br>    env:<br>      JOB_VAR: v | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-003 | core-concepts/variables-secrets-context-expressions | env变量 | env(step级) | 变量定义 | ${{env.VAR}} | step内env定义STEP_VAR | 该step可读$STEP_VAR | steps:<br>  - env:<br>      STEP_VAR: v | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-004 | core-concepts/variables-secrets-context-expressions | env变量 | env优先级step>job>workflow | 优先级 | ${{env.mascot}} | 三级同名mascot覆盖 | step级覆盖job级覆盖workflow级 | env:<br>  mascot: Mona<br>jobs:<br>  j:<br>    env:<br>      mascot: Tux<br>    steps:<br>      - env:<br>          mascot: Step | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-005 | core-concepts/variables-secrets-context-expressions | vars变量 | vars(组织级) | 配置变量 | ${{vars.VAR}} | 组织设置定义ORG_VAR | 组织下项目可用 | if: ${{vars.USE=='true'}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-006 | core-concepts/variables-secrets-context-expressions | vars变量 | vars(项目级) | 配置变量 | ${{vars.VAR}} | 项目设置定义PROJ_VAR | 仅当前项目可用 | run: echo ${{vars.PROJ_VAR}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-007 | core-concepts/variables-secrets-context-expressions | vars变量 | vars覆盖 | 优先级 | ${{vars.VAR}} | 项目级覆盖组织级 | 取项目级值 | run: echo ${{vars.DUP}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-008 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets(组织级) | 密钥 | ${{secrets.NAME}} | 组织设置定义SECRET_ORG | 组织下项目可用 | env:<br>  T: ${{secrets.SECRET_ORG}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-009 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets(项目级) | 密钥 | ${{secrets.NAME}} | 项目设置定义SECRET_PROJ | 仅当前项目可用 | env:<br>  K: ${{secrets.SECRET_PROJ}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-010 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets(环境级) | 密钥 | ${{secrets.NAME}} | 绑定environment的secrets | 仅job.environment匹配时可用 | jobs:<br>  d:<br>    environment: prod<br>    env:<br>      K: ${{secrets.PROD_KEY}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | FAIL | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-011 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets日志脱敏 | 安全 | ${{secrets.NAME}} | echo secrets值到日志 | 日志中替换为*** | run: echo "${{secrets.T}}" | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-012 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs(workflow_dispatch) | 输入 | ${{inputs.NAME}} | workflow_dispatch定义build_id | 手动触发时取传入值 | on:<br>  workflow_dispatch:<br>    inputs:<br>      build_id:<br>        required: true | workflow_dispatch |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-013 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs(workflow_call) | 输入 | ${{inputs.NAME}} | workflow_call定义deploy_target | 被调用时取传参 | on:<br>  workflow_call:<br>    inputs:<br>      deploy_target:<br>        required: true | workflow_call |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-014 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs仅支持string | 类型约束 | ${{inputs.NAME}} | inputs type只能string | 非string应报错 | inputs:<br>  n:<br>    type: string | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-015 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs default | 输入 | ${{inputs.NAME}} | inputs定义default | 未传参取default | inputs:<br>  env:<br>    default: dev | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(inputs default值仅在workflow_dispatch未传参时生效,无法从shell内部断言),仅验文档约束 | S6 | chaoran |  |
| TC-016 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs required校验 | 输入 | ${{inputs.NAME}} | required=true未传参 | 触发失败/提示缺必填 | inputs:<br>  bid:<br>    required: true | workflow_dispatch |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-017 | syntax-reference/context | 上下文总览 | context:atomgit | 上下文访问 | ${{atomgit.sha}} | 访问atomgit上下文 | 返回平台与事件信息 | run: echo ${atomgit.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-018 | syntax-reference/context | 上下文总览 | context:env | 上下文访问 | ${{env.MY_VAR}} | 访问env上下文 | 返回自定义环境变量 | run: echo ${env.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-019 | syntax-reference/context | 上下文总览 | context:vars | 上下文访问 | ${{vars.DEPLOY_ENV}} | 访问vars上下文 | 返回组织/项目配置变量 | run: echo ${vars.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-A | liyanghang |  |
| TC-020 | syntax-reference/context | 上下文总览 | context:job | 上下文访问 | ${{job.status}} | 访问job上下文 | 返回当前Job信息 | run: echo ${job.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-021 | syntax-reference/context | 上下文总览 | context:jobs | 上下文访问 | ${{jobs.deploy.result}} | 访问jobs上下文 | 返回可复用工作流已运行Job结果 | run: echo ${jobs.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |
| TC-022 | syntax-reference/context | 上下文总览 | context:steps | 上下文访问 | ${{steps.build.outputs.result}} | 访问steps上下文 | 返回当前Job各步骤信息 | run: echo ${steps.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 内步骤无 id 字段，steps 上下文无可引用的条目，无法断言 | Tier-A | liyanghang |  |
| TC-023 | syntax-reference/context | 上下文总览 | context:runner | 上下文访问 | ${{runner.os}} | 访问runner上下文 | 返回Runner执行环境 | run: echo ${runner.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |
| TC-024 | syntax-reference/context | 上下文总览 | context:secrets | 上下文访问 | ${{secrets.DEPLOY_TOKEN}} | 访问secrets上下文 | 返回加密密钥 | run: echo ${secrets.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-025 | syntax-reference/context | 上下文总览 | context:strategy | 上下文访问 | ${{strategy.job-index}} | 访问strategy上下文 | 返回矩阵策略信息 | run: echo ${strategy.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无 matrix 定义，strategy 上下文值无法在 shell 内部断言 | Tier-A | liyanghang |  |
| TC-026 | syntax-reference/context | 上下文总览 | context:matrix | 上下文访问 | ${{matrix.version}} | 访问matrix上下文 | 返回当前矩阵实例变量 | run: echo ${matrix.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无 matrix 定义，matrix 上下文为空，无法断言具体值 | Tier-A | liyanghang |  |
| TC-027 | syntax-reference/context | 上下文总览 | context:inputs | 上下文访问 | ${{inputs.environment}} | 访问inputs上下文 | 返回输入参数 | run: echo ${inputs.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |
| TC-028 | syntax-reference/context | atomgit上下文属性 | atomgit.event_name | 属性(string) | ${{atomgit.event_name}} | 读取atomgit.event_name | 返回当前触发事件名称,示例push | - run: echo ${{atomgit.event_name}} | any |  | event | run.event 或 run_detail.event | push\|pull_request\|schedule\|workflow_dispatch\|issue_comment\|workflow_call | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-029 | syntax-reference/context | atomgit上下文属性 | atomgit.sha | 属性(string) | ${{atomgit.sha}} | 读取atomgit.sha | 返回触发提交SHA,示例a1b2c3 | - run: echo ${{atomgit.sha}} | any |  | commit_id | run.commit_id 或 run_detail.commit_id | 长度=40,非空 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-030 | syntax-reference/context | atomgit上下文属性 | atomgit.ref | 属性(string) | ${{atomgit.ref}} | 读取atomgit.ref | 返回触发引用全名,示例refs/heads/main | - run: echo ${{atomgit.ref}} | any |  | branch | run.branch 或 run_detail.branch | 含 refs/heads/ 或 refs/tags/ 前缀 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-031 | syntax-reference/context | atomgit上下文属性 | atomgit.ref_name | 属性(string) | ${{atomgit.ref_name}} | 读取atomgit.ref_name | 返回触发引用短名,示例main | - run: echo ${{atomgit.ref_name}} | any |  | branch | run.branch 或 run_detail.branch | 不含 refs/ 前缀,如 main/v1 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-032 | syntax-reference/context | atomgit上下文属性 | atomgit.ref_type | 属性(string) | ${{atomgit.ref_type}} | 读取atomgit.ref_type | 返回引用类型branch/tag,示例branch | - run: echo ${{atomgit.ref_type}} | any |  | ref_type | run.ref_type 或 run_detail.ref_type | branch\|tag | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-033 | syntax-reference/context | atomgit上下文属性 | atomgit.event | 属性(object) | ${{atomgit.event}} | 读取atomgit.event | 返回事件完整payload,示例object | - run: echo ${{atomgit.event}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | syntax error near unexpected token '(' — atomgit.event 返回对象字面量，bash无法解析 | Tier-A | liyanghang |  |
| TC-034 | syntax-reference/context | atomgit上下文属性 | atomgit.workspace | 属性(string) | ${{atomgit.workspace}} | 读取atomgit.workspace | 返回Runner工作区路径,示例/home/runner | - run: echo ${{atomgit.workspace}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-035 | syntax-reference/context | atomgit上下文属性 | atomgit.action | 属性(string) | ${{atomgit.action}} | 读取atomgit.action | 返回当前Action名称,示例my-action | - run: echo ${{atomgit.action}} | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-1 | S13 | yulin |  |
| TC-036 | syntax-reference/context | atomgit上下文属性 | atomgit.token | 属性(string) | ${{atomgit.token}} | 读取atomgit.token | 返回ATOMGIT_TOKEN令牌,示例ghs_xxx | - run: echo ${{atomgit.token}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |
| TC-037 | syntax-reference/context | atomgit上下文属性 | atomgit.repository | 属性(string) | ${{atomgit.repository}} | 读取atomgit.repository | 返回仓库全名,示例owner/repo | - run: echo ${{atomgit.repository}} | any |  | repository | run.repository 或 run_detail.repository | owner/repo 形式 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-038 | syntax-reference/context | atomgit上下文属性 | atomgit.repository_owner | 属性(string) | ${{atomgit.repository_owner}} | 读取atomgit.repository_owner | 返回仓库所属组织,示例myorg | - run: echo ${{atomgit.repository_owner}} | any |  | repository_owner | run.repository_owner 或 run_detail.repository_owner | owner 名 | B API字段 | FAIL | FAIL | Tier-B | liyanghang |  |
| TC-039 | syntax-reference/context | atomgit上下文属性 | atomgit.repositoryUrl | 属性(string) | ${{atomgit.repositoryUrl}} | 读取atomgit.repositoryUrl | 返回仓库URL,示例https:// | - run: echo ${{atomgit.repositoryUrl}} | any |  | https_url | run.https_url 或 run_detail.https_url | https://gitcode.com/owner/repo 形式 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-040 | syntax-reference/context | atomgit上下文属性 | atomgit.run_id | 属性(string) | ${{atomgit.run_id}} | 读取atomgit.run_id | 返回工作流运行ID,示例12345 | - run: echo ${{atomgit.run_id}} | any |  | pipeline_run_id | run.pipeline_run_id 或 run_detail.pipeline_run_id | 非空,唯一 | B API字段 | FAIL | FAIL | Tier-B | liyanghang |  |
| TC-041 | syntax-reference/context | atomgit上下文属性 | atomgit.run_number | 属性(number) | ${{atomgit.run_number}} | 读取atomgit.run_number | 返回工作流运行编号,示例42 | - run: echo ${{atomgit.run_number}} | any |  | run_number | run.run_number 或 run_detail.run_number | 递增整数 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-042 | syntax-reference/context | atomgit上下文属性 | atomgit.run_attempt | 属性(number) | ${{atomgit.run_attempt}} | 读取atomgit.run_attempt | 返回工作流重试次数,示例1 | - run: echo ${{atomgit.run_attempt}} | any |  | run_attempt | run.run_attempt 或 run_detail.run_attempt | 重运行次数,首次=1 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-043 | syntax-reference/context | atomgit上下文属性 | atomgit.workflow | 属性(string) | ${{atomgit.workflow}} | 读取atomgit.workflow | 返回工作流名称,示例CI | - run: echo ${{atomgit.workflow}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-044 | syntax-reference/context | atomgit上下文属性 | atomgit.head_ref | 属性(string) | ${{atomgit.head_ref}} | 读取atomgit.head_ref | 返回PR源分支(仅PR),示例feature/x | - run: echo ${{atomgit.head_ref}} | any |  | head_ref | run.head_ref 或 run_detail.head_ref | PR 源分支,非 push 事件时空 | B API字段 | FAIL | FAIL | Tier-B | liyanghang |  |
| TC-045 | syntax-reference/context | atomgit上下文属性 | atomgit.base_ref | 属性(string) | ${{atomgit.base_ref}} | 读取atomgit.base_ref | 返回PR目标分支(仅PR),示例main | - run: echo ${{atomgit.base_ref}} | any |  | base_ref | run.base_ref 或 run_detail.base_ref | PR 目标分支,非 push 事件时空 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |
| TC-046 | syntax-reference/context | atomgit上下文属性 | atomgit.server_url | 属性(string) | ${{atomgit.server_url}} | 读取atomgit.server_url | 返回平台根URL,示例https://atomgit.com | - run: echo ${{atomgit.server_url}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-047 | syntax-reference/context | atomgit上下文属性 | atomgit.api_url | 属性(string) | ${{atomgit.api_url}} | 读取atomgit.api_url | 返回API基础URL,示例https://api.atomgit.com | - run: echo ${{atomgit.api_url}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-048 | syntax-reference/context | push事件字段 | atomgit.event.ref | 事件字段 | ${{atomgit.event.ref}} | push读取event.ref | 返回推送的完整ref | - run: echo ${{atomgit.event.ref}} | push |  | branch | run.branch 或 run_detail.branch | push 事件时=branch,非空 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-049 | syntax-reference/context | push事件字段 | atomgit.event.before | 事件字段 | ${{atomgit.event.before}} | push读取event.before | 返回推送前SHA | - run: echo ${{atomgit.event.before}} | push |  | before | run.before 或 run_detail.before | push 事件时=前一 commit SHA,非空 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-050 | syntax-reference/context | push事件字段 | atomgit.event.after | 事件字段 | ${{atomgit.event.after}} | push读取event.after | 返回推送后SHA | - run: echo ${{atomgit.event.after}} | push |  | after | run.after 或 run_detail.after | push 事件时=当前 commit SHA,非空 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-051 | syntax-reference/context | push事件字段 | atomgit.event.commits | 事件字段 | ${{atomgit.event.commits}} | push读取event.commits | 返回提交列表数组 | - run: echo ${{atomgit.event.commits}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-052 | syntax-reference/context | push事件字段 | atomgit.event.commits[].id | 事件字段 | ${{atomgit.event.commits[].id}} | push读取event.commits[].id | 返回单提交SHA | - run: echo ${{atomgit.event.commits[].id}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-053 | syntax-reference/context | push事件字段 | atomgit.event.commits[].message | 事件字段 | ${{atomgit.event.commits[].message}} | push读取event.commits[].message | 返回提交消息 | - run: echo ${{atomgit.event.commits[].message}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-054 | syntax-reference/context | push事件字段 | atomgit.event.commits[].author | 事件字段 | ${{atomgit.event.commits[].author}} | push读取event.commits[].author | 返回提交作者 | - run: echo ${{atomgit.event.commits[].author}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-055 | syntax-reference/context | push事件字段 | atomgit.event.commits[].added | 事件字段 | ${{atomgit.event.commits[].added}} | push读取event.commits[].added | 返回新增文件列表 | - run: echo ${{atomgit.event.commits[].added}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-056 | syntax-reference/context | push事件字段 | atomgit.event.commits[].modified | 事件字段 | ${{atomgit.event.commits[].modified}} | push读取event.commits[].modified | 返回修改文件列表 | - run: echo ${{atomgit.event.commits[].modified}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-057 | syntax-reference/context | push事件字段 | atomgit.event.commits[].removed | 事件字段 | ${{atomgit.event.commits[].removed}} | push读取event.commits[].removed | 返回删除文件列表 | - run: echo ${{atomgit.event.commits[].removed}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-058 | syntax-reference/context | push事件字段 | atomgit.event.base_ref | 事件字段 | ${{atomgit.event.base_ref}} | push读取event.base_ref | 返回基础ref | - run: echo ${{atomgit.event.base_ref}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-059 | syntax-reference/context | push事件字段 | atomgit.event.created | 事件字段 | ${{atomgit.event.created}} | push读取event.created | 返回是否新创建ref | - run: echo ${{atomgit.event.created}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-060 | syntax-reference/context | push事件字段 | atomgit.event.deleted | 事件字段 | ${{atomgit.event.deleted}} | push读取event.deleted | 返回是否删除ref | - run: echo ${{atomgit.event.deleted}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-061 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.number | 事件字段 | ${{atomgit.event.pull_request.number}} | PR读取event.pull_request.number | 返回PR编号 | - run: echo ${{atomgit.event.pull_request.number}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-062 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.title | 事件字段 | ${{atomgit.event.pull_request.title}} | PR读取event.pull_request.title | 返回PR标题 | - run: echo ${{atomgit.event.pull_request.title}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-063 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.body | 事件字段 | ${{atomgit.event.pull_request.body}} | PR读取event.pull_request.body | 返回PR描述 | - run: echo ${{atomgit.event.pull_request.body}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-064 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.state | 事件字段 | ${{atomgit.event.pull_request.state}} | PR读取event.pull_request.state | 返回PR状态open/closed | - run: echo ${{atomgit.event.pull_request.state}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-065 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.user.login | 事件字段 | ${{atomgit.event.pull_request.user.login}} | PR读取event.pull_request.user.login | 返回PR创建者 | - run: echo ${{atomgit.event.pull_request.user.login}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-066 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.head.ref | 事件字段 | ${{atomgit.event.pull_request.head.ref}} | PR读取event.pull_request.head.ref | 返回PR源分支名 | - run: echo ${{atomgit.event.pull_request.head.ref}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-067 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.head.sha | 事件字段 | ${{atomgit.event.pull_request.head.sha}} | PR读取event.pull_request.head.sha | 返回PR源分支最新SHA | - run: echo ${{atomgit.event.pull_request.head.sha}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-068 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.head.repo.full_name | 事件字段 | ${{atomgit.event.pull_request.head.repo.full_name}} | PR读取event.pull_request.head.repo.full_name | 返回PR源仓库全名 | - run: echo ${{atomgit.event.pull_request.head.repo.full_name}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-069 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.base.ref | 事件字段 | ${{atomgit.event.pull_request.base.ref}} | PR读取event.pull_request.base.ref | 返回PR目标分支名 | - run: echo ${{atomgit.event.pull_request.base.ref}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-070 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.base.repo.full_name | 事件字段 | ${{atomgit.event.pull_request.base.repo.full_name}} | PR读取event.pull_request.base.repo.full_name | 返回PR目标仓库全名 | - run: echo ${{atomgit.event.pull_request.base.repo.full_name}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-071 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.labels | 事件字段 | ${{atomgit.event.pull_request.labels}} | PR读取event.pull_request.labels | 返回PR标签列表 | - run: echo ${{atomgit.event.pull_request.labels}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-072 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.merged | 事件字段 | ${{atomgit.event.pull_request.merged}} | PR读取event.pull_request.merged | 返回PR是否已合并 | - run: echo ${{atomgit.event.pull_request.merged}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-073 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.draft | 事件字段 | ${{atomgit.event.pull_request.draft}} | PR读取event.pull_request.draft | 返回PR是否Draft | - run: echo ${{atomgit.event.pull_request.draft}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-074 | syntax-reference/context | pull_request事件字段 | atomgit.event.action | 事件字段 | ${{atomgit.event.action}} | PR读取event.action | 返回PR事件动作类型 | - run: echo ${{atomgit.event.action}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |
| TC-075 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.id | 事件字段 | ${{atomgit.event.comment.id}} | issue_comment读取event.comment.id | 返回评论ID | - run: echo ${{atomgit.event.comment.id}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-076 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.body | 事件字段 | ${{atomgit.event.comment.body}} | issue_comment读取event.comment.body | 返回评论内容 | - run: echo ${{atomgit.event.comment.body}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-077 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.user.login | 事件字段 | ${{atomgit.event.comment.user.login}} | issue_comment读取event.comment.user.login | 返回评论者 | - run: echo ${{atomgit.event.comment.user.login}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-078 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.created_at | 事件字段 | ${{atomgit.event.comment.created_at}} | issue_comment读取event.comment.created_at | 返回评论创建时间 | - run: echo ${{atomgit.event.comment.created_at}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-079 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.number | 事件字段 | ${{atomgit.event.issue.number}} | issue_comment读取event.issue.number | 返回Issue编号 | - run: echo ${{atomgit.event.issue.number}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-080 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.title | 事件字段 | ${{atomgit.event.issue.title}} | issue_comment读取event.issue.title | 返回Issue标题 | - run: echo ${{atomgit.event.issue.title}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-081 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.state | 事件字段 | ${{atomgit.event.issue.state}} | issue_comment读取event.issue.state | 返回Issue状态 | - run: echo ${{atomgit.event.issue.state}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-082 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.pull_request | 事件字段 | ${{atomgit.event.issue.pull_request}} | issue_comment读取event.issue.pull_request | 返回是否PR评论 | - run: echo ${{atomgit.event.issue.pull_request}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-083 | syntax-reference/context | issue_comment事件字段 | atomgit.event.action | 事件字段 | ${{atomgit.event.action}} | issue_comment读取event.action | 返回动作类型 | - run: echo ${{atomgit.event.action}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |
| TC-084 | syntax-reference/context | workflow_dispatch事件字段 | atomgit.event.inputs | 事件字段 | ${{atomgit.event.inputs}} | 读取手动触发输入参数对象 | 返回inputs对象 | - run: echo ${{atomgit.event.inputs}} | workflow_dispatch |  | inputs | run.inputs 或 run_detail.inputs | workflow_dispatch 事件时含触发参数 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-085 | syntax-reference/context | schedule事件字段 | atomgit.event.schedule | 事件字段 | ${{atomgit.event.schedule}} | 读取cron表达式列表 | 返回schedule数组 | - run: echo ${{atomgit.event.schedule}} | schedule |  | schedule | run.schedule 或 run_detail.schedule | schedule 事件时含 cron 表达式 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-086 | syntax-reference/context | env上下文 | env.first_name | 属性 | ${{env.first_name}} | 读取env上下文first_name | 返回Mona | - run: echo ${{env.first_name}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-087 | syntax-reference/context | env上下文 | env.super_duper_var | 属性 | ${{env.super_duper_var}} | 读取env上下文 | 返回totally_awesome | - run: echo ${{env.super_duper_var}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-088 | syntax-reference/context | job上下文 | job.status | 属性 | ${{job.status}} | 读取Job状态 | 返回success/failure/cancelled | - if: ${{job.status=='success'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-089 | syntax-reference/context | job上下文 | job.container | 属性 | ${{job.container}} | 读取自定义构建环境 | 返回container Object | - run: echo ${{job.container}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 未定义 container，job.container 为空对象，无法断言具体值 | Tier-A | liyanghang |  |
| TC-090 | syntax-reference/context | steps上下文 | steps.checkout.outputs | 属性 | ${{steps.checkout.outputs}} | 读取steps.checkout.outputs | 返回步骤输出对象 | - run: echo ${{steps.checkout.outputs}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-091 | syntax-reference/context | steps上下文 | steps.checkout.outcome | 属性 | ${{steps.checkout.outcome}} | 读取steps.checkout.outcome | 返回apply continue-on-error前结果 | - run: echo ${{steps.checkout.outcome}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-092 | syntax-reference/context | steps上下文 | steps.checkout.conclusion | 属性 | ${{steps.checkout.conclusion}} | 读取steps.checkout.conclusion | 返回apply后结果 | - run: echo ${{steps.checkout.conclusion}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-093 | syntax-reference/context | steps上下文 | steps.generate_number.outputs.random_number | 属性 | ${{steps.generate_number.outputs.random_number}} | 读取steps.generate_number.outputs.random_number | 返回步骤单输出值 | - run: echo ${{steps.generate_number.outputs.random_number}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-094 | syntax-reference/context | runner上下文 | runner.os | 属性 | ${{runner.os}} | 读取runner.os | 返回Linux/Windows/macOS | - run: echo ${{runner.os}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |
| TC-095 | syntax-reference/context | runner上下文 | runner.arch | 属性 | ${{runner.arch}} | 读取runner.arch | 返回X64/ARM/ARM64 | - run: echo ${{runner.arch}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=x86_64 | Tier-A | liyanghang |  |
| TC-096 | syntax-reference/context | runner上下文 | runner.name | 属性 | ${{runner.name}} | 读取runner.name | 返回Runner名称 | - run: echo ${{runner.name}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-097 | syntax-reference/context | runner上下文 | runner.temp | 属性 | ${{runner.temp}} | 读取runner.temp | 返回Runner临时目录 | - run: echo ${{runner.temp}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-098 | syntax-reference/context | runner上下文 | runner.tool_cache | 属性 | ${{runner.tool_cache}} | 读取runner.tool_cache | 返回Runner工具缓存目录 | - run: echo ${{runner.tool_cache}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-099 | syntax-reference/context | runner上下文 | runner.debug | 属性 | ${{runner.debug}} | 读取runner.debug | 返回是否debug | - run: echo ${{runner.debug}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |
| TC-100 | syntax-reference/context | secrets上下文 | secrets.atomgit_token | 属性 | ${{secrets.atomgit_token}} | 读取atomgit_token | 返回***脱敏 | env:<br>  T: ${{secrets.atomgit_token}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-101 | syntax-reference/context | secrets上下文 | secrets.NPM_TOKEN | 属性 | ${{secrets.NPM_TOKEN}} | 读取NPM_TOKEN | 返回***脱敏 | env:<br>  T: ${{secrets.NPM_TOKEN}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-102 | syntax-reference/context | secrets上下文 | secrets.SUPERSECRET | 属性 | ${{secrets.SUPERSECRET}} | 读取SUPERSECRET | 返回***脱敏 | env:<br>  T: ${{secrets.SUPERSECRET}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-103 | syntax-reference/context | matrix上下文 | matrix.os | 属性 | ${{matrix.os}} | 读取矩阵os值 | 返回ubuntu-latest | - run: echo ${{matrix.os}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 当前 job 无 matrix 定义，matrix.os 为空，无法断言 | Tier-A | liyanghang |  |
| TC-104 | syntax-reference/context | matrix上下文 | matrix.node | 属性 | ${{matrix.node}} | 读取矩阵node值 | 返回16 | - run: echo ${{matrix.node}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 当前 job 无 matrix 定义，matrix.node 为空，无法断言 | Tier-A | liyanghang |  |
| TC-105 | syntax-reference/context | 上下文可用性表 | atomgit@workflow级别 | 可用性 | ${{atomgit.x}} | 在workflow级别使用atomgit上下文 | 应可用 | # workflow级别<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-106 | syntax-reference/context | 上下文可用性表 | atomgit@job级别 | 可用性 | ${{atomgit.x}} | 在job级别使用atomgit上下文 | 应可用 | # job级别<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-107 | syntax-reference/context | 上下文可用性表 | atomgit@step级别 | 可用性 | ${{atomgit.x}} | 在step级别使用atomgit上下文 | 应可用 | # step级别<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-108 | syntax-reference/context | 上下文可用性表 | atomgit@条件表达式(if) | 可用性 | ${{atomgit.x}} | 在条件表达式(if)使用atomgit上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-109 | syntax-reference/context | 上下文可用性表 | atomgit@Action中 | 可用性 | ${{atomgit.x}} | 在Action中使用atomgit上下文 | 应可用 | # Action中<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-110 | syntax-reference/context | 上下文可用性表 | env@workflow级别 | 可用性 | ${{env.x}} | 在workflow级别使用env上下文 | 应可用 | # workflow级别<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-111 | syntax-reference/context | 上下文可用性表 | env@job级别 | 可用性 | ${{env.x}} | 在job级别使用env上下文 | 应可用 | # job级别<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-112 | syntax-reference/context | 上下文可用性表 | env@step级别 | 可用性 | ${{env.x}} | 在step级别使用env上下文 | 应可用 | # step级别<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-113 | syntax-reference/context | 上下文可用性表 | env@条件表达式(if) | 可用性 | ${{env.x}} | 在条件表达式(if)使用env上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-114 | syntax-reference/context | 上下文可用性表 | env@Action中 | 可用性 | ${{env.x}} | 在Action中使用env上下文 | 应可用 | # Action中<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-115 | syntax-reference/context | 上下文可用性表 | vars@workflow级别 | 可用性 | ${{vars.x}} | 在workflow级别使用vars上下文 | 应可用 | # workflow级别<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |
| TC-116 | syntax-reference/context | 上下文可用性表 | vars@job级别 | 可用性 | ${{vars.x}} | 在job级别使用vars上下文 | 应可用 | # job级别<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |
| TC-117 | syntax-reference/context | 上下文可用性表 | vars@step级别 | 可用性 | ${{vars.x}} | 在step级别使用vars上下文 | 应可用 | # step级别<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |
| TC-118 | syntax-reference/context | 上下文可用性表 | vars@条件表达式(if) | 可用性 | ${{vars.x}} | 在条件表达式(if)使用vars上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |
| TC-119 | syntax-reference/context | 上下文可用性表 | vars@Action中 | 可用性 | ${{vars.x}} | 在Action中使用vars上下文 | 应可用 | # Action中<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |
| TC-120 | syntax-reference/context | 上下文可用性表 | job@workflow级别 | 可用性 | ${{job.x}} | 在workflow级别使用job上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |
| TC-121 | syntax-reference/context | 上下文可用性表 | job@job级别 | 可用性 | ${{job.x}} | 在job级别使用job上下文 | 应可用 | # job级别<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-122 | syntax-reference/context | 上下文可用性表 | job@step级别 | 可用性 | ${{job.x}} | 在step级别使用job上下文 | 应可用 | # step级别<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-123 | syntax-reference/context | 上下文可用性表 | job@条件表达式(if) | 可用性 | ${{job.x}} | 在条件表达式(if)使用job上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-124 | syntax-reference/context | 上下文可用性表 | job@Action中 | 可用性 | ${{job.x}} | 在Action中使用job上下文 | 应可用 | # Action中<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-125 | syntax-reference/context | 上下文可用性表 | jobs@workflow级别(调用方) | 可用性 | ${{jobs.x}} | 在workflow级别(调用方)使用jobs上下文 | 应可用 | # workflow级别(调用方)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |
| TC-126 | syntax-reference/context | 上下文可用性表 | jobs@job级别(调用方) | 可用性 | ${{jobs.x}} | 在job级别(调用方)使用jobs上下文 | 应可用 | # job级别(调用方)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |
| TC-127 | syntax-reference/context | 上下文可用性表 | jobs@step级别(调用方) | 可用性 | ${{jobs.x}} | 在step级别(调用方)使用jobs上下文 | 应可用 | # step级别(调用方)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |
| TC-128 | syntax-reference/context | 上下文可用性表 | jobs@条件表达式(if) | 可用性 | ${{jobs.x}} | 在条件表达式(if)使用jobs上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |
| TC-129 | syntax-reference/context | 上下文可用性表 | jobs@Action中 | 可用性 | ${{jobs.x}} | 在Action中使用jobs上下文 | 不可用/报错 | # Action中<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（Action 中不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |
| TC-130 | syntax-reference/context | 上下文可用性表 | steps@workflow级别 | 可用性 | ${{steps.x}} | 在workflow级别使用steps上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |
| TC-131 | syntax-reference/context | 上下文可用性表 | steps@job级别(步骤后) | 可用性 | ${{steps.x}} | 在job级别(步骤后)使用steps上下文 | 应可用 | # job级别(步骤后)<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |
| TC-132 | syntax-reference/context | 上下文可用性表 | steps@step级别(当前步骤后) | 可用性 | ${{steps.x}} | 在step级别(当前步骤后)使用steps上下文 | 应可用 | # step级别(当前步骤后)<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |
| TC-133 | syntax-reference/context | 上下文可用性表 | steps@条件表达式(if) | 可用性 | ${{steps.x}} | 在条件表达式(if)使用steps上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |
| TC-134 | syntax-reference/context | 上下文可用性表 | steps@Action中 | 可用性 | ${{steps.x}} | 在Action中使用steps上下文 | 应可用 | # Action中<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |
| TC-135 | syntax-reference/context | 上下文可用性表 | runner@workflow级别 | 可用性 | ${{runner.x}} | 在workflow级别使用runner上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |
| TC-136 | syntax-reference/context | 上下文可用性表 | runner@job级别 | 可用性 | ${{runner.x}} | 在job级别使用runner上下文 | 应可用 | # job级别<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |
| TC-137 | syntax-reference/context | 上下文可用性表 | runner@step级别 | 可用性 | ${{runner.x}} | 在step级别使用runner上下文 | 应可用 | # step级别<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |
| TC-138 | syntax-reference/context | 上下文可用性表 | runner@条件表达式(if) | 可用性 | ${{runner.x}} | 在条件表达式(if)使用runner上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |
| TC-139 | syntax-reference/context | 上下文可用性表 | runner@Action中 | 可用性 | ${{runner.x}} | 在Action中使用runner上下文 | 应可用 | # Action中<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |
| TC-140 | syntax-reference/context | 上下文可用性表 | secrets@workflow级别 | 可用性 | ${{secrets.x}} | 在workflow级别使用secrets上下文 | 应可用 | # workflow级别<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-141 | syntax-reference/context | 上下文可用性表 | secrets@job级别 | 可用性 | ${{secrets.x}} | 在job级别使用secrets上下文 | 应可用 | # job级别<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-142 | syntax-reference/context | 上下文可用性表 | secrets@step级别 | 可用性 | ${{secrets.x}} | 在step级别使用secrets上下文 | 应可用 | # step级别<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-143 | syntax-reference/context | 上下文可用性表 | secrets@条件表达式(if) | 可用性 | ${{secrets.x}} | 在条件表达式(if)使用secrets上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-144 | syntax-reference/context | 上下文可用性表 | secrets@Action中 | 可用性 | ${{secrets.x}} | 在Action中使用secrets上下文 | 应可用 | # Action中<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-145 | syntax-reference/context | 上下文可用性表 | strategy@workflow级别 | 可用性 | ${{strategy.x}} | 在workflow级别使用strategy上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |
| TC-146 | syntax-reference/context | 上下文可用性表 | strategy@job级别 | 可用性 | ${{strategy.x}} | 在job级别使用strategy上下文 | 应可用 | # job级别<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-147 | syntax-reference/context | 上下文可用性表 | strategy@step级别 | 可用性 | ${{strategy.x}} | 在step级别使用strategy上下文 | 应可用 | # step级别<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-148 | syntax-reference/context | 上下文可用性表 | strategy@条件表达式(if) | 可用性 | ${{strategy.x}} | 在条件表达式(if)使用strategy上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |
| TC-149 | syntax-reference/context | 上下文可用性表 | strategy@Action中 | 可用性 | ${{strategy.x}} | 在Action中使用strategy上下文 | 不可用/报错 | # Action中<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |
| TC-150 | syntax-reference/context | 上下文可用性表 | matrix@workflow级别 | 可用性 | ${{matrix.x}} | 在workflow级别使用matrix上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |

> ⚠️ 仅展示前 150 条，完整 629 条请查看底部折叠区

| TC-151 | syntax-reference/context | 上下文可用性表 | matrix@job级别 | 可用性 | ${{matrix.x}} | 在job级别使用matrix上下文 | 应可用 | # job级别<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-152 | syntax-reference/context | 上下文可用性表 | matrix@step级别 | 可用性 | ${{matrix.x}} | 在step级别使用matrix上下文 | 应可用 | # step级别<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-153 | syntax-reference/context | 上下文可用性表 | matrix@条件表达式(if) | 可用性 | ${{matrix.x}} | 在条件表达式(if)使用matrix上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |
| TC-154 | syntax-reference/context | 上下文可用性表 | matrix@Action中 | 可用性 | ${{matrix.x}} | 在Action中使用matrix上下文 | 不可用/报错 | # Action中<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | SKIP: 平台侧校验行为（Action 中不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |
| TC-155 | syntax-reference/context | 上下文可用性表 | inputs@workflow级别 | 可用性 | ${{inputs.x}} | 在workflow级别使用inputs上下文 | 应可用 | # workflow级别<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-D | liyanghang |  |
| TC-156 | syntax-reference/context | 上下文可用性表 | inputs@job级别 | 可用性 | ${{inputs.x}} | 在job级别使用inputs上下文 | 应可用 | # job级别<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |
| TC-157 | syntax-reference/context | 上下文可用性表 | inputs@step级别 | 可用性 | ${{inputs.x}} | 在step级别使用inputs上下文 | 应可用 | # step级别<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |
| TC-158 | syntax-reference/context | 上下文可用性表 | inputs@条件表达式(if) | 可用性 | ${{inputs.x}} | 在条件表达式(if)使用inputs上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |
| TC-159 | syntax-reference/context | 上下文可用性表 | inputs@Action中 | 可用性 | ${{inputs.x}} | 在Action中使用inputs上下文 | 应可用 | # Action中<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |
| TC-160 | syntax-reference/expressions | 字面量 | 布尔true | 布尔 | ${{true}} | 使用字面量布尔true | 返回true | - if: ${{true}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-161 | syntax-reference/expressions | 字面量 | 布尔false | 布尔 | ${{false}} | 使用字面量布尔false | 返回false | - if: ${{false}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-162 | syntax-reference/expressions | 字面量 | null | null | ${{null}} | 使用字面量null | 返回null | - if: ${{null}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-163 | syntax-reference/expressions | 字面量 | 整数 | 数字 | ${{42}} | 使用字面量整数 | 返回42 | - if: ${{42}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 期望42,实际=42.0 | Tier-A | liyanghang |  |
| TC-164 | syntax-reference/expressions | 字面量 | 浮点 | 数字 | ${{3.14}} | 使用字面量浮点 | 返回3.14 | - if: ${{3.14}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-165 | syntax-reference/expressions | 字面量 | 字符串 | 字符串 | ${{'hello'}} | 使用字面量字符串 | 返回hello | - if: ${{'hello'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-166 | syntax-reference/expressions | 运算符 |  | 运算符 | ${{atomgit.ref=='refs/heads/main'}} | 使用运算符== | 分支等于main时true | - if: ${{atomgit.ref=='refs/heads/main'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-167 | syntax-reference/expressions | 运算符 | != | 运算符 | ${{atomgit.event_name!='schedule'}} | 使用运算符!= | 非定时事件true | - if: ${{atomgit.event_name!='schedule'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-168 | syntax-reference/expressions | 运算符 | ! | 运算符 | ${{!success}} | 使用运算符! | 前置非成功时true | - if: ${{!success}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-169 | syntax-reference/expressions | 运算符 | && | 运算符 | ${{success && atomgit.ref=='refs/heads/main'}} | 使用运算符&& | 成功且main时true | - if: ${{success && atomgit.ref=='refs/heads/main'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-170 | syntax-reference/expressions | 运算符 | \|\| | 运算符 | ${{failed \|\| cancelled}} | 使用运算符\|\| | 失败或取消时true | - if: ${{failed \|\| cancelled}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-171 | syntax-reference/expressions | 运算符 | > | 运算符 | ${{matrix.version>12}} | 使用运算符> | version>12时true | - if: ${{matrix.version>12}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-172 | syntax-reference/expressions | 运算符 | < | 运算符 | ${{matrix.version<14}} | 使用运算符< | version<14时true | - if: ${{matrix.version<14}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-173 | syntax-reference/expressions | 运算符 | >= | 运算符 | ${{strategy.job-total>=3}} | 使用运算符>= | job总数>=3时true | - if: ${{strategy.job-total>=3}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-174 | syntax-reference/expressions | 运算符 | <= | 运算符 | ${{inputs.count<=10}} | 使用运算符<= | count<=10时true | - if: ${{inputs.count<=10}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-175 | syntax-reference/expressions | 运算符优先级 | !>比较>==>&&>\|\| | 优先级 | ${{!a && b \|\| c}} | 验证运算符优先级 | 按!→比较→==→&&→\|\|求值 | - if: ${{!cancelled && success \|\| failed}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-176 | syntax-reference/expressions | 函数 | success | 函数 | ${{success}} | 调用函数success | 所有前置成功时true | - run: echo ${{success}} | any |  | status | run.status | SUCCESS,成功 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |
| TC-177 | syntax-reference/expressions | 函数 | always | 函数 | ${{always}} | 调用函数always | 任何情况true | - run: echo ${{always}} | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |
| TC-178 | syntax-reference/expressions | 函数 | cancelled | 函数 | ${{cancelled}} | 调用函数cancelled | 工作流取消时true | - run: echo ${{cancelled}} | any |  | status | run.status | CANCELLED,被取消 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |
| TC-179 | syntax-reference/expressions | 函数 | failed | 函数 | ${{failed}} | 调用函数failed | 任一前置失败时true | - run: echo ${{failed}} | any |  | status | run.status | FAILED,触发失败传播 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |
| TC-180 | syntax-reference/expressions | 函数 | contains | 函数 | ${{contains(atomgit.ref,'release')}} | 调用函数contains | ref含release时true | - run: echo ${{contains(atomgit.ref,'release')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-181 | syntax-reference/expressions | 函数 | startsWith | 函数 | ${{startsWith(atomgit.ref,'refs/tags/')}} | 调用函数startsWith | ref以refs/tags/开头时true | - run: echo ${{startsWith(atomgit.ref,'refs/tags/')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-182 | syntax-reference/expressions | 函数 | endsWith | 函数 | ${{endsWith(atomgit.ref_name,'.rc')}} | 调用函数endsWith | ref_name以.rc结尾时true | - run: echo ${{endsWith(atomgit.ref_name,'.rc')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-183 | syntax-reference/expressions | 函数 | format | 函数 | ${{format('Hello {0}!',name)}} | 调用函数format | 返回Hello <name>! | - run: echo ${{format('Hello {0}!',name)}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-184 | syntax-reference/expressions | 函数 | substring | 函数 | ${{substring(atomgit.sha,0,7)}} | 调用函数substring | 返回sha前7位 | - run: echo ${{substring(atomgit.sha,0,7)}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-185 | syntax-reference/expressions | 函数 | replace | 函数 | ${{replace(atomgit.ref,'refs/heads/','')}} | 调用函数replace | 返回main去掉前缀 | - run: echo ${{replace(atomgit.ref,'refs/heads/','')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-186 | syntax-reference/expressions | 函数 | hashFiles | 函数 | ${{hashFiles('src/**','package.json')}} | 调用函数hashFiles | 返回组合SHA256 | - run: echo ${{hashFiles('src/**','package.json')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-187 | syntax-reference/expressions | 函数 | toJson | 函数 | ${{toJson(atomgit.event)}} | 调用函数toJson | 返回event的JSON字符串 | - run: echo ${{toJson(atomgit.event)}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-188 | syntax-reference/expressions | 表达式示例 | 仅main且成功时执行 | 表达式示例 | - | 验证示例:仅main且成功时执行 | Deploy to production | if: ${{success && atomgit.ref=='refs/heads/main'}} | any | 组合条件 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: if条件只能通过步骤是否执行来观察,无法在run块内验证 | Tier-A | liyanghang |  |
| TC-189 | syntax-reference/expressions | 表达式示例 | 失败或取消仍执行清理 | 表达式示例 | - | 验证示例:失败或取消仍执行清理 | Cleanup resources | if: ${{always}} | any | always | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 | SKIP: always()的效果只能通过步骤是否在失败时执行来观察,无法在run块内验证 | Tier-A | liyanghang |  |
| TC-190 | syntax-reference/expressions | 表达式示例 | 仅失败时通知 | 表达式示例 | - | 验证示例:仅失败时通知 | Send failure notification | if: ${{failed}} | any | failed | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 | SKIP: failure()条件只能通过步骤是否在前置失败时执行来观察,无法在run块内验证 | Tier-A | liyanghang |  |
| TC-191 | syntax-reference/expressions | 表达式示例 | 标签推送时构建 | 表达式示例 | - | 验证示例:标签推送时构建 | Build release | if: ${{startsWith(atomgit.ref,'refs/tags/')}} | any | startsWith | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: startsWith if条件只能通过步骤在tag推送时是否执行来观察,无法在run块内验证 | S5 | chaoran |  |
| TC-192 | syntax-reference/expressions | 表达式示例 | format拼接字符串 | 表达式示例 | - | 验证示例:format拼接字符串 | echo $IMAGE_TAG | IMAGE_TAG: ${{format('{0}:{1}','myimage',atomgit.sha)}} | any | format | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-193 | syntax-reference/variables | inputs type规格 | inputs.type=string | 类型约束 | ${{inputs.NAME}} | inputs仅支持string | 定义type:string正常 | inputs:<br>  x:<br>    type: string | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-194 | syntax-reference/variables | 变量优先级 | vars项目级>组织级 | 优先级 | ${{vars.VAR}} | 同名vars项目级覆盖组织级 | 取项目级值 | run: echo ${{vars.DUP}} | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(vars需在AtomGit平台界面同时配置项目级和组织级同名变量才可验证覆盖规则),仅验语法声明 | S13 | yulin |  |
| TC-195 | syntax-reference/variables | 变量优先级 | secrets项目级>组织级 | 优先级 | ${{secrets.NAME}} | 同名secrets项目级覆盖组织级 | 取项目级值 | run: echo ${{secrets.DUP}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |
| TC-196 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_TOKEN | 系统变量 | $ATOMGIT_TOKEN | 读取系统变量ATOMGIT_TOKEN | 返回工作流认证令牌(自动生成),示例ghs_xxx | - run: echo $ATOMGIT_TOKEN | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |
| TC-197 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_SHA | 系统变量 | $ATOMGIT_SHA | 读取系统变量ATOMGIT_SHA | 返回触发提交SHA,示例a1b2c3 | - run: echo $ATOMGIT_SHA | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-198 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REF | 系统变量 | $ATOMGIT_REF | 读取系统变量ATOMGIT_REF | 返回触发引用全名,示例refs/heads/main | - run: echo $ATOMGIT_REF | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-199 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REF_NAME | 系统变量 | $ATOMGIT_REF_NAME | 读取系统变量ATOMGIT_REF_NAME | 返回触发引用短名,示例main | - run: echo $ATOMGIT_REF_NAME | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-200 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REF_TYPE | 系统变量 | $ATOMGIT_REF_TYPE | 读取系统变量ATOMGIT_REF_TYPE | 返回引用类型,示例branch | - run: echo $ATOMGIT_REF_TYPE | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-201 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_EVENT_NAME | 系统变量 | $ATOMGIT_EVENT_NAME | 读取系统变量ATOMGIT_EVENT_NAME | 返回触发事件名称,示例push | - run: echo $ATOMGIT_EVENT_NAME | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-202 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_EVENT_PATH | 系统变量 | $ATOMGIT_EVENT_PATH | 读取系统变量ATOMGIT_EVENT_PATH | 返回事件payload JSON文件路径,示例/home/runner/_temp/event.json | - run: echo $ATOMGIT_EVENT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-203 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_WORKSPACE | 系统变量 | $ATOMGIT_WORKSPACE | 读取系统变量ATOMGIT_WORKSPACE | 返回Runner工作区路径,示例/home/runner/workspace | - run: echo $ATOMGIT_WORKSPACE | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-204 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTION | 系统变量 | $ATOMGIT_ACTION | 读取系统变量ATOMGIT_ACTION | 返回当前Action名称,示例my-action | - run: echo $ATOMGIT_ACTION | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(ATOMGIT_ACTION仅在Action内部有值,普通步骤中可能为空),仅验语法声明 | S17 | liyanghang |  |
| TC-205 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REPOSITORY | 系统变量 | $ATOMGIT_REPOSITORY | 读取系统变量ATOMGIT_REPOSITORY | 返回仓库全名,示例owner/repo | - run: echo $ATOMGIT_REPOSITORY | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-206 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REPOSITORY_OWNER | 系统变量 | $ATOMGIT_REPOSITORY_OWNER | 读取系统变量ATOMGIT_REPOSITORY_OWNER | 返回仓库所属组织,示例myorg | - run: echo $ATOMGIT_REPOSITORY_OWNER | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: ATOMGIT_REPOSITORY_OWNER 为空 | Tier-A | liyanghang |  |
| TC-207 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_RUN_ID | 系统变量 | $ATOMGIT_RUN_ID | 读取系统变量ATOMGIT_RUN_ID | 返回工作流运行ID,示例12345 | - run: echo $ATOMGIT_RUN_ID | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-208 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_RUN_NUMBER | 系统变量 | $ATOMGIT_RUN_NUMBER | 读取系统变量ATOMGIT_RUN_NUMBER | 返回工作流运行编号,示例42 | - run: echo $ATOMGIT_RUN_NUMBER | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-209 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_RUN_ATTEMPT | 系统变量 | $ATOMGIT_RUN_ATTEMPT | 读取系统变量ATOMGIT_RUN_ATTEMPT | 返回重试次数,示例1 | - run: echo $ATOMGIT_RUN_ATTEMPT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: ATOMGIT_RUN_ATTEMPT 为空 | Tier-A | liyanghang |  |
| TC-210 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_WORKFLOW | 系统变量 | $ATOMGIT_WORKFLOW | 读取系统变量ATOMGIT_WORKFLOW | 返回工作流名称,示例CI Pipeline | - run: echo $ATOMGIT_WORKFLOW | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-211 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_HEAD_REF | 系统变量 | $ATOMGIT_HEAD_REF | 读取系统变量ATOMGIT_HEAD_REF | 返回PR源分支(仅PR),示例feature/x | - run: echo $ATOMGIT_HEAD_REF | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(ATOMGIT_HEAD_REF仅在pull_request触发时有值,push触发时为空),仅验语法声明 | Tier-A | liyanghang |  |
| TC-212 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_BASE_REF | 系统变量 | $ATOMGIT_BASE_REF | 读取系统变量ATOMGIT_BASE_REF | 返回PR目标分支(仅PR),示例main | - run: echo $ATOMGIT_BASE_REF | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(ATOMGIT_BASE_REF仅在pull_request触发时有值,push触发时为空),仅验语法声明 | Tier-A | liyanghang |  |
| TC-213 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_SERVER_URL | 系统变量 | $ATOMGIT_SERVER_URL | 读取系统变量ATOMGIT_SERVER_URL | 返回平台根URL,示例https://atomgit.com | - run: echo $ATOMGIT_SERVER_URL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-214 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_API_URL | 系统变量 | $ATOMGIT_API_URL | 读取系统变量ATOMGIT_API_URL | 返回API基础URL,示例https://api.atomgit.com | - run: echo $ATOMGIT_API_URL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-215 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_GRAPHQL_URL | 系统变量 | $ATOMGIT_GRAPHQL_URL | 读取系统变量ATOMGIT_GRAPHQL_URL | 返回GraphQL API URL,示例https://api.atomgit.com/graphql | - run: echo $ATOMGIT_GRAPHQL_URL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: ATOMGIT_GRAPHQL_URL 为空 | Tier-A | liyanghang |  |
| TC-216 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_OUTPUT | 系统变量 | $ATOMGIT_OUTPUT | 读取系统变量ATOMGIT_OUTPUT | 返回步骤输出文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_OUTPUT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-217 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ENV | 系统变量 | $ATOMGIT_ENV | 读取系统变量ATOMGIT_ENV | 返回步骤环境变量文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_ENV | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-218 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_PATH | 系统变量 | $ATOMGIT_PATH | 读取系统变量ATOMGIT_PATH | 返回步骤系统PATH文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-219 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_STEP_SUMMARY | 系统变量 | $ATOMGIT_STEP_SUMMARY | 读取系统变量ATOMGIT_STEP_SUMMARY | 返回步骤摘要文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_STEP_SUMMARY | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-1 | S17 | liyanghang |  |
| TC-220 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 系统变量 | $ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 读取系统变量ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 返回是否允许不安全命令,示例false(默认) | - run: echo $ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(该变量未设置时为空或false,设置时才注入,无法从shell内部验证平台默认值行为),仅验语法声明 | S13 | yulin |  |
| TC-221 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTION_REPOSITORY | 系统变量 | $ATOMGIT_ACTION_REPOSITORY | 读取系统变量ATOMGIT_ACTION_REPOSITORY | 返回Action来源仓库,示例owner/action-repo | - run: echo $ATOMGIT_ACTION_REPOSITORY | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(ATOMGIT_ACTION_REPOSITORY仅在Action插件内部有值,普通步骤中为空),仅验语法声明 | S17 | liyanghang |  |
| TC-222 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTION_REF | 系统变量 | $ATOMGIT_ACTION_REF | 读取系统变量ATOMGIT_ACTION_REF | 返回Action来源引用,示例v1 | - run: echo $ATOMGIT_ACTION_REF | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(ATOMGIT_ACTION_REF仅在Action插件内部有值,普通步骤中为空),仅验语法声明 | S17 | liyanghang |  |
| TC-223 | core-concepts/trigger-events | 触发事件类型 | push | 触发事件 | on:push | 配置push触发 | 对应代码推送时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-224 | core-concepts/trigger-events | 触发事件类型 | pull_request | 触发事件 | on:pull_request | 配置pull_request触发 | 对应Pull Request时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: 未知事件=Push(不在触发器声明范围内) | S4 | chaoran |  |
| TC-225 | core-concepts/trigger-events | 触发事件类型 | schedule | 触发事件 | on:schedule | 配置schedule触发 | 对应定时触发时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-226 | core-concepts/trigger-events | 触发事件类型 | workflow_dispatch | 触发事件 | on:workflow_dispatch | 配置workflow_dispatch触发 | 对应手动触发时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-A | liyanghang |  |
| TC-227 | core-concepts/trigger-events | 触发事件类型 | workflow_call | 触发事件 | on:workflow_call | 配置workflow_call触发 | 对应工作流调用时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-A | liyanghang |  |
| TC-228 | core-concepts/trigger-events | 触发事件类型 | issue_comment | 触发事件 | on:issue_comment | 配置issue_comment触发 | 对应Issue评论时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-229 | core-concepts/trigger-events | 触发配置 | push.branches | 触发配置 | branches:[main] | 配置push.branches | 仅指定分支push触发 | on:<br>  branches:[main] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-230 | core-concepts/trigger-events | 触发配置 | push.tags | 触发配置 | tags:['v*'] | 配置push.tags | 仅指定tag push触发 | on:<br>  tags:['v*'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-231 | core-concepts/trigger-events | 触发配置 | push.paths | 触发配置 | paths:['src/**'] | 配置push.paths | 仅指定路径变更触发 | on:<br>  paths:['src/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-232 | core-concepts/trigger-events | 触发配置 | push.paths-ignore | 触发配置 | paths-ignore:['**/*.md'] | 配置push.paths-ignore | 忽略路径不触发 | on:<br>  paths-ignore:['**/*.md'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-233 | core-concepts/trigger-events | 触发配置 | push.branches-ignore | 触发配置 | branches-ignore:['release/**'] | 配置push.branches-ignore | 忽略分支push不触发 | on:<br>  branches-ignore:['release/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-234 | core-concepts/trigger-events | 触发配置 | pull_request.types | 触发配置 | types:[open,reopen,update] | 配置pull_request.types | 仅指定类型PR触发 | on:<br>  types:[open,reopen,update] | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |
| TC-235 | core-concepts/trigger-events | 触发配置 | pull_request.branches | 触发配置 | branches:[main] | 配置pull_request.branches | 仅目标分支匹配触发 | on:<br>  branches:[main] | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |
| TC-236 | core-concepts/trigger-events | 触发配置 | pull_request.paths | 触发配置 | paths:['api/**'] | 配置pull_request.paths | 仅指定路径变更触发 | on:<br>  paths:['api/**'] | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |
| TC-237 | core-concepts/trigger-events | 触发配置 | schedule.cron | 触发配置 | cron:'0 2 * * *' | 配置schedule.cron | 按cron时间触发 | on:<br>  cron:'0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron触发时刻由平台调度器决定),仅验文档约束 | S3 | yulin |  |
| TC-238 | core-concepts/trigger-events | 触发配置 | workflow_dispatch.inputs | 触发配置 | inputs:build_id:type:string | 配置workflow_dispatch.inputs | 手动触发时可传参 | on:<br>  inputs:build_id:type:string | workflow_dispatch |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-239 | syntax-reference/workflow-commands | 工作流命令 | set-output | 工作流命令 | - | 使用命令set-output | 应:设置步骤输出 | - run: \|<br>    echo '::set-output name=K::V' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-240 | syntax-reference/workflow-commands | 工作流命令 | set-env | 工作流命令 | - | 使用命令set-env | 应:设置环境变量 | - run: \|<br>    echo '::set-env name=K::V' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-241 | syntax-reference/workflow-commands | 工作流命令 | add-path | 工作流命令 | - | 使用命令add-path | 应:添加系统PATH | - run: \|<br>    echo '::add-path::/custom/path' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-242 | syntax-reference/workflow-commands | 工作流命令 | set-step-summary | 工作流命令 | - | 使用命令set-step-summary | 应:设置步骤摘要 | - run: \|<br>    echo '::set-step-summary::content' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(步骤摘要显示在平台UI中,无法从shell内部验证是否渲染),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-243 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_OUTPUT写入 | 工作流命令 | - | 使用命令ATOMGIT_OUTPUT写入 | 应:通过文件设置输出 | - run: \|<br>    echo 'K=V' >> $ATOMGIT_OUTPUT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-244 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_ENV写入 | 工作流命令 | - | 使用命令ATOMGIT_ENV写入 | 应:通过文件设置环境变量 | - run: \|<br>    echo 'K=V' >> $ATOMGIT_ENV | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-245 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_PATH写入 | 工作流命令 | - | 使用命令ATOMGIT_PATH写入 | 应:通过文件添加PATH | - run: \|<br>    echo '/path' >> $ATOMGIT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-246 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_STEP_SUMMARY写入 | 工作流命令 | - | 使用命令ATOMGIT_STEP_SUMMARY写入 | 应:通过文件设置摘要 | - run: \|<br>    echo 'content' >> $ATOMGIT_STEP_SUMMARY | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-2 | S7 | chenqi |  |
| TC-247 | syntax-reference/workflow-commands | 工作流命令 | debug日志 | 工作流命令 | - | 使用命令debug日志 | 应:输出debug日志 | - run: \|<br>    echo '::debug::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::debug::命令由Runner平台解析渲染为调试日志,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-248 | syntax-reference/workflow-commands | 工作流命令 | error日志 | 工作流命令 | - | 使用命令error日志 | 应:输出error日志 | - run: \|<br>    echo '::error file=x,line=10::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::error::命令由Runner平台解析标注行错误,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-249 | syntax-reference/workflow-commands | 工作流命令 | warning日志 | 工作流命令 | - | 使用命令warning日志 | 应:输出warning日志 | - run: \|<br>    echo '::warning file=x,line=10::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::warning::命令由Runner平台解析渲染为警告标注,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-250 | syntax-reference/workflow-commands | 工作流命令 | notice日志 | 工作流命令 | - | 使用命令notice日志 | 应:输出notice日志 | - run: \|<br>    echo '::notice file=x,line=10::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::notice::命令由Runner平台解析渲染为通知标注,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-251 | syntax-reference/workflow-commands | 工作流命令 | group日志分组 | 工作流命令 | - | 使用命令group日志分组 | 应:日志分组显示 | - run: \|<br>    echo '::group::Title'...echo '::endgroup::' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::group::命令由Runner平台渲染为折叠分组UI,shell内部无法验证分组效果),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-252 | syntax-reference/workflow-commands | 工作流命令 | mask-value掩码 | 工作流命令 | - | 使用命令mask-value掩码 | 应:日志中掩码指定值 | - run: \|<br>    echo '::add-mask::secret' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::add-mask::*** | S7 | chenqi | 不存在用例 |
| TC-253 | syntax-reference/workflow-commands | 工作流命令 | stop-commands | 工作流命令 | - | 使用命令stop-commands | 应:暂停命令处理 | - run: \|<br>    echo '::stop-commands::token'...echo '::token::' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::stop-commands::效果由Runner平台处理,shell内部无法验证命令处理是否暂停),仅验语法声明 | S7 | chenqi | 不存在用例 |
| TC-254 | syntax-reference/runner-images-tools | Runner标签 | codearts-hosted | Runner标签 | runs-on:['codearts-hosted'] | 使用标签codearts-hosted | 调度到官方资源池Runner | runs-on: ['codearts-hosted'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-255 | syntax-reference/runner-images-tools | Runner标签 | self-hosted | Runner标签 | runs-on:['self-hosted'] | 使用标签self-hosted | 调度到自托管RunnerRunner | runs-on: ['self-hosted'] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-256 | syntax-reference/runner-images-tools | Runner标签 | ubuntu-latest | Runner标签 | runs-on:['ubuntu-latest'] | 使用标签ubuntu-latest | 调度到Ubuntu最新版Runner | runs-on: ['ubuntu-latest'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-257 | syntax-reference/runner-images-tools | Runner标签 | windows-latest | Runner标签 | runs-on:['windows-latest'] | 使用标签windows-latest | 调度到Windows最新版Runner | runs-on: ['windows-latest'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  |  | liyanghang |  |
| TC-258 | syntax-reference/runner-images-tools | Runner标签 | macos-latest | Runner标签 | runs-on:['macos-latest'] | 使用标签macos-latest | 调度到macOS最新版Runner | runs-on: ['macos-latest'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-259 | syntax-reference/runner-images-tools | Runner标签 | x64 | Runner标签 | runs-on:['x64'] | 使用标签x64 | 调度到x64架构Runner | runs-on: ['x64'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-260 | syntax-reference/runner-images-tools | Runner标签 | arm64 | Runner标签 | runs-on:['arm64'] | 使用标签arm64 | 调度到ARM64架构Runner | runs-on: ['arm64'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-261 | syntax-reference/runner-images-tools | Runner标签 | large | Runner标签 | runs-on:['large'] | 使用标签large | 调度到大型资源规格Runner | runs-on: ['large'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-262 | syntax-reference/runner-images-tools | Runner镜像 | container.image | 运行环境 | container:<br>  image: ubuntu:20.04 | 使用自定义容器镜像 | Job在容器内执行 | container:<br>  image: ubuntu:20.04 | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-263 | syntax-reference/runner-images-tools | Runner镜像 | container.options | 运行环境 | container:<br>  options: --cpus 1 | 使用容器选项 | 容器按选项启动 | container:<br>  options: --cpus 1 --user root | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-264 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.name | Job字段 | jobs.<id>.name:value | 配置jobs.<id>.name | 应:Job显示名称 | jobs:<br>  build:<br>    name: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-265 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.runs-on | Job字段 | jobs.<id>.runs-on:value | 配置jobs.<id>.runs-on | 应:Job运行环境标签 | jobs:<br>  build:<br>    runs-on: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-266 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.needs | Job字段 | jobs.<id>.needs:value | 配置jobs.<id>.needs | 应:Job依赖列表 | jobs:<br>  build:<br>    needs: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: run_id 为空 | Tier-A | liyanghang |  |
| TC-267 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.if | Job字段 | jobs.<id>.if:value | 配置jobs.<id>.if | 应:Job条件执行 | jobs:<br>  build:<br>    if: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-268 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.env | Job字段 | jobs.<id>.env:value | 配置jobs.<id>.env | 应:Job级环境变量 | jobs:<br>  build:<br>    env: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-269 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.steps | Job字段 | jobs.<id>.steps:value | 配置jobs.<id>.steps | 应:Job步骤列表 | jobs:<br>  build:<br>    steps: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-270 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.timeout-minutes | Job字段 | jobs.<id>.timeout-minutes:value | 配置jobs.<id>.timeout-minutes | 应:Job超时时间 | jobs:<br>  build:<br>    timeout-minutes: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-271 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.strategy | Job字段 | jobs.<id>.strategy:value | 配置jobs.<id>.strategy | 应:Job矩阵策略 | jobs:<br>  build:<br>    strategy: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-272 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.continue-on-error | Job字段 | jobs.<id>.continue-on-error:value | 配置jobs.<id>.continue-on-error | 应:Job失败是否继续 | jobs:<br>  build:<br>    continue-on-error: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-273 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.container | Job字段 | jobs.<id>.container:value | 配置jobs.<id>.container | 应:Job自定义容器 | jobs:<br>  build:<br>    container: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | FAIL | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |
| TC-274 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.environment | Job字段 | jobs.<id>.environment:value | 配置jobs.<id>.environment | 应:Job部署环境 | jobs:<br>  build:<br>    environment: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-275 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.permissions | Job字段 | jobs.<id>.permissions:value | 配置jobs.<id>.permissions | 应:Job权限配置 | jobs:<br>  build:<br>    permissions: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-276 | writing-pipelines/configure-jobs | 矩阵策略 | strategy.matrix | 矩阵字段 | strategy.matrix:value | 配置strategy.matrix | 应:矩阵变量定义 | strategy:<br>  matrix:<br>    os: [ubuntu, windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-277 | writing-pipelines/configure-jobs | 矩阵策略 | strategy.fail-fast | 矩阵字段 | strategy.fail-fast:value | 配置strategy.fail-fast | 应:矩阵失败是否取消全部 | strategy:<br>  matrix:<br>    os: [ubuntu, windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-278 | writing-pipelines/configure-jobs | 矩阵策略 | strategy.max-parallel | 矩阵字段 | strategy.max-parallel:value | 配置strategy.max-parallel | 应:矩阵最大并行数 | strategy:<br>  matrix:<br>    os: [ubuntu, windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-279 | writing-pipelines/configure-steps | Steps配置 | steps.name | Step字段 | steps.name:value | 配置steps.name | 应:步骤名称 | steps:<br>  - name: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-280 | writing-pipelines/configure-steps | Steps配置 | steps.run | Step字段 | steps.run:value | 配置steps.run | 应:执行shell命令 | steps:<br>  - run: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-281 | writing-pipelines/configure-steps | Steps配置 | steps.uses | Step字段 | steps.uses:value | 配置steps.uses | 应:调用Action插件 | steps:<br>  - uses: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-282 | writing-pipelines/configure-steps | Steps配置 | steps.with | Step字段 | steps.with:value | 配置steps.with | 应:传参给Action | steps:<br>  - with: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-283 | writing-pipelines/configure-steps | Steps配置 | steps.env | Step字段 | steps.env:value | 配置steps.env | 应:步骤级环境变量 | steps:<br>  - env: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-284 | writing-pipelines/configure-steps | Steps配置 | steps.if | Step字段 | steps.if:value | 配置steps.if | 应:步骤条件执行 | steps:<br>  - if: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-285 | writing-pipelines/configure-steps | Steps配置 | steps.id | Step字段 | steps.id:value | 配置steps.id | 应:步骤唯一标识 | steps:<br>  - id: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-286 | writing-pipelines/configure-steps | Steps配置 | steps.continue-on-error | Step字段 | steps.continue-on-error:value | 配置steps.continue-on-error | 应:步骤失败是否继续 | steps:<br>  - continue-on-error: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-287 | writing-pipelines/configure-steps | Steps配置 | steps.working-directory | Step字段 | steps.working-directory:value | 配置steps.working-directory | 应:步骤工作目录 | steps:<br>  - working-directory: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-288 | writing-pipelines/configure-steps | Steps配置 | steps.shell | Step字段 | steps.shell:value | 配置steps.shell | 应:步骤使用的shell | steps:<br>  - shell: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-289 | concurrency | 并发控制 | concurrency.max | 并发字段 | concurrency.max:value | 配置concurrency.max | 应:最大并发数 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-290 | concurrency | 并发控制 | concurrency.enable | 并发字段 | concurrency.enable:value | 配置concurrency.enable | 应:是否启用并发控制 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-291 | concurrency | 并发控制 | concurrency.preemption.enable | 并发字段 | concurrency.preemption.enable:value | 配置concurrency.preemption.enable | 应:是否启用抢占 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |
| TC-292 | concurrency | 并发控制 | concurrency.preemption.events | 并发字段 | concurrency.preemption.events:value | 配置concurrency.preemption.events | 应:可抢占事件列表 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |
| TC-293 | concurrency | 并发控制 | concurrency.exceed-action | 并发字段 | concurrency.exceed-action:value | 配置concurrency.exceed-action | 应:超限动作QUEUE/IGNORE/CANCEL | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |
| TC-294 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.name | 制品字段 | upload-artifact.name:value | 配置upload-artifact.name | 应:上传制品名称 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-295 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.path | 制品字段 | upload-artifact.path:value | 配置upload-artifact.path | 应:上传制品路径 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-296 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.retention-days | 制品字段 | upload-artifact.retention-days:value | 配置upload-artifact.retention-days | 应:制品保留天数 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-297 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.if-no-files-found | 制品字段 | upload-artifact.if-no-files-found:value | 配置upload-artifact.if-no-files-found | 应:无文件时行为 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-298 | writing-pipelines/upload-download-artifacts | 制品管理 | download-artifact.name | 制品字段 | download-artifact.name:value | 配置download-artifact.name | 应:下载制品名称 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-299 | writing-pipelines/upload-download-artifacts | 制品管理 | download-artifact.path | 制品字段 | download-artifact.path:value | 配置download-artifact.path | 应:下载制品目标路径 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-300 | writing-pipelines/upload-download-artifacts | 制品管理 | download-artifact.pattern | 制品字段 | download-artifact.pattern:value | 配置download-artifact.pattern | 应:下载制品匹配模式 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-301 | writing-pipelines/using-dependency-cache | 依赖缓存 | cache.path | 缓存字段 | cache.path:value | 配置cache.path | 应:缓存路径 | uses: cache<br>  with:<br>    path: ~/.cache/pip<br>    key: pip | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-302 | writing-pipelines/using-dependency-cache | 依赖缓存 | cache.key | 缓存字段 | cache.key:value | 配置cache.key | 应:缓存键(支持hashFiles) | uses: cache<br>  with:<br>    path: ~/.cache/pip<br>    key: pip | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-303 | writing-pipelines/using-dependency-cache | 依赖缓存 | cache.restore-keys | 缓存字段 | cache.restore-keys:value | 配置cache.restore-keys | 应:缓存恢复键列表 | uses: cache<br>  with:<br>    path: ~/.cache/pip<br>    key: pip | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-304 | writing-pipelines/using-actions | Action插件 | checkout | Action插件 | uses:checkout | 调用checkout | 应:拉取仓库代码 | - uses: checkout<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |
| TC-305 | writing-pipelines/using-actions | Action插件 | cache | Action插件 | uses:cache | 调用cache | 应:依赖缓存 | - uses: cache<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-306 | writing-pipelines/using-actions | Action插件 | upload-artifact | Action插件 | uses:upload-artifact | 调用upload-artifact | 应:上传制品 | - uses: upload-artifact<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-307 | writing-pipelines/using-actions | Action插件 | download-artifact | Action插件 | uses:download-artifact | 调用download-artifact | 应:下载制品 | - uses: download-artifact<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |
| TC-308 | writing-pipelines/using-actions | Action插件 | setup-python | Action插件 | uses:setup-python | 调用setup-python | 应:设置Python版本 | - uses: setup-python<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |
| TC-309 | writing-pipelines/using-actions | Action插件 | setup-node | Action插件 | uses:setup-node | 调用setup-node | 应:设置Node.js版本 | - uses: setup-node<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |
| TC-310 | writing-pipelines/using-actions | Action插件 | setup-java | Action插件 | uses:setup-java | 调用setup-java | 应:设置Java版本 | - uses: setup-java<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | FAIL | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |
| TC-311 | writing-pipelines/using-actions | Action插件 | manifest-management-plugin | Action插件 | uses:manifest-management-plugin | 调用manifest-management-plugin | 应:清单管理插件 | - uses: manifest-management-plugin<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |
| TC-312 | writing-pipelines/using-actions | Action插件 | official_shell_plugin | Action插件 | uses:official_shell_plugin | 调用official_shell_plugin | 应:官方Shell插件 | - uses: official_shell_plugin<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |
| TC-313 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs(单依赖) | 依赖配置 | jobs.b.needs:[a] | 配置needs(单依赖) | Job b依赖Job a串行 | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: run_id 为空 | Tier-A | liyanghang |  |
| TC-314 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs(多依赖) | 依赖配置 | jobs.c.needs:[a,b] | 配置needs(多依赖) | Job c依赖a和b | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-315 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs(空依赖) | 依赖配置 | needs:[] | 配置needs(空依赖) | Job无依赖可并行 | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-316 | writing-pipelines/configure-dependencies-order | 任务依赖 | DAG拓扑 | 依赖配置 | build->test->deploy | 配置DAG拓扑 | 复杂依赖形成DAG | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: run_id 为空 | Tier-A | liyanghang |  |
| TC-317 | writing-pipelines/configure-conditional-execution | 条件执行 | if:default() | 条件配置 | if: ${{default()}} | 配置if:default() | 默认条件前置成功时执行 | - if: ${{default()}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | suite-4 | Tier-A | liyanghang |  |
| TC-318 | writing-pipelines/configure-conditional-execution | 条件执行 | if:always() | 条件配置 | if: ${{always}} | 配置if:always() | 无论前置都执行 | - if: ${{always}} | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | FAIL | suite-4 | Tier-B | liyanghang |  |
| TC-319 | writing-pipelines/configure-conditional-execution | 条件执行 | if:success | 条件配置 | if: ${{success}} | 配置if:success | 前置成功时执行 | - if: ${{success}} | any |  | status | run.status | SUCCESS,成功 | B API字段 | FAIL |  | Tier-B | liyanghang |  |
| TC-320 | writing-pipelines/configure-conditional-execution | 条件执行 | if:failed | 条件配置 | if: ${{failed}} | 配置if:failed | 前置失败时执行 | - if: ${{failed}} | any |  | status | run.status | FAILED,触发失败传播 | B API字段 | FAIL |  | Tier-B | liyanghang |  |
| TC-321 | writing-pipelines/configure-conditional-execution | 条件执行 | if:cancelled | 条件配置 | if: ${{cancelled}} | 配置if:cancelled | 工作流取消时执行 | - if: ${{cancelled}} | any |  | status | run.status | CANCELLED,被取消 | B API字段 | FAIL |  | Tier-B | liyanghang |  |
| TC-322 | writing-pipelines/configure-conditional-execution | 条件执行 | if:分支匹配 | 条件配置 | if: ${{atomgit.ref=='refs/heads/main'}} | 配置if:分支匹配 | 仅main分支时执行 | - if: ${{atomgit.ref=='refs/heads/main'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-323 | writing-pipelines/configure-conditional-execution | 条件执行 | if:事件匹配 | 条件配置 | if: ${{atomgit.event_name=='push'}} | 配置if:事件匹配 | 仅push事件时执行 | - if: ${{atomgit.event_name=='push'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-324 | writing-pipelines/configure-conditional-execution | 条件执行 | if:前置步骤结果 | 条件配置 | if: ${{steps.build.outputs.result=='success'}} | 配置if:前置步骤结果 | 依据前置步骤输出 | - if: ${{steps.build.outputs.result=='success'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-325 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix单变量 | 矩阵配置 | matrix:<br>  os:[ubuntu,windows] | 配置matrix单变量 | 单变量矩阵展开2实例 | strategy:<br>  matrix:<br>  os:[ubuntu,windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-326 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix多变量 | 矩阵配置 | matrix:<br>  os:[ubuntu,windows]<br>  py:[3.9,3.10] | 配置matrix多变量 | 多变量矩阵展开4实例 | strategy:<br>  matrix:<br>  os:[ubuntu,windows]<br>  py:[3.9,3.10] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-327 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix include | 矩阵配置 | matrix:<br>  include:<br>    - os: macos | 配置matrix include | include追加特殊组合 | strategy:<br>  matrix:<br>  include:<br>    - os: macos | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-328 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix exclude | 矩阵配置 | matrix:<br>  exclude:<br>    - os: windows | 配置matrix exclude | exclude排除特定组合 | strategy:<br>  matrix:<br>  exclude:<br>    - os: windows | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-329 | writing-pipelines/configure-matrix-builds | 矩阵构建 | fail-fast:false | 矩阵配置 | strategy:<br>  fail-fast:false | 配置fail-fast:false | 矩阵失败不取消其它 | strategy:<br>  strategy:<br>  fail-fast:false | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: fail-fast=false 效果需让矩阵中某实例失败后观察其他实例是否继续,无法在正常运行中验证 | Tier-A | liyanghang |  |
| TC-330 | writing-pipelines/configure-matrix-builds | 矩阵构建 | max-parallel:3 | 矩阵配置 | strategy:<br>  max-parallel:3 | 配置max-parallel:3 | 矩阵最大并行数3 | strategy:<br>  strategy:<br>  max-parallel:3 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: max-parallel=3 效果需观察并发执行的矩阵实例数量,无法在单 step 内验证 | Tier-A | liyanghang |  |
| TC-331 | writing-pipelines/pass-output-between-jobs | 输出传递 | steps.<id>.outputs | 输出配置 | echo '::set-output name=k::v' | 配置steps.<id>.outputs | 步骤内设置输出 | echo '::set-output name=k::v' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-332 | writing-pipelines/pass-output-between-jobs | 输出传递 | job outputs映射 | 输出配置 | jobs:<br>  build:<br>    outputs:<br>      ver: ${{steps.x.outputs.ver}} | 配置job outputs映射 | Job级声明outputs | jobs:<br>  build:<br>    outputs:<br>      ver: ${{steps.x.outputs.ver}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP |  | Tier-A | liyanghang |  |
| TC-333 | writing-pipelines/pass-output-between-jobs | 输出传递 | 跨Job引用 | 输出配置 | jobs:<br>  deploy:<br>    needs: build<br>    env:<br>      V: ${{needs.build.outputs.ver}} | 配置跨Job引用 | 通过needs.<job>.outputs引用 | jobs:<br>  deploy:<br>    needs: build<br>    env:<br>      V: ${{needs.build.outputs.ver}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP |  | Tier-A | liyanghang |  |
| TC-334 | core-concepts/trigger-events | 触发事件完整列表 | push | 触发事件 | on:push | 配置push触发 | 应:代码推送事件触发workflow | on:<br>  push: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-335 | core-concepts/trigger-events | 触发事件完整列表 | pull_request | 触发事件 | on:pull_request | 配置pull_request触发 | 应:Pull Request事件触发workflow | on:<br>  pull_request: | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: 未知事件=Push(不在触发器声明范围内) | S4 | chaoran |  |
| TC-336 | core-concepts/trigger-events | 触发事件完整列表 | pull_request_target | 触发事件 | on:pull_request_target | 配置pull_request_target触发 | 应:PR目标分支上下文事件触发workflow | on:<br>  pull_request_target: | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: 未知事件=Push(不在触发器声明范围内) | S4 | chaoran |  |
| TC-337 | core-concepts/trigger-events | 触发事件完整列表 | schedule | 触发事件 | on:schedule | 配置schedule触发 | 应:定时触发事件触发workflow | on:<br>  schedule: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-338 | core-concepts/trigger-events | 触发事件完整列表 | workflow_dispatch | 触发事件 | on:workflow_dispatch | 配置workflow_dispatch触发 | 应:手动触发事件触发workflow | on:<br>  workflow_dispatch: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-339 | core-concepts/trigger-events | 触发事件完整列表 | workflow_call | 触发事件 | on:workflow_call | 配置workflow_call触发 | 应:工作流调用事件触发workflow | on:<br>  workflow_call: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-340 | core-concepts/trigger-events | 触发事件完整列表 | issue_comment | 触发事件 | on:issue_comment | 配置issue_comment触发 | 应:Issue评论事件触发workflow | on:<br>  issue_comment: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-341 | core-concepts/trigger-events | 触发事件完整列表 | issues | 触发事件 | on:issues | 配置issues触发 | 应:Issue事件事件触发workflow | on:<br>  issues: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-342 | core-concepts/trigger-events | 触发事件完整列表 | release | 触发事件 | on:release | 配置release触发 | 应:Release事件事件触发workflow | on:<br>  release: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-343 | core-concepts/trigger-events | 触发事件完整列表 | create | 触发事件 | on:create | 配置create触发 | 应:分支/标签创建事件触发workflow | on:<br>  create: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-344 | core-concepts/trigger-events | 触发事件完整列表 | delete | 触发事件 | on:delete | 配置delete触发 | 应:分支/标签删除事件触发workflow | on:<br>  delete: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-345 | core-concepts/trigger-events | 触发事件完整列表 | fork | 触发事件 | on:fork | 配置fork触发 | 应:Fork事件事件触发workflow | on:<br>  fork: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-346 | core-concepts/trigger-events | 触发事件完整列表 | watch | 触发事件 | on:watch | 配置watch触发 | 应:Star/Watch事件事件触发workflow | on:<br>  watch: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |
| TC-347 | running-pipelines | 运行流水线 | view-run-results | 运行操作 | - | 操作:查看运行结果 | 展示各阶段状态/耗时/结论 | # UI操作:view-run-results | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-348 | running-pipelines | 运行流水线 | view-job-logs | 运行操作 | - | 操作:查看任务日志 | 逐step查看完整日志 | # UI操作:view-job-logs | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-349 | running-pipelines | 运行流水线 | manually-trigger-pipeline | 运行操作 | - | 操作:手动触发 | UI手动触发并传参 | # UI操作:manually-trigger-pipeline | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-350 | running-pipelines | 运行流水线 | rerun-failed-jobs | 运行操作 | - | 操作:重新运行失败任务 | 仅重跑失败Job | # UI操作:rerun-failed-jobs | any |  | status | run.status | FAILED,触发失败传播 | B API字段 | PASS | suite-3 | Tier-B | liyanghang |  |
| TC-351 | security-permissions | 安全与权限 | permissions.repository | 安全配置 | read/write/admin | 配置permissions.repository | 授予仓库权限 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-352 | security-permissions | 安全与权限 | permissions.issue | 安全配置 | read/write/admin | 配置permissions.issue | 授予Issue权限 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-353 | security-permissions | 安全与权限 | permissions.pull_request | 安全配置 | read/write/admin | 配置permissions.pull_request | 授予PR权限 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-354 | security-permissions | 安全与权限 | secrets日志脱敏 | 安全配置 | echo ${{secrets.X}} | 配置secrets日志脱敏 | 日志替换为*** | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |
| TC-355 | security-permissions | 安全与权限 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 安全配置 | 是否允许不安全命令 | 配置ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 默认false禁止set-env | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-2 | S13 | yulin |  |
| TC-356 | security-permissions | 安全与权限 | ATOMGIT_TOKEN生命周期 | 安全配置 | 仅运行期间有效 | 配置ATOMGIT_TOKEN生命周期 | 运行后失效不可持久化 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-357 | action-development | Action插件开发 | action.yml元数据 | Action开发 | name/description/inputs/outputs | 配置action.yml元数据 | 声明Action元数据 | action.yml:<br>name/description/inputs/outputs | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-358 | action-development | Action插件开发 | inputs定义 | Action开发 | inputs:<br>  x:<br>    required: true | 配置inputs定义 | 声明输入参数 | action.yml:<br>inputs:<br>  x:<br>    required: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-359 | action-development | Action插件开发 | outputs定义 | Action开发 | outputs:<br>  result:<br>    description: '...' | 配置outputs定义 | 声明输出参数 | action.yml:<br>outputs:<br>  result:<br>    description: '...' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-360 | action-development | Action插件开发 | runs.using | Action开发 | using:'shell'/'composite'/'node' | 配置runs.using | 指定Action运行方式 | action.yml:<br>using:'shell'/'composite'/'node' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-361 | action-development | Action插件开发 | runs.steps | Action开发 | runs:<br>  steps:<br>    - run: ... | 配置runs.steps | composite步骤列表 | action.yml:<br>runs:<br>  steps:<br>    - run: ... | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S17 | liyanghang |  |
| TC-362 | action-development | Action插件开发 | runs.main | Action开发 | runs:<br>  main: 'index.js' | 配置runs.main | node入口文件 | action.yml:<br>runs:<br>  main: 'index.js' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S17 | liyanghang |  |
| TC-363 | core-concepts/runner-and-environment | Runner运行环境 | 官方资源池 | Runner环境 | runs-on:[codearts-hosted,ubuntu-latest,x64,large] | 配置官方资源池 | 调度到官方托管Runner | runs-on: [codearts-hosted, ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-364 | core-concepts/runner-and-environment | Runner运行环境 | 自托管资源池 | Runner环境 | runs-on:[self-hosted,arch=arm] | 配置自托管资源池 | 调度到自托管Runner | runs-on: [codearts-hosted, ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-365 | core-concepts/runner-and-environment | Runner运行环境 | 三段式标签 | Runner环境 | <pool>,<arch>,<flavor> | 配置三段式标签 | 按三段式标签格式调度 | runs-on: [codearts-hosted, ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-366 | core-concepts/workflow-job-step-action | 工作流结构 | workflow文件位置 | 工作流结构 | .gitcode/workflows/*.yml | 配置workflow文件位置 | 识别.workflows目录下YAML | .gitcode/workflows/*.yml | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-367 | core-concepts/workflow-job-step-action | 工作流结构 | workflow name | 工作流结构 | name: CI Pipeline | 配置workflow name | 显示在流水线列表 | name: CI Pipeline | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-368 | core-concepts/workflow-job-step-action | 工作流结构 | workflow on | 工作流结构 | on: push | 配置workflow on | 按声明事件触发 | on: push | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-369 | core-concepts/workflow-job-step-action | 工作流结构 | workflow env | 工作流结构 | env:<br>  GLOBAL: value | 配置workflow env | workflow级环境变量 | env:<br>  GLOBAL: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-370 | core-concepts/workflow-job-step-action | 工作流结构 | workflow concurrency | 工作流结构 | concurrency:<br>  max: 6 | 配置workflow concurrency | 控制并发 | concurrency:<br>  max: 6 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-371 | core-concepts/workflow-job-step-action | 工作流结构 | workflow stages | 工作流结构 | stages:<br>  s1:<br>    jobs: ... | 配置workflow stages | 按stages组织Job | stages:<br>  s1:<br>    jobs: ... | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-372 | core-concepts/workflow-job-step-action | 工作流结构 | job runs-on | 工作流结构 | runs-on: ubuntu-latest | 配置job runs-on | 按标签调度Runner | runs-on: ubuntu-latest | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-373 | core-concepts/workflow-job-step-action | 工作流结构 | job needs | 工作流结构 | needs: [build] | 配置job needs | 按依赖串行/并行 | needs: [build] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-374 | core-concepts/workflow-job-step-action | 工作流结构 | job strategy | 工作流结构 | strategy:<br>  matrix: ... | 配置job strategy | 按矩阵展开实例 | strategy:<br>  matrix: ... | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-375 | core-concepts/workflow-job-step-action | 工作流结构 | step run | 工作流结构 | run: echo hello | 配置step run | 执行shell命令 | run: echo hello | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-376 | core-concepts/workflow-job-step-action | 工作流结构 | step uses | 工作流结构 | uses: checkout | 配置step uses | 调用Action插件 | uses: checkout | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-377 | core-concepts/workflow-job-step-action | 工作流结构 | step with | 工作流结构 | with:<br>  param: value | 配置step with | 传参给Action | with:<br>  param: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-378 | core-concepts/artifacts-and-cache | 制品与缓存 | artifacts上传 | 制品/缓存 | uses: upload-artifact | 配置artifacts上传 | 上传构建产物 | - uses: artifacts上传 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-379 | core-concepts/artifacts-and-cache | 制品与缓存 | artifacts下载 | 制品/缓存 | uses: download-artifact | 配置artifacts下载 | 下载指定制品 | - uses: artifacts下载 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-380 | core-concepts/artifacts-and-cache | 制品与缓存 | artifacts retention | 制品/缓存 | retention-days: 14 | 配置artifacts retention | 按声明保留天数 | - uses: artifacts retention | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |
| TC-381 | core-concepts/artifacts-and-cache | 制品与缓存 | cache依赖缓存 | 制品/缓存 | uses: cache | 配置cache依赖缓存 | 缓存依赖加速构建 | - uses: cache依赖缓存 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-382 | core-concepts/artifacts-and-cache | 制品与缓存 | cache key hashFiles | 制品/缓存 | key: ${{hashFiles('**/lock')}} | 配置cache key hashFiles | 按文件哈希生成缓存键 | - uses: cache key hashFiles | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-383 | writing-pipelines/workflow-file-location-structure | 文件位置 | .gitcode/workflows/目录 | 路径规则 | - | workflow文件存放目录 | 仅识别该目录下.yml/.yaml | 目录: .gitcode/workflows/ | any | 其他后缀被忽略 | file_path | run.file_path | 以 .gitcode/workflows/ 开头 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-384 | writing-pipelines/workflow-file-location-structure | 文件位置 | .yml后缀识别 | 后缀规则 | - | 文件以.yml结尾 | 被识别为workflow | 文件: ci.yml | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-385 | writing-pipelines/workflow-file-location-structure | 文件位置 | .yaml后缀识别 | 后缀规则 | - | 文件以.yaml结尾 | 被识别为workflow | 文件: ci.yaml | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-386 | writing-pipelines/workflow-file-location-structure | 文件位置 | 其他后缀忽略 | 后缀规则 | - | 文件以.txt结尾 | 被忽略不识别 | 文件: ci.txt | any |  | — | — | —(仅可经Job日志断言) | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-387 | writing-pipelines/workflow-file-location-structure | 命名建议 | ci.yml | 命名 | - | 持续集成场景 | push/PR时构建测试 | 文件名: ci.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S13 | yulin |  |
| TC-388 | writing-pipelines/workflow-file-location-structure | 命名建议 | pr-check.yml | 命名 | - | 合并请求检查 | PR提交时自动检查 | 文件名: pr-check.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S13 | yulin |  |
| TC-389 | writing-pipelines/workflow-file-location-structure | 命名建议 | release.yml | 命名 | - | 发布流程 | Tag触发发布 | 文件名: release.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S13 | yulin |  |
| TC-390 | writing-pipelines/workflow-file-location-structure | 命名建议 | docker-build.yml | 命名 | - | Docker镜像构建 | 构建并推送镜像 | 文件名: docker-build.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL |  | S13 | yulin |  |
| TC-391 | writing-pipelines/workflow-file-location-structure | 命名建议 | nightly.yml | 命名 | - | 定时任务 | 每日定时构建 | 文件名: nightly.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL |  | S13 | yulin |  |
| TC-392 | writing-pipelines/workflow-file-location-structure | 命名建议 | deploy.yml | 命名 | - | 手动部署 | 手动触发部署 | 文件名: deploy.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 |  |  | S4 | chaoran |  |
| TC-393 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | name | 字段 | - | workflow展示名称 | 缺省时使用文件名 | name: ci | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-394 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | on | 字段 | - | 触发条件 | 定义触发事件 | on: push | any | 必填 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-395 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | env | 字段 | - | workflow级环境变量 | 所有job和step可见 | env:<br>  APP_NAME: x | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-396 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | defaults | 字段 | - | 默认设置 | 默认shell和working-directory | defaults:<br>  run:<br>    shell: bash | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-397 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | concurrency | 字段 | - | 并发控制 | 限制并行运行数 | concurrency:<br>  max: 3 | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-398 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | permissions | 字段 | - | 权限声明 | 控制TOKEN权限范围 | permissions:<br>  repository: read | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-399 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | stages | 字段 | - | 阶段定义 | 阶段串行控制 | stages:<br>  build: ... | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-400 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | jobs | 字段 | - | 任务集合 | 无stages时为顶层 | jobs:<br>  build: ... | any | 必填 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-401 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | post | 字段 | - | 后处理阶段 | 通知/清理/回写 | post:<br>  run_always: true | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-402 | writing-pipelines/workflow-file-location-structure | stages机制 | 阶段间串行 | 机制 | - | 多stage按定义顺序执行 | 前一stage完成后进入下一 | stages:<br>  - name: build<br>  - name: test | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-403 | writing-pipelines/workflow-file-location-structure | stages机制 | fail_fast=true | 机制 | - | stage中job失败 | 立即终止后续stage | stages:<br>  - fail_fast: true | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-404 | writing-pipelines/workflow-file-location-structure | stages机制 | fail_fast=false | 机制 | - | stage中job失败 | 不终止后续stage | stages:<br>  - fail_fast: false | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-405 | writing-pipelines/workflow-file-location-structure | stages机制 | 单stage可缺省 | 机制 | - | 仅一个stage时 | stages可省略,job默认并行 | jobs:<br>  a: ...<br>  b: ... | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-406 | writing-pipelines/workflow-file-location-structure | post机制 | run_always默认true | 机制 | - | post默认行为 | 无论成功失败都执行 | post:<br>  run_always: true | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-407 | writing-pipelines/workflow-file-location-structure | post机制 | run_always=false | 机制 | - | post设为false | 仅workflow成功时执行 | post:<br>  run_always: false | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-408 | writing-pipelines/workflow-file-location-structure | permissions快捷 | read-all | 快捷语法 | - | 所有权限设为read | 全部read | permissions: read-all | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-409 | writing-pipelines/workflow-file-location-structure | permissions快捷 | write-all | 快捷语法 | - | 所有权限设为write | 全部write | permissions: write-all | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-410 | writing-pipelines/workflow-file-location-structure | permissions快捷 | permissions:{} | 快捷语法 | - | 空对象 | 所有权限none(最小权限) | permissions: {} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-411 | writing-pipelines/workflow-file-location-structure | permissions项 | project | 权限项 | - | 项目访问权限 | read/write/none | permissions:<br>  project: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-412 | writing-pipelines/workflow-file-location-structure | permissions项 | pr | 权限项 | - | PR权限 | read/write/none | permissions:<br>  pr: write | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-413 | writing-pipelines/workflow-file-location-structure | permissions项 | issue | 权限项 | - | Issue权限 | read/write/none | permissions:<br>  issue: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-414 | writing-pipelines/workflow-file-location-structure | permissions项 | note | 权限项 | - | 评论/备注权限 | read/write/none | permissions:<br>  note: write | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-415 | writing-pipelines/workflow-file-location-structure | permissions项 | repository | 权限项 | - | 仓库权限 | read/write/none | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-416 | writing-pipelines/workflow-file-location-structure | permissions项 | hook | 权限项 | - | Webhook权限 | read/write/none | permissions:<br>  hook: none | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-417 | writing-pipelines/configure-triggers | 否定模式 | branches否定(!) | 模式 | - | branches用!前缀排除 | 排除指定分支 | branches:<br>  - 'feature/**'<br>  - '!feature/exp' | push | 必须与肯定模式组合 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-418 | writing-pipelines/configure-triggers | 否定模式 | paths否定(!) | 模式 | - | paths用!前缀排除 | 排除指定路径 | paths:<br>  - 'src/**'<br>  - '!src/docs/**' | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-419 | writing-pipelines/configure-triggers | 否定模式 | tags否定(!) | 模式 | - | tags用!前缀排除 | 排除指定tag | tags:<br>  - 'v*'<br>  - '!v*-alpha' | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-420 | writing-pipelines/configure-triggers | 否定模式 | 仅否定模式不触发 | 规则 | - | 只有否定模式无肯定 | workflow不会触发 | branches: ['!main'] | any | 需配合肯定模式 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-421 | writing-pipelines/configure-triggers | 过滤组合 | branches+paths组合 | 组合 | - | 分支和路径过滤组合 | 同时满足才触发 | on:<br>  push:<br>    branches: [main]<br>    paths: ['src/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-422 | writing-pipelines/configure-triggers | 过滤组合 | paths前300文件限制 | 规则 | - | paths匹配前300个变更文件 | 超出部分不参与匹配 | paths: ['src/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-423 | writing-pipelines/configure-triggers | 多事件组合 | push+PR+dispatch+schedule | 组合 | - | 同一workflow响应多事件 | 任一事件匹配即触发 | on:<br>  push:<br>  pull_request:<br>  workflow_dispatch:<br>  schedule: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-424 | writing-pipelines/configure-triggers | PR目标分支 | branches过滤目标分支 | 规则 | - | PR的branches过滤的是base分支 | PR目标分支不在列表则不触发 | on:<br>  pull_request:<br>    branches: [main] | pull_request | 非源分支 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |
| TC-425 | writing-pipelines/configure-triggers | PR types默认 | 默认types=[open,reopen,update] | 规则 | - | 不指定types时 | 默认三种不含merge | on:<br>  pull_request: | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 当前事件=Push,非pull_request,无法验证PR types | S4 | chaoran |  |
| TC-426 | writing-pipelines/configure-triggers | workflow_call | 嵌套最多2层 | 规则 | - | 可重用工作流嵌套调用 | 最多2层,不能再调用可重用 | uses: ./workflow.yml | workflow_call |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-427 | writing-pipelines/configure-triggers | schedule | cron UTC时区 | 规则 | - | cron使用UTC时间 | 需换算本地时间 | cron: '0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | suite-3 | S3 | yulin |  |
| TC-428 | writing-pipelines/configure-triggers | schedule | 仅默认分支生效 | 规则 | - | schedule仅在默认分支 | 非默认分支不触发定时 | on:<br>  schedule: | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S3 | yulin |  |
| TC-429 | writing-pipelines/configure-triggers | schedule | 最短间隔5分钟 | 规则 | - | schedule最短间隔 | 低于5分钟不生效 | cron: '*/5 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(平台限制由调度器强制执行),仅验文档约束 | S3 | yulin |  |
| TC-430 | writing-pipelines/configure-triggers | schedule | 调度延迟数分钟 | 规则 | - | 定时任务可能延迟 | 存在数分钟调度延迟 | cron: '0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(调度延迟由平台负载决定),仅验文档约束 | S3 | yulin |  |
| TC-431 | writing-pipelines/using-script-commands | 脚本执行 | 执行仓库内脚本 | 脚本 | bash ./scripts/build.sh | 执行仓库中已有脚本 | 脚本正常运行 | run: bash ./scripts/build.sh | any | 需先checkout | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-432 | writing-pipelines/using-script-commands | 脚本执行 | chmod设置执行权限 | 脚本 | chmod +x ./scripts/build.sh | 给脚本加执行权限 | 可直接执行 | run: chmod +x ./scripts/build.sh | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-433 | writing-pipelines/using-script-commands | 脚本执行 | 直接执行已授权脚本 | 脚本 | ./scripts/build.sh | 直接执行有权限的脚本 | 正常运行 | run: ./scripts/build.sh | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-434 | writing-pipelines/using-script-commands | 多行输出 | ATOMGIT_OUTPUT多行写入 | 输出 | echo 'content<<$EOF' >> $ATOMGIT_OUTPUT | 写入多行值到输出 | 用分隔符包围多行 | run: \|<br>  EOF=$(dd...)<br>  echo 'content<<$EOF' >> $ATOMGIT_OUTPUT | any | 使用随机分隔符 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-435 | writing-pipelines/using-script-commands | 多行输出 | 多行环境变量 | 输出 | echo 'var<<$EOF' >> $ATOMGIT_ENV | 写入多行环境变量 | 后续step可用多行值 | run: echo 'APP<<$EOF' >> $ATOMGIT_ENV | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-436 | writing-pipelines/using-script-commands | 脱敏命令 | ::add-mask:: | 安全 | echo '::add-mask::$MY_SECRET' | 日志中掩藏敏感信息 | 值显示为*** | run: echo '::add-mask::$MY_SECRET' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |
| TC-437 | writing-pipelines/using-script-commands | 脚本命令 | run执行shell | 脚本 | run: echo hello | 在step中执行shell命令 | 命令正常执行 | run: echo hello | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-438 | writing-pipelines/using-variables-secrets | 引用方式 | YAML中引用(表达式) | 引用 | ${{ env.APP_NAME }} | 在YAML字段中使用 | Runner执行前替换 | run: echo ${{ env.APP_NAME }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-439 | writing-pipelines/using-variables-secrets | 引用方式 | Runner中引用(环境变量) | 引用 | $APP_NAME | 在run命令中使用 | 由Shell解释 | run: echo $APP_NAME | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-440 | writing-pipelines/using-variables-secrets | 优先级总览 | Step级env>Job级env>Workflow级env>vars>系统变量 | 优先级 | - | 完整优先级顺序 | 按序覆盖 | - | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-441 | writing-pipelines/using-variables-secrets | 系统变量补充 | ATOMGIT_RUNNER_OS | 系统变量 | $ATOMGIT_RUNNER_OS | Runner操作系统 | 返回Linux/Windows/macOS | run: echo $ATOMGIT_RUNNER_OS | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |
| TC-442 | writing-pipelines/using-variables-secrets | 系统变量补充 | ATOMGIT_RUNNER_ARCH | 系统变量 | $ATOMGIT_RUNNER_ARCH | Runner架构 | 返回X64/ARM/ARM64 | run: echo $ATOMGIT_RUNNER_ARCH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |
| TC-443 | writing-pipelines/using-variables-secrets | secrets安全 | 不要echo secrets | 安全 | echo '${{secrets.X}}' | 可能绕过脱敏 | 避免此写法 | - | any | echo ${{secrets}}不安全 | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-444 | writing-pipelines/using-variables-secrets | secrets安全 | 不要写入制品/缓存 | 安全 | - | secrets不写入artifact | 避免泄露 | - | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-445 | writing-pipelines/using-variables-secrets | secrets安全 | 外部PR不暴露高权限 | 安全 | - | fork PR默认不暴露 | 高权限secret | - | pull_request |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S4 | chaoran |  |
| TC-446 | runner-management/using-hosted-runners | 托管Runner | 使用官方资源池 | Runner | runs-on: [ubuntu-latest, x64, small] | 无需自建基础设施 | 调度到官方托管Runner | runs-on: [ubuntu-latest, x64, small] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-447 | runner-management/using-hosted-runners | 托管Runner | 资源规格small | 标签 | small | 小型资源规格 | 调度到small规格Runner | runs-on: [ubuntu-latest, x64, small] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-448 | runner-management/using-hosted-runners | 托管Runner | 资源规格large | 标签 | large | 大型资源规格 | 调度到large规格Runner | runs-on: [ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-449 | runner-management/using-self-hosted-runners | 自托管Runner | 主机自托管 | Runner | runs-on: [self-hosted] | 部署在主机上 | 调度到自托管Runner | runs-on: [self-hosted] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-450 | runner-management/using-self-hosted-runners | 自托管Runner | Kubernetes自托管 | Runner | runs-on: [self-hosted, k8s] | 部署在K8s上 | 调度到K8s Runner | runs-on: [self-hosted, k8s] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-451 | runner-management/using-self-hosted-runners | 自托管Runner | 特殊硬件GPU | 场景 | runs-on: [self-hosted, gpu] | 需要GPU硬件 | 调度到带GPU的Runner | runs-on: [self-hosted, gpu] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-452 | runner-management/using-self-hosted-runners | 自托管Runner | 内网环境 | 场景 | runs-on: [self-hosted, intranet] | 需要内网环境 | 调度到内网Runner | runs-on: [self-hosted, intranet] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-453 | runner-management/selecting-runner-labels | 标签选择 | 操作系统标签 | 标签 | ubuntu-latest/windows-latest/macos-latest | 指定操作系统 | 调度到对应OS Runner | runs-on: [windows-latest] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-454 | runner-management/selecting-runner-labels | 标签选择 | 架构标签 | 标签 | x64/arm64 | 指定架构 | 调度到对应架构Runner | runs-on: [arm64] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-455 | runner-management/selecting-runner-labels | 标签选择 | 资源规格标签 | 标签 | small/large | 指定资源规格 | 调度到对应规格Runner | runs-on: [large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-456 | runner-management/selecting-runner-labels | 标签选择 | 自定义特征标签 | 标签 | gpu/special-tool | 自定义特征(如GPU) | 调度到匹配特征Runner | runs-on: [self-hosted, gpu] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-457 | runner-management/selecting-runner-labels | 标签选择 | 多标签组合 | 标签 | runs-on: [ubuntu-latest, x64, small] | 多标签同时指定 | 必须同时满足所有标签 | runs-on: [ubuntu-latest, x64, small] | any | AND逻辑 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-458 | runner-management/configuring-images-toolchains | 镜像工具链 | container自定义镜像 | 容器 | container:<br>  image: python:3.12 | 指定自定义Docker镜像 | Job在指定容器内执行 | container:<br>  image: python:3.12 | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-459 | runner-management/configuring-images-toolchains | 镜像工具链 | container特定语言版本 | 容器 | container:<br>  image: node:20 | 指定特定语言版本 | 使用指定语言环境 | container:<br>  image: node:20 | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-460 | runner-management/configuring-images-toolchains | 镜像工具链 | container完整构建环境 | 容器 | container:<br>  image: my-builder:latest | 使用完整构建环境 | 使用自定义构建环境 | container:<br>  image: my-builder:latest | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |
| TC-461 | syntax-reference/trigger-events | pull_request_target | pull_request_target事件 | 事件 | on:<br>  pull_request_target: | 运行在目标分支上下文 | 可读写目标仓库 | on:<br>  pull_request_target:<br>    types: [open] | pull_request_target | 用于secrets/写操作 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP | S4 | chaoran |  |
| TC-462 | syntax-reference/trigger-events | pull_request_target | fork PR安全风险 | 安全 | - | fork仓库PR也能触发 | 谨慎处理代码执行 | - | pull_request_target | 安全提示 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP | S4 | chaoran |  |
| TC-463 | syntax-reference/trigger-events | pull_request_target | 默认types=[open,reopen,update] | 规则 | - | 不指定types时 | 默认三种不含merge | on:<br>  pull_request_target: | pull_request_target |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP | S4 | chaoran |  |
| TC-464 | syntax-reference/trigger-events | issue_comment | issue_comment事件 | 事件 | on:<br>  issue_comment:<br>    types: [created] | Issue或PR评论触发 | 同时对Issue和PR评论生效 | on:<br>  issue_comment:<br>    types: [created] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |
| TC-465 | syntax-reference/trigger-events | issue_comment | types: created | 类型 | created | 评论创建时触发 | 触发workflow | types: [created] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP | S15 | chaoran |  |
| TC-466 | syntax-reference/trigger-events | issue_comment | types: edited | 类型 | edited | 评论编辑时触发 | 触发workflow | types: [edited] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |
| TC-467 | syntax-reference/trigger-events | issue_comment | types: deleted | 类型 | deleted | 评论删除时触发 | 触发workflow | types: [deleted] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |
| TC-468 | syntax-reference/trigger-events | issue_comment | 区分PR评论 | 条件 | atomgit.event.issue.pull_request | 判断是否PR评论 | 存在则为PR评论 | if: ${{atomgit.event.issue.pull_request}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP | S15 | chaoran |  |
| TC-469 | syntax-reference/trigger-events | pull_request_comment | pull_request_comment事件 | 事件 | on:<br>  pull_request_comment: | 仅在PR评论时触发 | 区别于issue_comment | on:<br>  pull_request_comment:<br>    types: [created] | pull_request_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |
| TC-470 | syntax-reference/trigger-events | pull_request_comment | comments正则过滤 | 过滤 | comments: ['/deploy'] | 基于正则过滤评论内容 | 仅匹配评论触发 | comments: ['/deploy', '/test'] | pull_request_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S4 | chaoran |  |
| TC-471 | syntax-reference/trigger-events | cron特殊符号 | * 任意值 | 符号 | * * * * * | 匹配任意值 | 每分钟触发 | cron: '* * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-472 | syntax-reference/trigger-events | cron特殊符号 | , 列表分隔 | 符号 | 1,3,5 | 列表分隔 | 第1、3、5 | cron: '0 0 * * 1,3,5' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-473 | syntax-reference/trigger-events | cron特殊符号 | - 范围 | 符号 | 1-5 | 范围 | 1到5 | cron: '0 0 * * 1-5' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-474 | syntax-reference/trigger-events | cron特殊符号 | / 步长 | 符号 | */15 | 步长 | 每15单位 | cron: '*/15 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-475 | syntax-reference/trigger-events | cron位置 | 分钟(0-59) | 位置 | cron: 'm * * * *' | 每小时第几分钟 | 0-59 | cron: '30 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |
| TC-476 | syntax-reference/trigger-events | cron位置 | 小时(0-23) | 位置 | cron: '* h * * *' | UTC时间小时 | 0-23 | cron: '0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |
| TC-477 | syntax-reference/trigger-events | cron位置 | 日(1-31) | 位置 | cron: '* * d * *' | 每月第几天 | 1-31 | cron: '0 0 1 * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |
| TC-478 | syntax-reference/trigger-events | cron位置 | 月(1-12) | 位置 | cron: '* * * m *' | 月份 | 1-12 | cron: '0 0 1 1 *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |
| TC-479 | syntax-reference/trigger-events | cron位置 | 星期(0-6) | 位置 | cron: '* * * * w' | 0=周日..6=周六 | 0-6 | cron: '0 0 * * 0' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |
| TC-480 | examples/nodejs-ci | Node.js示例 | npm ci构建 | 示例 | npm ci && npm test | Node.js项目CI | 构建和测试 | run: npm ci && npm test | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需npm工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-481 | examples/nodejs-ci | Node.js示例 | 多版本矩阵(node 18/20) | 示例 | matrix:<br>  node: [18,20] | 多版本矩阵测试 | 展开2实例 | strategy:<br>  matrix:<br>    node: [18, 20] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-4 | S11 | chenqi |  |
| TC-482 | examples/java-maven-ci | Java Maven示例 | mvn build | 示例 | mvn clean package | Maven项目构建 | 生成jar包 | run: mvn clean package | push |  | — | — | —(仅可经Job日志断言) | C 难真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | SKIP: 难真测(需mvn工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-483 | examples/java-maven-ci | Java Maven示例 | 多JDK矩阵(8/11/17) | 示例 | matrix:<br>  jdk: [8,11,17] | 多JDK版本测试 | 展开3实例 | strategy:<br>  matrix:<br>    jdk: [8, 11, 17] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | suite-4 | S11 | chenqi |  |
| TC-484 | examples/java-gradle-ci | Java Gradle示例 | gradle build | 示例 | gradle build | Gradle项目构建 | 生成构建结果 | run: gradle build | push |  | — | — | —(仅可经Job日志断言) | C 难真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | SKIP: 难真测(需gradle工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-485 | examples/java-gradle-ci | Java Gradle示例 | Gradle缓存 | 示例 | cache:<br>  path: ~/.gradle | 缓存Gradle依赖 | 加速后续构建 | uses: cache<br>  with:<br>    path: ~/.gradle | push |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S11 | chenqi |  |
| TC-486 | examples/go-ci | Go示例 | go build | 示例 | go build ./... | Go项目构建 | 生成二进制 | run: go build ./... | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-487 | examples/go-ci | Go示例 | go test | 示例 | go test ./... | Go项目测试 | 运行测试 | run: go test ./... | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-488 | examples/go-ci | Go示例 | go vet | 示例 | go vet ./... | Go静态检查 | 运行vet | run: go vet ./... | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-489 | examples/go-ci | Go示例 | go test覆盖率 | 示例 | go test -coverprofile=coverage.out | 生成覆盖率 | 输出coverage.out | run: go test -coverprofile=coverage.out | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-490 | examples/go-ci | Go示例 | 多Go版本矩阵(1.19/1.20/1.21) | 示例 | matrix:<br>  go: [1.19,1.20,1.21] | 多Go版本测试 | 展开3实例 | strategy:<br>  matrix:<br>    go: [1.19, 1.20, 1.21] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: matrix.go=1.2 不在预期集合(1.19,1.20,1.21) | S11 | chenqi |  |
| TC-491 | examples/python-ci | Python示例 | flake8检查 | 示例 | flake8 src/ --max-line-length=120 | Python lint检查 | 输出格式问题 | run: flake8 src/ --max-line-length=120 | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需flake8工具+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-492 | examples/python-ci | Python示例 | black格式检查 | 示例 | black --check --diff src/ | 格式检查 | 输出格式差异 | run: black --check --diff src/ | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需black工具+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-493 | examples/python-ci | Python示例 | isort导入排序 | 示例 | isort --check-only --diff src/ | 导入排序检查 | 输出导入差异 | run: isort --check-only --diff src/ | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需isort工具+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-494 | examples/python-ci | Python示例 | mypy类型检查 | 示例 | mypy src/ --ignore-missing-imports | 类型检查 | 输出类型问题 | run: mypy src/ --ignore-missing-imports | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需mypy工具+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-495 | examples/python-ci | Python示例 | pytest+覆盖率 | 示例 | pytest tests/ --cov=src --cov-report=xml | 单元测试+覆盖率 | 生成coverage.xml | run: pytest tests/ --cov=src | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需pytest+coverage工具+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-496 | examples/python-ci | Python示例 | 多Python矩阵(3.10/3.11/3.12) | 示例 | matrix:<br>  python: [3.10,3.11,3.12] | 多Python版本测试 | 展开3实例 | strategy:<br>  matrix:<br>    python: [3.10, 3.11, 3.12] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: matrix.python=3.1 不在预期集合(3.10,3.11,3.12) | S11 | chenqi |  |
| TC-497 | examples/python-ci | Python示例 | STEP_SUMMARY写入 | 示例 | echo '## 测试结果' >> $ATOMGIT_STEP_SUMMARY | 写入步骤摘要 | 摘要显示在UI | run: echo '## 结果' >> $ATOMGIT_STEP_SUMMARY | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: GITCODE_STEP_SUMMARY/GITHUB_STEP_SUMMARY 环境变量未注入，无法验证摘要写入 | S11 | chenqi |  |
| TC-498 | examples/python-ci | Python示例 | setup-python缓存pip | 示例 | setup-python:<br>  with:<br>    cache: 'pip' | 设置Python并缓存pip | 加速依赖安装 | uses: setup-python<br>  with:<br>    cache: 'pip' | push |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S11 | chenqi |  |
| TC-499 | examples/python-ci | Python示例 | python -m build打包 | 示例 | python -m build | 构建Python包 | 生成dist/ | run: python -m build | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(需python build工具+项目源码),仅验语法声明 | S11 | chenqi |  |
| TC-500 | examples/pr-code-check-example | PR检查示例 | 代码风格检查 | 示例 | run: flake8 src/ | PR代码风格 | 评论检查结果 | run: flake8 src/ | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(依赖lint外部工具+项目源码),仅验语法声明 | S4 | chaoran |  |
| TC-501 | examples/pr-code-check-example | PR检查示例 | 安全扫描 | 示例 | run: bandit -r src/ | PR安全扫描 | 输出安全问题 | run: bandit -r src/ | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(依赖SAST外部工具+项目源码),仅验语法声明 | S4 | chaoran |  |
| TC-502 | examples/pr-code-check-example | PR检查示例 | PR评论 | 示例 | gh pr comment | 自动评论PR | 输出检查结果 | run: gh pr comment $PR --body '...' | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | 没有gh命令，使用gitcode cli可以实现 | S4 | chaoran |  |
| TC-503 | examples/pr-code-check-example | PR检查示例 | 审查辅助 | 示例 | - if: ${{always}} | always条件执行 | 无论成功失败都评论 | if: ${{always}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(依赖平台API写PR评论),仅验语法声明 | S4 | chaoran |  |
| TC-504 | syntax-reference/trigger-events | cron特殊符号 | cron星号*任意值 | 边界 | cron: '* * * * *' | 星号匹配任意值 | 每分钟触发一次 | cron: '* * * * *' | schedule | 每段可独立用* | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | — | liyanghang |  |
| TC-505 | syntax-reference/trigger-events | cron特殊符号 | cron逗号,枚举 | 边界 | cron: '5,15,25 * * * *' | 逗号枚举多个值 | 第5/15/25分钟触发 | cron: '5,15,25 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-506 | syntax-reference/trigger-events | cron特殊符号 | cron连字符-区间 | 边界 | cron: '0-5 * * * *' | 连字符表示区间 | 第0~5分钟连续触发 | cron: '0-5 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-507 | syntax-reference/trigger-events | cron特殊符号 | cron斜杠/步长 | 边界 | cron: '*/15 * * * *' | 斜杠表示步长 | 每15分钟触发一次 | cron: '*/15 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-508 | syntax-reference/trigger-events | cron特殊符号 | cron问号?日或周 | 边界 | cron: '0 2 ? * *' | 问号代替日或周 | 日和周不能同时指定 | cron: '0 2 ? * *' | schedule | ?表示不指定 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-509 | syntax-reference/trigger-events | cron特殊符号 | cron字符L月末 | 边界 | cron: '0 0 L * *' | L表示最后 | 月末最后一天触发 | cron: '0 0 L * *' | schedule | L=last | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-510 | syntax-reference/trigger-events | cron特殊符号 | cron字符W最近工作日 | 边界 | cron: '0 0 15W * *' | W表示最近工作日 | 15号最近的工作日触发 | cron: '0 0 15W * *' | schedule | W=weekday | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-511 | syntax-reference/trigger-events | cron特殊符号 | cron字符#第N周 | 边界 | cron: '0 0 * * 2#3' | #表示第N个星期 | 每月第3个周二触发 | cron: '0 0 * * 2#3' | schedule | #=nth | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-512 | syntax-reference/trigger-events | cron特殊符号 | cron区间+步长组合 | 边界 | cron: '5-45/10 * * * *' | 区间和步长组合 | 5到45每10分钟触发 | cron: '5-45/10 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |
| TC-513 | syntax-reference/trigger-events | cron特殊符号 | cron非法值越界 | 边界 | cron: '70 * * * *' | 分钟超出0-59范围 | 应:拒绝或截断到边界 | cron: '70 * * * *' | schedule | 越界值 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |
| TC-514 | writing-pipelines/configure-triggers | 过滤组合 | paths满300文件 | 边界 | paths: ['src/**'] | 变更文件恰为300个 | 前300全参与匹配 | paths: ['src/**'] | push | 边界恰好不溢 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-515 | writing-pipelines/configure-triggers | 过滤组合 | paths溢出301文件 | 边界 | paths: ['src/**'] | 变更文件为301个 | 第301个不参与匹配,可能漏触发 | paths: ['src/**'] | push | 超限部分忽略 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |
| TC-516 | writing-pipelines/configure-triggers | 过滤组合 | paths空变更列表 | 边界 | paths: ['src/**'] | 无文件变更 | 不触发或退化判断 | paths: ['src/**'] | push | 空数组 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |
| TC-517 | writing-pipelines/configure-triggers | 过滤组合 | paths与paths-ignore同用 | 边界 | - | 两者同时声明 | 应:YAML解析报错,互斥 | paths+paths-ignore | push | 文档明示互斥 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |
| TC-518 | concurrency | 并发控制 | QUEUE队列满 | 边界 | exceed-action: QUEUE | 队列已满新任务 | 应:排队等待,后续可能延迟 | exceed-action: QUEUE | any | 队列上限 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |
| TC-519 | concurrency | 并发控制 | IGNORE丢弃 | 边界 | exceed-action: IGNORE | 并发已满新任务 | 应:直接丢弃,不排队 | exceed-action: IGNORE | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |
| TC-520 | concurrency | 并发控制 | CANCEL抢占 | 边界 | exceed-action: CANCEL | 并发已满新任务 | 应:取消旧任务执行新的 | exceed-action: CANCEL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-521 | concurrency | 并发控制 | max=1单并发 | 边界 | max: 1 | max设为最小值1 | 严格串行,无并发 | max: 1 | any | 边界值 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-522 | concurrency | 并发控制 | max=0非法值 | 边界 | max: 0 | max设为0 | 应:拒绝配置或视为无限 | max: 0 | any | 越界值 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-D | liyanghang |  |
| TC-523 | concurrency | 并发控制 | enable=false禁用 | 边界 | enable: false | 显式禁用并发控制 | 应:不限制并行数 | enable: false | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-524 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix空数组 | 边界 | matrix: {os: []} | 矩阵变量值为空数组 | 应:不生成实例或解析报错 | matrix: {os: []} | any | 空矩阵 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-D | liyanghang |  |
| TC-525 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix单值变量 | 边界 | matrix: {os: [ubuntu]} | 变量仅1个值 | 应:生成1个实例 | matrix: {os: [ubuntu]} | any | 退化非矩阵 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-526 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix三维展开 | 边界 | matrix: {os,arch,node} | 三维变量组合 | 应:笛卡尔积生成n1xn2xn3实例 | matrix: {os,arch,node} | any | 维度上限 | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 三维展开需专用三维矩阵 workflow 才能观察实例总数,当前 job 仅有二维矩阵 | Tier-A | liyanghang |  |
| TC-527 | writing-pipelines/configure-matrix-builds | 矩阵构建 | include无基础变量 | 边界 | include: [{x: 1}] | include变量未在matrix定义 | 应:include独立成实例或追加 | include: [{x: 1}] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: include 独立成实例需专用无基础矩阵变量的 workflow,无法在有基础变量的矩阵中验证 | Tier-A | liyanghang |  |
| TC-528 | writing-pipelines/configure-matrix-builds | 矩阵构建 | exclude全排除 | 边界 | exclude: [全部组合] | exclude排除所有组合 | 应:0实例,workflow不执行 | exclude: [全部] | any | 空矩阵 | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-A | liyanghang |  |
| TC-529 | writing-pipelines/configure-matrix-builds | 矩阵构建 | runs-on引用不存在变量 | 边界 | runs-on: ${{matrix.x}} | matrix未定义该变量 | 应:解析报错或空值 | runs-on: ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-530 | core-concepts/variables-secrets-context-expressions | secrets安全 | 引用未定义secret | 边界 | secrets.NOT_EXIST | 引用未在界面配置的secret | 应:返回空串而非报错 | env: {T: ${{secrets.NOT_EXIST}}} | any | 安全降级 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S1 | yulin |  |
| TC-531 | core-concepts/variables-secrets-context-expressions | secrets安全 | secret名含连字符 | 边界 | secrets.my-secret | secret名含连字符 | 应:正常访问 | ${{secrets.my-secret}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-532 | core-concepts/variables-secrets-context-expressions | secrets安全 | secret空值 | 边界 | secrets.EMPTY | secret配置为空串 | 应:返回空串,不报错 | ${{secrets.EMPTY}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |
| TC-533 | core-concepts/variables-secrets-context-expressions | 变量优先级 | env与vars同名 | 边界 | - | env和vars同名变量 | 应:env覆盖vars | - | any | env>vars规则 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(vars需在AtomGit平台界面定义同名变量才可对比,无法从shell内部独立验证覆盖结果),仅验语法声明 | S2 | yulin |  |
| TC-534 | core-concepts/variables-secrets-context-expressions | 变量优先级 | vars与系统变量同名 | 边界 | - | vars与ATOMGIT_*同名 | 应:vars覆盖系统变量 | - | any | vars>系统变量 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(vars需在AtomGit平台界面定义与系统变量同名的vars才可对比),仅验语法声明 | S2 | yulin |  |
| TC-535 | core-concepts/variables-secrets-context-expressions | 变量优先级 | secrets与vars同名 | 边界 | - | secrets与vars同名 | 应:独立命名空间互不影响 | - | any | 不同空间 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(secrets和vars均需平台界面定义同名项才可验证独立性),仅验语法声明 | S13 | yulin |  |
| TC-536 | syntax-reference/expressions | 字面量 | 布尔false | 边界 | ${{ false }} | 字面量false求值 | 返回false | ${{ false }} | any | 与true对称 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-537 | syntax-reference/expressions | 字面量 | 浮点数3.14 | 边界 | ${{ 3.14 }} | 浮点数字面量 | 返回3.14,支持小数 | ${{ 3.14 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-538 | syntax-reference/expressions | 字面量 | 字符串单引号 | 边界 | ${{ 'hello' }} | 字符串字面量 | 返回hello | ${{ 'hello' }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-539 | syntax-reference/expressions | 字面量 | 整数42 | 边界 | ${{ 42 }} | 整数字面量 | 返回42 | ${{ 42 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |
| TC-540 | syntax-reference/expressions | 运算符 | !=不等于 | 边界 | ${{ a != b }} | 不等于运算符 | a不等于b时true | ${{ atomgit.event_name != 'schedule' }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-541 | syntax-reference/expressions | 运算符 | >=大于等于 | 边界 | ${{ a >= b }} | 大于等于运算符 | a大于或等于b时true | ${{ matrix.version >= 12 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-542 | syntax-reference/expressions | 运算符 | <=小于等于 | 边界 | ${{ a <= b }} | 小于等于运算符 | a小于或等于b时true | ${{ inputs.count <= 10 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-543 | syntax-reference/expressions | 函数 | contains子串匹配 | 边界 | ${{ contains(s, item) }} | contains字符串子串 | 包含子串时true | ${{ contains(atomgit.ref, 'release') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-544 | syntax-reference/expressions | 函数 | contains数组匹配 | 边界 | ${{ contains(arr, item) }} | contains数组元素 | 包含该元素时true | ${{ contains(matrix.os, 'ubuntu') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-545 | syntax-reference/expressions | 函数 | startsWith区分大小写 | 边界 | ${{ startsWith(s, p) }} | startsWith大小写敏感 | 大写小写不匹配 | ${{ startsWith(atomgit.ref, 'refs/tags/') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-546 | syntax-reference/expressions | 函数 | format多占位符 | 边界 | ${{ format({0}{1}, a, b) }} | format多参数替换 | 按0,1...顺序替换 | ${{ format('{0}:{1}', 'img', 'v1') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-547 | syntax-reference/expressions | 函数 | substring截取 | 边界 | ${{ substring(s, 0, 7) }} | substring截取子串 | 从start截取len长度 | ${{ substring(atomgit.sha, 0, 7) }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-548 | syntax-reference/expressions | 函数 | replace替换 | 边界 | ${{ replace(s, old, new) }} | replace字符串替换 | 替换old为new | ${{ replace(atomgit.ref, 'refs/heads/', '') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-549 | syntax-reference/expressions | 函数 | toJson序列化 | 边界 | ${{ toJson(obj) }} | toJson对象转JSON | 返回JSON字符串 | ${{ toJson(atomgit.event) }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-550 | syntax-reference/expressions | 函数 | hashFiles多路径 | 边界 | ${{ hashFiles(a, b) }} | hashFiles多路径哈希 | 返回组合SHA256 | ${{ hashFiles('src/**', 'package.json') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |
| TC-551 | syntax-reference/workflow-commands | 工作流命令 | 废弃set-output格式 | 边界 | ::set-output name=k::v | 使用废弃旧格式 | 应:兼容但建议用新格式 | echo '::set-output name=k::v' | any | 文档标注废弃 | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 | SKIP: 难真测(废弃格式::set-output::兼容性由平台决定,shell内部无法验证平台是否处理),仅验语法声明 | Tier-A | liyanghang |  |
| TC-552 | syntax-reference/workflow-commands | 工作流命令 | 废弃set-env格式 | 边界 | ::set-env name=K::V | 使用废弃set-env | 应:兼容但建议用$ATOMGIT_ENV | echo '::set-env name=K::V' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL（命令未被解析，原样输出；DYNAMIC_VAR未被设置为环境变量，不具备向后兼容性） | SKIP: 难真测(废弃格式::set-env::兼容性由平台决定,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi |  |
| TC-553 | syntax-reference/workflow-commands | 工作流命令 | 废弃add-path格式 | 边界 | ::add-path::/p | 使用废弃add-path | 应:兼容但建议用$ATOMGIT_PATH | echo '::add-path::/p' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL（命令未被解析，原样输出；DYNAMIC_VAR未被设置为环境变量，不具备向后兼容性） | SKIP: 难真测(废弃格式::add-path::兼容性由平台决定,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi |  |
| TC-554 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_OUTPUT空值 | 边界 | echo k= >> $ATOMGIT_OUTPUT | 写入空值到输出 | 应:键为空,后续可读 | echo 'k=' >> $ATOMGIT_OUTPUT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-555 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_OUTPUT键重复 | 边界 | - | 同名键多次写入 | 应:后写覆盖前值 | echo k=v1 then k=v2 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-556 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_ENV跨Job失效 | 边界 | - | env仅当前Job后续step可用 | 跨Job不可见,需outputs传递 | echo K=V >> $ATOMGIT_ENV | any | 作用域边界 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-557 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_PATH重复添加 | 边界 | - | PATH多次添加同目录 | 应:可能重复,建议幂等 | echo /p >> $ATOMGIT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-558 | writing-pipelines/configure-triggers | 触发配置 | branches与branches-ignore同用 | 边界 | - | 两者同时声明 | 应:YAML解析报错,互斥 | branches+branches-ignore | push | 文档明示互斥 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |
| TC-559 | writing-pipelines/configure-triggers | 触发配置 | tags与tags-ignore同用 | 边界 | - | 两者同时声明 | 应:YAML解析报错,互斥 | tags+tags-ignore | push | 互斥 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |
| TC-560 | writing-pipelines/configure-triggers | 触发配置 | pull_request types非法值 | 边界 | types: [invalid] | types取非法值 | 应:拒绝,仅[merge,open,reopen,update] | types: [invalid] | pull_request | 越界 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S4 | chaoran |  |
| TC-561 | writing-pipelines/configure-triggers | 触发配置 | pull_request types含merge | 边界 | types: [merge] | types显式含merge | 合并PR时触发 | types: [merge] | pull_request | merge不在默认列表 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 当前事件=Push,非pull_request,无法验证PR types含merge | S4 | chaoran |  |
| TC-562 | writing-pipelines/configure-triggers | 触发配置 | schedule非默认分支 | 边界 | - | 在非默认分支定义schedule | 应:不触发(仅默认分支生效) | schedule: [{cron}] | schedule | 文档明示限制 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S3 | yulin |  |
| TC-563 | writing-pipelines/configure-triggers | 触发配置 | schedule调度延迟 | 边界 | - | 定时触发存在数分钟延迟 | 应:容忍数分钟延迟,不精确到秒 | - | schedule | 文档明示延迟 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S3 | yulin |  |
| TC-564 | writing-pipelines/configure-triggers | 触发配置 | workflow_call嵌套第3层 | 边界 | uses: ./deep.yml | 可重用工作流嵌套超过2层 | 应:拒绝执行,最多2层 | uses: ./deep.yml | workflow_call | 文档明示上限 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S4 | chaoran |  |
| TC-565 | writing-pipelines/configure-triggers | 触发配置 | 否定模式单独使用 | 边界 | branches: [!main] | 仅否定模式无肯定模式 | 应:workflow不触发 | branches: [!main] | push | 文档明示约束 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |
| TC-566 | syntax-reference/context | atomgit上下文属性 | atomgit.sha完整性 | 边界 | ${{ atomgit.sha }} | sha应为完整40字符 | 返回完整SHA而非截断 | ${{ atomgit.sha }} | any | 长度边界 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-567 | syntax-reference/context | atomgit上下文属性 | atomgit.ref格式 | 边界 | ${{ atomgit.ref }} | ref应含refs/前缀 | 返回refs/heads/main或refs/tags/v1 | ${{ atomgit.ref }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-568 | syntax-reference/context | atomgit上下文属性 | atomgit.ref_name无前缀 | 边界 | ${{ atomgit.ref_name }} | ref_name不含refs/前缀 | 返回main或v1 | ${{ atomgit.ref_name }} | any | 与ref区分 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-569 | syntax-reference/context | atomgit上下文属性 | atomgit.run_id唯一性 | 边界 | ${{ atomgit.run_id }} | 每次运行run_id唯一 | 返回唯一运行编号 | ${{ atomgit.run_id }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |
| TC-570 | syntax-reference/context | atomgit上下文属性 | atomgit.actor非空 | 边界 | ${{ atomgit.actor }} | actor应为触发用户名 | 返回用户名,非空 | ${{ atomgit.actor }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |
| TC-571 | runner-management/selecting-runner-labels | 标签选择 | runs-on无匹配标签 | 边界 | runs-on: [nonexistent] | 指定不存在标签 | 应:排队等待或失败 | runs-on: [nonexistent] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |
| TC-572 | runner-management/selecting-runner-labels | 标签选择 | runs-on空标签数组 | 边界 | runs-on: [] | 空标签数组 | 应:拒绝配置或匹配任意 | runs-on: [] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |
| TC-573 | runner-management/selecting-runner-labels | 标签选择 | runs-on单标签 | 边界 | runs-on: [ubuntu-latest] | 仅1个标签 | 应:匹配该标签Runner | runs-on: [ubuntu-latest] | any | 最小组合 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |
| TC-574 | runner-management/configuring-images-toolchains | 镜像工具链 | container不存在镜像 | 边界 | image: nonexistent:latest | 指定仓库中不存在的镜像 | 应:拉取失败,Job失败 | image: nonexistent:latest | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |
| TC-575 | runner-management/configuring-images-toolchains | 镜像工具链 | container镜像无tag | 边界 | image: ubuntu | 镜像名无tag | 应:使用默认latest或报错 | image: ubuntu | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S5 | chaoran |  |
| TC-576 | writing-pipelines/pass-output-between-jobs | 输出传递 | outputs跨Job空值 | 边界 | - | 前置Job输出为空 | 应:后续Job读取为空,不报错 | - | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(跨Job空值行为需在后续Job中观察needs引用结果,步骤内无法自验证),仅验语法声明 | Tier-A | liyanghang |  |
| TC-577 | writing-pipelines/pass-output-between-jobs | 输出传递 | outputs跨Job未声明 | 边界 | ${{needs.build.outputs.not_exist}} | 引用未声明的output | 应:返回空或报错 | ${{needs.build.outputs.not_exist}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |
| TC-578 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs引用不存在Job | 边界 | needs: [nonexistent] | 依赖不存在的Job | 应:解析报错 | needs: [nonexistent] | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-579 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs循环依赖 | 边界 | a needs b, b needs a | Job循环依赖 | 应:解析报错,检测到环 | a needs b, b needs a | any | 拓扑环 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-580 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs自依赖 | 边界 | a needs a | Job依赖自己 | 应:解析报错 | a needs a | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-581 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs type=非string | 边界 | type: integer | inputs声明非string类型 | 应:拒绝,仅支持string | inputs: {x: {type: integer}} | workflow_dispatch | 文档明示限制 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-582 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs无required无default | 边界 | - | 既无required也无default | 应:取空串或报错 | - | workflow_dispatch | 缺省边界 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-583 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs required传空串 | 边界 | - | 必填参数传空字符串 | 应:视为已传(空串)还是未传 | - | workflow_dispatch | 空串边界 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |
| TC-584 | writing-pipelines/workflow-file-location-structure | stages机制 | stages空 | 边界 | stages: {} | stages为空 | 应:不执行任何stage | stages: {} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-585 | writing-pipelines/workflow-file-location-structure | stages机制 | stages单stage单job | 边界 | - | 仅1个stage含1个job | 应:正常执行,退化普通workflow | - | any | 最小形态 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-586 | writing-pipelines/workflow-file-location-structure | post机制 | post run_always=false | 边界 | run_always: false | 显式关闭run_always | 应:仅成功时执行post | run_always: false | any | 与默认true对比 | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS |  | Tier-B | liyanghang |  |
| TC-587 | writing-pipelines/workflow-file-location-structure | post机制 | post无steps | 边界 | post: {} | post段为空 | 应:正常,post跳过 | post: {} | any | 空边界 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |
| TC-588 | security-permissions | permissions快捷 | permissions空对象 | 边界 | permissions: {} | permissions为空对象 | 应:所有权限none(最小权限) | permissions: {} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-589 | security-permissions | permissions快捷 | permissions write-all | 边界 | permissions: write-all | 快捷语法write-all | 应:所有权限write | permissions: write-all | any | 与read-all对称 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |
| TC-590 | security-permissions | permissions项 | permissions非法值 | 边界 | repository: invalid | 权限值非法 | 应:拒绝,仅read/write/none | repository: invalid | any | 越界值 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-591 | action-development/action-yml-metadata-syntax | action.yml元数据 | action.yml文件名 | 边界 | action.yml | 文件名必须为action.yml,大小写敏感 | 应:非action.yml名不被识别;Action.yml被拒 | - | any | 文档明示大小写敏感 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-592 | action-development/action-yml-metadata-syntax | action.yml元数据 | action.yml格式YAML | 边界 | - | 文件必须为YAML格式 | 应:非YAML格式解析报错 | - | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-593 | action-development/action-yml-metadata-syntax | action.yml元数据 | name字段必需 | 边界 | name: 'codecheck' | name字段必需 | 应:缺name平台报错 | name: 'codecheck' | any | 顶级字段必需 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-594 | action-development/action-yml-metadata-syntax | action.yml元数据 | version字段必需 | 边界 | version: '1.0.0' | version字段必需,语义化版本 | 应:缺version报错,非X.Y.Z报错 | version: '1.0.0' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-595 | action-development/action-yml-metadata-syntax | action.yml元数据 | author字段必需 | 边界 | author: 'XXX' | author字段必需 | 应:缺author报错 | author: 'XXX' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-596 | action-development/action-yml-metadata-syntax | action.yml元数据 | description字段必需 | 边界 | description: '样例插件' | description字段必需 | 应:缺description报错 | description: '样例插件' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-597 | action-development/action-yll-metadata-syntax | action.yml元数据 | inputs字段必需 | 边界 | inputs: {key_input: {...}} | inputs字段必需 | 应:缺inputs报错 | inputs: {key_input: {required: true}} | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-598 | action-development/action-yml-metadata-syntax | action.yml元数据 | outputs字段必需 | 边界 | outputs: {record_id: {...}} | outputs字段必需 | 应:缺outputs报错 | outputs: {record_id: {description: 'id'}} | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-599 | action-development/action-yml-metadata-syntax | action.yml元数据 | runs字段必需 | 边界 | runs: {using: 'node16', main: 'dist/main.js'} | runs字段必需 | 应:缺runs报错 | runs: {using: 'node16', main: 'dist/main.js'} | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-600 | action-development/top-level-fields | runs执行方式 | runs.using=node16 | 边界 | using: 'node16' | 指定node16运行时 | 应:用Node.js 16执行编译后js | using: 'node16' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-601 | action-development/top-level-fields | runs执行方式 | runs.using非node16 | 边界 | using: 'node20' | 指定非node16版本 | 应:拒绝,仅支持node16 | using: 'node20' | any | 越界值 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-602 | action-development/top-level-fields | runs执行方式 | runs.main入口文件 | 边界 | main: 'dist/main.js' | 指定main入口 | 应:执行该js文件 | main: 'dist/main.js' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-603 | action-development/top-level-fields | runs执行方式 | runs.main不存在文件 | 边界 | main: 'dist/notexist.js' | main指向不存在文件 | 应:运行时报错 | main: 'dist/notexist.js' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-604 | action-development/top-level-fields | runs执行方式 | runs.post清理入口 | 边界 | post: 'dist/stop.js' | 指定post入口 | 应:Action终止时执行清理 | post: 'dist/stop.js' | any | 可选字段 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |
| TC-605 | action-development/top-level-fields | post触发机制 | post主动停止触发 | 边界 | - | 用户点击停止流水线 | 应:调度服务主动调用post | - | any | 文档明示 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-606 | action-development/top-level-fields | post触发机制 | post自然调用+SIGINT | 边界 | process.on('SIGINT') | 插件运行完成后自动调用 | 应:需在main监听SIGINT并调用post | - | any | 需代码配合 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-607 | action-development/top-level-fields | inputs命名规则 | input_id字母开头 | 边界 | key_input: {...} | input_id以字母或_开头 | 应:合法,被接受 | key_input: {required: true} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-608 | action-development/top-level-fields | inputs命名规则 | input_id含非法字符 | 边界 | key-input!: {...} | input_id含!等非法字符 | 应:拒绝,仅允许字母数字-_ | key-input!: {required: true} | any | 越界值 |  |  |  | D 测不动 | PASS |  | Tier-D | liyanghang |  |
| TC-609 | action-development/top-level-fields | inputs命名规则 | INPUT_环境变量注入 | 边界 | INPUT_KEY_INPUT | 输入转大写,空格替_ | 应:运行时$INPUT_KEY_INPUT可读 | inputs: {key input: {default: test}} | any | 大写转换 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-610 | action-development/top-level-fields | inputs校验 | required=true未传 | 边界 | required: true | 必填输入未传值 | 应:平台不自动报错,需代码主动校验 | - | any | 文档明示行为 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-611 | action-development/top-level-fields | inputs校验 | default默认值 | 边界 | default: test | 未指定输入用default | 应:运行时取default值 | inputs: {x: {default: test}} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-612 | action-development/top-level-fields | outputs声明 | output_id唯一 | 边界 | record_id: {...} | output_id唯一标识符 | 应:重复id报错 | outputs: {record_id: {description: 'id'}} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-613 | action-development/top-level-fields | outputs声明 | output_id命名规则 | 边界 | record-id: {...} | output_id命名规则同input | 应:字母/_开头,含字母数字-_ | outputs: {record-id: {description: 'id'}} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-614 | action-development/action-yml-metadata-syntax | 版本号规范 | 版本号X.Y.Z格式 | 边界 | version: '1.0.0' | 语义化版本格式 | 应:合法被接受 | version: '1.0.0' | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-615 | action-development/action-yml-metadata-syntax | 版本号规范 | 版本号不可回退 | 边界 | version: '0.9.0' | 版本号低于已发布 | 应:拒绝,版本只能新增 | - | any | 文档明示 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-616 | action-development/action-yll-metadata-syntax | 版本号规范 | 版本号含字母特殊字符 | 边界 | version: '1.0.0a' | 版本号含字母 | 应:拒绝,仅数字和点 | version: '1.0.0a' | any | 越界值 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-617 | action-development/action-yml-metadata-syntax | 版本号规范 | 预发布版本标识 | 边界 | version: '1.0.0-alpha' | 预发布版本alpha/beta/rc | 应:合法被接受 | version: '1.0.0-alpha' | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-618 | action-development/action-yml-metadata-syntax | 文件名规范 | Action.yml大写A | 边界 | Action.yml | 文件名大写A开头 | 应:拒绝,大小写敏感仅action.yml | - | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-619 | action-development/runtime-environment-variables | 运行时环境变量 | INPUT_变量注入 | 边界 | $INPUT_KEY_INPUT | 输入参数转环境变量 | 应:运行时可读 | echo $INPUT_KEY_INPUT | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-620 | action-development/runtime-environment-variables | 运行时环境变量 | ATOMGIT_系统变量 | 边界 | $ATOMGIT_SHA | Action内可读系统变量 | 应:与workflow同源,可读 | echo $ATOMGIT_SHA | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-621 | action-development/plugin-security-specification | Action安全规范 | 敏感数据禁硬编码 | 边界 | - | 敏感数据禁止硬编码 | 应:必须通过secrets输入 | - | any | 文档明示 |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |
| TC-622 | action-development/plugin-security-specification | Action安全规范 | 敏感数据加密存储 | 边界 | - | 敏感数据必须加密存储 | 应:运行期加密,及时清理 | - | any |  |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |
| TC-623 | action-development/plugin-security-specification | Action安全规范 | 输入参数须验证 | 边界 | - | 所有输入参数须严格验证 | 应:代码层校验输入合法性 | - | any |  |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |
| TC-624 | action-development/plugin-packaging | Action打包 | package.json构建 | 边界 | package.json | 通过package.json构建编排 | 应:构建命令打出可执行js | - | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-625 | action-development/plugin-packaging | Action打包 | dist/可执行js | 边界 | dist/main.js | 构建产物为dist/下可执行js | 应:runs.main指向dist/内文件 | dist/main.js | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-626 | action-development/plugin-project-structure | Action项目结构 | 插件目录结构 | 边界 | - | 插件项目目录结构规范 | 应:含action.yml/src/dist/package.json | - | any |  |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |
| TC-627 | writing-pipelines/using-actions | Action调用 | uses本地路径引用 | 边界 | uses: ./.github/actions/my-action | 引用本地Action | 应:执行仓库内该路径的action.yml | uses: ./.github/actions/my-action | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-628 | writing-pipelines/using-actions | Action调用 | uses带版本@ | 边界 | uses: actions/checkout@v3 | 引用指定版本Action | 应:执行该版本 | uses: actions/checkout@v3 | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |
| TC-629 | writing-pipelines/using-actions | Action调用 | uses with传参 | 边界 | with: {key_input: value} | 向Action传输入参数 | 应:参数转INPUT_KEY_INPUT环境变量 | with: {key_input: value} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

<details>
<summary>📋 完整用例列表（展开）</summary>


| 用例ID | 文档章节 | 测试分类 | 测试对象 | 类型 | 引用语法 | 测试内容 | 预期结果 | YAML示例片段 | 触发事件 | 备注 | 可验API字段 | JSON路径 | 预期规则 | 真测可达性 | 测试结果 | 失败原因/备注 | 测试会话 | 责任人 | 用例不当 |

|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|

| TC-001 | core-concepts/variables-secrets-context-expressions | env变量 | env(workflow级) | 变量定义 | ${{env.VAR}} | workflow顶层env定义GLOBAL_VAR | Runner中$GLOBAL_VAR可读 | env:<br>  GLOBAL_VAR: v | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-002 | core-concepts/variables-secrets-context-expressions | env变量 | env(job级) | 变量定义 | ${{env.VAR}} | job内env定义JOB_VAR | 该job可读$JOB_VAR | jobs:<br>  b:<br>    env:<br>      JOB_VAR: v | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-003 | core-concepts/variables-secrets-context-expressions | env变量 | env(step级) | 变量定义 | ${{env.VAR}} | step内env定义STEP_VAR | 该step可读$STEP_VAR | steps:<br>  - env:<br>      STEP_VAR: v | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-004 | core-concepts/variables-secrets-context-expressions | env变量 | env优先级step>job>workflow | 优先级 | ${{env.mascot}} | 三级同名mascot覆盖 | step级覆盖job级覆盖workflow级 | env:<br>  mascot: Mona<br>jobs:<br>  j:<br>    env:<br>      mascot: Tux<br>    steps:<br>      - env:<br>          mascot: Step | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-005 | core-concepts/variables-secrets-context-expressions | vars变量 | vars(组织级) | 配置变量 | ${{vars.VAR}} | 组织设置定义ORG_VAR | 组织下项目可用 | if: ${{vars.USE=='true'}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-006 | core-concepts/variables-secrets-context-expressions | vars变量 | vars(项目级) | 配置变量 | ${{vars.VAR}} | 项目设置定义PROJ_VAR | 仅当前项目可用 | run: echo ${{vars.PROJ_VAR}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-007 | core-concepts/variables-secrets-context-expressions | vars变量 | vars覆盖 | 优先级 | ${{vars.VAR}} | 项目级覆盖组织级 | 取项目级值 | run: echo ${{vars.DUP}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-008 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets(组织级) | 密钥 | ${{secrets.NAME}} | 组织设置定义SECRET_ORG | 组织下项目可用 | env:<br>  T: ${{secrets.SECRET_ORG}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-009 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets(项目级) | 密钥 | ${{secrets.NAME}} | 项目设置定义SECRET_PROJ | 仅当前项目可用 | env:<br>  K: ${{secrets.SECRET_PROJ}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-010 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets(环境级) | 密钥 | ${{secrets.NAME}} | 绑定environment的secrets | 仅job.environment匹配时可用 | jobs:<br>  d:<br>    environment: prod<br>    env:<br>      K: ${{secrets.PROD_KEY}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | FAIL | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-011 | core-concepts/variables-secrets-context-expressions | secrets变量 | secrets日志脱敏 | 安全 | ${{secrets.NAME}} | echo secrets值到日志 | 日志中替换为*** | run: echo "${{secrets.T}}" | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-012 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs(workflow_dispatch) | 输入 | ${{inputs.NAME}} | workflow_dispatch定义build_id | 手动触发时取传入值 | on:<br>  workflow_dispatch:<br>    inputs:<br>      build_id:<br>        required: true | workflow_dispatch |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-013 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs(workflow_call) | 输入 | ${{inputs.NAME}} | workflow_call定义deploy_target | 被调用时取传参 | on:<br>  workflow_call:<br>    inputs:<br>      deploy_target:<br>        required: true | workflow_call |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-014 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs仅支持string | 类型约束 | ${{inputs.NAME}} | inputs type只能string | 非string应报错 | inputs:<br>  n:<br>    type: string | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-015 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs default | 输入 | ${{inputs.NAME}} | inputs定义default | 未传参取default | inputs:<br>  env:<br>    default: dev | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(inputs default值仅在workflow_dispatch未传参时生效,无法从shell内部断言),仅验文档约束 | S6 | chaoran |  |

| TC-016 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs required校验 | 输入 | ${{inputs.NAME}} | required=true未传参 | 触发失败/提示缺必填 | inputs:<br>  bid:<br>    required: true | workflow_dispatch |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-017 | syntax-reference/context | 上下文总览 | context:atomgit | 上下文访问 | ${{atomgit.sha}} | 访问atomgit上下文 | 返回平台与事件信息 | run: echo ${atomgit.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-018 | syntax-reference/context | 上下文总览 | context:env | 上下文访问 | ${{env.MY_VAR}} | 访问env上下文 | 返回自定义环境变量 | run: echo ${env.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-019 | syntax-reference/context | 上下文总览 | context:vars | 上下文访问 | ${{vars.DEPLOY_ENV}} | 访问vars上下文 | 返回组织/项目配置变量 | run: echo ${vars.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-A | liyanghang |  |

| TC-020 | syntax-reference/context | 上下文总览 | context:job | 上下文访问 | ${{job.status}} | 访问job上下文 | 返回当前Job信息 | run: echo ${job.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-021 | syntax-reference/context | 上下文总览 | context:jobs | 上下文访问 | ${{jobs.deploy.result}} | 访问jobs上下文 | 返回可复用工作流已运行Job结果 | run: echo ${jobs.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |

| TC-022 | syntax-reference/context | 上下文总览 | context:steps | 上下文访问 | ${{steps.build.outputs.result}} | 访问steps上下文 | 返回当前Job各步骤信息 | run: echo ${steps.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 内步骤无 id 字段，steps 上下文无可引用的条目，无法断言 | Tier-A | liyanghang |  |

| TC-023 | syntax-reference/context | 上下文总览 | context:runner | 上下文访问 | ${{runner.os}} | 访问runner上下文 | 返回Runner执行环境 | run: echo ${runner.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |

| TC-024 | syntax-reference/context | 上下文总览 | context:secrets | 上下文访问 | ${{secrets.DEPLOY_TOKEN}} | 访问secrets上下文 | 返回加密密钥 | run: echo ${secrets.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-025 | syntax-reference/context | 上下文总览 | context:strategy | 上下文访问 | ${{strategy.job-index}} | 访问strategy上下文 | 返回矩阵策略信息 | run: echo ${strategy.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无 matrix 定义，strategy 上下文值无法在 shell 内部断言 | Tier-A | liyanghang |  |

| TC-026 | syntax-reference/context | 上下文总览 | context:matrix | 上下文访问 | ${{matrix.version}} | 访问matrix上下文 | 返回当前矩阵实例变量 | run: echo ${matrix.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无 matrix 定义，matrix 上下文为空，无法断言具体值 | Tier-A | liyanghang |  |

| TC-027 | syntax-reference/context | 上下文总览 | context:inputs | 上下文访问 | ${{inputs.environment}} | 访问inputs上下文 | 返回输入参数 | run: echo ${inputs.x} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |

| TC-028 | syntax-reference/context | atomgit上下文属性 | atomgit.event_name | 属性(string) | ${{atomgit.event_name}} | 读取atomgit.event_name | 返回当前触发事件名称,示例push | - run: echo ${{atomgit.event_name}} | any |  | event | run.event 或 run_detail.event | push\|pull_request\|schedule\|workflow_dispatch\|issue_comment\|workflow_call | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-029 | syntax-reference/context | atomgit上下文属性 | atomgit.sha | 属性(string) | ${{atomgit.sha}} | 读取atomgit.sha | 返回触发提交SHA,示例a1b2c3 | - run: echo ${{atomgit.sha}} | any |  | commit_id | run.commit_id 或 run_detail.commit_id | 长度=40,非空 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-030 | syntax-reference/context | atomgit上下文属性 | atomgit.ref | 属性(string) | ${{atomgit.ref}} | 读取atomgit.ref | 返回触发引用全名,示例refs/heads/main | - run: echo ${{atomgit.ref}} | any |  | branch | run.branch 或 run_detail.branch | 含 refs/heads/ 或 refs/tags/ 前缀 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-031 | syntax-reference/context | atomgit上下文属性 | atomgit.ref_name | 属性(string) | ${{atomgit.ref_name}} | 读取atomgit.ref_name | 返回触发引用短名,示例main | - run: echo ${{atomgit.ref_name}} | any |  | branch | run.branch 或 run_detail.branch | 不含 refs/ 前缀,如 main/v1 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-032 | syntax-reference/context | atomgit上下文属性 | atomgit.ref_type | 属性(string) | ${{atomgit.ref_type}} | 读取atomgit.ref_type | 返回引用类型branch/tag,示例branch | - run: echo ${{atomgit.ref_type}} | any |  | ref_type | run.ref_type 或 run_detail.ref_type | branch\|tag | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-033 | syntax-reference/context | atomgit上下文属性 | atomgit.event | 属性(object) | ${{atomgit.event}} | 读取atomgit.event | 返回事件完整payload,示例object | - run: echo ${{atomgit.event}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | syntax error near unexpected token '(' — atomgit.event 返回对象字面量，bash无法解析 | Tier-A | liyanghang |  |

| TC-034 | syntax-reference/context | atomgit上下文属性 | atomgit.workspace | 属性(string) | ${{atomgit.workspace}} | 读取atomgit.workspace | 返回Runner工作区路径,示例/home/runner | - run: echo ${{atomgit.workspace}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-035 | syntax-reference/context | atomgit上下文属性 | atomgit.action | 属性(string) | ${{atomgit.action}} | 读取atomgit.action | 返回当前Action名称,示例my-action | - run: echo ${{atomgit.action}} | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-1 | S13 | yulin |  |

| TC-036 | syntax-reference/context | atomgit上下文属性 | atomgit.token | 属性(string) | ${{atomgit.token}} | 读取atomgit.token | 返回ATOMGIT_TOKEN令牌,示例ghs_xxx | - run: echo ${{atomgit.token}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |

| TC-037 | syntax-reference/context | atomgit上下文属性 | atomgit.repository | 属性(string) | ${{atomgit.repository}} | 读取atomgit.repository | 返回仓库全名,示例owner/repo | - run: echo ${{atomgit.repository}} | any |  | repository | run.repository 或 run_detail.repository | owner/repo 形式 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-038 | syntax-reference/context | atomgit上下文属性 | atomgit.repository_owner | 属性(string) | ${{atomgit.repository_owner}} | 读取atomgit.repository_owner | 返回仓库所属组织,示例myorg | - run: echo ${{atomgit.repository_owner}} | any |  | repository_owner | run.repository_owner 或 run_detail.repository_owner | owner 名 | B API字段 | FAIL | FAIL | Tier-B | liyanghang |  |

| TC-039 | syntax-reference/context | atomgit上下文属性 | atomgit.repositoryUrl | 属性(string) | ${{atomgit.repositoryUrl}} | 读取atomgit.repositoryUrl | 返回仓库URL,示例https:// | - run: echo ${{atomgit.repositoryUrl}} | any |  | https_url | run.https_url 或 run_detail.https_url | https://gitcode.com/owner/repo 形式 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-040 | syntax-reference/context | atomgit上下文属性 | atomgit.run_id | 属性(string) | ${{atomgit.run_id}} | 读取atomgit.run_id | 返回工作流运行ID,示例12345 | - run: echo ${{atomgit.run_id}} | any |  | pipeline_run_id | run.pipeline_run_id 或 run_detail.pipeline_run_id | 非空,唯一 | B API字段 | FAIL | FAIL | Tier-B | liyanghang |  |

| TC-041 | syntax-reference/context | atomgit上下文属性 | atomgit.run_number | 属性(number) | ${{atomgit.run_number}} | 读取atomgit.run_number | 返回工作流运行编号,示例42 | - run: echo ${{atomgit.run_number}} | any |  | run_number | run.run_number 或 run_detail.run_number | 递增整数 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-042 | syntax-reference/context | atomgit上下文属性 | atomgit.run_attempt | 属性(number) | ${{atomgit.run_attempt}} | 读取atomgit.run_attempt | 返回工作流重试次数,示例1 | - run: echo ${{atomgit.run_attempt}} | any |  | run_attempt | run.run_attempt 或 run_detail.run_attempt | 重运行次数,首次=1 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-043 | syntax-reference/context | atomgit上下文属性 | atomgit.workflow | 属性(string) | ${{atomgit.workflow}} | 读取atomgit.workflow | 返回工作流名称,示例CI | - run: echo ${{atomgit.workflow}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-044 | syntax-reference/context | atomgit上下文属性 | atomgit.head_ref | 属性(string) | ${{atomgit.head_ref}} | 读取atomgit.head_ref | 返回PR源分支(仅PR),示例feature/x | - run: echo ${{atomgit.head_ref}} | any |  | head_ref | run.head_ref 或 run_detail.head_ref | PR 源分支,非 push 事件时空 | B API字段 | FAIL | FAIL | Tier-B | liyanghang |  |

| TC-045 | syntax-reference/context | atomgit上下文属性 | atomgit.base_ref | 属性(string) | ${{atomgit.base_ref}} | 读取atomgit.base_ref | 返回PR目标分支(仅PR),示例main | - run: echo ${{atomgit.base_ref}} | any |  | base_ref | run.base_ref 或 run_detail.base_ref | PR 目标分支,非 push 事件时空 | B API字段 | PASS | suite-1 | Tier-B | liyanghang |  |

| TC-046 | syntax-reference/context | atomgit上下文属性 | atomgit.server_url | 属性(string) | ${{atomgit.server_url}} | 读取atomgit.server_url | 返回平台根URL,示例https://atomgit.com | - run: echo ${{atomgit.server_url}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-047 | syntax-reference/context | atomgit上下文属性 | atomgit.api_url | 属性(string) | ${{atomgit.api_url}} | 读取atomgit.api_url | 返回API基础URL,示例https://api.atomgit.com | - run: echo ${{atomgit.api_url}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-048 | syntax-reference/context | push事件字段 | atomgit.event.ref | 事件字段 | ${{atomgit.event.ref}} | push读取event.ref | 返回推送的完整ref | - run: echo ${{atomgit.event.ref}} | push |  | branch | run.branch 或 run_detail.branch | push 事件时=branch,非空 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-049 | syntax-reference/context | push事件字段 | atomgit.event.before | 事件字段 | ${{atomgit.event.before}} | push读取event.before | 返回推送前SHA | - run: echo ${{atomgit.event.before}} | push |  | before | run.before 或 run_detail.before | push 事件时=前一 commit SHA,非空 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-050 | syntax-reference/context | push事件字段 | atomgit.event.after | 事件字段 | ${{atomgit.event.after}} | push读取event.after | 返回推送后SHA | - run: echo ${{atomgit.event.after}} | push |  | after | run.after 或 run_detail.after | push 事件时=当前 commit SHA,非空 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-051 | syntax-reference/context | push事件字段 | atomgit.event.commits | 事件字段 | ${{atomgit.event.commits}} | push读取event.commits | 返回提交列表数组 | - run: echo ${{atomgit.event.commits}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-052 | syntax-reference/context | push事件字段 | atomgit.event.commits[].id | 事件字段 | ${{atomgit.event.commits[].id}} | push读取event.commits[].id | 返回单提交SHA | - run: echo ${{atomgit.event.commits[].id}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-053 | syntax-reference/context | push事件字段 | atomgit.event.commits[].message | 事件字段 | ${{atomgit.event.commits[].message}} | push读取event.commits[].message | 返回提交消息 | - run: echo ${{atomgit.event.commits[].message}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-054 | syntax-reference/context | push事件字段 | atomgit.event.commits[].author | 事件字段 | ${{atomgit.event.commits[].author}} | push读取event.commits[].author | 返回提交作者 | - run: echo ${{atomgit.event.commits[].author}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-055 | syntax-reference/context | push事件字段 | atomgit.event.commits[].added | 事件字段 | ${{atomgit.event.commits[].added}} | push读取event.commits[].added | 返回新增文件列表 | - run: echo ${{atomgit.event.commits[].added}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-056 | syntax-reference/context | push事件字段 | atomgit.event.commits[].modified | 事件字段 | ${{atomgit.event.commits[].modified}} | push读取event.commits[].modified | 返回修改文件列表 | - run: echo ${{atomgit.event.commits[].modified}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-057 | syntax-reference/context | push事件字段 | atomgit.event.commits[].removed | 事件字段 | ${{atomgit.event.commits[].removed}} | push读取event.commits[].removed | 返回删除文件列表 | - run: echo ${{atomgit.event.commits[].removed}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-058 | syntax-reference/context | push事件字段 | atomgit.event.base_ref | 事件字段 | ${{atomgit.event.base_ref}} | push读取event.base_ref | 返回基础ref | - run: echo ${{atomgit.event.base_ref}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-059 | syntax-reference/context | push事件字段 | atomgit.event.created | 事件字段 | ${{atomgit.event.created}} | push读取event.created | 返回是否新创建ref | - run: echo ${{atomgit.event.created}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-060 | syntax-reference/context | push事件字段 | atomgit.event.deleted | 事件字段 | ${{atomgit.event.deleted}} | push读取event.deleted | 返回是否删除ref | - run: echo ${{atomgit.event.deleted}} | push |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-061 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.number | 事件字段 | ${{atomgit.event.pull_request.number}} | PR读取event.pull_request.number | 返回PR编号 | - run: echo ${{atomgit.event.pull_request.number}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-062 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.title | 事件字段 | ${{atomgit.event.pull_request.title}} | PR读取event.pull_request.title | 返回PR标题 | - run: echo ${{atomgit.event.pull_request.title}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-063 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.body | 事件字段 | ${{atomgit.event.pull_request.body}} | PR读取event.pull_request.body | 返回PR描述 | - run: echo ${{atomgit.event.pull_request.body}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-064 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.state | 事件字段 | ${{atomgit.event.pull_request.state}} | PR读取event.pull_request.state | 返回PR状态open/closed | - run: echo ${{atomgit.event.pull_request.state}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-065 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.user.login | 事件字段 | ${{atomgit.event.pull_request.user.login}} | PR读取event.pull_request.user.login | 返回PR创建者 | - run: echo ${{atomgit.event.pull_request.user.login}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-066 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.head.ref | 事件字段 | ${{atomgit.event.pull_request.head.ref}} | PR读取event.pull_request.head.ref | 返回PR源分支名 | - run: echo ${{atomgit.event.pull_request.head.ref}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-067 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.head.sha | 事件字段 | ${{atomgit.event.pull_request.head.sha}} | PR读取event.pull_request.head.sha | 返回PR源分支最新SHA | - run: echo ${{atomgit.event.pull_request.head.sha}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-068 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.head.repo.full_name | 事件字段 | ${{atomgit.event.pull_request.head.repo.full_name}} | PR读取event.pull_request.head.repo.full_name | 返回PR源仓库全名 | - run: echo ${{atomgit.event.pull_request.head.repo.full_name}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-069 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.base.ref | 事件字段 | ${{atomgit.event.pull_request.base.ref}} | PR读取event.pull_request.base.ref | 返回PR目标分支名 | - run: echo ${{atomgit.event.pull_request.base.ref}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-070 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.base.repo.full_name | 事件字段 | ${{atomgit.event.pull_request.base.repo.full_name}} | PR读取event.pull_request.base.repo.full_name | 返回PR目标仓库全名 | - run: echo ${{atomgit.event.pull_request.base.repo.full_name}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-071 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.labels | 事件字段 | ${{atomgit.event.pull_request.labels}} | PR读取event.pull_request.labels | 返回PR标签列表 | - run: echo ${{atomgit.event.pull_request.labels}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-072 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.merged | 事件字段 | ${{atomgit.event.pull_request.merged}} | PR读取event.pull_request.merged | 返回PR是否已合并 | - run: echo ${{atomgit.event.pull_request.merged}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-073 | syntax-reference/context | pull_request事件字段 | atomgit.event.pull_request.draft | 事件字段 | ${{atomgit.event.pull_request.draft}} | PR读取event.pull_request.draft | 返回PR是否Draft | - run: echo ${{atomgit.event.pull_request.draft}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-074 | syntax-reference/context | pull_request事件字段 | atomgit.event.action | 事件字段 | ${{atomgit.event.action}} | PR读取event.action | 返回PR事件动作类型 | - run: echo ${{atomgit.event.action}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 非pull_request事件 | S14 | chaoran |  |

| TC-075 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.id | 事件字段 | ${{atomgit.event.comment.id}} | issue_comment读取event.comment.id | 返回评论ID | - run: echo ${{atomgit.event.comment.id}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-076 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.body | 事件字段 | ${{atomgit.event.comment.body}} | issue_comment读取event.comment.body | 返回评论内容 | - run: echo ${{atomgit.event.comment.body}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-077 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.user.login | 事件字段 | ${{atomgit.event.comment.user.login}} | issue_comment读取event.comment.user.login | 返回评论者 | - run: echo ${{atomgit.event.comment.user.login}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-078 | syntax-reference/context | issue_comment事件字段 | atomgit.event.comment.created_at | 事件字段 | ${{atomgit.event.comment.created_at}} | issue_comment读取event.comment.created_at | 返回评论创建时间 | - run: echo ${{atomgit.event.comment.created_at}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-079 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.number | 事件字段 | ${{atomgit.event.issue.number}} | issue_comment读取event.issue.number | 返回Issue编号 | - run: echo ${{atomgit.event.issue.number}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-080 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.title | 事件字段 | ${{atomgit.event.issue.title}} | issue_comment读取event.issue.title | 返回Issue标题 | - run: echo ${{atomgit.event.issue.title}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-081 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.state | 事件字段 | ${{atomgit.event.issue.state}} | issue_comment读取event.issue.state | 返回Issue状态 | - run: echo ${{atomgit.event.issue.state}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-082 | syntax-reference/context | issue_comment事件字段 | atomgit.event.issue.pull_request | 事件字段 | ${{atomgit.event.issue.pull_request}} | issue_comment读取event.issue.pull_request | 返回是否PR评论 | - run: echo ${{atomgit.event.issue.pull_request}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-083 | syntax-reference/context | issue_comment事件字段 | atomgit.event.action | 事件字段 | ${{atomgit.event.action}} | issue_comment读取event.action | 返回动作类型 | - run: echo ${{atomgit.event.action}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 非issue_comment事件 | S15 | chaoran |  |

| TC-084 | syntax-reference/context | workflow_dispatch事件字段 | atomgit.event.inputs | 事件字段 | ${{atomgit.event.inputs}} | 读取手动触发输入参数对象 | 返回inputs对象 | - run: echo ${{atomgit.event.inputs}} | workflow_dispatch |  | inputs | run.inputs 或 run_detail.inputs | workflow_dispatch 事件时含触发参数 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-085 | syntax-reference/context | schedule事件字段 | atomgit.event.schedule | 事件字段 | ${{atomgit.event.schedule}} | 读取cron表达式列表 | 返回schedule数组 | - run: echo ${{atomgit.event.schedule}} | schedule |  | schedule | run.schedule 或 run_detail.schedule | schedule 事件时含 cron 表达式 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-086 | syntax-reference/context | env上下文 | env.first_name | 属性 | ${{env.first_name}} | 读取env上下文first_name | 返回Mona | - run: echo ${{env.first_name}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-087 | syntax-reference/context | env上下文 | env.super_duper_var | 属性 | ${{env.super_duper_var}} | 读取env上下文 | 返回totally_awesome | - run: echo ${{env.super_duper_var}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-088 | syntax-reference/context | job上下文 | job.status | 属性 | ${{job.status}} | 读取Job状态 | 返回success/failure/cancelled | - if: ${{job.status=='success'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-089 | syntax-reference/context | job上下文 | job.container | 属性 | ${{job.container}} | 读取自定义构建环境 | 返回container Object | - run: echo ${{job.container}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 未定义 container，job.container 为空对象，无法断言具体值 | Tier-A | liyanghang |  |

| TC-090 | syntax-reference/context | steps上下文 | steps.checkout.outputs | 属性 | ${{steps.checkout.outputs}} | 读取steps.checkout.outputs | 返回步骤输出对象 | - run: echo ${{steps.checkout.outputs}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-091 | syntax-reference/context | steps上下文 | steps.checkout.outcome | 属性 | ${{steps.checkout.outcome}} | 读取steps.checkout.outcome | 返回apply continue-on-error前结果 | - run: echo ${{steps.checkout.outcome}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-092 | syntax-reference/context | steps上下文 | steps.checkout.conclusion | 属性 | ${{steps.checkout.conclusion}} | 读取steps.checkout.conclusion | 返回apply后结果 | - run: echo ${{steps.checkout.conclusion}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-093 | syntax-reference/context | steps上下文 | steps.generate_number.outputs.random_number | 属性 | ${{steps.generate_number.outputs.random_number}} | 读取steps.generate_number.outputs.random_number | 返回步骤单输出值 | - run: echo ${{steps.generate_number.outputs.random_number}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-094 | syntax-reference/context | runner上下文 | runner.os | 属性 | ${{runner.os}} | 读取runner.os | 返回Linux/Windows/macOS | - run: echo ${{runner.os}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |

| TC-095 | syntax-reference/context | runner上下文 | runner.arch | 属性 | ${{runner.arch}} | 读取runner.arch | 返回X64/ARM/ARM64 | - run: echo ${{runner.arch}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=x86_64 | Tier-A | liyanghang |  |

| TC-096 | syntax-reference/context | runner上下文 | runner.name | 属性 | ${{runner.name}} | 读取runner.name | 返回Runner名称 | - run: echo ${{runner.name}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-097 | syntax-reference/context | runner上下文 | runner.temp | 属性 | ${{runner.temp}} | 读取runner.temp | 返回Runner临时目录 | - run: echo ${{runner.temp}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-098 | syntax-reference/context | runner上下文 | runner.tool_cache | 属性 | ${{runner.tool_cache}} | 读取runner.tool_cache | 返回Runner工具缓存目录 | - run: echo ${{runner.tool_cache}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-099 | syntax-reference/context | runner上下文 | runner.debug | 属性 | ${{runner.debug}} | 读取runner.debug | 返回是否debug | - run: echo ${{runner.debug}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |

| TC-100 | syntax-reference/context | secrets上下文 | secrets.atomgit_token | 属性 | ${{secrets.atomgit_token}} | 读取atomgit_token | 返回***脱敏 | env:<br>  T: ${{secrets.atomgit_token}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-101 | syntax-reference/context | secrets上下文 | secrets.NPM_TOKEN | 属性 | ${{secrets.NPM_TOKEN}} | 读取NPM_TOKEN | 返回***脱敏 | env:<br>  T: ${{secrets.NPM_TOKEN}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-102 | syntax-reference/context | secrets上下文 | secrets.SUPERSECRET | 属性 | ${{secrets.SUPERSECRET}} | 读取SUPERSECRET | 返回***脱敏 | env:<br>  T: ${{secrets.SUPERSECRET}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-103 | syntax-reference/context | matrix上下文 | matrix.os | 属性 | ${{matrix.os}} | 读取矩阵os值 | 返回ubuntu-latest | - run: echo ${{matrix.os}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 当前 job 无 matrix 定义，matrix.os 为空，无法断言 | Tier-A | liyanghang |  |

| TC-104 | syntax-reference/context | matrix上下文 | matrix.node | 属性 | ${{matrix.node}} | 读取矩阵node值 | 返回16 | - run: echo ${{matrix.node}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 当前 job 无 matrix 定义，matrix.node 为空，无法断言 | Tier-A | liyanghang |  |

| TC-105 | syntax-reference/context | 上下文可用性表 | atomgit@workflow级别 | 可用性 | ${{atomgit.x}} | 在workflow级别使用atomgit上下文 | 应可用 | # workflow级别<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-106 | syntax-reference/context | 上下文可用性表 | atomgit@job级别 | 可用性 | ${{atomgit.x}} | 在job级别使用atomgit上下文 | 应可用 | # job级别<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-107 | syntax-reference/context | 上下文可用性表 | atomgit@step级别 | 可用性 | ${{atomgit.x}} | 在step级别使用atomgit上下文 | 应可用 | # step级别<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-108 | syntax-reference/context | 上下文可用性表 | atomgit@条件表达式(if) | 可用性 | ${{atomgit.x}} | 在条件表达式(if)使用atomgit上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-109 | syntax-reference/context | 上下文可用性表 | atomgit@Action中 | 可用性 | ${{atomgit.x}} | 在Action中使用atomgit上下文 | 应可用 | # Action中<br>- run: echo ${{atomgit.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-110 | syntax-reference/context | 上下文可用性表 | env@workflow级别 | 可用性 | ${{env.x}} | 在workflow级别使用env上下文 | 应可用 | # workflow级别<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-111 | syntax-reference/context | 上下文可用性表 | env@job级别 | 可用性 | ${{env.x}} | 在job级别使用env上下文 | 应可用 | # job级别<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-112 | syntax-reference/context | 上下文可用性表 | env@step级别 | 可用性 | ${{env.x}} | 在step级别使用env上下文 | 应可用 | # step级别<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-113 | syntax-reference/context | 上下文可用性表 | env@条件表达式(if) | 可用性 | ${{env.x}} | 在条件表达式(if)使用env上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-114 | syntax-reference/context | 上下文可用性表 | env@Action中 | 可用性 | ${{env.x}} | 在Action中使用env上下文 | 应可用 | # Action中<br>- run: echo ${{env.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-115 | syntax-reference/context | 上下文可用性表 | vars@workflow级别 | 可用性 | ${{vars.x}} | 在workflow级别使用vars上下文 | 应可用 | # workflow级别<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |

| TC-116 | syntax-reference/context | 上下文可用性表 | vars@job级别 | 可用性 | ${{vars.x}} | 在job级别使用vars上下文 | 应可用 | # job级别<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |

| TC-117 | syntax-reference/context | 上下文可用性表 | vars@step级别 | 可用性 | ${{vars.x}} | 在step级别使用vars上下文 | 应可用 | # step级别<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |

| TC-118 | syntax-reference/context | 上下文可用性表 | vars@条件表达式(if) | 可用性 | ${{vars.x}} | 在条件表达式(if)使用vars上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |

| TC-119 | syntax-reference/context | 上下文可用性表 | vars@Action中 | 可用性 | ${{vars.x}} | 在Action中使用vars上下文 | 应可用 | # Action中<br>- run: echo ${{vars.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: GitCode 不支持 vars 上下文，无法从 shell 内部读取并断言 | Tier-D | liyanghang |  |

| TC-120 | syntax-reference/context | 上下文可用性表 | job@workflow级别 | 可用性 | ${{job.x}} | 在workflow级别使用job上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |

| TC-121 | syntax-reference/context | 上下文可用性表 | job@job级别 | 可用性 | ${{job.x}} | 在job级别使用job上下文 | 应可用 | # job级别<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-122 | syntax-reference/context | 上下文可用性表 | job@step级别 | 可用性 | ${{job.x}} | 在step级别使用job上下文 | 应可用 | # step级别<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-123 | syntax-reference/context | 上下文可用性表 | job@条件表达式(if) | 可用性 | ${{job.x}} | 在条件表达式(if)使用job上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-124 | syntax-reference/context | 上下文可用性表 | job@Action中 | 可用性 | ${{job.x}} | 在Action中使用job上下文 | 应可用 | # Action中<br>- run: echo ${{job.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-125 | syntax-reference/context | 上下文可用性表 | jobs@workflow级别(调用方) | 可用性 | ${{jobs.x}} | 在workflow级别(调用方)使用jobs上下文 | 应可用 | # workflow级别(调用方)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |

| TC-126 | syntax-reference/context | 上下文可用性表 | jobs@job级别(调用方) | 可用性 | ${{jobs.x}} | 在job级别(调用方)使用jobs上下文 | 应可用 | # job级别(调用方)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |

| TC-127 | syntax-reference/context | 上下文可用性表 | jobs@step级别(调用方) | 可用性 | ${{jobs.x}} | 在step级别(调用方)使用jobs上下文 | 应可用 | # step级别(调用方)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |

| TC-128 | syntax-reference/context | 上下文可用性表 | jobs@条件表达式(if) | 可用性 | ${{jobs.x}} | 在条件表达式(if)使用jobs上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: jobs 上下文仅在 workflow_call 调用方可用，当前工作流无 workflow_call 触发 | Tier-A | liyanghang |  |

| TC-129 | syntax-reference/context | 上下文可用性表 | jobs@Action中 | 可用性 | ${{jobs.x}} | 在Action中使用jobs上下文 | 不可用/报错 | # Action中<br>- run: echo ${{jobs.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（Action 中不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |

| TC-130 | syntax-reference/context | 上下文可用性表 | steps@workflow级别 | 可用性 | ${{steps.x}} | 在workflow级别使用steps上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |

| TC-131 | syntax-reference/context | 上下文可用性表 | steps@job级别(步骤后) | 可用性 | ${{steps.x}} | 在job级别(步骤后)使用steps上下文 | 应可用 | # job级别(步骤后)<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |

| TC-132 | syntax-reference/context | 上下文可用性表 | steps@step级别(当前步骤后) | 可用性 | ${{steps.x}} | 在step级别(当前步骤后)使用steps上下文 | 应可用 | # step级别(当前步骤后)<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |

| TC-133 | syntax-reference/context | 上下文可用性表 | steps@条件表达式(if) | 可用性 | ${{steps.x}} | 在条件表达式(if)使用steps上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |

| TC-134 | syntax-reference/context | 上下文可用性表 | steps@Action中 | 可用性 | ${{steps.x}} | 在Action中使用steps上下文 | 应可用 | # Action中<br>- run: echo ${{steps.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前 job 无带 id 的前置步骤，steps 上下文无可断言的条目 | Tier-A | liyanghang |  |

| TC-135 | syntax-reference/context | 上下文可用性表 | runner@workflow级别 | 可用性 | ${{runner.x}} | 在workflow级别使用runner上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |

| TC-136 | syntax-reference/context | 上下文可用性表 | runner@job级别 | 可用性 | ${{runner.x}} | 在job级别使用runner上下文 | 应可用 | # job级别<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |

| TC-137 | syntax-reference/context | 上下文可用性表 | runner@step级别 | 可用性 | ${{runner.x}} | 在step级别使用runner上下文 | 应可用 | # step级别<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |

| TC-138 | syntax-reference/context | 上下文可用性表 | runner@条件表达式(if) | 可用性 | ${{runner.x}} | 在条件表达式(if)使用runner上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |

| TC-139 | syntax-reference/context | 上下文可用性表 | runner@Action中 | 可用性 | ${{runner.x}} | 在Action中使用runner上下文 | 应可用 | # Action中<br>- run: echo ${{runner.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 非法值=linux | Tier-A | liyanghang |  |

| TC-140 | syntax-reference/context | 上下文可用性表 | secrets@workflow级别 | 可用性 | ${{secrets.x}} | 在workflow级别使用secrets上下文 | 应可用 | # workflow级别<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-141 | syntax-reference/context | 上下文可用性表 | secrets@job级别 | 可用性 | ${{secrets.x}} | 在job级别使用secrets上下文 | 应可用 | # job级别<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-142 | syntax-reference/context | 上下文可用性表 | secrets@step级别 | 可用性 | ${{secrets.x}} | 在step级别使用secrets上下文 | 应可用 | # step级别<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-143 | syntax-reference/context | 上下文可用性表 | secrets@条件表达式(if) | 可用性 | ${{secrets.x}} | 在条件表达式(if)使用secrets上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-144 | syntax-reference/context | 上下文可用性表 | secrets@Action中 | 可用性 | ${{secrets.x}} | 在Action中使用secrets上下文 | 应可用 | # Action中<br>- run: echo ${{secrets.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-145 | syntax-reference/context | 上下文可用性表 | strategy@workflow级别 | 可用性 | ${{strategy.x}} | 在workflow级别使用strategy上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 平台侧校验行为（workflow 级别不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |

| TC-146 | syntax-reference/context | 上下文可用性表 | strategy@job级别 | 可用性 | ${{strategy.x}} | 在job级别使用strategy上下文 | 应可用 | # job级别<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-147 | syntax-reference/context | 上下文可用性表 | strategy@step级别 | 可用性 | ${{strategy.x}} | 在step级别使用strategy上下文 | 应可用 | # step级别<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-148 | syntax-reference/context | 上下文可用性表 | strategy@条件表达式(if) | 可用性 | ${{strategy.x}} | 在条件表达式(if)使用strategy上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |

| TC-149 | syntax-reference/context | 上下文可用性表 | strategy@Action中 | 可用性 | ${{strategy.x}} | 在Action中使用strategy上下文 | 不可用/报错 | # Action中<br>- run: echo ${{strategy.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |

| TC-150 | syntax-reference/context | 上下文可用性表 | matrix@workflow级别 | 可用性 | ${{matrix.x}} | 在workflow级别使用matrix上下文 | 不可用/报错 | # workflow级别<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |

| TC-151 | syntax-reference/context | 上下文可用性表 | matrix@job级别 | 可用性 | ${{matrix.x}} | 在job级别使用matrix上下文 | 应可用 | # job级别<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-152 | syntax-reference/context | 上下文可用性表 | matrix@step级别 | 可用性 | ${{matrix.x}} | 在step级别使用matrix上下文 | 应可用 | # step级别<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-153 | syntax-reference/context | 上下文可用性表 | matrix@条件表达式(if) | 可用性 | ${{matrix.x}} | 在条件表达式(if)使用matrix上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | suite-1 | Tier-D | liyanghang |  |

| TC-154 | syntax-reference/context | 上下文可用性表 | matrix@Action中 | 可用性 | ${{matrix.x}} | 在Action中使用matrix上下文 | 不可用/报错 | # Action中<br>- run: echo ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | SKIP: 平台侧校验行为（Action 中不可用/报错），无法从 shell 内部验证平台拒绝解析 | Tier-D | liyanghang |  |

| TC-155 | syntax-reference/context | 上下文可用性表 | inputs@workflow级别 | 可用性 | ${{inputs.x}} | 在workflow级别使用inputs上下文 | 应可用 | # workflow级别<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-D | liyanghang |  |

| TC-156 | syntax-reference/context | 上下文可用性表 | inputs@job级别 | 可用性 | ${{inputs.x}} | 在job级别使用inputs上下文 | 应可用 | # job级别<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |

| TC-157 | syntax-reference/context | 上下文可用性表 | inputs@step级别 | 可用性 | ${{inputs.x}} | 在step级别使用inputs上下文 | 应可用 | # step级别<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |

| TC-158 | syntax-reference/context | 上下文可用性表 | inputs@条件表达式(if) | 可用性 | ${{inputs.x}} | 在条件表达式(if)使用inputs上下文 | 应可用 | # 条件表达式(if)<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |

| TC-159 | syntax-reference/context | 上下文可用性表 | inputs@Action中 | 可用性 | ${{inputs.x}} | 在Action中使用inputs上下文 | 应可用 | # Action中<br>- run: echo ${{inputs.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 当前工作流未定义 workflow_dispatch inputs，inputs 上下文为空，无法断言 | Tier-A | liyanghang |  |

| TC-160 | syntax-reference/expressions | 字面量 | 布尔true | 布尔 | ${{true}} | 使用字面量布尔true | 返回true | - if: ${{true}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-161 | syntax-reference/expressions | 字面量 | 布尔false | 布尔 | ${{false}} | 使用字面量布尔false | 返回false | - if: ${{false}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-162 | syntax-reference/expressions | 字面量 | null | null | ${{null}} | 使用字面量null | 返回null | - if: ${{null}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-163 | syntax-reference/expressions | 字面量 | 整数 | 数字 | ${{42}} | 使用字面量整数 | 返回42 | - if: ${{42}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 期望42,实际=42.0 | Tier-A | liyanghang |  |

| TC-164 | syntax-reference/expressions | 字面量 | 浮点 | 数字 | ${{3.14}} | 使用字面量浮点 | 返回3.14 | - if: ${{3.14}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-165 | syntax-reference/expressions | 字面量 | 字符串 | 字符串 | ${{'hello'}} | 使用字面量字符串 | 返回hello | - if: ${{'hello'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-166 | syntax-reference/expressions | 运算符 |  | 运算符 | ${{atomgit.ref=='refs/heads/main'}} | 使用运算符== | 分支等于main时true | - if: ${{atomgit.ref=='refs/heads/main'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-167 | syntax-reference/expressions | 运算符 | != | 运算符 | ${{atomgit.event_name!='schedule'}} | 使用运算符!= | 非定时事件true | - if: ${{atomgit.event_name!='schedule'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-168 | syntax-reference/expressions | 运算符 | ! | 运算符 | ${{!success}} | 使用运算符! | 前置非成功时true | - if: ${{!success}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-169 | syntax-reference/expressions | 运算符 | && | 运算符 | ${{success && atomgit.ref=='refs/heads/main'}} | 使用运算符&& | 成功且main时true | - if: ${{success && atomgit.ref=='refs/heads/main'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-170 | syntax-reference/expressions | 运算符 | \|\| | 运算符 | ${{failed \|\| cancelled}} | 使用运算符\|\| | 失败或取消时true | - if: ${{failed \|\| cancelled}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-171 | syntax-reference/expressions | 运算符 | > | 运算符 | ${{matrix.version>12}} | 使用运算符> | version>12时true | - if: ${{matrix.version>12}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-172 | syntax-reference/expressions | 运算符 | < | 运算符 | ${{matrix.version<14}} | 使用运算符< | version<14时true | - if: ${{matrix.version<14}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-173 | syntax-reference/expressions | 运算符 | >= | 运算符 | ${{strategy.job-total>=3}} | 使用运算符>= | job总数>=3时true | - if: ${{strategy.job-total>=3}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-174 | syntax-reference/expressions | 运算符 | <= | 运算符 | ${{inputs.count<=10}} | 使用运算符<= | count<=10时true | - if: ${{inputs.count<=10}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-175 | syntax-reference/expressions | 运算符优先级 | !>比较>==>&&>\|\| | 优先级 | ${{!a && b \|\| c}} | 验证运算符优先级 | 按!→比较→==→&&→\|\|求值 | - if: ${{!cancelled && success \|\| failed}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-176 | syntax-reference/expressions | 函数 | success | 函数 | ${{success}} | 调用函数success | 所有前置成功时true | - run: echo ${{success}} | any |  | status | run.status | SUCCESS,成功 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |

| TC-177 | syntax-reference/expressions | 函数 | always | 函数 | ${{always}} | 调用函数always | 任何情况true | - run: echo ${{always}} | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |

| TC-178 | syntax-reference/expressions | 函数 | cancelled | 函数 | ${{cancelled}} | 调用函数cancelled | 工作流取消时true | - run: echo ${{cancelled}} | any |  | status | run.status | CANCELLED,被取消 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |

| TC-179 | syntax-reference/expressions | 函数 | failed | 函数 | ${{failed}} | 调用函数failed | 任一前置失败时true | - run: echo ${{failed}} | any |  | status | run.status | FAILED,触发失败传播 | B API字段 | PASS | suite-2 | Tier-B | liyanghang |  |

| TC-180 | syntax-reference/expressions | 函数 | contains | 函数 | ${{contains(atomgit.ref,'release')}} | 调用函数contains | ref含release时true | - run: echo ${{contains(atomgit.ref,'release')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-181 | syntax-reference/expressions | 函数 | startsWith | 函数 | ${{startsWith(atomgit.ref,'refs/tags/')}} | 调用函数startsWith | ref以refs/tags/开头时true | - run: echo ${{startsWith(atomgit.ref,'refs/tags/')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-182 | syntax-reference/expressions | 函数 | endsWith | 函数 | ${{endsWith(atomgit.ref_name,'.rc')}} | 调用函数endsWith | ref_name以.rc结尾时true | - run: echo ${{endsWith(atomgit.ref_name,'.rc')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-183 | syntax-reference/expressions | 函数 | format | 函数 | ${{format('Hello {0}!',name)}} | 调用函数format | 返回Hello <name>! | - run: echo ${{format('Hello {0}!',name)}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-184 | syntax-reference/expressions | 函数 | substring | 函数 | ${{substring(atomgit.sha,0,7)}} | 调用函数substring | 返回sha前7位 | - run: echo ${{substring(atomgit.sha,0,7)}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-185 | syntax-reference/expressions | 函数 | replace | 函数 | ${{replace(atomgit.ref,'refs/heads/','')}} | 调用函数replace | 返回main去掉前缀 | - run: echo ${{replace(atomgit.ref,'refs/heads/','')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-186 | syntax-reference/expressions | 函数 | hashFiles | 函数 | ${{hashFiles('src/**','package.json')}} | 调用函数hashFiles | 返回组合SHA256 | - run: echo ${{hashFiles('src/**','package.json')}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-187 | syntax-reference/expressions | 函数 | toJson | 函数 | ${{toJson(atomgit.event)}} | 调用函数toJson | 返回event的JSON字符串 | - run: echo ${{toJson(atomgit.event)}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-188 | syntax-reference/expressions | 表达式示例 | 仅main且成功时执行 | 表达式示例 | - | 验证示例:仅main且成功时执行 | Deploy to production | if: ${{success && atomgit.ref=='refs/heads/main'}} | any | 组合条件 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: if条件只能通过步骤是否执行来观察,无法在run块内验证 | Tier-A | liyanghang |  |

| TC-189 | syntax-reference/expressions | 表达式示例 | 失败或取消仍执行清理 | 表达式示例 | - | 验证示例:失败或取消仍执行清理 | Cleanup resources | if: ${{always}} | any | always | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 | SKIP: always()的效果只能通过步骤是否在失败时执行来观察,无法在run块内验证 | Tier-A | liyanghang |  |

| TC-190 | syntax-reference/expressions | 表达式示例 | 仅失败时通知 | 表达式示例 | - | 验证示例:仅失败时通知 | Send failure notification | if: ${{failed}} | any | failed | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 | SKIP: failure()条件只能通过步骤是否在前置失败时执行来观察,无法在run块内验证 | Tier-A | liyanghang |  |

| TC-191 | syntax-reference/expressions | 表达式示例 | 标签推送时构建 | 表达式示例 | - | 验证示例:标签推送时构建 | Build release | if: ${{startsWith(atomgit.ref,'refs/tags/')}} | any | startsWith | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: startsWith if条件只能通过步骤在tag推送时是否执行来观察,无法在run块内验证 | S5 | chaoran |  |

| TC-192 | syntax-reference/expressions | 表达式示例 | format拼接字符串 | 表达式示例 | - | 验证示例:format拼接字符串 | echo $IMAGE_TAG | IMAGE_TAG: ${{format('{0}:{1}','myimage',atomgit.sha)}} | any | format | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-193 | syntax-reference/variables | inputs type规格 | inputs.type=string | 类型约束 | ${{inputs.NAME}} | inputs仅支持string | 定义type:string正常 | inputs:<br>  x:<br>    type: string | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-194 | syntax-reference/variables | 变量优先级 | vars项目级>组织级 | 优先级 | ${{vars.VAR}} | 同名vars项目级覆盖组织级 | 取项目级值 | run: echo ${{vars.DUP}} | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(vars需在AtomGit平台界面同时配置项目级和组织级同名变量才可验证覆盖规则),仅验语法声明 | S13 | yulin |  |

| TC-195 | syntax-reference/variables | 变量优先级 | secrets项目级>组织级 | 优先级 | ${{secrets.NAME}} | 同名secrets项目级覆盖组织级 | 取项目级值 | run: echo ${{secrets.DUP}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |

| TC-196 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_TOKEN | 系统变量 | $ATOMGIT_TOKEN | 读取系统变量ATOMGIT_TOKEN | 返回工作流认证令牌(自动生成),示例ghs_xxx | - run: echo $ATOMGIT_TOKEN | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | Tier-A | liyanghang |  |

| TC-197 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_SHA | 系统变量 | $ATOMGIT_SHA | 读取系统变量ATOMGIT_SHA | 返回触发提交SHA,示例a1b2c3 | - run: echo $ATOMGIT_SHA | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-198 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REF | 系统变量 | $ATOMGIT_REF | 读取系统变量ATOMGIT_REF | 返回触发引用全名,示例refs/heads/main | - run: echo $ATOMGIT_REF | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-199 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REF_NAME | 系统变量 | $ATOMGIT_REF_NAME | 读取系统变量ATOMGIT_REF_NAME | 返回触发引用短名,示例main | - run: echo $ATOMGIT_REF_NAME | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-200 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REF_TYPE | 系统变量 | $ATOMGIT_REF_TYPE | 读取系统变量ATOMGIT_REF_TYPE | 返回引用类型,示例branch | - run: echo $ATOMGIT_REF_TYPE | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-201 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_EVENT_NAME | 系统变量 | $ATOMGIT_EVENT_NAME | 读取系统变量ATOMGIT_EVENT_NAME | 返回触发事件名称,示例push | - run: echo $ATOMGIT_EVENT_NAME | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-202 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_EVENT_PATH | 系统变量 | $ATOMGIT_EVENT_PATH | 读取系统变量ATOMGIT_EVENT_PATH | 返回事件payload JSON文件路径,示例/home/runner/_temp/event.json | - run: echo $ATOMGIT_EVENT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-203 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_WORKSPACE | 系统变量 | $ATOMGIT_WORKSPACE | 读取系统变量ATOMGIT_WORKSPACE | 返回Runner工作区路径,示例/home/runner/workspace | - run: echo $ATOMGIT_WORKSPACE | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-204 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTION | 系统变量 | $ATOMGIT_ACTION | 读取系统变量ATOMGIT_ACTION | 返回当前Action名称,示例my-action | - run: echo $ATOMGIT_ACTION | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(ATOMGIT_ACTION仅在Action内部有值,普通步骤中可能为空),仅验语法声明 | S17 | liyanghang |  |

| TC-205 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REPOSITORY | 系统变量 | $ATOMGIT_REPOSITORY | 读取系统变量ATOMGIT_REPOSITORY | 返回仓库全名,示例owner/repo | - run: echo $ATOMGIT_REPOSITORY | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-206 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_REPOSITORY_OWNER | 系统变量 | $ATOMGIT_REPOSITORY_OWNER | 读取系统变量ATOMGIT_REPOSITORY_OWNER | 返回仓库所属组织,示例myorg | - run: echo $ATOMGIT_REPOSITORY_OWNER | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: ATOMGIT_REPOSITORY_OWNER 为空 | Tier-A | liyanghang |  |

| TC-207 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_RUN_ID | 系统变量 | $ATOMGIT_RUN_ID | 读取系统变量ATOMGIT_RUN_ID | 返回工作流运行ID,示例12345 | - run: echo $ATOMGIT_RUN_ID | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-208 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_RUN_NUMBER | 系统变量 | $ATOMGIT_RUN_NUMBER | 读取系统变量ATOMGIT_RUN_NUMBER | 返回工作流运行编号,示例42 | - run: echo $ATOMGIT_RUN_NUMBER | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-209 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_RUN_ATTEMPT | 系统变量 | $ATOMGIT_RUN_ATTEMPT | 读取系统变量ATOMGIT_RUN_ATTEMPT | 返回重试次数,示例1 | - run: echo $ATOMGIT_RUN_ATTEMPT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: ATOMGIT_RUN_ATTEMPT 为空 | Tier-A | liyanghang |  |

| TC-210 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_WORKFLOW | 系统变量 | $ATOMGIT_WORKFLOW | 读取系统变量ATOMGIT_WORKFLOW | 返回工作流名称,示例CI Pipeline | - run: echo $ATOMGIT_WORKFLOW | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-211 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_HEAD_REF | 系统变量 | $ATOMGIT_HEAD_REF | 读取系统变量ATOMGIT_HEAD_REF | 返回PR源分支(仅PR),示例feature/x | - run: echo $ATOMGIT_HEAD_REF | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(ATOMGIT_HEAD_REF仅在pull_request触发时有值,push触发时为空),仅验语法声明 | Tier-A | liyanghang |  |

| TC-212 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_BASE_REF | 系统变量 | $ATOMGIT_BASE_REF | 读取系统变量ATOMGIT_BASE_REF | 返回PR目标分支(仅PR),示例main | - run: echo $ATOMGIT_BASE_REF | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(ATOMGIT_BASE_REF仅在pull_request触发时有值,push触发时为空),仅验语法声明 | Tier-A | liyanghang |  |

| TC-213 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_SERVER_URL | 系统变量 | $ATOMGIT_SERVER_URL | 读取系统变量ATOMGIT_SERVER_URL | 返回平台根URL,示例https://atomgit.com | - run: echo $ATOMGIT_SERVER_URL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-214 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_API_URL | 系统变量 | $ATOMGIT_API_URL | 读取系统变量ATOMGIT_API_URL | 返回API基础URL,示例https://api.atomgit.com | - run: echo $ATOMGIT_API_URL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-215 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_GRAPHQL_URL | 系统变量 | $ATOMGIT_GRAPHQL_URL | 读取系统变量ATOMGIT_GRAPHQL_URL | 返回GraphQL API URL,示例https://api.atomgit.com/graphql | - run: echo $ATOMGIT_GRAPHQL_URL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: ATOMGIT_GRAPHQL_URL 为空 | Tier-A | liyanghang |  |

| TC-216 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_OUTPUT | 系统变量 | $ATOMGIT_OUTPUT | 读取系统变量ATOMGIT_OUTPUT | 返回步骤输出文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_OUTPUT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-217 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ENV | 系统变量 | $ATOMGIT_ENV | 读取系统变量ATOMGIT_ENV | 返回步骤环境变量文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_ENV | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-218 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_PATH | 系统变量 | $ATOMGIT_PATH | 读取系统变量ATOMGIT_PATH | 返回步骤系统PATH文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-219 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_STEP_SUMMARY | 系统变量 | $ATOMGIT_STEP_SUMMARY | 读取系统变量ATOMGIT_STEP_SUMMARY | 返回步骤摘要文件路径,示例见工作流命令参考 | - run: echo $ATOMGIT_STEP_SUMMARY | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-1 | S17 | liyanghang |  |

| TC-220 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 系统变量 | $ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 读取系统变量ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 返回是否允许不安全命令,示例false(默认) | - run: echo $ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(该变量未设置时为空或false,设置时才注入,无法从shell内部验证平台默认值行为),仅验语法声明 | S13 | yulin |  |

| TC-221 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTION_REPOSITORY | 系统变量 | $ATOMGIT_ACTION_REPOSITORY | 读取系统变量ATOMGIT_ACTION_REPOSITORY | 返回Action来源仓库,示例owner/action-repo | - run: echo $ATOMGIT_ACTION_REPOSITORY | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(ATOMGIT_ACTION_REPOSITORY仅在Action插件内部有值,普通步骤中为空),仅验语法声明 | S17 | liyanghang |  |

| TC-222 | syntax-reference/variables | ATOMGIT_*系统变量 | ATOMGIT_ACTION_REF | 系统变量 | $ATOMGIT_ACTION_REF | 读取系统变量ATOMGIT_ACTION_REF | 返回Action来源引用,示例v1 | - run: echo $ATOMGIT_ACTION_REF | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(ATOMGIT_ACTION_REF仅在Action插件内部有值,普通步骤中为空),仅验语法声明 | S17 | liyanghang |  |

| TC-223 | core-concepts/trigger-events | 触发事件类型 | push | 触发事件 | on:push | 配置push触发 | 对应代码推送时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-224 | core-concepts/trigger-events | 触发事件类型 | pull_request | 触发事件 | on:pull_request | 配置pull_request触发 | 对应Pull Request时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: 未知事件=Push(不在触发器声明范围内) | S4 | chaoran |  |

| TC-225 | core-concepts/trigger-events | 触发事件类型 | schedule | 触发事件 | on:schedule | 配置schedule触发 | 对应定时触发时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-226 | core-concepts/trigger-events | 触发事件类型 | workflow_dispatch | 触发事件 | on:workflow_dispatch | 配置workflow_dispatch触发 | 对应手动触发时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-A | liyanghang |  |

| TC-227 | core-concepts/trigger-events | 触发事件类型 | workflow_call | 触发事件 | on:workflow_call | 配置workflow_call触发 | 对应工作流调用时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-A | liyanghang |  |

| TC-228 | core-concepts/trigger-events | 触发事件类型 | issue_comment | 触发事件 | on:issue_comment | 配置issue_comment触发 | 对应Issue评论时触发 | on:<br>  {e}: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-229 | core-concepts/trigger-events | 触发配置 | push.branches | 触发配置 | branches:[main] | 配置push.branches | 仅指定分支push触发 | on:<br>  branches:[main] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-230 | core-concepts/trigger-events | 触发配置 | push.tags | 触发配置 | tags:['v*'] | 配置push.tags | 仅指定tag push触发 | on:<br>  tags:['v*'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-231 | core-concepts/trigger-events | 触发配置 | push.paths | 触发配置 | paths:['src/**'] | 配置push.paths | 仅指定路径变更触发 | on:<br>  paths:['src/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-232 | core-concepts/trigger-events | 触发配置 | push.paths-ignore | 触发配置 | paths-ignore:['**/*.md'] | 配置push.paths-ignore | 忽略路径不触发 | on:<br>  paths-ignore:['**/*.md'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-233 | core-concepts/trigger-events | 触发配置 | push.branches-ignore | 触发配置 | branches-ignore:['release/**'] | 配置push.branches-ignore | 忽略分支push不触发 | on:<br>  branches-ignore:['release/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-234 | core-concepts/trigger-events | 触发配置 | pull_request.types | 触发配置 | types:[open,reopen,update] | 配置pull_request.types | 仅指定类型PR触发 | on:<br>  types:[open,reopen,update] | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |

| TC-235 | core-concepts/trigger-events | 触发配置 | pull_request.branches | 触发配置 | branches:[main] | 配置pull_request.branches | 仅目标分支匹配触发 | on:<br>  branches:[main] | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |

| TC-236 | core-concepts/trigger-events | 触发配置 | pull_request.paths | 触发配置 | paths:['api/**'] | 配置pull_request.paths | 仅指定路径变更触发 | on:<br>  paths:['api/**'] | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |

| TC-237 | core-concepts/trigger-events | 触发配置 | schedule.cron | 触发配置 | cron:'0 2 * * *' | 配置schedule.cron | 按cron时间触发 | on:<br>  cron:'0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron触发时刻由平台调度器决定),仅验文档约束 | S3 | yulin |  |

| TC-238 | core-concepts/trigger-events | 触发配置 | workflow_dispatch.inputs | 触发配置 | inputs:build_id:type:string | 配置workflow_dispatch.inputs | 手动触发时可传参 | on:<br>  inputs:build_id:type:string | workflow_dispatch |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-239 | syntax-reference/workflow-commands | 工作流命令 | set-output | 工作流命令 | - | 使用命令set-output | 应:设置步骤输出 | - run: \|<br>    echo '::set-output name=K::V' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-240 | syntax-reference/workflow-commands | 工作流命令 | set-env | 工作流命令 | - | 使用命令set-env | 应:设置环境变量 | - run: \|<br>    echo '::set-env name=K::V' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-241 | syntax-reference/workflow-commands | 工作流命令 | add-path | 工作流命令 | - | 使用命令add-path | 应:添加系统PATH | - run: \|<br>    echo '::add-path::/custom/path' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-242 | syntax-reference/workflow-commands | 工作流命令 | set-step-summary | 工作流命令 | - | 使用命令set-step-summary | 应:设置步骤摘要 | - run: \|<br>    echo '::set-step-summary::content' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(步骤摘要显示在平台UI中,无法从shell内部验证是否渲染),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-243 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_OUTPUT写入 | 工作流命令 | - | 使用命令ATOMGIT_OUTPUT写入 | 应:通过文件设置输出 | - run: \|<br>    echo 'K=V' >> $ATOMGIT_OUTPUT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-244 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_ENV写入 | 工作流命令 | - | 使用命令ATOMGIT_ENV写入 | 应:通过文件设置环境变量 | - run: \|<br>    echo 'K=V' >> $ATOMGIT_ENV | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-245 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_PATH写入 | 工作流命令 | - | 使用命令ATOMGIT_PATH写入 | 应:通过文件添加PATH | - run: \|<br>    echo '/path' >> $ATOMGIT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-246 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_STEP_SUMMARY写入 | 工作流命令 | - | 使用命令ATOMGIT_STEP_SUMMARY写入 | 应:通过文件设置摘要 | - run: \|<br>    echo 'content' >> $ATOMGIT_STEP_SUMMARY | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-2 | S7 | chenqi |  |

| TC-247 | syntax-reference/workflow-commands | 工作流命令 | debug日志 | 工作流命令 | - | 使用命令debug日志 | 应:输出debug日志 | - run: \|<br>    echo '::debug::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::debug::命令由Runner平台解析渲染为调试日志,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-248 | syntax-reference/workflow-commands | 工作流命令 | error日志 | 工作流命令 | - | 使用命令error日志 | 应:输出error日志 | - run: \|<br>    echo '::error file=x,line=10::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::error::命令由Runner平台解析标注行错误,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-249 | syntax-reference/workflow-commands | 工作流命令 | warning日志 | 工作流命令 | - | 使用命令warning日志 | 应:输出warning日志 | - run: \|<br>    echo '::warning file=x,line=10::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::warning::命令由Runner平台解析渲染为警告标注,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-250 | syntax-reference/workflow-commands | 工作流命令 | notice日志 | 工作流命令 | - | 使用命令notice日志 | 应:输出notice日志 | - run: \|<br>    echo '::notice file=x,line=10::msg' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::notice::命令由Runner平台解析渲染为通知标注,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-251 | syntax-reference/workflow-commands | 工作流命令 | group日志分组 | 工作流命令 | - | 使用命令group日志分组 | 应:日志分组显示 | - run: \|<br>    echo '::group::Title'...echo '::endgroup::' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::group::命令由Runner平台渲染为折叠分组UI,shell内部无法验证分组效果),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-252 | syntax-reference/workflow-commands | 工作流命令 | mask-value掩码 | 工作流命令 | - | 使用命令mask-value掩码 | 应:日志中掩码指定值 | - run: \|<br>    echo '::add-mask::secret' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::add-mask::*** | S7 | chenqi | 不存在用例 |

| TC-253 | syntax-reference/workflow-commands | 工作流命令 | stop-commands | 工作流命令 | - | 使用命令stop-commands | 应:暂停命令处理 | - run: \|<br>    echo '::stop-commands::token'...echo '::token::' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(::stop-commands::效果由Runner平台处理,shell内部无法验证命令处理是否暂停),仅验语法声明 | S7 | chenqi | 不存在用例 |

| TC-254 | syntax-reference/runner-images-tools | Runner标签 | codearts-hosted | Runner标签 | runs-on:['codearts-hosted'] | 使用标签codearts-hosted | 调度到官方资源池Runner | runs-on: ['codearts-hosted'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-255 | syntax-reference/runner-images-tools | Runner标签 | self-hosted | Runner标签 | runs-on:['self-hosted'] | 使用标签self-hosted | 调度到自托管RunnerRunner | runs-on: ['self-hosted'] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-256 | syntax-reference/runner-images-tools | Runner标签 | ubuntu-latest | Runner标签 | runs-on:['ubuntu-latest'] | 使用标签ubuntu-latest | 调度到Ubuntu最新版Runner | runs-on: ['ubuntu-latest'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-257 | syntax-reference/runner-images-tools | Runner标签 | windows-latest | Runner标签 | runs-on:['windows-latest'] | 使用标签windows-latest | 调度到Windows最新版Runner | runs-on: ['windows-latest'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  |  | liyanghang |  |

| TC-258 | syntax-reference/runner-images-tools | Runner标签 | macos-latest | Runner标签 | runs-on:['macos-latest'] | 使用标签macos-latest | 调度到macOS最新版Runner | runs-on: ['macos-latest'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-259 | syntax-reference/runner-images-tools | Runner标签 | x64 | Runner标签 | runs-on:['x64'] | 使用标签x64 | 调度到x64架构Runner | runs-on: ['x64'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-260 | syntax-reference/runner-images-tools | Runner标签 | arm64 | Runner标签 | runs-on:['arm64'] | 使用标签arm64 | 调度到ARM64架构Runner | runs-on: ['arm64'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-261 | syntax-reference/runner-images-tools | Runner标签 | large | Runner标签 | runs-on:['large'] | 使用标签large | 调度到大型资源规格Runner | runs-on: ['large'] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-262 | syntax-reference/runner-images-tools | Runner镜像 | container.image | 运行环境 | container:<br>  image: ubuntu:20.04 | 使用自定义容器镜像 | Job在容器内执行 | container:<br>  image: ubuntu:20.04 | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-263 | syntax-reference/runner-images-tools | Runner镜像 | container.options | 运行环境 | container:<br>  options: --cpus 1 | 使用容器选项 | 容器按选项启动 | container:<br>  options: --cpus 1 --user root | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-264 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.name | Job字段 | jobs.<id>.name:value | 配置jobs.<id>.name | 应:Job显示名称 | jobs:<br>  build:<br>    name: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-265 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.runs-on | Job字段 | jobs.<id>.runs-on:value | 配置jobs.<id>.runs-on | 应:Job运行环境标签 | jobs:<br>  build:<br>    runs-on: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-266 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.needs | Job字段 | jobs.<id>.needs:value | 配置jobs.<id>.needs | 应:Job依赖列表 | jobs:<br>  build:<br>    needs: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: run_id 为空 | Tier-A | liyanghang |  |

| TC-267 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.if | Job字段 | jobs.<id>.if:value | 配置jobs.<id>.if | 应:Job条件执行 | jobs:<br>  build:<br>    if: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-268 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.env | Job字段 | jobs.<id>.env:value | 配置jobs.<id>.env | 应:Job级环境变量 | jobs:<br>  build:<br>    env: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-269 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.steps | Job字段 | jobs.<id>.steps:value | 配置jobs.<id>.steps | 应:Job步骤列表 | jobs:<br>  build:<br>    steps: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-270 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.timeout-minutes | Job字段 | jobs.<id>.timeout-minutes:value | 配置jobs.<id>.timeout-minutes | 应:Job超时时间 | jobs:<br>  build:<br>    timeout-minutes: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-271 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.strategy | Job字段 | jobs.<id>.strategy:value | 配置jobs.<id>.strategy | 应:Job矩阵策略 | jobs:<br>  build:<br>    strategy: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-272 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.continue-on-error | Job字段 | jobs.<id>.continue-on-error:value | 配置jobs.<id>.continue-on-error | 应:Job失败是否继续 | jobs:<br>  build:<br>    continue-on-error: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-273 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.container | Job字段 | jobs.<id>.container:value | 配置jobs.<id>.container | 应:Job自定义容器 | jobs:<br>  build:<br>    container: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | FAIL | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |

| TC-274 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.environment | Job字段 | jobs.<id>.environment:value | 配置jobs.<id>.environment | 应:Job部署环境 | jobs:<br>  build:<br>    environment: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-275 | writing-pipelines/configure-jobs | Jobs配置 | jobs.<id>.permissions | Job字段 | jobs.<id>.permissions:value | 配置jobs.<id>.permissions | 应:Job权限配置 | jobs:<br>  build:<br>    permissions: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-276 | writing-pipelines/configure-jobs | 矩阵策略 | strategy.matrix | 矩阵字段 | strategy.matrix:value | 配置strategy.matrix | 应:矩阵变量定义 | strategy:<br>  matrix:<br>    os: [ubuntu, windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-277 | writing-pipelines/configure-jobs | 矩阵策略 | strategy.fail-fast | 矩阵字段 | strategy.fail-fast:value | 配置strategy.fail-fast | 应:矩阵失败是否取消全部 | strategy:<br>  matrix:<br>    os: [ubuntu, windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-278 | writing-pipelines/configure-jobs | 矩阵策略 | strategy.max-parallel | 矩阵字段 | strategy.max-parallel:value | 配置strategy.max-parallel | 应:矩阵最大并行数 | strategy:<br>  matrix:<br>    os: [ubuntu, windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-279 | writing-pipelines/configure-steps | Steps配置 | steps.name | Step字段 | steps.name:value | 配置steps.name | 应:步骤名称 | steps:<br>  - name: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-280 | writing-pipelines/configure-steps | Steps配置 | steps.run | Step字段 | steps.run:value | 配置steps.run | 应:执行shell命令 | steps:<br>  - run: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-281 | writing-pipelines/configure-steps | Steps配置 | steps.uses | Step字段 | steps.uses:value | 配置steps.uses | 应:调用Action插件 | steps:<br>  - uses: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-282 | writing-pipelines/configure-steps | Steps配置 | steps.with | Step字段 | steps.with:value | 配置steps.with | 应:传参给Action | steps:<br>  - with: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-283 | writing-pipelines/configure-steps | Steps配置 | steps.env | Step字段 | steps.env:value | 配置steps.env | 应:步骤级环境变量 | steps:<br>  - env: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-284 | writing-pipelines/configure-steps | Steps配置 | steps.if | Step字段 | steps.if:value | 配置steps.if | 应:步骤条件执行 | steps:<br>  - if: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-285 | writing-pipelines/configure-steps | Steps配置 | steps.id | Step字段 | steps.id:value | 配置steps.id | 应:步骤唯一标识 | steps:<br>  - id: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-286 | writing-pipelines/configure-steps | Steps配置 | steps.continue-on-error | Step字段 | steps.continue-on-error:value | 配置steps.continue-on-error | 应:步骤失败是否继续 | steps:<br>  - continue-on-error: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-287 | writing-pipelines/configure-steps | Steps配置 | steps.working-directory | Step字段 | steps.working-directory:value | 配置steps.working-directory | 应:步骤工作目录 | steps:<br>  - working-directory: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-288 | writing-pipelines/configure-steps | Steps配置 | steps.shell | Step字段 | steps.shell:value | 配置steps.shell | 应:步骤使用的shell | steps:<br>  - shell: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-289 | concurrency | 并发控制 | concurrency.max | 并发字段 | concurrency.max:value | 配置concurrency.max | 应:最大并发数 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-290 | concurrency | 并发控制 | concurrency.enable | 并发字段 | concurrency.enable:value | 配置concurrency.enable | 应:是否启用并发控制 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-291 | concurrency | 并发控制 | concurrency.preemption.enable | 并发字段 | concurrency.preemption.enable:value | 配置concurrency.preemption.enable | 应:是否启用抢占 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |

| TC-292 | concurrency | 并发控制 | concurrency.preemption.events | 并发字段 | concurrency.preemption.events:value | 配置concurrency.preemption.events | 应:可抢占事件列表 | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |

| TC-293 | concurrency | 并发控制 | concurrency.exceed-action | 并发字段 | concurrency.exceed-action:value | 配置concurrency.exceed-action | 应:超限动作QUEUE/IGNORE/CANCEL | concurrency:<br>  max: 6<br>  enable: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |

| TC-294 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.name | 制品字段 | upload-artifact.name:value | 配置upload-artifact.name | 应:上传制品名称 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-295 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.path | 制品字段 | upload-artifact.path:value | 配置upload-artifact.path | 应:上传制品路径 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-296 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.retention-days | 制品字段 | upload-artifact.retention-days:value | 配置upload-artifact.retention-days | 应:制品保留天数 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-297 | writing-pipelines/upload-download-artifacts | 制品管理 | upload-artifact.if-no-files-found | 制品字段 | upload-artifact.if-no-files-found:value | 配置upload-artifact.if-no-files-found | 应:无文件时行为 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-298 | writing-pipelines/upload-download-artifacts | 制品管理 | download-artifact.name | 制品字段 | download-artifact.name:value | 配置download-artifact.name | 应:下载制品名称 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-299 | writing-pipelines/upload-download-artifacts | 制品管理 | download-artifact.path | 制品字段 | download-artifact.path:value | 配置download-artifact.path | 应:下载制品目标路径 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-300 | writing-pipelines/upload-download-artifacts | 制品管理 | download-artifact.pattern | 制品字段 | download-artifact.pattern:value | 配置download-artifact.pattern | 应:下载制品匹配模式 | uses: upload-artifact<br>  with:<br>    name: report | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-301 | writing-pipelines/using-dependency-cache | 依赖缓存 | cache.path | 缓存字段 | cache.path:value | 配置cache.path | 应:缓存路径 | uses: cache<br>  with:<br>    path: ~/.cache/pip<br>    key: pip | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-302 | writing-pipelines/using-dependency-cache | 依赖缓存 | cache.key | 缓存字段 | cache.key:value | 配置cache.key | 应:缓存键(支持hashFiles) | uses: cache<br>  with:<br>    path: ~/.cache/pip<br>    key: pip | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-303 | writing-pipelines/using-dependency-cache | 依赖缓存 | cache.restore-keys | 缓存字段 | cache.restore-keys:value | 配置cache.restore-keys | 应:缓存恢复键列表 | uses: cache<br>  with:<br>    path: ~/.cache/pip<br>    key: pip | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-304 | writing-pipelines/using-actions | Action插件 | checkout | Action插件 | uses:checkout | 调用checkout | 应:拉取仓库代码 | - uses: checkout<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |

| TC-305 | writing-pipelines/using-actions | Action插件 | cache | Action插件 | uses:cache | 调用cache | 应:依赖缓存 | - uses: cache<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-306 | writing-pipelines/using-actions | Action插件 | upload-artifact | Action插件 | uses:upload-artifact | 调用upload-artifact | 应:上传制品 | - uses: upload-artifact<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-307 | writing-pipelines/using-actions | Action插件 | download-artifact | Action插件 | uses:download-artifact | 调用download-artifact | 应:下载制品 | - uses: download-artifact<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S9 | chenqi |  |

| TC-308 | writing-pipelines/using-actions | Action插件 | setup-python | Action插件 | uses:setup-python | 调用setup-python | 应:设置Python版本 | - uses: setup-python<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |

| TC-309 | writing-pipelines/using-actions | Action插件 | setup-node | Action插件 | uses:setup-node | 调用setup-node | 应:设置Node.js版本 | - uses: setup-node<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |

| TC-310 | writing-pipelines/using-actions | Action插件 | setup-java | Action插件 | uses:setup-java | 调用setup-java | 应:设置Java版本 | - uses: setup-java<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | FAIL | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |

| TC-311 | writing-pipelines/using-actions | Action插件 | manifest-management-plugin | Action插件 | uses:manifest-management-plugin | 调用manifest-management-plugin | 应:清单管理插件 | - uses: manifest-management-plugin<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |

| TC-312 | writing-pipelines/using-actions | Action插件 | official_shell_plugin | Action插件 | uses:official_shell_plugin | 调用official_shell_plugin | 应:官方Shell插件 | - uses: official_shell_plugin<br>  with:<br>    param: value | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S10 | chenqi |  |

| TC-313 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs(单依赖) | 依赖配置 | jobs.b.needs:[a] | 配置needs(单依赖) | Job b依赖Job a串行 | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: run_id 为空 | Tier-A | liyanghang |  |

| TC-314 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs(多依赖) | 依赖配置 | jobs.c.needs:[a,b] | 配置needs(多依赖) | Job c依赖a和b | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-315 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs(空依赖) | 依赖配置 | needs:[] | 配置needs(空依赖) | Job无依赖可并行 | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-316 | writing-pipelines/configure-dependencies-order | 任务依赖 | DAG拓扑 | 依赖配置 | build->test->deploy | 配置DAG拓扑 | 复杂依赖形成DAG | jobs:<br>  b:<br>    needs: [a] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: run_id 为空 | Tier-A | liyanghang |  |

| TC-317 | writing-pipelines/configure-conditional-execution | 条件执行 | if:default() | 条件配置 | if: ${{default()}} | 配置if:default() | 默认条件前置成功时执行 | - if: ${{default()}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | suite-4 | Tier-A | liyanghang |  |

| TC-318 | writing-pipelines/configure-conditional-execution | 条件执行 | if:always() | 条件配置 | if: ${{always}} | 配置if:always() | 无论前置都执行 | - if: ${{always}} | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | FAIL | suite-4 | Tier-B | liyanghang |  |

| TC-319 | writing-pipelines/configure-conditional-execution | 条件执行 | if:success | 条件配置 | if: ${{success}} | 配置if:success | 前置成功时执行 | - if: ${{success}} | any |  | status | run.status | SUCCESS,成功 | B API字段 | FAIL |  | Tier-B | liyanghang |  |

| TC-320 | writing-pipelines/configure-conditional-execution | 条件执行 | if:failed | 条件配置 | if: ${{failed}} | 配置if:failed | 前置失败时执行 | - if: ${{failed}} | any |  | status | run.status | FAILED,触发失败传播 | B API字段 | FAIL |  | Tier-B | liyanghang |  |

| TC-321 | writing-pipelines/configure-conditional-execution | 条件执行 | if:cancelled | 条件配置 | if: ${{cancelled}} | 配置if:cancelled | 工作流取消时执行 | - if: ${{cancelled}} | any |  | status | run.status | CANCELLED,被取消 | B API字段 | FAIL |  | Tier-B | liyanghang |  |

| TC-322 | writing-pipelines/configure-conditional-execution | 条件执行 | if:分支匹配 | 条件配置 | if: ${{atomgit.ref=='refs/heads/main'}} | 配置if:分支匹配 | 仅main分支时执行 | - if: ${{atomgit.ref=='refs/heads/main'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-323 | writing-pipelines/configure-conditional-execution | 条件执行 | if:事件匹配 | 条件配置 | if: ${{atomgit.event_name=='push'}} | 配置if:事件匹配 | 仅push事件时执行 | - if: ${{atomgit.event_name=='push'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-324 | writing-pipelines/configure-conditional-execution | 条件执行 | if:前置步骤结果 | 条件配置 | if: ${{steps.build.outputs.result=='success'}} | 配置if:前置步骤结果 | 依据前置步骤输出 | - if: ${{steps.build.outputs.result=='success'}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-325 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix单变量 | 矩阵配置 | matrix:<br>  os:[ubuntu,windows] | 配置matrix单变量 | 单变量矩阵展开2实例 | strategy:<br>  matrix:<br>  os:[ubuntu,windows] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-326 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix多变量 | 矩阵配置 | matrix:<br>  os:[ubuntu,windows]<br>  py:[3.9,3.10] | 配置matrix多变量 | 多变量矩阵展开4实例 | strategy:<br>  matrix:<br>  os:[ubuntu,windows]<br>  py:[3.9,3.10] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-327 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix include | 矩阵配置 | matrix:<br>  include:<br>    - os: macos | 配置matrix include | include追加特殊组合 | strategy:<br>  matrix:<br>  include:<br>    - os: macos | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-328 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix exclude | 矩阵配置 | matrix:<br>  exclude:<br>    - os: windows | 配置matrix exclude | exclude排除特定组合 | strategy:<br>  matrix:<br>  exclude:<br>    - os: windows | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-329 | writing-pipelines/configure-matrix-builds | 矩阵构建 | fail-fast:false | 矩阵配置 | strategy:<br>  fail-fast:false | 配置fail-fast:false | 矩阵失败不取消其它 | strategy:<br>  strategy:<br>  fail-fast:false | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: fail-fast=false 效果需让矩阵中某实例失败后观察其他实例是否继续,无法在正常运行中验证 | Tier-A | liyanghang |  |

| TC-330 | writing-pipelines/configure-matrix-builds | 矩阵构建 | max-parallel:3 | 矩阵配置 | strategy:<br>  max-parallel:3 | 配置max-parallel:3 | 矩阵最大并行数3 | strategy:<br>  strategy:<br>  max-parallel:3 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: max-parallel=3 效果需观察并发执行的矩阵实例数量,无法在单 step 内验证 | Tier-A | liyanghang |  |

| TC-331 | writing-pipelines/pass-output-between-jobs | 输出传递 | steps.<id>.outputs | 输出配置 | echo '::set-output name=k::v' | 配置steps.<id>.outputs | 步骤内设置输出 | echo '::set-output name=k::v' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-332 | writing-pipelines/pass-output-between-jobs | 输出传递 | job outputs映射 | 输出配置 | jobs:<br>  build:<br>    outputs:<br>      ver: ${{steps.x.outputs.ver}} | 配置job outputs映射 | Job级声明outputs | jobs:<br>  build:<br>    outputs:<br>      ver: ${{steps.x.outputs.ver}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP |  | Tier-A | liyanghang |  |

| TC-333 | writing-pipelines/pass-output-between-jobs | 输出传递 | 跨Job引用 | 输出配置 | jobs:<br>  deploy:<br>    needs: build<br>    env:<br>      V: ${{needs.build.outputs.ver}} | 配置跨Job引用 | 通过needs.<job>.outputs引用 | jobs:<br>  deploy:<br>    needs: build<br>    env:<br>      V: ${{needs.build.outputs.ver}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP |  | Tier-A | liyanghang |  |

| TC-334 | core-concepts/trigger-events | 触发事件完整列表 | push | 触发事件 | on:push | 配置push触发 | 应:代码推送事件触发workflow | on:<br>  push: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-335 | core-concepts/trigger-events | 触发事件完整列表 | pull_request | 触发事件 | on:pull_request | 配置pull_request触发 | 应:Pull Request事件触发workflow | on:<br>  pull_request: | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: 未知事件=Push(不在触发器声明范围内) | S4 | chaoran |  |

| TC-336 | core-concepts/trigger-events | 触发事件完整列表 | pull_request_target | 触发事件 | on:pull_request_target | 配置pull_request_target触发 | 应:PR目标分支上下文事件触发workflow | on:<br>  pull_request_target: | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: 未知事件=Push(不在触发器声明范围内) | S4 | chaoran |  |

| TC-337 | core-concepts/trigger-events | 触发事件完整列表 | schedule | 触发事件 | on:schedule | 配置schedule触发 | 应:定时触发事件触发workflow | on:<br>  schedule: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-338 | core-concepts/trigger-events | 触发事件完整列表 | workflow_dispatch | 触发事件 | on:workflow_dispatch | 配置workflow_dispatch触发 | 应:手动触发事件触发workflow | on:<br>  workflow_dispatch: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-339 | core-concepts/trigger-events | 触发事件完整列表 | workflow_call | 触发事件 | on:workflow_call | 配置workflow_call触发 | 应:工作流调用事件触发workflow | on:<br>  workflow_call: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-340 | core-concepts/trigger-events | 触发事件完整列表 | issue_comment | 触发事件 | on:issue_comment | 配置issue_comment触发 | 应:Issue评论事件触发workflow | on:<br>  issue_comment: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-341 | core-concepts/trigger-events | 触发事件完整列表 | issues | 触发事件 | on:issues | 配置issues触发 | 应:Issue事件事件触发workflow | on:<br>  issues: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-342 | core-concepts/trigger-events | 触发事件完整列表 | release | 触发事件 | on:release | 配置release触发 | 应:Release事件事件触发workflow | on:<br>  release: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-343 | core-concepts/trigger-events | 触发事件完整列表 | create | 触发事件 | on:create | 配置create触发 | 应:分支/标签创建事件触发workflow | on:<br>  create: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-344 | core-concepts/trigger-events | 触发事件完整列表 | delete | 触发事件 | on:delete | 配置delete触发 | 应:分支/标签删除事件触发workflow | on:<br>  delete: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-345 | core-concepts/trigger-events | 触发事件完整列表 | fork | 触发事件 | on:fork | 配置fork触发 | 应:Fork事件事件触发workflow | on:<br>  fork: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-346 | core-concepts/trigger-events | 触发事件完整列表 | watch | 触发事件 | on:watch | 配置watch触发 | 应:Star/Watch事件事件触发workflow | on:<br>  watch: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL: 未知事件=Push(不在触发器声明范围内) | Tier-A | liyanghang |  |

| TC-347 | running-pipelines | 运行流水线 | view-run-results | 运行操作 | - | 操作:查看运行结果 | 展示各阶段状态/耗时/结论 | # UI操作:view-run-results | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-348 | running-pipelines | 运行流水线 | view-job-logs | 运行操作 | - | 操作:查看任务日志 | 逐step查看完整日志 | # UI操作:view-job-logs | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-349 | running-pipelines | 运行流水线 | manually-trigger-pipeline | 运行操作 | - | 操作:手动触发 | UI手动触发并传参 | # UI操作:manually-trigger-pipeline | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-350 | running-pipelines | 运行流水线 | rerun-failed-jobs | 运行操作 | - | 操作:重新运行失败任务 | 仅重跑失败Job | # UI操作:rerun-failed-jobs | any |  | status | run.status | FAILED,触发失败传播 | B API字段 | PASS | suite-3 | Tier-B | liyanghang |  |

| TC-351 | security-permissions | 安全与权限 | permissions.repository | 安全配置 | read/write/admin | 配置permissions.repository | 授予仓库权限 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-352 | security-permissions | 安全与权限 | permissions.issue | 安全配置 | read/write/admin | 配置permissions.issue | 授予Issue权限 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-353 | security-permissions | 安全与权限 | permissions.pull_request | 安全配置 | read/write/admin | 配置permissions.pull_request | 授予PR权限 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-354 | security-permissions | 安全与权限 | secrets日志脱敏 | 安全配置 | echo ${{secrets.X}} | 配置secrets日志脱敏 | 日志替换为*** | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S13 | yulin |  |

| TC-355 | security-permissions | 安全与权限 | ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 安全配置 | 是否允许不安全命令 | 配置ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS | 默认false禁止set-env | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-2 | S13 | yulin |  |

| TC-356 | security-permissions | 安全与权限 | ATOMGIT_TOKEN生命周期 | 安全配置 | 仅运行期间有效 | 配置ATOMGIT_TOKEN生命周期 | 运行后失效不可持久化 | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-357 | action-development | Action插件开发 | action.yml元数据 | Action开发 | name/description/inputs/outputs | 配置action.yml元数据 | 声明Action元数据 | action.yml:<br>name/description/inputs/outputs | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-358 | action-development | Action插件开发 | inputs定义 | Action开发 | inputs:<br>  x:<br>    required: true | 配置inputs定义 | 声明输入参数 | action.yml:<br>inputs:<br>  x:<br>    required: true | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-359 | action-development | Action插件开发 | outputs定义 | Action开发 | outputs:<br>  result:<br>    description: '...' | 配置outputs定义 | 声明输出参数 | action.yml:<br>outputs:<br>  result:<br>    description: '...' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-360 | action-development | Action插件开发 | runs.using | Action开发 | using:'shell'/'composite'/'node' | 配置runs.using | 指定Action运行方式 | action.yml:<br>using:'shell'/'composite'/'node' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-361 | action-development | Action插件开发 | runs.steps | Action开发 | runs:<br>  steps:<br>    - run: ... | 配置runs.steps | composite步骤列表 | action.yml:<br>runs:<br>  steps:<br>    - run: ... | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S17 | liyanghang |  |

| TC-362 | action-development | Action插件开发 | runs.main | Action开发 | runs:<br>  main: 'index.js' | 配置runs.main | node入口文件 | action.yml:<br>runs:<br>  main: 'index.js' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S17 | liyanghang |  |

| TC-363 | core-concepts/runner-and-environment | Runner运行环境 | 官方资源池 | Runner环境 | runs-on:[codearts-hosted,ubuntu-latest,x64,large] | 配置官方资源池 | 调度到官方托管Runner | runs-on: [codearts-hosted, ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-364 | core-concepts/runner-and-environment | Runner运行环境 | 自托管资源池 | Runner环境 | runs-on:[self-hosted,arch=arm] | 配置自托管资源池 | 调度到自托管Runner | runs-on: [codearts-hosted, ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-365 | core-concepts/runner-and-environment | Runner运行环境 | 三段式标签 | Runner环境 | <pool>,<arch>,<flavor> | 配置三段式标签 | 按三段式标签格式调度 | runs-on: [codearts-hosted, ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-366 | core-concepts/workflow-job-step-action | 工作流结构 | workflow文件位置 | 工作流结构 | .gitcode/workflows/*.yml | 配置workflow文件位置 | 识别.workflows目录下YAML | .gitcode/workflows/*.yml | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-367 | core-concepts/workflow-job-step-action | 工作流结构 | workflow name | 工作流结构 | name: CI Pipeline | 配置workflow name | 显示在流水线列表 | name: CI Pipeline | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-368 | core-concepts/workflow-job-step-action | 工作流结构 | workflow on | 工作流结构 | on: push | 配置workflow on | 按声明事件触发 | on: push | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-369 | core-concepts/workflow-job-step-action | 工作流结构 | workflow env | 工作流结构 | env:<br>  GLOBAL: value | 配置workflow env | workflow级环境变量 | env:<br>  GLOBAL: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-370 | core-concepts/workflow-job-step-action | 工作流结构 | workflow concurrency | 工作流结构 | concurrency:<br>  max: 6 | 配置workflow concurrency | 控制并发 | concurrency:<br>  max: 6 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-371 | core-concepts/workflow-job-step-action | 工作流结构 | workflow stages | 工作流结构 | stages:<br>  s1:<br>    jobs: ... | 配置workflow stages | 按stages组织Job | stages:<br>  s1:<br>    jobs: ... | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-372 | core-concepts/workflow-job-step-action | 工作流结构 | job runs-on | 工作流结构 | runs-on: ubuntu-latest | 配置job runs-on | 按标签调度Runner | runs-on: ubuntu-latest | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-373 | core-concepts/workflow-job-step-action | 工作流结构 | job needs | 工作流结构 | needs: [build] | 配置job needs | 按依赖串行/并行 | needs: [build] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-374 | core-concepts/workflow-job-step-action | 工作流结构 | job strategy | 工作流结构 | strategy:<br>  matrix: ... | 配置job strategy | 按矩阵展开实例 | strategy:<br>  matrix: ... | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-375 | core-concepts/workflow-job-step-action | 工作流结构 | step run | 工作流结构 | run: echo hello | 配置step run | 执行shell命令 | run: echo hello | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-376 | core-concepts/workflow-job-step-action | 工作流结构 | step uses | 工作流结构 | uses: checkout | 配置step uses | 调用Action插件 | uses: checkout | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-377 | core-concepts/workflow-job-step-action | 工作流结构 | step with | 工作流结构 | with:<br>  param: value | 配置step with | 传参给Action | with:<br>  param: value | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-378 | core-concepts/artifacts-and-cache | 制品与缓存 | artifacts上传 | 制品/缓存 | uses: upload-artifact | 配置artifacts上传 | 上传构建产物 | - uses: artifacts上传 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-379 | core-concepts/artifacts-and-cache | 制品与缓存 | artifacts下载 | 制品/缓存 | uses: download-artifact | 配置artifacts下载 | 下载指定制品 | - uses: artifacts下载 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-380 | core-concepts/artifacts-and-cache | 制品与缓存 | artifacts retention | 制品/缓存 | retention-days: 14 | 配置artifacts retention | 按声明保留天数 | - uses: artifacts retention | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-3 | Tier-A | liyanghang |  |

| TC-381 | core-concepts/artifacts-and-cache | 制品与缓存 | cache依赖缓存 | 制品/缓存 | uses: cache | 配置cache依赖缓存 | 缓存依赖加速构建 | - uses: cache依赖缓存 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-382 | core-concepts/artifacts-and-cache | 制品与缓存 | cache key hashFiles | 制品/缓存 | key: ${{hashFiles('**/lock')}} | 配置cache key hashFiles | 按文件哈希生成缓存键 | - uses: cache key hashFiles | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-383 | writing-pipelines/workflow-file-location-structure | 文件位置 | .gitcode/workflows/目录 | 路径规则 | - | workflow文件存放目录 | 仅识别该目录下.yml/.yaml | 目录: .gitcode/workflows/ | any | 其他后缀被忽略 | file_path | run.file_path | 以 .gitcode/workflows/ 开头 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-384 | writing-pipelines/workflow-file-location-structure | 文件位置 | .yml后缀识别 | 后缀规则 | - | 文件以.yml结尾 | 被识别为workflow | 文件: ci.yml | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-385 | writing-pipelines/workflow-file-location-structure | 文件位置 | .yaml后缀识别 | 后缀规则 | - | 文件以.yaml结尾 | 被识别为workflow | 文件: ci.yaml | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-386 | writing-pipelines/workflow-file-location-structure | 文件位置 | 其他后缀忽略 | 后缀规则 | - | 文件以.txt结尾 | 被忽略不识别 | 文件: ci.txt | any |  | — | — | —(仅可经Job日志断言) | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-387 | writing-pipelines/workflow-file-location-structure | 命名建议 | ci.yml | 命名 | - | 持续集成场景 | push/PR时构建测试 | 文件名: ci.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S13 | yulin |  |

| TC-388 | writing-pipelines/workflow-file-location-structure | 命名建议 | pr-check.yml | 命名 | - | 合并请求检查 | PR提交时自动检查 | 文件名: pr-check.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S13 | yulin |  |

| TC-389 | writing-pipelines/workflow-file-location-structure | 命名建议 | release.yml | 命名 | - | 发布流程 | Tag触发发布 | 文件名: release.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | S13 | yulin |  |

| TC-390 | writing-pipelines/workflow-file-location-structure | 命名建议 | docker-build.yml | 命名 | - | Docker镜像构建 | 构建并推送镜像 | 文件名: docker-build.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL |  | S13 | yulin |  |

| TC-391 | writing-pipelines/workflow-file-location-structure | 命名建议 | nightly.yml | 命名 | - | 定时任务 | 每日定时构建 | 文件名: nightly.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL |  | S13 | yulin |  |

| TC-392 | writing-pipelines/workflow-file-location-structure | 命名建议 | deploy.yml | 命名 | - | 手动部署 | 手动触发部署 | 文件名: deploy.yml | any |  | — | — | —(仅可经Job日志断言) | C 难真测 |  |  | S4 | chaoran |  |

| TC-393 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | name | 字段 | - | workflow展示名称 | 缺省时使用文件名 | name: ci | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-394 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | on | 字段 | - | 触发条件 | 定义触发事件 | on: push | any | 必填 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-395 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | env | 字段 | - | workflow级环境变量 | 所有job和step可见 | env:<br>  APP_NAME: x | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-396 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | defaults | 字段 | - | 默认设置 | 默认shell和working-directory | defaults:<br>  run:<br>    shell: bash | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-397 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | concurrency | 字段 | - | 并发控制 | 限制并行运行数 | concurrency:<br>  max: 3 | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-398 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | permissions | 字段 | - | 权限声明 | 控制TOKEN权限范围 | permissions:<br>  repository: read | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-399 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | stages | 字段 | - | 阶段定义 | 阶段串行控制 | stages:<br>  build: ... | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-400 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | jobs | 字段 | - | 任务集合 | 无stages时为顶层 | jobs:<br>  build: ... | any | 必填 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-401 | writing-pipelines/workflow-file-location-structure | 基本结构字段 | post | 字段 | - | 后处理阶段 | 通知/清理/回写 | post:<br>  run_always: true | any | 可选 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-402 | writing-pipelines/workflow-file-location-structure | stages机制 | 阶段间串行 | 机制 | - | 多stage按定义顺序执行 | 前一stage完成后进入下一 | stages:<br>  - name: build<br>  - name: test | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-403 | writing-pipelines/workflow-file-location-structure | stages机制 | fail_fast=true | 机制 | - | stage中job失败 | 立即终止后续stage | stages:<br>  - fail_fast: true | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-404 | writing-pipelines/workflow-file-location-structure | stages机制 | fail_fast=false | 机制 | - | stage中job失败 | 不终止后续stage | stages:<br>  - fail_fast: false | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-405 | writing-pipelines/workflow-file-location-structure | stages机制 | 单stage可缺省 | 机制 | - | 仅一个stage时 | stages可省略,job默认并行 | jobs:<br>  a: ...<br>  b: ... | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-406 | writing-pipelines/workflow-file-location-structure | post机制 | run_always默认true | 机制 | - | post默认行为 | 无论成功失败都执行 | post:<br>  run_always: true | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-407 | writing-pipelines/workflow-file-location-structure | post机制 | run_always=false | 机制 | - | post设为false | 仅workflow成功时执行 | post:<br>  run_always: false | any |  | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-408 | writing-pipelines/workflow-file-location-structure | permissions快捷 | read-all | 快捷语法 | - | 所有权限设为read | 全部read | permissions: read-all | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-409 | writing-pipelines/workflow-file-location-structure | permissions快捷 | write-all | 快捷语法 | - | 所有权限设为write | 全部write | permissions: write-all | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-410 | writing-pipelines/workflow-file-location-structure | permissions快捷 | permissions:{} | 快捷语法 | - | 空对象 | 所有权限none(最小权限) | permissions: {} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-411 | writing-pipelines/workflow-file-location-structure | permissions项 | project | 权限项 | - | 项目访问权限 | read/write/none | permissions:<br>  project: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-412 | writing-pipelines/workflow-file-location-structure | permissions项 | pr | 权限项 | - | PR权限 | read/write/none | permissions:<br>  pr: write | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-413 | writing-pipelines/workflow-file-location-structure | permissions项 | issue | 权限项 | - | Issue权限 | read/write/none | permissions:<br>  issue: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-414 | writing-pipelines/workflow-file-location-structure | permissions项 | note | 权限项 | - | 评论/备注权限 | read/write/none | permissions:<br>  note: write | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-415 | writing-pipelines/workflow-file-location-structure | permissions项 | repository | 权限项 | - | 仓库权限 | read/write/none | permissions:<br>  repository: read | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-416 | writing-pipelines/workflow-file-location-structure | permissions项 | hook | 权限项 | - | Webhook权限 | read/write/none | permissions:<br>  hook: none | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-417 | writing-pipelines/configure-triggers | 否定模式 | branches否定(!) | 模式 | - | branches用!前缀排除 | 排除指定分支 | branches:<br>  - 'feature/**'<br>  - '!feature/exp' | push | 必须与肯定模式组合 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-418 | writing-pipelines/configure-triggers | 否定模式 | paths否定(!) | 模式 | - | paths用!前缀排除 | 排除指定路径 | paths:<br>  - 'src/**'<br>  - '!src/docs/**' | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-419 | writing-pipelines/configure-triggers | 否定模式 | tags否定(!) | 模式 | - | tags用!前缀排除 | 排除指定tag | tags:<br>  - 'v*'<br>  - '!v*-alpha' | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-420 | writing-pipelines/configure-triggers | 否定模式 | 仅否定模式不触发 | 规则 | - | 只有否定模式无肯定 | workflow不会触发 | branches: ['!main'] | any | 需配合肯定模式 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-421 | writing-pipelines/configure-triggers | 过滤组合 | branches+paths组合 | 组合 | - | 分支和路径过滤组合 | 同时满足才触发 | on:<br>  push:<br>    branches: [main]<br>    paths: ['src/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-422 | writing-pipelines/configure-triggers | 过滤组合 | paths前300文件限制 | 规则 | - | paths匹配前300个变更文件 | 超出部分不参与匹配 | paths: ['src/**'] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-423 | writing-pipelines/configure-triggers | 多事件组合 | push+PR+dispatch+schedule | 组合 | - | 同一workflow响应多事件 | 任一事件匹配即触发 | on:<br>  push:<br>  pull_request:<br>  workflow_dispatch:<br>  schedule: | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-424 | writing-pipelines/configure-triggers | PR目标分支 | branches过滤目标分支 | 规则 | - | PR的branches过滤的是base分支 | PR目标分支不在列表则不触发 | on:<br>  pull_request:<br>    branches: [main] | pull_request | 非源分支 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S4 | chaoran |  |

| TC-425 | writing-pipelines/configure-triggers | PR types默认 | 默认types=[open,reopen,update] | 规则 | - | 不指定types时 | 默认三种不含merge | on:<br>  pull_request: | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 当前事件=Push,非pull_request,无法验证PR types | S4 | chaoran |  |

| TC-426 | writing-pipelines/configure-triggers | workflow_call | 嵌套最多2层 | 规则 | - | 可重用工作流嵌套调用 | 最多2层,不能再调用可重用 | uses: ./workflow.yml | workflow_call |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-427 | writing-pipelines/configure-triggers | schedule | cron UTC时区 | 规则 | - | cron使用UTC时间 | 需换算本地时间 | cron: '0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | suite-3 | S3 | yulin |  |

| TC-428 | writing-pipelines/configure-triggers | schedule | 仅默认分支生效 | 规则 | - | schedule仅在默认分支 | 非默认分支不触发定时 | on:<br>  schedule: | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S3 | yulin |  |

| TC-429 | writing-pipelines/configure-triggers | schedule | 最短间隔5分钟 | 规则 | - | schedule最短间隔 | 低于5分钟不生效 | cron: '*/5 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(平台限制由调度器强制执行),仅验文档约束 | S3 | yulin |  |

| TC-430 | writing-pipelines/configure-triggers | schedule | 调度延迟数分钟 | 规则 | - | 定时任务可能延迟 | 存在数分钟调度延迟 | cron: '0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(调度延迟由平台负载决定),仅验文档约束 | S3 | yulin |  |

| TC-431 | writing-pipelines/using-script-commands | 脚本执行 | 执行仓库内脚本 | 脚本 | bash ./scripts/build.sh | 执行仓库中已有脚本 | 脚本正常运行 | run: bash ./scripts/build.sh | any | 需先checkout | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-432 | writing-pipelines/using-script-commands | 脚本执行 | chmod设置执行权限 | 脚本 | chmod +x ./scripts/build.sh | 给脚本加执行权限 | 可直接执行 | run: chmod +x ./scripts/build.sh | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-433 | writing-pipelines/using-script-commands | 脚本执行 | 直接执行已授权脚本 | 脚本 | ./scripts/build.sh | 直接执行有权限的脚本 | 正常运行 | run: ./scripts/build.sh | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-434 | writing-pipelines/using-script-commands | 多行输出 | ATOMGIT_OUTPUT多行写入 | 输出 | echo 'content<<$EOF' >> $ATOMGIT_OUTPUT | 写入多行值到输出 | 用分隔符包围多行 | run: \|<br>  EOF=$(dd...)<br>  echo 'content<<$EOF' >> $ATOMGIT_OUTPUT | any | 使用随机分隔符 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-435 | writing-pipelines/using-script-commands | 多行输出 | 多行环境变量 | 输出 | echo 'var<<$EOF' >> $ATOMGIT_ENV | 写入多行环境变量 | 后续step可用多行值 | run: echo 'APP<<$EOF' >> $ATOMGIT_ENV | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-436 | writing-pipelines/using-script-commands | 脱敏命令 | ::add-mask:: | 安全 | echo '::add-mask::$MY_SECRET' | 日志中掩藏敏感信息 | 值显示为*** | run: echo '::add-mask::$MY_SECRET' | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 |  | Tier-A | liyanghang |  |

| TC-437 | writing-pipelines/using-script-commands | 脚本命令 | run执行shell | 脚本 | run: echo hello | 在step中执行shell命令 | 命令正常执行 | run: echo hello | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-438 | writing-pipelines/using-variables-secrets | 引用方式 | YAML中引用(表达式) | 引用 | ${{ env.APP_NAME }} | 在YAML字段中使用 | Runner执行前替换 | run: echo ${{ env.APP_NAME }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-439 | writing-pipelines/using-variables-secrets | 引用方式 | Runner中引用(环境变量) | 引用 | $APP_NAME | 在run命令中使用 | 由Shell解释 | run: echo $APP_NAME | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-440 | writing-pipelines/using-variables-secrets | 优先级总览 | Step级env>Job级env>Workflow级env>vars>系统变量 | 优先级 | - | 完整优先级顺序 | 按序覆盖 | - | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-441 | writing-pipelines/using-variables-secrets | 系统变量补充 | ATOMGIT_RUNNER_OS | 系统变量 | $ATOMGIT_RUNNER_OS | Runner操作系统 | 返回Linux/Windows/macOS | run: echo $ATOMGIT_RUNNER_OS | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |

| TC-442 | writing-pipelines/using-variables-secrets | 系统变量补充 | ATOMGIT_RUNNER_ARCH | 系统变量 | $ATOMGIT_RUNNER_ARCH | Runner架构 | 返回X64/ARM/ARM64 | run: echo $ATOMGIT_RUNNER_ARCH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |

| TC-443 | writing-pipelines/using-variables-secrets | secrets安全 | 不要echo secrets | 安全 | echo '${{secrets.X}}' | 可能绕过脱敏 | 避免此写法 | - | any | echo ${{secrets}}不安全 | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-444 | writing-pipelines/using-variables-secrets | secrets安全 | 不要写入制品/缓存 | 安全 | - | secrets不写入artifact | 避免泄露 | - | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-445 | writing-pipelines/using-variables-secrets | secrets安全 | 外部PR不暴露高权限 | 安全 | - | fork PR默认不暴露 | 高权限secret | - | pull_request |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S4 | chaoran |  |

| TC-446 | runner-management/using-hosted-runners | 托管Runner | 使用官方资源池 | Runner | runs-on: [ubuntu-latest, x64, small] | 无需自建基础设施 | 调度到官方托管Runner | runs-on: [ubuntu-latest, x64, small] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-447 | runner-management/using-hosted-runners | 托管Runner | 资源规格small | 标签 | small | 小型资源规格 | 调度到small规格Runner | runs-on: [ubuntu-latest, x64, small] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-448 | runner-management/using-hosted-runners | 托管Runner | 资源规格large | 标签 | large | 大型资源规格 | 调度到large规格Runner | runs-on: [ubuntu-latest, x64, large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-449 | runner-management/using-self-hosted-runners | 自托管Runner | 主机自托管 | Runner | runs-on: [self-hosted] | 部署在主机上 | 调度到自托管Runner | runs-on: [self-hosted] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-450 | runner-management/using-self-hosted-runners | 自托管Runner | Kubernetes自托管 | Runner | runs-on: [self-hosted, k8s] | 部署在K8s上 | 调度到K8s Runner | runs-on: [self-hosted, k8s] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-451 | runner-management/using-self-hosted-runners | 自托管Runner | 特殊硬件GPU | 场景 | runs-on: [self-hosted, gpu] | 需要GPU硬件 | 调度到带GPU的Runner | runs-on: [self-hosted, gpu] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-452 | runner-management/using-self-hosted-runners | 自托管Runner | 内网环境 | 场景 | runs-on: [self-hosted, intranet] | 需要内网环境 | 调度到内网Runner | runs-on: [self-hosted, intranet] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-453 | runner-management/selecting-runner-labels | 标签选择 | 操作系统标签 | 标签 | ubuntu-latest/windows-latest/macos-latest | 指定操作系统 | 调度到对应OS Runner | runs-on: [windows-latest] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-454 | runner-management/selecting-runner-labels | 标签选择 | 架构标签 | 标签 | x64/arm64 | 指定架构 | 调度到对应架构Runner | runs-on: [arm64] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-455 | runner-management/selecting-runner-labels | 标签选择 | 资源规格标签 | 标签 | small/large | 指定资源规格 | 调度到对应规格Runner | runs-on: [large] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-456 | runner-management/selecting-runner-labels | 标签选择 | 自定义特征标签 | 标签 | gpu/special-tool | 自定义特征(如GPU) | 调度到匹配特征Runner | runs-on: [self-hosted, gpu] | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-457 | runner-management/selecting-runner-labels | 标签选择 | 多标签组合 | 标签 | runs-on: [ubuntu-latest, x64, small] | 多标签同时指定 | 必须同时满足所有标签 | runs-on: [ubuntu-latest, x64, small] | any | AND逻辑 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-458 | runner-management/configuring-images-toolchains | 镜像工具链 | container自定义镜像 | 容器 | container:<br>  image: python:3.12 | 指定自定义Docker镜像 | Job在指定容器内执行 | container:<br>  image: python:3.12 | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-459 | runner-management/configuring-images-toolchains | 镜像工具链 | container特定语言版本 | 容器 | container:<br>  image: node:20 | 指定特定语言版本 | 使用指定语言环境 | container:<br>  image: node:20 | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-460 | runner-management/configuring-images-toolchains | 镜像工具链 | container完整构建环境 | 容器 | container:<br>  image: my-builder:latest | 使用完整构建环境 | 使用自定义构建环境 | container:<br>  image: my-builder:latest | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | SKIP | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S8 | chenqi |  |

| TC-461 | syntax-reference/trigger-events | pull_request_target | pull_request_target事件 | 事件 | on:<br>  pull_request_target: | 运行在目标分支上下文 | 可读写目标仓库 | on:<br>  pull_request_target:<br>    types: [open] | pull_request_target | 用于secrets/写操作 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP | S4 | chaoran |  |

| TC-462 | syntax-reference/trigger-events | pull_request_target | fork PR安全风险 | 安全 | - | fork仓库PR也能触发 | 谨慎处理代码执行 | - | pull_request_target | 安全提示 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP | S4 | chaoran |  |

| TC-463 | syntax-reference/trigger-events | pull_request_target | 默认types=[open,reopen,update] | 规则 | - | 不指定types时 | 默认三种不含merge | on:<br>  pull_request_target: | pull_request_target |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP | S4 | chaoran |  |

| TC-464 | syntax-reference/trigger-events | issue_comment | issue_comment事件 | 事件 | on:<br>  issue_comment:<br>    types: [created] | Issue或PR评论触发 | 同时对Issue和PR评论生效 | on:<br>  issue_comment:<br>    types: [created] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |

| TC-465 | syntax-reference/trigger-events | issue_comment | types: created | 类型 | created | 评论创建时触发 | 触发workflow | types: [created] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP | S15 | chaoran |  |

| TC-466 | syntax-reference/trigger-events | issue_comment | types: edited | 类型 | edited | 评论编辑时触发 | 触发workflow | types: [edited] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |

| TC-467 | syntax-reference/trigger-events | issue_comment | types: deleted | 类型 | deleted | 评论删除时触发 | 触发workflow | types: [deleted] | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |

| TC-468 | syntax-reference/trigger-events | issue_comment | 区分PR评论 | 条件 | atomgit.event.issue.pull_request | 判断是否PR评论 | 存在则为PR评论 | if: ${{atomgit.event.issue.pull_request}} | issue_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP | S15 | chaoran |  |

| TC-469 | syntax-reference/trigger-events | pull_request_comment | pull_request_comment事件 | 事件 | on:<br>  pull_request_comment: | 仅在PR评论时触发 | 区别于issue_comment | on:<br>  pull_request_comment:<br>    types: [created] | pull_request_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S15 | chaoran |  |

| TC-470 | syntax-reference/trigger-events | pull_request_comment | comments正则过滤 | 过滤 | comments: ['/deploy'] | 基于正则过滤评论内容 | 仅匹配评论触发 | comments: ['/deploy', '/test'] | pull_request_comment |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP | S4 | chaoran |  |

| TC-471 | syntax-reference/trigger-events | cron特殊符号 | * 任意值 | 符号 | * * * * * | 匹配任意值 | 每分钟触发 | cron: '* * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-472 | syntax-reference/trigger-events | cron特殊符号 | , 列表分隔 | 符号 | 1,3,5 | 列表分隔 | 第1、3、5 | cron: '0 0 * * 1,3,5' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-473 | syntax-reference/trigger-events | cron特殊符号 | - 范围 | 符号 | 1-5 | 范围 | 1到5 | cron: '0 0 * * 1-5' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-474 | syntax-reference/trigger-events | cron特殊符号 | / 步长 | 符号 | */15 | 步长 | 每15单位 | cron: '*/15 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-475 | syntax-reference/trigger-events | cron位置 | 分钟(0-59) | 位置 | cron: 'm * * * *' | 每小时第几分钟 | 0-59 | cron: '30 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |

| TC-476 | syntax-reference/trigger-events | cron位置 | 小时(0-23) | 位置 | cron: '* h * * *' | UTC时间小时 | 0-23 | cron: '0 2 * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |

| TC-477 | syntax-reference/trigger-events | cron位置 | 日(1-31) | 位置 | cron: '* * d * *' | 每月第几天 | 1-31 | cron: '0 0 1 * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |

| TC-478 | syntax-reference/trigger-events | cron位置 | 月(1-12) | 位置 | cron: '* * * m *' | 月份 | 1-12 | cron: '0 0 1 1 *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |

| TC-479 | syntax-reference/trigger-events | cron位置 | 星期(0-6) | 位置 | cron: '* * * * w' | 0=周日..6=周六 | 0-6 | cron: '0 0 * * 0' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-3 | S3 | yulin |  |

| TC-480 | examples/nodejs-ci | Node.js示例 | npm ci构建 | 示例 | npm ci && npm test | Node.js项目CI | 构建和测试 | run: npm ci && npm test | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需npm工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-481 | examples/nodejs-ci | Node.js示例 | 多版本矩阵(node 18/20) | 示例 | matrix:<br>  node: [18,20] | 多版本矩阵测试 | 展开2实例 | strategy:<br>  matrix:<br>    node: [18, 20] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | suite-4 | S11 | chenqi |  |

| TC-482 | examples/java-maven-ci | Java Maven示例 | mvn build | 示例 | mvn clean package | Maven项目构建 | 生成jar包 | run: mvn clean package | push |  | — | — | —(仅可经Job日志断言) | C 难真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | SKIP: 难真测(需mvn工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-483 | examples/java-maven-ci | Java Maven示例 | 多JDK矩阵(8/11/17) | 示例 | matrix:<br>  jdk: [8,11,17] | 多JDK版本测试 | 展开3实例 | strategy:<br>  matrix:<br>    jdk: [8, 11, 17] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | suite-4 | S11 | chenqi |  |

| TC-484 | examples/java-gradle-ci | Java Gradle示例 | gradle build | 示例 | gradle build | Gradle项目构建 | 生成构建结果 | run: gradle build | push |  | — | — | —(仅可经Job日志断言) | C 难真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | SKIP: 难真测(需gradle工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-485 | examples/java-gradle-ci | Java Gradle示例 | Gradle缓存 | 示例 | cache:<br>  path: ~/.gradle | 缓存Gradle依赖 | 加速后续构建 | uses: cache<br>  with:<br>    path: ~/.gradle | push |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 |  SKIP（cq-s11-language-ci.yml已删除，Java工具链不可用，无独立workflow） | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S11 | chenqi |  |

| TC-486 | examples/go-ci | Go示例 | go build | 示例 | go build ./... | Go项目构建 | 生成二进制 | run: go build ./... | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-487 | examples/go-ci | Go示例 | go test | 示例 | go test ./... | Go项目测试 | 运行测试 | run: go test ./... | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-488 | examples/go-ci | Go示例 | go vet | 示例 | go vet ./... | Go静态检查 | 运行vet | run: go vet ./... | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-489 | examples/go-ci | Go示例 | go test覆盖率 | 示例 | go test -coverprofile=coverage.out | 生成覆盖率 | 输出coverage.out | run: go test -coverprofile=coverage.out | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需go工具链+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-490 | examples/go-ci | Go示例 | 多Go版本矩阵(1.19/1.20/1.21) | 示例 | matrix:<br>  go: [1.19,1.20,1.21] | 多Go版本测试 | 展开3实例 | strategy:<br>  matrix:<br>    go: [1.19, 1.20, 1.21] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: matrix.go=1.2 不在预期集合(1.19,1.20,1.21) | S11 | chenqi |  |

| TC-491 | examples/python-ci | Python示例 | flake8检查 | 示例 | flake8 src/ --max-line-length=120 | Python lint检查 | 输出格式问题 | run: flake8 src/ --max-line-length=120 | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需flake8工具+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-492 | examples/python-ci | Python示例 | black格式检查 | 示例 | black --check --diff src/ | 格式检查 | 输出格式差异 | run: black --check --diff src/ | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需black工具+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-493 | examples/python-ci | Python示例 | isort导入排序 | 示例 | isort --check-only --diff src/ | 导入排序检查 | 输出导入差异 | run: isort --check-only --diff src/ | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需isort工具+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-494 | examples/python-ci | Python示例 | mypy类型检查 | 示例 | mypy src/ --ignore-missing-imports | 类型检查 | 输出类型问题 | run: mypy src/ --ignore-missing-imports | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需mypy工具+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-495 | examples/python-ci | Python示例 | pytest+覆盖率 | 示例 | pytest tests/ --cov=src --cov-report=xml | 单元测试+覆盖率 | 生成coverage.xml | run: pytest tests/ --cov=src | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(需pytest+coverage工具+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-496 | examples/python-ci | Python示例 | 多Python矩阵(3.10/3.11/3.12) | 示例 | matrix:<br>  python: [3.10,3.11,3.12] | 多Python版本测试 | 展开3实例 | strategy:<br>  matrix:<br>    python: [3.10, 3.11, 3.12] | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | FAIL: matrix.python=3.1 不在预期集合(3.10,3.11,3.12) | S11 | chenqi |  |

| TC-497 | examples/python-ci | Python示例 | STEP_SUMMARY写入 | 示例 | echo '## 测试结果' >> $ATOMGIT_STEP_SUMMARY | 写入步骤摘要 | 摘要显示在UI | run: echo '## 结果' >> $ATOMGIT_STEP_SUMMARY | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: GITCODE_STEP_SUMMARY/GITHUB_STEP_SUMMARY 环境变量未注入，无法验证摘要写入 | S11 | chenqi |  |

| TC-498 | examples/python-ci | Python示例 | setup-python缓存pip | 示例 | setup-python:<br>  with:<br>    cache: 'pip' | 设置Python并缓存pip | 加速依赖安装 | uses: setup-python<br>  with:<br>    cache: 'pip' | push |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S11 | chenqi |  |

| TC-499 | examples/python-ci | Python示例 | python -m build打包 | 示例 | python -m build | 构建Python包 | 生成dist/ | run: python -m build | push |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(需python build工具+项目源码),仅验语法声明 | S11 | chenqi |  |

| TC-500 | examples/pr-code-check-example | PR检查示例 | 代码风格检查 | 示例 | run: flake8 src/ | PR代码风格 | 评论检查结果 | run: flake8 src/ | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(依赖lint外部工具+项目源码),仅验语法声明 | S4 | chaoran |  |

| TC-501 | examples/pr-code-check-example | PR检查示例 | 安全扫描 | 示例 | run: bandit -r src/ | PR安全扫描 | 输出安全问题 | run: bandit -r src/ | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(依赖SAST外部工具+项目源码),仅验语法声明 | S4 | chaoran |  |

| TC-502 | examples/pr-code-check-example | PR检查示例 | PR评论 | 示例 | gh pr comment | 自动评论PR | 输出检查结果 | run: gh pr comment $PR --body '...' | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | 没有gh命令，使用gitcode cli可以实现 | S4 | chaoran |  |

| TC-503 | examples/pr-code-check-example | PR检查示例 | 审查辅助 | 示例 | - if: ${{always}} | always条件执行 | 无论成功失败都评论 | if: ${{always}} | pull_request |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 难真测(依赖平台API写PR评论),仅验语法声明 | S4 | chaoran |  |

| TC-504 | syntax-reference/trigger-events | cron特殊符号 | cron星号*任意值 | 边界 | cron: '* * * * *' | 星号匹配任意值 | 每分钟触发一次 | cron: '* * * * *' | schedule | 每段可独立用* | — | — | —(仅可经Job日志断言) | C 难真测 | PASS |  | — | liyanghang |  |

| TC-505 | syntax-reference/trigger-events | cron特殊符号 | cron逗号,枚举 | 边界 | cron: '5,15,25 * * * *' | 逗号枚举多个值 | 第5/15/25分钟触发 | cron: '5,15,25 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-506 | syntax-reference/trigger-events | cron特殊符号 | cron连字符-区间 | 边界 | cron: '0-5 * * * *' | 连字符表示区间 | 第0~5分钟连续触发 | cron: '0-5 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-507 | syntax-reference/trigger-events | cron特殊符号 | cron斜杠/步长 | 边界 | cron: '*/15 * * * *' | 斜杠表示步长 | 每15分钟触发一次 | cron: '*/15 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-508 | syntax-reference/trigger-events | cron特殊符号 | cron问号?日或周 | 边界 | cron: '0 2 ? * *' | 问号代替日或周 | 日和周不能同时指定 | cron: '0 2 ? * *' | schedule | ?表示不指定 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-509 | syntax-reference/trigger-events | cron特殊符号 | cron字符L月末 | 边界 | cron: '0 0 L * *' | L表示最后 | 月末最后一天触发 | cron: '0 0 L * *' | schedule | L=last | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-510 | syntax-reference/trigger-events | cron特殊符号 | cron字符W最近工作日 | 边界 | cron: '0 0 15W * *' | W表示最近工作日 | 15号最近的工作日触发 | cron: '0 0 15W * *' | schedule | W=weekday | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-511 | syntax-reference/trigger-events | cron特殊符号 | cron字符#第N周 | 边界 | cron: '0 0 * * 2#3' | #表示第N个星期 | 每月第3个周二触发 | cron: '0 0 * * 2#3' | schedule | #=nth | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-512 | syntax-reference/trigger-events | cron特殊符号 | cron区间+步长组合 | 边界 | cron: '5-45/10 * * * *' | 区间和步长组合 | 5到45每10分钟触发 | cron: '5-45/10 * * * *' | schedule |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(cron符号语义由平台按POSIX解析),仅验文档约束 | S3 | yulin |  |

| TC-513 | syntax-reference/trigger-events | cron特殊符号 | cron非法值越界 | 边界 | cron: '70 * * * *' | 分钟超出0-59范围 | 应:拒绝或截断到边界 | cron: '70 * * * *' | schedule | 越界值 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |

| TC-514 | writing-pipelines/configure-triggers | 过滤组合 | paths满300文件 | 边界 | paths: ['src/**'] | 变更文件恰为300个 | 前300全参与匹配 | paths: ['src/**'] | push | 边界恰好不溢 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-515 | writing-pipelines/configure-triggers | 过滤组合 | paths溢出301文件 | 边界 | paths: ['src/**'] | 变更文件为301个 | 第301个不参与匹配,可能漏触发 | paths: ['src/**'] | push | 超限部分忽略 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |

| TC-516 | writing-pipelines/configure-triggers | 过滤组合 | paths空变更列表 | 边界 | paths: ['src/**'] | 无文件变更 | 不触发或退化判断 | paths: ['src/**'] | push | 空数组 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(过滤行为由平台决定是否触发),仅验文档约束 | S5 | chaoran |  |

| TC-517 | writing-pipelines/configure-triggers | 过滤组合 | paths与paths-ignore同用 | 边界 | - | 两者同时声明 | 应:YAML解析报错,互斥 | paths+paths-ignore | push | 文档明示互斥 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |

| TC-518 | concurrency | 并发控制 | QUEUE队列满 | 边界 | exceed-action: QUEUE | 队列已满新任务 | 应:排队等待,后续可能延迟 | exceed-action: QUEUE | any | 队列上限 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |

| TC-519 | concurrency | 并发控制 | IGNORE丢弃 | 边界 | exceed-action: IGNORE | 并发已满新任务 | 应:直接丢弃,不排队 | exceed-action: IGNORE | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | suite-4 | S8 | chenqi |  |

| TC-520 | concurrency | 并发控制 | CANCEL抢占 | 边界 | exceed-action: CANCEL | 并发已满新任务 | 应:取消旧任务执行新的 | exceed-action: CANCEL | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-521 | concurrency | 并发控制 | max=1单并发 | 边界 | max: 1 | max设为最小值1 | 严格串行,无并发 | max: 1 | any | 边界值 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-522 | concurrency | 并发控制 | max=0非法值 | 边界 | max: 0 | max设为0 | 应:拒绝配置或视为无限 | max: 0 | any | 越界值 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-D | liyanghang |  |

| TC-523 | concurrency | 并发控制 | enable=false禁用 | 边界 | enable: false | 显式禁用并发控制 | 应:不限制并行数 | enable: false | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-524 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix空数组 | 边界 | matrix: {os: []} | 矩阵变量值为空数组 | 应:不生成实例或解析报错 | matrix: {os: []} | any | 空矩阵 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-D | liyanghang |  |

| TC-525 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix单值变量 | 边界 | matrix: {os: [ubuntu]} | 变量仅1个值 | 应:生成1个实例 | matrix: {os: [ubuntu]} | any | 退化非矩阵 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-526 | writing-pipelines/configure-matrix-builds | 矩阵构建 | matrix三维展开 | 边界 | matrix: {os,arch,node} | 三维变量组合 | 应:笛卡尔积生成n1xn2xn3实例 | matrix: {os,arch,node} | any | 维度上限 | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 三维展开需专用三维矩阵 workflow 才能观察实例总数,当前 job 仅有二维矩阵 | Tier-A | liyanghang |  |

| TC-527 | writing-pipelines/configure-matrix-builds | 矩阵构建 | include无基础变量 | 边界 | include: [{x: 1}] | include变量未在matrix定义 | 应:include独立成实例或追加 | include: [{x: 1}] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: include 独立成实例需专用无基础矩阵变量的 workflow,无法在有基础变量的矩阵中验证 | Tier-A | liyanghang |  |

| TC-528 | writing-pipelines/configure-matrix-builds | 矩阵构建 | exclude全排除 | 边界 | exclude: [全部组合] | exclude排除所有组合 | 应:0实例,workflow不执行 | exclude: [全部] | any | 空矩阵 | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | Tier-A | liyanghang |  |

| TC-529 | writing-pipelines/configure-matrix-builds | 矩阵构建 | runs-on引用不存在变量 | 边界 | runs-on: ${{matrix.x}} | matrix未定义该变量 | 应:解析报错或空值 | runs-on: ${{matrix.x}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-530 | core-concepts/variables-secrets-context-expressions | secrets安全 | 引用未定义secret | 边界 | secrets.NOT_EXIST | 引用未在界面配置的secret | 应:返回空串而非报错 | env: {T: ${{secrets.NOT_EXIST}}} | any | 安全降级 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S1 | yulin |  |

| TC-531 | core-concepts/variables-secrets-context-expressions | secrets安全 | secret名含连字符 | 边界 | secrets.my-secret | secret名含连字符 | 应:正常访问 | ${{secrets.my-secret}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-532 | core-concepts/variables-secrets-context-expressions | secrets安全 | secret空值 | 边界 | secrets.EMPTY | secret配置为空串 | 应:返回空串,不报错 | ${{secrets.EMPTY}} | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S1 | yulin |  |

| TC-533 | core-concepts/variables-secrets-context-expressions | 变量优先级 | env与vars同名 | 边界 | - | env和vars同名变量 | 应:env覆盖vars | - | any | env>vars规则 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(vars需在AtomGit平台界面定义同名变量才可对比,无法从shell内部独立验证覆盖结果),仅验语法声明 | S2 | yulin |  |

| TC-534 | core-concepts/variables-secrets-context-expressions | 变量优先级 | vars与系统变量同名 | 边界 | - | vars与ATOMGIT_*同名 | 应:vars覆盖系统变量 | - | any | vars>系统变量 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 难真测(vars需在AtomGit平台界面定义与系统变量同名的vars才可对比),仅验语法声明 | S2 | yulin |  |

| TC-535 | core-concepts/variables-secrets-context-expressions | 变量优先级 | secrets与vars同名 | 边界 | - | secrets与vars同名 | 应:独立命名空间互不影响 | - | any | 不同空间 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 难真测(secrets和vars均需平台界面定义同名项才可验证独立性),仅验语法声明 | S13 | yulin |  |

| TC-536 | syntax-reference/expressions | 字面量 | 布尔false | 边界 | ${{ false }} | 字面量false求值 | 返回false | ${{ false }} | any | 与true对称 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-537 | syntax-reference/expressions | 字面量 | 浮点数3.14 | 边界 | ${{ 3.14 }} | 浮点数字面量 | 返回3.14,支持小数 | ${{ 3.14 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-538 | syntax-reference/expressions | 字面量 | 字符串单引号 | 边界 | ${{ 'hello' }} | 字符串字面量 | 返回hello | ${{ 'hello' }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-539 | syntax-reference/expressions | 字面量 | 整数42 | 边界 | ${{ 42 }} | 整数字面量 | 返回42 | ${{ 42 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |

| TC-540 | syntax-reference/expressions | 运算符 | !=不等于 | 边界 | ${{ a != b }} | 不等于运算符 | a不等于b时true | ${{ atomgit.event_name != 'schedule' }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-541 | syntax-reference/expressions | 运算符 | >=大于等于 | 边界 | ${{ a >= b }} | 大于等于运算符 | a大于或等于b时true | ${{ matrix.version >= 12 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-542 | syntax-reference/expressions | 运算符 | <=小于等于 | 边界 | ${{ a <= b }} | 小于等于运算符 | a小于或等于b时true | ${{ inputs.count <= 10 }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-543 | syntax-reference/expressions | 函数 | contains子串匹配 | 边界 | ${{ contains(s, item) }} | contains字符串子串 | 包含子串时true | ${{ contains(atomgit.ref, 'release') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-544 | syntax-reference/expressions | 函数 | contains数组匹配 | 边界 | ${{ contains(arr, item) }} | contains数组元素 | 包含该元素时true | ${{ contains(matrix.os, 'ubuntu') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-545 | syntax-reference/expressions | 函数 | startsWith区分大小写 | 边界 | ${{ startsWith(s, p) }} | startsWith大小写敏感 | 大写小写不匹配 | ${{ startsWith(atomgit.ref, 'refs/tags/') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-546 | syntax-reference/expressions | 函数 | format多占位符 | 边界 | ${{ format({0}{1}, a, b) }} | format多参数替换 | 按0,1...顺序替换 | ${{ format('{0}:{1}', 'img', 'v1') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-547 | syntax-reference/expressions | 函数 | substring截取 | 边界 | ${{ substring(s, 0, 7) }} | substring截取子串 | 从start截取len长度 | ${{ substring(atomgit.sha, 0, 7) }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-548 | syntax-reference/expressions | 函数 | replace替换 | 边界 | ${{ replace(s, old, new) }} | replace字符串替换 | 替换old为new | ${{ replace(atomgit.ref, 'refs/heads/', '') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-549 | syntax-reference/expressions | 函数 | toJson序列化 | 边界 | ${{ toJson(obj) }} | toJson对象转JSON | 返回JSON字符串 | ${{ toJson(atomgit.event) }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-550 | syntax-reference/expressions | 函数 | hashFiles多路径 | 边界 | ${{ hashFiles(a, b) }} | hashFiles多路径哈希 | 返回组合SHA256 | ${{ hashFiles('src/**', 'package.json') }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | UNKNOWN |  | Tier-A | liyanghang |  |

| TC-551 | syntax-reference/workflow-commands | 工作流命令 | 废弃set-output格式 | 边界 | ::set-output name=k::v | 使用废弃旧格式 | 应:兼容但建议用新格式 | echo '::set-output name=k::v' | any | 文档标注废弃 | — | — | —(仅可经Job日志断言) | A 可真测 | 用例不当 | SKIP: 难真测(废弃格式::set-output::兼容性由平台决定,shell内部无法验证平台是否处理),仅验语法声明 | Tier-A | liyanghang |  |

| TC-552 | syntax-reference/workflow-commands | 工作流命令 | 废弃set-env格式 | 边界 | ::set-env name=K::V | 使用废弃set-env | 应:兼容但建议用$ATOMGIT_ENV | echo '::set-env name=K::V' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL（命令未被解析，原样输出；DYNAMIC_VAR未被设置为环境变量，不具备向后兼容性） | SKIP: 难真测(废弃格式::set-env::兼容性由平台决定,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi |  |

| TC-553 | syntax-reference/workflow-commands | 工作流命令 | 废弃add-path格式 | 边界 | ::add-path::/p | 使用废弃add-path | 应:兼容但建议用$ATOMGIT_PATH | echo '::add-path::/p' | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL（命令未被解析，原样输出；DYNAMIC_VAR未被设置为环境变量，不具备向后兼容性） | SKIP: 难真测(废弃格式::add-path::兼容性由平台决定,shell内部无法验证平台是否处理),仅验语法声明 | S7 | chenqi |  |

| TC-554 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_OUTPUT空值 | 边界 | echo k= >> $ATOMGIT_OUTPUT | 写入空值到输出 | 应:键为空,后续可读 | echo 'k=' >> $ATOMGIT_OUTPUT | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-555 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_OUTPUT键重复 | 边界 | - | 同名键多次写入 | 应:后写覆盖前值 | echo k=v1 then k=v2 | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-556 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_ENV跨Job失效 | 边界 | - | env仅当前Job后续step可用 | 跨Job不可见,需outputs传递 | echo K=V >> $ATOMGIT_ENV | any | 作用域边界 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-557 | syntax-reference/workflow-commands | 工作流命令 | ATOMGIT_PATH重复添加 | 边界 | - | PATH多次添加同目录 | 应:可能重复,建议幂等 | echo /p >> $ATOMGIT_PATH | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-558 | writing-pipelines/configure-triggers | 触发配置 | branches与branches-ignore同用 | 边界 | - | 两者同时声明 | 应:YAML解析报错,互斥 | branches+branches-ignore | push | 文档明示互斥 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |

| TC-559 | writing-pipelines/configure-triggers | 触发配置 | tags与tags-ignore同用 | 边界 | - | 两者同时声明 | 应:YAML解析报错,互斥 | tags+tags-ignore | push | 互斥 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |

| TC-560 | writing-pipelines/configure-triggers | 触发配置 | pull_request types非法值 | 边界 | types: [invalid] | types取非法值 | 应:拒绝,仅[merge,open,reopen,update] | types: [invalid] | pull_request | 越界 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S4 | chaoran |  |

| TC-561 | writing-pipelines/configure-triggers | 触发配置 | pull_request types含merge | 边界 | types: [merge] | types显式含merge | 合并PR时触发 | types: [merge] | pull_request | merge不在默认列表 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 当前事件=Push,非pull_request,无法验证PR types含merge | S4 | chaoran |  |

| TC-562 | writing-pipelines/configure-triggers | 触发配置 | schedule非默认分支 | 边界 | - | 在非默认分支定义schedule | 应:不触发(仅默认分支生效) | schedule: [{cron}] | schedule | 文档明示限制 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S3 | yulin |  |

| TC-563 | writing-pipelines/configure-triggers | 触发配置 | schedule调度延迟 | 边界 | - | 定时触发存在数分钟延迟 | 应:容忍数分钟延迟,不精确到秒 | - | schedule | 文档明示延迟 | — | — | —(仅可经Job日志断言) | C 难真测 | FAIL | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S3 | yulin |  |

| TC-564 | writing-pipelines/configure-triggers | 触发配置 | workflow_call嵌套第3层 | 边界 | uses: ./deep.yml | 可重用工作流嵌套超过2层 | 应:拒绝执行,最多2层 | uses: ./deep.yml | workflow_call | 文档明示上限 | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S4 | chaoran |  |

| TC-565 | writing-pipelines/configure-triggers | 触发配置 | 否定模式单独使用 | 边界 | branches: [!main] | 仅否定模式无肯定模式 | 应:workflow不触发 | branches: [!main] | push | 文档明示约束 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |

| TC-566 | syntax-reference/context | atomgit上下文属性 | atomgit.sha完整性 | 边界 | ${{ atomgit.sha }} | sha应为完整40字符 | 返回完整SHA而非截断 | ${{ atomgit.sha }} | any | 长度边界 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-567 | syntax-reference/context | atomgit上下文属性 | atomgit.ref格式 | 边界 | ${{ atomgit.ref }} | ref应含refs/前缀 | 返回refs/heads/main或refs/tags/v1 | ${{ atomgit.ref }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-568 | syntax-reference/context | atomgit上下文属性 | atomgit.ref_name无前缀 | 边界 | ${{ atomgit.ref_name }} | ref_name不含refs/前缀 | 返回main或v1 | ${{ atomgit.ref_name }} | any | 与ref区分 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-569 | syntax-reference/context | atomgit上下文属性 | atomgit.run_id唯一性 | 边界 | ${{ atomgit.run_id }} | 每次运行run_id唯一 | 返回唯一运行编号 | ${{ atomgit.run_id }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | FAIL | FAIL | Tier-A | liyanghang |  |

| TC-570 | syntax-reference/context | atomgit上下文属性 | atomgit.actor非空 | 边界 | ${{ atomgit.actor }} | actor应为触发用户名 | 返回用户名,非空 | ${{ atomgit.actor }} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-1 | Tier-A | liyanghang |  |

| TC-571 | runner-management/selecting-runner-labels | 标签选择 | runs-on无匹配标签 | 边界 | runs-on: [nonexistent] | 指定不存在标签 | 应:排队等待或失败 | runs-on: [nonexistent] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |

| TC-572 | runner-management/selecting-runner-labels | 标签选择 | runs-on空标签数组 | 边界 | runs-on: [] | 空标签数组 | 应:拒绝配置或匹配任意 | runs-on: [] | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |

| TC-573 | runner-management/selecting-runner-labels | 标签选择 | runs-on单标签 | 边界 | runs-on: [ubuntu-latest] | 仅1个标签 | 应:匹配该标签Runner | runs-on: [ubuntu-latest] | any | 最小组合 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | 正确不通过 | Tier-A | liyanghang |  |

| TC-574 | runner-management/configuring-images-toolchains | 镜像工具链 | container不存在镜像 | 边界 | image: nonexistent:latest | 指定仓库中不存在的镜像 | 应:拉取失败,Job失败 | image: nonexistent:latest | any |  | — | — | —(仅可经Job日志断言) | C 难真测 | SKIP | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S5 | chaoran |  |

| TC-575 | runner-management/configuring-images-toolchains | 镜像工具链 | container镜像无tag | 边界 | image: ubuntu | 镜像名无tag | 应:使用默认latest或报错 | image: ubuntu | any |  | — | — | —(仅可经Job日志断言) | C �干细胞真测 | PASS | SKIP: 难真测(外部Action/凭据/镜像/外部资源),仅验语法声明 | S5 | chaoran |  |

| TC-576 | writing-pipelines/pass-output-between-jobs | 输出传递 | outputs跨Job空值 | 边界 | - | 前置Job输出为空 | 应:后续Job读取为空,不报错 | - | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | SKIP | SKIP: 难真测(跨Job空值行为需在后续Job中观察needs引用结果,步骤内无法自验证),仅验语法声明 | Tier-A | liyanghang |  |

| TC-577 | writing-pipelines/pass-output-between-jobs | 输出传递 | outputs跨Job未声明 | 边界 | ${{needs.build.outputs.not_exist}} | 引用未声明的output | 应:返回空或报错 | ${{needs.build.outputs.not_exist}} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-4 | Tier-A | liyanghang |  |

| TC-578 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs引用不存在Job | 边界 | needs: [nonexistent] | 依赖不存在的Job | 应:解析报错 | needs: [nonexistent] | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-579 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs循环依赖 | 边界 | a needs b, b needs a | Job循环依赖 | 应:解析报错,检测到环 | a needs b, b needs a | any | 拓扑环 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-580 | writing-pipelines/configure-dependencies-order | 任务依赖 | needs自依赖 | 边界 | a needs a | Job依赖自己 | 应:解析报错 | a needs a | any |  | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-581 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs type=非string | 边界 | type: integer | inputs声明非string类型 | 应:拒绝,仅支持string | inputs: {x: {type: integer}} | workflow_dispatch | 文档明示限制 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-582 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs无required无default | 边界 | - | 既无required也无default | 应:取空串或报错 | - | workflow_dispatch | 缺省边界 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-583 | core-concepts/variables-secrets-context-expressions | inputs变量 | inputs required传空串 | 边界 | - | 必填参数传空字符串 | 应:视为已传(空串)还是未传 | - | workflow_dispatch | 空串边界 | — | — | —(仅可经Job日志断言) | C 难真测 | PASS | SKIP: 测不动(平台侧校验/UI人工/外部仓库),仅验文档约束 | S16 | liyanghang |  |

| TC-584 | writing-pipelines/workflow-file-location-structure | stages机制 | stages空 | 边界 | stages: {} | stages为空 | 应:不执行任何stage | stages: {} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-585 | writing-pipelines/workflow-file-location-structure | stages机制 | stages单stage单job | 边界 | - | 仅1个stage含1个job | 应:正常执行,退化普通workflow | - | any | 最小形态 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-586 | writing-pipelines/workflow-file-location-structure | post机制 | post run_always=false | 边界 | run_always: false | 显式关闭run_always | 应:仅成功时执行post | run_always: false | any | 与默认true对比 | status | run.status | 无论 SUCCESS/FAILED 都执行 | B API字段 | PASS |  | Tier-B | liyanghang |  |

| TC-587 | writing-pipelines/workflow-file-location-structure | post机制 | post无steps | 边界 | post: {} | post段为空 | 应:正常,post跳过 | post: {} | any | 空边界 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS |  | Tier-A | liyanghang |  |

| TC-588 | security-permissions | permissions快捷 | permissions空对象 | 边界 | permissions: {} | permissions为空对象 | 应:所有权限none(最小权限) | permissions: {} | any |  | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-589 | security-permissions | permissions快捷 | permissions write-all | 边界 | permissions: write-all | 快捷语法write-all | 应:所有权限write | permissions: write-all | any | 与read-all对称 | — | — | —(仅可经Job日志断言) | A 可真测 | PASS | suite-2 | Tier-A | liyanghang |  |

| TC-590 | security-permissions | permissions项 | permissions非法值 | 边界 | repository: invalid | 权限值非法 | 应:拒绝,仅read/write/none | repository: invalid | any | 越界值 | — | — | —(仅可经Job日志断言) | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-591 | action-development/action-yml-metadata-syntax | action.yml元数据 | action.yml文件名 | 边界 | action.yml | 文件名必须为action.yml,大小写敏感 | 应:非action.yml名不被识别;Action.yml被拒 | - | any | 文档明示大小写敏感 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-592 | action-development/action-yml-metadata-syntax | action.yml元数据 | action.yml格式YAML | 边界 | - | 文件必须为YAML格式 | 应:非YAML格式解析报错 | - | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-593 | action-development/action-yml-metadata-syntax | action.yml元数据 | name字段必需 | 边界 | name: 'codecheck' | name字段必需 | 应:缺name平台报错 | name: 'codecheck' | any | 顶级字段必需 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-594 | action-development/action-yml-metadata-syntax | action.yml元数据 | version字段必需 | 边界 | version: '1.0.0' | version字段必需,语义化版本 | 应:缺version报错,非X.Y.Z报错 | version: '1.0.0' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-595 | action-development/action-yml-metadata-syntax | action.yml元数据 | author字段必需 | 边界 | author: 'XXX' | author字段必需 | 应:缺author报错 | author: 'XXX' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-596 | action-development/action-yml-metadata-syntax | action.yml元数据 | description字段必需 | 边界 | description: '样例插件' | description字段必需 | 应:缺description报错 | description: '样例插件' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-597 | action-development/action-yll-metadata-syntax | action.yml元数据 | inputs字段必需 | 边界 | inputs: {key_input: {...}} | inputs字段必需 | 应:缺inputs报错 | inputs: {key_input: {required: true}} | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-598 | action-development/action-yml-metadata-syntax | action.yml元数据 | outputs字段必需 | 边界 | outputs: {record_id: {...}} | outputs字段必需 | 应:缺outputs报错 | outputs: {record_id: {description: 'id'}} | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-599 | action-development/action-yml-metadata-syntax | action.yml元数据 | runs字段必需 | 边界 | runs: {using: 'node16', main: 'dist/main.js'} | runs字段必需 | 应:缺runs报错 | runs: {using: 'node16', main: 'dist/main.js'} | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-600 | action-development/top-level-fields | runs执行方式 | runs.using=node16 | 边界 | using: 'node16' | 指定node16运行时 | 应:用Node.js 16执行编译后js | using: 'node16' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-601 | action-development/top-level-fields | runs执行方式 | runs.using非node16 | 边界 | using: 'node20' | 指定非node16版本 | 应:拒绝,仅支持node16 | using: 'node20' | any | 越界值 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-602 | action-development/top-level-fields | runs执行方式 | runs.main入口文件 | 边界 | main: 'dist/main.js' | 指定main入口 | 应:执行该js文件 | main: 'dist/main.js' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-603 | action-development/top-level-fields | runs执行方式 | runs.main不存在文件 | 边界 | main: 'dist/notexist.js' | main指向不存在文件 | 应:运行时报错 | main: 'dist/notexist.js' | any |  |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-604 | action-development/top-level-fields | runs执行方式 | runs.post清理入口 | 边界 | post: 'dist/stop.js' | 指定post入口 | 应:Action终止时执行清理 | post: 'dist/stop.js' | any | 可选字段 |  |  |  | C 难真测 | PASS |  | S17 | liyanghang |  |

| TC-605 | action-development/top-level-fields | post触发机制 | post主动停止触发 | 边界 | - | 用户点击停止流水线 | 应:调度服务主动调用post | - | any | 文档明示 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-606 | action-development/top-level-fields | post触发机制 | post自然调用+SIGINT | 边界 | process.on('SIGINT') | 插件运行完成后自动调用 | 应:需在main监听SIGINT并调用post | - | any | 需代码配合 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-607 | action-development/top-level-fields | inputs命名规则 | input_id字母开头 | 边界 | key_input: {...} | input_id以字母或_开头 | 应:合法,被接受 | key_input: {required: true} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-608 | action-development/top-level-fields | inputs命名规则 | input_id含非法字符 | 边界 | key-input!: {...} | input_id含!等非法字符 | 应:拒绝,仅允许字母数字-_ | key-input!: {required: true} | any | 越界值 |  |  |  | D 测不动 | PASS |  | Tier-D | liyanghang |  |

| TC-609 | action-development/top-level-fields | inputs命名规则 | INPUT_环境变量注入 | 边界 | INPUT_KEY_INPUT | 输入转大写,空格替_ | 应:运行时$INPUT_KEY_INPUT可读 | inputs: {key input: {default: test}} | any | 大写转换 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-610 | action-development/top-level-fields | inputs校验 | required=true未传 | 边界 | required: true | 必填输入未传值 | 应:平台不自动报错,需代码主动校验 | - | any | 文档明示行为 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-611 | action-development/top-level-fields | inputs校验 | default默认值 | 边界 | default: test | 未指定输入用default | 应:运行时取default值 | inputs: {x: {default: test}} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-612 | action-development/top-level-fields | outputs声明 | output_id唯一 | 边界 | record_id: {...} | output_id唯一标识符 | 应:重复id报错 | outputs: {record_id: {description: 'id'}} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-613 | action-development/top-level-fields | outputs声明 | output_id命名规则 | 边界 | record-id: {...} | output_id命名规则同input | 应:字母/_开头,含字母数字-_ | outputs: {record-id: {description: 'id'}} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-614 | action-development/action-yml-metadata-syntax | 版本号规范 | 版本号X.Y.Z格式 | 边界 | version: '1.0.0' | 语义化版本格式 | 应:合法被接受 | version: '1.0.0' | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-615 | action-development/action-yml-metadata-syntax | 版本号规范 | 版本号不可回退 | 边界 | version: '0.9.0' | 版本号低于已发布 | 应:拒绝,版本只能新增 | - | any | 文档明示 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-616 | action-development/action-yll-metadata-syntax | 版本号规范 | 版本号含字母特殊字符 | 边界 | version: '1.0.0a' | 版本号含字母 | 应:拒绝,仅数字和点 | version: '1.0.0a' | any | 越界值 |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-617 | action-development/action-yml-metadata-syntax | 版本号规范 | 预发布版本标识 | 边界 | version: '1.0.0-alpha' | 预发布版本alpha/beta/rc | 应:合法被接受 | version: '1.0.0-alpha' | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-618 | action-development/action-yml-metadata-syntax | 文件名规范 | Action.yml大写A | 边界 | Action.yml | 文件名大写A开头 | 应:拒绝,大小写敏感仅action.yml | - | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-619 | action-development/runtime-environment-variables | 运行时环境变量 | INPUT_变量注入 | 边界 | $INPUT_KEY_INPUT | 输入参数转环境变量 | 应:运行时可读 | echo $INPUT_KEY_INPUT | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-620 | action-development/runtime-environment-variables | 运行时环境变量 | ATOMGIT_系统变量 | 边界 | $ATOMGIT_SHA | Action内可读系统变量 | 应:与workflow同源,可读 | echo $ATOMGIT_SHA | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-621 | action-development/plugin-security-specification | Action安全规范 | 敏感数据禁硬编码 | 边界 | - | 敏感数据禁止硬编码 | 应:必须通过secrets输入 | - | any | 文档明示 |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |

| TC-622 | action-development/plugin-security-specification | Action安全规范 | 敏感数据加密存储 | 边界 | - | 敏感数据必须加密存储 | 应:运行期加密,及时清理 | - | any |  |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |

| TC-623 | action-development/plugin-security-specification | Action安全规范 | 输入参数须验证 | 边界 | - | 所有输入参数须严格验证 | 应:代码层校验输入合法性 | - | any |  |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |

| TC-624 | action-development/plugin-packaging | Action打包 | package.json构建 | 边界 | package.json | 通过package.json构建编排 | 应:构建命令打出可执行js | - | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-625 | action-development/plugin-packaging | Action打包 | dist/可执行js | 边界 | dist/main.js | 构建产物为dist/下可执行js | 应:runs.main指向dist/内文件 | dist/main.js | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-626 | action-development/plugin-project-structure | Action项目结构 | 插件目录结构 | 边界 | - | 插件项目目录结构规范 | 应:含action.yml/src/dist/package.json | - | any |  |  |  |  | C 难真测 |  |  | S17 | liyanghang |  |

| TC-627 | writing-pipelines/using-actions | Action调用 | uses本地路径引用 | 边界 | uses: ./.github/actions/my-action | 引用本地Action | 应:执行仓库内该路径的action.yml | uses: ./.github/actions/my-action | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-628 | writing-pipelines/using-actions | Action调用 | uses带版本@ | 边界 | uses: actions/checkout@v3 | 引用指定版本Action | 应:执行该版本 | uses: actions/checkout@v3 | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

| TC-629 | writing-pipelines/using-actions | Action调用 | uses with传参 | 边界 | with: {key_input: value} | 向Action传输入参数 | 应:参数转INPUT_KEY_INPUT环境变量 | with: {key_input: value} | any |  |  |  |  | A 可真测 |  |  | Tier-A | liyanghang |  |

</details>

---

## 输入

- **A**: gitcode action文档
- **B**: https://docs.gitcode.com/docs/help/home/org_project/pipeline/
- **A**: github action 安全最佳实践
- **B**: https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
- **A**: github runner 历史问题
- **B**: onebox
- **A**: 所有社区 规格
- **B**: 待补充
- **A**: 其他产品遇到的问题
- **B**: onebox
- **A**: 优化措施 验证（缓存 + karmada）
- **B**: 待补充
- **A**: icsl 安全整改
- **B**: 待补充 md
- **A**: ascend 社区 需要的action
- **B**: onebox
- **A**: 稳定性用例
- **B**: 待补充
- **A**: 易用性 （产品易用性，习惯保留性，兼容性）
---

## 按章节统计


| 文档章节 | 用例数 |
|---|---|
| 文档章节 | 用例数 |
| action-development | 6 |
| action-development/action-yll-metadata-syntax | 2 |
| action-development/action-yml-metadata-syntax | 12 |
| action-development/plugin-packaging | 2 |
| action-development/plugin-project-structure | 1 |
| action-development/plugin-security-specification | 3 |
| action-development/runtime-environment-variables | 2 |
| action-development/top-level-fields | 14 |
| concurrency | 11 |
| core-concepts/artifacts-and-cache | 5 |
| core-concepts/runner-and-environment | 3 |
| core-concepts/trigger-events | 29 |
| core-concepts/variables-secrets-context-expressions | 25 |
| core-concepts/workflow-job-step-action | 12 |
| examples/go-ci | 5 |
| examples/java-gradle-ci | 2 |
| examples/java-maven-ci | 2 |
| examples/nodejs-ci | 2 |
| examples/pr-code-check-example | 4 |
| examples/python-ci | 9 |
| runner-management/configuring-images-toolchains | 5 |
| runner-management/selecting-runner-labels | 8 |
| runner-management/using-hosted-runners | 3 |
| runner-management/using-self-hosted-runners | 4 |
| running-pipelines | 4 |
| security-permissions | 9 |
| syntax-reference/context | 148 |
| syntax-reference/expressions | 48 |
| syntax-reference/runner-images-tools | 10 |
| syntax-reference/trigger-events | 29 |
| syntax-reference/variables | 30 |
| syntax-reference/workflow-commands | 22 |
| writing-pipelines/configure-conditional-execution | 8 |
| writing-pipelines/configure-dependencies-order | 7 |
| writing-pipelines/configure-jobs | 15 |
| writing-pipelines/configure-matrix-builds | 12 |
| writing-pipelines/configure-steps | 10 |
| writing-pipelines/configure-triggers | 26 |
| writing-pipelines/pass-output-between-jobs | 5 |
| writing-pipelines/upload-download-artifacts | 7 |
| writing-pipelines/using-actions | 12 |
| writing-pipelines/using-dependency-cache | 3 |
| writing-pipelines/using-script-commands | 7 |
| writing-pipelines/using-variables-secrets | 8 |
| writing-pipelines/workflow-file-location-structure | 38 |
| 合计 | 629 |
---

## 按分类统计


| 测试分类 | 用例数 |
|---|---|
| 测试分类 | 用例数 |
| 上下文可用性表 | 55 |
| ATOMGIT_*系统变量 | 27 |
| atomgit上下文属性 | 25 |
| 工作流命令 | 22 |
| 函数 | 20 |
| 触发配置 | 18 |
| cron特殊符号 | 14 |
| pull_request事件字段 | 14 |
| push事件字段 | 13 |
| 触发事件完整列表 | 13 |
| Jobs配置 | 12 |
| 工作流结构 | 12 |
| 矩阵构建 | 12 |
| 运算符 | 12 |
| 上下文总览 | 11 |
| 并发控制 | 11 |
| Steps配置 | 10 |
| 字面量 | 10 |
| Action插件 | 9 |
| Python示例 | 9 |
| action.yml元数据 | 9 |
| issue_comment事件字段 | 9 |
| 基本结构字段 | 9 |
| Runner标签 | 8 |
| inputs变量 | 8 |
| 条件执行 | 8 |
| 标签选择 | 8 |
| permissions项 | 7 |
| 任务依赖 | 7 |
| 制品管理 | 7 |
| Action插件开发 | 6 |
| runner上下文 | 6 |
| secrets安全 | 6 |
| stages机制 | 6 |
| 命名建议 | 6 |
| 安全与权限 | 6 |
| 触发事件类型 | 6 |
| 过滤组合 | 6 |
| Go示例 | 5 |
| cron位置 | 5 |
| issue_comment | 5 |
| permissions快捷 | 5 |
| runs执行方式 | 5 |
| 制品与缓存 | 5 |
| 变量优先级 | 5 |
| 表达式示例 | 5 |
| 输出传递 | 5 |
| 镜像工具链 | 5 |
| PR检查示例 | 4 |
| env变量 | 4 |
| post机制 | 4 |
| schedule | 4 |
| secrets变量 | 4 |
| steps上下文 | 4 |
| 否定模式 | 4 |
| 文件位置 | 4 |
| 版本号规范 | 4 |
| 自托管Runner | 4 |
| 运行流水线 | 4 |
| Action安全规范 | 3 |
| Action调用 | 3 |
| Runner运行环境 | 3 |
| inputs命名规则 | 3 |
| pull_request_target | 3 |
| secrets上下文 | 3 |
| vars变量 | 3 |
| 依赖缓存 | 3 |
| 托管Runner | 3 |
| 矩阵策略 | 3 |
| 脚本执行 | 3 |
| Action打包 | 2 |
| Java Gradle示例 | 2 |
| Java Maven示例 | 2 |
| Node.js示例 | 2 |
| Runner镜像 | 2 |
| env上下文 | 2 |
| inputs校验 | 2 |
| job上下文 | 2 |
| matrix上下文 | 2 |
| outputs声明 | 2 |
| post触发机制 | 2 |
| pull_request_comment | 2 |
| 多行输出 | 2 |
| 引用方式 | 2 |
| 系统变量补充 | 2 |
| 运行时环境变量 | 2 |
| Action项目结构 | 1 |
| PR types默认 | 1 |
| PR目标分支 | 1 |
| inputs type规格 | 1 |
| schedule事件字段 | 1 |
| workflow_call | 1 |
| workflow_dispatch事件字段 | 1 |
| 优先级总览 | 1 |
| 多事件组合 | 1 |
| 文件名规范 | 1 |
| 脚本命令 | 1 |
| 脱敏命令 | 1 |
| 运算符优先级 | 1 |
| 合计 | 629 |