from __future__ import annotations

from typing import Any, Dict, List, Optional, Union, Mapping, MutableMapping, Type, TypeVar

from camel_converter.pydantic_base import CamelBase


T = TypeVar("T", bound="CamelBase")


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
    api_key: Optional[str]
        Authentication token Meilisearch should send with each request to the embedder
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
    """

    source: str = "huggingFace"
    url: Optional[str] = None
    api_key: Optional[str] = None
    model: Optional[str] = None  # Defaults to BAAI/bge-base-en-v1.5
    dimensions: Optional[int] = None
    revision: Optional[str] = None
    document_template: Optional[str] = None
    document_template_max_bytes: Optional[int] = None  # Default to 400
    distribution: Optional[Distribution] = None
    binary_quantized: Optional[bool] = None


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
        Number of dimensions in the chosen model
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


class Embedders(CamelBase):
    """Container for embedder configurations.

    Parameters
    ----------
    embedders: Dict[str, Union[OpenAiEmbedder, HuggingFaceEmbedder, OllamaEmbedder, RestEmbedder, UserProvidedEmbedder]]
        Dictionary of embedder configurations, where keys are embedder names
    """

    embedders: Dict[
        str,
        Union[
            OpenAiEmbedder, HuggingFaceEmbedder, OllamaEmbedder, RestEmbedder, UserProvidedEmbedder
        ],
    ]


def validate_embedder_config(embedder_name: str, config: Dict[str, Any]) -> Dict[str, Any]:
    """Validate an embedder configuration.

    Parameters
    ----------
    embedder_name: str
        The name of the embedder
    config: Dict[str, Any]
        The embedder configuration

    Returns
    -------
    Dict[str, Any]
        The validated and cleaned embedder configuration

    Raises
    ------
    ValueError
        If the configuration is invalid
    """
    # Validate source field
    source = config.get("source")
    if source not in ["openAi", "huggingFace", "ollama", "rest", "userProvided"]:
        raise ValueError(
            f"Invalid source for embedder '{embedder_name}'. "
            f"Must be one of: 'openAi', 'huggingFace', 'ollama', 'rest', 'userProvided'."
        )

    # Create a copy of the config to avoid modifying the original
    cleaned_config = config.copy()

    # Validate based on source type
    if source == "openAi":
        OpenAiEmbedder(**cleaned_config)
    elif source == "huggingFace":
        HuggingFaceEmbedder(**cleaned_config)
    elif source == "ollama":
        OllamaEmbedder(**cleaned_config)
    elif source == "rest":
        # Validate required fields for REST embedder
        if "request" not in cleaned_config or "response" not in cleaned_config:
            raise ValueError(
                f"Embedder '{embedder_name}' with source 'rest' must include 'request' and 'response' fields."
            )
        RestEmbedder(**cleaned_config)
    elif source == "userProvided":
        # Validate required fields for UserProvided embedder
        if "dimensions" not in cleaned_config:
            raise ValueError(
                f"Embedder '{embedder_name}' with source 'userProvided' must include 'dimensions' field."
            )

        # Remove fields not supported by UserProvided
        for field in ["documentTemplate", "documentTemplateMaxBytes"]:
            if field in cleaned_config:
                del cleaned_config[field]

        UserProvidedEmbedder(**cleaned_config)

    # Clean up None values for optional fields
    if (
        "documentTemplateMaxBytes" in cleaned_config
        and cleaned_config["documentTemplateMaxBytes"] is None
    ):
        del cleaned_config["documentTemplateMaxBytes"]

    return cleaned_config


def validate_embedders(embedders: MutableMapping[str, Any]) -> MutableMapping[str, Any]:
    """Validate a dictionary of embedder configurations.

    Parameters
    ----------
    embedders: MutableMapping[str, Any]
        Dictionary of embedder configurations

    Returns
    -------
    MutableMapping[str, Any]
        The validated and cleaned embedder configurations

    Raises
    ------
    ValueError
        If any configuration is invalid
    """
    if not embedders:
        return embedders

    cleaned_embedders = {}
    for embedder_name, config in embedders.items():
        cleaned_embedders[embedder_name] = validate_embedder_config(embedder_name, config)

    return cleaned_embedders
