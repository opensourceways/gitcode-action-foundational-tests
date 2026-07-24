## 校验失败 · COMPAT-TOKEN-01-002 · GITHUB_TOKEN 在 GitCode 中应为空且不应被静默映射

**判定结果**: ERROR

**根因**: API 调用失败 (WAF 拦截 / 网络错误)
**响应**: {"status_code": 418, "text": "<!DOCTYPE html><html style=\"height:100%;width:100%\"><head><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\" /><meta http-equiv=\"Server\" content=\"CloudWAF\" /><title id=\"title\">访问被拦截！</title></head><body onload=\"bindall()\" style=\"height:100

- 维度: compatibility | 优先级: P0
- intent_ref: INTENT-COMPAT-020 | trigger: workflow_dispatch
