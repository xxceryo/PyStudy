# User Model Design

## Goal

Add a SQLAlchemy user model that stores authentication identity and editable
profile information while inheriting the project's common persistence fields.

## Model

Create `User` in `app/models/user.py` as a concrete subclass of
`app.db.base.Base` with table name `users`.

The model defines these fields:

- `username`: required `String(50)`, unique, and indexed. This is the stable
  login identifier.
- `password_hash`: required `String(255)`. Raw passwords must not be stored.
- `nickname`: optional `String(50)`, not unique, and editable.
- `avatar_url`: optional `String(500)`.
- `signature`: optional `String(255)`.
- `phone_number`: optional `String(32)`, unique, and indexed when present.

The inherited fields are `id`, `deleted`, `lock_version`, `gmt_create`, and
`gmt_modified`. Updating a nickname or other profile field relies on the
inherited `gmt_modified` update behavior.

Export `User` from `app/models/__init__.py` so model consumers can import it
from the package.

## Scope

This change only defines the persistence model. Password hashing behavior,
profile update services, API schemas, routes, repositories, and database
migrations are outside this change.

## Verification

Add SQLAlchemy mapping tests that verify:

- The user-specific and inherited columns are present.
- Required and optional columns have the intended nullability.
- Username and phone number have unique indexes.
- Declared string lengths match the design.
- `User` is exported from `app.models`.
