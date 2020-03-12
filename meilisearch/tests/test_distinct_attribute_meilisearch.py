import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestDistinctAttribute:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_distinct_attribute = 'title'
    default_distinct_attribute = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_update_distinct_attribute(self):
        response = self.index.update_distinct_attribute(self.new_distinct_attribute)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_distinct_attribute(self):
        response = self.index.get_distinct_attribute()
        assert isinstance(response, object)
        assert response == self.new_distinct_attribute

    def test_reset_distinct_attribute(self):
        response = self.index.reset_distinct_attribute()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(0.1)
        response = self.index.get_distinct_attribute()
        assert response == self.default_distinct_attribute
