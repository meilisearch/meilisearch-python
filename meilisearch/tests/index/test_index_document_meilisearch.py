import json
import pytest
import meilisearch
from meilisearch.tests import BASE_URL, MASTER_KEY, clear_all_indexes

class TestDocument:

    """ TESTS: all documents routes and optional params """

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

    def test_get_documents_default(self):
        """Tests getting documents on a clean index"""
        response = self.index.get_documents()
        assert isinstance(response, list)
        assert response == []

    def test_add_documents(self):
        """Tests adding new documents to a clean index"""
        response = self.index.add_documents(self.dataset_json)
        assert isinstance(response, object)
        assert 'updateId' in response
        assert self.index.get_primary_key() == 'id'
        update = self.index.wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'

    def test_get_document(self):
        """Tests getting one document on a populated index"""
        response = self.index.get_document('500682')
        assert isinstance(response, object)
        assert 'title' in response
        assert response['title'] == 'The Highwaymen'

    def test_get_document_inexistent(self):
        """Tests getting one INEXISTENT document on a populated index"""
        with pytest.raises(Exception):
            self.index.get_document('123')

    def test_get_documents_populated(self):
        """Tests getting documents on a populated index"""
        response = self.index.get_documents()
        assert isinstance(response, list)
        assert len(response) == 20

    def test_get_documents_offset_optional_params(self):
        """Tests getting documents on a populated index with optional parameters"""
        response = self.index.get_documents()
        assert isinstance(response, list)
        assert len(response) == 20
        response_offset_limit = self.index.get_documents({
            'limit': 3,
            'offset': 1,
            'attributesToRetrieve': 'title'
        })
        assert len(response_offset_limit) == 3
        assert response_offset_limit[0]['title'] == response[1]['title']

    def test_update_documents(self):
        """Tests updating a single document and a set of documents """
        response = self.index.get_documents()
        response[0]['title'] = 'Some title'
        update = self.index.update_documents([response[0]])
        assert isinstance(update, object)
        assert 'updateId' in update
        self.index.wait_for_pending_update(update['updateId'])
        response = self.index.get_documents()
        assert response[0]['title'] == 'Some title'
        update = self.index.update_documents(self.dataset_json)
        self.index.wait_for_pending_update(update['updateId'])
        response = self.index.get_documents()
        assert response[0]['title'] != 'Some title'

    def test_delete_document(self):
        """Tests deleting a single document"""
        response = self.index.delete_document('500682')
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        with pytest.raises(Exception):
            self.index.get_document('500682')

    def test_delete_documents(self):
        """Tests deleting a set of documents """
        to_delete = ['522681', '450465', '329996']
        response = self.index.delete_documents(to_delete)
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        for document in to_delete:
            with pytest.raises(Exception):
                self.index.get_document(document)

    def test_delete_all_documents(self):
        """Tests updating all the documents in the index"""
        response = self.index.delete_all_documents()
        assert isinstance(response, object)
        assert 'updateId' in response
        self.index.wait_for_pending_update(response['updateId'])
        response = self.index.get_documents()
        assert isinstance(response, list)
        assert response == []
