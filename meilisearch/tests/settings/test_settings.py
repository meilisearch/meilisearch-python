import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSetting:

    """ TESTS: all settings route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_settings = {
        'rankingRules': ['typo', 'words'],
        'searchableAttributes': ['title', 'overview']
    }
    default_ranking_rules = [
        'typo',
        'words',
        'proximity',
        'attribute',
        'wordsPosition',
        'exactness'
    ]

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_settings_default(self):
        """Tests getting all settings by default"""
        response = self.index.get_settings()
        assert isinstance(response, object)
        for rule in self.default_ranking_rules:
            assert rule in response['rankingRules']
        assert response['distinctAttribute'] is None
        assert response['searchableAttributes'] == ['*']
        assert response['displayedAttributes'] == ['*']
        assert response['stopWords'] == []
        assert response['synonyms'] == {}

    def test_update_settings(self):
        """Tests updating some settings"""
        response = self.index.update_settings(self.new_settings)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_settings()
        for rule in self.new_settings['rankingRules']:
            assert rule in response['rankingRules']
        assert response['distinctAttribute'] is None
        for attribute in self.new_settings['searchableAttributes']:
            assert attribute in response['searchableAttributes']
        assert response['displayedAttributes'] == ['*']
        assert response['stopWords'] == []
        assert response['synonyms'] == {}

    def test_reset_settings(self):
        """Tests resetting default settings"""
        response = self.index.reset_settings()
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_settings()
        for rule in self.default_ranking_rules:
            assert rule in response['rankingRules']
        assert response['distinctAttribute'] is None
        assert response['displayedAttributes'] == ['*']
        assert response['searchableAttributes'] == ['*']
        assert response['stopWords'] == []
        assert response['synonyms'] == {}
