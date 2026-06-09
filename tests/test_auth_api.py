import asyncio
from collections.abc import AsyncIterator, Iterator
from datetime import timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.security import create_access_token
from app.db.base import Base
from app.db.session import get_session
from app.main import create_app
from app.models import User


@pytest.fixture
def auth_client() -> Iterator[tuple[TestClient, async_sessionmaker[AsyncSession]]]:
    engine = create_async_engine("sqlite+aiosqlite://")
    session_factory = async_sessionmaker(engine, expire_on_commit=False)

    async def prepare_database() -> None:
        async with engine.begin() as connection:
            await connection.run_sync(Base.metadata.create_all)

    async def override_session() -> AsyncIterator[AsyncSession]:
        async with session_factory() as session:
            yield session

    asyncio.run(prepare_database())
    application = create_app()
    application.dependency_overrides[get_session] = override_session

    client = TestClient(application)
    yield client, session_factory

    client.close()
    asyncio.run(engine.dispose())


def register_user(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/auth/register",
        json={
            "username": "player_one",
            "password": "secure-password",
            "nickname": "Player One",
        },
    )
    assert response.status_code == 201
    return response.json()


def login_user(client: TestClient) -> dict[str, object]:
    response = client.post(
        "/auth/login",
        json={"username": "player_one", "password": "secure-password"},
    )
    assert response.status_code == 200
    return response.json()


def test_register_returns_public_user_and_stores_password_hash(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, session_factory = auth_client

    user_data = register_user(client)

    assert user_data == {
        "id": 1,
        "username": "player_one",
        "nickname": "Player One",
        "avatar_url": None,
        "signature": None,
    }

    async def load_user() -> User:
        async with session_factory() as session:
            return (await session.scalars(select(User))).one()

    stored_user = asyncio.run(load_user())
    assert stored_user.password_hash != "secure-password"


def test_register_rejects_duplicate_username(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, _ = auth_client
    register_user(client)

    response = client.post(
        "/auth/register",
        json={
            "username": "player_one",
            "password": "another-password",
            "nickname": "Another Player",
        },
    )

    assert response.status_code == 409
    assert response.json() == {"detail": "Username is already registered"}


def test_login_returns_usable_bearer_token(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, _ = auth_client
    register_user(client)

    login_data = login_user(client)

    assert login_data["token_type"] == "bearer"
    assert login_data["expires_in"] == 86400
    assert login_data["user"]["username"] == "player_one"
    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert response.status_code == 200
    assert response.json()["username"] == "player_one"


@pytest.mark.parametrize(
    ("username", "password"),
    [
        ("missing_user", "secure-password"),
        ("player_one", "incorrect-password"),
    ],
)
def test_login_rejects_invalid_credentials_uniformly(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
    username: str,
    password: str,
) -> None:
    client, _ = auth_client
    register_user(client)

    response = client.post(
        "/auth/login",
        json={"username": username, "password": password},
    )

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid username or password"}


@pytest.mark.parametrize(
    "headers",
    [
        {},
        {"Authorization": "Bearer invalid-token"},
    ],
)
def test_me_rejects_missing_or_invalid_token(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
    headers: dict[str, str],
) -> None:
    client, _ = auth_client

    response = client.get("/auth/me", headers=headers)

    assert response.status_code == 401
    assert response.headers["www-authenticate"] == "Bearer"


def test_me_rejects_deleted_user(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, session_factory = auth_client
    register_user(client)

    async def delete_user() -> None:
        async with session_factory() as session:
            user = (await session.scalars(select(User))).one()
            user.deleted = True
            await session.commit()

    asyncio.run(delete_user())

    response = client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {create_access_token(1)}"},
    )

    assert response.status_code == 401


def test_me_rejects_expired_token(
    auth_client: tuple[TestClient, async_sessionmaker[AsyncSession]],
) -> None:
    client, _ = auth_client
    register_user(client)

    response = client.get(
        "/auth/me",
        headers={
            "Authorization": (
                f"Bearer {create_access_token(1, expires_delta=timedelta(seconds=-1))}"
            )
        },
    )

    assert response.status_code == 401
