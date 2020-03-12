import meilisearch

class TestKey:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ key route """
    def test_create_key(self):
        response = self.client.create_key({
            "expiresAt": 1575985008,
            "description": "search key",
            "acl": ["documentsRead"],
            "indexes": ["movies"]
        })
        assert 'key' in response
        assert response['description'] == "search key"

    def test_get_keys(self):
        response = self.client.get_keys()
        assert isinstance(response, list)
        assert response[0]['description'] == "search key"

    def test_update_key(self):
        keys = self.client.get_keys()
        response = self.client.update_key(keys[0]["key"], {
            "description": "search key updated",
            "acl": ["documentsRead"],
            "indexes": ["movies"]
        })
        assert 'key' in response
        assert response['description'] == "search key updated"

    def test_get_key(self):
        keys = self.client.get_keys()
        response = self.client.get_key(keys[0]["key"])
        assert isinstance(response, object)
        assert keys[0]['description'] == "search key updated"

    def test_delete_key(self):
        keys = self.client.get_keys()
        response = self.client.delete_key(keys[0]["key"])
        assert response.status_code == 204
