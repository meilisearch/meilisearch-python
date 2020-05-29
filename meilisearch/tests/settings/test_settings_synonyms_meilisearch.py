import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSynonyms:

    """ TESTS: synonyms setting """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_synonyms = {
        'hp': ['harry potter']
    }

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_synonyms_default(self):
        """Tests getting default synonyms"""
        response = self.index.get_synonyms()
        assert isinstance(response, object)
        assert response == {}

    def test_update_synonyms(self):
        """Tests updating synonyms"""
        response = self.index.update_synonyms(self.new_synonyms)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_synonyms()
        assert isinstance(response, object)
        for synonym in self.new_synonyms:
            assert synonym in response

    def test_reset_synonyms(self):
        """Tests resetting synonyms"""
        response = self.index.reset_synonyms()
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_synonyms()
        assert response == {}
