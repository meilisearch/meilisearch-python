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


@patch("requests.post")
def test_meilisearch_api_error_falls_back_to_raw_message_for_non_json_response(mock_post):
    """Uses raw response text when an API error body is not valid JSON."""
    mock_post.configure_mock(__name__="post")
    mock_response = requests.models.Response()
    mock_response.status_code = 502
    mock_response._content = b"<html>Bad Gateway</html>"  # pylint: disable=protected-access
    mock_post.return_value = mock_response

    with pytest.raises(MeilisearchApiError) as exc:
        client = meilisearch.Client(BASE_URL, MASTER_KEY + "123")
        client.create_index("some_index")

    assert exc.value.status_code == 502
    assert exc.value.message == "<html>Bad Gateway</html>"
    assert exc.value.code is None
    assert exc.value.link is None
    assert exc.value.type is None


@patch("requests.post")
def test_meilisearch_api_error_falls_back_to_raw_message_for_non_object_json_response(mock_post):
    """Uses raw response text when parsed JSON is not an object."""
    mock_post.configure_mock(__name__="post")
    mock_response = requests.models.Response()
    mock_response.status_code = 502
    mock_response._content = b'["Bad Gateway"]'  # pylint: disable=protected-access
    mock_post.return_value = mock_response

    with pytest.raises(MeilisearchApiError) as exc:
        client = meilisearch.Client(BASE_URL, MASTER_KEY + "123")
        client.create_index("some_index")

    assert exc.value.status_code == 502
    assert exc.value.message == '["Bad Gateway"]'
    assert exc.value.code is None
    assert exc.value.link is None
    assert exc.value.type is None


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
