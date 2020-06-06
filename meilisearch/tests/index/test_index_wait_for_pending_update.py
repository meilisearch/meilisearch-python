from datetime import datetime
import json
import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestUpdate:

    """ TESTS: wait_for_pending_update method """

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

    def test_wait_for_pending_update_default(self):
        """Tests waiting for an update with default parameters"""
        response = self.index.add_documents([{'id': 1, 'title': 'Le Petit Prince'}])
        assert 'updateId' in response
        update = self.index.wait_for_pending_update(response['updateId'])
        assert isinstance(update, object)
        assert 'status' in update
        assert update['status'] != 'enqueued'

    def test_wait_for_pending_update_timeout(self):
        """Tests timeout risen by waiting for an update"""
        with pytest.raises(TimeoutError):
            self.index.wait_for_pending_update(2, timeout_in_ms=0)

    def test_wait_for_pending_update_interval_custom(self):
        """Tests call to wait for an update with custom interval"""
        response = self.index.add_documents(self.dataset_json)
        assert 'updateId' in response
        start_time = datetime.now()
        wait_update = self.index.wait_for_pending_update(
            response['updateId'],
            interval_in_ms=1000,
            timeout_in_ms=6000
        )
        time_delta = datetime.now() - start_time
        assert isinstance(wait_update, object)
        assert 'status' in wait_update
        assert wait_update['status'] != 'enqueued'
        assert time_delta.seconds >= 1

    def test_wait_for_pending_update_interval_zero(self):
        """Tests call to wait for an update with custom interval"""
        response = self.index.add_documents(self.dataset_json)
        assert 'updateId' in response
        wait_update = self.index.wait_for_pending_update(
            response['updateId'],
            interval_in_ms=0,
            timeout_in_ms=6000
        )
        assert isinstance(wait_update, object)
        assert 'status' in wait_update
        assert wait_update['status'] != 'enqueued'
