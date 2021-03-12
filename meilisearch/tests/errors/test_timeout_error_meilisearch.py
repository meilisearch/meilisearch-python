import pytest
import meilisearch
from meilisearch.errors import MeiliSearchTimeoutError
from meilisearch.tests import BASE_URL, MASTER_KEY


@pytest.mark.usefixtures("indexes_sample")
def test_client_timeout_error(small_movies):
    client = meilisearch.Client(BASE_URL, MASTER_KEY, timeout=1e-99)

    with pytest.raises(MeiliSearchTimeoutError):
        index = client.index("indexUID")
        index.add_documents(small_movies)


def test_client_timeout_set():
    timeout = 1
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY, timeout=timeout)

    with pytest.raises(Exception):
        client.health()

    assert client.config.timeout == timeout


def test_client_timeout_not_set():
    timeout = 10
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY)

    with pytest.raises(Exception):
        client.health()

    assert client.config.timeout == timeout
