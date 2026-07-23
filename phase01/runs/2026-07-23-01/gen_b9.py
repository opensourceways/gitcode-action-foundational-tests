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

write_text("SEC-NAME-01-002",
"""用例 ID:   SEC-NAME-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-025
母意图:    —
标题:      通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

前置条件:
  - 仓库配置了 secret API_KEY

操作步骤:
  1. 提交一个 workflow，执行 printenv 或读取 /proc/self/environ
  2. 触发 workflow 并查看运行日志

预期结果:
  - printenv 输出到日志时，secret 值必须被脱敏
  - 即使通过 env | grep 过滤，过滤后的值也应被脱敏

验证点:
  - [负向] printenv 输出到日志时，secret 值必须被脱敏，绝不应保留原值
  - [非功能] 即使通过 env | grep 过滤，过滤后的值也应被脱敏

清理:      重置 fixture 仓库
""")

write_yaml("SEC-NAME-01-002", build_yaml(
    "SEC-NAME-01-002", ["security"], "security", "P0",
    "通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏", "INTENT-SEC-025",
    {"repo_fixture": "with-secrets", "secrets": ["API_KEY"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  printenv-test:\n    name: Test printenv masking\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Run printenv\n        run: |\n          printenv | grep API_KEY || echo not found\n      - name: Read proc environ\n        run: |\n          cat /proc/self/environ | tr '\0' '\n' | grep API_KEY || echo not found",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "API_KEY"},
        {"type": "positive", "target": "run_logs", "equals": "masked_or_not_found"}
    ],
    "fixture"
))

write_text("SEC-COMM-01-001",
"""用例 ID:   SEC-COMM-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-026
母意图:    —
标题:      issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过

前置条件:
  - 仓库配置了评论触发 workflow

操作步骤:
  1. 提交一个由 issue_comment 触发的 workflow，配置关键字过滤
  2. 提交一条将关键字伪装在 markdown 代码块中的评论

预期结果:
  - 伪装在代码块或注释中的关键字绝不应触发 workflow
  - 触发记录应包含评论原始内容哈希，用于审计

验证点:
  - [负向] 伪装在代码块或注释中的关键字绝不应触发 workflow
  - [非功能] 触发记录应包含评论原始内容哈希，用于审计

清理:      重置 fixture 仓库
""")

write_yaml("SEC-COMM-01-001", build_yaml(
    "SEC-COMM-01-001", ["security"], "security", "P0",
    "issue_comment / pull_request_comment 触发关键字过滤必须不可被绕过", "INTENT-SEC-026",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "issue_comment", "as": "untrusted_contributor", "params": {}},
    "on:\n  issue_comment:\n    types: [created]\njobs:\n  comment-filter:\n    name: Test comment keyword filter\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check trigger\n        run: |\n          echo \"Triggered by comment\"",
    [
        {"type": "negative", "target": "run_status", "must_not_equal": "triggered_by_masked_keyword"},
        {"type": "positive", "target": "run_logs", "equals": "workflow_not_triggered"}
    ],
    "fixture"
))

write_text("SEC-ENV-01-001",
"""用例 ID:   SEC-ENV-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-027
母意图:    —
标题:      环境级 secret 必须经审批后才能被 workflow 访问

前置条件:
  - 仓库配置了环境级 secret PROD_TOKEN
  - 环境审批规则已启用

操作步骤:
  1. 提交一个引用环境级 secret 的 workflow
  2. 在审批前触发 workflow
  3. 审批后再次触发 workflow

预期结果:
  - 审批前 workflow 无法读取到环境 secret 的值
  - 审批后 secret 可被正常引用，job 成功执行

验证点:
  - [正向] 审批后 secret 可被正常引用，job 成功执行
  - [负向] 审批前 workflow 绝不应读取到环境 secret 的值

清理:      重置 fixture 仓库
""")

write_yaml("SEC-ENV-01-001", build_yaml(
    "SEC-ENV-01-001", ["security"], "security", "P0",
    "环境级 secret 必须经审批后才能被 workflow 访问", "INTENT-SEC-027",
    {"repo_fixture": "with-env-secrets", "secrets": ["PROD_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  env-secret-approved:\n    name: Access env secret after approval\n    runs-on: [dedicate-hosted, x64, large]\n    environment: production\n    steps:\n      - name: Use env secret\n        run: |\n          echo \"secret length is ${#PROD_TOKEN}\"",
    [
        {"type": "positive", "target": "run_status", "equals": "success_after_approval"},
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "PROD_TOKEN"}
    ],
    "fixture"
))

print("b9 done")
