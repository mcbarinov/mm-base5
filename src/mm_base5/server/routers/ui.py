from fastapi import APIRouter
from starlette.responses import HTMLResponse

from mm_base5.server.deps import CoreDep, TemplateDep

router = APIRouter(prefix="/system", include_in_schema=False)


@router.get("/")
def system_page(templates: TemplateDep, core: CoreDep) -> HTMLResponse:
    stats = core.system_service.get_stats()
    return templates.render("system.j2", stats=stats)
