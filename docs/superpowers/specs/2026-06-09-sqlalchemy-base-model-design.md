# SQLAlchemy Base Model Design

## Goal

Provide every SQLAlchemy entity with common persistence fields equivalent to the
provided MyBatis-Plus example.

## Design

Extend the existing `app.db.base.Base` declarative base with these inherited
columns:

- `id`: auto-incrementing integer primary key.
- `deleted`: non-null boolean logical-delete marker, defaulting to `False`.
- `lock_version`: non-null integer optimistic-lock version, defaulting to `1`.
- `gmt_create`: database-generated creation timestamp.
- `gmt_modified`: database-generated timestamp on insert and refreshed by
  SQLAlchemy whenever an ORM update is emitted.

Configure each subclass mapper to use `lock_version` as SQLAlchemy's
`version_id_col`. Logical deletion remains explicit: repositories may filter or
update `deleted`, but the base model does not silently alter queries.

## Verification

Mapping tests define a concrete model subclass and verify inherited columns,
defaults, timestamp generation metadata, and optimistic-lock mapper
configuration.
