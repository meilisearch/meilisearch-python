from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

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

    @classmethod
    def validate_config(cls, name: str, config: Dict[str, Any]) -> None:
        """Validate the configuration for an OpenAI embedder.

        Parameters
        ----------
        name: str
            The name of the embedder
        config: Dict[str, Any]
            The configuration to validate

        Raises
        ------
        ValueError
            If the configuration is invalid
        """
        if config.get("source") != "openAi":
            raise ValueError(f"Embedder '{name}' must have source 'openAi'")


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

    @classmethod
    def validate_config(cls, name: str, config: Dict[str, Any]) -> None:
        """Validate the configuration for a HuggingFace embedder.

        Parameters
        ----------
        name: str
            The name of the embedder
        config: Dict[str, Any]
            The configuration to validate

        Raises
        ------
        ValueError
            If the configuration is invalid
        """
        if config.get("source") != "huggingFace":
            raise ValueError(f"Embedder '{name}' must have source 'huggingFace'")


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

    @classmethod
    def validate_config(cls, name: str, config: Dict[str, Any]) -> None:
        """Validate the configuration for an Ollama embedder.

        Parameters
        ----------
        name: str
            The name of the embedder
        config: Dict[str, Any]
            The configuration to validate

        Raises
        ------
        ValueError
            If the configuration is invalid
        """
        if config.get("source") != "ollama":
            raise ValueError(f"Embedder '{name}' must have source 'ollama'")


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

    @classmethod
    def validate_config(cls, name: str, config: Dict[str, Any]) -> None:
        """Validate the configuration for a REST embedder.

        Parameters
        ----------
        name: str
            The name of the embedder
        config: Dict[str, Any]
            The configuration to validate

        Raises
        ------
        ValueError
            If the configuration is invalid
        """
        if config.get("source") != "rest":
            raise ValueError(f"Embedder '{name}' must have source 'rest'")

        if "request" not in config:
            raise ValueError(f"Embedder '{name}' with source 'rest' must include 'request' field")

        if "response" not in config:
            raise ValueError(f"Embedder '{name}' with source 'rest' must include 'response' field")


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

    @classmethod
    def validate_config(cls, name: str, config: Dict[str, Any]) -> None:
        """Validate the configuration for a user-provided embedder.

        Parameters
        ----------
        name: str
            The name of the embedder
        config: Dict[str, Any]
            The configuration to validate

        Raises
        ------
        ValueError
            If the configuration is invalid
        """
        if config.get("source") != "userProvided":
            raise ValueError(f"Embedder '{name}' must have source 'userProvided'")

        if "dimensions" not in config:
            raise ValueError(
                f"Embedder '{name}' with source 'userProvided' must include 'dimensions' field"
            )

        if "documentTemplate" in config:
            raise ValueError(
                f"Embedder '{name}' with source 'userProvided' cannot include 'documentTemplate' field"
            )


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

    @classmethod
    def validate_config(cls, config: Dict[str, Dict[str, Any]]) -> None:
        """Validate the configuration for embedders.

        Parameters
        ----------
        config: Dict[str, Dict[str, Any]]
            The configuration to validate, where keys are embedder names and values are embedder configurations

        Raises
        ------
        ValueError
            If the configuration is invalid
        """
        for name, embedder_config in config.items():
            source = embedder_config.get("source")
            if source not in ["openAi", "huggingFace", "ollama", "rest", "userProvided"]:
                raise ValueError(
                    f"Invalid source for embedder '{name}'. "
                    f"Must be one of: 'openAi', 'huggingFace', 'ollama', 'rest', 'userProvided'."
                )

            # Clean up None values for optional fields
            if (
                "documentTemplateMaxBytes" in embedder_config
                and embedder_config["documentTemplateMaxBytes"] is None
            ):
                del embedder_config["documentTemplateMaxBytes"]

            # Validate based on source
            if source == "openAi":
                OpenAiEmbedder.validate_config(name, embedder_config)
            elif source == "huggingFace":
                HuggingFaceEmbedder.validate_config(name, embedder_config)
            elif source == "ollama":
                OllamaEmbedder.validate_config(name, embedder_config)
            elif source == "rest":
                RestEmbedder.validate_config(name, embedder_config)
            elif source == "userProvided":
                UserProvidedEmbedder.validate_config(name, embedder_config)
