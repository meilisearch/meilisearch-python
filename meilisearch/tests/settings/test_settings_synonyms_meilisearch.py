
class TestSynonyms:

    """ TESTS: synonyms setting """

    new_synonyms = {
        'hp': ['harry potter']
    }

    def test_get_synonyms_default(self, sample_indexes):
        """Tests getting default synonyms"""
        response = sample_indexes[0].get_synonyms()
        assert isinstance(response, object)
        assert response == {}

    def test_update_synonyms(self, sample_indexes):
        """Tests updating synonyms"""
        response = sample_indexes[0].update_synonyms(self.new_synonyms)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = sample_indexes[0].get_synonyms()
        assert isinstance(response, object)
        for synonym in self.new_synonyms:
            assert synonym in response

    def test_reset_synonyms(self, sample_indexes):
        """Tests resetting synonyms"""
        response = sample_indexes[0].reset_synonyms()
        assert isinstance(response, object)
        assert 'updateId' in response
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = sample_indexes[0].get_synonyms()
        assert response == {}
