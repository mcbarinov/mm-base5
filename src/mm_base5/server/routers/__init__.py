from fastapi import APIRouter

from mm_base5.server.routers import dconfig_router, dvalue_router, ui_router

base_router = APIRouter()
base_router.include_router(ui_router.router)
base_router.include_router(dconfig_router.router)
base_router.include_router(dvalue_router.router)
