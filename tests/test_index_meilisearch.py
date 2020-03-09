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

class TestIndexe:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ index route """
    @pytest.mark.run(order=1)
    def test_create_index(self):
        """Tests an API call to create an index in MeiliSearch"""
        index = self.client.create_index(name="movies", uid="movies_uid")
        # TODO : test creating index with schema
        assert isinstance(index, object)
        assert index.name == "movies"
        assert index.uid == "movies_uid"

    def test_get_indexes(self):
        """Tests an API call to get all indexes in MeiliSearch"""
        response = self.client.get_indexes()
        assert isinstance(response, list)

    def test_get_index_with_name(self):
        """Tests an API call to get one index with name in MeiliSearch"""
        response = self.client.get_index(name="movies")
        assert isinstance(response, object)

    def test_get_index_with_uid(self):
        """Tests an API call to get one index with uid in MeiliSearch"""
        response = self.client.get_index(uid="movies_uid")
        assert isinstance(response, object)

    def test_index_info(self):
        """Tests an API call to get an index's info in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.info()
        assert isinstance(response, object)

    def test_update_index(self):
        """Tests an API call to update an index in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.update(name="movie")
        assert isinstance(response, object)

    """  schema route """
    def test_update_schema(self):
        """Tests an API call to update an schema in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.update_schema({
            'id': ['indexed','displayed','identifier'],
            'title':['displayed','indexed'],
            'poster':['displayed','indexed'],
            'overview':['indexed','displayed'],
            'release_date':['indexed','displayed']
        })
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_update_existing_schema(self):
        """Tests an API call to update an already existing schema in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.update_schema({
            'id': ['indexed','displayed','identifier'],
            'title':['displayed','indexed'],
            'poster':['displayed','indexed'],
            'overview':['indexed','displayed'],
            'release_date':['indexed','displayed', 'ranked']
        })
        assert isinstance(response, object)
        assert 'updateId' in response

    @pytest.mark.run(order=-1)
    def test_delete_index(self):
        """Tests an API call to delete an index in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.delete()
        assert isinstance(response, object)
        assert response.status_code == 204
