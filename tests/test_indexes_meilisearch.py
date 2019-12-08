import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import meilisearch
import pytest
import json

class TestIndexes: 
    client = meilisearch.Client("http://127.0.0.1:7700", None)

    # @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    # @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_create_index(self):
        """Tests an API call to create an in meiliSearch""" 
        index = self.client.create_index(name="movies",uid="movies_uid")
        print(index)
        assert isinstance(index, object)
        assert index.name == "movies"
        assert index.uid == "movies_uid"

    def test_get_all_indexes(self):
        """Tests an API call to get all indexes in meiliSearch"""
        response = self.client.get_all_indexes()
        assert isinstance(response, list)
    
    def test_get_index_with_name(self):
        """Tests an API call to get one index with name in meiliSearch"""
        response = self.client.get_index(name="movies")
        assert isinstance(response, object)
    
    def test_get_index_with_uid(self):
        """Tests an API call to get one index with uid in meiliSearch"""
        response = self.client.get_index(uid="movies_uid")
        assert isinstance(response, object)
    
    def test_index_info(self):
        """Tests an API call to get an index's info in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.info()
        print('resp', response)
        assert isinstance(response, object)

    def test_update_index(self):
        """Tests an API call to update an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.update(name="movie")
        assert isinstance(response, object)

    def test_update_schema(self):
        """Tests an API call to update an schema in meiliSearch"""
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
        """Tests an API call to update an already existing schema in meiliSearch"""
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
    
    def test_get_updates(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_updates()
        assert isinstance(response, list)
        assert 'status' in response[0]
    
    def test_get_one_update(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_one_update(0)
        assert isinstance(response, object)
        assert 'status' in response
        assert response['status'] == 'processed'

    def test_add_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        index = self.client.get_index(uid="movies_uid")
        response = index.add_documents(data);
        assert isinstance(response, object)
        assert 'updateId' in response


    def test_get_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_documents()
        assert isinstance(response, list)

    # DIfference between two routes ?
    def test_update_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        index = self.client.get_index(uid="movies_uid")
        response = index.update_documents([data[0]]);
        assert isinstance(response, object)
        assert 'updateId' in response

    # Captain Marvel
    def test_delete_one_document(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_one_document(299537);
        assert isinstance(response, object)
        assert 'updateId' in response

    # Escape Room, 522681
    # Glass, 450465
    # Dumbo, 329996 
    def test_delete_multiple_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_multiple_documents([522681, 450465, 329996]);
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_all_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_all_documents();
        assert isinstance(response, object)
        assert 'updateId' in response
    
    def test_delete_index(self):
        """Tests an API call to delete an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.delete()
        assert isinstance(response, object)
