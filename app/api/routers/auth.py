from fastapi import APIRouter, HTTPException, status

from app.api.dependencies import CurrentUser, DatabaseSession
from app.core.config import get_settings
from app.core.security import create_access_token
from app.repositories.user import UserRepository
from app.schemas.auth import LoginRequest, LoginResponse, RegisterRequest
from app.schemas.user import PublicUser
from app.services.auth import AuthService, DuplicateUsernameError

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post(
    "/register",
    response_model=PublicUser,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    request: RegisterRequest,
    session: DatabaseSession,
) -> PublicUser:
    service = AuthService(UserRepository(session))
    try:
        user = await service.register(
            username=request.username,
            password=request.password,
            nickname=request.nickname,
        )
    except DuplicateUsernameError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Username is already registered",
        ) from error
    return PublicUser.model_validate(user)


@router.post("/login", response_model=LoginResponse)
async def login(
    request: LoginRequest,
    session: DatabaseSession,
) -> LoginResponse:
    user = await AuthService(UserRepository(session)).authenticate(
        request.username,
        request.password,
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    settings = get_settings()
    return LoginResponse(
        access_token=create_access_token(user.id),
        expires_in=settings.access_token_expire_seconds,
        user=PublicUser.model_validate(user),
    )


@router.get("/me", response_model=PublicUser)
async def get_me(current_user: CurrentUser) -> PublicUser:
    return PublicUser.model_validate(current_user)
