import os,sys,inspect
current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir) 
import meilisearch
import pytest

class TestIndexes: 
    client = meilisearch.Client("http://127.0.0.1:7700", None)

    # @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    # @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
    def test_create_index(self, test_input, expected):
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

    def test_delete_index(self):
        """Tests an API call to delete an index in meiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.delete()
        assert isinstance(response, object)
