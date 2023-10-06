# pylint: disable=invalid-name


def test_basic_facet_search(index_with_documents_and_facets):
    """Tests facet search with a simple query."""
    response = index_with_documents_and_facets().facet_search("genre", "cartoon")
    assert isinstance(response, dict)
    assert response["facetHits"][0]["count"] == 3
    assert response["facetQuery"] == "cartoon"


def test_facet_search_with_empty_query(index_with_documents_and_facets):
    """Tests facet search with a empty query."""
    response = index_with_documents_and_facets().facet_search("genre")
    assert isinstance(response, dict)
    assert len(response["facetHits"]) == 4
    assert response["facetHits"][0]["value"] == "action"
    assert response["facetHits"][1]["count"] == 3
    assert response["facetQuery"] is None


def test_facet_search_with_q(index_with_documents_and_facets):
    """Tests facet search with a keyword query q."""
    response = index_with_documents_and_facets().facet_search("genre", "cartoon", {"q": "dragon"})
    assert isinstance(response, dict)
    assert response["facetHits"][0]["count"] == 1
    assert response["facetQuery"] == "cartoon"


def test_facet_search_with_filter(index_with_documents_and_facets):
    """Tests facet search with a filter."""
    index = index_with_documents_and_facets()
    task = index.update_filterable_attributes(["genre", "release_date"])
    index.wait_for_task(task.task_uid)
    response = index.facet_search("genre", "cartoon", {"filter": "release_date > 1149728400"})
    assert isinstance(response, dict)
    assert response["facetHits"][0]["count"] == 2
    assert response["facetQuery"] == "cartoon"


def test_facet_search_with_attributes_to_search_on(index_with_documents_and_facets):
    """Tests facet search with optional parameter attributesToSearchOn."""
    response = index_with_documents_and_facets().facet_search(
        "genre", "action", {"q": "aquaman", "attributesToSearchOn": ["overview"]}
    )
    assert isinstance(response, dict)
    assert len(response["facetHits"]) == 0
    assert response["facetQuery"] == "action"
