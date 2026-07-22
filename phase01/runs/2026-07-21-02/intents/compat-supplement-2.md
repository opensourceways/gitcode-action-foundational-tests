# 兼容性 Diff 补充产出 2 · BLIND-03 matrix include/exclude + BLIND-09 表达式函数边界

> 产出 Agent：compat-diff（差异猎手）
> Run：2026-07-21-02（增量更新，不修改历史结论）
> 目标盲区：BLIND-03 `C-EXEC-15~20 matrix include/exclude 正确性`、BLIND-09 `C-EXPR-04 表达式函数边界`
> 背景：
>   - BLIND-03：仅 REL-010（组合数上限探测）覆盖，matrix 展开正确性 / include 追加 / exclude 排除 / 动态 runs-on 的功能验证无独立 compatibility intent；基底 TC-325-328 覆盖 completeness 但本轮兼容差异未挖。
>   - BLIND-09：COMPAT-010/012/013 覆盖部分函数集与类型强转，但 format 参数边界、substring/replace/toJson 独立边界行为无 compatibility 层 intent。
> 接续规则：本文件 intent ID 从 INTENT-COMPAT-065 起，接续 compat-supplement.md 已有的 COMPAT-064。

---

```
意图 ID:    INTENT-COMPAT-065
维度标签:   [compatibility, completeness]
标题:       matrix include/exclude 展开语义与动态 runs-on 兼容性——追加变量、排除组合、新组合创建是否与 GitHub 一致

具体差异点:   matrix `include` 追加新变量/创建新组合、`exclude` 精确排除组合、以及 `runs-on` 动态引用 matrix 变量的展开语义。
GitHub 侧预期行为:
  - `include` 可向现有矩阵追加特定组合，或为已有组合添加额外变量；include 中未在基础矩阵定义的变量会被注入对应 job 实例。
  - `include` 可定义完全不在基础矩阵中的新组合（不依赖基础变量值），生成额外 job 实例。
  - `exclude` 为精确匹配：所有指定字段均匹配的组合才被排除；部分字段匹配不触发排除。
  - `runs-on` 可引用 `${{ matrix.os }}` 等变量动态选择 runner，单标签或数组均可。
GitCode 侧疑似行为:
  - spec/文档声明 include/exclude 语义与 GitHub 方向一致（追加/排除），但以下边界未声明：
    (a) include 能否创建完全脱离基础矩阵的新组合；
    (b) include 额外变量与基础矩阵变量同名时是覆盖还是报错；
    (c) exclude 是精确匹配还是子集匹配；
    (d) `runs-on: ${{ matrix.os }},${{ matrix.arch }},small` 为字符串拼接式（逗号分隔），与 GitHub 数组式/单标签式的解析差异。
  - 真实样本大量使用动态 runs-on（`runs-on: ${{ matrix.os }},${{ matrix.arch }},small`），但 GitCode 三段式标签体系使动态引用结果与 GitHub 单标签语义不同。
风险点:     迁移含复杂 matrix（如 op-plugin 多版本构建、cann 多架构）的 workflow 时：
  - include 若不能创建新组合，迁移的「补充实验平台」矩阵实例会静默丢失；
  - exclude 若为子集匹配而非精确匹配，会过度排除导致合法组合不运行；
  - runs-on 动态引用在三段式下的解析若与 GitHub 不同，matrix 展开后可能排不到 runner 或分配到错误规格。
预期系统行为:
  - include/exclude 展开结果（生成多少 job 实例、各实例变量集）与 GitHub 一致；
  - 动态 runs-on 引用 matrix 变量后，能正确映射到 GitCode runner 标签体系，或至少给出明确报错。
Oracle 来源: GitHub行为（workflow-syntax.md:169-170；矩阵展开语义）+ GitCode声明（configure-matrix-builds.md）
对齐方向:   一致性（include/exclude 展开语义应与 GitHub 一致；不一致即缺陷+缺口）+ 差异确认（runs-on 动态引用在三段式下的行为需坐实）

验证要点:
  - [正向] 基础矩阵 2×2=4 实例，include 追加 1 个新组合（含基础矩阵外的新变量）后共 5 实例，且新变量正确注入。
  - [正向] exclude 精确排除 1 个组合后剩余 3 实例，非目标组合不被误排除。
  - [正向] `runs-on: ${{ matrix.os }},${{ matrix.arch }},small` 正确调度到预期 runner。
  - [负向] include 不应因「新组合不含基础变量」而被静默忽略导致实例丢失。
  - [负向] exclude 不应因「子集匹配」而过度排除未声明的组合。
  - [负向] 动态 runs-on 解析失败时不应静默挂起无报错。

触发条件:   提交含基础矩阵 + include（含新变量/新组合）+ exclude + 动态 runs-on 的 workflow，观察生成的 job 实例数、各实例变量值、调度结果。
优先级线索: 关联 BLIND-03 中严重度 + testing-focus §3 matrix + §10 编排差异；建议 P1。关联 spec C-EXEC-15~C-EXEC-20、TC-325-328。
来源输入:   github-reference/reference/workflow-syntax.md:169-170；gitcode-spec/writing-pipelines/configure-matrix-builds.md；baseline/case-base-detail.md（TC-325~328）；coverage.md BLIND-03
```

```
意图 ID:    INTENT-COMPAT-066
维度标签:   [compatibility]
标题:       表达式函数 format 边界行为——参数不足/过剩、转义、非字符串参数处理是否与 GitHub 一致

具体差异点:   `format(template, args...)` 在占位符与参数个数不匹配、双花括号转义、非字符串参数传入时的边界行为。
GitHub 侧预期行为:
  - `format('Hello {0} {1}', 'A')`：参数不足时，`{1}` 原样保留（输出 `Hello A {1}`）——不报错。
  - `format('Hello {0}', 'A', 'B')`：参数过剩时，多余参数被忽略（输出 `Hello A`）。
  - `format('{{ {0} }}', 'A')`：双花括号转义为单花括号（输出 `{ A }`）。
  - 非字符串参数（数字/null/布尔）会被隐式转字符串后插入；对象/数组不可转字符串，可能报错或输出 `[object Object]` 类字符串。
  - 无最大参数数限制，但至少需要一个 replaceValue。
GitCode 侧疑似行为:
  - spec C-EXPR-04 / expressions.md 声明 `format(template, args...)` 使用 `{0}`、`{1}` ... 占位符依次替换，但以下边界未声明：
    (a) 参数个数 < 占位符个数时行为；
    (b) 参数个数 > 占位符个数时行为；
    (c) 双花括号转义是否支持；
    (d) 非字符串（数字、null、布尔、对象、数组）参数的处理方式。
  - 历史基底 TC-183 覆盖「format 拼接字符串」基本功能，TC-536~538 为字面量边界，均未触及 format 函数本身的参数边界。
风险点:     迁移 workflow 中 `format('v{0}.{1}', matrix.major)`（参数不足）或 `format('{0}', val, fallback)`（参数过剩）在 GitHub 有确定行为；若 GitCode 行为不同（如参数不足报错、参数过剩不忽略），则条件拼接/标签生成等逻辑会静默断裂。双花括号转义用于生成 JSON/helm 模板等场景，缺失则迁移直接失败。
预期系统行为: format 边界行为（参数不足原样保留、参数过剩忽略、双花括号转义、非字符串隐式转字符串）与 GitHub 一致。
Oracle 来源: GitHub行为（expressions.md:105-111）
对齐方向:   一致性（GitCode 未声明差异，应与 GitHub format 边界语义对齐；不一致即缺陷+缺口）

验证要点:
  - [正向] `format('A{0}B{1}C', 'x', 'y')` 输出 `AxByC`（正常替换）。
  - [正向] `format('{{ {0} }}', 'x')` 输出 `{ x }`（转义生效）。
  - [负向] `format('A{0}B{1}C', 'x')` 不应报错，应输出 `AxB{1}C`（参数不足原样保留）。
  - [负向] `format('A{0}B', 'x', 'y')` 不应因参数过剩而报错，应输出 `AxB`（多余参数忽略）。
  - [非功能] 非字符串参数（数字 42、null、true）应被转字符串插入，不导致表达式解析失败。

触发条件:   在 step env/run 中使用上述 5 种 format 边界表达式，echo 结果比对。
优先级线索: 关联 BLIND-09 中严重度 + testing-focus §10 表达式函数差异；建议 P1。关联 spec C-EXPR-04、TC-183、TC-547。
来源输入:   github-reference/reference/expressions.md:105-111；gitcode-spec/syntax-reference/expressions.md；gitcode-spec/COMPAT-NOTES.md §3；baseline/case-base-detail.md（TC-183）
```

```
意图 ID:    INTENT-COMPAT-067
维度标签:   [compatibility]
标题:       表达式函数 substring/replace/toJson 边界行为——越界、全局/首匹配、JSON 输出格式是否与 GitHub 对齐

具体差异点:   GitCode 特有 `substring`/`replace` 与 GitHub 也有但命名大小写不同的 `toJson`（GitHub 为 `toJSON`）的边界行为。
GitHub 侧预期行为:
  - `toJSON(value)`：返回 pretty-print JSON 字符串（含换行与缩进）；null 返回 `null`；对象属性顺序不确定（实现依赖）；数组按原序；布尔转 `true`/`false`。
  - **无 `substring`/`replace` 内置函数**——GitHub Actions 未提供这两个函数，迁移 workflow 若用到需在 step 中通过 shell 实现。
GitCode 侧疑似行为:
  - `substring(str, start, len)`：spec 仅声明「截取子字符串」，未声明 start 超界、len 超界、start 为负、len 为 0/负数时的行为。
  - `replace(str, old, new)`：spec 仅声明「替换字符串」，未声明是全局替换还是仅替换首个匹配；未声明 old 为空串时的行为。
  - `toJson(value)`：spec 声明「将对象序列化为 JSON 字符串」，但 pretty-print 格式（缩进/换行）、属性排序、null 处理、循环引用保护等边界未声明；命名大小写与 GitHub `toJSON` 不同（COMPAT-010 已标）。
  - 历史基底 TC-184/185/187 覆盖基本功能，TC-547/548 为 substring/replace 字面量边界，均未从 compatibility 层与 GitHub 对齐或确认 GitCode 特有边界。
风险点:     
  - `substring(github.sha, 0, 7)` 若越界行为与常见编程语言不同（如报错而非截断），commit short SHA 生成会失败。
  - `replace(ref, 'refs/heads/', '')` 若为全局替换但用户预期仅首匹配，或反之，则分支名处理逻辑错误。
  - `toJson` 输出格式若与 GitHub `toJSON` 不同（如无 pretty-print、属性排序差异），则下游「按行解析 JSON」或「hash 比对」的逻辑会静默失败。命名大小写差异（COMPAT-010）已标，此处聚焦行为边界。
预期系统行为:
  - substring 越界时安全截断（不报错），负 start/len 有确定处理。
  - replace 行为文档明确（全局或首个），空串 old 有确定处理。
  - toJson 输出为 pretty-print JSON，语义与 GitHub toJSON 一致（大小写命名差异除外）。
Oracle 来源: GitHub行为（expressions.md:119-121 toJSON）+ GitCode声明（expressions.md substring/replace/toJson）
对齐方向:   差异确认（substring/replace 为 GitCode 特有函数，坐实边界行为并回填文档）+ 一致性（toJson 序列化语义应与 GitHub toJSON 对齐）

验证要点:
  - [正向] `substring('hello', 0, 7)` 输出 `hello`（越界安全截断）。
  - [正向] `replace('aaa', 'a', 'b')` 行为被明确记录（全局 `bbb` 或首个 `baa`）。
  - [正向] `toJson(atomgit.event)` 输出为 pretty-print、合法 JSON，可被标准 JSON 解析器消费。
  - [负向] `substring('hello', 0, 7)` 不应报错导致表达式解析失败。
  - [负向] `replace('a/a', '/', '-')` 若文档未声明全局/首个，实测结果应被记录为权威行为。
  - [非功能] substring/replace 边界行为（越界、空 old、负索引）应文档化，消除「生产用但无规格」的黑盒状态。

触发条件:   在 step env/run 中分别测试：
  (a) `substring('hello', 0, 7)` / `substring('hello', 10, 3)` / `substring('hello', -1, 2)`；
  (b) `replace('aaa', 'a', 'b')` / `replace('a/a', '/', '-')` / `replace('abc', '', 'x')`；
  (c) `toJson(atomgit.event)` / `toJson(null)` / `toJson(true)`，比对输出格式与 GitHub toJSON。
优先级线索: 关联 BLIND-09 中严重度 + testing-focus §10 表达式函数差异；建议 P1。关联 spec C-EXPR-04、COMPAT-010、TC-184/185/187/547/548。
来源输入:   github-reference/reference/expressions.md:119-121；gitcode-spec/syntax-reference/expressions.md；gitcode-spec/COMPAT-NOTES.md §3；baseline/case-base-detail.md（TC-184/185/187/547/548）
```

---

## 补充说明

- **接续规则**：本文件 intent ID 从 INTENT-COMPAT-065 起，接续 compat-supplement.md 已有的 COMPAT-064。
- **历史复用**：
  - matrix 基础功能：TC-325（matrix单变量）、TC-326（matrix多变量）、TC-327（matrix include）、TC-328（matrix exclude）已在 completeness 维度覆盖基本语法；COMPAT-003（fail-fast 默认值）、COMPAT-028（strategy 上下文）已覆盖矩阵周边。本补充 intent **不重复基础语法验证**，聚焦「展开语义与 GitHub 对齐」这一 compatibility 盲区。
  - 表达式函数基础：TC-183（format）、TC-184（substring）、TC-185（replace）、TC-187（toJson）及边界 TC-547/548 已在 completeness 维度覆盖。本补充 intent **不重复基本功能验证**，聚焦「参数边界、越界、全局/首匹配、JSON 格式」等 compatibility 层差异。
- **跨维标签**：COMPAT-065 标 `[compatibility, completeness]`——因 matrix 展开正确性同时影响 compatibility 与 completeness；COMPAT-066/067 标 `[compatibility]`。
- **优先级建议**：三条均建议 P1（BLIND-03/09 中严重度）。若实测发现与 GitHub 行为不一致且影响迁移，应按 gate-log §2 标准升 P0。
- **与已有 intent 关系**：
  - 与 COMPAT-003（fail-fast 默认值）：不重复，COMPAT-003 聚焦 fail-fast 默认值，本文件聚焦 include/exclude 展开。
  - 与 COMPAT-010（缺失表达式函数）：不重复，COMPAT-010 聚焦函数集差异（join/fromJSON/case 缺失），本文件聚焦已有函数边界。
  - 与 COMPAT-012（类型强转）：不重复，COMPAT-012 聚焦 `==`/关系运算的隐式类型转换，本文件聚焦 format/substring/replace/toJson 的函数级边界。
- **纪律遵守**：
  - 不修改已有 compat.md / compat-supplement.md。
  - 不臆断差异——所有 GitCode 未声明边界均标「疑似」，验证方法在触发条件与验证要点中交代清楚。
  - 不写 GitCode 具体语法落地，停在意图层。

*产出时间: 2026-07-21*
*基于 coverage.md BLIND-03/09 + compat.md COMPAT-003/010/012/028 + compat-supplement.md COMPAT-062~064 + github-reference/ + gitcode-spec/ + baseline/case-base-detail.md 生成*
