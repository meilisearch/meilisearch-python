import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestStats:

    """ TESTS: stats route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        clear_all_indexes(self.client)
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_stats(self):
        """Tests getting stats of a single index"""
        response = self.index.get_stats()
        assert isinstance(response, object)
        assert 'numberOfDocuments' in response
        assert response['numberOfDocuments'] == 0
        assert 'isIndexing' in response
