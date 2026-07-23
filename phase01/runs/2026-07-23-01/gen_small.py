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

write_text("SEC-TOKEN-01-001",
"""用例 ID:   SEC-TOKEN-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-003
母意图:    —
标题:      fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限

前置条件:
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个使用 ATOMGIT_TOKEN 克隆代码的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - ATOMGIT_TOKEN 可成功执行 clone 等读操作
  - 尝试写操作时被平台强制拒绝

验证点:
  - [正向] ATOMGIT_TOKEN 可成功执行 clone 等读操作
  - [负向] 尝试写操作应返回 403 或失败

清理:      重置 fixture 仓库
""")

write_yaml("SEC-TOKEN-01-001", build_yaml(
    "SEC-TOKEN-01-001", ["security"], "security", "P0",
    "fork PR 触发 pull_request 时 ATOMGIT_TOKEN 必须仅拥有 read 权限", "INTENT-SEC-003",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  token-read:\n    name: Test token read only\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Clone with token\n        run: |\n          git clone https://x-access-token:${{ atomgit.token }}@atomgit.com/${{ atomgit.repository }}.git test-clone\n      - name: Attempt write via API\n        run: |\n          curl -s -o /dev/null -w \"%{http_code}\" -X POST \\n            \"https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues\" \\n            -H \"Authorization: token ${{ atomgit.token }}\" \\n            -d '{\"title\": \"test\"}'",
    [
        {"type": "positive", "target": "run_logs", "equals": "clone_successful"},
        {"type": "negative", "target": "run_logs", "must_not_contain": "write_permission_granted"}
    ],
    "fixture"
))

write_text("SEC-TOKEN-01-002",
"""用例 ID:   SEC-TOKEN-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-003
母意图:    SEC-TOKEN-01-001
标题:      fork PR 中 ATOMGIT_TOKEN 写操作被平台拒绝

前置条件:
  - 存在一个来自外部 fork 的 PR

操作步骤:
  1. 以 fork 贡献者身份提交一个尝试用 ATOMGIT_TOKEN 推送代码的 workflow
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - 推送操作返回权限拒绝（403）
  - 运行日志中显示权限不足

验证点:
  - [负向] 写操作绝不应成功
  - [正向] 权限拒绝信息明确

清理:      重置 fixture 仓库
""")

write_yaml("SEC-TOKEN-01-002", build_yaml(
    "SEC-TOKEN-01-002", ["security"], "security", "P0",
    "fork PR 中 ATOMGIT_TOKEN 写操作被平台拒绝", "INTENT-SEC-003",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  token-write-denied:\n    name: Test token write denied\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Attempt push\n        run: |\n          git clone https://x-access-token:${{ atomgit.token }}@atomgit.com/${{ atomgit.repository }}.git repo\n          cd repo\n          echo test > test.txt\n          git add test.txt\n          git commit -m \"test\"\n          git push origin main || echo \"push denied\"",
    [
        {"type": "negative", "target": "run_logs", "equals": "push_denied_or_403"},
        {"type": "positive", "target": "run_status", "equals": "completed"}
    ],
    "fixture"
))

print("small batch done")
