import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSearchableAttributes:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_searchable_attributes = ['title']

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_update_searchable_attributes(self):
        response = self.index.update_searchable_attributes(self.new_searchable_attributes)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_searchable_attributes(self):
        response = self.index.get_searchable_attributes()
        assert isinstance(response, object)
        assert response == self.new_searchable_attributes

    def test_reset_searchable_attributes(self):
        response = self.index.reset_searchable_attributes()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(0.1)
        response = self.index.get_searchable_attributes()
        assert isinstance(response, list)
