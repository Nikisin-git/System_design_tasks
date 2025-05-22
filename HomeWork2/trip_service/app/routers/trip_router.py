from typing import List
from fastapi import APIRouter, Depends, HTTPException
from app.schemas import TripCreateRequest, TripResponse, JoinTripRequest
from app.services.trip_service import TripService
from app.repositories.trip_repository import TripRepository
from app.auth import verify_token

router = APIRouter(prefix="/trips", tags=["trips"])
trip_service = TripService(repo=TripRepository())


@router.post("", response_model=TripResponse, dependencies=[Depends(verify_token)])
def create_trip(payload: TripCreateRequest):
    """
    Создание новой поездки.
    """
    try:
        new_trip = trip_service.create_trip(
            route_id=payload.route_id,
            driver_user_id=payload.driver_user_id,
            start_time=payload.start_time,
            max_passengers=payload.max_passengers,
        )
        return new_trip.dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/{trip_id}", response_model=TripResponse, dependencies=[Depends(verify_token)])
def get_trip_by_id(trip_id: int):
    """
    Получение информации о поездке по ID.
    """
    trip = trip_service.get_trip(trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Поездка не найдена")
    return trip.dict()


@router.get("", response_model=List[TripResponse], dependencies=[Depends(verify_token)])
def list_all_trips():
    """
    Получение списка всех поездок.
    """
    trips = trip_service.list_trips()
    return [t.dict() for t in trips]


@router.post("/{trip_id}/join", response_model=TripResponse, dependencies=[Depends(verify_token)])
def join_trip(trip_id: int, request: JoinTripRequest):
    """
    Подключение пользователей к поездке
    """
    try:
        trip = trip_service.join_trip(trip_id, request.user_id)
        return trip.dict()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
