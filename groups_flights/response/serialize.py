from datetime import date, datetime
from decimal import Decimal

from groups_flights.utils import CurrencyConvert


def to_json_dict(value):
    if value is None:
        return None
    if isinstance(value, CurrencyConvert):
        return {
            "value": float(value.value),
            "currency": value.currency,
        }
    if isinstance(value, dict):
        return {key: to_json_dict(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_json_dict(item) for item in value]
    if isinstance(value, datetime):
        if value.tzinfo is not None:
            value = value.replace(tzinfo=None)
        return value.isoformat(timespec="seconds")
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return float(value)
    return value
