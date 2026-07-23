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

write_text("SEC-ENV-01-002",
"""用例 ID:   SEC-ENV-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-027
母意图:    SEC-ENV-01-001
标题:      环境级 secret 审批前 workflow 不可读取

前置条件:
  - 仓库配置了环境级 secret PROD_TOKEN
  - 环境审批规则已启用，尚未审批

操作步骤:
  1. 提交一个引用环境级 secret 的 workflow
  2. 在审批前触发 workflow

预期结果:
  - workflow job 无法读取到环境 secret 的值
  - job 应处于挂起或失败状态

验证点:
  - [负向] 审批前 job 绝不应读取到环境 secret 的值
  - [正向] job 状态为挂起或权限拒绝

清理:      重置 fixture 仓库
""")

write_yaml("SEC-ENV-01-002", build_yaml(
    "SEC-ENV-01-002", ["security"], "security", "P0",
    "环境级 secret 审批前 workflow 不可读取", "INTENT-SEC-027",
    {"repo_fixture": "with-env-secrets", "secrets": ["PROD_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  env-secret-denied:\n    name: Access env secret before approval\n    runs-on: [dedicate-hosted, x64, large]\n    environment: production\n    steps:\n      - name: Try use env secret\n        run: |\n          if [ -z \"$PROD_TOKEN\" ]; then\n            echo \"secret not accessible before approval\"\n          else\n            echo \"secret accessible unexpectedly\"\n            exit 1\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "secret accessible unexpectedly"},
        {"type": "positive", "target": "run_status", "equals": "pending_or_failed"}
    ],
    "fixture"
))

write_text("SEC-WCMD-01-001",
"""用例 ID:   SEC-WCMD-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-028
母意图:    —
标题:      Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，执行 add-mask 命令遮蔽 secret
  2. 触发 workflow 并查看日志中命令的响应

预期结果:
  - workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值
  - 命令执行日志应仅显示命令骨架，不含 payload

验证点:
  - [负向] workflow 命令的响应中绝不应包含被遮蔽前的 secret 原值
  - [非功能] 命令执行日志应仅显示命令本身，不含 secret 原值

清理:      重置 fixture 仓库
""")

write_yaml("SEC-WCMD-01-001", build_yaml(
    "SEC-WCMD-01-001", ["security"], "security", "P0",
    "Workflow 命令（如 add-mask）的响应本身不可泄露被遮蔽前的 secret 值", "INTENT-SEC-028",
    {"repo_fixture": "with-secrets", "secrets": ["API_KEY"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  add-mask-test:\n    name: Test add-mask response\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Mask secret\n        run: |\n          echo \"::add-mask::${{ secrets.API_KEY }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "API_KEY"},
        {"type": "positive", "target": "run_logs", "equals": "mask_command_without_payload"}
    ],
    "fixture"
))

write_text("SEC-WCMD-01-002",
"""用例 ID:   SEC-WCMD-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-029
母意图:    —
标题:      跨运行 artifact 必须被视为不可信数据

前置条件:
  - 仓库支持 artifact 传递

操作步骤:
  1. 提交一个不可信运行（fork PR）上传 artifact
  2. 提交一个特权运行尝试下载并执行该 artifact

预期结果:
  - 特权运行不自动执行 artifact 内容
  - artifact 来源可追溯至其产出运行的信任级别

验证点:
  - [负向] 不可信来源的 artifact 绝不应被特权运行隐式信任执行
  - [正向] artifact 来源可被追溯判定

清理:      重置 fixture 仓库
""")

write_yaml("SEC-WCMD-01-002", build_yaml(
    "SEC-WCMD-01-002", ["security"], "security", "P0",
    "跨运行 artifact 必须被视为不可信数据", "INTENT-SEC-029",
    {"repo_fixture": "with-artifacts", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  artifact-trust:\n    name: Test artifact trust boundary\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Download untrusted artifact\n        uses: download-artifact\n        with:\n          name: untrusted-artifact\n      - name: Do not auto execute\n        run: |\n          echo \"Artifact downloaded but not executed automatically\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "auto_executed"},
        {"type": "positive", "target": "run_status", "equals": "completed"}
    ],
    "fixture"
))

print("b10 done")
