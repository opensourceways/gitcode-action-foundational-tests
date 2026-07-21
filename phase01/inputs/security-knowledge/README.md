# inputs/security-knowledge/ （建议）— 已补充 ✅

放 **CI/CD 安全防御知识与漏洞模式**。只放防御知识与模式分析，**不放真实 exploit**。

## 导航

- **[github-actions-security-series.md](github-actions-security-series.md)** — GitHub Security Lab 系列 4 篇文章摘要
  - Part 1: Preventing Pwn Requests（`pull_request_target` 滥用）
  - Part 2: Untrusted Input（表达式注入、shell 注入）
  - Part 3: Building Blocks（第三方 Action 供应链安全）
  - Part 4: New Patterns and Mitigations（cache 投毒、artifact 投毒、TOCTOU、label gates）
- **[issues.md](issues.md)** — 已知安全风险与历史问题（5 大实证关注点）
  - 多项目环境隔离、敏感信息管理、日志脱敏、共享盘敏感信息、网络隔离

## OWASP CI/CD Top 10 摘要

| 排名 | 风险项 | 核心描述 | GitCode 测试关注点 |
|---|---|---|---|
| CICD-01 | 不充分的流水线访问控制 | 过度授权、缺乏最小权限原则 | `permissions:` 是否生效、ATOMGIT_TOKEN 默认权限 |
| CICD-02 | 依赖链滥用 | 恶意依赖、typosquatting | `uses:` 是否支持 commit hash pin |
| CICD-03 | 恶意流水线执行 | 未经审核的代码触发特权流水线 | `pull_request_target` 上下文隔离、fork PR secret 隔离 |
| CICD-04 | 流水线配置篡改 | 攻击者修改 `.github/workflows` | 分支保护、CODEOWNERS 等价机制 |
| CICD-05 | 薄弱的凭证与 secret 管理 | secret 泄露、硬编码凭证 | secret 日志遮蔽、base64/拼接绕过 |
| CICD-06 | 不充分的隔离与沙箱 | runner 跨 job 残留、共享盘泄露 | workspace 清理、cache 跨项目隔离 |
| CICD-07 | 脆弱的第三方集成 | 第三方 Action / App 权限过大 | Action marketplace 审核机制 |
| CICD-08 | 审计与日志不足 | 缺乏可追溯的安全事件记录 | 日志保留期、日志导出权限、脱敏完整性 |
| CICD-09 | 不安全的系统配置 | runner/OS/容器默认配置宽松 | 网络出站策略、SSRF 防护 |
| CICD-10 | 供应链安全缺口 | 从源码到部署的全链路信任缺失 | artifact 完整性校验、缓存隔离 |

## CI/CD 安全加固手册

### 1. 工作流设计原则
- **分离特权与非特权流水线**：`pull_request`（非特权）+ `workflow_run`（特权）是防止 Pwn Requests 的标准模式
- **最小权限原则**：默认 token 设为 read-only，job 级别显式声明 `permissions`
- **避免 comment 触发**：用 `labeled` activity type + commit SHA 替代 `issue_comment`，防止 TOCTOU 与绕过审批

### 2. 输入验证
- **所有用户可控字段视为不可信**：PR 标题/正文、分支名、commit message、email、评论内容
- **禁用内联表达式**：不可信值必须先存入中间环境变量，再在 shell 中引用
- **禁止双重求值**：警惕 Action 内部模板引擎的二次渲染

### 3. Secret 与 Token 管理
- **fork PR 完全隔离**：secret 不可见、token 降级为只读或无权限
- **日志遮蔽不可绕过**：验证 base64、拼接、分片、多行值等绕过手段
- **Token 生命周期**：支持过期/轮换，禁止通过缓存复活旧 token

### 4. 供应链安全
- **Action 引用 pin 到完整 commit hash**：禁止 `@main` 或短 hash
- **审计第三方 Action**：关注向外部主机发送数据的行为
- **Artifact / Cache 视为不可信**：下载后验证校验和，fork PR cache 必须隔离

### 5. Runner 与环境隔离
- **Job 结束后彻底清理 workspace**：包括 `/tmp`、环境变量、磁盘残留
- **网络出站限制**：防止 SSRF、数据外传、内部服务暴露
- **并发隔离**：项目 A 的 runner 资源不可被项目 B 读取

## CVE / 公开漏洞模式速查

| 漏洞模式 | 典型 CVE / 案例 | 缓解措施 | 关联文档 |
|---|---|---|---|
| `pull_request_target` 滥用 | GitHub Security Lab (2021) | 分离 workflow + 不 checkout 不信任代码 | security-series Part 1/4 |
| Shell 脚本注入（表达式内联） | 多起公开事件 | 中间环境变量模式 | security-series Part 2 |
| Cache 投毒 | TOCTOU + 权限绕过 | fork PR cache 隔离、权限最小化 | security-series Part 4 |
| Artifact 投毒 | `workflow_run` 链式攻击 | 校验 artifact 来源、视为不可信 | security-series Part 4 |
| 第三方 Action 供应链攻击 | `tj-actions/changed-files` 等事件 | pin commit hash、审计源码 | security-series Part 3 |
| Secret 日志脱敏绕过 | GitHub `::add-mask::` 历史缺陷 | 覆盖 base64/拼接/多行值测试 | issues.md §3 |

## 消费方

- **security agent**：生成安全维度 intent 与风险项的核心知识输入
- **case-writer agent**：编写安全用例时的攻击面参考与修复方案对照

## 缺失影响（已解决）

~~安全维度退化为通用清单，缺针对性。~~  
现已通过 GitHub Security Lab 系列摘要、OWASP Top 10 映射、5 大实证问题、加固手册与 CVE 速查表覆盖安全测试的核心攻击面。

**已补充 / 2 份文档 + 加固手册 + OWASP Top 10 + CVE 速查 / 2026-07-21**
