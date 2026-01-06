import pytest

from tests.common import REMOTE_MS_1, REMOTE_MS_2
from tests.test_utils import reset_network_config


@pytest.mark.usefixtures("enable_network_options")
def test_get_all_networks(client):
    """Tests get all network in MS"""
    response = client.get_all_networks()

    assert isinstance(response, dict)


@pytest.mark.usefixtures("enable_network_options")
def test_add_or_update_networks(client):
    """Tests upsert network remote instance."""
    body = {
        "remotes": {
            REMOTE_MS_1: {
                "url": "http://localhost:7700",
                "searchApiKey": "xxxxxxxxxxxxxx",
                "writeApiKey": "xxxxxxxxx",
            },
            REMOTE_MS_2: {
                "url": "http://localhost:7720",
                "searchApiKey": "xxxxxxxxxxxxxxx",
                "writeApiKey": "xxxxxxxx",
            },
        },
    }
    response = client.add_or_update_networks(body=body)

    assert isinstance(response, dict)
    assert len(response["remotes"]) >= 2
    assert REMOTE_MS_2 in response["remotes"]
    assert REMOTE_MS_1 in response["remotes"]

    reset_network_config(client)


@pytest.mark.usefixtures("enable_network_options")
def test_configure_as_leader(client):
    """Test configuring the current instance as a Leader with one follower."""
    body = {
        "remotes": {
            REMOTE_MS_1: {
                "url": "http://localhost:7701",
                "searchApiKey": "remoteSearchKey",
            }
        },
        "leader": None,
    }
    response = client.add_or_update_networks(body)

    assert isinstance(response, dict)
    assert REMOTE_MS_1 in response["remotes"]
    assert response.get("leader") is None

    reset_network_config(client)
