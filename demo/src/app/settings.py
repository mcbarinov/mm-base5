from decimal import Decimal

from mm_std import utc_now

from mm_base5 import DC, DV, ServerConfig, DConfigModel, DValueModel


class ServerConfig(ServerConfig):
    tags: list[str] = ["data", "misc"]
    main_menu: dict[str, str] = {"/data": "data", "/misc": "misc"}


class DConfigSettings(DConfigModel):
    telegram_token = DC("", "telegram bot token", hide=True)
    telegram_chat_id = DC(0, "telegram chat id")
    telegram_polling = DC(False)
    telegram_admins = DC("", "admin1,admin2,admin3")
    price = DC(Decimal("1.23"), "long long long long long long long long long long long long long long long long ")
    secret_password = DC("abc", hide=True)
    long_cfg_1 = DC("many lines\n" * 5)


class DValueSettings(DValueModel):
    tmp1 = DV("bla")
    tmp2 = DV("bla")
    processed_block = DV(111, "bla bla about processed_block")
    last_checked_at = DV(utc_now(), "bla bla about last_checked_at", False)
