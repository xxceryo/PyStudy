# Agent Rules Index

本文件适用于整个仓库，仅作为 Agent 规则入口。执行任务前，应根据任务范围读取下列具体规则。

## Rule Files

- [项目结构与职责](agents/project.md)：项目架构、目录边界和分层约定。
- [开发规范](agents/development.md)：环境、依赖管理和常用开发命令。
- [测试规范](agents/testing.md)：测试编写、执行和验证要求。
- [编码规范](agents/coding-style.md)：Python 编码风格和实现约束。
- [Git 规范](agents/git.md)：分支、提交和安全操作要求。
- [Agent 规则维护规范](agents/agents-maintenance.md)：新增或修改 Agent 规则时必须遵循的要求。

## Usage

1. 始终读取本索引。
2. 读取与当前任务相关的规则文件；修改代码时至少读取项目、开发、测试和编码规范。
3. 涉及 Git 操作时读取 Git 规范。
4. 涉及本文件或 `agents/` 目录时读取 Agent 规则维护规范。
5. 更深层目录中的 `AGENTS.md` 可为其目录树补充或覆盖规则；直接用户指令优先级最高。
