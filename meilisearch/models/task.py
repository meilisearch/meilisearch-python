from __future__ import annotations

from typing import Any, Dict, Optional

from camel_converter.pydantic_base import CamelBase


class Task(CamelBase):
    uid: str
    index_uid: str
    status: str
    type: str
    details: Optional[Dict[str, Any]]
    duration: str
    enqueued_at: str
    started_at: str
    finished_at: str

class TaskInfo(CamelBase):
    task_uid: str | None
    index_uid: str
    status: str
    type: str
    details: Optional[Dict[str, Any]]
    duration: str | None
    enqueued_at: str
    started_at: str | None
    finished_at: str | None

class TaskResults:
    def __init__(self, resp: dict[str, Any]) -> None:
        self.results: list[Task] = [Task(**task) for task in resp['results']]
        self.limit: int = resp['limit']
        self.from_: int = resp['from']
        self.next_: int = resp['next']
