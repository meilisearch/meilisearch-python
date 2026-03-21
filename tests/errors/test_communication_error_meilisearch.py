# pylint: disable=invalid-name

from unittest.mock import patch

import pytest
import requests

import meilisearch
from meilisearch.errors import MeilisearchCommunicationError
from tests import MASTER_KEY


@patch("requests.post")
def test_meilisearch_communication_error_host(mock_post):
    mock_post.configure_mock(__name__="post")
    mock_post.side_effect = requests.exceptions.ConnectionError()
    client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY)
    with pytest.raises(MeilisearchCommunicationError):
        client.create_index("some_index")


@patch("requests.post")
def test_meilisearch_communication_error_no_protocol(mock_post):
    mock_post.configure_mock(__name__="post")
    mock_post.side_effect = requests.exceptions.InvalidSchema()
    client = meilisearch.Client("localhost:7700", MASTER_KEY)
    with pytest.raises(MeilisearchCommunicationError, match="no scheme/protocol supplied."):
        client.create_index("some_index")
