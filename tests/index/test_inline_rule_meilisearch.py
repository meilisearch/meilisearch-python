"""Tests for inline dynamic search rule preview on search and multi-search."""

import pytest

import meilisearch
from tests import common

pytestmark = pytest.mark.usefixtures("enable_dynamic_search_rules", "inline_rule_index")

INDEX_UID = "inline_rule_preview"
TASK_TIMEOUT_MS = 30_000

DOCUMENTS = [
    {
        "id": "1",
        "title": "super hero",
        "hero": "superman",
        "color": "blue",
        "category": "shirt",
        "stock_intent": "keep",
    },
    {
        "id": "2",
        "title": "super hero",
        "hero": "batman",
        "color": "yellow",
        "category": "pants",
        "stock_intent": "destock",
    },
]


@pytest.fixture
def inline_rule_index(client):
    """Index with the attributes used by inline rule preview."""
    task = client.create_index(INDEX_UID, {"primaryKey": "id"})
    client.wait_for_task(task.task_uid, timeout_in_ms=TASK_TIMEOUT_MS)
    index = client.index(INDEX_UID)
    settings_task = index.update_filterable_attributes(
        ["color", "category", "stock_intent", "hero"]
    )
    index.wait_for_task(settings_task.task_uid, timeout_in_ms=TASK_TIMEOUT_MS)
    documents_task = index.add_documents(DOCUMENTS)
    index.wait_for_task(documents_task.task_uid, timeout_in_ms=TASK_TIMEOUT_MS)
    return index


@pytest.fixture
def metadata_client():
    """Client that asks Meilisearch to include search metadata."""
    return meilisearch.Client(
        common.BASE_URL,
        common.MASTER_KEY,
        custom_headers={"Meili-Include-Metadata": "true"},
    )


def test_search_with_inline_rule_pins_document_and_returns_condition_outcomes(metadata_client):
    """A satisfied inline pin rule reorders hits and reports condition outcomes."""
    response = metadata_client.index(INDEX_UID).search(
        "super hero",
        {
            "inlineRule": {
                "uid": "user-likes-batman",
                "conditions": {"query": {"words": "hero"}},
                "actions": {"pin": [{"id": "2", "position": 0}]},
            }
        },
    )

    assert response["hits"][0]["id"] == "2"
    metadata = response["metadata"]
    assert isinstance(metadata["queryUid"], str)
    assert metadata["indexUid"] == INDEX_UID
    assert metadata["primaryKey"] == "id"
    assert metadata["inlineRuleConditionOutcomes"] == {
        "satisfiesActiveCondition": True,
        "satisfiesQueryWordsCondition": "satisfied",
    }


def test_multi_search_with_inline_rule_returns_condition_outcomes(metadata_client):
    """Only the query that sends inlineRule includes condition outcomes."""
    query = {
        "indexUid": INDEX_UID,
        "q": "super hero",
        "filter": "color = blue AND category = shirt",
    }
    response = metadata_client.multi_search(
        [
            query,
            {
                **query,
                "inlineRule": {
                    "uid": "special-sales",
                    "conditions": {
                        "query": {"words": "pants"},
                        "filter": {
                            "values": {
                                "color": "yellow",
                                "stock_intent": "destock",
                            }
                        },
                    },
                },
            },
        ]
    )

    assert response["results"][0]["hits"] == response["results"][1]["hits"]
    assert "inlineRuleConditionOutcomes" not in response["results"][0].get("metadata", {})
    assert response["results"][1]["metadata"]["inlineRuleConditionOutcomes"] == {
        "satisfiesActiveCondition": True,
        "satisfiesQueryWordsCondition": {"missingWord": {"word": "pants"}},
        "satisfiesFilterCondition": {"unmetConstraintOnField": {"field": "color"}},
    }
