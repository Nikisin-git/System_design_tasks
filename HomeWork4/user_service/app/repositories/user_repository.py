from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth import get_password_hash
from app.models import User

class UserRepository:
    
    @staticmethod
    async def create_user(
        session: AsyncSession,
        login: str,
        password: str,
        first_name: str,
        last_name: str,
        email: str,
        age: int
    ) -> User:
        result = await session.execute(select(User).where(User.login == login))
        if result.scalar_one_or_none():
            raise ValueError("User with this login already exists")

        user = User(
            login=login,
            full_name=f"{first_name} {last_name}",
            hashed_password=get_password_hash(password),
            email=email,
            age=age
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user


    @staticmethod
    async def get_by_login(session: AsyncSession, login: str) -> Optional[User]:
        result = await session.execute(select(User).where(User.login == login))
        return result.scalar_one_or_none()

    @staticmethod
    async def find_by_name(session: AsyncSession, first_name: str, last_name: str) -> List[User]:
        stmt = select(User)

        if first_name and last_name:
            stmt = stmt.where(User.full_name == f"{first_name} {last_name}")
        elif first_name:
            stmt = stmt.where(User.full_name.ilike(f"{first_name} %"))
        elif last_name:
            stmt = stmt.where(User.full_name.ilike(f"% {last_name}"))

        result = await session.execute(stmt)
        return result.scalars().all()