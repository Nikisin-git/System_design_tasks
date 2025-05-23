from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException

from app.schemas import UserCreateRequest, UserResponse
from app.services.user_service import UserService
from app.repositories.user_repository import UserRepository
from app.auth import verify_token

router = APIRouter(prefix="/users", tags=["users"])

user_service = UserService(repo=UserRepository())


@router.post("", response_model=UserResponse, dependencies=[Depends(verify_token)])
def create_user(payload: UserCreateRequest):
    """
    Создание нового пользователя .
    """
    try:
        user = user_service.register_user(
            login=payload.login,
            password=payload.password,
            first_name=payload.first_name,
            last_name=payload.last_name,
            email=payload.email,
            age=payload.age,
        )
        return user.dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{login}", response_model=UserResponse, dependencies=[Depends(verify_token)])
def get_user_by_login(login: str):
    """
    Поиск пользователя по логину 
    """
    user = user_service.get_user_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user.dict()


@router.get("", response_model=List[UserResponse], dependencies=[Depends(verify_token)])
def search_users(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
):
    """
    Поиск пользователей по имени и фамилии.
    """
    users = user_service.find_users_by_name(first_name or "", last_name or "")
    return [u.dict() for u in users]
