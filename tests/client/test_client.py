# pylint: disable=invalid-name

import pytest

import meilisearch
from tests import BASE_URL, MASTER_KEY


def test_get_client():
    """Tests getting a client instance."""
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    assert client.config
    response = client.health()
    assert response["status"] == "available"


def test_client_timeout_set():
    timeout = 5
    client = meilisearch.Client(BASE_URL, MASTER_KEY, timeout=timeout)
    response = client.health()
    assert client.config.timeout == timeout
    assert response["status"] == "available"


def test_client_timeout_not_set():
    default_timeout = None
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    response = client.health()
    assert client.config.timeout == default_timeout
    assert response["status"] == "available"


@pytest.mark.parametrize(
    "api_key, custom_headers, expected",
    (
        ("testKey", None, {"Authorization": "Bearer testKey"}),
        (
            "testKey",
            {"header_key_1": "header_value_1", "header_key_2": "header_value_2"},
            {
                "Authorization": "Bearer testKey",
                "header_key_1": "header_value_1",
                "header_key_2": "header_value_2",
            },
        ),
        (
            None,
            {"header_key_1": "header_value_1", "header_key_2": "header_value_2"},
            {
                "header_key_1": "header_value_1",
                "header_key_2": "header_value_2",
            },
        ),
        (None, None, {}),
    ),
)
def test_headers(api_key, custom_headers, expected):
    client = meilisearch.Client("127.0.0.1:7700", api_key=api_key, custom_headers=custom_headers)

    assert client.http.headers.items() >= expected.items()
