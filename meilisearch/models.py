from dataclasses import dataclass
from typing import Any, List, Dict, Optional
from camel_converter.pydantic_base import CamelBase

@dataclass
class MultiDocument:
    results: List[Dict[str, Any]]
    offset: int
    limit: int
    total: int

class Task(CamelBase):
    uid: Optional[str]
    index_uid: str
    task_uid: Optional[str]
    status: str
    type: str
    details: Optional[Dict[str, Any]]
    duration: Optional[str]
    enqueued_at: str
    started_at: Optional[str]
    finished_at: Optional[str]

class PaginatedTasks:
    def __init__(self, resp: Dict[str, Any]) -> None:
        self.results: List[Task] = [Task(**task) for task in resp['results']]
        self.limit: int = resp['limit']
        self.from_: int = resp['from']
        self.next_: int = resp['next']

class IndexStats(CamelBase):
    number_of_documents: int
    is_indexing: bool
    field_distribution: Dict[str, Any]
