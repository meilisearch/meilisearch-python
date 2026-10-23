import pytest
import requests

from meilisearch._httprequests import HttpRequests
from meilisearch.config import Config
from meilisearch.version import qualified_version
from tests import BASE_URL, MASTER_KEY


def test_get_headers_from_http_requests_instance():
    """Tests getting defined headers from instance in HttpRequests."""
    config = Config(BASE_URL, MASTER_KEY, timeout=None)
    http = HttpRequests(config=config)

    assert http.headers["Authorization"] == f"Bearer {MASTER_KEY}"
    assert http.headers["User-Agent"] == qualified_version()


def test_get_headers_with_multiple_user_agent():
    """Tests getting defined headers from instance in HttpRequests."""
    config = Config(
        BASE_URL,
        MASTER_KEY,
        timeout=None,
        client_agents=("Meilisearch Package1 (v1.1.1)", "Meilisearch Package2 (v2.2.2)"),
    )
    http = HttpRequests(config=config)

    assert http.headers["Authorization"] == f"Bearer {MASTER_KEY}"
    assert (
        http.headers["User-Agent"]
        == qualified_version() + ";Meilisearch Package1 (v1.1.1);Meilisearch Package2 (v2.2.2)"
    )


def test_reset_content_type_header():
    """Tests that the content type header is reset when no content type is provided."""
    config = Config(BASE_URL, MASTER_KEY, timeout=None)
    http = HttpRequests(config=config)

    http.headers["Content-Type"] = "application/json"
    assert http.headers["Content-Type"] == "application/json"

    http.send_request(http_method=requests.get, path="health")

    assert "Content-Type" not in http.headers


@pytest.mark.parametrize(
    "setting", ["searchable_attributes", "displayed_attributes", "ranking_rules"]
)
def test_empty_list_setting_is_not_reset(client, empty_index, setting):
    """An empty list configures a setting; None still resets its server default."""
    index = empty_index()
    update = getattr(index, f"update_{setting}")
    read = getattr(index, f"get_{setting}")
    default = read()
    assert default

    task = update([])
    client.wait_for_task(task.task_uid)
    assert read() == []

    task = update(None)
    client.wait_for_task(task.task_uid)
    assert read() == default


@pytest.mark.parametrize(
    ("body", "expected"),
    [([], "[]"), ({}, "{}"), (0, "0"), (False, "false"), (None, "null"), ("", ""), (b"[]", b"[]")],
)
def test_falsey_request_bodies_keep_their_wire_value(monkeypatch, body, expected):
    """Falsey JSON values must not be confused with a reset body."""
    captured = []

    def post(url, **kwargs):
        captured.append(kwargs["data"])
        response = requests.Response()
        response.status_code = 200
        response._content = b"{}"
        return response

    with monkeypatch.context() as patch:
        patch.setattr(requests, "post", post)
        http = HttpRequests(Config(BASE_URL, MASTER_KEY, timeout=None))
        http.post("example", body)

    assert captured == [expected]
