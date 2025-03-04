from fastapi import APIRouter

router = APIRouter(include_in_schema=False)


@router.get("/")
def index_page() -> str:
    return "Hello World!"
