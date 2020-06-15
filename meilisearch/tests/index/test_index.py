import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestIndex:

    """ TESTS: all index routes """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index_uid = 'indexUID'
    index_uid2 = 'indexUID2'

    def setup_class(self):
        clear_all_indexes(self.client)

    def test_create_index(self):
        """Tests creating an index"""
        index = self.client.create_index(uid=self.index_uid)
        assert isinstance(index, object)
        assert index.uid == self.index_uid
        assert index.get_primary_key() is None

    def test_create_index_with_primary_key(self):
        """Tests creating an index with a primary key"""
        index = self.client.create_index(uid=self.index_uid2, options={'primaryKey': 'book_id'})
        assert isinstance(index, object)
        assert index.uid == self.index_uid2
        assert index.get_primary_key() == 'book_id'

    def test_get_indexes(self):
        """Tests getting all indexes"""
        response = self.client.get_indexes()
        assert isinstance(response, list)
        assert response[0]['uid'] == self.index_uid

    def test_get_index_with_uid(self):
        """Tests getting one index with uid"""
        response = self.client.get_index(uid=self.index_uid)
        assert isinstance(response, object)
        assert response.uid == self.index_uid

    def test_get_index_with_none_uid(self):
        """Test raising an exception if the index UID is None"""
        with pytest.raises(Exception):
            self.client.get_index(uid=None)

    def test_index_info(self):
        """Tests getting an index's info"""
        index = self.client.get_index(uid=self.index_uid)
        response = index.info()
        assert isinstance(response, object)
        assert response['uid'] == self.index_uid
        assert response['primaryKey'] is None

    def test_index_info_with_wrong_uid(self):
        """Tests getting an index's info in MeiliSearch with a wrong UID"""
        with pytest.raises(Exception):
            self.client.get_index(uid='wrongUID').info()

    def test_get_primary_key(self):
        """Tests getting the primary-key of an index"""
        index = self.client.get_index(uid=self.index_uid)
        response = index.get_primary_key()
        assert response is None

    def test_update_index(self):
        """Tests updating an index"""
        index = self.client.get_index(uid=self.index_uid)
        response = index.update(primaryKey='objectID')
        assert isinstance(response, object)
        assert index.get_primary_key() == 'objectID'

    def test_delete_index(self):
        """Tests deleting an index"""
        index = self.client.get_index(uid=self.index_uid)
        response = index.delete()
        assert isinstance(response, object)
        assert response.status_code == 204
        with pytest.raises(Exception):
            self.client.get_index(uid=self.index_uid).info()
        index = self.client.get_index(uid=self.index_uid2)
        response = index.delete()
        assert isinstance(response, object)
        assert response.status_code == 204
        with pytest.raises(Exception):
            self.client.get_index(uid=self.index_uid2).info()
