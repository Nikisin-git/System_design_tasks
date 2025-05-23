from typing import List, Optional
from datetime import datetime


class Trip:
    """
    Доменная модель поездки (Trip).
    """

    def __init__(
        self,
        trip_id: int,
        route_id: int,
        driver_user_id: int,
        start_time: datetime,
        max_passengers: int,
        passenger_ids: Optional[List[int]],
    ):
        self.trip_id = trip_id
        self.route_id = route_id
        self.driver_user_id = driver_user_id
        self.start_time = start_time
        self.max_passengers = max_passengers
        self.passenger_ids = passenger_ids or []

    def dict(self) -> dict:
        return {
            "trip_id": self.trip_id,
            "route_id": self.route_id,
            "driver_user_id": self.driver_user_id,
            "start_time": self.start_time.isoformat(),
            "max_passengers": self.max_passengers,
            "passenger_ids": self.passenger_ids,
        }

    def __repr__(self):
        return (
            f"Trip(id={self.trip_id}, route_id={self.route_id}, driver_id={self.driver_user_id})"
        )
