from typing import List, Optional
from app.db import fake_trips_db, get_next_trip_id
from app.models import Trip
from datetime import datetime


class TripRepository:
    """
    Репозиторий для CRUD-операций с поездками.
    """

    @staticmethod
    def create_trip(
        route_id: int, driver_user_id: int, start_time: datetime, max_passengers: int
    ) -> Trip:
        new_id = get_next_trip_id()
        trip = Trip(
            trip_id=new_id,
            route_id=route_id,
            driver_user_id=driver_user_id,
            start_time=start_time,
            max_passengers=max_passengers,
        )
        fake_trips_db[new_id] = trip
        return trip

    @staticmethod
    def get_trip_by_id(trip_id: int) -> Optional[Trip]:
        return fake_trips_db.get(trip_id)

    @staticmethod
    def list_trips() -> List[Trip]:
        return list(fake_trips_db.values())

    @staticmethod
    def update_trip(trip: Trip) -> None:
        """
        Обновляет поездку (в памяти).
        """
        fake_trips_db[trip.trip_id] = trip
