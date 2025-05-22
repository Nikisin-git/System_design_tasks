from typing import List, Optional
from app.db import fake_users_db, get_next_user_id
from app.models import User


class UserRepository:
    """
    Репозиторий для работы с пользователями:
    создание, поиск по логину, поиск по имени и фамилии.
    Хранение - в памяти (fake_users_db).
    """

    @staticmethod
    def create_user(login: str, password: str, first_name: str, last_name: str, age:int) -> User:
        new_id = get_next_user_id()
        new_user = User(
            user_id=new_id,
            login=login,
            password=password,
            first_name=first_name,
            last_name=last_name,
            age=age,
        )
        fake_users_db[new_id] = new_user
        return new_user

    @staticmethod
    def get_by_login(login: str) -> Optional[User]:
        for user in fake_users_db.values():
            if user.login == login:
                return user
        return None

    @staticmethod
    def get_by_id(user_id: int) -> Optional[User]:
        return fake_users_db.get(user_id)

    @staticmethod
    def find_by_name(first_name: str, last_name: str) -> List[User]:
        result = []
        for user in fake_users_db.values():
            # Если не задана фамилия, ищем только по имени
            if first_name and last_name:
                if user.first_name == first_name and user.last_name == last_name:
                    result.append(user)
            elif first_name:
                if user.first_name == first_name:
                    result.append(user)
            elif last_name:
                if user.last_name == last_name:
                    result.append(user)
        return result
