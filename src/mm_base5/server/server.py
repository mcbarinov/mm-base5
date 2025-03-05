from fastapi import APIRouter, FastAPI

from mm_base5 import BaseServerConfig
from mm_base5.core.core import BaseCore, DB_co, DCONFIG_co, DVALUE_co
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
    app.include_router(base_router)
    app.include_router(router)
    return app
