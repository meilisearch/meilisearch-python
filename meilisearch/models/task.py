from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

import pydantic
from camel_converter.pydantic_base import CamelBase

from meilisearch._utils import is_pydantic_2, iso_to_date_time


class Task(CamelBase):
    uid: int
    index_uid: Union[str, None]
    status: str
    type: str
    details: Union[Dict[str, Any], None]
    error: Union[Dict[str, Any], None]
    canceled_by: Union[int, None]
    duration: Optional[str]
    enqueued_at: datetime
    started_at: Optional[datetime]
    finished_at: Optional[datetime]

    if is_pydantic_2():

        @pydantic.field_validator("enqueued_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:  # pylint: disable=invalid-name
            converted = iso_to_date_time(v)

            if not converted:  # pragma: no cover
                raise ValueError("enqueued_at is required")
            return converted

        @pydantic.field_validator("started_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_started_at(  # pylint: disable=invalid-name
            cls, v: str
        ) -> Union[datetime, None]:
            return iso_to_date_time(v)

        @pydantic.field_validator("finished_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_finished_at(  # pylint: disable=invalid-name
            cls, v: str
        ) -> Union[datetime, None]:
            return iso_to_date_time(v)

    else:  # pragma: no cover

        @pydantic.validator("enqueued_at", pre=True)
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:  # pylint: disable=invalid-name
            converted = iso_to_date_time(v)

            if not converted:
                raise ValueError("enqueued_at is required")

            return converted

        @pydantic.validator("started_at", pre=True)
        @classmethod
        def validate_started_at(  # pylint: disable=invalid-name
            cls, v: str
        ) -> Union[datetime, None]:
            return iso_to_date_time(v)

        @pydantic.validator("finished_at", pre=True)
        @classmethod
        def validate_finished_at(  # pylint: disable=invalid-name
            cls, v: str
        ) -> Union[datetime, None]:
            return iso_to_date_time(v)


class TaskInfo(CamelBase):
    task_uid: int
    index_uid: Union[str, None]
    status: str
    type: str
    enqueued_at: datetime

    if is_pydantic_2():

        @pydantic.field_validator("enqueued_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:  # pylint: disable=invalid-name
            converted = iso_to_date_time(v)

            if not converted:  # pragma: no cover
                raise ValueError("enqueued_at is required")

            return converted

    else:  # pragma: no cover

        @pydantic.validator("enqueued_at", pre=True)
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:  # pylint: disable=invalid-name
            converted = iso_to_date_time(v)

            if not converted:
                raise ValueError("enqueued_at is required")

            return converted


class TaskResults:
    def __init__(self, resp: Dict[str, Any]) -> None:
        self.results: List[Task] = [Task(**task) for task in resp["results"]]
        self.limit: int = resp["limit"]
        self.total: int = resp["total"]
        self.from_: int = resp["from"]
        self.next_: int = resp["next"]
