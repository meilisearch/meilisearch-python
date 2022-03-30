
import meilisearch
from tests import BASE_URL, MASTER_KEY

from meilisearch.config import Config
from meilisearch._httprequests import HttpRequests
from meilisearch.version import qualified_version

def test_get_headers_from_http_requests_instance():
    """Tests getting defined headers from instance in HttpRequests."""
    config = Config(BASE_URL, MASTER_KEY, timeout=None)
    http = HttpRequests(config=config)

    assert http.headers['Authorization'] == f"Bearer {MASTER_KEY}"
    assert http.headers['User-Agent'] == qualified_version()
