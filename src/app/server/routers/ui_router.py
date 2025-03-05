from fastapi import APIRouter
from starlette.responses import HTMLResponse

from app.server.deps import CoreDep
from mm_base5 import TemplateDep

router = APIRouter(include_in_schema=False)


@router.get("/")
def index_page(tpl: TemplateDep) -> HTMLResponse:
    return tpl.render("index.j2")


@router.get("/data")
def data_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    data = core.db.data.find({}, "-created_at", 100)
    return tpl.render("data.j2", data_list=data)
