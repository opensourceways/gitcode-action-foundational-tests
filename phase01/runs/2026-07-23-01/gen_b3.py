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

# SEC-007 multiline
write_text("SEC-MASK-01-005",
"""用例 ID:   SEC-MASK-01-005
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-007
母意图:    —
标题:      Secret 日志脱敏不可通过多行值输出绕过

前置条件:
  - 仓库配置了多行 secret MULTI_LINE_SECRET

操作步骤:
  1. 提交一个 workflow，直接 echo 多行 secret 到日志
  2. 触发 workflow 并查看运行日志

预期结果:
  - 多行 secret 的每一行在日志中均被脱敏
  - 换行符不应成为脱敏边界

验证点:
  - [负向] 多行 secret 的任一行均不应以明文出现在日志中
  - [非功能] 脱敏引擎应支持跨行匹配或整值匹配

清理:      重置 fixture 仓库
""")

write_yaml("SEC-MASK-01-005", build_yaml(
    "SEC-MASK-01-005", ["security"], "security", "P0",
    "Secret 日志脱敏不可通过多行值输出绕过", "INTENT-SEC-007",
    {"repo_fixture": "with-secrets", "secrets": ["MULTI_LINE_SECRET"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  multiline-mask:\n    name: Test multiline masking\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Echo multiline secret\n        run: |\n          echo \"${{ secrets.MULTI_LINE_SECRET }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "MULTI_LINE_SECRET"},
        {"type": "positive", "target": "run_logs", "equals": "multiline_masked_with_asterisks"}
    ],
    "fixture"
))

# SEC-008 fragment
write_text("SEC-MASK-01-006",
"""用例 ID:   SEC-MASK-01-006
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-008
母意图:    —
标题:      Secret 日志脱敏不可通过分片输出绕过

前置条件:
  - 仓库配置了 secret DEPLOY_TOKEN

操作步骤:
  1. 提交一个 workflow，逐字符或逐小段输出 secret
  2. 触发 workflow 并查看运行日志

预期结果:
  - 即使分片输出，secret 的各片段仍被脱敏
  - 或分片到不可还原长度以下

验证点:
  - [负向] secret 的分片输出绝不应在日志中保留明文
  - [非功能] 脱敏机制应设置最小匹配长度

清理:      重置 fixture 仓库
""")

write_yaml("SEC-MASK-01-006", build_yaml(
    "SEC-MASK-01-006", ["security"], "security", "P0",
    "Secret 日志脱敏不可通过分片输出绕过", "INTENT-SEC-008",
    {"repo_fixture": "with-secrets", "secrets": ["DEPLOY_TOKEN"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  fragment-bypass:\n    name: Test fragment bypass\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Echo secret character by character\n        run: |\n          secret=\"${{ secrets.DEPLOY_TOKEN }}\"\n          for (( i=0; i<${#secret}; i++ )); do\n            echo \"char $i: ${secret:$i:1}\"\n          done",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "DEPLOY_TOKEN"},
        {"type": "negative", "target": "run_logs", "eval": "llm_assisted", "rubric": "日志中 secret 的任意连续子串（如 3 字符以上）命中数应为 0"}
    ],
    "fixture"
))

# SEC-009 PR title injection
write_text("SEC-INJ-01-001",
"""用例 ID:   SEC-INJ-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-009
母意图:    —
标题:      不可信 PR 标题不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一个来自外部 fork 的 PR，其标题包含 shell 元字符

操作步骤:
  1. 提交一个 workflow，在 run 脚本中直接内联引用 PR 标题
  2. 在 fork PR 场景下触发该 workflow

预期结果:
  - PR 标题中的特殊字符不应被解释为 shell 命令执行
  - 表达式值应在脚本生成前完成求值并安全转义

验证点:
  - [负向] 含特殊字符的 PR 标题绝不应被解释为 shell 命令执行
  - [非功能] 安全写法（先存入中间环境变量再引用）应正常工作

清理:      重置 fixture 仓库
""")

write_yaml("SEC-INJ-01-001", build_yaml(
    "SEC-INJ-01-001", ["security"], "security", "P0",
    "不可信 PR 标题不可直接插进 run 脚本导致命令注入", "INTENT-SEC-009",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  pr-title-inj:\n    name: Test PR title injection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Inline PR title\n        run: |\n          echo \"PR title is ${{ atomgit.event.pull_request.title }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "injected_command_executed"},
        {"type": "positive", "target": "run_status", "equals": "success"}
    ],
    "fixture"
))

# SEC-010 branch injection
write_text("SEC-INJ-01-002",
"""用例 ID:   SEC-INJ-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-010
母意图:    —
标题:      不可信分支名不可直接插进 run 脚本导致命令注入

前置条件:
  - 存在一个分支名含 shell 元字符的 PR

操作步骤:
  1. 提交一个 workflow，在 run 脚本中直接内联引用分支名
  2. 触发该 workflow

预期结果:
  - 分支名中的特殊字符不应被解释为 shell 元字符
  - 表达式值应被安全求值

验证点:
  - [负向] 含特殊字符的分支名绝不应被解释为 shell 命令
  - [非功能] 安全写法（中间环境变量）应正常生效

清理:      重置 fixture 仓库
""")

write_yaml("SEC-INJ-01-002", build_yaml(
    "SEC-INJ-01-002", ["security"], "security", "P0",
    "不可信分支名不可直接插进 run 脚本导致命令注入", "INTENT-SEC-010",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "pull_request", "as": "untrusted_contributor", "params": {}},
    "on:\n  pull_request:\n    branches: [main]\njobs:\n  branch-inj:\n    name: Test branch name injection\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Inline branch name\n        run: |\n          echo \"Branch is ${{ atomgit.head_ref }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "injected_command_executed"},
        {"type": "positive", "target": "run_status", "equals": "success"}
    ],
    "fixture"
))

print("b3 done")
