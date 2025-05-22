from fastapi import APIRouter, HTTPException
from app.schemas import TokenRequest, TokenResponse
from app.repositories.user_repository import UserRepository
from app.auth import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
def login_for_access_token(data: TokenRequest):
    """
    Эндпоинт для получения JWT-токена по логину и паролю.
    """
    user = UserRepository.get_by_login(data.username)
    if not user or user.password != data.password:
        raise HTTPException(status_code=400, detail="Неверное имя пользовователя или пароль")
    token = create_access_token(username=user.login)
    return TokenResponse(access_token=token)
