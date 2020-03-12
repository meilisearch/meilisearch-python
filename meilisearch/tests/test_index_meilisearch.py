import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestIndex:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)

    """ index route """
    @pytest.mark.run(order=1)
    def test_create_index(self):
        """Tests an API call to create an index in MeiliSearch"""
        index = self.client.create_index(uid='movies_uid')
        assert isinstance(index, object)
        assert index.uid == 'movies_uid'

    def test_get_indexes(self):
        """Tests an API call to get all indexes in MeiliSearch"""
        response = self.client.get_indexes()
        assert isinstance(response, list)

    def test_get_index_with_uid(self):
        """Tests an API call to get one index with uid in MeiliSearch"""
        response = self.client.get_index(uid='movies_uid')
        assert isinstance(response, object)

    def test_get_index_with_none_uid(self):
        """Raises an exception if the index UID si None"""
        with pytest.raises(Exception):
            self.client.get_index(uid=None)

    def test_index_info(self):
        """Tests an API call to get an index's info in MeiliSearch"""
        index = self.client.get_index(uid='movies_uid')
        response = index.info()
        assert isinstance(response, object)
        assert response['uid'] == 'movies_uid'
        assert response['primaryKey'] is None

    def test_index_info_with_wrong_uid(self):
        """Tests an API call to get an index's info in MeiliSearch with a wrong UID"""
        with pytest.raises(Exception):
            self.client.get_index(uid='wrongUID').info()

    def test_get_primary_key(self):
        """Tests an API call to get primary-key of an index in MeiliSearch"""
        index = self.client.get_index(uid='movies_uid')
        response = index.get_primary_key()
        assert response is None

    def test_update_index(self):
        """Tests an API call to update an index in MeiliSearch"""
        index = self.client.get_index(uid='movies_uid')
        response = index.update(primaryKey='objectID')
        assert isinstance(response, object)
        assert index.get_primary_key() == 'objectID'

    @pytest.mark.run(order=-1)
    def test_delete_index(self):
        """Tests an API call to delete an index in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.delete()
        assert isinstance(response, object)
        assert response.status_code == 204
