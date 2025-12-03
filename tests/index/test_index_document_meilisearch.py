# pylint: disable=invalid-name

import json
from datetime import datetime
from json import JSONEncoder
from math import ceil
from uuid import UUID, uuid4
from warnings import catch_warnings

import pytest

from meilisearch.errors import MeilisearchApiError
from meilisearch.models.document import Document
from meilisearch.models.task import TaskInfo


class CustomEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, (UUID, datetime)):
            return str(o)

        # Let the base class default method raise the TypeError
        return super().default(o)


def test_get_documents_default(empty_index):
    """Tests getting documents on a clean index."""
    response = empty_index().get_documents()
    assert isinstance(response.results, list)
    assert response.results == []


def test_add_documents(empty_index, small_movies):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents(small_movies, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"
    assert update.customMetadata == "Test metadata"


def test_add_documents_empty(empty_index):
    """Tests adding empty string as documents to a clean index."""
    index = empty_index()
    with pytest.raises(Exception) as e_info:
        index.add_documents("")
    assert e_info.value.code == "missing_payload"
    assert e_info.value.type == "invalid_request"


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
    response = index.add_documents_in_batches(
        small_movies, batch_size, primary_key, metadata="Test metadata"
    )
    assert ceil(len(small_movies) / batch_size) == len(response)

    for r in response:
        assert r.task_uid is not None
        update = index.wait_for_task(r.task_uid)
        assert update.status == "succeeded"
        assert update.customMetadata == "Test metadata"

    assert index.get_primary_key() == expected_primary_key


def test_add_documents_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.add_documents(documents, serializer=CustomEncoder)
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"


def test_add_documents_in_batches_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.add_documents_in_batches(documents, batch_size=1, serializer=CustomEncoder)
    for task in response:
        update = index.wait_for_task(task.task_uid)
        assert update.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_add_documents_json_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.add_documents_json(
        documents, serializer=CustomEncoder, metadata="Test metadata"
    )
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"
    assert update.customMetadata == "Test metadata"


def test_add_documents_raw_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.add_documents_raw(
        documents,
        content_type="application/json",
        serializer=CustomEncoder,
        metadata="Test metadata",
    )
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"
    assert update.customMetadata == "Test metadata"


def test_update_documents_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.update_documents(documents, serializer=CustomEncoder, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"
    assert update.customMetadata == "Test metadata"


def test_update_documents_in_batches_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.update_documents_in_batches(documents, batch_size=1, serializer=CustomEncoder)
    for task in response:
        update = index.wait_for_task(task.task_uid)
        assert update.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_update_documents_json_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.update_documents_json(
        documents, serializer=CustomEncoder, metadata="Test metadata"
    )
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"
    assert update.customMetadata == "Test metadata"


def test_update_documents_raw_custom_serializer(empty_index):
    documents = [
        {"id": uuid4(), "title": "test 1", "when": datetime.now()},
        {"id": uuid4(), "title": "Test 2", "when": datetime.now()},
    ]
    index = empty_index()
    response = index.update_documents_raw(
        documents,
        content_type="application/json",
        serializer=CustomEncoder,
        metadata="Test metadata",
    )
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    update = index.wait_for_task(response.task_uid)
    assert index.get_primary_key() == "id"
    assert update.status == "succeeded"
    assert update.customMetadata == "Test metadata"


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
    with pytest.raises(MeilisearchApiError):
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
    response_offset_limit = index.get_documents({"limit": 3, "offset": 1, "fields": ["title"]})
    assert len(response_offset_limit.results) == 3
    assert hasattr(response_offset_limit.results[0], "title")
    assert response_offset_limit.results[0].title == response.results[1].title


def test_get_documents_offset_optional_params_list_of_fields(index_with_documents):
    """Tests getting documents from a populated index with optional parameters."""
    index = index_with_documents()
    response = index.get_documents()
    assert isinstance(response.results, list)
    assert len(response.results) == 20
    response_offset_limit = index.get_documents(
        {"limit": 3, "offset": 1, "fields": ["title", "genre"]}
    )
    assert len(response_offset_limit.results) == 3
    assert hasattr(response_offset_limit.results[0], "title")
    assert hasattr(response_offset_limit.results[0], "genre")
    assert response_offset_limit.results[0].title == response.results[1].title
    assert response_offset_limit.results[0].genre == response.results[1].genre


def test_get_documents_sort_fields(index_with_documents):
    """Tests getting documents sorted by fields."""
    index = index_with_documents()

    # Make fields sortable: include 'rating' and 'release_date'
    sortable_attributes = ["rating", "release_date"]
    task = index.update_sortable_attributes(sortable_attributes)
    index.wait_for_task(task.task_uid)  # wait until sortable attributes are set

    documents = [
        {"id": 1, "title": "Inception", "release_date": "2010-07-16", "rating": 8.8},
        {"id": 2, "title": "Interstellar", "release_date": "2014-11-07", "rating": 8.6},
        {"id": 3, "title": "Parasite", "release_date": "2019-05-30", "rating": 8.6},
        {"id": 4, "title": "The Matrix", "release_date": "1999-03-31", "rating": 8.7},
        {"id": 5, "title": "The Dark Knight", "release_date": "2008-07-18", "rating": 9.0},
    ]

    # Add documents
    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

    params = {
        "limit": 5,
        "fields": ["id", "title", "release_date", "rating"],
        "sort": ["rating:desc", "release_date:asc"],
    }
    response = index.get_documents(params)

    # prepare expected order
    sorted_docs = sorted(documents, key=lambda d: (-d["rating"], d["release_date"]))

    for resp_doc, expected_doc in zip(response.results, sorted_docs):
        assert resp_doc.id == expected_doc["id"]
        assert resp_doc.rating == expected_doc["rating"]
        assert resp_doc.release_date == expected_doc["release_date"]


@pytest.mark.parametrize(
    "sort_param",
    [
        ["rating:desc", "release_date:asc"],  # list format
        "rating:desc, release_date:asc",  # comma-separated string
    ],
)
def test_get_documents_sort_formats(index_with_documents, sort_param):
    index = index_with_documents()

    # Make fields sortable
    sortable_attributes = ["rating", "release_date"]
    task = index.update_sortable_attributes(sortable_attributes)
    index.wait_for_task(task.task_uid)

    documents = [
        {"id": 1, "title": "Inception", "release_date": "2010-07-16", "rating": 8.8},
        {"id": 2, "title": "Interstellar", "release_date": "2014-11-07", "rating": 8.6},
        {"id": 3, "title": "Parasite", "release_date": "2019-05-30", "rating": 8.6},
        {"id": 4, "title": "The Matrix", "release_date": "1999-03-31", "rating": 8.7},
        {"id": 5, "title": "The Dark Knight", "release_date": "2008-07-18", "rating": 9.0},
    ]

    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

    params = {"limit": 5, "fields": ["id", "title", "release_date", "rating"], "sort": sort_param}
    response = index.get_documents(params)

    sorted_docs = sorted(documents, key=lambda d: (-d["rating"], d["release_date"]))

    for resp_doc, expected_doc in zip(response.results, sorted_docs):
        assert resp_doc.id == expected_doc["id"]
        assert resp_doc.rating == expected_doc["rating"]
        assert resp_doc.release_date == expected_doc["release_date"]


def test_get_documents_filter(index_with_documents):
    index = index_with_documents()
    response = index.update_filterable_attributes(["genre"])
    index.wait_for_task(response.task_uid)
    response = index.get_documents({"filter": "genre=action"})
    genres = {x.genre for x in response.results}
    assert len(genres) == 1
    assert next(iter(genres)) == "action"


def test_get_documents_filter_with_fields(index_with_documents):
    index = index_with_documents()
    response = index.update_filterable_attributes(["genre"])
    index.wait_for_task(response.task_uid)
    response = index.get_documents({"fields": ["genre"], "filter": "genre=action"})
    genres = {x.genre for x in response.results}
    assert len(genres) == 1
    assert next(iter(genres)) == "action"


def test_get_similar_documents(empty_index):
    index = empty_index()
    index.update_embedders({"manual": {"source": "userProvided", "dimensions": 3}})

    hp3 = {
        "id": 1,
        "title": "Harry Potter and the Prisoner of Azkaban",
        "_vectors": {"manual": [0.8, 0.8, 0.8]},
    }
    hp4 = {
        "id": 2,
        "title": "Harry Potter and the Goblet of Fire",
        "_vectors": {"manual": [0.7, 0.7, 0.9]},
    }
    lotr = {"id": 3, "title": "The Lord of the Rings", "_vectors": {"manual": [0.6, 0.5, 0.2]}}

    addition = index.add_documents([hp3, hp4, lotr])
    index.wait_for_task(addition.task_uid)

    similars = index.get_similar_documents({"id": hp4["id"], "embedder": "manual"})

    assert similars["hits"][0]["id"] == hp3["id"]
    assert similars["hits"][1]["id"] == lotr["id"]


def test_update_documents(index_with_documents, small_movies):
    """Tests updating a single document and a set of documents."""
    index = index_with_documents()
    response = index.get_documents()
    doc = response.results[0]
    doc.title = "Some title"

    update = index.update_documents([dict(doc)], metadata="Test metadata")

    assert isinstance(update, TaskInfo)
    assert update.task_uid is not None
    task = index.wait_for_task(update.task_uid)
    assert task.customMetadata == "Test metadata"

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
    response = index.update_documents_in_batches(
        small_movies, batch_size, primary_key, metadata="Test metadata"
    )
    assert ceil(len(small_movies) / batch_size) == len(response)

    for r in response:
        assert r.task_uid is not None
        update = index.wait_for_task(r.task_uid)
        assert update.status == "succeeded"
        assert update.customMetadata == "Test metadata"

    assert index.get_primary_key() == expected_primary_key


def test_delete_document(index_with_documents):
    """Tests deleting a single document."""
    index = index_with_documents()
    response = index.delete_document("500682", metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.customMetadata == "Test metadata"

    with pytest.raises(MeilisearchApiError):
        index.get_document("500682")


def test_delete_documents_by_id(index_with_documents):
    """Tests deleting a set of documents."""
    with catch_warnings(record=True) as w:
        to_delete = [522681, "450465", 329996]
        index = index_with_documents()
        response = index.delete_documents(to_delete, metadata="Test metadata")
        assert isinstance(response, TaskInfo)
        assert response.task_uid is not None
        task = index.wait_for_task(response.task_uid)
        assert task.customMetadata == "Test metadata"

        for document in to_delete:
            with pytest.raises(MeilisearchApiError):
                index.get_document(document)
        assert "The use of ids is depreciated" in str(w[0].message)


def test_delete_documents(index_with_documents):
    index = index_with_documents()
    response = index.update_filterable_attributes(["genre"])
    index.wait_for_task(response.task_uid)
    response = index.get_documents()
    assert "action" in ([x.__dict__.get("genre") for x in response.results])
    response = index.delete_documents(filter="genre=action", metadata="Test metadata")
    task = index.wait_for_task(response.task_uid)
    task.customMetadata = "Test metadata"

    response = index.get_documents()
    genres = [x.__dict__.get("genre") for x in response.results]
    assert "action" not in genres
    assert "cartoon" in genres


def test_delete_all_documents(index_with_documents):
    """Tests deleting all the documents in the index."""
    index = index_with_documents()
    response = index.delete_all_documents(metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.customMetadata == "Test metadata"
    response = index.get_documents()
    assert isinstance(response.results, list)
    assert response.results == []


def test_add_documents_csv(empty_index, songs_csv):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents_csv(songs_csv, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.customMetadata == "Test metadata"
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
    response = index.update_documents_csv(songs_csv, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert task.customMetadata == "Test metadata"
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
    response = index.add_documents_json(small_movies_json_file, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert task.customMetadata == "Test metadata"
    assert index.get_primary_key() == "id"


def test_update_documents_json(index_with_documents, small_movies_json_file):
    """Tests updating a single document with json string."""
    index = index_with_documents()
    response = index.update_documents_json(small_movies_json_file, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.customMetadata == "Test metadata"
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_add_documents_ndjson(empty_index, songs_ndjson):
    """Tests adding new documents to a clean index."""
    index = empty_index()
    response = index.add_documents_ndjson(songs_ndjson, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.customMetadata == "Test metadata"
    assert task.status == "succeeded"
    assert index.get_primary_key() == "id"


def test_update_documents_ndjson(index_with_documents, songs_ndjson):
    """Tests updating a single document with ndjson string."""
    index = index_with_documents()
    response = index.update_documents_ndjson(songs_ndjson, metadata="Test metadata")
    assert isinstance(response, TaskInfo)
    assert response.task_uid is not None
    task = index.wait_for_task(response.task_uid)
    assert task.status == "succeeded"
    assert task.customMetadata == "Test metadata"
    assert index.get_primary_key() == "id"


# Tests for skip_creation parameter
def test_add_documents_with_skip_creation_true(empty_index):
    """Tests that skip_creation=True prevents creation of new documents."""
    index = empty_index()
    documents = [
        {"id": "1", "title": "Existing Document"},
    ]

    # First add a document normally
    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

    # Verify document exists
    doc = index.get_document("1")
    assert doc.title == "Existing Document"

    # Now try to add a new document with skip_creation=True - should be ignored
    new_documents = [
        {"id": "2", "title": "New Document"},
    ]
    task = index.add_documents(new_documents, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Document "2" should not exist because skip_creation=True prevents creation of new documents
    with pytest.raises(MeilisearchApiError):
        index.get_document("2")

    # Existing document should still be there
    doc = index.get_document("1")
    assert doc.title == "Existing Document"


def test_add_documents_with_skip_creation_false(empty_index):
    """Tests that skip_creation=False allows creation of new documents (default behavior)."""
    index = empty_index()
    documents = [
        {"id": "1", "title": "New Document"},
    ]

    # Add document with skip_creation=False (should work same as default)
    task = index.add_documents(documents, skip_creation=False)
    index.wait_for_task(task.task_uid)

    # Document should exist
    doc = index.get_document("1")
    assert doc.title == "New Document"


def test_add_documents_skip_creation_updates_existing(empty_index):
    """Tests that skip_creation=True still allows updating existing documents."""
    index = empty_index()
    documents = [
        {"id": "1", "title": "Original Title"},
    ]

    # Add document initially
    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

    # Update with skip_creation=True - should update existing document
    updated_documents = [
        {"id": "1", "title": "Updated Title"},
    ]
    task = index.add_documents(updated_documents, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Document should be updated
    doc = index.get_document("1")
    assert doc.title == "Updated Title"


def test_update_documents_with_skip_creation_true(empty_index):
    """Tests that update_documents with skip_creation=True prevents creation of new documents."""
    index = empty_index()
    documents = [
        {"id": "1", "title": "Existing Document"},
    ]

    # First add a document
    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

    # Now try to update with a new document - should be ignored
    new_documents = [
        {"id": "2", "title": "New Document"},
    ]
    task = index.update_documents(new_documents, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Document "2" should not exist because skip_creation=True prevents creation of new documents
    with pytest.raises(MeilisearchApiError):
        index.get_document("2")

    # Existing document should still be there and unchanged
    doc = index.get_document("1")
    assert doc.title == "Existing Document"


def test_update_documents_skip_creation_updates_existing(empty_index):
    """Tests that update_documents with skip_creation=True still updates existing documents."""
    index = empty_index()
    documents = [
        {"id": "1", "title": "Original Title"},
    ]

    # Add document initially
    task = index.add_documents(documents)
    index.wait_for_task(task.task_uid)

    # Update with skip_creation=True - should update existing document
    updated_documents = [
        {"id": "1", "title": "Updated Title"},
    ]
    task = index.update_documents(updated_documents, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Document should be updated
    doc = index.get_document("1")
    assert doc.title == "Updated Title"


def test_add_documents_in_batches_with_skip_creation(empty_index, small_movies):
    """Tests that skip_creation parameter works with add_documents_in_batches."""
    index = empty_index()

    # Add some documents first
    initial_docs = small_movies[:5]
    task = index.add_documents(initial_docs)
    index.wait_for_task(task.task_uid)

    # Try to add more documents with skip_creation=True
    new_docs = small_movies[5:10]
    task = index.add_documents_in_batches(new_docs, batch_size=2, skip_creation=True)
    assert isinstance(task, list)
    for t in task:
        index.wait_for_task(t.task_uid)

    # Only original documents should exist
    all_docs = index.get_documents().results
    existing_ids = {doc.id for doc in all_docs}
    original_ids = {doc["id"] for doc in initial_docs}
    assert existing_ids == original_ids


def test_update_documents_in_batches_with_skip_creation(empty_index, small_movies):
    """Tests that skip_creation parameter works with update_documents_in_batches."""
    index = empty_index()

    # Add some documents first
    initial_docs = small_movies[:5]
    task = index.add_documents(initial_docs)
    index.wait_for_task(task.task_uid)

    # Try to update with new documents with skip_creation=True
    new_docs = small_movies[5:10]
    task = index.update_documents_in_batches(new_docs, batch_size=2, skip_creation=True)
    assert isinstance(task, list)
    for t in task:
        index.wait_for_task(t.task_uid)

    # Only original documents should exist
    all_docs = index.get_documents().results
    existing_ids = {doc.id for doc in all_docs}
    original_ids = {doc["id"] for doc in initial_docs}
    assert existing_ids == original_ids


def test_add_documents_json_with_skip_creation(empty_index, small_movies_json_file):
    """Tests that skip_creation parameter works with add_documents_json."""
    index = empty_index()
    documents = json.loads(small_movies_json_file.decode("utf-8"))

    # Add first document
    first_doc = json.dumps([documents[0]]).encode("utf-8")
    task = index.add_documents_json(first_doc)
    index.wait_for_task(task.task_uid)

    # Try to add new document with skip_creation=True
    new_doc = json.dumps([documents[1]]).encode("utf-8")
    task = index.add_documents_json(new_doc, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Only first document should exist
    all_docs = index.get_documents().results
    assert len(all_docs) == 1
    assert all_docs[0].id == documents[0]["id"]


def test_update_documents_json_with_skip_creation(empty_index, small_movies_json_file):
    """Tests that skip_creation parameter works with update_documents_json."""
    index = empty_index()
    documents = json.loads(small_movies_json_file.decode("utf-8"))

    # Add first document using add_documents (expects list of dicts)
    task = index.add_documents([documents[0]])
    index.wait_for_task(task.task_uid)

    # Try to update with new document with skip_creation=True
    # update_documents_json accepts bytes (like the fixture) or list of dicts
    # Create bytes like the fixture does
    new_doc = json.dumps([documents[1]]).encode("utf-8")
    task = index.update_documents_json(new_doc, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Only first document should exist
    all_docs = index.get_documents().results
    assert len(all_docs) == 1
    assert all_docs[0].id == documents[0]["id"]


def test_add_documents_csv_with_skip_creation(empty_index, songs_csv):
    """Tests that skip_creation parameter works with add_documents_csv."""
    index = empty_index()

    # Add first two lines (header + first data row) manually
    lines = songs_csv.split(b"\n")
    first_two_lines = b"\n".join(lines[:2]) + b"\n"
    task = index.add_documents_csv(first_two_lines)
    index.wait_for_task(task.task_uid)

    # Verify first document exists
    all_docs = index.get_documents().results
    initial_count = len(all_docs)
    assert initial_count == 1

    # Try to add more with skip_creation=True
    task = index.add_documents_csv(songs_csv, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Only first document should exist (no new ones created)
    all_docs = index.get_documents().results
    assert len(all_docs) == initial_count


def test_update_documents_csv_with_skip_creation(empty_index, songs_csv):
    """Tests that skip_creation parameter works with update_documents_csv."""
    index = empty_index()

    # Add first two lines (header + first data row) manually
    lines = songs_csv.split(b"\n")
    first_two_lines = b"\n".join(lines[:2]) + b"\n"
    task = index.add_documents_csv(first_two_lines)
    index.wait_for_task(task.task_uid)

    # Verify first document exists
    all_docs = index.get_documents().results
    initial_count = len(all_docs)
    assert initial_count == 1

    # Try to update with more with skip_creation=True
    task = index.update_documents_csv(songs_csv.decode("utf-8"), skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Only first document should exist (no new ones created)
    all_docs = index.get_documents().results
    assert len(all_docs) == initial_count


def test_add_documents_ndjson_with_skip_creation(empty_index, songs_ndjson):
    """Tests that skip_creation parameter works with add_documents_ndjson."""
    index = empty_index()

    # Add first line
    first_line = songs_ndjson.split(b"\n")[0] + b"\n"
    task = index.add_documents_ndjson(first_line)
    index.wait_for_task(task.task_uid)

    # Try to add more with skip_creation=True
    task = index.add_documents_ndjson(songs_ndjson, skip_creation=True)
    index.wait_for_task(task.task_uid)

    # Only first document should exist
    all_docs = index.get_documents().results
    assert len(all_docs) == 1
