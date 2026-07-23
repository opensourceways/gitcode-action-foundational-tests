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

write_text("SEC-RUN-01-003",
"""用例 ID:   SEC-RUN-01-003
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-022
母意图:    —
标题:      自托管 Runner 跨项目残留必须被隔离

前置条件:
  - 自托管 runner 被多个项目共享

操作步骤:
  1. 项目 A 的 workflow 写入临时文件和环境变量
  2. 项目 B 的 workflow 在同一 runner 上检查残留

预期结果:
  - 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量
  - runner 清理失败时应标记为不可用

验证点:
  - [负向] 项目 B 的 job 绝不应读取到项目 A 残留的敏感文件或环境变量
  - [非功能] runner 清理失败时应标记为不可用，避免调度下一 job

清理:      重置 full_instance
""")

write_yaml("SEC-RUN-01-003", build_yaml(
    "SEC-RUN-01-003", ["security"], "security", "P0",
    "自托管 Runner 跨项目残留必须被隔离", "INTENT-SEC-022",
    {"repo_fixture": "self-hosted-shared", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  project-a:\n    name: Write project A data\n    runs-on: [self-hosted, x64, large]\n    steps:\n      - name: Write temp\n        run: |\n          echo project-a-secret > /tmp/project-a-temp.txt\n  project-b:\n    name: Check project B isolation\n    runs-on: [self-hosted, x64, large]\n    steps:\n      - name: Check no cross project leak\n        run: |\n          if [ -f /tmp/project-a-temp.txt ]; then\n            echo \"cross project leak\"\n            exit 1\n          else\n            echo \"isolated as expected\"\n          fi",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "cross project leak"},
        {"type": "positive", "target": "run_logs", "equals": "isolated_as_expected"}
    ],
    "full_instance"
))

write_text("SEC-NET-01-001",
"""用例 ID:   SEC-NET-01-001
维度标签:   [security]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-023
母意图:    —
标题:      Runner 网络出站必须受控，防止 SSRF 与内网跳板

前置条件:
  - 仓库配置了自托管或官方 runner

操作步骤:
  1. 提交一个 workflow，尝试访问内部元数据端点或内网地址
  2. 触发 workflow 并查看网络访问结果

预期结果:
  - 访问尝试返回超时或连接拒绝
  - 运行日志中无外发成功记录

验证点:
  - [负向] Runner 绝不应能访问内网元数据端点或内部服务
  - [非功能] 访问尝试应返回超时或连接拒绝，不应产生可识别的内部服务响应

清理:      重置 full_instance
""")

write_yaml("SEC-NET-01-001", build_yaml(
    "SEC-NET-01-001", ["security"], "security", "P0",
    "Runner 网络出站必须受控，防止 SSRF 与内网跳板", "INTENT-SEC-023",
    {"repo_fixture": "default", "secrets": [], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  ssrf-test:\n    name: Test SSRF prevention\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Access metadata endpoint\n        run: |\n          curl -s --max-time 5 http://169.254.169.254/ || echo \"access denied or timeout\"\n      - name: Access internal IP\n        run: |\n          curl -s --max-time 5 http://192.168.1.1/ || echo \"access denied or timeout\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain": "metadata_service_response"},
        {"type": "positive", "target": "run_logs", "equals": "access_denied_or_timeout"}
    ],
    "full_instance"
))

write_text("SEC-NAME-01-001",
"""用例 ID:   SEC-NAME-01-001
维度标签:   [security, compatibility]
维度:      安全性
优先级:    P0
溯源意图:  INTENT-SEC-024
母意图:    —
标题:      Secret/变量名含特殊字符时不可导致意外求值或权限绕过

前置条件:
  - 仓库配置了含中划线的 secret MY-VAR

操作步骤:
  1. 提交一个 workflow，引用 secrets.MY-VAR 并在 shell 中使用
  2. 触发 workflow 并查看运行日志

预期结果:
  - 含中划线的 secret 不应因解析错误而被泄露到日志
  - 若不支持中划线，应在 YAML 校验阶段报错

验证点:
  - [负向] 含中划线的 secret 绝不应因解析错误而被泄露到日志或环境变量
  - [非功能] 若不支持中划线，应在 YAML 校验阶段报错，而非运行期静默失败

清理:      重置 fixture 仓库
""")

write_yaml("SEC-NAME-01-001", build_yaml(
    "SEC-NAME-01-001", ["security", "compatibility"], "security", "P0",
    "Secret/变量名含特殊字符时不可导致意外求值或权限绕过", "INTENT-SEC-024",
    {"repo_fixture": "with-secrets", "secrets": ["MY-VAR"], "variables": {}, "branch_protection": "default"},
    {"event": "workflow_dispatch", "as": "maintainer", "params": {}},
    "on:\n  workflow_dispatch:\njobs:\n  special-name:\n    name: Test special secret name\n    runs-on: [dedicate-hosted, x64, large]\n    steps:\n      - name: Use hyphen secret\n        run: |\n          echo \"value is ${{ secrets.MY-VAR }}\"",
    [
        {"type": "negative", "target": "run_logs", "must_not_contain_secret": "MY-VAR"},
        {"type": "positive", "target": "run_status", "equals": "success_or_yaml_error"}
    ],
    "fixture"
))

print("b8 done")
