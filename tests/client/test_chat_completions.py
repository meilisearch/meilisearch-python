# pylint: disable=invalid-name

from unittest.mock import patch

import pytest
import requests

from meilisearch.errors import MeilisearchApiError, MeilisearchCommunicationError


class MockStreamingResponse:
    """Mock response object for testing streaming functionality."""

    def __init__(self, lines, ok=True, status_code=200, text=""):
        self.lines = lines
        self.ok = ok
        self.status_code = status_code
        self.text = text
        self._closed = False

    def iter_lines(self):
        """Simulate iter_lines() method of requests.Response."""
        yield from self.lines

    def close(self):
        """Simulate close() method of requests.Response."""
        self._closed = True

    def raise_for_status(self):
        """Simulate raise_for_status() method of requests.Response."""
        if not self.ok:
            raise requests.exceptions.HTTPError(f"HTTP {self.status_code}")


def test_create_chat_completion_basic_stream(client):
    """Test basic streaming functionality with successful response."""
    dummy_lines = [
        b'data: {"id":"chatcmpl-1","object":"chat.completion.chunk","choices":[{"delta":{"content":"Hello"}}]}',
        b'data: {"id":"chatcmpl-1","object":"chat.completion.chunk","choices":[{"delta":{"content":" world"}}]}',
        b'data: [DONE]'
    ]
    mock_resp = MockStreamingResponse(dummy_lines)

    with patch.object(client.http, 'post_stream', return_value=mock_resp) as mock_post:
        messages = [{"role": "user", "content": "Hi"}]
        chunks = list(client.create_chat_completion("my-assistant", messages=messages))

        # Verify the HTTP call was made correctly
        mock_post.assert_called_once_with(
            "chats/my-assistant/chat/completions",
            body={
                "model": "gpt-3.5-turbo",
                "messages": messages,
                "stream": True
            }
        )

        # Verify the chunks are parsed correctly
        assert len(chunks) == 2
        assert chunks[0]["choices"][0]["delta"]["content"] == "Hello"
        assert chunks[1]["choices"][0]["delta"]["content"] == " world"
        assert mock_resp._closed  # pylint: disable=protected-access


def test_create_chat_completion_stream_false_raises_error(client):
    """Test that stream=False raises ValueError."""
    messages = [{"role": "user", "content": "Test"}]

    with pytest.raises(ValueError, match="Non-streaming chat completions are not supported"):
        list(client.create_chat_completion("my-assistant", messages=messages, stream=False))


def test_create_chat_completion_json_decode_error(client):
    """Test that malformed JSON raises MeilisearchCommunicationError."""
    dummy_lines = [
        b'data: {"invalid": json}',  # Malformed JSON
    ]
    mock_resp = MockStreamingResponse(dummy_lines)

    with patch.object(client.http, 'post_stream', return_value=mock_resp):
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(MeilisearchCommunicationError, match="Failed to parse chat chunk"):
            list(client.create_chat_completion("my-assistant", messages=messages))


def test_create_chat_completion_http_error_propagated(client):
    """Test that HTTP errors from post_stream are properly propagated."""
    with patch.object(client.http, 'post_stream') as mock_post:
        error_response = MockStreamingResponse([], ok=False, status_code=400, text='{"message": "API Error"}')
        mock_post.side_effect = MeilisearchApiError("API Error", error_response)
        messages = [{"role": "user", "content": "Test"}]

        with pytest.raises(MeilisearchApiError, match="API Error"):
            list(client.create_chat_completion("my-assistant", messages=messages))


def test_get_chat_workspaces(client):
    """Test basic get_chat_workspaces functionality."""
    mock_response = {
        "results": [
            {"uid": "workspace1", "name": "My Workspace", "model": "gpt-3.5-turbo"},
            {"uid": "workspace2", "name": "Another Workspace", "model": "gpt-4"}
        ],
        "offset": 0,
        "limit": 20,
        "total": 2
    }

    with patch.object(client.http, 'get', return_value=mock_response) as mock_get:
        result = client.get_chat_workspaces()

        # Verify the HTTP call was made correctly
        mock_get.assert_called_once_with("chats")

        # Verify the response is returned as-is
        assert result == mock_response


def test_update_chat_workspace_settings(client):
    """Test basic update_chat_workspace_settings functionality."""
    mock_response = {
        "model": "gpt-4-turbo",
        "temperature": 0.8,
        "max_tokens": 1500
    }

    settings_update = {
        "temperature": 0.8,
        "max_tokens": 1500
    }

    with patch.object(client.http, 'patch', return_value=mock_response) as mock_patch:
        result = client.update_chat_workspace_settings("my-workspace", settings_update)

        # Verify the HTTP call was made correctly
        mock_patch.assert_called_once_with("chats/my-workspace/settings", body=settings_update)

        # Verify the response is returned as-is
        assert result == mock_response
