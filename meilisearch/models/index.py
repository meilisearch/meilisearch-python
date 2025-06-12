from __future__ import annotations

from enum import Enum
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
        return iter(self.__dict__.items())


class Faceting(CamelBase):
    max_values_per_facet: int
    sort_facet_values_by: Optional[Dict[str, str]] = None


class Pagination(CamelBase):
    max_total_hits: int


class MinWordSizeForTypos(CamelBase):
    one_typo: Optional[int] = None
    two_typos: Optional[int] = None


class TypoTolerance(CamelBase):
    enabled: bool = True
    disable_on_numbers: bool = False
    disable_on_attributes: Optional[List[str]] = None
    disable_on_words: Optional[List[str]] = None
    min_word_size_for_typos: Optional[MinWordSizeForTypos] = None


class PrefixSearch(str, Enum):
    INDEXING_TIME = "indexingTime"
    """
    Calculate prefix search during indexing. This is the default behavior.
    """

    DISABLED = "disabled"
    """
    Do not calculate prefix search. May speed up indexing, but will severely impact search result relevancy.
    """


class ProximityPrecision(str, Enum):
    BY_WORD = "byWord"
    BY_ATTRIBUTE = "byAttribute"


class EmbedderDistribution(CamelBase):
    mean: float
    sigma: float


class LocalizedAttributes(CamelBase):
    attribute_patterns: List[str]
    locales: List[str]
