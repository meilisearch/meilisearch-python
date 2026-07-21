from typing import Any

from camel_converter.pydantic_base import CamelBase


class SearchRule(CamelBase):
    """A dynamic search rule configured on a Meilisearch instance."""

    uid: str
    description: str | None = None
    precedence: int | None = None
    active: bool
    conditions: dict[str, Any]
    actions: list[dict[str, Any]]


class SearchRulesResults(CamelBase):
    """A paginated list of dynamic search rules."""

    results: list[SearchRule]
    offset: int
    limit: int
    total: int
