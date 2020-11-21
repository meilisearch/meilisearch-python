import json
from pytest import fixture

from meilisearch.tests import clear_all_indexes, common

@fixture(autouse=True)
def clear_indexes():
	"""
	Auto clear the indexes after each tetst function run.
	helps with identifying tests that are not independent.
	"""
	# Yield back to the test function
	yield
	# test function has finished, let's cleanup
	clear_all_indexes(common.client)


@fixture(scope="function")
def sample_indexes():
	indexes = []
	for index_args in common.index_fixture:
		indexes.append(common.client.create_index(**index_args))
	return indexes

@fixture(scope="session")
def small_movies():
	with open('./datasets/small_movies.json', 'r') as movie_file:
		yield json.loads(movie_file.read())
