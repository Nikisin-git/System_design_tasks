from typing import Dict
from app.models import Trip

fake_trips_db: Dict[int, Trip] = {}

fake_trip_id_sequence = 0


def get_next_trip_id() -> int:
    global fake_trip_id_sequence
    fake_trip_id_sequence += 1
    return fake_trip_id_sequence
