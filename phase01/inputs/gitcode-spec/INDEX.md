# GitCode Action（AtomGit Action）离线文档索引

> 来源：https://docs.gitcode.com/docs/help/home/org_project/pipeline/
> 抓取日期：2026-07-20 ｜ 抓取工具：WebFetch（页面转 Markdown）
> 共 50 页，镜像官方文档目录结构。GitCode 流水线引擎底层为 **AtomGit Action**，文档中多以「AtomGit Action」称呼。
> **持续勘误**：文档更新后可用 `/phase01-update` 或直接重抓对应页；每个文件头部 `<!-- source | fetched -->` 记录了来源与日期。

## 目录

| # | 文件 | 官方页 |
|---|---|---|
| 00 | [00-overview.md](00-overview.md) | 产品总览 |
| 01 | [01-quick-start.md](01-quick-start.md) | 快速开始 |
| **核心概念** | | |
| 02 | [core-concepts/workflow-job-step-action.md](core-concepts/workflow-job-step-action.md) | 工作流、任务、步骤和 Action |
| 03 | [core-concepts/trigger-events.md](core-concepts/trigger-events.md) | 触发事件 |
| 04 | [core-concepts/runner-and-environment.md](core-concepts/runner-and-environment.md) | Runner 和运行环境 |
| 05 | [core-concepts/variables-secrets-context-expressions.md](core-concepts/variables-secrets-context-expressions.md) | 变量、密钥、上下文和表达式 ⚠️英文待勘误 |
| 06 | [core-concepts/artifacts-and-cache.md](core-concepts/artifacts-and-cache.md) | 制品与缓存 |
| **编写流水线** | | |
| 07 | [writing-pipelines/workflow-file-location-structure.md](writing-pipelines/workflow-file-location-structure.md) | 工作流文件位置与基本结构 |
| 08 | [writing-pipelines/configure-triggers.md](writing-pipelines/configure-triggers.md) | 配置触发条件 |
| 09 | [writing-pipelines/configure-jobs.md](writing-pipelines/configure-jobs.md) | 配置任务 Jobs |
| 10 | [writing-pipelines/configure-steps.md](writing-pipelines/configure-steps.md) | 配置步骤 Steps |
| 11 | [writing-pipelines/using-script-commands.md](writing-pipelines/using-script-commands.md) | 使用脚本命令 |
| 12 | [writing-pipelines/using-actions.md](writing-pipelines/using-actions.md) | 使用 Action 插件 |
| 13 | [writing-pipelines/configure-dependencies-order.md](writing-pipelines/configure-dependencies-order.md) | 配置任务依赖与执行顺序 |
| 14 | [writing-pipelines/configure-conditional-execution.md](writing-pipelines/configure-conditional-execution.md) | 配置条件执行 |
| 15 | [writing-pipelines/configure-matrix-builds.md](writing-pipelines/configure-matrix-builds.md) | 配置矩阵构建 |
| 16 | [writing-pipelines/using-variables-secrets.md](writing-pipelines/using-variables-secrets.md) | 使用变量和密钥 |
| 17 | [writing-pipelines/pass-output-between-jobs.md](writing-pipelines/pass-output-between-jobs.md) | 任务间传递输出参数 ⚠️摘要待勘误 |
| 18 | [writing-pipelines/upload-download-artifacts.md](writing-pipelines/upload-download-artifacts.md) | 上传和下载制品 |
| 19 | [writing-pipelines/using-dependency-cache.md](writing-pipelines/using-dependency-cache.md) | 使用依赖缓存 |
| **运行流水线** | | |
| 20 | [running-pipelines/view-run-results.md](running-pipelines/view-run-results.md) | 查看流水线运行结果 |
| 21 | [running-pipelines/view-job-logs.md](running-pipelines/view-job-logs.md) | 查看任务日志 |
| 22 | [running-pipelines/manually-trigger-pipeline.md](running-pipelines/manually-trigger-pipeline.md) | 手动触发流水线 |
| 23 | [running-pipelines/rerun-failed-jobs.md](running-pipelines/rerun-failed-jobs.md) | 重新运行失败任务 |
| **Runner 管理** | | |
| 24 | [runner-management/using-hosted-runners.md](runner-management/using-hosted-runners.md) | 使用 AtomGit 托管 Runner |
| 25 | [runner-management/using-self-hosted-runners.md](runner-management/using-self-hosted-runners.md) | 使用自托管 Runner |
| 26 | [runner-management/selecting-runner-labels.md](runner-management/selecting-runner-labels.md) | 选择 Runner 标签 |
| 27 | [runner-management/configuring-images-toolchains.md](runner-management/configuring-images-toolchains.md) | 配置运行镜像和工具链 |
| **安全与权限** | | |
| 28 | [security-permissions/using-secrets.md](security-permissions/using-secrets.md) | 使用 Secrets 管理敏感信息 |
| 29 | [security-permissions/token-permissions.md](security-permissions/token-permissions.md) | Token 权限与最小授权 |
| 30 | [security-permissions/pr-mr-pipeline-security.md](security-permissions/pr-mr-pipeline-security.md) | PR/MR 流水线安全 |
| **语法与配置参考** | | |
| 31 | [syntax-reference/trigger-events.md](syntax-reference/trigger-events.md) | 触发事件（参考） |
| 32 | [syntax-reference/context.md](syntax-reference/context.md) | 上下文 |
| 33 | [syntax-reference/expressions.md](syntax-reference/expressions.md) | 表达式 |
| 34 | [syntax-reference/variables.md](syntax-reference/variables.md) | 变量 |
| 35 | [syntax-reference/workflow-commands.md](syntax-reference/workflow-commands.md) | 工作流命令 |
| 36 | [syntax-reference/runner-images-tools.md](syntax-reference/runner-images-tools.md) | Runner 镜像与预装工具 |
| **示例教程** | | |
| 37 | [examples/nodejs-ci.md](examples/nodejs-ci.md) | Node.js 项目 CI |
| 38 | [examples/java-maven-ci.md](examples/java-maven-ci.md) | Java Maven 项目 CI |
| 39 | [examples/java-gradle-ci.md](examples/java-gradle-ci.md) | Java Gradle 项目 CI |
| 40 | [examples/go-ci.md](examples/go-ci.md) | Go 项目 CI |
| 41 | [examples/python-ci.md](examples/python-ci.md) | Python 项目 CI |
| 42 | [examples/pr-code-check-example.md](examples/pr-code-check-example.md) | PR 代码检查示例 |
| **Action 插件开发** | | |
| 43 | [action-development/plugin-project-structure.md](action-development/plugin-project-structure.md) | 插件项目结构 |
| 44 | [action-development/action-yml-metadata-syntax.md](action-development/action-yml-metadata-syntax.md) | action.yml 元数据语法 |
| 45 | [action-development/top-level-fields.md](action-development/top-level-fields.md) | 顶级字段 |
| 46 | [action-development/runtime-environment-variables.md](action-development/runtime-environment-variables.md) | 运行时环境变量 |
| 47 | [action-development/plugin-development-guide.md](action-development/plugin-development-guide.md) | 插件开发指南 |
| 48 | [action-development/plugin-security-specification.md](action-development/plugin-security-specification.md) | 插件安全规范 |
| 49 | [action-development/plugin-packaging.md](action-development/plugin-packaging.md) | 插件打包 |
| **Action 市场** | | |
| 50 | [actions-market.md](actions-market.md) | 官方 Action 市场插件目录（49 个插件，含 README） |

## 勘误清单（待优化项）

| 文件 | 问题 | 处理建议 |
|---|---|---|
| core-concepts/variables-secrets-context-expressions.md | WebFetch 返回英文（模型转译） | 重抓，要求保留中文原文；内容与语法参考页重叠，可参照 34 变量页 |
| writing-pipelines/pass-output-between-jobs.md | WebFetch 返回摘要（丢失部分代码块） | 重抓补全；核心示例已按运行时环境变量页补齐 |

> 官方目录里 workflow_dispatch 编号为 1.6、workflow_call 为 1.8（跳过 1.7），系官方页原样，非抓取遗漏。

## 与本 team 的衔接

- 本目录是 `phase01/inputs/gitcode-spec/`（**必需**输入）的实体内容，供 spec-analyst / compat-diff / security / reliability / usability / case-writer 消费。
- 兼容性差异线索见同目录 [COMPAT-NOTES.md](COMPAT-NOTES.md)（抓取过程中发现的 GitCode↔GitHub 差异速记，喂给 compat-diff agent）。
