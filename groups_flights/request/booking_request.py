import json
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation


@dataclass
class BookingRequest:
    adult_seats_requested: int
    child_seats_requested: int
    adult_price_per_seat: Decimal
    child_price_per_seat: Decimal
    total_amount: Decimal
    flight_number: str
    origin: str
    destination: str
    departure_datetime: datetime
    arrival_datetime: datetime
    travel_class: str
    baggage_allowance: str
    meal_available: bool

    @classmethod
    def from_dict(cls, data: dict) -> "BookingRequest":
        required_fields = [
            "adult_seats_requested",
            "child_seats_requested",
            "adult_price_per_seat",
            "child_price_per_seat",
            "total_amount",
            "flight_number",
            "origin",
            "destination",
            "departure_datetime",
            "arrival_datetime",
            "travel_class",
            "baggage_allowance",
            "meal_available",
        ]
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        try:
            return cls(
                adult_seats_requested=int(data["adult_seats_requested"]),
                child_seats_requested=int(data["child_seats_requested"]),
                adult_price_per_seat=Decimal(str(data["adult_price_per_seat"])),
                child_price_per_seat=Decimal(str(data["child_price_per_seat"])),
                total_amount=Decimal(str(data["total_amount"])),
                flight_number=str(data["flight_number"]).strip(),
                origin=str(data["origin"]).strip().upper(),
                destination=str(data["destination"]).strip().upper(),
                departure_datetime=datetime.fromisoformat(data["departure_datetime"]),
                arrival_datetime=datetime.fromisoformat(data["arrival_datetime"]),
                travel_class=str(data["travel_class"]).strip(),
                baggage_allowance=str(data["baggage_allowance"]).strip(),
                meal_available=bool(data["meal_available"]),
            )
        except (TypeError, ValueError, InvalidOperation) as exc:
            raise ValueError(f"Invalid booking request data: {exc}") from exc

    @classmethod
    def from_json(cls, body: bytes) -> "BookingRequest":
        if not body:
            raise ValueError("Request body is required.")
        try:
            payload = json.loads(body)
        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON payload.") from exc
        if not isinstance(payload, dict):
            raise ValueError("Request body must be a JSON object.")
        return cls.from_dict(payload)
