from datetime import date, datetime
from decimal import Decimal


def to_json_dict(value):
    if isinstance(value, dict):
        return {key: to_json_dict(item) for key, item in value.items()}
    if isinstance(value, list):
        return [to_json_dict(item) for item in value]
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, Decimal):
        return str(value)
    return value
