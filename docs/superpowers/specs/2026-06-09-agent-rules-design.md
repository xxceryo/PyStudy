# Agent Rules Design

## Goal

为仓库初始化可维护的 Agent 规则体系。根目录 `AGENTS.md` 仅负责规则索引，具体规则存放在 `agents/` 目录。

## Structure

- `AGENTS.md`：说明适用范围、读取顺序并链接具体规则。
- `agents/project.md`：项目架构和目录职责。
- `agents/development.md`：环境、依赖和开发命令。
- `agents/testing.md`：测试要求。
- `agents/coding-style.md`：Python 编码规范。
- `agents/git.md`：Git 工作流和提交规范。
- `agents/agents-maintenance.md`：修改 Agent 规则时的维护规范。

## Principles

- 根索引保持简洁，不重复具体规则。
- 规则使用明确、可执行的表述。
- 规则发生变化时同步维护索引和相关文件。
- 不包含密钥、口令或仅适用于个人环境的配置。

## Verification

检查所有索引链接指向存在的文件，并确认规则覆盖项目、开发、测试、编码、Git 和规则维护六个主题。
