from fastapi import APIRouter

router = APIRouter(prefix="/api/misc", tags=["misc"])


# @router.get("/result-ok")
# def result_ok() -> Result[str]:
#     return Ok("it works")
#
#
# @router.get("/result-err")
# def result_err() -> Result[str]:
#     return Err("bla bla", data=["ssss", 123])
