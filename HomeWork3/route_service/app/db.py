from typing import Dict
from app.models import Route

"""
"Фейковая" база данных - словарь:
  key = ID маршрута
  value = Route
"""

fake_routes_db: Dict[int, Route] = {}

fake_route_id_sequence = 0


def get_next_route_id() -> int:
    global fake_route_id_sequence
    fake_route_id_sequence += 1
    return fake_route_id_sequence
