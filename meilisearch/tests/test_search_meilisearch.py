import time
import json
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestSearch:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        self.index.add_documents(data, primary_key='id')
        time.sleep(1)

    def teardown_class(self):
        self.index.delete()

    def test_basic_search(self):
        response = self.index.search('How to Train Your Dragon')
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'

    def test_basic_search_with_empty_params(self):
        response = self.index.search('How to Train Your Dragon', {})
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'
        assert '_formatted' not in response['hits'][0]

    def test_custom_search(self):
        response = self.index.search(
            'How to Train Your Dragon',
            {
                'attributesToHighlight': '*'
            }
        )
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'
        assert '_formatted' in response['hits'][0]
