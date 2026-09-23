from dataclasses import dataclass, asdict

from dataclasses_json import dataclass_json
import json

from groups_flights.models import Airline

@dataclass_json
@dataclass(frozen=True)
class AirlineData:
    airline_id: int
    airline_display: str

    # @classmethod
    # def from_model(cls, airline: Airline) -> "AirlineData":
    #     return cls(
    #         airline_id=airline.id,
    #         airline_display=f"{airline.code} - {airline.name}",
    #     )
  
    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict())