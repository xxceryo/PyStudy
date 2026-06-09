from pydantic import BaseModel, ConfigDict


class PublicUser(BaseModel):
    id: int
    username: str
    nickname: str | None
    avatar_url: str | None
    signature: str | None

    model_config = ConfigDict(from_attributes=True)
