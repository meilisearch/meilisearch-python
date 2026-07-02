from __future__ import annotations

from datetime import datetime
from typing import Any

import pydantic
from camel_converter.pydantic_base import CamelBase

from meilisearch._utils import is_pydantic_2, iso_to_date_time


class Task(CamelBase):
    uid: int
    index_uid: str | None = None
    status: str
    type: str
    details: dict[str, Any] | None = None
    error: dict[str, Any] | None = None
    canceled_by: int | None = None
    duration: str | None = None
    enqueued_at: datetime
    started_at: datetime | None = None
    finished_at: datetime | None = None
    network: dict[str, Any] | None = None
    custom_metadata: str | None = None

    if is_pydantic_2():

        @pydantic.field_validator("enqueued_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:
            converted = iso_to_date_time(v)

            if not converted:  # pragma: no cover
                raise ValueError("enqueued_at is required")
            return converted

        @pydantic.field_validator("started_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_started_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

        @pydantic.field_validator("finished_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_finished_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

    else:  # pragma: no cover

        @pydantic.validator("enqueued_at", pre=True)
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:
            converted = iso_to_date_time(v)

            if not converted:
                raise ValueError("enqueued_at is required")

            return converted

        @pydantic.validator("started_at", pre=True)
        @classmethod
        def validate_started_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

        @pydantic.validator("finished_at", pre=True)
        @classmethod
        def validate_finished_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)


class TaskInfo(CamelBase):
    task_uid: int
    index_uid: str | None
    status: str
    type: str
    enqueued_at: datetime

    if is_pydantic_2():

        @pydantic.field_validator("enqueued_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:
            converted = iso_to_date_time(v)

            if not converted:  # pragma: no cover
                raise ValueError("enqueued_at is required")

            return converted

    else:  # pragma: no cover

        @pydantic.validator("enqueued_at", pre=True)
        @classmethod
        def validate_enqueued_at(cls, v: str) -> datetime:
            converted = iso_to_date_time(v)

            if not converted:
                raise ValueError("enqueued_at is required")

            return converted


class TaskResults(CamelBase):
    results: list[Task]
    limit: int
    total: int
    from_: int | None
    next_: int | None


class Batch(CamelBase):
    uid: int
    details: dict[str, Any] | None = None
    stats: dict[str, int | dict[str, Any]] | None = None
    duration: str | None = None
    started_at: datetime | None = None
    finished_at: datetime | None = None
    progress: dict[str, float | list[dict[str, Any]]] | None = None

    if is_pydantic_2():

        @pydantic.field_validator("started_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_started_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

        @pydantic.field_validator("finished_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_finished_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

    else:  # pragma: no cover

        @pydantic.validator("started_at", pre=True)
        @classmethod
        def validate_started_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

        @pydantic.validator("finished_at", pre=True)
        @classmethod
        def validate_finished_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)


class BatchResults(CamelBase):
    results: list[Batch]
    total: int
    limit: int
    from_: int
    # None means last page
    next_: int | None
