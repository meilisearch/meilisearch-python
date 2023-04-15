# pylint: disable=invalid-name

from math import ceil

import pytest

from meilisearch.models.document import Document
from meilisearch.models.task import TaskInfo


def test_get_documents_default(empty_index):
    """Tests getting documents on a clean index."""
    response = empty_index().get_documents()
    assert isinstance(response.results, list)
    assert response.results == []


def test_add_documents(empty_index, small_movies):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents(small_movies)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"


def test_add_documents_empty(empty_index):
    """Tests adding empty string as documents to a clean index."""
    index = empty_index()
    with pytest.raises(Exception) as e_info:
        index.add_documents("")
    assert e_info.value.code == "missing_payload"
    assert e_info.value.type == "invalid_request"
    assert e_info.value.link == "https://docs.meilisearch.com/errors#missing_payload"


@pytest.mark.parametrize("batch_size", [2, 3, 1000])
@pytest.mark.parametrize(
    "primary_key, expected_primary_key",
    [("release_date", "release_date"), (None, "id")],
)
def test_add_documents_in_batches(
    batch_size,
    primary_key,
    expected_primary_key,
    empty_index,
    small_movies,
):
    index = empty_index()
    response = index.add_documents_in_batches(small_movies, batch_size, primary_key)
    assert ceil(len(small_movies) / batch_size) == len(response)

    for r in response:
        assert r.task_uid is not None
        update = index.wait_for_task(r.task_uid)
        assert update.status == "succeeded"

    assert index.get_primary_key() == expected_primary_key


def test_get_document(index_with_documents):
    """Tests getting one document from a populated index."""
    response = index_with_documents().get_document("500682")
    assert isinstance(response, Document)
    assert hasattr(response, "title")
    assert response.title == "The Highwaymen"


def test_get_document_with_fields(index_with_documents):
    """Tests getting one document from a populated index."""
    response = index_with_documents().get_document("500682", {"fields": ["id", "title"]})
    assert isinstance(response, Document)
    assert hasattr(response, "title")
    assert not hasattr(response, "poster")
    # assert 'poster' not in response
    assert response.title == "The Highwaymen"


def test_get_document_inexistent(empty_index):
    """Tests getting one inexistent document from a populated index."""
    with pytest.raises(Exception):
        empty_index().get_document("123")


def test_get_documents_populated(index_with_documents):
    """Tests getting documents from a populated index."""
    response = index_with_documents().get_documents()
    assert isinstance(response.results, list)
    assert len(response.results) == 20


def test_get_documents_offset_optional_params(index_with_documents):
    """Tests getting documents from a populated index with optional parameters."""
    index = index_with_documents()
    response = index.get_documents()
    assert isinstance(response.results, list)
    assert len(response.results) == 20
    response_offset_limit = index.get_documents({"limit": 3, "offset": 1, "fields": "title"})
    assert len(response_offset_limit.results) == 3
    assert hasattr(response_offset_limit.results[0], "title")
    assert response_offset_limit.results[0].title == response.results[1].title


def test_update_documents(index_with_documents, small_movies):
    """Tests updating a single document and a set of documents."""
    index = index_with_documents()
    response = index.get_documents()
    doc = response.results[0]
    doc.title = "Some title"

    update = index.update_documents([dict(doc)])

    assert isinstance(update, TaskInfo)
    assert update.task_uid is not None
    index.wait_for_task(update.task_uid)

    response = index.get_document(doc.id)
    assert response.title == "Some title"

    update = index.update_documents(small_movies)
    index.wait_for_task(update.task_uid)

    response = index.get_document(doc.id)
    assert response.title != "Some title"


@pytest.mark.parametrize("batch_size", [2, 3, 1000])
@pytest.mark.parametrize(
    "primary_key, expected_primary_key",
    [("release_date", "release_date"), (None, "id")],
)
def test_update_documents_in_batches(
    batch_size,
    primary_key,
    expected_primary_key,
    empty_index,
    small_movies,
):
    index = empty_index()
    response = index.update_documents_in_batches(small_movies, batch_size, primary_key)
    assert ceil(len(small_movies) / batch_size) == len(response)

    for r in response:
        assert r.task_uid is not None
        update = index.wait_for_task(r.task_uid)
        assert update.status == "succeeded"

    assert index.get_primary_key() == expected_primary_key


def test_delete_document(index_with_documents):
    """Tests deleting a single document."""
    index = index_with_documents()
    response = index.delete_document("500682")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    index.wait_for_task(response.task_uid)
    with pytest.raises(Exception):
        index.get_document("500682")


def test_delete_documents(index_with_documents):
    """Tests deleting a set of documents."""
    to_delete = [522681, "450465", 329996]
    index = index_with_documents()
    response = index.delete_documents(to_delete)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    index.wait_for_task(response.task_uid)
    for document in to_delete:
        with pytest.raises(Exception):
            index.get_document(document)


def test_delete_all_documents(index_with_documents):
    """Tests deleting all the documents in the index."""
    index = index_with_documents()
    response = index.delete_all_documents()
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    index.wait_for_task(response.task_uid)
    response = index.get_documents()
    assert isinstance(response.results, list)
    assert response.results == []


def test_add_documents_csv(empty_index, songs_csv):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents_csv(songs_csv)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_add_documents_csv_with_delimiter(empty_index, songs_csv_custom_separator):
    """Tests adding new documents to a clean index."""
    index = empty_index("csv-delimiter")
    response = index.add_documents_csv(songs_csv_custom_separator, csv_delimiter=";")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert task.details["receivedDocuments"] == 20
    documents = index.get_documents().results
    assert documents[1].country == "Europe"
    assert documents[4].artist == "Elton John"


def test_update_documents_csv(index_with_documents, songs_csv):
    """Tests updating a single document with csv string."""
    index = index_with_documents()
    response = index.update_documents_csv(songs_csv)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_update_documents_csv_with_delimiter(index_with_documents, songs_csv_custom_separator):
    """Tests adding new documents to a clean index."""
    index = index_with_documents()
    response = index.update_documents_csv(songs_csv_custom_separator, csv_delimiter=";")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert task.details["receivedDocuments"] == 20
    document = index.get_document("813645611")
    assert document.country == "Europe"
    assert document.artist == "Elton John"


def test_add_documents_json(empty_index, small_movies_json_file):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents_json(small_movies_json_file)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_update_documents_json(index_with_documents, small_movies_json_file):
    """Tests updating a single document with json string."""
    index = index_with_documents()
    response = index.update_documents_json(small_movies_json_file)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_add_documents_ndjson(empty_index, songs_ndjson):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents_ndjson(songs_ndjson)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_update_documents_ndjson(index_with_documents, songs_ndjson):
    """Tests updating a single document with ndjson string."""
    index = index_with_documents()
    response = index.update_documents_ndjson(songs_ndjson)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"
