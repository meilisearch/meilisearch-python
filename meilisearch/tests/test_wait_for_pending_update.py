from datetime import datetime
import json
import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY

class TestUpdate:
    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None

    def setup_class(self):
        self.index = self.client.create_index(uid='indexUID')

    def teardown_class(self):
        self.index.delete()

    def test_wait_for_pending_update_default(self):
        """Tests call to wait for an update with default parameters"""
        response = self.index.add_documents([{'id': 1, 'title': 'Le Petit Prince'}])
        assert 'updateId' in response
        wait_update = self.index.wait_for_pending_update(response['updateId'])
        assert isinstance(wait_update, object)
        assert 'status' in wait_update
        assert wait_update['status'] != 'enqueued'

    def test_wait_for_pending_update_timeout(self):
        """Tests timeout risen by waiting for an update"""
        with pytest.raises(TimeoutError):
            self.index.wait_for_pending_update(2, timeout_in_ms=0)

    def test_wait_for_pending_update_interval(self):
        """Tests call to wait for an update with custom interval"""
        dataset_file = open("datasets/small_movies.json", "r")
        dataset_json = json.loads(dataset_file.read())
        response = self.index.add_documents(dataset_json)
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
