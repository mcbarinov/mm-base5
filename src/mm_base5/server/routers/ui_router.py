from typing import Annotated, cast

from fastapi import APIRouter, Form
from starlette.responses import HTMLResponse, RedirectResponse

from mm_base5.server.deps import CoreDep, FormDep, TemplateDep
from mm_base5.server.utils import redirect

router = APIRouter(prefix="/system", include_in_schema=False)

# PAGES


@router.get("/")
def system_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    return tpl.render("system.j2", stats=core.system_service.get_stats())


@router.get("/dconfigs")
def dconfigs_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    return tpl.render("dconfigs.j2", info=core.system_service.get_dconfig_info())


@router.get("/dconfigs/toml")
def dconfigs_toml_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    return tpl.render("dconfigs_toml.j2", toml_str=core.system_service.export_dconfig_as_toml())


@router.get("/dconfigs/multiline/{key:str}")
def dconfigs_multiline_page(tpl: TemplateDep, core: CoreDep, key: str) -> HTMLResponse:
    return tpl.render("dconfigs_multiline.j2", dconfig=core.dconfig, key=key)


@router.get("/dvalues")
def dvalues_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    return tpl.render("dvalues.j2", info=core.system_service.get_dvalue_info())


@router.get("/dvalues/{key:str}")
def update_dvalue_page(tpl: TemplateDep, core: CoreDep, key: str) -> HTMLResponse:
    return tpl.render("dvalues_update.j2", value=core.system_service.export_dvalue_field_as_toml(key), key=key)


@router.get("/dlogs")
def dlogs_page(tpl: TemplateDep, core: CoreDep) -> HTMLResponse:
    return tpl.render("dlogs.j2", dlogs=core.db.dlog.find({}, "-created_at", 100))


# ACTIONS


@router.post("/dconfigs")
def update_dconfig(core: CoreDep, form: FormDep) -> RedirectResponse:
    data = cast(dict[str, str], form)
    core.system_service.update_dconfig(data)
    # flash(request, "dconfigs updated successfully", "success")
    return redirect("/system/dconfigs")


@router.post("/dconfigs/multiline/{key:str}")
def update_dconfig_multiline(core: CoreDep, key: str, value: Annotated[str, Form()]) -> RedirectResponse:
    core.system_service.update_dconfig({key: value})
    # flash(request, "dconfig updated successfully", "success")
    return redirect("/system/dconfigs")


@router.post("/dconfigs/toml")
def update_dconfig_from_toml(core: CoreDep, value: Annotated[str, Form()]) -> RedirectResponse:
    core.system_service.update_dconfig_from_toml(value)
    # flash(request, "dconfigs updated successfully", "success")
    return redirect("/system/dconfigs")


@router.post("/dvalues/{key:str}")
def update_dvalue(core: CoreDep, key: str, value: Annotated[str, Form()]) -> RedirectResponse:
    core.system_service.update_dvalue_field(key, value)
    # flash(request, "dvalue updated successfully", "success")
    return redirect("/system/dvalues")
