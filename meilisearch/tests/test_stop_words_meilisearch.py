import meilisearch

class TestUpdates:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ stop-words route """
    def test_add_stop_words(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.add_stop_words(['the', 'and'])
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_stop_words(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_stop_words()
        assert isinstance(response, list)

    def test_delete_stop_words(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_stop_words(['the'])
        assert isinstance(response, object)
        assert 'updateId' in response
