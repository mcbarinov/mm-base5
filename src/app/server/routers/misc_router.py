import time

from fastapi import APIRouter
from starlette.responses import PlainTextResponse

from app.server.deps import CoreDep
from mm_base5.core.errors import UserError

router = APIRouter(prefix="/api/misc", tags=["misc"])


@router.get("/user-error")
def user_error() -> str:
    raise UserError("user bla bla bla")


@router.get("/runtime-error")
def runtime_error() -> str:
    raise RuntimeError("runtime bla bla bla")


@router.get("/sleep/{seconds}", response_class=PlainTextResponse)
def sleep_seconds(seconds: int, core: CoreDep) -> str:
    start = time.perf_counter()
    core.logger.debug("sleep_seconds called: %d", seconds)
    time.sleep(seconds)
    counter = core.misc_service.increment_counter()
    core.logger.debug("sleep_seconds finished: %d, perf_couter=%s", seconds, time.perf_counter() - start)
    return f"counter: {counter}"


# @router.get("/result-ok")
# def result_ok() -> Result[str]:
#     return Ok("it works")
#
#
# @router.get("/result-err")
# def result_err() -> Result[str]:
#     return Err("bla bla", data=["ssss", 123])
