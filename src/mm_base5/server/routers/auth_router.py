from typing import Annotated

from fastapi import APIRouter, Form
from starlette import status
from starlette.responses import HTMLResponse, RedirectResponse

from mm_base5 import RenderDep
from mm_base5.server.auth import ACCESS_TOKEN_NAME
from mm_base5.server.deps import ServerConfigDep

router: APIRouter = APIRouter(prefix="/auth", include_in_schema=False)


@router.get("/login")
def login_page(render: RenderDep) -> HTMLResponse:
    return render.html("login.j2")


@router.post("/login")
def login(token: Annotated[str, Form()], server_config: ServerConfigDep) -> RedirectResponse:
    response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(ACCESS_TOKEN_NAME, value=token, domain=server_config.domain, httponly=True, max_age=60 * 60 * 24 * 30)
    return response


@router.get("/logout")
def logout(server_config: ServerConfigDep) -> RedirectResponse:
    response = RedirectResponse(url="/")
    response.delete_cookie(ACCESS_TOKEN_NAME, domain=server_config.domain)
    return response
