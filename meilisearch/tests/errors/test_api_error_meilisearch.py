# pylint: disable=invalid-name

from unittest.mock import patch
import pytest
import requests
import meilisearch
from meilisearch.errors import MeiliSearchApiError
from meilisearch.tests import BASE_URL, MASTER_KEY

def test_meilisearch_api_error_no_master_key():
    client = meilisearch.Client(BASE_URL)
    with pytest.raises(MeiliSearchApiError):
        client.create_index("some_index")

def test_meilisearch_api_error_wrong_master_key():
    client = meilisearch.Client(BASE_URL, MASTER_KEY + '123')
    with pytest.raises(MeiliSearchApiError):
        client.create_index("some_index")

@patch('requests.post')
def test_meilisearch_api_error_no_error_code(mock_post):
    """Here to test for regressions related to https://github.com/meilisearch/meilisearch-python/issues/305."""

    mock_response = requests.models.Response()
    mock_response.status_code = 408
    mock_post.return_value = mock_response

    with pytest.raises(MeiliSearchApiError):
        client = meilisearch.Client(BASE_URL, MASTER_KEY + '123')
        client.create_index('some_index')
