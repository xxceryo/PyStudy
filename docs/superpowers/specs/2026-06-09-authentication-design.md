# Authentication Design

## Goal

Implement username-based registration, login, and Bearer Token authentication
for the existing `User` model. Add matching Vue pages for a virtual item
marketplace while leaving the primary marketplace business area as an
authenticated empty state.

## Scope

This change includes:

- Username, password, and nickname registration.
- Username and password login.
- JWT Bearer access tokens with a 24-hour lifetime.
- Current-user authentication.
- Frontend login, registration, protected marketplace shell, and logout.
- A retro game marketplace visual direction.

This change does not include:

- Refresh tokens, token revocation, or a server-side logout endpoint.
- Phone-number login, SMS verification, roles, or permissions.
- Profile editing or marketplace business features.
- Product listings, inventory, orders, payments, or messaging.

## Authentication Decisions

The API returns a Bearer access token after login. The frontend stores it in
`localStorage` and sends it in the `Authorization: Bearer <token>` header.
Logging out only removes the token from frontend storage. Tokens expire after
24 hours and are not revoked before expiration.

JWT claims contain only the user ID, issued-at time, and expiration time. The
token is signed using an application secret supplied through configuration.
Missing, invalid, expired, or unverifiable tokens return `401 Unauthorized`.

## Backend Architecture

Follow the project's existing layers:

- `app/repositories/`: query and create users through an async SQLAlchemy
  session.
- `app/services/`: enforce registration rules, hash and verify passwords, and
  authenticate credentials.
- `app/schemas/`: define request and public response contracts.
- `app/core/`: provide password hashing and JWT encode/decode utilities.
- `app/api/`: expose authentication routes and resolve the current user from a
  Bearer token.

Raw passwords are never persisted. Password hashing uses an established
password-hashing library, and JWT handling uses an established JOSE/JWT
library. Deleted users cannot log in or access authenticated endpoints.

## API Contract

### `POST /auth/register`

Request:

```json
{
  "username": "player_one",
  "password": "secure-password",
  "nickname": "Player One"
}
```

Validation:

- `username`: 3 to 50 characters.
- `password`: 8 to 72 characters.
- `nickname`: 1 to 50 characters.

Success returns `201 Created` with public user information. An existing
username returns `409 Conflict`.

### `POST /auth/login`

Request:

```json
{
  "username": "player_one",
  "password": "secure-password"
}
```

Success returns `200 OK`:

```json
{
  "access_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": 1,
    "username": "player_one",
    "nickname": "Player One",
    "avatar_url": null,
    "signature": null
  }
}
```

Unknown usernames and incorrect passwords return the same `401 Unauthorized`
response to avoid disclosing account existence.

### `GET /auth/me`

Requires a Bearer token. Success returns the current public user. Missing,
invalid, expired, or deleted-user tokens return `401 Unauthorized`.

## Public User Data

Public user responses include:

- `id`
- `username`
- `nickname`
- `avatar_url`
- `signature`

They never include `password_hash`, `phone_number`, deletion state, or lock
version.

## Frontend Architecture

Add Vue Router with these routes:

- `/login`: username and password login form.
- `/register`: username, password, nickname, and password confirmation form.
- `/`: authenticated marketplace shell with an empty business state.

An auth module owns the token and current user state. At startup, it loads the
token from `localStorage` and calls `/auth/me`. Route guards redirect anonymous
users away from the marketplace and redirect authenticated users away from the
login and registration pages. Protected API responses with status `401` clear
the stored token.

The Vite development server proxies `/auth` requests to the FastAPI backend so
the frontend uses relative API paths during local development.

## Visual Design

The UI follows a retro game marketplace direction:

- Deep purple background with subtle perspective-grid details.
- Cyan primary actions and magenta highlights.
- Strong display typography, sharp cards, and small pixel-inspired accents.
- Clear, accessible form controls despite the stylized shell.

Login and registration share the same branded authentication layout. The
protected marketplace page keeps the brand shell, current-user summary, and
logout control, while its primary content displays a focused "market under
construction" empty state.

Static image generation is unnecessary for the initial implementation because
the visual direction can be built with CSS shapes, grids, and typography.

## Error Handling

- Request validation errors use FastAPI's standard `422` response.
- Duplicate usernames return `409`.
- Invalid credentials and authentication failures return `401`.
- Unexpected persistence or infrastructure errors propagate as server errors
  and are not presented as credential failures.
- Frontend forms display field validation and API errors without discarding
  entered non-password values.

## Testing And Verification

Backend tests use an isolated async SQLite database and dependency overrides;
they do not access MySQL, Redis, or external services. Tests cover:

- Successful registration and public response shape.
- Password hash persistence instead of raw password persistence.
- Duplicate username rejection.
- Successful login and usable access token.
- Uniform rejection of unknown users and incorrect passwords.
- Missing, invalid, and expired token rejection.
- Current-user retrieval.
- Deleted-user rejection.

The frontend currently has no test framework. Verify it with TypeScript type
checking, a production Vite build, and browser checks for registration, login,
route protection, authentication restoration, and logout.

