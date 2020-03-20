import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSetting:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_settings = {
        'rankingRules': ['typo'],
        'searchableAttributes': ['title']
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

    def test_update_settings(self):
        response = self.index.update_settings(self.new_settings)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_settings(self):
        response = self.index.get_settings()
        assert isinstance(response, object)
        assert response['rankingRules'] == self.new_settings['rankingRules']
        assert response['distinctAttribute'] is None
        assert response['searchableAttributes'] == self.new_settings['searchableAttributes']
        assert response['displayedAttributes'] == []
        assert response['stopWords'] == []
        assert response['synonyms'] == {}
        assert response['acceptNewFields'] is True

    def test_reset_settings(self):
        response = self.index.reset_settings()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(0.1)
        response = self.index.get_settings()
        assert response['rankingRules'] == self.default_ranking_rules
        assert response['distinctAttribute'] is None
        assert isinstance(response['searchableAttributes'], list)
        assert isinstance(response['displayedAttributes'], list)
        assert response['stopWords'] == []
        assert response['synonyms'] == {}
        assert response['acceptNewFields'] is True
