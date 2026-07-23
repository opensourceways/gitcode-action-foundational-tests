# Security Test Intents

> **Agent**: security (STRIDE / CI/CD attack-surface mapper)
> **Run**: 2026-07-21-01
> **输入快照**:
> - gitcode-spec/security-permissions/ (token-permissions.md, pr-mr-pipeline-security.md, using-secrets.md)
> - github-reference/security/ (secrets.md, pull_request_target.md, script-injections.md, secure-use.md, github-token.md)
> - **★ NEW**: security-knowledge/github-actions-security-series.md (GitHub Security Lab 4-part series)
> - **★ NEW**: security-knowledge/issues.md (known security risks from testing)
> - **★ NEW**: history/ (historical defects: issues-encountered.md, gitcode-actions-list.md)
> - testing-focus.md §2,5,6,7,8
> - baseline/risk-register.md, baseline/parity-matrix.md, baseline/quality-gate.md
> - existing-cases/cases.md (631 test cases)
> - **基始参考**: run 2026-07-20-01 intents/security.md (36 intents, SEC-001 to SEC-036)
> **变更摘要**:
> - CARRIED OVER: SEC-001 to SEC-036 (36 intents, 更新 source annotations)
> - **★ NEW (enabled by security-knowledge): SEC-037 to SEC-049 (13 intents)** — TOCTOU, workflow_run manipulation, double expression eval, email injection, multi-project isolation, secret lifecycle, log security, network isolation
> - **★ NEW (enabled by history/): SEC-050 to SEC-053 (4 intents)** — regression testing for confirmed real bugs (#51, #66, #85, #82)
> - **★ NEW (cross-referencing security series): SEC-054 to SEC-056 (3 intents)** — pull_request_target cache enforcement, action input token default abuse, runner cleanup for self-hosted
> **人工复审建议**: 建议由具备 CI/CD 攻击面知识的 reviewer 逐条审阅后签出（见 agent 护栏第 4 条）。

---

## 信任边界总览

| 主体/资产 | 信任级别 | 说明 |
|-----------|----------|------|
| 外部 fork 贡献者 | **不可信** | 任何人可 fork 并提 PR，触发 workflow，控制 fork 仓库中的 workflow YAML 和执行代码 |
| 仓库 owner/maintainer | 可信 | 有 push 权限，可修改目标仓库 workflow 与 secret 配置 |
| PR 标题/正文/分支名 | **不可信** | 完全由外部贡献者控制，可能包含任意字符串 |
| 提交信息/commit message | **不可信** | fork 侧可控 |
| 提交者 email / author name | **不可信** | RFC 5322 允许极端灵活格式，可嵌入 shell 元字符（新增） |
| ATOMGIT_TOKEN | **敏感资产** | 自动生成的认证令牌，权限由 permissions 声明决定 |
| 项目/组织级 Secret | **敏感资产** | 需严格隔离，不可对不可信主体暴露 |
| Runner 工作区 | **敏感资产** | 执行环境，fork PR 代码不应获得写回权限 |
| Cache | **敏感资产** | 跨 run 共享的缓存，不可被 fork PR 污染 |
| Artifact | **敏感资产** | 跨 job 传递的产物 |
| 共享文件系统 (/tmp 等) | **敏感资产** | 跨 job 可见的共享目录，可残留敏感文件（新增） |
| 内网/内部服务 | **敏感资产** | 若 runner 可访问内网，SSRF 攻击面（新增） |

**核心信任边界线**: fork PR (`pull_request` 事件) 与内部事件 (`push` / `pull_request_target`) 之间存在一条硬隔离边界——前者应被视作完全不可信输入。所有安全 intent 最终都围绕「这条边界是否被正确执行」展开。

---

## PART A — CARRIED OVER (从 2026-07-20-01 继承，更新 source)

> 以下 36 条 intent 来自上一轮 run，已对照新输入确认仍然适用。source 标注已更新以反映新增的 security-knowledge 和 history 交叉引用。每条 carry-over 不改变原 ID 和 intent 语义，仅补充新知识来源的关联。

```
意图 ID:    INTENT-SEC-001
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       fork PR 触发 pull_request 时 ATOMGIT_TOKEN 应为只读

风险点:     外部贡献者通过 fork 提 PR，触发 `pull_request` 事件。若 ATOMGIT_TOKEN 保有写权限，恶意 PR 可修改仓库代码、操作 Issue/PR、推送标签，相当于代码执行+仓库接管。这是 CI/CD 最经典的攻击面之一。
预期系统行为: 来自 fork 的 `pull_request` 事件下，ATOMGIT_TOKEN 仅拥有 `repository: read` 权限，无论 workflow 中 permissions 声明为何。任何写操作（推送、PR 评论、Issue 创建、Webhook 管理）均应被拒绝。
Oracle 来源: GitCode 规格 (token-permissions.md) 对齐 GitHub 行为 (secrets.md)。

验证要点:
  - [正向] fork PR 触发的 job 可正常 clone 代码 (repository:read)
  - [负向] fork PR 触发的 job 不应能推送代码到目标仓库 (repository:write 应被拒绝)
  - [负向] fork PR 触发的 job 不应能通过 API 创建/修改 PR 评论 (pr:write 应被拒绝)
  - [负向] fork PR 触发的 job 不应能读取项目级 Secret

负向断言目标: ATOMGIT_TOKEN 在 fork `pull_request` 场景下仅具 read 权限。判定证据：job 日志中 git push 输出含 "Permission denied" 或 "403"；${{ secrets.X }} 值为空。
优先级线索: RISK-SEC-01 (P0 blocker)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/, github-reference/security/secrets.md, security-knowledge/github-actions-security-series.md (Part 1), history/issues-encountered.md (#51)
```

---

```
意图 ID:    INTENT-SEC-002
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       fork PR 触发 pull_request 时不可访问项目/组织级 Secret

风险点:     若 Secret 对 fork PR 可见，攻击者只需在 fork 的 workflow 中 echo 任意 Secret 即可窃取凭证。history #51 已证实「fork 仓提 PR 能够获取到主仓的密钥」为真实 bug——这是已确认的安全漏洞，需要回归测试。
预期系统行为: `pull_request` 来自 fork 时，workflow 对 `${{ secrets.* }}` 的引用应返回空字符串或触发错误，绝不应暴露 secret 原始值。
Oracle 来源: GitCode 规格 (using-secrets.md) 对齐 GitHub 行为。

验证要点:
  - [负向] fork PR workflow 中 echo 项目级 Secret 到日志，日志不应出现原始值
  - [负向] fork PR workflow 中尝试用 Secret 做 HTTP 认证，请求不应成功
  - [正向] 同一 workflow 在非 fork (内部 PR) 触发时，Secret 应正常可用
  - [回归] 复现 history #51 场景——fork PR 是否仍可获取主仓密钥

负向断言目标: fork PR 不可读取仓库/组织级 Secret。判定证据：job 日志中 echo 输出为空；API 调用返回 401/403。
优先级线索: RISK-SEC-01 (P0 blocker)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md, github-reference/security/secrets.md, security-knowledge/issues.md (§2), history/issues-encountered.md (#51 ★ P0)
```

---

```
意图 ID:    INTENT-SEC-003
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       pull_request_target 仅在 base 分支 workflow 定义中运行，不执行 fork 侧 workflow YAML

风险点:     `pull_request_target` 的核心安全承诺是「workflow 定义来自目标仓库 base 分支，而非 fork」。若平台实现存在缺陷导致实际执行了 fork 侧的 workflow YAML，外部贡献者可以在高权限上下文中运行任意命令。GitHub 上已有多起因滥用导致的供应链安全事故 (Pwn Requests, Part 1)。
预期系统行为: `pull_request_target` 触发时，实际执行的 workflow 定义文件应来自目标仓库的默认分支。ATOMGIT_TOKEN 拥有 permissions 声明的完整权限（可写），Secret 可访问。
Oracle 来源: GitCode 规格 (pr-mr-pipeline-security.md) 对齐 GitHub 行为 (pull_request_target.md)。

验证要点:
  - [正向] 目标仓库 base 分支有 pull_request_target workflow，workflow 应正常执行
  - [负向] fork 侧修改 pull_request_target workflow 中的 run 命令，实际执行的应不是 fork 侧版本
  - [回归] history #66: pull_request_target 的 fork PR secret 隔离「目前还未实现」——若已实现，需验证

负向断言目标: fork 侧对 pull_request_target workflow YAML 的任何修改不应影响实际执行的逻辑。判定证据：对比 fork 侧 YAML 与 job 日志中实际执行的命令文本。
优先级线索: RISK-SEC-01 (P0 blocker)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md, github-reference/security/pull_request_target.md, security-knowledge/github-actions-security-series.md (Part 1, Part 4), history/issues-encountered.md (#66 ★ P0)
```

---

```
意图 ID:    INTENT-SEC-004
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       pull_request_target 下显式 checkout fork PR head 代码后不应自动执行其中脚本

风险点:     pull_request_target workflow 中 `checkout ref: head.sha` 后执行 `make build` 等命令，等于在高权限上下文运行 fork 侧任意代码。GitHub actions/checkout v7+ 有 `allow-unsafe-pr-checkout` 内置保护，GitCode 对应实现需验证。
预期系统行为: 若显式 checkout 了 head.sha，checkout action 应产生安全警告或要求 opt-in。这是 workflow 作者的有意识风险决策，平台不应自动阻止但应提供保护机制。
Oracle 来源: GitHub 行为 (pull_request_target.md, actions/checkout v7+ built-in protection)。

验证要点:
  - [正向] pull_request_target 下 checkout head.sha 后执行 fork 侧脚本——命令应被执行（作者有意行为）
  - [负向] GitCode 的 checkout action 应在 checkout fork PR head 时产生警告或要求显式确认
  - [负向] pull_request_target workflow 在无显式 checkout ref 时，不应自动获取 fork 侧代码变更

负向断言目标: 无显式 checkout ref 时不执行 fork 代码；显式 checkout 时有安全警告。判定证据：job 日志中 checkout step 的安全提示（如有）。
优先级线索: RISK-SEC-01 (P0 blocker)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md, github-reference/security/pull_request_target.md, security-knowledge/github-actions-security-series.md (Part 1, Part 4)
```

---

```
意图 ID:    INTENT-SEC-005
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       Secret 值直接 echo 到日志时应被脱敏为 `***`

风险点:     workflow 中 echo secret 值是最基础的泄露途径。已有用例 TC-011 覆盖基础场景。issues.md §3 确认此为已知安全关注点 (日志脱敏)。
预期系统行为: 任何通过 `${{ secrets.X }}` 引用且出现在日志输出中的 secret 值，必须被替换为 `***`。
Oracle 来源: GitCode 规格 (using-secrets.md) 对齐 GitHub 行为 (secrets.md)。

验证要点:
  - [正向] echo 非 secret 文本时日志正常显示
  - [负向] echo secret 值的日志行中不应出现原始 secret 明文
  - [负向] 同一 job 内多次引用同一 secret，每次出现均应被遮蔽

负向断言目标: 日志中不出现 secret 明文。判定证据：API 拉取 job 日志后对已知 secret 值做全文搜索。
优先级线索: RISK-SEC-02 (P0 blocker — 信息泄露)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md, github-reference/security/secrets.md, security-knowledge/issues.md (§3)
```

---

```
意图 ID:    INTENT-SEC-006
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       Secret 经过 base64 编码后 echo 到日志仍应被脱敏

风险点:     GitHub 文档承认「redaction is not guaranteed」对于变换后的值。base64/URL 编码、子字符串拼接等变换可绕过自动脱敏。issues.md §3 确认此为已知绕过场景 (base64 编码)。
预期系统行为: 理想情况下，base64 编码后的 secret 在日志中仍被遮蔽；至少应对常见编码模式有基本防护。
Oracle 来源: GitHub 行为 (secrets.md: redaction 局限声明)。

验证要点:
  - [负向] `echo <secret> | base64` 的输出若被输出到日志，不应泄露 secret 的原始值
  - [负向] base64 编码后再解码输出原始 secret 的场景，某一步应被遮蔽

负向断言目标: 日志中不出现未经遮蔽的 secret 值，无论是否经过编码变换。判定证据：搜索原始 secret 值 + base64 编码后的值。
优先级线索: RISK-SEC-02 (P1 — 已知局限)
破坏级别:   none
来源输入:   github-reference/security/secrets.md, security-knowledge/issues.md (§3), security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-007
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       Secret 通过子字符串拼接后 echo 到日志应仍被脱敏

风险点:     将 secret 拆分为两段再拼接输出可能绕过基于精确匹配的脱敏机制。issues.md §3 确认「拼接/插值」为脱敏绕过场景。
预期系统行为: 平台应对 secret 值的任意子串片段也有脱敏覆盖。
Oracle 来源: GitHub 行为 (secrets.md — 承认变换可绕过 redaction)。

验证要点:
  - [负向] 将 secret 拆为两半再拼接 echo，日志中不应出现完整的原始 secret 值
  - [负向] 逐个字符拼接 secret 再输出，不应出现完整 secret 值

负向断言目标: 完整 secret 明文不出现在日志中。判定证据：日志全文搜索原始 secret 值命中数为 0。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   github-reference/security/secrets.md, security-knowledge/issues.md (§3)
```

---

```
意图 ID:    INTENT-SEC-008
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       Secret 包含多行文本时应整体被脱敏

风险点:     多行 secret (SSH 私钥、PEM 证书) 的脱敏更难——每行需独立匹配，换行符可能导致遮蔽失败。
预期系统行为: 多行 secret 值中每一行在日志中出现时均应被遮蔽。
Oracle 来源: GitHub 行为 (secure-use.md: Never use structured data as a secret)。

验证要点:
  - [负向] 多行 secret 的每一行 echo 到日志时均应被遮蔽
  - [负向] 包含换行转义符的 secret 不应被还原为实际换行后的明文

负向断言目标: 多行 secret 无一行的明文出现在日志中。判定证据：逐行 grep secret 各行的内容命中数为 0。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   github-reference/security/secrets.md, github-reference/security/secure-use.md, security-knowledge/issues.md (§3)
```

---

```
意图 ID:    INTENT-SEC-009
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       PR 标题中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     将 `${{ atomgit.event.pull_request.title }}` 直接写进 `run:` 的 shell 脚本——表达式在 shell 执行前即被求值替换。GitHub Security Lab Part 2 确认此为 Actions 最常见高危漏洞类型 (CWE-94)。
预期系统行为: 平台应在表达式求值阶段对危险字符做转义或报错，不应静默执行。环境变量中间变量模式应有效阻止注入。
Oracle 来源: GitHub 行为 (script-injections.md) + Security Lab Part 2 (Untrusted Input)。

验证要点:
  - [负向] PR 标题含分号+命令，被直接插入 run: 不应执行该命令
  - [负向] PR 标题含反引号命令替换，不应被执行
  - [正向] 平台在 expr 求值阶段对危险字符的处理行为应一致 (报错或转义)

负向断言目标: 通过 PR 标题注入的额外 shell 命令不应在 runner 上执行。判定证据：job 日志中不出现注入命令的执行痕迹。
优先级线索: RISK-SEC-02 (P0 blocker — 注入)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2), testing-focus.md §6
```

---

```
意图 ID:    INTENT-SEC-010
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       PR 正文 (body) / Issue 正文中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     PR 正文和 Issue 正文同样是不可信输入，且正文更长、更复杂，注入面更大。Security Lab Part 2 列出 `github.event.issue.body` 和 `github.event.pull_request.body` 为不可信源。
预期系统行为: 同 INTENT-SEC-009——平台应提供危险引用模式的检测或文档警告。
Oracle 来源: GitHub 行为 (script-injections.md) + Security Lab Part 2。

验证要点:
  - [负向] PR 正文含多行注入 payload，被直接插入 run: 后不应被执行
  - [负向] PR 正文含 $() 命令替换、反引号命令替换，均不应被执行

负向断言目标: PR 正文中的 shell 元字符不应被解释执行为命令。判定证据：job 日志不出现注入命令的输出。
优先级线索: RISK-SEC-02 (P0 blocker — 注入)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-011
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       分支名中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     分支名是自由文本，允许 `/`、`-`、`_` 及某些特殊字符。Security Lab Part 2 指出 `zzz";echo${IFS}"hello";#` 是合法 git 分支名。`${{ atomgit.ref_name }}` 直接插入 shell 存在同等注入面。
预期系统行为: 分支名中的 shell 元字符不应被解释执行。
Oracle 来源: GitHub 行为 (script-injections.md) + Security Lab Part 2。

验证要点:
  - [负向] 分支名含分号+命令，被直接插入 run: 后不应执行
  - [负向] 分支名含管道符 + 命令，不应被执行

负向断言目标: 分支名中的特殊字符不被解释为 shell 命令。判定证据：job 日志不出现注入命令副作用。
优先级线索: RISK-SEC-02 (P0 blocker — 注入)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-012
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       提交信息 (commit message) 中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     提交信息同样是不可信输入 (fork 侧完全可控)。Security Lab Part 2 列出 `commits.*.message` 为不可信源。
预期系统行为: 平台不应让提交信息中的 shell 元字符被解释执行。
Oracle 来源: GitHub 行为 (script-injections.md) + Security Lab Part 2。

验证要点:
  - [负向] 提交信息含反引号命令替换，不应被执行
  - [负向] 提交信息含分号+额外命令，不应被执行

负向断言目标: 提交信息中的附加命令不产生执行副作用。判定证据：job 日志不出现注入命令执行痕迹。
优先级线索: RISK-SEC-02 (P0 blocker — 注入)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-013
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       通过环境变量安全引用不可信输入应不触发脚本注入

风险点:     这是 GitHub Actions + Security Lab Part 2 推荐的注入缓解方式——通过 `env:` 将不可信上下文赋给中间环境变量，再在 `run:` 中用 `$VAR` 引用。Security Lab Part 2 详细证明此模式有效。
预期系统行为: 通过 env 中间变量引用的不可信输入，shell 元字符不会被解释——它们被当作字面字符串。
Oracle 来源: GitHub 行为 (script-injections.md) + Security Lab Part 2 (修复方案)。

验证要点:
  - [正向] env 中间变量方式引用的含元字符的 PR 标题——不应触发命令执行
  - [正向] env 中间变量方式的 workflow 应正常完成

负向断言目标: 安全引用模式下注入不可行。判定证据：job 日志中 env 变量的值保留原始字符但不触发命令执行。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-014
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       不可信输入注入到 GITHUB_ENV / GITHUB_OUTPUT 文件不导致环境变量污染

风险点:     若将不可信输入写入 GITHUB_ENV (GitCode 对应原子)，后续 step 读取时可能发生二次注入。Security Lab Part 2 关注 workflow 命令通道的安全性。
预期系统行为: GITHUB_ENV 文件写入协议应对值做安全处理——多行值或含特殊字符的值不导致额外环境变量被注入。
Oracle 来源: GitHub 行为 (workflow commands 规范)。

验证要点:
  - [负向] 向 GITHUB_ENV 写入含换行符的不可信值，不应导致额外的环境变量被注入
  - [负向] 向 GITHUB_OUTPUT 写入含特殊字符的值，后续 step 不应被二次解释

负向断言目标: GITHUB_ENV/GITHUB_OUTPUT 协议不被不可信输入破坏。判定证据：后续 step echo 环境变量值 = 原始写入值。
优先级线索: RISK-SEC-02 (P0 blocker — 注入)
破坏级别:   none
来源输入:   testing-focus.md §6, github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-015
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       permissions: {} (空对象) 使 ATOMGIT_TOKEN 持有最小默认权限

风险点:     若平台未正确处理空 permissions，token 可能继承仓库级默认权限而非最小权限。Security Lab Part 3 强调最小权限原则。
预期系统行为: permissions: {} 时 ATOMGIT_TOKEN 仅拥有 `repository: read`，不可写。
Oracle 来源: GitCode 规格 (token-permissions.md) 对齐 GitHub + Security Lab Part 3 (最小权限)。

验证要点:
  - [负向] permissions: {} 下 git push 应被拒绝
  - [负向] permissions: {} 下 API 操作 PR 应返回 403
  - [正向] permissions: {} 下 git clone 应成功

负向断言目标: 空 permissions 等于最小权限。判定证据：写操作返回非零退出码或 HTTP 403。
优先级线索: RISK-SEC-01 (P0 blocker — 权限越界)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md, security-knowledge/github-actions-security-series.md (Part 3)
```

---

```
意图 ID:    INTENT-SEC-016
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       未声明 permissions 时 ATOMGIT_TOKEN 使用仓库设置中的默认权限

风险点:     permissions 默认值语义是兼容性差异高发区。若 GitCode 默认给 read-write 而用户以为默认只读，所有 workflow 在高权限下运行。
预期系统行为: 未声明 permissions 时 token 权限 = 仓库默认值。文档声明「使用仓库设置中定义的权限」。
Oracle 来源: GitCode 规格 (token-permissions.md)。

验证要点:
  - [正向] 仓库默认权限为 repository:read，未声明 permissions 应能 clone 但不能 push
  - [正向] 仓库默认权限为 repository:write，未声明 permissions 应能 push

负向断言目标: 未声明 permissions 时 token 权限 = 仓库默认值。判定证据：push/clone 结果与仓库默认权限一致。
优先级线索: RISK-SEC-01 (P0 blocker — 默认权限)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md
```

---

```
意图 ID:    INTENT-SEC-017
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       job 级 permissions 声明可覆盖 workflow 级声明

风险点:     遵循最小权限原则的关键能力。Security Lab Part 3 强调应在 job 级别显式声明 permissions: 收窄权限。
预期系统行为: job 级 permissions 覆盖 workflow 级的同名权限域。job 未声明时继承 workflow 级。
Oracle 来源: GitCode 规格 (token-permissions.md) + Security Lab Part 3。

验证要点:
  - [正向] workflow 级设 repository:none，job 级设 repository:read——job 应能 clone
  - [负向] workflow 级设 pr:write，job 级设 pr:none——job 不应能操作 PR

负向断言目标: job 级权限声明严格遵循——覆盖生效，无意外权限放大。判定证据：对比 job API 调用结果与 permissions 声明一致。
优先级线索: RISK-SEC-01 (P1)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md, security-knowledge/github-actions-security-series.md (Part 3)
```

---

```
意图 ID:    INTENT-SEC-018
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       第三方 action 引用未 pin 到 commit SHA 时有平台警告

风险点:     `uses: owner/repo@v1` 是可变的——tag 可被重指向，若 action 维护者账号被接管，所有引用者将运行恶意代码。Security Lab Part 3 详细分析了 5 种 pin 方式的安全等级：完整 commit hash 最安全。
预期系统行为: 平台应至少对浮动引用提供警告。SHA-pinned 引用应被接受且不受 tag 改写影响。
Oracle 来源: GitHub 行为 (secure-use.md) + Security Lab Part 3 (Building Blocks: 5 pin methods)。

验证要点:
  - [正向] `uses: action@<commit SHA>` 应接受并正常运行
  - [负向] `uses: action@main` 平台是否产生 lint/安全警告
  - [负向] tag 被覆盖指向新 commit 后，SHA-pinned 引用不应受影响

负向断言目标: 平台对浮动引用有可见警告机制；SHA-pinned 引用接受且不变。判定证据：workflow lint 输出 / job 日志中的 action checkout 信息。
优先级线索: RISK-SEC-02 (P1 — 供应链安全)
破坏级别:   none
来源输入:   github-reference/security/secure-use.md, security-knowledge/github-actions-security-series.md (Part 3)
```

---

```
意图 ID:    INTENT-SEC-019
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       fork PR 不应能写入或污染主分支的依赖缓存

风险点:     cache 是跨 run 共享状态。fork PR 若可写缓存，攻击者可投毒——替换依赖包、编译产物。Security Lab Part 4 明确指出：即使 `permissions: {}` 移除写权限，仍可投毒缓存影响其他 workflow。pull_request_target workflow 对缓存仅有 read-only 访问。
预期系统行为: fork PR workflow 写入的缓存不应被主分支命中；主分支已有缓存不被 fork PR 覆盖。
Oracle 来源: GitHub 行为 + Security Lab Part 4 (Cache Poisoning)。

验证要点:
  - [负向] fork PR 写入 cache key，主分支 push 读取同 key 不应命中
  - [负向] fork PR 不应覆盖主分支已有缓存条目

负向断言目标: fork PR 缓存与主分支隔离。判定证据：主分支 workflow cache restore step 返回 cache miss。
优先级线索: RISK-SEC-01 (P0 blocker — 缓存投毒)
破坏级别:   none
来源输入:   testing-focus.md §8, github-reference/security/pull_request_target.md, security-knowledge/github-actions-security-series.md (Part 4)
```

---

```
意图 ID:    INTENT-SEC-020
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       同一 workflow 多次运行之间的 cache 不应跨不同事件类型互相污染

风险点:     不同触发类型 (push/pull_request/schedule) 的缓存作用域若未正确隔离可能导致投毒。Security Lab Part 4 强调 cache scope 应按 branch + event type 隔离。
预期系统行为: cache key 作用域按分支和触发事件类型隔离。
Oracle 来源: GitHub 行为 (cache scope 按 branch + event type 隔离)。

验证要点:
  - [正向] 同分支两次 push：第一次写入 cache，第二次恢复应命中
  - [负向] fork PR 写入的 cache，内部 push 不应命中

负向断言目标: 跨事件 cache 隔离正确。判定证据：cache restore step 输出 (cache-hit = true/false)。
优先级线索: RISK-SEC-01 (P1)
破坏级别:   none
来源输入:   testing-focus.md §8, github-reference/security/pull_request_target.md, security-knowledge/github-actions-security-series.md (Part 4)
```

---

```
意图 ID:    INTENT-SEC-021
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       Secret 命名遵守约束 (大写字母+数字+下划线，不以 ATOMGIT_ / 数字开头)

风险点:     Secret 命名约束若不严格执行，以 ATOMGIT_ 开头的 secret 与系统变量冲突。
预期系统行为: 创建 secret 时平台应校验命名：仅允许 [A-Z0-9_]+，拒绝 ATOMGIT_ 或数字开头。
Oracle 来源: GitCode 规格 (using-secrets.md) 对齐 GitHub 行为。

验证要点:
  - [正向] 合法名称 (DEPLOY_KEY) 应能创建
  - [负向] 名称以 ATOMGIT_ 开头应被拒绝
  - [负向] 名称以数字开头应被拒绝

负向断言目标: 不合规名称在创建时被拒绝。判定证据：创建 API/UI 返回明确错误。
优先级线索: RISK-SEC-02 (P2)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md
```

---

```
意图 ID:    INTENT-SEC-022
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       环境 (environment) 级 Secret 受审批规则保护

风险点:     若无审批保护，绑定了 environment: prod 的 job 在未审批时就能读取生产 Secret。已有用例 TC-010 发现 environment 字段不被平台识别。
预期系统行为: job 在审批通过前应处于等待状态，不可读取环境级 Secret。若平台尚不支持，本 intent 记录为「待能力就绪后重测」。
Oracle 来源: GitCode 规格 (using-secrets.md)。

验证要点:
  - [正向] 审批通过后 job 开始执行，可读取环境级 Secret
  - [负向] 未审批时 job 应等待
  - [负向] 若 environment 字段当前不可用 (TC-010)，本 intent 状态为 blocked

负向断言目标: 未审批的 job 不能开始执行。判定证据：job 状态为 queued/waiting。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md, existing-cases/cases.md (TC-010)
```

---

```
意图 ID:    INTENT-SEC-023
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       ATOMGIT_TOKEN 在 job 结束后应自动失效

风险点:     若 token 在 job 结束后可继续使用，攻击者可能延迟使用窃取的 token。issues.md §2 关注「token 过期/轮换机制——过期 token 是否仍能通过缓存访问」。
预期系统行为: ATOMGIT_TOKEN 生命周期限定为单次 job——job 结束后立即失效。
Oracle 来源: GitCode 规格 (token-permissions.md) 对齐 GitHub 行为 (github-token.md)。

验证要点:
  - [正向] job 运行期间 ATOMGIT_TOKEN API 调用正常
  - [负向] job 完成后同 token 值 API 调用返回 401/403

负向断言目标: job 结束后 token 不可再用。判定证据：job 完成后 replays API 调用返回认证失败。
优先级线索: RISK-SEC-01 (P1 — token 生命周期)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md, github-reference/security/github-token.md, security-knowledge/issues.md (§2)
```

---

```
意图 ID:    INTENT-SEC-024
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       ATOMGIT_TOKEN 触发的操作不应产生递归 workflow 运行

风险点:     workflow 使用 ATOMGIT_TOKEN 推送代码后可能触发新的 workflow 运行导致无限递归。
预期系统行为: 使用 ATOMGIT_TOKEN 执行的 git push / PR 创建不应递归触发新 workflow run。
Oracle 来源: GitHub 行为 (github-token.md)。

验证要点:
  - [负向] workflow 中用 ATOMGIT_TOKEN 推送新 commit——不应触发新的 workflow 运行
  - [负向] workflow 中用 ATOMGIT_TOKEN 创建 PR——不应自动触发该 PR 的 workflow

负向断言目标: token 操作不产生递归 workflow。判定证据：仅有 1 个 run 而非链式触发。
优先级线索: RISK-SEC-01 (P1 — 递归 DoS)
破坏级别:   none
来源输入:   github-reference/security/github-token.md
```

---

```
意图 ID:    INTENT-SEC-025
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       fork PR 触发的 pull_request workflow 不应有持久的 runner 状态残留

风险点:     若 runner 在 fork PR job 结束后未正确清理，下一高权限 job 可能被残留状态污染。issues.md §1 和 §4 关注多项目隔离和共享盘残留。Security Lab Part 4 强调 ephemeral runner 的重要性。
预期系统行为: 每个 job 运行在干净环境中——fork PR job 的工作区、环境变量、后台进程在结束后被完全清理。
Oracle 来源: GitHub 行为 (ephemeral VM, 每个 job 全新环境)。

验证要点:
  - [负向] fork PR job 写入的文件，后续内部 job 不应能看到
  - [负向] fork PR job export 的环境变量不影响后续 job
  - [负向] fork PR job 启动的后台进程在结束后应被终止

负向断言目标: fork PR job 环境在结束后完全隔离。判定证据：后续 job 的 ls $GITHUB_WORKSPACE 和 env 不含前 job 残留。
优先级线索: RISK-SEC-01 (P0 blocker — runner 隔离)
破坏级别:   full_instance
来源输入:   testing-focus.md §4, github-reference/security/secure-use.md, security-knowledge/issues.md (§1, §4), security-knowledge/github-actions-security-series.md (Part 4)
```

---

```
意图 ID:    INTENT-SEC-026
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       跨 job artifact 在 fork PR 场景下不应被后续高权限 job 无条件信任

风险点:     fork PR 上传 artifact，高权限 workflow 下载使用而未经校验 = 二次攻击。Security Lab Part 4 特别警告 artifact 投毒——恶意 PR 上传被污染 artifact，workflow_run 下载后使用。
预期系统行为: artifact 作用域应与触发事件和权限上下文绑定。fork PR artifact 不被内部 push workflow 自动下载。
Oracle 来源: GitHub 行为 + Security Lab Part 4 (Artifact Poisoning)。

验证要点:
  - [负向] fork PR workflow 上传 artifact，后续内部 push workflow 不应能自动下载
  - [负向] 若支持跨 workflow artifact 下载，应提供来源标识

负向断言目标: fork PR artifact 不被后续内部 workflow 隐式继承。判定证据：内部 workflow artifact 列表不含 fork PR 条目。
优先级线索: RISK-SEC-01 (P1)
破坏级别:   none
来源输入:   testing-focus.md §8, github-reference/security/secure-use.md, security-knowledge/github-actions-security-series.md (Part 4)
```

---

```
意图 ID:    INTENT-SEC-027
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       `::add-mask::` workflow 命令的正确性与安全性

风险点:     `::add-mask::` 允许动态注册脱敏值。若实现有误 (mask 注册失败静默通过、stop-commands 解除 mask)，动态 secret 可能泄露。issues.md §3 记录 `::add-mask::` 命令返回值可能含被遮蔽前的值 (GitHub 已知问题)。
预期系统行为: `::add-mask::VALUE` 注册的值在后续日志中与内置 secret 同等遮蔽。`::stop-commands::` 不应恢复 mask。
Oracle 来源: GitHub 行为 (secure-use.md) + issues.md (known add-mask bypass)。

验证要点:
  - [正向] `echo '::add-mask::MY_DYNAMIC_SECRET'` 后 echo 该值，日志应显示 `***`
  - [负向] `::stop-commands::` 后不应恢复被 mask 的值
  - [负向] add-mask 命令本身的返回值不应泄露被遮蔽前的值 (regression for issues.md known bug)

负向断言目标: 动态 mask 值在整 job 生命周期被遮蔽；stop-commands 不恢复 mask。判定证据：日志中动态敏感值以 `***` 出现。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   github-reference/security/secure-use.md, security-knowledge/issues.md (§3)
```

---

```
意图 ID:    INTENT-SEC-028
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       fork PR 下 `::add-mask::` 命令注册新 mask 不应影响主分支 job

风险点:     mask 表若泄露到 runner 级别 (非 job 级)，fork PR job 可恶意填充 mask 表干扰后续 job 的 secret 脱敏。
预期系统行为: mask 仅在当前 job 内生效；不同 job 的 mask 表独立。
Oracle 来源: GitHub 行为 (secrets.md: runner can only redact secrets used within the current job)。

验证要点:
  - [负向] fork PR job 注册的 mask 值，在后续内部 job 中不应生效
  - [负向] fork PR job 注册大量 mask 不应影响后续 job 性能

负向断言目标: mask 表 job 级隔离。判定证据：后续 job echo fork PR 注册的 mask 值应显示为明文。
优先级线索: RISK-SEC-01 (P1)
破坏级别:   none
来源输入:   github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-029
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       fork PR 的 workflow 不应能修改目标仓库的 workflow 文件

风险点:     fork PR 若可通过 API 绕过权限修改 `.gitcode/workflows/*.yml`，等于供应链攻击。Security Lab Part 4 指出 workflow 文件本身就是敏感资产。
预期系统行为: fork PR 不应能推送对 workflow 目录的修改，也不应能通过 API 修改 workflow 文件。
Oracle 来源: GitHub 行为 (secure-use.md: CODEOWNERS 保护 workflow 目录)。

验证要点:
  - [负向] fork PR workflow 尝试 git push 修改 workflow YAML——应被拒绝
  - [负向] fork PR workflow 尝试 API 上传 workflow 文件——应返回 403

负向断言目标: fork PR run 不可直接修改目标仓库 workflow 定义。判定证据：git push 返回 "Permission denied" / API 返回 403。
优先级线索: RISK-SEC-01 (P0 blocker — workflow 篡改)
破坏级别:   none
来源输入:   github-reference/security/secure-use.md, security-knowledge/github-actions-security-series.md (Part 1, Part 4)
```

---

```
意图 ID:    INTENT-SEC-030
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       第三方 action 的输入参数中的不可信值不应导致 action 内部代码注入

风险点:     即使使用 action 而非内联脚本 (推荐实践)，若 action 内部以不安全方式处理 with 参数，注入仍发生。Security Lab Part 2 讨论了 action 内部模板引擎导致的二次求值问题。
预期系统行为: action 接收 with 参数时，不可信输入应被当作纯数据。
Oracle 来源: GitHub 行为 (script-injections.md) + Security Lab Part 2 (action 内模板注入)。

验证要点:
  - [负向] 含 shell 元字符的 PR 标题作为 with 参数传入 action，不应产生注入痕迹
  - [正向] 安全 JS/TS action 应正确处理含特殊字符的标题

负向断言目标: with 参数中不可信输入不被二次解释为代码。判定证据：action 日志不出现注入命令痕迹。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, security-knowledge/github-actions-security-series.md (Part 2)
```

---

```
意图 ID:    INTENT-SEC-031
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       composite action 内部的 `run:` 步骤中引用不可信 inputs 不应导致注入

风险点:     composite action 内部将 `${{ inputs.x }}` 直接插入 `run:` 时，若 inputs 来自不可信调用方，shell 注入仍发生。
预期系统行为: 与普通 workflow run 行为一致——表达式求值在 shell 前完成。
Oracle 来源: GitHub 行为 (composite action 与普通 workflow 同一执行模型)。

验证要点:
  - [负向] 含注入字符的 inputs 传入 composite action 直接用于 run: 不应执行注入命令
  - [正向] composite action 内通过 env 中间变量使用的 inputs 应安全

负向断言目标: composite action 内注入不成功。判定证据：job 日志无注入命令副作用。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   testing-focus.md §7, github-reference/security/script-injections.md
```

---

```
意图 ID:    INTENT-SEC-032
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       reusable workflow (workflow_call) 调用方传入的 secrets 不应被被调用方泄露到日志

风险点:     调用方通过 secrets: inherit 将 secret 传给被调用方。若被调用方不安全 echo，secret 泄露。
预期系统行为: secret 在被调用方日志中同等受脱敏保护。
Oracle 来源: GitHub 行为 (secret masking 对传入 secrets 同样生效)。

验证要点:
  - [负向] 被调用方 echo 调用方传入的 secret——日志应显示 `***`
  - [负向] 被调用方将传入 secret base64 编码后输出不应泄露

负向断言目标: 跨 workflow 传入的 secret 在接收方同等脱敏。判定证据：被调用方日志搜索 secret 明文命中数 = 0。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   testing-focus.md §7, github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-033
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       并发 workflow (concurrency) 下的 token/secret 隔离安全

风险点:     同一 runner 上并发运行的 jobs 之间，若隔离仅依赖进程边界，高权限 job 可能读取低权限 job 的 secret。issues.md §1 关注多项目并发隔离。
预期系统行为: 同一 runner 上并发 jobs 之间的 token 和 secret 完全隔离。
Oracle 来源: GitHub 行为 (每个 job 独立 GITHUB_TOKEN 和工作区)。

验证要点:
  - [负向] 并发 job A 不应能从同 runner 上 job B 的工作区读环境变量
  - [负向] 并发 job 不应能通过 /proc 读取其他 job 的 process args

负向断言目标: 并发 job 间 secret/token 完全隔离。判定证据：job A 日志不出现 job B 的 secret。
优先级线索: RISK-SEC-01 (P1 — 并发隔离)
破坏级别:   full_instance
来源输入:   testing-focus.md §3/§4, security-knowledge/issues.md (§1)
```

---

```
意图 ID:    INTENT-SEC-034
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       用户专属 token / PAT 的使用不应影响平台安全模型

风险点:     用户使用 PAT 替代 ATOMGIT_TOKEN 时，token 权限不受 permissions 字段约束——可能绕过 fork PR 隔离。
预期系统行为: 文档应明确声明 permissions 仅控制 ATOMGIT_TOKEN，手动 token 不受约束。
Oracle 来源: GitHub 行为 (github-token.md)。

验证要点:
  - [正向] 使用 PAT 的 fork PR workflow——secret 可被访问
  - [负向] 平台文档是否声明 permissions 不约束手动 token

负向断言目标: 文档明确警告 permissions 仅控制 ATOMGIT_TOKEN。判定证据：GitCode 安全文档中是否有此声明。
优先级线索: RISK-SEC-02 (P2)
破坏级别:   none
来源输入:   github-reference/security/github-token.md
```

---

```
意图 ID:    INTENT-SEC-035
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       事件负载 (event payload) 中不可信字段在 expression evaluation 阶段的类型安全

风险点:     `${{ atomgit.event.* }}` 返回 JSON 对象——若类型与预期不符可能导致意外 coercion 或注入。TC-033 发现 atomgit.event 返回对象字面量导致 bash syntax error。
预期系统行为: 表达式求值结果替换进 YAML 后的产物应在 shell 上下文中安全——不应因对象字面量导致 shell 语法错误。
Oracle 来源: GitHub 行为 (表达式求值类型处理)。

验证要点:
  - [负向] `${{ atomgit.event }}` 用于 run: 不应导致 shell 语法错误
  - [负向] `${{ atomgit.event.* }}` 嵌套对象用于 if: 不应崩掉解析器

负向断言目标: 表达式求值产物不导致 shell 语法错误或非预期代码执行。判定证据：job 日志无 syntax error。
优先级线索: RISK-SEC-02 (P1)
破坏级别:   none
来源输入:   github-reference/security/script-injections.md, existing-cases/cases.md (TC-033)
```

---

```
意图 ID:    INTENT-SEC-036
状态:      CARRIED OVER (2026-07-20-01)
维度标签:   [security]
标题:       平台内置 secret (ATOMGIT_TOKEN) 不应在未授权上下文被引用泄露

风险点:     `${{ secrets.atomgit_token }}` 是系统预置 secret——需验证 fork PR 下返回空值。已有用例 TC-100 覆盖脱敏但 fork PR 下行为未验证。
预期系统行为: fork PR 下 ${{ secrets.atomgit_token }} 返回空或降级后的只读 token，日志中应被脱敏。
Oracle 来源: GitCode 规格 (token-permissions.md)。

验证要点:
  - [负向] fork PR 下 echo ${{ secrets.atomgit_token }}——日志应为 `***` 或空
  - [负向] 内部 push 下 echo ${{ secrets.atomgit_token }}——应被遮蔽为 `***`

负向断言目标: ATOMGIT_TOKEN 在任何情况下日志均不泄露明文。判定证据：日志搜索 token 前缀命中数 = 0。
优先级线索: RISK-SEC-01 (P0 blocker — token 泄露)
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md
```

---

## PART B — ★ NEW (enabled by security-knowledge/ + history/ inputs)

> 以下 20 条 intent 得益于本次新增的安全知识输入 (GitHub Security Lab 系列 / issues.md / 历史缺陷数据)，是在 2026-07-20-01 基础上新增的覆盖。每条标注 `status: NEW` 和 `source` 文件。

---

### B.1 — TOCTOU, workflow_run, and IssueOps (from github-actions-security-series.md Part 4)

```
意图 ID:    INTENT-SEC-037
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       pull_request_target 的 TOCTOU 攻击——审批后恶意 commit 替换 PR 代码

风险点:     Security Lab Part 4 新发现的漏洞模式：攻击者提交无害 PR → 等待管理员审批/触发 pull_request_target → 在 workflow 实际执行前推送恶意 commit → workflow 以高权限执行恶意代码。因为 workflow 运行时 checkout head.sha 获取的是最新提交（而非审批时的提交），形成了时间差攻击窗口。
预期系统行为: 若 pull_request_target workflow 中 checkout 了 `head.sha`（而非 merge commit 或审批时的特定 commit），平台应提供保护机制——至少文档明确警告 TOCTOU 风险。理想情况下应支持「锁定审批时的 commit SHA」而非直接使用 `head.sha`（该值可能已变）。
Oracle 来源: Security Lab Part 4 (TOCTOU attack pattern)。GitHub 通过 actions/checkout v7+ 的 `allow-unsafe-pr-checkout` 提供部分保护。

验证要点:
  - [负向] PR 审批后、pull_request_target 执行前推送新的恶意 commit——workflow 执行的代码应与审批时的 commit 一致
  - [负向] head.sha 在 pull_request_target 执行时不应自动更新为攻击者新推送的 commit
  - [正向] pull_request_target 若使用 checkout 默认 ref (不显式指定 head.sha)，应 checkout base 分支——天然免疫 TOCTOU

负向断言目标: pull_request_target workflow 不被 TOCTOU 攻击利用——执行的代码版本可追溯且可控。判定证据：job 日志中 checkout 的 git SHA 等于审批时锁定的 commit，而非攻击者后推送的 commit。
优先级线索: RISK-SEC-01 (P0 blocker — pull_request_target 安全命脉)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 4 ★)
```

---

```
意图 ID:    INTENT-SEC-038
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       非默认分支上的旧版 workflow 文件不应成为攻击入口

风险点:     Security Lab Part 4 指出：即使默认分支的 pull_request_target workflow 已修复（安全），**其他分支上的旧版本 workflow 仍可被利用**。攻击者可以针对性地向含有旧版不安全 workflow 的分支提 PR，触发高权限执行。这是「修复了主分支 ≠ 修复了整个仓库」的典型案例。
预期系统行为: 平台应在 pull_request_target 触发时始终使用**默认分支**的 workflow 版本，无论 PR 的目标分支是什么。或者，支持仓库级配置「仅允许默认分支的 workflow 响应 pull_request_target 事件」。
Oracle 来源: Security Lab Part 4 (Non-default branch latent threats)。

验证要点:
  - [负向] 非默认分支 (如 dev) 有不安全的 pull_request_target workflow——向该分支提 PR 后，实际执行的应是默认分支的 workflow 版本
  - [负向] 攻击者修改非默认分支的 workflow 添加恶意命令，不应被实际执行
  - [正向] 默认分支的 pull_request_target workflow 更新安全修复后，所有 PR (不论目标分支) 均应使用最新版本

负向断言目标: 非默认分支上的旧 workflow 不成为 pull_request_target 的高权限执行入口。判定证据：无论目标分支，实际执行的 workflow steps 始终来自默认分支。
优先级线索: RISK-SEC-01 (P1 — 跨分支安全一致性)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 4 ★)
```

---

```
意图 ID:    INTENT-SEC-039
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       issue_comment 触发器不应绕过 PR 审批机制 (IssueOps TOCTOU)

风险点:     Security Lab Part 4 揭示的模式：`issue_comment` 触发 workflow 后，管理员评论了触发命令（如 `/deploy`），攻击者在 workflow 执行前推送恶意代码。因为 issue_comment workflow **不受 PR 审批机制保护**——管理员评论 ≠ 审查了代码。这与 pull_request_target 的 TOCTOU 风险有同样的机制。已确认的缓解方案：使用 **label gates**（`labeled` activity type + commit SHA）替代 comment 触发。
预期系统行为: 若 GitCode 支持 `issue_comment` 触发器——平台应文档化其安全风险：comment 触发不应被用于执行 PR 代码（除非使用了 commit SHA 锁定 + label gate 审批流程）。若支持 `labeled` activity type，应引导用户使用 label 替代 comment 作触发。
Oracle 来源: Security Lab Part 4 (IssueOps TOCTOU + label gates 缓解)。

验证要点:
  - [负向] issue_comment 触发后，攻击者推送恶意代码——workflow 不应执行新推送的代码（若使用了 head.sha）
  - [正向] labeled activity type 触发 workflow——应使用审批时锁定的 commit SHA，而非动态 head ref
  - [正向] 平台文档是否说明 issue_comment 触发器的安全注意事项

负向断言目标: issue_comment 触发器不被用于绕过 PR 代码审查。判定证据：workflow 日志中 checkout 的 commit SHA 与管理员评论时的 commit 一致。
优先级线索: RISK-SEC-01 (P0 blocker — 审批绕过)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 4 ★)
```

---

```
意图 ID:    INTENT-SEC-040
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 2)
维度标签:   [security]
标题:       表达式双重求值——action 内部模板引擎不应二次解释 ${{ }} 的结果

风险点:     Security Lab Part 2 详细分析了「双重表达式求值」攻击：某些 Action 内部使用模板引擎 (如 lodash.template) 处理输入。若 workflow 中 `${{
github.event.issue.title }}` 求值后传递给 action，action 内部的模板引擎再次对结果进行插值——攻击者在 PR 标题中放入 `{{ process.env.GITHUB_TOKEN }}`，第一次求值留下该字符串，第二次求值被模板引擎解析，导致 token 泄露或任意代码执行。这是 GitHub Actions 生态中真实存在的漏洞类。
预期系统行为: GitCode 的 action runner (若基于 Node.js) 不应在 action 内部对已求值的输入参数进行二次模板插值。若 platform SDK 使用模板系统，必须禁用对 with 参数的再处理。此条风险主要在 action 作者侧，但平台应有最佳实践文档和检测机制。
Oracle 来源: Security Lab Part 2 (Attack 1: Double expression evaluation)。

验证要点:
  - [负向] 将 `{{ process.env }}` 作为 PR 标题，经过 workflow `${{ }}` 求值后传给 action——action 内部不应将该字符串二次解释为模板变量
  - [负向] action 内部使用的模板引擎 (如 lodash) 不应对 `with:` 传入的参数进行 `_.template()` 处理
  - [正向] 平台文档是否提及 action 开发中模板注入的风险

负向断言目标: 传入 action with 参数的值不被 action 内部模板引擎二次解释。判定证据：action 日志输出不含二次插值产生的内容；workflow 不会因模板注入异常退出。
优先级线索: RISK-SEC-02 (P1 — 模板注入)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 2 ★)
```

---

```
意图 ID:    INTENT-SEC-041
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 2)
维度标签:   [security]
标题:       提交者 email 地址作为不可信输入不应导致 shell 注入

风险点:     Security Lab Part 2 指出 RFC 5322 允许极端灵活的 email 格式——如 `` `echo${IFS}hello`@domain.com `` 是合法的 email 地址。`${{ atomgit.event.head_commit.author.email }}` 和 `${{ atomgit.event.commits.*.author.email }}` 可直接被攻击者控制（fork 侧可设置任意 git user.email）。若此值被直接插入 `run:` 的 shell 脚本，email 中的反引号和特殊字符构成注入向量。**这是一个不常见但同等有效的注入面，往往被忽视。**
预期系统行为: email 地址上下文字段应与 PR 标题同等对待——属于不可信输入。直接写入 run: 存在注入风险；应使用 env 中间变量模式。平台应提供同等引用安全警告。
Oracle 来源: Security Lab Part 2 (Non-obvious untrusted sources: email addresses)。

验证要点:
  - [负向] 将 `echo${IFS}hello@evil.com` 设为 git user.email，workflow 中 `run: echo "${{ atomgit.event.head_commit.author.email }}"` 直接使用——不应执行 echo hello
  - [负向] email 中反引号命令替换不应被解释执行
  - [正向] 通过 env 中间变量引用 email——应安全地当字符串处理

负向断言目标: email 上下文字段中的 shell 元字符不产生执行副作用。判定证据：job 日志中无 email 注入导致的额外命令输出。
优先级线索: RISK-SEC-02 (P1 — 非常规注入面)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 2 ★)
```

---

```
意图 ID:    INTENT-SEC-042
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       workflow_run 事件下下载的 artifact 应被视为不可信输入

风险点:     Security Lab Part 4 明确警告：恶意 PR 可上传被污染的 artifact，特权 `workflow_run` workflow 下载该 artifact 后使用（如解压、执行脚本）而未经验证。这构成 artifact 投毒攻击。
预期系统行为: 若 GitCode 支持 `workflow_run` 触发（或其等价机制），从其他 workflow 下载的 artifact 应被显式标记来源（触发 workflow 的 run ID + 事件类型 + 是否来自 fork）。平台文档应明确警告 artifact 投毒风险。
Oracle 来源: Security Lab Part 4 (Artifact poisoning via workflow_run)。

验证要点:
  - [负向] fork PR 的 pull_request workflow 上传 artifact，特权 workflow_run workflow 下载——下载的 artifact 应有来源标记
  - [负向] workflow_run workflow 下载 artifact 后执行其中的脚本——应为作者有意识的风险决策
  - [正向] 若 GitCode 不支持 workflow_run，本 intent 标记为 N/A

负向断言目标: 跨 workflow 的 artifact 不被隐式信任——来源可溯、风险可感知。判定证据：artifact 元数据含来源 run_id + 触发事件 + fork/non-fork 标识。
优先级线索: RISK-SEC-01 (P1 — artifact 投毒)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 4 ★)
```

---

```
意图 ID:    INTENT-SEC-043
状态:      ★ NEW (enabled by security-knowledge/github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       workflow_run 不应对篡改触发事件类型的攻击免疫

风险点:     Security Lab Part 4 揭示：攻击者可修改触发 workflow 使其发出不同事件类型，从而意外触发一个特权 `workflow_run` workflow。例如：非特权 workflow 被修改为发出 `pull_request` 事件（而非预期的 `check_run` 事件），如果 workflow_run filter 未严格限定事件类型，特权 workflow 可能被意外触发。
预期系统行为: workflow_run 的触发事件类型 (types) 过滤应严格生效。特权 workflow 应在启动时验证：触发它的事件类型确实在允许列表中。
Oracle 来源: Security Lab Part 4 (workflow_run event manipulation)。

验证要点:
  - [负向] 攻击者修改非特权 workflow 以发出非预期事件类型——特权 workflow_run workflow **不应**被此事件触发
  - [负向] workflow_run 的 `types:` 过滤配置应严格匹配，不应松散匹配
  - [正向] 用 `branches` 过滤限制 workflow_run 仅响应默认分支的事件

负向断言目标: workflow_run 仅被声明的 `types:` 事件触发——不受攻击者篡改事件类型的影响。判定证据：特权 workflow 仅在被允许的事件类型发生时才会运行。
优先级线索: RISK-SEC-01 (P1 — 事件类型投毒)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 4 ★)
```

---

### B.2 — Multi-project isolation, secret lifecycle, log security (from security-knowledge/issues.md)

```
意图 ID:    INTENT-SEC-044
状态:      ★ NEW (enabled by security-knowledge/issues.md §1)
维度标签:   [security]
标题:       多项目共享 runner 环境下的跨项目数据隔离

风险点:     issues.md §1 明确指出：多个开源项目共享同一批 runner 资源。一个项目的 workflow 执行不应影响另一个项目。若 runner 非 ephemeral 或 cleanup 不彻底，项目 A 的工作区文件、环境变量、缓存、secret 可能在项目 B 的 job 中可见。这是共享环境下的隔离失效风险。
预期系统行为: 每个 job（无论属于哪个项目）应运行在干净的环境中——不应看到其他项目的残留文件、环境变量、进程。Runner workspace 应按项目区分且 job 后彻底清理。缓存和 artifact 命名空间应天然隔离（按项目+仓库区分）。
Oracle 来源: GitHub 行为 (GitHub-hosted runner 为 ephemeral VM, 每个 job 全新环境)。issues.md §1 描述了此风险在共享 runner 模型中尤为突出。

验证要点:
  - [负向] 项目 A 的 job 在 runner 写入文件后结束——项目 B 的后续 job 不应能看到这些文件
  - [负向] 项目 A 的 env 不影响项目 B 的 job
  - [负向] 项目 A 的 secret 值在项目 B 的 workflow 中不应可访问（跨项目 secret 隔离）
  - [负向] 项目 A 上传的 artifact 在项目 B 的 workflow 中不可直接下载

负向断言目标: 跨项目隔离——一个项目的数据不泄露到另一个项目的 workflow 运行中。判定证据：项目 B job 的 `ls $WORKSPACE` / `env` 不含项目 A 的残留数据。
优先级线索: RISK-SEC-01 (P0 blocker — 多租户隔离)
破坏级别:   full_instance (需在两个项目之间做跨项目验证)
来源输入:   security-knowledge/issues.md (§1 ★)
```

---

```
意图 ID:    INTENT-SEC-045
状态:      ★ NEW (enabled by security-knowledge/issues.md §2)
维度标签:   [security]
标题:       Secret 全生命周期管理——创建、更新、删除、过期、轮换

风险点:     issues.md §2 关注 secret 的「全生命周期安全问题」——不仅是运行时的脱敏，还包括：创建/更新/删除的权限控制、secret 在 workflow YAML 中的引用安全性、环境变量传递过程中的泄露风险、token 过期后的轮换机制、**过期 token 是否仍能通过缓存访问**。
预期系统行为:
  - Secret 创建/更新/删除操作应有权限控制 (谁有权限管理 secret)
  - Secret 更新后，新运行的 workflow 应使用新值 (不应缓存旧值)
  - Token 过期后不可再用于 API 调用 (包括缓存中的过期 token)
  - Secret 删除后，引用该 secret 的 workflow 应收到空值或错误
Oracle 来源: GitHub 行为 (secret lifecycle management) + issues.md §2。

验证要点:
  - [正向] secret 创建后立即可在 workflow 中引用
  - [正向] secret 更新后新 workflow run 应使用新值
  - [负向] secret 删除后引用该 secret 的 job 应收到空值或错误
  - [负向] 过期 token 通过缓存恢复后不应能通过 API 认证
  - [负向] 组织级 secret 在非授权仓库的 workflow 中不可访问

负向断言目标: Secret 生命周期各阶段行为正确——创建可用、更新生效、删除不可用、过期不可恢复。判定证据：各阶段 API 调用结果与预期一致。
优先级线索: RISK-SEC-01 (P0 blocker — secret 生命周期安全)
破坏级别:   none
来源输入:   security-knowledge/issues.md (§2 ★)
```

---

```
意图 ID:    INTENT-SEC-046
状态:      ★ NEW (enabled by security-knowledge/issues.md §3)
维度标签:   [security]
标题:       Workflow 日志的安全生命周期——保留期、下载权限、历史扫描

风险点:     issues.md §3 系统性地关注了日志的安全管理：日志默认保留多久、过期后是否彻底删除（不可恢复）、日志下载/导出是否需要权限控制、是否存在 API/工具可对历史日志做**敏感信息扫描**。
预期系统行为:
  - 日志应有明确的保留期 (如 90 天)，过期后不可访问
  - 日志下载/导出应受权限控制 (至少 write access)
  - 平台应提供（或声明不提供）历史日志敏感信息扫描能力
  - 不应存在 API 可绕过权限获取他人/他项目的日志
Oracle 来源: GitHub 行为 (log retention 默认 90 天, 企业可配置) + issues.md §3。

验证要点:
  - [负向] 非项目成员不应能通过 API 下载该项目的 workflow 日志
  - [负向] 超过保留期的日志不应可访问 (API 返回 404/410)
  - [正向] 日志下载权限=write 及以上
  - [正向] 平台文档声明日志保留期

负向断言目标: 日志访问受权限控制、日志过期不可恢复。判定证据：非授权用户 API 请求日志返回 403/404；过期日志请求返回 410 Gone。
优先级线索: RISK-SEC-02 (P1 — 日志安全)
破坏级别:   none
来源输入:   security-knowledge/issues.md (§3 ★)
```

---

```
意图 ID:    INTENT-SEC-047
状态:      ★ NEW (enabled by security-knowledge/issues.md §4)
维度标签:   [security]
标题:       共享文件系统 (/tmp, $HOME) 不应跨 job 残留敏感文件

风险点:     issues.md §4 关注 runner 的共享文件系统——`/tmp`、`/home/runner`、`$GITHUB_WORKSPACE` 等可能在 job 结束后残留敏感文件 (`.env`、`.git-credentials`)。若下一个 job (尤其是不同项目) 可访问这些文件，敏感数据泄露。Self-hosted runner 非 ephemeral 时此风险尤其严重。
预期系统行为: 每个 job 结束后，该 job 使用的所有文件系统路径 (workspace, /tmp, $HOME 下的临时目录) 应被彻底清理。或者 runner 为 ephemeral (一次性), job 后整个环境销毁。Self-hosted runner 应提供清理机制或文档警告残留风险。
Oracle 来源: GitHub 行为 (GitHub-hosted runner 为 ephemeral, 每个 job 全新环境) + issues.md §4。

验证要点:
  - [负向] job A 在 /tmp 写入含 secret 的文件后结束——job B 不应能看到该文件
  - [负向] job A 在 $HOME 写入 .git-credentials 后结束——job B 不应能看到
  - [负向] 缓存/artifact 目录不应包含意外的敏感文件 (.env 等)

负向断言目标: 共享文件系统在 job 间完全隔离——无跨 job 敏感文件可见。判定证据：job B 的 `find /tmp -name "*.env"` 返回空；`find $HOME -name ".git-credentials"` 返回空。
优先级线索: RISK-SEC-01 (P1 — 磁盘残留)
破坏级别:   full_instance (需在同 runner 上连续跑两个 job)
来源输入:   security-knowledge/issues.md (§4 ★)
```

---

```
意图 ID:    INTENT-SEC-048
状态:      ★ NEW (enabled by security-knowledge/issues.md §5)
维度标签:   [security]
标题:       Runner 网络隔离——出站控制 + SSRF 防护 + 内部服务暴露防护

风险点:     issues.md §5 系统性地关注了 workflow 运行时的网络攻击面：runner 是否可以访问内部网络/非公开服务 (SSRF 攻击面)、runner 的出站网络是否有限制 (防止数据外传到外部服务器)、fork PR workflow 是否与主 repo runner 共享网络命名空间。
预期系统行为:
  - Runner 不应能访问平台内部非公开服务 (如内部 API、数据库、管理接口)
  - Runner 的出站网络应仅限必要的外部服务 (如 GitHub/npm/pypi)，或不限但有速率/黑名单
  - Fork PR workflow 的网络访问范围应与内部 workflow 有区分 (至少文档说明)
  - Self-hosted runner 在内网部署时，不应成为攻击者访问内网的跳板
Oracle 来源: GitHub 行为 (GitHub-hosted runner 可出站访问 internet 但有限制) + issues.md §5。

验证要点:
  - [负向] workflow 中尝试 curl 访问 runner 内部 metadata 服务 (如 169.254.169.254)——应被阻止
  - [负向] workflow 中尝试 curl 访问 GitCode 内部 API (非公开)——应被阻止
  - [负向] fork PR workflow 不应能扫描同 runner 网络下的内部服务
  - [正向] workflow 可正常访问外部合法服务 (github.com, npmjs.org)

负向断言目标: SSRF 攻击面最小化——runner 不可访问内部服务、不可绕过网络边界。判定证据：内部地址 curl 返回 timeout/connection refused/403。
优先级线索: RISK-SEC-01 (P1 — 网络隔离)
破坏级别:   none (验证性探测, 不破坏网络)
来源输入:   security-knowledge/issues.md (§5 ★)
```

---

```
意图 ID:    INTENT-SEC-049
状态:      ★ NEW (enabled by security-knowledge/issues.md §5)
维度标签:   [security]
标题:       Self-hosted runner 在内网部署时的网络跳板风险

风险点:     issues.md §5 特别关注：self-hosted runner 在内网部署时可能成为攻击者的内网跳板。结合 GitHub 安全文档 (secure-use.md): self-hosted runner 「几乎永远不应用于公开仓库」——因为任何可提 PR 的人都能在 runner 上执行代码，进而横向移动访问内网资源。若 GitCode 的默认 runner 也是共享/非 ephemeral 的，此风险等比存在。
预期系统行为: 平台文档必须明确警告 self-hosted runner 的内网跳板风险。对于公开仓库，应推荐仅使用平台托管 runner。对于使用 self-hosted runner 的公开/内部仓库，应提供网络隔离指导（如 Kubernetes NetworkPolicy、firewall rules、runner 专用子网）。
Oracle 来源: GitHub 行为 (secure-use.md: self-hosted runner hardening) + issues.md §5。

验证要点:
  - [负向] 公开仓库的 self-hosted runner 上，fork PR 不应能访问 runner 所在的内网服务
  - [正向] 平台文档是否明确声明 self-hosted runner 的内网安全风险
  - [正向] 若 runner 支持 Kubernetes 部署，是否支持 NetworkPolicy 配置

负向断言目标: Self-hosted runner 不成为内网横向移动跳板——fork PR 代码无法访问 runner 所在网络的其他服务。判定证据：fork PR job 中 curl 内网地址返回 timeout/正拒绝；文档有明确的安全警告。
优先级线索: RISK-SEC-01 (P1 — 内网横向移动)
破坏级别:   none
来源输入:   security-knowledge/issues.md (§5 ★), github-reference/security/secure-use.md
```

---

### B.3 — Regression testing for confirmed historical bugs (from history/issues-encountered.md)

```
意图 ID:    INTENT-SEC-050
状态:      ★ NEW (enabled by history/issues-encountered.md #51 ★ P0)
维度标签:   [security]
标题:       [回归] fork 仓提 PR 应完全隔离主仓密钥——回归验证 #51

风险点:     history #51 是**已确认的真实安全漏洞**：「fork 仓提 PR 能够获取到主仓的密钥」。这是 fork PR 安全隔离的基准防线被击穿的实证。虽然此 bug 已被报告和处理，但安全隔离的回归风险是永久的——任何代码变更可能重新引入此问题。
预期系统行为: fork 仓提 PR 后，workflow 执行中对 `${{ secrets.* }}` 的引用应返回空字符串或触发错误——不应返回真实密钥值。
Oracle 来源: GitCode 规格 + history/issues-encountered.md #51 (★ P0 安全严重问题)。

验证要点:
  - [回归-负向] fork 仓创建 PR (含 workflow 引用项目级 Secret)——job 日志不应出现 secret 明文
  - [回归-负向] fork 仓创建 PR (含 workflow 引用组织级 Secret)——job 日志不应出现 secret 明文
  - [回归-负向] fork PR workflow 中尝试用 secret 值做 HTTP 认证——应返回认证失败
  - [回归-正向] 内部 PR 下同一 secret 应正常可用——确保 secret 本身是有效的

负向断言目标: fork PR 绝不可获取主仓任何密钥——历史 bug #51 已修复且不回退。判定证据：job 日志搜索已知 secret 值命中数 = 0；基于该 secret 的 API 调用返回 401/403。
优先级线索: RISK-SEC-01 (P0 blocker — 回归验证 #51)
破坏级别:   none
来源输入:   history/issues-encountered.md (#51 ★ P0 安全严重问题)
关联:       INTENT-SEC-001, INTENT-SEC-002 (互补——本 intent 专为回归验证)
```

---

```
意图 ID:    INTENT-SEC-051
状态:      ★ NEW (enabled by history/issues-encountered.md #66 ★ P0)
维度标签:   [security]
标题:       [回归] pull_request_target 的 fork PR secret 隔离——回归验证 #66

风险点:     history #66 记录了核心安全机制缺失：「pull_request_target 访问 secrets 的 fork PR 场景目前还未实现 (**开发中, 715**」——说明截至 2026-07-20, `pull_request_target` 事件的 fork PR secret 隔离**尚未正确实现**。这是 Security Lab Part 1 描述的 pwn request 的核心防线。需要在平台宣称支持后进行回归验证。
预期系统行为: (平台实现后) pull_request_target 事件下，fork PR workflow 应使用**目标仓库 base 分支**的 workflow 定义——即只有仓库维护者可控制执行逻辑。此时 ATOMGIT_TOKEN 拥有声明的高权限，Secret 可正常访问——**但这不是漏洞，而是设计的合法行为**。关键验证点：workflow 定义必须来自 base 分支而非 fork。
Oracle 来源: GitCode 规格 + history/issues-encountered.md #66 (★ P0 安全关注, 开发中)。

验证要点:
  - [回归-正向] 若 #66 已实现——pull_request_target 下 fork PR workflow 应使用 base 分支的 workflow 版本执行 (而非 fork 侧)
  - [回归-负向] fork 侧修改 pull_request_target workflow 添加 `echo secret`——不应被执行
  - [回归-正向] base 分支的 pull_request_target workflow 中显式 echo secret——应被遮蔽 (`***`)
  - [回归-状态] 若 #66 仍未实现——本 intent 标记为 blocked/by-design-gap

负向断言目标: pull_request_target 的 workflow 来源安全——来自 base 分支，不受 fork 侧修改影响。若平台尚未实现 secret 隔离，本 intent 为 blocker 状态。判定证据：执行日志中的 workflow steps 与 base 分支 YAML 一致。
优先级线索: RISK-SEC-01 (P0 blocker — 回归验证 #66)
破坏级别:   none
来源输入:   history/issues-encountered.md (#66 ★ P0 安全关注)
关联:       INTENT-SEC-003, INTENT-SEC-004 (互补——本 intent 专为回归验证)
```

---

```
意图 ID:    INTENT-SEC-052
状态:      ★ NEW (enabled by history/issues-encountered.md #85)
维度标签:   [security, completeness]
标题:       Workflow YAML 缓存不应导致旧版本 workflow 被执行

风险点:     history #85 记录了实用性的安全相关缺陷：「子 workflow 更新后从日志看用的还是旧代码 (yml 缓存问题)」。若 workflow YAML 被缓存而未使用最新版本，可能引发两类安全问题：(a) 安全修复后的 workflow 未生效——旧的有漏洞版本继续执行；(b) 攻击者利用缓存的时间窗口，在修复部署后仍触发旧版本。Security Lab Part 4 指出「非默认分支上的旧 workflow 仍可被利用」——若 YAML 缓存机制使旧版本残留，此风险进一步放大。
预期系统行为: 每次 workflow 触发时，应使用仓库中当前的 workflow YAML 版本——不应使用缓存的旧版本。若存在缓存（如对 reusable workflow 的缓存），应提供透明的缓存失效机制和版本标识。
Oracle 来源: history/issues-encountered.md #85 (已确认的 YAML 缓存问题) + Security Lab Part 4 (latent threats from old workflows)。

验证要点:
  - [负向] 修改 workflow YAML (如添加/修改 step) 并推送——下一次触发应执行新的 YAML 内容
  - [负向] 修改 reusable workflow YAML——调用方的下一次触发应使用新版本
  - [正向] 平台是否有机制确保 YAML 版本一致性 (如 ETag 或 version id)

负向断言目标: Workflow 始终执行仓库中的最新 YAML，不被缓存旧版本替代。判定证据：job 日志中的 step 列表与仓库当前 YAML 一致。
优先级线索: RISK-SEC-01 (P1 — 缓存一致性)
破坏级别:   none
来源输入:   history/issues-encountered.md (#85 ★ yml缓存未更新), security-knowledge/github-actions-security-series.md (Part 4)
```

---

```
意图 ID:    INTENT-SEC-053
状态:      ★ NEW (enabled by history/issues-encountered.md #82)
维度标签:   [security, compatibility]
标题:       `uses:` 字段应支持 `${{ }}` 表达式求值

风险点:     history #82 发现「uses 中不支持 `${{atomgit.repository}}`」——`uses:` 字段不接受表达式。这不仅是功能缺陷，也有安全影响：若 `uses:` 不支持表达式，workflow 作者不得不将仓库名硬编码，增加了配置复用的难度——在跨分支/跨仓库迁移时更易引入人为错误。从安全角度，`uses:` 字段的表达式求值应按与其他属性一致的规则处理：先求值再解析。若平台限制 `uses:` 字段不能使用表达式，应在文档中明确声明。
预期系统行为: `uses:` 字段中的 `${{ }}` 表达式应被正确求值——行为与 `run:`、`with:` 等其他字段中的表达式一致。若平台有意限制此能力 (如供应链安全考虑——防止动态 action 引用)，应有文档说明和有意义的错误信息。
Oracle 来源: GitHub 行为 (uses: 支持表达式求值) + history/issues-encountered.md #82。

验证要点:
  - [正向] `uses: ${{ atomgit.repository == 'owner/repo' && 'official_checkout' || 'fallback_checkout' }}`——应正确求值并引用
  - [负向] 若平台不支持 `uses:` 中的表达式——应产生明确的错误信息说明「uses 不支持表达式」
  - [负向] 表达式求值不应导致引用未预期的 action (表达式注入防护)

负向断言目标: uses 字段表达式求值行为可预测——支持与否都应文档化，不支持时给出清晰错误而非静默失败。判定证据：workflow 解析日志 / lint 输出明确指示 uses 字段的表达式能力。
优先级线索: RISK-SEC-02 (P2 — 兼容性/安全)
破坏级别:   none
来源输入:   history/issues-encountered.md (#82 ★ uses 不支持表达式)
```

---

### B.4 — Cross-referencing security series with existing coverage gaps

```
意图 ID:    INTENT-SEC-054
状态:      ★ NEW (cross-referencing security-knowledge/github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       pull_request_target workflow 对默认分支缓存仅有只读访问

风险点:     Security Lab Part 4 特别指出：pull_request_target workflow **对默认分支作用域下的缓存仅有 read-only 访问**——可恢复已有缓存条目但不能创建或覆盖。这是 GitHub 专门为 pull_request_target 增加的 cache 保护机制。需验证 GitCode 是否有等价保护。
预期系统行为: pull_request_target 触发时，cache write (save/upload) 应被拒绝或自动作用域隔离。cache restore 应正常工作（只读）。防止 fork PR 通过 pull_request_target 投毒缓存。
Oracle 来源: Security Lab Part 4 (cache read-only for pull_request_target) + pull_request_target.md GitHub 文档。

验证要点:
  - [正向] pull_request_target workflow 中 restore 缓存——应正常命中已有缓存
  - [负向] pull_request_target workflow 中 save/write 缓存——应被拒绝或写入隔离作用域
  - [负向] pull_request_target 写入的缓存不应被后续 push workflow 命中

负向断言目标: pull_request_target 下缓存仅只读——不可创建或覆盖默认分支缓存。判定证据：cache save step 输出 cache-saved=false (或返回 403)；后续 push workflow cache restore 不命中 pull_request_target 写入的条目。
优先级线索: RISK-SEC-01 (P1 — cache 投毒防护)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 4 ★)
关联:       INTENT-SEC-019, INTENT-SEC-020 (互补)
```

---

```
意图 ID:    INTENT-SEC-055
状态:      ★ NEW (cross-referencing security-knowledge/github-actions-security-series.md Part 3)
维度标签:   [security]
标题:       第三方 action 不应通过 input 默认值窃取 ATOMGIT_TOKEN

风险点:     Security Lab Part 3 揭示了一种巧妙的 token 窃取方式：控制 action YAML 定义的攻击者可以在 action 的 `inputs:` 中声明一个参数，其 `default` 设为 `${{ github.token }}`。当调用方未显式传入该参数时，默认值求值为 token——token 被注入到 action 内部可被攻击者利用。需验证 GitCode 的 action 机制是否对此有防护。
预期系统行为: action 的 `inputs.default` 中不应允许引用 `secrets.*` 或 `github.token` 上下文——这些应在 workflow YAML 层面求值，而非在 action 内部。或者平台在 action inputs 传递时 strip 这些敏感上下文引用。
Oracle 来源: Security Lab Part 3 (Token exposure through action input defaults)。

验证要点:
  - [负向] 第三方 action 的 inputs.default 设为 `${{ secrets.ATOMGIT_TOKEN }}`——实际传给 action 的值应为空或空字符串
  - [负向] action 的 inputs.default 设为 `${{ atomgit.token }}`——不应将内建 token 注入 action

负向断言目标: action 的 default 值不能窃取 token——敏感上下文在 action inputs 边界被正确隔离。判定证据：action 日志中打印的 input 值为空或 `***`，而非有效 token。
优先级线索: RISK-SEC-01 (P1 — token 窃取防护)
破坏级别:   none
来源输入:   security-knowledge/github-actions-security-series.md (Part 3 ★)
```

---

```
意图 ID:    INTENT-SEC-056
状态:      ★ NEW (cross-referencing security-knowledge/issues.md §4 + github-actions-security-series.md Part 4)
维度标签:   [security]
标题:       Self-hosted runner 在 job 结束后应执行 workspace 清理（或显式声明不清理）

风险点:     issues.md §4 关注共享盘残留，Security Lab Part 4 强调 ephemeral runner 的重要性。若 GitCode 涉及 self-hosted runner（自定义资源池）——已有 history 记录多个自定义资源池相关问题 (#7/#44/#52/#54/#69/#89)——非 ephemeral runner 上的 workspace 残留可能跨 job 可见。Ephemeral runner 的「job 后销毁整个环境」是消除此类风险的首选方案。若平台不提供 ephemeral runner，必须提供显式的清理机制。
预期系统行为: (a) 若 runner 是 ephemeral 的——job 结束后整个运行环境被销毁。 (b) 若 runner 非 ephemeral——平台必须在每个 job 前执行 workspace cleanup，且此清理应是不可绕过的。平台文档应声明 runner 类型及其清理行为。
Oracle 来源: GitHub 行为 (just-in-time/ephemeral runners) + Security Lab Part 4 + issues.md §4。

验证要点:
  - [负向] Self-hosted runner 上 job 结束后，下一个 job 不应能看到前 job 的 workspace 文件
  - [负向] 平台应提供 runner cleanup 行为的文档说明
  - [正向] 若 runner 为 ephemeral——验证 job 前后 runner 主机名/ID 不同 (新实例)

负向断言目标: 跨 job 无 workspace 残留——job 结束后 workspace 被彻底清理（或 runner 销毁）。判定证据：连续两个 job 的 ls $WORKSPACE 输出各自独立。
优先级线索: RISK-SEC-01 (P1 — workspace 清理)
破坏级别:   full_instance (需在同 runner 上连续跑两个 job)
来源输入:   security-knowledge/issues.md (§4 ★), security-knowledge/github-actions-security-series.md (Part 4)
```

---

## 覆盖度自检（按 agent CLAUDE.md 质量清单 + 新增 inputs）

对照 agent CLAUDE.md 质量清单 + 新增 security-knowledge/history 输入逐项自评：

| 覆盖项 | 覆盖状态 | 对应 Intent |
|--------|----------|-------------|
| fork PR 权限降级 (token 只读) | ✅ | INTENT-SEC-001 |
| fork PR secret 隔离 | ✅ | INTENT-SEC-002, INTENT-SEC-050 (回归) |
| pull_request_target 安全语义 | ✅ | INTENT-SEC-003, INTENT-SEC-004, INTENT-SEC-051 (回归) |
| pull_request_target TOCTOU 攻击 | ✅ ★ NEW | INTENT-SEC-037 |
| 非默认分支旧 workflow 潜伏威胁 | ✅ ★ NEW | INTENT-SEC-038 |
| issue_comment / IssueOps 审批绕过 | ✅ ★ NEW | INTENT-SEC-039 |
| secret 基础脱敏 (echo) | ✅ | INTENT-SEC-005 |
| secret base64/编码绕过脱敏 | ✅ | INTENT-SEC-006 |
| secret 拼接绕过脱敏 | ✅ | INTENT-SEC-007 |
| secret 多行脱敏 | ✅ | INTENT-SEC-008 |
| PR 标题/正文/分支名/commit msg 注入 | ✅ | INTENT-SEC-009, 010, 011, 012 |
| email 地址注入 | ✅ ★ NEW | INTENT-SEC-041 |
| 双重表达式求值 (模板注入) | ✅ ★ NEW | INTENT-SEC-040 |
| env 中间变量安全模式 | ✅ | INTENT-SEC-013 |
| GITHUB_ENV / GITHUB_OUTPUT 污染 | ✅ | INTENT-SEC-014 |
| permissions: {} 最小权限 | ✅ | INTENT-SEC-015 |
| 未声明 permissions 默认值 | ✅ | INTENT-SEC-016 |
| job 级 permissions 覆盖 | ✅ | INTENT-SEC-017 |
| 第三方 action pin (SHA) | ✅ | INTENT-SEC-018 |
| action input default 窃取 token | ✅ ★ NEW | INTENT-SEC-055 |
| fork PR cache 投毒 | ✅ | INTENT-SEC-019 |
| pull_request_target cache read-only | ✅ ★ NEW | INTENT-SEC-054 |
| 跨事件 cache 隔离 | ✅ | INTENT-SEC-020 |
| secret 命名约束 | ✅ | INTENT-SEC-021 |
| environment 审批保护 | ✅ | INTENT-SEC-022 |
| secret 全生命周期 (创建/更新/删除/过期) | ✅ ★ NEW | INTENT-SEC-045 |
| ATOMGIT_TOKEN 失效 | ✅ | INTENT-SEC-023 |
| 递归 workflow 防护 | ✅ | INTENT-SEC-024 |
| runner 残留隔离 | ✅ | INTENT-SEC-025 |
| self-hosted runner workspace 清理 | ✅ ★ NEW | INTENT-SEC-056 |
| multi-project runner 隔离 | ✅ ★ NEW | INTENT-SEC-044 |
| 共享文件系统跨 job 残留 | ✅ ★ NEW | INTENT-SEC-047 |
| artifact 跨信任边界 | ✅ | INTENT-SEC-026 |
| workflow_run artifact 投毒 | ✅ ★ NEW | INTENT-SEC-042 |
| workflow_run event 类型篡改 | ✅ ★ NEW | INTENT-SEC-043 |
| ::add-mask:: 命令安全 | ✅ | INTENT-SEC-027, 028 |
| workflow 文件篡改防护 | ✅ | INTENT-SEC-029 |
| action with 输入注入 | ✅ | INTENT-SEC-030 |
| composite action 内部注入 | ✅ | INTENT-SEC-031 |
| reusable workflow secret 泄露 | ✅ | INTENT-SEC-032 |
| 并发 token 隔离 | ✅ | INTENT-SEC-033 |
| PAT 权限模型文档 | ✅ | INTENT-SEC-034 |
| 表达式求值类型安全 | ✅ | INTENT-SEC-035 |
| ATOMGIT_TOKEN 内置 secret 安全 | ✅ | INTENT-SEC-036 |
| 网络隔离 (SSRF + 数据外传) | ✅ ★ NEW | INTENT-SEC-048 |
| self-hosted runner 内网跳板 | ✅ ★ NEW | INTENT-SEC-049 |
| 日志安全生命周期 (保留/下载/扫描) | ✅ ★ NEW | INTENT-SEC-046 |
| YAML 缓存一致性 | ✅ ★ NEW | INTENT-SEC-052 |
| uses: 表达式求值 | ✅ ★ NEW | INTENT-SEC-053 |

### OWASP CI/CD Top 10 映射 (新增覆盖)

| OWASP 条目 | 覆盖 Intent |
|------------|-------------|
| CICD-SEC-1: Insufficient Flow Control Mechanisms | INTENT-SEC-001, 002, 003, 004, 037, 038, 039, 043 |
| CICD-SEC-2: Inadequate Identity & Access Management | INTENT-SEC-015, 016, 017, 034 |
| CICD-SEC-3: Dependency Chain Abuse | INTENT-SEC-018, 030, 031, 055 |
| CICD-SEC-4: Poisoned Pipeline Execution (PPE) | INTENT-SEC-009, 010, 011, 012, 040, 041 |
| CICD-SEC-5: Insufficient PBAC (Pipeline-Based Access Controls) | INTENT-SEC-001, 002, 022, 050, 051 |
| CICD-SEC-6: Insufficient Credential Hygiene | INTENT-SEC-005, 006, 007, 008, 027, 028, 045 |
| CICD-SEC-7: Insecure System Configuration | INTENT-SEC-025, 044, 047, 048, 049, 056 |
| CICD-SEC-8: Ungoverned Usage of 3rd Party Services | INTENT-SEC-018, 030, 055 |
| CICD-SEC-9: Improper Artifact & Cache Integrity | INTENT-SEC-019, 020, 026, 042, 054 |
| CICD-SEC-10: Insufficient Logging & Visibility | INTENT-SEC-046 |

### 历史缺陷回归覆盖表

| History ID | 缺陷描述 | 回归验证 Intent |
|------------|----------|-----------------|
| #51 (P0) | fork PR 可获取主仓密钥 | INTENT-SEC-050 (★ NEW) |
| #66 (P0) | pull_request_target fork secret 隔离未实现 | INTENT-SEC-051 (★ NEW) |
| #85 | YAML 缓存导致旧 workflow 被执行 | INTENT-SEC-052 (★ NEW) |
| #82 | uses 字段不支持 `${{ }}` 表达式 | INTENT-SEC-053 (★ NEW) |

---

## 与已有用例的差异点（更新后）

| 已有用例 | 覆盖内容 | 本轮 intent 新覆盖 (vs 2026-07-20-01) |
|----------|----------|--------------------------------------|
| TC-011 | 基础 secret 脱敏 | secret 全生命周期 (SEC-045)、日志生命周期 (SEC-046) |
| TC-252 | ::add-mask:: 基础 | add-mask 返回值泄露已知 bug 回归 (SEC-027 updated) |
| TC-336 | pull_request_target 语法 | TOCTOU (SEC-037)、旧分支潜伏威胁 (SEC-038) |
| TC-345 | fork 触发事件 | 回归验证 #51/#66 (SEC-050, 051) |
| TC-301-305 | cache 基本使用 | pull_request_target cache read-only (SEC-054) |
| — | (无已有覆盖) | issue_comment 审批绕过 (SEC-039, ★ NEW) |
| — | (无已有覆盖) | 双重表达式求值 / 模板注入 (SEC-040, ★ NEW) |
| — | (无已有覆盖) | email 注入 (SEC-041, ★ NEW) |
| — | (无已有覆盖) | workflow_run artifact/event 投毒 (SEC-042, 043, ★ NEW) |
| — | (无已有覆盖) | 多项目 runner 隔离 (SEC-044, ★ NEW) |
| — | (无已有覆盖) | 网络隔离 SSRF (SEC-048, ★ NEW) |
| — | (无已有覆盖) | self-hosted runner 内网跳板 (SEC-049, ★ NEW) |
| — | (无已有覆盖) | action input default token 窃取 (SEC-055, ★ NEW) |
| — | (无已有覆盖) | workspace 清理 (SEC-056, ★ NEW) |

---

## 统计

- **总 intent 数**: 56 条
  - CARRIED OVER (2026-07-20-01): 36 条 (SEC-001 ~ SEC-036)
  - ★ NEW (enabled by security-knowledge/): 13 条 (SEC-037 ~ SEC-049)
  - ★ NEW (enabled by history/): 4 条 (SEC-050 ~ SEC-053)
  - ★ NEW (cross-referencing): 3 条 (SEC-054 ~ SEC-056)
- **P0 覆盖率**: 与 2026-07-20-01 相比，P0 blocker 新增 6 条 (SEC-037, SEC-039, SEC-044, SEC-045, SEC-050, SEC-051)，覆盖了 TOCTOU、多项目隔离、secret 生命周期、历史缺陷回归等上游盲区。
- **新增攻击面覆盖**: TOCTOU (1 条)、workflow_run 投毒 (2 条)、模板注入 (1 条)、email 注入 (1 条)、多租户隔离 (1 条)、网络隔离 (2 条)、日志安全 (1 条)、secret 生命周期 (1 条)、磁盘残留 (1 条)、历史回归 (4 条)、cache 精细控制 (1 条)、action input 窃取 (1 条)、workspace 清理 (1 条)。
- **输入利用率**: 5/5 个新增输入文件均被引用——github-actions-security-series.md (4 Parts, 10 intents), issues.md (5 sections, 6 intents), history/issues-encountered.md (4 confirmed bugs, 4 intents), history/gitcode-actions-list.md (context), existing-cases/cases.md (cross-ref).

---

> **复审建议**: 本轮在 2026-07-20-01 的 36 条 intent 基础上新增 20 条，总量 56 条。新增部分主要来自 Security Lab 4-part series 揭示的 TOCTOU/模板注入/workflow_run 投毒/email 注入等更精细的攻击面，以及 issues.md 关注的多项目隔离、网络隔离、磁盘残留、日志安全等运维层面的安全维度。建议：
> 1. TOCTOU (SEC-037)、issue_comment 审批绕过 (SEC-039)、双重表达式求值 (SEC-040) 是 Security Lab 揭露的**三种高危害但常被忽视**的模式——需有 CI/CD 安全经验的人复审验证方法的可执行性。
> 2. 回归验证 #51 (SEC-050) 和 #66 (SEC-051) 是**一经修复即可回归**的高价值 P0 用例——务必在平台宣称支持后第一时间执行。
> 3. 网络隔离 (SEC-048) 和 self-hosted runner 跳板 (SEC-049) 的验证依赖对 runner 基础设施的了解——若 runner 细节不可获取，标记为 blocked/by-infra-opacity。
> 4. 建议对多项目隔离 (SEC-044) 和共享文件系统残留 (SEC-047) 做一次系统性的跨项目穿透验证——这不仅是安全问题，也是多租户服务质量保障。
