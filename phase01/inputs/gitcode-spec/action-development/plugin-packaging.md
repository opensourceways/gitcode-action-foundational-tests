<!-- source: https://docs.gitcode.com/docs/help/home/org_project/pipeline/action-development/plugin-packaging | fetched: 2026-07-20 -->

# 插件打包

AtomGit Actions 插件需要执行构建命令打出可执行的 js 文件，在流水线上直接引用执行。通过配置 `package.json` 进行构建编排。

## 构建配置示例（TS 工程）

```json
{
  "name": "gitcode-actions-plugin-demo",
  "version": "1.0.11",
  "description": "demo插件",
  "main": "main.js",
  "scripts": {
    "build": "tsc",
    "package-main": "ncc build lib/main.js",
    "package-stop": "ncc build lib/stop.js -o dist/stop && move dist\\stop\\main.js dist\\stop.js && rmdir /S /Q dist\\stop",
    "test": "jest",
    "all": "npm run build && npm run package-main && npm run package-stop",
    "dev": "npm run build && npm run package"
  },
  "devDependencies": {
    "@actions/core": "^1.11.1",
    "@types/node": "^22.7.6"
  },
  "dependencies": {
    "axios": "^1.7.7"
  }
}
```

## 构建步骤

1. **编译**：`npm run build` — 执行 TypeScript 编译
2. **打包**：`npm run package-main` 和 `npm run package-stop` — 使用 ncc 打包为单文件
3. **一键构建**：`npm run all` — 编译 + 打包
