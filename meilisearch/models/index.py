from typing import Any, Dict
from camel_converter.pydantic_base import CamelBase

class IndexStats(CamelBase):
    number_of_documents: int
    is_indexing: bool
    field_distribution: Dict[str, Any]
