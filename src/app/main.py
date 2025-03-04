from fastapi import APIRouter, FastAPI

from app.core.core import Core
from app.server.jinja import custom_jinja
from app.server.routers import api, ui
from app.settings import ServerConfig
from mm_base5 import init_server


def start() -> FastAPI:
    core = Core()
    core.startup()
    router = APIRouter()
    # core.dconfig.price
    router.include_router(ui.router, include_in_schema=False)
    router.include_router(api.router, prefix="/api", tags=["api"])
    return init_server(core, ServerConfig(), custom_jinja, router)
