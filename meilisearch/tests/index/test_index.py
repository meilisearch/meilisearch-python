# pylint: disable=invalid-name

import pytest
from meilisearch.index import Index
from meilisearch.tests import common

def test_create_index(client):
    """Tests creating an index."""
    index = client.create_index(uid=common.INDEX_UID)
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID
    assert index.primary_key is None
    assert index.get_primary_key() is None

def test_create_index_with_primary_key(client):
    """Tests creating an index with a primary key."""
    index = client.create_index(uid=common.INDEX_UID2, options={'primaryKey': 'book_id'})
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID2
    assert index.primary_key == 'book_id'
    assert index.get_primary_key() == 'book_id'

def test_create_index_with_uid_in_options(client):
    """Tests creating an index with a primary key."""
    index = client.create_index(uid=common.INDEX_UID3, options={'uid': 'wrong', 'primaryKey': 'book_id'})
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID3
    assert index.primary_key == 'book_id'
    assert index.get_primary_key() == 'book_id'

@pytest.mark.usefixtures("indexes_sample")
def test_get_indexes(client):
    """Tests getting all indexes."""
    response = client.get_indexes()
    uids = [index['uid'] for index in response]
    assert isinstance(response, list)
    assert common.INDEX_UID in uids
    assert common.INDEX_UID2 in uids
    assert common.INDEX_UID3 in uids
    assert len(response) == 3

def test_index_with_any_uid(client):
    index = client.index('anyUID')
    assert isinstance(index, Index)
    assert index.uid == 'anyUID'
    assert index.primary_key is None
    assert index.config is not None
    assert index.http is not None

def test_index_with_none_uid(client):
    with pytest.raises(Exception):
        client.index(None)

@pytest.mark.usefixtures("indexes_sample")
def test_get_index_with_valid_uid(client):
    """Tests getting one index with uid."""
    response = client.get_index(uid=common.INDEX_UID)
    assert isinstance(response, Index)
    assert response.uid == common.INDEX_UID

def test_get_index_with_none_uid(client):
    """Test raising an exception if the index UID is None."""
    with pytest.raises(Exception):
        client.get_index(uid=None)

def test_get_index_with_wrong_uid(client):
    """Tests get_index with an non-existing index."""
    with pytest.raises(Exception):
        client.get_index(uid='wrongUID')

def test_get_or_create_index(client):
    """Test get_or_create_index method."""
    index_1 = client.get_or_create_index(common.INDEX_UID4)
    index_2 = client.get_or_create_index(common.INDEX_UID4)
    index_3 = client.get_or_create_index(common.INDEX_UID4)
    assert index_1.uid == index_2.uid == index_3.uid == common.INDEX_UID4
    update = index_1.add_documents([{
        'book_id': 1,
        'name': "Some book"
    }])
    index_1.wait_for_pending_update(update['updateId'])
    documents = index_2.get_documents()
    assert len(documents) == 1
    index_2.delete()
    with pytest.raises(Exception):
        client.get_index(index_3)

def test_get_or_create_index_with_primary_key(client):
    """Test get_or_create_index method with primary key."""
    index_1 = client.get_or_create_index('books', {'primaryKey': common.INDEX_UID4})
    index_2 = client.get_or_create_index('books', {'primaryKey': 'some_wrong_key'})
    assert index_1.primary_key == common.INDEX_UID4
    assert index_1.get_primary_key() == common.INDEX_UID4
    assert index_2.primary_key == common.INDEX_UID4
    assert index_2.get_primary_key() == common.INDEX_UID4
    index_1.delete()

@pytest.mark.usefixtures("indexes_sample")
def test_index_fetch_info(client):
    """Tests fetching the index info."""
    index = client.index(uid=common.INDEX_UID)
    response = index.fetch_info()
    assert isinstance(response, Index)
    assert response.uid == common.INDEX_UID
    assert response.primary_key is None
    assert response.primary_key == index.primary_key
    assert response.primary_key == index.get_primary_key()

@pytest.mark.usefixtures("indexes_sample")
def test_index_fetch_info_containing_primary_key(client):
    """Tests fetching the index info when a primary key has been set."""
    index = client.index(uid=common.INDEX_UID3)
    response = index.fetch_info()
    assert isinstance(response, Index)
    assert response.uid == common.INDEX_UID3
    assert response.primary_key == 'book_id'
    assert response.primary_key == index.primary_key
    assert response.primary_key == index.get_primary_key()

@pytest.mark.usefixtures("indexes_sample")
def test_get_primary_key(client):
    """Tests getting the primary key of an index."""
    index = client.index(uid=common.INDEX_UID3)
    assert index.primary_key is None
    response = index.get_primary_key()
    assert response == 'book_id'
    assert index.primary_key == 'book_id'
    assert index.get_primary_key() == 'book_id'

@pytest.mark.usefixtures("indexes_sample")
def test_update_index(client):
    """Tests updating an index."""
    index = client.index(uid=common.INDEX_UID)
    response = index.update(primaryKey='objectID')
    assert isinstance(response, Index)
    assert index.primary_key == 'objectID'
    assert index.get_primary_key() == 'objectID'

@pytest.mark.usefixtures("indexes_sample")
def test_delete_index(client):
    """Tests deleting an index."""
    response = client.index(uid=common.INDEX_UID).delete()
    assert response.status_code == 204
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID)
    response = client.index(uid=common.INDEX_UID2).delete()
    assert response.status_code == 204
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID2)
    response = client.index(uid=common.INDEX_UID3).delete()
    assert response.status_code == 204
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID3)
    assert len(client.get_indexes()) == 0
