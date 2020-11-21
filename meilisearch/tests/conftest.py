import json
from time import sleep
from pytest import fixture

from meilisearch.tests import clear_all_indexes, common
import meilisearch

@fixture(scope="session")
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
    # TODO: don't call other function, jsut do it here
    clear_all_indexes(client)


@fixture(scope="function")
def sample_indexes(client):
    indexes = []
    for index_args in common.index_fixture:
        indexes.append(client.create_index(**index_args))
    # Give the indexes to the test so it can use it
    yield indexes
    # tests finished, let's cleanup
    for index in indexes:
        try:
            index.delete()
        except meilisearch.errors.MeiliSearchApiError:
            # test deleted itself explicitly, pass
            pass


@fixture(scope="session")
def small_movies():
    with open('./datasets/small_movies.json', 'r') as movie_file:
        yield json.loads(movie_file.read())


@fixture(scope="function")
def indexed_small_movies(sample_indexes, small_movies):
    response = sample_indexes[0].add_documents(small_movies)
    sample_indexes[0].wait_for_pending_update(response['updateId'])
    # wait a bit for the index to build?
    # sleep(0.1)
    return sample_indexes
