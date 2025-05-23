from typing import Dict


class User:
    """
    Упрощенная модель пользователя.
    """

    def __init__(self, user_id: int, login: str, password: str, first_name: str, last_name: str, email:str, age:int):
        self.user_id = user_id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.email=email
        self.age=age

    def __repr__(self):
        return f"User(id={self.user_id}, login={self.login})"

    def dict(self) -> Dict:
        """
        Возвращает представление пользователя в виде словаря.
        """
        return {
            "user_id": self.user_id,
            "login": self.login,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
        }
