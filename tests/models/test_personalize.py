import pytest
from pydantic import ValidationError

from meilisearch.models.index import PersonalizeSearch


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
