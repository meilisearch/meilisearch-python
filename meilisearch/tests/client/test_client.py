# pylint: disable=invalid-name

import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

def test_get_client():
    """Tests getting a client instance."""
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    assert client.config
    response = client.health()
    assert response.status_code >= 200 and response.status_code < 400
