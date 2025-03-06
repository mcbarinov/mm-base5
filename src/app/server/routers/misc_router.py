from fastapi import APIRouter

from mm_base5.core.errors import UserError

router = APIRouter(prefix="/api/misc", tags=["misc"])


@router.get("/user-error")
def user_error() -> str:
    raise UserError("user bla bla bla")


@router.get("/runtime-error")
def runtime_error() -> str:
    raise RuntimeError("runtime bla bla bla")


# @router.get("/result-ok")
# def result_ok() -> Result[str]:
#     return Ok("it works")
#
#
# @router.get("/result-err")
# def result_err() -> Result[str]:
#     return Err("bla bla", data=["ssss", 123])
