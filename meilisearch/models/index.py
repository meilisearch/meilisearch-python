from __future__ import annotations

from typing import Any, Dict, Iterator, List, Optional

from camel_converter import to_snake
from camel_converter.pydantic_base import CamelBase


class IndexStats:
    __dict: Dict

    def __init__(self, doc: Dict[str, Any]) -> None:
        self.__dict = doc
        for key, val in doc.items():
            key = to_snake(key)
            if isinstance(val, dict):
                setattr(self, key, IndexStats(val))
            else:
                setattr(self, key, val)

    def __getattr__(self, attr: str) -> Any:
        if attr in self.__dict.keys():
            return attr
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())  # type: ignore


class Faceting(CamelBase):
    max_values_per_facet: int


class Pagination(CamelBase):
    max_total_hits: int


class MinWordSizeForTypos(CamelBase):
    one_typo: Optional[int] = None
    two_typos: Optional[int] = None


class TypoTolerance(CamelBase):
    enabled: bool = True
    disable_on_attributes: Optional[List[str]] = None
    disable_on_words: Optional[List[str]] = None
    min_word_size_for_typos: Optional[MinWordSizeForTypos] = None
