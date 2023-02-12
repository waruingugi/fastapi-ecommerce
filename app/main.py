from fastapi import FastAPI
from app.core.config import get_app_settings

from app.users import api as user_api
from app.auth import api as auth_api
from app.business_partner import api as business_partner_api
from typing import Any


def get_application() -> FastAPI:
    settings = get_app_settings()
    application: Any = FastAPI(
        title=settings.PROJECT_NAME,
        description="""
            Learning FastAPI by building an industry grade application.
        """,
        version=settings.API_VERSION
    )

    application.include_router(user_api.router, prefix=settings.API_V1_STR)
    application.include_router(auth_api.router, prefix=settings.API_V1_STR)
    application.include_router(business_partner_api.router, prefix=settings.API_V1_STR)


    return application


app = get_application()
