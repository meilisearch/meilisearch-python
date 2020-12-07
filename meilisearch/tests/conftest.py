# pylint: disable=redefined-outer-name
import json
from pytest import fixture

from meilisearch.tests import common
import meilisearch

@fixture(scope='session')
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
    # Deletes all the indexes in the MeiliSearch instance.
    indexes = client.get_indexes()
    for index in indexes:
        client.index(index['uid']).delete()

@fixture(scope='function')
def indexes_sample(client):
    indexes = []
    for index_args in common.INDEX_FIXTURE:
        indexes.append(client.create_index(**index_args))
    # Yields the indexes to the test to make them accessible.
    yield indexes

@fixture(scope='session')
def small_movies():
    """
    Runs once per session. Provides the content of small_movies.json.
    """
    with open('./datasets/small_movies.json', 'r') as movie_file:
        yield json.loads(movie_file.read())

@fixture(scope='function')
def empty_index(client):
    def index_maker(index_name=common.INDEX_UID):
        return client.create_index(uid=index_name)
    return index_maker

@fixture(scope='function')
def index_with_documents(empty_index, small_movies):
    def index_maker(index_name=common.INDEX_UID, documents=small_movies):
        index = empty_index(index_name)
        response = index.add_documents(documents)
        index.wait_for_pending_update(response['updateId'])
        return index
    return index_maker
