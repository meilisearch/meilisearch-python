import os
import sys
import time
import json
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import meilisearch


class TestIndexes:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ Client """
    def test_get_client(self):
        """Tests a call to get a client instance of meilisearch"""
        client = meilisearch.Client("http://127.0.0.1:7700", "123")
        assert client.config

    def test_get_client_without_apikey(self):
        """Tests a call to get a client instance of meilisearch"""
        client = meilisearch.Client("http://127.0.0.1:7700")
        assert client.config

    """ health route """
    def test_health(self):
        """Tests an API call to check the health of meilisearch"""
        response = self.client.health()
        assert response.status_code == 204

    """ sys-info route """
    def test_get_sys_info(self):
        """Tests an API call to check the system information of meilisearch"""
        response = self.client.get_sys_info()
        assert 'memoryUsage' in response

    """ version route """
    def test_get_version(self):
        """Tests an API call to get the version of meilisearch"""
        response = self.client.get_version()
        assert 'pkgVersion' in response

    """ index route """
    def test_create_index(self):
        """Tests an API call to create an index in meiliSearch"""
        index = self.client.create_index(name="movies", uid="movies_uid")
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
        assert isinstance(response, object)

    def test_update_index(self):
        """Tests an API call to update an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.update(name="movie")
        assert isinstance(response, object)

    """  schema route """
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

    """ updates route """
    def test_get_updates(self):
        """Tests a call to get updates of a given index"""
        index = self.client.get_index(uid="movies_uid")
        response = index.get_updates()
        assert isinstance(response, list)
        assert 'status' in response[0]

    def test_get_update(self):
        """Tests a call to get an update of a given operation"""
        index = self.client.get_index(uid="movies_uid")
        response = index.get_update(0)
        assert isinstance(response, object)
        assert 'status' in response
        assert response['status'] == 'processed'

    """ documents route """
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

    """ search route """
    def test_search_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.search({
            'q': 'How to Train Your Dragon'
        })
        assert isinstance(response, object)
        assert response["hits"][0]["id"] == '166428'

    """ stats route """
    def test_get_all_stats(self):
        response = self.client.get_all_stats()
        assert isinstance(response, object)
        assert 'databaseSize' in response

    def test_get_stats(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_stats()
        assert isinstance(response, object)
        assert 'numberOfDocuments' in response
        assert response['numberOfDocuments'] == 30

    """ stop-words route """
    def test_add_stop_words(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.add_stop_words(['the','and'])
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_get_stop_words(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.get_stop_words()
        assert isinstance(response, list)

    def test_delete_stop_words(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_stop_words(['the'])
        assert isinstance(response, object)
        assert 'updateId' in response


    """ key route """
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
        assert response.status_code == 204

    """ settings route """
    def test_add_settings(self):
        """Tests an API call to add setting to an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.add_settings({
            "rankingOrder": [
                "_sum_of_typos",
                "_number_of_words",
                "_word_proximity",
                "_sum_of_words_attribute",
                "_sum_of_words_position",
                "_exact",
                "release_date"
            ],
            "distinctField": "",
            "rankingRules": {
                "release_date": "dsc"
            }
        })
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_update_settings(self):
        """Tests an API call to update settings of an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.replace_settings({
            "rankingOrder": [
                "_sum_of_typos",
                "_number_of_words",
                "_word_proximity",
                "_sum_of_words_attribute",
                "_sum_of_words_position",
                "_exact",
                "release_date"
            ],
            "distinctField": "",
            "rankingRules": {
                "release_date": "dsc"
            }
        })
        assert isinstance(response, object)
        assert 'updateId' in response


    def test_get_settings(self):
        """Tests an API call to get settings of an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.get_settings()
        assert isinstance(response, object)
        assert 'rankingOrder' in response

    """ update route """
    def test_update_documents(self):
        json_file = open('./datasets/small_movies.json')
        data = json.load(json_file)
        index = self.client.get_index(uid="movies_uid")
        response = index.update_documents([data[0]])
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_document(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_document(299537)
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_documents([522681, 450465, 329996])
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_all_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.delete_all_documents()
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_delete_index(self):
        """Tests an API call to delete an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.delete()
        assert isinstance(response, object)
        assert response.status_code == 204
