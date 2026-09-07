from dataclasses import dataclass
from enum import Enum
from http import HTTPStatus
from typing import Any, Dict, Optional

from dataclasses_json import dataclass_json
from django.http import HttpResponse



class CoreStatus(Enum):
    Success = 1
    Error = 101


@dataclass_json
@dataclass
class CoreResponseData:
    equivalent_currency: str = None


@dataclass_json
@dataclass
class CoreResponse:
    success: bool
    message: str
    status: int
    data: object
    error: object
    errors: Optional[Dict[str, Any]] = None

    @staticmethod
    def get_response(
        success: bool = False,
        message: str = "",
        status: int = 101,
        error_code: int = None,
        response: dict = {},
        error: dict = {},
        errors: dict = {},
    ) -> TypedResponse:
        return {
            "success": success,
            "status": status,
            "message": message,
            "error_code": error_code,
            "response": response,
            "error": error,
            "errors": errors,
        }

    @staticmethod
    def generate_response(
        success: bool = False,
        message: str = "",
        status: int = 200,
        data: Any = None,
        error: Any = None,
        errors: Dict[str, Any] = None,
    ):
        return CoreResponse(
            success=success,
            message=message,
            status=status,
            data=data,
            error=error,
            errors=errors,
        )

    @staticmethod
    def send_response_params(
        success: bool = False,
        message: str = "",
        status: int = 200,
        data: Any = None,
        error: Any = None,
    ):
        response = CoreResponse(
            success=success,
            message=message,
            status=status,
            data=data,
            error=error,
        )
        return CoreResponse.send_response(response)

    @staticmethod
    def success_response(message: str = "", data: Any = None):
        response = CoreResponse(
            success=True,
            message=message,
            status=CoreStatus.Success.value,
            data=data,
            error={},
        )
        return CoreResponse.send_response(response)

    @staticmethod
    def send_response(response: "CoreResponse", http_status=HTTPStatus.OK):
        return HttpResponse(
            response.to_json(),
            content_type="application/json",
            status=http_status,
        )

    @staticmethod
    def send_success_response(response: "CoreResponse", status=HTTPStatus.OK):
        return CoreResponse.send_response(response, http_status=status)

    @staticmethod
    def send_error_response(response: "CoreResponse", status=HTTPStatus.BAD_REQUEST):
        return CoreResponse.send_response(response, http_status=status)

    @staticmethod
    def unauthorized_response(
        success: bool = False,
        message: str = "User does not have permission to perform this operation",
        status: int = 101,
        error_code: int = None,
        response: dict = {},
        error: dict = {},
    ) -> TypedResponse:
        return {
            "success": success,
            "status": status,
            "message": message,
            "error_code": error_code,
            "response": response,
            "error": error,
        }

    @classmethod
    def send_search_response(
        cls,
        success: bool = False,
        message: str = "",
        status: int = 200,
        data: Any = None,
        error: Any = None,
    ):
        response = cls(
            success=success,
            message=message,
            status=status,
            data=data,
            error=error,
        )
        return cls.send_response(response)
