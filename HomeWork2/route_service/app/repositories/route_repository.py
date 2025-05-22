from typing import List, Optional
from app.db import fake_routes_db, get_next_route_id
from app.models import Route


class RouteRepository:
    """
    Репозиторий для CRUD операций по маршрутам.
    """

    @staticmethod
    def create_route(start: str, end: str, waypoints: list[str], distance_length: int) -> Route:
        new_id = get_next_route_id()
        new_route = Route(route_id=new_id, start_point=start, end_point=end, waypoints=waypoints, distance=distance_length)
        fake_routes_db[new_id] = new_route
        return new_route

    @staticmethod
    def get_route_by_id(route_id: int) -> Optional[Route]:
        return fake_routes_db.get(route_id)

    @staticmethod
    def get_all_routes() -> List[Route]:
        return list(fake_routes_db.values())
