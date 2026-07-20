<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/plugin-security-specification | fetched: 2026-07-20 -->

# 插件安全规范

插件安全规范要求敏感数据禁止硬编码、必须通过安全输入获取并加密存储和及时清理，且所有输入参数须经严格验证。

## 敏感数据处理

### 敏感数据识别

以下类型的数据被视为敏感数据：

- 身份认证信息（token、password、api-key 等）
- 个人身份信息（姓名、邮箱、手机号等）
- 项目机密信息（商业计划、源代码等）
- 系统配置信息（数据库连接串等）

### 处理原则

1. **禁止硬编码**：严禁在代码中硬编码敏感信息
2. **使用安全输入**：通过安全的输入机制获取敏感数据
3. **加密存储**：敏感数据在存储和传输过程中必须加密
4. **最小化暴露**：只在必要时暴露敏感数据
5. **及时清理**：使用完毕后及时清理内存中的敏感数据

### 代码示例

```javascript
// 错误：硬编码 token
const token = 'hardcoded-token-12345';

// 正确：通过安全输入获取 token
const token = core.getInput('token');

// 使用后及时清理
function cleanupSensitiveData() {
  if (token) {
    token = null;
  }
}
```

## 输入参数安全验证

所有输入参数必须经过严格验证：

| 参数类型 | 验证规则 | 示例 |
|---------|--------|------|
| 字符串 | 长度限制、格式校验 | 邮箱格式、URL 格式 |
| 数字 | 范围检查、类型检查 | 正数、负数范围限制 |
| 文件 | 路径安全检查 | 防止路径遍历攻击 |
| 列表 | 元素验证、长度限制 | 最大元素数量限制 |
