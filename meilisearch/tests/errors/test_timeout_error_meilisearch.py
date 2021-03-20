import pytest
import meilisearch
from meilisearch.errors import MeiliSearchTimeoutError
from meilisearch.tests import BASE_URL, MASTER_KEY

def test_client_timeout_set():
    timeout = 1
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY, timeout=timeout)

    with pytest.raises(Exception):
        client.health()

    assert client.config.timeout == timeout
