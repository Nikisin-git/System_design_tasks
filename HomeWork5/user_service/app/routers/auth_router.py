from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_async_session
from app.schemas import TokenRequest, TokenResponse
from app.repositories.user_repository import UserRepository
from app.auth import create_access_token, verify_password

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=TokenResponse)
async def login_for_access_token(
    data: TokenRequest,
    session: AsyncSession = Depends(get_async_session),
):
    user = await UserRepository.get_by_login(session, data.username)
    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    token = create_access_token(username=user.login)
    return TokenResponse(access_token=token)