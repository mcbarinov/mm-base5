import time
from typing import Annotated

from fastapi import APIRouter, File, UploadFile
from mm_std import Err, Ok, Result

from app.server.deps import CoreDep
from mm_base5 import UserError

router = APIRouter(prefix="/api/misc", tags=["misc"])


@router.get("/user-error")
def user_error() -> str:
    raise UserError("user bla bla bla")


@router.get("/runtime-error")
def runtime_error() -> str:
    raise RuntimeError("runtime bla bla bla")


@router.get("/sleep/{seconds}")
def sleep_seconds(seconds: int, core: CoreDep) -> dict[str, object]:
    start = time.perf_counter()
    core.logger.debug("sleep_seconds called: %d", seconds)
    time.sleep(seconds)
    counter = core.misc_service.increment_counter()
    core.logger.debug("sleep_seconds: %d, perf_counter=%s, counter=%s", seconds, time.perf_counter() - start, counter)
    return {"sleep_seconds": seconds, "counter": counter, "perf_counter": time.perf_counter() - start}


@router.get("/result-ok")
def result_ok() -> Result[str]:
    return Ok("it works")


@router.get("/result-err")
def result_err() -> Result[str]:
    return Err("bla bla", data=["ssss", 123])


@router.post("/async-upload")
async def async_upload(file: Annotated[UploadFile, File()]) -> dict[str, str]:
    content = await file.read()
    text_content = content.decode("utf-8")
    return {"text_content": text_content}


@router.post("/sync-upload")
def sync_upload(file: Annotated[UploadFile, File()]) -> dict[str, str]:
    content = file.file.read()
    text_content = content.decode("utf-8")
    return {"text_content": text_content}
