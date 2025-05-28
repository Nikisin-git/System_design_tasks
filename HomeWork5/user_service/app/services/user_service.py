from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.user_repository import UserRepository
from app.services.cache_service import UserCacheService

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo
        
    async def register_user(
        self,
        session: AsyncSession,
        login: str,
        password: str,
        first_name: str,
        last_name: str,
        email:str,
        age:int,
    ) -> User:
        
        existing = await self.repo.get_by_login(session, login)      
        if existing:
            raise ValueError(f"Логин '{login}' уже занят")
        
        user = await self.repo.create_user(session, login, password, first_name, last_name, email, age)
        await UserCacheService.set_user_by_login(user)
        return user


    async def get_user_by_login(self, session: AsyncSession, login: str) -> Optional[User]:
        cached = await UserCacheService.get_user_by_login(login)
        if cached:
            return User(**cached)

        user = await self.repo.get_by_login(session, login)
        if user:
            await UserCacheService.set_user_by_login(user)
        return user

    async def find_users_by_name(
        self, session: AsyncSession, first_name: str, last_name: str) -> List[User]:
        cached = await UserCacheService.get_search_users(first_name, last_name)
        if cached:
            return [User(**u) for u in cached]

    
        users = await self.repo.find_by_name(session, first_name, last_name)
        if users:
            users_data = [{"id": u.id, "full_name": u.full_name, "login": u.login} for u in users]
            await UserCacheService.set_search_users(first_name, last_name, users_data)
        return users

    async def update_user_by_login(
        self,
        session: AsyncSession,
        login: str,
        full_name: Optional[str] = None,
    ) -> Optional[User]:
        user = await self.repo.get_by_login(session, login)
        if not user:
            return None

        updated_user = await self.repo.update_user(session, user, full_name)
        await UserCacheService.set_user_by_login(updated_user)
        return updated_user
