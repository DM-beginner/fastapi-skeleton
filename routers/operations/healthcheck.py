from typing import Any
from healthcheck import HealthCheck
from fastapi import APIRouter, Response

router = APIRouter(tags=['HealthCheck'])


@router.get("/healthcheck")
def health_check(response: Response) -> Any:
    message, status_code, headers = HealthCheck().run()
    response.status_code = status_code
    return message