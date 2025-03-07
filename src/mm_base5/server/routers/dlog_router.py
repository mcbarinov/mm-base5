from bson import ObjectId
from fastapi import APIRouter
from mm_mongo import MongoDeleteResult

from mm_base5.core.db import DLog
from mm_base5.server.deps import CoreDep

router: APIRouter = APIRouter(prefix="/api/system/dlogs", tags=["system"])


@router.get("/{id}")
def get_dlog(core: CoreDep, id: ObjectId) -> DLog:
    return core.db.dlog.get(id)


@router.delete("/{id}")
def delete_dlog(core: CoreDep, id: ObjectId) -> MongoDeleteResult:
    return core.db.dlog.delete(id)


@router.delete("/category/{category}")
def delete_by_category(core: CoreDep, category: str) -> MongoDeleteResult:
    return core.db.dlog.delete_many({"category": category})


@router.delete("")
def delete_all_dlogs(core: CoreDep) -> MongoDeleteResult:
    core.logger.debug("delete_all_dlogs called")
    return core.db.dlog.delete_many({})
