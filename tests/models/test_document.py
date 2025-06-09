# pylint: disable=unnecessary-dunder-call


import pytest

from meilisearch.models.document import Document


def test_doc_init():
    d = {"field1": "test 1", "field2": "test 2"}
    document = Document(d)
    assert dict(document) == d


def test_getattr():
    document = Document({"field1": "test 1", "field2": "test 2"})
    assert document.__getattr__("field1") == "test 1"


def test_getattr_not_found():
    document = Document({"field1": "test 1", "field2": "test 2"})
    with pytest.raises(AttributeError):
        document.__getattr__("bad")


def test_iter():
    document = Document({"field1": "test 1", "field2": "test 2"})
    assert list(iter(document)) == [("field1", "test 1"), ("field2", "test 2")]
