import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSysInfo:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    """ sys-info route """
    def test_get_sys_info(self):
        """Tests an API call to check the system information of MeiliSearch"""
        response = self.client.get_sys_info()
        assert 'memoryUsage' in response
        assert 'processorUsage' in response
        assert 'global' in response
        assert 'process' in response
