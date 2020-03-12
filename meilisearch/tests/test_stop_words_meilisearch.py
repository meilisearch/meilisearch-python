import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestStopWords:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_stop_words = ['of', 'the']
    default_stop_words = []

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_update_stop_words(self):
        response = self.index.update_stop_words(self.new_stop_words)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_stop_words(self):
        response = self.index.get_stop_words()
        assert isinstance(response, object)
        assert response == self.new_stop_words

    def test_reset_stop_words(self):
        response = self.index.reset_stop_words()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(0.1)
        response = self.index.get_stop_words()
        assert response == self.default_stop_words
