import json
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestDisplayedAttributes:

    """ TESTS: displayedAttributes setting """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    displayed_attributes = ['id', 'release_date', 'title', 'poster', 'overview', 'genre']
    dataset_file = None
    dataset_json = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')
        self.dataset_file = open('./datasets/small_movies.json', 'r')
        self.dataset_json = json.loads(self.dataset_file.read())
        self.dataset_file.close()

    def teardown_class(self):
        self.index.delete()

    def test_get_displayed_attributes(self):
        """ Tests getting the displayed attributes before and after indexing a dataset """
        response = self.index.get_displayed_attributes()
        assert isinstance(response, object)
        assert response == ['*']
        response = self.index.add_documents(self.dataset_json, primary_key='id')
        self.index.wait_for_pending_update(response['updateId'])
        get_attributes = self.index.get_displayed_attributes()
        assert get_attributes == ['*']

    def test_update_displayed_attributes(self):
        """Tests updating the displayed attributes"""
        response = self.index.update_displayed_attributes(self.displayed_attributes)
        self.index.wait_for_pending_update(response['updateId'])
        get_attributes_new = self.index.get_displayed_attributes()
        assert len(get_attributes_new) == len(self.displayed_attributes)
        for attribute in self.displayed_attributes:
            assert attribute in get_attributes_new

    def test_reset_displayed_attributes(self):
        """Tests the reset of displayedAttributes to default values (in dataset)"""
        response = self.index.reset_displayed_attributes()
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        get_attributes = self.index.get_displayed_attributes()
        assert get_attributes == ['*']
