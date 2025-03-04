from fastapi import APIRouter

from mm_base5.server.routers import dconfigs, ui

base_router = APIRouter()
base_router.include_router(ui.router)
base_router.include_router(dconfigs.router)
