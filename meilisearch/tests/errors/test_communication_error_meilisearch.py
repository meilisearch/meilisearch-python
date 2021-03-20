# pylint: disable=invalid-name

from unittest.mock import patch
import pytest
import requests
import meilisearch
from meilisearch.errors import MeiliSearchCommunicationError
from meilisearch.tests import MASTER_KEY


@patch("requests.post")
def test_meilisearch_communication_error_host(mock_post):
    mock_post.side_effect = requests.exceptions.ConnectionError()
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY)
    with pytest.raises(MeiliSearchCommunicationError):
        client.create_index("some_index")
