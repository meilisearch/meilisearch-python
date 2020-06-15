import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestSysInfo:

    """ TESTS: sysinfo route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        clear_all_indexes(self.client)
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_sys_info(self):
        """Tests getting the system information of the MeiliSearch instance"""
        response = self.client.get_sys_info()
        assert 'memoryUsage' in response
        assert 'processorUsage' in response
        assert 'global' in response
        assert 'process' in response
