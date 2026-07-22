# Intent Library · Run 2026-07-21-02

> 阶段A 五维度发散的汇总意图库。共 **160 条 intent**（spec 8 / compat 61 / security 33 / reliability 33 / usability 25）。
> 本文件是评审门禁 (STOP①) 的工作输入。门禁将在此基础上：去重、按风险登记册定优先级、对照 Parity Matrix 查盲区，并回标「准入/打回」列。
> **状态**：待门禁（门禁结论见 `gate-log.md`，回标后本表「门禁」列更新）。

## 汇总统计

| 维度来源 | intent 数 | ID 前缀 |
|---|---|---|
| 规格验证 (spec-analyst) | 8 | INTENT-COMP-* |
| 兼容性 (compat-diff) | 61 | INTENT-COMPAT-* |
| 安全性 (security) | 33 | INTENT-SEC-* |
| 稳定性 (reliability) | 33 | INTENT-REL-* |
| 易用性 (usability) | 25 | INTENT-USE-* |
| **合计** | **160** | — |

## 意图清单（按维度分组）

> 「门禁」列初始为 `待定`，STOP① 后回标 `准入` / `打回(原因)` / `合并→母ID`。

### 规格验证 (spec-analyst)（8 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-COMP-001 | [completeness, reliability] | 验证托管 Runner 声明的 6 档规格与实际可用性一致（尤其 large 及以上「需申请」） | 无法对齐（risk-register 模板态）；价值在于坐实容量声明，建议门禁据 | — | 待定 |
| INTENT-COMP-002 | [completeness, reliability] | 验证 concurrency.max 声明的取值范围 1-5 与越界拒绝行为 | 无法对齐（risk-register 模板态）；testing-focus §1 | — | 待定 |
| INTENT-COMP-003 | [completeness, reliability] | 验证 paths 过滤「仅匹配前 300 个变更文件」的边界声明 | 无法对齐（risk-register 模板态）；testing-focus §2 | — | 待定 |
| INTENT-COMP-004 | [completeness, compatibility] | 验证 workflow_call 嵌套「最多 2 层」的声明与超限拒绝 | 无法对齐（risk-register 模板态）；testing-focus §7 | 差异确认（GitCode 显式限 2 层，GitHub 上限不同，此处仅验证 GitCode 侧声明成立） | 待定 |
| INTENT-COMP-005 | [completeness, security] | 验证 inputs「仅支持 string 类型」声明——非 string 定义的处理 | 无法对齐（risk-register 模板态）；testing-focus §1 | — | 待定 |
| INTENT-COMP-006 | [completeness, usability] | 验证 permissions:{} 的实际权限——澄清「全 none」vs「repository:read」矛盾 | 无法对齐（risk-register 模板态）；testing-focus §5 | — | 待定 |
| INTENT-COMP-007 | [completeness, reliability, usability] | 验证重跑后 ATOMGIT_RUN_ID 是否变化——澄清两文档冲突声明 | 无法对齐（risk-register 模板态）；testing-focus §9 | — | 待定 |
| INTENT-COMP-008 | [completeness, compatibility] | 验证状态函数无括号写法（success/failed/cancelled/always）为唯一合法形式 | 无法对齐（risk-register 模板态）；testing-focus §1 | 差异确认（GitCode 语法与 GitHub 有意不同，验证 GitCode 侧声明成立） | 待定 |

### 兼容性 (compat-diff)（61 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-COMPAT-001 | [compatibility, usability] | 默认 shell 差异——未声明 shell 时 GitCode 与 GitHub 的默认解释器及错误处理标志是否一致 | 关联 testing-focus §10 默认值差异 + §11 迁移摩擦；风险 | 一致性（GitCode 未声明差异，应与 GitHub `-e` 语义对齐；实测不一致即缺陷+文档缺口） | 待定 |
| INTENT-COMPAT-002 | [compatibility, security] | 未声明 permissions 时默认 TOKEN 权限差异——GitCode「仓库设置权限」vs GitHub 明确默认集 | 关联 testing-focus §5 权限 + §11；安全敏感，建议 P1。 | 差异确认（权限域命名与默认集 GitCode 有意不同） | 待定 |
| INTENT-COMPAT-003 | [compatibility, reliability] | matrix `strategy.fail-fast` 默认值差异——GitCode 未声明默认，GitHub 默认 true | 关联 testing-focus §3 matrix + §10；建议 P1（资 | 一致性（GitCode 未声明差异，应与 GitHub 默认 true 对齐；若默认不同即缺陷+缺口） | 待定 |
| INTENT-COMPAT-004 | [compatibility] | job/step `continue-on-error` 默认值与 outcome/conclusion 语义一致性 | 关联 testing-focus §3 + §10；建议 P2。关联 spec  | 一致性（GitCode 未声明差异，应与 GitHub 对齐） | 待定 |
| INTENT-COMPAT-005 | [compatibility, reliability] | job `if` 缺省状态与「needs 失败则默认不执行」语义一致性 | 关联 testing-focus §3；建议 P1。关联 spec C-EXEC | 一致性（失败传播方向）+ 差异确认（覆盖写法函数名差异，见 009） | 待定 |
| INTENT-COMPAT-006 | [compatibility] | env 变量三级优先级与 GitHub 覆盖规则一致性（step>job>workflow） | 关联 testing-focus §10 上下文；建议 P2。关联 spec C | 一致性（env 三级覆盖）+ 差异确认（env/vars 优先级合并是否 GitCode 特有） | 待定 |
| INTENT-COMPAT-007 | [compatibility, reliability] | `post` / stage `fail_fast` 等 GitCode 特有编排默认值在迁移场景的隐式行为 | 关联 testing-focus §3 + §11；建议 P1。关联 spec  | 差异确认（GitCode 特有能力，验证默认值边界 + 是否文档化） | 待定 |
| INTENT-COMPAT-008 | [compatibility, usability] | 状态函数括号差异——GitHub `success()/failure()/always()/cancelled()` vs GitCode 无括号 + failed | 关联 testing-focus §1/§10/§11；建议 P0（迁移直接断点 | 差异确认（语法有意不同） | 待定 |
| INTENT-COMPAT-009 | [compatibility, usability] | GitCode 特有 `default()` 函数——GitHub 无对应，反向迁移与语义确认 | 关联 testing-focus §10 + §11；建议 P1（生产高频 +  | 差异确认（GitCode 特有，无 GitHub 对应） | 待定 |
| INTENT-COMPAT-010 | [compatibility] | 缺失表达式函数——GitHub `join()/fromJSON()/toJSON()/hashFiles()/case()` 在 GitCode 的支持状况 | 关联 testing-focus §10；建议 P1（动态矩阵是常见高级用法）。 | 差异确认（函数集有意/事实不同，需确认降级方式） | 待定 |
| INTENT-COMPAT-011 | [compatibility] | 字符串比较大小写敏感性差异——GitHub 忽略大小写 vs GitCode startsWith/endsWith 区分大小写 | 关联 testing-focus §10；建议 P2。关联 spec C-EXP | 差异确认（GitCode startsWith/endsWith 有意区分大小写） | 待定 |
| INTENT-COMPAT-012 | [compatibility] | 表达式类型强转 / loose equality 差异——空串、null、布尔在比较中的强转规则 | 关联 testing-focus §1/§10；建议 P2。关联 spec G- | 一致性（GitCode 未声明差异，应与 GitHub 强转表对齐；不一致即缺陷+缺口） | 待定 |
| INTENT-COMPAT-013 | [compatibility] | `hashFiles()` 行为一致性——glob 语义、无匹配返回值、workspace 相对基准 | 关联 testing-focus §8 cache + §10；建议 P2。关联 | 一致性（GitCode 未声明差异，应与 GitHub 对齐） | 待定 |
| INTENT-COMPAT-014 | [compatibility] | 引用不存在的上下文属性——GitHub 空串 vs GitCode 处理一致性 | 关联 testing-focus §10 上下文；建议 P2。关联 spec C | 一致性（GitCode 已声明同向，验证深层链边界） | 待定 |
| INTENT-COMPAT-015 | [compatibility, usability] | `${{ }}` 表达式求值时机——先求值再进 shell 的注入面与转义一致性 | 关联 testing-focus §6 注入 + §10；建议 P1。与 sec | 一致性（求值时机应与 GitHub 一致，验证 + 文档化） | 待定 |
| INTENT-COMPAT-016 | [compatibility] | `steps.<id>` 引用 —— GitCode `identifier:` 与 `id:` 的等价性与 outputs 引用一致性 | 关联 testing-focus §10 + §11；建议 P1（生产全量使用  | 差异确认（identifier 为疑似 GitCode 特有/别名，spec 未收录） | 待定 |
| INTENT-COMPAT-017 | [compatibility, usability] | pull_request types 取值差异——GitHub `opened/synchronize/reopened` vs GitCode `open/update/reopen` | 关联 testing-focus §2/§10/§11；建议 P0（CI 静默不 | 差异确认（types 命名/取值有意不同） | 待定 |
| INTENT-COMPAT-018 | [compatibility, usability] | PR 评论触发两种写法并存——`pull_request_comment`+`comments` vs `pr_comment`+`keyword` | 关联 testing-focus §2/§10；建议 P1（重复触发浪费资源 + | 差异确认（GitCode 特有事件，无 GitHub 对应） | 待定 |
| INTENT-COMPAT-019 | [compatibility, security] | PR 评论正则过滤引擎差异——`'^(?:\/)?compile*'` 的正则方言与匹配语义 | 关联 testing-focus §2/§6/§10；建议 P2。与 secur | 差异确认（GitCode 特有能力，坐实语义边界） | 待定 |
| INTENT-COMPAT-020 | [compatibility] | paths/branches diff 阈值差异——GitHub 1000 commits/3000 files vs GitCode 前 300 文件 | 关联 testing-focus §2/§10/§12；建议 P1（大仓库静默漏 | 差异确认（阈值有意不同） | 待定 |
| INTENT-COMPAT-021 | [compatibility] | PR checkout ref 格式差异——GitCode `refs/merge-requests/<id>/merge` vs GitHub `refs/pull/<n>/merge` | 关联 testing-focus §10/§11；建议 P1（迁移必改写点）。关 | 差异确认（ref 命名/术语有意不同） | 待定 |
| INTENT-COMPAT-022 | [compatibility] | schedule 时区差异——GitHub 支持 `timezone` 字段 vs GitCode 仅 UTC | 关联 testing-focus §2/§10；建议 P2。关联 spec C- | 差异确认（GitCode 有意仅 UTC） | 待定 |
| INTENT-COMPAT-023 | [compatibility] | branches/paths 过滤通配语义差异——`**`/`!`/`?`/`+`/`[]` glob 方言一致性 | 关联 testing-focus §2/§10；建议 P2。关联 spec C- | 一致性（GitCode 未声明差异，应与 GitHub glob 对齐；子集不同即缺陷+缺口） | 待定 |
| INTENT-COMPAT-024 | [compatibility] | workflow_dispatch/workflow_call inputs 类型差异——GitHub 5 类型 vs GitCode 仅 string | 关联 testing-focus §1/§10/§11；建议 P1（静默条件反转 | 差异确认（GitCode 有意仅 string） | 待定 |
| INTENT-COMPAT-025 | [compatibility, usability] | 上下文前缀差异——`github.*` → `atomgit.*` 全局替换的完备性与属性缺失 | 关联 testing-focus §10/§11；建议 P1（迁移核心改造点）。 | 差异确认（前缀有意不同） | 待定 |
| INTENT-COMPAT-026 | [compatibility, completeness] | 上下文属性缺失——`atomgit.actor`/`triggering_actor`/`workflow_ref` 等是否存在 | 关联 testing-focus §10；建议 P1（actor 缺失=安全门禁 | 一致性（核心属性应可用；缺失即兼容缺口） | 待定 |
| INTENT-COMPAT-027 | [compatibility] | `runner` 上下文差异——os/arch 取值格式与 name/tool_cache/temp 一致性 | 关联 testing-focus §4/§10；建议 P2。关联 spec C- | 一致性（取值格式应对齐；平台子集差异需文档化） | 待定 |
| INTENT-COMPAT-028 | [compatibility] | `strategy` 上下文差异——`job-index`/`job-total`/`max-parallel` 是否可用 | 关联 testing-focus §3/§10；建议 P2。关联 spec C- | 一致性（应可用；缺失即兼容缺口） | 待定 |
| INTENT-COMPAT-029 | [compatibility] | `atomgit.token` vs `secrets.ATOMGIT_TOKEN` vs `github.token` 获取方式差异 | 关联 testing-focus §5/§10/§11；建议 P1。与 secu | 差异确认（命名不同 + 能力边界坐实） | 待定 |
| INTENT-COMPAT-030 | [compatibility] | 上下文可用性矩阵差异——各上下文在 workflow/job/step/if 级的可用位置一致性 | 关联 testing-focus §10；建议 P2。关联 spec C-EXP | 一致性（GitCode 已声明同向，逐格验证） | 待定 |
| INTENT-COMPAT-031 | [compatibility, usability] | 环境文件变量前缀差异——`GITHUB_ENV/OUTPUT/PATH/STEP_SUMMARY` → `ATOMGIT_*` | 关联 testing-focus §10/§11；建议 P1（output 静默 | 差异确认（前缀有意不同） | 待定 |
| INTENT-COMPAT-032 | [compatibility] | 系统环境变量映射差异——`GITHUB_*` 全集 → `ATOMGIT_*` 及缺失变量 | 关联 testing-focus §10/§11；建议 P1。关联 spec C | 差异确认（前缀有意不同）+ 一致性（全集覆盖度） | 待定 |
| INTENT-COMPAT-033 | [compatibility] | RUNNER_OS/ARCH 双命名混乱——`RUNNER_*` vs `ATOMGIT_RUNNER_*` 及 GitHub 对齐 | 关联 testing-focus §10；建议 P2。关联 spec C-VAR | 差异确认（GitCode 内部矛盾，坐实实际命名） | 待定 |
| INTENT-COMPAT-034 | [compatibility] | 工作流日志命令差异——`::group::`/`::error::`/`::warning::`/`::notice::`/`::add-mask::` 支持度 | 关联 testing-focus §9/§10；建议 P2。关联 spec C- | 一致性（GitCode 未声明差异，应尽量对齐；子集不同即缺口） | 待定 |
| INTENT-COMPAT-035 | [compatibility] | 多行值 delimiter 协议与「不可覆盖默认变量」约束一致性 | 关联 testing-focus §3/§10；建议 P2。关联 spec C- | 一致性（GitCode 未声明差异，应对齐） | 待定 |
| INTENT-COMPAT-036 | [compatibility, usability] | runs-on 取值差异——GitHub 单标签 `ubuntu-latest` vs GitCode 三段式 `{os,arch,flavor}` | 关联 testing-focus §4/§10/§11；建议 P0（每 work | 差异确认（结构有意不同） | 待定 |
| INTENT-COMPAT-037 | [compatibility, usability] | runs-on 多种写法等价性——数组 `[..]` vs 花括号 `{..}` vs `default` vs 键值 `arch=arm` | 关联 testing-focus §4/§10；建议 P2。关联 spec C- | 差异确认（GitCode 特有多写法，坐实等价性） | 待定 |
| INTENT-COMPAT-038 | [compatibility] | 预装工具链版本差异——GitHub runner image 与 GitCode ubuntu-latest 预装软件差集 | 关联 testing-focus §4/§10；建议 P2。关联 spec C- | 差异确认（image 内容有意/事实不同） | 待定 |
| INTENT-COMPAT-039 | [compatibility] | 无 Windows/macOS runner——GitHub 三平台 vs GitCode 仅 Linux 的迁移降级 | 关联 testing-focus §4/§10/§11；建议 P1（跨平台项目迁 | 差异确认（平台集有意受限） | 待定 |
| INTENT-COMPAT-040 | [compatibility, reliability] | 资源规格标签差异——GitCode flavor（slim~2xlarge）与「large+ 需申请」vs GitHub 标准/大型 runner | 关联 testing-focus §4/§10/§12；建议 P2（与 INTE | 差异确认（规格表达有意不同） | 待定 |
| INTENT-COMPAT-041 | [compatibility, usability] | 未知/不支持顶层字段的处理——报错 vs 静默忽略（GitHub 有 `run-name` 等 GitCode 无） | 关联 testing-focus §1/§10/§11；建议 P1（静默功能缺失 | 一致性（应有校验；静默忽略即缺陷，需坐实降级方式） | 待定 |
| INTENT-COMPAT-042 | [compatibility, reliability] | concurrency 模型差异——GitHub `group`+`cancel-in-progress` vs GitCode `enable`+`max`+`exceed-action`+`preemption` | 关联 testing-focus §3/§10/§12；建议 P1。关联 spe | 差异确认（模型有意不同） | 待定 |
| INTENT-COMPAT-043 | [compatibility] | action `runs.using` 运行时差异——GitHub `node20`/`docker`/`composite` vs GitCode 仅 `node16` | 关联 testing-focus §7/§10/§11；建议 P1（限制 act | 差异确认（using 类型集有意/事实受限） | 待定 |
| INTENT-COMPAT-044 | [compatibility] | `uses` action 引用方式差异——GitHub `owner/repo@ref` marketplace vs GitCode 官方短名 + 本地 | 关联 testing-focus §7/§10/§11；建议 P1。与 secu | 差异确认（引用方式/生态有意不同） | 待定 |
| INTENT-COMPAT-045 | [compatibility] | 废弃命令处理差异——`::set-output`/`::set-env`/`::add-path` 在 GitCode 的降级 | 关联 testing-focus §10/§11；建议 P2。关联 spec C | 差异确认（GitCode 废弃程度需坐实） | 待定 |
| INTENT-COMPAT-046 | [compatibility, reliability] | step 输出/artifact 超限行为差异——1MB output、artifact 上限的降级方式 | 关联 testing-focus §8/§10/§12；建议 P2。与 reli | 差异确认（限额值/降级方式需坐实） | 待定 |
| INTENT-COMPAT-047 | [compatibility, usability] | checkout action 差异——GitCode `uses: checkout` 参数集与 GitHub `actions/checkout@v4` 等价性 | 关联 testing-focus §10/§11；建议 P1（checkout  | 差异确认（实现是否等价需坐实） | 待定 |
| INTENT-COMPAT-048 | [compatibility] | cache action 差异——key/restore-keys 语义、fork 隔离、跨 run 命中与 GitHub 等价性 | 关联 testing-focus §8/§10；建议 P2。与 security | 一致性（key 语义应对齐）+ 差异确认（隔离作用域坐实） | 待定 |
| INTENT-COMPAT-049 | [compatibility] | upload/download-artifact 差异——name 唯一性、path 默认、多 artifact 行为与 GitHub 等价性 | 关联 testing-focus §8/§10；建议 P2。关联 spec C- | 一致性（参数语义应对齐）+ 差异确认（命名/上限坐实） | 待定 |
| INTENT-COMPAT-050 | [compatibility] | setup-* action 差异——setup-node/python/java/go 的 version/cache 参数与版本解析 | 关联 testing-focus §10/§11；建议 P2。关联 spec C | 差异确认（参数规格无独立文档，需坐实） | 待定 |
| INTENT-COMPAT-051 | [compatibility] | action inputs 环境变量注入差异——`INPUT_<NAME>` 命名转换与 required 校验 | 关联 testing-focus §7/§10；建议 P2。关联 spec C- | 一致性（命名转换应与 GitHub 一致） | 待定 |
| INTENT-COMPAT-052 | [compatibility, security] | fork PR token 降权语义一致性——GitCode fork `pull_request` 是否确降只读 | 关联 testing-focus §5/§10；建议 P0（安全命脉）。与 se | 一致性（GitCode 声明与 GitHub 同向，重点坐实真实成立） | 待定 |
| INTENT-COMPAT-053 | [compatibility, security] | pull_request_target 语义一致性——base 上下文执行 + secret 可达 + cache 只读 | 关联 testing-focus §5/§8/§10；建议 P0（pwn req | 一致性（应与 GitHub 加固语义一致，坐实保护真实成立） | 待定 |
| INTENT-COMPAT-054 | [compatibility, security] | secret 日志脱敏一致性——`***` 遮掩对 base64/拼接/多行变形的覆盖与 GitHub 对齐 | 关联 testing-focus §5/§10；建议 P1。与 security | 一致性（脱敏覆盖不应弱于 GitHub） | 待定 |
| INTENT-COMPAT-055 | [compatibility, security] | permissions `{}` 语义确认——全 none vs repository:read 的兼容影响 | 关联 testing-focus §5/§10；建议 P1。与 security | 差异确认（GitCode 文档矛盾，坐实实际值） | 待定 |
| INTENT-COMPAT-056 | [compatibility, security] | recursive run 防护一致性——GitCode token 触发的运行是否防递归 | 关联 testing-focus §2/§5/§10；建议 P1（无限递归耗配额 | 一致性（应有防递归；缺失即缺陷+安全隐患） | 待定 |
| INTENT-COMPAT-057 | [compatibility, usability] | stages 编排层——GitHub 扁平 jobs 迁移到 GitCode 是否需引入 stages 及默认行为 | 关联 testing-focus §3/§10/§11；建议 P1（迁移结构落位 | 差异确认（GitCode 特有结构，坐实迁移落位） | 待定 |
| INTENT-COMPAT-058 | [compatibility, usability] | stages 两种写法 + 缩进瑕疵——列表 `- name:` vs 映射 `stage1:` 的解析容错 | 关联 testing-focus §1/§10/§11；建议 P2。关联 spe | 差异确认（GitCode 特有写法，坐实等价性） | 待定 |
| INTENT-COMPAT-059 | [compatibility] | GitCode 特有 stage 字段——`select`/`pre`/`fail-fast` 无 GitHub 对应的语义确认 | 关联 testing-focus §3/§10；建议 P1（生产必需 + 文档盲 | 差异确认（GitCode 特有，坐实语义） | 待定 |
| INTENT-COMPAT-060 | [compatibility, usability] | 非法 YAML / schema 校验报错质量——错在第几行、可操作提示与 GitHub 对齐 | 关联 testing-focus §1/§10/§11；建议 P1（迁移调试成本 | 一致性（报错质量不应劣于 GitHub） | 待定 |
| INTENT-COMPAT-061 | [compatibility] | workflow_call 复用差异——嵌套层数、secrets 传递、inputs 类型与 GitHub 对齐 | 关联 testing-focus §7/§10/§11；建议 P1。关联 spe | 差异确认（层数/inputs 有意不同）+ 一致性（outputs 映射语义） | 待定 |

### 安全性 (security)（33 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-SEC-001 | [security] | 验证来自 fork 的 pull_request 流水线无法读取项目级/组织级 Secret | 建议 P0 候选（testing-focus §5 安全命脉；issues.md | — | 待定 |
| INTENT-SEC-002 | [security] | 验证 fork pull_request 下 ATOMGIT_TOKEN 被强制降为只读（无视 permissions 声明） | 建议 P0 候选（testing-focus §5；权限越界=blocker 类 | — | 待定 |
| INTENT-SEC-003 | [security] | 验证 fork PR 可修改 workflow 文件但攻击范围受限（无 secret、无写权限） | 建议 P1 候选（依附 001/002；testing-focus §5）。 | — | 待定 |
| INTENT-SEC-004 | [security] | 验证 pull_request_target 使用 base 分支的 workflow 版本（PR 提交者不能改执行逻辑） | 建议 P0 候选（testing-focus §5；security-serie | — | 待定 |
| INTENT-SEC-018 | [security] | 验证 pull_request_target 下显式 checkout PR head 代码时的高权限注入风险被识别/防护 | 建议 P0 候选（testing-focus §5/§6；G-17 明确弱点）。 | — | 待定 |
| INTENT-SEC-009 | [security] | 验证 PR 标题/正文内联进 run 脚本时不导致命令执行（脚本注入） | 建议 P0 候选（testing-focus §6；security-serie | — | 待定 |
| INTENT-SEC-010 | [security] | 验证非显而易见的不可信源（分支名 head_ref / commit message / author email）不致注入 | 建议 P0 候选（testing-focus §6；最易漏防的注入面）。 | — | 待定 |
| INTENT-SEC-012 | [security] | 验证 issue_comment / pull_request_comment 评论正文内联不致注入 | 建议 P1 候选（testing-focus §6；GitCode 特有事件需实 | — | 待定 |
| INTENT-SEC-013 | [security] | 验证中间环境变量防御模式对注入的有效性（防御模式确认） | 建议 P1 候选（testing-focus §6；迁移防护指导正确性）。 | — | 待定 |
| INTENT-SEC-014 | [security, compatibility] | 验证双重表达式求值与 pull_request_comment 正则过滤的注入面 | 建议 P1 候选（testing-focus §6；G-18 缺口）。 | — | 待定 |
| INTENT-SEC-005 | [security] | 验证 Secret 值在日志中的基础自动脱敏（直接输出被 *** 遮蔽） | 建议 P0 候选（testing-focus §5；issues.md §3 P | — | 待定 |
| INTENT-SEC-006 | [security] | 验证编码变形（base64 等）后 Secret 的脱敏覆盖 | 建议 P0 候选（testing-focus §5；issues.md §3 明 | — | 待定 |
| INTENT-SEC-007 | [security] | 验证字符串拼接/分片输出时 Secret 的脱敏覆盖 | 建议 P0 候选（testing-focus §5；issues.md §3）。 | — | 待定 |
| INTENT-SEC-008 | [security] | 验证多行 Secret 值的逐行脱敏覆盖 | 建议 P1 候选（testing-focus §5；issues.md §3）。 | — | 待定 |
| INTENT-SEC-015 | [security] | 验证 permissions 收窄声明真实生效（越权操作被拒） | 建议 P0 候选（testing-focus §5；权限失效=blocker 类 | — | 待定 |
| INTENT-SEC-016 | [security, usability] | 验证 permissions:{} 的实际权限并消解「全 none vs repository:read」文档冲突 | 建议 P1 候选（testing-focus §5/§11；关联 G-06/G- | — | 待定 |
| INTENT-SEC-017 | [security] | 验证未声明 permissions 时的默认权限不宽于仓库设置（无隐性提权） | 建议 P1 候选（testing-focus §5；G-06 缺口）。 | — | 待定 |
| INTENT-SEC-023 | [security] | 验证 ATOMGIT_TOKEN 运行后失效且不可通过缓存/残留复活 | 建议 P1 候选（testing-focus §5；issues.md §2 t | — | 待定 |
| INTENT-SEC-036 | [security] | 验证 ATOMGIT_TOKEN 默认权限范围与 job 级覆盖的正确性 | 建议 P1 候选（testing-focus §5；issues.md §2 引 | — | 待定 |
| INTENT-SEC-021 | [security] | 验证 uses 支持 commit SHA 不可变引用，且可变 tag/分支引用的重写风险被识别 | 建议 P1 候选（testing-focus §7；security-serie | — | 待定 |
| INTENT-SEC-022 | [security] | 验证第三方 action 对 ATOMGIT_TOKEN / secret 的隐式获取受最小权限约束 | 建议 P1 候选（testing-focus §7；security-serie | — | 待定 |
| INTENT-SEC-019 | [security, reliability] | 验证 fork PR 无法投毒主分支缓存（cache 作用域隔离） | 建议 P0 候选（testing-focus §8；G-19 明确缺口；secu | — | 待定 |
| INTENT-SEC-020 | [security] | 验证 cache key 跨项目/跨仓库作用域隔离（无横向污染） | 建议 P1 候选（testing-focus §8；issues.md §1 多 | — | 待定 |
| INTENT-SEC-029 | [security] | 验证跨运行 artifact 被视为不可信数据（artifact 投毒防护） | 建议 P1 候选（testing-focus §8；security-serie | — | 待定 |
| INTENT-SEC-025 | [security, reliability] | 验证 Runner 跨 job/跨 run 无敏感残留（工作区/环境/凭据清理） | 建议 P0 候选（testing-focus §4；issues.md §1/§ | — | 待定 |
| INTENT-SEC-026 | [security] | 验证共享盘（/tmp、workspace）不跨 job 泄露敏感文件 | 建议 P1 候选（testing-focus §4；issues.md §4）。 | — | 待定 |
| INTENT-SEC-027 | [security, reliability] | 验证 Runner 网络出站边界（防 SSRF / 内网跳板 / 数据外传） | 建议 P1 候选（testing-focus §4；issues.md §5；G | — | 待定 |
| INTENT-SEC-028 | [security] | 验证多项目共享 Runner 的 Secret 与资源隔离（项目 A secret 不达项目 B） | 建议 P0 候选（testing-focus §4/§5；issues.md § | — | 待定 |
| INTENT-SEC-033 | [security, reliability] | 验证同主机 Runner 并发 job 间的隔离（进程/文件/环境互不可见） | 建议 P1 候选（testing-focus §4；issues.md §1 I | — | 待定 |
| INTENT-SEC-032 | [security] | 验证 Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄 | 建议 P1 候选（testing-focus §5/§8）。 | — | 待定 |
| INTENT-SEC-024 | [security] | 验证工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权 | 建议 P1 候选（testing-focus §6；C-ACT-02/05）。 | — | 待定 |
| INTENT-SEC-030 | [security, usability] | 验证环境保护规则（reviewers/wait timer）未审批时环境 Secret 不可访问 | 建议 P1 候选（testing-focus §5；G-20 缺口）。 | — | 待定 |
| INTENT-SEC-031 | [security] | 验证 TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定 | 建议 P1 候选（testing-focus §2/§6；security-se | — | 待定 |

### 稳定性 (reliability)（33 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-REL-001 | [reliability] | concurrency.max 边界值 1 与 5 的并发限制生效性 | — | — | 待定 |
| INTENT-REL-002 | [reliability] | concurrency.max 越界值（0 / 6 / 非整数）的校验拒绝 | — | — | 待定 |
| INTENT-REL-003 | [reliability] | exceed-action=QUEUE 超额排队的公平性与不丢失 | — | — | 待定 |
| INTENT-REL-004 | [reliability] | exceed-action=IGNORE 超额忽略的行为一致性 | — | — | 待定 |
| INTENT-REL-005 | [reliability] | preemption.events 上限 10 的边界与越界（11 个） | — | — | 待定 |
| INTENT-REL-006 | [reliability] | concurrency 抢占（preemption）取消运行中 job 的清理与恢复 | — | — | 待定 |
| INTENT-REL-007 | [reliability] | job timeout-minutes 边界：接近 360 分钟默认超时与显式短超时的强制终止 | — | — | 待定 |
| INTENT-REL-008 | [reliability] | rerun 次数上限 3 与 6 小时时效边界 | — | — | 待定 |
| INTENT-REL-009 | [reliability] | paths 过滤「前 300 个变更文件」边界与越界（301+ 命中不触发） | — | — | 待定 |
| INTENT-REL-010 | [reliability] | [探测] matrix 组合数上限——渐进加压找实际上限与越限行为 | — | — | 待定 |
| INTENT-REL-011 | [reliability] | [探测] 账户/仓库级全局并发上限——多 workflow 并发洪泛找实际上限 | — | — | 待定 |
| INTENT-REL-012 | [reliability, usability] | [探测] step 输出超 1MB/参数的行为——截断 vs 报错 | — | — | 待定 |
| INTENT-REL-013 | [reliability] | [探测] 制品（artifact）大小上限——渐进加压找上限与越限行为 | — | — | 待定 |
| INTENT-REL-014 | [reliability] | [探测] 缓存（cache）容量上限与 LRU 淘汰行为 | — | — | 待定 |
| INTENT-REL-015 | [reliability, usability] | [探测] 单 step 日志量上限——超长日志的截断/落盘/查看 | — | — | 待定 |
| INTENT-REL-016 | [reliability, usability] | [探测] workflow 文件大小上限——超大 YAML 的解析行为 | — | — | 待定 |
| INTENT-REL-017 | [reliability] | [探测] 单仓 secret 数量上限——渐进添加找上限 | — | — | 待定 |
| INTENT-REL-018 | [reliability] | [探测·故障] Runner 内存超限（OOM）行为与恢复 | — | — | 待定 |
| INTENT-REL-019 | [reliability] | [探测·故障] Runner 磁盘写满行为与恢复 | — | — | 待定 |
| INTENT-REL-020 | [reliability] | [故障] job 执行中 kill runner——运行状态收敛与可重跑 | — | — | 待定 |
| INTENT-REL-021 | [reliability] | [故障] 拉取 action/依赖时网络分区——超时与失败归因 | — | — | 待定 |
| INTENT-REL-022 | [reliability] | [故障] 平台依赖服务不可用（cache / artifact 服务）时的降级 | — | — | 待定 |
| INTENT-REL-023 | [reliability] | [故障] CPU 饱和——同 flavor 下的资源争用与稳态维持 | — | — | 待定 |
| INTENT-REL-024 | [reliability, security] | [故障·探测] 网络出站范围——外网/内网/DNS 可达性与中断行为 | — | — | 待定 |
| INTENT-REL-025 | [reliability] | [故障] container 私有镜像 registry 不可用/拉取超时 | — | — | 待定 |
| INTENT-REL-026 | [reliability] | [故障] needs 依赖 job 失败的传播与 if:always 恢复路径 | — | — | 待定 |
| INTENT-REL-027 | [reliability] | matrix strategy.fail-fast 语义——一实例失败取消其余的确定性 | — | — | 待定 |
| INTENT-REL-028 | [reliability] | stages.fail_fast 跨 stage 失败传播语义 | — | — | 待定 |
| INTENT-REL-029 | [reliability] | 取消/抢占时 post 清理钩子的执行保证 | — | — | 待定 |
| INTENT-REL-030 | [reliability] | 同一 push 连推的触发去重/幂等与并发触发排队公平性 | — | — | 待定 |
| INTENT-REL-031 | [reliability] | [大规模] 超多 step 的单 job 稳定性 | — | — | 待定 |
| INTENT-REL-032 | [reliability] | [大规模] 超大仓库 checkout 的磁盘/时间边界 | — | — | 待定 |
| INTENT-REL-033 | [reliability, security] | 托管 Runner 跨 job 复用的残留污染——去 flaky 隔离验证 | — | — | 待定 |

### 易用性 (usability)（25 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-USE-001 | [usability, compatibility] | 直接把 .github/workflows/ 搬到仓库根，workflow 是否静默不被识别（迁移第一摩擦点） | 关联迁移摩擦（testing-focus §11）；risk-register  | — | 待定 |
| INTENT-USE-002 | [usability, compatibility] | 直接搬运含 ${{ github.* }} 上下文的 workflow，报错是否点明「应改用 atomgit.*」 | 迁移摩擦高频（testing-focus §11）；risk-register  | — | 待定 |
| INTENT-USE-003 | [usability, compatibility] | GitHub 式状态函数 success()/failure()（带括号）的报错是否指明「GitCode 状态函数不带括号」 | 迁移摩擦（testing-focus §1/§11）；risk-register | — | 待定 |
| INTENT-USE-004 | [usability, compatibility] | 跨 job 输出引用 needs.<job>.outputs（GitHub 式）在 GitCode 是否可用/报错是否指向 jobs.<job>.outputs | 迁移摩擦 + 真实样本证据（testing-focus §3/§11）；risk | — | 待定 |
| INTENT-USE-005 | [usability, compatibility] | permissions 权限域用 GitHub 命名（contents/pull-requests）时的报错质量 | 迁移摩擦 + 安全相关（testing-focus §5/§11）；risk-r | — | 待定 |
| INTENT-USE-006 | [usability, compatibility] | runs-on 用 GitHub 单标签 ubuntu-latest 迁移时的行为与可理解性 | 迁移摩擦「开箱能否跑」（testing-focus §4/§11）；risk-r | — | 待定 |
| INTENT-USE-007 | [usability] | 非法 YAML（缩进/语法错误）的报错是否精确到行号 | 报错质量（testing-focus §1）；risk-register 模板态 | — | 待定 |
| INTENT-USE-008 | [usability, compatibility] | 未知/不支持顶层字段（如 GitHub 的 defaults 之外拼写或 GitHub 专有字段）的处理：报错还是静默忽略 | 报错质量 + 迁移摩擦（testing-focus §1/§11）；risk-r | — | 待定 |
| INTENT-USE-009 | [usability, compatibility] | 事件名 pr_comment / pull_request_comment 混用时的报错可理解性（真实样本证据） | 报错质量 + 真实样本证据（testing-focus §1/§2/§11）；r | — | 待定 |
| INTENT-USE-010 | [usability, compatibility] | inputs 声明 GitHub 式 type: boolean/choice/number 时的报错是否指引「仅支持 string」 | 迁移摩擦 + 静默语义陷阱（testing-focus §1/§11）；risk | — | 待定 |
| INTENT-USE-011 | [usability, compatibility] | 引用带 owner/版本的 GitHub action（actions/checkout@v4）时的报错可理解性 | 迁移摩擦（testing-focus §7/§11）；risk-register | — | 待定 |
| INTENT-USE-012 | [usability] | 废弃命令 ::set-output/::set-env/::add-path 使用时是否给出可操作的迁移提示 | 报错/调试质量（testing-focus §1/§9）；risk-regist | — | 待定 |
| INTENT-USE-013 | [usability, security] | permissions:{} 实际权限与文档两处冲突声明的核对（能否 clone 代码） | 文档质量 + 安全实践可用性（testing-focus §5/§11）；ris | — | 待定 |
| INTENT-USE-014 | [usability, reliability] | 重跑后 ATOMGIT_RUN_ID 是否变化——两文档冲突导致用户无法用作幂等键 | 文档质量 + 可观测性（testing-focus §9）；risk-regis | — | 待定 |
| INTENT-USE-015 | [usability, compatibility] | 系统变量命名 RUNNER_OS vs ATOMGIT_RUNNER_OS 两套并存导致用户不知该用哪个 | 文档质量 + 迁移摩擦（testing-focus §11）；risk-regi | — | 待定 |
| INTENT-USE-016 | [usability] | 文档夹带 GitHub 残留措辞（octocat/actions/checkout/GITHUB_*）误导迁移者 | 文档质量（testing-focus §11）；risk-register 模板 | — | 待定 |
| INTENT-USE-017 | [usability, compatibility] | stages 两种写法（列表 - name: vs 映射 stage1:）并存且示例缩进疑误，用户无所适从 | 文档质量 + 特有能力上手（testing-focus §3/§11）；risk | — | 待定 |
| INTENT-USE-018 | [usability] | 示例文档「可直接复刻」验证：quick-start 最小示例与内置 action 示例开箱可跑 | 文档易用性核心指标（business-context 维度1；testing-f | — | 待定 |
| INTENT-USE-019 | [usability, completeness] | 日志/示例引用 atomgit.actor 但 context 属性表未列，用户按文档引用取到空值 | 文档质量（testing-focus §9/§11）；risk-register | — | 待定 |
| INTENT-USE-020 | [usability, reliability] | 请求未开通规格（large+）或无匹配 Runner 时，排队是否有可理解反馈而非静默挂起 | 可观测性 + 迁移摩擦（testing-focus §4/§9/§12）；ris | — | 待定 |
| INTENT-USE-021 | [usability, security] | secret 脱敏在日志中的可观测性——用户误 echo secret 时能否看出被遮蔽 | 可观测性 + 安全体验（testing-focus §5/§9）；risk-re | — | 待定 |
| INTENT-USE-022 | [usability] | job/step 失败时日志能否定位到「哪个 step、哪条命令、退出码」 | 可观测性（testing-focus §9）；risk-register 模板态 | — | 待定 |
| INTENT-USE-023 | [usability] | workflow 命令注解 ::error::/::warning:: 能否在运行详情中可见并定位 | 可观测性（testing-focus §9）；risk-register 模板态 | — | 待定 |
| INTENT-USE-024 | [usability] | PR 场景状态回写（Checks/commit status）到 PR 页的可见性与可理解性 | 可观测性 + PR 工作流迁移（testing-focus §9/§11）；ri | — | 待定 |
| INTENT-USE-025 | [usability] | inputs 默认值在 shell 中以 ${var} 直接引用（真实样本写法）是否可用/失败可诊断 | 迁移摩擦 + 静默空值陷阱（testing-focus §1/§11）；risk | — | 待定 |

---

## 增量更新补充（/phase01-update · 2026-07-21 第1轮）

> 本次补充针对 `coverage.md` 高严重度盲区 BLIND-07 与 BLIND-08，由 reliability + compat-diff agent 并行发散，局部门禁后准入。

### 稳定性增补（3 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-REL-034 | [reliability, completeness] | cron 表达式运算符边界——标准运算符生效、静默忽略或报错 | BLIND-07 高严重度；历史 TC-471~474/505-512 NEEDS-UPDATE | 一致性（POSIX cron 语义） | **准入(P1)** |
| INTENT-REL-035 | [reliability] | schedule 最小调度间隔 enforcement——低于 5 分钟的拒绝/排队/降级行为 | BLIND-07 高严重度；历史 TC-429 NEEDS-UPDATE | 一致性（规格声明 5min 阈值） | **准入(P1)** |
| INTENT-REL-036 | [reliability, completeness] | schedule 触发收敛与取消语义——Scheduler 修复后调度运行可达终态 | BLIND-07 高严重度；历史 TC-391/427-430 NEEDS-UPDATE | 一致性（C-TRIG-08 + C-EXEC-24） | **准入(P1)** |

### 兼容性增补（3 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-COMPAT-062 | [compatibility, reliability] | RUNNER_* / ATOMGIT_* 系统变量 Shell 真实注入回归验证——历史 TC-441/442/206 FAIL 重验 | BLIND-08 高严重度；历史 TC-441/442/206 FAIL | 一致性（系统变量应默认注入且可读） | **准入(P1)** |
| INTENT-COMPAT-063 | [compatibility, reliability] | env > vars 优先级链在 Shell 中的真实覆盖回归验证——历史 TC-533「env 不注入 Shell」重验 | BLIND-08 高严重度；历史 TC-533/534 FAIL | 一致性（env 三级覆盖 + vars 不直接介入） | **准入(P1)** |
| INTENT-COMPAT-064 | [compatibility, reliability] | 缺失系统变量引用行为与注入时机验证——「未定义报错 vs 空串」及「启动前注入 vs 延迟注入」 | BLIND-08 高严重度；历史 TC-206 FAIL | 一致性（缺失变量空串、启动前注入、不可覆盖） | **准入(P1)** |

### 补充统计（第1轮）

| 项目 | 数值 |
|---|---|
| 新增 intent | 6 |
| 准入 | 6（P1=6） |
| 打回 | 0 |
| 合并 | 0 |
| **第1轮后 intent 总数** | **166**（原 160 + 新增 6） |

---

## 增量更新补充（/phase01-update · 2026-07-21 第2轮）

> 用户要求补齐所有剩余盲区。BLIND-04 标为 out-of-scope（action 开发侧）。> 由 reliability/security/completeness/compatibility/usability 五维度 agent 并行发散，局部门禁后准入。

### 稳定性增补（4 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 门禁 |
|---|---|---|---|---|
| INTENT-REL-037 | [reliability] | 手动取消时运行中 step 进程的终止信号与 grace period 行为 | BLIND-01 高严重度；历史 #39/TC-391 | **准入(P1)** |
| INTENT-REL-038 | [reliability] | 取消后运行终态收敛与 runner 资源释放时限 | BLIND-01 高严重度；历史 #39/TC-391 | **准入(P1)** |
| INTENT-REL-039 | [reliability] | preemption 抢占触发条件——事件匹配范围与作用域边界 | BLIND-11 中严重度 | **准入(P1)** |
| INTENT-REL-040 | [reliability] | preemption 被抢占 job/run 的终态、日志完整性与 runner 释放时效 | BLIND-11 中严重度 | **准入(P1)** |

### 安全性增补（4 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 门禁 |
|---|---|---|---|---|
| INTENT-SEC-037 | [security, completeness] | 验证保护分支上下文标志 `atomgit.ref_protected` 的可用性与正确性 | BLIND-05 中严重度 | **准入(P1)** |
| INTENT-SEC-038 | [security, reliability] | 验证环境保护 wait timer 倒计时期间环境 Secret 不可访问 | BLIND-11 中严重度 | **准入(P1)** |
| INTENT-SEC-039 | [security] | 验证私有 container 镜像拉取凭证的安全传递与日志不泄露 | BLIND-02 高严重度；历史 TC-273 | **准入(P1)** |
| INTENT-SEC-040 | [security, completeness] | 验证 container 运行时 step 对宿主机环境变量/Secret 的隔离有效性 | BLIND-02 高严重度 | **准入(P1)** |

### 完备性增补（5 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 门禁 |
|---|---|---|---|---|
| INTENT-COMP-009 | [completeness, security] | 验证 job 级 container 自定义镜像执行能力（含私有镜像认证） | BLIND-02 高严重度；历史 TC-273 FAIL | **准入(P1)** |
| INTENT-COMP-010 | [completeness, compatibility] | 验证 matrix include 向已有组合追加额外变量及新增组合的正确展开 | BLIND-03 中严重度；历史 TC-325-328 | **准入(P1)** |
| INTENT-COMP-011 | [completeness, compatibility] | 验证 matrix exclude 排除特定组合后剩余组合的正确性 | BLIND-03 中严重度；历史 TC-325-328 | **准入(P1)** |
| INTENT-COMP-012 | [completeness, compatibility] | 验证 matrix 动态 runs-on——不同组合是否调度到对应 Runner 标签 | BLIND-03 中严重度 | **准入(P1)** |
| INTENT-COMP-013 | [completeness, usability] | 验证 atomgit.actor 存在性与上下文种类数一致性（12 种声明 vs 实际表） | BLIND-10 中严重度 | **准入(P1)** |

### 兼容性增补（3 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 对齐方向 | 门禁 |
|---|---|---|---|---|---|
| INTENT-COMPAT-065 | [compatibility] | matrix include/exclude 展开语义与动态 runs-on 兼容性 | BLIND-03 中严重度 | 一致性 + 差异确认 | **准入(P1)** |
| INTENT-COMPAT-066 | [compatibility] | 表达式函数 format 边界行为——参数不足/过剩、转义、非字符串参数 | BLIND-09 中严重度 | 一致性 | **准入(P1)** |
| INTENT-COMPAT-067 | [compatibility] | 表达式函数 substring/replace/toJson 边界行为——越界、全局/首匹配、JSON 输出格式 | BLIND-09 中严重度 | 差异确认 + 一致性 | **准入(P1)** |

### 易用性增补（2 条）

| 意图 ID | 维度标签 | 标题 | 优先级线索 | 门禁 |
|---|---|---|---|---|
| INTENT-USE-026 | [usability] | Step Summary 可写性与可见性 | BLIND-06 低严重度 | **准入(P2)** |
| INTENT-USE-027 | [usability] | Badge 状态徽标可用性 | BLIND-06 低严重度 | **准入(P2)** |

### 补充统计（第2轮）

| 项目 | 数值 |
|---|---|
| 新增 intent | 18 |
| 准入 | 18（P1=16 / P2=2） |
| 打回 | 0 |
| 合并 | 0 |
| out-of-scope | 1（BLIND-04） |
| **更新后 intent 总数** | **184**（原 160 + 第1轮 6 + 第2轮 18） |

*更新原因：补齐 coverage.md 全部剩余盲区（BLIND-01/02/03/05/06/09/10/11），BLIND-04 判 out-of-scope。*
