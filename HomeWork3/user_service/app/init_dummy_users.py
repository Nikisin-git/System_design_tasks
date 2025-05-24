
import asyncio
import os
import sys

from faker import Faker
from sqlalchemy import select, func

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app.auth import get_password_hash
from app.db import async_session_maker
from app.models import User

fake = Faker()


async def create_dummy_users(count: int = 100):
    async with async_session_maker() as session:
        # Подсчитаем количество пользователей
        result = await session.execute(select(func.count()).select_from(User))
        user_count = result.scalar()

        if user_count >= 10:
            print(f"📦 Found {user_count} users — dummy users not needed.")
            return

        print(f"🚀 Found {user_count} users. Generating {count} dummy users...")

        for i in range(count):
            first_name = fake.first_name()
            last_name = fake.last_name()
            full_name = f"{first_name} {last_name}"
            login = f"user{i+1}"
            email=fake.email()
            age = fake.random_int(min=18, max=90)
            password = get_password_hash("secret")

            user = User(
                full_name=full_name,
                login=login,
                hashed_password=password,
                email=email,
                age=age
            )
            session.add(user)

        await session.commit()
        print("✅ Dummy users created!")


if __name__ == "__main__":
    asyncio.run(create_dummy_users())
