from app.core.types_ import AppService, AppServiceParams


class MiscService(AppService):
    def __init__(self, base_params: AppServiceParams) -> None:
        super().__init__(base_params)
