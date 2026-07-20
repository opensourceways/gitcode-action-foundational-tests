<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/writing-pipelines/using-dependency-cache | fetched: 2026-07-20 -->

# 使用依赖缓存

**适用场景**：当你需要缓存依赖包（npm、Maven、pip、Gradle 等）以加速后续构建时。

## 前提条件

- 已确认缓存目录路径。
- 已确认使用的 cache 插件版本（推荐 v4）。
- 理解缓存 key 和 restore-keys 的设计原则。

## 快速示例

```yaml
name: ci-with-cache
on:
  push:
    branches:
      - main
jobs:
  build:
    runs-on: [ubuntu-latest, x64, small]
    steps:
      - uses: checkout
      - name: Cache npm dependencies
        uses: cache
        with:
          path: ~/.npm
          key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
          restore-keys: |
            npm-${{ runner.os }}-
      - name: Install and test
        run: |
          npm ci
          npm test
```

## 配置说明

### cache 插件参数

```yaml
steps:
  - name: Cache dependencies
    uses: cache
    with:
      path: ~/.npm
      key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        npm-${{ runner.os }}-
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `path` | 是 | 缓存目录路径，支持单路径和多路径 |
| `key` | 是 | 缓存键，精确匹配时直接恢复缓存 |
| `restore-keys` | 否 | 前缀匹配的兜底恢复键列表，按顺序尝试 |

### 缓存匹配机制

1. 首先尝试精确匹配 `key`。
2. 精确匹配失败时，按 `restore-keys` 列表顺序尝试前缀匹配。
3. 前缀匹配恢复的是最近一次同前缀的缓存。
4. 所有匹配都失败时，step 执行后会将 `path` 内容保存为新缓存。

### 多路径缓存

```yaml
steps:
  - name: Cache multiple paths
    uses: cache
    with:
      path: |
        ~/.npm
        ~/.cache/pip
        node_modules
      key: deps-${{ runner.os }}-${{ hashFiles('package-lock.json', 'requirements.txt') }}
```

### 常见语言缓存示例

**Node.js / npm**

```yaml
steps:
  - name: Cache npm
    uses: cache
    with:
      path: ~/.npm
      key: npm-${{ runner.os }}-${{ hashFiles('package-lock.json') }}
      restore-keys: |
        npm-${{ runner.os }}-
  - run: npm ci
```

**Java / Maven**

```yaml
steps:
  - name: Cache Maven
    uses: cache
    with:
      path: ~/.m2/repository
      key: maven-${{ runner.os }}-${{ hashFiles('**/pom.xml') }}
      restore-keys: |
        maven-${{ runner.os }}-
  - run: mvn -B test
```

**Java / Gradle**

```yaml
steps:
  - name: Cache Gradle
    uses: cache
    with:
      path: |
        ~/.gradle/caches
        ~/.gradle/wrapper
      key: gradle-${{ runner.os }}-${{ hashFiles('**/*.gradle*', 'gradle-wrapper.properties') }}
      restore-keys: |
        gradle-${{ runner.os }}-
  - run: ./gradlew build
```

**Python / pip**

```yaml
steps:
  - name: Cache pip
    uses: cache
    with:
      path: ~/.cache/pip
      key: pip-${{ runner.os }}-${{ hashFiles('requirements.txt') }}
      restore-keys: |
        pip-${{ runner.os }}-
  - run: pip install -r requirements.txt
```

**Go**

```yaml
steps:
  - name: Cache Go modules
    uses: cache
    with:
      path: ~/go/pkg/mod
      key: go-${{ runner.os }}-${{ hashFiles('go.sum') }}
      restore-keys: |
        go-${{ runner.os }}-
  - run: go build ./...
```
