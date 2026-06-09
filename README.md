# Python Study

FastAPI backend managed with uv, with a Vue 3 and TypeScript frontend managed with npm.

## 项目结构

```text
PyStudy/
├── app/
│   ├── api/                  # API 路由、依赖项和接口实现
│   │   └── routers/          # 按业务模块拆分的路由
│   ├── core/                 # 应用配置等核心功能
│   ├── db/                   # 数据库与 Redis 连接管理
│   ├── models/               # SQLAlchemy 数据模型
│   ├── repositories/         # 数据访问层
│   ├── schemas/              # 请求与响应数据模型
│   ├── services/             # 业务逻辑层
│   └── main.py               # FastAPI 应用入口
├── frontend/                 # Vue 3 + TypeScript + Vite 前端
│   ├── public/               # 前端静态资源
│   ├── src/                  # 前端应用源码
│   ├── package.json          # 前端依赖与命令
│   └── vite.config.ts        # Vite 配置
├── doc/                      # 项目文档
├── tests/                    # 后端自动化测试
├── start.ps1                 # Windows 一键启动前后端开发服务
├── .env.example              # 环境变量示例
├── pyproject.toml            # 项目元数据和依赖配置
└── uv.lock                   # uv 依赖锁定文件
```

应用采用分层结构：API 层负责接收请求，Service 层处理业务逻辑，
Repository 层负责数据访问，Schema 和 Model 分别定义接口数据与数据库实体。

## Development

Start the backend and frontend together on Windows:

```powershell
.\start.ps1
```

The script creates `.env` from `.env.example` when needed, installs missing
dependencies, and stops both services when you press `Ctrl+C`.

Start the backend separately:

```powershell
Copy-Item .env.example .env
uv run fastapi dev app/main.py
```

Run tests:

```powershell
uv run pytest
```

Run the frontend:

```powershell
Set-Location frontend
npm install
npm run dev
```

Build the frontend:

```powershell
Set-Location frontend
npm run build
```
