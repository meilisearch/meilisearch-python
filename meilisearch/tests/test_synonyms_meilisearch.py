import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSynonyms:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_synonyms = {
        'hp': ['harry potter']
    }
    default_synonyms = {}

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_update_synonyms(self):
        response = self.index.update_synonyms(self.new_synonyms)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_synonyms(self):
        response = self.index.get_synonyms()
        assert isinstance(response, object)
        assert response == self.new_synonyms

    def test_reset_synonyms(self):
        response = self.index.reset_synonyms()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(2)
        response = self.index.get_synonyms()
        assert response == self.default_synonyms
