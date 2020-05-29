import json
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSearch:

    """ TESTS: search route """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    dataset_file = None
    dataset_json = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')
        self.dataset_file = open("./datasets/small_movies.json", "r")
        self.dataset_json = json.loads(self.dataset_file.read())
        self.dataset_file.close()
        response = self.index.add_documents(self.dataset_json, primary_key='id')
        self.index.wait_for_pending_update(response['updateId'])

    def teardown_class(self):
        self.index.delete()

    def test_basic_search_empty_query(self):
        """Tests search with an empty query"""
        response = self.index.search('')
        assert len(response['hits']) == 0

    def test_basic_search(self):
        """Tests search with an simple query"""
        response = self.index.search('How to Train Your Dragon')
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'

    def test_basic_search_with_empty_params(self):
        """Tests search with an simple query and empty params"""
        response = self.index.search('How to Train Your Dragon', {})
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'
        assert '_formatted' not in response['hits'][0]

    def test_custom_search(self):
        """Tests search with an simple query and custom parameter (attributesToHighlight)"""
        response = self.index.search(
            'Dragon',
            {
                'attributesToHighlight': 'title'
            }
        )
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'
        assert '_formatted' in response['hits'][0]
        assert 'dragon' in response['hits'][0]['_formatted']['title'].lower()

    def test_basic_search_params_with_wildcard(self):
        """Tests search with '*' in query params"""
        response = self.index.search(
            'a',
            {
                'limit': 5,
                'attributesToHighlight': '*',
                'attributesToRetrieve': '*',
                'attributesToCrop': '*',
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 5
        assert '_formatted' in response['hits'][0]
        assert "title" in response['hits'][0]['_formatted']

    def test_basic_search_params_with_simple_string(self):
        """Tests search with simple string in query params"""
        response = self.index.search(
            'a',
            {
                'limit': 5,
                'attributesToHighlight': 'title',
                'attributesToRetrieve': 'title',
                'attributesToCrop': 'title',
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 5
        assert '_formatted' in response['hits'][0]
        assert "title" in response['hits'][0]['_formatted']
        assert not "release_date" in response['hits'][0]['_formatted']

    # Add def test_basic_search_params_with_string_list(self):
    # when bug (issue #85) is fixed
