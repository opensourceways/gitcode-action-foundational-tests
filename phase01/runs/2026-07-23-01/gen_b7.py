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

write_text("SEC-ARTF-01-002",
"""用例 ID:   SEC-ARTF-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-019
母意图:    SEC-ARTF-01-001
标题:      跨仓库 artifact 下载返回 403 或 404

前置条件:
  - fork PR 已上传 artifact

操作步骤:
  1. 在主仓 workflow 中尝试下载 fork PR 的 artifact ID
  2. 查看下载结果

预期结果:
  - 下载返回 404 或权限拒绝
  - 不应静默返回空包或成功

验证点:
  - [负向] 跨仓库 artifact 下载绝不应成功
  - [正向] 返回明确的 404 或 403 错误

清理:      重置 fixture 仓库
""")

write_yaml("SEC-ARTF-01-002", build_yaml(
    "SEC-ARTF-01-002", ["security"], "security", "P0",
    "跨仓库 artifact 下载返回 403 或 404", "INTENT-SEC-019",
    {"repo_fixture": "with-artifacts", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  artifact-download:\n    name: Download artifact from main repo\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Attempt download fork artifact\n        run: |\n          curl -s -o /dev/null -w \"%{http_code}\" \\n            \"https://api.gitcode.com/api/v8/repos/${{ atomgit.repository }}/actions/artifacts/FORK_ARTIFACT_ID/zip?access_token=${{ atomgit.token }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "200"},
        {"type": "positive", "target": "run_logs", "equals": "403_or_404"}
    ],
    "fixture"
))

write_text("SEC-RUN-01-001",
"""用例 ID:   SEC-RUN-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-020
母意图:    —
标题:      Job 结束后 workspace 与临时文件必须被彻底清理

前置条件:
  - 仓库支持多 job workflow

操作步骤:
  1. 提交一个多 job workflow，job A 写入敏感临时文件
  2. job B 检查是否存在 job A 的残留文件

预期结果:
  - job B 绝不应读取到 job A 残留的敏感文件
  - 即使 job A 异常崩溃，清理钩子仍应执行

验证点:
  - [负向] job B 绝不应能读取到 job A 残留的敏感文件
  - [非功能] 即使 job A 异常崩溃，清理钩子仍应执行

清理:      重置 fixture 仓库
""")

write_yaml("SEC-RUN-01-001", build_yaml(
    "SEC-RUN-01-001", ["security"], "security", "P0",
    "Job 结束后 workspace 与临时文件必须被彻底清理", "INTENT-SEC-020",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  job-a:\n    name: Write sensitive file\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Write temp secret\n        run: |\n          echo sensitive-data > /tmp/sensitive-temp.txt\n  job-b:\n    name: Check cleanup\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check no residual\n        run: |\n          if [ -f /tmp/sensitive-temp.txt ]; then\n            echo \"residual found\"\n            exit 1\n          else\n            echo \"cleaned as expected\"\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "residual found"},
        {"type": "positive", "target": "run_logs", "equals": "cleaned_as_expected"}
    ],
    "fixture"
))

write_text("SEC-RUN-01-002",
"""用例 ID:   SEC-RUN-01-002
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-021
母意图:    —
标题:      Runner 环境变量与共享目录必须跨 job 隔离

前置条件:
  - 仓库支持多 job workflow

操作步骤:
  1. 提交一个多 job workflow，job A 设置环境变量和 /tmp 文件
  2. job B 检查环境变量和 /tmp 是否被污染

预期结果:
  - job B 的环境变量和共享目录在启动时为干净状态
  - job B 不应继承 job A 的设置

验证点:
  - [负向] job B 绝不应继承到 job A 设置的环境变量或 /tmp 残留
  - [非功能] 自托管 runner 上应执行与官方 runner 同等级别的清理

清理:      重置 fixture 仓库
""")

write_yaml("SEC-RUN-01-002", build_yaml(
    "SEC-RUN-01-002", ["security"], "security", "P0",
    "Runner 环境变量与共享目录必须跨 job 隔离", "INTENT-SEC-021",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  job-a-env:\n    name: Set env and tmp\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Set env\n        run: |\n          echo MY_SECRET_ENV=leaked >> $ATOMGIT_ENV\n          echo leaked-data > /tmp/env-test.txt\n  job-b-env:\n    name: Check env isolation\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Check env clean\n        run: |\n          if [ -n \"$MY_SECRET_ENV\" ] || [ -f /tmp/env-test.txt ]; then\n            echo \"isolation broken\"\n            exit 1\n          else\n            echo \"isolated as expected\"\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "isolation broken"},
        {"type": "positive", "target": "run_logs", "equals": "isolated_as_expected"}
    ],
    "fixture"
))

print("b7 done")
