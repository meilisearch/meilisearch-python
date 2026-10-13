"""Unit tests for inlineRule support on search and multi-search.

These tests verify that the parameter is correctly forwarded in the request
body. Full integration requires Meilisearch Enterprise + experimental feature.
"""

from unittest.mock import MagicMock

from meilisearch.client import Client
from meilisearch.index import Index


def test_search_passes_inline_rule():
    """inlineRule is included in the search request body."""
    config = MagicMock()
    config.paths.index = "indexes"
    config.paths.search = "search"
    index = Index(config, "movies")
    index.http = MagicMock()
    index.http.post.return_value = {"hits": []}

    inline_rule = {
        "uid": "user-likes-batman",
        "actions": {"scale": [{"filter": "hero = batman", "weight": 1.2}]},
    }
    index.search("super hero", opt_params={"inlineRule": inline_rule})

    index.http.post.assert_called_once()
    call_args = index.http.post.call_args
    if call_args.kwargs and "body" in call_args.kwargs:
        body = call_args.kwargs["body"]
    else:
        body = call_args.args[1] if len(call_args.args) > 1 else call_args[1].get("body")
    assert body["q"] == "super hero"
    assert body["inlineRule"] == inline_rule


def test_multi_search_passes_inline_rule():
    """inlineRule is included in multi-search query objects."""
    client = Client("http://localhost:7700", "masterKey")
    client.http = MagicMock()
    client.http.post.return_value = {"results": []}

    queries = [
        {"indexUid": "products", "q": "fashion"},
        {
            "indexUid": "products",
            "q": "fashion",
            "inlineRule": {"uid": "special-sales"},
        },
    ]
    client.multi_search(queries)

    client.http.post.assert_called_once()
    call_args = client.http.post.call_args
    if call_args.kwargs and "body" in call_args.kwargs:
        body = call_args.kwargs["body"]
    else:
        body = call_args.args[1] if len(call_args.args) > 1 else call_args[1].get("body")
    assert body["queries"] == queries
    assert body["queries"][1]["inlineRule"]["uid"] == "special-sales"
