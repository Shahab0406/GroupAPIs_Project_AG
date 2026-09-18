from .booking import GroupBookingDetailResponse
from .core_response import CoreResponse, CoreResponseData, CoreStatus
from .flight import FlightResponse
from .group import GroupResponse
from .invoice import GroupFlightsInvoiceResponse, GroupInvoiceDetailResponse
from .segment import SegmentResponse

__all__ = [
    "CoreResponse",
    "CoreResponseData",
    "CoreStatus",
    "FlightResponse",
    "GroupBookingDetailResponse",
    "GroupFlightsInvoiceResponse",
    "GroupInvoiceDetailResponse",
    "GroupResponse",
    "SegmentResponse",
]
