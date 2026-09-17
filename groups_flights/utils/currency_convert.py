from dataclasses import dataclass, field
from decimal import Decimal

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class CurrencyConvert:
    value: Decimal = field(
        metadata=config(
            encoder=lambda value: float(value),
            decoder=lambda value: Decimal(str(value)),
        ),
    )
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
