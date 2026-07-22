import yaml
import jsonschema
import os
import sys

schema_path = "phase01/schema/executable-case.schema.yaml"
cases_dir = "phase01/runs/2026-07-21-02/cases/yaml"

new_cases = [
    "REL-CANCEL-02-004.yaml",
    "REL-CANCEL-02-005.yaml",
    "REL-PREEMPT-02-001.yaml",
    "REL-PREEMPT-02-002.yaml",
    "SEC-REFPROT-02-001.yaml",
    "SEC-ENV-WAIT-02-001.yaml",
    "SEC-CONT-CRED-02-001.yaml",
    "SEC-CONT-ISOLATE-02-001.yaml",
    "COMP-CONTAINER-02-001.yaml",
    "COMP-MATRIX-02-005.yaml",
    "COMP-MATRIX-02-006.yaml",
    "COMP-MATRIX-02-007.yaml",
    "COMP-ACTOR-02-001.yaml",
    "COMPAT-MATRIX-02-001.yaml",
    "COMPAT-EXPRFN-02-002.yaml",
    "COMPAT-EXPRFN-02-003.yaml",
    "USE-SUMMARY-02-001.yaml",
    "USE-BADGE-02-001.yaml",
]

with open(schema_path, "r", encoding="utf-8") as f:
    schema = yaml.safe_load(f)

failures = []
for case in new_cases:
    path = os.path.join(cases_dir, case)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        jsonschema.validate(instance=data, schema=schema)
        print(f"[PASS] {case}")
    except Exception as e:
        print(f"[FAIL] {case}: {e}")
        failures.append((case, str(e)))

print(f"\nTotal: {len(new_cases)}, Pass: {len(new_cases)-len(failures)}, Fail: {len(failures)}")

if failures:
    with open("phase01/runs/2026-07-21-02/cases/compile-failures.md", "w", encoding="utf-8") as f:
        f.write("# Compile Failures · 增量更新第2轮\n\n")
        for case, err in failures:
            f.write(f"## {case}\n\n```\n{err}\n```\n\n")
    sys.exit(1)
else:
    print("All cases passed schema validation.")
    sys.exit(0)
