# Environment Manager（env-manager）

## 类型
确定性脚本（Bash + git + api-client / IaC 工具）

## 职责
按用例的 `teardown.reset` 级别，在执行前准备隔离的测试环境，在执行后清理。**环境隔离是「可重复执行」承诺的物理前提。**

## 依赖
- `git`（clone/push/delete 仓库）
- `api-client` 脚本（GitCode API 操作）
- IaC 工具（Terraform / Ansible — 用于 `full_instance` 级重置）
- 平台配置：`phase01/inputs/platform-config/`（如存在）

## 输入
- 用例 YAML 的 `setup` 字段：`{ repo_fixture, secrets, variables, branch_protection }`
- 用例 YAML 的 `teardown` 字段：`{ reset: fixture|full_instance|none }`
- 平台访问凭证（API token、git credentials）

## 处理逻辑

### 阶段一：环境准备（setup）

```bash
# 1. 按 repo_fixture 创建/获取测试仓库
case "$REPO_FIXTURE" in
  with-secrets)
    # 从 fixture 模板克隆，预配置了 secrets 的仓库
    REPO_URL=$(create_fixture_repo "with-secrets")
    ;;
  clean)
    # 空仓库，无 secrets/variables
    REPO_URL=$(create_fixture_repo "clean")
    ;;
  with-branch-protection)
    REPO_URL=$(create_fixture_repo "with-branch-protection")
    ;;
  *)
    # 使用默认 clean fixture
    REPO_URL=$(create_fixture_repo "clean")
    ;;
esac

# 2. Clone 到临时工作区
WORK_DIR="/tmp/phase02-<case-id>-$(date +%s)"
git clone "$REPO_URL" "$WORK_DIR"
cd "$WORK_DIR"

# 3. 配置 secrets（通过 GitCode API 或 UI 操作）
for secret in "${SETUP_SECRETS[@]}"; do
  # 用占位符对应的测试值配置 secret
  # 注意：真实值从环境变量注入，不出现在脚本中
  api_set_secret "$OWNER" "$REPO" "$secret" "${TEST_SECRET_VALUE}"
done

# 4. 配置 variables
for var in "${SETUP_VARIABLES[@]}"; do
  api_set_variable "$OWNER" "$REPO" "$var" "${TEST_VAR_VALUE}"
done

# 5. 设置 branch protection（如需要）
if [ "$BRANCH_PROTECTION" != "none" ]; then
  api_set_branch_protection "$OWNER" "$REPO" "main" "$BRANCH_PROTECTION"
fi

# 6. 产出测试仓库上下文
echo "{\"owner\": \"$OWNER\", \"repo\": \"$REPO\", \"branch\": \"main\", \"work_dir\": \"$WORK_DIR\"}"
```

### Fixture 模板管理

预定义 fixture 模板：

| 模板名 | 内容 | 用途 |
|---|---|---|
| `clean` | 空仓库，无 secrets，无 branch protection，默认分支 main | 大多数功能/兼容性用例 |
| `with-secrets` | 预配置 `DEPLOY_TOKEN`、`API_KEY` 等占位 secret | 安全用例 |
| `with-branch-protection` | main 分支受保护，需 PR 合并 | PR/MR 安全用例 |
| `with-matrix` | 含多环境配置文件 | matrix 测试 |

Fixture 模板作为 GitCode 上的模板仓库维护，env-manager 通过 API clone/fork 创建测试实例。

### 阶段二：环境清理（teardown）

```bash
case "$RESET_LEVEL" in
  fixture)
    # 删除临时仓库
    api_delete_repo "$OWNER" "$REPO"
    # 清理临时工作区
    rm -rf "$WORK_DIR"
    ;;

  full_instance)
    # 触发 IaC 全量重置
    # 这会重建整个测试实例（runner、网络、存储等）
    terraform destroy -auto-approve
    terraform apply -auto-approve
    ;;

  none)
    # 不清理（仅用于不需要隔离的纯查询类用例）
    ;;
esac
```

### 环境健康检查

每次准备环境后，执行快速健康检查：

```bash
health_check() {
  # 1. 仓库可访问
  api_get_repo "$OWNER" "$REPO" || return 1

  # 2. Runner 在线
  RUNNERS=$(api_list_runners "$OWNER" "$REPO")
  [ $(echo "$RUNNERS" | jq 'length') -gt 0 ] || return 1

  # 3. API 可用
  api_get_run "$OWNER" "$REPO" "1" > /dev/null 2>&1  # 任意请求验证连通性

  return 0
}

if ! health_check; then
  echo "ENV_ERROR: 环境健康检查失败" && exit 1
fi
```

## 输出
- **环境上下文 JSON**：`{ owner, repo, branch, work_dir, fixture_type, reset_level }`
- 环境健康检查结果

## 环境变量
```bash
# 必需
GITCODE_ACCESS_TOKEN    # API 访问 token
GITCODE_USERNAME        # Git 操作身份

# 可选（full_instance 级重置时必需）
TF_VAR_gitcode_instance_id   # Terraform 实例 ID
ANSIBLE_INVENTORY            # Ansible inventory 路径
```

## 错误处理
- Fixture 创建失败 → `ENV_ERROR`，不执行该用例
- 环境健康检查失败 → `ENV_ERROR`，阻断后续依赖该环境的用例
- 清理失败 → 记录告警但不阻断后续用例（残留资源需人工清理）
- `full_instance` 重置失败 → **阻断**所有后续用例

## 质量要求
- 每条用例的环境完全隔离，无状态泄露
- Fixture 模板预先建好并验证可用
- 清理操作幂等（重复执行不报错）
- `full_instance` 级重置必须在无其他用例运行时执行
