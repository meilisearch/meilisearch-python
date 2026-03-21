# pylint: disable=invalid-name

from unittest.mock import patch

import pytest
import requests

import meilisearch
from meilisearch.errors import MeilisearchApiError, version_error_hint_message
from tests import BASE_URL, MASTER_KEY


def test_meilisearch_api_error_no_master_key():
    client = meilisearch.Client(BASE_URL)
    with pytest.raises(MeilisearchApiError):
        client.create_index("some_index")


def test_meilisearch_api_error_wrong_master_key():
    client = meilisearch.Client(BASE_URL, MASTER_KEY + "123")
    with pytest.raises(MeilisearchApiError):
        client.create_index("some_index")


@patch("requests.post")
def test_meilisearch_api_error_no_code(mock_post):
    """Here to test for regressions related to https://github.com/meilisearch/meilisearch-python/issues/305."""
    mock_post.configure_mock(__name__="post")
    mock_response = requests.models.Response()
    mock_response.status_code = 408
    mock_post.return_value = mock_response

    with pytest.raises(MeilisearchApiError):
        client = meilisearch.Client(BASE_URL, MASTER_KEY + "123")
        client.create_index("some_index")


def test_version_error_hint_message():
    mock_response = requests.models.Response()
    mock_response.status_code = 408

    class FakeClass:
        @version_error_hint_message
        def test_method(self):
            raise MeilisearchApiError("This is a test", mock_response)

    with pytest.raises(MeilisearchApiError) as e:
        fake = FakeClass()
        fake.test_method()

    assert (
        "MeilisearchApiError. This is a test. Hint: It might not be working because you're not up to date with the Meilisearch version that test_method call requires."
        == str(e.value)
    )
