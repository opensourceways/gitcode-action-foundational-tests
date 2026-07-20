<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/action-yml-metadata-syntax | fetched: 2026-07-20 -->

# action.yml 元数据语法

`action.yml` 是插件的核心配置文件，包含插件的元数据、输入输出、运行环境等信息。使用 `action.yml` 来识别和加载插件。

## 完整示例

```yaml
# action.yml 元数据语法
name: 'action-demo'
version: '1.0.0'
author: 'XXX'
description: '样例插件'
inputs:
  key_input:
    description: '单行输入测试'
    required: true
    default: test
outputs:
  record_id:
    description: "记录ID"
  report_url:
    description: "报告链接"
runs:
  using: 'node16'
  main: 'dist/main.js'
  post: 'dist/stop.js'
```

## 定义文件格式规范

| 规则 | 说明 |
|------|------|
| 格式 | **强制** YAML 格式 |
| 文件名 | **强制** 必须命名为 `action.yml`，大小写敏感 |

## 版本号规范

版本号采用语义化版本格式 `X.Y.Z`（如 `1.0.0`）：

| 版本段 | 含义 | 递增条件 | 示例 |
|--------|------|---------|------|
| X（主版本号） | 重大功能变更、不兼容的 API 变更 | 不兼容的重大变更 | `1.0.0` → `2.0.0` |
| Y（次版本号） | 向下兼容的新功能增加 | 向下兼容的新功能 | `1.0.0` → `1.1.0` |
| Z（修订号） | 向下兼容的问题修复 | 向下兼容的问题修复 | `1.0.0` → `1.0.1` |

> **注意**
>
> * 版本号只能新增，不能回退
> * 版本号中不允许包含字母或特殊字符，只使用数字和点分隔符
> * 预发布版本标识可使用：`1.0.0-alpha`、`1.0.0-beta`、`1.0.0-rc` 等
