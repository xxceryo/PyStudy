# Authentication Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add username registration, JWT Bearer login, current-user authentication, and matching Vue marketplace authentication pages.

**Architecture:** Keep persistence in a user repository, authentication rules in a service, token and password primitives in `app.core.security`, and HTTP contracts in schemas and auth routes. The Vue application uses Vue Router and a small auth store/API module backed by `localStorage`.

**Tech Stack:** Python 3.12, FastAPI, SQLAlchemy async, pwdlib Argon2, PyJWT, pytest, Vue 3, TypeScript, Vue Router, Vite

---

### Task 1: Security primitives and configuration

**Files:**
- Modify: `app/core/config.py`
- Create: `app/core/security.py`
- Modify: `.env.example`
- Create: `tests/test_security.py`
- Modify: `pyproject.toml`
- Modify: `uv.lock`

- [x] Write failing tests for password hashing/verification, JWT user ID round trips, and expired/invalid token rejection.
- [x] Run `uv run pytest tests/test_security.py -v` and verify failure because security helpers do not exist.
- [x] Add `pwdlib[argon2]` and `pyjwt`, then implement recommended password hashing and HS256 JWT helpers using configured secret and 24-hour lifetime.
- [x] Run `uv run pytest tests/test_security.py -v` and verify all security tests pass.

### Task 2: Registration and login API

**Files:**
- Create: `app/schemas/user.py`
- Create: `app/schemas/auth.py`
- Create: `app/repositories/user.py`
- Create: `app/services/auth.py`
- Create: `app/api/routers/auth.py`
- Modify: `app/api/router.py`
- Create: `tests/test_auth_api.py`
- Modify: `pyproject.toml`
- Modify: `uv.lock`

- [x] Write failing isolated API tests for successful registration, password-hash persistence, duplicate usernames, successful login, and uniform invalid-credential rejection.
- [x] Run focused auth API tests and verify they fail because routes do not exist.
- [x] Add async SQLite test support and implement schemas, repository, service, and `/auth/register` plus `/auth/login`.
- [x] Run focused auth API tests and verify they pass.

### Task 3: Current-user Bearer authentication

**Files:**
- Modify: `app/api/dependencies.py`
- Modify: `app/api/routers/auth.py`
- Modify: `tests/test_auth_api.py`

- [x] Write failing tests for `/auth/me`, missing/invalid tokens, expired tokens, and deleted-user rejection.
- [x] Run focused tests and verify expected authentication failures.
- [x] Implement Bearer token parsing and current-user database lookup, then add `/auth/me`.
- [x] Run focused tests and verify all authentication scenarios pass.

### Task 4: Vue authentication experience

**Files:**
- Modify: `frontend/package.json`
- Modify: `frontend/package-lock.json`
- Modify: `frontend/vite.config.ts`
- Modify: `frontend/index.html`
- Modify: `frontend/src/main.ts`
- Modify: `frontend/src/App.vue`
- Create: `frontend/src/router.ts`
- Create: `frontend/src/auth.ts`
- Create: `frontend/src/api.ts`
- Create: `frontend/src/types.ts`
- Create: `frontend/src/styles.css`
- Create: `frontend/src/views/LoginView.vue`
- Create: `frontend/src/views/RegisterView.vue`
- Create: `frontend/src/views/MarketplaceView.vue`

- [x] Install Vue Router and define typed API/auth modules with `localStorage` restoration and `401` cleanup.
- [x] Add routes and guards for anonymous/authenticated redirects.
- [x] Build the retro game marketplace login, registration, and protected empty-state pages.
- [x] Configure the Vite `/auth` development proxy and run `npm run build`.

### Task 5: Integrated verification

**Files:**
- Modify only files required by issues discovered during verification.

- [x] Run `uv run pytest`.
- [x] Run `npm run build` in `frontend/`.
- [x] Start the application where local infrastructure permits and verify the frontend routes and visual layout in a browser.
- [x] Run `git diff --check` and inspect the final diff for scope and secrets.
