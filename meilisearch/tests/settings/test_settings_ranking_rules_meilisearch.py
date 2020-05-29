import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestRankingRules:

    """ TESTS: ranking rules route """

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

    def test_get_ranking_rules_default(self):
        """Tests getting the default ranking rules"""
        response = self.index.get_ranking_rules()
        assert isinstance(response, object)
        for rule in self.default_ranking_rules:
            assert rule in response

    def test_update_ranking_rules(self):
        """Tests changing the ranking rules"""
        response = self.index.update_ranking_rules(self.new_ranking_rules)
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        response = self.index.get_ranking_rules()
        assert isinstance(response, object)
        for rule in self.new_ranking_rules:
            assert rule in response

    def test_reset_ranking_rules(self):
        """Tests resetting the ranking rules"""
        response = self.index.reset_ranking_rules()
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        response = self.index.get_ranking_rules()
        for rule in self.default_ranking_rules:
            assert rule in response
