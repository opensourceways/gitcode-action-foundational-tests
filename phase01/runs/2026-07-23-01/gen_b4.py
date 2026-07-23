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

# SEC-011 comment injection
write_text("SEC-INJ-01-003",
"""用例 ID:   SEC-INJ-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-011
母意图:    —
标题:      不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一条包含 shell 元字符的评论

操作步骤:
  1. 提交一个由 issue_comment 触发的 workflow，在 run 中引用评论 body
  2. 提交一条含 shell 元字符的评论触发 workflow

预期结果:
  - 评论 body 中的 shell 元字符不应被解释为命令执行
  - 即使评论被编辑，重新触发时仍应维持安全过滤

验证点:
  - [负向] 含 shell 元字符的评论内容绝不应被解释为命令执行
  - [非功能] 即使评论被编辑，重新触发时仍应维持安全过滤

清理:      重置 fixture 仓库
""")

write_yaml("SEC-INJ-01-003", build_yaml(
    "SEC-INJ-01-003", ["security"], "security", "P0",
    "不可信 issue/PR 评论内容不可直接插进 run 脚本导致命令注入", "INTENT-SEC-011",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "issue_comment", "as": "untrusted_contributor", "params": {}},
    "on:\n  issue_comment:\n    types: [created]\njobs:\n  comment-inj:\n    name: Test comment injection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Inline comment body\n        run: |\n          echo \"Comment is ${{ atomgit.event.comment.body }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "injected_command_executed"},
        {"type": "positive", "target": "run_status", "equals": "success"}
    ],
    "fixture"
))

# SEC-012 commit message injection
write_text("SEC-INJ-01-004",
"""用例 ID:   SEC-INJ-01-004
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-012
母意图:    —
标题:      不可信 commit message 不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一条 commit message 含反引号或分号的 push

操作步骤:
  1. 提交一个由 push 触发的 workflow，在 run 中引用 commit message
  2. 推送一条含 shell 元字符的 commit

预期结果:
  - commit message 中的 shell 元字符不应被解释为命令执行
  - 安全写法（中间环境变量）应正常生效

验证点:
  - [负向] 含反引号或分号的 commit message 绝不应被解释为命令执行
  - [非功能] 安全写法（中间环境变量）应正常生效

清理:      重置 fixture 仓库
""")

write_yaml("SEC-INJ-01-004", build_yaml(
    "SEC-INJ-01-004", ["security"], "security", "P0",
    "不可信 commit message 不可直接插进 run 脚本导致命令注入", "INTENT-SEC-012",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "push", "as": "untrusted_contributor", "params": {}},
    "on:\n  push:\n    branches: [main]\njobs:\n  commit-inj:\n    name: Test commit message injection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Inline commit message\n        run: |\n          echo \"Message is ${{ atomgit.event.commits[0].message }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "injected_command_executed"},
        {"type": "positive", "target": "run_status", "equals": "success"}
    ],
    "fixture"
))

# SEC-013 double template
write_text("SEC-INJ-01-005",
"""用例 ID:   SEC-INJ-01-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-013
母意图:    —
标题:      表达式求值必须防止双重模板渲染（二次求值）

前置条件:
  - 仓库支持表达式求值

操作步骤:
  1. 提交一个 workflow，在输入中包含模板语法字符（如 {{ 1 + 1 }}）
  2. 触发 workflow 并查看运行日志

预期结果:
  - 外层 ${{ }} 求值结果中的模板语法字符应被转义
  - 不再触发内层模板引擎求值

验证点:
  - [负向] 含模板语法的外部输入绝不应在内层 Action 中被二次求值
  - [非功能] 二次求值若无法避免，应至少被沙箱化

清理:      重置 fixture 仓库
""")

write_yaml("SEC-INJ-01-005", build_yaml(
    "SEC-INJ-01-005", ["security"], "security", "P0",
    "表达式求值必须防止双重模板渲染（二次求值）", "INTENT-SEC-013",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  double-template:\n    name: Test double template eval\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Pass template syntax\n        run: |\n          echo \"Input: ${{ '{{ 1 + 1 }}' }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "2"},
        {"type": "positive", "target": "run_logs", "equals": "template_chars_escaped"}
    ],
    "fixture"
))

# SEC-014a commit hash pin
write_text("SEC-SUPPLY-01-001",
"""用例 ID:   SEC-SUPPLY-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-014
母意图:    —
标题:      第三方 Action 引用应支持完整 commit hash 固定

前置条件:
  - 仓库可引用外部 Action

操作步骤:
  1. 提交一个 workflow，使用完整 commit SHA 引用第三方 Action
  2. 触发 workflow

预期结果:
  - 完整 commit SHA 引用可成功执行 action
  - commit SHA 不匹配时 job 应失败或拒绝执行

验证点:
  - [正向] 完整 commit SHA 引用可成功执行 action
  - [负向] commit SHA 不匹配或分支被重写时，job 应失败或拒绝执行

清理:      重置 fixture 仓库
""")

write_yaml("SEC-SUPPLY-01-001", build_yaml(
    "SEC-SUPPLY-01-001", ["security"], "security", "P0",
    "第三方 Action 引用应支持完整 commit hash 固定", "INTENT-SEC-014",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  hash-pin:\n    name: Test commit hash pinning\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Use pinned action\n        uses: docker/build-push-action@1234567890abcdef1234567890abcdef12345678",
    [
        {"type": "positive", "target": "run_status", "equals": "success_or_action_executed"},
        {"type": "negative", "target": "run_logs", "must_not_contain": "unauthorized_action_execution"}
    ],
    "fixture"
))

print("b4 done")
