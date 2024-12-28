from typing import Optional

from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str = ""
    token_type: str = ""

class CreateUserRequest(BaseModel):
    username: str = ""
    name: str
    email: EmailStr
    password: str


class CreatePostRequest(BaseModel):
    caption: str
    post_media_url: str
    background_music_url: Optional[str]
    category: Optional[str]
