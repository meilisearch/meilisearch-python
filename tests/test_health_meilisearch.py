import os
import sys
import inspect
import meilisearch

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

class TestHealth:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ health route """
    def test_health(self):
        """Tests an API call to check the health of MeiliSearch"""
        response = self.client.health()
        assert response.status_code == 204
