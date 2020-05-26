import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestHealth:

    """ TESTS: health route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    def test_health(self):
        """Tests checking the health of MeiliSearch instance"""
        response = self.client.health()
        assert response.status_code == 200
