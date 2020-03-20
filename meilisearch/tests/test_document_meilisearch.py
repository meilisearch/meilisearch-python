import time
import json
import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestDocument:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_add_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        response = self.index.add_documents(data, primary_key='id')
        time.sleep(1)
        assert isinstance(response, object)
        assert 'updateId' in response
        assert self.index.get_primary_key() == 'id'

    def test_get_documents(self):
        response = self.index.get_documents({
            'offset': 1,
            'limit': 5,
            'attributesToRetrieve': 'title'
        })
        assert isinstance(response, list)
        assert 'title' in response[0]
        assert 'overview' not in response[0]

    def test_get_document(self):
        response = self.index.get_document(500682)
        assert isinstance(response, object)
        assert 'title' in response
        assert response['title'] == 'The Highwaymen'

    def test_update_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        response = self.index.update_documents([data[0]])
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-4)
    def test_delete_document(self):
        response = self.index.delete_document(299537)
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-3)
    def test_delete_documents(self):
        response = self.index.delete_documents([522681, 450465, 329996])
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-2)
    def test_delete_all_documents(self):
        response = self.index.delete_all_documents()
        assert isinstance(response, object)
        assert 'updateId' in response
