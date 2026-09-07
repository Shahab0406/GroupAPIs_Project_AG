from typing import Any, Dict, Optional, TypedDict


class TypedResponse(TypedDict, total=False):
    success: bool
    status: int
    message: str
    error_code: Optional[int]
    response: dict
    error: dict
    errors: Dict[str, Any]
