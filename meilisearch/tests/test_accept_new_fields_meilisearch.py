import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestAcceptNewFields:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = client.create_index(uid='indexUID')
    new_accept_new_fields = True

    def teardown_class(self):
        self.index.delete()

    def test_update_accept_new_fields(self):
        response = self.index.update_accept_new_fields(self.new_accept_new_fields)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_accept_new_fields(self):
        response = self.index.get_accept_new_fields()
        assert isinstance(response, object)
        assert response == self.new_accept_new_fields
