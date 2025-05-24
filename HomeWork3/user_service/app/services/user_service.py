from typing import Optional, List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User
from app.repositories.user_repository import UserRepository


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
        
        return await self.repo.create_user(session, login, password, first_name, last_name, email, age)
        

    async def get_user_by_login(self, session: AsyncSession, login: str) -> Optional[User]:
        return await self.repo.get_by_login(session, login)

    async def find_users_by_name(
        self, session: AsyncSession, first_name: str, last_name: str
    ) -> List[User]:
        return await self.repo.find_by_name(session, first_name, last_name)
