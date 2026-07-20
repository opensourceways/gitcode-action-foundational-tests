<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/runner-management/configuring-images-toolchains | fetched: 2026-07-20 -->

# 配置运行镜像和工具链

**适用场景**：当托管 Runner 的预装工具链不符合项目需求——需要特定语言版本、专用依赖、或完整构建环境——可通过 `container` 字段指定自定义 Docker 镜像。

## 配置说明

### container 字段基本用法

```yaml
# 配置运行镜像和工具链
stages:
  - name: build
    jobs:
      - name: maven-build
        runs-on: {ubuntu-24,x64,medium}
        container:
          image: maven:3.9-eclipse-temurin-21     # 使用 Maven + JDK21 镜像
        steps:
          - run: mvn clean package
```

### container 字段完整配置

```yaml
jobs:
  - name: custom-env
    runs-on: {ubuntu-24,x64,medium}
    container:
      image: myregistry.example.com/myapp-builder:2.0
      credentials:
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
      env:
        BUILD_MODE: release
        JAVA_HOME: /usr/lib/jvm/java-21
      volumes:
        - /data/cache:/cache
      options: --hostname builder-node --memory 12g
    steps:
      - run: make release
```

| 字段 | 说明 |
|------|------|
| `image` | Docker 镜像全称（含标签） |
| `credentials` | 私有镜像仓库认证，引用 Secret |
| `env` | 容器内环境变量 |
| `volumes` | 挂载卷（Host → Container） |
| `options` | Docker run 附加参数 |

### 自定义镜像构建

若公共镜像无法满足需求，可自建镜像并推送至镜像仓库：

```dockerfile
# Dockerfile.ci
FROM ubuntu:24.04
RUN apt-get update && apt-get install -y \
    build-essential cmake git \
    python3.12 python3-pip \
    nodejs npm \
    && rm -rf /var/lib/apt/lists/*
RUN pip3 install pytest black mypy
WORKDIR /workspace
```

```bash
docker build -t myregistry.example.com/ci-builder:1.0 -f Dockerfile.ci .
docker push myregistry.example.com/ci-builder:1.0
```

```yaml
# .gitcode/workflows/custom.yml
jobs:
  - name: full-build
    runs-on: {ubuntu-24,x64,medium}
    container:
      image: myregistry.example.com/ci-builder:1.0
      credentials:
        username: ${{ secrets.REGISTRY_USERNAME }}
        password: ${{ secrets.REGISTRY_PASSWORD }}
    steps:
      - run: pytest
      - run: make build
```
