from typing import Any

from camel_converter.pydantic_base import CamelBase


class DynamicSearchRule(CamelBase):
    uid: str
    description: str | None = None
    priority: int | None = None
    active: bool
    conditions: list[dict[str, Any]]
    actions: list[dict[str, Any]]


class DynamicSearchRuleResults(CamelBase):
    results: list[DynamicSearchRule]
    offset: int
    limit: int
    total: int
