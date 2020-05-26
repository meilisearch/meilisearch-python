import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestStopWords:

    """ TESTS: stop words setting """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_stop_words = ['of', 'the']

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_stop_words_default(self):
        """Tests call to get stop words by default"""
        response = self.index.get_stop_words()
        assert isinstance(response, object)
        assert response == []

    def test_update_stop_words(self):
        """Tests call to modify stop words"""
        response = self.index.update_stop_words(self.new_stop_words)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_stop_words()
        assert isinstance(response, object)
        for stop_word in self.new_stop_words:
            assert stop_word in response

    def test_reset_stop_words(self):
        """Tests call to reset stop words"""
        response = self.index.reset_stop_words()
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_stop_words()
        assert response == []
