# Case Writer 编译校验规则

> case-writer agent 生成 YAML 时必须逐条遵守。本文件整合了 schema 校验 + GitCode 平台实测验证规则（来源：demo 仓库 `AGENTS.md`）。
> 遵守此规则可一次通过 `/phase02-schema-check` 和平台 YAML 校验。

---

## 1. Runner 标签格式 ★ [平台实测]

**只用数组格式，禁止 `{}` 对象格式。**

```yaml
# ✅ 正确 — 数组格式（demo 仓库实测可用）
runs-on: [ubuntu-latest, x64, small]
runs-on: [self-hosted, arch=arm]
runs-on: [self-hosted, arch=arm, group=006]   # K8s 自托管 runner（group=006）
runs-on: ['codearts-hosted', 'ubuntu-latest', 'x64', 'large']

# ❌ 错误 — 对象格式被平台拒绝
runs-on: {ubuntu-24, x64, small}       # unknown property
runs-on: default                        # 不明确的标签
```

**匹配逻辑**：`runs-on` 中列出的所有标签必须同时存在于 Runner 的标签集合中。

### 1a. 默认 runs-on（非 runs-on 测试时）★

**如果当前用例不测 `runs-on` 行为，应使用ubuntu-latest，不用虚拟化 runner（ubuntu-latest），以节省执行时间：**

```yaml
# ✅ 默认 — 不测 runs-on 时首选

runs-on: [ubuntu-latest, x64, small]
runs-on: [ubuntu-latest, arm64, small]

# 仅在用例本身测试 runs-on 标签/runner 选择逻辑时才用
runs-on: [dedicate-hosted, x64, large]
runs-on: [dedicate-hosted, arm64, large]       # ARM 架构时
runs-on: [self-hosted, arch=arm, group=006]    # K8s self-hosted runner 用例
runs-on: [ubuntu-latest, x64, small]
runs-on: [self-hosted, arch=arm]
```

> dedicate-hosted 是物理宿主机，启动和构建速度远快于虚拟化 runner。测 runs-on 本身的行为时才需要用其他标签。

---

## 2. Job name 必填 ★ [平台实测]

每个 job 必须显式声明 `name`，平台报 `jobs[id].name: The value cannot be empty`。

```yaml
# ✅ 正确
jobs:
  hello:
    name: Print hello message       # ← 必填
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - name: Say hello
        run: echo "hello"

# ❌ 错误
jobs:
  hello:
    runs-on: [ubuntu-latest, x64, small]   # 缺 name
```

---

## 3. Step name 必填 + 非法字符清理 ★ [平台实测]

### 3a. 每个 step 必须有 `name`

包括 bare `uses:` step：

```yaml
# ❌ 错误
- uses: checkout

# ✅ 正确
- name: (TC) checkout source
  uses: checkout
```

### 3b. Step name 仅允许以下字符 [平台校验]

允许：中文、A-Z a-z 0-9、`-` `_` `,` `;` `:` `.` `/` `(` `)` `（` `）` 及空格；长度 1-128。

**禁止**：`[` `]` `|` `!` `>` `&` `#` `?` `*` `=` `<` `'` `"` `@` `$` `{` `}` `+`

```yaml
# ❌ 含 [ ] — 替换为 ( )
- name: "[TC-001] env(workflow级)"

# ✅
- name: "(TC-001) env workflow 级"
```

### 3c. `defaults.run` 下不能包含 `name`

`defaults.run` 仅支持 `shell:` 和 `working-directory:`。

---

## 4. `if:` 表达式：`${{ }}` 包裹 + `always()` 带括号 [平台实测 2026-07-21]

⚠️ **官方文档与平台部署的校验器不一致，以平台实测为准。** 官方 `configure-conditional-execution.md`
写裸关键字 `${{ always }}`，但 ComputingActionTest 仓库实测部署的校验器**拒绝**裸关键字，只认 `always()`（带括号）。

实测结果（pilot 3 版 push 的网页校验错误，API 把错误藏在 `message:null`，须看网页 UI）：

| 写法 | 平台校验结果 |
|---|---|
| `if: ${{ always() }}` | ✅ **接受**（目前唯一确认可用的状态函数） |
| `if: ${{ always }}`（文档写法·裸） | ❌ 拒绝：`表达式：always 第1位出现不支持的关键字` |
| `if: ${{ failed }}`（文档写法·裸） | ❌ 拒绝：`表达式：failed 第1位出现不支持的关键字` |
| `if: ${{ success() }}` | ❌ 拒绝：`表达式：success() 第1位出现不支持的函数` |
| `if: ${{ failure() }}`（GitHub 语法） | ❌ 拒绝：`表达式：failure() 第1位出现不支持的函数` |

### 4d. `failure()` vs `failed` — 命名差异 [官方文档 COMPAT-NOTES.md]

GitCode 与 GitHub Actions 对「失败」状态函数使用了**不同名称**：

| 平台 | 语法 | 是否带括号 |
|------|------|------------|
| **GitCode** | `${{ failed }}` | 无括号（keyword） |
| **GitHub** | `${{ failure() }}` | 带括号（function call） |

```yaml
# ❌ 错误 — GitHub 语法，平台拒绝
if: ${{ failure() }}

# ✅ 正确 — 唯一确认可用的状态函数
if: ${{ always() }}
```

> 来源：`COMPAT-NOTES.md` 明确注明 "GitCode 的失败函数名为 `failed`，GitHub 为 `failure()`"。
> 实测 `${{ failed }}`（无括号）也被平台拒绝（见上表），因此当前实际可用的状态函数仅有 `${{ always() }}`。

- ✅ **清理/兜底步骤**（无论成败都执行）用 `if: ${{ always() }}`。
- ⚠️ **success / failure 门控暂无确认可用写法**：文档的裸 `success`/`failed` 与 GitHub 的 `success()` 平台都拒。
  未实测确认前，**不要写状态门控**；需要条件时改用 `${{ atomgit.* }}` 显式表达式
  （如 `if: ${{ atomgit.ref == 'refs/heads/main' }}`）或 job 级 `needs`。
- ⚠️ 表达式函数 `startsWith()` / `contains()` / `endsWith()` 带括号——是否被平台接受同样待实测。

> 教训：曾据官方文档把本规则从 `always()` 改成裸 `always`，随后 pilot 实测证明平台拒绝裸关键字——
> **文档在此处是错的，平台校验器才是 ground truth。** 已改回 `always()`。

---

## 4b. `uses:` Action 引用格式 [官方文档 + 2026-07-23 更新]

### Step-level `uses:`（steps 内）— 仅支持插件/Action

| 类型 | 语法 | 例 |
|---|---|---|
| 官方插件 | **裸插件名** | `uses: checkout` / `uses: setup-node` / `uses: cache` |
| 开源插件 | `owner/repo[/path]@ref` | `uses: docker/build-push-action@v6` |
| 本仓 Action | `./path` | `uses: ./.gitcode/actions/my-action` |

- ❌ **禁止 `official_` 前缀**：GitCode 官方插件就是裸名。`official_checkout` 不是合法语法，应写 `checkout`。
- ❌ **禁止 GitHub 内置全名** `actions/checkout@v4` / `actions/setup-node@v4`——**除非**该用例本身在测 GitHub 格式是否报错（COMPAT 负向用例，须在 rubric 明示预期报错）。
- ❌ **step 级别不支持 `.yml` 工作流路径**：`uses: ./.gitcode/workflows/xxx.yml` 只能在 **job 级别**使用（`workflow_call` 复用），放在 step 级别会被验证器拒绝（`格式错误：pluginname@version`）。
- 已知官方内置插件名：`checkout` `setup-node` `setup-go` `setup-java` `setup-python` `cache` `upload-artifact` `download-artifact`。
- 云集成类插件（OBS/SWR/k8s/docker 登录等）exact 名称以 **GitCode 插件市场**为准；未确认前用 hyphen 命名（如 `obs-upload`）并登记 spec-gap，**勿臆造**。

### Job-level `uses:`（jobs 内）— 支持工作流复用

```yaml
# ✅ job 级别——复用另一个 workflow 文件
jobs:
  caller:
    uses: ./.gitcode/workflows/reusable.yml

# ❌ step 级别——不支持 .yml 文件
steps:
  - uses: ./.gitcode/workflows/reusable.yml   # 平台拒绝
```

---

## 5. Job steps 数量限制 ≤ 16 [平台限制]

超出 16 个 step 必须拆分 job（加 `-b`、`-c` 后缀）。

---

## 4c. 单行 `run:` 含冒号必须用 block scalar `|` [平台实测 2026-07-21]

GitCode 的 workflow 解析器对**单行 `run:` 值里的冒号**会误判为嵌套映射，即使值已用双引号包裹也报错：
`Nested mappings are not allowed in compact mappings`。

```yaml
# ❌ 单行 run 含冒号 → 平台报 Nested mappings 错误（双引号也救不了）
- name: demo
  run: echo "ALWAYS_OK: done"

# ✅ 用 block scalar |（多行）——已实测通过
- name: demo
  run: |
    echo "ALWAYS_OK: done"
```

规则：**所有 `run:` 一律写成 `run: |` block scalar**（哪怕只有一行）。这样冒号、引号、`$` 全部安全。
来源：pilot `pilot-format.yml` 实测（line 19 冒号触发该错误，改 block scalar 后消失）。

---

## 6. `on.push` 不能同时有 `paths` 和 `paths-ignore` [平台限制]

若同时存在，保留 `paths`，删除 `paths-ignore`。

---

## 7. `vars` 上下文不支持 [平台限制]

GitCode 平台不支持 `vars.*` 上下文。引用 `vars` 的用例标注 SKIP 或改用 `atomgit.*`。

---

## 8. `on:` 必须是 map，禁止数组格式 ★★★ [平台实测 · 152/173 命中]

**这是最高频错误。** GitCode 要求 `on:` 是 map（`on:\n  push:`），不是数组（`on:\n- push`）。

```yaml
# ✅ 正确 — map 格式
on:
  push:
  workflow_dispatch:

# ❌ 错误 — 数组格式（平台报 GitcodeOn deserialize 错误）
on:
- push
```

**注意**：case YAML 中 `workflow:` 字段用 block scalar `|` 写入时，缩进必须正确。`on:` 下的触发事件必须缩进 2 空格，不能是 `- ` 列表项。

### 8a. 默认触发事件（非 trigger 测试时）★

**如果当前用例不测 trigger 语义（事件类型、过滤器、分支匹配等），`on` 应使用 `workflow_dispatch` 而非 `push`：**

```yaml
# ✅ 默认 — 不测 trigger 时
on:
  workflow_dispatch:

# 仅在用例本身测试 push/PR/tag/fork 等触发事件时才用
on:
  push:
    branches: [main]
```

> `workflow_dispatch` 仅手动/API 触发，不会因常规 push 误触发无关 workflow，避免污染共享仓 run 列表、避免排队竞争。测 trigger 语义的用例才用对应事件。

---

## 9. `${{ }}` 在未加引号的字符串中导致 YAML 解析失败 ★ [平台实测]

`run:` 值中含 `${{ }}` 且未加引号时，YAML 解析器将 `:` 误认为 mapping 分隔符，报 `mapping values are not allowed here`。

```yaml
# ❌ 错误 — ${{ }} 中的 : 被误解析
run: echo "Direct: ${{ secrets.TEST_SECRET }}"

# ✅ 正确 — 整个值加引号
run: "echo \"Direct: ${{ secrets.TEST_SECRET }}\""
```

**规则**：任何含 `${{ }}` 的 `run:` 值必须用双引号包裹，内部双引号转义为 `\"`。

---

## 10. 禁止重复键 ★ [平台实测]

YAML mapping 中不能有重复的键。平台报 `在构建映射时，发现重复的键位于 [行X,列5] 处`。

常见场景：
- `name:` 在 job/step 级别重复出现
- `on:` 下同一事件写了多次

---

## 11. `on.<event>` branches 限制 ★ [平台实测]

`on.merge_requests` 和 `on.pull_request_target` 的 `branches` + `branches-ignore` 之和必须 ≥1 且 ≤32。

```yaml
# ❌ 错误 — 列表为空或超出 32
on:
  merge_requests:
    branches: []
    branches-ignore: []

# ✅ 正确
on:
  merge_requests:
    branches: [main]
```

---

## 12. `on.<event>.types` 允许值 ★ [平台实测]

| 事件 | 允许的 types |
|---|---|
| `pull_request_comment` | `created`, `deleted`, `edited` |
| `merge_requests` | `close`, `merge`, `open`, `reopen`, `update` |

```yaml
# ❌ 错误
on:
  pull_request_comment:
    types: [new]        # 不允许，应为 created

# ❌ 错误
on:
  merge_requests:
    types: [opened]     # 不允许，应为 open
```

---

## 13. `permissions` 不支持 ★ [平台实测 · 2026-07-23 确认]

GitCode 平台**完全不支持** `permissions` 字段——无论是 workflow 级还是 job 级。报 `unknown property`（workflow 级）或 `jobs[id].permissions: unknown property`（job 级）。

```yaml
# ❌ 错误 — workflow 级
permissions:
  contents: read
  pull-requests: write

# ❌ 错误 — job 级
jobs:
  test:
    permissions:
      contents: read

# ✅ 正确 — 删除所有 permissions 块
```

---

## 14. YAML 写入注意事项 ★

### 14a. `on:` 关键字保护

YAML 1.1 将 `on` 解析为 boolean `true`。写入 workflow YAML 时必须使用 block scalar `|` 格式，**禁止**用 `yaml.dump()` 重新序列化 workflow 字段。

```yaml
# ✅ 正确 — workflow 使用 block scalar
workflow: |
  on:
    push:
  jobs:
    ...

# ❌ 错误 — 会被 yaml.dump 转为 true: 
workflow: "on:\n- push\n..."
```

### 14b. 标题引号

标题含 `:` `{` `}` `[` `]` `$` `#` `&` `*` `!` `|` `>` `%` `@` `` ` `` 时必须双引号包裹。

---

---

## 16. `environment` 不支持 ★ [平台实测 · 2026-07-23]

GitCode 平台不支持 `jobs[id].environment` 字段，报 `jobs[id].environment: unknown property`。

```yaml
# ❌ 错误
jobs:
  deploy:
    environment: production

# ✅ 正确 — 删除 environment 块
```

---

## 17. `stages` 必须是 map，不是数组 ★ [平台实测 · 2026-07-23]

GitCode 的 `stages` 字段必须是 map 格式（`stages: {default: {jobs: {...}}}`），不支持数组格式 `stages: [{...}]`。数组格式报 `Cannot deserialize Map from Array value`。

```yaml
# ❌ 错误 — 数组格式
stages:
  - stage1:
      jobs:
        test:
          runs-on: [ubuntu-latest, x64, small]
          steps: [...]

# ✅ 正确 — map 格式
stages:
  default:
    jobs:
      test:
        runs-on: [ubuntu-latest, x64, small]
        steps: [...]
```

---

## 18. `run-name` 不支持 ★ [平台实测 · 2026-07-23]

GitCode 平台不支持 `run-name` 字段（GitHub Actions 特性），报 `run-name: unknown property`。

```yaml
# ❌ 错误
run-name: Deploy to ${{ inputs.environment }}

# ✅ 正确 — 删除 run-name
```

---

## 19. `concurrency` 校验规则 ★ [平台实测 · 2026-07-23]

### 19a. `preemption.events` 仅允许 `[mr_id]`

```yaml
# ❌ 错误 — push 不是允许值
concurrency:
  preemption:
    events: [push]

# ✅ 正确
concurrency:
  preemption:
    events: [mr_id]
```

### 19b. `max` ≥ 1

`concurrency.max` 不得小于 1，报 `值不能小于1`。

### 19c. `exceed-action` 不能为空

`concurrency.exceed-action` 不能为空值。

---

## 20. `services` / `post.steps` 不支持 ★ [平台实测 · 2026-07-23]

GitCode 平台不支持 GitHub Actions 的 `jobs[id].services` 和 `post.steps`，均报 `unknown property`。

```yaml
# ❌ 错误
jobs:
  test:
    services:
      redis:
        image: redis

# ❌ 错误
post:
  steps:
    - name: cleanup
      run: echo done

# ✅ 正确 — 不写这两个字段
```

---

## 21. `on.schedule` 必须是数组 ★ [平台实测 · 2026-07-23]

GitCode 的 `on.schedule` 必须是数组格式（`schedule: [{cron: ...}]`），不支持单对象格式 `schedule: {cron: ...}`。对象格式报 `Cannot deserialize ArrayList from Object value`。

```yaml
# ❌ 错误 — 对象格式
on:
  schedule:
    cron: "0 0 * * *"

# ✅ 正确 — 数组格式
on:
  schedule:
    - cron: "0 0 * * *"
```

---

## 22. 未知顶层字段拒绝 ★ [平台实测 · 2026-07-23]

GitCode 校验器拒绝任何不在 schema 中的顶层字段（如拼写错误的 `on` 变体、GitHub 专有字段等），报 `unknown_field: unknown property`。

常见误写：`jobs` → `job`、`steps` → `step`、`runs-on` → `run-on`、`workflow_dispatch` 拼写错误。

---

## 15. 标题（title）引号规则

### 16. ID 格式规则

```
<维度前缀>-<主题>-\d{2}-\d{3}(-V\d+)?
```

- 维度前缀：`COMP` | `COMPAT` | `REL` | `SEC` | `USE`
- 主题：`[A-Z0-9]+(?:-[A-Z0-9]+)*`
- run 序列：2 位数字，序号：3 位数字

### 17. 触发事件枚举

`push | pr | pull_request | fork_pr | pull_request_target | pull_request_comment | manual | schedule | tag | workflow_dispatch | issue_comment`

### 18. 必填字段 + 断言纪律

| 检查项 | 规则 |
|---|---|
| `dimension=security` | 至少 1 条 `type: negative` |
| `fault_injection` 非空 | `teardown.reset` 不得为 `none` |
| 所有维度 | `assertions` 非空数组 |
| `setup` | 必含 `repo_fixture` |

---

## 生成时自检清单

case-writer 在写入每个 YAML 前执行：

- [ ] `on:` 用 map 格式（`push:`），不是数组（`- push`）
- [ ] 不测 trigger 时 `on` 用 `workflow_dispatch`
- [ ] `runs-on` 用数组格式 `[ubuntu-latest, x64, small]`
- [ ] 不测 runs-on 时用 `[dedicate-hosted, x64, large]` 或 `[dedicate-hosted, arm64, large]`
- [ ] 每个 job 有 `name:`
- [ ] 每个 step 有 `name:`，无 `[` `]` `$` `{` `}` 等非法字符
- [ ] `if:` 表达式用 `${{ }}` 包裹，函数带 `()`
- [ ] 含 `${{ }}` 的 `run:` 值用双引号包裹
- [ ] workflow 字段用 block scalar `|`，不用 `yaml.dump()`
- [ ] 每个 job steps ≤ 16
- [ ] 无重复键
- [ ] `on.<event>.types` 使用平台允许的值
- [ ] 无 `permissions` 块
- [ ] 无 `environment` 块
- [ ] 无 `run-name`
- [ ] 无 `services` / `post.steps`
- [ ] `stages` 用 map 格式（不是数组）
- [ ] `on.schedule` 用数组格式（不是单对象）
- [ ] `concurrency.preemption.events` 只用 `[mr_id]`
- [ ] `dimension=security` → 含 `type: negative`
- [ ] 所有必填字段非空

---

*最后更新: 2026-07-23 · 来源: Run 2026-07-23-01 284 条平台校验 + Run 2026-07-21-02 173 条 + Run 2026-07-20-02 128 条 + demo 仓库 AGENTS.md 12 条平台规则*
