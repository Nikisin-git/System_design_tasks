from typing import Optional, List
from app.models import User
from app.repositories.user_repository import UserRepository


class UserService:
    """
    Бизнес-логика работы с пользователями.
    """

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, login: str, password: str, first_name: str, last_name: str, age:int) -> User:
        existing = self.repo.get_by_login(login)
        if existing:
            raise ValueError(f"Логин '{login}' уже занят")
        return self.repo.create_user(login, password, first_name, last_name, age)

    def get_user_by_login(self, login: str) -> Optional[User]:
        return self.repo.get_by_login(login)

    def find_users_by_name(self, first_name: str, last_name: str) -> List[User]:
        return self.repo.find_by_name(first_name, last_name)
