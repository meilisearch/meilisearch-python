import pytest

class TestDocument:

    """ TESTS: all documents routes and optional params """

    def test_get_documents_default(self, sample_indexes):
        """Tests getting documents on a clean index"""
        response = sample_indexes[0].get_documents()
        assert isinstance(response, list)
        assert response == []

    def test_add_documents(self, sample_indexes, small_movies):
        """Tests adding new documents to a clean index"""
        response = sample_indexes[0].add_documents(small_movies)
        assert isinstance(response, object)
        assert 'updateId' in response
        assert sample_indexes[0].get_primary_key() == 'id'
        update = sample_indexes[0].wait_for_pending_update(response['updateId'])
        assert update['status'] == 'processed'

    def test_get_document(self, indexed_small_movies):
        """Tests getting one document on a populated index"""
        response = indexed_small_movies[0].get_document('500682')
        assert isinstance(response, object)
        assert 'title' in response
        assert response['title'] == 'The Highwaymen'

    def test_get_document_inexistent(self, sample_indexes):
        """Tests getting one INEXISTENT document on a populated index"""
        with pytest.raises(Exception):
            sample_indexes[0].get_document('123')

    def test_get_documents_populated(self, indexed_small_movies):
        """Tests getting documents on a populated index"""

        response = indexed_small_movies[0].get_documents()
        assert isinstance(response, list)
        assert len(response) == 20

    def test_get_documents_offset_optional_params(self, indexed_small_movies, small_movies):
        """Tests getting documents on a populated index with optional parameters"""
        # Add movies to the index
        indexed_small_movies[0].add_documents(small_movies)

        response = indexed_small_movies[0].get_documents()
        assert isinstance(response, list)
        assert len(response) == 20
        response_offset_limit = indexed_small_movies[0].get_documents({
            'limit': 3,
            'offset': 1,
            'attributesToRetrieve': 'title'
        })
        assert len(response_offset_limit) == 3
        assert response_offset_limit[0]['title'] == response[1]['title']

    def test_update_documents(self, indexed_small_movies, small_movies):
        """Tests updating a single document and a set of documents """
        response = indexed_small_movies[0].get_documents()
        response[0]['title'] = 'Some title'
        update = indexed_small_movies[0].update_documents([response[0]])
        assert isinstance(update, object)
        assert 'updateId' in update
        indexed_small_movies[0].wait_for_pending_update(update['updateId'])
        response = indexed_small_movies[0].get_documents()
        assert response[0]['title'] == 'Some title'
        update = indexed_small_movies[0].update_documents(small_movies)
        indexed_small_movies[0].wait_for_pending_update(update['updateId'])
        response = indexed_small_movies[0].get_documents()
        assert response[0]['title'] != 'Some title'

    def test_delete_document(self, indexed_small_movies):
        """Tests deleting a single document"""
        response = indexed_small_movies[0].delete_document('500682')
        assert isinstance(response, object)
        assert 'updateId' in response
        indexed_small_movies[0].wait_for_pending_update(response['updateId'])
        with pytest.raises(Exception):
            indexed_small_movies[0].get_document('500682')

    def test_delete_documents(self, indexed_small_movies):
        """Tests deleting a set of documents """
        to_delete = ['522681', '450465', '329996']
        response = indexed_small_movies[0].delete_documents(to_delete)
        assert isinstance(response, object)
        assert 'updateId' in response
        indexed_small_movies[0].wait_for_pending_update(response['updateId'])
        for document in to_delete:
            with pytest.raises(Exception):
                indexed_small_movies[0].get_document(document)

    def test_delete_all_documents(self, indexed_small_movies):
        """Tests updating all the documents in the index"""
        response = indexed_small_movies[0].delete_all_documents()
        assert isinstance(response, object)
        assert 'updateId' in response
        indexed_small_movies[0].wait_for_pending_update(response['updateId'])
        response = indexed_small_movies[0].get_documents()
        assert isinstance(response, list)
        assert response == []
