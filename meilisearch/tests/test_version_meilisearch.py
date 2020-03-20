import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestVersion:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    """ version route """
    def test_get_version(self):
        """Tests an API call to get the version of MeiliSearch"""
        response = self.client.get_version()
        assert 'pkgVersion' in response
        assert 'commitSha' in response
        assert 'buildDate' in response
