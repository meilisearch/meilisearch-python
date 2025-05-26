"""Tests for auto-launch functionality."""

import meilisearch
from meilisearch._local_server import LocalMeilisearchServer


def test_client_auto_launch():
    """Test that client can auto-launch a local Meilisearch instance."""
    # Create client without URL - should auto-launch
    with meilisearch.Client() as client:
        # Verify the client has a local server
        assert client._local_server is not None
        assert isinstance(client._local_server, LocalMeilisearchServer)

        # Verify we can communicate with the server
        assert client.is_healthy()

        # Test basic operations
        # Create an index
        task = client.create_index("test_index")
        client.wait_for_task(task.task_uid)

        # Get the index
        index = client.get_index("test_index")
        assert index.uid == "test_index"

        # Add documents
        documents = [{"id": 1, "title": "Test Document"}, {"id": 2, "title": "Another Document"}]
        task = index.add_documents(documents)
        client.wait_for_task(task.task_uid)

        # Search
        results = index.search("test")
        assert len(results["hits"]) > 0

    # After context manager exits, server should be stopped
    # We can't easily test this without trying to connect again


def test_client_auto_launch_with_api_key():
    """Test auto-launch with a custom API key."""
    api_key = "test_master_key_123"

    with meilisearch.Client(api_key=api_key) as client:
        assert client._local_server is not None
        assert client._local_server.master_key == api_key
        assert client.config.api_key == api_key

        # Should be able to use the client normally
        assert client.is_healthy()


def test_client_with_url_no_auto_launch():
    """Test that providing a URL prevents auto-launch."""
    # This will connect to the test server started by conftest.py
    client = meilisearch.Client("http://127.0.0.1:7700", "masterKey")

    # Should not have a local server
    assert client._local_server is None

    # Should still work normally
    assert client.is_healthy()


def test_client_del_cleanup():
    """Test that __del__ properly cleans up the local server."""
    client = meilisearch.Client()
    assert client._local_server is not None

    # Store reference to local server
    local_server = client._local_server

    # Delete the client
    del client

    # The local server should have been stopped
    # (We can't easily verify the process is dead without platform-specific code)
