from datetime import datetime
from typing import Any

import pydantic
from camel_converter.pydantic_base import CamelBase

from meilisearch._utils import is_pydantic_2, iso_to_date_time


class SearchRule(CamelBase):
    """A dynamic search rule configured on a Meilisearch instance."""

    uid: str
    description: str | None = None
    precedence: int | None = None
    active: bool
    conditions: dict[str, Any]
    actions: list[dict[str, Any]]
    last_updated_at: datetime | None = None

    if is_pydantic_2():

        @pydantic.field_validator("last_updated_at", mode="before")  # type: ignore[attr-defined]
        @classmethod
        def validate_last_updated_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)

    else:  # pragma: no cover

        @pydantic.validator("last_updated_at", pre=True)
        @classmethod
        def validate_last_updated_at(cls, v: str) -> datetime | None:
            return iso_to_date_time(v)


class SearchRulesResults(CamelBase):
    """A paginated list of dynamic search rules."""

    results: list[SearchRule]
    offset: int
    limit: int
    total: int
