import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestAcceptNewFields:

    """ TESTS: acceptNewFields setting """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    new_accept_new_fields = True

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_get_accept_new_fields(self):
        """ Test the default behaviour of getting acceptNewFields setting """
        response = self.index.get_accept_new_fields()
        assert isinstance(response, object)
        assert response == self.new_accept_new_fields

    def test_update_accept_new_fields(self):
        """ Test changing the acceptNewFields value """
        response = self.index.update_accept_new_fields(not self.new_accept_new_fields)
        assert isinstance(response, object)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_accept_new_fields()
        assert response == (not self.new_accept_new_fields)
