# pylint: disable=redefined-outer-name

import pytest

from meilisearch.models.embedders import (
    CompositeEmbedder,
    HuggingFaceEmbedder,
    OpenAiEmbedder,
    PoolingType,
    UserProvidedEmbedder,
)


def test_get_default_embedders(empty_index):
    """Tests getting default embedders."""
    response = empty_index().get_embedders()

    assert response is None


def test_update_embedders_with_user_provided_source(new_embedders, empty_index):
    """Tests updating embedders."""
    index = empty_index()
    response_update = index.update_embedders(new_embedders)
    update = index.wait_for_task(response_update.task_uid)
    response_get = index.get_embedders()
    assert update.status == "succeeded"
    assert isinstance(response_get.embedders["default"], UserProvidedEmbedder)
    assert isinstance(response_get.embedders["open_ai"], OpenAiEmbedder)


def test_reset_embedders(new_embedders, empty_index):
    """Tests resetting the typo_tolerance setting to its default value."""
    index = empty_index()

    # Update the settings
    response_update = index.update_embedders(new_embedders)
    update1 = index.wait_for_task(response_update.task_uid)
    assert update1.status == "succeeded"
    # Get the setting after update
    response_get = index.get_embedders()
    assert isinstance(response_get.embedders["default"], UserProvidedEmbedder)
    assert isinstance(response_get.embedders["open_ai"], OpenAiEmbedder)
    # Reset the setting
    response_reset = index.reset_embedders()
    update2 = index.wait_for_task(response_reset.task_uid)
    # Get the setting after reset
    assert update2.status == "succeeded"
    assert isinstance(response_get.embedders["default"], UserProvidedEmbedder)
    assert isinstance(response_get.embedders["open_ai"], OpenAiEmbedder)
    response_last = index.get_embedders()
    assert response_last is None


def test_openai_embedder_format(empty_index):
    """Tests that OpenAi embedder has the required fields and proper format."""
    index = empty_index()

    openai_embedder = {
        "openai": {
            "source": "openAi",
            "apiKey": "test-key",
            "model": "text-embedding-3-small",
            "dimensions": 1536,
            "documentTemplateMaxBytes": 400,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binaryQuantized": False,
        }
    }
    response = index.update_embedders(openai_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["openai"].source == "openAi"
    assert embedders.embedders["openai"].model == "text-embedding-3-small"
    assert embedders.embedders["openai"].dimensions == 1536
    assert hasattr(embedders.embedders["openai"], "document_template")
    assert embedders.embedders["openai"].document_template_max_bytes == 400
    assert embedders.embedders["openai"].distribution.mean == 0.5
    assert embedders.embedders["openai"].distribution.sigma == 0.1
    assert embedders.embedders["openai"].binary_quantized is False


def test_huggingface_embedder_format(empty_index):
    """Tests that HuggingFace embedder has the required fields and proper format."""
    index = empty_index()

    huggingface_embedder = {
        "huggingface": {
            "source": "huggingFace",
            "model": "BAAI/bge-base-en-v1.5",
            "revision": "main",
            "documentTemplateMaxBytes": 400,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binaryQuantized": False,
        }
    }
    response = index.update_embedders(huggingface_embedder)
    index.wait_for_task(response.task_uid, timeout_in_ms=60000)  # embedder config can take longer.
    embedders = index.get_embedders()
    assert embedders.embedders["huggingface"].source == "huggingFace"
    assert embedders.embedders["huggingface"].model == "BAAI/bge-base-en-v1.5"
    assert embedders.embedders["huggingface"].revision == "main"
    assert hasattr(embedders.embedders["huggingface"], "document_template")
    assert embedders.embedders["huggingface"].document_template_max_bytes == 400
    assert embedders.embedders["huggingface"].distribution.mean == 0.5
    assert embedders.embedders["huggingface"].distribution.sigma == 0.1
    assert embedders.embedders["huggingface"].binary_quantized is False
    assert embedders.embedders["huggingface"].pooling is PoolingType.USE_MODEL


def test_ollama_embedder_format(empty_index):
    """Tests that Ollama embedder has the required fields and proper format."""
    index = empty_index()

    ollama_embedder = {
        "ollama": {
            "source": "ollama",
            "url": "http://localhost:11434/api/embeddings",
            "apiKey": "test-key",
            "model": "llama2",
            "dimensions": 4096,
            "documentTemplateMaxBytes": 400,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binaryQuantized": False,
        }
    }
    response = index.update_embedders(ollama_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["ollama"].source == "ollama"
    assert embedders.embedders["ollama"].url == "http://localhost:11434/api/embeddings"
    assert embedders.embedders["ollama"].model == "llama2"
    assert embedders.embedders["ollama"].dimensions == 4096
    assert hasattr(embedders.embedders["ollama"], "document_template")
    assert embedders.embedders["ollama"].document_template_max_bytes == 400
    assert embedders.embedders["ollama"].distribution.mean == 0.5
    assert embedders.embedders["ollama"].distribution.sigma == 0.1
    assert embedders.embedders["ollama"].binary_quantized is False


def test_rest_embedder_format(empty_index):
    """Tests that Rest embedder has the required fields and proper format."""
    index = empty_index()

    rest_embedder = {
        "rest": {
            "source": "rest",
            "url": "http://localhost:8000/embed",
            "apiKey": "test-key",
            "dimensions": 512,
            "documentTemplateMaxBytes": 400,
            "request": {"model": "MODEL_NAME", "input": "{{text}}"},
            "response": {"result": {"data": ["{{embedding}}"]}},
            "headers": {"Authorization": "Bearer test-key"},
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binaryQuantized": False,
        }
    }
    response = index.update_embedders(rest_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["rest"].source == "rest"
    assert embedders.embedders["rest"].url == "http://localhost:8000/embed"
    assert embedders.embedders["rest"].dimensions == 512
    assert hasattr(embedders.embedders["rest"], "document_template")
    assert embedders.embedders["rest"].document_template_max_bytes == 400
    assert embedders.embedders["rest"].request == {"model": "MODEL_NAME", "input": "{{text}}"}
    assert embedders.embedders["rest"].response == {"result": {"data": ["{{embedding}}"]}}
    assert embedders.embedders["rest"].headers == {"Authorization": "Bearer test-key"}
    assert embedders.embedders["rest"].distribution.mean == 0.5
    assert embedders.embedders["rest"].distribution.sigma == 0.1
    assert embedders.embedders["rest"].binary_quantized is False


def test_user_provided_embedder_format(empty_index):
    """Tests that UserProvided embedder has the required fields and proper format."""
    index = empty_index()

    user_provided_embedder = {
        "user_provided": {
            "source": "userProvided",
            "dimensions": 512,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binaryQuantized": False,
        }
    }
    response = index.update_embedders(user_provided_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["user_provided"].source == "userProvided"
    assert embedders.embedders["user_provided"].dimensions == 512
    assert embedders.embedders["user_provided"].distribution.mean == 0.5
    assert embedders.embedders["user_provided"].distribution.sigma == 0.1
    assert embedders.embedders["user_provided"].binary_quantized is False


@pytest.mark.usefixtures("enable_composite_embedders")
def test_composite_embedder_format(empty_index):
    """Tests that CompositeEmbedder embedder has the required fields and proper format."""
    index = empty_index()

    embedder = HuggingFaceEmbedder().model_dump(by_alias=True, exclude_none=True)

    # create composite embedder
    composite_embedder = {
        "composite": {
            "source": "composite",
            "searchEmbedder": embedder,
            "indexingEmbedder": embedder,
        }
    }

    response = index.update_embedders(composite_embedder)
    update = index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert update.status == "succeeded"

    assert embedders.embedders["composite"].source == "composite"

    # ensure serialization roundtrips nicely
    assert isinstance(embedders.embedders["composite"], CompositeEmbedder)
    assert isinstance(embedders.embedders["composite"].search_embedder, HuggingFaceEmbedder)
    assert isinstance(embedders.embedders["composite"].indexing_embedder, HuggingFaceEmbedder)

    # ensure search_embedder has no document_template
    assert getattr(embedders.embedders["composite"].search_embedder, "document_template") is None
    assert (
        getattr(
            embedders.embedders["composite"].search_embedder,
            "document_template_max_bytes",
        )
        is None
    )
    assert getattr(embedders.embedders["composite"].indexing_embedder, "document_template")
