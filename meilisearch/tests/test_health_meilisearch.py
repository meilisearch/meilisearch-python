import os
import sys
import inspect
import meilisearch

CURRENT_DIR = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
sys.path.insert(0, PARENT_DIR)

class TestHealth:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ health route """
    def test_health(self):
        """Tests an API call to check the health of MeiliSearch"""
        response = self.client.health()
        assert response.status_code == 204
