from pydantic import BaseModel


class UserCreate(BaseModel):
    id: str
    username: str
    follower_count: int
    location: str
    verified: bool
    bot: bool