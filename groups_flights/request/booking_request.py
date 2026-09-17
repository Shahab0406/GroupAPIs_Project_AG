from dataclasses import dataclass

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class BookingRequest:
    group_id: int
    adult_seats_requested: int
    child_seats_requested: int
