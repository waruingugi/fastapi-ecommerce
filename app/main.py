from fastapi import FastAPI
from app.core.config import settings

from app.users import api as user_api
from app.auth import api as auth_api
from app.business_partner import api as business_partner_api
from app.roles import api as roles_api
from app.common import api as common_api
from typing import Any
from asgi_correlation_id import CorrelationIdMiddleware


def get_application() -> FastAPI:
    application: Any = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
            Learning FastAPI by building an industry grade application.
        """,
        version=settings.API_VERSION,
        swagger_ui_parameters={"persistAuthorization": True},
    )

    application.include_router(auth_api.router, prefix=settings.API_V1_STR)
    application.include_router(roles_api.router, prefix=settings.API_V1_STR)
    application.include_router(user_api.router, prefix=settings.API_V1_STR)
    application.include_router(business_partner_api.router, prefix=settings.API_V1_STR)
    application.include_router(common_api.router, prefix=settings.API_V1_STR)
    application.add_middleware(CorrelationIdMiddleware)

    return application


app = get_application()
