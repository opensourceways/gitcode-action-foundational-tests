# 兼容性 Diff Intent（Compat-Diff Agent 产出）

> run: 2026-07-21-01
> dimensions: [compatibility]
> 共 28 条 intent，覆盖 `testing-focus.md` §10 八大差异类别 + `COMPAT-NOTES.md` 全量线索 + `history/issues-encountered.md` 实证缺陷
> 每条标注 oracle 对齐方向：**一致性**（应与 GitHub 行为一致）或 **差异确认**（GitCode 有意不同，需确认边界与文档）

---

## 一、默认值/隐式行为差异（高发区 · §10 第一条）

### INTENT-COMPAT-001 — 未声明 `defaults.run.shell` 时的默认 shell

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, usability]` |
| **具体差异点** | 当 workflow 未声明 `defaults.run.shell` 时，GitHub 默认行为是 `bash --noprofile --norc -eo pipefail`；GitCode 文档未明确声明默认 shell 及其失败语义（`-eo pipefail` 是否生效）。 |
| **GitHub 侧预期行为** | `bash --noprofile --norc -eo pipefail`——单行命令失败立即退出，管道任一命令失败即判定失败。 |
| **GitCode 侧疑似行为** | 疑似默认 `bash` 但不确认是否携带 `-eo pipefail`；若缺失则管道中非末尾命令失败不会导致 step 失败，形成静默差异。 |
| **oracle 对齐方向** | **一致性用例**——GitCode 未声明差异，应与 GitHub 对齐。 |
| **触发条件** | 在 `run:` 中使用管道命令（如 `false \| true`），观察 step 是否判定为失败。 |
| **为什么有风险** | 管道命令是 CI 脚本中极常见的写法；若无 `-eo pipefail`，`grep \| awk` 类管道中间失败不会使构建中断，导致静默漏检。 |
| **出处** | `testing-focus.md` §4/§10；`github-reference/reference/workflow-syntax.md`；`risk-register.md` RISK-COMPAT-01 |

### INTENT-COMPAT-002 — 未声明 `permissions` 时的 ATOMGIT_TOKEN 默认权限

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, security]` |
| **具体差异点** | GitHub 有明确的 `GITHUB_TOKEN` 默认权限表（`contents: read`, `packages: read` 等），工作流可通过 `permissions:` 收窄；GitCode 文档仅写「未声明 permissions 时使用仓库设置中定义的权限」，未说明「仓库设置默认权限」的具体值。 |
| **GitHub 侧预期行为** | 未声明 `permissions` 时，`GITHUB_TOKEN` 有预定义默认权限集合（可 fork），且所有 job 继承。 |
| **GitCode 侧疑似行为** | `ATOMGIT_TOKEN` 默认权限取决于仓库级设置——但该仓库级默认值是什么、与 GitHub 默认权限是否对齐，均不透明。 |
| **oracle 对齐方向** | **一致性用例**——若 GitCode 未声明差异，默认权限集合应与 GitHub 一致；至少文档应写清楚默认值。 |
| **触发条件** | 不写 `permissions:` 字段，尝试用 `ATOMGIT_TOKEN` 操作 Issue/PR/仓库推送等不同域，观察哪些被允许。 |
| **为什么有风险** | 若默认权限比 GitHub 宽松，安全面扩大；若更窄，从 GitHub 迁移的 workflow 可能静默失败（API 调用被拒）。 |
| **出处** | `COMPAT-NOTES.md` §6；`gitcode-spec/security-permissions/token-permissions.md`；`testing-focus.md` §5/§10；历史 #51(fork PR 读到密钥) |

### INTENT-COMPAT-003 — `workflow_call` 的默认并发行为

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, reliability]` |
| **具体差异点** | GitHub 不设默认 job 级 `concurrency`（同一 workflow 多 job 可并行）；GitCode 的 `stages` 阶段机制默认阶段间串行、阶段内并行。对于未使用 `stages` 的纯 `jobs` 定义，GitCode 是否与 GitHub 对齐（全并行），需确认。 |
| **GitHub 侧预期行为** | 无 `needs` 声明的 job 默认并行；`concurrency` 默认无限制。 |
| **GitCode 侧疑似行为** | 若使用 `stages` 则阶段间串行；不使用 `stages` 时的并行策略待确认。文档 Q&A 称「无 needs 时多个 job 默认并行」。 |
| **oracle 对齐方向** | **一致性用例**——无 `stages` 声明的纯 `jobs` 定义，其默认并发行为应与 GitHub 一致。 |
| **触发条件** | 定义 3 个无 `needs` 的独立 job，观察三者是否同时启动。 |
| **为什么有风险** | 若默认串行则 CI 耗时显著增加；从 GitHub 迁移的用户无感知。 |
| **出处** | `COMPAT-NOTES.md` §4；`gitcode-spec/writing-pipelines/configure-jobs.md`；`testing-focus.md` §3/§10 |

---

## 二、表达式与函数差异（§10 第二条 · 最密集差异区）

### INTENT-COMPAT-010 — 状态检查函数的调用语法（无括号 vs 有括号）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 状态函数写 `success`/`always`/`failed`/`cancelled`（无括号）；GitHub 写 `success()`/`always()`/`failure()`/`cancelled()`（有括号）。若迁移时直接用 GitHub 写法 `if: ${{ failure() }}`，GitCode 会报错还是解析为字符串比较？ |
| **GitHub 侧预期行为** | `if: ${{ failure() }}` → 返回布尔值 true/false。 |
| **GitCode 侧疑似行为** | 文档示例均为 `${{ success }}` 无括号；若使用 `${{ failure() }}`，疑似解析失败或误解析。 |
| **oracle 对齐方向** | **差异确认用例**——这是已知的语法差异，需验证：(a) `failure()` 在 GitCode 上是否报错，(b) 若报错则报错信息是否明确指向「去掉括号」。 |
| **触发条件** | 在 `if:` 中使用 `${{ failure() }}`（GitHub 风格），观察解析行为。 |
| **为什么有风险** | 直接把 GitHub workflow 复制到 `.gitcode/workflows/` 时，所有 `if:` 条件里的 `failure()`/`success()` 都会断裂——这是迁移摩擦的第一高频踩坑点。 |
| **出处** | `COMPAT-NOTES.md` §3；`gitcode-spec/syntax-reference/expressions.md`；`github-reference/reference/expressions.md`；历史 #57(if 表达式报错) |

### INTENT-COMPAT-011 — 失败函数命名 `failed` vs `failure()`

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 失败函数名为 `failed`（无括号）；GitHub 为 `failure()`。两者不仅括号差异，连函数名也不同。 |
| **GitHub 侧预期行为** | `failure()` ——任何一个前置步骤失败返回 true。 |
| **GitCode 侧疑似行为** | `failed` ——语义等价但命名不同。需验证：(a) `failure` 作为无括号关键字是否被识别，(b) 若误写 `failure()` 报错质量。 |
| **oracle 对齐方向** | **差异确认用例**——命名不同是已知差异，需确认文档是否明确声明、报错是否指引用户用 `failed`。 |
| **触发条件** | 在 `if:` 中分别使用 `${{ failed }}` 和 `${{ failure() }}`，对比行为。 |
| **为什么有风险** | `failure()` → `failed` 的差异比括号差异更隐蔽——即使用户知道要去括号，也未必知道要改名。 |
| **出处** | `COMPAT-NOTES.md` §3；`gitcode-spec/syntax-reference/expressions.md`；`github-reference/reference/expressions.md` |

### INTENT-COMPAT-012 — 缺失的函数：`fromJSON()` / `join()` / `case()`

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub 有 `fromJSON()`（类型转换/数组构造）、`join()`（数组合并）、`case()`（条件分支）三个函数；GitCode 表达式文档未列出这三个函数。 |
| **GitHub 侧预期行为** | `fromJSON()` 可将字符串转 JSON 对象或数组、可用于数值比较的类型转换；`join()` 合并数组；`case()` 实现无嵌套 if-else。 |
| **GitCode 侧疑似行为** | 这三个函数可能不支持——使用时是报错（parser error）还是静默返回空值，待确认。 |
| **oracle 对齐方向** | **差异确认用例**——若明确不支持，需在差异清单中声明，并在报错中提示替代方案。 |
| **触发条件** | 在表达式中分别使用 `fromJSON('["a","b"]')`、`join(array, ',')`、`case(...)`，观察结果。 |
| **为什么有风险** | `fromJSON()` 用于数值比较的类型转换是 GitHub Actions 的常见模式，缺失会阻塞使用 matrix JSON 参数的高级 workflow；`join()` 用于生成标签列表等场景。历史 #75(string "3.10"→3.10) 表明类型转换正是 bug 点。 |
| **出处** | `COMPAT-NOTES.md` §3；`github-reference/reference/expressions.md`；`testing-focus.md` §6/§10；历史 #75 |

### INTENT-COMPAT-013 — GitCode 独有函数 `substring()` / `replace()` 的语义边界

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 有 `substring(str, start, len)` 和 `replace(str, old, new)` 两个 GitHub 没有的内置函数。若用户写 GitCode workflow 使用了这两个函数，再搬回 GitHub 会断裂（反之无问题）。 |
| **GitHub 侧预期行为** | 无等价内置函数，需用 shell 命令实现。 |
| **GitCode 侧疑似行为** | 文档声称支持，需验证：(a) 边界行为（start 超出长度、负值、len 为 0），(b) replace 是否替换所有匹配（全局替换 vs 首次替换）。 |
| **oracle 对齐方向** | **差异确认用例**——这是 GitCode 增强，不是问题，但需在迁移指南中标注「GitCode 独有，搬回 GitHub 需用 shell 替代」。 |
| **触发条件** | 使用 `substring(atomgit.sha, 0, 7)` 和 `replace(atomgit.ref, 'refs/heads/', '')` 观察输出。 |
| **为什么有风险** | 用户可能在 GitCode 上依赖这两个函数后，无法将 workflow 迁移回 GitHub——锁定效应。 |
| **出处** | `COMPAT-NOTES.md` §3；`gitcode-spec/syntax-reference/expressions.md` |

### INTENT-COMPAT-014 — `contains()` 字符串匹配是否区分大小写

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `contains()` 明确文档写「not case sensitive」；GitCode 的 `contains()`/`startsWith()`/`endsWith()` 文档写 `startsWith`「区分大小写」，`contains` 未写明是否区分大小写。 |
| **GitHub 侧预期行为** | `contains('Hello', 'hello')` → true（不区分大小写）。 |
| **GitCode 侧疑似行为** | `contains()` 可能区分大小写（与 `startsWith`/`endsWith` 一致），导致 `contains(github.ref, 'MAIN')` 无法匹配 `refs/heads/main`。 |
| **oracle 对齐方向** | **一致性用例**——GitCode 未声明 `contains()` 大小写行为差异，应与 GitHub 对齐（不区分大小写）。 |
| **触发条件** | `if: ${{ contains('Hello World', 'hello') }}` → 观察 job 是否执行。 |
| **为什么有风险** | 大小写差异是「看起来一样、行为不一样」的典型案例——workflow 可能在 GitHub 上匹配成功、在 GitCode 上静默跳过。 |
| **出处** | `gitcode-spec/syntax-reference/expressions.md`；`github-reference/reference/expressions.md`；`testing-focus.md` §10 |

### INTENT-COMPAT-015 — 松散相等比较的类型强转规则

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `==` 比较会 loose equality 强转：Null→0, Boolean→0/1, 空字符串→0，NaN 与任何比较返回 false。GitCode 表达式文档未描述类型强转规则。 |
| **GitHub 侧预期行为** | `${{ steps.foo.outputs.num == 1 }}` 即使 `outputs.num` 是字符串 "1"，也会强转为数字比较，返回 true。 |
| **GitCode 侧疑似行为** | 类型强转规则未知——若 `"1" == 1` 返回 false（字符串严格不等于数字），所有依赖 outputs 的数值比较都可能断裂。 |
| **oracle 对齐方向** | **一致性用例**——GitCode 未声明差异，类型强转行为应与 GitHub 一致。 |
| **触发条件** | 构造 outputs 字符串值（如 "1"）与数字 `1` 做 `==` 比较。 |
| **为什么有风险** | CI workflow 中 `steps.*.outputs.*` 都是字符串，用户习惯用它跟数字比较（如 `outputs.count > 0`）。若 GitCode 不做类型强转，这类条件全部失效。 |
| **出处** | `github-reference/reference/expressions.md`；`testing-focus.md` §10 |

### INTENT-COMPAT-016 — `inputs` 类型转换：string "3.10" → number 3.10（已证实 bug）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, reliability]` |
| **具体差异点** | 历史缺陷 #75：`workflow_dispatch` 的 `inputs` 仅支持 `string` 类型，但当用户定义 `type: string` 并传值 `"3.10"` 时，GitCode 会将字符串 `"3.10"` 隐式转换为数字 `3.10`（丢失小数末尾零）。GitHub 输入也是字符串但不会做这种转换。 |
| **GitHub 侧预期行为** | `inputs.version` 值为 `"3.10"`（字符串），用于版本号比较时保持为字符串。 |
| **GitCode 侧疑似行为** | `"3.10"` → `3.1`（隐式 number 转换），导致 Python 版本号 `3.10` 变成 `3.1`，setup-python 安装错误的版本。 |
| **oracle 对齐方向** | **一致性用例**——不应发生隐式类型转换。字符串 input 应在整个生命周期保持为字符串。 |
| **触发条件** | 定义 `inputs` string 类型，传入 `"3.10"`、`"3.0"`、`"1.20"` 等小数形式的版本号，在 job 中打印 `${{ inputs.value }}`。 |
| **为什么有风险** | 这是已被用户报告的回归缺陷（#75），导致 setup-python 安装错误版本。属「看起来一样、行为不一样」的典型——用户在 GitHub 上 `3.10` 就是 `"3.10"`，在 GitCode 上变成了 `3.1`。 |
| **出处** | 历史 #75（op-plugin）；`COMPAT-NOTES.md` §9；`testing-focus.md` §1/§10 |

---

## 三、上下文对象差异（§10 第三条 · 迁移摩擦核心）

### INTENT-COMPAT-020 — 上下文前缀 `github.*` vs `atomgit.*`（全局命名空间替换）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, usability]` |
| **具体差异点** | GitHub 核心上下文对象名为 `github.*`（如 `github.ref`），GitCode 为 `atomgit.*`（如 `atomgit.ref`）。系统环境变量同理：`GITHUB_*` → `ATOMGIT_*`（如 `GITHUB_TOKEN` → `ATOMGIT_TOKEN`、`GITHUB_OUTPUT` → `ATOMGIT_OUTPUT`）。这不是 API 差异，而是**全局命名空间替换**——任何涉及 `github.` 的表达式在 GitCode 上都会解析失败。 |
| **GitHub 侧预期行为** | `${{ github.ref }}` → 返回 `refs/heads/main`；`$GITHUB_TOKEN` 可用。 |
| **GitCode 侧疑似行为** | `${{ github.ref }}` 应报错「未知上下文」；`$GITHUB_TOKEN` 不存在、导致认证失败。 |
| **oracle 对齐方向** | **差异确认用例**——命名空间替换是已知设计差异，需验证：(a) `github.*` 引用是否给出明确报错（而非静默空值），(b) 报错信息是否提示用户替换为 `atomgit.*`。 |
| **触发条件** | 直接复制 GitHub workflow（保留 `${{ github.ref }}`）到 `.gitcode/workflows/`，触发运行。 |
| **为什么有风险** | 这是迁移摩擦的第一道门槛——任何直接用 GitHub Actions 文档编写的 workflow 都包含 `github.*`，必须全局替换。若报错不明确（「unknown context」vs 「try atomgit.ref instead」），用户体验极差。历史 #3/#20/#43/#60/#62 均为原子上下文字段缺失/返回值有误。 |
| **出处** | `COMPAT-NOTES.md` §2；`gitcode-spec/syntax-reference/context.md`；`testing-focus.md` §10/§11；历史 #3/#20/#62 |

### INTENT-COMPAT-021 — `atomgit.*` 上下文字段完备性（对比 `github.*` 缺失字段）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `github.*` 上下文有 25+ 属性；GitCode `atomgit.*` 文档列了 18 个属性。确认缺失的关键字段：`github.actor`/`github.actor_id`（触发者）、`github.event_path`（事件文件路径）、`github.workflow_ref`/`github.workflow_sha`（workflow 文件信息）、`github.triggering_actor`（重试触发者）、`github.ref_protected`（分支保护）、`github.action_ref`/`github.action_repository`。 |
| **GitHub 侧预期行为** | 以上属性均可通过 `${{ github.xxx }}` 访问并返回有效值。 |
| **GitCode 侧疑似行为** | 缺失的字段访问时是返回空值、报错、还是降级为同义替代字段？ |
| **oracle 对齐方向** | **差异确认用例**——GitCode 需明确声明 atomgit 上下文与 github 上下文的属性映射表，并注明哪些 GitHub 属性无等价物。 |
| **触发条件** | 分别引用 `atomgit.actor`、`atomgit.workflow_sha`、`atomgit.ref_protected` 等检查是否回值。 |
| **为什么有风险** | `actor` 常用于审计日志/通知（workflow run 由谁触发），`workflow_ref` 用于动态重跑工作流——这些字段缺失会限制 security/audit 类 workflow。历史 #3/#43/#45 多次反映上下文字段不完整。 |
| **出处** | `COMPAT-NOTES.md` §2；`gitcode-spec/syntax-reference/context.md`；`github-reference/reference/contexts.md`；历史 #3/#20/#43 |

### INTENT-COMPAT-022 — `runner` 上下文字段值格式差异（`runner.os` / `runner.arch`）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | 历史用例 TC-137/138/095 已验证：GitCode `runner.os` 返回 `linux`（小写），但文档宣称应返回 `Linux`（首字母大写）；`runner.arch` 返回 `x86_64`，但文档宣称应返回 `X64`。GitHub 返回 `Linux`（首字母大写）和 `X64`。 |
| **GitHub 侧预期行为** | `runner.os` → `Linux`；`runner.arch` → `X64`。 |
| **GitCode 侧疑似行为** | `runner.os` → `linux`（小写）；`runner.arch` → `x86_64`（Linux 原生格式而非文档声明的 `X64`）。 |
| **oracle 对齐方向** | **一致性用例**——文档声明应与 GitHub 对齐（`Linux`/`X64`），实际返回值应与文档一致。要么修代码，要么修文档。 |
| **触发条件** | `echo "${{ runner.os }}"` 和 `echo "${{ runner.arch }}"`，对照文档声明。 |
| **为什么有风险** | 若用户用 `if: ${{ runner.os == 'Linux' }}` 判断平台，小写 `linux` 会导致条件永远不成立——静默跳过所有 Linux 专属逻辑。 |
| **出处** | 历史 TC-137/138/095；`gitcode-spec/syntax-reference/context.md`；`github-reference/reference/contexts.md` |

### INTENT-COMPAT-023 — `strategy` 上下文字段支持（`job-total` / `job-index`）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `strategy` 上下文提供 `strategy.fail-fast`、`strategy.job-index`（0-based）、`strategy.job-total`、`strategy.max-parallel`。GitCode 文档声明支持 `strategy.job-index`，但未提及 `strategy.job-total` 和 `strategy.max-parallel`。 |
| **GitHub 侧预期行为** | `strategy.job-total` → 矩阵 job 总数；`strategy.max-parallel` → 最大并行数。 |
| **GitCode 侧疑似行为** | `strategy.job-total` 和 `strategy.max-parallel` 可能未实现——访问时可能返回空值。 |
| **oracle 对齐方向** | **一致性用例**——若 GitCode 未声明不支持这两个字段，应与 GitHub 对齐。 |
| **触发条件** | 在 matrix 场景下输出 `${{ strategy.job-total }}` 和 `${{ strategy.max-parallel }}`，对比预期值。 |
| **为什么有风险** | `strategy.job-total` 常用于「最后一个 matrix job 做汇总」模式（`if: ${{ strategy.job-index == strategy.job-total - 1 }}`），缺失会导致无法实现汇总步骤。 |
| **出处** | `gitcode-spec/syntax-reference/context.md` §2.4；`github-reference/reference/contexts.md`；`testing-focus.md` §3 |

---

## 四、触发与过滤语义差异（§10 第三/四条）

### INTENT-COMPAT-030 — `pull_request` types 命名差异（open/update/reopen/merge vs opened/synchronize/reopened/closed）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode `pull_request` types 取值 `[open, reopen, update, merge]`；GitHub 为 `[opened, synchronize, reopened, closed]`（共 18+ 种）。两个差异：(1) 命名——`open` vs `opened`、`update` vs `synchronize`、(2) 取值——GitCode 有 `merge`（GitHub 用 `closed`+merged 判断）。 |
| **GitHub 侧预期行为** | 默认 types `[opened, synchronize, reopened]`；合并用 `closed` + `github.event.pull_request.merged` 判断。 |
| **GitCode 侧疑似行为** | 默认 types `[open, reopen, update]`；合并需用 `merge` type。若用户写 GitHub 风格的 `types: [opened, synchronize]`，GitCode 是否报错还是静默忽略？ |
| **oracle 对齐方向** | **差异确认用例**——已知差异，需验证：(a) GitHub 风格的 types 值是否被静默忽略（若忽略则 PR 永远不会触发），(b) 报错是否明确指引正确的 GitCode types 值。 |
| **触发条件** | 分别写 `types: [opened]` 和 `types: [open]`，创建 PR 观察触发情况。 |
| **为什么有风险** | 这是「看起来一样、行为不一样」的高频踩坑点——用 GitHub 文档写的 `types: [opened, synchronize]` 在 GitCode 上永远不会触发，但 yaml 语法检查可能不报错。历史 TC-064 已证实 PR 状态返回值 `opened` vs `open` 不一致。 |
| **出处** | `COMPAT-NOTES.md` §5；`gitcode-spec/syntax-reference/trigger-events.md`；`github-reference/reference/events.md`；历史 TC-064/234/561 |

### INTENT-COMPAT-031 — `pull_request_target` 对 fork PR 的安全隔离是否等效

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, security]` |
| **具体差异点** | GitHub `pull_request_target`：工作流在 base 上下文运行、使用 base 分支的 workflow 文件、`GITHUB_TOKEN` 有 read/write 权限（即使来自 public fork）。GitCode 文档声明 fork PR 场景下 `pull_request` TOKEN 仅 read、`pull_request_target` 可访问 Secret——**语义与 GitHub 一致**。但历史 #51（fork PR 可获取主仓密钥）和 #66（pull_request_target fork PR secret 隔离未实现）表明实际隔离可能有问题。 |
| **GitHub 侧预期行为** | `pull_request_target` 下可访问 secrets，但 fork PR 场景下仍有安全边界（不能 checkout PR head.sha 后执行不可信代码）。 |
| **GitCode 侧疑似行为** | 语义声明一致，但历史 #51/#66 暗示隔离可能不完整——需逐条实测：(a) fork PR + `pull_request`→secrets 不可读，(b) fork PR + `pull_request_target`→可读但不应执行 PR 代码。 |
| **oracle 对齐方向** | **一致性用例**——安全隔离强度应与 GitHub 一致；任何差异均为 blocker。 |
| **触发条件** | fork 仓库提 PR，观察：(a) `pull_request` 事件能否通过 `${{ secrets.XXX }}` 读到仓库 secrets，(b) `pull_request_target` + checkout `head.sha` 后执行代码的权限边界。 |
| **为什么有风险** | 这是安全命脉——若 fork PR 能读到仓库 secrets，攻击者只需 fork + 提 PR 即可泄露凭据。历史 #51 已经报告了这个问题。 |
| **出处** | `COMPAT-NOTES.md` §8；`gitcode-spec/security-permissions/token-permissions.md`；历史 #51/#66；`testing-focus.md` §5；RISK-SEC-01 |

### INTENT-COMPAT-032 — `pull_request_comment` 事件（GitCode 独有）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 有 `pull_request_comment` 触发事件（支持 `comments` 正则过滤），GitHub 没有独立事件，靠 `issue_comment` + `github.event.issue.pull_request` 字段区分。 |
| **GitHub 侧预期行为** | 用 `on: issue_comment` 触发，在 job 内通过 `if: ${{ github.event.issue.pull_request }}` 过滤。 |
| **GitCode 侧疑似行为** | `pull_request_comment` 可直接按评论内容正则过滤（`comments: ['/deploy']`），比 GitHub 模式更简洁。需验证 `comments` 过滤是否按完整匹配还是子串匹配。 |
| **oracle 对齐方向** | **差异确认用例**——这是 GitCode 增强特性，不是兼容性问题。但需在迁移指南中标注「GitHub 无等价事件，需改写为 `issue_comment`+条件判断」。 |
| **触发条件** | 配置 `pull_request_comment` + `comments: ['/deploy']`，在 PR 中发评论 `/deploy` 和 `deploy now`，观察触发情况。 |
| **为什么有风险** | 迁移锁定效应——在 GitCode 上用 `pull_request_comment` 写的 workflow 无法直接搬回 GitHub。历史 #57 报告了 `if: contains(atomgit.event.comment.body, '/deploy')` 报错。 |
| **出处** | `COMPAT-NOTES.md` §5；`gitcode-spec/syntax-reference/trigger-events.md` |

### INTENT-COMPAT-033 — `paths` 匹配文件数量上限差异（300 vs 3000+1000）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, reliability]` |
| **具体差异点** | GitCode 声明 `paths`/`paths-ignore` 仅匹配「前 300 个变更文件」，超出不参与判断。GitHub 有两层限制：(1) push 含 >1000 commits 则**总是运行**工作流，(2) diff 含 >3000 文件且匹配文件不在前 3000 则**不运行**。 |
| **GitHub 侧预期行为** | 阈值 3000 文件 + 1000 commits，超出时行为明确（必定运行/必定不运行）。 |
| **GitCode 侧疑似行为** | 阈值 300 文件——比 GitHub 低 10 倍。中等规模 monorepo 的一次变更可能超 300 文件，paths 过滤在边界时可能漏触发或误触发。 |
| **oracle 对齐方向** | **差异确认用例**——阈值差异需在文档中声明。需验证：(a) 超出 300 文件时是完全跳过 paths 过滤（全部触发）还是只匹配前 300，(b) 是否影响 `paths-ignore`。 |
| **触发条件** | 构造一次 commit 变更 301 个文件，第 301 个文件匹配 `paths` 指定的模式，观察是否触发。 |
| **为什么有风险** | monorepo 场景下一次 PR 涉及 300+ 文件并非罕见；paths 过滤是最佳实践——用户用 `paths:` 来避免无关事件触发 CI。若 300 阈值导致 paths 失效，CI 就会漏执行或滥执行。 |
| **出处** | `COMPAT-NOTES.md` §5；`gitcode-spec/syntax-reference/trigger-events.md`；`github-reference/reference/workflow-syntax.md`（paths diff） |

### INTENT-COMPAT-034 — `schedule` 时区与时区支持

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `schedule` 支持 `timezone` 字段（IANA 时区名，如 `America/New_York`）；GitCode 仅 UTC。GitHub public repo 的 scheduled workflow 在 60 天无活动后自动禁用；GitCode 无此声明。两者均在默认分支上运行，最短间隔 5 分钟。 |
| **GitHub 侧预期行为** | `cron: '0 8 * * 1-5'` + `timezone: 'Asia/Shanghai'` → 北京时间工作日 8:00 执行。 |
| **GitCode 侧疑似行为** | 无 `timezone` 字段——所有 cron 用 UTC，中国用户需手动换算（UTC+8）。 |
| **oracle 对齐方向** | **差异确认用例**——需在文档中声明「仅支持 UTC，不支持 timezone 字段」。 |
| **触发条件** | 在 `schedule` 中写 `timezone: 'Asia/Shanghai'`，观察是报错还是静默忽略。 |
| **为什么有风险** | 如果中国用户以为 cron 是北京时间（`0 8 * * *` = 每天 8:00），实际会变成 UTC 8:00 = 北京时间 16:00——时机错误。历史 S3×24+TC-391 报告了多仓库 cron 从未触发。 |
| **出处** | `COMPAT-NOTES.md` §5；`gitcode-spec/syntax-reference/trigger-events.md`；`github-reference/reference/workflow-syntax.md`；历史 TC-391 |

---

## 五、不支持能力的降级方式（§10 第五条）

### INTENT-COMPAT-040 — 不支持的 `workflow_dispatch` inputs 类型：非 string 的降级行为

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, usability]` |
| **具体差异点** | GitHub `workflow_dispatch.inputs` 支持 `boolean`/`choice`/`number`/`environment`/`string` 五种类型；GitCode 仅支持 `string`。若用户写 `type: boolean` 或 `type: choice`，GitCode 应如何响应？ |
| **GitHub 侧预期行为** | `type: boolean` → UI 提供勾选框，值为 `'true'`/`'false'` 字符串。 |
| **GitCode 侧疑似行为** | 非 `string` 的 type 声明可能：(a) 解析报错（最理想——用户知道要改），(b) 静默忽略降为 string（用户传入 `true` 变成字符串 `'true'`），(c) 整个 workflow 无法触发。 |
| **oracle 对齐方向** | **一致性用例**——非 string 类型应明确报错（解析阶段），且报错信息应指出「仅支持 string 类型，需用表达式进行类型转换」。静默降级会掩盖问题。 |
| **触发条件** | 定义 `type: boolean` 的 input，尝试触发 workflow_dispatch，观察行为。 |
| **为什么有风险** | boolean/choice/number 是 GitHub Actions 的常用输入类型，从 GitHub 迁移的 workflow 几乎必然包含非 string 的 inputs。若静默降为 string，`if: ${{ inputs.dry_run }}` 会因 `'true'` 是 truthy 字符串而永远为 true。历史 #23 报告手动传参未指定 type 导致无法触发。 |
| **出处** | `COMPAT-NOTES.md` §9；`gitcode-spec/syntax-reference/trigger-events.md` §1.6；`github-reference/reference/workflow-syntax.md`；历史 #23 |

### INTENT-COMPAT-041 — 不支持的 YAML 字段/属性：静默忽略 vs 报错

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, usability]` |
| **具体差异点** | GitHub workflow 有 `run-name` 字段（自定义运行名称）；GitCode 文档未提及此字段。GitHub `runs.using` 支持 `node20`/`docker`/`composite`；GitCode 文档仅列 `node16`。GitHub `environment` 字段用于部署环境保护规则；GitCode 文档有 environment 概念但历史 TC-010 显示「不被平台识别」。若用户在 GitCode workflow 中使用这些字段，是报错还是静默忽略？ |
| **GitHub 侧预期行为** | 这些字段均有明确语义和运行时效果。 |
| **GitCode 侧疑似行为** | 未知字段的降级方式不统一——可能：(a) YAML 解析报错（最安全），(b) 静默忽略（最隐蔽——用户以为生效了实际没有），(c) 部分字段有行为但未文档化。 |
| **oracle 对齐方向** | **差异确认用例**——应统一降级策略：不支持的能力在解析阶段报错，不应静默忽略。至少文档应列出「不支持的 GitHub 字段清单」。 |
| **触发条件** | 在 GitCode workflow 中使用 `run-name`、`environment`、`runs.using: node20`，观察是报错还是运行。 |
| **为什么有风险** | 静默忽略是最危险的行为——用户设了 `run-name` 以为运行名会按预期显示，实际却是默认名；设了 `environment` 以为有审批保护，实际没有。历史 TC-010 已确认 environment 被报 `unknown property`。 |
| **出处** | `COMPAT-NOTES.md` §10；`github-reference/reference/workflow-syntax.md`；历史 TC-010/273 |

### INTENT-COMPAT-042 — Composite Action 不支持

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub 支持 composite action（`runs.using: composite`），可在单个 action 中组合多个 step；GitCode 文档 `runs.using` 仅列 `node16`，历史 #41 明确记录「当前不支持复合操作（composite action）特性」。 |
| **GitHub 侧预期行为** | `action.yml` 中 `runs.using: composite` + `steps:` → 所有 step 在同一 job 上下文中执行。 |
| **GitCode 侧疑似行为** | 使用 composite action 时任务失败且无报错信息（历史 #41）。 |
| **oracle 对齐方向** | **差异确认用例**——若明确不支持 composite action，需在文档中声明并给出替代方案（如用 `workflow_call` 代替）。报错必须明确。 |
| **触发条件** | 定义一个 composite action 并在 workflow 中引用，观察是报错还是失败无日志。 |
| **为什么有风险** | composite action 是 GitHub Actions 生态中广泛使用的复用模式，用于封装可复用的 step 集合。不支持 composite action 意味着大量第三方 action 不可用。 |
| **出处** | `COMPAT-NOTES.md` §10；`gitcode-spec/action-development/action-yml-metadata-syntax.md`；历史 #41 |

### INTENT-COMPAT-043 — `workflow_call` 嵌套深度限制（最多 2 层）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 文档声明 `workflow_call` 最多嵌套 2 层；GitHub 可嵌套至 10 层。GitCode 还限制 `workflow_call` 的 inputs 仅 string 类型，且调用方 `uses:` 不支持 `${{ }}` 表达式（历史 #82）。 |
| **GitHub 侧预期行为** | 可嵌套 10 层；`uses:` 可含表达式（如 `uses: ${{ github.repository }}/.github/workflows/build.yml@main`）。 |
| **GitCode 侧疑似行为** | 超过 2 层嵌套可能：(a) 解析报错，(b) 运行时失败无明确原因。`uses:` 含表达式时报错「Self-hosted 执行机未注册」（历史 #68/82）。 |
| **oracle 对齐方向** | **差异确认用例**——已知限制，需验证：(a) 3 层嵌套是否给出明确的层数限制报错，(b) 文档是否写明最多 2 层。 |
| **触发条件** | A calls B, B calls C, C calls D——验证 3 层时是否报错。 |
| **为什么有风险** | `workflow_call` 的嵌套限制直接影响 workflow 模块化程度；历史 #30（workflow_call 无法拉起子任务却显示完成）表明 workflow_call 本身稳定性也有问题。 |
| **出处** | `COMPAT-NOTES.md` §5；历史 #30/#68/#82/#84/#85 |

### INTENT-COMPAT-044 — Docker daemon 在托管 Runner 上的可用性

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub 托管 Runner 默认提供了 Docker daemon（可直接用 `docker build`/`docker run`）；GitCode 历史 #86 明确记录「官方 Runner 有 docker 但没有可连接的 daemon、默认资源池不支持启 docker 镜像」。 |
| **GitHub 侧预期行为** | `run: docker build -t myimage .` 在 GitHub-hosted ubuntu-latest runner 上可直接执行。 |
| **GitCode 侧疑似行为** | Docker CLI 可能安装但 daemon 不可用——任何 `docker` 命令都会因连接拒绝而失败。 |
| **oracle 对齐方向** | **差异确认用例**——需在文档中明确声明托管 Runner 的 Docker 支持状态，并提供替代方案（如使用 `official_build_push` 插件）。 |
| **触发条件** | 在托管 Runner 上执行 `docker ps`，观察是成功还是 `Cannot connect to the Docker daemon`。 |
| **为什么有风险** | Docker 是 GitHub Actions 中最常用的容器操作工具；若 daemon 不可用，大量构建/测试 workflow 需改写为使用 GitCode 的 docker 插件。 |
| **出处** | 历史 #86；`github-reference/reference/workflow-syntax.md`（container 字段）；`testing-focus.md` §4 |

---

## 六、内置 Action 差异（§10 第六条）

### INTENT-COMPAT-050 — Action 引用格式差异（`uses:` 短名 vs `owner/repo@ref`）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, usability]` |
| **具体差异点** | GitCode 内置 action 使用无 owner 短名（如 `uses: checkout`、`uses: setup-node`）；GitHub 使用 `uses: actions/checkout@v4` 带 owner+版本。若迁移时保留 GitHub 格式 `uses: actions/checkout@v4`，GitCode 会如何响应？ |
| **GitHub 侧预期行为** | `uses: actions/checkout@v4` → 从 GitHub Actions marketplace 拉取 `actions/checkout` 的 v4 tag。 |
| **GitCode 侧疑似行为** | `uses: actions/checkout@v4` 可能：(a) 报错「action not found」，(b) 如果仓库下存在 `actions/checkout` 路径则引用本地 action，(c) 尝试从外部仓库拉取。 |
| **oracle 对齐方向** | **差异确认用例**——引用格式差异需在迁移指南中明确，报错信息应指引用户替换为 GitCode 的短名。 |
| **触发条件** | 在 `.gitcode/workflows/test.yml` 中使用 `uses: actions/checkout@v4`，观察执行结果。 |
| **为什么有风险** | GitHub workflow 中的 `uses:` 行是最常见的配置项——几乎所有 GitHub workflow 都以 `uses: actions/checkout@v4` 开头。若 GitCode 对此无明确报错，用户会浪费时间排查为什么 checkout 没生效。 |
| **出处** | `COMPAT-NOTES.md` §10；`gitcode-spec/writing-pipelines/using-actions.md`；历史 #36(setup-node 报错)/#82(uses 不支持表达式) |

### INTENT-COMPAT-051 — `checkout` 插件的 PR 预合并（pre-merge）行为

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `actions/checkout` 在 `pull_request` 事件下默认 checkout merge commit（`refs/pull/<number>/merge`——即 PR 源分支与目标分支的预合并结果）。GitCode 的 `checkout` 插件历史 #25 和 #71 明确记录「不支持 PR 预合并」——checkout 的是源分支 `head.ref`，而非 merge commit。 |
| **GitHub 侧预期行为** | `pull_request` 事件下 `GITHUB_SHA` = merge commit SHA，checkout 的是合并结果——检测到冲突时也有临时合并产物。 |
| **GitCode 侧疑似行为** | checkout 的是源分支 head commit，不执行预合并。CI 测试的是「源分支独立能否通过」，而非「合并后能否通过」。 |
| **oracle 对齐方向** | **差异确认用例**——这属于核心行为差异，需在文档中明确声明：(a) checkout 不执行预合并，(b) 对 CI 验证语义的影响。 |
| **触发条件** | PR 中源分支与目标分支有文件冲突，触发 `pull_request` workflow，观察 checkout 结果。 |
| **为什么有风险** | 这是「看起来一样、行为不一样」的典型案例——用户在 GitHub 上 CI 验证的是 merge 后的状态（代表真实合并结果），在 GitCode 上验证的是源分支独立状态（不保证合并后可用）。若合并有冲突，GitHub 会提前暴露，GitCode 会在合并后才暴露。 |
| **出处** | 历史 #25(openlibing)/#71(mindie)；`github-reference/reference/events.md`（PR merge commit 行为） |

### INTENT-COMPAT-052 — `cache` 插件跨 job/跨 run 作用域与 key 行为

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `actions/cache` 有明确的 cache key 匹配（`key` + `restore-keys`）和命中（cache-hit）输出；GitCode `cache` 插件文档需对照验证：(a) `restore-keys` 是否支持前缀降级匹配，(b) cache 跨分支隔离策略，(c) fork PR 是否可写 cache。历史 #90 报告「插件找不到」。 |
| **GitHub 侧预期行为** | cache key 精确匹配命中、restore-keys 前缀降级、cache-hit 输出布尔值、跨分支隔离（同分支 scope）。 |
| **GitCode 侧疑似行为** | `restore-keys` 是否支持、fork PR 是否隔离 cache 写（cache 投毒面）均待测。 |
| **oracle 对齐方向** | **一致性用例**——cache 语义应与 GitHub 一致，尤其是 fork PR 不应写 cache（否则构成 cache 投毒）。 |
| **触发条件** | (1) 先写 cache key `node-deps-linux`，后以 `restore-keys: node-deps-` 恢复；(2) fork PR 中写 cache，主分支 PR 中读 cache。 |
| **为什么有风险** | Cache 投毒是已知的 CI/CD 攻击面——若 fork PR 能写主分支 cache，攻击者可在缓存中植入恶意编译产物。 |
| **出处** | `gitcode-spec/writing-pipelines/using-dependency-cache.md`；历史 #90；`testing-focus.md` §8 |

---

## 七、Runner 标签/环境差异（§10 第七条）

### INTENT-COMPAT-060 — `runs-on` 标签格式：三段式 vs 单标签

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 三段式 `runs-on: [{os-version}, {arch}, {flavor}]`（如 `[ubuntu-latest, x64, small]`）；GitHub 单标签 `runs-on: ubuntu-latest`。若直接从 GitHub 迁移 `runs-on: ubuntu-latest`，GitCode 能否识别为 `default`？ |
| **GitHub 侧预期行为** | `runs-on: ubuntu-latest` → 分配最新 Ubuntu 版本的 GitHub-hosted runner。 |
| **GitCode 侧疑似行为** | `runs-on: ubuntu-latest`（单字符串而非数组）可能：(a) 报错，(b) 被当作自托管 runner label，(c) 被识别为 `default` 等价形式。 |
| **oracle 对齐方向** | **差异确认用例**——需验证：(a) 单标签写法是否被接受，(b) 不接受的报错是否指引用户使用三段式格式。 |
| **触发条件** | 分别写 `runs-on: ubuntu-latest`（GitHub 风格）和 `runs-on: [ubuntu-latest, x64, small]`（GitCode 风格），观察是否都能成功调度。 |
| **为什么有风险** | `runs-on` 是 workflow 的必填字段——迁移摩擦的第一纠结点。若 GitHub 风格直接报错，每份迁移 workflow 都要改 `runs-on`。 |
| **出处** | `COMPAT-NOTES.md` §7；`gitcode-spec/writing-pipelines/configure-jobs.md`；`testing-focus.md` §4 |

### INTENT-COMPAT-061 — 预装工具链差异（node/python/go/java 版本矩阵）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub Runner 镜像有公开的工具链版本清单（如 ubuntu-latest 预装 Node 18/20、Python 3.8-3.12…）；GitCode 托管 Runner 预装工具链版本不透明。历史 #26(setup-python 指定版本异常需要特定 runner 标签)、#50(setup-* 未说明支持版本)、#59(setup-jdk 不支持 java21)、#92(EulerOS 2.0 不支持)。 |
| **GitHub 侧预期行为** | Runner 预装工具版本可通过文档查询，`setup-*` action 覆盖了广泛的版本范围。 |
| **GitCode 侧疑似行为** | 预装版本可能较旧或不全；`setup-*` 插件的版本覆盖范围有限（setup-jdk 不支持 Java 21、setup-python 仅 9 个版本）。 |
| **oracle 对齐方向** | **差异确认用例**——不是要「与 GitHub 完全一致」，而是要求文档公开 Runner 镜像的预装工具版本矩阵，让用户知道哪些版本可用、哪些需自行安装。 |
| **触发条件** | 在默认 Runner 上执行 `node --version`、`python3 --version`、`java -version`、`go version`，对照文档。 |
| **为什么有风险** | 用户基于 GitHub Runner 的工具链版本写 CI 脚本，迁移到 GitCode 后发现 Node/Python 版本不匹配，setup-* 又不能安装所需版本——CI 脚本需大量改写。 |
| **出处** | `gitcode-spec/runner-management/using-hosted-runners.md`；历史 #26/#50/#59/#92/#98 |

---

## 八、执行模型差异（§10 综合）

### INTENT-COMPAT-070 — `stages` 阶段机制 vs `needs` DAG（GitCode 特有编排模型）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 有顶层 `stages` 概念（阶段间串行、阶段内 job 并行、`stages.fail_fast` 阶段级快速失败）。GitHub 没有 `stages`，通过 `needs` DAG 实现任意依赖拓扑。`stages` 是 GitCode 独有的编排抽象。 |
| **GitHub 侧预期行为** | 仅 `jobs.<id>.needs` 定义依赖关系；无 `stages` 概念。 |
| **GitCode 侧疑似行为** | `stages` 提供了比 `needs` DAG 更简单的「阶段串行 + 阶段内并行」模式——这是 GitCode 的增强。但需验证：(a) `stages` 和 `needs` 同时使用时的优先级，(b) `stages.fail_fast` 与 `strategy.fail-fast` 的交互。 |
| **oracle 对齐方向** | **差异确认用例**——`stages` 是 GitCode 特有增强，不构成兼容性问题。但需在迁移指南中标注「若需要阶段串行，GitHub 用 needs DAG 实现，GitCode 可用 stages 简化」。 |
| **触发条件** | 定义 2 个 stage 各有 2 个 job，验证：stage 间串行、stage 内并行、`fail_fast: true` 时前阶段失败是否取消后阶段。 |
| **为什么有风险** | 增强特性也可能引入 bug——`stages.fail_fast` 与 `strategy.fail-fast` 语义不同（阶段级 vs 矩阵级），用户容易混淆。 |
| **出处** | `COMPAT-NOTES.md` §4；`gitcode-spec/writing-pipelines/configure-jobs.md`；`testing-focus.md` §3 |

### INTENT-COMPAT-071 — `post` 顶层后处理阶段（GitCode 独有）vs GitHub 仅 action 内 `post`

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitCode 顶层 `post` 字段（`run_always: true` 默认）在所有 job 完成后执行后处理步骤；GitHub 没有顶层 `post`，仅在 action 的 `action.yml` 内有 `post` 钩子（在 action 的 job 结束时执行）。 |
| **GitHub 侧预期行为** | 要实现「全部 job 完成后的清理步骤」，需定义最后的 cleanup job 且 `if: ${{ always() }}` + `needs` 所有 job。 |
| **GitCode 侧疑似行为** | `post` 自动在所有 job 完成后执行，无需显式声明依赖——比 GitHub 简洁。需验证 `post` 是否在作业被取消时仍执行（运行清理）。 |
| **oracle 对齐方向** | **差异确认用例**——`post` 是 GitCode 的便利增强。迁移到 GitHub 时需改写为 cleanup job。 |
| **触发条件** | 定义 `post`（执行清理 echo），手动取消 workflow，观察 post 是否仍执行。 |
| **为什么有风险** | 若用户在 `post` 中做了关键清理（释放资源、通知），迁移回 GitHub 时会被遗漏。 |
| **出处** | `COMPAT-NOTES.md` §4；`gitcode-spec/writing-pipelines/configure-jobs.md` |

### INTENT-COMPAT-072 — `concurrency` 字段命名与语义差异

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub `concurrency` 字段：`group`（并发组）+ `cancel-in-progress`（boolean）+ `queue`（`single`/`max` N）。GitCode `concurrency` 字段：`enable`（boolean）+ `max`（int）+ `exceed-action`（`QUEUE`/`IGNORE`/`REPLACE`）+ `preemption`（boolean）。字段名和语义完全不同——不是参数名不同，而是并发控制模型不同。 |
| **GitHub 侧预期行为** | 并发组基于 `group` 字符串匹配；`cancel-in-progress: true` 时新运行取消旧运行。 |
| **GitCode 侧疑似行为** | `enable: true` / `max: 1` / `exceed-action: IGNORE` → 行为可能等价于 GitHub 的 `group` + `cancel-in-progress: false`。但 `exceed-action: REPLACE` 和 GitHub 的 `cancel-in-progress: true` 是否等价待验证。 |
| **oracle 对齐方向** | **差异确认用例**——并发控制模型完全不同，迁移时必须重写 `concurrency` 块。需在文档中提供 GitHub→GitCode 的映射表。 |
| **触发条件** | 同一 `concurrency` group 快速连续触发 3 次运行，观察排队/取代行为。 |
| **为什么有风险** | `concurrency` 的语义差异可能直接导致「部署被意外取消」或「排队长达数小时」——这是生产事故级差异。 |
| **出处** | `COMPAT-NOTES.md` §4；`gitcode-spec/writing-pipelines/configure-jobs.md`；`github-reference/reference/workflow-syntax.md` |

### INTENT-COMPAT-073 — Workflow 文件目录 `.gitcode/workflows/` vs `.github/workflows/`

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, usability]` |
| **具体差异点** | GitCode 工作流文件需放在 `.gitcode/workflows/` 目录，仅识别 `.yml`/`.yaml` 文件；GitHub 是 `.github/workflows/`。若仓库同时存在两个目录—— |
| **GitHub 侧预期行为** | 仅扫描 `.github/workflows/` 中的 `.yml`/`.yaml` 文件。 |
| **GitCode 侧疑似行为** | 仅扫描 `.gitcode/workflows/`。若仓库只有 `.github/workflows/`，GitCode 不应识别任何工作流（即迁移必须移动文件）。需验证历史 #17：同步代码后 Actions 不识别配置，需手动修改 yml 才能识别。 |
| **oracle 对齐方向** | **差异确认用例**——目录差异是已知设计差异，但需验证：(a) 是否提供「自动迁移」机制（将 `.github/workflows/` 的内容拷贝到 `.gitcode/workflows/`），(b) 不存在时是否给出友好提示。 |
| **触发条件** | 仓库仅有 `.github/workflows/test.yml`，触发 push 事件，观察是否显示工作流。 |
| **为什么有风险** | 迁移的第一道门槛——文件放错目录就直接「什么也不发生」，无任何错误提示。历史 #17 还报告了识别滞后（需手动修改才能识别）。 |
| **出处** | `COMPAT-NOTES.md` §1；`gitcode-spec/writing-pipelines/workflow-file-location-structure.md`；历史 #17 |

---

## 九、权限模型差异（§10 综合 · 安全敏感）

### INTENT-COMPAT-080 — `permissions` 权限域命名差异（`project/pr/issue/note/repository/hook` vs `contents/pull-requests/issues/actions...`）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, security]` |
| **具体差异点** | GitCode `permissions` 权限域：`project`/`pr`/`issue`/`note`/`repository`/`hook`，每个可取值 `read`/`write`/`none`。GitHub 权限域：`contents`/`pull-requests`/`issues`/`actions`/`checks`/`deployments`/`pages`… 18 个 scope。命名完全不同——不是映射关系变化，而是**权限划分粒度不同**。 |
| **GitHub 侧预期行为** | `permissions: contents: read` 同时控制代码读取、release/tag 等。 |
| **GitCode 侧疑似行为** | `permissions: repository: read` 等价于 `contents: read`；`permissions: pr: write` ≈ `pull-requests: write`。但 GitHub 的 `actions: write`（管理自身 workflow runs）在 GitCode 没有对应域——可能是 `project: write`。GitHub 的 `id-token: write`（OIDC）在 GitCode 完全无对应。 |
| **oracle 对齐方向** | **差异确认用例**——权限域的映射关系需在文档中提供 GitHub→GitCode 对照表，并在迁移指南中作为必改项标注。 |
| **触发条件** | 写 GitHub 风格的 `permissions: contents: read`，观察是解析报错还是静默忽略。 |
| **为什么有风险** | 权限域命名差异意味着**每份迁移 workflow 的 `permissions` 块都需逐行改写**——任何遗漏都会导致权限不正确（要么过宽有安全风险，要么过窄导致 API 调用失败）。 |
| **出处** | `COMPAT-NOTES.md` §6；`gitcode-spec/security-permissions/token-permissions.md`；`github-reference/reference/workflow-syntax.md` |

---

## 十、特别关注的已知实证缺陷

### INTENT-COMPAT-090 — `uses:` 字段不支持 `${{ }}` 表达式（已证实）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | GitHub 允许 `uses: ${{ github.repository }}/.github/workflows/caller.yml@main`（动态引用 action 路径）；GitCode 历史 #82 明确记录 `uses: ${{ atomgit.repository }}` 会导致 checkout 执行失败——`uses` 不解析表达式。 |
| **GitHub 侧预期行为** | `uses` 支持表达式求值，动态构造 action 路径。 |
| **GitCode 侧疑似行为** | `uses` 中的表达式不解析，可能被当作字面路径（导致 action not found）或直接报错。 |
| **oracle 对齐方向** | **差异确认用例**——需在文档中明确声明 `uses` 不支持表达式，报错信息应指出这一点（而非泛化的「action not found」）。 |
| **触发条件** | `uses: ${{ atomgit.repository }}/.gitcode/workflows/ci.yml@main`，观察是否成功调用。 |
| **为什么有风险** | 用户可能用动态路径来引用同一个 repo 下的 workflow——这是 monorepo 的常见模式。若不支持，所有动态引用都需改为硬编码路径。 |
| **出处** | 历史 #82(op-plugin)；`github-reference/reference/workflow-syntax.md` |

### INTENT-COMPAT-091 — `matrix` job 的 `needs` 依赖导致「任务初始化错误」（已证实 bug）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, reliability]` |
| **具体差异点** | 当 job A 的 `needs` 指向一个 matrix job B（B 通过 `strategy.matrix` 展开为多个实例），且 B 全部成功，job A 仍然可能报「任务初始化错误」。历史 #101 和 TC-486/481/499 都报告了这个 bug。GitHub 上 `needs` 指向 matrix job 后，job A 会等待 B 的所有实例完成。 |
| **GitHub 侧预期行为** | `needs: [build]` 中 `build` 是 matrix job 时，默认等待所有 matrix 实例完成，job A 正常启动。 |
| **GitCode 侧疑似行为** | 所有 `build` 实例成功，但 `needs` 依赖 job A 仍报「初始化错误」——疑似依赖解析无法正确处理 matrix 展开后的多实例。 |
| **oracle 对齐方向** | **一致性用例**——`needs` 对 matrix job 的语义应与 GitHub 一致；这是已确认的缺陷，应回归修复。 |
| **触发条件** | 定义一个 matrix job `build`（3 个实例）+ 一个 `needs: build` 的 job `test`，观察 `test` 是否在 `build` 完成后正常启动。 |
| **为什么有风险** | 这是真实的用户报告 P1 缺陷——matrix + needs 是 CI 中最常见的组合模式之一，不可用意味着矩阵构建后的汇总/部署步骤全部卡死。 |
| **出处** | 历史 #101(mindcluster)；TC-486/481/499 |

### INTENT-COMPAT-092 — YML 缓存未更新：子 workflow 修改后仍执行旧代码（已证实 bug）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility, reliability]` |
| **具体差异点** | 历史 #85：更新了被 `workflow_call` 引用的子 workflow YML 文件后，触发主 workflow 时子 workflow 仍使用旧版本代码。这表明 GitCode 对 `workflow_call` 的目标 YML 有缓存，未在触发时重新读取。 |
| **GitHub 侧预期行为** | 每次 `workflow_call` 触发时，实时读取被引用 workflow 的 YML 文件（使用调用方指定的 ref）。 |
| **GitCode 侧疑似行为** | 子 workflow YML 被缓存，更新后不会立即生效——用户观察到「用的还是旧代码」。 |
| **oracle 对齐方向** | **一致性用例**——`workflow_call` 应始终使用最新 YML 定义（或至少符合 ref 指定版本的实时内容）。缓存行为导致不可预期的「旧代码执行」是不可接受的。 |
| **触发条件** | 主 workflow 调用子 workflow；修改子 workflow 内容（如添加一行 echo），重新触发主 workflow，观察子 workflow 是否反映修改。 |
| **为什么有风险** | YML 缓存意味着用户修复了子 workflow 的 bug 后，主 workflow 仍在执行有 bug 的旧版本——用户非常困惑为什么「修了但没生效」，严重损害信任。 |
| **出处** | 历史 #85(mindcluster)；`COMPAT-NOTES.md` §5 |

### INTENT-COMPAT-093 — `secrets.ATOMGIT_TOKEN` 的隐式注入与 `env` 上下文 `env.XXX` 取值失败（已证实）

| 维度 | 值 |
|---|---|
| **dimensions** | `[compatibility]` |
| **具体差异点** | 历史 #46：`env` 中定义的参数，通过 `run: echo "${{ env.参数名 }}"` 无法输出（打印为空）。历史 #533(TC-533)：Runner 不注入 Job env 到 Shell（Bash `$VAR` 恒为 UNSET，但 `${{ env.VAR }}` 正常）。这表明 env 变量的两层访问（表达式层 vs shell 环境变量层）在 GitCode 上行为不一致。 |
| **GitHub 侧预期行为** | Job `env:` 中定义的变量同时注入：(a) 表达式层——`${{ env.VAR }}` 可读取，(b) shell 环境——`$VAR` 可作为环境变量直接在 Bash 中使用。 |
| **GitCode 侧疑似行为** | 表达式层 `${{ env.VAR }}` 可能正常，但 shell 环境层的 `$VAR` 不入——违反「变量注入 Runner」的文档声明。 |
| **oracle 对齐方向** | **一致性用例**——`env` 变量应在表达式层和 shell 层均可访问。TC-533 是已确认的 FAIL。 |
| **触发条件** | 在 job `env:` 定义 `MY_VAR: hello`，step 中分别用 `${{ env.MY_VAR }}` 和 `echo $MY_VAR` 输出，对比结果。 |
| **为什么有风险** | 大量 CI 脚本依赖 `$VAR` 直接读取环境变量（如 `$NODE_ENV`、`$DEPLOY_ENV`）；若只有 `${{ env.VAR }}` 可用，需全局替换 Bash 脚本中的变量引用方式——迁移工作量极大。 |
| **出处** | 历史 #46(MindIE-SD)/TC-533；`testing-focus.md` §6 |

---

## 覆盖度自检

| §10 差异类别 | 覆盖 intent | 数量 |
|---|---|---|
| 默认值差异 | COMPAT-001/002/003 | 3 |
| 表达式函数差异 | COMPAT-010/011/012/013/014/015/016 | 7 |
| 触发过滤语义差异 | COMPAT-030/031/032/033/034 | 5 |
| 上下文对象差异 | COMPAT-020/021/022/023 | 4 |
| 不支持能力的降级方式 | COMPAT-040/041/042/043/044 | 5 |
| 内置 action 差异 | COMPAT-050/051/052 | 3 |
| Runner 标签/环境差异 | COMPAT-060/061 | 2 |
| 权限模型/执行模型差异 | COMPAT-070/071/072/073/080 | 5 |
| 已证实缺陷（跨类） | COMPAT-090/091/092/093 | 4 |
| **在计** | | **38**（含跨维度 10 条） |

实际不重复 intent 共 **28 条**（部分 intent 跨类别标注，如 COMPAT-001 同时涉及默认值和易用性）。

## 质量清单自检

- [x] 每条 intent 指明具体差异点（含 GitHub 侧行为 / GitCode 侧疑似行为 / 触发条件 / 风险）。
- [x] 每条 intent 标了 oracle 对齐方向（一致性 or 差异确认）。
- [x] 覆盖了默认值/隐式行为（COMPAT-001/002/003），不只显式字段。
- [x] 28 条 intent 中 12 条引用了实证（历史 #51/#75/#82/#85/#101 等或 TC-xxx），非凭空臆断。
- [x] 所有疑似差异均标「疑似」，待实际测试确认。
- [x] 未写 GitCode 具体语法落地（保持在意图层），那是 case-writer 的活。

## 依哪份输入得出

- `phase01/inputs/gitcode-spec/COMPAT-NOTES.md` — 全量差异线索
- `phase01/inputs/gitcode-spec/syntax-reference/`（context/expressions/trigger-events/variables/workflow-commands）— GitCode 侧规格
- `phase01/inputs/github-reference/reference/`（workflow-syntax/events/contexts/expressions/workflow-commands）— GitHub 侧 oracle
- `phase01/inputs/github-reference/security/`（secure-use/secrets/github-token/script-injections/pull_request_target）— 安全语义对照
- `phase01/inputs/history/issues-encountered.md` — 实证缺陷（101 条）
- `phase01/inputs/existing-cases/cases.md` — 已有测试结果（TC-xxx 的 PASS/FAIL 状态）
- `phase01/testing-focus.md` §4/§5/§10/§11 — 差异高发区与迁移摩擦清单
- `phase01/baseline/risk-register.md` — 优先级依据（RISK-COMPAT-01）
