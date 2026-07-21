# GitCode 文档契约测试规则

## 1. 目的

本工程验证 GitCode 官方文档描述的能力是否真实可用。测试对象是“文档契约”，不是 GitHub Actions 兼容性，也不是探索平台可能存在但文档未描述的替代能力。

本规则适用于后续全部 S1、S2、S3、S13 测试和其他 GitCode Actions 能力验证。

## 2. 唯一依据

测试需求和实现依据按以下优先级使用：

1. 测试仓 `LiYanghang00/demo` 中的 `gitcode-docs/`，作为 GitCode 官方文档本地快照和唯一语法、语义来源。
2. `gitcode-pipeline-test-cases.xlsx`，用于确定 TC 范围、测试目标和预期结果。
3. GitCode 平台的 Run、Job、Step、日志、设置页面和 API 原始响应，作为实际行为证据。

以下内容不能作为能力契约来源：

- GitHub Actions、GitLab CI、Gitee Go 或其他 CI 平台的经验。
- 本地 `S1/`、`S2/`、`S3/`、`S13/` 目录中的旧计划、旧记录和旧证据。
- Workflow 中自行打印的 `PASS`、`FAIL`、`BLOCKED` 文本。
- 文件名、Job 名、Step 名或 YAML 被仓库接受这一事实。
- 无官方文档依据的替代变量、替代语法、兼容性写法和推测性解释。

## 3. 核心判定原则

### 3.1 PASS

同时满足以下条件才可判定 `PASS`：

1. YAML 严格使用 `gitcode-docs/` 明确给出的语法和引用方式。
2. 文档明确要求的界面资源、权限和触发条件已配置。
3. 平台实际行为符合文档和 Excel 预期。
4. 存在可复核的 Run、Job、Step、日志、设置页面或 API 证据。

### 3.2 FAIL

满足任一条件即判定 `FAIL`：

1. 严格按文档编写并满足前置条件后，实际行为与文档不一致。
2. 平台拒绝创建或保存文档契约要求的配置、名称或资源。
3. 文档声明某项能力，但文档提供的方法不足以实现或验证该能力。
4. Workflow 被平台识别，但文档规定的字段、上下文、环境变量、优先级、触发器或运行行为不生效。

不要为避免 FAIL 而设计文档外的替代验证。

### 3.3 BLOCKED

仅在文档明确要求的外部前置条件尚未准备时使用，例如：

- 尚未在组织或项目设置中创建文档要求的 Variable 或 Secret。
- 尚未授予文档要求的项目权限。
- 尚未创建文档要求的 MR、Tag、Environment 或 Registry。
- 观察窗口尚未结束。

资源配置完成后，必须转为实际的 PASS 或 FAIL，不能长期停留在 BLOCKED。

### 3.4 PARTIAL

只用于平台行为已发生，但文档契约要求的关键证据暂时无法取得，例如日志下载接口失败且页面日志尚未导出。

不得因为只验证了文档预期的一部分就主动增加额外对照测试；若文档本身没有给出完成完整能力验证的方法，按 3.2 判定 FAIL。

### 3.5 SKIP

原则上不使用。文档已经声明的能力不应因“难测”而 SKIP。平台不支持、拒绝配置或无法按文档实现时，应记录为 FAIL。

## 4. 开发规则

### 4.1 先定位文档原文

编写每个 TC 前必须记录：

- 官方文档文件路径。
- 可定位的标题、表格或原文。
- 文档给出的 YAML 语法。
- 文档规定的预期行为。
- 文档要求的界面配置和权限。

没有文档原文，不编写 YAML，不凭其他平台经验补全。

### 4.2 最小直接断言

每个 TC 只验证一个文档契约：

- 使用文档给出的字段和引用方式。
- 直接比较文档规定的值。
- 断言失败必须非零退出。
- 非敏感值可以输出实际值，便于复核。
- 敏感值只允许按文档要求验证掩码，不保存明文。

禁止：

- 用另一个名称替代文档要求的同名变量。
- 用固定 `echo PASS` 或 `echo FAIL` 代替断言。
- 为解释失败增加文档未描述的“读取层”“兼容层”“统一入口”等模型。
- 为证明一个文档能力而引入其他平台的惯用写法。

### 4.3 界面配置属于文档前置条件

文档要求在组织、项目、Environment 或其他设置页面创建资源时：

1. 先人工完成配置。
2. 保存设置页面截图或 API 响应。
3. 再运行 YAML。
4. 配置正确但行为不符合文档时判 FAIL。

未配置资源时的空值或失败不能直接归因于平台能力。

### 4.4 真实事件必须真实触发

| 文档能力 | 有效证据 |
| --- | --- |
| `workflow_dispatch` | Manual Run |
| `push` | Push 事件 Run |
| `pull_request` / MR | MR 事件 Run |
| Tag/Release | 对应 Tag 或 Release 事件 Run |
| `schedule` | Schedule 事件 Run |

手动运行不能替代 Push、MR、Tag 或 Schedule。

## 5. 证据规则

证据强度从高到低：

1. 平台设置或 API 的原始接受/拒绝响应。
2. Run API 的 Workflow、事件、分支、提交 SHA、时间和状态。
3. Job API 的资源、环境、步骤和状态。
4. 页面下载的原始 Job/Step 日志。
5. 已脱敏的日志摘录。

Workflow 中自行打印的结论不是证据，只有输出的实际值、平台状态和退出码才是证据。

每次执行至少记录：

```text
TC
官方文档路径与原文
Workflow 文件与提交 SHA
Run ID / Job ID
触发事件
前置配置证据
实际值和退出状态
PASS / FAIL / BLOCKED / PARTIAL
```

## 6. 当前测试能力边界

### 6.1 可以由 YAML 直接验证

- 上下文表达式是否展开为文档规定值。
- `env` 是否按文档注入 Runner，Shell 是否能通过 `$VAR` 读取。
- 非敏感 `vars` 是否能通过 `${{ vars.NAME }}` 读取。
- 系统 `ATOMGIT_*` 变量是否存在并符合文档含义。
- 同一 Workflow 内的 env 作用域和优先级。
- Shell 命令、输出、退出码和后续 Step 行为。
- 文档明确支持的 Action、容器和过程文件能力。

### 6.2 需要人工完成文档前置配置

- 组织级和项目级 Variables。
- 组织级、项目级和 Environment Secrets。
- 项目权限和组织授权。
- MR、Tag、Release、Docker Registry 等外部资源。
- 平台设置页面中的名称合法性和资源创建。

这些人工操作只负责满足文档前置条件，不用于设计额外的测试模型。

### 6.3 需要等待真实平台事件

- Schedule。
- Push、MR、Tag、Release 等事件触发。
- 调度延迟和“不触发”类规则。

观察窗口结束前不判 FAIL。窗口结束且配置始终有效但未触发，判 FAIL。

### 6.4 当前工具限制

- Run API、Job API 可读取结构化状态。
- Job 日志下载 API 可能返回 404，需要用户从页面下载日志。
- 当前没有稳定的 Workflow 列表 API。
- 仓库存在多人并发修改，测试前后必须确认目标 Workflow 始终位于 `.gitcode/workflows/`。
- 新文件可能未被平台注册；优先复用已注册过的 Workflow 文件名，但该行为本身若与文档不符，应记录为平台问题。

## 7. 已确认的 S2 文档契约

根据 `gitcode-docs/`：

1. `env:` 在 workflow、job、step 级定义后，会直接注入 Runner。
2. `run:` 中通过 `$VAR_NAME` 读取 env。
3. `${{ env.VAR_NAME }}` 用于表达式读取。
4. vars 在组织和项目设置页面创建，通过 `${{ vars.VAR_NAME }}` 读取。
5. 项目 vars 覆盖组织级同名 vars。
6. 总优先级为 `Step env > Job env > Workflow env > vars > ATOMGIT_*`。
7. 系统变量由 Runner 自动注入，`ATOMGIT_SHA` 表示触发提交 SHA。

因此：

- TC-533 中 Job env 已配置但 Shell `$SAME_NAME=UNSET`，直接违反文档，FAIL。
- TC-534 中平台拒绝创建同名 `ATOMGIT_SHA` vars，导致文档声明的 `vars > ATOMGIT_*` 无法成立，FAIL。

## 8. 执行前检查清单

- [ ] 已定位 `gitcode-docs/` 原文。
- [ ] YAML 只使用文档明确语法。
- [ ] 未引入 GitHub Actions 或其他 CI 平台假设。
- [ ] 文档前置资源已配置并留证。
- [ ] 每个 TC 有直接非零断言。
- [ ] 真实触发能力使用真实事件。
- [ ] 目标 Workflow 在整个观察窗口内保持位于 `.gitcode/workflows/`。
- [ ] 失败后没有设计文档外替代方案规避 FAIL。
- [ ] 结论已写入 `session-test-coverage-report.md`。

## 9. 已确认的 S3 文档契约结论

根据 `gitcode-docs/writing-pipelines/configure-triggers.html` 和 `gitcode-docs/syntax-reference/trigger-events.html`：

- `schedule` 使用 `on.schedule` 下的 `- cron: '<POSIX 五段式>'`。
- cron 使用 UTC。
- schedule 只在默认分支生效。
- 定时任务可能有数分钟延迟。
- 最短间隔为 5 分钟。

实测 Workflow 严格符合上述语法，位于默认分支活跃目录，Manual Run 成功证明文件已注册且可执行；但计划时间后观察超过 15 分钟仍没有任何 Schedule Run。

因此：

1. TC-237、427、430、563 直接 `FAIL`。
2. 其余 20 条依赖基础 Schedule 的间隔、分支、运算符、字段和扩展语法能力无法按文档方法验证，按统一规则 `FAIL`。
3. S3 共 24 条，全部 `FAIL`。
4. 该结论不等于逐项证明每种 cron 运算符解析错误；准确含义是基础 Scheduler 不生效，使全部 S3 文档能力不可用或不可验证。

## 10. 已确认的 S13 文档契约结论

最新证据来自已注册文件 `.gitcode/workflows/yyl-session13-workflows.yml` 的 Manual Run `7f524e67ce9f417284f606b9d9d08a55`。Run 的 `head_sha` 为 `fe9ef776a4213c79e1fb303e127978d71457273a`，该提交下的 S13 Workflow 已核对与修订提交 `c195b38` 内容一致。

1. TC-220：直接输出并精确断言 `$ATOMGIT_ACTIONS_ALLOW_UNSECURE_COMMANDS=false`。页面实际值为 `UNSET`，Step code 1，判定 `FAIL`。
2. TC-273：严格使用文档的 Job `container.image` 语法和公开固定镜像 `alpine:3.20`。Job API 保留容器配置，但平台返回“任务申请资源错误”，Step 未启动，判定 `FAIL`。
3. TC-304：`uses: checkout` 完成，随后对仓库内现存 Workflow 文件的断言完成，判定 `PASS`。
4. TC-355：第一 Step 输出无敏感内容的废弃 `set-env` 命令，第二 Step 实际值为 `TC355_PROBE=UNSET` 且断言完成，说明命令没有传播，判定 `PASS`。
5. TC-220 与 TC-355 必须分开判定：系统变量默认值缺失不影响已由两步实际行为证明的 `set-env` 禁用能力。

## 11. 已确认的 S1 环境 Secret 契约结论

TC-010 的 Excel 示例要求在 Job 中设置 `environment: prod`，以验证环境级 Secret 仅在环境匹配时可用。平台对匹配和不匹配两个最小 Job 均在语法检查阶段返回：

```text
jobs[tc_010_matching_environment].environment: unknown property
jobs[tc_010_unmatched_environment].environment: unknown property
```

官方文档 `gitcode-docs/security-permissions/using-secrets.html` 只声明环境级 Secret 可配置审批人，但没有给出 `jobs.<id>.environment` 或其他绑定环境的 YAML 语法。因此该能力无法按文档和 Excel 提供的方法实现或验证，TC-010 判定 `FAIL`。无效 Job 应从聚合 Workflow 移除，不能用其他 CI 平台字段替代。

## 12. 已确认的 S1 Secret 页面日志结论

最新页面日志证据确认：

1. TC-011、TC-100、TC-101、TC-102 输出完整 Secret 时，页面日志均显示为 `***`，且对应 Secret 非空，因此四条均判定 `PASS`。报告中不得保存 Secret 明文。
2. TC-008 的组织级 Secret 非空断言以 code 1 退出。现有证据没有证明组织 Secret 已创建并授权当前项目，因此仍判定 `BLOCKED`；只有补齐设置页面或 API 前置配置证据后再次失败，才能判定 `FAIL`。
3. TC-009 的 Job `1528540471846772736_1528540471792246793` 日志输出 `project_secret_present=true`，证明项目 Secret 在当前项目可用；由于尚无未配置同名 Secret 的对照项目证据，仍判定 `PARTIAL`。
4. TC-530 的 Job `1528540471846772736_1528540471792246807` 日志输出 `undefined_secret_empty=true` 且 Step 成功，证明未定义 Secret 展开为空，维持 `PASS`。
5. TC-443 的最新 Job `1528547518814236672_1528547518721962003` checkout `main` 后扫描 3 个 yyl Workflow，日志明确列出文件清单，并输出 `unsafe_secret_output_match_count=0`、`secret_output_audit_passed=true`；结合提交 `24050c8` 中可复核的直接表达式输出、Secret/Token 变量输出、切片和编码检查，判定 `PASS`。
6. TC-444 的最新 Job `1528547518814236672_1528547518721962005` checkout `main` 后扫描同一组 3 个 yyl Workflow，日志输出 `artifact_cache_action_count=0`、`unsafe_secret_persistence_match_count=0`、`secret_persistence_audit_passed=true`；结合提交 `24050c8` 中对 Artifact/Cache 参数和 Secret 文件写入路径的检查，证明受测 Workflow 没有 Secret 持久化配置，判定 `PASS`。

## 13. 已确认的 S13 MR / Tag / 命名空间结论

最新证据来自提交 `ddff527` 上的三次真实事件 Run：

1. TC-388 的 MR Run `d726006aee574ba3987fca6568c2d8a1`（事件 `MR`）中，TC-388 Job 以 `COMPLETED` 退出。平台通过 `on: pull_request` 触发 Workflow 后，Run API 记录事件为 `MR`，Job 成功证明 MR 事件触发能力可用，因此判定 `PASS`。
2. TC-389 的 CreateTag Run `1d0cc8e20e594847a53f21f9f3a7aeb3`（事件 `CreateTag`）中，TC-389 Job 以 `COMPLETED` 退出。平台通过 `on: push: tags: [v*]` 触发 Workflow 后，Run API 记录事件为 `CreateTag`，Job 成功证明 Tag 事件触发能力可用，因此判定 `PASS`。
3. TC-535 在上述两次 Run 中均以 `COMPLETED` 退出。测试使用同名 `YYL_TEST`（Secret 和 vars 均为 `1234`），Job 成功读取两者，Secret 非空断言通过且日志中 Secret 值被自动掩码为 `***`，vars 值直接输出为 `1234`，证明两个命名空间独立共存且均可用，因此判定 `PASS`。
4. TC-390 缺少 Docker Registry 和认证资源，文档声明了 Docker 构建与推送能力，但当前没有足够资源按文档方法完成验证；在资源到位前无法确认该能力是否实际可用，因此判定 `FAIL`。
5. TC-391 依赖 Schedule 事件触发，但基础 Scheduler 已在 S3 中确认为不工作；在与 S3 共用 Scheduler 失效证据的前提下，文档声明的每日定时构建能力不可按文档方法验证，因此判定 `FAIL`。

## 14. 已确认的组织/项目 Secret 与 Variable 结论

最新证据来自 `ComputingActionTest/bingo` 仓库的 Run `0bea150607d7401ab58c2f6e393e11a5`（事件 `Manual`，分支 `main`），Workflow 为 `yyl-blocked-tests.yml`。

前置配置：

| 资源类型 | 级别 | 名称 | 值 |
| --- | --- | --- | --- |
| Secret | 组织 | `SECRET_ORG` | `org_secret` |
| Variable | 组织 | `ORG_VAR` | `org_value` |
| Variable | 组织 | `DUP` | `org_value` |
| Variable | 项目 | `DUP` | `project_value` |
| Secret | 组织 | `DUP` | `org_secret` |
| Secret | 项目 | `DUP` | `project_secret` |

全部 5 个 Job 以 `COMPLETED` 退出：

1. TC-008 的 `secrets.SECRET_ORG` 精确值内存比较通过（`test "$SECRET_VAL" = "org_secret"`），证明组织 Secret 在组织下项目中可用，判定 `PASS`。
2. TC-005 的 `vars.ORG_VAR` 精确值断言通过（`= "org_value"`），证明组织 Variable 在组织下项目中可用，判定 `PASS`。
3. TC-007 的 `vars.DUP` 解析值为 `project_value`（而非组织级 `org_value`），证明项目 Variable 覆盖组织 Variable，判定 `PASS`。
4. TC-194 与 TC-007 测试同一覆盖关系，`vars.DUP` = `project_value` 且 != `org_value`，双重断言通过，判定 `PASS`。
5. TC-195 的 `secrets.DUP` 在存在组织级 `DUP = org_secret` 的情况下，精确值内存比较为 `project_secret` 而非 `org_secret`，证明项目 Secret 覆盖组织 Secret，判定 `PASS`。`test` 命令不输出 Secret 值到日志。

## 15. 已确认的 Job env Shell 注入失败结论

TC-533 验证文档契约：Job `env:` 定义的变量会注入 Runner 并通过 `$VAR_NAME` 在 Shell 中读取，且优先级 `env > vars`。

独立测试三次，横跨两个仓库和组织：

| 测试 | 仓库 | env 名 | Shell `$VAR` | `${{ env.VAR }}` | 结论 |
| --- | --- | --- | --- | --- | --- |
| 1 | LiYanghang00/demo | `SAME_NAME` | `UNSET` | `env_value` | 仅表达式层生效 |
| 2 | ComputingActionTest/bingo | `YYL_TEST` | `UNSET` | `env_value` | 同 1，且此场景下 `${{ vars.YYL_TEST }}` 也被遮蔽为空 |
| 3 | ComputingActionTest/bingo | `PROBE` | `UNSET` | `env_val` | 最简纯 env 测试，排除命名冲突 |

三层独立证据一致：GitCode Runner **完全不将 Job `env:` 注入 Shell 环境**。表达式层 `${{ env.VAR }}` 正常，但 Bash `$VAR` 恒为 UNSET。

此行为直接违反官方文档两处声明：

> `gitcode-docs/syntax-reference/variables.html`：在 workflow、job、step 的 `env:` 中定义的变量会直接注入 Runner，`run:` 中可通过 `$VAR_NAME` 读取。

> `gitcode-docs/writing-pipelines/using-variables-secrets.html`：总优先级 `Step env > Job env > Workflow env > vars > ATOMGIT_*`。

由于环境变量注入不生效，上述优先级链根本无法在 Runner 内部成立。TC-533 判定 `FAIL`，该判定不依赖于特定仓库、组织或变量名。

此外，测试 2 揭示了一个附带问题：env 同名时不仅 Shell 层面缺值，表达式层的 `${{ vars.VAR_NAME }}` 也返回空（而非预期的 vars 值），说明 env 不仅在注入层面失效，在表达式上下文解析层也存在非预期的遮蔽行为。
