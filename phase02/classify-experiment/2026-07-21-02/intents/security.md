# 安全维度 · 攻击面测绘与防御性验收目标

> 产出 Agent：security（攻击面测绘师 / 防御性安全评审）
> Run：2026-07-21-02
> 角色红线：**只产防御性验收目标（系统应防住什么 / 什么不应发生），不产可利用 payload / exploit / 绕过步骤**。攻击面用意图层语言描述，落地由 case-writer 在受控 fixture 内完成。
> 来源输入：
> - `inputs/security-knowledge/`（github-actions-security-series.md · issues.md · README/OWASP CI/CD Top 10，fetched 2026-07-20/21）
> - `inputs/gitcode-spec/security-permissions/`（pr-mr-pipeline-security.md · token-permissions.md · using-secrets.md，fetched 2026-07-20）
> - `inputs/business-context/README.md`（部署模型：官方托管 + 自托管主机(内网) + 自托管 K8s，2026-07-21）
> - 本 run `intents/spec.md`（C-SEC-01~14 能力项 + 缺口 G-15~G-20）
> - `testing-focus.md` §5 secrets / §6 注入 / §7 供应链 / §8 cache

---

## 0. 信任边界总览（先画边界，再逐面扫）

### 0.1 不可信主体（外部可控，攻击发起点）
- **外部 fork 贡献者**：任何人可 fork 后提 PR，触发 `pull_request` / `pull_request_target` / `pull_request_comment` 流水线——开源社区最大攻击面。
- **PR/Issue 评论者**：`issue_comment` / `pull_request_comment` 触发面。
- **不可信事件负载字段**（攻击者可控）：PR 标题/正文、分支名(`head_ref`)、commit message、commit author name/email、评论正文——见 security-series Part 2。
- **第三方 action 作者**：`uses:` 引用的外部代码，在流水线上下文内运行。
- **相邻项目**：多项目共享 runner 资源池（issues.md §1），另一项目的 workflow 是横向不可信主体。

### 0.2 敏感资产（应被保护的对象）
- 项目级 / 组织级 / 环境级 **Secret**（`${{ secrets.* }}`）。
- **ATOMGIT_TOKEN**（自动令牌，可 clone/push/评论/操作资源，C-SEC-06）。
- **Runner**（宿主/容器文件系统、`/tmp`、`$ATOMGIT_WORKSPACE`、内网网络位置、进程空间）。
- **Cache / Artifact**（跨 job/run 共享数据，投毒载体）。
- **workflow 执行逻辑**（不应被不可信 PR 改写后以高权限运行）。

### 0.3 可触发的特权路径（重点监视）
- `pull_request_target`：base 上下文运行、有 secret + 写 token（C-TRIG-03 / C-SEC-10）——最易被滥用。
- `pull_request` from fork：应强制 token 只读 + secret 隔离（C-SEC-05 / C-SEC-09）。
- 显式 `checkout head.sha` + 高权限上下文：文档自承的注入点（G-17 / pr-mr-pipeline-security.md:72-78）。
- Cache 写：fork PR 写缓存污染主分支（G-19）。

### 0.4 覆盖矩阵（攻击面 × 威胁类别 × intent）
| 攻击面 | STRIDE / OWASP CI/CD | intent |
|---|---|---|
| Fork PR secret 隔离 | Info Disclosure / CICD-03,05 | 001,002,003 |
| pull_request_target 滥用 | Elevation / CICD-03 | 004,018 |
| Secret 日志脱敏变形泄露 | Info Disclosure / CICD-05 | 005,006,007,008 |
| 表达式/脚本注入 | Tampering,Elevation / CICD-03 | 009,010,012,013,014 |
| Token 权限过大 / 最小权限 | Elevation / CICD-01 | 015,016,017,023,036 |
| Action pin 供应链 | Tampering / CICD-02,10 | 021,022 |
| Cache / Artifact 投毒 | Tampering / CICD-06,10 | 019,020,029 |
| Runner 逃逸 / 残留 / 网络 | Info Disclosure,Elevation / CICD-06,09 | 025,026,027,028,033 |
| 侧信道外泄 / 写协议污染 | Info Disclosure,Tampering / CICD-05 | 024,032 |
| 审批 gate / TOCTOU | Repudiation,Elevation / CICD-03,08 | 030,031 |

> 说明：优先级线索标注中，风险登记册（`baseline/risk-register.md`）当前为模板态（见 spec.md），故各条「优先级线索」给出建议 P0/P1 候选 + testing-focus 依据，最终定级交门禁。

---

## 1. Fork PR 隔离组（不可信 fork 贡献者 → secret / token）

```
意图 ID:    INTENT-SEC-001
维度标签:   [security]
标题:       验证来自 fork 的 pull_request 流水线无法读取项目级/组织级 Secret

风险点:     开源社区任何人可 fork 提 PR。若 fork PR 能读到 Secret，则任意外部人可窃取部署凭据/API Key——CICD-05 薄弱 secret 管理 + CICD-03 恶意流水线执行。
预期系统行为: `pull_request` 事件来自 fork 时，`${{ secrets.* }}` 解析为空/不可用，workflow 无从获得项目级与组织级 Secret 明文。
Oracle 来源: GitCode规格（using-secrets.md:68 「fork 的 workflow 不可访问项目级 Secret」；pr-mr-pipeline-security.md:42-44；C-SEC-05）

验证要点:
  - [正向] 同仓库（非 fork）分支的 pull_request 可正常读取按作用域授权的 Secret。
  - [负向] fork PR 的 workflow 引用 `secrets.DEPLOY_TOKEN` 时不得取到明文；日志与任何输出中不出现 Secret 原值。
  - [非功能] 隔离行为不依赖用户显式声明，默认强制生效。

负向断言目标: 外部 fork 贡献者绝不应获得任一项目级/组织级 Secret 明文。判定证据 =（a）引用点求值为空占位而非真实值；（b）运行日志、artifact、step summary、output 全链路 grep 不到该 Secret 明文或其可逆编码；（c）无 Secret 相关环境变量注入 fork job。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-03/CICD-05；CVE 类：fork PR secret 泄露。
优先级线索: 建议 P0 候选（testing-focus §5 安全命脉；issues.md §2 敏感信息管理列为 P0）。
破坏级别:   fixture
来源输入:   using-secrets.md:63-71；pr-mr-pipeline-security.md:38-44；issues.md §2；security-series 总结点 4
```

```
意图 ID:    INTENT-SEC-002
维度标签:   [security]
标题:       验证 fork pull_request 下 ATOMGIT_TOKEN 被强制降为只读（无视 permissions 声明）

风险点:     若 fork PR 能提升 ATOMGIT_TOKEN 写权限，外部人可推代码/改仓库/操作 PR。文档承诺「无论 permissions 如何声明，fork PR 的 token 仅 read」（C-SEC-09）——需坐实此强制降权真实生效，且不能被 workflow 内声明放大。
预期系统行为: fork 来源的 `pull_request` 运行时，ATOMGIT_TOKEN 实际权限恒为 read，即使 workflow 顶层/ job 级声明 `permissions: repository: write` 亦被忽略降权。
Oracle 来源: GitCode规格（token-permissions.md:105；pr-mr-pipeline-security.md:8-16,40-42；C-SEC-09）

验证要点:
  - [正向] fork PR 中用 token 执行只读操作（clone/读取）成功。
  - [负向] fork PR 中即便声明 write 权限，用 token 执行写操作（推送/改 PR/评论）应被服务端拒绝；不得因 workflow 声明而获得写权限。
  - [非功能] 降权由平台强制，PR 提交者无法通过修改 fork 内 workflow 文件绕过。

负向断言目标: fork PR 上下文中 ATOMGIT_TOKEN 绝不应具备任何写权限。判定证据 =（a）写类 API 调用返回权限拒绝（403/等价）；（b）仓库/PR 状态无因该 job 产生的变更副作用；（c）token 权限自省（若可查）显示 read。
威胁类别: STRIDE-Elevation of Privilege；OWASP CICD-01/CICD-03。
优先级线索: 建议 P0 候选（testing-focus §5；权限越界=blocker 类）。
破坏级别:   fixture
来源输入:   token-permissions.md:97-105；pr-mr-pipeline-security.md:7-16
```

```
意图 ID:    INTENT-SEC-003
维度标签:   [security]
标题:       验证 fork PR 可修改 workflow 文件但攻击范围受限（无 secret、无写权限）

风险点:     `pull_request` 执行 fork 分支上的代码，含 PR 提交者修改过的 workflow 文件（pr-mr-pipeline-security.md:40）。需确认「可改 workflow 定义」这一事实不转化为实质危害——即改了也拿不到 secret、得不到写权限，攻击面被 001+002 的隔离封死。
预期系统行为: 即使 fork PR 修改 workflow 文件（增加试图输出 secret 或提权的步骤），运行仍在只读 token + 无 secret 的受限上下文内，无实质越权/泄露后果。
Oracle 来源: GitCode规格（pr-mr-pipeline-security.md:44 「可改 workflow，但无 secret 和写权限，攻击范围有限」）

验证要点:
  - [正向] fork PR 修改 workflow 后，非特权步骤（lint/build）正常运行。
  - [负向] fork PR 修改 workflow 试图读取 secret 或执行写操作时，不得成功——改 workflow 不应成为提权/泄密跳板。
  - [非功能] `pull_request` 使用 fork 中 workflow 版本这一行为本身不放大权限。

负向断言目标: 「可修改 workflow 文件」绝不应等价于「可获得 secret 或写权限」。判定证据 = 修改后的 workflow 各泄密/提权步骤均因 001/002 隔离而失败，无副作用产生。
威胁类别: STRIDE-Tampering→Elevation；OWASP CICD-04 流水线配置篡改。
优先级线索: 建议 P1 候选（依附 001/002；testing-focus §5）。
破坏级别:   fixture
来源输入:   pr-mr-pipeline-security.md:18-44
```

---

## 2. pull_request_target 滥用组（特权上下文 × 不可信代码）

```
意图 ID:    INTENT-SEC-004
维度标签:   [security]
标题:       验证 pull_request_target 使用 base 分支的 workflow 版本（PR 提交者不能改执行逻辑）

风险点:     `pull_request_target` 在 base 上下文运行、有完整 secret 与写 token（C-SEC-10）。其安全前提是「执行逻辑来自目标仓库 base 分支，PR 提交者无法修改」。若平台错用了 fork 分支的 workflow 文件，则外部人可在高权限上下文注入任意逻辑——Pwn Request（security-series Part 1）。
预期系统行为: `pull_request_target` 触发时，加载并执行 base 分支中的 workflow 文件版本，忽略 fork PR 对 workflow 文件的任何修改。
Oracle 来源: GitCode规格（pr-mr-pipeline-security.md:74 「workflow 文件使用目标仓库版本，PR 提交者无法修改执行逻辑」；C-SEC-10）

验证要点:
  - [正向] base 分支 workflow 按其定义执行，可访问 secret 与写 token。
  - [负向] fork PR 分支内对 workflow 文件的改动（新增窃密/提权步骤）不得被 `pull_request_target` 运行采用。
  - [非功能] 该来源选择由平台强制，非用户可配。

负向断言目标: `pull_request_target` 绝不应执行来自不可信 fork 的 workflow 定义。判定证据 =（a）运行采用的 workflow 内容哈希/步骤集与 base 分支一致，与 fork PR 改动不一致；（b）fork PR 注入的步骤未出现在执行记录中。
威胁类别: STRIDE-Elevation；OWASP CICD-03；CVE 类：Pwn Request。
优先级线索: 建议 P0 候选（testing-focus §5；security-series Part 1/4 头号模式）。
破坏级别:   fixture
来源输入:   pr-mr-pipeline-security.md:46-78；security-series Part 1/Part 4
```

```
意图 ID:    INTENT-SEC-018
维度标签:   [security]
标题:       验证 pull_request_target 下显式 checkout PR head 代码时的高权限注入风险被识别/防护

风险点:     文档自承（G-17 / pr-mr-pipeline-security.md:72-78）：`pull_request_target` 若显式 `checkout head.sha` 并执行其中脚本，等于在有 secret + 写 token 的上下文运行不可信代码——典型注入点。需验证系统是否提供防护约束或至少不放大隐性权限（如不自动把 secret 注入到执行不可信代码的步骤环境）。
预期系统行为: 即使显式 checkout 不可信 head 代码，平台不应把 secret 自动暴露给运行不可信代码的步骤；应存在可用的隔离手段（分离 workflow / 不 checkout 不可信代码 / 权限收窄）使该模式可被安全实现。
Oracle 来源: GitCode规格（pr-mr-pipeline-security.md:72-78 风险声明）+ GitHub行为（security-series Part 1/4 分离 workflow 缓解）；缺口 G-17 待实测确立防护边界。

验证要点:
  - [正向] 采用「不 checkout 不可信代码 / 分离特权步骤」的安全写法时，构建报告类流程可正常完成。
  - [负向] 在高权限 `pull_request_target` 上下文执行不可信 PR 代码时，该代码不应能读到未显式传入的 secret，也不应默认继承写 token 到不可信执行段。
  - [非功能] 文档/平台应能让用户判定「哪些步骤在跑不可信代码」。

负向断言目标: 不可信 PR 代码绝不应因运行在 `pull_request_target` 上下文而自动获得 secret 明文或写 token。判定证据 =（a）不可信代码执行段环境无 secret；（b）无越权写副作用；（c）secret 未出现在该段日志/输出。
威胁类别: STRIDE-Elevation；OWASP CICD-03；CVE 类：pull_request_target + checkout head.sha 注入。
优先级线索: 建议 P0 候选（testing-focus §5/§6；G-17 明确弱点）。
破坏级别:   fixture
来源输入:   pr-mr-pipeline-security.md:46-78；spec.md G-17；security-series Part 1/4
```

---

## 3. 表达式 / 脚本注入组（不可信事件负载 → 命令执行）

> 红线遵守：以下仅描述「以含 shell 元字符/命令替换语法的不可信输入」这一意图层攻击面，不给出具体可利用 payload 串。

```
意图 ID:    INTENT-SEC-009
维度标签:   [security]
标题:       验证 PR 标题/正文内联进 run 脚本时不导致命令执行（脚本注入）

风险点:     把 `${{ atomgit.event.pull_request.title/body }}` 等不可信字段直接内联进 `run:`，表达式在脚本生成前被替换，含命令分隔/替换语法的标题会被当作脚本执行——业界最常见 Actions 漏洞类（security-series Part 2）。
预期系统行为: 不可信字段经安全处理（中间环境变量）后不应改变脚本结构；含元字符的输入被当作数据而非代码。
Oracle 来源: GitHub行为（security-series Part 2 中间环境变量模式）+ GitCode规格（C-EXPR-06 事件负载）；缺口：GitCode 对内联表达式注入无专门防护声明，需实测。

验证要点:
  - [正向] 正常 PR 标题被正确当作字符串输出/处理。
  - [负向] 构造含命令分隔符/命令替换语法的 PR 标题时，不应触发任何计划外命令执行或副作用（无外连、无文件写、无 secret 读取）。
  - [非功能] 防护不依赖用户「记得转义」，中间变量模式应稳定有效。

负向断言目标: 不可信 PR 标题/正文绝不应被解释为可执行命令。判定证据 =（a）标记性副作用（如向受控 sink 的探测请求）未发生；（b）进程/文件系统无注入产物；（c）secret 未被该路径读出。
威胁类别: STRIDE-Tampering/Elevation；OWASP CICD-03；CVE 类：表达式内联 shell 注入。
优先级线索: 建议 P0 候选（testing-focus §6；security-series 头号注入面）。
破坏级别:   fixture
来源输入:   security-series Part 2；spec.md C-EXPR-06；testing-focus §6
```

```
意图 ID:    INTENT-SEC-010
维度标签:   [security]
标题:       验证非显而易见的不可信源（分支名 head_ref / commit message / author email）不致注入

风险点:     security-series Part 2 强调：分支名、commit message、author name/email 是最危险的隐蔽注入源（合法 git 分支名/RFC5322 email 可含 shell 语法）。这些常被误认为「系统生成的可信值」而直接内联。
预期系统行为: 上述字段内联到脚本/表达式时，含元字符的值被当作数据；经中间变量引用不改变脚本结构。
Oracle 来源: GitHub行为（security-series Part 2 不可信源清单）+ GitCode规格（C-EXPR-05/06 head_ref、event.commits 字段）。

验证要点:
  - [正向] 常规分支名/commit message/email 正常处理。
  - [负向] 构造含命令替换/分隔语法的分支名、commit message 或 author email 时，不应触发计划外命令执行或副作用。
  - [非功能] 覆盖 push/pull_request 两类事件负载来源。

负向断言目标: 分支名 / commit message / author email 绝不应成为命令注入通道。判定证据 = 同 SEC-009（受控 sink 无探测、无注入产物、secret 未泄）。
威胁类别: STRIDE-Tampering/Elevation；OWASP CICD-03；CVE 类：隐蔽字段 shell 注入。
优先级线索: 建议 P0 候选（testing-focus §6；最易漏防的注入面）。
破坏级别:   fixture
来源输入:   security-series Part 2（分支名/email 示例）；spec.md C-EXPR-05/06
```

```
意图 ID:    INTENT-SEC-012
维度标签:   [security]
标题:       验证 issue_comment / pull_request_comment 评论正文内联不致注入

风险点:     `issue_comment`（C-TRIG-04）与 GitCode 特有 `pull_request_comment`（C-TRIG-05）由任意评论者触发，评论正文是不可信输入。内联进 `run:` 同样构成注入面；且评论触发不受 PR 审批保护（IssueOps 陷阱，security-series Part 4）。
预期系统行为: 评论正文经中间变量安全处理，含元字符内容被当作数据；评论触发路径不绕过应有的审批/权限约束。
Oracle 来源: GitHub行为（security-series Part 4 IssueOps）+ GitCode规格（C-TRIG-04/05 事件负载）。

验证要点:
  - [正向] 正常评论内容被正确当作字符串处理。
  - [负向] 构造含命令语法的评论正文时不应触发计划外命令执行；评论触发不应获得超出该评论者身份的权限。
  - [非功能] 覆盖 Issue 评论与 PR 评论两种来源。

负向断言目标: 评论正文绝不应被解释为命令，评论触发绝不应成为提权/绕审批通道。判定证据 =（a）受控 sink 无探测、无注入产物；（b）触发运行的权限与评论者身份一致，无越权副作用。
威胁类别: STRIDE-Tampering/Elevation；OWASP CICD-03；CVE 类：IssueOps 注入。
优先级线索: 建议 P1 候选（testing-focus §6；GitCode 特有事件需实测）。
破坏级别:   fixture
来源输入:   security-series Part 4；spec.md C-TRIG-04/05
```

```
意图 ID:    INTENT-SEC-013
维度标签:   [security]
标题:       验证中间环境变量防御模式对注入的有效性（防御模式确认）

风险点:     业界标准缓解是「不可信值先存中间 env 变量，再在 shell 中引用 `$VAR`」（security-series Part 2 修复方案）。需正向坐实此模式在 GitCode 表达式求值时序下同样有效——否则给用户的迁移防护建议落空。
预期系统行为: 通过 `env:` 传入不可信值再以 `$VAR` 引用时，表达式在脚本生成前完成求值并存入变量，不参与脚本结构生成，注入被阻断。
Oracle 来源: GitHub行为（security-series Part 2 修复方案）+ GitCode规格（C-VAR-01~03 env 语义）。

验证要点:
  - [正向] 中间变量模式下，含元字符的不可信值被安全当作数据处理，功能正常。
  - [负向] 同一恶意输入在「内联表达式」写法下若能注入、在「中间变量」写法下必须不能注入——证明模式有效。
  - [非功能] 该模式在 GitCode 的表达式替换时序下与 GitHub 行为一致。

负向断言目标: 采用中间环境变量模式后，不可信输入绝不应改变脚本结构或触发命令执行。判定证据 = 中间变量写法下受控 sink 无探测、无注入产物。
威胁类别: STRIDE-Tampering（防御验证）；OWASP CICD-03。
优先级线索: 建议 P1 候选（testing-focus §6；迁移防护指导正确性）。
破坏级别:   fixture
来源输入:   security-series Part 2 修复方案；spec.md C-VAR-01~03
```

```
意图 ID:    INTENT-SEC-014
维度标签:   [security, compatibility]
标题:       验证双重表达式求值与 pull_request_comment 正则过滤的注入面

风险点:     两处叠加风险：(1) 某些 action 内部有二次模板渲染，不可信值经外层 `${{ }}` 求值后被内层引擎再求值→可执行代码（security-series Part 2 攻击 1）；(2) `pull_request_comment` 的 `comments` 正则过滤（C-TRIG-05）引擎/语法未声明（G-18），正则本身可能被恶意评论构造绕过或引发异常。
预期系统行为: 表达式求值不应对不可信值做隐式二次求值；正则过滤应有确定语义，不因恶意评论内容被绕过或崩溃。
Oracle 来源: GitHub行为（security-series Part 2 双重求值）+ 差异声明（G-18 正则引擎待实测确立）。

验证要点:
  - [正向] 正常评论按 `comments` 正则正确匹配/过滤触发。
  - [负向] 不可信值不应被隐式二次求值执行；构造异常评论内容不应绕过正则门禁触发本不该触发的特权流程，也不应导致过滤异常放行。
  - [非功能] 正则引擎/语法边界应可被文档化判定（关联 usability/compat）。

负向断言目标: 不可信输入绝不应经二次求值执行，也不应绕过 comments 正则门禁。判定证据 =（a）无二次求值产物；（b）不匹配的评论未触发特权运行。
威胁类别: STRIDE-Tampering/Elevation；OWASP CICD-03；CVE 类：双重求值 / 过滤绕过。
优先级线索: 建议 P1 候选（testing-focus §6；G-18 缺口）。
破坏级别:   fixture
来源输入:   security-series Part 2 攻击 1；spec.md G-18 / C-TRIG-05
```

---

## 4. Secret 日志脱敏变形泄露组（Info Disclosure）

> 前提事实：GitCode 文档自承脱敏可被绕过（C-SEC-03 / using-variables-secrets.md:116-120），且声明「不应依赖脱敏作为安全边界」。以下验证脱敏对各类变形的覆盖广度——脱敏是纵深防御的一层，覆盖越广越好，但不作为唯一边界。

```
意图 ID:    INTENT-SEC-005
维度标签:   [security]
标题:       验证 Secret 值在日志中的基础自动脱敏（直接输出被 *** 遮蔽）

风险点:     Secret 若原样出现在日志（echo、环境打印、报错回显）即泄露。基础脱敏是第一道防线（C-SEC-03）。
预期系统行为: 授权 job 中 Secret 明文一旦进入标准输出/错误流，应被替换为 `***`，包括意外的错误消息回显。
Oracle 来源: GitCode规格（using-secrets.md:66 日志遮掩；variables.md:48；C-SEC-03）

验证要点:
  - [正向] 授权 job 中 Secret 可正常用于业务操作（不影响功能）。
  - [负向] Secret 原值不应以明文出现在任何 step 日志、报错消息或注解中。
  - [非功能] 遮蔽对 stdout 与 stderr 均生效。

负向断言目标: Secret 明文绝不应出现在运行日志中。判定证据 = 全量日志 grep 该占位 Secret 原值命中数为 0，对应位置显示 `***`。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05。
优先级线索: 建议 P0 候选（testing-focus §5；issues.md §3 P0）。
破坏级别:   fixture
来源输入:   using-secrets.md:62-71；spec.md C-SEC-03；issues.md §3
```

```
意图 ID:    INTENT-SEC-006
维度标签:   [security]
标题:       验证编码变形（base64 等）后 Secret 的脱敏覆盖

风险点:     历史缺陷：将 Secret 编码（如 base64）后输出，脱敏引擎只匹配原值而漏掉编码形态，导致可逆泄露（issues.md §3；README CVE 速查）。
预期系统行为: Secret 经常见可逆编码后输出时，理想情况下其编码形态也被遮蔽；若平台不覆盖，则该缺口必须被明确记录并有补偿控制（不作为唯一边界）。
Oracle 来源: GitHub行为（`::add-mask::` 历史缺陷）+ GitCode规格（C-SEC-03 自承可绕过）；缺口：GitCode 对编码变形覆盖度未声明，需实测。

验证要点:
  - [负向] Secret 的 base64（及其他常见可逆编码）形态不应以可还原明文的方式出现在日志。
  - [非功能] 若确证未覆盖，须记录为已知缺口并验证不依赖脱敏作为唯一边界（配合 fork 隔离等）。

负向断言目标: Secret 的可逆编码形态绝不应导致明文可被从日志还原。判定证据 =（a）日志中不存在可解码回原 Secret 的串；（b）若存在，标记为确认缺陷并登记。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏编码绕过。
优先级线索: 建议 P0 候选（testing-focus §5；issues.md §3 明确历史缺陷）。
破坏级别:   fixture
来源输入:   issues.md §3；security-knowledge/README CVE 速查；spec.md C-SEC-03
```

```
意图 ID:    INTENT-SEC-007
维度标签:   [security]
标题:       验证字符串拼接/分片输出时 Secret 的脱敏覆盖

风险点:     将 Secret 分片或与其他字符拼接后逐段输出，可绕过按完整串匹配的脱敏（security-series Part 2 分片输出绕过；issues.md §3）。
预期系统行为: 分片/拼接形态下脱敏尽力覆盖；不能覆盖之处须被记录，并确保不作为唯一安全边界。
Oracle 来源: GitHub行为（分片输出绕过）+ GitCode规格（C-SEC-03）；缺口待实测。

验证要点:
  - [负向] Secret 被拆分/拼接后逐段输出时，不应能从日志重组出完整明文。
  - [非功能] 覆盖边界须可判定并记录。

负向断言目标: Secret 绝不应通过分片/拼接从日志被重组还原。判定证据 = 按段落重组日志片段无法还原出占位 Secret 原值；若可，登记为缺陷。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏分片绕过。
优先级线索: 建议 P0 候选（testing-focus §5；issues.md §3）。
破坏级别:   fixture
来源输入:   security-series Part 2；issues.md §3；spec.md C-SEC-03
```

```
意图 ID:    INTENT-SEC-008
维度标签:   [security]
标题:       验证多行 Secret 值的逐行脱敏覆盖

风险点:     多行 Secret（如 PEM 私钥）若脱敏仅按单行匹配，中间行可能明文泄露（issues.md §3）。
预期系统行为: 多行 Secret 的每一行在日志中均被遮蔽。
Oracle 来源: GitCode规格（C-SEC-03）+ GitHub行为；缺口待实测。

验证要点:
  - [正向] 多行 Secret 可正常用于业务（如 SSH 私钥认证）。
  - [负向] 多行 Secret 的任意一行不应以明文出现在日志。
  - [非功能] 遮蔽覆盖首行、中间行、末行。

负向断言目标: 多行 Secret 的任何一行明文绝不应出现在日志。判定证据 = 逐行 grep 每一行原文命中数为 0。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：多行值脱敏遗漏。
优先级线索: 建议 P1 候选（testing-focus §5；issues.md §3）。
破坏级别:   fixture
来源输入:   issues.md §3；spec.md C-SEC-03
```

---

## 5. Token 权限过大 / 最小权限组（Elevation · CICD-01）

```
意图 ID:    INTENT-SEC-015
维度标签:   [security]
标题:       验证 permissions 收窄声明真实生效（越权操作被拒）

风险点:     若 `permissions:` 声明为文档橱窗、实际不约束 token，则「最小权限」形同虚设，被攻陷步骤可越权操作（CICD-01）。需坐实收窄确实降低 token 能力。
预期系统行为: job 声明某权限域为 `none`/`read` 后，该域的写操作用 ATOMGIT_TOKEN 执行应被服务端拒绝。
Oracle 来源: GitCode规格（token-permissions.md:24-47 权限域；C-SEC-07）

验证要点:
  - [正向] 声明 `pr: write` 时评论 PR 成功；声明 `repository: read` 时 clone 成功。
  - [负向] 声明 `pr: none` 后用 token 评论/操作 PR 应被拒绝；声明 `repository: read` 后推送应被拒绝。
  - [非功能] job 级覆盖顶层 permissions 的收窄生效。

负向断言目标: 被收窄为 none/read 的权限域绝不应仍可执行写操作。判定证据 =（a）越权 API 调用返回权限拒绝；（b）无对应副作用（无评论/无推送）。
威胁类别: STRIDE-Elevation；OWASP CICD-01。
优先级线索: 建议 P0 候选（testing-focus §5；权限失效=blocker 类）。
破坏级别:   fixture
来源输入:   token-permissions.md:24-104；spec.md C-SEC-07
```

```
意图 ID:    INTENT-SEC-016
维度标签:   [security, usability]
标题:       验证 permissions:{} 的实际权限并消解「全 none vs repository:read」文档冲突

风险点:     G-21：`permissions: {}` 两处文档冲突（一处称全 none，一处称仅 repository:read）。这决定最小权限模式下 token 究竟能做什么，是安全+易用双敏感点；若实际权限宽于文档承诺，则最小权限被架空。
预期系统行为: `permissions: {}` 有唯一确定的最小权限集，与至少一处文档一致，且不宽于承诺。
Oracle 来源: 差异声明（workflow-file-location-structure.md:216-223 vs token-permissions.md:103 冲突，需实测确立权威值回写 Parity Matrix）；缺口 G-06/G-21。

验证要点:
  - [正向] 设 `permissions: {}` 后测得 ATOMGIT_TOKEN 的确定实际权限集。
  - [负向] 实际权限不应宽于两处文档承诺的较小者；不应出现「声明最小却仍能写」的越权。
  - [非功能] 实测结果消解文档矛盾，供 compat-diff 定 oracle、usability 出勘误。

负向断言目标: `permissions: {}` 下 token 绝不应具备任何写权限。判定证据 = 各权限域写操作全部被拒；实测权限集与承诺一致。
威胁类别: STRIDE-Elevation；OWASP CICD-01。
优先级线索: 建议 P1 候选（testing-focus §5/§11；关联 G-06/G-21）。
破坏级别:   fixture
来源输入:   spec.md G-06/G-21；token-permissions.md:97-105；workflow-file-location-structure.md:212-224
```

```
意图 ID:    INTENT-SEC-017
维度标签:   [security]
标题:       验证未声明 permissions 时的默认权限不宽于仓库设置（无隐性提权）

风险点:     未声明 permissions 时「使用仓库设置权限」（C-SEC-07），但仓库默认权限具体范围未给（G-06）。若默认过宽（如默认 write-all），则大量未显式声明的 workflow 隐性持有过大 token——CICD-01。
预期系统行为: 未声明 permissions 的运行，token 权限严格等于仓库设置所定义，不超出；默认应倾向最小/只读。
Oracle 来源: GitCode规格（token-permissions.md:101）+ 差异声明（G-06 默认范围待实测）。

验证要点:
  - [正向] 未声明 permissions 时，token 权限与仓库设置一致。
  - [负向] token 实际权限不应超出仓库设置声明的范围；默认不应无条件是 write-all。
  - [非功能] 默认权限范围可被观测并文档化。

负向断言目标: 未声明 permissions 绝不应导致 token 获得超出仓库设置的权限。判定证据 = 实测权限集 ⊆ 仓库设置；无隐性写提权。
威胁类别: STRIDE-Elevation；OWASP CICD-01。
优先级线索: 建议 P1 候选（testing-focus §5；G-06 缺口）。
破坏级别:   fixture
来源输入:   token-permissions.md:97-105；spec.md G-06
```

```
意图 ID:    INTENT-SEC-023
维度标签:   [security]
标题:       验证 ATOMGIT_TOKEN 运行后失效且不可通过缓存/残留复活

风险点:     ATOMGIT_TOKEN「仅运行期有效，运行后失效，勿持久化」（C-SEC-06）。若过期 token 能通过缓存、artifact 或 runner 磁盘残留被后续运行复用，则等于长期凭据泄露（security-series 总结点 6；issues.md §2）。
预期系统行为: token 在运行结束后即失效；即使被写入 cache/artifact/磁盘，后续读取到的旧 token 用于鉴权应被拒绝。
Oracle 来源: GitCode规格（token-permissions.md:11-20；C-SEC-06）+ GitHub行为（token 生命周期）。

验证要点:
  - [正向] 运行期内 token 正常鉴权。
  - [负向] 运行结束后，用先前运行遗留（缓存/artifact/磁盘）的旧 token 鉴权应失败；旧 token 不应被「复活」。
  - [非功能] token 失效与运行生命周期强绑定。

负向断言目标: 已结束运行的 ATOMGIT_TOKEN 绝不应仍可用于鉴权。判定证据 = 用过期 token 的 API 调用返回鉴权失败；无任何依赖旧 token 成功的操作。
威胁类别: STRIDE-Elevation/Spoofing；OWASP CICD-05。
优先级线索: 建议 P1 候选（testing-focus §5；issues.md §2 token 轮换）。
破坏级别:   fixture
来源输入:   token-permissions.md:11-20；issues.md §2；security-series 总结点 6
```

```
意图 ID:    INTENT-SEC-036
维度标签:   [security]
标题:       验证 ATOMGIT_TOKEN 默认权限范围与 job 级覆盖的正确性

风险点:     内置 token 默认权限范围是最小权限落地的基线（issues.md §2；CICD-01）。默认过宽或 job 级覆盖不生效，都会导致特权面失控。
预期系统行为: 默认 token 权限范围可被确定枚举；顶层与 job 级 permissions 的继承/覆盖语义（job 级收窄生效）符合文档。
Oracle 来源: GitCode规格（token-permissions.md:99-104 permissions 与 token 关系表；C-SEC-07）

验证要点:
  - [正向] 顶层声明被各 job 继承；job 级声明覆盖顶层。
  - [负向] job 级收窄后不应仍保留顶层的更大权限；默认权限不应包含未声明的写域。
  - [非功能] 权限范围与覆盖关系可被观测判定。

负向断言目标: token 绝不应持有超出（顶层∩job级）有效声明的权限。判定证据 = 各权限域实测与有效声明一致，越权写被拒。
威胁类别: STRIDE-Elevation；OWASP CICD-01。
优先级线索: 建议 P1 候选（testing-focus §5；issues.md §2 引用 INTENT-SEC-036）。
破坏级别:   fixture
来源输入:   token-permissions.md:97-104；issues.md §2
```

---

## 6. Action pin 供应链组（Tampering · CICD-02/10）

```
意图 ID:    INTENT-SEC-021
维度标签:   [security]
标题:       验证 uses 支持 commit SHA 不可变引用，且可变 tag/分支引用的重写风险被识别

风险点:     `uses: owner/repo@ref` 若只能用可变 tag/`@main`，第三方 action 作者（或攻陷者）可重写该 ref 引入恶意代码——供应链攻击（security-series Part 3；tj-actions 类事件；CICD-02/10）。文档已给推荐度：SHA 生产推荐、@main 不推荐（C-ACT-07）。
预期系统行为: 支持完整 commit SHA pin，pin 后引用不可变——上游重写 tag 不影响已 pin 到 SHA 的运行；可变引用的风险可被用户识别。
Oracle 来源: GitCode规格（using-actions.md:94-100 版本引用推荐；C-ACT-07）+ GitHub行为（security-series Part 3 五种 pin）。

验证要点:
  - [正向] `@<完整SHA>` 引用能正常解析并稳定执行同一版本。
  - [负向] 同一可变 tag 被上游重新指向后，已 pin 到 SHA 的引用不应随之改变所执行的代码。
  - [非功能] 文档/机制应能让用户区分不可变 vs 浮动引用。

负向断言目标: pin 到完整 SHA 的 action 引用绝不应因上游 tag/分支被重写而执行到非预期代码。判定证据 = SHA-pinned 运行的 action 内容哈希在上游 tag 重写前后一致。
威胁类别: STRIDE-Tampering；OWASP CICD-02/CICD-10；CVE 类：可变 tag 重写供应链攻击。
优先级线索: 建议 P1 候选（testing-focus §7；security-series Part 3）。
破坏级别:   fixture
来源输入:   using-actions.md:94-100；security-series Part 3；spec.md C-ACT-07
```

```
意图 ID:    INTENT-SEC-022
维度标签:   [security]
标题:       验证第三方 action 对 ATOMGIT_TOKEN / secret 的隐式获取受最小权限约束

风险点:     被 `uses:` 引用的 action 即使 YAML 未显式传 token，仍可访问运行上下文的 token 与环境中的 secret（security-series Part 3 「Token 暴露」）；恶意 action 可默认拉取 token 外泄。
预期系统行为: 第三方 action 能访问的 token 权限受 job 的 `permissions` 收窄约束；未显式传入的 secret 不应自动出现在 action 可读环境。
Oracle 来源: GitHub行为（security-series Part 3）+ GitCode规格（C-SEC-07 permissions 收窄）。

验证要点:
  - [正向] 收窄 permissions 后，第三方 action 仅能行使被授予的最小权限。
  - [负向] 第三方 action 不应能行使超出 job permissions 的 token 权限；未显式传入的 secret 不应默认可被 action 读取。
  - [非功能] 权限约束对 action 内部代码同样强制。

负向断言目标: 第三方 action 绝不应获得超出 job permissions 的 token 权限或未授予的 secret。判定证据 =（a）action 内越权写操作被拒；（b）action 环境中无未传入的 secret。
威胁类别: STRIDE-Info Disclosure/Elevation；OWASP CICD-07/CICD-02。
优先级线索: 建议 P1 候选（testing-focus §7；security-series Part 3）。
破坏级别:   fixture
来源输入:   security-series Part 3；spec.md C-SEC-07/C-ACT-06
```

---

## 7. Cache / Artifact 投毒组（Tampering · CICD-06/10）

```
意图 ID:    INTENT-SEC-019
维度标签:   [security, reliability]
标题:       验证 fork PR 无法投毒主分支缓存（cache 作用域隔离）

风险点:     G-19：cache 声明「同仓库所有运行共享」（C-ART-06），未声明是否含 fork PR。若 fork PR 能写入主分支可读的缓存，则外部人可投毒缓存污染主分支后续构建——即便 `permissions: {}` 移除写权限仍可投毒（security-series Part 4 明确）。
预期系统行为: fork PR 写入的缓存与主分支/受信任运行的缓存作用域隔离；fork PR 不应能覆盖或注入主分支使用的缓存条目。
Oracle 来源: 差异声明（G-19 待实测确立作用域）+ GitHub行为（security-series Part 4 fork cache 隔离缓解）。

验证要点:
  - [正向] 同仓库受信任运行间缓存正常命中复用。
  - [负向] fork PR 运行写入的缓存不应被主分支/受信任运行命中使用；fork 不应能覆盖既有主分支缓存键。
  - [非功能] 缓存键作用域按信任边界隔离，行为可观测。

负向断言目标: fork PR 绝不应污染主分支或受信任运行使用的缓存。判定证据 =（a）主分支运行未命中 fork 写入的缓存条目；（b）主分支缓存内容哈希不被 fork 运行改变。
威胁类别: STRIDE-Tampering；OWASP CICD-06/CICD-10；CVE 类：cache 投毒 / TOCTOU。
优先级线索: 建议 P0 候选（testing-focus §8；G-19 明确缺口；security-series Part 4）。
破坏级别:   fixture
来源输入:   artifacts-and-cache.md:36-42；spec.md G-19；security-series Part 4；issues.md §4
```

```
意图 ID:    INTENT-SEC-020
维度标签:   [security]
标题:       验证 cache key 跨项目/跨仓库作用域隔离（无横向污染）

风险点:     多项目共享 runner 与缓存基础设施（issues.md §1）。若缓存命名空间不按仓库/项目隔离，项目 A 可读/写项目 B 的缓存——横向投毒与信息泄露（CICD-06）。
预期系统行为: 缓存条目按仓库/项目命名空间隔离，一个项目的运行不能读取或覆盖另一项目的缓存。
Oracle 来源: GitCode规格（artifacts-and-cache.md:36-42 「同仓库共享」隐含跨仓库隔离）+ 差异声明（跨项目边界待实测）。

验证要点:
  - [正向] 同仓库内缓存按 key 正常共享。
  - [负向] 项目 A 的运行不应命中或覆盖项目 B 的缓存条目（即使 key 同名）。
  - [非功能] 命名空间隔离对读与写均生效。

负向断言目标: 一个项目/仓库绝不应读取或覆盖另一项目/仓库的缓存。判定证据 = 跨项目同名 key 互不命中；A 写入不改变 B 的缓存内容。
威胁类别: STRIDE-Info Disclosure/Tampering；OWASP CICD-06。
优先级线索: 建议 P1 候选（testing-focus §8；issues.md §1 多项目隔离）。
破坏级别:   full_instance
来源输入:   artifacts-and-cache.md:36-42；issues.md §1
```

```
意图 ID:    INTENT-SEC-029
维度标签:   [security]
标题:       验证跨运行 artifact 被视为不可信数据（artifact 投毒防护）

风险点:     恶意 PR 上传被污染的 artifact，特权后续运行（workflow_run 等价链式场景）下载后未校验即使用——artifact 投毒（security-series Part 4）。GitCode 是否有等价特权链取决于其触发模型，但「下游消费上游 artifact」的信任问题通用。
预期系统行为: 不同信任级别运行间的 artifact 传递有清晰边界；来自不可信（fork PR）运行的 artifact 不应被特权运行隐式信任消费。
Oracle 来源: GitHub行为（security-series Part 4 artifact 投毒）+ GitCode规格（C-ART-01/02 artifact 跨 job 传递）；缺口：GitCode workflow_run 等价机制待实测。

验证要点:
  - [正向] 同信任级别运行间 artifact 正常传递使用。
  - [负向] 不可信运行产出的 artifact 不应在特权运行中被自动信任/执行；下游对 artifact 内容应可校验来源。
  - [非功能] artifact 来源/信任级别可被判定。

负向断言目标: 不可信来源的 artifact 绝不应被特权运行隐式信任执行。判定证据 =（a）特权运行不自动执行 artifact 内容；（b）artifact 来源可追溯至其产出运行的信任级别。
威胁类别: STRIDE-Tampering；OWASP CICD-10；CVE 类：artifact 投毒 / workflow_run 链式攻击。
优先级线索: 建议 P1 候选（testing-focus §8；security-series Part 4）。
破坏级别:   fixture
来源输入:   security-series Part 4；spec.md C-ART-01/02
```

---

## 8. Runner 隔离 / 残留 / 网络组（Info Disclosure · Elevation · CICD-06/09）

```
意图 ID:    INTENT-SEC-025
维度标签:   [security, reliability]
标题:       验证 Runner 跨 job/跨 run 无敏感残留（工作区/环境/凭据清理）

风险点:     G-15：托管 Runner 是否 ephemeral、跨 job 残留污染未声明（仅 RUNNER_TEMP 每 job 清空）。若复用 Runner 不彻底清理，上一 job/run 的 secret、token、`.git-credentials`、`.env`、缓存文件可被下一 job（尤其相邻不可信项目）读取——CICD-06；issues.md §1/§4。
预期系统行为: 每个 job 起始获得干净环境；上一运行遗留的凭据/敏感文件/环境变量不可见于后续 job。
Oracle 来源: 差异声明（G-15 ephemeral 语义待实测）+ GitHub行为（ephemeral runner 清理）+ 规格线索（RUNNER_TEMP 每 job 清空，C-RUN-12）。

验证要点:
  - [正向] job 起始工作区为预期干净初始状态。
  - [负向] 后续 job 不应能读取到前序 job/run 写入的 secret、token、凭据文件或敏感环境变量残留。
  - [非功能] 清理覆盖工作区、`/tmp`、`$HOME`、环境变量与进程空间。

负向断言目标: 前序运行的敏感数据绝不应残留可被后续 job 读取。判定证据 = 后续 job 在常见残留位置（workspace/`/tmp`/`$HOME`/环境变量）grep 前序标记性凭据命中数为 0。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06；CVE 类：runner 复用残留泄露。
优先级线索: 建议 P0 候选（testing-focus §4；issues.md §1/§4；G-15）。
破坏级别:   full_instance
来源输入:   spec.md G-15/C-RUN-12；issues.md §1/§4；security-knowledge/README §5
```

```
意图 ID:    INTENT-SEC-026
维度标签:   [security]
标题:       验证共享盘（/tmp、workspace）不跨 job 泄露敏感文件

风险点:     issues.md §4：`/tmp`、`$ATOMGIT_WORKSPACE`、`/home/runner` 等共享目录可能跨 job 残留敏感文件（`.env`、`.git-credentials`）。与 025 互补，聚焦共享目录可见性边界。
预期系统行为: 一个 job 写入共享目录的敏感文件不应对另一（并发或后继）job 可见；缓存/artifact 不应意外携带敏感文件。
Oracle 来源: GitCode规格（C-RUN-12 隔离线索）+ 差异声明（跨 job 共享目录可见性待实测）；issues.md §4。

验证要点:
  - [负向] job A 在共享目录写入的敏感文件不应被 job B 读取；打包的缓存/artifact 不应意外包含 `.env`/`.git-credentials` 类文件。
  - [非功能] 覆盖并发 job 与后继 job 两种时序。

负向断言目标: 一个 job 的敏感文件绝不应经共享目录泄露给另一 job。判定证据 = job B 在共享目录读取 job A 写入的标记文件失败；导出的缓存/artifact 清单不含敏感文件。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06。
优先级线索: 建议 P1 候选（testing-focus §4；issues.md §4）。
破坏级别:   full_instance
来源输入:   issues.md §4；spec.md C-RUN-12
```

```
意图 ID:    INTENT-SEC-027
维度标签:   [security, reliability]
标题:       验证 Runner 网络出站边界（防 SSRF / 内网跳板 / 数据外传）

风险点:     G-14：网络出站范围（内网/DNS/代理）未详，仅「有外网权限」（C-RUN-13）。自托管 Runner 常部署于内网（business-context 部署模型），若无出站边界，不可信 PR 运行可探测/访问内部服务成为跳板，或把 secret 外传——CICD-09；issues.md §5。
预期系统行为: 不可信运行的网络出站有可界定边界；自托管内网场景下，Runner 不应无差别成为内网横向访问跳板；数据外传面可被识别/限制。
Oracle 来源: GitCode规格（C-RUN-13 出站声明）+ 差异声明（G-14 出站范围待实测）；business-context 自托管内网部署。

验证要点:
  - [正向] 声明允许的外网访问（如拉依赖）正常。
  - [负向] 不可信运行不应能任意访问内部/非公开服务；不应存在无约束的 secret 外传通道未被识别。
  - [非功能] 网络边界在容器/VM/裸机 Runner 上的差异可被判定（关联 reliability）。

负向断言目标: 不可信运行绝不应无约束访问内网服务或外传敏感数据而不被察觉。判定证据 =（a）对受控内网 sink 的探测被阻断或记录；（b）出站策略可枚举。
威胁类别: STRIDE-Info Disclosure/Elevation；OWASP CICD-09；SSRF 类。
优先级线索: 建议 P1 候选（testing-focus §4；issues.md §5；G-14；自托管内网部署）。
破坏级别:   full_instance
来源输入:   spec.md G-14/C-RUN-13；issues.md §5；business-context 部署模型
```

```
意图 ID:    INTENT-SEC-028
维度标签:   [security]
标题:       验证多项目共享 Runner 的 Secret 与资源隔离（项目 A secret 不达项目 B）

风险点:     issues.md §1：多开源项目共享同一批 Runner。项目 A 的 secret/token/资源绝不应在项目 B 的 workflow 中可访问，否则一个项目被攻陷即横向波及——CICD-06。
预期系统行为: Secret 作用域严格绑定其所属组织/项目（C-SEC-01）；项目 B 的运行无法获取项目 A 的 secret 或读取其运行时资源。
Oracle 来源: GitCode规格（using-secrets.md:14-25 作用域；C-SEC-01）+ 差异声明（共享 runner 横向隔离待实测）；issues.md §1。

验证要点:
  - [正向] 各项目在其作用域内正常使用自身 secret。
  - [负向] 项目 B 的 workflow 不应能读取项目 A 的项目级 secret，也不应读取其运行时内存/磁盘/环境残留。
  - [非功能] 隔离在并发共享 Runner 时依然成立。

负向断言目标: 一个项目的 secret/资源绝不应被另一项目的运行访问。判定证据 =（a）项目 B 引用项目 A 的 secret 名求值为空；（b）跨项目残留读取失败（含并发场景）。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06；CVE 类：多租户隔离失效。
优先级线索: 建议 P0 候选（testing-focus §4/§5；issues.md §1 首要历史关注点）。
破坏级别:   full_instance
来源输入:   using-secrets.md:14-25；issues.md §1；spec.md C-SEC-01
```

```
意图 ID:    INTENT-SEC-033
维度标签:   [security, reliability]
标题:       验证同主机 Runner 并发 job 间的隔离（进程/文件/环境互不可见）

风险点:     C-RUN-12：主机 Runner 同主机多 Job 共享环境。并发 job 若能互相读取进程环境（含 secret 注入的环境变量）、文件或工作区，则同主机相邻 job 成为泄露通道——issues.md §1。
预期系统行为: 并发 job 间进程空间、环境变量、工作区相互隔离；一个 job 的 secret 环境变量不可被并发 job 读取。
Oracle 来源: GitCode规格（C-RUN-12 主机 Runner 共享环境说明）+ 差异声明（并发 job 隔离度待实测）；issues.md §1。

验证要点:
  - [负向] 并发 job B 不应能枚举/读取并发 job A 的进程环境变量（尤其 secret）、打开其工作区文件或读取其临时目录。
  - [非功能] 隔离对主机 Runner 与 K8s Pod Runner 的差异可被判定。

负向断言目标: 并发 job 绝不应读取到相邻 job 的 secret 环境变量或私有文件。判定证据 = job B 枚举系统进程环境/文件时无法取得 job A 注入的标记性 secret。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06。
优先级线索: 建议 P1 候选（testing-focus §4；issues.md §1 INTENT-SEC-033）。
破坏级别:   full_instance
来源输入:   spec.md C-RUN-12；issues.md §1
```

---

## 9. 侧信道外泄 / 写协议污染组

```
意图 ID:    INTENT-SEC-032
维度标签:   [security]
标题:       验证 Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄

风险点:     日志脱敏之外的输出通道（`ATOMGIT_OUTPUT`、artifact、`ATOMGIT_STEP_SUMMARY`）若不做同等遮蔽，被攻陷步骤可把 secret 写入这些侧信道外泄——脱敏只覆盖日志则形同虚设（security-series Part 2 提示 secret 落盘/输出）。
预期系统行为: Secret 若被写入 output/artifact/step summary，应被遮蔽或该风险被明确记录并有补偿控制；不应存在「日志遮了但 summary 明文」的缺口。
Oracle 来源: GitCode规格（C-ACT-02 文件协议、C-OBS-04 step summary、C-ART-01 artifact）+ 差异声明（侧信道遮蔽覆盖待实测）。

验证要点:
  - [负向] Secret 明文不应以未遮蔽形式出现在 step summary、job output 或上传的 artifact 中。
  - [非功能] 覆盖 output/summary/artifact 三条侧信道。

负向断言目标: Secret 绝不应经 output/artifact/step summary 侧信道以明文外泄。判定证据 = 三类产物中 grep 占位 secret 原值命中数为 0；若命中，登记为缺陷。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏侧信道绕过。
优先级线索: 建议 P1 候选（testing-focus §5/§8）。
破坏级别:   fixture
来源输入:   spec.md C-ACT-02/C-OBS-04/C-ART-01；security-series Part 2
```

```
意图 ID:    INTENT-SEC-024
维度标签:   [security]
标题:       验证工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权

风险点:     `>> $ATOMGIT_ENV` / `$ATOMGIT_OUTPUT` / `$ATOMGIT_PATH` 文件协议（C-ACT-02）若被不可信输入注入多行内容，可污染后续 step 的环境变量或 PATH，进而劫持后续命令——GitHub 同类 env 注入漏洞模式（testing-focus §6）。
预期系统行为: 不可信值写入这些协议文件时不应能注入额外环境变量/PATH 条目；多行/换行注入被安全处理。
Oracle 来源: GitHub行为（GITHUB_ENV 注入模式）+ GitCode规格（C-ACT-02 文件协议 `>>` 追加语义）。

验证要点:
  - [负向] 含换行/协议控制字符的不可信值写入 `ATOMGIT_ENV/OUTPUT/PATH` 时，不应注入计划外的环境变量、output 或 PATH 条目劫持后续 step。
  - [非功能] 多行值应经随机 delimiter 等机制安全写入（C-ACT-05）。

负向断言目标: 不可信输入绝不应经写协议文件注入环境变量/PATH 劫持后续步骤。判定证据 = 后续 step 环境/PATH 无注入条目；被劫持命令未执行。
威胁类别: STRIDE-Tampering/Elevation；OWASP CICD-03；CVE 类：GITHUB_ENV/PATH 注入。
优先级线索: 建议 P1 候选（testing-focus §6；C-ACT-02/05）。
破坏级别:   fixture
来源输入:   spec.md C-ACT-02/C-ACT-05；testing-focus §6
```

---

## 10. 审批 gate / TOCTOU 组（Repudiation · Elevation · CICD-03/08）

```
意图 ID:    INTENT-SEC-030
维度标签:   [security, usability]
标题:       验证环境保护规则（reviewers/wait timer）未审批时环境 Secret 不可访问

风险点:     G-20：环境保护规则机制未详（C-SEC-14），仅「可配审批人」。若审批 gate 可被绕过或未生效，则受保护环境的部署 secret 在未经审批时即可被访问——CICD-03；issues.md §2。
预期系统行为: 绑定审批的环境级 Secret，在审批通过前对 job 不可访问；wait timer 未到/reviewer 未批时 job 不进入可访问 secret 的阶段。
Oracle 来源: GitCode规格（using-secrets.md:70 环境审批；C-SEC-14）+ 差异声明（G-20 机制待实测）。

验证要点:
  - [正向] 审批通过后，环境 secret 可被授权 job 正常访问。
  - [负向] 审批通过前，job 不应能访问该环境的 secret，也不应能通过重触发/改事件绕过审批门。
  - [非功能] 审批状态与 secret 可访问性强绑定，可审计。

负向断言目标: 未经审批绝不应访问受保护环境的 secret。判定证据 =（a）未审批时引用环境 secret 求值为空/阻断；（b）无绕过审批直达部署阶段的路径。
威胁类别: STRIDE-Elevation/Repudiation；OWASP CICD-03/CICD-08。
优先级线索: 建议 P1 候选（testing-focus §5；G-20 缺口）。
破坏级别:   fixture
来源输入:   using-secrets.md:63-71；spec.md G-20/C-SEC-14
```

```
意图 ID:    INTENT-SEC-031
维度标签:   [security]
标题:       验证 TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定

风险点:     security-series Part 4：审批 workflow 的 TOCTOU——管理员审批/评论触发后、执行前，攻击者推送恶意 commit，使特权运行执行新代码；`issue_comment` 触发不受 PR 审批保护。唯一有效缓解是 label gate + 固定 commit SHA（而非 head ref）。
预期系统行为: 特权触发应绑定审批时刻的具体 commit（SHA 固定），审批后推送的新 commit 不应被已授权的特权运行自动采用；评论/标签触发路径不绕过代码固定。
Oracle 来源: GitHub行为（security-series Part 4 label gate + commit SHA 缓解）+ GitCode规格（C-TRIG-04/05 评论触发；C-EXPR-05 head_ref/sha）；缺口：GitCode 是否支持 labeled activity type 待实测。

验证要点:
  - [正向] 采用固定 commit SHA 的受控触发按审批时的代码执行。
  - [负向] 审批/触发后推送的新 commit 不应被该次特权运行自动执行（避免 TOCTOU 提权）；评论触发不应绕过 PR 审批获得特权。
  - [非功能] 是否提供 label gate 等价机制可被判定（关联迁移防护建议）。

负向断言目标: 审批后推送的恶意代码绝不应被已授权特权运行执行。判定证据 = 特权运行执行的 commit 与审批时锁定的 SHA 一致，非最新 head。
威胁类别: STRIDE-Elevation/Tampering；OWASP CICD-03；CVE 类：TOCTOU / IssueOps 绕审批。
优先级线索: 建议 P1 候选（testing-focus §2/§6；security-series Part 4）。
破坏级别:   fixture
来源输入:   security-series Part 4；spec.md C-TRIG-04/05/C-EXPR-05
```

---

## 11. 覆盖自检与交接

### 11.1 角色卡强制覆盖清单核对
| 必覆盖攻击面 | 对应 intent | 状态 |
|---|---|---|
| fork PR secret 隔离 | 001,003,028 | ✅ |
| pull_request_target 滥用 | 004,018 | ✅ |
| secret masking 变形泄露 | 005,006,007,008,032 | ✅ |
| 脚本注入 | 009,010,012,013,014,024 | ✅ |
| action pin 供应链 | 021,022 | ✅ |
| cache 投毒 | 019,020,029 | ✅ |
| runner 逃逸残留 | 025,026,033 | ✅ |
| token 权限过大 | 002,015,016,017,023,036 | ✅ |
| （补充）网络隔离/SSRF | 027 | ✅ |
| （补充）审批 gate / TOCTOU | 030,031 | ✅ |

### 11.2 与 spec.md 缺口对齐（G-15~G-20 全覆盖）
- G-15 runner ephemeral/残留 → SEC-025；G-16 脱敏变形 → SEC-006/007/008；G-17 _target+checkout 注入 → SEC-018；G-18 pull_request_comment 正则注入 → SEC-014；G-19 fork cache 投毒 → SEC-019；G-20 环境保护规则 → SEC-030。
- 附带覆盖 G-06/G-21（permissions 默认/空语义）→ SEC-016/017；G-14（网络出站）→ SEC-027。

### 11.3 建议门禁定级线索汇总
- **P0 候选（8 条）**：SEC-001（fork secret 隔离）、SEC-002（fork token 降权）、SEC-004（_target 用 base workflow）、SEC-009/010（脚本注入主/隐蔽源）、SEC-018（_target checkout 注入）、SEC-019（fork cache 投毒）、SEC-028（多项目 secret 隔离）；脱敏 SEC-005/006/007 亦建议 P0（issues.md §3 定 P0）。
- 上述均对应 testing-focus 安全命脉章节；risk-register 当前模板态，最终定级交门禁按 rules §2。

### 11.4 红线合规声明
- 全文仅描述意图层攻击面与防御性验收目标，未包含可直接利用的 payload、exploit 代码或绕过步骤。
- 无真实密钥/token/内网地址，敏感值一律占位符（`DEPLOY_TOKEN` 等）。
- 每条 intent 均含明确「负向断言目标（什么不应发生）+ 确定性判定证据」。

---

> ⚠️ **人工复审建议**：本安全维度产物建议追加一名**熟悉 CI/CD 攻击面（GitHub Actions / OWASP CI/CD Top 10）的安全工程师**做人工复审，重点核对：(1) fork 隔离与 pull_request_target 的信任边界判定证据是否充分；(2) 脱敏变形与侧信道覆盖是否遗漏新型编码；(3) 多项目/多租户 Runner 隔离的破坏级别（full_instance）在受控实例上的可复位性。case-writer 展开时须严守红线，攻击 payload 仅在受控 fixture 内构造，不写入文本用例正文。
