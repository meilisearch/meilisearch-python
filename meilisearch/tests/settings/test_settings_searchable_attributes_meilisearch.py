
class TestSearchableAttributes:

    """ TESTS: searchableAttributes setting """

    new_searchable_attributes = ['something', 'random']
    full_searchable_attributes = ['id', 'title', 'poster', 'overview', 'release_date']

    def test_get_searchable_attributes(self, sample_indexes, small_movies):
        """Tests getting the searchable attributes on an empty and populated index"""
        response = sample_indexes[0].get_searchable_attributes()
        assert isinstance(response, object)
        assert response == ['*']
        response = sample_indexes[0].add_documents(small_movies, primary_key='id')
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        get_attributes = sample_indexes[0].get_searchable_attributes()
        assert get_attributes == ['*']


    def test_update_searchable_attributes(self, sample_indexes):
        """Tests updating the searchable attributes"""
        response = sample_indexes[0].update_searchable_attributes(self.new_searchable_attributes)
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        response = sample_indexes[0].get_searchable_attributes()
        assert len(response) == len(self.new_searchable_attributes)
        for attribute in self.new_searchable_attributes:
            assert attribute in response

    def test_reset_searchable_attributes(self, sample_indexes):
        """Tests reseting searchable attributes"""
        response = sample_indexes[0].reset_searchable_attributes()
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        response = sample_indexes[0].get_searchable_attributes()
        assert response == ['*']
