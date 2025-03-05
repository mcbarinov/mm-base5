from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from mm_base5.core.db import DValue
from mm_base5.server.deps import CoreDep

router: APIRouter = APIRouter(prefix="/api/system/dvalues", tags=["system"])


@router.get("/toml", response_class=PlainTextResponse)
def get_dvalues_as_toml(core: CoreDep) -> str:
    return core.system_service.export_dvalue_as_toml()


@router.get("/{key}/toml", response_class=PlainTextResponse)
def get_dvalue_field_as_toml(core: CoreDep, key: str) -> str:
    return core.system_service.export_dvalue_field_as_toml(key)


@router.get("/{key}/value")
def get_dvalue_value(core: CoreDep, key: str) -> object:
    return core.system_service.get_dvalue_value(key)


@router.get("/{key}")
def get_dvalue_key(core: CoreDep, key: str) -> DValue:
    return core.db.dvalue.get(key)
