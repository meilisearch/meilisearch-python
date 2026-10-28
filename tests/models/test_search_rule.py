from meilisearch.models.search_rule import SearchRule


def test_search_rule_parses_filter_condition_and_last_updated_at():
    response = {
        "uid": "red-shirts",
        "lastUpdatedAt": "2026-07-28T04:39:26Z",
        "active": True,
        "conditions": {
            "filter": {
                "values": {
                    "color": "red",
                    "category": "shirt",
                }
            }
        },
        "actions": {"pin": [{"id": "123", "position": 1}]},
    }

    rule = SearchRule(**response)

    assert rule.last_updated_at == response["lastUpdatedAt"]
    assert rule.conditions == response["conditions"]
