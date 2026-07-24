## 校验失败 · SEC-NAME-01-002 · 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

**判定结果**: ERROR

**根因**: API 调用失败 (WAF 拦截 / 网络错误)
**响应**: {"status_code": 418, "text": "<!DOCTYPE html><html style=\"height:100%;width:100%\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><meta http-equiv=\"Server\" content=\"CloudWAF\" /><title id=\"title\">访问被拦截！</title></head><body onload=\"bindall()\" style=\"height:100

**影响**:
- **阻塞性**: ⚪无影响 — 触发了 WAF/网关拦截（HTTP 418），测试本身未能提交或执行，非安全缺陷
- **静默性**: 🟢明确报错 — API 返回 HTTP 418 及 CloudWAF 拦截页面，错误信息清晰可观测
- **影响面**: 🟢单用例 — 仅影响 SEC-NAME-01-002 的本次单次提交尝试
- **综合**: 测试因 WAF 拦截（HTTP 418）未能执行，属网络/网关层环境问题，非平台安全机制缺陷
- **是否有规避手段**: 是 — 确认 WAF 拦截规则后将测试请求加入白名单或调整请求特征

- 维度: security | 优先级: P0
- intent_ref: INTENT-SEC-025 | trigger: workflow_dispatch
