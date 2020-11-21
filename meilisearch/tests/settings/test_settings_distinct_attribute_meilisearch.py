
class TestDistinctAttribute:

    """ TESTS: distinctAttribute setting """

    new_distinct_attribute = 'title'
    default_distinct_attribute = None

    def test_get_distinct_attribute(self, sample_indexes):
        """Tests geting the distinct attributes"""
        response = sample_indexes[0].get_distinct_attribute()
        assert isinstance(response, object)
        assert response == self.default_distinct_attribute

    def test_update_distinct_attribute(self, sample_indexes):
        """Tests creating a custom distinct attribute and checks it has been set correctly"""
        response = sample_indexes[0].update_distinct_attribute(self.new_distinct_attribute)
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        response = sample_indexes[0].get_distinct_attribute()
        assert isinstance(response, object)
        assert response == self.new_distinct_attribute

    def test_reset_distinct_attribute(self, sample_indexes):
        """Tests resetting distinct attribute"""
        response = sample_indexes[0].reset_distinct_attribute()
        assert isinstance(response, object)
        assert 'updateId' in response
        sample_indexes[0].wait_for_pending_update(response['updateId'])
        response = sample_indexes[0].get_distinct_attribute()
        assert response == self.default_distinct_attribute
