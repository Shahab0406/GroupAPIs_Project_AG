import json
from dataclasses import dataclass


@dataclass
class BookingRequest:
    group_id: int
    adult_seats_requested: int
    child_seats_requested: int

    @classmethod
    def from_dict(cls, data: dict) -> "BookingRequest":
        required_fields = [
            "group_id",
            "adult_seats_requested",
            "child_seats_requested",
        ]
        missing = [field for field in required_fields if field not in data]
        if missing:
            raise ValueError(f"Missing required fields: {', '.join(missing)}")

        try:
            return cls(
                group_id=int(data["group_id"]),
                adult_seats_requested=int(data["adult_seats_requested"]),
                child_seats_requested=int(data["child_seats_requested"]),
            )
        except (TypeError, ValueError) as exc:
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
