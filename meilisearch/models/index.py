from __future__ import annotations

from enum import Enum
from typing import Dict, List, Optional, Union

from camel_converter.pydantic_base import CamelBase


class IndexStats(CamelBase):
    number_of_documents: int
    is_indexing: bool
    field_distribution: Dict[str, int]


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
    disable_on_attributes: Optional[List[str]] = None
    disable_on_words: Optional[List[str]] = None
    min_word_size_for_typos: Optional[MinWordSizeForTypos] = None


class ProximityPrecision(str, Enum):
    BY_WORD = "byWord"
    BY_ATTRIBUTE = "byAttribute"


class LocalizedAttributes(CamelBase):
    attribute_patterns: List[str]
    locales: List[str]


class OpenAiEmbedder(CamelBase):
    source: str = "openAi"
    model: Optional[str] = None  # Defaults to text-embedding-3-small
    dimensions: Optional[int] = None  # Uses the model default
    api_key: Optional[str] = None  # Can be provided through a CLI option or environment variable
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None  # Default to 400


class HuggingFaceEmbedder(CamelBase):
    source: str = "huggingFace"
    model: Optional[str] = None  # Defaults to BAAI/bge-base-en-v1.5
    revision: Optional[str] = None
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None  # Default to 400


class UserProvidedEmbedder(CamelBase):
    source: str = "userProvided"
    dimensions: int


class Embedders(CamelBase):
    embedders: Dict[str, Union[OpenAiEmbedder, HuggingFaceEmbedder, UserProvidedEmbedder]]
