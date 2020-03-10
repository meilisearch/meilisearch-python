import meilisearch

class TestUpdates:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ sys-info route """
    def test_get_sys_info(self):
        """Tests an API call to check the system information of MeiliSearch"""
        response = self.client.get_sys_info()
        assert 'memoryUsage' in response
