# pylint: disable=redefined-outer-name

from meilisearch.models.embedders import OpenAiEmbedder, UserProvidedEmbedder


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


def test_embedder_format_fields(empty_index):
    """Tests that each embedder type has the required fields and proper format."""
    index = empty_index()

    # Test OpenAi embedder
    openai_embedder = {
        "openai": {
            "source": "openAi",
            "api_key": "test-key",
            "model": "text-embedding-3-small",
            "dimensions": 1536,
            "document_template": "{{title}}",
            "document_template_max_bytes": 400,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binary_quantized": False,
        }
    }
    response = index.update_embedders(openai_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["openai"].source == "openAi"
    assert embedders.embedders["openai"].api_key == "test-key"
    assert embedders.embedders["openai"].model == "text-embedding-3-small"
    assert embedders.embedders["openai"].dimensions == 1536
    assert embedders.embedders["openai"].document_template == "{{title}}"
    assert embedders.embedders["openai"].document_template_max_bytes == 400
    assert embedders.embedders["openai"].distribution.mean == 0.5
    assert embedders.embedders["openai"].distribution.sigma == 0.1
    assert embedders.embedders["openai"].binary_quantized is False

    # Test HuggingFace embedder
    huggingface_embedder = {
        "huggingface": {
            "source": "huggingFace",
            "model": "BAAI/bge-base-en-v1.5",
            "dimensions": 768,
            "revision": "main",
            "document_template": "{{title}}",
            "document_template_max_bytes": 400,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binary_quantized": False,
        }
    }
    response = index.update_embedders(huggingface_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["huggingface"].source == "huggingFace"
    assert embedders.embedders["huggingface"].model == "BAAI/bge-base-en-v1.5"
    assert embedders.embedders["huggingface"].dimensions == 768
    assert embedders.embedders["huggingface"].revision == "main"
    assert embedders.embedders["huggingface"].document_template == "{{title}}"
    assert embedders.embedders["huggingface"].document_template_max_bytes == 400
    assert embedders.embedders["huggingface"].distribution.mean == 0.5
    assert embedders.embedders["huggingface"].distribution.sigma == 0.1
    assert embedders.embedders["huggingface"].binary_quantized is False

    # Test Ollama embedder
    ollama_embedder = {
        "ollama": {
            "source": "ollama",
            "url": "http://localhost:11434/api/embeddings",
            "api_key": "test-key",
            "model": "llama2",
            "dimensions": 4096,
            "document_template": "{{title}}",
            "document_template_max_bytes": 400,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binary_quantized": False,
        }
    }
    response = index.update_embedders(ollama_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["ollama"].source == "ollama"
    assert embedders.embedders["ollama"].url == "http://localhost:11434/api/embeddings"
    assert embedders.embedders["ollama"].api_key == "test-key"
    assert embedders.embedders["ollama"].model == "llama2"
    assert embedders.embedders["ollama"].dimensions == 4096
    assert embedders.embedders["ollama"].document_template == "{{title}}"
    assert embedders.embedders["ollama"].document_template_max_bytes == 400
    assert embedders.embedders["ollama"].distribution.mean == 0.5
    assert embedders.embedders["ollama"].distribution.sigma == 0.1
    assert embedders.embedders["ollama"].binary_quantized is False

    # Test Rest embedder
    rest_embedder = {
        "rest": {
            "source": "rest",
            "url": "http://localhost:8000/embed",
            "api_key": "test-key",
            "dimensions": 512,
            "document_template": "{{title}}",
            "document_template_max_bytes": 400,
            "request": {"text": "{{title}}"},
            "response": {"embedding": "vector"},
            "headers": {"Authorization": "Bearer test-key"},
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binary_quantized": False,
        }
    }
    response = index.update_embedders(rest_embedder)
    index.wait_for_task(response.task_uid)
    embedders = index.get_embedders()
    assert embedders.embedders["rest"].source == "rest"
    assert embedders.embedders["rest"].url == "http://localhost:8000/embed"
    assert embedders.embedders["rest"].api_key == "test-key"
    assert embedders.embedders["rest"].dimensions == 512
    assert embedders.embedders["rest"].document_template == "{{title}}"
    assert embedders.embedders["rest"].document_template_max_bytes == 400
    assert embedders.embedders["rest"].request == {"text": "{{title}}"}
    assert embedders.embedders["rest"].response == {"embedding": "vector"}
    assert embedders.embedders["rest"].headers == {"Authorization": "Bearer test-key"}
    assert embedders.embedders["rest"].distribution.mean == 0.5
    assert embedders.embedders["rest"].distribution.sigma == 0.1
    assert embedders.embedders["rest"].binary_quantized is False

    # Test UserProvided embedder
    user_provided_embedder = {
        "user_provided": {
            "source": "userProvided",
            "dimensions": 512,
            "distribution": {"mean": 0.5, "sigma": 0.1},
            "binary_quantized": False,
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
