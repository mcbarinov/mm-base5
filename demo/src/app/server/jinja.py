from markupsafe import Markup
from mm_base5 import CustomJinja

from app.core.core import Core
from app.core.db import DataStatus


def data_status(status: DataStatus) -> Markup:
    color = "black"
    if status == DataStatus.OK:
        color = "green"
    elif status == DataStatus.ERROR:
        color = "red"
    return Markup(f"<span style='color: {color};'>{status.value}</span>")  # nosec: B704


def header_info(_core: Core) -> Markup:
    info = "<span style='color: red'>bbb</span>"
    return Markup(info)  # nosec: B704


def footer_info(_core: Core) -> Markup:
    info = ""
    return Markup(info)  # nosec: B704


custom_jinja = CustomJinja(
    header_info=header_info,
    header_info_new_line=False,
    footer_info=footer_info,
    filters={"data_status": data_status},
)
