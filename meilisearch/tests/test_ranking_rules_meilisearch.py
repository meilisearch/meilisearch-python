import time
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestRankingRules:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_ranking_rules = ['typo', 'exactness']
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

    def test_update_ranking_rules(self):
        response = self.index.update_ranking_rules(self.new_ranking_rules)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_ranking_rules(self):
        response = self.index.get_ranking_rules()
        assert isinstance(response, object)
        assert response == self.new_ranking_rules

    def test_reset_ranking_rules(self):
        response = self.index.reset_ranking_rules()
        assert isinstance(response, object)
        assert 'updateId' in response
        time.sleep(0.1)
        response = self.index.get_ranking_rules()
        assert response == self.default_ranking_rules
