import pytest

from tests.common import BASE_URL, REMOTE_MS_1
from tests.test_utils import reset_network_config


@pytest.mark.usefixtures("enable_network_options")
def test_update_and_get_network_settings(client):
    """Test updating and getting network settings."""
    instance_name = REMOTE_MS_1
    options = {
        "self": instance_name,
        "remotes": {
            instance_name: {
                "url": BASE_URL,
                "searchApiKey": "search-key-1",
                "writeApiKey": "write-key-1",
            }
        },
        "sharding": True,
    }

    client.add_or_update_networks(options)
    response = client.get_all_networks()

    assert response["self"] == options["self"]
    assert response["remotes"][instance_name]["url"] == options["remotes"][instance_name]["url"]
    assert (
        response["remotes"][instance_name]["searchApiKey"]
        == options["remotes"][instance_name]["searchApiKey"]
    )
    assert (
        response["remotes"][instance_name]["writeApiKey"]
        == options["remotes"][instance_name]["writeApiKey"]
    )
    reset_network_config(client)
