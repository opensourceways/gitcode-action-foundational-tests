<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/upload-download-artifacts | fetched: 2026-07-20 -->

# 上传和下载制品

**适用场景**：当你需要在 job 之间传递构建产物（如编译结果、测试报告、打包文件等）时。

## 前提条件

- 已确认使用的 artifact 插件版本。
- 已确认制品大小不超过限制。

## 快速示例

```yaml
name: build-and-package
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - uses: checkout
      - name: Build
        run: |
          mkdir -p dist
          echo "hello" > dist/app.txt
      - name: Upload artifact
        uses: upload-artifact
        with:
          name: app-dist
          path: dist/
  deploy:
    runs-on: [ubuntu-latest, x64, small]
    needs: build
    steps:
      - name: Download artifact
        uses: download-artifact
        with:
          name: app-dist
          path: dist/
      - name: Verify artifact
        run: cat dist/app.txt
```

## 配置说明

### 上传制品

```yaml
steps:
  - name: Upload artifact
    uses: upload-artifact
    with:
      name: app-dist
      path: dist/
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 制品名称，同一 workflow 中唯一 |
| `path` | 是 | 上传路径，支持文件和目录，支持 glob 模式 |

**上传多个路径：**

```yaml
steps:
  - name: Upload multiple paths
    uses: upload-artifact
    with:
      name: build-output
      path: |
        dist/
        reports/
        coverage/
```

### 下载制品

```yaml
steps:
  - name: Download artifact
    uses: download-artifact
    with:
      name: app-dist
      path: dist/
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `name` | 是 | 要下载的制品名称 |
| `path` | 否 | 下载目标路径，默认为当前工作目录 |

**下载当前 workflow 所有制品：**

```yaml
steps:
  - name: Download all artifacts
    uses: download-artifact
    with:
      path: artifacts/
```
