from sqlalchemy.exc import IntegrityError

from app.core.security import hash_password, verify_password
from app.models import User
from app.repositories.user import UserRepository


class DuplicateUsernameError(ValueError):
    pass


class AuthService:
    def __init__(self, users: UserRepository) -> None:
        self.users = users

    async def register(
        self,
        username: str,
        password: str,
        nickname: str,
    ) -> User:
        if await self.users.get_by_username(username) is not None:
            raise DuplicateUsernameError

        try:
            return await self.users.create(
                username=username,
                password_hash=hash_password(password),
                nickname=nickname,
            )
        except IntegrityError as error:
            await self.users.session.rollback()
            raise DuplicateUsernameError from error

    async def authenticate(self, username: str, password: str) -> User | None:
        user = await self.users.get_by_username(username)
        if user is None or not verify_password(password, user.password_hash):
            return None
        return user
