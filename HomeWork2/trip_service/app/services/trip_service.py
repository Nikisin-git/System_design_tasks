from typing import Optional, List
from datetime import datetime
from app.repositories.trip_repository import TripRepository
from app.models import Trip


class TripService:
    """
    Бизнес-логика по работе с поездками.
    """

    def __init__(self, repo: TripRepository):
        self.repo = repo

    def create_trip(
        self, route_id: int, driver_user_id: int, start_time: datetime, max_passengers: int
    ) -> Trip:
        # Здесь можно было бы проверять, существует ли такой route_id в RouteService,
        # есть ли пользователь driver_user_id в UserService и т.д.
        # Пока что делаем упрощённо (никаких проверок).
        return self.repo.create_trip(
            route_id=route_id,
            driver_user_id=driver_user_id,
            start_time=start_time,
            max_passengers=max_passengers,
        )

    def get_trip(self, trip_id: int) -> Optional[Trip]:
        return self.repo.get_trip_by_id(trip_id)

    def list_trips(self) -> List[Trip]:
        return self.repo.list_trips()

    def join_trip(self, trip_id: int, user_id: int) -> Trip:
        trip = self.repo.get_trip_by_id(trip_id)
        if not trip:
            raise ValueError(f"Trip with id {trip_id} not found")

        if user_id in trip.passenger_ids:
            raise ValueError(f"User {user_id} already joined trip {trip_id}")

        if len(trip.passenger_ids) >= trip.max_passengers:
            raise ValueError(f"No more seats available in trip {trip_id}")

        # Добавляем пассажира
        trip.passenger_ids.append(user_id)
        self.repo.update_trip(trip)
        return trip
