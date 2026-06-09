# 开发规范

## 环境与依赖

- 使用 Python 3.12 或项目声明的更高兼容版本。
- 后端使用 `uv` 管理依赖、虚拟环境和命令执行。
- 前端使用 `frontend/package.json` 声明兼容的 Node.js 版本，并使用 npm 管理依赖和命令。
- 新增依赖前确认标准库或现有依赖无法满足需求。
- 使用 `uv add <package>` 添加运行时依赖，使用 `uv add --dev <package>` 添加开发依赖。
- 依赖变化时必须同步提交 `pyproject.toml` 和 `uv.lock`。
- 前端使用 `npm install <package>` 添加运行时依赖，使用 `npm install --save-dev <package>` 添加开发依赖。
- 前端依赖变化时必须同步提交 `frontend/package.json` 和 `frontend/package-lock.json`。
- 不提交 `.env`、密钥、口令或其他敏感信息；环境变量示例维护在 `.env.example`。

## 常用命令

```powershell
uv sync
uv run fastapi dev app/main.py
uv run pytest
Set-Location frontend
npm install
npm run dev
npm run build
```

## 修改原则

- 修改前先阅读相关模块和测试，遵循现有实现模式。
- 保持改动聚焦，不夹带无关重构或格式化。
- 公共接口或配置项发生变化时，同步更新测试、示例和相关文档。
- 不手工修改生成文件或锁文件内容；使用对应工具更新。
