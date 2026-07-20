<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/plugin-project-structure | fetched: 2026-07-20 -->

# 插件项目结构

## 概述

开发 AtomGit Actions 插件需要遵循特定的规范和最佳实践，涵盖插件元数据定义、代码开发、插件引用的完整流程。

## 适用对象

本文档面向 AtomGit Actions 类型插件的开发人员。

## 插件项目结构

AtomGit Actions 插件的标准目录结构如下：

```
action-repo/
├── dist/
│   └── index.js              # 插件核心代码（构建产物）
│   └── stop.js               # [可选] 插件停止后处理代码
├── action.yml                # 插件元数据文件
└── README.md                 # 插件说明文档
```

### 核心文件说明

| 目录/文件 | 说明 |
|---------|------|
| `action.yml` | 元数据文件，定义插件输入参数、输出结果、执行文件等核心配置 |
| `dist/` | 可执行代码所在目录，由构建工具生成 |
| `README.md` | 插件的详细介绍文档 |
| 其他 | JS/TS 项目开发源码，目录结构无强制规定 |
