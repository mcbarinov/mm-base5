from collections.abc import Callable
from dataclasses import dataclass
from functools import partial
from typing import Any

import mm_jinja
from jinja2 import ChoiceLoader, Environment, PackageLoader
from markupsafe import Markup
from mm_mongo import json_dumps
from starlette.requests import Request
from starlette.responses import HTMLResponse

from mm_base5.core.core import BaseCoreAny
from mm_base5.server import utils
from mm_base5.server.config import ServerConfig


def system_log_data_truncate(data: object) -> str:
    if not data:
        return ""
    res = json_dumps(data)
    if len(res) > 100:
        return res[:100] + "..."
    return res


@dataclass
class CustomJinja:
    header_info: Callable[..., Markup] | None = None
    header_info_new_line: bool = False
    footer_info: Callable[..., Markup] | None = None
    filters: dict[str, Callable[..., Any]] | None = None
    globals: dict[str, Any] | None = None


def init_env(core: BaseCoreAny, server_config: ServerConfig, custom_jinja: CustomJinja) -> Environment:
    loader = ChoiceLoader([PackageLoader("mm_base5.server"), PackageLoader("app.server")])

    header_info = custom_jinja.header_info if custom_jinja.header_info else lambda _: Markup("")
    footer_info = custom_jinja.footer_info if custom_jinja.footer_info else lambda _: Markup("")
    custom_filters: dict[str, Callable[..., Any]] = {
        "system_log_data_truncate": system_log_data_truncate,
    }
    custom_globals: dict[str, Any] = {
        "core_config": core.core_config,
        "server_config": server_config,
        "dconfig": core.dconfig,
        "dvalue": core.dvalue,
        "confirm": Markup(""" onclick="return confirm('sure?')" """),
        "header_info": partial(header_info, core),
        "footer_info": partial(footer_info, core),
        "header_info_new_line": custom_jinja.header_info_new_line,
        "app_version": utils.get_package_version("app"),
        "mm_base5_version": utils.get_package_version("mm_base5"),
    }

    if custom_jinja.globals:
        custom_globals |= custom_jinja.globals
    if custom_jinja.filters:
        custom_filters |= custom_jinja.filters

    return mm_jinja.init_jinja(loader, custom_globals=custom_globals, custom_filters=custom_filters)


class Render:
    def __init__(self, env: Environment, request: Request) -> None:
        self.env = env
        self.request = request

    def html(self, template_name: str, **kwargs: object) -> HTMLResponse:
        flash_messages = self.request.session.pop("flash_messages") if "flash_messages" in self.request.session else []
        html_content = self.env.get_template(template_name).render(kwargs | {"flash_messages": flash_messages})
        return HTMLResponse(content=html_content, status_code=200)

    def flash(self, message: str, is_error: bool = False) -> None:
        if "flash_messages" not in self.request.session:
            self.request.session["flash_messages"] = []
        self.request.session["flash_messages"].append({"message": message, "error": is_error})
