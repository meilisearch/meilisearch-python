import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestStat:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_all_stats(self):
        response = self.client.get_all_stats()
        assert isinstance(response, object)
        assert 'databaseSize' in response

    def test_get_stats(self):
        response = self.index.get_stats()
        assert isinstance(response, object)
        assert 'numberOfDocuments' in response
        assert response['numberOfDocuments'] == 0
