# pylint: disable=invalid-name

from datetime import datetime

import pytest
from meilisearch.client import Client
from meilisearch.errors import MeiliSearchApiError
from meilisearch.index import Index
from tests import BASE_URL, common, MASTER_KEY

def test_create_index(client, empty_index):
    """Tests creating an index."""
    index = empty_index()
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID
    assert index.primary_key is None
    assert index.get_primary_key() is None

def test_create_index_with_primary_key(client):
    """Tests creating an index with a primary key."""
    response = client.create_index(uid=common.INDEX_UID2, options={'primaryKey': 'book_id'})
    client.wait_for_task(response['taskUid'])
    index = client.get_index(uid=common.INDEX_UID2)
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID2
    assert index.primary_key == 'book_id'
    assert index.get_primary_key() == 'book_id'

def test_create_index_with_uid_in_options(client):
    """Tests creating an index with a primary key."""
    response = client.create_index(uid=common.INDEX_UID3, options={'uid': 'wrong', 'primaryKey': 'book_id'})
    client.wait_for_task(response['taskUid'])
    index = client.get_index(uid=common.INDEX_UID3)
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID3
    assert index.primary_key == 'book_id'
    assert index.get_primary_key() == 'book_id'

@pytest.mark.usefixtures("indexes_sample")
def test_get_indexes(client):
    """Tests getting all indexes."""
    response = client.get_indexes()
    uids = [index.uid for index in response['results']]
    assert isinstance(response['results'], list)
    assert common.INDEX_UID in uids
    assert common.INDEX_UID2 in uids
    assert common.INDEX_UID3 in uids
    assert len(response['results']) == 3

@pytest.mark.usefixtures("indexes_sample")
def test_get_indexes_with_parameters(client):
    """Tests getting all indexes."""
    response = client.get_indexes(parameters={'limit':1, 'offset': 1})
    assert len(response['results']) == 1

@pytest.mark.usefixtures("indexes_sample")
def test_get_raw_indexes(client):
    response = client.get_raw_indexes()
    uids = [index['uid'] for index in response['results']]
    assert isinstance(response['results'], list)
    assert common.INDEX_UID in uids
    assert common.INDEX_UID2 in uids
    assert common.INDEX_UID3 in uids
    assert len(response['results']) == 3

@pytest.mark.usefixtures("indexes_sample")
def test_get_raw_indexeswith_parameters(client):
    response = client.get_raw_indexes(parameters={'limit':1, 'offset': 1})
    assert isinstance(response['results'], list)
    assert len(response['results']) == 1

def test_index_with_any_uid(client):
    index = client.index('anyUID')
    assert isinstance(index, Index)
    assert index.uid == 'anyUID'
    assert index.primary_key is None
    assert index.created_at is None
    assert index.updated_at is None
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
    assert isinstance(response.created_at, datetime)
    assert isinstance(response.updated_at, datetime)

def test_get_index_with_none_uid(client):
    """Test raising an exception if the index UID is None."""
    with pytest.raises(Exception):
        client.get_index(uid=None)

def test_get_index_with_wrong_uid(client):
    """Tests get_index with an non-existing index."""
    with pytest.raises(Exception):
        client.get_index(uid='wrongUID')

@pytest.mark.usefixtures("indexes_sample")
def test_get_raw_index_with_valid_uid(client):
    response = client.get_raw_index(uid=common.INDEX_UID)
    assert isinstance(response, dict)
    assert response["uid"] == common.INDEX_UID

def test_get_raw_index_with_none_uid(client):
    with pytest.raises(Exception):
        client.get_raw_index(uid=None)

def test_get_raw_index_with_wrong_uid(client):
    with pytest.raises(Exception):
        client.get_raw_index(uid='wrongUID')

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

def test_update_index(empty_index):
    """Tests updating an index."""
    index = empty_index()
    response = index.update(primary_key='objectID')
    index.wait_for_task(response['taskUid'])
    response = index.fetch_info()
    assert isinstance(response, Index)
    assert index.get_primary_key() == 'objectID'
    assert isinstance(index.created_at, datetime)
    assert isinstance(index.updated_at, datetime)

@pytest.mark.usefixtures("indexes_sample")
def test_delete_index_by_client(client):
    """Tests deleting an index."""
    response = client.index(uid=common.INDEX_UID).delete()
    assert response['status'] == 'enqueued'
    client.wait_for_task(response['taskUid'])
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID)
    response = client.index(uid=common.INDEX_UID2).delete()
    assert response['status'] == 'enqueued'
    client.wait_for_task(response['taskUid'])
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID2)
    response = client.index(uid=common.INDEX_UID3).delete()
    assert response['status'] == 'enqueued'
    client.wait_for_task(response['taskUid'])
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID3)
    assert len(client.get_indexes()['results']) == 0

@pytest.mark.usefixtures("indexes_sample")
def test_delete(client):
    assert client.get_index(uid=common.INDEX_UID)
    deleted = Client(BASE_URL, MASTER_KEY).index(common.INDEX_UID).delete()
    client.wait_for_task(deleted['taskUid'])
    with pytest.raises(MeiliSearchApiError):
        client.get_index(uid=common.INDEX_UID)

@pytest.mark.usefixtures("indexes_sample")
def test_delete_index(client):
    assert client.get_index(uid=common.INDEX_UID)
    deleted = Client(BASE_URL, MASTER_KEY).delete_index(uid=common.INDEX_UID)
    client.wait_for_task(deleted['taskUid'])
    with pytest.raises(MeiliSearchApiError):
        client.get_index(uid=common.INDEX_UID)
