import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestUpdate:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')
        self.index.add_documents([{'id': 1, 'title': 'Le Petit Prince'}])
        time.sleep(0.1)

    def teardown_class(self):
        self.index.delete()

    def test_get_all_update_status(self):
        """Tests a call to get updates of a given index"""
        response = self.index.get_all_update_status()
        assert isinstance(response, list)
        assert 'status' in response[0]

    def test_get_update(self):
        """Tests a call to get an update of a given operation"""
        response = self.index.get_update_status(0)
        assert isinstance(response, object)
        assert 'status' in response
        assert response['status'] == 'processed'
