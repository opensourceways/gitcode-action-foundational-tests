# GitCode Actions 插件目录

> 项目: `ComputingActionTest/foundational-tests` | 插件总数: 49

---

## 1. MaliciousCodePrScan

- **name**: `malicious-code-pr-scan`
- **creator**: wukong_admin
- **被引用**: 4
- **版本**: 1.0.0

# malicious-code-pr-scan-action

恶意代码 PR 扫描的 GitCode Action 插件，用于在 PR（Pull Request）场景下自动进行恶意代码扫描门禁检查。

## 项目结构

```
malicious-code-pr-scan-action/
├── action.yml                              # Action 定义（输入/输出/运行方式）
├── dist/
│   ├── malicious-code-pr-scan.js           # 扫描主逻辑
│   └── signer.js                           # API 网关签名工具
└── README.md
```

## 工作原理

1. **创建扫描任务** — 调用后端恶意代码扫描服务 API 提交扫描请求
2. **轮询扫描结果** — 每 10 秒查询一次任务状态，最长等待 30 分钟
3. **门禁判定** — 扫描通过则 exit(0)，不通过则 exit(-1) 阻断 PR

## Action 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `scan-access-key` | 扫描服务访问密钥 (AK) | 是 | — |
| `scan-secret-key` | 扫描服务密钥 (SK) | 是 | — |
| `result-access-key` | 查询服务访问密钥 (AK) | 是 | — |
| `result-secret-key` | 查询服务密钥 (SK) | 是 | — |
| `pr-id` | PR 编号 | 是 | — |
| `repository-name` | 仓库名称（如 `owner/repo`） | 是 | — |
| `codecheck-ip` | 代码检查服务地址 | 否 | `https://apig.openlibing.com` |
| `codecheck-prefix` | 服务 API 路径前缀 | 否 | `/openlibing-anti-poison` |
| `gitcode-domain` | GitCode 域名（用于拼接 PR URL） | 否 | `https://gitcode.com` |
| `project-name` | 项目名称（用于扫描任务） | 否 | `openLiBing` |
| `rule` | 任务规则列表（字符串） | 否 | `""` |

### rule 参数格式

`rule` 为字符串，格式为 `语言:规则1,规则2;语言2`，各语言之间用分号分隔：

```
Java:java_scan/download_exec.yar,java_scan/info_leak.yar;Python
```

- 语言后跟冒号，规则 ID 之间用逗号分隔
- 仅指定语言不指定规则（如 `Java;Python`）表示启用该语言全部规则
- 空字符串表示使用默认规则

## 使用方式

### 方式一：手动触发（workflow_dispatch）

在仓库的 `.gitcode/workflows/` 目录下创建工作流文件，通过手动输入 PR 编号和仓库名称触发扫描：

```yaml
name: malicious-code-pr-scan

on:
  workflow_dispatch:
    inputs:
      pr-id:
        description: 'PR编号'
        required: true
      repository-name:
        description: '仓库名称'
        required: true
      gitcode-domain:
        description: 'gitcode域名'
        required: false
      project-name:
        description: '项目名称'
        required: false
      rule:
        description: '扫描规则'
        required: false
        default: "Java:java_scan/download_exec.yar,java_scan/info_leak.yar;Python"

jobs:
  sca-pr-scan:
    runs-on: ubuntu-latest
    name: Malicious Code PR Scan
    steps:
      - name: Checkout
        uses: checkout

      - name: Run Malicious Code PR Scan
        id: malicious-code-pr-scan
        uses: malicious-code-pr-scan
        with:
          scan-access-key: ${{ secrets.MALICIOUS_PR_SCAN_ACCESS_KEY }}
          scan-secret-key: ${{ secrets.MALICIOUS_PR_SCAN_SECRET_KEY }}
          result-access-key: ${{ secrets.MALICIOUS_PR_RESULT_ACCESS_KEY }}
          result-secret-key: ${{ secrets.MALICIOUS_PR_RESULT_SECRET_KEY }}
          pr-id: ${{ inputs.pr-id }}
          repository-name: ${{ inputs.repository-name }}
          gitcode-domain: ${{ inputs.gitcode-domain }}
          project-name: ${{ inputs.project-name }}
          rule: ${{ inputs.rule }}
```

### 方式二：PR 事件自动触发

在仓库的 `.gitcode/workflows/` 目录下创建工作流文件，PR 打开/重新打开/更新时自动触发扫描：

```yaml
name: malicious-code-pr-scan

on:
  pull_request_target:
    branches: 
      - '*'
  pull_request_comment:
    types: [created]
    comment: ['malicious-code-pr-scan']
    branches: 
      - '*'

jobs:
  sca-pr-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: checkout

      - name: Run Malicious Code PR Scan
        id: malicious-code-pr-scan
        uses: malicious-code-pr-scan
        with:
          scan-access-key: ${{ secrets.MALICIOUS_PR_SCAN_ACCESS_KEY }}
          scan-secret-key: ${{ secrets.MALICIOUS_PR_SCAN_SECRET_KEY }}
          result-access-key: ${{ secrets.MALICIOUS_PR_RESULT_ACCESS_KEY }}
          result-secret-key: ${{ secrets.MALICIOUS_PR_RESULT_SECRET_KEY }}
          pr-id: ${{ atomgit.event.pull_request.number }}
          repository-name: ${{ atomgit.repository }}
          gitcode-domain: ${{ atomgit.api_url }}
          project-name: "openLiBing"
          rule: "Java:java_scan/download_exec.yar,java_scan/info_leak.yar;Python"
```

## 密钥配置

需要在仓库的 Secrets 中配置以下密钥：

| Secret 名称 | 说明 |
|-------------|------|
| `MALICIOUS_PR_SCAN_ACCESS_KEY` | 恶意代码扫描服务 AK |
| `MALICIOUS_PR_SCAN_SECRET_KEY` | 恶意代码扫描服务 SK |
| `MALICIOUS_PR_RESULT_ACCESS_KEY` | 查询结果服务 AK |
| `MALICIOUS_PR_RESULT_SECRET_KEY` | 查询结果服务 SK |

## 退出码

| 退出码 | 含义 |
|--------|------|
| 0 | 扫描通过，未发现恶意代码 |
| -1 | 扫描发现恶意代码 / 任务创建失败 / 查询超时 / 运行时错误 |

## 构建

项目使用 `@vercel/ncc` 打包 Action 代码，`adm-zip` 生成可分发的 zip 包：

```bash
# 仅打包 Action 代码
npm run package

# 打包并生成 zip
npm run build
```

构建产物为 `malicious-code-pr-scan-action.zip`，包含 Action 定义、扫描主逻辑和签名工具。

---

## 2. OpenlibingCodeMetricsAction

- **name**: `openlibing-code-metrics-action`
- **creator**: wukong_admin
- **被引用**: 15
- **版本**: 1.0.3

# openlibing-code-metrics-action

代码度量扫描插件 - 检测代码规模、平均函数代码行数、平均圈复杂度、代码重复率和文件重复率。

## 功能

| 指标 | 说明 | 工具 |
|------|------|------|
| 代码规模 | 有效代码行数 | scc |
| 平均函数代码行数 | 函数体有效代码行的算术平均值 | lizard |
| 平均圈复杂度 | 函数级圈复杂度的算术平均值 | lizard |
| 代码重复率 | 跨文件重复代码行占有效代码行的百分比 | jscpd |
| 文件重复率 | 内容完全一致文件占总文件数的百分比 | MD5哈希比对 |

## 使用方式

```yaml
jobs:
  code-metrics-scan:
    name: 代码度量检测
    runs-on: ["codearts-hosted", "ubuntu-latest", "x64", "large"]
    steps:
      - name: Checkout
        uses: checkout

      - name: code-metrics-scan
        uses: openlibing-code-metrics-action
        env:
          CODEMETRICS_APIG_BASE_URL: ${{ secrets.CODEMETRICS_APIG_BASE_URL }}
          CODEMETRICS_APIG_APP_KEY: ${{ secrets.CODEMETRICS_APIG_APP_KEY }}
          CODEMETRICS_APIG_APP_SECRET: ${{ secrets.CODEMETRICS_APIG_APP_SECRET }}
```

## 输入参数

| 参数 | 必填 | 默认值         | 说明                                  |
|------|------|-------------|-------------------------------------|
| source-dir | 否 | `./`        | 源代码目录路径，当扫描指定代码仓时必填checkout指定仓的path |
| repository | 否 | -           | 流水线所属仓库的 owner/repo，用于上报，默认自动获取     |
| config-file | 否 | -           | 配置文件路径（.metrics.yml）                |
| exclude-dirs | 否 | -           | 排除目录列表，逗号分隔，不填时默认扫描全部路径             |
| allowed-extensions | 否 | -           | 允许的文件扩展名，逗号分隔，不填时默认扫描所有文件类型         |
| output | 否 | metrics.json | 结果输出文件路径                            |
| upload | 否 | true        | 是否上传检测结果到 coderepo 服务               |

## 环境变量

上传功能需要以下环境变量：

| 变量 | 必填 | 说明                                        |
|------|------|-------------------------------------------|
| CODEMETRICS_APIG_BASE_URL | 是 | coderepo 服务地址（APIG 网关 baseUrl，https://apig.openlibing.com:443)           |
| CODEMETRICS_APIG_APP_KEY | 是 | APIG 网关 AppKey（即 AK，用于 HMAC-SHA256 签名）    |
| CODEMETRICS_APIG_APP_SECRET | 是 | APIG 网关 AppSecret（即 SK，用于 HMAC-SHA256 签名） |

## 输出

| 输出 | 说明 |
|------|------|
| code-scale | 代码规模（有效代码行数） |
| avg-function-loc | 平均函数代码行数 |
| avg-cyclomatic-complexity | 平均圈复杂度 |
| total-code-duplication-rate | 代码重复率（%） |
| total-file-duplication-rate | 文件重复率（%） |

## 依赖

- **scc** - 代码行数统计（内置二进制包 bin/scc）
- **lizard** - 函数复杂度分析（Python 包，需 pip install）
- **jscpd** - 代码重复检测（npm 依赖）


---

## 3. OpenlibingSecurityCompilationOptionsAction

- **name**: `openlibing-security-compilation-options-action`
- **creator**: wukong_admin
- **被引用**: 65
- **版本**: 1.0.3

# openlibing-security-compilation-options-action

安全编译选项扫描插件 - 检测 ELF 文件安全编译选项开启率。

## 功能

检测构建产物（ELF 二进制文件）的 8 项安全编译选项：

| 选项 | 说明 |
|------|------|
| BIND_NOW | 立即绑定（全 RELRO） |
| NX | 堆栈不可执行 |
| PIC | 地址无关代码 |
| PIE | 位置无关可执行文件 |
| RELRO | GOT 表保护 |
| Run-time Search Path | 动态库搜索路径（YES 表示存在不安全搜索路径） |
| SP / Stack Protector | 栈保护 |
| Strip | 符号表剥离 |

自动解压 `.whl`/`.zip`/`.tar.gz`/`.jar` 等包格式，跳过 `.debug`/`.dbg` 调试符号文件。

## 使用方式

```yaml
name: openlibing-security-compilation-options-action

on:
  workflow_dispatch:
  push:
    branches: [ "master" ]

jobs:
  security-compilation-options-action:
    name: 安全编译选项开启率扫描
    runs-on: ["codearts-hosted", "ubuntu-latest", "x64", "large"]
    steps:
      - name: Checkout current repository
        uses: checkout

      - name: setup-jdk
        uses: setup-jdk
        with:
          jdk-version: '21'
          maven-version: '3.9.15'

      - name: build
        run: |
          echo "===== Maven 构建打包 ====="
          mvn -gs .mvn/settings.xml -B clean package -DskipTests \
            -Dopenlibing_mvn_repo_username="$OPENLIBING_MVN_REPO_USERNAME" \
            -Dopenlibing_mvn_repo_password="$OPENLIBING_MVN_REPO_PASSWORD"
        env:
          OPENLIBING_MVN_REPO_USERNAME: ${{ secrets.OPENLIBING_MVN_REPO_USERNAME }}
          OPENLIBING_MVN_REPO_PASSWORD: ${{ secrets.OPENLIBING_MVN_REPO_PASSWORD }}

      - name: security-compilation-options-action
        uses: openlibing-security-compilation-options-action
        env:
          SEC_OPTION_APIG_APP_KEY: ${{ secrets.OPENLIBING_APIG_KEY }}
          SEC_OPTION_APIG_APP_SECRET: ${{ secrets.OPENLIBING_APIG_SECRET }}
```

## 输入参数

| 参数 | 必填 | 默认值                    | 说明                                                                                                               |
|------|------|------------------------|------------------------------------------------------------------------------------------------------------------|
| source-dir | 否 | target                 | 构建产物目录路径                                                                                                         |
| repository | 否 | -                      | 流水线所属仓库的 owner/repo，用于上报，不传时自动获取                           |
| output | 否 | sec-option-result.json | 结果输出文件路径                                                                                                         |
| upload | 否 | true                   | 是否上传检测结果到 cicd 服务                                                                                                |

## 环境变量

上传功能需要以下环境变量（通过 APIG 网关调用 cicd 接口）：

| 变量 | 说明 |
|------|------|
| SEC_OPTION_APIG_APP_KEY | APIG 网关 AppKey（AK，用于 SDK-HMAC-SHA256 签名） |
| SEC_OPTION_APIG_APP_SECRET | APIG 网关 AppSecret（SK，用于 SDK-HMAC-SHA256 签名） |

## 输出

每个安全编译选项开启率选项输出 3 个值：

| 输出 | 说明 |
|------|------|
| {option}-total-files | 参与计算的文件数（排除 N/A） |
| {option}-yes-count | 满足数 |
| {option}-rate | 开启率（%） |

扫描的安全编译选项包括：bindNow, nx, pic, pie, relro, rpath, sp, strip

## 依赖

- **pyelftools** - ELF 文件解析（Python 包，需 pip install）


---

## 4. swr

- **name**: `swr`
- **creator**: wukong_admin
- **被引用**: 0
- **版本**: 1.0.0

# swr目录说明

本插件主要用于支持基于华为云容器镜像仓库(SWR)的镜像制作/上传/下载能力

> **注意**：使用此插件无法使用默认资源池，需资源池中安装docker工具

## 通用参数说明

| 参数名 | 必填 | 说明                                                                                                                   |
|--------|------|----------------------------------------------------------------------------------------------------------------------|
| action | 是 | 操作类型：支持单个或多个配置，可选 `build`、`push`、`pull`。插件行为顺序固定，若都勾选，会按照 build、push、pull 的顺序执行                                      |
| auth-user | 是 | 用户身份信息配置，支持 `current` 或 `other`<br/>- `current`：使用当前流水线执行用户身份访问SWR仓库<br/>- `other`：可指定用户身份，需配置 ak、sk 参数，建议通过私密参数进行引用 |
| region | 是 | SWR局点信息，如北京四：`cn-north-4`                                                                                            |
| organization | 是 | SWR有效组织名称，需注意账号访问权限                                                                                                  |
| ak | 否 | IAM用户 accesskey，当 auth-user 为 `other` 时必填，建议使用私密参数引用                                                                 |
| sk | 否 | IAM用户 secretkey，当 auth-user 为 `other` 时必填，建议使用私密参数引用                                                                 |

---

## 一、构建镜像 (build)

### 使用场景
制作Docker镜像并推送到SWR仓库

### 参数说明

| 参数名 | 必填 | 说明                                                                                                               |
|--------|------|------------------------------------------------------------------------------------------------------------------|
| docker-context | 是 | 镜像制作上下文，相对于当前系统参数 workspace 的路径                                                                                  |
| dockerfile | 是 | Dockerfile文件所在路径，相对于当前系统参数 workspace 的路径                                                                         |
| use-cache | 否 | 镜像制作是否使用缓存<br/>- `yes`：使用缓存<br/>- `no`：不使用缓存，镜像制作时会添加 `--no-cache`                                               |
| set-metadata | 否 | 镜像制作是否添加构建元数据<br/>- `yes`：添加构建元信息<br/>- `no`：不添加<br/><br/>构建元信息包括：流水线任务名称、流水线任务地址、流水线序号、流水线触发人、代码库、代码分支、commitId |
| build-args | 否 | 镜像制作时使用的参数，支持两种格式：<br/>**1、多行格式**<br/>**2、JSON字符串格式**：<br/>```[{"key":"ENV","value":"PROD"}]```             |
| image-name | 是 | 镜像名称，如 `swr.cn-north-7.myhuaweicloud.com/xxx/test0316:2026031602` 中的 `test0316`                                  |
| image-tag | 是 | 镜像标签，如 `swr.cn-north-7.myhuaweicloud.com/xxx/test0316:2026031602` 中的 `2026031602`                                |

### 配置示例

```yaml
- name: swr
  uses: swr
  with:
    action: "build"
    auth-user: current
    region: cn-north-4
    organization: "my-org"
    docker-context: .
    dockerfile: ./Dockerfile
    use-cache: yes
    set-metadata: yes
    build-args: |
      VERSION=1.0.0
      ENV=prod
    image-name: "my-app"
    image-tag: "v1.0.0"
```

---

## 二、推送镜像 (push)

### 使用场景
将本地镜像推送到SWR仓库

### 参数说明

| 参数名 | 必填 | 说明 |
|--------|------|------|
| image-name | 是 | 镜像名称 |
| image-tag | 是 | 镜像标签 |

### 配置示例

```yaml
- name: swr
  uses: swr
  with:
    action: "push"
    auth-user: current
    region: cn-north-4
    organization: "my-org"
    image-name: "my-app"
    image-tag: "v1.0.0"
```

---

## 三、拉取镜像 (pull)

### 使用场景
从SWR仓库拉取镜像到本地

### 参数说明

| 参数名 | 必填 | 说明 |
|--------|------|------|
| image-name | 是 | 镜像名称 |
| image-tag | 是 | 镜像标签 |

### 配置示例

```yaml
- name: swr
  uses: swr
  with:
    action: "pull"
    auth-user: current
    region: cn-north-4
    organization: "my-org"
    image-name: "my-app"
    image-tag: "v1.0.0"
```

---

## 四、组合操作示例

### 构建并推送镜像

```yaml
- name: swr
  uses: swr
  with:
    action: "build,push"
    auth-user: current
    region: cn-north-4
    organization: "my-org"
    docker-context: .
    dockerfile: ./Dockerfile
    use-cache: yes
    set-metadata: yes
    image-name: "my-app"
    image-tag: "v1.0.0"
```

### 使用其他用户身份推送镜像

```yaml
- name: swr
  uses: swr
  with:
    action: "push"
    auth-user: other
    region: cn-north-4
    organization: "my-org"
    image-name: "my-app"
    image-tag: "v1.0.0"
    ak: "ak"
    sk: "sk"
```

### 完整流程：构建、推送、拉取

```yaml
- name: swr
  uses: swr
  with:
    action: "build,push,pull"
    auth-user: current
    region: cn-north-4
    organization: "my-org"
    docker-context: .
    dockerfile: ./Dockerfile
    use-cache: yes
    set-metadata: yes
    image-name: "my-app"
    image-tag: "v1.0.0"
```

---

## 5. PathsChangesFilter

- **name**: `paths-changes-filter`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.0.9

# Paths Changes Filter

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js Version](https://img.shields.io/badge/Node.js-%3E%3D%2024-brightgreen)](https://nodejs.org/)

**Paths Changes Filter** 是一个 GitHub Action（现已适配 GitCode 平台），用于根据文件变更路径实现工作流步骤和作业的条件执行。通过检测 Pull Request、分支推送或最近提交中修改的文件，智能触发相应的 CI/CD 流程。

该插件特别适用于 Monorepo 项目和大型代码仓库，可以显著节省 CI/CD 资源消耗，避免对未变更组件进行不必要的构建和测试。

---

## 目录

- [核心功能](#核心功能)
- [技术架构](#技术架构)
- [安装指南](#安装指南)
- [快速开始](#快速开始)
- [配置说明](#配置说明)
- [输入输出参数](#输入输出参数)
- [使用示例](#使用示例)
- [高级用法](#高级用法)
- [常见问题](#常见问题)
- [贡献指南](#贡献指南)
- [许可证](#许可证)

---

## 核心功能

### 1. 多场景变更检测

| 场景 | 触发方式 | 检测策略 |
|------|----------|----------|
| **Pull Request** | `pull_request` / `pull_request_target` | 相对于 PR 基础分支检测变更 |
| **功能分支** | `push` 或其他事件 | 基于 merge-base 与配置的基础分支比较 |
| **合并队列** | `merge_group` | 使用事件中的 base 和 head commit SHA |
| **长生命周期分支** | `push` 事件 | 相对于推送前最近一次提交检测 |
| **本地变更** | 任意事件 + `base: HEAD` | 检测当前 HEAD 的已暂存和未提交变更 |

### 2. 灵活的过滤规则

- 支持 glob 模式匹配（基于 [picomatch](https://github.com/micromatch/picomatch) 库）
- 支持按文件变更状态过滤：`added`、`modified`、`deleted`、`renamed`
- 支持 YAML 锚点复用和规则组合
- 支持排除模式（以 `!` 开头）
- 支持谓词量词配置：`some`（默认，至少一个匹配）或 `every`（全部匹配）

### 3. 丰富的输出格式

- `none`：禁用文件列表输出
- `csv`：逗号分隔的文件名列表
- `json`：JSON 数组格式
- `shell`：适用于 Linux shell 的空格分隔列表
- `escape`：使用反斜杠转义的空格分隔列表

---

## 技术架构

### 模块结构

```
paths-filter/
├── src/
│   ├── main.ts              # 主入口，参数解析和流程编排
│   ├── filter.ts            # YAML 配置解析与路径模式匹配
│   ├── git.ts               # Git 命令执行与变更检测
│   ├── file.ts              # 文件类型定义与状态枚举
│   └── list-format/
│       ├── csv-escape.ts    # CSV 格式转义
│       └── shell-escape.ts  # Shell 参数转义
├── action.yml               # GitCode Action 元数据
└── dist/
    └── index.js             # 打包后的执行文件
```

### 核心组件

| 组件 | 职责 |
|------|------|
| **Filter** | 解析 YAML 过滤规则，执行路径模式匹配 |
| **Git 模块** | 执行 git diff、merge-base 等命令获取变更 |
| **API 客户端** | 通过 REST API 获取 PR 变更文件列表 |
| **输出格式化** | 将匹配结果序列化为指定格式 |

### 依赖技术

- **Node.js**: >= 24
- **@actions/core**: GitHub Actions 核心库
- **@actions/exec**: Git 命令执行
- **@octokit/rest**: REST API 客户端
- **picomatch**: glob 模式匹配
- **js-yaml**: YAML 配置解析

---

## 安装指南

### 前置要求

- Node.js >= 24
- Git
- 支持 GitCode Pipeline 或 GitHub Actions 的代码仓库

### 构建步骤

```bash
# 克隆仓库
git clone https://gitcode.com/your-namespace/paths-filter.git
cd paths-filter

# 安装依赖
npm install

# 构建项目
npm run build

# 打包 Action
npm run pack
```

### 在项目中使用

#### 方式一：直接引用构建产物

```yaml
- uses: ./path/to/paths-filter
  id: changes
  with:
    filters: |
      src:
        - 'src/**'
```

#### 方式二：发布到市场

将构建产物发布到 GitCode 市场或其他可访问位置，然后使用完整路径引用。

---

## 快速开始

### 最简示例

```yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  detect-changes:
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1

      - uses: ./
        id: changes
        with:
          filters: |
            src:
              - 'src/**'
            docs:
              - 'docs/**'

  build:
    needs: detect-changes
    if: ${{ needs.detect-changes.outputs.src == 'true' }}
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1
      - run: npm run build
```

### 条件步骤执行

```yaml
- uses: ./
  id: changes
  with:
    filters: |
      backend:
        - 'backend/**'
      frontend:
        - 'frontend/**'

- name: 后端测试
  if: ${{ steps.changes.outputs.backend == 'true' }}
  run: npm run test:backend

- name: 前端测试
  if: ${{ steps.changes.outputs.frontend == 'true' }}
  run: npm run test:frontend
```

---

## 配置说明

### 过滤规则语法

#### 基本语法

```yaml
filter_name:
  - 'path/pattern/**'
  - 'another/pattern/*.js'
```

#### 带状态过滤

```yaml
filter_name:
  - added|modified: 'src/**'    # 仅匹配新增或修改的文件
  - deleted: 'docs/**'          # 仅匹配删除的文件
```

#### 排除模式

```yaml
backend:
  - 'pkg/**'
  - '!**/*.md'                  # 排除所有 markdown 文件
  - '!**/*.jpeg'                # 排除所有 jpeg 文件
```

#### YAML 锚点复用

```yaml
shared: &shared
  - common/**
  - config/**

src:
  - *shared                     # 引用 shared 中的规则
  - src/**

tests:
  - *shared
  - tests/**
```

### 谓词量词

默认情况下，文件只需匹配任意一个模式即可被包含。可以通过 `predicate-quantifier` 参数修改此行为：

```yaml
- uses: ./
  with:
    predicate-quantifier: every  # 所有模式都必须匹配
    filters: |
      backend:
        - 'pkg/a/b/c/**'
        - '!**/*.md'              # 必须不是 md 文件
        - '!**/*.jpeg'            # 必须不是 jpeg 文件
```

---

## 输入输出参数

### 输入参数

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| `filters` | string | 是 | - | 过滤规则配置（YAML 字符串或文件路径） |
| `token` | string | 否 | `${{ gitcode.token }}` | 访问令牌，用于调用 API |
| `base` | string | 否 | 默认分支 | 比较基准分支、标签或 commit SHA |
| `ref` | string | 否 | `${{ gitcode.ref }}` | 要检测变更的 Git 引用 |
| `sha` | string | 否 | `${{ gitcode.sha }}` | 事件相关的 commit SHA |
| `repo` | string | 否 | `${{ gitcode.action_repository }}` | 仓库标识 |
| `event-name` | string | 否 | `${{ gitcode.event_name }}` | 触发事件名称 |
| `working-directory` | string | 否 | - | 工作目录路径 |
| `list-files` | string | 否 | `none` | 匹配文件列表输出格式 |
| `initial-fetch-depth` | number | 否 | `100` | 初始 fetch 深度 |
| `predicate-quantifier` | string | 否 | `some` | 谓词量词：`some` 或 `every` |

### 输出参数

| 输出 | 类型 | 说明 |
|------|------|------|
| `${FILTER_NAME}` | boolean | 该过滤器是否有文件匹配 |
| `${FILTER_NAME}_count` | number | 匹配文件的数量 |
| `${FILTER_NAME}_files` | string | 匹配文件的列表（格式取决于 `list-files`） |
| `changes` | string | 所有匹配的过滤器名称（JSON 数组） |

---

## 使用示例

### 示例一：Monorepo 项目的条件测试

```yaml
name: Monorepo CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  detect-changes:
    runs-on: euleros-2.10.1
    outputs:
      packages: ${{ steps.filter.outputs.changes }}
    steps:
      - uses: checkout-action@0.0.1

      - uses: ./
        id: filter
        with:
          filters: |
            pkg1: packages/pkg1/**
            pkg2: packages/pkg2/**
            pkg3: packages/pkg3/**

  test:
    needs: detect-changes
    strategy:
      matrix:
        package: ${{ fromJSON(needs.detect-changes.outputs.packages) }}
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1
      - run: npm test --workspace=${{ matrix.package }}
```

### 示例二：基于变更类型执行不同任务

```yaml
- uses: ./
  id: changes
  with:
    filters: |
      added:
        - added: '**'
      modified:
        - modified: '**'
      deleted:
        - deleted: '**'

- name: 处理新增文件
  if: ${{ steps.changes.outputs.added == 'true' }}
  run: echo "New files: ${{ steps.changes.outputs.added_files }}"

- name: 处理修改文件
  if: ${{ steps.changes.outputs.modified == 'true' }}
  run: echo "Modified files: ${{ steps.changes.outputs.modified_files }}"
```

### 示例三：使用 JSON 格式传递文件列表

```yaml
- uses: ./
  id: changes
  with:
    list-files: json
    filters: |
      docs:
        - '**.md'

- name: 检查文档
  if: ${{ steps.changes.outputs.docs == 'true' }}
  run: |
    echo "Changed documentation files:"
    echo '${{ steps.changes.outputs.docs_files }}' | jq -r '.[]' | xargs textlint
```

### 示例四：功能分支变更检测

```yaml
on:
  push:
    branches:
      - feature/**

jobs:
  build:
    runs-on: euleros-2.10.1
    steps:
      - uses: checkout-action@0.0.1
        with:
          fetch-depth: 20

      - uses: ./
        id: filter
        with:
          base: main  # 与 main 分支比较
          filters: |
            src:
              - 'src/**'
```

### 示例五：检测首次推送

```yaml
- uses: ./
  id: changes
  with:
    filters: |
      all: '**'

- name: 首次推送处理
  if: ${{ steps.changes.outputs.all == 'true' }}
  run: |
    echo "This is the first push of the branch"
    echo "All tracked files will be listed as added"
```

---

## 高级用法

### 自定义文件列表输出格式

#### CSV 格式

```yaml
- uses: ./
  id: changes
  with:
    list-files: csv
    filters: |
      src: 'src/**'

- name: 显示变更
  run: echo "Changed files: ${{ steps.changes.outputs.src_files }}"
# 输出示例: "file1.txt","path/to/file2.txt"
```

#### Shell 格式

```yaml
- uses: ./
  id: changes
  with:
    list-files: shell
    filters: |
      src: 'src/**'

- name: Lint 检查
  if: ${{ steps.changes.outputs.src == 'true' }}
  run: npx eslint ${{ steps.changes.outputs.src_files }}
# 输出示例: 'src/file1.ts' 'src/file2.ts'
```

#### Escape 格式

```yaml
- uses: ./
  id: changes
  with:
    list-files: escape
    filters: |
      src: 'src/**'

- name: 处理特殊字符文件名
  run: |
    for file in ${{ steps.changes.outputs.src_files }}; do
      echo "Processing: $file"
    done
```

### 使用外部配置文件

将过滤规则定义在单独的文件中：

```yaml
# .gitcode/filters.yaml
src:
  - src/**
  - '!**/*.test.ts'

lib:
  - lib/**
  - '!lib/**/*.d.ts'
```

引用方式：

```yaml
- uses: ./
  with:
    filters: .gitcode/filters.yaml
```

### 深度 Fetch 配置

对于历史较长的分支，可能需要增加 fetch 深度：

```yaml
- uses: ./
  with:
    initial-fetch-depth: 500
    filters: |
      src: 'src/**'
```

---

## 常见问题

### Q: 如何处理重命名文件？

重命名的文件会被分解为两个操作：删除原文件 + 添加新文件。这是 git diff 的默认行为，确保变更检测的准确性。

### Q: 为什么第一次运行没有检测到变更？

可能的原因：
1. 分支是首次推送，没有 merge-base
2. fetch-depth 太小，未能获取足够的历史
3. 基础分支名称配置不正确

解决方案：增加 `initial-fetch-depth` 值，或确保完整获取分支历史。

### Q: 如何在非 PR 事件中使用？

使用 `base` 和 `ref` 参数手动指定比较基准：

```yaml
- uses: ./
  with:
    base: develop
    ref: feature/my-branch
    filters: |
      src: 'src/**'
```

### Q: 支持哪些文件状态？

支持以下文件状态：
- `added`：新增文件
- `modified`：修改文件
- `deleted`：删除文件
- `renamed`：重命名文件
- `copied`：复制文件
- `unmerged`：合并冲突文件

### Q: 如何调试变更检测？

启用详细日志：

```yaml
- uses: ./
  id: changes
  with:
    filters: |
      src: 'src/**'
```

查看 GitCode Pipeline 的日志输出，可以观察到详细的变更检测过程。

---

## 贡献指南

欢迎提交 Issue 和 Pull Request！

### 开发环境搭建

```bash
# 克隆仓库
git clone https://gitcode.com/your-namespace/paths-filter.git
cd paths-filter

# 安装依赖
npm install

# 运行测试
npm test

# 构建
npm run build

# 代码格式化
npm run format

# 代码检查
npm run lint

# 完整构建（包含以上所有步骤）
npm run all
```

### 代码规范

- 遵循 TypeScript 最佳实践
- 使用 Prettier 进行代码格式化
- 遵循 ESLint 规则
- 所有新功能需要添加测试用例
- 确保所有测试通过

### 测试覆盖

项目使用 Jest 进行测试，覆盖以下模块：

| 测试文件 | 覆盖内容 |
|----------|----------|
| `filter.test.ts` | 过滤规则解析与匹配 |
| `git.test.ts` | Git 命令执行与变更检测 |
| `csv-escape.test.ts` | CSV 格式化 |
| `shell-escape.test.ts` | Shell 参数转义 |

---

## 许可证

本项目基于 [MIT 许可证](https://opensource.org/licenses/MIT)开源。

---

## 更新日志

### v1.0.0

- 完成 GitCode 平台适配
- 支持多场景变更检测
- 支持多种输出格式
- 支持谓词量词配置
- 完整的测试覆盖


---

## 6. Cache

- **name**: `cache`
- **creator**: wukong_admin
- **被引用**: 272
- **版本**: 1.0.8

# Cache

流水线缓存插件，用法参考了 [actions/cache@v5](https://github.com/actions/cache)：在 Job 开始时按 `key` **恢复**缓存，Job 成功结束后再把 `path` **保存**上去，加速依赖安装与构建产物复用。

## 快速开始

同一 Job 内最常见写法：先恢复，再跑业务，Job 成功后自动保存。

```yaml
- name: 恢复 / 保存依赖缓存
  id: cache
  identifier: cache   # 后续用 steps.cache.outputs.xxx 时需要
  uses: cache
  with:
    path: |
      node_modules
      ~/.npm
    key: node-${{ atomgit.pipeline_run_id }}-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      node-
```

之后可用 `${{ steps.cache.outputs.cache-hit }}` 判断是否精确命中主 `key`。

## 跨 Job：先保存，再恢复

不同 Job 默认是干净环境。用**相同的 `key` + `path`**，Job A 保存后，Job B（`needs` 依赖 A）再恢复即可。

Job A — 写入并保存：

```yaml
- name: 保存缓存
  uses: cache
  with:
    key: cache-e2e-${{ atomgit.pipeline_run_id }}
    path: |
      /tmp/cache-test/node_modules
      /tmp/cache-test/.env
```

Job B — 恢复（可先覆盖本地再拉缓存）：

```yaml
- name: 恢复缓存
  id: cache
  identifier: cache
  uses: cache
  with:
    key: cache-e2e-${{ atomgit.pipeline_run_id }}
    path: |
      /tmp/cache-test/node_modules
      /tmp/cache-test/.env
    fail-on-cache-miss: 'true'

- run: echo "cache-hit=${{ steps.cache.outputs.cache-hit }}"
```

要点：主入口在步骤开始时 restore，Job **成功结束**后自动 save；跨 Job 必须 key/path 一致；读 `cache-hit` 时设置 `id` / `identifier`。

## 输入参数

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `path` | 是 | - | 要缓存的文件/目录，支持多行 |
| `key` | 是 | - | 缓存主键；精确匹配时 `cache-hit` 为 `true` |
| `restore-keys` | 否 | - | 主 key 未命中时的前缀回退列表；此时 `cache-hit` 为 `false` |
| `enableCrossOsArchive` | 否 | `false` | 是否允许跨 OS 读写同一份缓存 |
| `fail-on-cache-miss` | 否 | `false` | 未找到任何缓存时是否让步骤失败 |
| `lookup-only` | 否 | `false` | 只检查是否存在，不下载；Job 成功后的 post save 仍可能执行 |

## 输出

| 输出 | 说明 |
|------|------|
| `cache-hit` | 主 `key` **精确命中**为 `true`；仅 `restore-keys` 命中或未命中为 `false` |

读取示例：

```yaml
- name: 查看是否命中
  run: echo "cache-hit=${{ steps.cache.outputs.cache-hit }}"
```

> `cache-hit` 只在 **restore（main）** 阶段写出；Job 结束时的自动 save（post）不会改这个输出。

## 使用建议

- **key 要可区分**：按依赖锁文件、语言版本、流水线运行等组合，例如 `node-${{ hashFiles('**/package-lock.json') }}`，或按次运行隔离：`cache-e2e-${{ atomgit.pipeline_run_id }}`。
- **path 写全**：多路径用多行列表；restore 时会按同样 path 解压覆盖本地文件。
- **跨 Job 依赖**：恢复侧 Job 用 `needs` 等待保存侧完成，避免还没上传就去拉。
- **强制命中**：E2E 或「必须有缓存」场景可设 `fail-on-cache-miss: 'true'`。
- **上下文**：YAML 里用 `${{ atomgit.* }}`（缓存 key 推荐 `atomgit.pipeline_run_id`）由 Runner 解析；插件内部会兼容 `ATOMGIT_*` / `GITHUB_*` 环境变量，一般无需在 workflow 里手动映射。

## License

MIT


---

## 7. AssociatePrComment

- **name**: `associate-pr-comment`
- **creator**: wukong_admin
- **被引用**: 78
- **版本**: 1.0.4

# Associate Workflow to PR Commit

创建虚拟工作流运行记录，将其关联到指定的 PR Commit SHA。

## 功能说明

本插件将当前工作流运行记录与代码仓库进行虚拟关联，使得在 PR 页面能够查看相关工作流的执行状态。

## 使用示例

```yaml
post:
  jobs:
    job_identifier:
      name: post_job
      select: selected_by_default
      needs: []
      steps:
        -
          name: associate-pr-comment
          uses: associate-pr-comment
      if: "${{ default() }}"
      runs-on:
        - default 
```

## 构建

```bash
npm install
npm run build
npm run package-main
npm run package-stop
```


---

## 8. manifest-management-plugin

- **name**: `manifest-management-plugin`
- **creator**: wukong_admin
- **被引用**: 1686
- **版本**: 1.0.8

# Manifest Management Plugin

## 简介

Manifest Management Plugin（Manifest管理插件）是一款基于原生Kubernetes实现的CodeArts Deploy自定义部署插件。它能够根据Kubernetes Manifest资源定义文件执行资源的创建和释放操作，依赖前置的checkout插件拉取manifest所在的代码仓库。

## 功能特性

- **资源创建（DEPLOY）**：根据Manifest定义文件创建Kubernetes资源
- **资源释放（CRUSH）**：根据Manifest定义文件删除Kubernetes资源
- **变量替换**：支持在Manifest文件中使用变量占位符，运行时会进行渲染替换
- **健康检查**：支持等待Job资源创建完成并获取Pod日志
- **多区域支持**：支持华为云多个区域的部署

## 输入参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| `token` | string | 是 | 访问CodeArts的令牌 |
| `gitcode_token` | string | 是 | 访问Gitcode的令牌 |
| `action` | radio | 是 | 操作类型：<br>- `DEPLOY`：创建资源<br>- `CRUSH`：释放资源 |
| `repo` | linkSelect | 是 | 前置checkout操作拉取的代码仓路径 |
| `branch` | linkSelect | 是 | 待操作的Manifest定义所在代码仓分支 |
| `file_path` | input | 是 | 待操作的Manifest定义所在代码仓文件路径，从根目录开始 |
| `custom_shell_script` | shell | 否 | 自定义命令行，在yaml中可通过`${INPUT_CUSTOM_SHELL_SCRIPT}`方式拼接 |

## 使用前提

1. 工作流中需先配置 `checkout` 插件，用于拉取包含Manifest文件的代码仓库
2. 集群访问凭证（kubeconfig）需提前配置在 `/tmp/.kube/config` 路径
3. 确保Kubernetes集群可访问，且当前运行节点有足够的权限操作目标资源

## 工作流程

### DEPLOY（创建资源）

1. 解析输入参数，获取代码仓库路径和Manifest文件路径
2. 执行 `get_manifest.py` 获取Manifest文件内容
3. 执行 `config.sh` 进行配置处理和变量替换
4. 执行 `get_rendered_manifest.py` 渲染最终的Manifest文件
5. 执行 `kubectl apply` 创建资源
6. 等待Pod创建完成（最多60次尝试，每5秒一次）
7. 输出Pod日志并检查Job执行状态

### CRUSH（释放资源）

1. 解析输入参数，获取代码仓库路径和Manifest文件路径
2. 执行 `get_manifest.py` 获取Manifest文件内容
3. 执行 `config.sh` 进行配置处理
4. 执行 `get_rendered_manifest.py` 渲染Manifest文件
5. 执行 `kubectl delete` 删除资源

## 输出变量

| 变量名 | 说明 |
|--------|------|
| `exit_code` | 容器退出码 |

## 错误处理

- **资源创建失败**：kubectl apply命令返回非零退出码时，插件会输出错误信息并退出
- **Pod未创建**：等待超时（60次×5秒）仍未检测到Pod时，返回超时错误
- **Job执行失败**：检测到Job状态为Failed时，输出失败原因并返回错误码

## 项目结构

```
manifest_management_plugin/
├── action.yml              # 插件定义文件
├── package.json            # Node.js依赖配置
├── tsconfig.json           # TypeScript配置
├── zip.js                  # 打包脚本
├── src/
│   ├── main.ts             # 插件入口
│   ├── core/
│   │   └── core.ts         # 核心工具函数
│   ├── common/
│   │   ├── constant.ts     # 常量定义（区域映射等）
│   │   └── utils.ts        # 通用工具函数
│   ├── log/
│   │   ├── log.ts          # 日志工具
│   │   ├── Errors.ts       # 错误定义
│   │   └── errorCode.ts    # 错误码定义
│   └── reportutils.ts      # 报告工具
├── dist/                   # 编译输出目录
│   ├── index.js            # 打包后的入口文件
│   ├── main_pipeline.sh    # 主流程脚本
│   ├── get_manifest.py     # 获取Manifest脚本
│   ├── get_repo.py         # 获取仓库信息脚本
│   ├── get_rendered_manifest.py  # 渲染Manifest脚本
│   ├── config.sh           # 配置文件
│   ├── check_health.py     # 健康检查脚本
│   ├── get_status.py       # 获取状态脚本
│   ├── http_util.py        # HTTP工具脚本
│   ├── rolling.py          # 滚动更新脚本
│   └── kube_config         # Kubernetes配置
└── node_modules/           # Node.js依赖包
```

## 构建和打包

```bash
# 安装依赖
npm install

# 编译TypeScript
npm run build

# 打包主入口
npm run package-main

# 打包插件
npm run dev
```

## 版本信息

- **插件版本**：1.0.1
- **作者**：XXX
- **运行环境**：Node.js 16

## 许可证

ISC



---

## 9. Codecheck

- **name**: `codecheck_gitcode_v2`
- **creator**: wukong_admin
- **被引用**: 156
- **版本**: 0.0.8


# CodeCheckPlugin
动态创建/更新/删除codecheck任务，执行codecheck工程，上传质量报告，监听执行进度，提供执行过程错误原因与指导

## 1.功能

* `CodeCheck`插件;


## 2.使用方法

* 在workflow工程yaml中配置调用

## 3.输入参数说明
    注意事项：
        1.配置字段请检查字段值的准确性，非必填数据无法准确性校验，异常数据也会更新成功，会影响codecheck执行结果
        2.非必填字段如果不配置，则创建/更新不会有此字段，如果配置为空，会创建/更新此字段为空
        3.undefined为保留字段值，请毋将字段值配置为undefined
### project_id:
        codecheck创建任务是的项目id
        是否必要: 必要
### task_name:
        codecheck已创建的任务名;
        是否必要: 必要
### branch:
        执行代码检查时选择检查的代码分支;
        是否必要: 必要
### exclusions:
        排除参数
        是否必要: 非必要
### include_paths:
        检查目录参数
        是否必要: 非必要
### rule_sets:
        规则集,例如：'[{"language":"C#","rule_name":"通用检查规则集"}]'
        是否必要: 非必要
### custom_params:
        自定义编译参数,例如：'[{"key":"compileTool","value":"dotnet"},{"key":"buildToolVersion","value":"dotnetcore3.1"},{"key":"compileScriptCmd","value":"dotnet build sample1.sln"}]'
        是否必要: 非必要

## 4.使用样例
### 4.1 在codearts上创建codecheck任务
#### 4.1.1 在gitcode上创建访问凭证
gitcode界面 - 右上角头像 - 个人设置 - 访问令牌 - 新建访问令牌
填写令牌名称 - 权限选为 只读 - 新建访问令牌
复制保存新建的令牌
#### 4.1.2 在codearts上创建代码仓授权
codecheck项目界面 - 通用设置 - 服务扩展点管理 - 新建服务扩展点 - gitcode | 通用gitcode（gitcode测试环境要选通用git）
填写链接名称 - git仓url - git账户名 - 上面创建的访问令牌 - 确定
#### 4.1.3 新建codecheck任务
代码检查界面 - 新建任务
选择gitcode | 通用git - 任务名 - 选择服务扩展点 - 选择代码仓 - 默认分支 - 检查语言 - 确定
### 4.2 在gitcode上创建流水线任务
gitcode项目界面 - actions - 新建流水线
配置yml，如下
gitcode项目界面 - 项目设置 - action密钥与变量 - 新建仓库密钥
### 4.3 执行流水线任务
#### 4.3.1 执行版本任务
gitcode项目界面 - actions - 选择创建出来的流水线 - 运行 - 选择分支 - 运行workflow
#### 4.3.1 执行合并请求任务
确保yml配置pull_request - 新建合并请求
#### sample:
```
name: mergeCI  #流水线名

on:  
  pull_request:    # 合并请求触发
    types: [open, reopen, update]
    branches: ["main"]
  push:            # 推送到分支触发
    branches: ["main"]
  workflow_dispatch:


stages:
  1769063174487682f53cf-0e5c-4b6e-9d00-f6e4bf662ef9:
    name: 阶段2  # 阶段名
    select: selected_by_default
    jobs:
      JOB_WJKHX:
        name: 任务名2  # 任务名
        select: selected_by_default
        needs: []
        steps:
          - name: Login to CodeArts
            uses: codearts-login  # 引用流水线授权插件
            with:
              region: cn-south-1                        #地域  华南广州 cn-south-1   北京四 cn-north-4
              name: CodeCheck_gray02                    # 账号名
              password: ${{ secrets.USER_PASSWORD }}    # 账号密码，配置在项目私密参数里
              domain-name: hwstaff_zhangjunhui          # 租户名
            id: login
          - name: check测试执行
            uses: codecheck_gitcode_v2                  # 代码检查插件名
            with:
              #rule_sets: '[{"language":"C++","rule_name":"secbrella-cpp"},{"language":"GO","rule_name":"全面检查规则集"},{"language":"php","rule_name":"通用检查规则集"},{"language":"arkts","rule_name":"通用检查规则集"},{"language":"css","rule_name":"CSS-sonar"},{"language":"PYTHON","rule_name":"Python测试 1+/2#"},{"language":"Javascript","rule_name":"鸿蒙JAVASCRIPT语言推荐内容检查规则集"},{"language":"TYPESCRIPT","rule_name":"CodeMars_TS"}]'
              #custom_params: '[{"key":"compileTool","value":"cmake"},{"key":"buildToolVersion","value":"cmake3.15.5-gcc8.3.0"},{"key":"compileScriptCmd","value":"dos2unix build.sh && sh build.sh"}]'
              #exclusions: ''
              #include_paths: ''
              project_id: bbd56f56ab7e4ea3aafa127ab9ba6783 # 必填。创建任务时的project_id
              task_name: littlecode_gitcode_test123        # 必填。创建任务时的任务名
              branch: main                                 # 执行版本级任务时的分支。不影响mr。
        runs-on: 
        - default
```

---

## 10. OpenlibingUploadSarif

- **name**: `openlibing-upload-sarif`
- **creator**: wukong_admin
- **被引用**: 275
- **版本**: 1.0.6

# openlibing-upload-sarif

## 简介

将 CodeQL 扫描结果(SARIF 文件)上传到华为云 OBS 对象存储,并生成标准化的构建产物 JSON,同时通过 APIG 网关回调通知 OpenLibing 服务。

- **插件名**: `openlibing-upload-sarif`

## 功能特性

- 自动检查并定位 SARIF 文件路径(支持 workspace 和 Git 目录自动发现)
- 自动下载安装 `obsutil` 命令行工具
- 上传 SARIF 文件到 OBS 桶 `openlibing-codeql`,设置公共读权限
- 根据 SARIF 文件生成构建产物 `build-result.json`
- 通过 APIG 网关回调通知 OpenLibing 扫描服务
- 支持 APIG 三种鉴权方式:AppKey/AppSecret、AppCode

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| sarif_file | SARIF 文件路径(相对路径或绝对路径) | 是 | - |
| obs_ak | OBS Access Key ID | 是 | - |
| obs_sk | OBS Secret Access Key | 是 | - |
| apig_app_key | APIG 网关 AppKey(鉴权头: `Appkey`) | 否 | - |
| apig_app_secret | APIG 网关 AppSecret(鉴权头: `AppSecret`) | 否 | - |
| apig_app_code | APIG 网关 AppCode(鉴权头: `X-Apig-AppCode`) | 否 | - |

## 输出参数

| 参数 | 说明 |
|------|------|
| result | 上传结果:`success` 或 `failed` |
| download_url | SARIF 文件在 OBS 上的下载地址 |
| build_result_url | 构建产物 JSON 在 OBS 上的下载地址 |

## OBS 路径规则

最终 OBS 对象键的格式为(路径前缀内置为 `codeql-results`,不可配置):

```
codeql-results/{repoBaseName}/{YYYYMMDD.HH}/{sarifFileName}
```

- `repoBaseName`: 从环境变量 `ATOMGIT_REPOSITORY` 或 `GIT_REPOSITORY` 提取仓库名
- 时间戳: 按执行时刻生成,精确到小时

OBS 桶: `openlibing-codeql`
- 写入 Endpoint: `obs.cn-southwest-2.myhuaweicloud.com`
- 读取 Endpoint: `https://openlibing-codeql.obs.cn-southwest-2.myhuaweicloud.com`

## 回调通知

上传成功后,插件会通过 APIG 网关向 OpenLibing 服务发送 POST 回调,携带仓库、流水线、提交与 SARIF 下载地址等信息。

回调 payload 字段:

| 字段 | 来源 |
|------|------|
| repoUrl | `ATOMGIT_REPOSITORY_URL` |
| pipelineId | `ATOMGIT_PIPELINE_ID` |
| pipelineName | `PIPELINE_NAME` |
| pipelineRunId | `ATOMGIT_PIPELINE_RUN_ID` / `PIPELINE_RUN_ID` |
| branch | `ATOMGIT_REF_NAME` |
| commitId | `ATOMGIT_SHA` |
| obsUrl | SARIF 文件下载地址 |

APIG 网关鉴权(按需组合):

| 输入参数 | 请求头 | 说明 |
|----------|--------|------|
| `apig_app_key` | `Appkey` | AppKey 鉴权 |
| `apig_app_secret` | `AppSecret` | 与 AppKey 配套使用 |
| `apig_app_code` | `X-Apig-AppCode` | AppCode 简单鉴权 |

执行日志中会输出当前是否携带了各 APIG 凭据(不打印明文)。回调失败不会影响最终结果(只输出 WARN 日志),SARIF 上传成功即视为成功。

## 使用示例

### 基础用法

```yaml
steps:
  - name: 检出代码
    uses: checkout
    with:
      repository: https://gitcode.com/your-org/your-repo.git
      ref: master

  - name: 运行 CodeQL 扫描
    uses: codeql-action
    with:
      language: javascript
      source-root: ./
      output-path: ./codeql-results.sarif
      query-suite: security-and-quality

  - name: 上传 SARIF 到 OpenLibing
    uses: openlibing-upload-sarif
    with:
      sarif_file: ./codeql-results.sarif
      obs_ak: ${{ secrets.OPENLIBING_OBS_AK }}
      obs_sk: ${{ secrets.OPENLIBING_OBS_SK }}
      apig_app_key: ${{ secrets.OPENLIBING_APIG_APP_KEY }}
      apig_app_secret: ${{ secrets.OPENLIBING_APIG_APP_SECRET }}
```

> APIG 鉴权为可选配置,若无需回调鉴权可省略 `apig_app_key` / `apig_app_secret` / `apig_app_code` 三个字段。

## 构建产物 JSON 格式

插件会在临时目录下生成 `build-result.json`,并随 SARIF 一同上传到 OBS,示例结构:

```json
{
  "type": "build",
  "buildings": [
    {
      "name": "codeql-results.sarif",
      "type": "CodeQL代码检查结果(sarif)",
      "downloadUrl": "https://openlibing-codeql.obs.cn-southwest-2.myhuaweicloud.com/codeql-results/your-repo/20250625.14/codeql-results.sarif"
    }
  ]
}
```

## 执行流程

1. 校验输入参数(`sarif_file`、`obs_ak`、`obs_sk`)
2. 检查 SARIF 文件存在(自动尝试在 workspace 与 Git 目录中查找)
3. 下载并解压 `obsutil` 工具
4. 根据仓库名与时间戳构建 OBS 路径
5. 生成 `build-result.json` 构建产物
6. 上传构建产物目录与 SARIF 文件到 OBS
7. 通过 APIG 回调通知 OpenLibing 服务

## 注意事项

- 运行前需先使用 `official_checkout` 检出代码,以便插件能从环境变量中获取仓库信息
- 需要前置执行 `codeql-action` 等可生成 SARIF 文件的步骤,并提供 `sarif_file` 路径
- 回调通知失败仅产生 WARN,不会阻断流程,最终结果以 OBS 上传是否成功为准
- OBS 桶 `openlibing-codeql`、路径前缀 `codeql-results`、APIG 回调地址均已硬编码在插件中,如有变更需修改源码
- 插件运行依赖 Bash 环境(使用 `shell: '/bin/bash'` 调用 `execSync`)



---

## 11. OpenlibingPreCommitAction

- **name**: `openlibing-pre-commit-action`
- **creator**: wukong_admin
- **被引用**: 2644
- **版本**: 1.0.29

# openlibing-pre-commit-action

## 简介

安装 pre-commit 并对代码仓库执行钩子检查。支持 PR 增量检查和全量检查自动切换。

## 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| extra_args | pre-commit 运行参数。为空时自动判断：PR 事件检查增量文件，非 PR 检查全量；填写时按指定参数执行 | 否 | 空（自动判断） |

## 输出参数

| 参数 | 说明 |
|------|------|
| result | 运行结果：success 或 failed |
| checked_files | 检查的文件范围 |

## 使用示例

### 推荐方式：使用自定义执行机（推荐）

当 `.pre-commit-config.yaml` 中配置的 hooks 仓库地址不是 GitCode 镜像仓时（例如使用了 GitHub 等外部仓库的 hooks），云端执行机可能无法访问这些外部地址。推荐通过自定义执行机（self-hosted runner）来运行，自定义执行机可以访问外部网络资源。流水线配置如下：

```yaml
jobs:
  pre-commit:
    name: pre-commit
    runs-on: ['self-hosted', 'os=ubuntu', 'arch=x64']  # ⚠️ 自定义执行机：必须包含 'self-hosted'，其余标签根据执行机注册时的标签填写，用于精确调度
    steps:
      - name: checkout
        uses: checkout

      - name: setup-python
        uses: setup-python
        with:
          python-version: '3.14'

      - name: run pre-commit
        uses: openlibing-pre-commit-action
        with:
          extra_args: ${{ inputs.extra_args }}
          gc_token: ${{ inputs.GC_TOKEN }}
```

> **关于 `runs-on`**：`'self-hosted'` 为固定必填项，表示使用自定义执行机；后续标签（如 `'os=ubuntu'`、`'arch=x64'`）需与执行机注册时设置的标签一致，流水线将根据标签精确调度到对应的执行机。

#### 自定义执行机准备工作

1. **安装执行机代理**：在组织或仓库的 **Settings → Actions → Runners** 中按照指引下载并安装 self-hosted runner 代理程序
2. **网络要求**：执行机需能访问外部网络（如 GitHub），以便拉取 hooks 仓库
3. **标签配置**：自定义执行机通过 `runs-on: ['self-hosted', 标签]` 的方式使用，注册执行机时可添加自定义标签（如 `os=ubuntu`、`arch=x64`），流水线将根据标签精确调度到对应的执行机

#### 对应的 .pre-commit-config.yaml 示例

以下示例中的 hooks 来自 GitHub 等外部仓库，云端执行机无法访问，**需要使用自定义执行机**，配置如下：

```yaml
repos:
  # ❌ GitHub 仓库 — pre-commit 官方检查工具，云端执行机无法访问，需要自定义执行机
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  # ❌ GitHub 仓库 — Python 代码格式化，同样需要自定义执行机
  - repo: https://github.com/psf/black
    rev: 24.4.2
    hooks:
      - id: black

  # ❌ GitHub 仓库 — gitleaks 敏感信息扫描，需要自定义执行机
  # 安装说明：自动安装依赖 Go 运行环境，有外网代理可自动编译安装（200M+）
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks
        entry: gitleaks dir
```

### 云端执行机（仅使用 GitCode 镜像仓的 hooks）

如果 `.pre-commit-config.yaml` 中所有 hooks 均来自 GitCode 镜像仓，可直接使用云端执行机运行，流水线配置如下：

```yaml
jobs:
  pre-commit:
    name: pre-commit
    runs-on: ['codearts-hosted', 'ubuntu-latest', x64, 'large']  # ☁️ 云端执行机：使用 codearts-hosted 提供的云端运行环境
    steps:
      - name: checkout
        uses: checkout

      - name: setup-python
        uses: setup-python
        with:
          python-version: '3.14'

      - name: run pre-commit
        uses: openlibing-pre-commit-action
        with:
          extra_args: ${{ inputs.extra_args }}
```

#### 对应的 .pre-commit-config.yaml 示例

以下示例中的 hooks 均来自 GitCode 镜像仓，云端执行机可直接访问，**无需自定义执行机**，配置如下：

```yaml
repos:
  # ✅ GitCode 镜像仓 — pre-commit 官方检查工具，国内网络可使用 gitcode 镜像仓加速下载
  - repo: https://gitcode.com/gh_mirrors/pr/pre-commit-hooks
    rev: v4.6.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer

  # ✅ GitCode 镜像仓 — gitleaks 敏感信息扫描，国内网络可使用镜像仓加速下载
  # 安装说明：自动安装依赖 Go 运行环境，国内网络无代理建议先手动下载并安装 Go 环境：https://golang.google.cn/dl
  - repo: https://gitcode.com/GitHub_Trending/gi/gitleaks
    rev: v8.30.1
    hooks:
      - id: gitleaks
        entry: gitleaks dir
```

> **判断依据**：hooks 的 `repo` 地址以 `https://gitcode.com/` 开头的是 GitCode 镜像仓，云端执行机可直接访问；以 `https://github.com/` 或其他外部地址开头的，需要使用自定义执行机。

## GC_TOKEN 配置

`GC_TOKEN` 用于访问私有仓库（私仓）时进行身份认证，区分私仓的访问权限。

### 配置方式

需要在组织中配置 Actions 密钥 `GC_TOKEN`，配置步骤：

1. 进入组织（或仓库）的 **Settings → Secrets → Actions**
2. 新建密钥，名称为 `GC_TOKEN`，值为具有代码访问权限的访问令牌

## 注意事项

- 运行前需先使用 `checkout` 检出代码
- 运行前需先使用 `setup-python` 配置 Python 环境
- 项目根目录需包含 `.pre-commit-config.yaml` 配置文件
- PR 增量检查依赖 `ATOMGIT_BASE_REF` 和 `ATOMGIT_HEAD_REF` 环境变量


---

## 12. ScaPrScan

- **name**: `sca-pr-scan`
- **creator**: wukong_admin
- **被引用**: 436
- **版本**: 1.3.0

# sca-action

SCA 合法合规门禁检查的 GitCode Action 插件，用于在 PR（Pull Request）场景下自动进行开源片段扫描，检测代码中的合规风险。

## 项目结构

```
sca-action/
├── actions/
│   └── sca-pr-action/            # SCA PR 扫描 Action
│       ├── action.yml            # Action 定义（输入/输出/运行方式）
│       └── dist/
│           ├── sca-pr-scan.js    # 扫描主逻辑
│           └── signer.js         # API 网关签名工具
├── package.json                  # 项目配置与构建脚本
└── README.md
```

## 工作原理

1. **获取 PR 信息** — 根据平台域名、仓库名和 PR 编号构造 PR 链接
2. **创建扫描任务** — 调用 SCA 扫描服务 API 提交扫描请求（携带项目名称）
3. **轮询扫描结果** — 每 10 秒查询一次任务状态，最长等待 30 分钟
4. **输出扫描结论** — 根据未确认风险文件数判定 `pass` / `no pass`，并输出报告地址

## Action 输入参数

| 参数 | 说明 | 必填 | 默认值 |
|------|------|------|--------|
| `scan-access-key` | SCA 扫描服务访问密钥 (AK) | 是 | — |
| `scan-secret-key` | SCA 扫描服务密钥 (SK) | 是 | — |
| `pr-id` | PR 编号 | 是 | — |
| `repository-name` | 仓库名称（如 `owner/repo`） | 是 | — |
| `codecheck-ip` | 代码检查服务地址 | 否 | `https://apig.openlibing.com` |
| `codecheck-prefix` | 服务 API 路径前缀 | 否 | `/openlibing-sca` |
| `platform-domain` | 平台域名（用于拼接 PR URL，支持 GitCode/Gitee/GitHub） | 否 | `https://gitcode.com` |
| `project-name` | 项目名称（用于扫描任务） | 是 | - |

## Action 输出

| 输出 | 说明 |
|------|------|
| `result` | 扫描结果：`pass` 表示通过，`no pass` 表示存在风险 |
| `report-url` | 扫描结果报告地址 |
| `scan-id` | 扫描任务 ID |

## 使用方式

### 方式一：手动触发（workflow_dispatch）

在仓库的 `.github/workflows/` 目录下创建工作流文件，通过手动输入 PR 编号和仓库名称触发扫描：

```yaml
name: SCA PR Scan

on:
  workflow_dispatch:
    inputs:
      pr-id:
        description: 'PR编号'
        required: true
      repository-name:
        description: '仓库名称'
        required: true
      platform-domain:
        description: '平台域名'
        required: false
      project-name:
        description: '项目名称'
        required: false

jobs:
  sca-pr-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: checkout

      - name: Run SCA PR Scan
        id: sca-pr-scan
        uses: sca-pr-scan
        with:
          scan-access-key: ${{ secrets.SCAN_ACCESS_KEY }}
          scan-secret-key: ${{ secrets.SCAN_SECRET_KEY }}
          pr-id: ${{ inputs.pr-id }}
          repository-name: ${{ inputs.repository-name }}
          platform-domain: ${{ inputs.platform-domain }}
          project-name: ${{ inputs.project-name }}

      - name: Scan Result
        if: always()
        run: |
          echo "Scan ID: ${{ steps.sca-pr-scan.outputs.scan-id }}"
          echo "Result: ${{ steps.sca-pr-scan.outputs.result }}"
          echo "Report URL: ${{ steps.sca-pr-scan.outputs.report-url }}"

      - name: Check Scan Result
        if: steps.sca-pr-scan.outputs.result == 'no pass'
        run: |
          echo "::error::SCA scan detected risks. Report: ${{ steps.sca-pr-scan.outputs.report-url }}"
          exit 1
```

### 方式二：PR 事件自动触发

在仓库的 `.gitcode/workflows/` 目录下创建工作流文件，PR 打开/重新打开/更新时自动触发扫描：

```yaml
name: SCA PR Scan

on:
  pull_request:
    types: [open, reopen, update]

jobs:
  sca-pr-scan:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: checkout

      - name: Run SCA PR Scan
        id: sca-pr-scan
        uses: sca-pr-scan
        with:
          scan-access-key: ${{ secrets.SCAN_ACCESS_KEY }}
          scan-secret-key: ${{ secrets.SCAN_SECRET_KEY }}
          pr-id: ${{ atomgit.event.pull_request.number }}
          repository-name: ${{ atomgit.repository }}
          platform-domain: ${{ atomgit.api_url }}
          project-name: ${{ inputs.project-name }}
```

## 密钥配置

需要在仓库的 Secrets 中配置以下密钥：

| Secret 名称 | 说明 |
|-------------|------|
| `SCAN_ACCESS_KEY` | SCA 扫描服务 AK |
| `SCAN_SECRET_KEY` | SCA 扫描服务 SK |

## 构建

项目使用 `@vercel/ncc` 打包 Action 代码，`adm-zip` 生成可分发的 zip 包：

```bash
# 仅打包 Action 代码
npm run package

# 打包并生成 zip
npm run build
```

构建产物为 `sca-pr-action.zip`，包含 Action 定义、扫描主逻辑和签名工具。


---

## 13. JestReport

- **name**: `jest-report`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.0.3

# jest-report

解析 Jest 测试结果文件并生成可读的 Markdown 测试报告，一个步骤完成测试结果收集与展示。

- **结果解析**：支持解析 Jest JUnit XML 格式的测试结果文件
- **自动执行**：可选由插件自动执行测试命令，无需额外步骤
- **灵活路径**：支持 glob 模式匹配测试结果文件
- **Markdown 报告**：自动生成包含通过/失败/跳过统计、失败用例详情的可读报告
- **失败控制**：可配置失败用例或空结果时是否将步骤标记为失败
- **详细日志**：支持 verbose 模式输出完整测试结果

---

## 快速开始

### 流水线配置示例

```yaml
 -
    name: checkout
    uses: checkout
    with:
      repository: **********
      ref: master
      token: ******
      path: "test"
 -
    name: setup-node
    uses: setup-node
    with:
      node-version: 22.22.2
      architecture: x64
 -
    name: 安装依赖
    run: |
      cd test
      npm install
 -
    name: jest-report
    identifier: jest-report
    uses: jest
    with:
      # （可选）测试结果文件路径，支持 glob
      path: junit.xml
      # （可选）是否由插件执行测试命令
      run-tests: "true"
      # （可选）测试执行命令
      test-command: npx jest || true
      # （可选）执行测试命令的工作目录
      working-directory: "./test"
      # （可选）存在失败用例时是否标记步骤失败
      fail-on-error: "false"
      # （可选）未找到结果文件时是否标记步骤失败
      fail-on-empty: "true"
      # （可选）列出哪些测试用例
      list-tests: failed
      # （可选）详细日志输出
      verbose: "false"
```


### 参数说明

| 参数名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `path` | 否 | - | Jest 测试结果文件路径，支持 glob 模式匹配，如 `junit.xml` |
| `run-tests` | 否 | `false` | 是否由插件执行测试命令。设为 `true` 时插件自动运行测试，无需额外的测试执行步骤 |
| `test-command` | 否 | `npx jest` | 测试执行命令，仅在 `run-tests` 为 `true` 时生效 |
| `working-directory` | 否 | `./` | 执行测试命令的工作目录 |
| `fail-on-error` | 否 | `true` | 存在失败用例时是否将步骤标记为失败。设为 `false` 时即使有失败用例步骤也标记为成功 |
| `fail-on-empty` | 否 | `true` | 未找到测试结果文件时是否将步骤标记为失败 |
| `list-tests` | 否 | `failed` | 报告中列出哪些测试用例：`all`（全部）、`failed`（仅失败）、`none`（不列出） |
| `verbose` | 否 | `false` | 是否启用详细日志输出 |

### 输出参数

| 参数名 | 说明 | 示例值 |
|--------|------|--------|
| `conclusion` | 最终结论 | `success` / `failure` |
| `passed` | 通过的测试用例数 | `42` |
| `failed` | 失败的测试用例数 | `3` |
| `skipped` | 跳过的测试用例数 | `1` |
| `summary_file` | 生成的测试报告 Markdown 文件路径 | `/path/to/test-reporter-summary.md` |

---

## 使用场景

### 场景一：仅解析已有测试结果

适用于已有独立的测试执行步骤，仅需解析结果并生成报告：

```yaml
 -
    name: 执行测试
    run: |
      cd test
      npx jest --ci --reporters=jest-junit
 -
    name: jest-report
    uses: jest
    with:
      path: test/junit.xml
      fail-on-error: "true"
      list-tests: failed
```

### 场景二：由插件执行测试

适用于无需单独配置测试步骤，插件一站式执行并报告：

```yaml
 -
    name: jest-report
    uses: jest
    with:
      run-tests: "true"
      test-command: npx jest --ci || true
      working-directory: "./test"
      fail-on-error: "false"
      list-tests: all
```

### 场景三：查看报告内容

在后续步骤中查看生成的报告文件：

```yaml
 -
    name: 查看报告
    uses: official_shell_plugin
    with:
      OFFICIAL_SHELL_SCRIPT_INPUT: |
        if [ -f "test-reporter-summary.md" ]; then
          cat test-reporter-summary.md
        else
          echo "未找到报告文件"
        fi
```

---

## Markdown 报告样例

```markdown
# Jest 测试报告

> **结论**: ✅ 通过 | **通过**: 42 | **失败**: 3 | **跳过**: 1

---

## 测试套件统计

| 状态 | 数量 |
| :--- | :--- |
| ✅ 通过 | 42 |
| ❌ 失败 | 3 |
| ⏭️ 跳过 | 1 |
| **总计** | **46** |

---

## 失败用例详情

### 1. ❌ utils.test.ts — should format date correctly

| 属性 | 值 |
| :--- | :--- |
| **测试套件** | `tests/utils.test.ts` |
| **用例名称** | `should format date correctly` |
| **失败原因** | Expected "2024-01-01" but received "01/01/2024" |

---

### 2. ❌ api.test.ts — should handle error response

| 属性 | 值 |
| :--- | :--- |
| **测试套件** | `tests/api.test.ts` |
| **用例名称** | `should handle error response` |
| **失败原因** | Timeout - Async callback was not invoked within the 5000 ms timeout |

---
```

---

## 常见问题

### 如何生成 JUnit XML 格式的测试结果

需要安装 `jest-junit` 依赖并在 Jest 配置中启用：

```bash
npm install --save-dev jest-junit
```

在 `jest.config.js` 中配置：

```js
module.exports = {
  reporters: [
    'default',
    'jest-junit'
  ]
};
```

或通过命令行参数：

```bash
npx jest --ci --reporters=jest-junit
```

### 使用自定义结果文件路径

通过 `path` 参数指定，支持 glob 模式：

```yaml
with:
  path: "**/junit.xml"
```

### 测试失败但不阻塞流水线

设置 `fail-on-error: "false"`，即使有失败用例步骤也会标记为成功，适用于测试结果仅供参考的场景。

### 未找到结果文件

确保测试已正确执行并生成了 JUnit XML 文件。若需忽略空结果，设置 `fail-on-empty: "false"`。


---

## 14. GithubTagAction

- **name**: `github-tag-action`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 2.0.3

# github-tag-action

自动计算语义化版本号并创建/推送 Git 标签，支持手动指定和基于 Conventional Commits 规范的自动版本计算。

- 手动模式，直接指定版本号创建标签
- 自动模式，基于 Conventional Commits 提交规范自动计算下一个版本号
- 强制升级，可通过 `custom-release` 参数覆盖自动计算结果
- 安全设计，访问令牌不在日志中明文输出，路径遍历防护

## 版本号自动计算规则

插件根据 [Conventional Commits](https://www.conventionalcommits.org/) 规范分析提交信息：

| 提交信息 | 升级类型 | 示例 |
|---------|---------|------|
| `fix: 修复xxx` | Patch（修订号） | `v1.0.0` → `v1.0.1` |
| `feat: 新增xxx` | Minor（次版本号） | `v1.0.0` → `v1.1.0` |
| 包含 `BREAKING CHANGE` | Major（主版本号） | `v1.0.0` → `v2.0.0` |

## Usage

### 手动指定版本号

```yaml
- name: github-tag-action
  uses: github-tag-action
  with:
    tag-version: v1.0.0
    access-token: ${{ 你的访问令牌 }}
    branch: master
```

### 自动计算版本号（推荐）

```yaml
- name: github-tag-action
  uses: github-tag-action
  with:
    calculate-version: 'true'
    default-bump: patch
    branch: master
    access-token: ${{ 你的访问令牌 }}
```

### 自动模式 + 强制指定升级类型

```yaml
- name: github-tag-action
  uses: github-tag-action
  with:
    calculate-version: 'true'
    custom-release: minor
    branch: master
    access-token: ${{ 你的访问令牌 }}
```

### 完整双阶段流水线

```yaml
stages:
  version_tag_stage:
    jobs:
      tag_job:
        name: 版本计算与打标签
        steps:
          - name: checkout
            uses: checkout
            with:
              repository: ${{ 你的仓库地址 }}
              ref: master
              token: ${{ 你的访问令牌 }}
              fetch-depth: 0

          - name: github-tag-action
            uses: github-tag-action
            with:
              calculate-version: 'true'
              default-bump: patch
              branch: master
              access-token: ${{ 你的访问令牌 }}
```

> **提示**：自动版本计算模式需要 `fetch-depth: 0`（完整历史记录）才能正确分析提交信息。

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|--------|------|
| tag-version | 否 | — | 标签版本号，手动模式必填（如 `v1.0.0`） |
| calculate-version | 否 | false | 是否启用自动版本计算，设为 `true` 启用 |
| default-bump | 否 | patch | 当提交无匹配时的默认升级类型：`patch` / `minor` / `major` / `none` |
| custom-release | 否 | — | 强制升级类型，优先级最高：`patch` / `minor` / `major` |
| tag-message | 否 | — | 标签信息，默认使用版本号 |
| branch | **是** | — | 目标分支，如 `master`、`main` |
| access-token | 否 | — | Git 访问令牌，也支持 `ACCESS_TOKEN` / `GIT_TOKEN` 环境变量 |
| repository-path | 否 | — | 仓库路径（如 `./my-repo`），未指定则使用当前目录 |

> **说明**：`calculate-version` 为 `false` 时，`tag-version` 必填；为 `true` 时，插件自动计算版本号。

## Outputs

| 输出 | 说明 |
|------|------|
| success | 操作是否成功（`true` / `false`） |
| tag-version | 创建的标签版本号（如 `v1.2.3`） |
| tag-hash | 标签对应的提交哈希 |
| bump-type | 版本升级类型（`patch` / `minor` / `major` / `none`，仅自动模式） |

## 常见问题

### 执行报错 `unable to auto-detect email address`

流水线环境中 Git 未配置 `user.email` 和 `user.name`。**本插件 v2.0.0+ 已自动处理此问题**，会在创建标签前自动配置默认的用户信息。

### 标签已存在会怎样？

插件会检测标签是否存在，如果已存在会报错并停止，避免覆盖已有标签。

### 如何查看插件运行日志？

在流水线执行记录中，点击对应步骤即可查看详细日志输出。

## 提交信息规范参考

推荐在团队内推行 [Conventional Commits](https://www.conventionalcommits.org/) 规范，确保版本号能被正确计算：

```
feat: 新增用户注册功能
fix: 修复登录页面样式问题
fix(api): 修复接口超时异常
feat(backend): 添加缓存支持

BREAKING CHANGE: 重构了核心 API 接口
```


---

## 15. SetupYarn

- **name**: `setup-yarn`
- **creator**: wukong_admin
- **被引用**: 30
- **版本**: 1.0.3

# setup-yarn

通过 npm 安装并配置指定版本的 Yarn 包管理器，一个步骤完成 Yarn 构建环境准备。

- Yarn 安装，支持精确版本（`1.22.19`）和系列版本（`1`）两种模式
- 支持从 `.nvmrc` 版本文件读取版本
- 本地缓存复用，重复流水线跳过下载
- 自动设置 `YARN_HOME`、`PATH`，无需手动配置
- 支持架构选择（`x64`/`arm64`）

## 目录

- [Usage](#usage)
  - [基础用法：指定 Yarn 版本](#基础用法指定-yarn-版本)
  - [从 .nvmrc 文件读取版本](#从-nvmrc-文件读取版本)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [版本文件](#版本文件)

## Usage

### 基础用法：指定 Yarn 版本

```yaml
name: setup-yarn
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-yarn
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-yarn
        select: selected_by_default
        needs: []
        steps:
          - name: setup-yarn
            uses: setup-yarn
            with:
              yarn-version: '1'
          - name: Verify
            run: |-
                yarn --version
                echo "YARN_HOME=$YARN_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

精确版本：

```yaml
- name: setup-yarn
  uses: setup-yarn
  with:
    yarn-version: '1.22.19'
```

### 从 .nvmrc 文件读取版本

在代码仓库根目录放置 `.nvmrc` 文件，内容为版本号：

```text
1.22.19
```

流水线配置：

```yaml
name: setup-yarn-from-file
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-yarn
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-yarn
        select: selected_by_default
        needs: []
        steps:
          - name: setup-yarn
            uses: setup-yarn
            with:
              yarn-version-file: '.nvmrc'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                yarn --version
                echo "YARN_HOME=$YARN_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `yarn-version` | 否 | `''` | Yarn 版本，支持精确模式（`1.22.19`）和系列模式（`1`）。与 `yarn-version-file` 至少填一个 |
| `yarn-version-file` | 否 | `''` | 版本文件路径，支持 `.nvmrc` |
| `architecture` | 否 | `''` | CPU 架构（`x64`、`arm64`），默认取操作系统架构 |

## Outputs

| 输出 | 说明 |
|------|------|
| `version` | 实际安装的 Yarn 版本 |
| `tool-home` | Yarn 安装目录 |
| `yarn-home` | YARN_HOME 环境变量值（华为云 CodeArts 兼容） |
| `yarn-bin` | Yarn bin 目录路径（华为云 CodeArts 兼容） |
| `env-file` | 环境变量文件路径，可在后续步骤中使用 source 命令加载 |

## 版本文件

当 `yarn-version` 为空且 `yarn-version-file` 有值时，插件从指定文件读取 Yarn 版本。`yarn-version` 有值时优先使用，忽略 `yarn-version-file`。两者都为空时报错。

**`.nvmrc`**（nvm 格式）：

```text
1.22.19
```

或系列版本：

```text
1
```


---

## 16. SetupTerraform

- **name**: `setup-terraform`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 2.0.3

# setup-terraform

> **版本：2.0.3**

在流水线中安装指定版本的 Terraform CLI，支持版本文件读取、缓存管理和凭证配置。

- 指定版本安装或从 `.terraform-version` 文件读取
- 缓存已安装的二进制文件，加速后续构建
- 自动设置 `TERRAFORM_HOME` 和 `PATH` 环境变量
- 支持配置 Terraform Cloud 凭证（`.terraformrc`）

## 目录

- [Usage](#usage)
  - [指定版本](#指定版本)
  - [从版本文件读取](#从版本文件读取)
  - [配置 Terraform Cloud 凭证](#配置-terraform-cloud-凭证)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [版本文件](#版本文件)

## Usage

### 指定版本

```yaml
name: setup-terraform
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建
        select: selected_by_default
        needs: []
        steps:
          - name: setup-terraform
            uses: setup-terraform
            with:
              version: '1.7.0'
          - name: Verify
            run: |-
              terraform version
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 从版本文件读取

项目根目录放置 `.terraform-version` 文件，插件自动读取版本号：

```yaml
steps:
  - name: setup-terraform
    uses: setup-terraform
    with:
      version-file: '.terraform-version'
```

### 配置 Terraform Cloud 凭证

安装 Terraform CLI 的同时写入 `.terraformrc` 凭证配置，用于后续与 Terraform Cloud 交互：

```yaml
steps:
  - name: setup-terraform
    uses: setup-terraform
    with:
      version: '1.7.0'
      cli-config-hostname: 'app.terraform.io'
      cli-config-token: '${{ env.TFC_TOKEN }}'
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| version | 否 | `''` | Terraform 版本，如 `1.7.0`、`latest` |
| version-file | 否 | `''` | `.terraform-version` 文件路径 |
| enable-cache | 否 | `true` | 启用二进制缓存 |
| custom-install-path | 否 | `''` | 自定义 Terraform 安装/下载目录，优先级最高。用于规避默认缓存目录权限问题（EACCES） |
| set-env | 否 | `true` | 设置 `TERRAFORM_HOME` 和 `PATH` 环境变量 |
| cli-config-hostname | 否 | `''` | Terraform CLI credentials hostname |
| cli-config-token | 否 | `''` | Terraform CLI credentials token |
| token | 否 | `${{ cloud_dragon_token }}` | 工作流认证 token |
| verbose | 否 | `true` | 详细日志 |

## Outputs

| 输出 | 说明 |
|------|------|
| terraform-version | 实际安装的 Terraform 版本 |
| terraform-path | terraform 二进制文件路径 |
| cache-hit | 是否命中缓存 |
| cache-enabled | 缓存是否启用 |
| download-source | 下载来源 |
| version-source | 版本来源（explicit / version-file / latest-resolved / semver-resolved） |

## 版本文件

在项目根目录创建 `.terraform-version` 文件，写入所需版本号：

```
1.7.0
```

插件读取该文件后自动安装对应版本。`version` 和 `version-file` 同时指定时，`version` 优先。


---

## 17. SetupPython

- **name**: `setup-python`
- **creator**: wukong_admin
- **被引用**: 3524
- **版本**: 2.0.8

# setup-python

## 目录

[TOC]

## 概述

​	`setup-python` 用于在 CodeArts Pipeline 中安装并配置指定版本的 Python。插件会通过 CodeArts 构建工具接口查询可用的 Python 预构建包，按当前运行机的系统、发行版版本和 CPU 架构选择匹配包；

​	1.支持版本号，范围

​	2.支持从.python-version文件读取版本号

## Usage

### 1.精确安装：安装 Python 3.14.3

以下是一个最简的示例，它使用 `actions/setup-python` 安装 Python，并打印版本号验证安装

1.创建流水线，在流水线的.**gitcode/workflows/xxxxx.yml**里面输入如下内容：

```yaml
# .gitcode/workflows/test.yml
name: python
on:
  push:
    branches: [ "main"]
  workflow_dispatch:

stages:
  stage1:
    name: 阶段_1
    select: selected_by_default
    jobs:
      JOB_WJKHX:
        name: 执行shell
        select: selected_by_default
        needs: []
        steps:
        # 1.安装 Python（只需指定版本）
          - name: setup-python
            uses: setup-python
            with: 
             version: 3.14.3
          # 2.验证安装
          - name: Python version
            run: python --version           
        if: "${{ default() }}"
        runs-on: ['codearts-hosted', 'euler-latest', x64, 'large']
    pre:
    - type: auto
```

核心yaml，上述完整代码的steps一部分，在这里面更改version可已更改下载python的版本

```yaml
        steps:
          - name: setup-python
            uses: setup-python
            with: 
             version: 3.14.3
```

##### 注：uses必须和插件名字相同，不需要在后面追加版本号

### 2.从 .python-version 文件读取版本

```yaml
# .gitcode/workflows/test.yml
name: python
on:
  push:
    branches: [ "main"]
  workflow_dispatch:

stages:
  stage1:
    name: 阶段_1
    select: selected_by_default
    jobs:
      JOB_WJKHX:
        name: 执行shell
        select: selected_by_default
        needs: []
        steps:
        # 1.安装 Python（只需指定版本文件）
          - name: setup-python
            uses: setup-python
            with: 
             version-file:'.python-version'
          # 2.验证安装
          - name: Python version
            run: python --version           
        if: "${{ default() }}"
        runs-on: ['codearts-hosted', 'ubuntu-latest', x64, 'large']
    pre:
    - type: auto
```



## Inputs

| 参数           | 必填 | 默认值     | 说明                                                         |
| -------------- | ---- | ---------- | ------------------------------------------------------------ |
| `version`      | 否   | `''`       | Python 版本号、范围或别名，如 3.12、>=3.9、~3.10.0           |
| `version-file` | 否   | `''`       | 版本文件路径，如 `.python-version`（与 `version` 至少提供一个） |
| `tool-cache`   | 否   | `'true'`   | 是否启用本地工具缓存                                         |
| `dep-cache`    | 否   | `'false'`  | 是否输出依赖缓存元信息（pip 缓存）                           |
| `arch`         | 否   | `''`       | 目标架构，如 `x64`、`arm64`                                  |
| `latest`       | 否   | `'false'`  | 是否选择满足条件的最新版本                                   |
| `cache`        | 否   | `'false'`  | 兼容旧模板，等价于 `dep-cache`                               |
| `cache-path`   | 否   | `''`       | 缓存依赖文件路径或缓存定位线索                               |
| `cache-scope`  | 否   | `'branch'` | 缓存隔离范围，支持 `branch` 或 `repo`                        |

## Outputs

| 参数             | 说明                                                |
| ---------------- | --------------------------------------------------- |
| `version`        | 实际安装并生效的 Python 版本                        |
| `tool-home`      | Python 安装目录                                     |
| `tool-bin`       | Python 可执行文件路径或 bin 目录                    |
| `tool-cache-hit` | 是否命中本地工具缓存                                |
| `cache-key`      | 提供给通用 cache 插件使用的缓存键                   |
| `cache-paths`    | 提供给通用 cache 插件使用的缓存路径列表，按换行分隔 |

---

## 18. SetupPnpm

- **name**: `setup-pnpm`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.0.3

# setup-pnpm

通过 npm 安装并配置指定版本的 pnpm 包管理器，一个步骤完成 pnpm 构建环境准备。

- pnpm 安装，支持精确版本（`10.1.0`）和系列版本（`10`）两种模式
- 支持从 `.nvmrc` 版本文件读取版本
- 本地缓存复用，重复流水线跳过下载
- 自动设置 `PNPM_HOME`、`PATH`，无需手动配置
- 支持架构选择（`x64`/`arm64`）

## 目录

- [Usage](#usage)
  - [基础用法：指定 pnpm 版本](#基础用法指定-pnpm-版本)
  - [从 .nvmrc 文件读取版本](#从-nvmrc-文件读取版本)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [版本文件](#版本文件)

## Usage

### 基础用法：指定 pnpm 版本

```yaml
name: setup-pnpm
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-pnpm
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-pnpm
        select: selected_by_default
        needs: []
        steps:
          - name: setup-pnpm
            uses: setup-pnpm
            with:
              pnpm-version: '10'
          - name: Verify
            run: |-
              pnpm --version
              echo "PNPM_HOME=$PNPM_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

精确版本：

```yaml
- name: setup-pnpm
  uses: setup-pnpm@1.0.2
  with:
    pnpm-version: '10.1.0'
```

### 从 .nvmrc 文件读取版本

在代码仓库根目录放置 `.nvmrc` 文件，内容为版本号：

```text
10.1.0
```

流水线配置：

```yaml
name: setup-pnpm-from-file
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-pnpm
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-pnpm
        select: selected_by_default
        needs: []
        steps:
          - name: setup-pnpm
            uses: setup-pnpm
            with:
              pnpm-version-file: '.nvmrc'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                pnpm --version
                echo "PNPM_HOME=$PNPM_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `pnpm-version` | 否 | `''` | pnpm 版本，支持精确模式（`10.1.0`）和系列模式（`10`）。与 `pnpm-version-file` 至少填一个 |
| `pnpm-version-file` | 否 | `''` | 版本文件路径，支持 `.nvmrc` |
| `architecture` | 否 | `''` | CPU 架构（`x64`、`arm64`），默认取操作系统架构 |

## Outputs

| 输出 | 说明 |
|------|------|
| `version` | 实际安装的 pnpm 版本 |
| `tool-home` | pnpm 安装目录 |
| `pnpm-home` | PNPM_HOME 环境变量值（华为云 CodeArts 兼容） |
| `pnpm-bin` | pnpm bin 目录路径（华为云 CodeArts 兼容） |
| `env-file` | 环境变量文件路径，可在后续步骤中使用 source 命令加载 |

## 版本文件

当 `pnpm-version` 为空且 `pnpm-version-file` 有值时，插件从指定文件读取 pnpm 版本。`pnpm-version` 有值时优先使用，忽略 `pnpm-version-file`。两者都为空时报错。

**`.nvmrc`**（nvm 格式）：

```text
10.1.0
```

或系列版本：

```text
10
```


---

## 19. SetupPhp

- **name**: `setup-php`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.0.9

# setup-php

安装并配置指定版本的 PHP，一个步骤完成 PHP 构建环境准备。

- PHP 安装，支持精确版本（`8.2.10`）和系列版本（`8`）两种模式
- 支持从版本文件读取版本
- 从华为云 OBS 获取安装包，支持多平台架构（`x64`/`arm64`）
- 本地缓存复用，重复流水线跳过下载
- 自动设置 `PHP_HOME`、`PATH`
- 自动检测并安装 PHP 运行时系统依赖

## 目录

- [Usage](#usage)
  - [基础用法：指定 PHP 版本](#基础用法指定-php-版本)
  - [从版本文件读取版本](#从版本文件读取版本)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [版本文件](#版本文件)

## Usage

### 基础用法：指定 PHP 版本

```yaml
name: setup-php
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-php
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-php
        select: selected_by_default
        needs: []
        steps:
          - name: setup-php
            uses: setup-php@1.0.9
            with:
              php-version: '8'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                php --version
                echo "PHP_HOME=$PHP_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

精确版本：

```yaml
- name: setup-php
  uses: setup-php@1.0.9
  with:
    php-version: '8.2.10'
```

### 从版本文件读取版本

在代码仓库根目录放置版本文件，内容为版本号：

```text
8.2.10
```

流水线配置：

```yaml
name: setup-php-from-file
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-php
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-php
        select: selected_by_default
        needs: []
        steps:
          - name: setup-php
            uses: setup-php@1.0.9
            with:
              php-version-file: '.php-version'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                php --version
                echo "PHP_HOME=$PHP_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `php-version` | 否 | `''` | PHP 版本，支持精确模式（`8.2.10`）和系列模式（`8`）。与 `php-version-file` 至少填一个 |
| `php-version-file` | 否 | `''` | 版本文件路径 |
| `architecture` | 否 | `''` | CPU 架构（`x64`、`arm64`），默认取操作系统架构 |
| `update-environment` | 否 | `true` | 设置 `PHP_HOME` 和 `PATH` |
| `token` | 否 | `${{ cloud_dragon_token }}` | 工作流认证 token，从 OBS 下载时必填 |

## Outputs

| 输出 | 说明 |
|------|------|
| `php-version` | 实际安装的 PHP 版本 |
| `php-path` | PHP 安装目录 |

## 版本文件

当 `php-version` 为空且 `php-version-file` 有值时，插件从指定文件读取 PHP 版本。`php-version` 有值时优先使用，忽略 `php-version-file`。两者都为空时报错。

**`.php-version`**：

```text
8.2.10
```

或系列版本：

```text
8
```


---

## 20. SetupNode

- **name**: `setup-node`
- **creator**: wukong_admin
- **被引用**: 694
- **版本**: 1.1.0

# setup-node

安装并配置指定版本的 Node.js 与包管理器，一个步骤完成 Node.js 构建环境准备。

- Node.js 安装，支持精确版本（`18.17.0`）和系列版本（`18`）两种模式
- 支持从 `.nvmrc`、`.node-version` 版本文件读取版本
- 支持包管理器选择（npm/yarn/pnpm）及版本指定
- 支持自定义 registry 镜像地址
- 本地缓存复用，重复流水线跳过下载
- 自动设置 `NODE_HOME`、`PATH`，包管理器自动配置镜像

## 目录

- [Usage](#usage)
  - [基础用法：指定 Node.js 版本](#基础用法指定-nodejs-版本)
  - [从 .nvmrc 文件读取版本](#从-nvmrc-文件读取版本)
  - [指定包管理器和镜像](#指定包管理器和镜像)
  - [Node.js + 包管理器同时安装](#nodejs--包管理器同时安装)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [版本文件](#版本文件)

## Usage
### 基础用法：指定 Node.js 版本

```yaml
name: setup-node
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-node
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-node
        select: selected_by_default
        needs: []
        steps:
          - name: setup-node
            uses: setup-node
            with:
              node-version: '18'
          - name: Verify
            run: |-
               node -v
               echo "NODE_HOME=$NODE_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

精确版本：

```yaml
- name: setup-node
  uses: setup-node
  with:
    node-version: '18.17.0'
```
接口存在的版本
| 版本 | 最新小版本 |
| :--- | :--- |
| 16.x | 16.20.2 |
| 18.x | 18.20.8 |
| 20.x | 20.20.2 |
| 22.x | 22.22.2 |
| 24.x | 24.14.1 |
### 从 .nvmrc 文件读取版本

在代码仓库根目录放置 `.nvmrc` 文件，内容为版本号：

```text
18.17.0
```

流水线配置：

```yaml
name: setup-node-from-file
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-node
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-node
        select: selected_by_default
        needs: []
        steps:
          - name: setup-node
            uses: setup-node
            with:
              node-version-file: '.nvmrc'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                node -v
                echo "NODE_HOME=$NODE_HOME"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 指定包管理器和镜像

指定 `package-manager` 和 `registry-url` 即可配置包管理器及其镜像：

```yaml
name: setup-node-registry
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-node
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-node
        select: selected_by_default
        needs: []
        steps:
          - name: setup-node
            uses: setup-node
            with:
              node-version: '18'
              package-manager: 'npm'
              registry-url: 'https://registry.npmmirror.com/'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                node -v
                npm config get registry
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### Node.js + 包管理器同时安装

指定 `package-manager` 和 `package-manager-version` 即可同时安装指定版本的包管理器：

```yaml
name: setup-node-yarn
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建setup-node
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建setup-node
        select: selected_by_default
        needs: []
        steps:
          - name: setup-node
            uses: setup-node
            with:
              node-version: '18'
              package-manager: 'yarn'
              package-manager-version: '1.22.19'
              registry-url: 'https://registry.npmmirror.com/'
          - name: Verify
            uses: official_shell_plugin
            with:
              OFFICIAL_SHELL_SCRIPT_INPUT: |-
                node -v
                yarn --version
                echo "YARN_REGISTRY=$YARN_REGISTRY"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `node-version` | 否 | `''` | Node.js 版本，支持精确模式（`18.17.0`）和系列模式（`18`）。与 `node-version-file` 至少填一个 |
| `node-version-file` | 否 | `''` | 版本文件路径，支持 `.nvmrc`、`.node-version` |
| `architecture` | 否 | `''` | CPU 架构（`x64`、`arm64`），默认取操作系统架构 |
| `package-manager` | 否 | `npm` | 包管理器类型（`npm`、`yarn`、`pnpm`） |
| `package-manager-version` | 否 | `''` | 包管理器版本 |
| `registry-url` | 否 | `''` | 包管理器 registry 镜像地址 |
| `update-environment` | 否 | `true` | 设置 `NODE_HOME` 和 `PATH` |
| `token` | 是 | `${{ cloud_dragon_token }}` | 工作流认证 token，由流水线自动注入 |

## Outputs

| 输出 | 说明 |
|------|------|
| `node-version` | 实际安装的 Node.js 版本 |
| `node-path` | Node.js 安装目录 |
| `package-manager` | 使用的包管理器类型 |
| `package-manager-version` | 包管理器版本 |
| `registry-url` | 镜像地址 |

## 版本文件

当 `node-version` 为空且 `node-version-file` 有值时，插件从指定文件读取 Node.js 版本。`node-version` 有值时优先使用，忽略 `node-version-file`。两者都为空时报错。

**`.nvmrc`**（nvm 格式）：

```text
18.17.0
```

或系列版本：

```text
18
```

**`.node-version`**：

```text
18.17.0
```


---

## 21. SetupJdk

- **name**: `setup-jdk`
- **creator**: wukong_admin
- **被引用**: 1549
- **版本**: 2.0.7

# setup-jdk

> **版本：2.0.7**

一个步骤完成 Java 构建环境准备 — JDK + Maven 一体化管理插件。

## 特性

- JDK + Maven 一体化安装
- 支持精确版本（17.0.18+8）和系列版本（17）
- 支持 `.java-version`、`.tool-versions` 版本文件读取版本
- 本地缓存复用，重复流水线跳过下载
- 自动设置 `JAVA_HOME`、`PATH`、`MAVEN_HOME`

## 目录

- [Usage](#usage)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [版本文件](#版本文件)
- [支持版本](#支持版本)

## Usage

### 基础用法：指定 JDK 版本

```yaml
name: build
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建
        select: selected_by_default
        needs: []
        steps:
          - name: checkout
            uses: checkout
          - name: setup-jdk
            uses: setup-jdk
            with:
              jdk-version: '17'
          - name: verify
            run: |-
              java -version 2>&1
              echo "JAVA_HOME=$JAVA_HOME"
        if: "${{ default() }}"
        runs-on: ['self-hosted', 'os=ubuntu', 'arch=x64']
        pre:
          - type: auto
```

### 精确版本

```yaml
- name: setup-jdk
  uses: setup-jdk
  with:
    jdk-version: '17.0.18+8'
```

### 从版本文件读取版本

在代码仓库根目录放置 `.java-version` 文件，内容为版本号（如 `17.0.18+8` 或 `17`）：

```yaml
- name: setup-jdk
  uses: setup-jdk
  with:
    jdk-version-file: '.java-version'
```

### JDK + Maven 同时安装

指定 `maven-version` 即可同时安装 Maven，默认配置华为云镜像源。

```yaml
- name: setup-jdk
  uses: setup-jdk
  with:
    jdk-version: '17'
    maven-version: '3.9.15'
```

### 自定义 Maven settings.xml

通过 `maven-custom-settings` 传入自定义 `settings.xml` 内容，覆盖默认镜像配置：

```yaml
- name: setup-jdk
  uses: setup-jdk
  with:
    jdk-version: '17'
    maven-version: '3.9.15'
    maven-custom-settings: |
      <settings>
        <mirrors>
          <mirror>
            <id>my-mirror</id>
            <mirrorOf>central</mirrorOf>
            <url>https://my-repo.example.com/maven2</url>
          </mirror>
        </mirrors>
      </settings>
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `jdk-version` | 否 | `''` | JDK 版本，支持精确模式（17.0.18+8）和系列模式（17）。与 `jdk-version-file` 至少填一个 |
| `jdk-version-file` | 否 | `''` | 版本文件路径，支持 `.java-version`、`.tool-versions` |
| `jdk-distribution` | 否 | `temurin` | JDK 发行版标签，用于缓存命名和安装路径标识 |
| `arch` | 否 | `''` | 目标架构（如 `arm64`、`x64`），留空则自动检测 |
| `enable-cache` | 否 | `true` | 启用 JDK 缓存 |
| `custom-install-path` | 否 | `''` | 自定义 JDK 安装/下载目录，优先级最高。用于规避默认缓存目录权限问题（EACCES） |
| `temp-install-dir` | 否 | `''` | 缓存禁用且未指定 custom-install-path 时的临时安装目录 |
| `set-env` | 否 | `true` | 设置 `JAVA_HOME` 和 `PATH` |
| `dl-timeout-mins` | 否 | `10` | 下载超时（分钟） |
| `dl-max-retries` | 否 | `3` | 最大下载重试次数 |
| `token` | 否 | `${{ cloud_dragon_token }}` | 工作流认证 token |
| `verbose` | 否 | `true` | 详细日志 |
| `maven-version` | 否 | `''` | Maven 版本（如 3.9.15），指定则同时安装 Maven |
| `maven-download-url` | 否 | `''` | Maven 直链下载地址 |
| `maven-enable-cache` | 否 | `true` | 启用 Maven 缓存 |
| `maven-custom-settings` | 否 | `''` | 自定义 `settings.xml` 内容，覆盖默认镜像配置 |
| `maven-repo-cache-scope` | 否 | `all` | Maven 仓库缓存范围：all 或 selective |
| `maven-artifact-ids` | 否 | `''` | 逗号分隔的 Maven artifact ID，仅 selective 模式使用 |

## Outputs

| 输出 | 说明 |
|------|------|
| `java-home` | JDK 安装目录 |
| `java-version` | 实际安装的 JDK 版本 |
| `cache-hit` | 是否命中 JDK 缓存 |
| `cache-enabled` | 是否启用缓存 |
| `cache-path` | JDK 缓存路径 |
| `install-path` | 安装路径 |
| `download-source` | 下载来源（cache / obs / api） |
| `version-source` | 版本来源（explicit / version-file） |
| `maven-home` | Maven 安装目录（未指定 maven-version 时为空） |
| `maven-version` | 实际安装的 Maven 版本（未指定 maven-version 时为空） |
| `maven-cache-hit` | 是否命中 Maven 缓存 |

## 版本文件

支持以下版本文件格式：

- `.java-version`：内容为版本号，如 `17.0.18+8` 或 `17`
- `.tool-versions`：标准 asdf 格式，如 `java 17.0.18+8`

## 支持版本

### JDK (Temurin)

| 主版本 | 最新小版本 | 说明 |
|--------|-----------|------|
| 8 | 8.0.482+8 | LTS |
| 11 | 11.0.30+7 | LTS |
| 17 | 17.0.18+8 | LTS，常用稳定版 |
| 21 | 21.0.10+7 | LTS，推荐 |
| 25 | 25.0.2+10 | 最新 LTS |

> 支持精确版本（如 `17.0.18+8`）和系列版本（如 `17`，自动解析到最新小版本）。

### Maven

| 主版本 | 最新小版本 | 说明 |
|--------|-----------|------|
| 3.8.x | 3.8.9 | 常用稳定版 |
| 3.9.x | 3.9.15 | 最新稳定版 |

> 指定 `maven-download-url` 可使用自定义下载地址。

## 构建

```bash
npm run all    # sync-version + tsc + ncc + zip
```


---

## 22. SetupGradle

- **name**: `setup-gradle`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.3.2

# setup-gradle

> **版本：1.3.2**

在流水线中安装并缓存 Gradle，支持版本文件自动检测和自定义下载源。

## 特性

- 指定版本或从 `gradle-wrapper.properties` 自动读取
- 自定义镜像源站下载（华为云镜像等）
- 安装缓存，重复构建跳过下载
- 自动设置 `GRADLE_HOME` 和 `PATH`

## 目录

- [Usage](#usage)
  - [基础用法](#基础用法)
  - [指定下载地址](#指定下载地址)
  - [从 gradle-wrapper.properties 读取版本](#从-gradle-wrapperproperties-读取版本)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [支持版本](#支持版本)

## Usage

### 基础用法

```yaml
name: setup-gradle
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建
        select: selected_by_default
        needs: []
        steps:
          - name: setup-gradle
            uses: setup-gradle
            with:
              gradle-version: '8.10.2'
          - name: Verify
            run: |-
              gradle --version
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 指定下载地址

指定 `download-url` 时优先使用自定义下载源（如华为云镜像）：

```yaml
- name: setup-gradle
  uses: setup-gradle
  with:
    gradle-version: '8.10.2'
    download-url: 'https://mirrors.huaweicloud.com/gradle/gradle-8.10.2-bin.zip'
```

`download-url` 支持 `${version}` 占位符：

```yaml
- name: setup-gradle
  uses: setup-gradle
  with:
    gradle-version: '8.5'
    download-url: 'https://mirrors.huaweicloud.com/gradle/gradle-${version}-bin.zip'
```

### 从 gradle-wrapper.properties 读取版本

项目已包含 `gradle-wrapper.properties` 时，无需手动填写版本号：

```yaml
- name: setup-gradle
  uses: setup-gradle
  with:
    gradle-version-file: 'gradle/wrapper/gradle-wrapper.properties'
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| gradle-version | 否 | — | Gradle 版本，如 `8.10.2` 或 `8.5`（系列版本自动解析最新小版本） |
| gradle-version-file | 否 | — | 版本文件路径，支持 `gradle-wrapper.properties` 或纯版本号文件 |
| download-url | 否 | — | Gradle 发行版直链地址。支持 `${version}` 占位符 |
| enable-cache | 否 | true | 启用安装缓存，命中时跳过下载 |
| custom-install-path | 否 | — | 自定义 Gradle 安装/下载目录，优先级最高。用于规避默认缓存目录权限问题（EACCES） |
| set-env | 否 | true | 设置 GRADLE_HOME 和 PATH |
| gradle-user-home | 否 | — | 自定义 Gradle User Home 路径 |
| dl-timeout-mins | 否 | 30 | 下载超时（分钟） |
| dl-max-retries | 否 | 3 | 最大下载重试次数 |
| verbose | 否 | true | 详细日志 |

## Outputs

| 输出 | 说明 |
|------|------|
| gradle-home | Gradle 安装目录 |
| gradle-version | 实际安装版本 |
| gradle-user-home | Gradle User Home 路径 |
| cache-hit | 是否命中缓存 |
| cache-enabled | 缓存是否启用 |
| download-source | 下载来源 |
| version-source | 版本来源（input / version-file / auto-detect） |

## 支持版本

| 主版本 | 说明 |
|--------|------|
| 7.x | 稳定版 |
| 8.x | 最新稳定版，推荐 |

> **系列版本**：输入 `8.5` 会自动解析到该系列最新小版本。
> **版本文件**：支持从 `gradle-wrapper.properties` 自动读取版本号。


---

## 23. SetupGo

- **name**: `setup-go`
- **creator**: wukong_admin
- **被引用**: 30
- **版本**: 2.0.2

# setup-go

## 目录

[TOC]

## 概述

​	`setup-go` 用于在 CodeArts Pipeline 中安装并配置指定版本的 go。插件会通过 CodeArts 构建工具接口查询可用的 go 预构建包，按当前运行的系统、发行版版本和 CPU 架构选择匹配包；

​	1.支持版本号，范围

​	2.支持从.go-version文件读取版本号

## Usage

### 1.精确安装：安装 go 1.23

以下是一个最简的 GitHub Actions workflow 示例，它使用 `actions/setup-go` 安装 go，并打印版本号验证安装

1.创建流水线，再流水线的.**gitcode/workflows/xxxxx.yml**里面输入如下内容：

```yaml
# .gitcode/workflows/test.yml
name: go
on:
  push:
    branches: [ "main"]
  workflow_dispatch:

stages:
  stage1:
    name: 阶段_1
    select: selected_by_default
    jobs:
      JOB_WJKHX:
        name: 执行shell
        select: selected_by_default
        needs: []
        steps:
        # 1.安装 （只需指定版本）
          - name: setup-go
            uses: setup-go
            with: 
             version: 1.23
          # 2.验证安装
          - name: Go version
            run: go version           
        if: "${{ default() }}"
        runs-on:
        - default
    pre:
    - type: auto
```

核心yaml，上述完整代码的steps一部分，在这里面更改version可已更改下载go的版本

```yaml
        steps:
          - name: setup-go
            uses: setup-go
            with: 
             version: 1.23
```

##### 注：uses必须和插件名字相同，不需要在后面追加版本号

### 2.从 .go-version 文件读取版本

```yaml
# .gitcode/workflows/test.yml
name: go
on:
  push:
    branches: [ "main"]
  workflow_dispatch:

stages:
  stage1:
    name: 阶段_1
    select: selected_by_default
    jobs:
      JOB_WJKHX:
        name: 执行shell
        select: selected_by_default
        needs: []
        steps:
        # 1.安装 （只需指定版本）
          - name: setup-go
            uses: setup-go
            with: 
             version-file:'.go-version'
          # 2.验证安装
          - name: Go version
            run: go version           
        if: "${{ default() }}"
        runs-on:
        - default
    pre:
    - type: auto
```



## Inputs

| 参数           | 必填 | 默认值     | 说明                                            |
| -------------- | ---- | ---------- | ----------------------------------------------- |
| `version`      | 否   | `''`       | 目标 Go 版本或版本范围，如 1.21、1.21.3、>=1.20 |
| `version-file` | 否   | `''`       | 版本文件路径，支持 go.mod、.go-version          |
| `tool-cache`   | 否   | `'true'`   | 是否启用本地工具缓存                            |
| `dep-cache`    | 否   | `'true'`   | 是否输出依赖缓存元信息                          |
| `arch`         | 否   | `''`       | 目标架构，支持 x64、x86、arm64                  |
| `latest`       | 否   | `'false'`  | 是否强制使用最新稳定版                          |
| `cache`        | 否   | `'true'`   | 兼容字段，语义等价于 `dep-cache`                |
| `cache-path`   | 否   | `''`       | 自定义依赖缓存路径                              |
| `cache-scope`  | 否   | `'branch'` | 缓存隔离范围，支持 `branch` 或 `repo`           |
| `update-env`   | 否   | `'true'`   | 是否更新 PATH 和 Go 相关环境变量                |

## Outputs

| 参数             | 说明                                                |
| ---------------- | --------------------------------------------------- |
| `version`        | 实际安装的 Go 精确版本号                            |
| `go-path`        | Go 可执行文件的完整绝对路径                         |
| `tool-home`      | Go 安装目录（GOROOT）                               |
| `tool-bin`       | Go bin 目录路径                                     |
| `tool-cache-hit` | 是否命中本地工具缓存                                |
| `cache-key`      | 依赖缓存键，供通用 cache 插件使用                   |
| `cache-paths`    | 依赖缓存路径列表，供通用 cache 插件使用，按换行分隔 |

---

## 24. PytestReport

- **name**: `pytest-report`
- **creator**: wukong_admin
- **被引用**: 15
- **版本**: 1.0.0

# pytest-report

解析 pytest JUnit XML 测试结果，自动生成 Markdown 格式测试报告并输出到 `ATOMGIT_STEP_SUMMARY`，同时提供标准化的测试结果输出变量供流水线后续步骤使用。

- **自动执行测试**：支持由插件直接运行 pytest 命令，无需额外步骤
- **JUnit XML 解析**：自动解析 pytest 生成的 JUnit XML 格式结果文件
- **Markdown 报告**：生成包含测试概览、结果统计、失败用例详情的可读报告
- **支持 Glob 路径**：支持通配符匹配多个 XML 结果文件
- **灵活的工作目录**：可指定测试执行和结果查找的工作目录
- **失败控制**：可选择是否将测试失败标记为步骤失败
- **用例过滤**：支持列出全部用例、仅失败用例或不列出用例
- **标准输出**：提供结论、通过数、失败数、跳过数等标准化输出变量

---

## 快速开始

### 流水线配置示例

```yaml
 -
    name: pytest-report
    uses: pytest-report
    identifier: pytest
    with:
      # （必填）pytest JUnit XML 测试结果文件路径，支持 glob 通配符
      path: "report.xml"
      # （可选）是否由插件执行 pytest 命令，false 表示只解析已有 XML 文件
      run-tests: "true"
      # （可选）run-tests 为 true 时执行的测试命令
       test-command: "pip install --break-system-packages -r requirements.txt && pytest tests/ --junitxml=report.xml -v"
      # （可选）执行 pytest 命令和查找结果文件的工作目录
      working-directory: "./test"
      # （可选）存在失败用例时是否将步骤标记为失败
      fail-on-error: "false"
      # （可选）未找到测试结果文件时是否将步骤标记为失败
      fail-on-empty: "true"
      # （可选）列出哪些测试用例：all（全部）、failed（仅失败）、none（不列出）
      list-tests: "failed"
      # （可选）是否启用详细输出模式
      verbose: "true"

    if: "${{ default() }}"
    runs-on: ["codearts-hosted", "ubuntu-latest", "x64", "large"]
```

### 完整示例

```yaml
name: pytest-report

on:
  push:
    branches: [ "main" ]
  workflow_dispatch:

stages:
  stage1:
    name: 阶段_1
    select: selected_by_default
    jobs:
      JOB_PYTEST:
        name: 执行pytest测试
        select: selected_by_default
        needs: []
        steps:

          - 
            name: checkout
            uses: checkout
            with:
               repository: ********
               ref: master
               token: *****
               path: "test"

          -
            name: setup-python
            uses: setup-python
            with: 
             python-version: 3.12
             architecture: 'x64'

          - 
            name: install-dependencies
            run: |
              cd test
              pip install --break-system-packages -r requirements.txt

          - 
            name: pytest-report
            uses: pytest-report
            identifier: pytest
            with:
             path: "report.xml"
             run-tests: "true"
             test-command: "pip install --break-system-packages -r requirements.txt && pytest tests/ --junitxml=report.xml -v"
             working-directory: "./test"
             fail-on-error: "false"
             fail-on-empty: "true"
             list-tests: "failed"
             verbose: "true"

          - 
            name: check-report
            run: |
              echo "=== 从 GITHUB_WORKSPACE 读取报告 ==="
              echo "工作目录: $GITHUB_WORKSPACE"

              # 检查多个可能的位置
              for path in "$GITHUB_WORKSPACE/test-report.md" "test-report.md" "./test/test-report.md"; do
                if [ -f "$path" ]; then
                  echo "找到报告: $path"
                  cat "$path"
                  found=1
                  break
                fi
              done

              if [ -z "$found" ]; then
                echo "未找到报告文件"
                echo "尝试搜索..."
                find /home -name "test-report.md" -type f 2>/dev/null | head -5
              fi

        if: "${{ default() }}"
        runs-on: ["codearts-hosted", "ubuntu-latest", "x64", "large"]
    pre:
    - type: auto
```
---

### 后续步骤读取报告

```yaml
 -
    name: check-report
    run: |
      echo "测试结论: ${{ steps.pytest.outputs.conclusion }}"
      echo "通过: ${{ steps.pytest.outputs.passed }}"
      echo "失败: ${{ steps.pytest.outputs.failed }}"
      echo "跳过: ${{ steps.pytest.outputs.skipped }}"
      echo "=== 报告内容 ==="
      cat "${{ steps.pytest.outputs.summary_file }}"
```

---

## 参数说明

| 参数名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `path` | **是**（当 `run-tests=false` 时） | - | pytest JUnit XML 测试结果文件路径，支持 glob 通配符，如 `report.xml` 或 `**/report-*.xml` |
| `run-tests` | 否 | `false` | 是否由插件执行 pytest 命令。`true` 时插件先运行测试再解析结果；`false` 时仅解析已有 XML 文件 |
| `test-command` | 否 | `pytest --junitxml=report.xml` | `run-tests` 为 `true` 时执行的 pytest 命令，可按需添加参数如 `-v`、`-k` 等 |
| `working-directory` | 否 | 当前工作目录 | 执行 pytest 命令和查找结果文件的工作目录，相对于流水线工作空间根目录 |
| `fail-on-error` | 否 | `false` | 存在失败测试用例时是否将步骤标记为失败。设为 `true` 时步骤变红；`false` 时仅输出 warning |
| `fail-on-empty` | 否 | `true` | 未找到匹配的 JUnit XML 文件时是否将步骤标记为失败 |
| `list-tests` | 否 | `failed` | 测试报告中列出哪些用例：`all`（全部）、`failed`（仅失败）、`none`（不列出） |
| `verbose` | 否 | `false` | 是否启用详细输出模式，开启后会输出更多执行日志 |

## 输出参数

| 参数名 | 说明 | 示例值 |
|--------|------|--------|
| `conclusion` | 测试总体结论 | `success` / `failure` |
| `passed` | 通过的测试用例数 | `42` |
| `failed` | 失败的测试用例数 | `3` |
| `skipped` | 跳过的测试用例数 | `1` |
| `summary_file` | 生成的 Markdown 报告文件路径 | `/tmp/step_summary_xxx.md` |

---

## 报告内容示例

插件生成的 Markdown 报告包含以下内容：

```markdown
# pytest 测试报告

## 📊 测试概览

| 项目 | 值 |
|------|-----|
| **总体结论** | ❌ 失败 |
| **总用例数** | 69 |
| **通过率** | 88.4% |
| **总耗时** | 31.43s |
| **工作目录** | `./test` |
| **测试命令** | `pytest tests/ --junitxml=report.xml -v` |

### 结果统计

| 状态 | 数量 | 占比 |
|------|------|------|
| ✅ 通过 | 61 | 88.4% |
| ❌ 失败 | 8 | 11.6% |
| ⏭️ 跳过 | 0 | 0.0% |

### 各文件统计

| 文件 | 总数 | 通过 | 失败 | 跳过 | 耗时 |
|------|------|------|------|------|------|
| report.xml | 69 | 61 | 8 | 0 | 31.43s |

## ❌ 失败用例详情

| 测试类 | 用例名 | 错误信息 |
|--------|--------|----------|
| tests.test_python_server.TestSecurityBugs | test_sql_injection_in_users | AssertionError: SQL注入成功... |

---

*报告生成时间: 2026-06-24T07:00:00.000Z*
```


---

## 25. PypiPublish

- **name**: `pypi-publish`
- **creator**: wukong_admin
- **被引用**: 15
- **版本**: 1.0.6

# PyPI-DevTools_pypi-publish 使用示例

这是一个用于华为云流水线的 PyPI 发布插件，专门用于发布 Python 包到官方 PyPI 仓库。

## 功能特性

- 支持发布到官方 PyPI 仓库（upload.pypi.org）和 TestPyPI（test.pypi.org）
- 支持 PyPI 访问令牌认证（推荐使用 `__token__` 用户名）
- 支持用户名/密码认证
- 自动构建 Python 包（使用 `python -m build`）
- 支持跳过已存在版本的发布
- 支持详细输出模式（verbose）

## 华为云流水线配置示例

### 方式1：通过输入参数传递 PyPI 令牌

```yaml
- name: pypi-publish
  uses: pypi-publish@1.0.0
  with:
    package-path: './my-python-package'
    pypi-token: 'pypi-AgEIcHlwaS5vcmcCJGYwZ...'
    test-pypi: 'false'
    skip-existing: 'false'
    verbose: 'true'
```

### 方式2：通过环境变量传递 PyPI 令牌

```yaml
- name: pypi-publish
  uses: pypi-publish@1.0.0
  with:
    package-path: './my-python-package'
    test-pypi: 'false'
  env:
    token: '${{ secrets.PYPI_TOKEN }}'
```

### 方式3：使用用户名和密码认证

```yaml
- name: pypi-publish
  uses: pypi-publish@1.0.0
  with:
    package-path: './my-python-package'
    pypi-username: 'my_username'
    pypi-password: '${{ secrets.PYPI_PASSWORD }}'
    test-pypi: 'false'
```

### 方式4：发布到 TestPyPI（测试仓库）

```yaml
- name: pypi-publish
  uses: pypi-publish@1.0.0
  with:
    package-path: './my-python-package'
    pypi-token: '${{ secrets.TEST_PYPI_TOKEN }}'
    test-pypi: 'true'
    skip-existing: 'true'
```

## 参数说明

### 输入参数

| 参数名 | 描述 | 必需 | 默认值 |
|--------|------|------|--------|
| `package-path` | 要发布的 npm 包路径 | 否 | `.`（当前目录） |
| `npm-token` | npm 访问令牌 | 否（可通过环境变量提供） | `''` |
| `tag` | 发布标签 | 否 | `latest` |
| `access` | 包访问权限 | 否 | `public` |
| `verbose` | 详细输出模式 | 否 | `false` |

### 环境变量

| 环境变量名 | 描述 | 对应输入参数 |
|------------|------|--------------|
| `pypi-token` | PyPI 密码或访问令牌 | `pypi-token` |
| `username` | PyPI 用户名 | `pypi-username` |
| `password` | PyPI 访问令牌 | `pypi-password` |
| `repositoryUrl` | PyPI 仓库地址 | `pypi-repository` |

### 输出参数

| 输出参数名 | 描述 |
|------------|------|
| `success` | 发布是否成功 |
| `package-name` | 发布的包名 |
| `version` | 发布的版本 |
| `registry` | 使用的 registry |

## 完整流水线示例

```yaml
on:
  sources: {}
  concurrency:
    max: 5
    enable: false
    preemption:
      enable: false
      events:
      - mr_id
    exceed-action: IGNORE

stages:
  17761517793640addca29-d0b4-4617-a737-a098a42243fd:
    jobs:
      JOB_eAdsD:
        name: npm-publish-job
        select: selected_by_default
        needs: []
        steps:
        - name: official_checkout
          uses: official_checkout
          with:
            repository: 'https://github.com/your-org/your-repo.git'
            ref: master
            path: ''
            token: your-git-token
            fetch-depth: 1
            submodules: 'false'
            lfs: 'false'
            clean: 'true'
        
        - name: npm-publish
          uses: npm-publish@1.0.0
          with:
            package-path: './my-package'
            tag: 'latest'
            access: 'public'
            verbose: 'true'
          env:
            NPM_TOKEN: '${{ secrets.NPM_TOKEN }}'
        
        if: '${{ default() }}'
        runs-on:
        - default
    pre:
    - type: auto
    name: 发布阶段
    select: selected_by_default
    fail_fast: false
```

## 注意事项

1. **npm 访问令牌**：你需要一个有效的 npm 访问令牌。可以在 npm 官网生成：
   - 登录 npmjs.com
   - 点击头像 → Access Tokens
   - 生成新的令牌（建议选择 "Publish" 权限）

2. **包权限**：
   - `public`：公开包，任何人都可以安装
   - `restricted`：私有包，需要付费 npm 账户

3. **发布标签**：
   - `latest`：默认标签
   - `beta`、`next`、`alpha`、`rc`：预发布标签
   - 自定义标签：必须符合 npm 标签命名规范

4. **详细输出模式**：
   - 设置为 `true` 时，输出详细的调试信息
   - 用于排查问题

---

## 26. NpmPublish

- **name**: `npm-publish`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.0.6

# Npm-DevTools_npm-publish 使用示例

这是一个用于 gitcode CI/CD 流水线的 npm 发布插件，专门用于发布到官方 npm 仓库。

## 功能特性

- 支持发布到官方 npm 仓库（registry.npmjs.org）
- 支持 npm 访问令牌认证
- 支持自定义发布标签（tag）
- 支持包访问权限设置（public/restricted）
- 支持详细输出模式（verbose）

## gitcode CI/CD 流水线配置示例

### 方式1：通过输入参数传递 npm-token

```yaml
- name: npm-publish
  uses: npm-publish
  with:
    package-path: './my-package'
    npm-token: xxx
    tag: 'latest'
    access: 'public'
    verbose: 'true'
```

### 方式2：通过环境变量传递 npm-token

```yaml
- name: npm-publish
  uses: npm-publish
  with:
    package-path: './my-package'
    tag: 'latest'
    access: 'public'
  env:
    token: '${{ secrets.NPM_TOKEN }}'
```

### 方式3：完全通过环境变量（推荐）

```yaml
- name: npm-publish
  uses: npm-publish
  env:
    token: '${{ secrets.NPM_TOKEN }}'
    NPM_TAG: 'latest'
    NPM_ACCESS: 'public'
    VERBOSE: 'true'
```

## 参数说明

### 输入参数

| 参数名 | 描述 | 必需 | 默认值 |
|--------|------|------|--------|
| `package-path` | 要发布的 npm 包路径 | 否 | `.`（当前目录） |
| `npm-token` | npm 访问令牌 | 否（可通过环境变量提供） | `''` |
| `tag` | 发布标签 | 否 | `latest` |
| `access` | 包访问权限 | 否 | `public` |
| `verbose` | 详细输出模式 | 否 | `false` |

### 环境变量

| 环境变量名 | 描述 | 对应输入参数 |
|------------|------|--------------|
| `token` | npm 访问令牌 | `npm-token` |
| `NPM_TAG` | 发布标签 | `tag` |
| `NPM_ACCESS` | 包访问权限 | `access` |
| `VERBOSE` | 详细输出模式 | `verbose` |

### 输出参数

| 输出参数名 | 描述 |
|------------|------|
| `success` | 发布是否成功 |
| `package-name` | 发布的包名 |
| `version` | 发布的版本 |
| `registry` | 使用的 registry |

## 完整流水线示例

```yaml
on:
  sources: {}
  concurrency:
    max: 5
    enable: false
    preemption:
      enable: false
      events:
      - mr_id
    exceed-action: IGNORE

stages:
  17761517793640addca29-d0b4-4617-a737-a098a42243fd:
    jobs:
      JOB_eAdsD:
        name: npm-publish-job
        select: selected_by_default
        needs: []
        steps:
        - name: checkout
          uses: checkout
          with:
            repository: xxx
            ref: master
            path: ''
            token: xxx
            fetch-depth: 1
            submodules: 'false'
            lfs: 'false'
            clean: 'true'
        
        - name: npm-publish
          uses: npm-publish
          with:
            package-path: './my-package'
            tag: 'latest'
            access: 'public'
            verbose: 'true'
          env:
            token: '${{ secrets.NPM_TOKEN }}'
        
        if: '${{ default() }}'
        runs-on:
        - default
    pre:
    - type: auto
    name: 发布阶段
    select: selected_by_default
    fail_fast: false
```

## 注意事项

1. **npm 访问令牌**：你需要一个有效的 npm 访问令牌。可以在 npm 官网生成：
   - 登录 npmjs.com
   - 点击头像 → Access Tokens
   - 生成新的令牌（建议选择 "Publish" 权限）

2. **包权限**：
   - `public`：公开包，任何人都可以安装
   - `restricted`：私有包，需要付费 npm 账户

3. **发布标签**：
   - `latest`：默认标签
   - `beta`、`next`、`alpha`、`rc`：预发布标签
   - 自定义标签：必须符合 npm 标签命名规范

4. **详细输出模式**：
   - 设置为 `true` 时，输出详细的调试信息
   - 用于排查问题

---

## 27. NotifyWecom

- **name**: `notify-wecom`
- **creator**: wukong_admin
- **被引用**: 32
- **版本**: 1.0.0

# notify-wecom

CodeArts 流水线通知插件 — 企业微信（WeCom）消息通知。

## 功能特性

- 支持 5 种消息类型：`text`、`markdown`、`markdown_v2`、`news`（图文）、`raw`（自定义 JSON）
- @提及：按 userid @指定人、按手机号 @指定人
- WeCom markdown 内置颜色自动映射（success→info, failure→warning, cancelled→comment）
- 流水线上下文自动注入（分支、提交、执行人等）
- `{{var}}` 模板变量自定义消息内容
- 指数退避重试 + 超时控制
- 失败策略可选（fail-on-error）
- 统一输出：notify-status / response-code / response-msg

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `webhook` | 是 | - | WeCom 机器人 Webhook URL |
| `mentioned-list` | 否 | `''` | @指定人的 userid，逗号分隔（text 消息生效） |
| `mentioned-mobile-list` | 否 | `''` | @指定人的手机号，逗号分隔（text 消息生效） |
| `msg-type` | 否 | `markdown` | 消息类型：text / markdown / markdown_v2 / news / raw |
| `title` | 否 | `流水线通知` | 通知标题 |
| `status` | 否 | 自动检测 | 流水线状态：success / failure / cancelled |
| `custom-content` | 否 | `''` | 自定义消息内容，支持 `{{var}}` 模板。raw 模式须为合法 JSON。news 模式须为含 articles 数组的 JSON |
| `include-pipeline-info` | 否 | `true` | 是否自动包含流水线信息摘要 |
| `pipeline-url` | 否 | 自动拼接 | 流水线详情页 URL |
| `branch` | 否 | 自动检测 | 覆盖分支名 |
| `commit-id` | 否 | 自动检测 | 覆盖提交 SHA |
| `executor` | 否 | 自动检测 | 覆盖执行人名称 |
| `fail-on-error` | 否 | `false` | 通知失败是否导致流水线失败 |
| `timeout-seconds` | 否 | `10` | HTTP 请求超时（秒） |
| `max-retries` | 否 | `2` | 最大重试次数 |
| `verbose` | 否 | `false` | 是否启用详细日志 |

## 输出参数

| 参数 | 说明 |
|------|------|
| `notify-status` | 通知结果：success 或 failed |
| `response-code` | HTTP 响应状态码 |
| `response-msg` | 业务响应消息 |

## 模板变量

`custom-content` 中可使用以下变量：

| 变量 | 说明 |
|------|------|
| `{{status}}` | 流水线状态 |
| `{{status_emoji}}` | 状态对应的 emoji |
| `{{status_color_wecom}}` | 状态对应的 WeCom 颜色（info/warning/comment） |
| `{{pipeline_id}}` | 流水线 ID |
| `{{branch}}` | 分支名 |
| `{{executor}}` | 执行人 |
| `{{trigger_type}}` | 触发方式 |
| `{{commit_short}}` | 提交短 SHA |
| `{{pipeline_url}}` | 流水线详情页 URL |

## 使用示例

### 基础用法（markdown 消息）

```yaml
- name: notify-wecom
  uses: notify-wecom
  with:
    webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    msg-type: markdown
    title: 'CI 构建通知'
```

### markdown_v2 消息

```yaml
- name: notify-wecom
  uses: notify-wecom
  with:
    webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    msg-type: markdown_v2
    title: '部署完成'
```

### @指定人（text 消息）

```yaml
- name: notify-wecom
  uses: notify-wecom
  with:
    webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    msg-type: text
    mentioned-list: 'zhangsan,lisi'
    mentioned-mobile-list: '13800138000'
```

### 图文消息（news）

```yaml
- name: notify-wecom
  uses: notify-wecom
  with:
    webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    msg-type: news
    title: '版本发布'
    pipeline-url: 'https://example.com/release/123'
```

### 自定义内容

```yaml
- name: notify-wecom
  uses: notify-wecom
  with:
    webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    msg-type: markdown
    custom-content: |
      ### 构建结果 {{status_emoji}}
      > **状态**: <font color="{{status_color_wecom}}">{{status}}</font>
      > **分支**: {{branch}}
      > **提交**: {{commit_short}}
      > **流水线链接**: {{pipeline_url}}
```

### raw 模式（完全自定义 JSON）

```yaml
- name: notify-wecom
  uses: notify-wecom
  with:
    webhook: https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx
    msg-type: raw
    custom-content: '{"msgtype":"image","image":{"base64":"xxx","md5":"xxx"}}'
```

## 构建

```bash
npm install
npm run all    # 编译 + 打包 + zip
```

构建产物：`dist/index.js`（ncc 单文件打包）


---

## 28. NotifyFeishu

- **name**: `notify-feishu`
- **creator**: wukong_admin
- **被引用**: 48
- **版本**: 1.0.0

# notify-feishu

CodeArts 流水线通知插件 — 飞书（Feishu）消息通知。

## 功能特性

- 支持 4 种消息类型：`text`、`post`（富文本）、`interactive`（消息卡片）、`raw`（自定义 JSON）
- 加签安全验证（secret）
- 消息卡片状态颜色自动映射（success→blue, failure→red, cancelled→orange）
- 流水线上下文自动注入（分支、提交、执行人等）
- `{{var}}` 模板变量自定义消息内容
- 指数退避重试 + 超时控制
- 失败策略可选（fail-on-error）
- 统一输出：notify-status / response-code / response-msg

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `webhook` | 是 | - | 飞书机器人 Webhook URL |
| `secret` | 否 | `''` | 签名校验密钥 |
| `msg-type` | 否 | `interactive` | 消息类型：text / post / interactive / raw |
| `title` | 否 | `流水线通知` | 通知标题 |
| `status` | 否 | 自动检测 | 流水线状态：success / failure / cancelled |
| `custom-content` | 否 | `''` | 自定义消息内容，支持 `{{var}}` 模板。raw 模式须为合法 JSON |
| `include-pipeline-info` | 否 | `true` | 是否自动包含流水线信息摘要 |
| `pipeline-url` | 否 | 自动拼接 | 流水线详情页 URL |
| `branch` | 否 | 自动检测 | 覆盖分支名 |
| `commit-id` | 否 | 自动检测 | 覆盖提交 SHA |
| `executor` | 否 | 自动检测 | 覆盖执行人名称 |
| `fail-on-error` | 否 | `false` | 通知失败是否导致流水线失败 |
| `timeout-seconds` | 否 | `10` | HTTP 请求超时（秒） |
| `max-retries` | 否 | `2` | 最大重试次数 |
| `verbose` | 否 | `false` | 是否启用详细日志 |

## 输出参数

| 参数 | 说明 |
|------|------|
| `notify-status` | 通知结果：success 或 failed |
| `response-code` | HTTP 响应状态码 |
| `response-msg` | 业务响应消息 |

## 模板变量

`custom-content` 中可使用以下变量：

| 变量 | 说明 |
|------|------|
| `{{status}}` | 流水线状态 |
| `{{status_emoji}}` | 状态对应的 emoji |
| `{{status_color}}` | 状态对应的飞书卡片颜色（blue/red/orange/grey） |
| `{{pipeline_id}}` | 流水线 ID |
| `{{branch}}` | 分支名 |
| `{{executor}}` | 执行人 |
| `{{trigger_type}}` | 触发方式 |
| `{{commit_short}}` | 提交短 SHA |
| `{{pipeline_url}}` | 流水线详情页 URL |

## 使用示例

### 基础用法（interactive 消息卡片）

```yaml
- name: notify-feishu
  uses: notify-feishu
  with:
    webhook: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
    secret: xxx
    msg-type: interactive
    title: 'CI 构建通知'
```

### 富文本消息（post）

```yaml
- name: notify-feishu
  uses: notify-feishu
  with:
    webhook: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
    msg-type: post
    title: '部署完成'
```

### 自定义内容

```yaml
- name: notify-feishu
  uses: notify-feishu
  with:
    webhook: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
    msg-type: interactive
    custom-content: |
      **构建结果**: {{status}} {{status_emoji}}
      **分支**: {{branch}}
      **提交**: {{commit_short}}
```

### raw 模式（完全自定义 JSON）

```yaml
- name: notify-feishu
  uses: notify-feishu
  with:
    webhook: https://open.feishu.cn/open-apis/bot/v2/hook/xxx
    msg-type: raw
    custom-content: '{"msg_type":"text","content":{"text":"自定义消息"}}'
```

## 构建

```bash
npm install
npm run all    # 编译 + 打包 + zip
```

构建产物：`dist/index.js`（ncc 单文件打包）


---

## 29. JunitReport

- **name**: `junit-report`
- **creator**: wukong_admin
- **被引用**: 48
- **版本**: 1.1.3

# junit-report

解析 JUnit XML 测试结果文件，生成 Markdown 报告并输出到 `ATOMGIT_STEP_SUMMARY`。

支持两种模式：
- **仅解析模式**（默认）：解析已有的 JUnit XML 结果文件
- **执行并解析模式**：先执行测试命令，再解析结果

支持 **失败用例重试机制**：对失败的用例自动重跑，重跑通过的标记为「偶发通过（flaky）」，帮助过滤 CI 环境偶发失败。

## Usage

### 基础用法（仅解析）

```yaml
steps:
  - uses: setup-jdk
  - run: mvn test

  - uses: junit-report
    with:
      path: 'target/surefire-reports/TEST-*.xml'
```

### 执行并解析模式

```yaml
steps:
  - uses: setup-jdk

  - uses: junit-report
    with:
      run-tests: 'true'
      test-command: 'mvn test'
      working-directory: './my-project'
      path: 'target/surefire-reports/TEST-*.xml'
```

### 失败重试模式

```yaml
steps:
  - uses: setup-jdk
  - run: mvn test

  - uses: junit-report
    with:
      path: 'target/surefire-reports/TEST-*.xml'
      test-command: 'mvn test'
      retry-count: '2'
      fail-on-error: 'false'
```

重试流程：
1. 解析首次测试结果，识别失败用例
2. 用 `test-command` + 失败用例过滤参数重跑（Maven 自动加 `-Dtest=Class1,Class2`，Gradle 自动加 `--tests Class1`）
3. 重跑通过的用例标记为 `flaky`（偶发通过），最终结论为 `success`
4. 重跑仍失败的用例保持 `failed`，最终结论为 `failure`

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| path | 否 | — | JUnit XML 测试结果文件路径，支持 glob |
| run-tests | 否 | false | 是否由插件执行测试命令 |
| test-command | 否 | mvn test | 测试执行命令（run-tests=true 时作为首次命令；retry-count>0 时作为重试命令） |
| working-directory | 否 | — | 执行测试命令的工作目录 |
| retry-count | 否 | 0 | 失败用例重试次数（0=不重试） |
| fail-on-error | 否 | true | 存在失败用例时是否中断步骤 |
| fail-on-empty | 否 | true | 未找到结果文件时是否中断步骤 |
| list-tests | 否 | failed | 列出哪些测试用例：all、failed、none |
| verbose | 否 | false | 详细日志输出 |

## Outputs

| 输出 | 说明 |
|------|------|
| conclusion | 最终结论：success 或 failure |
| passed | 通过的测试用例数 |
| failed | 失败的测试用例数 |
| skipped | 跳过的测试用例数 |
| flaky | 重试后通过的偶发失败用例数 |
| summary_file | 生成的测试报告 Markdown 文件路径 |

## 支持的 JUnit XML 格式

- Maven Surefire（`target/surefire-reports/TEST-*.xml`）
- Gradle（`build/test-results/test/TEST-*.xml`）

## 报告示例

### 无重试，有失败

```markdown
## 测试结果: ❌ 失败 (共 300 个用例)

| 状态 | 数量 |
|------|------|
| ✅ 通过 | 298 |
| ❌ 失败 | 2 |
| ⏭️ 跳过 | 5 |

### 失败用例
| 测试类 | 用例名 | 状态 | 错误信息 |
|--------|--------|------|----------|
| LoginTest | testTimeout | ❌ | Connection timeout after 5000ms |
| UploadTest | testLargeFile | ❌ | OutOfMemoryError: Java heap space |
```

### 重试后，偶发通过

```markdown
## 测试结果: ✅ 通过 (共 300 个用例)

| 状态 | 数量 |
|------|------|
| ✅ 通过 | 298 |
| ❌ 失败 | 0 |
| ⏭️ 跳过 | 5 |
| ⚠️ 偶发通过 | 1 |

### 失败用例
| 测试类 | 用例名 | 状态 | 错误信息 |
|--------|--------|------|----------|
| LoginTest | testTimeout | ⚠️ | |
```


---

## 30. NotifyEmail

- **name**: `notify-email`
- **creator**: wukong_admin
- **被引用**: 47
- **版本**: 1.0.0

# notify-email

CodeArts 流水线通知插件 — 邮件通知。

## 功能特性

- 9 种邮箱服务商预设：QQ、163、126、139、Gmail、Outlook、企业QQ（exmail-qq）、阿里云、自定义
- 3 种邮件正文格式：`text`（纯文本）、`html`（HTML）、`markdown`（Markdown 自动转 HTML）
- 内置 Markdown → HTML 转换器（支持标题/加粗/斜体/链接/代码/引用/列表/分割线）
- 精美 HTML 邮件模板（表格布局 + 响应式样式）
- 抄送（CC）/ 密送（BCC）支持
- 流水线上下文自动注入（分支、提交、执行人等）
- `{{var}}` 模板变量自定义邮件内容
- 指数退避重试 + 瞬态错误识别 + 超时控制
- 失败策略可选（fail-on-error）
- 统一输出：notify-status / response-code / response-msg

## 邮箱服务商预设

| 预设名 | SMTP 服务器 | 端口 | SSL |
|--------|------------|------|-----|
| `qq` | smtp.qq.com | 465 | 是 |
| `163` | smtp.163.com | 465 | 是 |
| `126` | smtp.126.com | 465 | 是 |
| `139` | smtp.139.com | 465 | 是 |
| `gmail` | smtp.gmail.com | 465 | 是 |
| `outlook` | smtp-mail.outlook.com | 587 | 否 |
| `exmail-qq` | smtp.exmail.qq.com | 465 | 是 |
| `aliyun` | smtp.aliyun.com | 465 | 是 |
| `custom` | 用户自定义 | - | - |

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `email-provider` | 否 | `custom` | 邮箱服务商预设 |
| `smtp-server` | 否 | `''` | SMTP 服务器地址，使用预设时自动填充 |
| `smtp-port` | 否 | `''` | SMTP 端口，使用预设时自动填充 |
| `smtp-secure` | 否 | `true` | 是否使用 SSL/TLS |
| `smtp-username` | 否 | `''` | SMTP 认证用户名（通常为邮箱地址） |
| `smtp-password` | 否 | `''` | SMTP 认证密码或授权码 |
| `email-from` | 否 | 同 smtp-username | 发件人邮箱地址 |
| `email-to` | 是 | - | 收件人邮箱，逗号分隔 |
| `email-cc` | 否 | `''` | 抄送邮箱，逗号分隔 |
| `email-bcc` | 否 | `''` | 密送邮箱，逗号分隔 |
| `email-body-type` | 否 | `html` | 邮件正文格式：text / html / markdown |
| `title` | 否 | `流水线通知` | 邮件主题 |
| `status` | 否 | 自动检测 | 流水线状态：success / failure / cancelled |
| `custom-content` | 否 | `''` | 自定义邮件内容，支持 `{{var}}` 模板 |
| `include-pipeline-info` | 否 | `true` | 是否自动包含流水线信息摘要 |
| `pipeline-url` | 否 | 自动拼接 | 流水线详情页 URL |
| `branch` | 否 | 自动检测 | 覆盖分支名 |
| `commit-id` | 否 | 自动检测 | 覆盖提交 SHA |
| `executor` | 否 | 自动检测 | 覆盖执行人名称 |
| `fail-on-error` | 否 | `false` | 通知失败是否导致流水线失败 |
| `timeout-seconds` | 否 | `10` | SMTP 连接超时（秒） |
| `max-retries` | 否 | `2` | 最大重试次数 |
| `verbose` | 否 | `false` | 是否启用详细日志 |

## 输出参数

| 参数 | 说明 |
|------|------|
| `notify-status` | 通知结果：success 或 failed |
| `response-code` | SMTP 响应码（成功为 0） |
| `response-msg` | 结果消息 |

## 模板变量

`custom-content` 和 `title` 中可使用以下变量：

| 变量 | 说明 |
|------|------|
| `{{status}}` | 流水线状态 |
| `{{status_emoji}}` | 状态对应的 emoji |
| `{{pipeline_id}}` | 流水线 ID |
| `{{branch}}` | 分支名 |
| `{{executor}}` | 执行人 |
| `{{trigger_type}}` | 触发方式 |
| `{{commit_short}}` | 提交短 SHA |
| `{{pipeline_url}}` | 流水线详情页 URL |

## 使用示例

### QQ 邮箱（零配置）

```yaml
- name: notify-email
  uses: notify-email
  with:
    email-provider: qq
    smtp-username: 'your_email@qq.com'
    smtp-password: 'your_auth_code'
    email-to: 'recipient@example.com'
    title: 'CI 构建通知'
```

### 163 邮箱 + HTML 正文

```yaml
- name: notify-email
  uses: notify-email
  with:
    email-provider: 163
    smtp-username: 'your_email@163.com'
    smtp-password: 'your_auth_code'
    email-to: 'recipient1@example.com,recipient2@example.com'
    email-cc: 'lead@example.com'
    email-body-type: html
    title: '部署完成 {{status_emoji}}'
```

### Markdown 正文

```yaml
- name: notify-email
  uses: notify-email
  with:
    email-provider: qq
    smtp-username: 'your_email@qq.com'
    smtp-password: 'your_auth_code'
    email-to: 'recipient@example.com'
    email-body-type: markdown
    custom-content: |
      ### 构建结果 {{status_emoji}}
      - **状态**: {{status}}
      - **分支**: {{branch}}
      - **提交**: {{commit_short}}
      - [查看详情]({{pipeline_url}})
```

### 自定义 SMTP 服务器

```yaml
- name: notify-email
  uses: notify-email
  with:
    email-provider: custom
    smtp-server: 'smtp.company.com'
    smtp-port: '465'
    smtp-secure: 'true'
    smtp-username: 'sender@company.com'
    smtp-password: 'password'
    email-from: 'CI Bot <sender@company.com>'
    email-to: 'team@company.com'
    email-body-type: text
    title: '流水线通知'
```

## 构建

```bash
npm install
npm run all    # 编译 + 打包 + zip
```

构建产物：`dist/index.js`（ncc 单文件打包）


---

## 31. NotifyDingtalk

- **name**: `notify-dingtalk`
- **creator**: wukong_admin
- **被引用**: 48
- **版本**: 1.0.0

# notify-dingtalk

CodeArts 流水线通知插件 — 钉钉（DingTalk）消息通知。

## 功能特性

- 支持 4 种消息类型：`text`、`markdown`、`actionCard`、`raw`（自定义 JSON）
- 加签安全验证（secret）
- @提及：按手机号 @指定人、@所有人
- 流水线上下文自动注入（分支、提交、执行人等）
- `{{var}}` 模板变量自定义消息内容
- 指数退避重试 + 超时控制
- 失败策略可选（fail-on-error）
- 统一输出：notify-status / response-code / response-msg

## 输入参数

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `webhook` | 是 | - | 钉钉机器人 Webhook URL |
| `secret` | 否 | `''` | 加签密钥 |
| `at-mobiles` | 否 | `''` | @指定人的手机号，逗号分隔 |
| `at-all` | 否 | `false` | 是否 @所有人 |
| `msg-type` | 否 | `markdown` | 消息类型：text / markdown / actionCard / raw |
| `title` | 否 | `流水线通知` | 通知标题 |
| `status` | 否 | 自动检测 | 流水线状态：success / failure / cancelled |
| `custom-content` | 否 | `''` | 自定义消息内容，支持 `{{var}}` 模板。raw 模式须为合法 JSON |
| `include-pipeline-info` | 否 | `true` | 是否自动包含流水线信息摘要 |
| `pipeline-url` | 否 | 自动拼接 | 流水线详情页 URL |
| `branch` | 否 | 自动检测 | 覆盖分支名 |
| `commit-id` | 否 | 自动检测 | 覆盖提交 SHA |
| `executor` | 否 | 自动检测 | 覆盖执行人名称 |
| `action-url` | 否 | `''` | ActionCard 按钮跳转 URL，为空时回退到 pipeline-url |
| `action-title` | 否 | `查看详情` | ActionCard 按钮文字 |
| `fail-on-error` | 否 | `false` | 通知失败是否导致流水线失败 |
| `timeout-seconds` | 否 | `10` | HTTP 请求超时（秒） |
| `max-retries` | 否 | `2` | 最大重试次数 |
| `verbose` | 否 | `false` | 是否启用详细日志 |

## 输出参数

| 参数 | 说明 |
|------|------|
| `notify-status` | 通知结果：success 或 failed |
| `response-code` | HTTP 响应状态码 |
| `response-msg` | 业务响应消息 |

## 模板变量

`custom-content` 中可使用以下变量：

| 变量 | 说明 |
|------|------|
| `{{status}}` | 流水线状态 |
| `{{status_emoji}}` | 状态对应的 emoji |
| `{{pipeline_id}}` | 流水线 ID |
| `{{branch}}` | 分支名 |
| `{{executor}}` | 执行人 |
| `{{trigger_type}}` | 触发方式 |
| `{{commit_short}}` | 提交短 SHA |
| `{{pipeline_url}}` | 流水线详情页 URL |

## 使用示例

### 基础用法（markdown 消息）

```yaml
- name: notify-dingtalk
  uses: notify-dingtalk
  with:
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxx
    secret: SECxxx
    msg-type: markdown
    title: 'CI 构建通知'
```

### ActionCard 消息

```yaml
- name: notify-dingtalk
  uses: notify-dingtalk
  with:
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxx
    msg-type: actionCard
    title: '部署完成'
    action-title: '查看部署详情'
    action-url: 'https://example.com/deploy/123'
```

### @指定人

```yaml
- name: notify-dingtalk
  uses: notify-dingtalk
  with:
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxx
    at-mobiles: '13800138000,13900139000'
    at-all: false
```

### 自定义内容

```yaml
- name: notify-dingtalk
  uses: notify-dingtalk
  with:
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxx
    msg-type: markdown
    custom-content: |
      ### 构建结果 {{status_emoji}}
      > 分支: {{branch}}
      > 提交: {{commit_short}}
      > [查看详情]({{pipeline_url}})
```

### raw 模式（完全自定义 JSON）

```yaml
- name: notify-dingtalk
  uses: notify-dingtalk
  with:
    webhook: https://oapi.dingtalk.com/robot/send?access_token=xxx
    msg-type: raw
    custom-content: '{"msgtype":"link","link":{"title":"标题","text":"内容","messageUrl":"https://example.com"}}'
```

## 构建

```bash
npm install
npm run all    # 编译 + 打包 + zip
```

构建产物：`dist/index.js`（ncc 单文件打包）


---

## 32. GitAutoCommit

- **name**: `git-auto-commit`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.0.2

# Git自动提交插件

华为云流水线插件，用于自动检测代码变更、提交并推送到远程仓库。

## 功能特性

- 自动检测Git仓库中的代码变更
- 支持自定义提交信息和提交者信息
- 支持文件匹配模式（通配符）
- 支持指定目标分支
- 支持跳过空提交（没有变更时）
- 支持创建Git标签
- 支持多种认证方式（HTTP/SSH）
- 支持华为云CI/CD环境变量
- 支持代码自动格式化（基于Prettier）

## 华为云流水线配置示例

### 基本使用示例

```yaml
- name: git-auto-commit
  uses: git-auto-commit@1.0.0
  with:
    commit_message: "自动提交：流水线构建结果"
    commit_user_name: "流水线机器人"
    commit_user_email: "pipeline@example.com"
    file_pattern: "*.js *.ts *.json"
    skip_empty: true
```

### 完整配置示例

```yaml
- name: git-auto-commit
  uses: git-auto-commit@1.0.0
  with:
    commit_message: "发布版本 v1.0.0"
    commit_user_name: "发布机器人"
    commit_user_email: "release@company.com"
    file_pattern: "*"
    branch: "main"
    skip_empty: false
    tag_name: "v1.0.0"
    access_token: "${{ secrets.GIT_TOKEN }}"
```

### 通过环境变量传递令牌

```yaml
- name: git-auto-commit
  uses: git-auto-commit@1.0.0
  with:
    commit_message: "自动提交变更"
  env:
    CI_COMMIT_TOKEN: "${{ secrets.CI_COMMIT_TOKEN }}"
```

## 参数说明

### 输入参数

| 参数名 | 类型 | 必需 | 默认值 | 描述 |
|--------|------|------|--------|------|
| `commit_message` | string | 否 | "Apply automatic changes" | 提交信息 |
| `commit_user_name` | string | 否 | "流水线机器人" | 提交者用户名 |
| `commit_user_email` | string | 否 | "pipeline-robot@huaweicloud.com" | 提交者邮箱 |
| `file_pattern` | string | 否 | "*" | 文件匹配模式，支持通配符 |
| `branch` | string | 否 | "" | 目标分支，为空时使用当前分支 |
| `skip_empty` | boolean | 否 | false | 是否跳过空提交（没有变更时） |
| `tag_name` | string | 否 | "" | 标签名称，为空时不创建标签 |
| `access_token` | string | 否 | "" | Git访问令牌，用于推送代码 |
| `format_code` | boolean | 否 | false | 是否自动格式化代码（调用prettier） |
| `format_exclude_extensions` | string | 否 | "[]" | 格式化排除的后缀，JSON数组字符串 |
| `format_prettier_config` | string | 否 | "" | Prettier配置文件路径 |

### 环境变量

插件支持以下环境变量作为访问令牌的备选来源：

| 环境变量名 | 描述 | 优先级 |
|------------|------|--------|
| `CI_COMMIT_TOKEN` | 华为云CI提交令牌 | 1 |
| `GIT_TOKEN` | Git访问令牌 | 2 |
| `ACCESS_TOKEN` | 通用访问令牌 | 3 |
| `CI_JOB_TOKEN` | 华为云CI作业令牌 | 4 |
| `CI_PROJECT_TOKEN` | 华为云CI项目令牌 | 5 |
| `CI_REGISTRY_TOKEN` | 华为云CI注册表令牌 | 6 |

**注意**：环境变量的优先级低于 `access_token` 输入参数。

### 输出参数

| 输出参数名 | 类型 | 描述 |
|------------|------|------|
| `success` | boolean | 操作是否成功 |
| `has_changes` | boolean | 是否有代码变更 |
| `commit_hash` | string | 提交哈希值 |
| `tag_created` | boolean | 是否创建了标签 |

## 使用场景

### 场景1：自动提交构建产物

```yaml
- name: 构建项目
  run: npm run build
  
- name: 自动提交构建产物
  uses: git-auto-commit@1.0.0
  with:
    commit_message: "更新构建产物"
    file_pattern: "dist/**"
    skip_empty: true
```

### 场景2：版本发布

```yaml
- name: 更新版本号
  run: npm version patch
  
- name: 提交并打标签
  uses: git-auto-commit@1.0.0
  with:
    commit_message: "发布新版本"
    tag_name: "${{ env.NEW_VERSION }}"
    access_token: "${{ secrets.GIT_TOKEN }}"
```

### 场景3：文档更新

```yaml
- name: 生成文档
  run: npm run docs
  
- name: 提交文档更新
  uses: git-auto-commit@1.0.0
  with:
    commit_message: "更新文档"
    file_pattern: "docs/** *.md"
    skip_empty: true
```

## 认证方式

### HTTP认证
- 使用访问令牌：`https://oauth2:YOUR_TOKEN@github.com/username/repo.git`
- 支持华为云CI/CD环境变量

### SSH认证
- 使用SSH密钥：`git@github.com:username/repo.git`
- 需要在流水线中配置SSH密钥

## 错误处理

插件会处理以下常见错误：

1. **Git未安装**：提示用户安装Git并添加到PATH
2. **非Git仓库**：提示当前目录不是Git仓库
3. **认证失败**：提示检查访问令牌或SSH密钥
4. **网络错误**：提示检查网络连接
5. **无变更跳过**：当 `skip_empty=true` 且无变更时，正常退出

## 开发说明

### 项目结构
```
src/
├── framework/          # 框架层
│   ├── logger.ts      # 日志工具
│   └── git-helper.ts  # Git操作工具
├── plugin/            # 插件层
│   └── git-auto-committer.ts  # 核心业务逻辑
├── types.ts           # 类型定义
├── constants.ts       # 常量定义
├── inputs.ts          # 输入参数处理
├── outputs.ts         # 输出参数处理
└── main.ts           # 入口文件
```

### 构建命令
```bash
# 安装依赖
npm install

# 构建插件
npm run build

# 清理构建产物
npm run clean

# 代码检查
npm run lint

# 代码格式化
npm run format
```

### 技术栈
- TypeScript 5.x
- @actions/core - 华为云插件核心库
- @actions/exec - 命令执行工具
- @vercel/ncc - 代码打包工具

## 许可证

MIT License

## 支持与反馈

如有问题或建议，请通过以下方式联系：
- GitHub Issues: https://github.com/huaweicloud/git-auto-commit-action/issues
- 华为云技术支持

---

## 33. DockerMetadata

- **name**: `docker-metadata`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.3.5

# docker-metadata

生成 Docker 镜像标签和 OCI 标注，纯计算不涉及下载。

- 7 种标签模板：semver / match / edge / ref / raw / sha / schedule
- 多镜像名、自定义 OCI labels、flavor 前缀/后缀/latest 控制
- 全局表达式（`{{branch}}`、`{{sha}}`、`{{tag}}` 等）
- override 参数覆盖 Git 上下文，适配手动触发等无代码源场景
- images 为空时降级输出，不阻塞流水线

## 目录

- [Usage](#usage)
  - [基础用法：SHA 标签](#基础用法sha-标签)
  - [分支引用标签](#分支引用标签)
  - [semver 标签](#semver-标签)
  - [多镜像 + 自定义 labels](#多镜像--自定义-labels)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [标签模板语法](#标签模板语法)
  - [type=schedule](#typeschedule)
  - [type=semver](#typesemver)
  - [type=match](#typematch)
  - [type=edge](#typeedge)
  - [type=ref](#typeref)
  - [type=raw](#typeraw)
  - [type=sha](#typesha)
  - [默认标签规则](#默认标签规则)
  - [flavor 配置](#flavor-配置)
  - [全局表达式](#全局表达式)
  - [Tag 清洗规则](#tag-清洗规则)

## Usage

### 基础用法：SHA 标签

最简配置，为每次提交生成 SHA 标签。

```yaml
name: docker-metadata
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建
        select: selected_by_default
        needs: []
        steps:
          - name: docker-metadata
            uses: docker-metadata
            with:
              images: 'ghcr.io/myteam/myapp'
              tags: type=sha
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 分支引用标签

根据当前分支名生成标签，适合持续集成场景。分支名中的 `/` 自动替换为 `-`（如 `feat/new-feature` 变为 `feat-new-feature`）。

```yaml
name: docker-metadata
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建
        select: selected_by_default
        needs: []
        steps:
          - name: docker-metadata
            uses: docker-metadata
            with:
              images: 'ghcr.io/myteam/myapp'
              tags: |
                type=ref,event=branch
                type=sha
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### semver 标签

当 Git 标签为 semver 格式（如 `v1.2.3`）时，自动解析版本号并生成多级标签。

```yaml
name: docker-metadata
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 发布
    select: selected_by_default
    jobs:
      JOB_RELEASE:
        name: 发布
        select: selected_by_default
        needs: []
        steps:
          - name: docker-metadata
            uses: docker-metadata
            with:
              images: 'ghcr.io/myteam/myapp'
              tags: |
                type=semver,pattern={{version}}
                type=semver,pattern={{major}}.{{minor}}
                type=semver,pattern={{major}}
              flavor: latest=true
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

标签 `v1.2.3` 将生成：`1.2.3`、`1.2`、`1`、`latest`。

预发布版本（含 `beta`/`rc`/`alpha`）仅扩展 `{{version}}`，不生成 `{{major}}`/`{{minor}}`/`{{patch}}` 和 `latest`。

### 多镜像 + 自定义 labels

同时推送到多个仓库，并添加自定义 OCI 标注。

```yaml
name: docker-metadata
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 发布
    select: selected_by_default
    jobs:
      JOB_RELEASE:
        name: 发布
        select: selected_by_default
        needs: []
        steps:
          - name: docker-metadata
            uses: docker-metadata
            with:
              images: |
                myteam/myapp
                ghcr.io/myteam/myapp
              tags: |
                type=semver,pattern={{version}}
                type=sha
              labels: |
                org.opencontainers.image.vendor=myteam
                org.opencontainers.image.licenses=MIT
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| images | 否 | '' | Docker 镜像名，换行或逗号分隔（如 `ghcr.io/user/app`）。空值触发降级输出，仅生成 tag 名称 |
| tags | 否 | '' | 标签模板，换行分隔（如 `type=sha`、`type=ref,event=branch`）。为空时使用默认规则 |
| flavor | 否 | '' | 前缀/后缀/latest 等配置（如 `latest=true`、`prefix=v`、`suffix=-alpine`） |
| labels | 否 | '' | 自定义 OCI 标注，换行或逗号分隔（如 `org.opencontainers.image.vendor=MyCorp`） |
| sep-tags | 否 | 换行 | tags 输出的分隔符 |
| sep-labels | 否 | 换行 | labels 输出的分隔符 |
| override-branch | 否 | '' | 覆盖分支名，手动触发或需要显式指定时使用 |
| override-sha | 否 | '' | 覆盖 Commit SHA，手动触发或需要显式指定时使用 |
| override-tag | 否 | '' | 覆盖 Git Tag 名 |
| override-pr | 否 | '' | 覆盖 PR 编号 |
| default-branch | 否 | '' | 默认分支名（用于 isDefaultBranch 检测和 type=edge 条件），未设置时默认为 main |

## Outputs

| 输出 | 说明 |
|------|------|
| version | 生成的版本号（最高优先级 tag 值，不含镜像名前缀） |
| tags | 完整标签列表（含镜像名前缀，如 `ghcr.io/user/app:1.2.3`） |
| tag-names | 不含镜像名前缀的标签名（如 `1.2.3`） |
| labels | OCI 标注列表（`key=value` 格式） |
| json | 全部元数据 JSON，包含 version / tags / tagNames / labels / images / timestamp |

## 标签模板语法

标签模板通过 `tags` 输入配置，每行一条规则，格式为 `type=xxx,key=value,...`。规则按优先级从高到低排序，`version` 输出取最高优先级的 tag 值。

### type=schedule

优先级 1000。仅在定时触发事件时激活，支持日期模板。

| pattern | 输出 |
|---------|------|
| `nightly` | `nightly` |
| `{{date 'YYYYMMDD'}}` | `20260415` |

```yaml
tags: |
  type=schedule,pattern=nightly
  type=schedule,pattern={{date 'YYYYMMDD'}}
```

### type=semver

优先级 900。从 Git 标签解析 semver 版本号，仅在 tag 事件时激活。

| Git 标签 | pattern | 输出 |
|----------|---------|------|
| `v1.2.3` | `{{version}}` | `1.2.3` |
| `v1.2.3` | `{{major}}.{{minor}}` | `1.2` |
| `v1.2.3` | `v{{major}}` | `v1` |
| `v2.0.8-beta.67` | `{{version}}` | `2.0.8-beta.67` |

预发布版本（含 `rc`/`beta`/`alpha`）仅扩展 `{{version}}`，不生成 `{{major}}`/`{{minor}}`/`{{patch}}` 标签，也不生成 `latest`。

```yaml
tags: |
  type=semver,pattern={{version}}
  type=semver,pattern={{major}}.{{minor}}
  type=semver,pattern={{major}}
```

### type=match

优先级 800。对 Git 标签执行正则匹配，提取捕获组内容。

| Git 标签 | pattern | group | 输出 |
|----------|---------|-------|------|
| `v1.2.3` | `\d+\.\d+\.\d+` | `0` | `1.2.3` |
| `release-v2.0` | `release-v(\d+\.\d+)` | `1` | `2.0` |

```yaml
tags: |
  type=match,pattern=\d+\.\d+\.\d+,group=0
  type=match,pattern=release-v(\d+\.\d+\.\d+),group=1
```

### type=edge

优先级 700。反映默认分支最新提交的标签，仅在当前分支为默认分支时生效。

默认分支判断优先级：`default-branch` 输入 > 平台环境变量 > `main`。

| 配置 | 条件 | 输出 |
|------|------|------|
| 默认 | 当前分支 == 默认分支 | `edge` |
| `branch=main` | 当前分支 == `main` | `edge` |
| 任意 | 当前分支 != 默认分支 | 不生成 |

```yaml
tags: |
  type=edge
  type=edge,branch=main
```

### type=ref

优先级 600。根据 Git 引用类型生成标签。

| 事件 | 引用 | 输出 |
|------|------|------|
| push（分支） | `refs/heads/main` | `main` |
| push（含斜杠分支） | `refs/heads/feat/new-feature` | `feat-new-feature` |
| push（标签） | `refs/tags/v1.2.3` | `v1.2.3` |
| PR | `refs/pull/42/merge` | `pr-42` |

分支名中的 `/` 自动替换为 `-`。

```yaml
tags: |
  type=ref,event=branch
  type=ref,event=tag
  type=ref,event=pr
```

### type=raw

优先级 200。输出自定义标签值，支持全局表达式扩展。

| value | 输出 |
|-------|------|
| `stable` | `stable` |
| `{{branch}}-snapshot` | `main-snapshot` |

```yaml
tags: |
  type=raw,value=stable,enable={{is_default_branch}}
  type=raw,value={{branch}}-snapshot
```

### type=sha

优先级 100。输出 Git 提交 SHA 标签。

| format | 输出 |
|--------|------|
| `short`（默认） | `sha-860c190` |
| `long` | `sha-860c1907a5d5c5e9b3f2a1c4d7e8f9a0b1c2d3e4` |

```yaml
tags: |
  type=sha
  type=sha,format=long
```

### 默认标签规则

当 `tags` 输入为空时，使用以下默认规则：

```yaml
tags: |
  type=schedule
  type=ref,event=branch
  type=ref,event=tag
  type=ref,event=pr
```

### flavor 配置

通过 `flavor` 输入控制标签的前缀、后缀和 latest 行为。

| 属性 | 默认值 | 说明 |
|------|--------|------|
| `latest` | `auto` | `true` 强制添加 latest，`false` 禁用，`auto` 仅 semver 正式版添加 |
| `prefix` | `''` | 为所有标签添加前缀 |
| `suffix` | `''` | 为所有标签添加后缀 |
| `onlatest` | `true` | 前缀/后缀是否应用于 latest 标签 |

```yaml
flavor: |
  latest=true
  prefix=v
  suffix=-alpine
```

### 全局表达式

在标签模板的 `prefix`、`suffix`、`value`、`enable` 属性以及 `labels` 中可使用以下表达式：

| 表达式 | 说明 |
|--------|------|
| `{{branch}}` | 触发流水线的分支名 |
| `{{tag}}` | 触发流水线的标签名 |
| `{{sha}}` | 短提交 SHA |
| `{{base_ref}}` | PR 的目标分支 |
| `{{is_default_branch}}` | 是否为默认分支（`true`/`false`） |
| `{{is_not_default_branch}}` | 是否非默认分支 |
| `{{date 'FORMAT'}}` | 当前日期（moment 格式） |

### Tag 清洗规则

生成的 tag 值自动清洗以符合 Docker tag 命名规范：

- 所有字符转为小写
- 非法字符（非 `[a-zA-Z0-9._-]`）替换为 `-`
- 连续 `-` 合并为单个
- 去除首尾的 `.` 和 `-`


---

## 34. CodeqlAction

- **name**: `codeql-action`
- **creator**: wukong_admin
- **被引用**: 312
- **版本**: 1.1.0

# codeql-action

安装并配置 CodeQL 安全扫描引擎，对源代码进行安全漏洞扫描与分析，一个步骤完成代码安全检测。

- **多语言支持**：支持 9 种编程语言的安全扫描
- **三种构建模式**：`none` 静态分析、`autobuild` 自动构建、`manual` 手动构建命令，适配不同项目场景
- **查询套件选择**：支持三个级别的安全查询套件，可多选组合
- **自动下载**：自动从 OBS 获取并缓存指定版本的 CodeQL CLI
- **多级缓存**：支持持久缓存、临时缓存、本地 bundle 三级缓存机制
- **优雅降级**：编译型语言在缺少构建工具时自动降级为 `--build-mode=none`
- **自定义配置文件**：支持 GitHub `codeql-config.yml` 格式，可指定 paths/paths-ignore/queries/packs/query-filters 等
- **目录权限提前校验**：在分析开始前检查输出目录权限并自动创建缺失目录，避免长时间分析后因权限不足失败
- **智能路径处理**：`output-path` 指定输出目录（多语言时生成 `codeql-results-{lang}.sarif`），`report-path` 可指定完整文件路径或仅指定目录（自动补全文件名）
- **查询失败原因捕获**：分析失败时自动分段输出 stderr 尾部，避免长日志被截断丢失关键错误信息
- **SARIF 输出**：扫描结果以标准 SARIF 格式输出，每语言独立文件
- **Markdown 报告**：自动生成包含严重程度统计、告警详情、数据流路径、修复建议的可读报告
- **三级告警过滤**：支持 `min-severity` 按 note/warning/error 过滤；内置路径过滤排除测试/第三方目录
- **灵活配置**：支持自定义查询、内存限制、线程数、详细日志

接口存在的版本

| 类型       | 版本    | 最新小版本 |
| ---------- | ------- | ---------- |
| `稳定 LTS` | `2.25.4` | `2.25.4`   |

---

## 快速开始

### 流水线配置示例

```yaml
 -
    name: checkout
    uses: checkout
    with:
      repository: https://gitcode.com/xxx/java.git
      ref: master
      token: xxx
      path: "test"
 -
    name: setup-jdk
    uses: setup-jdk
    with:
      jdk-version: 17
      architecture: 'x64'
 -
    name: codeql-action
    uses: codeql-action
    identifier: codeql
    with:
      # （必填）要扫描的编程语言，支持：javascript, python, java, cpp, csharp, go, ruby, swift。多个用逗号分隔
      language: "java,javascript"
      # （可选）源代码根目录，默认使用当前工作目录
      source-root: "./test"
      # （可选）CodeQL CLI 版本，留空自动获取 OBS 最新版本
      codeql-version: ""
      # （可选）查询套件，默认 security-extended。支持逗号分隔多选
      query-suite: "security-and-quality,security-extended,security-experimental"
      # （可选）数据库构建模式：autobuild（需要安装对应构建工具）或 none（纯静态分析，默认）
      build-mode: autobuild
      # （可选）最低告警级别过滤：note（全部显示，默认）、warning（仅 warning 及以上）、error（仅 error）
      min-severity: "note"
      # （必填）生成的扫描报告保存路径（Markdown 格式）
      report-path: "./test/codeql-security-report.md"
      # （必填）扫描结果输出目录（多语言时生成 codeql-results-{lang}.sarif）
      output-path: "./test/codeql-results"
      # （可选）CodeQL 分析使用的内存上限，单位 MB
      ram: ""
      # （可选）CodeQL 分析使用的线程数，默认使用所有可用核心
      threads: ""
      # （可选）自定义 CodeQL 查询路径，多个用逗号分隔
      queries: ""
      # （可选）是否启用详细输出模式
      verbose: "true"
      # （可选）访问凭据，用于 OBS 下载认证。默认使用流水线内置凭据
      # token: ""

    if: "${{ default() }}"
    runs-on: ["codearts-hosted", "ubuntu-latest", "x64", "large"]
```


         
### 参数说明

| 参数名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `language` | **是** | `javascript` | 要扫描的编程语言，多语言用英文逗号分隔。支持：`javascript`(或`js`), `python`, `java`, `cpp`, `csharp`, `go`, `ruby`, `swift`, `kotlin` |
| `output-path` | **是** | - | 扫描结果输出目录，多语言时在此目录下生成 `codeql-results-{lang}.sarif`（如 `codeql-results-java.sarif`），如 `./test/codeql-results` |
| `report-path` | **是** | - | 标记报告保存路径（Markdown 格式），如 `./test/codeql-security-report.md` |
| `source-root` | 否 | 工作目录 | 源代码根目录，自动识别 `GITHUB_WORKSPACE`、`CI_PROJECT_DIR` 等常见环境变量 |
| `codeql-version` | 否 | `latest` | CodeQL CLI 版本号，留空或 `latest` 自动获取 OBS 上最新版本 |
| `query-suite` | 否 | `security-extended` | 查询套件：`security-and-quality` / `security-extended` / `security-experimental`，支持逗号分隔多选 |
| `queries` | 否 | 空 | 自定义查询路径（`.ql` 文件），多个用逗号分隔 |
| `github-repository` | 否 | 空 | GitHub 仓库地址，用于加载定制查询（可选） |
| `build-mode` | 否 | `none` | 数据库构建模式：`autobuild`（自动构建，需安装对应构建工具）、`none`（纯静态分析）或 `manual`（手动构建，需配合 `build-command`）。详见下方说明 |
| `build-command` | 否（manual 模式必填） | 空 | 手动构建命令，仅 `build-mode=manual` 时使用。支持多行，将按顺序执行。例如：`cmake -B build && cmake --build build -j4` |
| `config-file` | 否 | 空 | 自定义 CodeQL 配置文件路径，参考 GitHub `codeql-config.yml` 格式。例如：`./.github/codeql/codeql-config.yml` |
| `min-severity` | 否 | `note` | 最低告警级别过滤：`note`（显示所有）、`warning`（仅 warning 及以上）、`error`（仅 error）。设置为 `warning` 或 `error` 可过滤低级别噪音 |
| `ram` | 否 | 自动 | CodeQL 分析内存上限（单位 MB），低于 2048MB 将使用系统默认值 |
| `threads` | 否 | 所有核心 | CodeQL 分析使用的线程数 |
| `verbose` | 否 | `false` | 是否启用详细输出模式，开启后会输出 autobuild 构建命令的详细日志 |
| `token` | **是** | - | 访问凭据，用于 OBS 下载认证。支持从环境变量 `WORKFLOW_TOKEN` 获取 |

### 输出参数

| 参数名 | 说明 | 示例值 |
|--------|------|--------|
| `success` | 扫描是否成功 | `true` / `false` |
| `sarif-output` | SARIF 报告文件所在目录路径 | `/path/to/sarif-dir` |
| `sarif-id` | SARIF 数据的唯一标识 ID | `codeql-1684567890123` |
| `report-path` | Markdown 报告文件路径 | `/path/to/codeql-report.md` |
| `total-issues` | 发现的告警总数 | `42` |
| `codeql-version` | 使用的 CodeQL CLI 版本 | `2.25.4` |
| `languages` | 已扫描的编程语言列表 | `javascript,java` |
| `rule-count` | 执行的查询规则数量 | `202` |

---

## 支持的语言

| # | 标识符 | 语言 | 默认模式 | 可通过 `build-mode` 切换 | 说明 |
|---|--------|------|---------|------------------------|------|
| 1 | `javascript` (或 `js`) | JavaScript / TypeScript | none | 否，始终 none | 无需编译，直接分析源码 |
| 2 | `python` | Python | none | 否，始终 none | 无需编译，直接分析源码 |
| 3 | `ruby` | Ruby | none | 否，始终 none | 无需编译，直接分析源码 |
| 4 | `java` | Java | none（默认） | **是** | `build-mode: autobuild` 需安装 Maven 或 Gradle |
| 5 | `kotlin` | Kotlin | none（默认） | **是** | `build-mode: autobuild` 需安装 Maven 或 Gradle |
| 6 | `cpp` | C / C++ | none（默认） | **是** | `build-mode: autobuild` 需安装 make/cmake/g++ |
| 7 | `csharp` | C# | autobuild | 否，始终 autobuild | **必须依赖 autobuild**，需要 .NET SDK |
| 8 | `go` | Go | autobuild | 否，始终 autobuild | **必须依赖 autobuild**，需要 Go 编译器 |
| 9 | `swift` | Swift | autobuild | 否，始终 autobuild | **必须依赖 autobuild**，需要 Swift 编译器 |

> **注意**：
> - csharp / go / swift 由于语言特性不支持 `--build-mode=none`，如果运行环境缺少对应的构建工具，将跳过该语言的扫描
> - java / kotlin / cpp 可通过 `build-mode` 参数在 autobuild 和 none 之间切换
> - javascript / python / ruby 始终使用 none 模式，不受 `build-mode` 影响

### 多语言扫描组合示例

```yaml
# 全量扫描所有支持的语言（耗时最长）
language: "javascript,python,java,kotlin,cpp,csharp,go,ruby,swift"

# 前端项目
language: "javascript"

# Java 微服务 + 前端
language: "java,javascript"

# Python 数据科学项目
language: "python"

# Go 微服务项目
language: "go"

# C/C++ 嵌入式项目
language: "cpp"
```

---



## 查询套件

| 查询套件 | 说明 | 适用场景 |
|---------|------|---------|
| `security-and-quality` | 安全和质量查询 | **推荐**，覆盖常见漏洞及代码质量问题，误报率低 |
| `security-extended` | 安全扩展查询（默认） | 在 `security-and-quality` 基础上增加更多安全查询 |
| `security-experimental` | 实验性安全查询 | 包含最新的实验性规则，可能不稳定 |

### 查询套件覆盖范围对比

| 漏洞类型 | security-and-quality | security-extended | security-experimental |
|---------|:---:|:---:|:---:|
| SQL 注入 | ✅ | ✅ | ✅ |
| XSS 跨站脚本 | ✅ | ✅ | ✅ |
| 命令注入 | ✅ | ✅ | ✅ |
| 路径遍历 | ✅ | ✅ | ✅ |
| 不安全的反序列化 | ✅ | ✅ | ✅ |
| 不安全的随机数 | ✅ | ✅ | ✅ |
| 原型污染 | ✅ | ✅ | ✅ |
| CSRF | ✅ | ✅ | ✅ |
| 日志注入 | ✅ | ✅ | ✅ |
| 硬编码数据作为代码执行 | ❌ | ✅ | ✅ |
| ReDoS 正则拒绝服务 | ❌ | ✅ | ✅ |
| 实验性规则 | ❌ | ❌ | ✅ |

---

## 告警严重程度分级

插件内置自定义规则映射表，根据 `ruleId`（规则 ID）对告警进行三级分类。

| 等级 | 级别代码 | 图标 | 说明 |
|:---|:---|:---|:---|
| **高危** | `error` | 🔴 Error | 可能导致直接安全入侵的漏洞 |
| **中危** | `warning` | 🟠 Warning | 需要关注的安全告警 |
| **低危** | `note` | 🟡 Note | 参考信息或轻微问题 |

> **判定逻辑**：采用**就高原则**。先取 SARIF 原始 `level`（无则默认 `warning`），再按 `ruleId` 匹配规则表，如果匹配到的等级更高则升级，但不会降级。

---

## Markdown 报告样例

```markdown
# CodeQL 安全扫描报告

> **分析工具**: CodeQL 2.25.4 | **语言**: javascript,java | **查询套件**: security-and-quality

| 严重程度 | 数量 |
| :--- | :--- |
| 🔴 高危 | 3 |
| 🟠 中危 | 7 |
| 🟡 低危 | 2 |
| **总计** | **12** |

---

## 发现的告警

### 1. 🟠 Warning — js/redos

| 属性 | 值 |
| :--- | :--- |
| **文件路径** | `src/app.js` |
| **行号** | 42:18 |
| **规则** | `js/redos` |
| **级别** | 🟠 Warning |
| **状态** | ⚠️ 待修复 |
| **描述** | This regular expression may run slow on crafted input. |

**数据流路径 (6 步):**

| # | 文件位置 | 描述 |
| :--- | :--- | :--- |
| 1 | `app.js:10:5` | 入口点 (source) — user input |
| 2 | `app.js:15:10` | RegExp constructor |
| ... | ... | ... |
| 6 | `app.js:42:18` | 风险点 (sink) — exec() |

---
```

---

## 常见问题

### CodeQL CLI 下载失败

确保流水线已配置以下环境变量（或通过 `token` 参数传入）：

| 环境变量 | 说明 |
|---------|------|
| `WORKFLOW_REGION` | 区域（如 `cn-north-4`） |
| `WORKFLOW_EXECUTE_DOMAIN_ID` | 租户 ID |
| `WORKFLOW_TOKEN` | 访问凭据 |

### 数据库构建模式（build-mode）

`build-mode` 参数控制编译型语言的数据库创建方式，**默认值为 `none`**。JS/Python/Ruby 解释型语言不支持 `manual` 和 `autobuild`，始终使用 `none`。

| 值 | 效果 | 适用语言 |
|----|------|---------|
| `none`（默认） | 纯静态分析，无需构建工具，秒级完成 | Java / Kotlin / C++ |
| `autobuild` | 自动检测构建工具并执行构建 | Java / Kotlin / C++ / C# / Go / Swift |
| `manual` | 使用 `build-command` 指定构建命令 | Java / Kotlin / C++ / C# / Go / Swift |

#### build-mode: manual 使用示例

**Java（Maven 项目）**：需要配合 `setup-jdk` 安装 JDK 和 Maven。

```yaml
-
  name: setup-jdk
  uses: setup-jdk
  with:
    jdk-version: "17"
    maven-version: '3.8.9'
-
  name: codeql-action
  uses: codeql-action
  with:
    language: "java"
    build-mode: manual
    build-command: |
      mvn compile -DskipTests
    source-root: "./test"
    output-path: ./test/codeql-results
    report-path: ./test/codeql-report.md
```

**Java（Gradle 项目）**：

```yaml
-
  name: setup-jdk
  uses: setup-jdk
  with:
    jdk-version: "17"
    gradle-version: '8.5'
-
  name: codeql-action
  uses: codeql-action
  with:
    language: "java"
    build-mode: manual
    build-command: |
      gradle compileJava
    source-root: "./test"
    output-path: ./test/codeql-results
    report-path: ./test/codeql-report.md
```

**C/C++（CMake 项目）**：需环境预装 g++、cmake、make（ubuntu-latest 已自带）。

```yaml
-
  name: codeql-action
  uses: codeql-action
  with:
    language: "cpp"
    build-mode: manual
    build-command: |
      cmake -B build -G "Unix Makefiles"
      cmake --build build -j4
    source-root: "./test"
    output-path: ./test/codeql-results
    report-path: ./test/codeql-report.md
```

**Go 项目**：Go 自动使用 autobuild，通常不需要 manual。如需指定构建命令：

```yaml
-
  name: setup-go
  uses: setup-go
  with:
    version: "1.21"
    architecture: 'x64'
-
  name: codeql-action
  uses: codeql-action
  with:
    language: "go"
    build-mode: manual
    build-command: |
      go build ./...
    source-root: "./test"
    output-path: ./test/codeql-results
    report-path: ./test/codeql-report.md
```

> **`build-command` 中的命令会在 CodeQL tracer 环境下先后执行两次**：第一次预检捕获编译错误，第二次在 tracer 插桩下重新编译以收集精确的调用关系数据。预检通过后会清理 `build/` 和 `target/` 目录再执行第二次编译。

### 编译型语言扫描失败

以下语言 **需要构建环境**（不支持 `--build-mode=none`），运行环境缺少对应构建工具时将跳过扫描：

| 语言 | 所需构建文件 | 所需运行时 |
|------|------------|-----------|
| **C#** | `.csproj` 或 `.sln` | .NET SDK |
| **Go** | `go.mod` | Go 编译器 |
| **Swift** | `Package.swift` | Swift 编译器 |

以下语言支持 `--build-mode=none` 纯静态分析，也支持 autobuild 编译型分析：

| 语言 | 构建文件 | 构建工具 | `none` | `autobuild` |
|------|---------|---------|--------|------------|
| **Java / Kotlin** | `pom.xml` → `mvn`；`build.gradle` → `gradle` | Maven / Gradle | ✅ 直接分析源码 | ✅ 需要 Maven 或 Gradle |
| **C / C++** | `Makefile` / `CMakeLists.txt` | make / cmake | ✅ 直接分析源码 | ✅ 需要 make 或 cmake |

> **建议**：
> - 如果项目有完整的构建配置文件且环境已安装对应工具，使用 `build-mode: autobuild` 可获得更精确的分析结果
> - 如果仅需快速安全扫描，或环境缺少构建工具，使用 `build-mode: none` 或留空自动检测即可

### 测试文件路径过滤

插件内置了测试文件路径过滤功能，自动排除以下路径中的告警（不统计到总数）：

| 排除模式 | 说明 |
|---------|------|
| `/src/test/` | Maven/Gradle 标准测试目录 |
| `/tests/` | 项目根目录下的 `tests/` |
| `/__tests__/` | Jest 测试目录 |
| `/__spec__/` | 规范测试目录 |
| `node_modules/` | JavaScript 依赖 |
| `/vendor/` | PHP/Go 依赖 |
| `/third_party/` | 第三方依赖 |
| `.git/` | Git 对象 |

> **注意**：路径过滤仅排除 `src/test/` 等明确测试目录中的告警。对于将测试代码放在 `src/main/` 下的项目（如 OWASP Benchmark），所有告警均正常统计，不会因为文件名包含 "Test" 而被误排除。日志会显示 `📊 路径过滤: 排除了 X 个测试文件中的告警（全部 X 个）`。

### 告警级别过滤（min-severity）

通过 `min-severity` 参数可以按级别过滤告警：

| 值 | 效果 |
|----|------|
| `note`（默认） | 显示所有告警 |
| `warning` | 只显示 warning 及以上级别（过滤 note） |
| `error` | 只显示 error 级别 |

> 对于 `--build-mode=none` 产生的较多低级别噪音，建议设置 `min-severity: warning` 以减少噪音。

### 如何查看扫描结果

1. **SARIF 文件**：可导入安全平台进行可视化分析
2. **Markdown 报告**：可直接在流水线产物中查看
3. **流水线日志**：输出包含告警总数、分级统计、前 10 条问题详情




---

## 35. ApiDispatch

- **name**: `api-dispatch`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.1.2

# api-dispatch

第三方接口调度插件 — 在 CI/CD 流水线中发起 HTTP API 请求，支持认证、重试、状态码校验和响应字段提取。

## 功能特性

- 支持 GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS（输入校验，非法方法报错）
- Bearer Token / Basic Auth / 自定义认证头（凭据自动掩码，互斥优先 Bearer）
- 5xx / 429 / 网络错误 / 超时自动重试
- 状态码校验（支持 2XX/3XX 通配符）
- 动态字段提取（嵌套路径，点替换为破折号作为输出名）
- 响应体保存到文件
- ATOMGIT 跨 step 输出（优先级：ATOMGIT > CODEHUB > GITHUB）
- SSL 证书忽略（仅测试用，通过自定义 Agent 实现）
- 输入参数校验（URL、method、数值参数、basic-auth 格式）

## Usage

### 基础 GET 请求

```yaml
steps:
  - uses: api-dispatch
    with:
      url: 'https://api.example.com/v1/status'
      output-fields: 'data.status'
```

### POST 请求 + Bearer Token

```yaml
steps:
  - uses: api-dispatch
    id: create_bug
    with:
      url: 'https://api.example.com/v1/bugs'
      method: 'POST'
      bearer-token: '${{ secrets.API_TOKEN }}'
      body: '{"title":"CI构建失败","severity":"high"}'
      accept: '201'
      output-fields: 'data.id,data.url'
```

### 禅道 API 调用

```yaml
steps:
  # 1. 登录获取 token
  - uses: api-dispatch
    id: zentao_login
    with:
      url: 'https://your-zentao.com/api.php/v1/tokens'
      method: 'POST'
      body: '{"account":"your_account","password":"your_password"}'
      output-fields: 'token'
      log-response: 'false'

  # 2. 创建 Bug（禅道使用自定义 Token 头）
  - uses: api-dispatch
    id: create_bug
    with:
      url: 'https://your-zentao.com/api.php/v1/bugs'
      method: 'POST'
      bearer-token: '${{ steps.zentao_login.outputs.token }}'
      auth-header: 'Token'
      body: '{"product":1,"title":"CI构建失败","type":"codeerror","severity":3}'
      accept: '201,200'
      output-fields: 'id'
```

> **注意**：`${{ steps.*.outputs.* }}` 跨 step 语法在 GitCode 平台已支持（ATOMGIT_OUTPUT），CodeArts 平台需确认支持情况。

### 重试 + 保存响应

```yaml
steps:
  - uses: api-dispatch
    with:
      url: 'https://api.example.com/v1/data'
      max-retries: '3'
      retry-interval: '2000'
      save-response: 'true'
      accept: '2XX'
```

### 自定义认证头（非标准 Token API）

```yaml
steps:
  - uses: api-dispatch
    with:
      url: 'https://api.example.com/v1/data'
      bearer-token: '${{ secrets.API_KEY }}'
      auth-header: 'X-API-Key'
```

> **说明**：`auth-header` 默认 `Authorization`（标准 Bearer 场景）。当 API 使用非标准认证头（如禅道的 `Token`、`X-API-Key`），只需设置 `auth-header`，token 值不会加 `Bearer ` 前缀。

### 自定义请求头

```yaml
steps:
  - uses: api-dispatch
    with:
      url: 'https://api.example.com/v1/data'
      headers: '{"X-Custom-Header":"value","Accept":"application/json"}'
```

> **注意**：`headers` 中的键会覆盖默认 `Content-Type`。如果需要自定义 Content-Type，优先使用 `content-type` 输入参数。

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| url | 是 | — | 请求 URL（必须为合法 HTTP/HTTPS URL） |
| method | 否 | GET | HTTP 方法（仅允许 GET/POST/PUT/PATCH/DELETE/HEAD/OPTIONS） |
| headers | 否 | {} | 请求头 JSON 键值对 |
| body | 否 | — | 请求体 JSON（POST/PUT/PATCH 时使用） |
| content-type | 否 | application/json | Content-Type 头 |
| bearer-token | 否 | — | Bearer Token 认证（日志自动掩码） |
| auth-header | 否 | Authorization | 自定义认证头名称（如 Token、X-API-Key），配合 bearer-token 使用 |
| basic-auth | 否 | — | Basic 认证（格式 username:password，日志自动掩码） |
| timeout | 否 | 30000 | 请求超时时间（毫秒，必须为正整数） |
| max-retries | 否 | 0 | 最大重试次数（0=不重试，必须为非负整数） |
| retry-interval | 否 | 1000 | 重试间隔（毫秒，必须为非负整数） |
| accept | 否 | 2XX | 可接受状态码（逗号分隔，支持通配符） |
| ignore-ssl | 否 | false | 禁用 SSL 证书验证（不安全，仅测试用） |
| output-fields | 否 | — | 从响应体提取的字段路径（逗号分隔，支持嵌套如 data.items.0.id） |
| save-response | 否 | false | 将响应体保存到 api-response.json 文件 |
| log-response | 否 | false | 在日志中打印响应状态和正文（截断2000字符，注意可能包含敏感信息） |

## Outputs

| 输出 | 说明 |
|------|------|
| response-status | HTTP 响应状态码 |
| response-headers | 响应头 JSON 字符串（数组值用逗号拼接） |
| response-body | 原始响应体文本 |
| response-file | 保存的响应文件路径（仅 save-response=true 时设置） |
| {自定义字段} | 通过 output-fields 提取，点替换为破折号（如 data.id → data-id） |

> **冲突检测**：如果 output-fields 生成的输出名与内置输出（response-status、response-headers、response-body、response-file）冲突，会跳过并发出警告。

## 重试规则

以下情况自动触发重试：
- HTTP 5xx 状态码
- HTTP 429（速率限制）
- 网络连接错误（DNS 解析失败、连接拒绝等）
- 请求超时

总尝试次数 = max-retries + 1。所有重试失败后抛出错误。

## 状态码匹配

- 精确匹配：`200,201,204`
- 通配符匹配：`2XX`（匹配 200-299）、`3XX`（匹配 300-399）
- 默认值改为 `2XX`，兼容所有成功状态码（包括 202 Accepted）

## 字段提取说明

- 使用点路径访问嵌套字段：`data.id`、`data.user.name`
- 数组元素用数字索引：`data.items.0.id`（JavaScript 点语法）
- 提取的值自动转为字符串
- 字段未找到时发出警告，不会导致步骤失败

---

## 36. dedicate-preheat-plugin

- **name**: `dedicate-preheat-plugin`
- **creator**: wukong_admin
- **被引用**: 29
- **版本**: 1.0.5

# dedicate-preheat-plugin

资源预热插件，负责通过接收 namespace_id、arch、flavor、image_name、resource_pool_name 等参数，发送请求获取构建资源，并轮询等待执行完成。

---

## 目录

- [功能](#功能)
- [Usage](#usage)
- [Inputs](#inputs)
- [Outputs](#outputs)

---

## 功能   

| 特性     | 说明 |
|--------|------|
| 预热请求接口 | /v1/runner-groups/preheat |
| 查询请求接口 | /v1/runner-groups/preheat/query |
| 请求参数   | namespace_id, image, arch, flavor, resource_pool_name |
| 认证方式   | x-auth-token |
| 轮询间隔   | 15秒 |

---

## Usage

### 基础用法

```yaml
- name: dedicate-preheat-plugin
  uses: dedicate-preheat-plugin
  with:
    namespace_id: 'namespace-123'
    arch: 'x86'
    flavor: 'large'
    image_name: 'build-image:latest'
    resource_pool_name: 'pool-xxx'
    timeout: '3600'
```

### 超时设置说明

- `timeout` 参数可选，默认值为 3600 秒
- 插件会轮询等待所有实例完成，直到：
  - 所有实例状态均为 FINISHED（成功）、ABNORMAL 或 CANCELED（失败）
  - 达到超时时间

---

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `namespace_id` | 是 | — | 命名空间ID |
| `arch` | 是 | — | 架构类型 (如 x86, arm) |
| `flavor` | 否 | — | 规格类型（如 large、medium、small） |
| `image_name` | 是 | — | 镜像名称 |
| `resource_pool_name` | 否 | — | 资源池名称 |
| `timeout` | 否 | 3600 | 超时时间（秒） |

---

## Outputs

本插件无 outputs 定义。

---

## 注意事项

- 插件会通过日志输出异常实例的 cmd_uuid、job_sign、status 和 message
- 如果有实例状态为 ABNORMAL 或 CANCELED，插件执行结果为失败
- 如果达到超时时间，插件执行结果为失败


---

## 37. ArtifactUploader

- **name**: `artifact-uploader`
- **creator**: wukong_admin
- **被引用**: 0
- **版本**: 1.0.4

# artifact-uploader

本插件用于将构建产物上传至 CodeArts 软件发布库，支持在流水线中自动完成软件包的归档与发布。

## 功能特性

- 支持将指定文件上传至 CodeArts 软件发布库
- 支持自定义上传目录
- 支持多 Region 部署（自动根据 region 拼接发布库地址）
- 支持目录创建与上传
- 支持批量文件上传（最大 1000 个文件），并发限制 10
- 大文件分块上传（8MB 分块），异步超时 4 小时
- 自动从流水线上下文获取项目、用户等认证信息

## 输入参数

| 参数名 | 是否必填 | 默认值 | 说明                                                |
| --- | --- | --- |---------------------------------------------------|
| `token` | 是 | `${{ X_AUTH_TOKEN }}` | 用户Token，用于接口认证                                    |
| `region` | 是 | - | CodeArts Region 信息，例如 `cn-north-4`、`cn-north-7` 等 |
| `file_path` | 是 | - | 待上传文件的完整路径，支持字母、数字、下划线、横线、斜杠、点、反斜杠、星号、问号等常用字符     |
| `upload_path` | 否 | - | 自定义上传目录，支持字母、数字、下划线、横线、斜杠，长度 1-128 字符             |

## 输出参数

本插件通过流水线上下文输出上传结果，上传完成后可在后续任务中通过软件发布库查看已上传的制品。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `success` | boolean | 上传是否成功 |
| `artifactId` | string | 上传成功后返回的制品 ID |
| `path` | string | 上传到依赖库时的路径 |
| `error.code` | string | 上传失败时的错误码，如 `UPLOAD_ERROR` |
| `error.message` | string | 上传失败时的错误详情 |

## 使用示例

### 基础用法

上传指定文件到软件发布库：

```yaml
- name: 上传软件发布库
  uses: artifact-uploader@1.0.3
  with:
    region: cn-south-1
    file_path: /home/octopus/runner/workers/0.0.3.15.version/worker_dir/tujian_test/cynb_gogogo/test_file.txt
```

### 指定自定义上传目录

上传文件并指定发布库中的目标目录：

```yaml
- name: 上传软件发布库
  uses: artifact-uploader@1.0.3
  with:
    region: cn-south-1
    file_path: /home/octopus/runner/workers/0.0.3.15.version/worker_dir/tujian_test/cynb_gogogo/test_file.txt
    upload_path: 'release/v1.0.0'
```

### 在完整流水线中使用

在构建任务完成后上传制品：

```yaml
stages:
  stage1:
    name: 阶段_1
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建与发布
        needs: []
        select: selected_by_default
        steps:
        - name: 执行shell
          uses: official_shell_plugin
          with:
            OFFICIAL_SHELL_SCRIPT_INPUT: |
              echo "Hello, World!" > /home/octopus/runner/workers/0.0.3.15.version/worker_dir/tujian_test/cynb_gogogo/test_file.txt
        - name: 上传软件发布库
          uses: artifact-uploader@1.0.3
          with:
            region: cn-south-1
            file_path: /home/octopus/runner/workers/0.0.3.15.version/worker_dir/tujian_test/cynb_gogogo/test_file.txt
            upload_path: 'prod/latest'
        if: "${{ default() }}"
        runs-on:
        - default
    pre:
    - type: auto
```


---

## 38. checkout

- **name**: `checkout`
- **creator**: wukong_admin
- **被引用**: 132341
- **版本**: 1.0.6

# 1. CHECKOUT

在流水线工作区中检出目标代码仓库，支持多仓库、子模块及大文件存储 (LFS)。

## 1.1 checkout目录说明

本插件主要用于支持用户选择多流水线代码源checkout能力，用户只能执行流水线配置有权限的代码源，会校验用户的执行权限。

## 1.2 功能特性

- **多源与多路复用检出**：支持在同一个流水线 Job 中多次调用，通过配置不同的 path 将多个不同的代码仓库按目录结构精准下载
- **细粒度目标定位**：支持精确拉取特定的分支 (Branch)、标签 (Tag) 或具体的提交哈希 (Commit SHA)
- **高级代码结构支持**：
  - 子模块 (Submodules)：支持按需加载或递归拉取嵌套子模块
  - 大文件存储 (Git LFS)：原生支持AI模型等场景的二进制大文件拉取
- **环境兼容性**：支持 Linux, Windows, macOS 等不同操作系统
- **性能优化**：支持浅克隆和检出深度控制，避免巨型仓库超时和磁盘爆满
- **环境隔离**：确保每次构建起点是干净可预期的

## 1.3 参数

### 1.3.1 输入参数

| 参数名           | 类型      | 必填 | 默认值                          | 描述                                                                          |
|---------------|---------|----|------------------------------|-----------------------------------------------------------------------------|
| `repository`  | String  | 是  | `${{atomgit.repositoryUrl}}` | 目标代码库完整地址                                                                   |
| `ref`         | String  | 是  | `${{atomgit.ref}}`           | 分支名、Tag 或 Commit SHA                                                        |
| `path`        | String  | 否  | `WORKSPACE/仓库名`     | 代码检出后的存放相对路径。支持多仓库并发克隆的核心参数。默认为`WORKSPACE/仓库名`                     |
| `endpoint_id` | String  | 否  | 无                            | 节点ID，若该参数不为空，会自动获取对应的访问令牌，并覆盖用户填入的token参数。                                  |
| `token`       | Secret  | 否  | 暂无                           | 代码仓认证方式之一，个人代码仓访问令牌。https下载链接需通过该参数进行仓库认证。                                  |
| `ssh-key`     | Secret  | 否  | 无                            | 代码仓认证方式之一，SSH 部署密钥。ssh下载链接需通过该参数进行仓库认证。注：本插件不支持加密的ssh密钥对。                   |
| `fetch-depth` | Int     | 否  | `1`                          | 检出深度。默认为 1（浅克隆，极大提升速度）。如果设为 0 则拉取全部历史记录（适合需要做全量 Sonar 扫描或构建 Changelog 的场景）。 |
| `submodules`  | String  | 否  | `false`                      | 是否检出子模块。可选 true（拉取）、false（不拉取）、recursive（递归拉取所有嵌套子模块）。注：子模块与主仓需同一代码仓平台。     |
| `lfs`         | Boolean | 否  | `false`                      | 是否下载 Git LFS（大文件存储）文件。若该参数为true，所在环境需要提前安装好git lfs模块。                       |
| `clean`       | Boolean | 否  | `true`                       | 是否在检出前执行 git clean -ffdx 等命令清理工作区。保证构建环境的纯洁性。                               |

### 1.3.2 输出参数

| 参数名      | 类型     | 描述                           |
|----------|--------|------------------------------|
| `commit` | String | 实际检出的 Commit SHA, 用法请参考1.4.2 |
| `ref`    | String | 实际检出的分支或 Tag 名称, 用法请参考1.4.2              |
| `path`   | String | 代码实际存放的绝对工作路径, 用法请参考1.4.2                |

## 1.4 使用方法

**目前不支持代码仓、访问token、分支的默认加载，需要流水线侧支持**

### 1.4.1 最速用法（文件名main.yml, 直接粘就能用!）

```yaml
permissions:
  project: read
  pr: read
  issue: read
  note: read
  repository: read

name: main

on:
  workflow_dispatch:

stages:
  stage1:
    name: 阶段_01
    select: selected_by_default
    jobs:
      JOB_FNZhc:
        name: checkout_job
        select: selected_by_default
        needs: [ ]
        steps:
          - name: fast_checkout
            identifier: fast_checkout
            uses: checkout
            with: # 啥都不用写, 默认下载当前流水线触发仓
            # repository: 'https://test.gitcode.net/test_enterprise/label_test.git'
            # ref: main
            # path: repo
            # token: 代码仓token
            # ssh-key: ""
            # endpoint_id: ""
            # fetch-depth: 1
            # submodules: "false"
            # lfs: "false"
            # clean: "true"
          # 跨step查看下载情况
          - name: show_repository
            uses: official_shell
            with:
              script: |
                CHECKOUT_COMMIT="${{ steps.fast_checkout.outputs.commit }}"
                CHECKOUT_REF="${{ steps.fast_checkout.outputs.ref }}"
                CHECKOUT_PATH="${{ steps.fast_checkout.outputs.path }}"
                echo "检出代码所在commit: $CHECKOUT_COMMIT"
                echo "检出代码所在分支/tag名: $CHECKOUT_REF"
                echo "检出代码所在绝对路径: $CHECKOUT_PATH"
                ls -ahl $CHECKOUT_PATH
        if: "${{ default() }}"
        runs-on:
          - default
```

### 1.4.2 基本用法

```yaml
# 下载分支
- name: Checkout repository with branch
  identifier: checkout_with_branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
# 跨step查看下载情况
- name: show repository
  uses: official_shell
  with:
    script: |
      echo "检出代码所在commit: ${{ steps.checkout_with_branch.outputs.commit }}"
      echo "检出代码所在分支/tag名: ${{ steps.checkout_with_branch.outputs.ref }}"
      echo "检出代码所在绝对路径: ${{ steps.checkout_with_branch.outputs.path }}"
      ls -ahl $CHECKOUT_PATH

# 下载commitid
- name: Checkout repository with sha
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: c7f9091578ff55667b773ba666952272b80e86fd
    token: 你的代码仓pat

# 下载tag
- name: Checkout repository with tag
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/tags/111111
    token: 你的代码仓pat

# 下载预合并分支（不同代码仓预合并分支规则不同，详见不同代码仓官方文档）
- name: Checkout repository with pre merge
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/merge-requests/3/merge
    token: 你的代码仓pat
```

### 1.4.3 高级用法

#### 1.4.3.1 检出特定深度

```yaml
# 拉取最新一层的提交
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    fetch-depth: 1  # 默认值，不填就是这个

# 拉取最近5层提交
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    fetch-depth: 5

# 小于等于0时，拉取完整代码
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    fetch-depth: 0
```

#### 1.4.3.2 处理子模块

```yaml
# 默认值, 不拉取子模块
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    submodules: false  # 默认值, 不拉取子模块

# 拉取直接子模块
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    submodules: true  # 拉取直接子模块

# 递归拉取所有嵌套子模块（子模块下的子模块也会拉取）
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    submodules: recursive  # 递归拉取所有嵌套子模块（子模块下的子模块也会拉取）
```

#### 1.4.3.3 处理大文件 (LFS)

```yaml
# 默认值, 不拉取大文件
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    lfs: false  # 默认值, 不拉取大文件

# 拉取大文件
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    lfs: true  # 拉取大文件

# 递归拉取子模块和大文件（两者同时配合，在下载子模块的同时，会把子模块下的大文件一并下载）
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    lfs: true  # 拉取大文件
    submodules: recursive  # 递归拉取所有嵌套子模块（子模块下的子模块也会拉取）
```

#### 1.4.3.4 下载前清理工作目录

```yaml
# 默认值为true，执行git clean命令。git clean 用于删除未跟踪（untracked）的文件，即那些没有被git管理的文件（比如新建但未add的文件、编译产物等）。
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    clean: true # 默认值为true，执行git clean命令

# false，不执行git clean命令，直接在原有目录下下载代码
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
    clean: false # false，不执行git clean命令，直接在原有目录下下载代码
```

### 1.4.3 支持多种认证方式

#### 1.4.3.1 Token 认证（https格式的下载链接使用Token进行认证）

```yaml
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: https://gitcode.com/xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    token: 你的代码仓pat
```

#### 1.4.3.2 SSH 密钥认证（git@格式的下载链接使用SSH进行认证）

```yaml
- name: Checkout repository with branch
  uses: checkout
  with:
    repository: git@gitcode.com:xxxxxx/gitcode-codecheck-test.git
    ref: refs/heads/master
    ssh-key: |
      -----BEGIN OPENSSH PRIVATE KEY-----
      我是ssh-key，注意ssh-key不能加密，且格式需要完整（包括换行符）
      建议使用yaml的块语法（即|后换行）填写ssh-key
      -----END OPENSSH PRIVATE KEY-----
```

## 1.5 故障排除

### 1.5.1 认证失败

确保：

1. Token 有足够的权限访问目标仓库
2. SSH 密钥格式正确且对应的公开密钥已添加到目标仓库（不能加密）
3. 仓库地址格式正确（pat对应https格式，SSH密钥对应git@格式）

### 1.5.2 子模块初始化失败

检查：

1. 主仓库是否先成功检出
2. 子模块配置是否正确
3. 网络连接是否正常
4. 子模块认证方式是否与主仓库相同（例如子模块使用git@下载代码, 但是认证方式使用的是token）

### 1.5.3 LFS 文件下载失败

验证：

1. **运行环境是否安装GIT LFS模块**
2. 磁盘空间是否足够
3. 对应仓库平台是否支持LFS功能


---

## 39. codecov

- **name**: `codecov`
- **creator**: wukong_admin
- **被引用**: 38
- **版本**: 1.3.9

# codecov

解析覆盖率报告并生成本地 HTML 报告，支持多格式自动识别。

- 多格式覆盖，支持 lcov、cobertura、jacoco、gcov、clover、istanbul 等主流格式
- 自动搜索，无需手动指定文件路径即可发现覆盖率报告
- 本地 HTML 报告，解析后直接生成到指定目录
- 源码增强，HTML 报告内嵌源码逐行标色（覆盖/未覆盖/部分覆盖）
- CI 门禁，支持行/分支/函数覆盖率阈值检查，不达标可中断流水线
- Step Summary，自动将覆盖率摘要写入步骤 Summary，在流水线页面直接查看

## Usage

### 基础用法

```yaml
name: codecov
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  coverage:
    name: 覆盖率
    select: selected_by_default
    jobs:
      CODECOV:
        name: 生成覆盖率报告
        select: selected_by_default
        needs: []
        steps:
          - name: 生成覆盖率报告
            uses: codecov
            with:
              files: |
                coverage/lcov.info
                coverage/cobertura-coverage.xml
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 自动搜索 + 自定义输出目录

```yaml
- name: 自动搜索覆盖率文件
  uses: codecov
  with:
    directory: "coverage"
    output-dir: "./reports/coverage"
```

### 仅指定文件

```yaml
- name: 指定覆盖率文件
  uses: codecov
  with:
    files: "build/reports/jacoco/test/jacocoTestReport.xml"
    output-dir: "./coverage-report"
```

### 源码增强（内嵌源码逐行标色）

```yaml
- name: 生成带源码的覆盖率报告
  uses: codecov
  with:
    files: "coverage/lcov.info"
    source-root: "./src"
```

设置 `source-root` 后，HTML 报告中每个文件会内嵌源码，并根据覆盖状态逐行标色：
- 🟩 绿色：已覆盖
- 🟥 红色：未覆盖
- 🟨 黄色：部分覆盖（分支覆盖）

### CI 门禁（覆盖率阈值检查）

```yaml
- name: 覆盖率报告 + 门禁检查
  uses: codecov
  with:
    files: "coverage/lcov.info"
    threshold-lines: 80        # 行覆盖率必须 ≥ 80%
    threshold-branches: 60     # 分支覆盖率必须 ≥ 60%
    threshold-functions: 70    # 函数覆盖率必须 ≥ 70%
    fail-on-error: true        # 不达标时流水线失败
```

设为 0 表示不检查该项。门禁结果通过 `gate-result` 输出，可在后续步骤中使用：

```yaml
- name: 检查门禁结果
  if: steps.coverage.outputs.gate-result == 'fail'
  run: echo "覆盖率门禁未通过！"
```

### Step Summary（步骤摘要）

插件运行后自动将 Markdown 格式的覆盖率摘要写入 Step Summary，无需额外配置。在流水线 Job 页面点击步骤即可直接查看覆盖率概览，包含：

- 总体覆盖率状态（✅ 良好 / ⚠️ 一般 / ❌ 较差）
- 行/分支/函数覆盖率汇总表
- 各文件覆盖率明细表（带颜色标识）

摘要效果示例：

```
覆盖率报告: ✅ 良好
格式: LCOV | 报告: coverage.info

总体覆盖率
指标      | 覆盖率  | 覆盖/总计
行覆盖率  | 75.0%  | 6 / 8
分支覆盖率 | -      | -
函数覆盖率 | 100.0% | 3 / 3

文件覆盖率
文件           | 行%       | 分支% | 函数%
calculator.c  | 🟢 80.0%  | -     | 100.0%
utils.c       | 🟡 66.7%  | -     | 100.0%
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| files | 否 | — | 覆盖率报告文件路径，逗号或换行分隔 |
| directory | 否 | — | 搜索覆盖率报告的目录 |
| output-dir | 否 | ./coverage-report | HTML 报告输出目录 |
| source-root | 否 | — | 源码根目录，设置后在 HTML 报告中内嵌源码逐行标色 |
| threshold-lines | 否 | 0 | 行覆盖率门禁阈值(0-100)，0 表示不检查 |
| threshold-branches | 否 | 0 | 分支覆盖率门禁阈值(0-100)，0 表示不检查 |
| threshold-functions | 否 | 0 | 函数覆盖率门禁阈值(0-100)，0 表示不检查 |
| fail-on-error | 否 | true | 解析失败或门禁不达标时是否中断步骤 |
| verbose | 否 | false | 详细日志输出 |
| disable-search | 否 | false | 禁用自动搜索覆盖率文件 |

> **说明**：`files` 和 `directory` 均为非必填。若都不指定，插件会自动在项目根目录搜索覆盖率文件。

## Outputs

| 输出 | 说明 |
|------|------|
| report-status | 报告生成状态：success / failed |
| report-dir | HTML 报告输出目录绝对路径 |
| report-files | 生成的 HTML 报告文件列表 |
| parsed-files | 解析的覆盖率文件列表 |
| html-report-path | 最后一个生成的 HTML 报告文件路径 |
| gate-result | 门禁结果：pass / fail（未配置阈值时不输出） |

## Changelog

### v1.3.8

- 新增 Step Summary 功能：自动将 Markdown 格式覆盖率摘要写入 `ATOMGIT_STEP_SUMMARY`，在流水线页面直接查看
- 修复 Outputs 不生效问题：改用 `ATOMGIT_OUTPUT` 写入 outputs（替代 `@actions/core` 的 `setOutput`）
- 修复自动搜索：新增 `coverage.info` 到 LCOV 搜索模式
- 修复覆盖率显示：分母为 0 时显示 `-` 而非误导性的 100%
- 修复打包问题：移除 ncc `--minify` 选项，避免代码丢失


---

## 40. ObsDownload

- **name**: `obs-download`
- **creator**: wukong_admin
- **被引用**: 101852
- **版本**: 1.1.2

# obs-download

从 OBS 下载文件到本地，支持断点续传和并行下载。

- 多对象批量下载，每行指定一个对象路径
- 断点续传，网络中断后可从上次位置继续
- 并行下载，可配置单对象分片并发和多对象并行数
- 支持匿名访问公共桶（无需 AK/SK），访问私有桶需提供 AK/SK 认证

## 目录

- [Usage](#usage)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [认证模式说明](#认证模式说明)

## Usage

### 基础下载（AK/SK 认证）

```yaml
name: obs-download
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  download:
    name: 下载制品
    select: selected_by_default
    jobs:
      DOWNLOAD:
        name: 从OBS下载
        select: selected_by_default
        needs: []
        steps:
          - name: 下载制品
            uses: obs-download
            with:
              endpoint: "obs.cn-north-4.myhuaweicloud.com"
              bucket: "my-bucket"
              access-key: "${{ Secret.OBS_AK }}"
              secret-key: "${{ Secret.OBS_SK }}"
              key: "artifacts/app.tar.gz"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 匿名下载公共桶（无需 AK/SK）

当目标桶为公共读桶时，可省略 `access-key` 和 `secret-key`，插件将以匿名模式访问：

```yaml
- name: 从公共桶下载
  uses: obs-download
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "public-bucket"
    key: "artifacts/app.tar.gz"
```

> **注意**：匿名模式仅适用于公共桶的公共读对象。如果访问私有桶但未提供 AK/SK，将返回 403 错误并提示需要认证凭据。

### 多文件并行下载

```yaml
- name: 多文件下载
  uses: obs-download
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.OBS_AK }}"
    secret-key: "${{ Secret.OBS_SK }}"
    key: |
      artifacts/app.tar.gz
      artifacts/app.sha256
    path: "./downloads"
    file-concurrency: "2"
```

### 大文件分片下载

```yaml
- name: 大文件下载
  uses: obs-download
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.OBS_AK }}"
    secret-key: "${{ Secret.OBS_SK }}"
    key: "artifacts/large-dataset.bin"
    part-size: "52428800"
    task-num: "10"
    enable-checkpoint: "true"
```

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| endpoint | 是 | — | OBS endpoint，如 `obs.cn-north-4.myhuaweicloud.com` |
| bucket | 是 | — | OBS 桶名 |
| access-key | 否 | — | Access Key ID，访问公共桶时可省略 |
| secret-key | 否 | — | Secret Access Key，访问公共桶时可省略 |
| key | 是 | — | 对象路径，多个对象每行一个 |
| path | 否 | ./ | 本地下载目标目录 |
| part-size | 否 | 9437184 | 分块大小（字节，默认 9MB） |
| task-num | 否 | 5 | 单对象分段下载并发数 |
| file-concurrency | 否 | 1 | 多对象并行下载数，1 为串行 |
| enable-checkpoint | 否 | true | 启用断点续传 |
| max-retry-count | 否 | 3 | SDK 层失败重试次数 |
| timeout | 否 | 10 | HTTP 请求超时（秒），SDK 默认 60s 会导致失败时长时间挂起 |
| retry-attempts | 否 | 2 | 插件层传输异常（如 IncompletedDownload）重试次数 |
| retry-delay-ms | 否 | 2000 | 插件层重试间隔（毫秒） |
| fail-on-error | 否 | true | 下载失败是否中断步骤 |

> **AK/SK 规则**：`access-key` 和 `secret-key` 必须同时提供或同时省略。仅提供其中一个将导致校验错误。

## Outputs

| 输出 | 说明 |
|------|------|
| download-status | 下载状态：success / failed |
| download-path | 主对象本地绝对路径 |
| file-size | 主对象文件大小（字节） |
| download-duration | 下载耗时（秒） |
| obs-etag | 主对象 ETag |
| obs-request-id | OBS 请求 ID（排障用） |
| downloaded-count | 成功下载数量 |
| failed-count | 失败数量 |
| result-summary | 下载结果摘要 |

## 认证模式说明

插件根据是否提供 AK/SK 自动判断认证模式：

| 模式 | 条件 | 适用场景 | 错误提示 |
|------|------|---------|---------|
| **AK/SK 认证** | access-key 和 secret-key 均非空 | 私有桶或需认证的公共桶 | 认证失败时提示检查凭据是否正确 |
| **匿名访问** | access-key 和 secret-key 均为空 | 公共桶的公共读对象 | 403 时提示目标桶可能为私有桶，需提供 AK/SK |

执行报告的 `[基本信息]` 区块会显示当前认证模式，便于排障确认。


---

## 41. ObsUpload

- **name**: `obs-upload`
- **creator**: wukong_admin
- **被引用**: 105272
- **版本**: 1.1.4

# obs-upload

上传本地制品到 OBS，支持断点续传和分段并发上传。

- 单文件、目录递归、Glob 通配符三种路径输入方式
- 正则表达式过滤：支持 include-regex 包含和 exclude-regex 排除
- 无文件时行为可配置：warn / error / ignore
- 模板前缀自动按仓库/分支/构建号组织对象路径
- 大文件自动分片并发上传，可自定义分片大小和并发数
- 断点续传，网络中断后可从上次位置继续
- 支持匿名访问公共读写桶（无需 AK/SK），访问私有桶或公共读桶需提供 AK/SK 认证

## 目录

- [Usage](#usage)
- [artifact-path 路径类型说明](#artifact-path-路径类型说明)
- [Inputs](#inputs)
- [Outputs](#outputs)
- [认证模式说明](#认证模式说明)

## Usage

### 基础上传（AK/SK 认证）

```yaml
name: obs-upload
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  upload:
    name: 上传制品
    select: selected_by_default
    jobs:
      UPLOAD:
        name: 上传到OBS
        select: selected_by_default
        needs: []
        steps:
          - name: 上传制品
            uses: obs-upload
            with:
              endpoint: "obs.cn-north-4.myhuaweicloud.com"
              bucket: "my-bucket"
              access-key: "${{ Secret.OBS_AK }}"
              secret-key: "${{ Secret.OBS_SK }}"
              artifact-path: "target/app.jar"
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### 匿名上传公共读写桶（无需 AK/SK）

当目标桶的 ACL 设置为"公共读写"时，可省略 `access-key` 和 `secret-key`，插件将以匿名模式上传：

```yaml
- name: 上传到公共读写桶
  uses: obs-upload
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "public-read-write-bucket"
    artifact-path: "target/app.jar"
```

> **注意**：匿名模式仅适用于公共读写桶。公共读桶或私有桶不支持匿名上传，未提供 AK/SK 时将返回 403 错误并提示需要认证凭据。公共读写桶存在安全风险，请谨慎使用。

### 上传整个目录

```yaml
- name: 上传目录
  uses: obs-upload
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.OBS_AK }}"
    secret-key: "${{ Secret.OBS_SK }}"
    artifact-path: "dist/"
    object-prefix: "releases/v1/"
```

`dist/` 目录下的所有文件将递归上传，保留子目录结构。例如 `dist/lib/app.jar` → OBS key 为 `releases/v1/lib/app.jar`。

### 使用 Glob 通配符

```yaml
- name: Glob 模式上传
  uses: obs-upload
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.OBS_AK }}"
    secret-key: "${{ Secret.OBS_SK }}"
    artifact-path: "dist/**/*.jar"
    object-prefix: "releases/v1/"
```

匹配 `dist/` 下所有子目录中的 `.jar` 文件，保留目录结构。

### 多路径 + 正则排除

```yaml
- name: 多路径上传+排除
  uses: obs-upload
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.OBS_AK }}"
    secret-key: "${{ Secret.OBS_SK }}"
    artifact-path: |
      build/libs/*.jar
      build/reports/
    exclude-regex: |
      -sources\.jar$
      -javadoc\.jar$
    object-prefix-template: "${trigger_repo}/${trigger_branch}/${build_no}/"
```

### 正则包含 + 排除组合

```yaml
- name: 正则过滤上传
  uses: obs-upload
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.OBS_AK }}"
    secret-key: "${{ Secret.OBS_SK }}"
    artifact-path: "dist/"
    include-regex: '\.(jar|zip)$'
    exclude-regex: '/test/'
    object-prefix: "releases/v1/"
    if-no-files-found: error
```

### 临时凭证 + 大文件分片

```yaml
- name: 临时凭证上传
  uses: obs-upload
  with:
    endpoint: "obs.cn-north-4.myhuaweicloud.com"
    bucket: "my-bucket"
    access-key: "${{ Secret.TMP_AK }}"
    secret-key: "${{ Secret.TMP_SK }}"
    security-token: "${{ Secret.SECURITY_TOKEN }}"
    artifact-path: "target/large-file.bin"
    part-size: "52428800"
    task-num: "10"
```

## artifact-path 路径类型说明

支持三种输入方式，每行一个：

| 输入方式 | 示例 | 说明 |
|----------|------|------|
| 单个文件 | `build/app.jar` | 与旧版行为一致，OBS key 为 `prefix/app.jar` |
| 目录 | `dist/` | 递归上传目录下所有文件，保留子目录结构 |
| Glob 模式 | `dist/**/*.jar` | 匹配的文件保留子目录结构 |

**OBS key 计算规则：**

| 输入类型 | 输入示例 | 文件 | OBS key |
|----------|---------|------|---------|
| 单个文件 | `build/app.jar` | — | `prefix/app.jar` |
| 目录 | `dist/` | `dist/lib/app.jar` | `prefix/lib/app.jar` |
| Glob | `dist/**/*.jar` | `dist/lib/app.jar` | `prefix/lib/app.jar` |

**边界情况：**

| 场景 | 行为 |
|------|------|
| 空目录 | 报错 `Directory is empty` |
| Glob 无匹配 | 取 `if-no-files-found` 配置 |
| 路径不存在 | 报错 `Artifact path not found` |
| 所有文件被正则过滤 | 取 `if-no-files-found` 配置 |

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| endpoint | 是 | — | OBS endpoint，如 `obs.cn-north-4.myhuaweicloud.com` |
| bucket | 是 | — | OBS 桶名 |
| access-key | 否 | — | Access Key ID，访问公共读写桶时可省略 |
| secret-key | 否 | — | Secret Access Key，访问公共读写桶时可省略 |
| security-token | 否 | — | 临时安全令牌，使用临时 AK/SK 时必填；匿名模式下不可使用 |
| artifact-path | 是 | — | 制品路径（文件、目录或 glob 模式，每行一个） |
| include-regex | 否 | — | 包含正则（每行一个），只上传匹配的文件 |
| exclude-regex | 否 | — | 排除正则（每行一个），排除匹配的文件，优先级高于 include-regex |
| if-no-files-found | 否 | warn | 无文件匹配时的行为：warn / error / ignore |
| object-prefix | 否 | artifacts/ | 对象前缀 |
| object-prefix-template | 否 | — | 对象前缀模板，支持 `${trigger_repo}`、`${trigger_branch}`、`${build_no}` 变量，优先于 object-prefix |
| multipart-threshold-bytes | 否 | — | 分块上传阈值（字节），超过此大小自动分片 |
| part-size | 否 | 9437184 | 分片大小（字节），留空时代码内默认 9MB |
| task-num | 否 | 5 | 并发上传任务数，留空时代码内默认 5 |
| enable-checkpoint | 否 | true | 启用断点续传 |
| max-retry-count | 否 | 3 | 失败重试次数 |
| trigger-repo | 否 | — | 触发仓库名覆盖 |
| trigger-branch | 否 | — | 触发分支覆盖 |
| trigger-commit | 否 | — | 触发提交覆盖 |
| overwrite | 否 | true | 是否覆盖已存在的对象 |
| fail-on-error | 否 | true | 上传失败是否中断步骤 |

> **AK/SK 规则**：`access-key` 和 `secret-key` 必须同时提供或同时省略。仅提供其中一个将导致校验错误。

## Outputs

| 输出 | 说明 |
|------|------|
| primary-key | 首个上传对象 Key |
| primary-url | 首个上传对象 URL |
| uploaded-count | 上传文件数量 |
| result-summary | 上传结果摘要 |

## 认证模式说明

插件根据是否提供 AK/SK 自动判断认证模式：

| 模式 | 条件 | 适用场景 | 错误提示 |
|------|------|---------|---------|
| **AK/SK 认证** | access-key 和 secret-key 均非空 | 私有桶、公共读桶、公共读写桶 | 认证失败时提示检查凭据是否正确 |
| **匿名访问** | access-key 和 secret-key 均为空 | 公共读写桶（桶 ACL 设置为公共读写） | 403 时提示目标桶可能为公共读桶或私有桶，不支持匿名上传 |

执行报告的 `[基本信息]` 区块会显示当前认证模式，便于排障确认。

---

## 42. DockerLogin

- **name**: `docker-login`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.2.3

# docker-login

将 Docker Registry 凭证写入认证文件，供 Kaniko 或其他容器工具读取，无需 Docker CLI。

> **GitCode 环境**：`runs-on: ['codearts-hosted', 'ubuntu-latest', 'x64', 'large']` 已预装 Kaniko，无需额外安装 `setup-kaniko`，可直接使用 `docker-login` + `docker-build-push`。

## 使用方式

### 登录华为云 SWR（长期凭证）

SWR 长期登录凭证格式：用户名 `bearertoken@{租户ID}`，密码为 Base64 编码的长期 token：

```yaml
steps:
  - name: docker-login
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'bearertoken@{租户ID}'
      password: '${{ secrets.SWR_LONG_TOKEN }}'
      use-sudo: true
```

对应的 `docker login` 命令格式：
```bash
docker login -u bearertoken@{租户ID} -p {长期token} swr.cn-north-4.myhuaweicloud.com
```

### 登录华为云 SWR（短期凭证）

SWR 短期登录凭证格式：用户名 `区域@{AK}`，密码为 SK 对应的短期 token：

```yaml
steps:
  - name: docker-login
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'cn-north-4@{AK}'
      password: '${{ secrets.SWR_SHORT_TOKEN }}'
      use-sudo: true
```

对应的 `docker login` 命令格式：
```bash
docker login -u cn-north-4@HST3W0MOUVMCUNRQIZOE -p <短期token> swr.cn-north-4.myhuaweicloud.com
```

> **注意**：长期凭证有效期长，适合 CI/CD 流水线固定使用；短期凭证定期过期，需要定期更新。

### 登录其他仓库

```yaml
steps:
  - name: docker-login
    uses: docker-login
    with:
      registry: 'harbor.example.com'
      username: '${{ secrets.REGISTRY_USER }}'
      password: '${{ secrets.REGISTRY_PASS }}'
```

不填 `registry` 时默认登录 Docker Hub：
```yaml
steps:
  - name: docker-login
    uses: docker-login
    with:
      username: '${{ secrets.DOCKERHUB_USER }}'
      password: '${{ secrets.DOCKERHUB_TOKEN }}'
```

### 多仓库登录

```yaml
steps:
  - name: docker-login-dockerhub
    uses: docker-login
    with:
      username: '${{ secrets.DOCKERHUB_USER }}'
      password: '${{ secrets.DOCKERHUB_TOKEN }}'

  - name: docker-login-swr
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'bearertoken@{租户ID}'
      password: '${{ secrets.SWR_LONG_TOKEN }}'
      use-sudo: true
```

### 受限环境 sudo 模式

CI 环境中 Kaniko 需要 sudo 运行时，开启 `use-sudo` 将认证文件复制到 `/kaniko/.docker/`：

```yaml
steps:
  - name: docker-login
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'bearertoken@{租户ID}'
      password: '${{ secrets.SWR_LONG_TOKEN }}'
      use-sudo: true

  - name: docker-build-push
    uses: docker-build-push
    with:
      context: '.'
      dockerfile: 'Dockerfile'
      tags: 'swr.cn-north-4.myhuaweicloud.com/pipeline/app:latest'
      use-sudo: true
```

## 参数

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `registry` | 否 | Docker Hub | Registry 地址 |
| `username` | 是 | - | 认证用户名 |
| `password` | 是 | - | 认证密码或 token |
| `use-sudo` | 否 | `false` | sudo 模式，复制 config.json 到 `/kaniko/.docker/` |
| `fail-on-error` | 否 | `true` | 登录失败是否中断步骤 |
| `verbose` | 否 | `false` | 详细日志输出（密码始终脱敏） |
| `dry-run` | 否 | `false` | 试运行模式，仅验证输入不写入 config.json |

## Outputs

| 输出 | 说明 |
|------|------|
| `registry` | 实际登录的 Registry 地址 |
| `login-status` | 登录结果：success 或 failed |
| `docker-config-path` | 包含 config.json 的目录路径（用于 DOCKER_CONFIG 环境变量） |

## 华为云 SWR 凭证格式说明

| 凭证类型 | 用户名格式 | 密码格式 | 有效期 | 适用场景 |
|---------|-----------|---------|------|---------|
| 长期凭证 | `bearertoken@{租户ID}` | Base64 编码长期 token | 长期有效 | CI/CD 固定流水线 |
| `短期凭证` | `{区域}@{AK}` | SK 生成的短期 token | 定期过期 | 临时调试、需定期更新 |

### docker login 命令对照

```bash
# 长期凭证
docker login -u bearertoken@{租户ID} -p {长期token} swr.cn-north-4.myhuaweicloud.com

# 短期凭证
docker login -u cn-north-4@{AK} -p {短期token} swr.cn-north-4.myhuaweicloud.com
```

---

## 43. DockerBuildPush

- **name**: `docker-build-push`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.2.5

# docker-build-push

使用 Kaniko 构建并推送 Docker 镜像到 Registry，无需 Docker daemon。

> **GitCode 环境**：`runs-on: ['codearts-hosted', 'ubuntu-latest', 'x64', 'large']` 已预装 Kaniko，无需额外安装 `setup-kaniko`，可直接使用 `docker-login` + `docker-build-push`。

## 与 Kaniko 的关系

本插件底层调用 Kaniko executor 完成 Dockerfile 解析、镜像构建和推送。流水线运行环境需满足以下任一条件：

1. 使用 GitCode CodeArts 托管运行环境（`runs-on: ['codearts-hosted', 'ubuntu-latest', 'x64', 'large']`），Kaniko 已预装在 `/usr/local/bin/kaniko`，可直接使用。
2. 自托管运行环境需自行安装 Kaniko executor，或通过 `kaniko-path` 参数指定 Kaniko 可执行文件路径。

登录步骤（`docker-login`）生成的 `config.json` 会通过 `DOCKER_CONFIG` 环境变量或 `/kaniko/.docker/config.json`（sudo 模式）传递给 Kaniko，用于 Registry 认证。

## 前置条件

需要先完成 Registry 登录，典型流水线顺序：

```yaml
steps:
  - name: docker-login
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'bearertoken@{租户ID}'
      password: '${{ secrets.SWR_TOKEN }}'
      use-sudo: true
  - name: docker-build-push
    uses: docker-build-push
    with:
      tags: 'swr.cn-north-4.myhuaweicloud.com/pipeline/app:latest'
```

## 使用方式

### 示例 1：构建并推送到华为云 SWR（完整流水线）

包含代码检出、JDK 编译、登录、构建推送的完整流程：

```yaml
steps:
  - name: checkout
    uses: checkout
    with:
      repository: https://test.gitcode.net/xxx/app.git
      ref: master
      token: xxx
      path: app

  - name: Setup JDK
    uses: setup-jdk
    with:
      jdk-version: '17'
      maven-version: '3.9.6'

  - name: Build jar
    run: |-
      cd app && mvn package -DskipTests

  - name: Docker Login SWR
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'bearertoken@{租户ID}'
      password: '${{ secrets.SWR_LONG_TOKEN }}'
      use-sudo: true

  - name: Build and Push
    uses: docker-build-push
    with:
      context: '.'
      dockerfile: 'Dockerfile'
      tags: 'swr.cn-north-4.myhuaweicloud.com/pipeline/jdk-test:latest'
      push: true
      workdir: app
      use-sudo: true
```

### 示例 2：只构建不推送

本地测试场景，仅构建镜像不推送到 Registry：

```yaml
steps:
  - name: docker-build-push
    uses: docker-build-push
    with:
      context: '.'
      dockerfile: 'Dockerfile'
      tags: 'myapp:latest'
      push: false
```

### 示例 3：多标签推送

同时为镜像打多个 tag（如版本号 + latest），推送到同一 Registry：

```yaml
steps:
  - name: docker-build-push
    uses: docker-build-push
    with:
      context: '.'
      dockerfile: 'Dockerfile'
      tags: 'swr.cn-north-4.myhuaweicloud.com/pipeline/app:v1.0.0,swr.cn-north-4.myhuaweicloud.com/pipeline/app:latest'
      push: true
      use-sudo: true
```

### 示例 4：多仓库推送

先登录多个仓库，然后用逗号分隔 tags，将镜像同时推送到不同 Registry：

```yaml
steps:
  - name: docker-login-dockerhub
    uses: docker-login
    with:
      username: '${{ secrets.DOCKERHUB_USER }}'
      password: '${{ secrets.DOCKERHUB_TOKEN }}'

  - name: docker-login-swr
    uses: docker-login
    with:
      registry: 'swr.cn-north-4.myhuaweicloud.com'
      username: 'bearertoken@{租户ID}'
      password: '${{ secrets.SWR_TOKEN }}'
      use-sudo: true

  - name: docker-build-push
    uses: docker-build-push
    with:
      tags: 'myuser/app:v1.0.0,swr.cn-north-4.myhuaweicloud.com/pipeline/app:v1.0.0'
      push: true
      use-sudo: true
```

### 示例 5：指定工作目录

`workdir` 指定构建上下文所在子目录（包含 Dockerfile 的目录）：

```yaml
steps:
  - name: docker-build-push
    uses: docker-build-push
    with:
      workdir: my-service
      dockerfile: 'Dockerfile'
      tags: 'myapp:latest'
      push: true
```

## 参数

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `context` | 否 | `.` | 构建上下文路径（相对于工作目录） |
| `dockerfile` | 否 | `Dockerfile` | Dockerfile 路径（相对于 context） |
| `tags` | 否 | - | 镜像标签，多个换行分隔（如 `registry/repo:tag`） |
| `push` | 否 | `true` | 是否推送镜像（`false` 时仅构建不推送） |
| `build-args` | 否 | - | 构建参数，`KEY=VALUE` 格式，多个换行分隔 |
| `labels` | 否 | - | OCI 标签，`KEY=VALUE` 格式，多个换行分隔 |
| `target` | 否 | - | 多阶段构建目标阶段 |
| `cache` | 否 | `false` | 是否启用构建缓存 |
| `cache-ref` | 否 | - | 缓存仓库地址（启用缓存时必填） |
| `verbose` | 否 | `false` | 详细日志输出（显示 kaniko debug 信息，已过滤无关噪音） |
| `workdir` | 否 | 自动检测 | 工作目录（context 和 dockerfile 的基准路径，默认自动检测 ATOMGIT_WORKSPACE） |
| `kaniko-path` | 否 | `''` | Kaniko executor 可执行文件路径（留空时默认 `/usr/local/bin/kaniko`，也可通过 KANIKO_EXECUTOR_PATH 环境变量指定） |
| `run-as-root` | 否 | `false` | 非 root 环境下用 unshare 以 root 身份运行 kaniko |
| `use-sudo` | 否 | `false` | sudo 模式运行 Kaniko |
| `docker-config` | 否 | 自动检测 | Docker config.json 所在目录路径（覆盖 DOCKER_CONFIG 环境变量） |
| `ignore-paths` | 否 | - | Kaniko 忽略的路径，多个换行分隔 |
| `registry-mirror` | 否 | - | Kaniko registry mirror（格式: `host:port`，Docker Hub 不可达时使用） |

## Outputs

| 输出 | 说明 |
|------|------|
| `push-status` | 推送状态：success / failed |
| `image-tags` | 镜像标签列表（逗号分隔） |
| `digest` | 镜像 digest（sha256:...） |
| `image-id` | 镜像 ID |

## 镜像地址格式

本插件基于 Kaniko，支持任意标准 Docker Registry（华为云 SWR、阿里云 ACR、Docker Hub、私有 Registry 等）。

### 华为云 SWR

```
swr.{区域}.myhuaweicloud.com/{组织名}/{镜像名}:{标签}
```

示例：
- `swr.cn-north-4.myhuaweicloud.com/pipeline/jdk-test:latest`
- `swr.cn-north-4.myhuaweicloud.com/pipeline/jdk-test:v1.0.0`

### 阿里云 ACR

```
registry.{区域}.aliyuncs.com/{命名空间}/{镜像名}:{标签}
```

示例：
- `registry.cn-hangzhou.aliyuncs.com/myns/app:v1.0.0`

### Docker Hub

```
{用户名}/{镜像名}:{标签}
```

示例：
- `myuser/myapp:latest`

### 私有 Registry

```
{host}:{port}/{镜像名}:{标签}
```

示例：
- `harbor.example.com:5000/myapp:v1.0.0`

> **注意**：推送前必须先通过 `docker-login` 完成对应 Registry 的认证。

## 典型流水线组合

| 步骤 | 插件 | 说明 |
|------|------|------|
| 1 | `checkout` | 检出代码 |
| 2 | `setup-jdk` | 安装 JDK + Maven |
| 3 | `run` | 编译打包 |
| 4 | `docker-login` | 登录镜像仓库 |
| 5 | `docker-build-push` | 构建推送镜像 |
| 6 | `notify` | 通知构建结果 |

---

## 44. BuildAccelerate

- **name**: `build-accelerate`
- **creator**: wukong_admin
- **被引用**: 51809
- **版本**: 2.2.7

# build-accelerate

> **版本：2.1.9（无计时套餐）**

C/C++ 构建加速插件。下载安装构建加速工具，配置远端缓存服务器，实现增量编译加速。

---

## 目录

- [功能](#功能)
- [注意事项](#注意事项)
- [Usage](#usage)
- [Inputs](#inputs)
- [Outputs](#outputs)

---

## 功能

| 特性 | 说明 |
|------|------|
| 加速对象 | C/C++ 编译 |
| 加速原理 | 缓存编译产物 |
| 远端缓存 | 配置共享缓存服务器池，跨流水线复用缓存 |
| 退出码透传 | 构建命令退出码原样透传，非 0 终止流水线 |
| 自定义安装目录 | 支持 `install-dir` 指定加速工具安装路径，规避 `/tmp` 权限问题 |

---

## 注意事项

### 构建命令执行机制

构建加速工具内部通过 `bash -c` 包裹用户命令执行，因此：

- 命令中的相对路径会被自动解析为绝对路径
- 建议使用 `BuildAccelerate` 关键字后直接跟构建命令，如 `BuildAccelerate make -j$(nproc)`

### 缓存要求

加速工具仅缓存**纯编译步骤**（`gcc -c` / `g++ -c`），不缓存链接步骤。编译命令必须包含 `-c` 参数：

```bash
# 会被缓存
gcc -c main.c -o main.o
g++ -c src/main.cpp -o build/main.o

# 不会被缓存（skip）
gcc main.c -o main           # 缺少 -c，编译+链接一步完成
g++ src/main.cpp -o demo     # 缺少 -c，跳过缓存
```

使用 CMake/Makefile 构建时，内部会自动拆分为编译步骤和链接步骤，可正常加速。

### 退出码透传

构建命令的退出码原样透传，不做转换：命令返回 0 视为成功；返回非 0 退出码时，流水线按通用语义终止该步骤。若需在构建命令返回非 0 后继续执行后续命令，请在用户脚本内自行控制（例如 `set +e` 或显式捕获退出码）。

### 自定义安装目录

默认安装到 `/tmp/codearts`。当运行环境 `/tmp` 权限受限时，可通过 `install-dir` 指定其他可写目录：

```yaml
- name: Build accelerate
  uses: build-accelerate
  with:
    command: 'cd project && BuildAccelerate make -j$(nproc)'
    install-dir: '/tmp/setup-buildaccelerate'
```

> 指定 `install-dir` 后，加速工具及其命令路径会统一指向该目录，后续步骤中直接使用 `BuildAccelerate` 关键字即可，无需额外配置。



## Usage

`command` 可直接在插件中完成项目自身的构建命令，`BuildAccelerate` 是加速关键字，用户只需在原有构建命令前加上 `BuildAccelerate` 即可启用加速。

### 常见构建场景

```yaml
# Makefile 项目
command: 'cd project && BuildAccelerate make -j$(nproc)'

# CMake 项目
command: |
  cd project && mkdir -p build && cd build
  cmake .. -DBUILD_TESTS=OFF
  BuildAccelerate make -j$(nproc)

# 自定义构建脚本
command: 'cd project && BuildAccelerate ./build.sh'

# 仅编译指定文件（需 -c 参数）
command: 'BuildAccelerate g++ -c src/main.cpp -o build/main.o'
```

> **核心原则**：`BuildAccelerate` 后面跟的就是项目原本的构建命令，无需改变构建流程，只需在编译命令前加上 `BuildAccelerate` 关键字。

### 完整流水线示例

```yaml
name: build-accelerate-demo
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: build-accelerate-test
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: build-accelerate
        select: selected_by_default
        needs: []
        steps:
          - name: checkout
            uses: official_checkout
            with:
              repository: https://example.com/org/project.git
              ref: main
              token: ${{ secrets.REPO_TOKEN }}
              path: project

          - name: Build accelerate
            uses: build-accelerate
            with:
              command: |
                cd project
                mkdir -p build
                cd build
                cmake .. -DBUILD_TESTS=OFF -DBUILD_PERF_TESTS=OFF
                BuildAccelerate make -j$(nproc)
              AC_CACHE_DIR: '/tmp/cloudcache'
              AC_BUILD_DIR: 'project'
        if: "${{ default() }}"
        runs-on: ['codearts-hosted', 'ubuntu-latest', 'x64', 'large']
```

### 仅下载安装加速工具

不执行构建，仅安装加速工具。适用于在其他 shell 插件中手动执行加速构建命令的场景：

```yaml
- name: Setup build accelerator
  uses: build-accelerate
  with:
    command: ''
    AC_SERVER_IP: ${{ secrets.AC_SERVER_IP }}

# 在其他 shell 步骤中使用 BuildAccelerate
- name: Build with shell
  uses: official_shell
  with:
    OFFICIAL_SHELL_SCRIPT_INPUT: |
      cd project
      mkdir -p build && cd build
      cmake .. -DBUILD_TESTS=OFF
      BuildAccelerate make -j$(nproc)
```

---

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `command` | 否 | — | 构建命令，为空时仅安装加速工具 |
| `AC_SERVER_IP` | 否 | `127.0.0.1` | 远端缓存服务器地址，多个用 `:` 分隔 |
| `AC_CACHE_DIR` | 否 | `/tmp/codearts_cache` | 本地缓存目录 |
| `AC_BUILD_DIR` | 否 | 无 | 代码根目录，用于跨路径缓存命中 |
| `AC_CACHE_MAXSIZE` | 否 | `50G` | 缓存目录最大存储空间 |
| `AC_VERSION` | 否 | `1.0` | 加速工具版本号 |
| `install-dir` | 否 | `/tmp/codearts` | 加速工具安装目录。`/tmp` 权限受限时可指定其他可写目录，例如 `/tmp/setup-buildaccelerate` |

---

## Outputs

本插件无 outputs 定义（无计时套餐，不输出耗时记录等变量）。


---

## 45. BuildCache

- **name**: `build-cache`
- **creator**: wukong_admin
- **被引用**: 16
- **版本**: 1.1.2

# cache

流水线缓存插件，通过华为云 OBS 对象存储实现构建产物缓存恢复与保存，加速流水线执行。

---

## 目录

- [About](#about)
- [Usage](#usage)
- [Inputs](#inputs)
- [Outputs](#outputs)

---

## About

cache 是流水线缓存插件，支持远程（OBS）和本地两种缓存模式：

1. **main 阶段**：检查缓存是否存在，命中则下载解压到本地路径
2. **post 阶段**：缓存未命中时，压缩本地目录并上传到 OBS

| 特性 | 说明 |
|------|------|
| 缓存模式 | Remote（OBS 远程）/ Local（本地磁盘） |
| 存储后端 | 华为云 OBS SDK |
| 安全 | 路径遍历检测 + key 清洗 + 系统目录保护 |
| Mock 模式 | 支持 MOCK_STORAGE_DIR 本地测试 |
| 输出文件 | `/tmp/cache-output.json`（cache_hit 状态） |

---

## Usage

### 基础用法：Remote 模式缓存

```yaml
name: cache-demo
on:
  push:
    branches: ["master"]
  workflow_dispatch:

stages:
  stage1:
    name: 构建
    select: selected_by_default
    jobs:
      JOB_BUILD:
        name: 构建
        select: selected_by_default
        needs: []
        steps:
          - name: build-cache
            uses: build-cache
            with:
              name: 'my-cache'
              endpoint: 'obs.cn-north-4.myhuaweicloud.com'
              bucket: 'your_bucket'
              access-key: 'your_access_key'
              secret-key: 'your_secret_key'
              key: 'cache-test'
              path: '/tmp/cache-test'
              mode: 'Remote'
          - name: Build
            run: |-
              CACHE_HIT="false"
              if [ -f /tmp/cache-output.json ]; then
                CACHE_HIT=$(cat /tmp/cache-output.json | grep -o '"cache_hit"[[:space:]]*:[[:space:]]*"[^"]*"' | head -1 | cut -d'"' -f4)
              fi
              if [ "$CACHE_HIT" = "true" ]; then
                echo "缓存已命中，跳过构建"
                exit 0
              fi
              echo "缓存未命中，构建中..."
              mkdir -p /tmp/cache-test
              echo "Cache test $(date)" > /tmp/cache-test/test.txt
        if: "${{ default() }}"
        runs-on:
          - default
    pre:
      - type: auto
```

### Local 模式缓存

```yaml
- name: build-cache
  uses: build-cache
  with:
    name: 'local-cache'
    endpoint: 'localhost'
    bucket: 'local'
    access-key: 'none'
    secret-key: 'none'
    key: 'my-key'
    path: '/tmp/cache-test'
    mode: 'Local'
```

---

## Inputs

| 参数 | 必填 | 默认值 | 说明 |
|------|:--:|------|------|
| `name` | 是 | — | 缓存标识名称 |
| `endpoint` | 是 | — | OBS 桶的 endpoint 地址 |
| `bucket` | 是 | — | OBS 桶名称 |
| `access-key` | 是 | — | OBS 访问密钥 AK |
| `secret-key` | 是 | — | OBS 访问密钥 SK |
| `key` | 是 | — | 缓存文件在 OBS 中的存储路径 |
| `path` | 是 | — | 执行机本地缓存文件路径 |
| `mode` | 否 | `Remote` | 缓存模式：`Remote`（远程 OBS）或 `Local`（本地） |

> **post 行为**：post 阶段仅在 main 阶段成功时执行（`post-if: success()`）。若构建步骤失败，post 阶段不会触发，缓存不会上传。

---

## Outputs

| 输出 | 说明 |
|------|------|
| `cache_hit` | 是否命中缓存，`true` 表示命中，`false` 表示未命中 |


---

## 46. UploadArtifact

- **name**: `upload-artifact`
- **creator**: wukong_admin
- **被引用**: 972
- **版本**: 1.0.16

# upload-artifact

将工作流产物上传到**Pipeline 制品服务**。

---

## 使用示例

### 上传目录

```yaml
- name: 上传到 Artifact 服务
  id: upload
  identifier: upload # steps.xxx.outputs.xxx 使用
  uses: upload-artifact
  with:
    name: simple-artifact
    path: /tmp/simple-e2e/
    overwrite: true # 覆盖同名制品，否则报错
    if-no-files-found: error
    retention-days: 1
```

### 读取输出

```yaml
- run: |
    echo "artifact-id=${{ steps.upload.outputs.artifact-id }}"
    echo "artifact-url=${{ steps.upload.outputs.artifact-url }}"
    echo "artifact-digest=${{ steps.upload.outputs.artifact-digest }}"
```

---

## Inputs

| 输入名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `name` | 否 | `artifact` | Artifact 名称 |
| `path` | **是** | - | 文件/目录路径（支持通配符；相对路径相对工作区） |
| `if-no-files-found` | 否 | `warn` | 无文件时：`warn` / `error` / `ignore` |
| `retention-days` | 否 | `0` | 保留天数（`0` = 服务端默认） |
| `compression-level` | 否 | `6` | 压缩级别 0–9 |
| `overwrite` | 否 | `false` | 是否覆盖同名 Artifact |
| `include-hidden-files` | 否 | `false` | 是否包含隐藏文件 |

---

## Outputs

| 输出名 | 说明 |
|--------|------|
| `artifact-id` | Artifact 唯一 ID |
| `artifact-url` | 制品页面 URL；门户未配置时回退为对象存储路径 |
| `artifact-digest` | SHA-256 摘要 |

通过 `steps.<id>.outputs.<name>` 引用，例如 `${{ steps.upload.outputs.artifact-id }}`。

---

## 注意

- 同一流水线（`workflow_id`）下同名 Artifact 已存在且未设 `overwrite: true` 时会失败。


---

## 47. DownloadArtifact

- **name**: `download-artifact`
- **creator**: wukong_admin
- **被引用**: 952
- **版本**: 1.0.7

# download-artifact

从**Pipeline 制品服务**下载工作流产物。

---

## 使用示例

### 按 Artifact ID 下载

```yaml
- name: 从 Artifact 服务下载
  id: download
  identifier: download # steps.xxx.outputs.xxx 使用
  uses: download-artifact
  with:
    artifact-ids: ${{ steps.upload.outputs.artifact-id }}
    path: ./simple-download
```

多个 ID 用逗号分隔，例如 `1,2,3`。

### 按名称下载

```yaml
- name: 从 Artifact 服务下载
  id: download
  identifier: download
  uses: download-artifact
  with:
    name: simple-artifact
    path: ./simple-download
```

### 读取输出

```yaml
- run: |
    echo "download-path=${{ steps.download.outputs.download-path }}"
```

---

## Inputs

| 输入名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `artifact-ids` | 否 | - | 按 ID 下载（多个用逗号分隔）；**不可与 `name` 同时使用** |
| `name` | 否 | - | 按名称下载；为空且未指定 `artifact-ids` / `pattern` 时下载全部制品 |
| `path` | 否 | `.` | 下载目标目录（相对路径相对工作区） |
| `pattern` | 否 | - | 按名称 glob 过滤 |
| `merge-multiple` | 否 | `false` | 下载多个制品时是否合并到同一目录 |
| `skip-decompress` | 否 | `false` | 是否跳过解压 |
| `digest-mismatch` | 否 | `error` | 摘要校验失败时：`error` / `warn` / `info` / `ignore` |

---

## Outputs

| 输出名 | 说明 |
|--------|------|
| `download-path` | 下载目标目录的绝对路径 |

通过 `steps.<id>.outputs.<name>` 引用，例如 `${{ steps.download.outputs.download-path }}`。

---

## 注意

- 不强制依赖 `upload-artifact` 插件本身；只要制品服务中已有对应制品即可下载。常见做法是同流水线内先用 `upload-artifact` 上传。
- 使用 `artifact-ids` 时，ID 一般来自同 job 内上传步骤的输出，例如 `${{ steps.upload.outputs.artifact-id }}`（要求该步骤配置了 `id` / `identifier`）。
- `name` 与 `artifact-ids` 不能同时指定。
- 未指定 `name` / `artifact-ids` / `pattern` 时，会下载当前流水线范围内的全部制品。
- 下载多个制品且 `merge-multiple: false`（默认）时，每个制品会落在以制品名命名的子目录中。


---

## 48. AtomgitCache

- **name**: `atomgit-cache`
- **creator**: wukong_admin
- **被引用**: 114
- **版本**: 1.0.6

# Pipeline Cache Action

对标 [actions/cache@v5](https://github.com/actions/cache) 的 GitHub Actions 缓存步骤，支持独立 restore/save 入口。

## 存储与上传（华为云 OBS）

- **Save（post）**：固定为 **Twirp `CreateCacheEntry` → 对 `signed_upload_url` 整包 HTTP(S) PUT → `FinalizeCacheEntryUpload`**，适用于 **华为云 OBS**（及同类）网关签发的预签名 URL；**不使用** `@azure/storage-blob` 上传。  
- **Restore（main）**：仍通过 **`@actions/cache.restoreCache`**（Twirp 取 `signed_download_url` 后下载；非 Azure Blob 主机名时走 HTTP 分块）。  
- 若 OBS 预签名要求固定 **`Content-Type`**，请在 Runner 上设置 **`PIPELINE_CACHE_OBS_PUT_CONTENT_TYPE`**（须与网关签发约束一致）。详见 **`docs/cache-platform-ai-executable-spec.md`** §10.1、§10.1.1、§3.1。

## 使用方式

### 主入口（restore + save 联动）

```yaml
- uses: actions/cache@v5
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 独立 Restore Only

```yaml
- uses: ./path/to/action-restore-only.yml
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
    restore-keys: |
      ${{ runner.os }}-node-
```

### 独立 Save Only

```yaml
- uses: ./path/to/action-save-only.yml
  with:
    path: node_modules
    key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
```

## 输入参数

| 参数 | 必需 | 默认值 | 说明 |
|------|------|--------|------|
| `path` | 是 | - | 要缓存的路径（文件、目录或通配符） |
| `key` | 是 | - | 缓存的唯一 key |
| `restore-keys` | 否 | - | 查找缓存时的 fallback key 列表 |
| `enableCrossOsArchive` | 否 | false | 是否允许跨平台恢复缓存 |
| `fail-on-cache-miss` | 否 | false | 缓存未命中时是否失败 |
| `lookup-only` | 否 | false | 仅检查缓存是否存在，不下载 |

## 输出

| 输出 | 说明 |
|------|------|
| `cache-hit` | 是否命中缓存 |
| `cache-id` | 保存缓存后的 ID（save only） |

## AtomGit 兼容性

在 AtomGit 自托管 Runner 上运行时，所有非空 `ATOMGIT_<X>` 会在 action 进程入口被写入对应 `GITHUB_<X>`（ATOMGIT 优先，GITHUB 兜底），下游逻辑统一从 `GITHUB_<X>` 读取。例如 `ATOMGIT_REPOSITORY` 会写入 `GITHUB_REPOSITORY`、`ATOMGIT_REF` 会写入 `GITHUB_REF`，无需在 workflow 中再做手动赋值。

不处理 `RUNNER_*` 前缀。`ACTIONS_*` 见下。

**`ACTIONS_*`（与 upload-artifact 对齐）**：bootstrap 会将非空 `ATOMGIT_ACTIONS_RUNTIME_TOKEN` / `ATOMGIT_ACTIONS_RESULTS_URL` 同步到 `ACTIONS_*`（仅当后者为空）；各读点并对 `ATOMGIT_ACTIONS_*` 做读时回退。未配置 URL 时由 `ACTIONS_RUNTIME_TOKEN` 拉取 `runtime-config?plugin=cache` 写入 `ACTIONS_RESULTS_URL`。

**Runner 必做**：对插件 **`atomgit-cache`** 在 spawn Node 时注入与 **`upload-artifact` / `download-artifact` 相同** 的 runtime 环境（不必在 YAML 里写 `server-url`）。主步骤 `dist/restore/index.js` 与 **post** `dist/save/index.js` 均需注入。

### 别名作用域 vs Runner 平台职责

本 alias **只在本 action 子进程内** 改写 `process.env`，下面这些场景**仍依赖 AtomGit Runner 自行做兼容暴露**，本 action 无法替平台兜底：

- **工作流上下文表达式 `${{ github.* }}`**：在 action 执行**之前**由 runner 表达式引擎解析，与 `process.env` 改写不在同一时序。AtomGit Runner 必须暴露 `github` 上下文（或在表达式层做 `atomgit` → `github` 映射），才能让用户在 YAML 里继续使用 `${{ github.run_id }}` 这类写法。
- **action 输入注入（`with:` → `INPUT_*`）**：runner 必须以 `INPUT_KEY` / `INPUT_PATH` 等**字面量**注入到子进程，`@actions/core` 的 `getInput` 只认这些固定名。
- **同 Job 内的 `run:` shell 步骤、第三方 action**：在自己的子进程内独立运行，看不到本 action 的 `process.env` 改写。建议 AtomGit Runner 同时双注入 `GITHUB_*` 与 `ATOMGIT_*`。

完整责任矩阵见 `docs/cache-platform-ai-executable-spec.md` §3.7.1 与设计 spec §9.1。

## 项目结构

```
.
├── action.yml               # 主入口配置
├── action-restore-only.yml  # 独立 restore 入口
├── action-save-only.yml     # 独立 save 入口
├── src/
│   ├── restore/
│   │   ├── index.ts         # restore 主入口
│   │   ├── restoreOnly.ts   # restore-only 独立入口
│   │   └── restoreImpl.ts   # restore 核心逻辑
│   └── save/
│       ├── index.ts         # save 主入口
│       ├── saveOnly.ts      # save-only 独立入口
│       └── saveImpl.ts      # save 核心逻辑
└── dist/                    # ncc 打包（save 含 OBS 整包 PUT 逻辑）
```

## 开发

```bash
# 安装依赖
npm install

# 构建（tsc + ncc 打包）
npm run build

# 清理构建产物
npm run clean:bundle

# 完整打包：构建 + 生成 cache-5.zip
npm run bundle

# 类型检查 + 测试
npm run test
```

### 打包产物结构

`cache-5.zip` 解压后得到 `cache-5/` 目录（与压缩包主版本一致），可直接作为 GitHub Actions workflow 的 `uses` 路径：

```
cache-5/
├── action.yml              # 主入口（restore + save 联动）
├── action-restore-only.yml # 独立 restore 入口
├── action-save-only.yml    # 独立 save 入口
└── dist/                   # ncc 打包产物（与 GitHub 原生一致）
    ├── constants.js
    ├── constants.d.ts
    ├── restore/
    │   └── index.js        # 主入口的 restore 部分
    ├── save/
    │   └── index.js        # 主入口的 post (save) 部分
    ├── restore-only/
    │   └── index.js
    ├── save-only/
    │   └── index.js
    └── utils/              # 共享工具（由 tsc 编译）
        ├── cacheVersion.js
        ├── actionUtils.js
        ├── twirpClient.js
        └── stateProvider.js
```

action yml 中通过 `main:` / `post:` 引用的入口点均已指向对应 ncc bundle，无需额外文件。

## License

MIT


---

## 49. 执行shell命令

- **name**: `official_shell`
- **creator**: wukong_admin
- **被引用**: 73041
- **版本**: 1.0.0

*（无 README）*

---

