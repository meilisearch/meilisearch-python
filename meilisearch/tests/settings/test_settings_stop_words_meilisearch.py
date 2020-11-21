
class TestStopWords:

    """ TESTS: stop words setting """

    new_stop_words = ['of', 'the']

    def test_get_stop_words_default(self, sample_indexes):
        """Tests call to get stop words by default"""
        response = sample_indexes[0].get_stop_words()
        assert isinstance(response, object)
        assert response == []

    def test_update_stop_words(self, sample_indexes):
        """Tests call to modify stop words"""
        response = sample_indexes[0].update_stop_words(self.new_stop_words)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = sample_indexes[0].get_stop_words()
        assert isinstance(response, object)
        for stop_word in self.new_stop_words:
            assert stop_word in response

    def test_reset_stop_words(self, sample_indexes):
        """Tests call to reset stop words"""
        response = sample_indexes[0].reset_stop_words()
        assert isinstance(response, object)
        assert 'updateId' in response
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = sample_indexes[0].get_stop_words()
        assert response == []
