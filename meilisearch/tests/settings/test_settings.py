
class TestSetting:

    """ TESTS: all settings route """

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

    def test_get_settings_default(self, sample_indexes):
        """Tests getting all settings by default"""
        response = sample_indexes[0].get_settings()
        assert isinstance(response, object)
        for rule in self.default_ranking_rules:
            assert rule in response['rankingRules']
        assert response['distinctAttribute'] is None
        assert response['searchableAttributes'] == ['*']
        assert response['displayedAttributes'] == ['*']
        assert response['stopWords'] == []
        assert response['synonyms'] == {}

    def test_update_settings(self, sample_indexes):
        """Tests updating some settings"""
        response = sample_indexes[0].update_settings(self.new_settings)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = sample_indexes[0].get_settings()
        for rule in self.new_settings['rankingRules']:
            assert rule in response['rankingRules']
        assert response['distinctAttribute'] is None
        for attribute in self.new_settings['searchableAttributes']:
            assert attribute in response['searchableAttributes']
        assert response['displayedAttributes'] == ['*']
        assert response['stopWords'] == []
        assert response['synonyms'] == {}

    def test_reset_settings(self, sample_indexes):
        """Tests resetting default settings"""
        response = sample_indexes[0].reset_settings()
        assert isinstance(response, object)
        assert 'updateId' in response
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = sample_indexes[0].get_settings()
        for rule in self.default_ranking_rules:
            assert rule in response['rankingRules']
        assert response['distinctAttribute'] is None
        assert response['displayedAttributes'] == ['*']
        assert response['searchableAttributes'] == ['*']
        assert response['stopWords'] == []
        assert response['synonyms'] == {}
