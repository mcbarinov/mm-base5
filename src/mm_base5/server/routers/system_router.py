from fastapi import APIRouter
from rich import inspect
from starlette.responses import PlainTextResponse

from mm_base5.server.deps import CoreDep

router = APIRouter(prefix="/api/system", tags=["system"])


@router.get("/stats")
def get_stats(core: CoreDep) -> dict[str, object]:
    res = core.system_service.get_stats().model_dump()
    inspect(res)
    return res


@router.get("/logfile", response_class=PlainTextResponse)
def get_logfile(core: CoreDep) -> str:
    core.logger.info("ddd")
    return core.system_service.read_logfile()


@router.delete("/logfile")
def clean_logfile(core: CoreDep) -> None:
    core.system_service.clean_logfile()
