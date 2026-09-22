from typing import Any


def make_request(
    request_id: int,
    method: str,
    params: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "id": request_id,
        "method": method,
        "params": params or {},
    }


def make_response(
    request_id: int,
    result: Any,
) -> dict[str, Any]:
    return {
        "id": request_id,
        "result": result,
    }