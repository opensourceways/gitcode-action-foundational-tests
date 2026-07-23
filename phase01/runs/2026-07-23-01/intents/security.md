# 安全维度测试意图（Security Intents）

> 产出：安全 Agent（security）
> 日期：2026-07-22
> 覆盖：fork PR 隔离 / pull_request_target 滥用 / secret 日志脱敏 / 表达式注入 / 供应链 / cache&artifact 投毒 / runner 隔离 / 权限最小化 / 评论触发 / 环境审批 / 网络边界 / 侧信道
> 总量：36 条

---

## 输入退化标注

- `inputs/business-context/`：**⚠️ 仅 README.md（空模板），无实际部署模型、历史安全问题记录、迁移改造点、Runner 拓扑**。安全 Agent 对「自托管 Runner 内网部署」的攻击面评估（如 SSRF、内网跳板、跨项目隔离）依据的是 `gitcode-spec/runner-management/using-self-hosted-runners.md` 中的规格片段与 `security-knowledge/issues.md` 的通用关注点，而非真实部署数据。若后续补充 business-context，需重新审视 SEC-023、SEC-028、SEC-029 的判定证据是否需追加特定网络拓扑。

---

## 1. 信任边界图（文字描述）

### 1.1 不可信主体（攻击发起点）
- **外部 fork 贡献者**：任何人可 fork 后提 PR，触发 `pull_request` / `pull_request_target` / `pull_request_comment` 流水线——开源社区最大攻击面。
- **PR/Issue 评论者**：`issue_comment` / `pull_request_comment` 触发面，不受 PR 审批保护。
- **不可信事件负载字段**（攻击者可控）：PR 标题/正文、分支名(`head_ref`)、commit message、commit author name/email、评论正文。
- **第三方 action 作者**：`uses:` 引用的外部代码，在流水线上下文内运行，可隐式获取 token。
- **相邻项目/仓库**：多项目共享 runner 资源池时，项目 A 的 workflow 对项目 B 构成横向不可信主体。

### 1.2 敏感资产（应被保护的对象）
- 项目级 / 组织级 / 环境级 **Secret**（`${{ secrets.* }}`）。
- **ATOMGIT_TOKEN**（自动令牌，可 clone/push/评论/操作资源）。
- **Runner**（宿主/容器文件系统、`/tmp`、`$GITHUB_WORKSPACE`、内网网络位置、进程空间、环境变量）。
- **Cache / Artifact**（跨 job/run 共享数据，投毒载体与信息泄露通道）。
- **workflow 执行逻辑**（不应被不可信 PR 改写后以高权限运行）。

### 1.3 可触发的特权路径（重点监视）
- **`pull_request_target`**：base 上下文运行、有 secret + 写 token——最易被滥用（Pwn Request）。
- **`pull_request` from fork**：应强制 token 只读 + secret 隔离。
- **显式 `checkout head.sha` + 高权限上下文**：文档自承的注入点。
- **Cache 写**：fork PR 写缓存污染主分支；跨项目写缓存横向污染。
- **Artifact 传递**：不可信运行产出的 artifact 被特权运行下载执行。
- **评论触发**：`issue_comment` / `pull_request_comment` 可绕过 PR 审批。

---

## 2. 按 STRIDE 分类的攻击面扫描结果

| STRIDE 类别 | 攻击面 | 对应 intent | 覆盖数 |
|---|---|---|---|
| **S 伪装 (Spoofing)** | Action typosquatting、TOCTOU 伪装、过期 token 复用 | SEC-015, SEC-023, SEC-031 | 3 |
| **T 篡改 (Tampering)** | Workflow 文件篡改、Cache 投毒、Artifact 投毒、Action 供应链重写、写协议注入、表达式注入 | SEC-003, SEC-009~014, SEC-018~021, SEC-024, SEC-029 | 14 |
| **R 抵赖 (Repudiation)** | 环境审批 gate 绕过、评论触发审计缺失、TOCTOU 无代码固定 | SEC-026, SEC-027, SEC-030, SEC-031 | 4 |
| **I 信息泄露 (Info Disclosure)** | Fork PR secret 泄露、日志脱敏绕过、Runner 残留、侧信道、网络外泄、跨项目 secret 访问 | SEC-001, SEC-002, SEC-004~008, SEC-020~022, SEC-025, SEC-028, SEC-032, SEC-033 | 15 |
| **D 拒绝服务 (DoS)** | 大 artifact/cache 资源耗尽、恶意 workflow 资源滥用 | SEC-019, SEC-029 | 2 |
| **E 权限提升 (Elevation)** | pull_request_target 滥用、token 权限过大、permissions 声明失效、环境 secret 绕过、评论触发提权 | SEC-001~003, SEC-016, SEC-017, SEC-030, SEC-036 | 7 |

> 注：一条 intent 可跨多个 STRIDE 类别，上表按主要类别归类，覆盖数按去重 intent 计。

---

## 3. Intent 列表

### 攻击面组 A：Fork PR Secret 与 Token 隔离（P0 命脉）

```
意图 ID:    INTENT-SEC-001
维度标签:   [security]
标题:       fork PR 触发 pull_request 时不可读取项目 secrets

风险点:     外部 fork 贡献者可能在 workflow 中引用 secrets 以窃取敏感凭证（如部署密钥、API Token）。若隔离失败，任意 fork PR 均可直接获取仓库机密。
预期系统行为: 来自 fork 的 PR 触发的 pull_request 事件 workflow 中，所有项目级和组织级 secrets 对 job 不可见；引用 secrets 时返回空值或导致 job 失败。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 在 fork PR 的 workflow 中引用 secrets 时，系统返回空或安全报错，job 不崩溃
  - [负向] 运行日志中绝不应出现 secrets 占位符的原值或可还原形式
  - [非功能] 隔离机制应在所有 runner 类型（官方/自托管）上一致生效

负向断言目标: 系统绝不应将项目 secrets 的原值（或任何可还原形式）传递给 fork PR 的 job 环境；判定证据：运行日志中 secrets 相关环境变量值为空或 ***，对日志全文搜索 secret 原值命中数为 0。
威胁类别: STRIDE-Info Disclosure / Elevation；OWASP CICD-03 / CICD-05；CVE 类：fork PR secret 泄露
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md；security-knowledge/issues.md §2
```

```
意图 ID:    INTENT-SEC-002
维度标签:   [security]
标题:       pull_request_target 事件下显式 checkout 不可信 PR 代码时，secrets 与写权限仍应受控

风险点:     pull_request_target 在 base 分支上下文运行，拥有完整 secrets 和写权限；若显式 checkout PR head 代码并执行，等于在高权限上下文中运行不可信代码。历史上 GitHub 因此出现“Pwn Requests”漏洞。
预期系统行为: 系统应阻止或至少限制在 pull_request_target 中直接执行未经审核的 fork PR 代码；若允许 checkout，则应有额外隔离机制（如标签门控、手动审批）。
Oracle 来源: GitCode规格 / GitHub行为

验证要点:
  - [负向] 绝不应在无审批情况下，让 pull_request_target 的 job 直接执行 fork PR 的构建脚本并访问 secrets
  - [非功能] 若存在审批机制，未审批状态下 job 应处于挂起或拒绝态

负向断言目标: 系统绝不应允许 pull_request_target 事件在未经二次授权的情况下，将 base 分支的 secrets 暴露给 fork PR 的不可信代码；判定证据：运行日志中无 secrets 原值泄露，且 workflow 执行结果应显示权限拒绝或进入审批态。
威胁类别: STRIDE-Elevation；OWASP CICD-03；CVE 类：Pwn Request / pull_request_target 滥用
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 1/4；pr-mr-pipeline-security.md
```

```
意图 ID:    INTENT-SEC-003
维度标签:   [security]
标题:       fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限

风险点:     若 fork PR 的 ATOMGIT_TOKEN 权限未强制降级，攻击者可通过 PR 修改仓库、创建评论或操作项目资源，实现权限提升。
预期系统行为: 无论 workflow 中声明何种 permissions，来自 fork PR 的 pull_request 事件下 ATOMGIT_TOKEN 实际权限仅 read；写操作被平台强制拒绝。
Oracle 来源: GitCode规格

验证要点:
  - [正向] ATOMGIT_TOKEN 可成功执行 clone 等读操作
  - [负向] 尝试写操作（如 push、评论、修改 PR 状态）应返回 403 或失败

负向断言目标: 系统绝不应授予 fork PR 的 ATOMGIT_TOKEN 写权限；判定证据：尝试使用 token 调用写 API 时返回权限拒绝，且运行日志中 token 的 effective scope 不包含 write。
威胁类别: STRIDE-Elevation；OWASP CICD-01 / CICD-03
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/token-permissions.md；gitcode-spec/security-permissions/pr-mr-pipeline-security.md
```

---

### 攻击面组 B：Secret 日志脱敏与绕过（P0 命脉）

```
意图 ID:    INTENT-SEC-004
维度标签:   [security]
标题:       Secret 值在运行日志、step summary 和错误堆栈中必须被自动脱敏为 ***

风险点:     若 secrets 被直接打印到日志，任何有日志访问权限的人均可读取。错误堆栈或 step summary 也是泄露高发区。
预期系统行为: 任何 step 的输出（stdout、stderr、step summary、异常堆栈）中，secrets 的原值均替换为 ***。
Oracle 来源: GitCode规格

验证要点:
  - [正向] echo 或打印包含 secret 时日志显示 ***
  - [负向] 日志、summary、堆栈中绝不应出现 secret 原值

负向断言目标: 系统绝不应在运行日志、step summary、错误堆栈中输出 secrets 的原值；判定证据：下载日志全文搜索 secret 原值，命中数为 0。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：secret 日志脱敏绕过
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/using-secrets.md；security-knowledge/issues.md §3
```

```
意图 ID:    INTENT-SEC-005
维度标签:   [security]
标题:       Secret 日志脱敏不可通过 base64 编码绕过

风险点:     攻击者可能在 job 中对 secret 做 base64 编码后再输出，以逃避简单字符串匹配脱敏，随后在外部解码还原。
预期系统行为: 日志扫描机制应能识别 base64 编码后的 secret 值，或 secret 值无论以何种编码出现在日志中均被遮蔽。
Oracle 来源: GitHub行为（已知绕过模式）

验证要点:
  - [负向] base64 编码后的 secret 绝不应以明文形式出现在日志中
  - [非功能] 脱敏机制应覆盖常见编码变换（base64、urlencode、hex）

负向断言目标: 系统绝不应让 secret 的 base64 编码值以可还原形式出现在日志中；判定证据：日志中 base64 编码后的字符串与 secret 原值存在一一对应关系时应被遮蔽或拦截。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏编码绕过
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §3；security-knowledge/github-actions-security-series.md Part 2
```

```
意图 ID:    INTENT-SEC-006
维度标签:   [security]
标题:       Secret 日志脱敏不可通过字符串拼接或插值绕过

风险点:     攻击者将 secret 拆分为多段通过字符串拼接输出，每段均不命中完整的 secret 字符串，从而绕过静态匹配。
预期系统行为: 日志脱敏机制应能识别拼接后的完整 secret 值或分片值，确保无法通过日志重构原值。
Oracle 来源: GitHub行为

验证要点:
  - [负向] 拼接后的 secret 值绝不应以可还原形式出现在日志中
  - [非功能] 即使分多行、多步骤输出，也应保持脱敏一致性

负向断言目标: 系统绝不应允许通过字符串拼接/插值手段在日志中重构出 secret 原值；判定证据：日志全文搜索 secret 的任意连续子串（长度超过阈值）命中数为 0。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏分片绕过
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §3
```

```
意图 ID:    INTENT-SEC-007
维度标签:   [security]
标题:       Secret 日志脱敏不可通过多行值输出绕过

风险点:     多行 secret（如 SSH 密钥、JSON 配置）跨行输出时，行级匹配或逐行扫描可能漏掉换行后的片段。
预期系统行为: 多行 secret 的每一行或整体在日志中均被脱敏；换行符不应成为脱敏边界。
Oracle 来源: GitCode规格

验证要点:
  - [负向] 多行 secret 的任一行均不应以明文出现在日志中
  - [非功能] 脱敏引擎应支持跨行匹配或整值匹配

负向断言目标: 系统绝不应让多行 secret 的任意一行以明文出现在日志中；判定证据：使用多行占位符 secret（如 MULTI_LINE_SECRET）运行后，日志中无对应行内容。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：多行值脱敏遗漏
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §3；security-knowledge/github-actions-security-series.md Part 2
```

```
意图 ID:    INTENT-SEC-008
维度标签:   [security]
标题:       Secret 日志脱敏不可通过分片输出绕过

风险点:     攻击者逐字符或逐小段输出 secret，每段均不触发固定长度匹配，最终在外部拼合还原。
预期系统行为: 即使分片输出，secret 的各片段仍被脱敏；或分片到不可还原长度以下。
Oracle 来源: GitHub行为

验证要点:
  - [负向] secret 的分片输出绝不应在日志中保留明文
  - [非功能] 脱敏机制应设置最小匹配长度，低于该长度的片段亦应被识别或模糊化

负向断言目标: 系统绝不应允许通过逐字符/逐段输出在日志中还原 secret 原值；判定证据：日志中 secret 的任意连续子串（如 3 字符以上）命中数应为 0。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏分片绕过
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §3；security-knowledge/github-actions-security-series.md Part 2
```

---

### 攻击面组 C：表达式与脚本注入（P0 命脉）

```
意图 ID:    INTENT-SEC-009
维度标签:   [security]
标题:       不可信 PR 标题/正文不可直接插进 run 脚本导致命令注入

风险点:     PR 标题、正文来自外部贡献者，若直接内联到 run: 的 ${{ }} 中，攻击者可能注入 shell 命令，实现 secrets 窃取或仓库篡改。
预期系统行为: 系统应阻止或警告在 run: 中直接引用不可信事件字段；若执行，则表达式值应在脚本生成前完成求值并安全转义，不解释为 shell 元字符。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [负向] 含特殊字符（引号、分号、反引号、管道符）的 PR 标题绝不应被解释为 shell 命令执行
  - [非功能] 安全写法（先存入中间环境变量再引用）应正常工作

负向断言目标: 系统绝不应将 PR 标题/正文中的特殊字符解释为 shell 命令的一部分；判定证据：运行日志中无额外命令执行痕迹，且无异常外发请求记录。
威胁类别: STRIDE-Tampering / Elevation；OWASP CICD-03；CVE 类：表达式内联 shell 注入
优先级线索: RISK-SEC-02（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 2；testing-focus.md §6
```

```
意图 ID:    INTENT-SEC-010
维度标签:   [security]
标题:       不可信分支名/标签名不可直接插进 run 脚本导致命令注入

风险点:     git 分支名和标签名可包含极端字符（如引号、反斜杠、分号），直接内联到 run 脚本会导致注入。RFC 中分支名合法但 shell 危险。
预期系统行为: 同 SEC-009，事件字段值在脚本生成前完成安全求值，不触发命令执行。
Oracle 来源: GitHub行为

验证要点:
  - [负向] 含特殊字符的分支名绝不应被解释为 shell 命令
  - [非功能] 安全写法（中间环境变量）应正常生效

负向断言目标: 系统绝不应将 atomgit.head_ref 或类似上下文中含特殊字符的分支名解释为 shell 元字符；判定证据：运行日志中无由分支名触发的额外命令执行。
威胁类别: STRIDE-Tampering / Elevation；OWASP CICD-03；CVE 类：隐蔽字段 shell 注入
优先级线索: RISK-SEC-02（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 2
```

```
意图 ID:    INTENT-SEC-011
维度标签:   [security]
标题:       不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入

风险点:     issue_comment / pull_request_comment 触发时，评论 body 是攻击者可控的，直接插进 run 脚本会导致命令执行。且评论触发不受 PR 审批机制保护。
预期系统行为: 同 SEC-009，或评论触发 workflow 应对 body 做严格过滤与转义。
Oracle 来源: GitHub行为

验证要点:
  - [负向] 含 shell 元字符的评论内容绝不应被解释为命令执行
  - [非功能] 即使评论被编辑，重新触发时仍应维持安全过滤

负向断言目标: 系统绝不应将 atomgit.event.comment.body 中的 shell 元字符解释为命令执行；判定证据：运行日志中无由评论内容触发的额外命令执行。
威胁类别: STRIDE-Tampering / Elevation；OWASP CICD-03；CVE 类：IssueOps 注入
优先级线索: RISK-SEC-02（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 2/4；testing-focus.md §6
```

```
意图 ID:    INTENT-SEC-012
维度标签:   [security]
标题:       不可信 commit message / author email 不可直接插进 run 脚本导致命令注入

风险点:     commit message 和 author email 格式极端灵活（RFC 5322 允许反引号等），可被构造为注入载荷。push 事件触发时这些字段进入事件上下文。
预期系统行为: 同 SEC-009，事件字段值在脚本生成前完成安全求值。
Oracle 来源: GitHub行为

验证要点:
  - [负向] 含反引号或分号的 commit message 绝不应被解释为命令执行
  - [非功能] 安全写法（中间环境变量）应正常生效

负向断言目标: 系统绝不应将 commit message 或 author email 中的 shell 元字符解释为命令执行；判定证据：运行日志中无由 commit 信息触发的额外命令执行。
威胁类别: STRIDE-Tampering / Elevation；OWASP CICD-03；CVE 类：隐蔽字段 shell 注入
优先级线索: RISK-SEC-02（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 2
```

```
意图 ID:    INTENT-SEC-013
维度标签:   [security]
标题:       表达式求值必须防止双重模板渲染（二次求值）

风险点:     某些 Action 内部使用模板引擎（如 lodash），攻击者输入 {{ 1 + 1 }} 在外层 ${{ }} 求值后，被内层模板引擎二次求值，导致任意代码执行。
预期系统行为: 外层 ${{ }} 求值结果中的模板语法字符应被转义，不再触发内层模板引擎求值。
Oracle 来源: GitHub行为

验证要点:
  - [负向] 含模板语法的外部输入绝不应在内层 Action 中被二次求值
  - [非功能] 二次求值若无法避免，应至少被沙箱化

负向断言目标: 系统绝不应允许 ${{ }} 求值结果中的模板元字符在内层 Action 或插件中被二次求值；判定证据：输入包含 {{ ... }} 时，运行日志中无异常计算结果或代码执行痕迹。
威胁类别: STRIDE-Tampering / Elevation；OWASP CICD-03；CVE 类：双重模板求值
优先级线索: RISK-SEC-02（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 2
```

---

### 攻击面组 D：第三方 Action 供应链

```
意图 ID:    INTENT-SEC-014
维度标签:   [security]
标题:       第三方 Action 引用应支持完整 commit hash 固定

风险点:     若仅支持 branch/tag 引用，攻击者可通过重 tag 或推送恶意 commit 到 branch 污染供应链，导致所有使用该 action 的仓库被入侵。
预期系统行为: uses: 语法支持通过完整 commit SHA 固定 action 版本，且解析后不可被浮动引用覆盖。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [正向] 完整 commit SHA 引用可成功执行 action
  - [负向] commit SHA 不匹配或分支被重写时，job 应失败或拒绝执行

负向断言目标: 系统绝不应在 commit SHA 已改变或被重写时仍执行旧/恶意的 action 代码；判定证据：当引用的 commit SHA 与仓库实际 HEAD 不一致时，job 进入失败状态。
威胁类别: STRIDE-Tampering；OWASP CICD-02 / CICD-10；CVE 类：可变 tag 重写供应链攻击
优先级线索: RISK-SEC-02（供应链）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 3
```

```
意图 ID:    INTENT-SEC-015
维度标签:   [security]
标题:       第三方 Action 来源应具备信任边界（typosquatting / 未审核 Action 限制）

风险点:     攻击者注册与知名 action 相似的名称（typosquatting），或向 marketplace 上传恶意 action，用户 typo 后执行恶意代码。
预期系统行为: 非官方 Action 在首次使用时应触发警告或需管理员审批；Action 名称解析应防止近源混淆。
Oracle 来源: 差异声明

验证要点:
  - [负向] 与官方 action 名称高度相似的恶意 Action 绝不应被静默解析为合法来源
  - [非功能] 首次使用未审核 Action 时应留下审计记录

负向断言目标: 系统绝不应在无提示的情况下执行来自未审核来源的 Action，也不应将 typosquatting 名称解析为合法仓库；判定证据：使用近似名称的 Action 触发时，运行结果报“Action 未找到”或进入审批态。
威胁类别: STRIDE-Spoofing / Tampering；OWASP CICD-02 / CICD-07
优先级线索: RISK-SEC-02（供应链）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 3；security-knowledge/issues.md §2
```

---

### 攻击面组 E：Token 权限与最小化

```
意图 ID:    INTENT-SEC-016
维度标签:   [security]
标题:       显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN

风险点:     若 permissions 声明仅为语法糖，实际未限制 ATOMGIT_TOKEN 的权限，则最小权限原则失效，攻击者可通过过度授权 token 修改仓库或泄露数据。
预期系统行为: 当 workflow 或 job 级显式声明 permissions: repository: read 时，ATOMGIT_TOKEN 实际无法执行写操作；token 的 effective scope 与声明严格一致。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 声明 read 时读操作（clone、API 读取）成功
  - [负向] 声明 read 时写操作（push、评论、修改 PR）返回 403 或失败

负向断言目标: 系统绝不应在显式收窄 permissions 后仍授予 ATOMGIT_TOKEN 超出声明范围的权限；判定证据：调用超出声明范围的 API 时返回权限拒绝，且运行日志中 token 的 effective scope 与声明一致。
威胁类别: STRIDE-Elevation；OWASP CICD-01
优先级线索: RISK-SEC-01 / RISK-SEC-02
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/token-permissions.md
```

```
意图 ID:    INTENT-SEC-017
维度标签:   [security]
标题:       未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）

风险点:     默认权限过大将导致所有 workflow 在无感知情况下拥有写权限，极大增加攻击面；任何被入侵的 action 或注入均可直接修改仓库。
预期系统行为: 未声明 permissions 时，ATOMGIT_TOKEN 默认仅拥有仓库 read 权限及必要的元数据读权限；写操作被平台拒绝。
Oracle 来源: GitCode规格 / 差异声明

验证要点:
  - [负向] 默认状态下 ATOMGIT_TOKEN 绝不应拥有写权限
  - [非功能] 默认权限应在组织级可配置为更严格（如 none）

负向断言目标: 系统绝不应在未声明 permissions 的情况下授予 ATOMGIT_TOKEN 写权限；判定证据：在无任何 permissions 声明的 workflow 中，尝试 push 或修改 PR 均返回权限拒绝。
威胁类别: STRIDE-Elevation；OWASP CICD-01
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/token-permissions.md；security-knowledge/github-actions-security-series.md Part 3
```

---

### 攻击面组 F：Cache & Artifact 投毒

```
意图 ID:    INTENT-SEC-018
维度标签:   [security]
标题:       fork PR 写入的 cache 必须不可被主仓后续 workflow 读取

风险点:     攻击者通过 fork PR 向缓存写入恶意依赖或构建产物，主仓后续 build 读取后导致供应链投毒。即使 token 无写权限，cache 写权限仍可能开放。
预期系统行为: fork PR 的 cache 写入应隔离在 fork 命名空间下，主仓 workflow 的 restore 不可命中该缓存；缓存键应带仓库级隔离前缀。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [负向] 主仓 workflow 在 fork PR 写入 cache 后，绝不应命中到该缓存
  - [非功能] 缓存命中率监控应显示跨仓库命中为 0

负向断言目标: 系统绝不应让主仓 workflow 的 cache restore 命中由 fork PR 写入的缓存键；判定证据：主仓后续运行日志中 cache restore 为 miss，且缓存命中率监控中无跨仓库命中记录。
威胁类别: STRIDE-Tampering；OWASP CICD-06 / CICD-10；CVE 类：cache 投毒 / TOCTOU
优先级线索: RISK-SEC-01 / RISK-SEC-02（P0 blocker）
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 4；testing-focus.md §8；parity-matrix.md cache fork 隔离（❓）
```

```
意图 ID:    INTENT-SEC-019
维度标签:   [security]
标题:       fork PR 上传的 artifact 必须不可被主仓 workflow 下载或执行

风险点:     攻击者通过 fork PR 上传被污染的 artifact（如恶意编译产物、篡改的测试报告），主仓后续 job 或 workflow 下载后执行，实现投毒或权限提升。
预期系统行为: fork PR 的 artifact 与主仓 artifact 在命名空间上隔离；主仓不可通过 artifact ID 下载 fork PR 的 artifact。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [负向] 主仓 workflow 绝不应能下载到 fork PR 上传的 artifact
  - [非功能] 跨仓库 artifact 下载应返回 404 或权限拒绝，不应静默返回空包

负向断言目标: 系统绝不应允许主仓 workflow 通过 artifact 下载 API 获取到 fork PR 上传的制品；判定证据：主仓 job 尝试下载 fork PR 的 artifact ID 时返回 404 或权限拒绝。
威胁类别: STRIDE-Tampering / DoS；OWASP CICD-10；CVE 类：artifact 投毒 / workflow_run 链式攻击
优先级线索: RISK-SEC-01 / RISK-SEC-02
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 4；testing-focus.md §8
```

---

### 攻击面组 G：Runner 隔离与残留

```
意图 ID:    INTENT-SEC-020
维度标签:   [security]
标题:       Job 结束后 workspace 与临时文件必须被彻底清理，防止跨 job 敏感信息泄露

风险点:     上一 job 写入的敏感文件（如 .env、临时密钥、编译缓存）若未被清理，下一 job 或后续 run 可能读取，导致跨 job 信息泄露。
预期系统行为: 每个 job 的 workspace 在结束时（无论成功/失败）均执行清理，后续 job 无法访问前一 job 的残留文件。
Oracle 来源: GitCode规格 / 差异声明

验证要点:
  - [负向] job B 绝不应能读取到 job A 残留的敏感文件
  - [非功能] 即使 job A 异常崩溃，清理钩子仍应执行

负向断言目标: 系统绝不应让同一 run 中的后续 job 或后续 run 读取到前一个 job 的 workspace 残留文件；判定证据：在 job B 中搜索 job A 的临时文件路径，结果为不存在或为空。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06；CVE 类：runner 复用残留泄露
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §4；testing-focus.md §4
```

```
意图 ID:    INTENT-SEC-021
维度标签:   [security]
标题:       Runner 环境变量与共享目录（/tmp 等）必须跨 job 隔离

风险点:     环境变量或 /tmp 目录中的敏感数据在 job 之间共享，导致跨 job 信息泄露；自托管 runner 尤其容易因残留而暴露。
预期系统行为: 每个 job 的环境变量和共享目录（如 /tmp）在 job 启动时为干净状态，不受前一 job 污染；job 结束后全局环境变量被重置。
Oracle 来源: GitCode规格

验证要点:
  - [负向] job B 绝不应继承到 job A 设置的环境变量或 /tmp 残留
  - [非功能] 自托管 runner 上应执行与官方 runner 同等级别的清理

负向断言目标: 系统绝不应让 job B 的环境变量或共享目录中包含 job A 设置的敏感值；判定证据：job B 启动后检查环境变量和 /tmp，无前序 job 的敏感残留。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §1/§4；testing-focus.md §4
```

```
意图 ID:    INTENT-SEC-022
维度标签:   [security]
标题:       自托管 Runner 跨项目残留必须被隔离，防止项目间信息泄露

风险点:     多项目共享同一批自托管 runner 时，项目 A 的 workflow 残留文件/环境变量被项目 B 继承，导致跨项目 secret 泄露或环境污染。
预期系统行为: 自托管 runner 在 job 结束后应彻底清理 workspace 和全局状态，不同项目的 job 之间不可见残留。
Oracle 来源: GitCode规格 / 差异声明

验证要点:
  - [负向] 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量
  - [非功能] runner 清理失败时应标记为不可用，避免调度下一 job

负向断言目标: 系统绝不应让项目 B 的 workflow 读取到项目 A 在 runner 上留下的任何文件或环境变量；判定证据：项目 B job 中搜索项目 A 的临时文件路径，结果为不存在。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-06；CVE 类：多租户隔离失效
优先级线索: RISK-SEC-01
破坏级别:   full_instance
来源输入:   security-knowledge/issues.md §1；testing-focus.md §4
```

---

### 攻击面组 H：网络与环境安全

```
意图 ID:    INTENT-SEC-023
维度标签:   [security]
标题:       Runner 网络出站必须受控，防止 SSRF 与内网跳板

风险点:     在自托管或共享 runner 上，恶意 workflow 可访问内部元数据端点（如 169.254.169.254）、内网服务或外泄数据，将 runner 变为内网跳板。
预期系统行为: 官方 runner 应有出站网络策略限制，默认不可访问内部网络地址或特定内网域名；自托管 runner 文档应明确网络防火墙要求。
Oracle 来源: 差异声明

验证要点:
  - [负向] Runner 绝不应能访问内网元数据端点或内部服务
  - [非功能] 访问尝试应返回超时或连接拒绝，不应产生可识别的内部服务响应

负向断言目标: 系统绝不应让 workflow 的 job 通过 runner 访问内网敏感地址或元数据端点；判定证据：访问尝试返回超时或连接拒绝，运行日志中无外发成功记录。
威胁类别: STRIDE-Info Disclosure / Elevation；OWASP CICD-09；SSRF 类
优先级线索: RISK-SEC-02
破坏级别:   full_instance
来源输入:   security-knowledge/issues.md §5；testing-focus.md §4；inputs/dimensional-coverage-gaps/README.md 维度3
```

---

### 攻击面组 I：输入处理与命名安全

```
意图 ID:    INTENT-SEC-024
维度标签:   [security, compatibility]
标题:       Secret/变量名含特殊字符（如中划线）时不可导致意外求值或权限绕过

风险点:     变量名含中划线时，shell 中 ${MY-VAR} 被解释为 ${MY} 减 ${VAR}，可能导致 secret 值被错误解析或暴露到日志；也可能引发 bad substitution 错误导致信息泄露。
预期系统行为: 含中划线的 secret/变量名在表达式求值和 shell 传递时应被正确处理，不触发错误解析或值泄露。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [负向] 含中划线的 secret 绝不应因解析错误而被泄露到日志或环境变量
  - [非功能] 若不支持中划线，应在 YAML 校验阶段报错，而非运行期静默失败

负向断言目标: 系统绝不应因 secret/变量名含中划线而导致值被错误展开或泄露到日志；判定证据：运行日志中无由解析错误产生的部分 secret 值，且 job 不因此异常失败导致敏感信息暴露。
威胁类别: STRIDE-Info Disclosure / Tampering；OWASP CICD-05
优先级线索: RISK-SEC-02
破坏级别:   fixture
来源输入:   inputs/dimensional-coverage-gaps/README.md 维度3（历史 #38）
```

```
意图 ID:    INTENT-SEC-025
维度标签:   [security]
标题:       通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时，日志中必须保持脱敏

风险点:     即使 secrets 未主动 echo，攻击者仍可在 job 中执行 printenv 或读取 /proc/self/environ 获取环境变量；若日志中保留这些输出，则等同于泄露。
预期系统行为: printenv 等环境变量枚举命令的输出在日志中，所有 secrets 值必须显示为 *** 或空值；环境变量本身的存在性不影响脱敏。
Oracle 来源: GitCode规格

验证要点:
  - [负向] printenv 输出到日志时，secret 值必须被脱敏，绝不应保留原值
  - [非功能] 即使通过 env | grep 过滤，过滤后的值也应被脱敏

负向断言目标: 系统绝不应让 printenv 或类似环境变量枚举命令的输出在日志中保留 secrets 原值；判定证据：运行日志中 printenv 输出对应行显示 *** 或空值，对日志全文搜索 secret 原值命中数为 0。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏侧信道绕过
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 2；security-knowledge/issues.md §2
```

---

### 攻击面组 J：触发器与审批安全

```
意图 ID:    INTENT-SEC-026
维度标签:   [security]
标题:       issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过

风险点:     攻击者可能在评论中插入伪装的关键字（如 /deploy 包裹在 markdown 代码块中）触发 workflow，或在执行前推送恶意代码（TOCTOU）。评论触发还不受 PR 审批机制保护。
预期系统行为: 评论触发 workflow 时，关键字过滤应精确匹配，且不应被 markdown 格式、HTML 注释或字符串拼接绕过。
Oracle 来源: GitCode规格 / 差异声明

验证要点:
  - [负向] 伪装在代码块或注释中的关键字绝不应触发 workflow
  - [非功能] 触发记录应包含评论原始内容哈希，用于审计

负向断言目标: 系统绝不应让被 markdown 代码块、HTML 注释或字符串拼接伪装的关键字触发评论型 workflow；判定证据：评论内容虽含关键字但处于代码块内时，workflow 不被触发。
威胁类别: STRIDE-Tampering / Repudiation；OWASP CICD-03 / CICD-08；CVE 类：TOCTOU / IssueOps 绕审批
优先级线索: RISK-SEC-02
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 4；testing-focus.md §6
```

```
意图 ID:    INTENT-SEC-027
维度标签:   [security]
标题:       环境级 secret 必须经审批后才能被 workflow 访问

风险点:     环境级 secret（如生产部署密钥）若无需审批即可被任意 workflow 使用，则存在越权部署风险；攻击者一旦入侵 workflow 即可直接操作生产环境。
预期系统行为: 配置了环境审批规则的 secret，在审批人未批准前，workflow job 无法读取；审批记录应留痕。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 审批后 secret 可被正常引用，job 成功执行
  - [负向] 审批前 workflow 绝不应读取到环境 secret 的值

负向断言目标: 系统绝不应在审批人未批准的情况下将环境级 secret 的值传递给 workflow job；判定证据：审批前 job 的 secret 引用为空或运行失败，审批后恢复正常。
威胁类别: STRIDE-Elevation / Repudiation；OWASP CICD-03 / CICD-08
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/using-secrets.md
```

---

### 攻击面组 K：Workflow 命令与特殊机制

```
意图 ID:    INTENT-SEC-028
维度标签:   [security]
标题:       Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

风险点:     GitHub Actions 历史上 ::add-mask:: 命令的响应可能包含被遮蔽前的值，导致日志中既执行了脱敏又泄露了原值。
预期系统行为: 执行 ::add-mask:: 或等价 workflow 命令时，命令的响应/回显中不应包含待遮蔽的原始值；命令执行与日志输出应原子性脱敏。
Oracle 来源: GitHub行为

验证要点:
  - [负向] workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值
  - [非功能] 命令执行日志应仅显示命令骨架，不含 payload

负向断言目标: 系统绝不应在 workflow 命令的响应或日志回显中输出待遮蔽的 secret 原值；判定证据：日志中 ::add-mask:: 相关行仅显示命令本身，无 secret 原值。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：add-mask 响应泄露
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   security-knowledge/issues.md §3
```

```
意图 ID:    INTENT-SEC-029
维度标签:   [security]
标题:       跨运行 artifact 必须被视为不可信数据（artifact 投毒防护）

风险点:     恶意 PR 上传被污染的 artifact，特权后续运行（workflow_run 等价链式场景）下载后未校验即使用——artifact 投毒。GitCode 是否有等价特权链取决于其触发模型，但「下游消费上游 artifact」的信任问题通用。
预期系统行为: 不同信任级别运行间的 artifact 传递有清晰边界；来自不可信（fork PR）运行的 artifact 不应被特权运行隐式信任消费。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [正向] 同信任级别运行间 artifact 正常传递使用。
  - [负向] 不可信运行产出的 artifact 不应在特权运行中被自动信任/执行；下游对 artifact 内容应可校验来源。
  - [非功能] artifact 来源/信任级别可被判定。

负向断言目标: 不可信来源的 artifact 绝不应被特权运行隐式信任执行。判定证据 =（a）特权运行不自动执行 artifact 内容；（b）artifact 来源可追溯至其产出运行的信任级别。
威胁类别: STRIDE-Tampering / DoS；OWASP CICD-10；CVE 类：artifact 投毒 / workflow_run 链式攻击
优先级线索: RISK-SEC-02
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 4；testing-focus.md §8
```

---

### 攻击面组 L：侧信道与环境变量注入

```
意图 ID:    INTENT-SEC-030
维度标签:   [security]
标题:       工作流写协议（ATOMGIT_ENV/OUTPUT/PATH）不被不可信输入污染提权

风险点:     >> $ATOMGIT_ENV / $ATOMGIT_OUTPUT / $ATOMGIT_PATH 文件协议若被不可信输入注入多行内容，可污染后续 step 的环境变量或 PATH，进而劫持后续命令——GitHub 同类 GITHUB_ENV 注入漏洞模式。
预期系统行为: 不可信值写入这些协议文件时不应能注入额外环境变量/PATH 条目；多行/换行注入被安全处理。
Oracle 来源: GitHub行为 / GitCode规格

验证要点:
  - [负向] 含换行/协议控制字符的不可信值写入 ATOMGIT_ENV/OUTPUT/PATH 时，不应注入计划外的环境变量、output 或 PATH 条目劫持后续 step。
  - [非功能] 多行值应经随机 delimiter 等机制安全写入。

负向断言目标: 不可信输入绝不应经写协议文件注入环境变量/PATH 劫持后续步骤。判定证据 = 后续 step 环境/PATH 无注入条目；被劫持命令未执行。
威胁类别: STRIDE-Tampering / Elevation；OWASP CICD-03；CVE 类：GITHUB_ENV/PATH 注入
优先级线索: RISK-SEC-02
破坏级别:   fixture
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md；testing-focus.md §6
```

```
意图 ID:    INTENT-SEC-031
维度标签:   [security]
标题:       TOCTOU：审批后推送新 commit / 评论触发不绕过审批与代码固定

风险点:     审批 workflow 的 TOCTOU——管理员审批/评论触发后、执行前，攻击者推送恶意 commit，使特权运行执行新代码；issue_comment 触发不受 PR 审批保护。唯一有效缓解是 label gate + 固定 commit SHA（而非 head ref）。
预期系统行为: 特权触发应绑定审批时刻的具体 commit（SHA 固定），审批后推送的新 commit 不应被已授权的特权运行自动采用；评论/标签触发路径不绕过代码固定。
Oracle 来源: GitHub行为 / 差异声明

验证要点:
  - [正向] 采用固定 commit SHA 的受控触发按审批时的代码执行。
  - [负向] 审批/触发后推送的新 commit 不应被该次特权运行自动执行（避免 TOCTOU 提权）；评论触发不应绕过 PR 审批获得特权。
  - [非功能] 是否提供 label gate 等价机制可被判定（关联迁移防护建议）。

负向断言目标: 审批后推送的恶意代码绝不应被已授权特权运行执行。判定证据 = 特权运行执行的 commit 与审批时锁定的 SHA 一致，非最新 head。
威胁类别: STRIDE-Elevation / Tampering / Repudiation；OWASP CICD-03；CVE 类：TOCTOU / IssueOps 绕审批
优先级线索: RISK-SEC-02
破坏级别:   fixture
来源输入:   security-knowledge/github-actions-security-series.md Part 4；testing-focus.md §2/§6
```

```
意图 ID:    INTENT-SEC-032
维度标签:   [security]
标题:       Secret 不经 output / artifact / step summary 侧信道绕过脱敏外泄

风险点:     日志脱敏之外的输出通道（ATOMGIT_OUTPUT、artifact、ATOMGIT_STEP_SUMMARY）若不做同等遮蔽，被攻陷步骤可把 secret 写入这些侧信道外泄——脱敏只覆盖日志则形同虚设。
预期系统行为: Secret 若被写入 output/artifact/step summary，应被遮蔽或该风险被明确记录并有补偿控制；不应存在「日志遮了但 summary 明文」的缺口。
Oracle 来源: GitCode规格 / 差异声明

验证要点:
  - [负向] Secret 明文不应以未遮蔽形式出现在 step summary、job output 或上传的 artifact 中。
  - [非功能] 覆盖 output/summary/artifact 三条侧信道。

负向断言目标: Secret 绝不应经 output/artifact/step summary 侧信道以明文外泄。判定证据 = 三类产物中 grep 占位 secret 原值命中数为 0；若命中，登记为缺陷。
威胁类别: STRIDE-Info Disclosure；OWASP CICD-05；CVE 类：脱敏侧信道绕过
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   gitcode-spec/syntax-reference/workflow-commands.md；security-knowledge/github-actions-security-series.md Part 2
```

```
意图 ID:    INTENT-SEC-033
维度标签:   [security]
标题:       大 artifact / 大 cache 必须受配额与边界限制，防止资源耗尽型攻击

风险点:     攻击者通过上传超大 artifact 或写入超大 cache 消耗共享存储配额，导致平台服务降级或拒绝服务；也可能利用大文件传递隐藏恶意载荷。
预期系统行为: artifact 与 cache 应有大小上限、保留期上限与配额限制；超限上传应被拦截或报错，不应导致平台级降级。
Oracle 来源: GitCode规格 / 差异声明

验证要点:
  - [负向] 超过大小上限的 artifact/cache 上传绝不应成功写入
  - [非功能] 超限时应给出明确报错（大小限制值），不应静默截断或卡死

负向断言目标: 系统绝不应允许无限制大小的 artifact/cache 上传导致资源耗尽或平台降级；判定证据：超限上传返回明确大小限制错误，且平台存储监控无异常膨胀。
威胁类别: STRIDE-DoS / Tampering；OWASP CICD-06 / CICD-10
优先级线索: RISK-SEC-02
破坏级别:   fixture
来源输入:   gitcode-spec/core-concepts/artifacts-and-cache.md；parity-matrix.md upload-artifact（🟡）
```

```
意图 ID:    INTENT-SEC-034
维度标签:   [security, compatibility]
标题:       OIDC / 短时凭据支持若缺失，必须明确标注为平台限制并提供替代安全方案

风险点:     云部署场景需要 short-lived token（如 AWS/GCP/Azure OIDC 集成）。若不支持 OIDC，用户可能被迫在 secrets 中存储长期云凭证，增加泄露后的影响面。
预期系统行为: 若支持 OIDC，则 token 应有严格生命周期（如 <5 分钟）且一次性使用；若不支持，文档应明确标注，并建议使用最小权限的长期 token + 定期轮换。
Oracle 来源: 差异声明

验证要点:
  - [负向] 不支持 OIDC 时，系统绝不应提供可长期复用的高权限云部署凭证作为默认方案
  - [非功能] 若支持，应提供审计日志追踪 OIDC token 的签发与使用

负向断言目标: 系统绝不应在缺少 OIDC 支持的情况下，默认可通过长期 token 进行云部署而不提供替代安全机制；判定证据：文档中明确标注 OIDC 不支持，或 OIDC token 确实具备短时效与一次性。
威胁类别: STRIDE-Info Disclosure / Elevation；OWASP CICD-05
优先级线索: RISK-SEC-01（若支持则 P0，若不支持则 P1 缺口）
破坏级别:   none
来源输入:   inputs/dimensional-coverage-gaps/README.md 维度1/3；testing-focus.md §5
```

```
意图 ID:    INTENT-SEC-035
维度标签:   [security]
标题:       验证 pull_request_target 使用 base 分支的 workflow 版本（PR 提交者不能改执行逻辑）

风险点:     pull_request_target 在 base 上下文运行、有完整 secret 与写 token。其安全前提是「执行逻辑来自目标仓库 base 分支，PR 提交者无法修改」。若平台错用了 fork 分支的 workflow 文件，则外部人可在高权限上下文注入任意逻辑——Pwn Request。
预期系统行为: pull_request_target 触发时，加载并执行 base 分支中的 workflow 文件版本，忽略 fork PR 对 workflow 文件的任何修改。
Oracle 来源: GitCode规格

验证要点:
  - [正向] base 分支 workflow 按其定义执行，可访问 secret 与写 token。
  - [负向] fork PR 分支内对 workflow 文件的改动（新增窃密/提权步骤）不得被 pull_request_target 运行采用。
  - [非功能] 该来源选择由平台强制，非用户可配。

负向断言目标: pull_request_target 绝不应执行来自不可信 fork 的 workflow 定义。判定证据 =（a）运行采用的 workflow 内容哈希/步骤集与 base 分支一致，与 fork PR 改动不一致；（b）fork PR 注入的步骤未出现在执行记录中。
威胁类别: STRIDE-Elevation；OWASP CICD-03；CVE 类：Pwn Request
优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md；security-knowledge/github-actions-security-series.md Part 1/4
```

```
意图 ID:    INTENT-SEC-036
维度标签:   [security]
标题:       ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

风险点:     内置 token 默认权限范围是最小权限落地的基线。默认过宽或 job 级覆盖不生效，都会导致特权面失控。
预期系统行为: 默认 token 权限范围可被确定枚举；顶层与 job 级 permissions 的继承/覆盖语义（job 级收窄生效）符合文档。
Oracle 来源: GitCode规格

验证要点:
  - [正向] 顶层声明被各 job 继承；job 级声明覆盖顶层。
  - [负向] job 级收窄后不应仍保留顶层的更大权限；默认权限不应包含未声明的写域。
  - [非功能] 权限范围与覆盖关系可被观测判定。

负向断言目标: token 绝不应持有超出（顶层∩job级）有效声明的权限。判定证据 = 各权限域实测与有效声明一致，越权写被拒。
威胁类别: STRIDE-Elevation；OWASP CICD-01
优先级线索: RISK-SEC-01
破坏级别:   fixture
来源输入:   gitcode-spec/security-permissions/token-permissions.md；security-knowledge/issues.md §2
```

---

## 4. 覆盖自检与质量清单

- [x] 每条 intent 有明确的「不应发生」负向目标。
- [x] fork PR / pull_request_target / secret masking（含 base64/拼接/多行/分片）/ 脚本注入 / action pin / cache 投毒 / artifact 投毒 / runner 残留 / 网络隔离 / 权限最小化 / 评论触发 / 环境审批 / 侧信道 / OIDC 缺口 / TOCTOU 均有覆盖。
- [x] 每条给出确定性判定证据（日志不含明文、权限拒绝、404/403、缓存 miss 等）。
- [x] 未出现真实密钥/token/内网地址，均使用占位符或描述性语言。
- [x] 未包含可直接利用的攻击 payload、exploit 代码或绕过步骤。
- [x] 已标注输入退化（business-context 为空模板）。

> **人工复审建议**：请具备 CI/CD 攻击面经验的工程师对以下命脉 intent 做重点复审——INTENT-SEC-001（fork PR secret 隔离）、INTENT-SEC-002（pull_request_target 滥用防护）、INTENT-SEC-009（表达式注入）。这 3 条直接对应 RISK-SEC-01/02 的 P0 blocker，需确保判定证据在真实环境中可观测、可自动化断言。
