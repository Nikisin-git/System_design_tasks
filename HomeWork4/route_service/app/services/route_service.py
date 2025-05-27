from typing import List, Optional
from app.models import Route
from app.repositories.route_repository import RouteRepository


class RouteService:

    def __init__(self, repo: RouteRepository):
        self.repo = repo

    async def create_new_route(self, start: str, end: str, waypoints: list[str], distance:int) -> Route:
        # Здесь можно вызвать MapService, посмотреть расстояние и т.п.
        # Пока что просто создаём
        return await self.repo.create_route(start, end, waypoints, distance)

    async def get_route(self, route_id: str) -> Optional[Route]:
        return await self.repo.get_route_by_id(route_id)

    async def list_routes(self) -> List[Route]:
        return await self.repo.get_all_routes()

    async def search_routes(
        self,
        start_point: Optional[str] = None,
        end_point: Optional[str] = None,
    ) -> List[Route]:
        return await self.repo.find_routes(start_point, end_point)