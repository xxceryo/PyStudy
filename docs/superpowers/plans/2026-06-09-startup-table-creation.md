# Startup Table Creation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Optionally create missing registered SQLAlchemy tables during FastAPI startup.

**Architecture:** Encapsulate schema initialization in the database session module and conditionally call it from the FastAPI lifespan before yielding. Control the behavior with a production-safe setting that defaults to disabled and is enabled in the local `.env.example`. Tests replace external database and Redis operations with isolated async substitutes.

**Tech Stack:** Python 3.12, FastAPI lifespan, SQLAlchemy 2.0 asyncio, pytest

---

### Task 1: Initialize registered database tables

**Files:**
- Modify: `app/db/session.py`
- Create: `tests/test_db_session.py`

- [x] **Step 1: Write the failing database initialization test**
- [x] **Step 2: Run the focused test and verify it fails**
- [x] **Step 3: Implement `initialize_database()`**
- [x] **Step 4: Run the focused test and verify it passes**

### Task 2: Run initialization during application startup

**Files:**
- Modify: `app/core/config.py`
- Modify: `.env.example`
- Modify: `app/main.py`
- Modify: `tests/test_config.py`
- Modify: `tests/test_app.py`

- [x] **Step 1: Write failing configuration and lifespan tests**
- [x] **Step 2: Run the focused test and verify it fails**
- [x] **Step 3: Add the setting and conditionally call `initialize_database()`**
- [x] **Step 4: Run focused and full tests**
