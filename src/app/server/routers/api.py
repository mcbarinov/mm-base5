from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["api"])


@router.get("/hello")
def hello() -> str:
    return "Hello World!"
