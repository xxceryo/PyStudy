from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.scalar(
            select(User).where(User.id == user_id, User.deleted.is_(False))
        )

    async def get_by_username(self, username: str) -> User | None:
        return await self.session.scalar(
            select(User).where(
                User.username == username,
                User.deleted.is_(False),
            )
        )

    async def create(
        self,
        username: str,
        password_hash: str,
        nickname: str,
    ) -> User:
        user = User(
            username=username,
            password_hash=password_hash,
            nickname=nickname,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user
