# Demo — PR 触发自动化验证

验证 GitCode `on: pull_request` 工作流能否通过 API 自动触发并脚本化。

## 前提

```bash
# 根目录 .env 需包含：
GITCODE_ACCESS_TOKEN=<bot_token>           # ComputingActionTest 仓库 bot token
CONTRIBUTOR_GITCODE_TOKEN=<contrib_token>  # 第二个账号 token（teamfi），用于 fork
GITCODE_EXECUTOR=ccijunk
GITCODE_OWNER=ComputingActionTest
GITCODE_REPO=foundational-tests
GITCODE_BRANCH=main
GITCODE_COOKIE=<optional>
```

## 脚本

| 脚本 | 用途 | 状态 |
|------|------|------|
| `demo_pr_trigger.py` | same-repo PR (`feature → main`) 触发 | PR 创建成功，workflow 不触发 |
| `demo_fork_pr.py` | fork PR (`teamfi:branch → upstream main`) 触发 | 全流程自动化成功，workflow 不触发 |
| `demo_push_sanity.py` | `on: push` 触发验证（对照） | 正常 |

## 运行

```bash
cd phase02/classify-experiment/demo
python3 demo_pr_trigger.py    # same-repo PR
python3 demo_fork_pr.py       # fork PR
```

## 结论

| 发现 | 详情 |
|------|------|
| `POST /api/v5/repos/.../pulls` 创建 PR | ✅ 同仓库 + 跨仓库均成功 |
| `POST /api/v5/repos/.../forks` 创建 fork | ✅ |
| Contributor token clone + push fork | ✅ |
| `PATCH /pulls/:id` 关闭 PR | ✅ |
| **`on: pull_request` workflow 触发** | **❌ 4 次尝试均不触发** |
| 平台根本原因 | API 创建 PR 不触发 workflow（只 Web UI 触发或需额外配置） |

## 关键代码模式

### 跨仓库 fork PR 创建

```python
# 1. Bot 推 workflow 到 upstream main
# .gitcode/workflows/xxx.yml 必须存在于 base 分支

# 2. Contributor fork 仓库
POST /api/v5/repos/{upstream_owner}/{repo}/forks
Authorization: contributor_token

# 3. Contributor 推分支到 fork
git push origin {feature_branch}

# 4. Contributor 创建跨仓库 PR
POST /api/v5/repos/{upstream_owner}/{repo}/pulls
{
  "title": "...",
  "head": "{fork_owner}:{feature_branch}",
  "base": "main"
}
Authorization: contributor_token
```

### 常见坑

- **fork 初始化延迟**: `POST /forks` 返回后需等 15-20s 才能 git clone
- **rate limit**: `POST /forks` 每分钟 1 次，重复创建返回 HTTP 429
- **workflow 必须在 base 分支**: `on: pull_request` 的 YAML 必须在 PR 目标分支（main），不在 feature 分支
- **v8 runs API 的 event 始终为 `Manual`**: 平台将所有 run 的 event 字段统一标为 `Manual`
- **`.env` 内联注释**: `value  # comment` 格式需特殊处理，`python-dotenv` 不认
