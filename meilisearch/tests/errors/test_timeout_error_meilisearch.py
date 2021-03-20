from unittest.mock import patch
import pytest
import requests
import meilisearch
from meilisearch.errors import MeiliSearchTimeoutError
from meilisearch.tests import BASE_URL, MASTER_KEY


@patch("requests.get")
def test_client_timeout_error(mock_get):
    mock_get.side_effect = requests.exceptions.Timeout()
    client = meilisearch.Client(BASE_URL, MASTER_KEY, timeout=1)

    with pytest.raises(MeiliSearchTimeoutError):
        client.version()


def test_client_timeout_set():
    timeout = 1
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY, timeout=timeout)

    with pytest.raises(Exception):
        client.health()

    assert client.config.timeout == timeout
