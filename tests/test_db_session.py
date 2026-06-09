import asyncio
from collections.abc import Callable
from types import TracebackType
from typing import Any

from app.db.base import Base
from app.db import session as db_session


class FakeConnection:
    def __init__(self) -> None:
        self.run_sync_callable: Callable[..., Any] | None = None

    async def run_sync(self, callable_: Callable[..., Any]) -> None:
        self.run_sync_callable = callable_


class FakeBeginContext:
    def __init__(self, connection: FakeConnection) -> None:
        self.connection = connection

    async def __aenter__(self) -> FakeConnection:
        return self.connection

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        return None


class FakeEngine:
    def __init__(self) -> None:
        self.connection = FakeConnection()

    def begin(self) -> FakeBeginContext:
        return FakeBeginContext(self.connection)


def test_initialize_database_creates_registered_tables(monkeypatch: Any) -> None:
    fake_engine = FakeEngine()
    monkeypatch.setattr(db_session, "engine", fake_engine)

    asyncio.run(db_session.initialize_database())

    assert fake_engine.connection.run_sync_callable == Base.metadata.create_all
