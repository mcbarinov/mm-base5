from pathlib import Path

from fastapi import APIRouter, FastAPI
from starlette.staticfiles import StaticFiles

from mm_base5 import BaseServerConfig
from mm_base5.core.core import BaseCore, DB_co, DCONFIG_co, DVALUE_co
from mm_base5.server.auth import AccessTokenMiddleware
from mm_base5.server.jinja import CustomJinja, Template

from .routers import base_router


# noinspection PyUnresolvedReferences
def init_server(
    core: BaseCore[DCONFIG_co, DVALUE_co, DB_co],
    server_config: BaseServerConfig,
    custom_jinja: CustomJinja,
    router: APIRouter,
) -> FastAPI:
    app = FastAPI()
    app.state.core = core
    app.state.templates = Template(core, server_config, custom_jinja)
    app.state.server_config = server_config
    app.include_router(base_router)
    app.include_router(router)
    app.mount("/assets", StaticFiles(directory=Path(__file__).parent.absolute() / "assets"), name="assets")
    app.add_middleware(AccessTokenMiddleware, access_token=server_config.access_token)
    return app
