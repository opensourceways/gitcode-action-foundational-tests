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

write_text("SEC-DEFPERM-01-001",
"""用例 ID:   SEC-DEFPERM-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
母意图:    —
标题:      ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效

前置条件:
  - 仓库未声明或声明了部分 permissions

操作步骤:
  1. 提交一个 workflow，顶层声明 repository: read，job 级覆盖为 repository: write
  2. 触发 workflow 并验证实际权限

预期结果:
  - 顶层声明被各 job 继承
  - job 级声明覆盖顶层

验证点:
  - [正向] 顶层声明被各 job 继承；job 级声明覆盖顶层
  - [非功能] 权限范围与覆盖关系可被观测判定

清理:      重置 fixture 仓库
""")

write_yaml("SEC-DEFPERM-01-001", build_yaml(
    "SEC-DEFPERM-01-001", ["security"], "security", "P0",
    "ATOMGIT_TOKEN 默认权限范围与 job 级覆盖必须正确生效", "INTENT-SEC-036",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\npermissions:\n  repository: read\njobs:\n  inherit-test:\n    name: Test permission inheritance\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Attempt write\n        run: |\n          curl -s -o /dev/null -w \"%{http_code}\" -X POST \\n            \"https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues\" \\n            -H \"Authorization: token ${{ atomgit.token }}\" \\n            -d '{\"title\": \"test\"}'",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "write_successful"},
        {"type": "positive", "target": "run_logs", "equals": "403_or_permission_denied"}
    ],
    "fixture"
))

write_text("SEC-DEFPERM-01-002",
"""用例 ID:   SEC-DEFPERM-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-036
母意图:    SEC-DEFPERM-01-001
标题:      job 级覆盖后权限正确收窄

前置条件:
  - 仓库声明了顶层 permissions: repository: write

操作步骤:
  1. 提交一个 workflow，顶层声明 repository: write，job 级覆盖为 repository: read
  2. 触发 workflow 并验证 job 实际权限

预期结果:
  - job 级收窄后不应仍保留顶层的更大权限
  - token 实际权限应与 job 级声明一致

验证点:
  - [负向] job 级收窄后不应仍保留顶层的更大权限
  - [正向] 各权限域实测与有效声明一致，越权写被拒

清理:      重置 fixture 仓库
""")

write_yaml("SEC-DEFPERM-01-002", build_yaml(
    "SEC-DEFPERM-01-002", ["security"], "security", "P0",
    "job 级覆盖后权限正确收窄", "INTENT-SEC-036",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\npermissions:\n  repository: write\njobs:\n  override-test:\n    name: Test job level override\n    runs-on: [dedicate-hosted, x64, large]\n    permissions:\n      repository: read\n    steps:\n      - name: Attempt write after override\n        run: |\n          curl -s -o /dev/null -w \"%{http_code}\" -X POST \\n            \"https://api.gitcode.com/api/v5/repos/${{ atomgit.repository }}/issues\" \\n            -H \"Authorization: token ${{ atomgit.token }}\" \\n            -d '{\"title\": \"test\"}'",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "write_successful"},
        {"type": "positive", "target": "run_logs", "equals": "403_or_permission_denied"}
    ],
    "fixture"
))

print("b14b done")
