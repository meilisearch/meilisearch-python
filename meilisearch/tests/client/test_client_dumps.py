import json
import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes, wait_for_dump_creation
from meilisearch.errors import MeiliSearchApiError

class TestClientDumps:

    """ TESTS: Client dumps creation and status """

    client = meilisearch.Client(BASE_URL, MASTER_KEY)
    index = None
    dataset_file = None
    dataset_json = None

    def setup_class(self):
        clear_all_indexes(self.client)
        self.dataset_file = open('./datasets/small_movies.json', 'r')
        self.dataset_json = json.loads(self.dataset_file.read())
        self.dataset_file.close()

    def setup_method(self, method):
        """Creates and populates an index before each test is run"""
        self.index = self.client.create_index(uid='indexUID-' + method.__name__)
        response = self.index.add_documents(self.dataset_json, primary_key='id')
        self.index.wait_for_pending_update(response['updateId'])

    def teardown_method(self, method):
        self.client.get_index('indexUID-' + method.__name__).delete()

    def teardown_class(self):
        """Cleans all indexes in MEiliSearch when all the test are done"""
        clear_all_indexes(self.client)

    def test_dump_creation(self):
        """Tests the creation of a MeiliSearch dump"""
        dump = self.client.create_dump()
        assert dump['uid'] is not None
        assert dump['status'] == 'processing'
        wait_for_dump_creation(self.client, dump['uid'])

    def test_dump_status_route(self):
        """Tests the route for getting a MeiliSearch dump status"""
        dump = self.client.create_dump()
        assert dump['uid'] is not None
        assert dump['status'] == 'processing'
        dump_status = self.client.get_dump_status(dump['uid'])
        assert dump_status['uid'] is not None
        assert dump_status['status'] is not None
        wait_for_dump_creation(self.client, dump['uid'])

    def test_dump_status_nonexistent_uid_raises_error(self):
        """Tests the route for getting a nonexistent dump status"""
        with pytest.raises(MeiliSearchApiError):
            self.client.get_dump_status('uid_not_exists')
