import meilisearch

class TestUpdates:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ updates route """
    def test_get_updates(self):
        """Tests a call to get updates of a given index"""
        index = self.client.get_index(uid="movies_uid")
        response = index.get_updates()
        assert isinstance(response, list)
        assert 'status' in response[0]

    def test_get_update(self):
        """Tests a call to get an update of a given operation"""
        index = self.client.get_index(uid="movies_uid")
        response = index.get_update(0)
        assert isinstance(response, object)
        assert 'status' in response
        assert response['status'] == 'processed'
