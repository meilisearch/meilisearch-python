from __future__ import annotations

from typing import Any, Dict, Union

from camel_converter.pydantic_base import CamelBase


class Task(CamelBase):
    uid: str
    index_uid: Union[str, None]
    status: str
    type: str
    details: Dict[str, Any]
    error: Union[Dict[str, Any], None]
    canceled_by: Union[int, None]
    duration: str
    enqueued_at: str
    started_at: str
    finished_at: str


class TaskInfo(CamelBase):
    task_uid: int
    index_uid: Union[str, None]
    status: str
    type: str
    enqueued_at: str


class TaskResults:
    def __init__(self, resp: Dict[str, Any]) -> None:
        self.results: list[Task] = [Task(**task) for task in resp["results"]]
        self.limit: int = resp["limit"]
        self.from_: int = resp["from"]
        self.next_: int = resp["next"]
