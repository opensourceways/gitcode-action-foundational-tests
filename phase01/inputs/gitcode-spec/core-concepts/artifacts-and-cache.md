<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/core-concepts/artifacts-and-cache | fetched: 2026-07-20 -->

# 制品与缓存

## 制品（Artifacts）

制品是工作流运行产生的文件，可跨任务传递：

```yaml
steps:
  - uses: upload-artifact
    with:
      name: build-output
      path: dist/
  - uses: download-artifact
    with:
      name: build-output
      path: ./app
```

## 缓存（Cache）

缓存用于加速依赖安装，避免重复下载：

```yaml
steps:
  - uses: cache
    with:
      key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
      path: ~/.npm
      restore-keys: |
        npm-${{ runner.os }}-
```

## 制品 vs 缓存

| 特性 | 制品 | 缓存 |
|------|------|------|
| 用途 | 传递构建产物（跨 Job） | 加速依赖安装（跨运行） |
| 生命周期 | 可设定保留天数 | 长期保留，LRU淘汰 |
| 访问范围 | 同 Workflow 的 Job 间 | 同仓库的所有运行 |
