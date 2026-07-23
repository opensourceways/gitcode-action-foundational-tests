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

write_text("SEC-PERM-01-002",
"""用例 ID:   SEC-PERM-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-016
母意图:    SEC-PERM-01-001
标题:      permissions 声明 read 时写操作被平台拒绝

前置条件:
  - 仓库配置了 permissions: repository: read

操作步骤:
  1. 提交一个 workflow，job 级声明 repository: read
  2. 触发 workflow 并执行 push 操作

预期结果:
  - push 操作返回 403 权限拒绝
  - token 的 effective scope 与声明一致

验证点:
  - [负向] 写操作绝不应在 read-only 声明下成功
  - [正向] 返回明确的权限拒绝错误

清理:      重置 fixture 仓库
""")

write_yaml("SEC-PERM-01-002", build_yaml(
    "SEC-PERM-01-002", ["security"], "security", "P0",
    "permissions 声明 read 时写操作被平台拒绝", "INTENT-SEC-016",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  perm-write-denied:\n    name: Test write denied under read\n    runs-on: [dedicate-hosted, x64, large]\n    permissions:\n      repository: read\n    steps:\n      - name: Clone repo\n        run: |\n          git clone https://x-access-token:${{ atomgit.token }}@atomgit.com/${{ atomgit.repository }}.git repo\n      - name: Attempt push\n        run: |\n          cd repo\n          echo test > test.txt\n          git add test.txt\n          git commit -m test\n          git push origin main || echo push denied as expected",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "push_successful"},
        {"type": "positive", "target": "run_logs", "equals": "push_denied_or_403"}
    ],
    "fixture"
))

write_text("SEC-PERM-01-004",
"""用例 ID:   SEC-PERM-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-017
母意图:    SEC-PERM-01-003
标题:      默认状态下写操作被 403 拒绝

前置条件:
  - 仓库未声明 permissions

操作步骤:
  1. 提交一个未声明 permissions 的 workflow，尝试 push
  2. 触发 workflow

预期结果:
  - push 操作返回权限拒绝
  - 默认权限不包含未声明的写域

验证点:
  - [负向] 默认状态下写操作绝不应成功
  - [正向] 权限拒绝信息明确

清理:      重置 fixture 仓库
""")

write_yaml("SEC-PERM-01-004", build_yaml(
    "SEC-PERM-01-004", ["security"], "security", "P0",
    "默认状态下写操作被 403 拒绝", "INTENT-SEC-017",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  default-write-denied:\n    name: Test default write denied\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Attempt push without permissions\n        run: |\n          git clone https://x-access-token:${{ atomgit.token }}@atomgit.com/${{ atomgit.repository }}.git repo\n          cd repo\n          echo test > test.txt\n          git add test.txt\n          git commit -m test\n          git push origin main || echo push denied as expected",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "push_successful"},
        {"type": "positive", "target": "run_logs", "equals": "push_denied_or_403"}
    ],
    "fixture"
))

print("b6a done")
