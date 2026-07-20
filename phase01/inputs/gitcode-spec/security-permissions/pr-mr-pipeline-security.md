<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/security-permissions/pr-mr-pipeline-security | fetched: 2026-07-20 -->

# PR/MR 流水线安全

## 配置说明

### pull_request vs pull_request_target 安全差异

| 维度 | `pull_request` | `pull_request_target` |
|------|---|---|
| **执行代码来源** | fork 仓库的代码（PR 提交） | 目标仓库的代码（主分支上的 workflow 版本） |
| **ATOMGIT_TOKEN 权限** | 仅 read 权限（安全限制） | 按 permissions 声明的完整权限 |
| **Secrets 可访问性** | fork 来源不可访问项目 Secret | 可访问项目 Secret |
| **workflow 文件版本** | 使用 fork 中的 workflow 版本 | 使用目标分支中的 workflow 版本 |
| **适用场景** | 安全的代码检查、lint、构建 | 需要写权限的部署、发布、评论 |
| **checkout默认代码来源** | PR预合并分支 | base分支 |

### pull_request 事件详解

```yaml
# PR/MR 流水线安全
on:
  pull_request:
    branches: [main]
permissions:
  repository: read        # pull_request 下 ATOMGIT_TOKEN 仅 read
  pr: read                # 不可写操作 PR
stages:
  - name: check
    jobs:
      - name: lint-and-test
        runs-on: {ubuntu-24,x64,small}
        steps:
          - run: npm run lint
          - run: npm test
```

**安全机制**：

- **代码来源**：执行 fork 仓库 PR 分支上的代码，包括 PR 提交者修改的 workflow 文件。
- **权限限制**：ATOMGIT_TOKEN 仅拥有 read 权限，无法推送代码、修改 PR、操作项目资源。
- **Secret 隔离**：来自 fork 的 workflow **不可读取**项目级和组织级 Secret。

> **这意味着**：恶意 PR 提交者可以修改 workflow 文件内容，但由于无 Secret 和写权限，攻击范围有限——无法窃取凭证、无法修改仓库。

### pull_request_target 事件详解

```yaml
# .gitcode/workflows/pr-build.yml
on:
  pull_request_target:
    branches: [main]
permissions:
  repository: write       # pull_request_target 下可拥有写权限
  pr: write               # 可评论/操作 PR
stages:
  - name: build
    jobs:
      - name: build-and-report
        runs-on: {ubuntu-24,x64,medium}
        steps:
          - uses: checkout
            with:
              ref: ${{ atomgit.event.pull_request.head.sha }}   # checkout PR 代码
          - run: make build
          - run: |
              curl -X POST "https://atomgit.com/api/v5/repos/${{ atomgit.repository }}/pulls/${{ atomgit.event.pull_request.number }}/comments" \
                -H "Authorization: token $ATOMGIT_TOKEN" \
                -d '{"body": "Build succeeded ✅"}'
```

**安全机制**：

- **代码来源**：workflow 文件使用目标仓库（main 分支）的版本，而非 fork 中的版本。这是关键差异——PR 提交者**无法修改**执行逻辑。
- **权限范围**：ATOMGIT_TOKEN 拥有 permissions 声明的完整权限，可写仓库、操作 PR。
- **Secret 可访问**：可读取项目级和组织级 Secret。

> **风险提示**：`pull_request_target` 下若显式 checkout 了 PR 源分支代码（`head.sha`）并执行其中的构建脚本，等于在高权限上下文中运行不可信代码——这是典型的注入风险点，需谨慎评审 checkout 的内容与后续命令。
