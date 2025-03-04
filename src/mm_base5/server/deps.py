from typing import Annotated, cast

from fastapi import Depends, Request

from mm_base5.core.core import BaseCoreAny
from mm_base5.server.jinja import Template


def get_core(request: Request) -> BaseCoreAny:
    return cast(BaseCoreAny, request.app.state.core)


def get_template(request: Request) -> Template:
    return cast(Template, request.app.state.templates)


CoreDep = Annotated[BaseCoreAny, Depends(get_core)]
TemplateDep = Annotated[Template, Depends(get_template)]
