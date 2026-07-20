# inputs/gitcode-api/ （**必需**）— 已补充 ✅

GitCode Actions API 参考手册。agent 基于此文档组装 API 调用参数，辅助第二部分测试执行。

来源: https://docs.gitcode.com/docs/apis/ (Actions 分类) | 2026-07-20

## 内容

- **[api-reference.md](api-reference.md)** — 20 个 v8 Actions API 端点完整参考
  - Base URL: `https://api.gitcode.com`
  - 认证: OAuth2.0 `access_token` query parameter
  - 典型调用场景（验证 run 状态·检查 job 日志·验证并发·清理 artifact）
  - curl 示例

## 消费方

- **case-writer agent**: 编译 YAML 时，为 API 可验证的断言标注可用的 API 端点
- **第二部分 harness**: 执行时直接依据本文档组装 API 调用

## 已补充 / 20 个端点 / 2026-07-20
