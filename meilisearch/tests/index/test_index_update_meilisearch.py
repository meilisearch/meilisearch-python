import json
import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestUpdate:

    """ TESTS: all update routes """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    dataset_file = None
    dataset_json = None

    def setup_class(self):
        clear_all_indexes(self.client)
        self.index = self.client.create_index(uid='indexUID')
        self.dataset_file = open('./datasets/small_movies.json', 'r')
        self.dataset_json = json.loads(self.dataset_file.read())
        self.dataset_file.close()

    def teardown_class(self):
        self.index.delete()

    def test_get_all_update_status_default(self):
        """Tests getting the updates list of an empty index"""
        response = self.index.get_all_update_status()
        assert isinstance(response, list)
        assert response == []

    def test_get_all_update_status(self):
        """Tests getting the updates list of a populated index"""
        response = self.index.add_documents(self.dataset_json)
        assert 'updateId' in response
        response = self.index.add_documents(self.dataset_json)
        assert 'updateId' in response
        response = self.index.get_all_update_status()
        assert len(response) == 2

    def test_get_update(self):
        """Tests getting an update of a given operation"""
        response = self.index.add_documents(self.dataset_json)
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'
        response = self.index.get_update_status(response['updateId'])
        assert 'updateId' in response
        assert 'type' in response
        assert 'duration' in response
        assert 'enqueuedAt' in response
        assert 'processedAt' in response

    def test_get_update_inexistent(self):
        """Tests getting an update of an INEXISTENT operation"""
        with pytest.raises(Exception):
            self.index.get_update_status('999')
