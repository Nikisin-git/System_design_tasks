from typing import Dict
from app.models import User

"""
'Фейковая' база данных в памяти.
Словарь:
  key = user_id (int)
  value = объект User
"""
fake_users_db: Dict[int, User] = {}

# Для генерации айдишников
fake_user_id_sequence = 0


def get_next_user_id() -> int:
    global fake_user_id_sequence
    fake_user_id_sequence += 1
    return fake_user_id_sequence


# Создадим администратора при старте
admin_user = User(
    user_id=1, login="admin", password="secret", first_name="Admin", last_name="User", age="0"
)
fake_users_db[1] = admin_user
fake_user_id_sequence = 1
