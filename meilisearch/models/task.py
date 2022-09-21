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
    task_uid: Optional[str]
    index_uid: str
    status: str
    type: str
    details: Optional[Dict[str, Any]]
    duration: Optional[str]
    enqueued_at: str
    started_at: Optional[str]
    finished_at: Optional[str]

class TaskResults:
    def __init__(self, resp: Dict[str, Any]) -> None:
        self.results: list[Task] = [Task(**task) for task in resp['results']]
        self.limit: int = resp['limit']
        self.from_: int = resp['from']
        self.next_: int = resp['next']
