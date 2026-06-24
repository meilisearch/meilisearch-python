from typing import Any, Dict, List, Optional

from camel_converter.pydantic_base import CamelBase


class DynamicSearchRule(CamelBase):
    uid: str
    description: Optional[str] = None
    priority: Optional[int] = None
    active: bool
    conditions: List[Dict[str, Any]]
    actions: List[Dict[str, Any]]


class DynamicSearchRuleResults(CamelBase):
    results: List[DynamicSearchRule]
    offset: int
    limit: int
    total: int
