# inputs/gitcode-spec/ （**必需**）— 已补充 ✅

GitCode Action（AtomGit Action）官方流水线文档的**离线镜像**，抓取自
https://docs.gitcode.com/docs/help/home/org_project/pipeline/ （2026-07-20，共 50 页）。

## 导航
- **[INDEX.md](INDEX.md)** — 全部 50 页索引 + 来源 URL + 勘误清单
- **[COMPAT-NOTES.md](COMPAT-NOTES.md)** — 抓取中发现的 GitCode↔GitHub 差异速记（喂 compat-diff agent）

## 结构（镜像官方目录）
```
00-overview.md / 01-quick-start.md
core-concepts/        (5)   核心概念
writing-pipelines/    (13)  编写流水线
running-pipelines/    (4)   运行流水线
runner-management/    (4)   Runner 管理
security-permissions/ (3)   安全与权限
syntax-reference/     (6)   语法与配置参考
examples/             (6)   示例教程
action-development/   (7)   Action 插件开发
```

## 消费方
spec-analyst · case-writer（编译 YAML 语法依据）· security（权限/隔离）· reliability（配额/runner）· usability（错误/文档）· compat-diff（对照 COMPAT-NOTES + github-reference）

## 持续勘误
- 每个文件头 `<!-- source | fetched -->` 记录来源与抓取日期。
- 文档更新后重抓对应页覆盖即可；两处已知待优化项见 INDEX.md 勘误清单。
- 抓取方式：WebFetch 逐页转 Markdown（要求保留中文原文与完整代码块/表格）。

**已补充 / 50 页 / 2026-07-20**
