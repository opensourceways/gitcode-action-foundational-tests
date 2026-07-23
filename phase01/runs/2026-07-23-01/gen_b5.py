import os, json

BASE = r"D:/业务/action/gitcode-action-foundational-tests/phase01/runs/2026-07-23-01/cases"

def write_text(cid, body):
    with open(os.path.join(BASE, "text", cid + ".md"), "w", encoding="utf-8") as f:
        f.write(body)

def write_yaml(cid, body):
    with open(os.path.join(BASE, "yaml", cid + ".yaml"), "w", encoding="utf-8") as f:
        f.write(body)

def build_yaml(cid, dims, dim, pri, title, intent, setup, trigger, wf, assertions, teardown, fault=None):
    lines = []
    lines.append("id: " + cid)
    lines.append("dimensions: " + json.dumps(dims))
    lines.append("dimension: " + dim)
    lines.append("priority: " + pri)
    lines.append('title: "' + title + '"')
    lines.append("intent_ref: " + intent)
    lines.append("setup:")
    lines.append("  repo_fixture: " + setup.get("repo_fixture", "default"))
    if setup.get("secrets"):
        lines.append("  secrets: " + json.dumps(setup["secrets"]))
    lines.append("workflow: |")
    for wl in wf.split("\n"):
        lines.append("  " + wl)
    lines.append("trigger:")
    lines.append("  event: " + trigger["event"])
    lines.append("  as: " + trigger["as"])
    lines.append("  params: " + json.dumps(trigger.get("params", {})))
    lines.append("fault_injection: null")
    lines.append("assertions:")
    for a in assertions:
        lines.append("  - type: " + a["type"])
        lines.append("    target: " + a["target"])
        for k, v in a.items():
            if k in ("type", "target"):
                continue
            lines.append("    " + k + ": " + json.dumps(v))
    lines.append("teardown:")
    lines.append("  reset: " + teardown)
    return "\n".join(lines) + "\n"

# SEC-014b hash mismatch
write_text("SEC-SUPPLY-01-002",
"""用例 ID:   SEC-SUPPLY-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
母意图:    SEC-SUPPLY-01-001
标题:      commit hash 不匹配时第三方 Action 应被拒绝执行

前置条件:
  - 仓库可引用外部 Action

操作步骤:
  1. 提交一个 workflow，使用一个不存在的 commit SHA 引用 Action
  2. 触发 workflow

预期结果:
  - job 进入失败状态或明确拒绝执行
  - 系统不应静默回退到分支 HEAD

验证点:
  - [负向] 错误 commit SHA 绝不应执行 Action
  - [正向] 返回明确的 Action 未找到或 SHA 不匹配错误

清理:      重置 fixture 仓库
""")

write_yaml("SEC-SUPPLY-01-002", build_yaml(
    "SEC-SUPPLY-01-002", ["security"], "security", "P0",
    "commit hash 不匹配时第三方 Action 应被拒绝执行", "INTENT-SEC-014",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  hash-mismatch:\n    name: Test hash mismatch rejection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Use invalid hash action\n        uses: docker/build-push-action@0000000000000000000000000000000000000000",
    [
        {"type": "negative", "target": "run_status", "must_not_equal": "success"},
        {"type": "positive", "target": "run_logs", "equals": "action_not_found_or_sha_mismatch"}
    ],
    "fixture"
))

# SEC-015 typosquatting
write_text("SEC-SUPPLY-01-003",
"""用例 ID:   SEC-SUPPLY-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-015
母意图:    —
标题:      第三方 Action 来源应具备信任边界（typosquatting 限制）

前置条件:
  - 仓库可引用外部 Action

操作步骤:
  1. 提交一个 workflow，引用一个与官方 Action 名称高度相似的 Action
  2. 触发 workflow

预期结果:
  - 系统不应静默解析 typosquatting 名称为合法来源
  - 首次使用未审核 Action 时应触发警告或需审批

验证点:
  - [负向] 与官方 action 名称高度相似的恶意 Action 绝不应被静默解析为合法来源
  - [非功能] 首次使用未审核 Action 时应留下审计记录

清理:      重置 fixture 仓库
""")

write_yaml("SEC-SUPPLY-01-003", build_yaml(
    "SEC-SUPPLY-01-003", ["security"], "security", "P0",
    "第三方 Action 来源应具备信任边界（typosquatting 限制）", "INTENT-SEC-015",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  typo-test:\n    name: Test typosquatting rejection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Use typo action\n        uses: checkout-action@v1",
    [
        {"type": "negative", "target": "run_status", "must_not_equal": "success"},
        {"type": "positive", "target": "run_logs", "equals": "action_not_found_or_unapproved"}
    ],
    "fixture"
))

# SEC-016a permissions effective
write_text("SEC-PERM-01-001",
"""用例 ID:   SEC-PERM-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
母意图:    —
标题:      显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN

前置条件:
  - 仓库配置了 permissions 声明

操作步骤:
  1. 提交一个 workflow，在 job 级显式声明 repository: read
  2. 触发 workflow 并尝试执行写操作

预期结果:
  - 声明 read 时读操作成功
  - 声明 read 时写操作返回 403 或失败

验证点:
  - [正向] 声明 read 时读操作（clone、API 读取）成功
  - [负向] 声明 read 时写操作（push、评论、修改 PR）返回 403 或失败

清理:      重置 fixture 仓库
""")

write_yaml("SEC-PERM-01-001", build_yaml(
    "SEC-PERM-01-001", ["security"], "security", "P0",
    "显式声明的 permissions 必须在 job 级实际生效并限制 ATOMGIT_TOKEN", "INTENT-SEC-016",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  perm-read:\n    name: Test permissions read only\n    runs-on: [dedicate-hosted, x64, large]\n    permissions:\n      repository: read\n      pr: none\n      issue: none\n      note: none\n      project: none\n      hook: none\n    steps:\n      - name: Attempt write\n        run: |\n          curl -s -o /dev/null -w \"%{http_code}\" -X POST \\n            \"https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues\" \\n            -H \"Authorization: token ${{ atomgit.token }}\" \\n            -d '{\"title\": \"test\"}'",
    [
        {"type": "positive", "target": "run_logs", "equals": "read_operations_successful"},
        {"type": "negative", "target": "run_logs", "must_not_contain": "write_permission_granted"}
    ],
    "fixture"
))

# SEC-017a default read only
write_text("SEC-PERM-01-003",
"""用例 ID:   SEC-PERM-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-017
母意图:    —
标题:      未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）

前置条件:
  - 仓库未配置 permissions 声明

操作步骤:
  1. 提交一个未声明 permissions 的 workflow
  2. 触发 workflow 并尝试执行写操作

预期结果:
  - 默认状态下 ATOMGIT_TOKEN 仅拥有仓库 read 权限
  - 写操作被平台拒绝

验证点:
  - [负向] 默认状态下 ATOMGIT_TOKEN 绝不应拥有写权限
  - [非功能] 默认权限应在组织级可配置为更严格（如 none）

清理:      重置 fixture 仓库
""")

write_yaml("SEC-PERM-01-003", build_yaml(
    "SEC-PERM-01-003", ["security"], "security", "P0",
    "未声明 permissions 时 ATOMGIT_TOKEN 默认权限必须最小化（read-only）", "INTENT-SEC-017",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  default-perm:\n    name: Test default permissions\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Attempt write without permissions\n        run: |\n          curl -s -o /dev/null -w \"%{http_code}\" -X POST \\n            \"https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues\" \\n            -H \"Authorization: token ${{ atomgit.token }}\" \\n            -d '{\"title\": \"test\"}'",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "write_permission_granted"},
        {"type": "positive", "target": "run_status", "equals": "completed"}
    ],
    "fixture"
))

print("b5 done")
