import asyncio
from types import SimpleNamespace
from typing import Any

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app import main
from app.main import create_app


def test_health_check() -> None:
    client = TestClient(create_app())

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_lifespan_initializes_database_when_enabled(monkeypatch: Any) -> None:
    calls: list[str] = []

    async def initialize_database() -> None:
        calls.append("initialize_database")

    async def close_redis() -> None:
        calls.append("close_redis")

    async def close_database() -> None:
        calls.append("close_database")

    monkeypatch.setattr(main, "initialize_database", initialize_database, raising=False)
    monkeypatch.setattr(main, "close_redis", close_redis)
    monkeypatch.setattr(main, "close_database", close_database)
    monkeypatch.setattr(
        main,
        "get_settings",
        lambda: SimpleNamespace(auto_create_tables=True),
    )

    async def run_lifespan() -> None:
        async with main.lifespan(FastAPI()):
            assert calls == ["initialize_database"]

    asyncio.run(run_lifespan())

    assert calls == ["initialize_database", "close_redis", "close_database"]


def test_lifespan_skips_database_initialization_when_disabled(
    monkeypatch: Any,
) -> None:
    calls: list[str] = []

    async def initialize_database() -> None:
        calls.append("initialize_database")

    async def close_redis() -> None:
        calls.append("close_redis")

    async def close_database() -> None:
        calls.append("close_database")

    monkeypatch.setattr(main, "initialize_database", initialize_database, raising=False)
    monkeypatch.setattr(main, "close_redis", close_redis)
    monkeypatch.setattr(main, "close_database", close_database)
    monkeypatch.setattr(
        main,
        "get_settings",
        lambda: SimpleNamespace(auto_create_tables=False),
    )

    async def run_lifespan() -> None:
        async with main.lifespan(FastAPI()):
            assert calls == []

    asyncio.run(run_lifespan())

    assert calls == ["close_redis", "close_database"]
