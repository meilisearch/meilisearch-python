import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestStats:

    """ TESTS: client stats route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    index2 = None

    def setup_class(self):
        clear_all_indexes(self.client)
        self.index = self.client.create_index(uid='indexUID')
        self.index_2 = self.client.create_index(uid='indexUID2')

    def teardown_class(self):
        self.index.delete()
        self.index_2.delete()

    def test_get_all_stats(self):
        """Tests getting all stats after creating two indexes"""
        response = self.client.get_all_stats()
        assert isinstance(response, object)
        assert 'databaseSize' in response
        assert isinstance(response['databaseSize'], int)
        assert 'lastUpdate' in response
        assert 'indexes' in response
        assert 'indexUID' in response['indexes']
        assert 'indexUID2' in response['indexes']
