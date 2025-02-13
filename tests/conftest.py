# pylint: disable=redefined-outer-name
import json
from typing import Optional

import requests
from pytest import fixture

import meilisearch
from meilisearch.errors import MeilisearchApiError
from meilisearch.models.index import OpenAiEmbedder, UserProvidedEmbedder
from tests import common


@fixture(scope="session")
def client():
    return meilisearch.Client(common.BASE_URL, common.MASTER_KEY)


@fixture(autouse=True)
def clear_indexes(client):
    """
    Auto-clears the indexes after each test function run.
    Makes all the test functions independent.
    """
    # Yields back to the test function.
    yield
    # Deletes all the indexes in the Meilisearch instance.
    indexes = client.get_indexes()
    for index in indexes["results"]:
        task = client.index(index.uid).delete()
        client.wait_for_task(task.task_uid)


@fixture(autouse=True)
def clear_all_tasks(client):
    """
    Auto-clears the tasks after each test function run.
    Makes all the test functions independent.
    """
    client.delete_tasks({"statuses": ["succeeded", "failed", "canceled"]})


@fixture(scope="function")
def indexes_sample(client):
    indexes = []
    for index_args in common.INDEX_FIXTURE:
        task = client.create_index(**index_args)
        client.wait_for_task(task.task_uid)
        indexes.append(client.get_index(index_args["uid"]))
    # Yields the indexes to the test to make them accessible.
    yield indexes


@fixture(scope="session")
def small_movies():
    """
    Runs once per session. Provides the content of small_movies.json.
    """
    with open("./datasets/small_movies.json", encoding="utf-8") as movie_file:
        yield json.loads(movie_file.read())


@fixture(scope="session")
def small_movies_json_file():
    """
    Runs once per session. Provides the content of small_movies.json from read.
    """
    with open("./datasets/small_movies.json", encoding="utf-8") as movie_json_file:
        return movie_json_file.read().encode("utf-8")


@fixture(scope="session")
def songs_csv():
    """
    Runs once per session. Provides the content of songs.csv from read.
    """
    with open("./datasets/songs.csv", encoding="utf-8") as song_csv_file:
        return song_csv_file.read().encode("utf-8")


@fixture(scope="session")
def songs_csv_custom_separator():
    """
    Runs once per session. Provides the content of songs_custom_delimiter.csv from read.
    """
    with open("./datasets/songs_custom_delimiter.csv", encoding="utf-8") as song_csv_file:
        return song_csv_file.read().encode("utf-8")


@fixture(scope="session")
def songs_ndjson():
    """
    Runs once per session. Provides the content of songs.ndjson from read.
    """
    with open("./datasets/songs.ndjson", encoding="utf-8") as song_ndjson_file:
        return song_ndjson_file.read().encode("utf-8")


@fixture(scope="session")
def nested_movies():
    """
    Runs once per session. Provides the content of nested_movies.json.
    """
    with open("./datasets/nested_movies.json", encoding="utf-8") as nested_movie_file:
        yield json.loads(nested_movie_file.read())


@fixture(scope="function")
def empty_index(client, index_uid: Optional[str] = None):
    index_uid = index_uid if index_uid else common.INDEX_UID

    def index_maker(index_uid=index_uid):
        task = client.create_index(uid=index_uid)
        client.wait_for_task(task.task_uid)
        return client.get_index(uid=index_uid)

    return index_maker


@fixture(scope="function")
def index_with_documents(empty_index, small_movies):
    def index_maker(index_uid=common.INDEX_UID, documents=small_movies):
        index = empty_index(index_uid)
        task = index.add_documents(documents)
        index.wait_for_task(task.task_uid)
        return index

    return index_maker


@fixture(scope="function")
def index_with_documents_and_vectors(empty_index, small_movies):
    small_movies[0]["_vectors"] = {"default": [0.1, 0.2]}
    for movie in small_movies[1:]:
        movie["_vectors"] = {"default": [0.9, 0.9]}

    def index_maker(index_uid=common.INDEX_UID, documents=small_movies):
        index = empty_index(index_uid)
        settings_update_task = index.update_embedders(
            {
                "default": {
                    "source": "userProvided",
                    "dimensions": 2,
                }
            }
        )
        index.wait_for_task(settings_update_task.task_uid)
        document_addition_task = index.add_documents(documents)
        index.wait_for_task(document_addition_task.task_uid)
        return index

    return index_maker


@fixture(scope="function")
def index_with_documents_and_facets(empty_index, small_movies):
    def index_maker(index_uid=common.INDEX_UID, documents=small_movies):
        index = empty_index(index_uid)
        task_1 = index.update_filterable_attributes(["genre"])
        index.wait_for_task(task_1.task_uid)
        task_2 = index.add_documents(documents)
        index.wait_for_task(task_2.task_uid)
        return index

    return index_maker


@fixture(scope="function")
def test_key(client):
    key_info = {
        "description": "test",
        "actions": ["search"],
        "indexes": ["movies"],
        "expiresAt": None,
    }

    key = client.create_key(key_info)

    yield key

    try:
        client.delete_key(key.key)
    except MeilisearchApiError:
        pass


@fixture(scope="function")
def test_key_info(client):
    key_info = {
        "name": "testKeyName",
        "description": "test",
        "actions": ["search"],
        "indexes": [common.INDEX_UID],
        "expiresAt": None,
    }

    yield key_info

    try:
        keys = client.get_keys().results
        key = next(x for x in keys if x.description == key_info["description"])
        client.delete_key(key.key)
    except MeilisearchApiError:
        pass
    except StopIteration:
        pass


@fixture(scope="function")
def get_private_key(client):
    keys = client.get_keys().results
    key = next(x for x in keys if "Default Search API" in x.name)
    return key


@fixture
def enable_vector_search():
    requests.patch(
        f"{common.BASE_URL}/experimental-features",
        headers={"Authorization": f"Bearer {common.MASTER_KEY}"},
        json={"vectorStore": True},
        timeout=10,
    )
    yield
    requests.patch(
        f"{common.BASE_URL}/experimental-features",
        headers={"Authorization": f"Bearer {common.MASTER_KEY}"},
        json={"vectorStore": False},
        timeout=10,
    )


@fixture
def enable_edit_documents_by_function():
    requests.patch(
        f"{common.BASE_URL}/experimental-features",
        headers={"Authorization": f"Bearer {common.MASTER_KEY}"},
        json={"editDocumentsByFunction": True},
        timeout=10,
    )
    yield
    requests.patch(
        f"{common.BASE_URL}/experimental-features",
        headers={"Authorization": f"Bearer {common.MASTER_KEY}"},
        json={"editDocumentsByFunction": False},
        timeout=10,
    )


@fixture
def new_embedders():
    return {
        "default": UserProvidedEmbedder(dimensions=1).model_dump(by_alias=True),
        "open_ai": OpenAiEmbedder().model_dump(by_alias=True),
    }
