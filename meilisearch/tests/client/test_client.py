# pylint: disable=invalid-name

import pytest

import meilisearch
from meilisearch.errors import MeiliSearchTimeoutError
from meilisearch.tests import BASE_URL, MASTER_KEY

def test_get_client():
    """Tests getting a client instance."""
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    assert client.config
    response = client.health()
    assert response.status_code >= 200 and response.status_code < 400


def test_client_timeout_set():
    client = meilisearch.Client(BASE_URL, MASTER_KEY, timeout=5)
    response = client.health()
    assert response.status_code >= 200 and response.status_code < 400


def test_client_timeout_not_set():
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    response = client.health()
    assert response.status_code >= 200 and response.status_code < 400


def test_client_timeout_error():
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY, timeout=1)

    with pytest.raises(MeiliSearchTimeoutError):
        client.health()
