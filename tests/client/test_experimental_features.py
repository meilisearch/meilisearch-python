"""Tests for experimental features API."""


def test_get_experimental_features(client):
    """Test getting experimental features."""
    response = client.get_experimental_features()
    assert isinstance(response, dict)
    # Check that at least one known experimental feature is present
    assert "multimodal" in response or "vectorStoreSetting" in response


def test_update_experimental_features(client):
    """Test updating experimental features."""
    # Enable multimodal
    response = client.update_experimental_features({"multimodal": True})
    assert isinstance(response, dict)
    assert response.get("multimodal") is True

    # Disable multimodal
    response = client.update_experimental_features({"multimodal": False})
    assert isinstance(response, dict)
    assert response.get("multimodal") is False


def test_update_multiple_experimental_features(client):
    """Test updating multiple experimental features at once."""
    response = client.update_experimental_features(
        {"multimodal": True, "vectorStoreSetting": True}
    )
    assert isinstance(response, dict)
    # At least one should be accepted (depending on Meilisearch version)
    assert "multimodal" in response or "vectorStoreSetting" in response
