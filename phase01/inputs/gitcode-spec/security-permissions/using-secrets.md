<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/security-permissions/using-secrets | fetched: 2026-07-20 -->

# 使用 Secrets 管理敏感信息

## 概述

**适用场景**：流水线中需要使用密码、API Key、访问凭证等敏感信息，但不希望将其硬编码于 workflow 文件或代码仓库中。

## 配置说明

### 创建 Secret

#### 组织级 Secret

1. 进入组织 **组织设置 → 密钥与变量 → 组织秘钥**
2. 点击 **新建组织密钥**
3. 输入 Name（如 `PROD_DEPLOY_KEY`）和 Value
4. 点击 **新建密钥**

#### 项目级 Secret

1. 进入项目 **项目设置 → 密钥与变量 → 仓库密钥**
2. 点击 **新建仓库密钥**
3. 输入 Name 和 Value
4. 点击 **新建密钥**

### 在 workflow 中引用 Secret

```yaml
# 使用 Secrets 管理敏感信息
stages:
  - name: deploy
    jobs:
      - name: push-to-prod
        runs-on: {ubuntu-24,x64,medium}
        steps:
          - run: |
              ssh -i ${{ secrets.PROD_DEPLOY_KEY }} \
                user@prod-server.example.com \
                "deploy.sh ${{ secrets.PROD_API_TOKEN }}"
```

引用语法为 `${{ secrets.SECRET_NAME }}`，Secret 名称规则：

- 仅允许大写字母、数字和下划线
- 不得以 `ATOMGIT_` 开头（与系统变量冲突）
- 不得以数字开头

### 在 container credentials 中使用 Secret

```yaml
jobs:
  - name: private-image-build
    runs-on: {ubuntu-24,x64,medium}
    container:
      image: registry.example.com/myapp:latest
      credentials:
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
```

### Secret 安全机制

| 安全措施 | 说明 |
|--------|------|
| 日志遮掩 | Secret 值在日志中自动替换为 `***` |
| 不可查看 | 创建后无法在界面查看原值，只能更新覆盖 |
| Fork 隔离 | `pull_request` 来自 fork 的 workflow **不可访问**项目级 Secret |
| 环境审批 | 环境级 Secret 可配置审批人，未经审批 job 不可访问 |

> **重要**：`pull_request` 事件下，来自 fork 仓库的 PR 触发的 workflow 无法读取项目 Secret，这是安全隔离机制。若需在 PR 流水线中使用 Secret，请使用 `pull_request_target` 事件。
