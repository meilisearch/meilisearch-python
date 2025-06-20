# pylint: disable=unnecessary-dunder-call

import pytest

from meilisearch.models.index import IndexStats


def test_getattr():
    document = IndexStats({"field1": "test 1", "fiels2": "test 2"})
    assert document.__getattr__("field1") == "test 1"


def test_getattr_not_found():
    document = IndexStats({"field1": "test 1", "fiels2": "test 2"})
    with pytest.raises(AttributeError):
        document.__getattr__("bad")


def test_iter():
    # I wrote a test what what this does, but I have a feeling this isn't actually what it was
    # expected to do when written as it doesn't really act like I would expect an iterator to act.
    document = IndexStats({"field1": "test 1", "fiels2": "test 2"})

    assert next(document.__iter__()) == (
        "_IndexStats__dict",
        {"field1": "test 1", "fiels2": "test 2"},
    )
