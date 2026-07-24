#!/usr/bin/env python3
"""
批量为 text 用例添加参照来源字段
基于用例标题关键词和 intent_ref 推断 inputs 来源文件
"""
import os, re, glob

TEXT_DIR = "phase01/runs/2026-07-23-01/cases/text"

# 关键词 → 来源映射（按优先级排序，先匹配的先应用）
KEYWORD_SOURCES = [
    # existing-cases
    (r"KEEP-TC", "inputs/existing-cases/cases.md"),

    # 安全类
    (r"secret|脱敏|TOKEN|权限|permission|fork.*PR|注入|injection|攻击|供应链|TOCTOU|SSRF|DOS|mask|cache.*隔离|artifact.*隔离|侧信道|环境审批", "inputs/security-knowledge/issues.md; inputs/github-reference/security/"),

    # Runner / 标签 / 资源
    (r"runner|runs-on|标签|self-hosted|K8s|GPU|内网|资源|磁盘|内存|CPU|规格|xlarge|small|medium|large|镜像拉取|container", "inputs/gitcode-spec/runner-management/selecting-runner-labels.md; inputs/platform-config/instance-config.md"),

    # 触发事件
    (r"push|pull_request|schedule|cron|触发|事件|comment|issue|tag|分支|paths|branches|types|workflow_dispatch|workflow_call", "inputs/gitcode-spec/core-concepts/trigger-events.md"),

    # 变量 / 表达式 / 上下文
    (r"env|vars|变量|context|上下文|表达式|expression|函数|运算符|success|failure|always|contains|hashFiles|toJson|join|fromJSON|null|字面量", "inputs/gitcode-spec/core-concepts/variables-secrets-context-expressions.md; inputs/gitcode-spec/syntax-reference/expressions.md; inputs/gitcode-spec/syntax-reference/context.md"),

    # workflow 结构 / jobs / steps
    (r"job|step|workflow|stage|post|needs|并发|concurrency|timeout|if|条件|output|依赖|矩阵|matrix|include|exclude|嵌套", "inputs/gitcode-spec/core-concepts/workflow-job-step-action.md; inputs/gitcode-spec/writing-pipelines/configure-jobs.md"),

    # artifact / cache
    (r"artifact|制品|cache|缓存|upload|download|hashFiles", "inputs/gitcode-spec/core-concepts/artifacts-and-cache.md"),

    # Action 开发 / 使用
    (r"action\.yml|Action|插件|checkout|setup-java|setup-node|uses", "inputs/gitcode-spec/action-development/top-level-fields.md"),

    # 工作流命令
    (r"set-env|add-path|set-output|add-mask|group|stop-commands|workflow.*命令|summary|annotation|debug|error|warning", "inputs/gitcode-spec/syntax-reference/workflow-commands.md"),

    # 日志 / UI / 可观测性
    (r"日志|log|搜索|下载|徽标|badge|rerun|状态|view|结果|渲染|Markdown", "inputs/gitcode-spec/running-pipelines/view-job-logs.md; inputs/gitcode-spec/running-pipelines/view-run-results.md"),

    # YAML / 目录 / 文件位置
    (r"YAML|目录|dir|\.gitcode|\.github|workflow.*位置|文件位置|未知字段|非法值|校验", "inputs/gitcode-spec/writing-pipelines/workflow-file-location-structure.md"),

    # 兼容性 / 迁移
    (r"兼容|compat|迁移|migrat|GitHub|差异|降级|等价", "inputs/github-reference/reference/workflow-syntax.md; inputs/gitcode-spec/COMPAT-NOTES.md"),

    # 脚本 / shell
    (r"shell|脚本|script|bash|powershell|执行|run", "inputs/gitcode-spec/syntax-reference/runner-images-tools.md; inputs/gitcode-spec/writing-pipelines/using-script-commands.md"),

    # 性能 / 可靠性边界
    (r"性能|perf|压力|洪泛|flood|边界|超时|timeout|并发.*压测|大规格|日志.*性能|镜像拉取", "inputs/platform-config/instance-config.md"),

    # 历史问题
    (r"历史|已知.*bug|故障|问题|修复", "inputs/history/issues-encountered.md"),
]

# 维度默认来源
DIM_DEFAULT = {
    "completeness": "inputs/gitcode-spec/",
    "compatibility": "inputs/github-reference/reference/workflow-syntax.md; inputs/gitcode-spec/COMPAT-NOTES.md",
    "security": "inputs/security-knowledge/issues.md; inputs/github-reference/security/",
    "reliability": "inputs/platform-config/instance-config.md; inputs/gitcode-spec/core-concepts/runner-and-environment.md",
    "usability": "inputs/gitcode-spec/; inputs/business-context/README.md",
}

def infer_source(case_id, title, dimension, intent_ref):
    # 1. KEEP-TC 溯源
    if intent_ref and "KEEP-TC" in intent_ref:
        return "inputs/existing-cases/cases.md"

    # 2. 关键词匹配
    title_lower = title.lower()
    for pattern, source in KEYWORD_SOURCES:
        if re.search(pattern, title_lower):
            return source

    # 3. 维度默认
    return DIM_DEFAULT.get(dimension, "inputs/gitcode-spec/")

def process_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # 提取字段
    case_id_match = re.search(r"用例 ID:\s+(\S+)", content)
    title_match = re.search(r"标题:\s+(.+)", content)
    dim_match = re.search(r"维度:\s+(.+)", content)
    intent_match = re.search(r"溯源意图:\s+(\S+)", content)

    case_id = case_id_match.group(1) if case_id_match else ""
    title = title_match.group(1).strip() if title_match else ""
    dimension = dim_match.group(1).strip() if dim_match else ""
    intent_ref = intent_match.group(1).strip() if intent_match else ""

    source = infer_source(case_id, title, dimension, intent_ref)

    # 检查是否已有参照来源
    if "参照来源:" in content:
        return False, f"已存在参照来源: {case_id}"

    # 在"溯源意图"行后插入"参照来源"
    new_line = f"参照来源:  {source}\n"

    # 匹配溯源意图行及其后的内容
    pattern = r"(溯源意图:\s+\S+\n)"
    if re.search(pattern, content):
        content = re.sub(pattern, r"\1" + new_line, content, count=1)
    else:
        # 如果没有溯源意图，在标题前插入
        content = re.sub(r"(标题:\s+)", new_line + r"\1", content, count=1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    return True, f"已更新: {case_id} -> {source}"

def main():
    files = sorted(glob.glob(os.path.join(TEXT_DIR, "*.md")))
    updated = 0
    skipped = 0
    errors = []

    for filepath in files:
        try:
            ok, msg = process_file(filepath)
            if ok:
                updated += 1
            else:
                skipped += 1
            if updated <= 5 or not ok:
                print(msg)
        except Exception as e:
            errors.append(f"{filepath}: {e}")
            print(f"ERROR: {filepath}: {e}")

    print(f"\n总计: {len(files)} 个文件, 更新 {updated} 个, 跳过 {skipped} 个, 错误 {len(errors)} 个")

if __name__ == "__main__":
    main()
