import json
from pytest import fixture

from meilisearch.tests import common
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
    indexes = client.get_indexes()
    for index in indexes:
        client.index(index['uid']).delete()


@fixture(scope="function")
def sample_indexes(client):
    indexes = []
    for index_args in common.index_fixture:
        indexes.append(client.create_index(**index_args))
    # yield the indexes to the test so it can use it
    yield indexes
    # test finished, let's cleanup
    for index in indexes:
        try:
            index.delete()
        except meilisearch.errors.MeiliSearchApiError:
            # test deleted index explicitly
            pass


@fixture(scope="session")
def small_movies():
    """
    Run once per session, provide the content of small_movies.json
     as a dictionary to the test.
    """
    with open('./datasets/small_movies.json', 'r') as movie_file:
        yield json.loads(movie_file.read())


@fixture(scope="function")
def indexed_small_movies(sample_indexes, small_movies):
    """
    Add small movies sample entries to the index(es)
    """
    response = sample_indexes[0].add_documents(small_movies)
    sample_indexes[0].wait_for_pending_update(response['updateId'])
    return sample_indexes
