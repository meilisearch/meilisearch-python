import os
import sys
import inspect
import meilisearch

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)


class TestStats:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

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
