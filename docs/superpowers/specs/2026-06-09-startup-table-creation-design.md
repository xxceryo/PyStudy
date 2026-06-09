# Startup Table Creation Design

## Goal

Ensure all registered SQLAlchemy model tables exist before the FastAPI
application starts accepting requests.

## Design

Add `initialize_database()` to `app/db/session.py`. It imports the models
package so model tables are registered in `Base.metadata`, opens an async
engine transaction, and calls `Base.metadata.create_all` through
`AsyncConnection.run_sync`.

Add an `auto_create_tables` boolean setting. Its code default is `False`, while
`.env.example` enables it for local development with
`PYSTUDY_AUTO_CREATE_TABLES=true`.

At the beginning of the FastAPI lifespan, call `initialize_database()` before
yielding only when `auto_create_tables` is enabled. Keep the existing Redis and
database shutdown cleanup behavior.

`create_all()` checks for existing tables and creates only missing tables. It
does not migrate or modify existing table structures. Database connection or
DDL failures propagate and prevent application startup.

## Verification

Add isolated tests that verify:

- Database initialization invokes `Base.metadata.create_all` through an async
  engine connection.
- The setting defaults to disabled and can be enabled through the environment.
- Application lifespan initializes the database before accepting requests only
  when configured.
- Existing shutdown cleanup still runs.
