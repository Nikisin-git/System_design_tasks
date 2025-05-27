from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.schemas import RouteCreateRequest, RouteResponse
from app.services.route_service import RouteService
from app.repositories.route_repository import RouteRepository
from app.auth import verify_token

router = APIRouter(prefix="/routes", tags=["routes"])

service = RouteService(repo=RouteRepository())


@router.post("", response_model=RouteResponse, dependencies=[Depends(verify_token)])
async def create_route(data: RouteCreateRequest):
    """
    Создать новый маршрут.
    """
    route = await service.create_new_route(
        start=data.start_point,
        end=data.end_point,
        waypoints=data.waypoints or [],
        distance=data.distance
    )
    return route.dict()


@router.get("/{route_id}", response_model=RouteResponse, dependencies=[Depends(verify_token)])
async def get_route_by_id(route_id: str):
    """
    Поиск маршрута по ID
    """
    route = await service.get_route(route_id)
    if not route:
        raise HTTPException(status_code=404, detail="Маршрут не найден")
    return route.dict()

@router.get("", response_model=List[RouteResponse], dependencies=[Depends(verify_token)])
async def list_all_routes(
    start_point: Optional[str] = Query(None, description="Начальная точка маршрута"),
    end_point: Optional[str] = Query(None, description="Конечная точка маршрута"),
):

    """
    Поиск маршрута.
    """
    if start_point or end_point:
        routes = await service.search_routes(start_point, end_point)
    else:
        routes = await service.list_routes()
    return [r.dict() for r in routes]