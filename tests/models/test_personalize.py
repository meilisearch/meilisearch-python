from unittest.mock import MagicMock

import pytest
from pydantic import ValidationError

from meilisearch.config import Config
from meilisearch.index import Index
from meilisearch.models.index import PersonalizeSearch


def _make_index() -> Index:
    index = Index(Config("http://localhost:7700", "masterKey"), "movies")
    index.http = MagicMock()
    index.http.post.return_value = {"hits": []}
    return index


def test_personalize_search_model_dump_by_alias():
    personalize = PersonalizeSearch(user_context="The user prefers...")
    assert personalize.model_dump(by_alias=True) == {"userContext": "The user prefers..."}


def test_personalize_search_model_requires_user_context():
    with pytest.raises(ValidationError):
        PersonalizeSearch()


def test_personalize_search_model_from_camel_case_dict():
    personalize = PersonalizeSearch(**{"userContext": "kept as-is"})
    assert personalize.user_context == "kept as-is"


def test_personalize_search_model_from_snake_case_dict():
    personalize = PersonalizeSearch(**{"user_context": "snake"})
    assert personalize.user_context == "snake"


def test_search_serializes_personalize_model_to_post_body():
    index = _make_index()

    index.search("query", personalize=PersonalizeSearch(user_context="prefers sci-fi"))

    index.http.post.assert_called_once_with(
        "indexes/movies/search",
        body={"q": "query", "personalize": {"userContext": "prefers sci-fi"}},
    )


def test_search_serializes_personalize_dict_to_post_body():
    index = _make_index()

    index.search("query", personalize={"userContext": "prefers sci-fi"})

    index.http.post.assert_called_once_with(
        "indexes/movies/search",
        body={"q": "query", "personalize": {"userContext": "prefers sci-fi"}},
    )
