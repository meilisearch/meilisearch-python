import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestHealth:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    """ health route """
    def test_health(self):
        """Tests an API call to check the health of MeiliSearch"""
        response = self.client.health()
        assert response.status_code == 200
