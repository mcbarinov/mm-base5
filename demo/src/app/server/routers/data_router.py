import time

from bson import ObjectId
from fastapi import APIRouter
from mm_mongo import MongoDeleteResult, MongoInsertManyResult, MongoInsertOneResult, MongoUpdateResult

from app.core.db import Data
from app.server.deps import CoreDep

router = APIRouter(prefix="/api/data", tags=["data"])


@router.post("/generate-one")
def generate_one(core: CoreDep) -> MongoInsertOneResult[ObjectId]:
    return core.data_service.generate_one()


@router.post("/generate-many")
def generate_many(core: CoreDep) -> MongoInsertManyResult[ObjectId]:
    return core.data_service.generate_many()


@router.get("/{id}")
def get_data(core: CoreDep, id: ObjectId) -> Data:
    return core.db.data.get(id)


@router.post("/{id}/inc")
def inc_data(core: CoreDep, id: ObjectId, value: int | None = None) -> MongoUpdateResult[ObjectId]:
    return core.db.data.update(id, {"$inc": {"value": value or 1}})


@router.delete("/{id}")
def delete_data(core: CoreDep, id: ObjectId) -> MongoDeleteResult:
    return core.db.data.delete(id)


@router.get("/sleep/{seconds}")
def sleep_seconds(seconds: int, core: CoreDep) -> dict[str, object]:
    start = time.perf_counter()
    core.logger.debug("sleep_seconds called: %d", seconds)
    time.sleep(seconds)
    counter = core.misc_service.increment_counter()
    core.logger.debug("sleep_seconds: %d, perf_counter=%s, counter=%s", seconds, time.perf_counter() - start, counter)
    return {"sleep_seconds": seconds, "counter": counter, "perf_counter": time.perf_counter() - start}
