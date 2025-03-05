from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Form
from starlette.responses import HTMLResponse, RedirectResponse

from app.server.deps import CoreDep
from mm_base5 import TemplateDep, redirect

router = APIRouter(include_in_schema=False)


@router.get("/")
def index_page(tpl: TemplateDep) -> HTMLResponse:
    return tpl.render("index.j2")


@router.get("/data")
def data_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    data = core.db.data.find({}, "-created_at", 100)
    return tpl.render("data.j2", data_list=data)


@router.get("/misc")
def misc_page(tpl: TemplateDep) -> HTMLResponse:
    return tpl.render("misc.j2", zero=0)


# ACTIONS
@router.post("/data/{id}/inc")
def inc_data(core: CoreDep, id: ObjectId, value: Annotated[int, Form()]) -> RedirectResponse:
    core.db.data.update_one({"_id": id}, {"$inc": {"value": value}})
    # flash(request, f"Data {id} incremented by {value}", "success")
    return redirect("/data")
