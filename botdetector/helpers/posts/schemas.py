from pydantic import BaseModel


class PostCreate(BaseModel):
    text: str
    user_id: str
