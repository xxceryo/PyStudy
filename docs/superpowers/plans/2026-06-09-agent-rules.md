# Agent Rules Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 初始化以根目录索引和分类规则文件组成的 Agent 规则体系。

**Architecture:** 根目录 `AGENTS.md` 作为唯一入口，仅声明适用范围和规则索引。具体、可执行的规则按职责拆分到 `agents/` 目录，降低后续维护冲突。

**Tech Stack:** Markdown, Git

---

### Task 1: Create Rule Index

**Files:**
- Create: `AGENTS.md`

- [ ] 创建根目录规则索引，列出六个规则文件及其职责。
- [ ] 声明规则读取和优先级约定。

### Task 2: Create Concrete Rules

**Files:**
- Create: `agents/project.md`
- Create: `agents/development.md`
- Create: `agents/testing.md`
- Create: `agents/coding-style.md`
- Create: `agents/git.md`
- Create: `agents/agents-maintenance.md`

- [ ] 按项目当前 FastAPI、uv、pytest 和分层结构编写具体规则。
- [ ] 增加 Git 工作流、提交消息和安全操作要求。
- [ ] 增加修改 `AGENTS.md` 与 `agents/` 规则文件时的维护要求。

### Task 3: Verify

**Files:**
- Verify: `AGENTS.md`
- Verify: `agents/*.md`

- [ ] 检查索引中的每个链接均存在。
- [ ] 检查 Git 状态，确保只包含预期文件。
