import json
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestAttributesForFaceting:

    """ TESTS: attributesForFaceting setting """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    attributes_for_faceting = ['title', 'release_date']
    dataset_file = None
    dataset_json = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')
        self.dataset_file = open('./datasets/small_movies.json', 'r')
        self.dataset_json = json.loads(self.dataset_file.read())
        self.dataset_file.close()

    def teardown_class(self):
        self.index.delete()

    def test_get_attributes_for_faceting(self):
        """ Tests getting the attributes for faceting """
        response = self.index.get_attributes_for_faceting()
        assert isinstance(response, object)
        assert response == []

    def test_update_attributes_for_faceting(self):
        """Tests updating the attributes for faceting"""
        response = self.index.update_attributes_for_faceting(self.attributes_for_faceting)
        self.index.wait_for_pending_update(response['updateId'])
        get_attributes_new = self.index.get_attributes_for_faceting()
        assert len(get_attributes_new) == len(self.attributes_for_faceting)
        get_attributes = self.index.get_attributes_for_faceting()
        for attribute in self.attributes_for_faceting:
            assert attribute in get_attributes

    def test_reset_attributes_for_faceting(self):
        """Tests the reset of attributes for faceting to default values (in dataset)"""
        response = self.index.reset_attributes_for_faceting()
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        response = self.index.get_attributes_for_faceting()
        assert isinstance(response, object)
        assert response == []
