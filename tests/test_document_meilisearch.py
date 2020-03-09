import os
import sys
import time
import json
import pytest
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import meilisearch

class TestUpdates:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    def test_add_documents(self):
        """Tests a call to add documents"""
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        index = self.client.get_index(uid="movies_uid")
        response = index.add_documents(data)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_documents(self):

        index = self.client.get_index(uid="movies_uid")
        time.sleep(1)
        response = index.get_documents({
            'offset': 1,
            'limit': 5,
            'attributesToRetrieve': 'title'
        })
        assert isinstance(response, list)
        assert 'title' in response[0]
        assert 'overview' not in response[0]

    def test_get_document(self):
        time.sleep(1)
        index = self.client.get_index(uid="movies_uid")
        response = index.get_document(500682)
        assert isinstance(response, object)
        assert 'title' in response
        assert response['title'] == "The Highwaymen"


    def test_update_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        index = self.client.get_index(uid="movies_uid")
        response = index.update_documents([data[0]])
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-4)
    def test_delete_document(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_document(299537)
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-3)
    def test_delete_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_documents([522681, 450465, 329996])
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-2)
    def test_delete_all_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_all_documents()
        assert isinstance(response, object)
        assert 'updateId' in response
