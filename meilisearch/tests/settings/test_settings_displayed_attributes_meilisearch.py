
class TestDisplayedAttributes:

    """ TESTS: displayedAttributes setting """

    displayed_attributes = ['id', 'release_date', 'title', 'poster', 'overview', 'genre']

    def test_get_displayed_attributes(self, sample_indexes, small_movies):
        """ Tests getting the displayed attributes before and after indexing a dataset """
        response = sample_indexes[0].get_displayed_attributes()
        assert isinstance(response, object)
        assert response == ['*']
        response = sample_indexes[0].add_documents(small_movies, primary_key='id')
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        get_attributes = sample_indexes[0].get_displayed_attributes()
        assert get_attributes == ['*']

    def test_update_displayed_attributes(self, sample_indexes):
        """Tests updating the displayed attributes"""
        response = sample_indexes[0].update_displayed_attributes(self.displayed_attributes)
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        get_attributes_new = sample_indexes[0].get_displayed_attributes()
        assert len(get_attributes_new) == len(self.displayed_attributes)
        for attribute in self.displayed_attributes:
            assert attribute in get_attributes_new

    def test_reset_displayed_attributes(self, sample_indexes):
        """Tests the reset of displayedAttributes to default values (in dataset)"""
        response = sample_indexes[0].reset_displayed_attributes()
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        get_attributes = sample_indexes[0].get_displayed_attributes()
        assert get_attributes == ['*']
