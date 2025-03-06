from pathlib import Path

from fastapi import APIRouter, FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles

from mm_base5 import BaseServerConfig, CoreConfig
from mm_base5.core.core import BaseCore, DB_co, DCONFIG_co, DVALUE_co
from mm_base5.server import utils
from mm_base5.server.auth import AccessTokenMiddleware
from mm_base5.server.jinja import CustomJinja, Template
from mm_base5.server.routers import base_router


# noinspection PyUnresolvedReferences
def init_server(
    core: BaseCore[DCONFIG_co, DVALUE_co, DB_co],
    server_config: BaseServerConfig,
    custom_jinja: CustomJinja,
    router: APIRouter,
) -> FastAPI:
    app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)
    app.state.core = core
    app.state.templates = Template(core, server_config, custom_jinja)
    app.state.server_config = server_config
    app.include_router(base_router)
    app.include_router(router)
    app.mount("/assets", StaticFiles(directory=Path(__file__).parent.absolute() / "assets"), name="assets")
    app.add_middleware(AccessTokenMiddleware, access_token=server_config.access_token)
    configure_openapi(app, core.core_config, server_config)
    return app


def configure_openapi(app: FastAPI, core_config: CoreConfig, server_config: BaseServerConfig) -> None:
    @app.get("/system/openapi.json", include_in_schema=False)
    async def get_open_api_endpoint() -> JSONResponse:
        openapi = get_openapi(
            title=core_config.app_name,
            version=utils.get_package_version("app"),
            routes=app.routes,
            tags=server_config.tags_metadata,
        )
        return JSONResponse(openapi)

    @app.get("/system/openapi", include_in_schema=False)
    async def get_documentation() -> HTMLResponse:
        return get_swagger_ui_html(openapi_url="/system/openapi.json", title=core_config.app_name)
