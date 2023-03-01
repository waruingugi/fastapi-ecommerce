import logging
import sys
from functools import lru_cache
from typing import cast, Callable, Dict

from fastapi.routing import APIRoute
from fastapi import Depends, Request, Response


logging.basicConfig(
    level=logging.INFO,
    handlers=[logging.StreamHandler(sys.stdout)],
    format="[%(asctime)s] %(levelname)s - %(message)s"
)

@lru_cache
def instantiate_logger() -> logging.Logger:
    logger_ = logging.getLogger(__name__)

    return logger_


logger = cast(logging.Logger, instantiate_logger())


RESTRICTED_PAYLOAD_URLS = [
    "auth/access-token",
    "auth/login",
]


class LoggingRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            request_log_data = await prepare_request_logging_data(request)


def should_log_payload(request: Request) -> bool:
    """Do not log requests in RESTRICTED_PAYLOAD_URLS"""
    return not (request.url.path in RESTRICTED_PAYLOAD_URLS)


async def prepare_request_logging_data(
    request: Request, read_body: bool = True
) -> dict:
    """Format request to dictionary"""
    payload = None
    if read_body and should_log_payload(request):
        payload = await request.body()

    headers_for_logging = dict(request.headers)
    headers_for_logging.pop("authorization", None)

    request_log_data = dict(
        method=request.method,
        url=str(request.url),
        headers=headers_for_logging,
        payload=payload
    )
    return request_log_data