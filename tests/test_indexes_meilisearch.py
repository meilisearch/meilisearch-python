import json
import time 
import os
import sys
import inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import meilisearch

class TestIndexes: 
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    def test_get_client(self):
        client = meilisearch.Client("http://127.0.0.1:7700", "123")
        assert client.config
    
    def test_health(self):
        """Tests an API call to check the health of meilisearch"""     
        response = self.client.health()
        assert response.status_code == 204

    def test_get_sys_info(self):
        """Tests an API call to check the system information of meilisearch"""
        response = self.client.get_sys_info()
        assert 'memoryUsage' in response

    def test_get_version(self):
        """Tests an API call to get the version of meilisearch"""
        response = self.client.get_version()
        assert 'pkgVersion' in response   

    def test_create_index(self):
        """Tests an API call to create an index in meiliSearch"""
        index = self.client.create_index(name="movies", uid="movies_uid")
        print(index)
        # TODO : test creating index with schema
        assert isinstance(index, object)
        assert index.name == "movies"
        assert index.uid == "movies_uid"

    def test_get_indexes(self):
        """Tests an API call to get all indexes in meiliSearch"""
        response = self.client.get_indexes()
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
    
    def test_get_update(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_update(0)
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

    def test_search_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.search({
            'q': 'How to Train Your Dragon'
        })
        print(response["hits"][0]["id"])
        assert isinstance(response, object)
        assert response["hits"][0]["id"] == '166428'

    def test_create_key(self):
        response = self.client.create_key({
            "expiresAt": 1575985008 ,
            "description": "search key",
            "acl": ["documentsRead"],
            "indexes": ["movies"]
        })
        assert 'key' in response
        assert response['description'] == "search key"
    
    def test_get_keys(self):
        response = self.client.get_keys()
        print(response)
        assert isinstance(response, list)
        assert response[0]['description'] == "search key"

    def test_update_key(self):
        keys = self.client.get_keys()
        response = self.client.update_key(keys[0]["key"], {
            "description": "search key updated",
            "acl": ["documentsRead"],
            "indexes": ["movies"]
        })
        assert 'key' in response
        assert response['description'] == "search key updated"
    
    
    def test_get_key(self):
        keys = self.client.get_keys()
        response = self.client.get_key(keys[0]["key"])
        assert isinstance(response, object)
        assert keys[0]['description'] == "search key updated"

    def test_delete_key(self):
        keys = self.client.get_keys()
        response = self.client.delete_key(keys[0]["key"])
        print(response)
        assert response.status_code == 204

    # DIfference between two routes ?
    def test_update_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        index = self.client.get_index(uid="movies_uid")
        response = index.update_documents([data[0]]);
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_document(self):
        index = self.client.get_index(uid="movies_uid")
        # DELETE element Captain Marvel
        response = index.delete_document(299537);
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_documents(self):
        index = self.client.get_index(uid="movies_uid")
        # Deleted element
        # Escape Room, 522681
        # Glass, 450465
        # Dumbo, 329996 
        response = index.delete_documents([522681, 450465, 329996]);
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
        assert response.status_code == 204
