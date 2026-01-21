# pylint: disable=invalid-name

from datetime import datetime

import pytest

from meilisearch.client import Client
from meilisearch.errors import MeilisearchApiError
from meilisearch.index import Index
from tests import BASE_URL, MASTER_KEY, common


def test_create_index(empty_index):
    """Tests creating an index."""
    index = empty_index()
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID
    assert index.primary_key is None
    assert index.get_primary_key() is None


def test_create_index_with_primary_key(client):
    """Tests creating an index with a primary key."""
    response = client.create_index(uid=common.INDEX_UID2, options={"primaryKey": "book_id"})
    client.wait_for_task(response.task_uid)
    index = client.get_index(uid=common.INDEX_UID2)
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID2
    assert index.primary_key == "book_id"
    assert index.get_primary_key() == "book_id"


def test_create_index_with_uid_in_options(client):
    """Tests creating an index with a primary key."""
    response = client.create_index(
        uid=common.INDEX_UID3, options={"uid": "wrong", "primaryKey": "book_id"}
    )
    client.wait_for_task(response.task_uid)
    index = client.get_index(uid=common.INDEX_UID3)
    assert isinstance(index, Index)
    assert index.uid == common.INDEX_UID3
    assert index.primary_key == "book_id"
    assert index.get_primary_key() == "book_id"


@pytest.mark.usefixtures("indexes_sample")
def test_get_indexes(client):
    """Tests getting all indexes."""
    response = client.get_indexes()
    uids = [index.uid for index in response["results"]]
    assert isinstance(response["results"], list)
    assert common.INDEX_UID in uids
    assert common.INDEX_UID2 in uids
    assert common.INDEX_UID3 in uids
    assert len(response["results"]) == 3


@pytest.mark.usefixtures("indexes_sample")
def test_get_indexes_with_parameters(client):
    """Tests getting all indexes."""
    response = client.get_indexes(parameters={"limit": 1, "offset": 1})
    assert len(response["results"]) == 1


@pytest.mark.usefixtures("indexes_sample")
def test_get_raw_indexes(client):
    response = client.get_raw_indexes()
    uids = [index["uid"] for index in response["results"]]
    assert isinstance(response["results"], list)
    assert common.INDEX_UID in uids
    assert common.INDEX_UID2 in uids
    assert common.INDEX_UID3 in uids
    assert len(response["results"]) == 3


@pytest.mark.usefixtures("indexes_sample")
def test_get_raw_indexeswith_parameters(client):
    response = client.get_raw_indexes(parameters={"limit": 1, "offset": 1})
    assert isinstance(response["results"], list)
    assert len(response["results"]) == 1


def test_index_with_any_uid(client):
    index = client.index("anyUID")
    assert isinstance(index, Index)
    assert index.uid == "anyUID"
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
        client.get_index(uid="wrongUID")


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
        client.get_raw_index(uid="wrongUID")


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
    assert response.primary_key == "book_id"
    assert response.primary_key == index.primary_key
    assert response.primary_key == index.get_primary_key()


@pytest.mark.usefixtures("indexes_sample")
def test_get_primary_key(client):
    """Tests getting the primary key of an index."""
    index = client.index(uid=common.INDEX_UID3)
    assert index.primary_key is None
    response = index.get_primary_key()
    assert response == "book_id"
    assert index.primary_key == "book_id"
    assert index.get_primary_key() == "book_id"


def test_update_index(empty_index):
    """Tests updating an index."""
    index = empty_index()
    response = index.update(primary_key="objectID")
    index.wait_for_task(response.task_uid)
    response = index.fetch_info()
    assert isinstance(response, Index)
    assert index.get_primary_key() == "objectID"
    assert isinstance(index.created_at, datetime)
    assert isinstance(index.updated_at, datetime)


@pytest.mark.usefixtures("indexes_sample")
def test_delete_index_by_client(client):
    """Tests deleting an index."""
    response = client.index(uid=common.INDEX_UID).delete()
    assert response.status == "enqueued"
    client.wait_for_task(response.task_uid)
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID)
    response = client.index(uid=common.INDEX_UID2).delete()
    assert response.status == "enqueued"
    client.wait_for_task(response.task_uid)
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID2)
    response = client.index(uid=common.INDEX_UID3).delete()
    assert response.status == "enqueued"
    client.wait_for_task(response.task_uid)
    with pytest.raises(Exception):
        client.get_index(uid=common.INDEX_UID3)
    assert len(client.get_indexes()["results"]) == 0


@pytest.mark.usefixtures("indexes_sample")
def test_delete(client):
    assert client.get_index(uid=common.INDEX_UID)
    deleted = Client(BASE_URL, MASTER_KEY).index(common.INDEX_UID).delete()
    client.wait_for_task(deleted.task_uid)
    with pytest.raises(MeilisearchApiError):
        client.get_index(uid=common.INDEX_UID)


@pytest.mark.usefixtures("indexes_sample")
def test_delete_index(client):
    assert client.get_index(uid=common.INDEX_UID)
    deleted = Client(BASE_URL, MASTER_KEY).delete_index(uid=common.INDEX_UID)
    client.wait_for_task(deleted.task_uid)
    with pytest.raises(MeilisearchApiError):
        client.get_index(uid=common.INDEX_UID)


@pytest.mark.usefixtures("indexes_sample")
def test_index_compact(client):
    """Tests the compaction of an index."""
    index = client.index(common.INDEX_UID)
    # Get stats before compaction
    stats_before = index.get_stats()

    task_info = index.compact()
    client.wait_for_task(task_info.task_uid)
    stats_after = index.get_stats()

    assert stats_before.number_of_documents == stats_after.number_of_documents
    assert stats_after.is_indexing is False


@pytest.mark.usefixtures("indexes_sample")
def test_rename_index(client):
    """Test renaming an existing index."""
    original_uid = common.INDEX_UID
    new_uid = f"{original_uid}_renamed"
    index = client.index(original_uid)

    # Perform the rename
    task_info = index.update(new_uid=new_uid)
    client.wait_for_task(task_info.task_uid)

    # Verify the index now exists with the new UID
    renamed_index = client.index(new_uid)
    info = renamed_index.fetch_info()
    assert info.uid == new_uid

    # # Verify the old UID no longer exists
    with pytest.raises(MeilisearchApiError):
        client.index(original_uid).fetch_info()  # Assert old UID is gone


@pytest.mark.usefixtures("indexes_sample")
def test_index_update_and_rename(client):
    """Test updating primary key and renaming an index together."""
    original_uid = common.INDEX_UID
    new_uid = f"{original_uid}_renamed"
    index = client.index(original_uid)

    # 1. Update the primary key
    task_info = index.update(primary_key="objectID", new_uid=new_uid)
    client.wait_for_task(task_info.task_uid)

    # Verify the index now exists with the new UID
    renamed_index = client.index(new_uid)
    info = renamed_index.fetch_info()
    assert info.uid == new_uid
    assert renamed_index.get_primary_key() == "objectID"


@pytest.mark.usefixtures("indexes_sample")
def test_index_update_without_params(client):
    """Test updating primary key and renaming an index together."""
    index = client.index(common.INDEX_UID)
    with pytest.raises(ValueError) as exc:
        index.update()

    assert "primary_key" in str(exc.value) or "new_uid" in str(exc.value)


@pytest.mark.usefixtures("indexes_sample")
def test_get_fields(client, small_movies):
    """Tests getting all fields of an index via the new /fields endpoint."""
    index = client.index(uid=common.INDEX_UID)
    task = index.add_documents(small_movies)
    client.wait_for_task(task.task_uid)

    fields = index.get_fields()

    assert isinstance(fields, list)
    assert len(fields) > 0
    assert "name" in fields[0]
    assert "searchable" in fields[0]
    assert "filterable" in fields[0]
    assert "sortable" in fields[0]


@pytest.mark.usefixtures("indexes_sample")
def test_get_fields_with_configurations(client, small_movies):
    """Tests get_fields() reflects index settings configurations."""
    index = client.index(uid=common.INDEX_UID)
    task = index.add_documents(small_movies)
    client.wait_for_task(task.task_uid)

    task = index.update_searchable_attributes(["title"])
    client.wait_for_task(task.task_uid)

    fields = index.get_fields()
    title_field = next((f for f in fields if f["name"] == "title"), None)

    assert title_field is not None
    assert title_field["searchable"]["enabled"] is True


@pytest.mark.usefixtures("indexes_sample")
def test_get_fields_with_filter(client, small_movies):
    """Tests get_fields() with filter parameters."""
    index = client.index(uid=common.INDEX_UID)
    task = index.add_documents(small_movies)
    client.wait_for_task(task.task_uid)

    task = index.update_searchable_attributes(["title"])
    client.wait_for_task(task.task_uid)

    # Filter only searchable fields
    searchable_fields = index.get_fields(filter={"searchable": True})

    assert isinstance(searchable_fields, list)
    assert len(searchable_fields) > 0
    assert all(field["searchable"]["enabled"] is True for field in searchable_fields)


@pytest.mark.usefixtures("indexes_sample")
def test_get_fields_with_pagination(client, small_movies):
    """Tests get_fields() with pagination parameters."""
    index = client.index(uid=common.INDEX_UID)
    task = index.add_documents(small_movies)
    client.wait_for_task(task.task_uid)

    # Get all fields first to know total count
    all_fields = index.get_fields()
    total_fields = len(all_fields)
    
    # Test pagination with offset and limit
    page1 = index.get_fields(offset=0, limit=2)
    assert isinstance(page1, list)
    assert len(page1) <= 2
    
    # If we have more than 2 fields, test second page
    if total_fields > 2:
        page2 = index.get_fields(offset=2, limit=2)
        assert isinstance(page2, list)
        assert len(page2) <= 2
        
        # Verify pages don't overlap
        page1_names = {f["name"] for f in page1}
        page2_names = {f["name"] for f in page2}
        assert page1_names.isdisjoint(page2_names)
    
    # Test with just limit (no offset)
    limited = index.get_fields(limit=3)
    assert isinstance(limited, list)
    assert len(limited) <= 3
    
    # Test with just offset (no limit, uses default)
    offset_only = index.get_fields(offset=1)
    assert isinstance(offset_only, list)
