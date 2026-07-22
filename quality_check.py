import os
import re

text_dir = "phase01/runs/2026-07-21-02/cases/text"
yaml_dir = "phase01/runs/2026-07-21-02/cases/yaml"

new_cases = [
    ("REL-CANCEL-02-004", "INTENT-REL-037"),
    ("REL-CANCEL-02-005", "INTENT-REL-038"),
    ("REL-PREEMPT-02-001", "INTENT-REL-039"),
    ("REL-PREEMPT-02-002", "INTENT-REL-040"),
    ("SEC-REFPROT-02-001", "INTENT-SEC-037"),
    ("SEC-ENV-WAIT-02-001", "INTENT-SEC-038"),
    ("SEC-CONT-CRED-02-001", "INTENT-SEC-039"),
    ("SEC-CONT-ISOLATE-02-001", "INTENT-SEC-040"),
    ("COMP-CONTAINER-02-001", "INTENT-COMP-009"),
    ("COMP-MATRIX-02-005", "INTENT-COMP-010"),
    ("COMP-MATRIX-02-006", "INTENT-COMP-011"),
    ("COMP-MATRIX-02-007", "INTENT-COMP-012"),
    ("COMP-ACTOR-02-001", "INTENT-COMP-013"),
    ("COMPAT-MATRIX-02-001", "INTENT-COMPAT-065"),
    ("COMPAT-EXPRFN-02-002", "INTENT-COMPAT-066"),
    ("COMPAT-EXPRFN-02-003", "INTENT-COMPAT-067"),
    ("USE-SUMMARY-02-001", "INTENT-USE-026"),
    ("USE-BADGE-02-001", "INTENT-USE-027"),
]

issues = []
for case_id, intent_ref in new_cases:
    md_path = os.path.join(text_dir, f"{case_id}.md")
    yaml_path = os.path.join(yaml_dir, f"{case_id}.yaml")
    
    # Check text case exists
    if not os.path.exists(md_path):
        issues.append(f"{case_id}: text case missing")
        continue
    
    # Check yaml exists
    if not os.path.exists(yaml_path):
        issues.append(f"{case_id}: yaml case missing")
        continue
    
    with open(md_path, "r", encoding="utf-8") as f:
        md_content = f.read()
    
    with open(yaml_path, "r", encoding="utf-8") as f:
        yaml_content = f.read()
    
    # 1. 维度标签非空
    if "维度标签:" not in md_content or not re.search(r"维度标签:\s*\[\S+\]", md_content):
        issues.append(f"{case_id}: 维度标签缺失或为空")
    
    # 2. run 序列 02
    if "-02-" not in case_id:
        issues.append(f"{case_id}: ID 不含 run 序列 02")
    
    # 3. intent_ref 溯源
    if f"溯源意图:  {intent_ref}" not in md_content:
        issues.append(f"{case_id}: 文本用例未溯源到 {intent_ref}")
    
    if f"intent_ref: {intent_ref}" not in yaml_content:
        issues.append(f"{case_id}: YAML 未溯源到 {intent_ref}")
    
    # 4. teardown.reset
    if "清理:      fixture" not in md_content:
        issues.append(f"{case_id}: 文本用例未声明 fixture 清理")
    if "reset: fixture" not in yaml_content:
        issues.append(f"{case_id}: YAML 未声明 teardown.reset=fixture")
    
    # 5. 安全用例检查
    if case_id.startswith("SEC-"):
        if "不应" not in md_content:
            issues.append(f"{case_id}: 安全用例文本层不含「不应发生」")
        if "type: negative" not in yaml_content:
            issues.append(f"{case_id}: 安全用例 YAML 层无 negative 断言")
    
    # 6. 无真实密钥（简单检查常见敏感词）
    banned = ["password123", "secret123", "token123", "192.168.", "10.0.0.", "admin:admin"]
    for b in banned:
        if b in md_content or b in yaml_content:
            issues.append(f"{case_id}: 发现疑似真实敏感值 '{b}'")

if issues:
    print("Quality issues found:")
    for i in issues:
        print(f"  - {i}")
else:
    print("All 18 new cases passed quality checks.")
