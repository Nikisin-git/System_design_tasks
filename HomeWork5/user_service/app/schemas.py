from typing import Optional
from pydantic import BaseModel, Field


class UserCreateRequest(BaseModel):
    """
    Схема для создания пользователя.
    """

    login: str = Field(..., examples=["johndoe"])
    password: str = Field(..., examples=["secret"])
    first_name: str = Field(..., examples=["John"])
    last_name: str = Field(..., examples=["Doe"])
    email: str = Field(..., examples=["johndoe@gmail.com"])
    age: int = Field(..., examples=["21"])

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    login: str
    full_name: str
    email: Optional[str] = None
    age: Optional[int] = None

    class Config:
        from_attributes = True


class TokenRequest(BaseModel):
    """
    Схема для запроса токена (логин/пароль).
    """

    username: str
    password: str


class TokenResponse(BaseModel):
    """
    Схема для ответа при успешной аутентификации.
    """

    access_token: str
    token_type: str = "bearer"
