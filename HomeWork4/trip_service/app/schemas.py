from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class TripCreateRequest(BaseModel):
    """
    Схема для создания поездки.
    """

    route_id: int = Field(..., examples=[10])
    driver_user_id: int = Field(..., examples=[1])
    start_time: datetime = Field(..., examples=["2025-03-28T10:00:00"])
    max_passengers: int = Field(..., examples=[4])


class TripResponse(BaseModel):
    """
    Схема для вывода информации о поездке.
    """

    trip_id: int
    route_id: int
    driver_user_id: int
    start_time: datetime
    max_passengers: int
    passenger_ids: List[int] = []

    class Config:
        from_attributes = True


class JoinTripRequest(BaseModel):
    """
    Схема для присоединения пользователя к поездке.
    """

    user_id: int = Field(..., examples=[2])
