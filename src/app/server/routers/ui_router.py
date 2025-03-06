from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Form
from starlette.responses import HTMLResponse, RedirectResponse

from app.server.deps import CoreDep
from mm_base5 import RenderDep, redirect

router = APIRouter(include_in_schema=False)


@router.get("/")
def index_page(render: RenderDep) -> HTMLResponse:
    return render.html("index.j2")


@router.get("/data")
def data_page(render: RenderDep, core: CoreDep) -> HTMLResponse:
    data = core.db.data.find({}, "-created_at", 100)
    return render.html("data.j2", data_list=data)


@router.get("/misc")
def misc_page(render: RenderDep) -> HTMLResponse:
    return render.html("misc.j2", zero=0)


# ACTIONS
@router.post("/data/{id}/inc")
def inc_data(render: RenderDep, core: CoreDep, id: ObjectId, value: Annotated[int, Form()]) -> RedirectResponse:
    core.db.data.update_one({"_id": id}, {"$inc": {"value": value}})
    render.flash(f"Data {id} incremented by {value}")
    return redirect("/data")
