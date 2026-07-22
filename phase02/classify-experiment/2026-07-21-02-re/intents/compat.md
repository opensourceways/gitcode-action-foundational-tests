# 兼容性 Diff 产出 · GitCode Action ↔ GitHub Actions 差异确认意图库

> 产出 Agent：compat-diff（差异猎手）
> Run：2026-07-21-02
> 角色：系统性对比 GitHub 官方语义（oracle 基准）与 GitCode 能力清单 + 真实 workflow 样本，产出「疑似不一致」test intent。**本次最高价值资产。**
> 来源输入：
>   - `inputs/github-reference/`（13 文件，GitHub 官方语义，fetched 2026-07-20）——差异 oracle 基准
>   - `inputs/workflow-samples/`（cann 7 文件 + op-plugin 1 文件，真实生产 workflow）——佐证「现实常见写法」
>   - `inputs/business-context/README.md`（维度3 竞品兼容性测试大纲，2026-07-21；Runner/迁移改造点仍为模板态）
>   - 本 run `intents/spec.md`（133 能力项 + 36 缺口；重点消费 §2.4 文档矛盾 + 所有标「模糊/未知」且影响 compatibility 项）
>   - `testing-focus.md` §10 兼容性差异高发区、§11 迁移摩擦（扫描骨架）

## 阅读约定

- **ID**：`INTENT-COMPAT-NNN`（rules §1.3）；维度缩写 COMPAT。
- **对齐方向（rules §4，每条必标）**：
  - **一致性用例**：GitCode 未声明差异，预期应与 GitHub 行为一致；GitHub 官方语义为 oracle。若实测不一致 = 缺陷信号。
  - **差异确认用例**：GitCode 文档已声明/疑似有意不同，需确认差异边界 + 文档是否声明清楚；实测结果回写 Parity Matrix 成权威 oracle。
- 每条含角色卡要求字段：`具体差异点 / GitHub 侧预期行为 / GitCode 侧疑似行为 / oracle 对齐方向 / 触发条件 / 为什么有风险 / dimensions`。
- **护栏**：不臆断，标「疑似」；不写 GitCode 具体语法落地；覆盖默认值/隐式行为，不只显式字段。

## 差异分组骨架（按 testing-focus §10）

| 组 | 差异类别 | intent 区间 |
|---|---|---|
| A | 默认值/隐式行为差异 | 001–007 |
| B | 表达式函数/求值语义差异 | 008–016 |
| C | 触发过滤/事件语义差异 | 017–024 |
| D | 上下文对象差异（atomgit.* vs github.*） | 025–030 |
| E | 环境变量/工作流命令差异 | 031–035 |
| F | Runner 标签/环境差异 | 036–040 |
| G | 不支持能力的降级方式 | 041–046 |
| H | 内置 action 差异 | 047–051 |
| I | 安全语义兼容差异 | 052–056 |
| J | 结构/编排模型差异 | 057–061 |

---

## A 组 · 默认值 / 隐式行为差异（testing-focus §10 默认值差异）

> 未声明字段的默认行为是差异最高发区。真实样本大量省略 shell/permissions/fail-fast，迁移时默认值不一致会「静默改变行为」。

```
意图 ID:    INTENT-COMPAT-001
维度标签:   [compatibility, usability]
标题:       默认 shell 差异——未声明 shell 时 GitCode 与 GitHub 的默认解释器及错误处理标志是否一致

具体差异点:   step 未写 `shell:` 时的默认 shell 及其调用参数（尤其 `-e` fail-on-error / pipefail）。
GitHub 侧预期行为: Linux 默认 `bash -e {0}`（bash 不可用回退 `sh -e`）；`bash` 显式指定时为 `bash --noprofile --norc -eo pipefail {0}`。中途命令非零退出即 fail。
GitCode 侧疑似行为: spec C-EXEC-10/C-STRUCT-08 默认 shell「未声明」（G-03），示例用 bash；是否带 `-e`/`pipefail` 未声明。真实样本（cann 全系列）多行 `run:` 均未声明 shell 且依赖中途失败即停。
风险点:     若 GitCode 默认不加 `-e`，GitHub 上「前面命令失败即终止」的脚本迁移后会继续执行后续行，产生静默错误结果（构建假成功）。这是「看起来一样、行为不一样」的典型。
预期系统行为: 未声明 shell 的多行 run，中途命令失败时 step 应失败（与 GitHub `-e` 语义一致）。
Oracle 来源: GitHub行为（workflow-syntax.md:106 shell 表）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub `-e` 语义对齐；实测不一致即缺陷+文档缺口）

验证要点:
  - [正向] 显式 `shell: bash` 的多行脚本，中途失败按 pipefail/-e 终止。
  - [负向] 未声明 shell 时，不应出现「中途命令失败但 step 仍绿、后续命令照跑」的静默放行。
  - [非功能] 默认 shell 行为应可从文档确定，不需实测才知。

触发条件:   一个多行 `run:` step，第一行 `false`（或 `cmd_not_exist`），第二行 `echo reached`，观察 step 结论与是否输出 reached。
优先级线索: 关联 testing-focus §10 默认值差异 + §11 迁移摩擦；风险登记册模板态，建议 P1（静默错误结果影响大）。
来源输入:   github-reference/reference/workflow-syntax.md:106；spec.md C-EXEC-10/C-STRUCT-08/G-03；workflow-samples/cann/*（多行 run 无 shell 声明）
```

```
意图 ID:    INTENT-COMPAT-002
维度标签:   [compatibility, security]
标题:       未声明 permissions 时默认 TOKEN 权限差异——GitCode「仓库设置权限」vs GitHub 明确默认集

具体差异点:   顶层/job 均未写 `permissions:` 时，自动 TOKEN 的默认权限范围。
GitHub 侧预期行为: 默认权限由仓库/组织设置决定，官方给出明确的 permissive/restricted 两套默认表（contents 等按表授予），权限域名为 `contents/pull-requests/issues/...`。
GitCode 侧疑似行为: spec C-SEC-07 称「未声明时用仓库设置权限」，但 G-06 指出「仓库设置默认权限」具体范围未给；权限域为 `repository/pr/issue/project/note/hook`（与 GitHub 完全不同的命名与粒度）。
风险点:     迁移 workflow 若依赖「默认能 clone / 默认能评论 PR」，GitCode 默认权限集不明 + 权限域不对应，可能默认不足（clone 失败）或默认过宽（越权）。命名不对应导致 GitHub `permissions: contents: read` 直接搬运无法识别。
预期系统行为: 未声明 permissions 时有确定、可查的默认权限集；GitHub 式权限域名应被明确处理（报错或映射），不静默忽略。
Oracle 来源: 差异声明（GitCode 权限模型有意不同，需实测 + 文档确立权威默认集，回写 Parity Matrix）
对齐方向:   差异确认（权限域命名与默认集 GitCode 有意不同）

验证要点:
  - [正向] 未声明 permissions 时，checkout（clone）可用性符合文档声明的默认集。
  - [负向] GitHub 式 `permissions: contents: read` 不应被静默忽略而实际授予了写权限。
  - [非功能] 默认权限集应可从文档查明（当前 G-06 缺口）。

触发条件:   分别提交（a）无 permissions（b）GitHub 式 `permissions: {contents: read}`（c）GitCode 式 `permissions: {repository: read}` 的最小 workflow，比对 TOKEN 实际可执行的操作集。
优先级线索: 关联 testing-focus §5 权限 + §11；安全敏感，建议 P1。关联 spec G-06、security 维度。
来源输入:   github-reference/reference/workflow-syntax.md:62-90；spec.md C-SEC-07/G-06
```

```
意图 ID:    INTENT-COMPAT-003
维度标签:   [compatibility, reliability]
标题:       matrix `strategy.fail-fast` 默认值差异——GitCode 未声明默认，GitHub 默认 true

具体差异点:   矩阵作业未写 `fail-fast:` 时，一个实例失败是否取消其余实例。
GitHub 侧预期行为: `strategy.fail-fast` 默认 `true`——任一 matrix 实例失败立即取消其余所有 in-progress/queued 实例。
GitCode 侧疑似行为: spec C-EXEC-18 默认值「未声明」（G-02），文档仅说明取值语义未给默认。
风险点:     若 GitCode 默认 false（或行为相反），迁移的多版本矩阵测试（如 op-plugin 的多 pytorch 版本、cann 多架构构建）在一个版本失败时，GitHub 会快速取消省资源，GitCode 可能全跑完——反之亦然。默认值差异直接改变失败传播与资源消耗。
预期系统行为: 未声明 fail-fast 的矩阵，失败传播行为应与 GitHub 默认 true 一致，或文档明确声明差异。
Oracle 来源: GitHub行为（workflow-syntax.md:170 strategy）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub 默认 true 对齐；若默认不同即缺陷+缺口）

验证要点:
  - [正向] 显式 `fail-fast: true` 时一实例失败取消其余。
  - [负向] 未声明 fail-fast 时，不应出现与 GitHub 默认相反的失败传播（用户按 GitHub 心智预期被违背）。
  - [非功能] 默认值应文档化（当前 G-02 缺口）。

触发条件:   3 实例矩阵，中间实例 `exit 1`，其余 `sleep 60`，观察未声明 fail-fast 时其余实例是否被取消。
优先级线索: 关联 testing-focus §3 matrix + §10；建议 P1（资源与结果双重影响）。关联 spec G-02、reliability 维度。
来源输入:   github-reference/reference/workflow-syntax.md:170；spec.md C-EXEC-18/G-02；workflow-samples/op-plugin（多版本 build 并列）
```

```
意图 ID:    INTENT-COMPAT-004
维度标签:   [compatibility]
标题:       job/step `continue-on-error` 默认值与 outcome/conclusion 语义一致性

具体差异点:   未声明 `continue-on-error` 时的默认值，及其对 `steps.<id>.outcome` vs `conclusion` 的影响是否与 GitHub 一致。
GitHub 侧预期行为: 默认 `false`；`continue-on-error: true` 时 step 失败不致 job 失败，`outcome`=真实结果、`conclusion`=success。
GitCode 侧疑似行为: spec C-EXEC-07/C-EXEC-13 默认值「隐含 false」，由语义推断（G-04），未显式声明；outcome/conclusion 机制 C-EXPR-09 声明存在但边界未详。
风险点:     若 GitCode 默认值或 outcome/conclusion 拆分语义不同，依赖「step 失败但继续、后续用 conclusion 判断」的迁移 workflow 会走错分支。
预期系统行为: 默认 false；continue-on-error=true 时 outcome/conclusion 拆分与 GitHub 一致。
Oracle 来源: GitHub行为（workflow-syntax.md:160,172；contexts.md:98-99）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub 对齐）

验证要点:
  - [正向] step 设 continue-on-error:true 且失败，job 不失败，后续 step 执行。
  - [负向] 未声明时 step 失败不应被静默容忍（默认不应是 true）。
  - [非功能] outcome≠conclusion 的取值可被下游 if 稳定引用。

触发条件:   step A `continue-on-error: true` + `exit 1`，step B 读 `steps.A.outcome`/`steps.A.conclusion` 分别 echo；对照未声明的 step。
优先级线索: 关联 testing-focus §3 + §10；建议 P2。关联 spec G-04。
来源输入:   github-reference/reference/workflow-syntax.md:160,172；spec.md C-EXEC-07/C-EXEC-13/C-EXPR-09/G-04
```

```
意图 ID:    INTENT-COMPAT-005
维度标签:   [compatibility, reliability]
标题:       job `if` 缺省状态与「needs 失败则默认不执行」语义一致性

具体差异点:   下游 job 未写 `if` 时，上游 needs 失败后是否执行；以及 `if: always` 覆盖行为。
GitHub 侧预期行为: 依赖 job 失败则下游默认跳过；需 `if: ${{ always() }}` 或 `!cancelled()` 才继续；`if` 缺省隐含 `success()`。
GitCode 侧疑似行为: spec C-EXEC-02/C-EXEC-03 声明「依赖 job 失败则当前默认不执行（除非 if: always）」，`if` 缺省=success——方向一致，但 GitCode 用无括号 `always`，且真实样本用 `if: ${{ default() }}`（GitHub 无此函数，见 INTENT-COMPAT-009）。
风险点:     语义方向虽一致，但触发「继续执行」的写法不同（`always()` vs `always` vs `default()`），迁移时函数名/括号差异导致条件失效——本应跳过却执行或反之。
预期系统行为: needs 失败传播方向与 GitHub 一致；覆盖写法差异被明确文档化。
Oracle 来源: GitHub行为（workflow-syntax.md:136；expressions.md:153-159）
对齐方向:   一致性（失败传播方向）+ 差异确认（覆盖写法函数名差异，见 009）

验证要点:
  - [正向] 上游 job 失败，未写 if 的下游 job 被跳过。
  - [负向] 上游失败时未写 if 的下游不应仍然执行。
  - [非功能] 「让下游在上游失败时仍跑」的推荐写法应文档明确（GitCode 侧是 always 还是 default）。

触发条件:   job A `exit 1`；job B `needs: [A]` 无 if；job C `needs: [A]` + `if: ${{ always }}`；观察 B/C 是否执行。
优先级线索: 关联 testing-focus §3；建议 P1。关联 spec C-EXEC-02。
来源输入:   github-reference/reference/workflow-syntax.md:136；spec.md C-EXEC-02/C-EXEC-03；workflow-samples/cann/*（if: ${{ default() }}）
```

```
意图 ID:    INTENT-COMPAT-006
维度标签:   [compatibility]
标题:       env 变量三级优先级与 GitHub 覆盖规则一致性（step>job>workflow）

具体差异点:   同名 env 在 workflow/job/step 三级同时定义时的覆盖顺序与生效值。
GitHub 侧预期行为: step env > job env > workflow env，就近覆盖。
GitCode 侧疑似行为: spec C-VAR-02/C-VAR-03 声明同一顺序 step>job>workflow env>vars>系统变量；方向一致，但 GitCode 额外把 `vars` 和 `ATOMGIT_*` 系统变量纳入同一优先级链，GitHub 中 vars 是独立 context 不参与 env 覆盖。
风险点:     GitCode 将 vars 与 env 合并进同一优先级链，可能导致 GitHub 中「env.X 与 vars.X 互不干扰」的假设在迁移后失效——同名时被意外覆盖。
预期系统行为: env 三级覆盖与 GitHub 一致；env 与 vars 的相互作用被明确定义。
Oracle 来源: GitHub行为（workflow-syntax.md:94；variables.md:63-66）
对齐方向:   一致性（env 三级覆盖）+ 差异确认（env/vars 优先级合并是否 GitCode 特有）

验证要点:
  - [正向] 三级同名 env，step 级值生效。
  - [负向] 同名 vars 不应静默覆盖 env（若 GitCode 合并链，需文档声明）。
  - [非功能] 优先级链文档表述清晰。

触发条件:   workflow/job/step 各定义 `env: FOO`，step 读 `$FOO`；再加同名 `vars.FOO` 观察是否介入。
优先级线索: 关联 testing-focus §10 上下文；建议 P2。关联 spec C-VAR-02/C-VAR-03。
来源输入:   github-reference/reference/workflow-syntax.md:94；variables.md:63-66；spec.md C-VAR-02/C-VAR-03
```

```
意图 ID:    INTENT-COMPAT-007
维度标签:   [compatibility, reliability]
标题:       `post` / stage `fail_fast` 等 GitCode 特有编排默认值在迁移场景的隐式行为

具体差异点:   GitCode 顶层 `post`（默认 run_always:true）与 `stages.fail_fast`（默认未声明）是 GitHub 无对应的编排层；其默认值决定迁移后新增的隐式行为。
GitHub 侧预期行为: GitHub 无 stages/post 概念；清理靠 action 的 `post:` 钩子，失败传播靠 job needs + fail-fast(matrix)。
GitCode 侧疑似行为: spec C-STRUCT-06 `stages.fail_fast` 默认未声明（G-01）；C-STRUCT-07 `post` 默认 run_always:true。真实样本（ops-nn）每个 stage 显式写 `fail-fast: true` + `pre: - type: auto`。
风险点:     从 GitHub 迁移的扁平 jobs（无 stages）落到 GitCode 时，若被隐式包裹进单 stage，其 fail_fast 默认值不明会改变失败传播；post 默认恒执行可能让 GitHub 中「仅成功才清理」的逻辑变成总是清理。
预期系统行为: 无 stages 的迁移 workflow 的失败传播、post 的默认执行条件均有明确文档化默认。
Oracle 来源: 差异声明（GitCode 特有编排层，需确立默认值并声明迁移影响）
对齐方向:   差异确认（GitCode 特有能力，验证默认值边界 + 是否文档化）

验证要点:
  - [正向] 显式 stages + fail_fast:true 按声明串行终止。
  - [负向] 无 stages 的扁平 jobs 不应因隐式 stage 默认值产生未预期的失败传播。
  - [非功能] post 默认执行条件（run_always）在文档中清晰，迁移指引说明其与 GitHub action post 的差异。

触发条件:   （a）无 stages 的多 job workflow 观察失败传播；（b）含 post 的 workflow 令主流程失败，观察 post 是否执行。
优先级线索: 关联 testing-focus §3 + §11；建议 P1。关联 spec C-STRUCT-06/C-STRUCT-07/G-01。
来源输入:   spec.md C-STRUCT-06/C-STRUCT-07/G-01；workflow-samples/cann/ops-nn_action.yml（stage fail-fast/pre）
```

---

## B 组 · 表达式函数 / 求值语义差异（testing-focus §10 表达式函数差异）

> 同名函数边界行为、类型转换、空值处理是隐性差异高发区；状态函数括号差异是迁移直接断点。

```
意图 ID:    INTENT-COMPAT-008
维度标签:   [compatibility, usability]
标题:       状态函数括号差异——GitHub `success()/failure()/always()/cancelled()` vs GitCode 无括号 + failed

具体差异点:   状态检查函数的语法形态（带括号否）与失败函数命名（`failure` vs `failed`）。
GitHub 侧预期行为: `if: ${{ success() }}` / `failure()` / `always()` / `cancelled()`——**必须带括号**，失败函数名 `failure()`。
GitCode 侧疑似行为: spec C-EXPR-03/C-EXEC-12 声明无括号 `success`/`failed`/`cancelled`/`always`，且失败函数名为 **`failed`** 非 failure。
风险点:     迁移直接断点——GitHub workflow 的 `if: ${{ failure() }}` 搬到 GitCode：`failure` 名不识别 + 带括号语法可能非法。若 GitCode 把未知标识符求值为空/false，则「失败时执行」的 step 恒不执行（错过失败处理）；若求值报错则迁移即失败。这是最高频迁移摩擦之一。
预期系统行为: GitHub 式 `success()`/`failure()`（带括号）应有确定处理——明确报错指出应改无括号 + `failed`，不应静默恒真/恒假。
Oracle 来源: 差异声明（GitCode 语法有意不同，实测确立处理方式回写 Parity Matrix）
对齐方向:   差异确认（语法有意不同）

验证要点:
  - [正向] GitCode `if: ${{ failed }}` 在前置失败时为真、成功时为假。
  - [负向] GitHub 式 `if: ${{ failure() }}` 或 `success()` 不应被静默当作恒真/恒假而错误放行或跳过关键 step。
  - [非功能] 报错应明确指向「状态函数无括号 + 用 failed」，降低迁移摩擦。

触发条件:   前置 step 失败后，分别用 `if: ${{ failed }}`（GitCode）、`if: ${{ failure() }}`（GitHub 式）、`if: ${{ failure }}` 三种写法的清理 step，观察各自是否执行。
优先级线索: 关联 testing-focus §1/§10/§11；建议 P0（迁移直接断点 + 静默错过失败处理）。关联 spec C-EXPR-03、INTENT-COMP-008。
来源输入:   github-reference/reference/expressions.md:137-177；spec.md C-EXPR-03/C-EXEC-12
```

```
意图 ID:    INTENT-COMPAT-009
维度标签:   [compatibility, usability]
标题:       GitCode 特有 `default()` 函数——GitHub 无对应，反向迁移与语义确认

具体差异点:   真实样本大量使用 `if: "${{ default() }}"`（cann 全系列 job 级），GitHub 表达式函数集无 `default()`。
GitHub 侧预期行为: GitHub 无 `default()` 函数；`if: ${{ default() }}` 会被判为未知函数 → 表达式错误 / workflow 校验失败。
GitCode 侧疑似行为: 真实生产样本（arm_compile/x86_compile/codecheck/staticcheck/llt/ops-nn）几乎每个 job 都写 `if: "${{ default() }}"`，疑为 GitCode「默认选择/默认执行」语义，但 spec.md 能力清单**未列出 `default()` 函数**（C-EXPR-04 函数集缺此项）——文档缺口。
风险点:     双向风险：(a) 反向迁移（GitCode→GitHub）此写法直接失效；(b) 正向迁移用户看不懂 `default()`，且 spec 未文档化该函数，属能力清单遗漏。需坐实其语义（是否等价「无条件执行/默认选中」）。
预期系统行为: `default()` 有明确定义的语义并被文档化；其与 `success`（if 缺省）的区别清晰。
Oracle 来源: 差异声明（GitCode 特有函数，spec 未收录，需实测 + 文档确立）
对齐方向:   差异确认（GitCode 特有，无 GitHub 对应）

验证要点:
  - [正向] `if: ${{ default() }}` 的 job 在正常/前置失败下的执行行为被明确记录。
  - [负向] 不应存在「文档未定义但生产广泛使用」的黑盒函数——需回填能力清单。
  - [非功能] 语义应可从文档查明（当前为 spec 缺口，建议登记新 G）。

触发条件:   job 用 `if: ${{ default() }}`，分别在上游成功/失败/取消三态下观察是否执行；与 `if: ${{ success }}` 对比。
优先级线索: 关联 testing-focus §10 + §11；建议 P1（生产高频 + 文档盲区）。关联 spec C-EXPR-04（函数集缺口）。
来源输入:   workflow-samples/cann/arm_compile_action.yml:68 等全系列；spec.md C-EXPR-04
```

```
意图 ID:    INTENT-COMPAT-010
维度标签:   [compatibility]
标题:       缺失表达式函数——GitHub `join()/fromJSON()/toJSON()/hashFiles()/case()` 在 GitCode 的支持状况

具体差异点:   GitCode spec 列出的函数集（contains/startsWith/endsWith/format/substring/replace/hashFiles/toJson）与 GitHub 函数集的差集。
GitHub 侧预期行为: GitHub 提供 contains/startsWith/endsWith/format/join/toJSON/fromJSON/hashFiles/case 等；`fromJSON` 用于 matrix 动态展开与字符串转数字，极常用。
GitCode 侧疑似行为: spec C-EXPR-04 列出函数中**无 `join`、无 `fromJSON`、无 `case`**，却多出 GitHub 没有的 `substring`/`replace`。`toJson`（小写 s）命名大小写也与 GitHub `toJSON` 不同。
风险点:     (a) 迁移中依赖 `fromJSON(needs.x.outputs.matrix)` 的动态矩阵 workflow 直接失效；(b) `join(labels.*.name)` 失效；(c) `toJSON` vs `toJson` 大小写差异导致函数名不识别。这些是常见 GitHub 高级用法的断点。
预期系统行为: 缺失函数应明确报错「不支持」而非静默返回空；大小写差异应文档化或大小写不敏感。
Oracle 来源: GitHub行为（expressions.md:113-135）
对齐方向:   差异确认（函数集有意/事实不同，需确认降级方式）

验证要点:
  - [正向] GitCode 列出的 substring/replace 按声明工作。
  - [负向] `fromJSON`/`join`/`case` 若不支持，不应静默求值为空导致后续逻辑走错（应明确报错）。
  - [非功能] `toJson` 与 GitHub `toJSON` 的大小写兼容性明确。

触发条件:   分别用 `${{ fromJSON('["a","b"]')[0] }}`、`${{ join(...) }}`、`${{ toJSON(atomgit) }}` 表达式，观察是求值成功、报错还是静默空。
优先级线索: 关联 testing-focus §10；建议 P1（动态矩阵是常见高级用法）。关联 spec C-EXPR-04/G-33。
来源输入:   github-reference/reference/expressions.md:113-135；spec.md C-EXPR-04/G-33
```

```
意图 ID:    INTENT-COMPAT-011
维度标签:   [compatibility]
标题:       字符串比较大小写敏感性差异——GitHub 忽略大小写 vs GitCode startsWith/endsWith 区分大小写

具体差异点:   `==` 字符串比较与 contains/startsWith/endsWith 的大小写处理。
GitHub 侧预期行为: GitHub **比较字符串时忽略大小写**（`==` 与 contains/startsWith/endsWith 均 case-insensitive）。
GitCode 侧疑似行为: spec C-EXPR-04 明确「startsWith/endsWith **区分大小写**；contains 支持子串」——与 GitHub 相反。`==` 大小写敏感性 GitCode 未声明。
风险点:     迁移的条件判断（如 `startsWith(atomgit.ref, 'refs/tags/V')` 或分支名比较）在 GitHub 忽略大小写会命中，GitCode 区分大小写会漏判——「该触发的没触发/该匹配的没匹配」的静默逻辑错误。
预期系统行为: 大小写敏感性应文档明确；与 GitHub 不一致处需在迁移指引标注。
Oracle 来源: GitHub行为（expressions.md:53,68,85-101）
对齐方向:   差异确认（GitCode startsWith/endsWith 有意区分大小写）

验证要点:
  - [正向] GitCode `startsWith('Hello','He')` 为真、`startsWith('Hello','he')` 为假（区分）。
  - [负向] 迁移的大小写不敏感比较不应静默改变判定结果而无提示。
  - [非功能] `==` 的大小写行为文档化。

触发条件:   `if: ${{ startsWith('MAIN', 'main') }}` 与 `if: ${{ 'MAIN' == 'main' }}` 两条，比对 GitCode 与 GitHub 求值。
优先级线索: 关联 testing-focus §10；建议 P2。关联 spec C-EXPR-04/G-33。
来源输入:   github-reference/reference/expressions.md:53,68,85-101；spec.md C-EXPR-04
```

```
意图 ID:    INTENT-COMPAT-012
维度标签:   [compatibility]
标题:       表达式类型强转 / loose equality 差异——空串、null、布尔在比较中的强转规则

具体差异点:   `==`/关系运算的隐式类型转换（null→0、''→0、bool→0/1、非法字符串→NaN）与 falsy 判定。
GitHub 侧预期行为: 明确的 loose equality：Null→0、''→0、true→1、Array/Object→NaN，NaN 参与任何关系比较恒 false；falsy 集 `false/0/-0/""/''/null`。
GitCode 侧疑似行为: spec C-EXPR-01 列字面量类型，但 G-33 指出「空值处理、类型转换、边界行为未详述」——GitCode 是否采用同样的强转表未声明。
风险点:     依赖隐式转换的条件（如 `if: ${{ inputs.count > 0 }}` 而 inputs 恒为 string，或 `if: ${{ env.FLAG }}` 判空）在两平台强转规则不同则分支走向不同。尤其 GitCode inputs 仅 string（C-VAR-07），字符串 'false' 在条件中是否判真直接影响 INTENT-COMP-005 场景。
预期系统行为: 强转/falsy 规则与 GitHub 一致或明确文档化差异。
Oracle 来源: GitHub行为（expressions.md:57-69）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub 强转表对齐；不一致即缺陷+缺口）

验证要点:
  - [正向] `${{ '' == 0 }}`、`${{ null == 0 }}`、`${{ 'false' }}` 作条件的求值与 GitHub 一致。
  - [负向] 字符串 'false' 不应在两平台产生相反的真值判定（迁移语义误判）。
  - [非功能] 强转规则文档化（当前 G-33 缺口）。

触发条件:   一组表达式 `${{ '' == 0 }}` / `${{ '0' == 0 }}` / `if: ${{ 'false' }}` / `if: ${{ '' }}`，比对两平台。
优先级线索: 关联 testing-focus §1/§10；建议 P2。关联 spec G-33、INTENT-COMP-005。
来源输入:   github-reference/reference/expressions.md:57-69；spec.md C-EXPR-01/C-VAR-07/G-33
```

```
意图 ID:    INTENT-COMPAT-013
维度标签:   [compatibility]
标题:       `hashFiles()` 行为一致性——glob 语义、无匹配返回值、workspace 相对基准

具体差异点:   `hashFiles(path)` 的无匹配返回、多路径逗号分隔、相对目录基准、大小写。
GitHub 侧预期行为: 相对 `GITHUB_WORKSPACE`；多 path 逗号分隔；无匹配返回**空字符串**；每文件 SHA-256 再聚合；Windows 上大小写不敏感。
GitCode 侧疑似行为: spec C-EXPR-04/C-ART-07 列出 hashFiles 支持多参数生成 key，但相对基准（ATOMGIT_WORKSPACE？）、无匹配返回值未声明。cache 场景（C-ART-05）强依赖此函数生成稳定 key。
风险点:     缓存 key 生成是 hashFiles 主用途——若无匹配返回值不同（GitHub 空串 vs GitCode 报错/其他），或相对基准不同，迁移的 cache workflow 会 key 漂移导致缓存永不命中（性能退化，非报错，隐性）。
预期系统行为: hashFiles 相对 workspace、无匹配返回空串、多路径语义与 GitHub 一致。
Oracle 来源: GitHub行为（expressions.md:127-131）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub 对齐）

验证要点:
  - [正向] `hashFiles('**/package-lock.json')` 命中文件时生成稳定非空 hash。
  - [负向] 无匹配文件时不应产生不稳定 key（应返回空串，行为可预期）。
  - [非功能] 相对基准目录文档明确。

触发条件:   同一组文件在两平台计算 hashFiles；另构造无匹配 glob 观察返回值。
优先级线索: 关联 testing-focus §8 cache + §10；建议 P2。关联 spec C-EXPR-04/C-ART-05/C-ART-07。
来源输入:   github-reference/reference/expressions.md:127-131；spec.md C-EXPR-04/C-ART-05/C-ART-07
```

```
意图 ID:    INTENT-COMPAT-014
维度标签:   [compatibility]
标题:       引用不存在的上下文属性——GitHub 空串 vs GitCode 处理一致性

具体差异点:   访问上下文中不存在的属性（如 `atomgit.event.xxx` 在当前事件无该字段）时的求值。
GitHub 侧预期行为: 引用不存在的 context 属性求值为**空字符串**（不报错）。
GitCode 侧疑似行为: spec C-EXPR-06 声明「引用不存在属性求值为空字符串」——方向一致。但深层链式访问（`atomgit.event.pull_request.number` 在 push 事件下）是否同样安全返回空、还是报错未系统验证。真实样本大量跨事件复用同一 env（如 ops-nn 的 `MERGE_ID: ${{atomgit.event.pull_request.number}}` 在 pr_comment 与 push 双触发下）。
风险点:     双触发 workflow（pull_request_comment + pr_comment，或迁移中 push+PR 混用）里，同一表达式在不同事件下 payload 字段存在性不同；若 GitCode 对缺失深层属性报错而非返回空，则跨事件复用的 workflow 在某些事件下崩溃。
预期系统行为: 缺失属性（含深层链）求值为空串，与 GitHub 一致，不报错。
Oracle 来源: GitHub行为（contexts.md；events.md payload）
对齐方向:   一致性（GitCode 已声明同向，验证深层链边界）

验证要点:
  - [正向] push 事件下 `${{ atomgit.event.pull_request.number }}` 求值为空串不报错。
  - [负向] 深层缺失属性不应导致表达式解析失败使整个 workflow 无法运行。
  - [非功能] 行为跨事件一致。

触发条件:   同一 workflow 由 push 与 pull_request 双触发，含引用 PR-only 深层属性的 env，观察 push 下是否正常运行。
优先级线索: 关联 testing-focus §10 上下文；建议 P2。关联 spec C-EXPR-06。
来源输入:   github-reference/reference/contexts.md:35-59；spec.md C-EXPR-06；workflow-samples/cann/ops-nn_action.yml:15
```

```
意图 ID:    INTENT-COMPAT-015
维度标签:   [compatibility, usability]
标题:       `${{ }}` 表达式求值时机——先求值再进 shell 的注入面与转义一致性

具体差异点:   `run:` 中 `${{ }}` 是否在 shell 执行前被替换（模板注入语义）。
GitHub 侧预期行为: `${{ }}` 在 shell 脚本生成**之前**求值并字面替换，故不可信输入直接拼进 `run:` 会导致命令注入（script injection）。
GitCode 侧疑似行为: 真实样本大量把 `${{ }}` 直接拼入 run（如 codecheck `--pr_id ${MERGE_ID}` 混用 shell 变量与 `${{ }}`）；spec 未专门声明求值时机（script-injections.md 对接点指出需验证）。
风险点:     若 GitCode 求值时机与 GitHub 一致（先替换），则同样存在注入面，迁移的不安全写法风险平移；若不一致（如运行时才展开），则 `${{ atomgit.event.pull_request.title }}` 等的行为与转义与 GitHub 不同，可能破坏依赖字面替换的脚本。二者都需坐实。
预期系统行为: 求值时机明确文档化；与 GitHub 一致（先求值），并在文档提示注入风险。
Oracle 来源: GitHub行为（script-injections.md:30）
对齐方向:   一致性（求值时机应与 GitHub 一致，验证 + 文档化）

验证要点:
  - [正向] `run: echo "${{ inputs.x }}"` 中 inputs.x 被字面替换。
  - [负向] 含 shell 元字符的不可信输入拼入 run，其求值/转义行为与 GitHub 一致（不应产生比 GitHub 更宽松的注入面且无文档警示）。
  - [非功能] 求值时机文档化，配套注入缓解建议（交 security 维度深挖）。

触发条件:   `run` 中拼入含 `"; echo INJECTED` 的表达式值，观察是否被当命令执行（与 GitHub 对照）。注：仅意图层，具体 payload 归 security agent。
优先级线索: 关联 testing-focus §6 注入 + §10；建议 P1。与 security 维度交叉。关联 spec C-ACT-01。
来源输入:   github-reference/security/script-injections.md:30；spec.md C-ACT-01；workflow-samples/cann/codecheck_action.yml:108
```

```
意图 ID:    INTENT-COMPAT-016
维度标签:   [compatibility]
标题:       `steps.<id>` 引用 —— GitCode `identifier:` 与 `id:` 的等价性与 outputs 引用一致性

具体差异点:   真实样本用 `identifier: process_checkout` 标识 step，而 GitHub/GitCode 文档均用 `id:`；下游却用 `steps.<name>.outputs` 引用。
GitHub 侧预期行为: step 唯一标识字段是 `id:`；下游用 `steps.<id>.outputs.<x>` 引用；无 `identifier` 字段。
GitCode 侧疑似行为: spec C-EXEC-09 声明用 `id:`，但真实生产样本（cann 全系列）一律用 `identifier:`，且下游用 `steps.<identifier>.outputs.path`（如 `steps.process_checkout.outputs.path`）引用成功。疑似 GitCode 支持 `identifier` 作为 `id` 的别名/替代，但文档未声明。
风险点:     (a) 文档-实现不一致：文档说 `id`，生产用 `identifier`，迁移用户困惑该用哪个；(b) 若迁移的 GitHub workflow 用 `id:`，需确认 GitCode 是否同样支持（否则所有 steps.<id> 引用失效）；(c) 二者混用时 outputs 索引键以哪个为准未知。
预期系统行为: `id` 与 `identifier` 的关系明确（等价/别名/择一）；GitHub 式 `id:` 在 GitCode 可用。
Oracle 来源: 差异声明（GitCode 出现文档外字段 identifier，需实测 + 文档澄清）
对齐方向:   差异确认（identifier 为疑似 GitCode 特有/别名，spec 未收录）

验证要点:
  - [正向] 用 `id:` 定义 step，`steps.<id>.outputs` 可引用（GitHub 兼容）。
  - [负向] `identifier` 与 `id` 混用/仅用其一时，outputs 引用不应静默取空导致下游拿到空值。
  - [非功能] 文档澄清二者关系，消除迁移困惑。

触发条件:   step 分别用 `id: s1` 和 `identifier: s2` 设 output，下游 `steps.s1.outputs.x` / `steps.s2.outputs.x` 各引用，观察哪个生效。
优先级线索: 关联 testing-focus §10 + §11；建议 P1（生产全量使用 + 文档盲区）。关联 spec C-EXEC-09。
来源输入:   spec.md C-EXEC-09；workflow-samples/cann/arm_compile_action.yml:24,42 等全系列
```

---

## C 组 · 触发过滤 / 事件语义差异（testing-focus §10 触发过滤语义差异）

> 真实样本暴露差异最密集区：事件名、types 取值、PR 评论触发的两种写法并存、merge ref 格式。事件语义差异导致「CI 不触发」是最痛迁移摩擦。

```
意图 ID:    INTENT-COMPAT-017
维度标签:   [compatibility, usability]
标题:       pull_request types 取值差异——GitHub `opened/synchronize/reopened` vs GitCode `open/update/reopen`

具体差异点:   `pull_request`/`pull_request_target` 的 activity types 命名与取值。
GitHub 侧预期行为: types 取值 `opened`/`synchronize`/`reopened`/`closed`/...；默认 `[opened, synchronize, reopened]`。判断合并用 `closed` + `github.event.pull_request.merged`。
GitCode 侧疑似行为: spec C-TRIG-02 取值 `[merge, open, reopen, update]`，默认 `[open, reopen, update]`——命名（open vs opened、update vs synchronize、reopen vs reopened）与取值双重差异，且 GitCode 有独有的 `merge` type。
风险点:     **最高频迁移断点**：GitHub workflow 写 `types: [opened, synchronize]` 搬到 GitCode，若 GitCode 不识别 `opened`/`synchronize`，则 PR 更新时 **CI 完全不触发**（静默不运行，用户以为集成通过）。business-context 维度3 明确列此为已知摩擦。
预期系统行为: GitHub 式 types 值应被明确处理——报错提示「应改用 open/update」，而非静默接受却永不匹配。
Oracle 来源: 差异声明（GitCode types 命名有意不同，权威值回写 Parity Matrix）
对齐方向:   差异确认（types 命名/取值有意不同）

验证要点:
  - [正向] GitCode `types: [open, update]` 在 PR 创建/更新时正确触发。
  - [负向] GitHub 式 `types: [opened, synchronize]` 不应被静默接受却在 PR 更新时不触发（应报错或有告警）。
  - [非功能] 报错/文档应指明命名映射（opened→open, synchronize→update）。

触发条件:   两个 workflow 分别用 GitHub 式与 GitCode 式 types，对同一 PR 执行 open→push update→reopen，比对各自触发次数。
优先级线索: 关联 testing-focus §2/§10/§11；建议 P0（CI 静默不触发，最痛点）。关联 spec C-TRIG-02、business-context 维度3。
来源输入:   github-reference/reference/events.md:9-22,99-106；spec.md C-TRIG-02；business-context/README.md（已知摩擦）
```

```
意图 ID:    INTENT-COMPAT-018
维度标签:   [compatibility, usability]
标题:       PR 评论触发两种写法并存——`pull_request_comment`+`comments` vs `pr_comment`+`keyword`

具体差异点:   触发 PR 评论的事件名与过滤字段，真实样本中**同一文件内两种写法并存**。
GitHub 侧预期行为: GitHub 无独立 PR 评论事件，用 `issue_comment` + `github.event.issue.pull_request` 判断；无正则内容过滤字段。
GitCode 侧疑似行为: 真实样本出现两套：op-plugin 与 ops-nn 用 `pull_request_comment: {types, branches, comments: ['^(?:\/)?compile*']}`；sub_pipline_support 与 ops-nn（同文件）又用 `pr_comment: {types, keyword: '^(?:\/)?compile*'}`。spec C-TRIG-05 只记 `pull_request_comment` + `comments`，**未记 `pr_comment`/`keyword`**。同义功能两个事件名 + 两个过滤字段名（comments 数组 vs keyword 标量）。
风险点:     (a) spec 遗漏 `pr_comment`/`keyword`，属能力清单盲区；(b) 两者是别名、择一、还是同时触发导致**重复运行**未知——ops-nn 同文件同时写两个可能导致每条评论触发两次；(c) `comments`（数组正则）与 `keyword`（标量正则）语义/引擎是否一致未知。
预期系统行为: 明确 `pull_request_comment` 与 `pr_comment` 关系；同文件并存时的触发次数确定（不应意外重复）。
Oracle 来源: 差异声明（GitCode 特有事件，spec 部分遗漏，需实测 + 文档澄清）
对齐方向:   差异确认（GitCode 特有事件，无 GitHub 对应）

验证要点:
  - [正向] 单独用 `pull_request_comment` 或 `pr_comment` 时，匹配评论正确触发一次。
  - [负向] 同文件并存二者时不应对同一评论**重复触发两次**（除非文档明确声明）。
  - [非功能] `comments` 与 `keyword` 的正则引擎/语法一致或文档说明差异；`pr_comment` 应回填能力清单。

触发条件:   （a）仅 pull_request_comment；（b）仅 pr_comment；（c）二者并存（模拟 ops-nn）三个 workflow，发同一条 `/compile` 评论，比对触发次数。
优先级线索: 关联 testing-focus §2/§10；建议 P1（重复触发浪费资源 + 文档盲区）。关联 spec C-TRIG-05/G-18。
来源输入:   workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:12-15；cann/ops-nn_action.yml:4-10；cann/sub_pipline_support.yaml；spec.md C-TRIG-05
```

```
意图 ID:    INTENT-COMPAT-019
维度标签:   [compatibility, security]
标题:       PR 评论正则过滤引擎差异——`'^(?:\/)?compile*'` 的正则方言与匹配语义

具体差异点:   `comments`/`keyword` 过滤所用正则引擎、锚定、大小写、部分匹配 vs 全匹配。
GitHub 侧预期行为: GitHub 无此内建正则评论过滤（需在 step 内自行匹配），无对应 oracle——纯 GitCode 特性。
GitCode 侧疑似行为: 真实样本正则 `'^(?:\/)?compile*'`（含非捕获组 `(?:)`、`compile*` 实际是 `compil` + `e*`，疑写法瑕疵）。spec C-TRIG-05 标「正则引擎/语法未声明」（模糊）+ G-18 标注注入面未声明。
风险点:     (a) `compile*` 星号作用于 `e` 而非「compile 开头」，用户以为匹配 compile 开头实则匹配 `compil`+任意个 e——语义陷阱；(b) 正则引擎（PCRE/RE2/Go regexp）不同则 `(?:)` 等语法支持不同，跨样本迁移可能解析失败；(c) 恶意评论构造匹配绕过属安全面。
预期系统行为: 正则引擎/方言文档化；锚定与部分匹配语义明确；异常正则有明确报错。
Oracle 来源: GitCode规格（C-TRIG-05，需实测确立，无 GitHub oracle）
对齐方向:   差异确认（GitCode 特有能力，坐实语义边界）

验证要点:
  - [正向] `'^(?:\/)?compile'` 对 `/compile` 与 `compile` 评论均匹配触发。
  - [负向] 非预期评论（如仅 `comp`）不应误触发；非法正则不应静默匹配全部。
  - [非功能] 引擎/语法文档化（当前模糊 + G-18）。

触发条件:   构造评论 `/compile`、`compile`、`compileee`、`comp`、`xcompile`，观察匹配触发情况，反推引擎与锚定语义。
优先级线索: 关联 testing-focus §2/§6/§10；建议 P2。与 security 维度交叉（G-18 注入面）。关联 spec C-TRIG-05/G-18。
来源输入:   workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:15；cann/ops-nn_action.yml:7；spec.md C-TRIG-05/G-18
```

```
意图 ID:    INTENT-COMPAT-020
维度标签:   [compatibility]
标题:       paths/branches diff 阈值差异——GitHub 1000 commits/3000 files vs GitCode 前 300 文件

具体差异点:   paths 过滤在大变更下的截断阈值与「超阈值必跑/不跑」规则。
GitHub 侧预期行为: push >1000 commits **总是运行**；diff >3000 文件且匹配文件不在前 3000 则**不运行**；PR 用 three-dot diff，push 用 two-dot diff。
GitCode 侧疑似行为: spec C-TRIG-10/C-QUOTA-05 声明「匹配前 **300** 个变更文件，超出不参与判断」——阈值（300 vs 3000）差一个数量级，且未声明「大 commit 数是否必跑」及 diff 比较方式（two/three-dot）。
风险点:     大 PR（>300 文件）迁移后触发行为差异巨大：GitHub 前 3000 内匹配即触发，GitCode 仅看前 300，第 301+ 文件命中 paths 会**静默不触发**。大型仓库（如 cann/pytorch 级）此差异导致「改了受监控目录却没跑 CI」。
预期系统行为: 截断阈值文档明确；超阈值行为（必跑/不跑）与截断可观测。
Oracle 来源: 差异声明（阈值有意不同，确认边界）
对齐方向:   差异确认（阈值有意不同）

验证要点:
  - [正向] ≤300 文件变更命中 paths 正常触发。
  - [负向] 仅第 301+ 文件命中 paths（前 300 不命中）时不触发——确认截断存在。
  - [非功能] diff 比较方式（two/three-dot）与大 commit 数行为文档化。

触发条件:   单次 push 变更 350 文件，命中 paths 的文件分别置于第 1–300 与第 301+ 位，比对触发；对照 GitHub 3000 阈值。
优先级线索: 关联 testing-focus §2/§10/§12；建议 P1（大仓库静默漏触发）。关联 spec C-TRIG-10/C-QUOTA-05/INTENT-COMP-003。
来源输入:   github-reference/reference/workflow-syntax.md:40-44,212；spec.md C-TRIG-10/C-QUOTA-05
```

```
意图 ID:    INTENT-COMPAT-021
维度标签:   [compatibility]
标题:       PR checkout ref 格式差异——GitCode `refs/merge-requests/<id>/merge` vs GitHub `refs/pull/<n>/merge`

具体差异点:   检出 PR 合并提交所用的 ref 命名，及 `atomgit.ref`/`GITHUB_REF` 在 PR 下的取值。
GitHub 侧预期行为: PR 事件 `GITHUB_REF` = `refs/pull/<PR_NUMBER>/merge`；checkout PR 用此 ref。
GitCode 侧疑似行为: 真实样本用 `ref: refs/merge-requests/${{ env.pr_id }}/merge`（op-plugin）——「merge-requests」而非「pull」，术语沿用 GitLab MR。同时其他样本用 `atomgit.event.pull_request.merge_commit_sha || atomgit.sha`（cann 系列）。spec C-EXPR-05 列 atomgit.ref 但未给 PR 下具体格式。
风险点:     迁移 GitHub workflow 里硬编码 `refs/pull/${{ github.event.number }}/merge` 到 GitCode 会检出失败（ref 不存在）。术语差异（pull vs merge-request）+ 两套 checkout 惯例（ref 字符串 vs merge_commit_sha）导致迁移必须改写 checkout。
预期系统行为: PR ref 格式文档明确；GitHub 式 `refs/pull/...` 的兼容性明确（是否也接受）。
Oracle 来源: 差异声明（ref 命名有意不同，确认格式）
对齐方向:   差异确认（ref 命名/术语有意不同）

验证要点:
  - [正向] GitCode `refs/merge-requests/<id>/merge` 正确检出合并提交。
  - [负向] GitHub 式 `refs/pull/<n>/merge` 不应静默检出错误提交（应明确失败或兼容）。
  - [非功能] `atomgit.ref`/`atomgit.ref_name` 在 PR 下取值文档化，供迁移映射。

触发条件:   PR 场景下分别用 `refs/merge-requests/<id>/merge`、`refs/pull/<n>/merge`、`merge_commit_sha` 三种 checkout ref，比对检出的 commit。
优先级线索: 关联 testing-focus §10/§11；建议 P1（迁移必改写点）。关联 spec C-EXPR-05/C-ACT-09。
来源输入:   github-reference/reference/events.md:16;variables.md:34；workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:91；cann/arm_compile_action.yml:27
```

```
意图 ID:    INTENT-COMPAT-022
维度标签:   [compatibility]
标题:       schedule 时区差异——GitHub 支持 `timezone` 字段 vs GitCode 仅 UTC

具体差异点:   `schedule.cron` 是否支持 `timezone`，以及默认时区。
GitHub 侧预期行为: 默认 UTC，但**支持 `timezone`（IANA）字段**指定时区。
GitCode 侧疑似行为: spec C-TRIG-08 声明「UTC 时区」，未提 timezone 字段——疑不支持。
风险点:     迁移含 `timezone: "America/New_York"` 的定时任务到 GitCode，若 `timezone` 被静默忽略，则任务在错误时间（UTC）运行——如「工作日早 9 点扫描」变成午夜跑，业务时序错乱且无报错。
预期系统行为: `timezone` 字段应被明确处理（报错或声明仅 UTC），不静默忽略。
Oracle 来源: 差异声明（GitCode 仅 UTC，确认降级方式）
对齐方向:   差异确认（GitCode 有意仅 UTC）

验证要点:
  - [正向] GitCode UTC cron 按 UTC 触发。
  - [负向] 带 `timezone` 字段的 cron 不应被静默忽略而在非预期时间运行（应报错/告警）。
  - [非功能] 「仅 UTC，请自行换算」文档明确。

触发条件:   提交带 `timezone` 的 schedule workflow，观察是否报错、忽略字段、还是按声明时区运行。
优先级线索: 关联 testing-focus §2/§10；建议 P2。关联 spec C-TRIG-08。
来源输入:   github-reference/reference/events.md:48-58;workflow-syntax.md:46-53；spec.md C-TRIG-08
```

```
意图 ID:    INTENT-COMPAT-023
维度标签:   [compatibility]
标题:       branches/paths 过滤通配语义差异——`**`/`!`/`?`/`+`/`[]` glob 方言一致性

具体差异点:   过滤模式的通配符集与匹配语义（`*` 不跨 `/`、`**` 跨、`!` 取反、字符类）。
GitHub 侧预期行为: 完整 filter cheat sheet：`*`（不含/）、`**`（含/）、`?`、`+`、`[]`、`!`；`branches`/`branches-ignore` 不可同用。
GitCode 侧疑似行为: spec C-TRIG-09/C-TRIG-10 声明支持 `**` 与取反 `!`，「二者不可同时使用」与 GitHub 一致；但 `?`/`+`/`[]` 字符类是否支持未声明。真实样本用 `branches: [ '*' ]`（op-plugin）。
风险点:     迁移含 `branches: ['release/**', '!release/*-rc']` 或字符类 `v[0-9]` 的过滤，若 GitCode glob 方言子集不同，则分支匹配结果不同——「该跑的分支没跑/不该跑的跑了」。`'*'` 是否匹配所有分支（含带 `/` 的）也需确认（GitHub `*` 不跨 `/`）。
预期系统行为: 通配方言与 GitHub 一致或明确文档化支持子集。
Oracle 来源: GitHub行为（workflow-syntax.md:190-200 filter cheat sheet）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub glob 对齐；子集不同即缺陷+缺口）

验证要点:
  - [正向] `**` 跨层匹配、`!` 取反按 GitHub 语义工作。
  - [负向] `branches: ['*']` 是否匹配 `feature/x`（含/）应与 GitHub 一致（GitHub `*` 不匹配含/分支），不应静默扩大/缩小匹配。
  - [非功能] 支持的通配符集文档化。

触发条件:   分支 `main`/`feature/x`/`release/1.0`，用 `['*']`、`['**']`、`['v[0-9]*']`、`['release/**','!release/*-rc']` 分别过滤，比对触发。
优先级线索: 关联 testing-focus §2/§10；建议 P2。关联 spec C-TRIG-09/C-TRIG-10。
来源输入:   github-reference/reference/workflow-syntax.md:190-200；spec.md C-TRIG-09/C-TRIG-10；workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:14
```

```
意图 ID:    INTENT-COMPAT-024
维度标签:   [compatibility]
标题:       workflow_dispatch/workflow_call inputs 类型差异——GitHub 5 类型 vs GitCode 仅 string

具体差异点:   手动/复用工作流 inputs 支持的类型集。
GitHub 侧预期行为: `workflow_dispatch` inputs 支持 `boolean/choice/number/environment/string`；`workflow_call` 支持 `boolean/number/string`。
GitCode 侧疑似行为: spec C-TRIG-06/C-TRIG-07/C-VAR-07 反复声明 inputs **仅 string**。真实样本 op-plugin 顶层 `inputs:` 全部 `type: string`；cann workflow_call inputs 亦全 string。
风险点:     迁移含 `type: boolean`/`type: choice`/`type: number` 的 dispatch inputs 到 GitCode：若静默降级为 string，则 `if: ${{ inputs.flag }}` 中布尔 'false' 判真（字符串非空即真）——**条件逻辑反转**，最危险的静默语义误判（见 INTENT-COMP-005/COMPAT-012）。choice 的下拉枚举也丢失。
预期系统行为: 非 string 类型应报错提示「仅支持 string，请用表达式转换」，不静默降级致语义误判。
Oracle 来源: 差异声明（GitCode 仅 string，确认降级方式）
对齐方向:   差异确认（GitCode 有意仅 string）

验证要点:
  - [正向] `type: string` inputs 及其 default/required 正常。
  - [负向] `type: boolean` 值 'false' 不应被当字符串在 `if` 中判真（静默语义反转）。
  - [非功能] 非法 type 报错指引改用 string + 表达式转换。

触发条件:   dispatch inputs 定义 `flag: {type: boolean, default: false}`，job `if: ${{ inputs.flag }}`，观察是否执行（string 'false' 非空→可能判真）。
优先级线索: 关联 testing-focus §1/§10/§11；建议 P1（静默条件反转）。关联 spec C-TRIG-06/C-VAR-07/INTENT-COMP-005。
来源输入:   github-reference/reference/events.md:59-73;workflow-syntax.md:55-60；spec.md C-TRIG-06/C-TRIG-07/C-VAR-07；workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:16-36
```

---

## D 组 · 上下文对象差异（testing-focus §10 上下文对象差异 · atomgit.* vs github.*）

> 前缀替换是迁移最机械但最易漏的改造点；属性齐全度与值格式差异是隐性断点。

```
意图 ID:    INTENT-COMPAT-025
维度标签:   [compatibility, usability]
标题:       上下文前缀差异——`github.*` → `atomgit.*` 全局替换的完备性与属性缺失

具体差异点:   核心上下文对象前缀（github vs atomgit）及各属性是否一一对应。
GitHub 侧预期行为: `github.*` 提供 actor/sha/ref/ref_name/ref_type/event/repository/run_id/... 全属性。
GitCode 侧疑似行为: spec C-EXPR-05 `atomgit.*` 列出 event_name/sha/ref/ref_name/ref_type/event/workspace/token/repository/run_id/run_number/run_attempt/head_ref/base_ref/server_url/api_url 等。business-context 维度3 明确迁移改造点=「所有 `${{ github.* }}` 全局替换为 `${{ atomgit.* }}`」。
风险点:     (a) 机械替换遗漏（如漏改一处 `github.sha`）→ GitCode 下 `github` 上下文不存在 → 求值为空或报错；(b) 部分属性 GitCode 无对应（如 `github.triggering_actor`/`github.workflow_ref`/`github.repositoryUrl` 是否有 atomgit 对应未声明）→ 替换后取空值。
预期系统行为: atomgit.* 属性集覆盖迁移所需；无对应属性有文档说明；`github.*`（未替换残留）有确定处理。
Oracle 来源: 差异声明（前缀有意不同，属性映射需确认）
对齐方向:   差异确认（前缀有意不同）

验证要点:
  - [正向] `atomgit.sha`/`atomgit.ref`/`atomgit.repository` 等核心属性取值正确。
  - [负向] 残留的 `github.sha` 不应静默返回空使脚本拿到空 SHA（应可诊断）。
  - [非功能] github→atomgit 属性映射表文档化，标注无对应项。

触发条件:   同一 workflow 分别引用全套 atomgit.* 属性与个别 github.* 残留，比对取值与报错。
优先级线索: 关联 testing-focus §10/§11；建议 P1（迁移核心改造点）。关联 spec C-EXPR-05、business-context 维度3。
来源输入:   github-reference/reference/contexts.md:24-59；spec.md C-EXPR-05；business-context/README.md（改造点）
```

```
意图 ID:    INTENT-COMPAT-026
维度标签:   [compatibility, completeness]
标题:       上下文属性缺失——`atomgit.actor`/`triggering_actor`/`workflow_ref` 等是否存在

具体差异点:   GitHub 常用属性在 atomgit 上下文中的存在性。
GitHub 侧预期行为: `github.actor`/`github.actor_id`/`github.triggering_actor`/`github.workflow`/`github.workflow_ref`/`github.workflow_sha`/`github.repository_owner` 均存在。
GitCode 侧疑似行为: spec G-28 指出 `atomgit.actor`/`atomgit.actor_id` 被 example/日志页引用但 **context.md 属性表未列**（自相矛盾）；`triggering_actor`/`workflow_ref`/`workflow_sha`/`repository_owner` 在 C-EXPR-05 列表中**缺失**。G-29 指出上下文正文称 12 种但表仅 11 行。
风险点:     迁移依赖 `github.actor`（如权限判断 `if: github.actor == 'dependabot'`）或 `github.workflow_ref`（badge/审计）的 workflow，若 atomgit 无对应属性 → 求值空 → 权限判断失效（安全）或功能缺失。actor 缺失尤其危险：基于发起人的门禁会全部失效。
预期系统行为: 迁移关键属性（actor 等）应存在且文档列全；缺失项明确标注替代方案。
Oracle 来源: GitHub行为（contexts.md:24-59）
对齐方向:   一致性（核心属性应可用；缺失即兼容缺口）

验证要点:
  - [正向] `atomgit.actor` 若存在则返回发起人，可用于门禁。
  - [负向] 基于 actor 的安全门禁不应因 actor 取空而静默放行所有人。
  - [非功能] 属性表补全（消解 G-28/G-29 矛盾）。

触发条件:   echo `${{ atomgit.actor }}`/`${{ atomgit.triggering_actor }}`/`${{ atomgit.workflow_ref }}`，观察各返回值/空。
优先级线索: 关联 testing-focus §10；建议 P1（actor 缺失=安全门禁失效）。关联 spec C-EXPR-05/G-28/G-29。
来源输入:   github-reference/reference/contexts.md:32-57；spec.md C-EXPR-05/G-28/G-29
```

```
意图 ID:    INTENT-COMPAT-027
维度标签:   [compatibility]
标题:       `runner` 上下文差异——os/arch 取值格式与 name/tool_cache/temp 一致性

具体差异点:   `runner.os`/`runner.arch` 取值格式与可用属性。
GitHub 侧预期行为: `runner.os`∈`Linux/Windows/macOS`；`runner.arch`∈`X86/X64/ARM/ARM64`；含 name/temp/tool_cache/debug。
GitCode 侧疑似行为: spec C-EXPR-10 `runner.os`∈`Linux/Windows/macOS`、`arch`∈`X64/ARM/ARM64`（**无 X86**）；contexts.md 差异提示指 GitCode 目前仅 Linux（ubuntu/euler）。
风险点:     (a) 迁移中 `if: runner.os == 'Windows'` 分支在 GitCode（仅 Linux）恒不命中，Windows-only 步骤静默跳过；(b) arch 取值缺 X86，依赖 `runner.arch == 'X86'` 的逻辑失效；(c) 大小写（X64 vs x64）——真实样本 runs-on 用小写 `x64`，而 runner.arch 声明大写 `X64`，比较大小写敏感性存疑。
预期系统行为: runner.os/arch 取值格式与 GitHub 一致；不支持平台的分支行为可预期。
Oracle 来源: GitHub行为（contexts.md:61-70）
对齐方向:   一致性（取值格式应对齐；平台子集差异需文档化）

验证要点:
  - [正向] `runner.os`=='Linux'、`runner.arch`=='X64' 在 ubuntu x64 runner 上成立。
  - [负向] `runner.arch == 'X86'` 不应因取值缺失而导致意外行为；`x64` 与 `X64` 大小写不一致不应破坏比较。
  - [非功能] 平台/arch 取值集文档化。

触发条件:   echo runner.os/arch/name/temp/tool_cache；`if: ${{ runner.arch == 'X64' }}` 与 `== 'x64'` 各测。
优先级线索: 关联 testing-focus §4/§10；建议 P2。关联 spec C-EXPR-10。
来源输入:   github-reference/reference/contexts.md:61-70；spec.md C-EXPR-10；workflow-samples/cann/*（runs-on x64 小写）
```

```
意图 ID:    INTENT-COMPAT-028
维度标签:   [compatibility]
标题:       `strategy` 上下文差异——`job-index`/`job-total`/`max-parallel` 是否可用

具体差异点:   matrix 作业内 `strategy.*` 上下文属性支持度。
GitHub 侧预期行为: `strategy.fail-fast`/`strategy.job-index`（0 基）/`strategy.job-total`/`strategy.max-parallel` 均可读。
GitCode 侧疑似行为: spec C-EXPR-07 上下文列表含 strategy，但未列具体属性；contexts.md 差异提示明确「GitHub `strategy.job-total`/`job-index` 需验证 GitCode 是否支持」。
风险点:     迁移中用 `strategy.job-index` 做分片（如把 matrix 索引映射到测试分片，类似 op-plugin 的 TEST_RANK/TSET_WORD_SIZE 手动分片）的 workflow，若 GitCode 无此属性则分片逻辑失效，所有实例跑同一分片或报错。
预期系统行为: strategy 子属性可用或明确不支持并给替代。
Oracle 来源: GitHub行为（contexts.md:101-108）
对齐方向:   一致性（应可用；缺失即兼容缺口）

验证要点:
  - [正向] matrix 作业内 `strategy.job-index`/`job-total` 返回正确索引/总数。
  - [负向] 不支持时不应静默返回空导致分片错乱（应报错）。
  - [非功能] strategy 属性支持度文档化。

触发条件:   3 实例矩阵，每实例 echo `${{ strategy.job-index }}`/`${{ strategy.job-total }}`，验证 0/1/2 与 3。
优先级线索: 关联 testing-focus §3/§10；建议 P2。关联 spec C-EXPR-07。
来源输入:   github-reference/reference/contexts.md:101-108；spec.md C-EXPR-07；workflow-samples/op-plugin（手动分片 TEST_RANK）
```

```
意图 ID:    INTENT-COMPAT-029
维度标签:   [compatibility]
标题:       `atomgit.token` vs `secrets.ATOMGIT_TOKEN` vs `github.token` 获取方式差异

具体差异点:   自动令牌的多种获取路径与等价性。
GitHub 侧预期行为: 通过 `${{ secrets.GITHUB_TOKEN }}` 或 `${{ github.token }}` 获取，二者等价。
GitCode 侧疑似行为: spec C-EXPR-05/C-VAR-04 显示可用 `atomgit.token` 或 `secrets.ATOMGIT_TOKEN`；真实样本却多用**自定义** `secrets.GIT_TOKEN`（cann 全系列 checkout token）而非内置 token——疑内置 token 权限不足需自备 PAT。
风险点:     (a) 迁移的 `secrets.GITHUB_TOKEN` 需改为 `secrets.ATOMGIT_TOKEN` 或 `atomgit.token`，遗漏则取空；(b) 真实样本普遍自备 `GIT_TOKEN` 暗示内置 token 在 checkout/push 场景可能不够用（权限或跨库），这与 GitHub「GITHUB_TOKEN 开箱可 clone」的假设冲突，是隐性迁移摩擦。
预期系统行为: 内置 token 获取路径等价且文档明确；内置 token 能力边界（能否 clone 本库/私有库）清晰。
Oracle 来源: 差异声明（token 命名有意不同 + 能力边界需确认）
对齐方向:   差异确认（命名不同 + 能力边界坐实）

验证要点:
  - [正向] `atomgit.token` 与 `secrets.ATOMGIT_TOKEN` 取到同一有效令牌，可 clone 本库。
  - [负向] 迁移残留 `secrets.GITHUB_TOKEN` 不应静默取空导致 checkout 无认证失败且信息不清。
  - [非功能] 内置 token 与自备 PAT 的适用场景文档化（为何样本普遍自备）。

触发条件:   分别用 atomgit.token / secrets.ATOMGIT_TOKEN / secrets.GITHUB_TOKEN(残留) 做 checkout，比对成功性。
优先级线索: 关联 testing-focus §5/§10/§11；建议 P1。与 security 交叉。关联 spec C-SEC-06/C-EXPR-05。
来源输入:   github-reference/security/github-token.md:24；spec.md C-SEC-06/C-EXPR-05；workflow-samples/cann/*（secrets.GIT_TOKEN）
```

```
意图 ID:    INTENT-COMPAT-030
维度标签:   [compatibility]
标题:       上下文可用性矩阵差异——各上下文在 workflow/job/step/if 级的可用位置一致性

具体差异点:   `secrets`/`job`/`steps`/`matrix`/`runner` 等在不同层级（workflow/job/step/if）的可用性。
GitHub 侧预期行为: 明确可用性矩阵：`job`/`steps`/`runner`/`strategy`/`matrix` 在 workflow 级**不可用**；`secrets`/`env`/`vars`/`inputs` workflow 级可用；`steps` 仅 after 可用。
GitCode 侧疑似行为: spec C-EXPR-08 声明有可用性矩阵且「job/runner/steps/matrix/strategy 在 workflow 级不可用」——方向与 GitHub 一致，但完整对照未逐格验证。真实样本在 job `if` 用 `jobs.<id>.outputs`（op-plugin build_skip），需确认 `jobs` 上下文（caller）可用位置。
风险点:     若某上下文可用位置与 GitHub 不同（如 GitCode 允许 workflow 级用 matrix，或禁止 job if 用 needs），迁移的表达式在错误位置引用会解析失败或取空——报错质量与位置差异影响迁移调试。
预期系统行为: 可用性矩阵与 GitHub 一致或明确文档差异。
Oracle 来源: GitHub行为（contexts.md:110-124）
对齐方向:   一致性（GitCode 已声明同向，逐格验证）

验证要点:
  - [正向] job 级 `if` 引用 `needs.<job>.outputs`/`jobs.<job>.outputs` 生效（op-plugin 场景）。
  - [负向] 在 workflow 级引用 `matrix.*`/`runner.*` 不应被静默接受取空（应报错定位）。
  - [非功能] 可用性矩阵逐格文档化。

触发条件:   逐个上下文在 workflow/job/step/if 四个位置引用，比对可用性与 GitHub 矩阵。
优先级线索: 关联 testing-focus §10；建议 P2。关联 spec C-EXPR-07/C-EXPR-08。
来源输入:   github-reference/reference/contexts.md:110-124；spec.md C-EXPR-08；workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:190
```

---

## E 组 · 环境变量 / 工作流命令差异（testing-focus §10 · GITHUB_* vs ATOMGIT_*）

```
意图 ID:    INTENT-COMPAT-031
维度标签:   [compatibility, usability]
标题:       环境文件变量前缀差异——`GITHUB_ENV/OUTPUT/PATH/STEP_SUMMARY` → `ATOMGIT_*`

具体差异点:   工作流命令文件协议的环境变量名前缀。
GitHub 侧预期行为: `echo "k=v" >> "$GITHUB_OUTPUT"`；`$GITHUB_ENV`/`$GITHUB_PATH`/`$GITHUB_STEP_SUMMARY`/`$GITHUB_STATE`；`>>` 追加。
GitCode 侧疑似行为: spec C-ACT-02 用 `ATOMGIT_OUTPUT`/`ATOMGIT_ENV`/`ATOMGIT_PATH`/`ATOMGIT_STEP_SUMMARY`；真实样本 op-plugin `echo "build_skip=${BUILD_SKIP}" >> "$ATOMGIT_OUTPUT"`。**无 ATOMGIT_STATE**（GitHub 有 GITHUB_STATE 供 pre/post 共享）。
风险点:     (a) 迁移中 `>> $GITHUB_OUTPUT` 未改前缀 → 写入名为 GITHUB_OUTPUT 的普通文件（该 shell 变量为空则写到空路径/报错），output 设置**静默失败**，下游取空；(b) 缺 ATOMGIT_STATE → 依赖 GITHUB_STATE 的 pre/post 状态传递的 action 迁移后失效。
预期系统行为: ATOMGIT_* 文件协议与 GitHub 等价（除前缀）；残留 GITHUB_* 有确定处理；STATE 缺失有说明。
Oracle 来源: 差异声明（前缀有意不同）
对齐方向:   差异确认（前缀有意不同）

验证要点:
  - [正向] `>> $ATOMGIT_OUTPUT` 设置的 output 被下游 `steps.<id>.outputs` 读到。
  - [负向] 残留 `>> $GITHUB_OUTPUT` 不应静默成功却让下游取空（应可诊断）。
  - [非功能] STATE 等缺失变量文档标注替代方案。

触发条件:   step 分别用 `>> $ATOMGIT_OUTPUT` 与 `>> $GITHUB_OUTPUT` 设 output，下游读取比对。
优先级线索: 关联 testing-focus §10/§11；建议 P1（output 静默失败）。关联 spec C-ACT-02/C-VAR-04。
来源输入:   github-reference/reference/workflow-commands.md:94-136；spec.md C-ACT-02；workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:179
```

```
意图 ID:    INTENT-COMPAT-032
维度标签:   [compatibility]
标题:       系统环境变量映射差异——`GITHUB_*` 全集 → `ATOMGIT_*` 及缺失变量

具体差异点:   默认注入的系统环境变量前缀与全集覆盖。
GitHub 侧预期行为: `GITHUB_SHA/REF/REF_NAME/REF_TYPE/EVENT_NAME/EVENT_PATH/WORKSPACE/REPOSITORY/RUN_ID/RUN_NUMBER/RUN_ATTEMPT/...` + `RUNNER_*`；含 `GITHUB_GRAPHQL_URL`/`RUNNER_DEBUG`/`GITHUB_REPOSITORY_OWNER`/`GITHUB_TRIGGERING_ACTOR`。
GitCode 侧疑似行为: spec C-VAR-04 列 `ATOMGIT_*` 全集；但 `GITHUB_REPOSITORY_OWNER`/`GITHUB_TRIGGERING_ACTOR`/`GITHUB_REPOSITORY_ID` 是否有 ATOMGIT 对应未确认。真实样本用 `$ATOMGIT_WORKSPACE`（op-plugin build.sh）、`$ATOMGIT_OUTPUT`。
风险点:     迁移脚本里 `$GITHUB_WORKSPACE`/`$GITHUB_SHA` 硬编码未改 → GitCode 下这些变量未定义（空）→ `cd $GITHUB_WORKSPACE` 变成 `cd `（切到 HOME）→ 构建在错误目录执行。系统变量是脚本层最易残留的硬编码。
预期系统行为: ATOMGIT_* 覆盖迁移所需系统变量；残留 GITHUB_* 未定义可诊断；缺失变量文档标注。
Oracle 来源: GitHub行为（variables.md:15-60）
对齐方向:   差异确认（前缀有意不同）+ 一致性（全集覆盖度）

验证要点:
  - [正向] `$ATOMGIT_WORKSPACE`/`$ATOMGIT_SHA` 等在 run 中有正确值。
  - [负向] 残留 `$GITHUB_WORKSPACE` 为空时脚本行为可诊断（不应静默 cd 到错误目录且无提示）。
  - [非功能] 变量映射表 + 缺失项文档化（关联 G-23 键位不一致、G-31 GitHub 残留措辞）。

触发条件:   run 中 echo 全套 ATOMGIT_* 与残留 GITHUB_* 变量，比对定义性。
优先级线索: 关联 testing-focus §10/§11；建议 P1。关联 spec C-VAR-04/G-23/G-31。
来源输入:   github-reference/reference/variables.md:15-60；spec.md C-VAR-04/G-23/G-31；workflow-samples/cann/ops-nn_action.yml:144
```

```
意图 ID:    INTENT-COMPAT-033
维度标签:   [compatibility]
标题:       RUNNER_OS/ARCH 双命名混乱——`RUNNER_*` vs `ATOMGIT_RUNNER_*` 及 GitHub 对齐

具体差异点:   runner 系统变量前缀（GitCode 文档内自相矛盾）。
GitHub 侧预期行为: `RUNNER_OS`/`RUNNER_ARCH`/`RUNNER_NAME`/`RUNNER_TEMP`/`RUNNER_TOOL_CACHE`/`RUNNER_ENVIRONMENT`（值 github-hosted）。
GitCode 侧疑似行为: spec C-VAR-05/C-VAR-08/G-23 指出**同一含义两套命名并存**：`RUNNER_OS/ARCH` vs `ATOMGIT_RUNNER_OS/ARCH`，两文档不一致；`RUNNER_ENVIRONMENT` 值为 `gitcode-hosted`。
风险点:     (a) 迁移脚本 `$RUNNER_OS` 在 GitCode 若实际是 `$ATOMGIT_RUNNER_OS` → 取空；(b) GitCode 内部双命名并存，用户不知该用哪个，写错即空值；(c) `RUNNER_ENVIRONMENT` 值 github-hosted vs gitcode-hosted 差异使 `if: runner.environment == 'github-hosted'` 判断失效。
预期系统行为: runner 变量命名唯一确定（消解 G-23）；与 GitHub 对齐或明确映射。
Oracle 来源: 差异声明（GitCode 文档矛盾，需实测定权威）
对齐方向:   差异确认（GitCode 内部矛盾，坐实实际命名）

验证要点:
  - [正向] 实际生效的 runner 变量名（RUNNER_OS 或 ATOMGIT_RUNNER_OS）返回正确值。
  - [负向] 另一套命名不应静默取空使脚本拿不到 os/arch。
  - [非功能] 消解双命名矛盾（G-23），文档统一。

触发条件:   run 中同时 echo `$RUNNER_OS`/`$ATOMGIT_RUNNER_OS`/`$RUNNER_ARCH`/`$ATOMGIT_RUNNER_ARCH`/`$RUNNER_ENVIRONMENT`，看哪套有值。
优先级线索: 关联 testing-focus §10；建议 P2。关联 spec C-VAR-05/C-VAR-08/G-23。
来源输入:   github-reference/reference/variables.md:54-60；spec.md C-VAR-05/C-VAR-08/G-23
```

```
意图 ID:    INTENT-COMPAT-034
维度标签:   [compatibility]
标题:       工作流日志命令差异——`::group::`/`::error::`/`::warning::`/`::notice::`/`::add-mask::` 支持度

具体差异点:   `::command::` 系列日志/注解命令的支持集与语法。
GitHub 侧预期行为: `::group::`/`::endgroup::`/`::error file=,line=::`/`::warning::`/`::notice::`/`::debug::`/`::add-mask::`/`::stop-commands::`；注解落到 PR/commit。
GitCode 侧疑似行为: spec C-SEC-11 确认 `::add-mask::` 支持且未废弃；但 `::group::`/`::error::`/`::notice::`/`::stop-commands::` 是否支持在 spec 中**未系统列出**（C-ACT-03 只提废弃的 set-output/set-env/add-path）。
风险点:     迁移 workflow 大量用 `::group::` 折叠日志、`::error::` 生成注解，若 GitCode 不支持则这些命令作为普通文本打印（日志噪音）或注解不生成——可观测性退化，PR 上看不到错误注解（易用性+兼容性）。
预期系统行为: 支持的日志命令集与 GitHub 一致或明确文档化子集；不支持命令的降级（原样打印 vs 报错）明确。
Oracle 来源: GitHub行为（workflow-commands.md:46-84）
对齐方向:   一致性（GitCode 未声明差异，应尽量对齐；子集不同即缺口）

验证要点:
  - [正向] `::add-mask::` 遮掩生效（spec 已确认）。
  - [负向] `::group::`/`::error::` 若不支持，不应静默当普通文本污染日志且丢失注解（应文档说明）。
  - [非功能] 支持命令集文档化。

触发条件:   run 中输出 `::group::x`/`::error::msg`/`::notice::msg`，观察是否折叠/生成注解或原样打印。
优先级线索: 关联 testing-focus §9/§10；建议 P2。关联 spec C-SEC-11/C-ACT-03。
来源输入:   github-reference/reference/workflow-commands.md:46-84；spec.md C-SEC-11/C-ACT-03
```

```
意图 ID:    INTENT-COMPAT-035
维度标签:   [compatibility]
标题:       多行值 delimiter 协议与「不可覆盖默认变量」约束一致性

具体差异点:   写 ATOMGIT_ENV/OUTPUT 多行值的 heredoc delimiter 语法，及能否覆盖 ATOMGIT_*/RUNNER_* 默认变量。
GitHub 侧预期行为: 多行用 `{name}<<{delimiter}\n{value}\n{delimiter}`；**不能覆盖** `GITHUB_*`/`RUNNER_*` 默认变量；写 env 的当前 step 不可见新值，后续 step 可见。
GitCode 侧疑似行为: spec C-ACT-05 声明多行用「随机 delimiter」，C-ACT-02 声明「当前 step 写入后续 step 生效」——方向一致。但「不可覆盖默认变量」约束 GitCode 未声明；delimiter 语法细节未详。
风险点:     (a) 迁移的多行 output（如 JSON/日志块）若 delimiter 语法不同则解析错误；(b) 若 GitCode 允许覆盖 ATOMGIT_SHA 等默认变量（GitHub 禁止），恶意/误写可污染系统变量影响下游——安全兼容双面。
预期系统行为: 多行 delimiter 与 GitHub 一致；默认变量不可覆盖约束存在或明确声明。
Oracle 来源: GitHub行为（workflow-commands.md:100-108）
对齐方向:   一致性（GitCode 未声明差异，应对齐）

验证要点:
  - [正向] heredoc 多行值正确写入 output/env 并被下游完整读取。
  - [负向] 尝试 `echo "ATOMGIT_SHA=x" >> $ATOMGIT_ENV` 不应覆盖系统 SHA（应被拒绝，与 GitHub 一致）。
  - [非功能] delimiter 语法文档化。

触发条件:   写多行 output（含换行的 JSON）验证读取；再尝试覆盖 ATOMGIT_SHA 观察是否生效。
优先级线索: 关联 testing-focus §3/§10；建议 P2。关联 spec C-ACT-02/C-ACT-05。
来源输入:   github-reference/reference/workflow-commands.md:100-108；spec.md C-ACT-02/C-ACT-05
```

---

## F 组 · Runner 标签 / 环境差异（testing-focus §10 runner 标签/环境差异）

> `runs-on` 取值是迁移最显眼改造点；真实样本 runs-on 写法极其多样（数组/花括号/default/self-hosted 映射），是差异富矿。

```
意图 ID:    INTENT-COMPAT-036
维度标签:   [compatibility, usability]
标题:       runs-on 取值差异——GitHub 单标签 `ubuntu-latest` vs GitCode 三段式 `{os,arch,flavor}`

具体差异点:   `runs-on` 值的结构（单标签 vs 三段式标签集）。
GitHub 侧预期行为: `runs-on: ubuntu-latest`（单标签）或 `[self-hosted, linux, x64]`；标签是 runner 标签集子集匹配。
GitCode 侧疑似行为: spec C-RUN-01/C-RUN-04 三段式 `{os-version, arch, flavor}`，如 `[ubuntu-latest, x64, small]`；`default` 快捷=`[ubuntu-latest,x64,small]`。真实样本极多样：`[dedicate-hosted, x64, 2xlarge]`、`["codearts-hosted","ubuntu-latest","x64","small"]`、`- default`、`['self-hosted','arch=arm','smoke=204']`。
风险点:     迁移 `runs-on: ubuntu-latest`（GitHub 单标签）到 GitCode：若 GitCode 要求三段式，则单标签可能匹配失败（排不到 runner）或被特殊解释。反之真实样本的 `dedicate-hosted`/`codearts-hosted`/`arch=arm` 键值式标签是 GitCode 特有，GitHub 无。**这是每个迁移 workflow 必改点**。
预期系统行为: runs-on 取值规则明确；GitHub 式单标签 `ubuntu-latest` 的兼容处理清晰（可用/需补全/报错）。
Oracle 来源: 差异声明（runs-on 结构有意不同）
对齐方向:   差异确认（结构有意不同）

验证要点:
  - [正向] GitCode `[ubuntu-latest, x64, small]` 与 `default` 正确分配 runner。
  - [负向] GitHub 式裸 `runs-on: ubuntu-latest` 不应静默挂起排不到 runner 而无明确报错。
  - [非功能] 单标签→三段式的迁移映射文档化。

触发条件:   分别提交 `runs-on: ubuntu-latest`（GitHub 式）、`[ubuntu-latest,x64,small]`、`default` 的 job，比对调度结果与报错时限。
优先级线索: 关联 testing-focus §4/§10/§11；建议 P0（每 workflow 必改 + 排不到 runner 静默挂起）。关联 spec C-RUN-01/C-RUN-02/C-RUN-04、business-context 维度3。
来源输入:   github-reference/reference/workflow-syntax.md:133-134,209；spec.md C-RUN-01/C-RUN-02/C-RUN-04；workflow-samples/cann/*、op-plugin
```

```
意图 ID:    INTENT-COMPAT-037
维度标签:   [compatibility, usability]
标题:       runs-on 多种写法等价性——数组 `[..]` vs 花括号 `{..}` vs `default` vs 键值 `arch=arm`

具体差异点:   同一 runner 选择的多种语法形态是否等价。
GitHub 侧预期行为: 仅数组或单标签；无花括号式、无 `key=value` 标签式。
GitCode 侧疑似行为: spec C-RUN-04/G-27 指出「数组式 `[..]` 与花括号式 `{..}` 并存，是否等价未声明」。真实样本另见 `- default`（列表项式）、`['self-hosted','arch=arm','smoke=204']`（键值标签混入数组）、注释掉的 `[ self-hosted, arch=x64, os=euler ]`。
风险点:     (a) 花括号 `{ubuntu-24,x64,small}` 在 YAML 中是 flow-mapping（键无值），与数组语义可能被解析器区别对待——写法瑕疵导致解析歧义；(b) `arch=arm` 键值标签 vs 位置标签两种范式混用，匹配规则不明；(c) 迁移者不知选哪种写法。这是 G-27 文档矛盾的直接落地验证。
预期系统行为: 各写法等价性明确；非法/歧义写法有报错。
Oracle 来源: 差异声明（GitCode 内部多写法并存，需实测定等价性）
对齐方向:   差异确认（GitCode 特有多写法，坐实等价性）

验证要点:
  - [正向] 数组式与 default 均能调度到预期 runner。
  - [负向] 花括号式若与数组式语义不同，不应静默调度到非预期 runner。
  - [非功能] 推荐写法 + 各写法等价性文档化（消解 G-27）。

触发条件:   同一 runner 目标用 `[ubuntu-latest,x64,small]`、`{ubuntu-latest,x64,small}`、`default`、键值式分别提交，比对调度结果。
优先级线索: 关联 testing-focus §4/§10；建议 P2。关联 spec C-RUN-04/G-27。
来源输入:   spec.md C-RUN-04/G-27；workflow-samples/cann/ops-nn_action.yml:40,73-74,371；op-plugin:9
```

```
意图 ID:    INTENT-COMPAT-038
维度标签:   [compatibility]
标题:       预装工具链版本差异——GitHub runner image 与 GitCode ubuntu-latest 预装软件差集

具体差异点:   托管 runner 预装的语言/构建/CLI 工具及版本。
GitHub 侧预期行为: ubuntu-latest 预装明确清单（Node/Python/Go/Java 多版本 + docker/jq/gh 等），版本随 image 版本文档化。
GitCode 侧疑似行为: spec C-RUN-11/G-30 指出预装工具链两文档版本列表**不一致**（Node 18/20 vs 18/20/22 等）+「随镜像更新变化」；G-32 os 取值各文档不一。
风险点:     迁移依赖特定预装版本（如 `node --version` 期望 20、或直接用 `gh` CLI）的 workflow，若 GitCode 预装版本/工具不同则脚本失败（命令 not found 或版本不符）。GitHub 的 `ubuntu-latest` 与 GitCode 的 `ubuntu-latest` 同名但内容不同——「看起来一样、装的不一样」。
预期系统行为: 预装清单文档准确一致；缺失工具需 setup-* 显式安装的指引明确。
Oracle 来源: GitHub行为（GitHub runner-images 清单）+ 差异声明
对齐方向:   差异确认（image 内容有意/事实不同）

验证要点:
  - [正向] 文档声明预装的工具在 runner 上可用且版本匹配。
  - [负向] 迁移脚本依赖的工具（如 gh/特定 node 版本）缺失时应能明确诊断（command not found）而非诡异行为。
  - [非功能] 预装清单文档一致（消解 G-30）。

触发条件:   run 中 `node -v`/`python3 -V`/`go version`/`java -version`/`which gh docker jq yq`，比对文档声明与 GitHub。
优先级线索: 关联 testing-focus §4/§10；建议 P2。关联 spec C-RUN-11/G-30/G-32。
来源输入:   github-reference/reference/contexts.md:131（Linux only 提示）；spec.md C-RUN-11/G-30/G-32
```

```
意图 ID:    INTENT-COMPAT-039
维度标签:   [compatibility]
标题:       无 Windows/macOS runner——GitHub 三平台 vs GitCode 仅 Linux 的迁移降级

具体差异点:   支持的 runner 操作系统平台集。
GitHub 侧预期行为: `windows-latest`/`macos-latest`/`ubuntu-latest` 三平台；跨平台 matrix 常见。
GitCode 侧疑似行为: spec C-RUN-01 + contexts.md 差异提示：GitCode 目前**仅 Linux**（ubuntu/euler），无 Windows/macOS。
风险点:     迁移含 `runs-on: windows-latest` 或 `os: [ubuntu, windows, macos]` 矩阵的 workflow：Windows/macOS 作业在 GitCode 无 runner 可分配。若静默挂起 → 整个 workflow 卡住；若报错 → 需删除这些作业。跨平台项目迁移直接受阻。且 pwsh/cmd shell（Windows）在纯 Linux 下不可用。
预期系统行为: 请求 windows/macos runner 应明确报错「不支持该平台」而非无限排队；shell: pwsh/cmd 的处理明确。
Oracle 来源: 差异声明（GitCode 仅 Linux）
对齐方向:   差异确认（平台集有意受限）

验证要点:
  - [正向] Linux runner 作业正常。
  - [负向] `runs-on: windows-latest` 不应静默挂起无反馈（应明确报错平台不支持）。
  - [非功能] 不支持平台清单 + `shell: pwsh/cmd` 行为文档化。

触发条件:   提交 `runs-on: windows-latest` 及 `shell: pwsh` 的 job，观察报错/挂起/时限。
优先级线索: 关联 testing-focus §4/§10/§11；建议 P1（跨平台项目迁移受阻）。关联 spec C-RUN-01。
来源输入:   github-reference/reference/workflow-syntax.md:106,134;contexts.md:131；spec.md C-RUN-01
```

```
意图 ID:    INTENT-COMPAT-040
维度标签:   [compatibility, reliability]
标题:       资源规格标签差异——GitCode flavor（slim~2xlarge）与「large+ 需申请」vs GitHub 标准/大型 runner

具体差异点:   runner 资源规格的表达方式与可用性。
GitHub 侧预期行为: 标准 runner 固定规格（2-core 等），大型 runner 通过自定义标签；无 slim/small/large flavor 概念。
GitCode 侧疑似行为: spec C-RUN-03 六档 flavor（slim/small/medium/large/xlarge/2xlarge），**托管默认仅 slim/small/medium，large+ 需申请客服**。真实样本大量用 `2xlarge`/`xlarge`/`large`（cann 生产）——依赖已申请的大规格。
风险点:     (a) 迁移 workflow 无 flavor 概念，需补全第三段（否则如 INTENT-COMPAT-036 排不到）；(b) 直接用 `large`/`2xlarge` 而未申请 → 排不到 runner 静默挂起（INTENT-COMP-001 已覆盖容量侧，此处聚焦迁移侧）；(c) flavor 名与实际 CPU/内存映射需迁移者理解。
预期系统行为: flavor 语义文档明确；未开通规格请求有明确报错。
Oracle 来源: 差异声明（GitCode flavor 体系有意不同）
对齐方向:   差异确认（规格表达有意不同）

验证要点:
  - [正向] small/medium 默认可用规格正常调度。
  - [负向] 未申请的 large+ 不应静默无限排队（与 INTENT-COMP-001 呼应）。
  - [非功能] flavor→资源映射 + 申请流程文档化。

触发条件:   分别请求 small 与未申请 large 的 job，比对调度与报错。
优先级线索: 关联 testing-focus §4/§10/§12；建议 P2（与 INTENT-COMP-001 变体关联，聚焦迁移视角）。关联 spec C-RUN-03。
来源输入:   spec.md C-RUN-03；workflow-samples/cann/*（2xlarge/xlarge/large）
```

---

## G 组 · 不支持能力的降级方式（testing-focus §10 · 报错 vs 静默忽略 vs 部分支持）

> 「降级方式分类」是角色卡明确方法论。不支持能力被静默忽略是最危险的兼容陷阱。

```
意图 ID:    INTENT-COMPAT-041
维度标签:   [compatibility, usability]
标题:       未知/不支持顶层字段的处理——报错 vs 静默忽略（GitHub 有 `run-name` 等 GitCode 无）

具体差异点:   workflow 含 GitCode 不识别的字段（如 GitHub `run-name`、`concurrency.cancel-in-progress`）时的处理。
GitHub 侧预期行为: GitHub 对未知顶层字段做 schema 校验报错；`run-name`/`permissions`/`concurrency.group` 等为合法字段。
GitCode 侧疑似行为: spec G-35 明确「非法 YAML/未知字段处理（报错 vs 静默忽略）未声明」——全文档未涉及。GitHub 有 `run-name`（workflow-syntax.md:15）GitCode 文档未提及。
风险点:     迁移 workflow 保留 GitHub 特有字段（`run-name`/`concurrency.cancel-in-progress`/`concurrency.group`/`jobs.<id>.environment`）时：若 GitCode 静默忽略 → 功能悄悄失效（如 run-name 不生效、并发组不生效导致重复运行）；若报错 → 需清理。**静默忽略是最危险的**——用户以为迁移成功实则行为缺失。
预期系统行为: 未知字段应报错或至少告警（指出该字段不支持），不完全静默忽略。
Oracle 来源: GitHub行为（schema 校验）+ 差异声明
对齐方向:   一致性（应有校验；静默忽略即缺陷，需坐实降级方式）

验证要点:
  - [正向] 合法 GitCode 字段正常。
  - [负向] GitHub 特有字段（run-name/cancel-in-progress）不应被静默忽略致功能缺失且无任何提示。
  - [非功能] 未知字段处理策略文档化（关联 G-35）。

触发条件:   提交含 `run-name:`、`concurrency: {group:, cancel-in-progress:}`、`jobs.x.environment:` 的 workflow，观察报错/告警/静默忽略。
优先级线索: 关联 testing-focus §1/§10/§11；建议 P1（静默功能缺失）。关联 spec G-35。
来源输入:   github-reference/reference/workflow-syntax.md:15,108-118,184；spec.md G-35
```

```
意图 ID:    INTENT-COMPAT-042
维度标签:   [compatibility, reliability]
标题:       concurrency 模型差异——GitHub `group`+`cancel-in-progress` vs GitCode `enable`+`max`+`exceed-action`+`preemption`

具体差异点:   并发控制的字段模型与语义完全不同。
GitHub 侧预期行为: `concurrency: {group: <表达式>, cancel-in-progress: bool}`；同 group 同时仅一个运行，新运行取消旧的。`queue: single/max`。
GitCode 侧疑似行为: spec C-EXEC-21/C-EXEC-22 用 `{enable, max(1-5), exceed-action: IGNORE/QUEUE, preemption: {enable, events}}`——无 group 概念，用 max 数值 + 抢占事件。真实样本 op-plugin `concurrency: {max:5, exceed-action:QUEUE, enable:true, preemption:{enable:true, events:[mr_id]}}`。
风险点:     完全不同的模型：迁移 GitHub `concurrency: {group: ${{github.ref}}, cancel-in-progress: true}` 到 GitCode 无直接对应——group 表达式无处安放，cancel-in-progress 语义要用 preemption 表达。若 GitCode 静默忽略 group → 并发去重失效 → 同分支重复运行浪费资源/竞态。preemption.events 的 `mr_id` 语义（按 MR 抢占）也无 GitHub 对应。
预期系统行为: 两模型映射关系文档化；GitHub 式 concurrency 字段有明确处理。
Oracle 来源: 差异声明（并发模型有意不同）
对齐方向:   差异确认（模型有意不同）

验证要点:
  - [正向] GitCode `max`+`exceed-action:QUEUE` 按声明排队。
  - [负向] GitHub 式 `group`+`cancel-in-progress` 不应被静默忽略致并发去重失效（同 ref 重复跑）。
  - [非功能] concurrency 模型迁移映射文档化。

触发条件:   （a）GitCode 式 concurrency 并发超 max 观察 QUEUE/IGNORE；（b）GitHub 式 group+cancel-in-progress 提交观察是否报错/忽略。
优先级线索: 关联 testing-focus §3/§10/§12；建议 P1。关联 spec C-EXEC-21/C-EXEC-22/C-QUOTA-01。
来源输入:   github-reference/reference/workflow-syntax.md:108-118；spec.md C-EXEC-21/C-EXEC-22；workflow-samples/op-plugin/PR-pipeline_op-plugin.yml:3-9
```

```
意图 ID:    INTENT-COMPAT-043
维度标签:   [compatibility]
标题:       action `runs.using` 运行时差异——GitHub `node20`/`docker`/`composite` vs GitCode 仅 `node16`

具体差异点:   自定义 action 的执行运行时类型。
GitHub 侧预期行为: `runs.using` 支持 `node20`/`node16`/`docker`/`composite`；composite action 组合多 step 极常用。
GitCode 侧疑似行为: spec C-ACT-12 文档**仅列出 `node16`**（唯一列出值），无 docker/composite。
风险点:     (a) 迁移使用 composite action（`using: composite`）的本地/第三方 action 到 GitCode 若不支持 → action 无法加载；(b) Docker action（`using: docker`）不支持 → 大量社区 action 失效；(c) `node20`/`node16` 版本差异——GitHub 已弃用 node16，GitCode 仅 node16，新 action 用 node20 可能不兼容。这直接限制可复用的 action 生态。
预期系统行为: 支持的 using 类型明确；不支持类型（docker/composite/node20）的 action 有明确加载报错。
Oracle 来源: 差异声明（GitCode 运行时受限）
对齐方向:   差异确认（using 类型集有意/事实受限）

验证要点:
  - [正向] `using: node16` 的 action 正常执行。
  - [负向] `using: composite`/`using: docker`/`using: node20` 的 action 不应静默不执行任何逻辑却报成功（应明确不支持报错）。
  - [非功能] 支持的 runtime 清单文档化。

触发条件:   分别引用 node16 / composite / docker / node20 的 action，观察加载与执行。
优先级线索: 关联 testing-focus §7/§10/§11；建议 P1（限制 action 生态复用）。关联 spec C-ACT-12。
来源输入:   github-reference/reference/workflow-syntax.md:142-143；spec.md C-ACT-12
```

```
意图 ID:    INTENT-COMPAT-044
维度标签:   [compatibility]
标题:       `uses` action 引用方式差异——GitHub `owner/repo@ref` marketplace vs GitCode 官方短名 + 本地

具体差异点:   action 引用的三种形态与来源信任。
GitHub 侧预期行为: `actions/checkout@v4`（marketplace owner/repo@ref）、`./local`、`docker://`；marketplace 生态庞大。
GitCode 侧疑似行为: spec C-ACT-06/C-ACT-08 三种：官方短名（无 owner，如 `uses: checkout`）、`owner/repo/path@ref`、本仓 `./path`。真实样本混用：`uses: checkout`（短名）、`uses: setup-python`、`uses: obs-upload`、`uses: cann/.gitcode/actions/precommit@master`、`uses: WWQ129/.gitcode/actions/Only_Doc_Commit_Check@main`。
风险点:     (a) GitCode 官方短名 `uses: checkout`（无版本）无 GitHub 对应——GitHub 必须 `actions/checkout@vN`；迁移时 `actions/checkout@v4` 是否被 GitCode 识别（owner=actions 的库是否存在）未知；(b) GitCode 无 marketplace，社区 action `owner/repo@ref` 需目标托管在 GitCode 上——GitHub 上的 action 直接引用会失败；(c) 短名解析到哪个实现、版本如何固定（短名无 @ref）安全性存疑。
预期系统行为: 引用方式明确；GitHub marketplace 引用的兼容处理清晰；短名版本固定策略明确。
Oracle 来源: 差异声明（引用生态有意不同）
对齐方向:   差异确认（引用方式/生态有意不同）

验证要点:
  - [正向] `uses: checkout` 短名与 `owner/repo/path@ref` 正常解析执行。
  - [负向] `uses: actions/checkout@v4`（GitHub 式）不应静默解析到错误实现或空操作。
  - [非功能] 短名的版本/来源固定策略文档化（供应链安全，交 security）。

触发条件:   分别 `uses: checkout`、`uses: actions/checkout@v4`、`uses: 不存在owner/repo@ref`，观察解析结果。
优先级线索: 关联 testing-focus §7/§10/§11；建议 P1。与 security 供应链交叉。关联 spec C-ACT-06/C-ACT-07/C-ACT-08。
来源输入:   github-reference/reference/workflow-syntax.md:142；spec.md C-ACT-06/C-ACT-07/C-ACT-08；workflow-samples/cann/*、op-plugin
```

```
意图 ID:    INTENT-COMPAT-045
维度标签:   [compatibility]
标题:       废弃命令处理差异——`::set-output`/`::set-env`/`::add-path` 在 GitCode 的降级

具体差异点:   GitHub 已弃用、GitCode 也声明废弃的旧工作流命令，实际执行时的处理。
GitHub 侧预期行为: `::set-output name=k::v` 等已弃用，GitHub 运行时会**报警告但仍可能工作**一段时间，最终禁用。
GitCode 侧疑似行为: spec C-ACT-03 声明这些命令已废弃改用文件协议；但 G-24 指出插件开发指南示例**仍用 `::set-output var=`**（且语法 `var=` 与正文 `name=` 不一致）——文档自相矛盾。实际是否还工作未知。
风险点:     (a) 迁移的旧 workflow/action 用 `::set-output` 若 GitCode 完全不支持（静默丢弃）→ output 设置失败下游取空，且无警告；(b) 若部分支持则行为不确定；(c) `var=` vs `name=` 语法差异使照文档写也可能失败。老旧 action 迁移的隐性断点。
预期系统行为: 废弃命令有明确处理（警告 + 兼容期，或明确报错），不静默丢弃；语法文档统一。
Oracle 来源: GitHub行为（GitHub 弃用但兼容）+ 差异声明
对齐方向:   差异确认（GitCode 废弃程度需坐实）

验证要点:
  - [正向] 文件协议 `>> $ATOMGIT_OUTPUT` 正常。
  - [负向] `::set-output name=k::v` 若不支持不应静默丢弃使下游取空（应警告/报错）。
  - [非功能] 废弃命令语法与兼容策略文档统一（消解 G-24）。

触发条件:   step 用 `echo "::set-output name=k::v"` 设 output，下游读取观察是否生效/警告/失败。
优先级线索: 关联 testing-focus §10/§11；建议 P2。关联 spec C-ACT-03/G-24。
来源输入:   github-reference/reference/workflow-commands.md:26-44；spec.md C-ACT-03/G-24
```

```
意图 ID:    INTENT-COMPAT-046
维度标签:   [compatibility, reliability]
标题:       step 输出/artifact 超限行为差异——1MB output、artifact 上限的降级方式

具体差异点:   超过限额（output 1MB/参数、artifact 大小）时截断 vs 报错。
GitHub 侧预期行为: GitHub output 有大小限制超限报错；artifact 有明确上限与保留策略。
GitCode 侧疑似行为: spec C-ACT-04/C-QUOTA-06 声明 output 每参数 1MB 但**超限行为未声明**（G-12）；C-ART-04 artifact 上限「已确认不超过限制」但**无具体值**（未知）。
风险点:     迁移中大 output（如完整测试报告写 output）或大 artifact，超限时 GitCode 若静默截断 → 下游拿到不完整数据却无报错（数据损坏静默传播）；若行为与 GitHub 不同则迁移预期落空。
预期系统行为: 超限行为明确（报错优于静默截断）；限额值文档化。
Oracle 来源: 差异声明 + GitHub行为
对齐方向:   差异确认（限额值/降级方式需坐实）

验证要点:
  - [正向] 限额内 output/artifact 正常。
  - [负向] 超 1MB output 不应静默截断使下游拿到损坏数据（应报错或明确截断标记）。
  - [非功能] 限额值 + 超限行为文档化（关联 G-12）。

触发条件:   写 >1MB 的单个 output 参数，下游读取比对完整性；上传接近上限的 artifact。
优先级线索: 关联 testing-focus §8/§10/§12；建议 P2。与 reliability 交叉。关联 spec C-ACT-04/C-QUOTA-06/G-12。
来源输入:   spec.md C-ACT-04/C-QUOTA-06/C-ART-04/G-12
```

---

## H 组 · 内置 action 差异（testing-focus §10 内置 action 差异）

> checkout/cache/setup-* 是每个 workflow 的地基；对应实现是否等价直接决定「开箱能跑多少」。

```
意图 ID:    INTENT-COMPAT-047
维度标签:   [compatibility, usability]
标题:       checkout action 差异——GitCode `uses: checkout` 参数集与 GitHub `actions/checkout@v4` 等价性

具体差异点:   checkout 的参数（ref/fetch-depth/token/path/repository/submodules/...）支持度与默认行为。
GitHub 侧预期行为: `actions/checkout@v4` 参数丰富：ref/repository/token/path/fetch-depth(默认1)/submodules/persist-credentials/clean 等；默认 checkout 触发 ref。
GitCode 侧疑似行为: spec C-ACT-09 仅列 `ref`/`fetch-depth`；真实样本另用 `token`、`path`（如 `path: "./runner"` 多仓 checkout）、`repository`（checkout 其他库）。C-ACT-08 短名 `checkout` 无版本。submodules/persist-credentials 等是否支持未声明。
风险点:     (a) 迁移 `actions/checkout@v4` 需改为 `uses: checkout`（短名）；(b) 依赖 `submodules: recursive`/`persist-credentials`/`clean` 等参数若 GitCode 不支持则子模块拉不到/凭据行为不同；(c) 默认 fetch-depth（GitHub 1 浅克隆 vs GitCode 未声明）不同 → `git log`/`git describe` 依赖历史的脚本失败；(d) 真实样本必带 `token: secrets.GIT_TOKEN`，暗示默认 token 不足（呼应 COMPAT-029）。
预期系统行为: checkout 参数集与 GitHub 对齐或明确子集；默认 fetch-depth 等行为文档化。
Oracle 来源: GitHub行为（actions/checkout 规格）+ 差异声明
对齐方向:   差异确认（实现是否等价需坐实）

验证要点:
  - [正向] `uses: checkout` + ref/token/path 按声明检出。
  - [负向] 依赖 submodules/深历史的迁移 workflow 不应因默认参数不同静默拿到不完整代码。
  - [非功能] 参数集 + 默认 fetch-depth 文档化。

触发条件:   用 fetch-depth 默认值做 `git log --oneline | wc -l`；用 `submodules: recursive` 检出含子模块仓库，比对 GitHub。
优先级线索: 关联 testing-focus §10/§11；建议 P1（checkout 是地基）。关联 spec C-ACT-08/C-ACT-09。
来源输入:   github-reference/reference/workflow-syntax.md:142；spec.md C-ACT-08/C-ACT-09；workflow-samples/cann/codecheck_action.yml:95-102（path 多仓）
```

```
意图 ID:    INTENT-COMPAT-048
维度标签:   [compatibility]
标题:       cache action 差异——key/restore-keys 语义、fork 隔离、跨 run 命中与 GitHub 等价性

具体差异点:   cache 的 key 精确匹配 + restore-keys 前缀兜底 + 作用域隔离。
GitHub 侧预期行为: `actions/cache` key 精确 + restore-keys 前缀；cache 按分支作用域，默认分支 cache 可被特性分支读；PR 有隔离。
GitCode 侧疑似行为: spec C-ART-05/C-ART-06 声明 key 精确 + restore-keys 前缀 + LRU；「**同仓库所有运行共享**」——但 G-19 指出 fork PR cache 是否隔离未声明（投毒面）。
风险点:     (a) 迁移 cache workflow 若 key 生成（hashFiles，见 COMPAT-013）行为不同则命中率变化；(b) 「同仓库所有运行共享」若含 fork PR → fork 可投毒主分支 cache（安全，交 security）；(c) restore-keys 前缀匹配顺序/回退语义与 GitHub 是否一致影响命中。
预期系统行为: cache key/restore-keys 语义与 GitHub 一致；作用域隔离明确（尤其 fork）。
Oracle 来源: GitHub行为（actions/cache 规格）+ 差异声明
对齐方向:   一致性（key 语义应对齐）+ 差异确认（隔离作用域坐实）

验证要点:
  - [正向] key 命中直接恢复；未命中走 restore-keys 前缀。
  - [负向] fork PR 不应能覆盖/污染主分支 cache（与 GitHub pull_request_target 只读 cache 对齐，交 security）。
  - [非功能] 作用域/隔离文档化（关联 G-19）。

触发条件:   同 key 两次 run 验证命中；restore-keys 前缀回退验证；fork PR 写 cache 观察是否影响主分支。
优先级线索: 关联 testing-focus §8/§10；建议 P2。与 security（cache 投毒）交叉。关联 spec C-ART-05/C-ART-06/G-19。
来源输入:   github-reference/security/pull_request_target.md:58（cache 只读）；spec.md C-ART-05/C-ART-06/G-19
```

```
意图 ID:    INTENT-COMPAT-049
维度标签:   [compatibility]
标题:       upload/download-artifact 差异——name 唯一性、path 默认、多 artifact 行为与 GitHub 等价性

具体差异点:   artifact 上传下载的参数与命名/覆盖语义。
GitHub 侧预期行为: `actions/upload-artifact@v4` name 必须唯一（v4 不可同名合并）、path 支持 glob；download 按 name 或全部。
GitCode 侧疑似行为: spec C-ART-01/C-ART-02 声明 upload `name`（workflow 内唯一）+ `path`（必填 glob/多路径）+ retention-days；download `name` 必填 path 默认当前目录，不指定 name 下载全部——方向与 GitHub v4 接近。真实样本用 OBS 自建上传（obs-upload）而非内置 artifact，暗示内置 artifact 可能能力不足。
风险点:     (a) name 唯一性冲突处理（GitHub v4 报错 vs GitCode？）不同则并行上传同名行为差异；(b) retention-days 默认（GitCode 90 天 vs GitHub 视设置）不同致 artifact 过早/过晚清理；(c) 真实项目弃用内置 artifact 转 OBS，暗示大文件/性能场景内置能力边界（呼应 C-ART-04 上限未知）。
预期系统行为: artifact 参数/命名语义与 GitHub 对齐或明确差异；同名冲突处理明确。
Oracle 来源: GitHub行为 + 差异声明
对齐方向:   一致性（参数语义应对齐）+ 差异确认（命名/上限坐实）

验证要点:
  - [正向] upload + download 跨 job 传递制品成功。
  - [负向] 同 name 并行上传不应静默覆盖丢数据（应与 GitHub 一致报错或明确合并规则）。
  - [非功能] retention 默认值 + name 唯一语义文档化。

触发条件:   两 job 上传同 name artifact 观察冲突处理；跨 job download 验证；不指定 name 下载全部验证。
优先级线索: 关联 testing-focus §8/§10；建议 P2。关联 spec C-ART-01/C-ART-02/C-ART-03/C-ART-04。
来源输入:   spec.md C-ART-01/C-ART-02/C-ART-03；workflow-samples/cann/*（obs-upload 自建）
```

```
意图 ID:    INTENT-COMPAT-050
维度标签:   [compatibility]
标题:       setup-* action 差异——setup-node/python/java/go 的 version/cache 参数与版本解析

具体差异点:   语言环境安装 action 的参数（version 规格、cache、architecture）与版本解析。
GitHub 侧预期行为: `setup-node`（node-version 支持 `20`/`lts/*`/`.nvmrc`）、`setup-java`（java-version+distribution）、`setup-python`、`setup-go` + cache 参数；version 支持范围/别名。
GitCode 侧疑似行为: spec C-ACT-10 参数由示例观察（node-version/java-version+distribution/go-version/python-version + cache），**无独立参数规格页**。真实样本 `uses: setup-python`（无版本参数，裸用）。
风险点:     (a) 迁移 `node-version: 'lts/*'` 或 `.nvmrc` 文件解析若 GitCode 不支持 → 装错版本/失败；(b) `distribution:`（Java 的 temurin/zulu 等）取值集不同 → 装不到指定发行版；(c) cache 参数（npm/pip/maven）与内置 cache 联动是否一致；(d) 裸 `setup-python` 无版本时的默认版本行为未知。
预期系统行为: setup-* 参数与 GitHub 对齐或明确子集；version 别名/文件解析支持度文档化。
Oracle 来源: GitHub行为（setup-* 规格）+ 差异声明
对齐方向:   差异确认（参数规格无独立文档，需坐实）

验证要点:
  - [正向] `node-version: '20'` 等精确版本正确安装。
  - [负向] `lts/*`/`.nvmrc`/未知 distribution 不应静默装成默认版本致构建用错运行时。
  - [非功能] setup-* 参数规格页补全。

触发条件:   `setup-node` 用 `20`/`lts/*`/`.nvmrc` 三种 version 规格，`setup-java` 用不同 distribution，比对安装结果。
优先级线索: 关联 testing-focus §10/§11；建议 P2。关联 spec C-ACT-10。
来源输入:   spec.md C-ACT-10；workflow-samples/op-plugin:137（裸 setup-python）
```

```
意图 ID:    INTENT-COMPAT-051
维度标签:   [compatibility]
标题:       action inputs 环境变量注入差异——`INPUT_<NAME>` 命名转换与 required 校验

具体差异点:   action 的 with 参数转为 `INPUT_*` 环境变量的命名规则与 required 行为。
GitHub 侧预期行为: with 参数生成 `INPUT_<NAME>`（大写、空格转 `_`）；`required: true` 缺失时 GitHub 运行时**不自动报错**（需 action 代码校验，与 GitCode 一致）。
GitCode 侧疑似行为: spec C-ACT-14 声明生成 `INPUT_<NAME>`（大写、空格转 `_`），`required:true` 缺失不自动报错——与 GitHub 一致。但连字符 `-` 的转换（GitHub 保留 `-`？）、特殊字符处理未详。
风险点:     (a) with 参数名含 `-`（如 `node-version`）转为 `INPUT_NODE-VERSION` 还是 `INPUT_NODE_VERSION`——GitHub 保留连字符，若 GitCode 转下划线则 action 代码读 env 失败；(b) required 都不自动校验虽一致，但迁移者若依赖平台校验会两边都踩坑。
预期系统行为: INPUT_* 命名转换与 GitHub 一致（尤其连字符）；required 语义一致。
Oracle 来源: GitHub行为（workflow-commands.md toolkit）
对齐方向:   一致性（命名转换应与 GitHub 一致）

验证要点:
  - [正向] `with: {my_input: v}` → `INPUT_MY_INPUT` 可读。
  - [负向] `with: {node-version: v}` 的连字符转换不应与 GitHub 不同致 action 读 env 落空。
  - [非功能] 命名转换规则（尤其 `-`）文档化。

触发条件:   本地 action with 含 `node-version`/`my input`/`camelCase` 参数，action 内 echo 对应 INPUT_* 变量，比对命名。
优先级线索: 关联 testing-focus §7/§10；建议 P2。关联 spec C-ACT-14。
来源输入:   github-reference/reference/workflow-commands.md:34；spec.md C-ACT-14
```

---

## I 组 · 安全语义兼容差异（testing-focus §10/§5 · 与 security 维度交叉，聚焦「兼容行为差异」侧）

> 本组只出「与 GitHub 安全语义是否一致」的兼容 intent；攻击 payload/exploit 归 security agent（rules §6）。

```
意图 ID:    INTENT-COMPAT-052
维度标签:   [compatibility, security]
标题:       fork PR token 降权语义一致性——GitCode fork `pull_request` 是否确降只读

具体差异点:   来自 fork 的 `pull_request` 事件下自动 token 的权限降级。
GitHub 侧预期行为: fork PR 的 `GITHUB_TOKEN` 只读，secrets 不传递（除 GITHUB_TOKEN）；需写权限用 pull_request_target。
GitCode 侧疑似行为: spec C-SEC-09/C-SEC-05 声明 fork `pull_request` token 仅 read 且无视 permissions 声明，fork 不可访问 secret——**方向与 GitHub 一致**。需实测确认隔离强度真的落地。
风险点:     若 GitCode 降权未真正生效（如 fork PR 仍能拿到写 token 或读到 secret），则迁移的 fork 协作流程存在越权/泄密——「文档说一致但实现有洞」。这是兼容性验证的安全命脉交叉点：预期一致，重点是坐实一致性真实成立。
预期系统行为: fork PR token 确为只读、secret 确不可达，与 GitHub 一致。
Oracle 来源: GitHub行为（github-token.md；secrets.md）+ GitCode 声明
对齐方向:   一致性（GitCode 声明与 GitHub 同向，重点坐实真实成立）

验证要点:
  - [正向] 非 fork（本仓）PR token 按 permissions 生效。
  - [负向] fork PR 的 token 不应能写仓库、不应读到项目/组织 secret（防御性验证，交 security 深挖 payload）。
  - [非功能] 降权行为文档与实现一致。

触发条件:   以 fork 贡献者身份提交 `pull_request`，job 内尝试读 secret / 用 token 写操作，观察是否被拒（意图层，具体断言交 security）。
优先级线索: 关联 testing-focus §5/§10；建议 P0（安全命脉）。与 security 维度强交叉。关联 spec C-SEC-05/C-SEC-09。
来源输入:   github-reference/security/github-token.md:42;secrets.md；spec.md C-SEC-05/C-SEC-09
```

```
意图 ID:    INTENT-COMPAT-053
维度标签:   [compatibility, security]
标题:       pull_request_target 语义一致性——base 上下文执行 + secret 可达 + cache 只读

具体差异点:   `pull_request_target` 的执行上下文、token 权限、cache 读写、workflow 文件来源。
GitHub 侧预期行为: 运行于 base 默认分支上下文，用默认分支的 workflow 文件（PR 不可改）；token read/write；可访问 secret；cache 对默认分支作用域**只读**（防投毒）；checkout v7+ 有 allow-unsafe-pr-checkout 保护。
GitCode 侧疑似行为: spec C-TRIG-03/C-SEC-10 声明 _target 用 base 分支 workflow 文件、可读写目标仓库、访问 secret——方向一致。但 cache 只读保护、checkout 是否有等价 unsafe-checkout 防护**未声明**（events.md 差异提示指需实测）。
风险点:     (a) 若 GitCode _target 下 cache 非只读 → fork 可经 _target 投毒 cache；(b) 若 checkout 无 unsafe-pr-checkout 等价保护 → pwn request 面比 GitHub 更宽；(c) workflow 文件是否真的取 base（PR 不可改执行逻辑）需坐实——若取 PR 版本则 fork 可改逻辑拿 secret（严重）。
预期系统行为: _target 的隔离控制（base workflow、cache 只读、checkout 保护）与 GitHub 一致。
Oracle 来源: GitHub行为（pull_request_target.md）+ GitCode 声明
对齐方向:   一致性（应与 GitHub 加固语义一致，坐实保护真实成立）

验证要点:
  - [正向] _target 下用 base 分支 workflow 文件 + 可访问 secret。
  - [负向] _target 下 fork 不应能改执行逻辑、不应能写 cache 投毒（防御性，交 security）。
  - [非功能] cache 只读 / checkout 保护文档化。

触发条件:   fork PR 触发 _target，尝试（a）改 PR 内 workflow 观察是否用 base 版；（b）写 cache 观察是否被拒（意图层，payload 交 security）。
优先级线索: 关联 testing-focus §5/§8/§10；建议 P0（pwn request 面）。与 security 强交叉。关联 spec C-TRIG-03/C-SEC-10/G-17/G-19。
来源输入:   github-reference/security/pull_request_target.md:53-64；spec.md C-TRIG-03/C-SEC-10/G-17
```

```
意图 ID:    INTENT-COMPAT-054
维度标签:   [compatibility, security]
标题:       secret 日志脱敏一致性——`***` 遮掩对 base64/拼接/多行变形的覆盖与 GitHub 对齐

具体差异点:   secret 在日志中的自动脱敏范围（直接打印、base64、拼接、多行变形）。
GitHub 侧预期行为: secret 值自动 `***` 遮掩；但变形（base64/分段）后可能绕过——GitHub 也不保证完全防护，建议不依赖脱敏为边界。
GitCode 侧疑似行为: spec C-SEC-03 明确「`echo "${{ secrets.X }}"` 可能绕过脱敏」为**已声明弱点**（G-16）；方向与 GitHub「不应依赖脱敏」一致。
风险点:     兼容侧关注点：迁移者从 GitHub 带来的「脱敏心智」在 GitCode 是否同等（不多不少）。若 GitCode 脱敏覆盖比 GitHub 更弱（如连直接 `echo` 都不遮掩），则迁移后原本在 GitHub 被遮掩的日志在 GitCode 泄露——「看起来一样、防护更弱」。
预期系统行为: 直接引用的 secret 至少被遮掩（与 GitHub 同级）；变形绕过两边都存在且文档同等提示。
Oracle 来源: GitHub行为（secrets.md 脱敏）+ GitCode 声明
对齐方向:   一致性（脱敏覆盖不应弱于 GitHub）

验证要点:
  - [正向] 直接 `echo ${{ secrets.X }}` 在日志显示 `***`。
  - [负向] GitCode 脱敏不应比 GitHub 更弱（如直接引用都不遮掩）——防御性，具体变形 payload 交 security。
  - [非功能] 脱敏边界文档同等提示「勿依赖」。

触发条件:   日志中直接打印 secret（意图层，仅验证直接引用遮掩；base64/拼接变形交 security agent）。
优先级线索: 关联 testing-focus §5/§10；建议 P1。与 security 交叉。关联 spec C-SEC-03/G-16。
来源输入:   github-reference/security/secrets.md；spec.md C-SEC-03/G-16
```

```
意图 ID:    INTENT-COMPAT-055
维度标签:   [compatibility, security]
标题:       permissions `{}` 语义确认——全 none vs repository:read 的兼容影响

具体差异点:   `permissions: {}` 的实际权限（GitCode 文档自相矛盾）与 GitHub `{}` 对齐。
GitHub 侧预期行为: `permissions: {}` = 禁用所有权限（全 none）。
GitCode 侧疑似行为: spec C-SEC-08/G-21 指出 GitCode 两文档冲突：一处「全 none」、一处「仅 repository:read」。
风险点:     迁移 `permissions: {}`（GitHub 意图=最小权限全禁）到 GitCode：若 GitCode 实际是 repository:read（非全 none），则比 GitHub 多了读权限——最小权限意图被削弱（安全）；若确为全 none 则 checkout 可能失败（clone 需读权限，易用性）。二义性直接影响最小权限实践。
预期系统行为: `{}` 有唯一确定语义，与 GitHub（全 none）对齐或明确声明差异。
Oracle 来源: 差异声明（GitCode 内部矛盾，实测定权威回写 Parity Matrix）
对齐方向:   差异确认（GitCode 文档矛盾，坐实实际值）

验证要点:
  - [正向] `permissions: {}` 后 token 实际权限集唯一可确定。
  - [负向] 不应「文档 A 说全 none 但实际能读/写」而无记录。
  - [非功能] 消解 G-21 矛盾，与 GitHub `{}` 语义对齐说明。

触发条件:   设 `permissions: {}` 后尝试 checkout（需读）与评论 PR（需写），反推实际权限集。
优先级线索: 关联 testing-focus §5/§10；建议 P1。与 security/usability 交叉。关联 spec C-SEC-08/G-21/INTENT-COMP-006。
来源输入:   github-reference/reference/workflow-syntax.md:88；spec.md C-SEC-08/G-21
```

```
意图 ID:    INTENT-COMPAT-056
维度标签:   [compatibility, security]
标题:       recursive run 防护一致性——GitCode token 触发的运行是否防递归

具体差异点:   由自动 token 触发的事件是否再触发新 workflow（防无限递归）。
GitHub 侧预期行为: `GITHUB_TOKEN` 触发的事件**一般不创建新 workflow 运行**（防递归）；例外 workflow_dispatch/repository_dispatch；token 创建的 PR 需人工审批才跑。
GitCode 侧疑似行为: spec 未系统声明 ATOMGIT_TOKEN 的 recursive run 防护（github-token.md 对接点明确指出需验证）。
风险点:     迁移中「workflow 用 token push/评论触发另一 workflow」的模式：若 GitCode 无防递归 → token 的 push 触发新 run，新 run 又 push → **无限递归**耗尽配额；若防护规则与 GitHub 不同 → 迁移的自动化链条断裂（本应触发的没触发或本应静默的递归了）。
预期系统行为: ATOMGIT_TOKEN 触发的事件有防递归机制，与 GitHub 一致或明确声明。
Oracle 来源: GitHub行为（github-token.md:26-35）
对齐方向:   一致性（应有防递归；缺失即缺陷+安全隐患）

验证要点:
  - [正向] token 的普通 push 不触发新 workflow 运行（防递归）。
  - [负向] 不应出现 token 操作触发无限递归运行耗尽配额。
  - [非功能] 防递归规则 + 例外事件文档化。

触发条件:   workflow 用 ATOMGIT_TOKEN push 一个 commit 到触发分支，观察是否触发新 run（应不触发）。
优先级线索: 关联 testing-focus §2/§5/§10；建议 P1（无限递归耗配额）。与 security/reliability 交叉。关联 spec C-SEC-06。
来源输入:   github-reference/security/github-token.md:26-35；spec.md C-SEC-06
```

---

## J 组 · 结构 / 编排模型差异（testing-focus §1/§10 · GitCode 特有结构层）

> stages/post/pre/select 等是 GitCode 相对 GitHub 的结构性增量；YAML 解析容错也在此。

```
意图 ID:    INTENT-COMPAT-057
维度标签:   [compatibility, usability]
标题:       stages 编排层——GitHub 扁平 jobs 迁移到 GitCode 是否需引入 stages 及默认行为

具体差异点:   GitCode `stages`（阶段间串行、阶段内 job 并行）是 GitHub 无的结构层；扁平 jobs 迁移的落位。
GitHub 侧预期行为: GitHub 无 stages；job 顺序全靠 `needs` DAG；所有无依赖 job 并行。
GitCode 侧疑似行为: spec C-STRUCT-04/C-STRUCT-05 stages 可缺省（单阶段所有 job 并行）；有 stages 时 job 嵌套于 stage 内。真实样本大量用显式 stages（op-plugin stage_1/2/3、ops-nn stage1-4）+ 阶段内并行 + `needs` 混用未见。
风险点:     (a) 迁移 GitHub 扁平 `jobs:`（顶层）到 GitCode：无 stages 时 jobs 是否仍可顶层（C-STRUCT-02 称无 stages 时 jobs 顶层）——需坐实扁平结构可直接跑；(b) GitHub 靠 needs 表达的顺序，迁移后是保留 needs 还是需改造成 stages？两种编排范式并存时 needs 与 stage 顺序的相互作用未声明；(c) 阶段内默认全并行 vs GitHub 需显式无 needs。
预期系统行为: 扁平 jobs（GitHub 式）可直接迁移运行；needs 与 stages 的关系明确。
Oracle 来源: 差异声明（GitCode 特有编排层）
对齐方向:   差异确认（GitCode 特有结构，坐实迁移落位）

验证要点:
  - [正向] 无 stages 的顶层 jobs + needs DAG（GitHub 式）在 GitCode 正常执行。
  - [负向] GitHub 式 needs 不应因引入隐式 stage 而失效或顺序错乱。
  - [非功能] stages vs needs 编排选择的迁移指引文档化。

触发条件:   提交纯 GitHub 式（顶层 jobs + needs，无 stages）workflow，观察是否直接运行且 needs 顺序正确。
优先级线索: 关联 testing-focus §3/§10/§11；建议 P1（迁移结构落位）。关联 spec C-STRUCT-02/C-STRUCT-04/C-STRUCT-05。
来源输入:   github-reference/reference/workflow-syntax.md:120-131；spec.md C-STRUCT-02/C-STRUCT-04/C-STRUCT-05；workflow-samples/op-plugin、cann/ops-nn
```

```
意图 ID:    INTENT-COMPAT-058
维度标签:   [compatibility, usability]
标题:       stages 两种写法 + 缩进瑕疵——列表 `- name:` vs 映射 `stage1:` 的解析容错

具体差异点:   stages 定义的两种 YAML 形态（列表项 vs 映射键）与文档缩进瑕疵。
GitHub 侧预期行为: 无 stages 概念，无此差异。
GitCode 侧疑似行为: spec C-STRUCT-09/G-26 指出 stages 两种写法并存（列表 `- name:` vs 映射 `stage1:`），等价性未澄清；示例缩进疑有误。真实样本用**映射式**（`stage_1:`/`stage1:` 作键），op-plugin 与 ops-nn 均如此。
风险点:     (a) 两种写法若非等价，迁移者按文档某处写法可能解析失败；(b) YAML 映射式 stages 里 job 也是映射键（`SCA:`/`JOB_compile:`），与 GitHub jobs 映射一致但多套一层 stage——缩进层级深，易错；(c) 文档缩进瑕疵会误导用户写出解析失败的 YAML。这是 G-26 的落地验证。
预期系统行为: 两种写法等价性明确；YAML 解析对缩进错误有清晰报错（第几行）。
Oracle 来源: 差异声明（GitCode 特有，坐实等价性 + 解析容错）
对齐方向:   差异确认（GitCode 特有写法，坐实等价性）

验证要点:
  - [正向] 映射式与列表式 stages 若都合法则行为等价。
  - [负向] 缩进错误的 stages 不应静默按错误结构执行（应报错定位行号）。
  - [非功能] 推荐写法 + 解析报错质量（消解 G-26）。

触发条件:   同一编排分别用列表式与映射式 stages 提交，比对执行；故意缩进错一层观察报错。
优先级线索: 关联 testing-focus §1/§10/§11；建议 P2。关联 spec C-STRUCT-09/G-26。
来源输入:   spec.md C-STRUCT-09/G-26；workflow-samples/op-plugin:52,74；cann/ops-nn_action.yml:21-22
```

```
意图 ID:    INTENT-COMPAT-059
维度标签:   [compatibility]
标题:       GitCode 特有 stage 字段——`select`/`pre`/`fail-fast` 无 GitHub 对应的语义确认

具体差异点:   真实样本 stage/job 上的 `select: selected_by_default`、`pre: - type: auto`、stage 级 `fail-fast: true` 等 GitCode 独有字段。
GitHub 侧预期行为: 无这些字段；job 选择靠 if/needs，无「默认选中」概念，无 stage 级 pre/fail-fast。
GitCode 侧疑似行为: 真实样本 ops-nn 每 stage 带 `pre: - type: auto` + `fail-fast: true`；op-plugin job 带 `select: selected_by_default`。spec 中 `stages.fail_fast`（C-STRUCT-06）有记，但 `select`/`pre`/`pre.type: auto` **未在能力清单出现**——文档盲区。
风险点:     (a) `select: selected_by_default` 语义（手动触发时默认选中该 job？）未文档化，影响 workflow_dispatch/评论触发时 job 的默认执行集——迁移者不知如何控制；(b) `pre: - type: auto` 阶段预处理语义未知（自动做什么？）；(c) 这些字段是生产必需但 spec 缺失，属能力清单重大遗漏。
预期系统行为: select/pre 等字段语义文档化并回填能力清单；缺失时行为明确。
Oracle 来源: 差异声明（GitCode 特有字段，spec 遗漏，需实测 + 文档）
对齐方向:   差异确认（GitCode 特有，坐实语义）

验证要点:
  - [正向] `select: selected_by_default` 的 job 在默认触发下执行行为被记录。
  - [负向] 不应存在「生产广泛使用但文档零记载」的编排字段——需回填清单。
  - [非功能] select/pre/pre.type 语义文档化（建议登记新 G）。

触发条件:   含 `select`/`pre: -type:auto` 的 stage 分别在自动/手动触发下观察 job 选择与预处理行为。
优先级线索: 关联 testing-focus §3/§10；建议 P1（生产必需 + 文档盲区）。关联 spec C-STRUCT-05/C-STRUCT-06。
来源输入:   workflow-samples/cann/ops-nn_action.yml:99-101,249-251；op-plugin:55,76；spec.md C-STRUCT-05/C-STRUCT-06
```

```
意图 ID:    INTENT-COMPAT-060
维度标签:   [compatibility, usability]
标题:       非法 YAML / schema 校验报错质量——错在第几行、可操作提示与 GitHub 对齐

具体差异点:   语法错误/类型错误/缺必填字段时的报错定位与可操作性。
GitHub 侧预期行为: GitHub 对 workflow 做 schema 校验，报错指出行号与问题字段（如「on is required」）。
GitCode 侧疑似行为: spec G-35 指出「非法 YAML/未知字段处理未声明」；报错质量全文档未涉及。真实样本混用多种写法（identifier/select/pre）暗示解析器较宽松。
风险点:     迁移必然产生大量语法/字段错误（前述各组差异），报错质量直接决定迁移调试成本。若 GitCode 报错泛化（「解析失败」无行号）或静默忽略错误字段 → 用户无法定位，迁移摩擦剧增（business-context 维度2 明确关注报错精准度）。
预期系统行为: 语法/schema 错误报错含行号 + 可操作提示，不劣于 GitHub。
Oracle 来源: GitHub行为（schema 校验报错）
对齐方向:   一致性（报错质量不应劣于 GitHub）

验证要点:
  - [正向] 合法 workflow 正常解析。
  - [负向] 缺 `on:`/类型错误/缩进错不应给泛化「失败」无定位，也不应静默忽略。
  - [非功能] 报错含行号 + 字段名 + 改法建议（eval: llm_assisted 判可理解性，交 usability）。

触发条件:   提交（a）缺 on（b）types 类型写错（c）缩进错（d）未知字段的 workflow，评估报错定位质量。
优先级线索: 关联 testing-focus §1/§10/§11；建议 P1（迁移调试成本）。与 usability 交叉。关联 spec G-35、business-context 维度2。
来源输入:   github-reference/reference/workflow-syntax.md:8；spec.md G-35；business-context/README.md 维度2
```

```
意图 ID:    INTENT-COMPAT-061
维度标签:   [compatibility]
标题:       workflow_call 复用差异——嵌套层数、secrets 传递、inputs 类型与 GitHub 对齐

具体差异点:   可重用工作流的嵌套上限、secrets/inputs 传递、outputs 映射。
GitHub 侧预期行为: reusable workflow 可嵌套（有层数限制）；`secrets: inherit` 或显式传；inputs 支持 boolean/number/string；outputs 经 jobs.<id>.outputs 传。
GitCode 侧疑似行为: spec C-TRIG-07 嵌套**最多 2 层**（不能再套）；inputs 仅 string；可声明 secrets。真实样本大量 `uses: .gitcode/workflows/xxx.yml` + 显式 `secrets: {OBS_AK: ...}` 传递 + `with:` 传 inputs + outputs 经 `jobs.JOB_x.outputs`（arm_compile outputs 映射）。
风险点:     (a) 嵌套层数（GitCode 2 层 vs GitHub 更深）——深层复用迁移超限（呼应 INTENT-COMP-004）;(b) GitCode 无 `secrets: inherit`？需逐个显式传，迁移 `secrets: inherit` 的 workflow 失效；(c) inputs 仅 string（呼应 COMPAT-024）;(d) outputs 映射语法 `${{ jobs.JOB_x.outputs.y }}`（样本 arm_compile）与 GitHub `${{ jobs.x.outputs.y }}` 是否一致。
预期系统行为: 复用机制与 GitHub 对齐或明确差异（层数/secrets inherit/inputs 类型）。
Oracle 来源: GitHub行为（workflow-syntax.md workflow_call）+ 差异声明
对齐方向:   差异确认（层数/inputs 有意不同）+ 一致性（outputs 映射语义）

验证要点:
  - [正向] `uses: .gitcode/workflows/x.yml` + 显式 secrets/with 正常调用并取 outputs。
  - [负向] `secrets: inherit`（GitHub 式）不应静默不传致被调 workflow 拿不到 secret。
  - [非功能] 嵌套层数、secrets 传递方式、outputs 映射文档化。

触发条件:   （a）2 层与 3 层嵌套调用观察超限；（b）`secrets: inherit` 观察是否支持；（c）outputs 跨 workflow_call 映射验证。
优先级线索: 关联 testing-focus §7/§10/§11；建议 P1。关联 spec C-TRIG-07/C-EXEC-06/INTENT-COMP-004。
来源输入:   github-reference/reference/workflow-syntax.md:55；events.md:70-73；spec.md C-TRIG-07/C-EXEC-06；workflow-samples/cann/arm_compile_action.yml:12-16、op-plugin:191-194
```

---

## 交接说明

- **本产出 61 条兼容性 intent**，按 A–J 十组覆盖 testing-focus §10 全部差异类别 + §11 迁移摩擦。
- **对齐方向分布**：一致性用例 **21** 条（GitCode 未声明差异、应与 GitHub 对齐，实测不一致即缺陷）；差异确认用例 **40** 条（GitCode 有意/事实不同，实测回写 Parity Matrix 成权威 oracle）。部分 intent 兼含两方向（如 COMPAT-005/006/032/048/061），归类以主导方向计。
- **给 case-writer**：每条含触发条件 + 三线断言线索（状态/日志/副作用），可直接展开；破坏性/fork 类与 security 维度共享 fixture（with-secrets、fork-contributor）。
- **回填 spec 缺口**：本轮新发现 spec **未收录**的生产字段/函数，建议登记新缺口——`default()` 函数（COMPAT-009）、`identifier`（016）、`pr_comment`/`keyword`（018）、`select`/`pre`/`pre.type:auto`（059）。这些是「生产广泛使用但文档零记载」的高价值盲区。
- **与 security 维度交叉**：I 组（052–056）+ COMPAT-015/019/044/048 只出兼容行为差异侧，攻击 payload/exploit 归 security（rules §6）。
- **优先级线索**：P0 候选=COMPAT-008（状态函数）/017（PR types）/036（runs-on）/052/053（fork 安全）——迁移直接断点或安全命脉；待风险登记册脱离模板态后由门禁定级。
- **输入版本**：github-reference fetched 2026-07-20；workflow-samples cann+op-plugin（2026-07-21 目录）；spec.md Run 2026-07-21-02；business-context 2026-07-21（Runner/迁移改造点仍模板态，维度3 兼容大纲已用）。若输入刷新按 rules §12 重审。
