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

write_text("SEC-BASE-01-001",
"""用例 ID:   SEC-BASE-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-035
母意图:    —
标题:      pull_request_target 使用 base 分支的 workflow 版本

前置条件:
  - 仓库 base 分支和 fork PR 分支的 workflow 内容不同

操作步骤:
  1. 在 fork PR 分支修改 workflow 文件（新增窃密步骤）
  2. 触发 pull_request_target 事件
  3. 检查实际执行的 workflow 版本

预期结果:
  - pull_request_target 触发时加载并执行 base 分支中的 workflow 文件版本
  - fork PR 分支内对 workflow 文件的改动不得被采用

验证点:
  - [正向] base 分支 workflow 按其定义执行，可访问 secret 与写 token
  - [负向] fork PR 分支内对 workflow 文件的改动不得被 pull_request_target 运行采用

清理:      重置 fixture 仓库
""")

write_yaml("SEC-BASE-01-001", build_yaml(
    "SEC-BASE-01-001", ["security"], "security", "P0",
    "pull_request_target 使用 base 分支的 workflow 版本", "INTENT-SEC-035",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request_target", "as": "maintainer", "params": {}},
    "on:\n  pull_request_target:\n    branches: [main]\njobs:\n  base-version:\n    name: Verify base workflow version\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Echo from base\n        run: |\n          echo \"Executing base branch workflow\"",
    [
        {"type": "positive", "target": "run_logs", "equals": "base_branch_workflow_executed"},
        {"type": "negative", "target": "run_logs", "must_not_contain": "fork_injected_step"}
    ],
    "fixture"
))

write_text("SEC-BASE-01-002",
"""用例 ID:   SEC-BASE-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-035
母意图:    SEC-BASE-01-001
标题:      fork PR 改 workflow 不被 pull_request_target 采用

前置条件:
  - fork PR 分支修改了 workflow 文件

操作步骤:
  1. 在 fork PR 分支新增一个输出 secret 的步骤到 workflow
  2. 触发 pull_request_target 事件
  3. 检查运行日志中是否出现该步骤

预期结果:
  - fork PR 注入的步骤未出现在执行记录中
  - 运行采用的 workflow 内容哈希/步骤集与 base 分支一致

验证点:
  - [负向] pull_request_target 绝不应执行来自不可信 fork 的 workflow 定义
  - [正向] 运行采用的 workflow 内容哈希/步骤集与 base 分支一致

清理:      重置 fixture 仓库
""")

write_yaml("SEC-BASE-01-002", build_yaml(
    "SEC-BASE-01-002", ["security"], "security", "P0",
    "fork PR 改 workflow 不被 pull_request_target 采用", "INTENT-SEC-035",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request_target", "as": "maintainer", "params": {}},
    "on:\n  pull_request_target:\n    branches: [main]\njobs:\n  reject-fork-wf:\n    name: Reject fork workflow changes\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Base step only\n        run: |\n          echo \"Only base steps run\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "fork_injected_step"},
        {"type": "positive", "target": "run_status", "equals": "success_with_base_workflow"}
    ],
    "fixture"
))

print("b14a done")
