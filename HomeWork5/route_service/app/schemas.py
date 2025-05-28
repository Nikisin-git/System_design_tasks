from pydantic import BaseModel, Field
from typing import List, Optional


class RouteCreateRequest(BaseModel):
    """
    Данные при создании нового маршрута.
    """

    start_point: str = Field(..., examples=["Москва"])
    end_point: str = Field(..., examples=["Ярославль"])
    waypoints: Optional[List[str]] = Field(default=None, examples=[["Михнево", "Истра"]])
    distance: int = Field(..., example=270)


class RouteResponse(BaseModel):
    """
    Схема ответа для информации о маршруте.
    """

    route_id: str
    start_point: str
    end_point: str
    waypoints: List[str] = []
    distance: int

    class Config:
        from_attributes = True
