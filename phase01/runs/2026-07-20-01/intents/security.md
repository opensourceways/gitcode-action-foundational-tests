# Security Test Intents

> **Agent**: security (STRIDE / CI/CD attack-surface mapper)
> **Run**: 2026-07-20-01
> **输入快照**: gitcode-spec/security-permissions/ (token-permissions.md, pr-mr-pipeline-security.md, using-secrets.md), github-reference/security/ (secrets.md, pull_request_target.md, script-injections.md, secure-use.md, github-token.md), testing-focus.md §5/6/7/8, baseline/risk-register.md, existing-cases/cases.md
> **⚠️ 输入退化声明**: `security-knowledge/` 目录缺失（仅含 README 空壳）—— 缺少 OWASP CI/CD Top 10 摘要、CVE 模式分析、公开漏洞知识库。安全维度未获得针对性加固知识输入，以下 intent 基于通用威胁建模 + GitCode/GitHub 规格文档推导，覆盖面可能遗漏平台特有漏洞模式。**强烈建议补充后重跑本维度**。
> **人工复审建议**: 建议由具备 CI/CD 攻击面知识的 reviewer 逐条审阅后签出（见 agent 护栏第 4 条）。

---

## 信任边界总览

| 主体/资产 | 信任级别 | 说明 |
|-----------|----------|------|
| 外部 fork 贡献者 | **不可信** | 任何人可 fork 并提 PR，触发 workflow，控制 fork 仓库中的 workflow YAML 和执行代码 |
| 仓库 owner/maintainer | 可信 | 有 push 权限，可修改目标仓库 workflow 与 secret 配置 |
| PR 标题/正文/分支名 | **不可信** | 完全由外部贡献者控制，可能包含任意字符串 |
| 提交信息/commit message | **不可信** | fork 侧可控 |
| ATOMGIT_TOKEN | **敏感资产** | 自动生成的认证令牌，权限由 permissions 声明决定 |
| 项目/组织级 Secret | **敏感资产** | 需严格隔离，不可对不可信主体暴露 |
| Runner 工作区 | **敏感资产** | 执行环境，fork PR 代码不应获得写回权限 |
| Cache | **敏感资产** | 跨 run 共享的缓存，不可被 fork PR 污染 |
| Artifact | **敏感资产** | 跨 job 传递的产物 |

**核心信任边界线**: fork PR (`pull_request` 事件) 与内部事件 (`push` / `pull_request_target`) 之间存在一条硬隔离边界——前者应被视作完全不可信输入。所有安全 intent 最终都围绕「这条边界是否被正确执行」展开。

---

```
意图 ID:    INTENT-SEC-001
维度标签:   [security]
标题:       fork PR 触发 pull_request 时 ATOMGIT_TOKEN 应为只读

风险点:     外部贡献者通过 fork 提 PR，触发 `pull_request` 事件。若 ATOMGIT_TOKEN 保有写权限，恶意 PR 可修改仓库代码、操作 Issue/PR、推送标签，相当于代码执行+仓库接管。这是 CI/CD 最经典的攻击面之一。
预期系统行为: 来自 fork 的 `pull_request` 事件下，ATOMGIT_TOKEN 仅拥有 `repository: read` 权限，无论 workflow 中 permissions 声明为何。任何写操作（推送、PR 评论、Issue 创建、Webhook 管理）均应被拒绝。
Oracle 来源: GitCode 规格（token-permissions.md：「pull_request 事件来自 fork 仓库时，ATOMGIT_TOKEN 仅拥有 read 权限，无论 permissions 如何声明」）对齐 GitHub 行为（secrets.md：「pull_request from fork cannot access repository secrets; only GITHUB_TOKEN is passed, read-only」）。

验证要点:
  - [正向] fork PR 触发的 job 可正常 clone 代码（repository:read）
  - [负向] fork PR 触发的 job 不应能推送代码到目标仓库（repository:write 应被拒绝）
  - [负向] fork PR 触发的 job 不应能通过 API 创建/修改 PR 评论（pr:write 应被拒绝，即使 permissions 声明了 write）
  - [负向] fork PR 触发的 job 不应能读取项目级 Secret（无论 permissions 声明为何）

负向断言目标: ATOMGIT_TOKEN 在 fork `pull_request` 场景下仅具 read 权限——推送被拒返回非零退出码 / API 调用返回 403 / secret 引用返回空字符串。判定证据：job 日志中 git push 输出含 "Permission denied" 或 "403"；${{ secrets.X }} 值为空。

优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   none（纯防御性验证，只读不改）
来源输入:   gitcode-spec/security-permissions/token-permissions.md、gitcode-spec/security-permissions/pr-mr-pipeline-security.md、github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-002
维度标签:   [security]
标题:       fork PR 触发 pull_request 时不可访问项目/组织级 Secret

风险点:     这是 fork PR 隔离的核心安全机制。若 Secret 对 fork PR 可见，攻击者只需在 fork 的 workflow 中 echo 任意 Secret 即可窃取凭证。GitHub Actions 曾出现因 pull_request_target 误用导致 secret 泄露的 CVE 级事件。
预期系统行为: `pull_request` 来自 fork 时，workflow 对 `${{ secrets.* }}` 的引用应返回空字符串或触发错误，绝不应暴露 secret 原始值。
Oracle 来源: GitCode 规格（using-secrets.md：「pull_request 来自 fork 的 workflow 不可访问项目级 Secret」）对齐 GitHub 行为。

验证要点:
  - [负向] fork PR workflow 中 echo 项目级 Secret 到日志，日志不应出现原始值（返回空或 `***`）
  - [负向] fork PR workflow 中尝试用 Secret 做 HTTP 认证，请求不应成功
  - [正向] 同一 workflow 在非 fork（内部 PR）触发时，Secret 应正常可用

负向断言目标: fork PR 不可读取仓库/组织级 Secret——${{ secrets.X }} 求值为空字符串；基于 Secret 的 API 调用返回认证失败。判定证据：job 日志中 echo 输出为空；API 调用返回 401/403。

优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md、github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-003
维度标签:   [security]
标题:       pull_request_target 仅在 base 分支 workflow 定义中运行，不执行 fork 侧 workflow YAML

风险点:     `pull_request_target` 的核心安全承诺是「workflow 定义来自目标仓库 base 分支，而非 fork」。若平台实现存在缺陷导致实际执行了 fork 侧的 workflow YAML，外部贡献者可以在高权限上下文中运行任意命令——这是业界熟知的 "pwn request" 模式。GitHub 上已有多起因滥用 pull_request_target 导致的供应链安全事故。
预期系统行为: `pull_request_target` 触发时，实际执行的 workflow 定义文件应来自目标仓库的默认分支（如 main），即使 fork 侧修改了同名 workflow 文件。ATOMGIT_TOKEN 拥有 permissions 声明的完整权限（可写），Secret 可访问。
Oracle 来源: GitCode 规格（pr-mr-pipeline-security.md：「workflow 文件使用目标仓库（main 分支）的版本，而非 fork 中的版本」）对齐 GitHub 行为（pull_request_target.md：「the workflow is taken from the base repository's default branch, not from the pull request」）。

验证要点:
  - [正向] 目标仓库 base 分支有 pull_request_target workflow，fork 侧无修改——workflow 应正常执行
  - [负向] fork 侧修改（或新增）pull_request_target workflow 中的 run 命令，实际执行的不应是 fork 侧版本
  - [负向] fork 侧的 workflow 文件中添加的 shell 命令不应在 runner 上执行

负向断言目标: fork 侧对 pull_request_target workflow YAML 的任何修改不应影响实际执行的逻辑——执行的 workflow 定义来自 base 分支，fork 侧新增的命令不出现在日志中。判定证据：对比 fork 侧 YAML 与 job 日志中实际执行的命令文本。

优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md、github-reference/security/pull_request_target.md
```

---

```
意图 ID:    INTENT-SEC-004
维度标签:   [security]
标题:       pull_request_target 下显式 checkout fork PR head 代码后不应自动执行其中脚本

风险点:     pull_request_target 本身的 workflow 定义来自 base 分支（安全），但若 workflow 作者在 steps 中 `checkout ref: head.sha` 并随后执行 `make build` / `npm test` 等命令，等于在高权限上下文中运行了 fork 侧的任意代码——这是 "pwn request" 的标准形态。GitCode 的 checkout action 是否有等价于 GitHub `actions/checkout` v7+ 的 `allow-unsafe-pr-checkout` 保护待验证。
预期系统行为: 当 pull_request_target workflow 中 `uses: checkout with ref: ${{ atomgit.event.pull_request.head.sha }}` 后立即执行 `run: make build`，该 `make build` 实际运行的是 fork 侧代码。这是 workflow 作者的**有意识风险决策**，平台不应自动阻止——但平台应提供保护机制（如 checkout action 内置警告）或文档明确标注此风险。GitCode 若提供等价于 GitHub `allow-unsafe-pr-checkout` 的保护，默认应启用。
Oracle 来源: GitHub 行为（pull_request_target.md：「The checkout step alone does not execute untrusted code... The vulnerability is completed by the next step that runs code checked out」——这是 workflow 作者的责任，但 actions/checkout v7+ 默认阻止 unsafe checkout 需显式 opt-out）。

验证要点:
  - [正向] pull_request_target 下 checkout head.sha 后执行 fork 侧 Makefile/build 脚本——命令应被执行（这是作者的有意行为）
  - [负向] GitCode 的 checkout action 应在 checkout fork PR head 时产生警告或要求显式确认（如 GitHub 的 allow-unsafe-pr-checkout）
  - [负向] pull_request_target workflow 在无显式 checkout ref 时，不应自动获取 fork 侧代码变更

负向断言目标: pull_request_target 在未显式 checkout head.sha 时不应执行 fork 侧的任何代码。若显式 checkout 了 head.sha，checkout action 应产生安全警告或要求 opt-in。判定证据：job 日志中 checkout step 的安全提示（如有）；对比 checkout 后的 git log 确认代码来源。

优先级线索: RISK-SEC-01（P0 blocker）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/pr-mr-pipeline-security.md、github-reference/security/pull_request_target.md
```

---

```
意图 ID:    INTENT-SEC-005
维度标签:   [security]
标题:       Secret 值直接 echo 到日志时应被脱敏为 `***`

风险点:     workflow 中错误地 echo secret 值是最常见也是最基础的泄露途径。平台必须确保 secret 值被替换为 `***`。已有用例 TC-011 覆盖了基础场景（`echo "${{secrets.T}}"`），本 intent 关注更严格的验证：确保脱敏确实发生（而非仅语境依赖）、以及跨多种输出模式的覆盖。
预期系统行为: 任何通过 `${{ secrets.X }}` 引用且出现在 stdout/stderr 日志输出中的 secret 值，必须被替换为 `***`。即使是完全逐字 echo，也不应泄露。
Oracle 来源: GitCode 规格（using-secrets.md：「Secret 值在日志中自动替换为 ***」）对齐 GitHub 行为（secrets.md：「GitHub automatically redacts the contents of all GitHub secrets that are printed to workflow logs」）。

验证要点:
  - [正向] echo 非 secret 文本时日志正常显示
  - [负向] echo secret 值的日志行中不应出现原始 secret 明文（应显示 `***` 或等效遮蔽）
  - [负向] 同一 job 内多次引用同一 secret，每次出现均应被遮蔽

负向断言目标: 日志中不出现 secret 明文——`grep <已知secret值>` 在 job 日志中命中数为 0。判定证据：API 拉取 job 日志后对已知 secret 值做全文搜索。

优先级线索: RISK-SEC-02（P0 blocker — 信息泄露）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md、github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-006
维度标签:   [security]
标题:       Secret 经过 base64 编码后 echo 到日志仍应被脱敏

风险点:     GitHub 的 secret 脱敏机制不能保证防住所有变形——如果 secret 值被 base64 编码、URL 编码、或通过子字符串拼接后输出，自动 redaction 可能失效。攻击者可能利用这一点：在 fork PR 的 workflow 中将 secret base64 编码后输出，因为编码后的字符串与原始 secret 不匹配从而绕过脱敏。这是公开文档中已知的局限。
预期系统行为: 理想情况下，base64 编码后的 secret 在日志中仍被遮蔽；至少应对常见编码模式有基本防护。若无法做到完全覆盖（GitHub 同样承认此局限），应至少有相关文档声明。
Oracle 来源: GitHub 行为（secrets.md：「there are multiple ways a secret value can be transformed, this redaction is not guaranteed」——承认局限但对常见编码有部分防护）。

验证要点:
  - [负向] `echo <secret> | base64` 的输出若被输出到日志，不应泄露 secret 的原始值
  - [负向] base64 编码后再解码输出原始 secret 的场景，日志中的某一步应被遮蔽

负向断言目标: 日志中不出现未经遮蔽的 secret 值，无论是否经过编码变换。判定证据：API 拉取 job 日志后搜索原始 secret 值 + base64 编码后的值；若平台支持对 base64 编码值的遮蔽，则两项均不应命中。

优先级线索: RISK-SEC-02（P1 — 已知局限但需验证基线）
破坏级别:   none
来源输入:   github-reference/security/secrets.md（「redaction is not guaranteed」段）
```

---

```
意图 ID:    INTENT-SEC-007
维度标签:   [security]
标题:       Secret 通过子字符串拼接后 echo 到日志应仍被脱敏

风险点:     与 base64 编码类似，将 secret 拆分为两段再拼接输出（如 `echo "${FIRST_HALF}${SECOND_HALF}"`）可能绕过基于精确匹配的脱敏机制。这是已知的 secret masking 绕过手法。
预期系统行为: 理想情况下平台应对 secret 值的任意子串片段也有脱敏覆盖（如每个字符级单独 mask）。若无法做到，至少对完整拼接结果应有效遮蔽。
Oracle 来源: GitHub 行为（secrets.md——承认变换可绕过红化）。

验证要点:
  - [负向] 将 secret 拆为两半再拼接 echo，日志中不应出现完整的原始 secret 值
  - [负向] 逐个字符拼接 secret 再输出，日志中不应出现完整 secret 值

负向断言目标: 完整 secret 明文不出现在日志中——任何形式的拼接重组后 echo 均不泄露。判定证据：日志全文搜索原始 secret 值命中数为 0。

优先级线索: RISK-SEC-02（P1）
破坏级别:   none
来源输入:   github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-008
维度标签:   [security]
标题:       Secret 包含多行文本时应整体被脱敏

风险点:     多行 secret（如 SSH 私钥、PEM 证书）的脱敏更难——每行需要独立匹配，且换行符可能导致遮蔽失败。GitHub 文档提到「structured data as secret can cause redaction to fail」。
预期系统行为: 多行 secret 值中每一行在日志中出现时均应被遮蔽。secret 设置时若包含换行符，平台应正确处理（存储、注入、脱敏全线支持）。
Oracle 来源: GitHub 行为（secure-use.md：「Never use structured data as a secret — redaction depends on exact match」）。

验证要点:
  - [负向] 多行 secret 的每一行 echo 到日志时均应被遮蔽
  - [负向] 单行包含换行转义符（\n）的 secret 在日志中出现时不应被还原为实际换行后的明文

负向断言目标: 多行 secret 无一行的明文出现在日志中。判定证据：逐行 grep secret 各行的内容在 job 日志中命中数为 0。

优先级线索: RISK-SEC-02（P1）
破坏级别:   none
来源输入:   github-reference/security/secrets.md、github-reference/security/secure-use.md
```

---

```
意图 ID:    INTENT-SEC-009
维度标签:   [security]
标题:       PR 标题中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     将 `${{ atomgit.event.pull_request.title }}` 直接写进 `run:` 的 shell 脚本，表达式在 shell 执行前即被求值替换——若 PR 标题包含分号、反引号、命令替换等 shell 元字符，攻击者可注入任意命令。这是 GitHub Actions 最常见的高危漏洞类型，已被 CWE-94 收录。已有用例 TC-033 发现了 atomgit.event 返回对象字面量的问题（bash 报 syntax error），但未系统覆盖注入。
预期系统行为: 这是**用户的使用安全责任**而非平台自动防护——但平台至少应在以下层面提供防护：(a) expr 求值阶段对特定字符做转义（如单引号未闭合时报错而非静默通过）；(b) 文档明确警告脚本注入风险；(c) 若提供的 workflow linter/validator 能对「将不可信上下文直接写入 run:」模式产生 warning。
Oracle 来源: GitHub 行为（script-injections.md：「Expressions inside ${{ }} are evaluated and substituted before the shell script runs」——和 GitCode 机制一致）。

验证要点:
  - [负向] PR 标题含分号+命令（如 `fix"; ls /"`），在被直接插入 `run:` 的脚本中不应执行该命令
  - [负向] PR 标题含反引号命令替换，不应被执行
  - [正向] 平台在 expr 求值阶段对危险字符的处理行为应一致（报错或转义），不应静默执行

负向断言目标: 通过 PR 标题注入的额外 shell 命令不应在 runner 上执行。判定证据：job 日志中不出现注入命令的执行痕迹（如 ls 的输出、文件列表）；若平台选择报错而非静默注掉，job 应有明确错误信息。

优先级线索: RISK-SEC-02（P0 blocker — 注入）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、testing-focus.md §6
```

---

```
意图 ID:    INTENT-SEC-010
维度标签:   [security]
标题:       PR 正文（body）中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     与 PR 标题相同，PR 正文（`atomgit.event.pull_request.body` 或 `atomgit.event.issue.body`）同样是不可信输入。正文通常更长、更复杂，注入面更大。
预期系统行为: 同 INTENT-SEC-009——平台应提供危险的上下文引用模式的检测或文档警告。用户应使用中间环境变量方式（env: TITLE: ${{ ... }}）安全引用不可信输入，而非直接插入 run:。
Oracle 来源: GitHub 行为（script-injections.md——推荐使用中间 env 变量而非直接插值）。

验证要点:
  - [负向] PR 正文含多行注入 payload（shell 命令），被直接插入 run: 后不应被执行
  - [负向] PR 正文含 $() 命令替换、反引号命令替换，均不应被执行

负向断言目标: PR 正文中的 shell 元字符不应被解释执行为命令。判定证据：job 日志中不出现注入命令的输出。

优先级线索: RISK-SEC-02（P0 blocker — 注入）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、testing-focus.md §6
```

---

```
意图 ID:    INTENT-SEC-011
维度标签:   [security]
标题:       分支名中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     分支名是完全由开发者控制的自由文本（允许包含 `/`、`-`、`_` 以及某些特殊字符）。GitHub 文档特别指出 `zzz";echo${IFS}"hello";#` 可以是合法的分支名。将 `${{ atomgit.ref_name }}` 直接插入 shell 脚本同样存在注入面。
预期系统行为: 分支名中的 shell 元字符不应被解释执行。平台不应让分支名中的命令注入成功运行。
Oracle 来源: GitHub 行为（script-injections.md：「branch names... can be quite flexible in terms of their permitted content... would be a possible attack vector」）。

验证要点:
  - [负向] 分支名含分号+命令，被直接插入 run: 后不应执行该命令
  - [负向] 分支名含管道符 + 命令，不应被执行

负向断言目标: 分支名中的特殊字符不应被解释为 shell 命令。判定证据：job 日志中不出现注入命令的副作用。

优先级线索: RISK-SEC-02（P0 blocker — 注入）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、testing-focus.md §6
```

---

```
意图 ID:    INTENT-SEC-012
维度标签:   [security]
标题:       提交信息（commit message）中的不可信输入不应通过 ${{ }} 直接插入 run: 导致命令注入

风险点:     提交信息同样是不可信输入（fork 侧完全可控）。`${{ atomgit.event.head_commit.message }}` 若直接插入 `run:` 中执行，提交信息中的换行与反引号可能构成命令注入。
预期系统行为: 同 INTENT-SEC-009——平台不应让提交信息中的 shell 元字符被解释执行。
Oracle 来源: GitHub 行为（script-injections.md——commit message 是较少被提及但同等有效的注入面）。

验证要点:
  - [负向] 提交信息含反引号命令替换，不应被执行
  - [负向] 提交信息含分号+额外命令，不应被执行

负向断言目标: 提交信息中的附加命令不产生执行副作用。判定证据：job 日志中不出现注入命令的执行痕迹。

优先级线索: RISK-SEC-02（P0 blocker — 注入）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、testing-focus.md §6
```

---

```
意图 ID:    INTENT-SEC-013
维度标签:   [security]
标题:       通过环境变量安全引用不可信输入应不触发脚本注入

风险点:     这是 GitHub Actions 文档推荐的注入缓解方式——通过 `env:` 将不可信上下文赋给中间环境变量，再在 `run:` 中通过 `$VAR`（而非 `${{ }}`）引用。验证 GitCode 平台是否支持此安全模式。
预期系统行为: 通过 env 中间变量引用的不可信输入，shell 元字符不会被解释——它们被当作字面字符串处理。
Oracle 来源: GitHub 行为（script-injections.md：「Use an intermediate environment variable」）。

验证要点:
  - [正向] env 中间变量方式引用的 PR 标题中虽含 `"; ls /"` 等元字符，但 ls 不应被执行
  - [正向] env 中间变量方式的 workflow 应正常完成（不被 shell 注入打断）

负向断言目标: 此种安全引用模式下注入不可行——env 中间变量将不可信输入当作字面字符串。判定证据：job 日志中 env 变量的值保留原始字符（含分号/引号）但不触发命令执行；workflow 正常完成。

优先级线索: RISK-SEC-02（P1 — 安全最佳实践的可用性验证）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、testing-focus.md §6
```

---

```
意图 ID:    INTENT-SEC-014
维度标签:   [security]
标题:       不可信输入注入到 GITHUB_ENV / GITHUB_OUTPUT 文件不导致环境变量污染

风险点:     若 workflow 将不可信输入写入 `GITHUB_ENV`（在 GitCode 侧可能为 `ATOMGIT_ENV` 或等效文件），后续 step 读取该环境变量时可能发生二次注入。若文件写入协议存在解析差异（如换行处理不一致），可能导致环境变量被注入额外赋值。
预期系统行为: `GITHUB_ENV` / `GITHUB_ENV` 文件写入协议应对值内容做安全处理——多行值或含特殊字符的值不导致额外的环境变量被注入。平台的文件解析应与 GitHub 一致（单行 `KEY=VALUE` 格式，换行分界）。
Oracle 来源: GitHub 行为（workflow commands 规范——GITHUB_ENV 使用 `KEY=VALUE<<EOF` 多行定界符语法处理特殊字符）。

验证要点:
  - [负向] 向 GITHUB_ENV 写入含换行符的不可信值，不应导致额外的环境变量被注入
  - [负向] 向 GITHUB_OUTPUT 写入含特殊字符的值，后续 step 读取时不应被二次解释

负向断言目标: GITHUB_ENV/GITHUB_OUTPUT 文件写入/读取协议不被不可信输入破坏。判定证据：后续 step echo 环境变量值 = 原始写入值 / step 检查 env 数量 = 预期值（无额外注入变量）。

优先级线索: RISK-SEC-02（P0 blocker — 注入）
破坏级别:   none
来源输入:   testing-focus.md §6、github-reference/security/script-injections.md
```

---

```
意图 ID:    INTENT-SEC-015
维度标签:   [security]
标题:       permissions: {}（空对象）使 ATOMGIT_TOKEN 持有最小默认权限

风险点:     若平台未正确处理 `permissions: {}`（空对象），token 可能继承仓库级默认权限而非最小权限。GitCode 文档声明空 permissions 时 ATOMGIT_TOKEN 仅具 `repository: read` 最小默认权限——需验证。
预期系统行为: workflow 声明 `permissions: {}`（空）时，ATOMGIT_TOKEN 仅拥有 `repository: read`，不可写仓库、不可操作 PR/Issue、不可管理 Webhook。
Oracle 来源: GitCode 规格（token-permissions.md：「permissions: {}（空）→ ATOMGIT_TOKEN 仅拥有最小默认权限（repository:read）」）。

验证要点:
  - [负向] permissions: {} 下，`git push` 到目标仓库应被拒绝
  - [负向] permissions: {} 下，通过 API 操作 PR（创建评论、合并）应返回 403
  - [正向] permissions: {} 下，`git clone` 应正常成功

负向断言目标: 空 permissions 等于最小权限——所有写操作被拒绝。判定证据：写操作返回非零退出码或 HTTP 403。

优先级线索: RISK-SEC-01（P0 blocker — 权限越界）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md
```

---

```
意图 ID:    INTENT-SEC-016
维度标签:   [security]
标题:       未声明 permissions 时 ATOMGIT_TOKEN 使用仓库设置中的默认权限

风险点:     permissions 的默认值语义是兼容性差异高发区——GitHub 与 GitCode 的默认行为可能不同。如果 GitCode 默认给 read-write 而用户以为默认是只读，则所有 workflow 运行在高权限下。
预期系统行为: 未声明 permissions 时，ATOMGIT_TOKEN 的权限应等于仓库设置中定义的默认值（不是平台硬编码的固定值）。文档声明「使用仓库设置中定义的权限」——需验证这一行为。
Oracle 来源: GitCode 规格（token-permissions.md：「未声明 permissions → 使用仓库设置中定义的权限」）。

验证要点:
  - [正向] 仓库默认权限设为 repository:read，未声明 permissions 的 workflow 应能 clone 但不能 push
  - [正向] 仓库默认权限设为 repository:write，未声明 permissions 的 workflow 应能 push

负向断言目标: 未声明 permissions 时 token 权限 = 仓库默认值——权限不被意外放大或缩小。判定证据：push/clone 结果与仓库默认权限设置一致。

优先级线索: RISK-SEC-01（P0 blocker — 默认权限行为不明）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md
```

---

```
意图 ID:    INTENT-SEC-017
维度标签:   [security]
标题:       job 级 permissions 声明可覆盖 workflow 级声明

风险点:     遵循最小权限原则的关键能力：允许 workflow 级设默认（较严），特定 job 申请额外权限（较宽）。若 job 级覆盖不生效，所有 job 只能使用 workflow 级权限——宽松场景下权限过大；严格场景下 job 功能受阻。已有用例 TC-275 覆盖了配置字段存在性，但未验证实际权限生效。
预期系统行为: job 级 `permissions:` 声明覆盖 workflow 级的同名权限域。job 未声明时继承 workflow 级的声明。
Oracle 来源: GitCode 规格（token-permissions.md：「顶层声明 permissions → 所有 job 继承顶层权限，除非 job 级覆盖」）。

验证要点:
  - [正向] workflow 级设 repository:none，job 级设 repository:read——job 应能 clone
  - [负向] workflow 级设 pr:write，job 级设 pr:none——job 不应能通过 API 操作 PR
  - [负向] workflow 级设 repository:read，job 级未设——job 权限不应变为 write

负向断言目标: job 级权限声明严格遵循——job 级覆盖生效，未设则继承 workflow 级，不存在意外的权限放大。判定证据：对比 job API 调用结果（成功/403）与 job 级 permissions 声明一致。

优先级线索: RISK-SEC-01（P1 — 权限模型正确性）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md
```

---

```
意图 ID:    INTENT-SEC-018
维度标签:   [security]
标题:       第三方 action 引用未 pin 到 commit SHA 时有平台警告

风险点:     `uses: owner/repo@v1`（tag）的引用是可变的——tag 可被重指向不同的 commit，若 action 维护者账号被接管或被恶意更新，所有引用该 action 的 workflow 将运行恶意代码。GitHub 安全加固强烈建议 pin 到完整 commit SHA（`uses: owner/repo@<40-char-SHA>`）。GitCode 若未提供等价安全保障（pin 建议/警告/verified creator），供应链风险高于 GitHub。
预期系统行为: 平台应至少对浮动引用（tag/branch）提供警告或推荐 commit SHA。理想情况下，action registry 应显示验证标识（如 GitHub 的 "Verified creator"）。
Oracle 来源: GitHub 行为（secure-use.md：「Pin actions to a full-length commit SHA — the only way to use an action as an immutable release」）。

验证要点:
  - [正向] 提交使用 `uses: action@<commit SHA>` 的 workflow——应接受并正常运行
  - [负向] 提交使用 `uses: action@main`（浮动分支）的 workflow——平台是否产生 lint/安全警告
  - [负向] tag 被覆盖指向新 commit 后，引用该 tag 的 workflow 拉取到的 action 代码是否更新（验证可变性）

负向断言目标: 平台对浮动引用的使用有可见警告机制；SHA-pinned 引用接受且不受 tag 改写影响。判定证据：workflow 提交时的 lint 输出 / job 日志中的 action checkout 信息。

优先级线索: RISK-SEC-02（P1 — 供应链安全）
破坏级别:   none
来源输入:   github-reference/security/secure-use.md、testing-focus.md §7
```

---

```
意图 ID:    INTENT-SEC-019
维度标签:   [security]
标题:       fork PR 不应能写入或污染主分支的依赖缓存

风险点:     cache 是跨 run 共享的状态存储。fork PR 若可以写入缓存（如通过 `uses: cache` step 写缓存项），攻击者可以在 PR 中写入被污染的依赖缓存（替换了恶意版本的 npm 包、编译产物），后续主分支的 workflow 读取该缓存后执行被污染代码。GitHub 对 `pull_request_target` 限制了缓存为只读，对 `pull_request` fork PR 的缓存隔离也有限制。
预期系统行为: fork PR 触发的 workflow 不应能写入对主分支可见的缓存 key（缓存 key 应按分支/事件类型作用域隔离）。或者 fork PR 写入的缓存应在不同作用域下，主分支 workflow 读取时不命中 fork PR 写入的条目。
Oracle 来源: GitHub 行为（pull_request_target.md：「workflows triggered by pull_request_target have read-only access to the cache in the default branch's scope」——对 pull_request fork PR 的缓存也有类似隔离）。

验证要点:
  - [负向] fork PR workflow 写入一个 cache key，随后主分支 push workflow 读取同 key 时不应命中 fork PR 写入的缓存
  - [负向] fork PR workflow 不应能覆盖主分支已存在的缓存条目

负向断言目标: fork PR 的缓存写入与主分支缓存隔离——主分支 workflow 不命中 fork PR 写入的缓存；主分支已有缓存不被 fork PR 覆盖。判定证据：主分支 workflow 的 cache restore 日志显示 cache miss（而非命中 fork PR 写入的条目）。

优先级线索: RISK-SEC-01（P0 blocker — 缓存投毒）
破坏级别:   none
来源输入:   testing-focus.md §8、github-reference/security/pull_request_target.md
```

---

```
意图 ID:    INTENT-SEC-020
维度标签:   [security]
标题:       同一 workflow 多次运行之间的 cache 不应跨不同事件类型互相污染

风险点:     不仅是 fork PR——即使都是内部事件，不同触发类型的缓存作用域若未正确隔离，也可能导致 cache 投毒。例如 schedule 触发写入的缓存不应被 push 触发无条件信任。
预期系统行为: cache key 的作用域应按分支和触发事件类型隔离。push 写入的缓存可被同分支后续 push 命中；pull_request 写入的缓存不应被 push 命中；schedule 写入的缓存与 push 隔离。
Oracle 来源: GitHub 行为（cache 作用域按 branch + 触发事件隔离）。

验证要点:
  - [正向] 同分支两次 push 事件：第一次写入 cache，第二次恢复应命中
  - [负向] push 事件写入的 cache，pull_request 事件（内部 PR）恢复时应命中（同分支共享）
  - [负向] fork PR 写入的 cache，内部 push 不应命中

负向断言目标: 跨事件类型和作用域的缓存隔离正确——不应命中的 cache key 返回 miss。判定证据：cache restore step 的输出（cache-hit = true/false）。

优先级线索: RISK-SEC-01（P1 — 缓存隔离）
破坏级别:   none
来源输入:   testing-focus.md §8、github-reference/security/pull_request_target.md
```

---

```
意图 ID:    INTENT-SEC-021
维度标签:   [security]
标题:       Secret 命名遵守约束（大写字母+数字+下划线，不以 ATOMGIT_ / 数字开头）

风险点:     Secret 命名约束若不严格执行，可能导致：以 ATOMGIT_ 开头的 secret 与系统变量冲突、数字开头的 secret 被误解为字面量、含特殊字符的 secret 导致 YAML 解析错误。GitCode 文档声明了与 GitHub 一致的约束。已有用例 TC-008/009 覆盖了创建和引用层面，但未验证约束执行。
预期系统行为: 创建 secret 时，平台应校验命名：仅允许 `[A-Z0-9_]+`，拒绝以 `ATOMGIT_` 或数字开头，给出明确错误提示。
Oracle 来源: GitCode 规格（using-secrets.md：「仅允许大写字母、数字和下划线，不得以 ATOMGIT_ 开头，不得以数字开头」）对齐 GitHub 行为。

验证要点:
  - [正向] 合法名称（如 `DEPLOY_KEY`, `NPM_TOKEN_2024`）应能创建
  - [负向] 名称以 `ATOMGIT_` 开头（如 `ATOMGIT_MY_TOKEN`）——应被拒绝并有错误提示
  - [负向] 名称以数字开头（如 `1MY_SECRET`）——应被拒绝
  - [负向] 名称含小写字母或特殊字符（如 `my-token`, `deploy.key`）——应被拒绝

负向断言目标: 不合规的 secret 名称在创建时被平台拒绝。判定证据：创建 API 或 UI 操作返回明确错误信息。

优先级线索: RISK-SEC-02（P2 — 配置安全）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md
```

---

```
意图 ID:    INTENT-SEC-022
维度标签:   [security]
标题:       环境（environment）级 Secret 受审批规则保护

风险点:     GitCode 文档提到环境级 Secret 可配置审批人——若无此保护，绑定了 `environment: prod` 的 job 在未审批时就能读取生产 Secret，环境隔离形同虚设。GitHub 的环境保护规则支持 required reviewers 和 wait timer。已有用例 TC-010 发现 environment 字段不被平台识别，需验证当前状态。 预期系统行为: 若平台当前版本支持 environment 保护——job 声明 `jobs.<id>.environment: prod` 后，job 在审批通过前应处于等待状态，不可读取环境级 Secret。审批通过后 job 开始执行并可读取。若 platform 尚不支持，本 intent 记录为「待能力就绪后重测」。
Oracle 来源: GitCode 规格（using-secrets.md：「环境级 Secret 可配置审批人，未经审批 job 不可访问」）。

验证要点:
  - [正向] 审批通过后 job 开始执行，可读取环境级 Secret
  - [负向] 未审批时 job 应等待，不应执行
  - [负向] 若 environment 字段当前不可用（如 TC-010 发现的「unknown property」），本 intent 状态为 blocked

负向断言目标: 未审批的 job 不能开始执行，不能读取环境级 Secret。判定证据：job 状态为 queued/waiting；API 返回 pending approval 状态。

优先级线索: RISK-SEC-02（P1 — 若支持则 blocker，否则记录为平台能力缺口）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/using-secrets.md、existing-cases/cases.md (TC-010)
```

---

```
意图 ID:    INTENT-SEC-023
维度标签:   [security]
标题:       ATOMGIT_TOKEN 在 job 结束后应自动失效

风险点:     若 token 在 job 结束后可继续使用（未过期或可刷新），攻击者可能通过延迟使用窃取到 token 的后续 abuse。GitHub 的 GITHUB_TOKEN 在 job 结束时过期。GitCode 的 ATOMGIT_TOKEN 应遵循相同生命周期。
预期系统行为: ATOMGIT_TOKEN 的生命周期严格限定为单次 job——job 结束后 token 应立即失效，不可用于后续 API 调用。
Oracle 来源: GitCode 规格（token-permissions.md：「每次流水线运行时，AtomGit Action 自动生成 ATOMGIT_TOKEN」——隐含每次 job 独立生成）对齐 GitHub 行为（github-token.md：「GITHUB_TOKEN expires when the job finishes」）。

验证要点:
  - [正向] job 运行期间，使用 ATOMGIT_TOKEN 的 API 调用应正常返回
  - [负向] job 完成后，使用同一 ATOMGIT_TOKEN 值的 API 调用应返回 401/403

负向断言目标: job 结束后的 ATOMGIT_TOKEN 不可再用。判定证据：job 完成后 replay API 调用返回认证失败。

优先级线索: RISK-SEC-01（P1 — token 生命周期安全）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md、github-reference/security/github-token.md
```

---

```
意图 ID:    INTENT-SEC-024
维度标签:   [security]
标题:       ATOMGIT_TOKEN 触发的操作不应产生递归 workflow 运行

风险点:     workflow 使用 ATOMGIT_TOKEN 推送代码或创建 PR 后，若平台将此操作事件解释为新的 workflow 触发，可能导致无限递归（如 push → workflow → push → workflow...）。GitHub 默认防止此行为。GitCode 应有等价防护。
预期系统行为: 使用 ATOMGIT_TOKEN 执行的 git push / PR 创建 / Issue 评论等操作，不应递归触发新的 workflow run（或应进入需审批状态）。
Oracle 来源: GitHub 行为（github-token.md：「Events triggered by GITHUB_TOKEN will generally not create a new workflow run」）。

验证要点:
  - [负向] workflow 中使用 ATOMGIT_TOKEN 推送新 commit——不应触发新的 workflow 运行
  - [负向] workflow 中使用 ATOMGIT_TOKEN 创建 PR——不应自动触发该 PR 的 workflow（或应进入 approval-required 状态）

负向断言目标: token 触发的操作不产生非预期的递归 workflow。判定证据：确认仅有 1 个 workflow run 被该 push/PR 触发（而非链式触发的多个 runs）。

优先级线索: RISK-SEC-01（P1 — 递归攻击 DoS / 资源耗尽）
破坏级别:   none
来源输入:   github-reference/security/github-token.md
```

---

```
意图 ID:    INTENT-SEC-025
维度标签:   [security]
标题:       fork PR 触发的 pull_request workflow 不应有持久的 runner 状态残留

风险点:     若 runner 在 fork PR job 结束后未正确清理（工作目录、环境变量、安装的依赖、后台进程），下一个 job（可能是高权限的内部 workflow）可能被 fork PR job 的残留状态污染。这需要 runner 是 ephemeral（一次性）的或具有严格的 job 间隔离。
预期系统行为: 每个 job 运行在干净的环境中——fork PR job 的工作区、环境变量、docker 容器、后台进程在 job 结束后被完全清理，不可被后续 job 访问。若 runner 复用，清理必须完成。
Oracle 来源: GitHub 行为（GitHub-hosted runner 为 ephemeral VM，每个 job 获得全新环境）。

验证要点:
  - [负向] fork PR job 在 runner 工作区写入文件后结束，同 runner 后续的内部 job 不应能看到这些文件
  - [负向] fork PR job export 的环境变量不影响同 runner 后续 job
  - [负向] fork PR job 启动的后台进程在 job 结束后应被终止

负向断言目标: fork PR job 的执行环境在 job 结束后完全隔离于后续 job。判定证据：后续 job 的 `ls $GITHUB_WORKSPACE` 和 `env` 输出不含前一个 fork PR job 的残留内容。

优先级线索: RISK-SEC-01（P0 blocker — runner 隔离）
破坏级别:   full_instance（需验证 runner 清理机制）
来源输入:   testing-focus.md §4、github-reference/security/secure-use.md
```

---

```
意图 ID:    INTENT-SEC-026
维度标签:   [security]
标题:       跨 job artifact 在 fork PR 场景下不应被后续高权限 job 无条件信任

风险点:     fork PR workflow 上传了 artifact（如构建产物），若另一个高权限 workflow（如 push 或 pull_request_target）下载并使用该 artifact 而未经校验，攻击者可上传恶意 artifact 进行二次攻击。GitHub 的 `workflow_run` 事件中特别警告需 treat artifacts from other workflows with caution。
预期系统行为: artifact 作用域应与触发事件和权限上下文绑定——fork PR 上传的 artifact 不应被内部 push workflow 自动下载（需显式 cross-workflow 引用且有安全警告）。
Oracle 来源: GitHub 行为（secure-use.md：「Workflows triggered on workflow_run should treat artifacts from other workflows with caution」）。

验证要点:
  - [负向] fork PR workflow 上传 artifact，后续内部 push workflow 不应能自动下载该 artifact（需显式引用 fork PR 的 run ID）
  - [负向] 若支持跨 workflow artifact 下载，平台应提供 artifact 来源标识

负向断言目标: fork PR 的 artifact 不被后续内部 workflow 隐式继承。判定证据：内部 workflow 的 artifact 下载列表不含 fork PR 上传的条目（除非显式跨 workflow 引用）。

优先级线索: RISK-SEC-01（P1 — artifact 跨信任边界污染）
破坏级别:   none
来源输入:   testing-focus.md §8、github-reference/security/secure-use.md
```

---

```
意图 ID:    INTENT-SEC-027
维度标签:   [security]
标题:       `::add-mask::` workflow 命令的正确性与安全性

风险点:     `::add-mask::` 命令允许 workflow 动态注册额外需脱敏的值。若命令实现有误（如 mask 注册失败静默通过、mask 可被 `::stop-commands::` 解除），动态 secret 可能泄露。已有用例 TC-252（add-mask）未覆盖安全验证层。
预期系统行为: `::add-mask::VALUE` 注册的值应在后续日志中与内置 secret 同等遮蔽。`::stop-commands::` 不应恢复已被 mask 的值。
Oracle 来源: GitHub 行为（secure-use.md：「Use ::add-mask::VALUE to mask non-secret sensitive info」）。GitCode 对应有 `workflow-commands` 支持此命令。

验证要点:
  - [正向] `echo '::add-mask::MY_DYNAMIC_SECRET'` 后 `echo MY_DYNAMIC_SECRET`，日志应显示 `***`
  - [负向] 发出 `::stop-commands::` 后 echo 被 mask 的值，不应恢复为明文（mask 注册应不可逆）
  - [负向] 不同 step 多次注册不同 mask 值，不应相互覆盖或泄露

负向断言目标: 动态 mask 值在注册后整 job 生命周期内被遮蔽；stop-commands 不会恢复 mask。判定证据：日志中动态注册的敏感值以 `***` 出现。

优先级线索: RISK-SEC-02（P1）
破坏级别:   none
来源输入:   github-reference/security/secure-use.md
```

---

```
意图 ID:    INTENT-SEC-028
维度标签:   [security]
标题:       fork PR 下 `::add-mask::` 命令注册新 mask 不应影响主分支 job

风险点:     若 fork PR job 中 `::add-mask::` 的效果泄露到 runner 级别（而非限定在当前 job），mask 表可能被恶意填充大量条目导致主分支 job 的合法 secret 脱敏被干扰。需要验证 mask 注册的隔离性。
预期系统行为: `::add-mask::` 注册的 mask 仅在当前 job 内生效；不同 job（包括同 runner 上后续 job）的 mask 表应独立。
Oracle 来源: GitHub 行为（secrets.md：「The runner can only redact secrets used within the current job」——mask 作用域是 job 级）。

验证要点:
  - [负向] fork PR job 中注册的 mask 值，在后续同 runner 的内部 job 中不应生效
  - [负向] fork PR job 中注册大量 mask 条目，不应影响后续 job 的性能或脱敏正确性

负向断言目标: mask 表的 job 级隔离——fork PR job 的 mask 不影响其他 job。判定证据：后续 job 中 echo fork PR 注册的 mask 值，应显示为明文（因为该 job 没有该 mask）。

优先级线索: RISK-SEC-01（P1）
破坏级别:   none
来源输入:   github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-029
维度标签:   [security]
标题:       fork PR 的 workflow 不应能修改目标仓库的 workflow 文件

风险点:     fork PR 的 ATOMGIT_TOKEN 仅 read——但若 token 权限降级未生效，或通过其他路径（如 API 绕过），fork PR 有可能修改 `.gitcode/workflows/*.yml` 文件内容。这会直接导致供应链攻击——修改后的 workflow 在下一次触发的内部事件（如 push）中以高权限运行攻击者代码。GitHub 将此列为高优先级防护（建议用 CODEOWNERS 保护 workflow 目录）。
预期系统行为: fork PR 触发的 workflow 不应能推送对 `.gitcode/workflows/` 目录的任何修改，也不应能通过 API 修改 workflow 文件。
Oracle 来源: GitHub 行为（secure-use.md：「Add .github/workflows to the code owners list so any proposed changes require approval」）。

验证要点:
  - [负向] fork PR workflow 尝试通过 git push 修改 workflow YAML——应被拒绝
  - [负向] fork PR workflow 尝试通过 API 修改/上传 workflow 文件——应返回 403
  - [正向] fork PR 通过正常的 PR diff（workflow 文件在 PR 分支中）——这应被视为正常的代码审查流程

负向断言目标: fork PR 的 workflow run 不能直接修改目标仓库 workflow 定义。判定证据：git push 返回 "Permission denied" / API 返回 403。

优先级线索: RISK-SEC-01（P0 blocker — workflow 篡改防护）
破坏级别:   none
来源输入:   github-reference/security/secure-use.md、testing-focus.md §7
```

---

```
意图 ID:    INTENT-SEC-030
维度标签:   [security]
标题:       第三方 action 的输入参数中的不可信值不应导致 action 内部代码注入

风险点:     即使 workflow 作者使用了 action 而非内联脚本（推荐的安全实践），若将不可信输入直接传给 action 的 `with:` 参数，而 action 内部又以不安全方式处理该参数（如直接插入 shell 命令），注入仍然发生。关键是平台是否对 action 有沙箱或输入校验机制。
预期系统行为: action 接收 `with:` 参数时，不可信输入应被当作纯数据——不应在 action 内部被二次解释为代码。action 的 JavaScript runner 环境应天然免疫 shell 注入（不经过 shell），但若 action 自身 `exec()` 了传入参数则仍脆弱。
Oracle 来源: GitHub 行为（script-injections.md：「Use an action instead of an inline script — avoids injection because the value isn't used to generate a shell script」）。

验证要点:
  - [负向] 将含 shell 元字符的 PR 标题作为 action 的 with 参数传入，action 处理后的日志输出不应包含注入命令的执行痕迹
  - [正向] 使用安全的 JavaScript/TypeScript action，标题含特殊字符应被正确处理为字符串

负向断言目标: with 参数中的不可信输入不被 action 内执行引擎解释为代码。判定证据：action 日志中不出现注入命令的执行痕迹；action 正常完成或产生明确的校验错误。

优先级线索: RISK-SEC-02（P1 — action 输入边界）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、testing-focus.md §7
```

---

```
意图 ID:    INTENT-SEC-031
维度标签:   [security]
标题:       composite action 内部的 `run:` 步骤中引用不可信 inputs 不应导致注入

风险点:     composite action 封装了多个 `run:` step——若 composite action 内部将 `${{ inputs.x }}` 直接插入 `run:`（而 inputs 来自外部不可信调用方），shell 注入仍然发生。这要求平台对 composite action 内的表达式求值与普通 workflow 同等对待。
预期系统行为: composite action 声明内部 step 时，expression evaluation 应在 shell 执行前完成——与普通 workflow 的 `run:` 行为一致。不可信输入若直接写入 `run:` 同样面临注入风险，但这是 action 作者的责任。平台应提供 lint 警告。
Oracle 来源: GitHub 行为（composite action 的 `run:` 与普通 workflow run 同一执行模型）。

验证要点:
  - [负向] 将含 shell 注入字符的不可信值传入 composite action 的 inputs，该 input 直接用于 `run:` 时不应执行注入命令
  - [正向] composite action 内通过 env 中间变量使用的 inputs 应安全

负向断言目标: composite action 内的注入不成功（与普通 workflow 注入防护水平一致）。判定证据：job 日志中不出现注入命令的副作用。

优先级线索: RISK-SEC-02（P1）
破坏级别:   none
来源输入:   testing-focus.md §7、github-reference/security/script-injections.md
```

---

```
意图 ID:    INTENT-SEC-032
维度标签:   [security]
标题:       reusable workflow（workflow_call）调用方传入的 secrets 不应被被调用方泄露到日志

风险点:     调用方通过 `secrets: inherit` 或显式 `secrets: {KEY: ${{ secrets.X }}}` 将 secret 传给被调用的 reusable workflow——若被调用方不安全处理（echo 到日志），secret 将泄露。这是信任边界：调用方信任被调用方保护传入的 secret。
预期系统行为: secret 在被调用方 workflow 的日志中同等受脱敏保护——不论 secret 来自调用方传入还是被调用方自己的 secret，遮蔽行为应一致。
Oracle 来源: GitHub 行为（secret masking 对传入 secrets 同样生效）。

验证要点:
  - [负向] 被调用方 workflow 中 echo 调用方传入的 secret，日志应显示 `***`
  - [负向] 被调用方将传入的 secret 做 base64 编码后输出，不应泄露

负向断言目标: 跨 workflow 传入的 secret 在接收方日志中同等脱敏。判定证据：被调用方 job 日志搜索 secret 明文命中数 = 0。

优先级线索: RISK-SEC-02（P1）
破坏级别:   none
来源输入:   testing-focus.md §7、github-reference/security/secrets.md
```

---

```
意图 ID:    INTENT-SEC-033
维度标签:   [security]
标题:       并发 workflow（concurrency）下的 token/secret 隔离安全

风险点:     并发场景下同一仓库的多个 workflow runs 同时运行——若 token/secret 在 job 间的隔离仅依赖 runner 进程边界而 runner 被复用，高权限 job 可能读取到并发低权限 job 的 secret。需要验证同 runner 上的并发隔离。
预期系统行为: 同一 runner 上同时运行的多个 jobs 之间的 token 和 secret 完全隔离——一个 job 不能通过文件系统或进程间通信读取到另一个 job 的 secret。
Oracle 来源: GitHub 行为（每个 job 获得独立的 GITHUB_TOKEN 和独立工作区）。

验证要点:
  - [负向] 并发 job A（有 secret 访问）不应能从同 runner 上并发 job B 的工作区读到 job B 的环境变量
  - [负向] 并发 job 不应能通过 `/proc` 或共享内存读取到其他 job 的 process args（含 secret）

负向断言目标: 并发 job 间 secret/token 完全隔离。判定证据：job A 的日志中不出现 job B 的 secret 或 token 值。

优先级线索: RISK-SEC-01（P1 — 并发隔离）
破坏级别:   full_instance
来源输入:   testing-focus.md §3/§4
```

---

```
意图 ID:    INTENT-SEC-034
维度标签:   [security]
标题:       用户专属 token / PAT 的使用不应影响平台安全模型

风险点:     若用户在自己的 workflow 中使用个人访问令牌（PAT）或手动创建的 token 替代 ATOMGIT_TOKEN，该 token 的权限不受 `permissions:` 字段约束——可能绕过 fork PR 隔离。平台是否有机制检测或警告此行为？
预期系统行为: 平台不应直接禁止用户使用自备 token（因为可能是需要特定权限的合法场景），但文档应明确警告：`permissions:` 仅控制 ATOMGIT_TOKEN，手动注入的 token 不受约束，须自行管理权限。
Oracle 来源: GitHub 行为（github-token.md——明确区分 GITHUB_TOKEN 自动生成 vs PAT 手动管理）。

验证要点:
  - [正向] 使用自备 PAT 的 fork PR workflow——secret 可被访问（因为 PAT 是用户主动暴露的）
  - [负向] 平台文档是否明确声明 permissions 不约束手动注入的 token

负向断言目标: 平台文档明确声明 permissions 仅控制 ATOMGIT_TOKEN，手动 token 需自行管理——不应让用户误以为 permissions 约束了所有 token。判定证据：GitCode 安全文档中是否存在此声明。

优先级线索: RISK-SEC-02（P2 — 文档/易用性安全）
破坏级别:   none
来源输入:   github-reference/security/github-token.md
```

---

```
意图 ID:    INTENT-SEC-035
维度标签:   [security]
标题:       事件负载（event payload）中不可信字段在 expression evaluation 阶段的类型安全

风险点:     `${{ atomgit.event.* }}` 返回的是 JSON 对象——若事件负载中的字段类型与 workflow 作者预期不符（如字符串 vs 数字 vs 对象），可能导致意外的类型 coercion 或注入。已有用例 TC-033 发现 `atomgit.event` 返回对象字面量导致 bash 报错（syntax error near unexpected token '('），说明表达式求值产物没有被安全 escape。
预期系统行为: `${{ }}` 表达式的求值结果被替换进 YAML 后的产物应在 shell 上下文中是安全的——至少不应因为数据结构（如对象字面量）导致 shell 语法错误或执行意外代码。
Oracle 来源: GitHub 行为（表达式求值后替换为 JSON 字符串或特定类型的字面值）。

验证要点:
  - [负向] `${{ atomgit.event }}` 被用于 `run:` 不应导致 shell 语法错误（应为序列化后的字符串）
  - [负向] `${{ atomgit.event.* }}` 中嵌套对象/数组被用于条件判断 `if:` 时不应崩掉解析器
  - [正向] `${{ toJSON(atomgit.event) }}` 或 `fromJSON()` 函数若支持，应返回合法 JSON

负向断言目标: expression evaluation 产物在替换后不导致 shell 语法错误或非预期代码执行。判定证据：job 日志无 syntax error；若无法安全替换，平台应在前置 lint/parse 阶段报错。

优先级线索: RISK-SEC-02（P1 — 表达式求值安全）
破坏级别:   none
来源输入:   github-reference/security/script-injections.md、existing-cases/cases.md (TC-033)
```

---

```
意图 ID:    INTENT-SEC-036
维度标签:   [security]
标题:       平台内置 secret（ATOMGIT_TOKEN）不应在未授权上下文被引用泄露

风险点:     `${{ secrets.atomgit_token }}` 是系统预置的 secret 引用——需验证其脱敏行为与用户创建的 secret 一致，且在 fork PR 场景下返回空值（而非 token 明文）。已有用例 TC-100 覆盖了 secrets.atomgit_token 的脱敏，但 fork PR 下的行为未验证。
预期系统行为: fork PR 下 `${{ secrets.atomgit_token }}` 返回空或降级后的只读 token，其值在日志中应被脱敏。
Oracle 来源: GitCode 规格（token-permissions.md / using-secrets.md——ATOMGIT_TOKEN 是自动生成的 secret）。

验证要点:
  - [负向] fork PR 下 echo `${{ secrets.atomgit_token }}`——日志输出应为 `***` 或空，不应是有效 token
  - [负向] 内部 push 下 echo `${{ secrets.atomgit_token }}`——日志输出应被遮蔽为 `***`

负向断言目标: ATOMGIT_TOKEN 在 fork PR 下为空/降级，在内部事件下被脱敏——任何情况下日志均不泄露 token 明文。判定证据：日志搜索 token 前缀（如 `ghs_` 或 GitCode 对应 token 前缀）命中数 = 0。

优先级线索: RISK-SEC-01（P0 blocker — token 泄露）
破坏级别:   none
来源输入:   gitcode-spec/security-permissions/token-permissions.md、gitcode-spec/security-permissions/using-secrets.md
```

---

## 覆盖度自检

对照 agent CLAUDE.md 质量清单逐项自评：

| 覆盖项 | 是否覆盖 | 对应 Intent |
|--------|----------|-------------|
| fork PR 权限降级（token 只读） | ✅ | INTENT-SEC-001 |
| fork PR secret 隔离 | ✅ | INTENT-SEC-002 |
| pull_request_target 安全语义 | ✅ | INTENT-SEC-003, INTENT-SEC-004 |
| secret 基础脱敏（echo） | ✅ | INTENT-SEC-005 |
| secret base64/编码绕过脱敏 | ✅ | INTENT-SEC-006 |
| secret 拼接绕过脱敏 | ✅ | INTENT-SEC-007 |
| secret 多行脱敏 | ✅ | INTENT-SEC-008 |
| PR 标题注入 | ✅ | INTENT-SEC-009 |
| PR 正文注入 | ✅ | INTENT-SEC-010 |
| 分支名注入 | ✅ | INTENT-SEC-011 |
| commit message 注入 | ✅ | INTENT-SEC-012 |
| env 中间变量安全模式 | ✅ | INTENT-SEC-013 |
| GITHUB_ENV / GITHUB_OUTPUT 污染 | ✅ | INTENT-SEC-014 |
| permissions: {} 最小权限 | ✅ | INTENT-SEC-015 |
| 未声明 permissions 默认值 | ✅ | INTENT-SEC-016 |
| job 级 permissions 覆盖 | ✅ | INTENT-SEC-017 |
| 第三方 action pin（SHA） | ✅ | INTENT-SEC-018 |
| fork PR cache 投毒 | ✅ | INTENT-SEC-019 |
| 跨事件 cache 隔离 | ✅ | INTENT-SEC-020 |
| secret 命名约束 | ✅ | INTENT-SEC-021 |
| environment 审批保护 | ✅ | INTENT-SEC-022 |
| ATOMGIT_TOKEN 失效 | ✅ | INTENT-SEC-023 |
| 递归 workflow 防护 | ✅ | INTENT-SEC-024 |
| runner 残留隔离 | ✅ | INTENT-SEC-025 |
| artifact 跨信任边界 | ✅ | INTENT-SEC-026 |
| ::add-mask:: 命令安全 | ✅ | INTENT-SEC-027, INTENT-SEC-028 |
| workflow 文件篡改防护 | ✅ | INTENT-SEC-029 |
| action with 输入注入 | ✅ | INTENT-SEC-030 |
| composite action 内部注入 | ✅ | INTENT-SEC-031 |
| reusable workflow secret 泄露 | ✅ | INTENT-SEC-032 |
| 并发 token 隔离 | ✅ | INTENT-SEC-033 |
| PAT 权限模型文档 | ✅ | INTENT-SEC-034 |
| 表达式求值类型安全 | ✅ | INTENT-SEC-035 |
| ATOMGIT_TOKEN 内置 secret 安全 | ✅ | INTENT-SEC-036 |

## 与已有用例的差异点

| 已有用例 | 覆盖内容 | 本批 intent 新覆盖 |
|----------|----------|-------------------|
| TC-011 | 基础 secret 脱敏（echo） | base64/拼接/多行绕过、fork PR 下 secret 可用性 |
| TC-252 | ::add-mask:: 基础使用 | add-mask 安全性（跨 job 隔离、stop-commands 不恢复）|
| TC-275 | jobs.<id>.permissions 字段存在性 | 权限实际生效（空 permissions 最小权限、job 级覆盖）|
| TC-351-353 | permissions 单域 read/write 配置 | 跨域组合、fork PR 强降级、未声明时的默认行为 |
| TC-336 | pull_request_target 触发语法 | pull_request_target 安全语义完整验证（base 分支执行、checkout head.sha 风险）|
| TC-345 | fork 触发事件 | fork PR + pull_request 权限降级、secret 隔离 |
| TC-301-305 | cache 基本使用 | fork PR cache 隔离、跨事件 cache 作用域|
| TC-100-102 | secrets.atomgit_token 引用/脱敏 | fork PR 下 token 实际权限、token 生命周期|

## 已知缺口（待补充输入后完善）

以下安全领域因 `security-knowledge/` 和 `business-context/` 缺失而无法深入：

1. **GitCode 特有 CVE/漏洞模式**：无历史漏洞参考，无法针对已知已修漏洞设计回归验证。
2. **自托管 Runner 内网环境攻击面**：无部署信息，无法评估 runner 是否可在内网横向移动、访问内部服务。
3. **OIDC / 短时凭据**：GitCode 是否支持 OIDC 未知——若支持，相关 token 交换安全性需覆盖；若不支持，此条标记为 N/A。
4. **workflow 命令注入（`::` 前缀）**：除 `::add-mask::` 和 `::stop-commands::` 外，GitCode 支持的全部 workflow 命令列表未知——每条命令都有独立的注入/滥用面。
5. **runner 容器逃逸**：无 runner 基础设施细节，无法设计容器/VM 逃逸验证。
6. **Dependabot/自动版本更新**：不确定 GitCode 是否有等价的安全更新机制。
7. **速率限制与 DoS 防护**：fork PR 批量触发消耗 runner 资源——无容量参数无法建模。

---

> **复审建议**：本批次 36 条 intent 覆盖了 CI/CD 安全的 6 个核心攻击面（fork PR 隔离 / secret 脱敏 / 脚本注入 / 权限模型 / 供应链 / cache-artifact 跨边界）。强烈建议由具备 CI/CD 安全实战经验的 reviewer 逐条审阅，重点关注：
> 1. 注入面（INTENT-SEC-009 至 SEC-014）的 oracle 预期是否合理（平台防护 vs. 用户责任边界）
> 2. pull_request_target（INTENT-SEC-003/004）的语义验证是否足够——这是历史最高危面
> 3. cache 投毒（INTENT-SEC-019/020）的验证方法是否可执行（依赖平台 cache 实现细节）
>
> 建议在补充 `security-knowledge/` 输入后重跑本维度，重点补充：OWASP CI/CD Top 10 对应覆盖、GitHub Actions 已知 CVE 的对标验证。
