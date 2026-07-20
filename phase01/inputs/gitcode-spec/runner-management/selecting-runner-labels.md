<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/runner-management/selecting-runner-labels | fetched: 2026-07-20 -->

# 选择 Runner 标签

**适用场景**：当你需要精确控制 job 在哪类 Runner 上执行——指定操作系统、架构、资源规格、或自定义特征（GPU、特定工具链）——需要理解标签匹配规则。

## 配置说明

### 标签类型对照

| Runner 类型 | 标签格式 | 示例 |
|-----------|---------|------|
| 官方托管 | 三段式 `{os},{arch},{spec}` 或组合标签 | `{ubuntu-24,x64,small}` |
| 官方托管（默认） | `default` | `default`（等效 [ubuntu-latest, x64, small]） |
| 自托管 | `self-hosted` + 自定义标签 | `[self-hosted, linux, gpu]` |

### 匹配规则

**规则一：全匹配**

`runs-on` 中的所有标签必须同时存在于 Runner 的标签集合中，才视为匹配。

```yaml
# 选择 Runner 标签
# ✅ 匹配
runs-on: [self-hosted, linux, x64]
# ✅ 匹配
runs-on: [self-hosted, npu, cann]
# ❌ 不匹配（缺少 macos）
runs-on: [self-hosted, pypto]
```

**规则二：default 等价**

`runs-on: default` 等价于 `runs-on: [ubuntu-latest, x64, small]`。
