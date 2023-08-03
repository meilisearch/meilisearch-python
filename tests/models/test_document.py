# pylint: disable=unnecessary-dunder-call


import pytest

from meilisearch.models.document import Document


def test_getattr():
    document = Document({"field1": "test 1", "fiels2": "test 2"})
    assert document.__getattr__("field1") == "field1"


def test_getattr_not_found():
    document = Document({"field1": "test 1", "fiels2": "test 2"})
    with pytest.raises(AttributeError):
        document.__getattr__("bad")


def test_iter():
    # I wrote a test what what this does, but I have a feeling this isn't actually what it was
    # expected to do when written as it doesn't really act like I would expect an iterator to act.
    document = Document({"field1": "test 1", "fiels2": "test 2"})

    assert next(document.__iter__()) == (
        "_Document__doc",
        {"field1": "test 1", "fiels2": "test 2"},
    )
