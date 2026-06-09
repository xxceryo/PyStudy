# 项目结构与职责

## 项目概览

本项目是使用 Python 3.12、FastAPI、SQLAlchemy、Redis 和 MySQL 构建的后端项目，使用 `uv` 管理依赖和命令。

## 目录职责

- `app/api/`：API 路由、依赖项和接口层逻辑。
- `app/core/`：配置及跨模块核心能力。
- `app/db/`：数据库、Redis 连接和基础持久化设施。
- `app/models/`：SQLAlchemy 数据模型。
- `app/repositories/`：数据访问逻辑。
- `app/schemas/`：请求、响应及内部数据结构。
- `app/services/`：业务逻辑和业务流程编排。
- `tests/`：自动化测试。
- `doc/`：项目使用和技术文档。
- `docs/superpowers/`：设计与实施计划记录。

## 分层约束

- API 层负责协议转换、输入校验和响应组织，不直接实现复杂业务逻辑。
- Service 层负责业务规则，不直接依赖 HTTP 请求或响应对象。
- Repository 层封装数据访问，不承载业务决策。
- Schema 与 Model 分离，不直接将数据库模型作为外部 API 契约。
- 新代码应放入职责最匹配的现有目录，除非新增边界具有明确必要性。
