from __future__ import annotations

from enum import Enum
from typing import Any, Dict, Optional, Union

from camel_converter.pydantic_base import CamelBase


class Distribution(CamelBase):
    """Distribution settings for embedders.

    Parameters
    ----------
    mean: float
        Mean value between 0 and 1
    sigma: float
        Sigma value between 0 and 1
    """

    mean: float
    sigma: float


class PoolingType(str, Enum):
    """Pooling strategies for HuggingFaceEmbedder.

    Attributes
    ----------
    USE_MODEL : str
        Use the model's default pooling strategy.
    FORCE_MEAN : str
        Force mean pooling over the token embeddings.
    FORCE_CLS : str
        Use the [CLS] token embedding as the sentence representation.
    """

    USE_MODEL = "useModel"
    FORCE_MEAN = "forceMean"
    FORCE_CLS = "forceCls"


class OpenAiEmbedder(CamelBase):
    """OpenAI embedder configuration.

    Parameters
    ----------
    source: str
        The embedder source, must be "openAi"
    url: Optional[str]
        The URL Meilisearch contacts when querying the embedder
    api_key: Optional[str]
        Authentication token Meilisearch should send with each request to the embedder
    model: Optional[str]
        The model your embedder uses when generating vectors (defaults to text-embedding-3-small)
    dimensions: Optional[int]
        Number of dimensions in the chosen model
    document_template: Optional[str]
        Template defining the data Meilisearch sends to the embedder
    document_template_max_bytes: Optional[int]
        Maximum allowed size of rendered document template (defaults to 400)
    distribution: Optional[Distribution]
        Describes the natural distribution of search results
    binary_quantized: Optional[bool]
        Once set to true, irreversibly converts all vector dimensions to 1-bit values
    """

    source: str = "openAi"
    url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None  # Defaults to text-embedding-3-small
    dimensions: Optional[int] = None  # Uses the model default
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None  # Default to 400
    distribution: Optional[Distribution] = None
    binary_quantized: Optional[bool] = None


class HuggingFaceEmbedder(CamelBase):
    """HuggingFace embedder configuration.

    Parameters
    ----------
    source: str
        The embedder source, must be "huggingFace"
    url: Optional[str]
        The URL Meilisearch contacts when querying the embedder
    model: Optional[str]
        The model your embedder uses when generating vectors (defaults to BAAI/bge-base-en-v1.5)
    dimensions: Optional[int]
        Number of dimensions in the chosen model
    revision: Optional[str]
        Model revision hash
    document_template: Optional[str]
        Template defining the data Meilisearch sends to the embedder
    document_template_max_bytes: Optional[int]
        Maximum allowed size of rendered document template (defaults to 400)
    distribution: Optional[Distribution]
        Describes the natural distribution of search results
    binary_quantized: Optional[bool]
        Once set to true, irreversibly converts all vector dimensions to 1-bit values
    pooling: Optional[PoolingType]
        Configures how individual tokens are merged into a single embedding
    """

    source: str = "huggingFace"
    url: Optional[str] = None
    model: Optional[str] = None  # Defaults to BAAI/bge-base-en-v1.5
    dimensions: Optional[int] = None
    revision: Optional[str] = None
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None  # Default to 400
    distribution: Optional[Distribution] = None
    binary_quantized: Optional[bool] = None
    pooling: Optional[PoolingType] = PoolingType.USE_MODEL


class OllamaEmbedder(CamelBase):
    """Ollama embedder configuration.

    Parameters
    ----------
    source: str
        The embedder source, must be "ollama"
    url: Optional[str]
        The URL Meilisearch contacts when querying the embedder (defaults to http://localhost:11434/api/embeddings)
    api_key: Optional[str]
        Authentication token Meilisearch should send with each request to the embedder
    model: Optional[str]
        The model your embedder uses when generating vectors
    dimensions: Optional[int]
        Number of dimensions in the chosen model
    document_template: Optional[str]
        Template defining the data Meilisearch sends to the embedder
    document_template_max_bytes: Optional[int]
        Maximum allowed size of rendered document template (defaults to 400)
    distribution: Optional[Distribution]
        Describes the natural distribution of search results
    binary_quantized: Optional[bool]
        Once set to true, irreversibly converts all vector dimensions to 1-bit values
    """

    source: str = "ollama"
    url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None
    dimensions: Optional[int] = None
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None
    distribution: Optional[Distribution] = None
    binary_quantized: Optional[bool] = None


class RestEmbedder(CamelBase):
    """REST API embedder configuration.

    Parameters
    ----------
    source: str
        The embedder source, must be "rest"
    url: Optional[str]
        The URL Meilisearch contacts when querying the embedder
    api_key: Optional[str]
        Authentication token Meilisearch should send with each request to the embedder
    dimensions: Optional[int]
        Number of dimensions in the embeddings
    document_template: Optional[str]
        Template defining the data Meilisearch sends to the embedder
    document_template_max_bytes: Optional[int]
        Maximum allowed size of rendered document template (defaults to 400)
    request: Dict[str, Any]
        A JSON value representing the request Meilisearch makes to the remote embedder
    response: Dict[str, Any]
        A JSON value representing the request Meilisearch expects from the remote embedder
    headers: Optional[Dict[str, str]]
        Custom headers to send with the request
    distribution: Optional[Distribution]
        Describes the natural distribution of search results
    binary_quantized: Optional[bool]
        Once set to true, irreversibly converts all vector dimensions to 1-bit values
    """

    source: str = "rest"
    url: Optional[str] = None
    api_key: Optional[str] = None
    dimensions: Optional[int] = None
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None
    request: Dict[str, Any]
    response: Dict[str, Any]
    headers: Optional[Dict[str, str]] = None
    distribution: Optional[Distribution] = None
    binary_quantized: Optional[bool] = None


class UserProvidedEmbedder(CamelBase):
    """User-provided embedder configuration.

    Parameters
    ----------
    source: str
        The embedder source, must be "userProvided"
    dimensions: int
        Number of dimensions in the embeddings
    distribution: Optional[Distribution]
        Describes the natural distribution of search results
    binary_quantized: Optional[bool]
        Once set to true, irreversibly converts all vector dimensions to 1-bit values
    """

    source: str = "userProvided"
    dimensions: int
    distribution: Optional[Distribution] = None
    binary_quantized: Optional[bool] = None


class CompositeEmbedder(CamelBase):
    """Composite embedder configuration.

    Parameters
    ----------
    source: str
        The embedder source, must be "composite"
    indexing_embedder: Union[
        OpenAiEmbedder,
        HuggingFaceEmbedder,
        OllamaEmbedder,
        RestEmbedder,
        UserProvidedEmbedder,
    ]
    search_embedder: Union[
        OpenAiEmbedder,
        HuggingFaceEmbedder,
        OllamaEmbedder,
        RestEmbedder,
        UserProvidedEmbedder,
    ]"""

    source: str = "composite"
    search_embedder: Union[
        OpenAiEmbedder,
        HuggingFaceEmbedder,
        OllamaEmbedder,
        RestEmbedder,
        UserProvidedEmbedder,
    ]
    indexing_embedder: Union[
        OpenAiEmbedder,
        HuggingFaceEmbedder,
        OllamaEmbedder,
        RestEmbedder,
        UserProvidedEmbedder,
    ]


# Type alias for the embedder union type
EmbedderType = Union[
    OpenAiEmbedder,
    HuggingFaceEmbedder,
    OllamaEmbedder,
    RestEmbedder,
    UserProvidedEmbedder,
    CompositeEmbedder,
]


class Embedders(CamelBase):
    """Container for embedder configurations.

    Parameters
    ----------
    embedders: Dict[str, Union[OpenAiEmbedder, HuggingFaceEmbedder, OllamaEmbedder, RestEmbedder, UserProvidedEmbedder]]
        Dictionary of embedder configurations, where keys are embedder names
    """

    embedders: Dict[str, EmbedderType]
