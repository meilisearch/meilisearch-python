import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSearchableAttributes:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_displayed_attributes = ['title']

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_update_displayed_attributes(self):
        response = self.index.update_displayed_attributes(self.new_displayed_attributes)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_displayed_attributes(self):
        response = self.index.get_displayed_attributes()
        assert isinstance(response, object)
        assert response == self.new_displayed_attributes

    def test_reset_displayed_attributes(self):
        response = self.index.reset_displayed_attributes()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(0.1)
        response = self.index.get_displayed_attributes()
        assert isinstance(response, list)
