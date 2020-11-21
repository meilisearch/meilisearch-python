class TestRankingRules:

    """ TESTS: ranking rules route """

    new_ranking_rules = ['typo', 'exactness']
    default_ranking_rules = [
        'typo',
        'words',
        'proximity',
        'attribute',
        'wordsPosition',
        'exactness'
    ]

    def test_get_ranking_rules_default(self, sample_indexes):
        """Tests getting the default ranking rules"""
        response = sample_indexes[0].get_ranking_rules()
        assert isinstance(response, object)
        for rule in self.default_ranking_rules:
            assert rule in response

    def test_update_ranking_rules(self, sample_indexes):
        """Tests changing the ranking rules"""
        response = sample_indexes[0].update_ranking_rules(self.new_ranking_rules)
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        response = sample_indexes[0].get_ranking_rules()
        assert isinstance(response, object)
        for rule in self.new_ranking_rules:
            assert rule in response

    def test_reset_ranking_rules(self, sample_indexes):
        """Tests resetting the ranking rules"""
        response = sample_indexes[0].reset_ranking_rules()
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        response = sample_indexes[0].get_ranking_rules()
        for rule in self.default_ranking_rules:
            assert rule in response
