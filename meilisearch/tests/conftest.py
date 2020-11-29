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
    Auto clear the indexes after each tetst function run.
    helps with identifying tests that are not independent.
    """
    # Yield back to the test function
    yield
    # test function has finished, let's cleanup
    indexes = client.get_indexes()
    for index in indexes:
        client.index(index['uid']).delete()


@fixture(scope='function')
def indexes_sample(client):
    indexes = []
    for index_args in common.INDEX_FIXTURE:
        indexes.append(client.create_index(**index_args))
    # yield the indexes to the test so it can use it
    yield indexes


@fixture(scope='session')
def small_movies():
    """
    Run once per session, provide the content of small_movies.json
     as a dictionary to the test.
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
