import json
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSearchableAttributes:

    """ TESTS: searchableAttributes setting """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    dataset_file = None
    dataset_json = None
    new_searchable_attributes = ['something', 'random']
    full_searchable_attributes = ['id', 'title', 'poster', 'overview', 'release_date']

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')
        self.dataset_file = open('./datasets/small_movies.json', 'r')
        self.dataset_json = json.loads(self.dataset_file.read())
        self.dataset_file.close()

    def teardown_class(self):
        self.index.delete()

    def test_get_searchable_attributes(self):
        """Tests getting the searchable attributes on an empty and populated index"""
        response = self.index.get_searchable_attributes()
        assert isinstance(response, object)
        assert response == ['*']
        response = self.index.add_documents(self.dataset_json, primary_key='id')
        self.index.wait_for_pending_update(response['updateId'])
        get_attributes = self.index.get_searchable_attributes()
        assert get_attributes == ['*']


    def test_update_searchable_attributes(self):
        """Tests updating the searchable attributes"""
        response = self.index.update_searchable_attributes(self.new_searchable_attributes)
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        response = self.index.get_searchable_attributes()
        assert len(response) == len(self.new_searchable_attributes)
        for attribute in self.new_searchable_attributes:
            assert attribute in response

    def test_reset_searchable_attributes(self):
        """Tests reseting searchable attributes"""
        response = self.index.reset_searchable_attributes()
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        response = self.index.get_searchable_attributes()
        assert response == ['*']
