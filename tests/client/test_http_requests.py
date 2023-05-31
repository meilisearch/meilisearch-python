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
        client_agents=["Meilisearch Package1 (v1.1.1)", "Meilisearch Package2 (v2.2.2)"],
    )
    http = HttpRequests(config=config)

    assert http.headers["Authorization"] == f"Bearer {MASTER_KEY}"
    assert (
        http.headers["User-Agent"]
        == qualified_version() + ";Meilisearch Package1 (v1.1.1);Meilisearch Package2 (v2.2.2)"
    )
