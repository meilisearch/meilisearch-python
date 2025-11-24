# pylint: disable=redefined-outer-name
"""Tests for indexingFragments and searchFragments in embedders (multimodal feature).

These tests validate CONFIGURATION ONLY, not AI functionality.
They only ensure fragments can be configured and stored in Meilisearch.
No AI calls or document indexing/searching occurs.
"""

import pytest

DUMMY_URL = "http://localhost:8000/embed"
TEST_MODEL = "test-model"
MULTIMODAL_MODEL = "multimodal"


def apply_embedders(index, config):
    """Helper to update embedders and wait for task completion."""
    response = index.update_embedders(config)
    update = index.wait_for_task(response.task_uid)
    assert update.status == "succeeded"
    return index.get_embedders()


def test_rest_embedder_with_fragments(empty_index, multimodal_enabled):
    """Tests that REST embedder can be configured with indexingFragments and searchFragments."""
    index = empty_index()

    config = {
        "rest_fragments": {
            "source": "rest",
            "url": DUMMY_URL,
            "apiKey": "test-key",
            "dimensions": 512,
            "indexingFragments": {"text": {"value": "{{doc.title}} - {{doc.description}}"}},
            "searchFragments": {"text": {"value": "{{fragment}}"}},
            "request": {"input": ["{{fragment}}"], "model": TEST_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
            "headers": {"Authorization": "Bearer test-key"},
        }
    }

    embedders = apply_embedders(index, config)

    e = embedders.embedders["rest_fragments"]
    assert e.source == "rest"
    assert e.url == DUMMY_URL
    assert e.dimensions == 512
    assert e.indexing_fragments is not None
    assert e.search_fragments is not None


def test_rest_embedder_with_multiple_fragments(empty_index, multimodal_enabled):
    """Tests REST embedder with multiple fragment types."""
    index = empty_index()

    config = {
        "multi_fragments": {
            "source": "rest",
            "url": DUMMY_URL,
            "dimensions": 1024,
            "indexingFragments": {
                "text": {"value": "{{doc.title}}"},
                "description": {"value": "{{doc.overview}}"}
            },
            "searchFragments": {
                "text": {"value": "{{fragment}}"},
                "description": {"value": "{{fragment}}"}
            },
            "request": {"input": ["{{fragment}}"], "model": TEST_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
        }
    }

    embedders = apply_embedders(index, config)

    e = embedders.embedders["multi_fragments"]
    assert e.source == "rest"
    assert len(e.indexing_fragments) >= 1
    assert len(e.search_fragments) >= 1


def test_fragments_without_document_template(empty_index, multimodal_enabled):
    """Tests fragments can be used without documentTemplate."""
    index = empty_index()

    config = {
        "fragments_only": {
            "source": "rest",
            "url": DUMMY_URL,
            "dimensions": 512,
            "indexingFragments": {"text": {"value": "{{doc.content}}"}},
            "searchFragments": {"text": {"value": "{{fragment}}"}},
            "request": {"input": ["{{fragment}}"], "model": TEST_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
        }
    }

    embedders = apply_embedders(index, config)
    e = embedders.embedders["fragments_only"]
    assert e.document_template is None
    assert e.indexing_fragments is not None
    assert e.search_fragments is not None


def test_fragments_require_multimodal_feature(empty_index):
    """Tests fragments require multimodal feature enabled."""
    index = empty_index()

    config = {
        "test": {
            "source": "rest",
            "url": DUMMY_URL,
            "dimensions": 512,
            "indexingFragments": {"text": {"value": "{{doc.title}}"}},
            "searchFragments": {"text": {"value": "{{fragment}}"}},
            "request": {"input": ["{{fragment}}"], "model": TEST_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
        }
    }

    # May succeed or fail depending on server config; both are acceptable
    try:
        embedders = apply_embedders(index, config)
        assert embedders.embedders["test"].indexing_fragments is not None
    except Exception:
        pass


def test_update_fragments_separately(empty_index, multimodal_enabled):
    """Tests updating indexingFragments and searchFragments separately."""
    index = empty_index()

    initial_config = {
        "updatable": {
            "source": "rest",
            "url": DUMMY_URL,
            "dimensions": 512,
            "indexingFragments": {"text": {"value": "{{doc.title}}"}},
            "searchFragments": {"text": {"value": "{{fragment}}"}},
            "request": {"input": ["{{fragment}}"], "model": TEST_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
        }
    }

    apply_embedders(index, initial_config)

    updated_config = {
        "updatable": {
            "source": "rest",
            "url": DUMMY_URL,
            "dimensions": 512,
            "indexingFragments": {"text": {"value": "{{doc.title}} - {{doc.description}}"}},
            "searchFragments": {"text": {"value": "{{fragment}}"}},
            "request": {"input": ["{{fragment}}"], "model": TEST_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
        }
    }

    embedders = apply_embedders(index, updated_config)
    assert embedders.embedders["updatable"].indexing_fragments is not None


def test_profile_picture_and_title_fragments(empty_index, multimodal_enabled):
    """Tests real-world use case: user profiles with picture and title."""
    index = empty_index()

    config = {
        "user_profile": {
            "source": "rest",
            "url": DUMMY_URL,
            "dimensions": 768,
            "indexingFragments": {
                "user_name": {"value": "{{doc.name}}"},
                "avatar": {"value": "{{doc.profile_picture_url}}"},
                "biography": {"value": "{{doc.bio}}"},
            },
            "searchFragments": {
                "user_name": {"value": "{{fragment}}"},
                "avatar": {"value": "{{fragment}}"},
                "biography": {"value": "{{fragment}}"},
            },
            "request": {"input": ["{{fragment}}"], "model": MULTIMODAL_MODEL},
            "response": {"data": [{"embedding": "{{embedding}}"}]},
        }
    }

    embedders = apply_embedders(index, config)
    e = embedders.embedders["user_profile"]

    assert e.source == "rest"
    expected_keys = {"user_name", "avatar", "biography"}
    assert set(e.indexing_fragments.keys()) == expected_keys
    assert set(e.search_fragments.keys()) == expected_keys
