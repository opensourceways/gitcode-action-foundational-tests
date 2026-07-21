# inputs/history/

历史经验输入，让风险优先级有实证依据。

消费方：全体 agent（尤其 orchestrator 定火力）· 风险登记册

---

## 当前内容

### issues-encountered.md

来源：`gitcode issues.xlsx` 工作表「遇到的问题」，101 行，2026-07-20 导出。

涵盖试点项目：mindcluster · MindIE-SD · pytorch · openlibing · openubmc · op-plugin · akg · mindie · MindSpore

**数量**：101 条原始问题（编号连续，含 2 条图片型问题已省略），跨越 2026 年 5 月至 7 月。

**高频问题域**（已在文件末尾汇总）：

| 类别 | 条数 | 代表问题 |
|------|------|---------|
| 变量/参数处理 | 15+ | `${{ }}` 求值、bad substitution、类型转换（#75）、中划线（#38）、yml 缓存未更新（#85） |
| Plugin/Action 兼容性 | 12+ | setup-* 版本支持、checkout PR 预合并不支持（#25/#71）、composite action 不支持（#41） |
| 日志/调试体验 | 5+ | 日志无法下载（#6）、加载 7min（#14）、乱序（#80）、不显示（#81） |
| Runner/资源调度 | 10+ | 自定义资源池拉镜像失败（#44/#52/#54）、arm/x86 架构不区分（#48） |
| workflow_call / 依赖 | 8+ | 子任务无法拉起（#30）、if 不生效（#64）、matrix needs 依赖 bug（#101） |
| 触发/调度 | 8+ | fork PR 触发不了（#22）、手动触发参数（#23）、频繁触发（#67） |
| 上下文/系统变量 | 7+ | atomgit 字段缺失（#3/#20）、ATOMGIT.REPOSITORY 返回占位符（#62） |

**P0 安全问题**：
- `#51`：fork PR 可获取主仓密钥（安全隔离失败）
- `#66`：`pull_request_target` 的 fork PR secret 隔离未实现（开发中，715 计划上线）

### gitcode-actions-list.md

来源：`gitcode issues.xlsx` 工作表「action」，26 行，2026-07-20 导出。

包含 25 个官方 Action 的引用名（`uses:` 值）、用途分类、已知缺陷编号对照，以及 P0/P1 完备性覆盖优先级建议。

覆盖分类：代码检出 · 语言运行时安装（setup-jdk/gradle/node/yarn/pnpm/python/go）· 构建加速与 IaC · Shell 执行 · 制品管理 · OBS 对象存储 · SWR 容器镜像 · Docker · K8s 部署 · CI/CD 工具集成

### gitcode issues.xlsx

原始导出文件，保留备查。

---

已补充 / 2026-07-20
