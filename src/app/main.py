from fastapi import APIRouter, FastAPI

from app.core.core import Core
from app.server.jinja import custom_jinja
from app.server.routers import data_router, misc_router, ui_router
from app.settings import ServerConfig
from mm_base5 import init_server


def start() -> FastAPI:
    core = Core()
    core.startup()
    router = APIRouter()
    # core.dconfig.price
    router.include_router(ui_router.router)
    router.include_router(data_router.router)
    router.include_router(misc_router.router)
    return init_server(core, ServerConfig(), custom_jinja, router)
