import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestVersion:
    """ TESTS: version route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        clear_all_indexes(self.client)
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_version(self):
        """Tests getting the version of the MeiliSearch instance"""
        response = self.client.get_version()
        assert 'pkgVersion' in response
        assert 'commitSha' in response
        assert 'buildDate' in response
