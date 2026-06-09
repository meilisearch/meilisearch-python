from typing import Any, Dict, List, Optional

from camel_converter.pydantic_base import CamelBase
from pydantic import ConfigDict


class DynamicSearchRule(CamelBase):
    """Model for a Meilisearch dynamic search rule."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    uid: str
    description: Optional[str] = None
    priority: Optional[int] = None
    active: Optional[bool] = None
    conditions: Optional[List[Dict[str, Any]]] = None
    actions: Optional[List[Dict[str, Any]]] = None


class DynamicSearchRuleResults(CamelBase):
    """Model for dynamic search rules list results."""

    model_config = ConfigDict(arbitrary_types_allowed=True)
    results: List[DynamicSearchRule]
    offset: int
    limit: int
    total: int
