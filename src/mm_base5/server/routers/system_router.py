from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from mm_base5.core.system_service import Stats
from mm_base5.server.deps import BaseCoreDep

router: APIRouter = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/stats")
def get_stats(core: BaseCoreDep) -> Stats:
    return core.system_service.get_stats()


@router.get("/logfile", response_class=PlainTextResponse)
def get_logfile(core: BaseCoreDep) -> str:
    return core.system_service.read_logfile()


@router.delete("/logfile")
def clean_logfile(core: BaseCoreDep) -> None:
    core.system_service.clean_logfile()


@router.post("/update-proxies")
def update_proxies(core: BaseCoreDep) -> int | None:
    return core.system_service.update_proxies()
