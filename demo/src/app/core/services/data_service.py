import random

from bson import ObjectId
from mm_mongo import MongoInsertManyResult, MongoInsertOneResult
from mm_std import hr

from app.core.db import Data, DataStatus
from app.core.types_ import AppService, AppServiceParams


class DataService(AppService):
    def __init__(self, base_params: AppServiceParams) -> None:
        super().__init__(base_params)

    def generate_one(self) -> MongoInsertOneResult[ObjectId]:
        status = random.choice(list(DataStatus))
        value = random.randint(0, 1_000_000)

        return self.db.data.insert_one(Data(id=ObjectId(), status=status, value=value))

    def generate_many(self) -> MongoInsertManyResult[ObjectId]:
        res = hr("https://httpbin.org/get")
        self.dlog("generate_many", {"res": res.json, "large-data": "abc" * 100})
        self.dlog("ddd", self.dconfig.telegram_token)
        new_data_list = [
            Data(id=ObjectId(), status=random.choice(list(DataStatus)), value=random.randint(0, 1_000_000)) for _ in range(10)
        ]
        return self.db.data.insert_many(new_data_list)
