## 校验失败 · SEC-NAME-01-002 · 通过 printenv 或进程枚举获取 ATOMGIT_TOKEN/secrets 时日志中必须保持脱敏

**判定结果**: ERROR

**根因**: API 调用失败 (WAF 拦截 / 网络错误)
**响应**: {"status_code": 418, "text": "<!DOCTYPE html><html style=\"height:100%;width:100%\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><meta http-equiv=\"Server\" content=\"CloudWAF\" /><title id=\"title\">访问被拦截！</title></head><body onload=\"bindall()\" style=\"height:100

- 维度: security | 优先级: P0
- intent_ref: INTENT-SEC-025 | trigger: workflow_dispatch
