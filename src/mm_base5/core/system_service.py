from __future__ import annotations

import threading
from datetime import datetime
from logging import Logger

import pydash
from mm_std import Scheduler, toml_dumps, toml_loads
from pydantic import BaseModel

from mm_base5.core.config import CoreConfig
from mm_base5.core.db import BaseDb, DConfigType
from mm_base5.core.dconfig import DConfigStorage
from mm_base5.core.dvalue import DValueStorage
from mm_base5.core.errors import UserError


class Stats(BaseModel):
    class ThreadInfo(BaseModel):
        name: str
        daemon: bool
        func_name: str | None

    class Job(BaseModel):
        func: str
        interval: int
        is_running: bool
        last_at: datetime

        @classmethod
        def from_scheduler_job(cls, job: Scheduler.Job) -> Stats.Job:
            return cls(
                func=job.func.__qualname__,
                interval=job.interval,
                is_running=job.is_running,
                last_at=job.last_at,
            )

    db: dict[str, int]  # collection name -> count
    logfile: int  # size in bytes
    system_log: int  # count
    threads: list[ThreadInfo]
    scheduler_jobs: list[Job]


class DConfigInfo(BaseModel):
    dconfig: dict[str, object]
    descriptions: dict[str, str]
    types: dict[str, DConfigType]
    hidden: set[str]


class DValueInfo(BaseModel):
    dvalue: dict[str, object]
    persistent: dict[str, bool]
    descriptions: dict[str, str]


# noinspection PyMethodMayBeStatic
class SystemService:
    def __init__(self, core_config: CoreConfig, logger: Logger, db: BaseDb, scheduler: Scheduler) -> None:
        self.logger = logger
        self.db = db
        self.logfile = core_config.data_dir / "app.log"
        self.scheduler = scheduler

    # dconfig

    def get_dconfig_info(self) -> DConfigInfo:
        return DConfigInfo(
            dconfig=DConfigStorage.storage,
            descriptions=DConfigStorage.descriptions,
            types=DConfigStorage.types,
            hidden=DConfigStorage.hidden,
        )

    def export_dconfig_as_toml(self) -> str:
        result = pydash.omit(DConfigStorage.storage, *DConfigStorage.hidden)
        return toml_dumps(result)

    def update_dconfig_from_toml(self, toml_value: str) -> bool | None:
        data = toml_loads(toml_value)
        if isinstance(data, dict):
            return DConfigStorage.update({key: str(value) for key, value in data.items()})

    def update_dconfig(self, data: dict[str, str]) -> bool:
        return DConfigStorage.update(data)

    # dvalue
    def get_dvalue_info(self) -> DValueInfo:
        return DValueInfo(
            dvalue=DValueStorage.storage,
            persistent=DValueStorage.persistent,
            descriptions=DValueStorage.descriptions,
        )

    def export_dvalue_as_toml(self) -> str:
        return toml_dumps(DValueStorage.storage)

    def export_dvalue_field_as_toml(self, key: str) -> str:
        return toml_dumps({key: DValueStorage.storage[key]})

    def get_dvalue_value(self, key: str) -> object:
        return DValueStorage.storage[key]

    def update_dvalue_field(self, key: str, toml_str: str) -> None:
        data = toml_loads(toml_str)
        if key not in data:
            raise UserError(f"Key '{key}' not found in toml data")
        DValueStorage.update_value(key, data[key])

    # slogs
    def get_dlog_category_stats(self) -> dict[str, int]:
        result = {}
        for category in self.db.dlog.collection.distinct("category"):
            result[category] = self.db.dlog.count({"category": category})
        return result

    # system

    def get_stats(self) -> Stats:
        # threads
        threads = []
        for t in threading.enumerate():
            target = t.__dict__.get("_target")
            func_name = None
            if target:
                func_name = target.__qualname__
            threads.append(Stats.ThreadInfo(name=t.name, daemon=t.daemon, func_name=func_name))
        threads = pydash.sort(threads, key=lambda x: x.name)

        # db
        db_stats = {}
        for col in self.db.database.list_collection_names():
            db_stats[col] = self.db.database[col].estimated_document_count()

        return Stats(
            db=db_stats,
            logfile=self.logfile.stat().st_size,
            system_log=self.db.dlog.count({}),
            threads=threads,
            scheduler_jobs=[Stats.Job.from_scheduler_job(j) for j in self.scheduler.jobs],
        )

    def read_logfile(self) -> str:
        return self.logfile.read_text(encoding="utf-8")

    def clean_logfile(self) -> None:
        self.logfile.write_text("")
