from datetime import datetime

from meilisearch.models.search_rule import SearchRule

RULE_RESPONSE = {
    "uid": "black-friday",
    "active": True,
    "conditions": {"query": {"words": "black friday"}},
    "actions": [],
}


def test_search_rule_parses_last_updated_at():
    rule = SearchRule(
        **RULE_RESPONSE,
        lastUpdatedAt="2026-07-27T06:47:12.123456789Z",
    )

    assert rule.last_updated_at == datetime(2026, 7, 27, 6, 47, 12, 123456)


def test_search_rule_accepts_response_without_last_updated_at():
    rule = SearchRule(**RULE_RESPONSE)

    assert rule.last_updated_at is None
