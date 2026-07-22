from __future__ import annotations

from collections.abc import Iterator
from enum import Enum
from typing import Any

from camel_converter.pydantic_base import CamelBase
from pydantic import ConfigDict, field_validator


class FieldDistribution:
    __dict: dict

    def __init__(self, dist: dict[str, int]) -> None:
        self.__dict = dist
        for key, value in dist.items():
            setattr(self, key, value)

    def __getattr__(self, attr: str) -> int:
        if attr in self.__dict.keys():
            return self.__dict[attr]
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())


class SizeFormat(str, Enum):
    RAW = "raw"
    HUMAN = "human"


class IndexStats(CamelBase):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    number_of_documents: int
    is_indexing: bool
    field_distribution: FieldDistribution
    internal_database_sizes: dict[str, Any] | None = None

    @field_validator("field_distribution", mode="before")
    @classmethod
    def build_field_distribution(cls, v: Any) -> FieldDistribution:
        if not isinstance(v, dict):
            raise TypeError('"field_distribution" in IndexStats must be a dict')

        return FieldDistribution(v)


class Faceting(CamelBase):
    max_values_per_facet: int
    sort_facet_values_by: dict[str, str] | None = None


class Pagination(CamelBase):
    max_total_hits: int


class MinWordSizeForTypos(CamelBase):
    one_typo: int | None = None
    two_typos: int | None = None


class TypoTolerance(CamelBase):
    enabled: bool = True
    disable_on_numbers: bool = False
    disable_on_attributes: list[str] | None = None
    disable_on_words: list[str] | None = None
    min_word_size_for_typos: MinWordSizeForTypos | None = None


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
    attribute_patterns: list[str]
    locales: list[str]
