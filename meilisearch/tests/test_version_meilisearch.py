import meilisearch

class TestUpdates:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ version route """
    def test_get_version(self):
        """Tests an API call to get the version of MeiliSearch"""
        response = self.client.get_version()
        assert 'pkgVersion' in response
