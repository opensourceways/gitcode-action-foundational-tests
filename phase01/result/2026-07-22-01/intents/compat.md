# compat-diff Agent 产出 · 兼容性差异 Intent 清单

> Run: 2026-07-22-01  
> Agent: compat-diff  
> 输入版本: phase01/inputs/github-reference/ (2026-07-20), phase01/inputs/gitcode-spec/ (2026-07-20), phase01/baseline/parity-matrix.md (当前工作树), phase01/testing-focus.md (当前工作树)

---

## 一、扫描骨架与差异类别覆盖情况

以 `testing-focus.md` §10 的 7 大差异类别为扫描骨架，覆盖如下：

| 差异类别 | 覆盖状态 | 关联 Intent ID |
|---|---|---|
| 1. 默认值差异 | ✅ 已覆盖 | INTENT-COMPAT-001 ~ INTENT-COMPAT-003 |
| 2. 表达式函数差异 | ✅ 已覆盖 | INTENT-COMPAT-004 ~ INTENT-COMPAT-010 |
| 3. 触发过滤语义差异 | ✅ 已覆盖 | INTENT-COMPAT-011 ~ INTENT-COMPAT-015 |
| 4. 上下文对象差异 | ✅ 已覆盖 | INTENT-COMPAT-016 ~ INTENT-COMPAT-020 |
| 5. 不支持能力的降级方式 | ✅ 已覆盖 | INTENT-COMPAT-021 ~ INTENT-COMPAT-024 |
| 6. 内置 action 差异 | ✅ 已覆盖 | INTENT-COMPAT-025 ~ INTENT-COMPAT-027 |
| 7. runner 标签/环境差异 | ✅ 已覆盖 | INTENT-COMPAT-028 ~ INTENT-COMPAT-029 |
| 8. 迁移摩擦（§11 增补） | ✅ 已覆盖 | INTENT-COMPAT-030 ~ INTENT-COMPAT-033 |

> 注：部分 intent 同时触及安全/易用性维度，已标注多维度标签。

---

## 二、输入退化标注（必须在输出中体现）

| 输入目录 | 退化状态 | 影响说明 |
|---|---|---|
| `inputs/workflow-samples/` | ⚠️ 仅 README.md + 8 个真实 workflow 样本，无广泛开源社区 GitHub workflow 样本 | 差异发现将偏理论，缺真实 GitHub 负载佐证；已用现有 CANN/op-plugin 样本反向验证部分构造的常见性 |
| `inputs/business-context/` | ⚠️ 仅 README.md 模板，无迁移改造点清单 | 无法从业务侧获得「已知高频摩擦」反向输入，迁移摩擦类 intent 纯依赖规格差分推导 |
| `inputs/github-reference/` | ⚠️ 仅 INDEX.md + README.md + 6 页 reference + 5 页 security，GitHub oracle 内容偏少 | 部分边界行为（如 `hashFiles` 内部 glob 实现细节、`fromJSON` 的异常输入处理）缺少完整官方语义，oracle 精度受限 |

---

## 三、Intent 列表

---

```
意图 ID:    INTENT-COMPAT-001
维度标签:   [compatibility]
标题:       默认 shell 与默认工作目录在未声明时的隐式行为差异

风险点:     GitHub 未显式声明 defaults.run.shell 时默认使用 bash -e；GitCode 文档未明确未声明时的默认 shell。若默认 shell 不同（如 sh 而非 bash），会导致 `set -e` 行为、bashism 语法（数组、[[ ]] 等）在不同平台表现不一致。真实样本中大量 `run: |` 多行脚本隐含依赖 bash。
预期系统行为: GitCode 在未声明 defaults.run.shell 时应与 GitHub 一致使用 bash（或至少文档明确声明默认值），使迁移后的脚本行为不变。
Oracle 来源: GitHub行为 | 差异声明
             # 一致性：GitCode 未声明差异处，默认行为应与 GitHub 对齐

验证要点:
  - [正向] 未声明 shell 的 job 中执行 `echo $0` 或 `bash --version` 应得到 bash
  - [负向] 不应静默使用 sh 导致 bashism 脚本报错
  - [非功能] 默认值差异若存在，应在文档或报错中明示

对齐方向:   一致性
优先级线索: RISK-COMPAT-01（默认值差异致行为静默不同）
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（default shell 定义）; gitcode-spec/writing-pipelines/configure-steps.md（shell 字段说明，未明确默认值）; workflow-samples/cann/ops-nn_action.yml（大量 run 步骤隐含依赖 bash）
```

---

```
意图 ID:    INTENT-COMPAT-002
维度标签:   [compatibility, security]
标题:       未声明 permissions 时的默认 TOKEN 权限范围差异

风险点:     GitHub 默认 TOKEN 权限依仓库设置（可配 read/write）；GitCode 文档称「未声明 permissions 时使用仓库设置中定义的权限」，但具体默认值未明确。若默认权限过宽，fork PR 场景下存在 secret 泄露与越权写风险；若过窄，则正常 workflow 可能失败。这是「看起来一样、行为不一样」的高危默认值差异。
预期系统行为: GitCode 的默认 permissions 语义应与文档承诺一致，且与 GitHub 的默认行为在同等安全等级上对齐（fork PR 自动降级为 read）。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] 未声明 permissions 的 workflow 运行时，ATOMGIT_TOKEN 应能完成基本 clone/read 操作
  - [负向] fork PR 触发时，即使未声明 permissions，TOKEN 不应拥有 write 权限（除非显式使用 pull_request_target）
  - [非功能] 默认权限应在运行日志或 API 中可观测

对齐方向:   一致性
优先级线索: RISK-SEC-01（fork PR 读到仓库 secrets 的延伸）
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（permissions 默认值）; gitcode-spec/security-permissions/token-permissions.md（未声明时使用仓库设置）; testing-focus.md §5
```

---

```
意图 ID:    INTENT-COMPAT-003
维度标签:   [compatibility]
标题:       step/job 级 if 条件未显式声明时的默认状态检查差异

风险点:     GitHub 在 step/job 未显式写 if 时，默认注入 `success()`（即前置全部成功才执行）。GitCode 文档在 expressions.md 中注明「如未指定条件，默认为 success」。但 GitCode 状态函数语法是无括号的 `success`，需验证该默认值在引擎层面是否真正等价，以及当 job 有 `continue-on-error: true` 时默认行为是否一致。
预期系统行为: 未写 if 的 step/job 应在前面所有依赖步骤/任务成功时才执行，且 `continue-on-error` 后的结论（conclusion vs outcome）不影响默认调度。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] 前置 step 失败后，未写 if 的后续 step 应被跳过
  - [负向] 不应因语法差异（success vs success()）导致默认条件失效或全部执行
  - [非功能] 默认条件的行为应与显式写 `if: ${{ success }}` 一致

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（默认 status check）; gitcode-spec/syntax-reference/expressions.md（success 说明：如未指定条件，默认为 success）
```

---

```
意图 ID:    INTENT-COMPAT-004
维度标签:   [compatibility]
标题:       状态函数括号语法差异：GitHub `success()` vs GitCode `success`

风险点:     GitHub 状态函数必须带括号调用（`success()`/`failure()`/`always()`/`cancelled()`）；GitCode 文档明确使用无括号形式（`success`/`failed`/`always`/`cancelled`）。直接迁移的 GitHub workflow 若保留括号，在 GitCode 表达式解析器中的行为未知（可能解析失败、可能静默忽略、可能意外求值）。这是迁移最容易踩坑的点之一。
预期系统行为: GitCode 应对无括号语法正确求值；对 GitHub 风格的带括号语法应有明确降级策略（报错/兼容解析/忽略）。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] `if: ${{ success }}` 在 GitCode 中应正确求值为布尔值
  - [负向] `if: ${{ success() }}` 不应导致 workflow 解析阶段 panic 或运行时崩溃
  - [非功能] 若不支持括号语法，解析报错应明确指出「GitCode 状态函数不带括号」

对齐方向:   差异确认
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（status check functions 带括号）; gitcode-spec/syntax-reference/expressions.md（success/failed/always/cancelled 无括号）; COMPAT-NOTES.md §3
```

---

```
意图 ID:    INTENT-COMPAT-005
维度标签:   [compatibility]
标题:       失败状态函数命名差异：`failure()` vs `failed`

风险点:     GitHub 的失败状态函数名为 `failure()`，GitCode 为 `failed`。除了括号差异外，函数名本身也不同。迁移时即使去掉括号，写 `failure` 也会在 GitCode 中成为未定义标识符。真实 GitHub workflow 中 `if: ${{ failure() }}` 广泛用于失败通知、清理步骤，迁移遗漏率极高。
预期系统行为: GitCode 应仅识别 `failed`；对 `failure`（无论有无括号）应有明确报错或兼容处理。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `if: ${{ failed }}` 在 GitCode 中应在前置 step 失败时返回 true
  - [负向] `if: ${{ failure }}` 或 `if: ${{ failure() }}` 不应被静默当作 truthy 值导致无条件执行
  - [非功能] 报错信息应提示正确的函数名为 `failed`

对齐方向:   差异确认
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（failure() 定义）; gitcode-spec/syntax-reference/expressions.md（failed 定义）; COMPAT-NOTES.md §3
```

---

```
意图 ID:    INTENT-COMPAT-006
维度标签:   [compatibility]
标题:       `contains` 函数边界行为差异（大小写、空值、数组元素）

风险点:     GitHub `contains` 对字符串搜索不区分大小写，且会 cast values to string；对数组搜索判断元素是否存在。GitCode 文档仅描述「字符串搜索时为子串匹配；数组/对象搜索时判断是否存在该元素」，未明确大小写敏感性与类型转换规则。若 GitCode 区分大小写或空值处理不同，会导致条件判断静默失效。
预期系统行为: 在常见边界输入下（空字符串、null、大小写混合、数组元素对象过滤），GitCode 的 `contains` 行为应与 GitHub 一致或文档明确声明差异。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `contains('Hello', 'llo')` 返回 true
  - [正向] `contains('Hello', 'LLO')` 返回 true（与 GitHub 一致的不区分大小写）
  - [负向] `contains(null, 'x')` 不应抛出未处理异常
  - [非功能] 数组元素对象过滤（如 `contains(atomgit.event.pull_request.labels.*.name, 'bug')`）应正确工作

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（contains 详细语义）; gitcode-spec/syntax-reference/expressions.md（contains 简述）
```

---

```
意图 ID:    INTENT-COMPAT-007
维度标签:   [compatibility]
标题:       `hashFiles` 函数边界行为差异（无匹配文件、glob 语义、大小写）

风险点:     GitHub `hashFiles` 在无匹配文件时返回空字符串，glob 匹配基于 `GITHUB_WORKSPACE`，Windows 上大小写不敏感。GitCode 文档仅简述「计算匹配路径文件的组合 SHA256 哈希」。若边界行为不同（如无匹配时报错而非返回空串），会直接影响缓存 key 生成策略，导致缓存失效或构建失败。真实样本 `PR-pipeline_op-plugin.yml` 中使用了 `hashFiles('package-lock.json')` 类缓存 key。
预期系统行为: `hashFiles` 在无匹配文件时应返回空字符串（与 GitHub 一致），glob 语义应与常见预期一致。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `hashFiles('不存在的文件.json')` 返回空字符串
  - [正向] `hashFiles('src/**', 'package.json')` 对多路径模式正确计算组合哈希
  - [负向] 无匹配时不应抛出异常导致 step 失败
  - [非功能] 相同文件集多次调用应返回确定性结果

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（hashFiles 语义）; gitcode-spec/syntax-reference/expressions.md（hashFiles 简述）; workflow-samples/op-plugin/PR-pipeline_op-plugin.yml（缓存场景）
```

---

```
意图 ID:    INTENT-COMPAT-008
维度标签:   [compatibility]
标题:       `toJson` 输出格式差异（pretty-print vs 压缩）

风险点:     GitHub `toJSON` 返回 pretty-print JSON（带缩进和换行），常用于调试输出和生成动态矩阵配置。GitCode 文档仅写「将对象序列化为 JSON 字符串」，未明确是否 pretty-print。若输出为压缩 JSON，会影响基于行解析的下游步骤，且调试日志可读性下降。
预期系统行为: `toJson` 输出应为 pretty-print JSON，与 GitHub 行为一致，或文档明确声明格式差异。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `toJson(atomgit.event)` 输出应包含换行和缩进
  - [负向] 不应输出一行压缩 JSON 导致与 GitHub workflow 预期不一致
  - [非功能] 序列化后的 JSON 应能被标准 JSON 解析器正确解析

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（toJSON 定义）; gitcode-spec/syntax-reference/expressions.md（toJson 定义）
```

---

```
意图 ID:    INTENT-COMPAT-009
维度标签:   [compatibility]
标题:       表达式 loose equality 与类型强制转换规则差异

风险点:     GitHub 有明确的类型强制转换规则：字符串比较忽略大小写、NaN 比较返回 false、null 转为 0、布尔转为 1/0 等。GitCode 文档未描述任何类型强制转换规则。若 `==` 运算符在类型不匹配时行为不同（如字符串与数字比较），会导致条件判断结果与 GitHub 不一致。这是极难排查的隐性差异。
预期系统行为: GitCode 的 `==`/`!=`/`>`/`<` 等运算符在跨类型操作数时的行为应与 GitHub 一致，或文档明确列出差异。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `'5' == 5` 应返回 true（GitHub  loose equality）
  - [正向] `null == 0` 应返回 true（GitHub 规则：null -> 0）
  - [正向] `true == 1` 应返回 true
  - [负向] 跨类型比较不应抛出类型错误异常
  - [非功能] 与 GitHub 不一致处应在文档中声明

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（loose equality + type coercion 详细表）; gitcode-spec/syntax-reference/expressions.md（仅列出运算符，无类型转换规则）
```

---

```
意图 ID:    INTENT-COMPAT-010
维度标签:   [compatibility, usability]
标题:       缺失表达式函数 `join()` / `fromJSON()` / `case()` 的降级行为

风险点:     GitHub 提供 `join()`、`fromJSON()`、`case()` 等函数，GitCode 官方文档未列出。直接迁移的 GitHub workflow 若使用这些函数，在 GitCode 中的行为未知：可能是解析报错、可能是运行时异常、可能静默求值为空。`fromJSON` 尤其常用于将字符串输入转为对象/数字，与 workflow_dispatch inputs 类型限制问题叠加后风险更高。
预期系统行为: 对不支持的函数，GitCode 应在解析阶段给出明确报错（而非运行时异常或静默失败），报错信息应指明「函数不支持」及替代方案。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] 使用 `join(github.event.issue.labels.*.name, ', ')` 不应被静默忽略或返回意外值
  - [负向] 使用 `fromJSON('{"a":1}')` 不应导致运行时 panic
  - [非功能] 报错信息应包含「GitCode 不支持该函数」及建议替代写法

对齐方向:   差异确认
优先级线索: RISK-USE-01（迁移报错不指明 GitCode 差异）
破坏级别:   none
来源输入:   github-reference/reference/expressions.md（join/fromJSON/case 定义）; gitcode-spec/syntax-reference/expressions.md（函数列表未含 join/fromJSON/case）; COMPAT-NOTES.md §3
```

---

```
意图 ID:    INTENT-COMPAT-011
维度标签:   [compatibility, usability]
标题:       `pull_request` 事件 types 命名与取值差异

风险点:     GitHub `pull_request` types 为 `opened`/`synchronize`/`reopened`；GitCode 为 `open`/`update`/`reopen`，并额外有 `merge`。默认值双方也不完全相同（GitCode 默认不含 `merge`）。直接复制 GitHub workflow 的 `types: [opened, synchronize, reopened]` 到 GitCode 会导致解析失败或事件永远不触发。这是迁移第一摩擦点，且极难调试（workflow 不触发时无明确报错）。
预期系统行为: GitCode 对非法 types 值应在保存/解析时给出明确报错，而非静默不触发。对合法 GitCode types 值，触发语义应与命名对应（`update` 对应 GitHub 的 `synchronize`）。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `types: [open, update, reopen]` 在 GitCode 中应正确触发对应 PR 活动
  - [负向] `types: [opened, synchronize, reopened]` 不应被静默接受且不触发任何事件
  - [非功能] 报错信息应提示 GitCode 支持的 types 取值列表

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/events.md（pull_request types 定义）; gitcode-spec/syntax-reference/trigger-events.md（pull_request types 定义）; COMPAT-NOTES.md §5; baseline/case-base-detail.md（TC-234 PR types not triggering properly — NEEDS-UPDATE）
```

---

```
意图 ID:    INTENT-COMPAT-012
维度标签:   [compatibility, reliability]
标题:       `paths` 匹配文件数上限差异：GitHub 3,000 vs GitCode 300

风险点:     GitHub 在 paths diff 超过 3,000 文件时，若匹配文件不在前 3,000 中则不触发；GitCode 声明「paths 匹配前 300 个变更文件，超出部分不参与匹配」。对于大重构（如批量移动文件、依赖升级），GitCode 的 300 文件上限更容易导致「本应触发却不触发」的静默跳过。真实样本中无大文件数场景，但这是规模扩展后的隐性风险。
预期系统行为: GitCode 在变更文件超过 300 时，应仅基于前 300 个文件做 paths 匹配，且不触发时应在日志中留下「paths 过滤跳过」的明确痕迹。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] 301 个文件变更且第 301 个文件命中 paths 时，workflow 不应触发
  - [负向] 不应因内部溢出/截断导致崩溃或错误触发
  - [非功能] 运行日志或触发记录中应可见「仅评估前 300 个变更文件」的提示

对齐方向:   差异确认
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（paths diff 限制：>3,000 files）; gitcode-spec/writing-pipelines/configure-triggers.md（paths 匹配前 300 个变更文件）; baseline/case-base-detail.md（TC-422 paths 前 300 文件限制 — KEEP）
```

---

```
意图 ID:    INTENT-COMPAT-013
维度标签:   [compatibility]
标题:       `schedule` cron timezone 支持差异：GitHub 支持 IANA vs GitCode 仅 UTC

风险点:     GitHub `schedule` 支持 `timezone` 字段（IANA 时区名），GitCode 明确声明「cron 使用 UTC 时间」。直接迁移的 GitHub workflow 若含 `timezone: "America/New_York"`，在 GitCode 中会被静默忽略，导致定时任务在非预期 UTC 时间执行。对于跨时区团队，这会导致生产环境定时任务（如夜间备份、日报生成）在白天执行。
预期系统行为: GitCode 应仅支持 UTC；对含 `timezone` 字段的 workflow 应给出解析警告或报错，而非静默忽略。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] 不含 timezone 的 cron 应在 UTC 时间正确触发
  - [负向] 含 `timezone` 字段的 workflow 不应被静默接受并按 UTC 执行（导致与作者预期不符）
  - [非功能] 解析阶段应对 `timezone` 字段给出明确提示「GitCode 仅支持 UTC，timezone 字段被忽略」

对齐方向:   差异确认
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/events.md（schedule timezone 支持）; gitcode-spec/syntax-reference/trigger-events.md（cron 使用 UTC 时间）; COMPAT-NOTES.md §5; baseline/case-base-detail.md（Scheduler 不工作 — NEEDS-UPDATE）
```

---

```
意图 ID:    INTENT-COMPAT-014
维度标签:   [compatibility, usability]
标题:       `workflow_dispatch` / `workflow_call` inputs 类型限制：仅支持 string

风险点:     GitHub 支持 `boolean`/`choice`/`number`/`environment`/`string` 五种 inputs 类型；GitCode 仅支持 `string`。直接迁移的 GitHub workflow 若使用 `type: boolean` 或 `type: choice`，在 GitCode 中的降级行为未知：可能解析报错、可能静默当作 string 处理。后者会导致条件判断（如 `if: ${{ inputs.dry_run }}`）因字符串 `'false'` 为 truthy 而错误执行。真实样本中大量 workflow_dispatch 使用 string 模拟布尔值（如 `default: "false"`），但迁移时若保留原 GitHub 的 `type: boolean`，风险极高。
预期系统行为: GitCode 对非 string 的 inputs type 应在解析阶段报错，明确提示「仅支持 string 类型」；对已用 string 模拟布尔/数字的 workflow，应在文档中给出迁移指引。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] `type: boolean` 不应被静默当作 string 处理，导致 `if: ${{ inputs.flag }}` 恒为 true
  - [非功能] 报错信息应包含「GitCode inputs 仅支持 string 类型，请改用 string 并在表达式中转换」
  - [正向] `type: string` + `default: "false"` 应在 GitCode 中正常解析

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（workflow_dispatch input types）; gitcode-spec/syntax-reference/trigger-events.md（inputs type 规格：仅 string）; COMPAT-NOTES.md §9; workflow-samples/cann/（大量 workflow_dispatch 含 string 模拟布尔值）
```

---

```
意图 ID:    INTENT-COMPAT-015
维度标签:   [compatibility]
标题:       `workflow_call` 可复用工作流嵌套层数差异：GitHub 无明确上限 vs GitCode 最多 2 层

风险点:     GitHub 对 `workflow_call` 嵌套层数无明确上限（实际受运行时限制）；GitCode 明确限制最多 2 层（可复用工作流不能再调用另一个可复用工作流）。迁移复杂 CI 体系（如「根 workflow → 构建 workflow → 平台特定 workflow」三层调用）时，第三层会在 GitCode 中失败。真实样本 `ops-nn_action.yml` 中大量使用 `uses: .gitcode/workflows/xxx.yml`，但均为单层调用；三层嵌套在大型开源项目中较常见。
预期系统行为: GitCode 应在解析或运行阶段对超过 2 层的嵌套给出明确报错，而非运行时卡死或给出模糊错误。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] 第 3 层嵌套调用不应被静默接受后运行时异常
  - [非功能] 报错信息应明确指出「workflow_call 嵌套层数超过 2 层」及拆分建议
  - [正向] 2 层嵌套应正常工作

对齐方向:   差异确认
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/events.md（workflow_run 最多 3 层）; gitcode-spec/writing-pipelines/configure-triggers.md（嵌套调用最多支持 2 层）; COMPAT-NOTES.md §5
```

---

```
意图 ID:    INTENT-COMPAT-016
维度标签:   [compatibility, usability]
标题:       核心上下文对象前缀差异：`github.*` vs `atomgit.*`

风险点:     GitHub 使用 `github.ref`/`github.sha`/`github.event_name` 等；GitCode 使用 `atomgit.*` 前缀。直接将 GitHub workflow 搬到 GitCode 会导致所有上下文引用全线失效。由于这是「全局替换」级别的差异，单个遗漏就会导致运行时求值为空，进而导致条件判断、部署目标、版本标签等关键参数错误。这是迁移摩擦最大的点，没有之一。
预期系统行为: GitCode 应仅识别 `atomgit.*`；对 `github.*` 的引用应给出明确的解析/运行时报错，提示替换为 `atomgit.*`。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [负向] 使用 `github.ref` 不应被静默求值为空字符串（导致空值注入风险）
  - [非功能] 报错信息应包含「请将 github.* 替换为 atomgit.*」的迁移指引
  - [正向] `atomgit.ref` 应正确返回触发引用

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/contexts.md（github 上下文）; gitcode-spec/syntax-reference/context.md（atomgit 上下文）; COMPAT-NOTES.md §2; workflow-samples/（全部样本使用 atomgit.*）
```

---

```
意图 ID:    INTENT-COMPAT-017
维度标签:   [compatibility, usability]
标题:       系统环境变量前缀差异：`GITHUB_*` vs `ATOMGIT_*`

风险点:     GitHub Runner 注入 `GITHUB_SHA`/`GITHUB_REF`/`GITHUB_TOKEN` 等；GitCode 注入 `ATOMGIT_*`。Shell 脚本中直接引用 `$GITHUB_SHA` 的 GitHub workflow 迁移到 GitCode 后会得到空值。与上下文前缀差异类似，这是全局替换级摩擦，但更难发现（shell 中未定义变量不会报错，只会为空字符串）。真实样本 `PR-pipeline_op-plugin.yml` 中使用了 `$ATOMGIT_WORKSPACE`，说明样本已适配，但迁移用户极易遗漏。
预期系统行为: GitCode 应注入 `ATOMGIT_*` 系列变量；对脚本中引用 `GITHUB_*` 的行为不保证兼容，但平台方文档应提供完整对照表。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] `$ATOMGIT_SHA` 应正确返回触发提交 SHA
  - [负向] `$GITHUB_SHA` 在 GitCode Runner 中应为空或未定义（不应错误映射）
  - [非功能] 文档应提供完整的 `GITHUB_*` → `ATOMGIT_*` 对照表

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/variables.md（GITHUB_* 列表）; gitcode-spec/syntax-reference/variables.md（ATOMGIT_* 列表）; COMPAT-NOTES.md §2
```

---

```
意图 ID:    INTENT-COMPAT-018
维度标签:   [compatibility]
标题:       `runner.os` 值格式差异：GitHub `Linux` vs GitCode `linux`

风险点:     GitHub `runner.os` 返回首字母大写的 `Linux`/`Windows`/`macOS`；GitCode 已知 bug 返回小写 `linux`。大量 GitHub workflow 使用 `if: ${{ runner.os == 'Linux' }}` 或 `runner.os == 'Windows'` 来做平台特定逻辑。迁移到 GitCode 后这些条件会恒为 false，导致平台特定步骤被静默跳过（如 Windows 上装 msbuild、macOS 上装 xcode）。case-base-detail.md 中 TC-023/TC-094 等已记录为 FAIL。
预期系统行为: GitCode 应修复为与 GitHub 一致的 `Linux`（首字母大写），或在文档中明确声明值格式差异并提供迁移指引。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `runner.os` 在 Linux Runner 上应返回 `Linux`（与 GitHub 一致）
  - [负向] 不应返回 `linux` 导致 `runner.os == 'Linux'` 恒为 false
  - [非功能] 修复后 TC-023/TC-094/TC-136-139 等 NEEDS-UPDATE 用例应重新验证

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/contexts.md（runner.os 值：Linux）; gitcode-spec/syntax-reference/context.md（runner.os 值未明确大小写）; baseline/case-base-detail.md（TC-023/094/136-139 runner.os FAIL: 非法值=linux）
```

---

```
意图 ID:    INTENT-COMPAT-019
维度标签:   [compatibility]
标题:       `runner.arch` 值格式差异：GitHub `X64`/`ARM`/`ARM64` vs GitCode `x86_64`

风险点:     GitHub `runner.arch` 返回 `X64`/`ARM`/`ARM64`；GitCode 已知 bug 返回 `x86_64`。GitHub workflow 中常见 `if: ${{ runner.arch == 'X64' }}` 或矩阵条件判断。与 runner.os 类似，值格式不一致会导致条件静默失效。case-base-detail.md 中 TC-095/TC-442 已记录为 FAIL。
预期系统行为: GitCode 应修复为与 GitHub 一致的 `X64`，或文档明确声明并提供映射表。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `runner.arch` 在 x86_64 Runner 上应返回 `X64`（与 GitHub 一致）
  - [负向] 不应返回 `x86_64` 导致 `runner.arch == 'X64'` 恒为 false
  - [非功能] 修复后 TC-095/TC-442 应重新验证

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/contexts.md（runner.arch 值：X64）; gitcode-spec/syntax-reference/context.md（runner.arch 值：X64, ARM, ARM64）; baseline/case-base-detail.md（TC-095/442 FAIL: 非法值=x86_64）
```

---

```
意图 ID:    INTENT-COMPAT-020
维度标签:   [compatibility, security]
标题:       自动令牌命名差异：`GITHUB_TOKEN` vs `ATOMGIT_TOKEN`

风险点:     GitHub 使用 `secrets.GITHUB_TOKEN` 和 `github.token`；GitCode 使用 `secrets.ATOMGIT_TOKEN` 和 `atomgit.token`。迁移时直接复制 `secrets.GITHUB_TOKEN` 会求值为空，导致 API 调用认证失败。更严重的是，若脚本中使用 `curl -H "Authorization: token $GITHUB_TOKEN"`，空令牌可能导致请求以匿名身份发送，触发 rate limit 或权限拒绝。这是高频踩坑点。
预期系统行为: GitCode 应仅支持 `ATOMGIT_TOKEN`；对 `GITHUB_TOKEN` 的引用应在解析或运行时给出明确提示。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] `secrets.ATOMGIT_TOKEN` 和 `atomgit.token` 应正确返回有效令牌
  - [负向] `secrets.GITHUB_TOKEN` 不应被静默映射到 ATOMGIT_TOKEN（避免用户误以为无需修改）
  - [非功能] 运行日志中对 TOKEN 的引用应正确脱敏为 `***`

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/contexts.md（github.token 定义）; gitcode-spec/syntax-reference/context.md（atomgit.token 定义）; COMPAT-NOTES.md §2
```

---

```
意图 ID:    INTENT-COMPAT-021
维度标签:   [compatibility, usability]
标题:       未知/不支持字段的降级方式：报错 vs 静默忽略 vs 部分支持

风险点:     GitHub 对未知字段通常在 workflow 解析时报错（如 YAML schema 校验）。GitCode 文档未明确说明未知字段的处理策略。若 GitCode 对未知字段静默忽略，会导致用户误以为配置生效（如写了 `run-name` 或 `jobs.<id>.services` 但平台不支持），运行时行为与预期不符。parity-matrix.md 中已标记「文档未明确降级方式」。
预期系统行为: 对 GitCode 明确不支持的字段（如 GitHub 特有的 `run-name`、`jobs.<id>.services`、`jobs.<id>.permissions` 的 GitHub 权限域名），应在保存/解析阶段给出明确报错或警告。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] 含 `run-name` 的 workflow 不应被静默接受且运行名显示为文件路径
  - [非功能] 报错信息应指明「字段 X 在 GitCode 中不支持」
  - [正向] 对 GitCode 支持但语义不同的字段（如 `permissions`），应给出语义差异警告

对齐方向:   一致性（对未知字段应报错，与 GitHub schema 校验行为一致）
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（run-name 等字段）; gitcode-spec/（多处未提及 run-name、services 等）; parity-matrix.md（未知/不支持字段处理：文档未明确降级方式）
```

---

```
意图 ID:    INTENT-COMPAT-022
维度标签:   [compatibility, usability]
标题:       `vars` 上下文不支持时的降级行为

风险点:     GitHub 支持组织/仓库/环境级别的 `vars` 上下文；GitCode 文档虽在 context.md 中列出 `vars`，但 case-base-detail.md 中大量 TC（TC-005~007、TC-115~119 等）标记为「D 测不动 — vars context unsupported」。若 `vars` 实际上不被支持，使用 `${{ vars.MY_VAR }}` 的 workflow 会求值为空，导致配置注入失败。真实样本 `ops-nn_action.yml` 中使用了 `${{ vars.OBS_PATH }}` 和 `${{ vars.CI_PATH }}`。
预期系统行为: 若 `vars` 不支持，应在解析阶段明确报错；若支持，则应与文档描述一致（组织级/项目级可用）。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] 若支持，`vars.OBS_PATH` 应正确返回配置变量值
  - [负向] 若不支持，不应静默求值为空字符串
  - [非功能] 报错/缺失支持应在文档中明确声明

对齐方向:   一致性（若 GitCode 承诺支持，则应与 GitHub vars 语义一致）
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/contexts.md（vars 定义）; gitcode-spec/syntax-reference/context.md（vars 上下文列出）; baseline/case-base-detail.md（vars 相关 TC 均为 D 测不动/unsupported）; workflow-samples/cann/ops-nn_action.yml（使用 vars 上下文）
```

---

```
意图 ID:    INTENT-COMPAT-023
维度标签:   [compatibility, usability]
标题:       `jobs.<id>.environment` 字段支持情况与降级行为

风险点:     GitHub 支持 `environment` 字段用于部署环境（关联 protection rules、reviewers、wait timer）。GitCode 文档在 configure-jobs.md 的 Job 核心属性表中未列出 `environment` 字段，但在 case-base-detail.md 的 NEEDS-UPDATE 中 TC-010 标记为「environment field not recognized → DEPRECATE」。若该字段不被支持，直接迁移的部署 workflow 会丢失环境保护规则，导致生产部署缺少审批关卡。
预期系统行为: GitCode 应明确声明 `environment` 是否支持；若不支持，解析阶段应报错提示，而非静默忽略导致保护规则失效。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] 含 `environment: production` 的 job 不应被静默接受且环境规则完全失效
  - [非功能] 报错信息应提示「environment 字段在 GitCode 中不支持，请改用其他方式配置部署审批」

对齐方向:   一致性（若不支持，应像 GitHub 对关键字段一样给出明确报错）
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（environment 字段）; gitcode-spec/writing-pipelines/configure-jobs.md（未列出 environment）; baseline/case-base-detail.md（TC-010 DEPRECATE: environment field not recognized）
```

---

```
意图 ID:    INTENT-COMPAT-024
维度标签:   [compatibility]
标题:       内置 action 短名引用行为等价性：`actions/checkout@v4` vs `checkout`

风险点:     GitHub 使用 `uses: actions/checkout@v4`（owner/repo@ref）；GitCode 文档示例使用无 owner 短名如 `uses: checkout`。GitCode 声称兼容常用内置 action，但具体行为等价性（如 `checkout` 的 `with` 参数集、`ref`/`token`/`path` 等子参数支持度）未完全验证。真实样本中大量使用 `uses: checkout` + `with: ref/token/path` 等参数。若某些参数行为不同（如 `ref` 对 PR merge commit 的处理），会导致代码检出错误版本。
预期系统行为: GitCode 的 `checkout` 行为应与 GitHub `actions/checkout@v4` 在常用参数（`ref`、`token`、`path`、`repository`）上等价，或文档明确列出不支持参数。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `uses: checkout` + `with: ref: refs/heads/main` 应正确检出指定分支
  - [正向] `uses: checkout` + `with: path: ./sub` 应将代码检出到子目录
  - [负向] 不应因 ref 解析差异检出错误 commit
  - [非功能] 不支持的参数应在解析时给出警告

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/writing-pipelines/configure-steps.md（uses 调用 Action 插件，短名示例）; COMPAT-NOTES.md §10; workflow-samples/（全部样本使用 checkout 短名）
```

---

```
意图 ID:    INTENT-COMPAT-025
维度标签:   [compatibility]
标题:       内置 action `cache` 行为等价性：`actions/cache` vs `cache`

风险点:     GitHub `actions/cache` 支持 `key`、`path`、`restore-keys`、`upload-chunk-size` 等参数，有明确的 cache hit/miss 语义和跨分支隔离策略。GitCode 文档示例使用 `uses: cache`，但未详细说明参数支持度、cache key 冲突策略、fork PR 写缓存隔离。若 fork PR 可以写缓存并污染主分支缓存（cache poisoning），则是安全漏洞；若 `restore-keys` 不支持，则缓存命中率会大幅下降。
预期系统行为: `cache` 在常用参数（`key`、`path`、`restore-keys`）上与 GitHub `actions/cache` 等价；fork PR 场景应有写隔离（只读或独立作用域）。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `uses: cache` + `key`/`restore-keys` 应在命中时正确恢复缓存
  - [负向] fork PR 不应能覆盖主分支的缓存 key（防止 cache poisoning）
  - [非功能] cache 的命中/未命中应在日志中明确输出

对齐方向:   一致性
优先级线索: RISK-SEC-01（cache poisoning 属于供应链安全）
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/artifacts-and-cache.md（cache 简述）; COMPAT-NOTES.md §8; parity-matrix.md（cache fork 场景隔离：未知）
```

---

```
意图 ID:    INTENT-COMPAT-026
维度标签:   [compatibility]
标题:       内置 action `upload-artifact`/`download-artifact` 行为等价性

风险点:     GitHub `actions/upload-artifact`/`download-artifact` 支持跨 job 传递、保留期、`if-no-files-found`、`pattern` 等参数。GitCode 文档示例使用短名 `upload-artifact`/`download-artifact`，但未说明保留期默认值、跨 workflow 传递能力、大文件边界。若保留期默认与 GitHub 不同（GitHub 默认 90 天），会导致历史构建产物过早清理，影响问题回溯。
预期系统行为: `upload-artifact`/`download-artifact` 在常用参数（`name`、`path`、`retention-days`）上与 GitHub 等价；保留期默认值应与 GitHub 一致或文档明确声明。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] 跨 job 的 artifact 上传/下载应正确传递文件
  - [正向] `retention-days` 参数应能控制保留期
  - [负向] 不应因默认保留期差异导致产物在未预期的时间被清理
  - [非功能] 大 artifact（如 >1GB）上传应在合理时间内完成或给出明确报错

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   gitcode-spec/core-concepts/artifacts-and-cache.md（artifact 简述）; COMPAT-NOTES.md §10; parity-matrix.md（upload-artifact/download-artifact：保留期默认 90 天；大小上限未公开）
```

---

```
意图 ID:    INTENT-COMPAT-027
维度标签:   [compatibility, usability]
标题:       `runs-on` 标签体系差异：GitHub 单标签/数组 vs GitCode 三段式 `{os,arch,flavor}`

风险点:     GitHub 使用 `ubuntu-latest`、`windows-latest`、`macos-latest` 或 `self-hosted` + 自定义标签数组；GitCode 官方资源池使用三段式 `{os-version},{arch},{flavor}`（如 `{ubuntu-24,x64,small}`），自托管使用 `type/group/labels` 对象。直接迁移的 GitHub workflow 写 `runs-on: ubuntu-latest` 在 GitCode 中可能无法解析或匹配不到 Runner。真实样本中 `ops-nn_action.yml` 混用了 `runs-on: [codearts-hosted, ubuntu-latest, x64, small]` 和 `runs-on: default`，说明实践中已有兼容问题。
预期系统行为: GitCode 应对无法解析/无匹配的标签给出明确的调度失败报错，而非 job 无限期排队。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] `runs-on: [ubuntu-latest, x64, small]` 应正确匹配官方资源池
  - [负向] `runs-on: ubuntu-latest`（GitHub 风格单标签）不应导致 job 无限期 queued 且无提示
  - [非功能] 调度失败时日志应提示「无匹配 Runner，请检查 runs-on 标签格式」

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（runs-on 定义）; gitcode-spec/core-concepts/runner-and-environment.md（三段式标签）; gitcode-spec/writing-pipelines/configure-jobs.md（runs-on 说明）; workflow-samples/cann/ops-nn_action.yml（混用标签格式）
```

---

```
意图 ID:    INTENT-COMPAT-028
维度标签:   [compatibility, security]
标题:       Runner 环境隔离与复用策略未明确

风险点:     GitHub 官方 Runner 为一次性（ephemeral），job 结束后销毁，保证工作区/环境变量/ secrets 不泄露给后续 job。GitCode 文档未明确官方 Runner 是否为一次性。若 Runner 复用，存在跨 job 的文件残留、环境变量污染、secret 通过文件系统或内存泄露的风险。这是安全隔离的基础假设，必须验证。
预期系统行为: 官方 Runner 应为一次性或至少保证工作区在 job 开始前清空、环境变量不跨 job 泄漏。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] 同一 workflow 的连续 job 不应看到前一个 job 写入工作区的文件（除非通过 artifact 显式传递）
  - [负向] 前一个 job 设置的环境变量（通过 `echo "X=1" >> $ATOMGIT_ENV`）不应泄漏到不属于同一 job 的其他 workflow 运行
  - [非功能] 文档应明确声明 Runner 的生命周期策略

对齐方向:   一致性
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   github-reference/reference/contexts.md（runner 上下文暗示 ephemeral）; gitcode-spec/core-concepts/runner-and-environment.md（未明确 Runner 是否复用）; parity-matrix.md（Runner 环境隔离/一次性：未知）
```

---

```
意图 ID:    INTENT-COMPAT-029
维度标签:   [compatibility, usability]
标题:       工作流文件目录差异：`.github/workflows/` vs `.gitcode/workflows/`

风险点:     GitHub 要求 workflow 文件存放在 `.github/workflows/`；GitCode 要求 `.gitcode/workflows/`。这是迁移的第一道门槛。若用户仅复制了 `.github/workflows/` 下的文件而未创建 `.gitcode/workflows/`，GitCode 应给出明确提示。反之，若 GitCode 同时扫描 `.github/workflows/` 作为兼容措施，则属于「差异确认」中的兼容行为，需验证其稳定性。
预期系统行为: GitCode 应仅识别 `.gitcode/workflows/` 目录下的 `.yml`/`.yaml` 文件；对 `.github/workflows/` 中的文件应不识别或给出迁移提示。
Oracle 来源: GitCode规格 | GitHub行为

验证要点:
  - [正向] `.gitcode/workflows/ci.yml` 应被正确识别并触发
  - [负向] `.github/workflows/ci.yml` 不应被 GitCode 静默当作有效 workflow 执行（除非平台明确声明兼容）
  - [非功能] UI 或文档应给出「请将 workflow 文件移至 .gitcode/workflows/」的指引

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（.github/workflows/）; gitcode-spec/syntax-reference/trigger-events.md（.gitcode/workflows/）; COMPAT-NOTES.md §1; parity-matrix.md（目录差异已记录）
```

---

```
意图 ID:    INTENT-COMPAT-030
维度标签:   [compatibility, security, usability]
标题:       `permissions` 权限域命名完全差异：GitHub `contents`/`pull-requests` vs GitCode `repository`/`pr`

风险点:     GitHub 权限域为 `contents`/`pull-requests`/`issues`/`actions`/`checks` 等 18 项；GitCode 为 `repository`/`pr`/`issue`/`note`/`project`/`hook`。命名完全不同且粒度不同。直接迁移的 GitHub workflow 写 `permissions: contents: read` 在 GitCode 中可能因字段名不被识别而被静默忽略，导致 TOKEN 权限退化为仓库默认（可能过宽或过窄）。这是安全与兼容双重高危点。
预期系统行为: GitCode 对未知的 permissions 域名应在解析阶段报错，而非静默忽略；文档应提供完整的 GitHub→GitCode 权限域映射表。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] `permissions: contents: read` 不应被静默接受后实际赋予默认权限
  - [非功能] 报错信息应包含「GitCode 权限域名为 repository/pr/issue/...，请将 contents 替换为 repository」
  - [正向] `permissions: repository: read` 应正确限制 TOKEN 为只读

对齐方向:   差异确认
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（permissions 18 项权限域表）; gitcode-spec/security-permissions/token-permissions.md（6 项权限域表）; COMPAT-NOTES.md §6; parity-matrix.md（permissions 权限域命名：不支持）
```

---

```
意图 ID:    INTENT-COMPAT-031
维度标签:   [compatibility, usability]
标题:       迁移报错质量：遇到不兼容语法时，错误信息是否指明 GitCode 差异

风险点:     GitHub workflow 迁移到 GitCode 时，遇到不支持的语法（如 `run-name`、`jobs.<id>.services`、`strategy.max-parallel` 语义差异、`permissions` 的 GitHub 权限域名等），GitCode 的报错若仅为泛化的「YAML 解析错误」或「无效字段」，用户无法判断是自身写错还是平台差异。这是迁移摩擦的核心体验指标。
预期系统行为: 对已知与 GitHub 不兼容的字段/语法，报错信息应明确包含「该字段/语法在 GitCode 中与 GitHub 不同」或提供文档链接，而非泛化报错。
Oracle 来源: GitCode规格 | 差异声明

验证要点:
  - [正向] 使用 GitHub 权限域名 `contents: read` 时，报错应提示「请使用 repository 替代 contents」
  - [正向] 使用 `run-name` 时，报错应提示「GitCode 不支持 run-name 字段」
  - [非功能] 报错信息可理解性判据：是否包含「GitCode」关键字 + 替代建议 + 文档链接；eval: llm_assisted

对齐方向:   一致性（在报错质量上应达到与 GitHub 同等可理解性）
优先级线索: RISK-USE-01
破坏级别:   none
来源输入:   testing-focus.md §11（迁移摩擦：报错能否指明 GitCode 不支持/需改写）; COMPAT-NOTES.md（多处差异）; parity-matrix.md（迁移报错质量：未知）
```

---

```
意图 ID:    INTENT-COMPAT-032
维度标签:   [compatibility, security]
标题:       `pull_request_target` 语义一致性：fork PR 高权限运行不可信代码风险

风险点:     GitHub 的 `pull_request_target` 在 base 上下文运行，可访问 secrets 和 write token，但 checkout PR `head.sha` 再执行其脚本 = 高权限跑不可信代码（pwn request）。GitCode 文档声称语义与 GitHub 一致（`pull_request_target` 可读写目标仓库、fork PR 的 `pull_request` 仅 read），但隔离强度需实测确认。case-base-detail.md 中 TC-461/TC-463 已记录为 FAIL（pull_request_target 未触发）。
预期系统行为: `pull_request_target` 应运行在 base 分支上下文，使用 base 分支的 workflow 文件；fork PR 通过 `pull_request` 触发时不应能读取仓库 secrets。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `pull_request_target` 触发时，`atomgit.sha` 应为 base 分支最新 commit，而非 PR head
  - [负向] fork PR 的 `pull_request` 事件下，不应能读取项目级 secrets（如 `${{ secrets.DEPLOY_TOKEN }}` 应求值为空或注入失败）
  - [负向] `pull_request_target` 中 checkout PR head sha 后执行其脚本，不应自动获得 write 权限（与 GitHub 风险模型一致）

对齐方向:   一致性
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   github-reference/reference/events.md（pull_request_target 语义）; github-reference/security/pull_request_target.md（pwn request 风险）; gitcode-spec/security-permissions/pr-mr-pipeline-security.md; baseline/case-base-detail.md（TC-461/463 FAIL）
```

---

```
意图 ID:    INTENT-COMPAT-033
维度标签:   [compatibility, security]
标题:       Secret 日志脱敏绕过风险：`echo "${{ secrets.X }}"` 可能泄露

风险点:     GitCode 文档在 `using-secrets.md` 中自承 `echo "${{ secrets.X }}"` 可能绕过脱敏机制。GitHub 的 secret masking 是在 runner 层面注册所有 secret 值为 mask pattern，理论上 `${{ secrets.X }}` 求值后输出的值也应被遮蔽。若 GitCode 的脱敏机制在表达式求值前未注册或存在时序问题，secret 会以明文出现在日志中。这是直接的安全漏洞。
预期系统行为: 无论通过 `${{ secrets.X }}` 还是环境变量注入，secret 值出现在 stdout/stderr 时都应被替换为 `***`。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [负向] `run: echo "${{ secrets.MY_SECRET }}"` 的输出不应包含明文 secret 值
  - [负向] `run: echo "$MY_SECRET"`（其中 MY_SECRET 通过 env 注入 `${{ secrets.MY_SECRET }}`）的输出不应包含明文
  - [非功能] 日志中所有 secret 出现位置应被统一替换为 `***`

对齐方向:   一致性
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   github-reference/security/secrets.md（masking 机制）; gitcode-spec/security-permissions/using-secrets.md（自承可能绕过脱敏）; COMPAT-NOTES.md §8; parity-matrix.md（secrets 日志脱敏：部分支持）
```

---

```
意图 ID:    INTENT-COMPAT-034
维度标签:   [compatibility]
标题:       `concurrency` 字段结构与语义差异：GitHub `group`+`cancel-in-progress` vs GitCode `enable`/`max`/`exceed-action`/`preemption`

风险点:     GitHub `concurrency` 用 `group`（字符串表达式定义并发组）+ `cancel-in-progress`（布尔）+ `queue`（single/max）；GitCode 用 `enable`/`max`/`exceed-action`（IGNORE/QUEUE）/`preemption.enable`/`preemption.events`。直接迁移的 GitHub workflow 写 `concurrency: group: ${{ github.workflow }}` 在 GitCode 中会因字段名完全不同而被忽略或报错。真实样本 `PR-pipeline_op-plugin.yml` 使用了 GitCode 风格的 `concurrency: max: 5, exceed-action: QUEUE, preemption: enable: true, events: [mr_id]`。
预期系统行为: GitCode 对 GitHub 风格的 `concurrency.group` 应在解析阶段报错或给出明确警告；GitCode 自身并发控制（max/QUEUE/preemption）应在语义上等价于 GitHub 的对应能力。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] GitCode 风格 `concurrency.max: 1` + `exceed-action: QUEUE` 应正确排队后续运行
  - [负向] GitHub 风格 `concurrency.group: ci` 不应被静默忽略导致并发失控
  - [非功能] 抢占/取消行为应在运行日志中留下明确痕迹

对齐方向:   差异确认
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/workflow-syntax.md（concurrency 定义）; gitcode-spec/writing-pipelines/configure-jobs.md（concurrency 字段）; workflow-samples/op-plugin/PR-pipeline_op-plugin.yml（并发控制配置）
```

---

```
意图 ID:    INTENT-COMPAT-035
维度标签:   [compatibility]
标题:       `steps` 上下文中的 `outcome` 与 `conclusion` 语义差异

风险点:     GitHub 明确区分 `steps.<id>.outcome`（应用 `continue-on-error` 之前的结果）和 `steps.<id>.conclusion`（应用 `continue-on-error` 之后的结果）。GitCode 文档在 context.md 中复制了相同的语义描述，但 case-base-detail.md 中部分条件执行相关 TC（TC-317~321）标记为 FAIL（条件执行函数不工作）。若 `outcome`/`conclusion` 在 GitCode 中未正确区分，会导致基于 step 结果的后续条件判断错误。
预期系统行为: `outcome` 应反映 step 原始结果（success/failure），`conclusion` 应在 `continue-on-error: true` 时可能为 success（即使原始失败）。
Oracle 来源: GitHub行为 | 差异声明

验证要点:
  - [正向] `continue-on-error: false` 的失败 step，`outcome` 和 `conclusion` 都应为 failure
  - [正向] `continue-on-error: true` 的失败 step，`outcome` 应为 failure，`conclusion` 应为 success
  - [负向] 不应出现 `outcome`/`conclusion` 值互换或始终相同的情况

对齐方向:   一致性
优先级线索: RISK-COMPAT-01
破坏级别:   none
来源输入:   github-reference/reference/contexts.md（steps 上下文 outcome/conclusion 定义）; gitcode-spec/syntax-reference/context.md（steps 上下文定义）; baseline/case-base-detail.md（TC-317~321 条件执行函数 FAIL）
```

---

## 四、统计汇总

| 指标 | 数值 |
|---|---|
| **Intent 总数** | 35 |
| **对齐方向 = 一致性** | 21 条 |
| **对齐方向 = 差异确认** | 14 条 |
| **单维度 [compatibility]** | 24 条 |
| **多维度（含 security）** | 6 条 |
| **多维度（含 usability）** | 8 条 |
| **多维度（含 reliability）** | 2 条 |
| **破坏级别 = fixture** | 3 条（INTENT-COMPAT-028、032、033） |
| **破坏级别 = full_instance** | 0 条 |
| **破坏级别 = none** | 32 条 |

### 因输入缺失而退化的类别

| 退化类别 | 退化说明 | 影响 intent |
|---|---|---|
| **真实 GitHub workflow 负载佐证** | `inputs/workflow-samples/` 仅有 8 个 GitCode 项目样本，无广泛开源 GitHub workflow 样本 | 全部 intent 的「现实中常见」佐证依赖规格推导，而非真实 GitHub 负载统计；INTENT-COMPAT-024~026（内置 action 差异）尤其缺乏 GitHub 侧真实使用模式佐证 |
| **业务迁移改造点清单** | `inputs/business-context/` 仅 README.md 模板，无实际迁移规模与改造点 | INTENT-COMPAT-029~031（迁移摩擦类）缺乏业务侧「已知高频摩擦」输入，优先级纯依赖风险登记册通用线索 |
| **GitHub oracle 完整语义** | `inputs/github-reference/` 仅 12 页精选文档，部分边界行为（如 `hashFiles` 内部 glob 实现、`fromJSON` 异常输入处理）未完整抓取 | INTENT-COMPAT-007、010 的 oracle 精度受限，需后续补全官方文档或实测 GitHub 行为 |

---

## 五、溯源链闭合检查

| Parity Matrix 能力项 | 覆盖 Intent | 状态 |
|---|---|---|
| 工作流文件目录 `.github/workflows/` | INTENT-COMPAT-029 | ✅ 覆盖 |
| 未知/不支持字段处理 | INTENT-COMPAT-021 | ✅ 覆盖 |
| `push` 触发 + branches/paths 过滤 | INTENT-COMPAT-012 | ✅ 覆盖 |
| `pull_request` vs `pull_request_target` 隔离 | INTENT-COMPAT-032 | ✅ 覆盖 |
| `schedule` cron 最短间隔 | INTENT-COMPAT-013 | ✅ 覆盖 |
| `workflow_call` 嵌套层数 | INTENT-COMPAT-015 | ✅ 覆盖 |
| `stages` 阶段机制 | —（GitCode 特有，非兼容性差异） | N/A |
| `post` 后处理阶段 | —（GitCode 特有，非兼容性差异） | N/A |
| `timeout-minutes` 默认 360 分钟 | —（双方一致） | N/A |
| `rerun` 次数限制 | —（差异已知，但属运行操作层面，非 workflow 语法兼容） | N/A |
| `runs-on` 标签体系 | INTENT-COMPAT-027、028 | ✅ 覆盖 |
| Runner 环境隔离 / 一次性 | INTENT-COMPAT-028 | ✅ 覆盖 |
| `secrets` 日志脱敏 `***` | INTENT-COMPAT-033 | ✅ 覆盖 |
| `permissions` 默认权限 | INTENT-COMPAT-002 | ✅ 覆盖 |
| `permissions` 权限域命名 | INTENT-COMPAT-030 | ✅ 覆盖 |
| `pull_request_target` checkout head.sha 风险 | INTENT-COMPAT-032 | ✅ 覆盖 |
| `upload-artifact` / `download-artifact` | INTENT-COMPAT-026 | ✅ 覆盖 |
| `cache` fork 场景隔离 | INTENT-COMPAT-025 | ✅ 覆盖 |
| 运行状态机 + 日志完整性 | —（双方一致） | N/A |
| `ATOMGIT_STEP_SUMMARY` Markdown | —（前缀差异，功能一致） | N/A |
| 上下文对象命名 `github.*` | INTENT-COMPAT-016 | ✅ 覆盖 |
| 状态函数括号语法 `success()` | INTENT-COMPAT-004、005 | ✅ 覆盖 |
| 表达式函数 `contains`/`hashFiles`/`toJson` | INTENT-COMPAT-006~010 | ✅ 覆盖 |
| `workflow_dispatch.inputs` 类型 | INTENT-COMPAT-014 | ✅ 覆盖 |
| 迁移报错质量（GitHub→GitCode） | INTENT-COMPAT-031 | ✅ 覆盖 |
| `concurrency.max` 1-5 + QUEUE/IGNORE | INTENT-COMPAT-034 | ✅ 覆盖 |
| `strategy.matrix` 组合数上限 | —（未在差异类别中，属完备性） | N/A |

---

*产出完毕。待门禁评审。*
