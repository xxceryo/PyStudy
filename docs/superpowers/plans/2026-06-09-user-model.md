# User Model Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a SQLAlchemy `User` model with authentication identity, editable profile fields, and inherited persistence fields.

**Architecture:** Define the model in a focused `app.models.user` module and re-export it from the models package. Verify the declarative mapping directly with SQLAlchemy inspection tests without accessing an external database.

**Tech Stack:** Python 3.12, SQLAlchemy 2.0, pytest

---

### Task 1: Define and export the user model

**Files:**
- Create: `app/models/user.py`
- Modify: `app/models/__init__.py`
- Create: `tests/test_user_model.py`

- [x] **Step 1: Write the failing mapping tests**

Create tests that import `User` from `app.models` and inspect its table. Verify
the table name, user-specific and inherited columns, nullability, string
lengths, unique indexes, and package export.

- [x] **Step 2: Run tests to verify they fail**

Run: `uv run pytest tests/test_user_model.py -v`

Expected: collection fails because `User` is not exported from `app.models`.

- [x] **Step 3: Write minimal implementation**

Create `User(Base)` with table name `users` and typed SQLAlchemy 2.x
`mapped_column` fields for `username`, `password_hash`, `nickname`,
`avatar_url`, `signature`, and `phone_number`. Export `User` from
`app.models`.

- [x] **Step 4: Run focused tests**

Run: `uv run pytest tests/test_user_model.py -v`

Expected: all user model tests pass.

- [x] **Step 5: Run full test suite**

Run: `uv run pytest`

Expected: all tests pass.
