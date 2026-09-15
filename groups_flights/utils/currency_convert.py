from dataclasses import dataclass
from decimal import Decimal


@dataclass
class CurrencyConvert:
    value: Decimal
    currency: str

    @classmethod
    def from_amount(cls, value: Decimal, currency: str) -> "CurrencyConvert":
        return cls(value=value, currency=currency)

    @classmethod
    def from_amount_optional(
        cls,
        value: Decimal | None,
        currency: str,
    ) -> "CurrencyConvert | None":
        if value is None or value == 0:
            return None
        return cls(value=value, currency=currency)

    @classmethod
    def from_dict(cls, data: dict) -> "CurrencyConvert":
        return cls(
            value=Decimal(str(data["value"])),
            currency=data["currency"],
        )
