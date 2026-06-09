# SQLAlchemy Base Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reusable common fields and optimistic locking to every SQLAlchemy model.

**Architecture:** Extend the existing declarative `Base` so concrete models inherit
the columns automatically. Use SQLAlchemy mapper configuration for versioning and
column defaults/update expressions for automatic persistence values.

**Tech Stack:** Python 3.12, SQLAlchemy 2.0, pytest

---

### Task 1: Define and verify common model fields

**Files:**
- Modify: `app/db/base.py`
- Create: `tests/test_db_base.py`

- [x] **Step 1: Write the failing mapping test**

Define a concrete test model inheriting from `Base`, then assert its inherited
column names, primary key, defaults, timestamp expressions, and mapper
`version_id_col`.

- [x] **Step 2: Run test to verify it fails**

Run: `uv run pytest tests/test_db_base.py -v`

Expected: FAIL because the common fields do not exist.

- [x] **Step 3: Write minimal implementation**

Add typed `mapped_column` attributes to `Base` and a declared mapper argument
that selects the inherited `lock_version` column.

- [x] **Step 4: Run focused and full tests**

Run: `uv run pytest tests/test_db_base.py -v`

Expected: PASS.

Run: `uv run pytest`

Expected: all tests PASS.
