# pylint: disable=invalid-name

from collections import Counter

import pytest


def test_basic_search(index_with_documents):
    """Tests search with a simple query."""
    response = index_with_documents().search("How to Train Your Dragon")
    assert isinstance(response, dict)
    assert response["hits"][0]["id"] == "166428"
    assert response["estimatedTotalHits"] is not None
    assert "hitsPerPage" is not response


def test_basic_search_with_empty_params(index_with_documents):
    """Tests search with a simple query and empty params."""
    response = index_with_documents().search("How to Train Your Dragon", {})
    assert isinstance(response, dict)
    assert response["hits"][0]["id"] == "166428"
    assert "_formatted" not in response["hits"][0]


def test_basic_search_with_empty_query(index_with_documents):
    """Tests search with an empty query and empty params."""
    response = index_with_documents().search("")
    assert isinstance(response, dict)
    assert len(response["hits"]) == 20
    assert response["query"] == ""


def test_basic_search_with_no_query(index_with_documents):
    """Tests search with no query [None] and empty params."""
    response = index_with_documents().search(None, {})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 20


def test_custom_search(index_with_documents):
    """Tests search with a simple query and a custom parameter (attributesToHighlight)."""
    response = index_with_documents().search("Dragon", {"attributesToHighlight": ["title"]})
    assert isinstance(response, dict)
    assert response["hits"][0]["id"] == "166428"
    assert "_formatted" in response["hits"][0]
    assert "dragon" in response["hits"][0]["_formatted"]["title"].lower()


def test_custom_search_with_empty_query(index_with_documents):
    """Tests search with an empty query and custom parameter (attributesToHighlight)."""
    response = index_with_documents().search("", {"attributesToHighlight": ["title"]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 20
    assert response["query"] == ""


def test_custom_search_with_no_query(index_with_documents):
    """Tests search with no query [None] and a custom parameter (limit)."""
    response = index_with_documents().search(None, {"limit": 5})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 5


def test_custom_search_params_with_wildcard(index_with_documents):
    """Tests search with '*' in query params."""
    response = index_with_documents().search(
        "a",
        {
            "limit": 5,
            "attributesToHighlight": ["*"],
            "attributesToRetrieve": ["*"],
            "attributesToCrop": ["*"],
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 5
    assert "_formatted" in response["hits"][0]
    assert "title" in response["hits"][0]["_formatted"]


def test_custom_search_params_with_simple_string(index_with_documents):
    """Tests search with a list of one string in query params."""
    response = index_with_documents().search(
        "a",
        {
            "limit": 5,
            "attributesToHighlight": ["title"],
            "attributesToRetrieve": ["title"],
            "attributesToCrop": ["title"],
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 5
    assert "_formatted" in response["hits"][0]
    assert "title" in response["hits"][0]["_formatted"]
    assert not "release_date" in response["hits"][0]["_formatted"]


def test_custom_search_params_with_string_list(index_with_documents):
    """Tests search with string list in query params."""
    response = index_with_documents().search(
        "a",
        {
            "limit": 5,
            "attributesToRetrieve": ["title", "overview"],
            "attributesToHighlight": ["title"],
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 5
    assert "title" in response["hits"][0]
    assert "overview" in response["hits"][0]
    assert not "release_date" in response["hits"][0]
    assert "title" in response["hits"][0]["_formatted"]
    assert "overview" in response["hits"][0]["_formatted"]


def test_custom_search_params_with_crop_marker(index_with_documents):
    """Tests search with a list of one string in query params."""
    response = index_with_documents().search(
        "dragon",
        {
            "limit": 1,
            "attributesToCrop": ["overview"],
            "cropLength": 10,
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "_formatted" in response["hits"][0]
    assert "overview" in response["hits"][0]["_formatted"]
    assert response["hits"][0]["_formatted"]["overview"].count(" ") < 10
    assert response["hits"][0]["_formatted"]["overview"].count("…") == 2


def test_custom_search_params_with_customized_crop_marker(index_with_documents):
    """Tests search with a list of one string in query params."""
    response = index_with_documents().search(
        "dragon",
        {
            "limit": 1,
            "attributesToCrop": ["overview"],
            "cropLength": 10,
            "cropMarker": "(ꈍᴗꈍ)",
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "_formatted" in response["hits"][0]
    assert "overview" in response["hits"][0]["_formatted"]
    assert response["hits"][0]["_formatted"]["overview"].count("(ꈍᴗꈍ)") == 2


def test_custom_search_params_with_highlight_tag(index_with_documents):
    """Tests search with a list of one string in query params."""
    response = index_with_documents().search(
        "dragon",
        {
            "limit": 1,
            "attributesToHighlight": ["*"],
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "_formatted" in response["hits"][0]
    assert "title" in response["hits"][0]["_formatted"]
    assert (
        response["hits"][0]["_formatted"]["title"]
        == "How to Train Your <em>Dragon</em>: The Hidden World"
    )


def test_custom_search_params_with_customized_highlight_tag(index_with_documents):
    """Tests search with a list of one string in query params."""
    response = index_with_documents().search(
        "dragon",
        {
            "limit": 1,
            "attributesToHighlight": ["*"],
            "highlightPreTag": "(⊃｡•́‿•̀｡)⊃ ",
            "highlightPostTag": " ⊂(´• ω •`⊂)",
        },
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "_formatted" in response["hits"][0]
    assert "title" in response["hits"][0]["_formatted"]
    assert (
        response["hits"][0]["_formatted"]["title"]
        == "How to Train Your (⊃｡•́‿•̀｡)⊃ Dragon ⊂(´• ω •`⊂): The Hidden World"
    )


def test_custom_search_params_with_facets_distribution(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"facets": ["genre"]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 12
    assert "facetDistribution" in response
    assert "genre" in response["facetDistribution"]
    assert response["facetDistribution"]["genre"]["cartoon"] == 1
    assert response["facetDistribution"]["genre"]["action"] == 3
    assert response["facetDistribution"]["genre"]["fantasy"] == 1


def test_custom_search_params_with_filter_string(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"filter": "genre = action"})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 3
    assert "facetDistribution" not in response


def test_custom_search_params_with_filter_string_with_space(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre"])
    index.wait_for_task(update.task_uid)
    response = index.search("galaxy", {"filter": "genre = 'sci fi'"})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "facetDistribution" not in response


def test_custom_search_params_with_multiple_filter_string_with_space(
    index_with_documents,
):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre", "release_date"])
    index.wait_for_task(update.task_uid)
    response = index.search("galaxy", {"filter": "genre = 'sci fi' AND release_date < 1550000000"})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "facetDistribution" not in response


def test_custom_search_params_with_array_filter_with_space(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre", "release_date"])
    index.wait_for_task(update.task_uid)
    response = index.search("galaxy", {"filter": ["genre = 'sci fi'", "release_date < 1550000000"]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "facetDistribution" not in response


def test_custom_search_params_with_mutilple_filter_string(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre", "release_date"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"filter": "genre = action AND release_date < 1550000000"})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 2
    assert "facetDistribution" not in response
    assert response["hits"][0]["title"] == "Avengers: Infinity War"


def test_custom_search_params_with_filter(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"filter": [["genre = action"]]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 3
    assert "facetDistribution" not in response


def test_custom_search_params_with_multiple_filter(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre"])
    index.wait_for_task(update.task_uid)
    response = index.search(
        "world", {"filter": ["genre = action", ["genre = action", "genre = action"]]}
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 3
    assert "facetDistribution" not in response


def test_custom_search_params_with_many_params(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(["genre"])
    index.wait_for_task(update.task_uid)
    response = index.search(
        "world",
        {"filter": [["genre = action"]], "attributesToRetrieve": ["title", "poster"]},
    )
    assert isinstance(response, dict)
    assert len(response["hits"]) == 3
    assert "facetDistribution" not in response
    assert "title" in response["hits"][0]
    assert "poster" in response["hits"][0]
    assert "overview" not in response["hits"][0]
    assert "release_date" not in response["hits"][0]
    assert response["hits"][0]["title"] == "Avengers: Infinity War"


def test_custom_search_params_with_sort_string(index_with_documents):
    index = index_with_documents()
    response = index.update_ranking_rules(
        ["words", "typo", "sort", "proximity", "attribute", "exactness"]
    )
    index.wait_for_task(response.task_uid)
    update = index.update_sortable_attributes(["title"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"sort": ["title:asc"]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 12
    assert "facetDistribution" not in response
    assert response["hits"][0]["title"] == "Alita: Battle Angel"
    assert response["hits"][1]["title"] == "Aquaman"


def test_custom_search_params_with_sort_int(index_with_documents):
    index = index_with_documents()
    response = index.update_ranking_rules(
        ["words", "typo", "sort", "proximity", "attribute", "exactness"]
    )
    index.wait_for_task(response.task_uid)
    update = index.update_sortable_attributes(["release_date"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"sort": ["release_date:asc"]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 12
    assert "facetDistribution" not in response
    assert response["hits"][0]["title"] == "Avengers: Infinity War"
    assert response["hits"][1]["title"] == "Redcon-1"


def test_custom_search_params_with_multiple_sort(index_with_documents):
    index = index_with_documents()
    response = index.update_ranking_rules(
        ["words", "typo", "sort", "proximity", "attribute", "exactness"]
    )
    index.wait_for_task(response.task_uid)
    update = index.update_sortable_attributes(["title", "release_date"])
    index.wait_for_task(update.task_uid)
    response = index.search("world", {"sort": ["title:asc", "release_date:asc"]})
    assert isinstance(response, dict)
    assert len(response["hits"]) == 12
    assert "facetDistribution" not in response
    assert response["hits"][0]["title"] == "Alita: Battle Angel"
    assert response["hits"][1]["title"] == "Aquaman"


def test_phrase_search(index_with_documents):
    response = index_with_documents().search('coco "dumbo"')
    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert "facetDistribution" not in response
    assert "title" in response["hits"][0]
    assert "poster" in response["hits"][0]
    assert "overview" in response["hits"][0]
    assert "release_date" in response["hits"][0]
    assert response["hits"][0]["title"] == "Dumbo"
    assert "_formatted" not in response["hits"][0]


def test_basic_search_on_nested_documents(index_with_documents, nested_movies):
    """Tests search with a simple query on nested fields."""
    response = index_with_documents("nested_fields_index", nested_movies).search("An awesome")
    assert isinstance(response, dict)
    assert response["hits"][0]["id"] == 5
    assert len(response["hits"]) == 1


def test_search_on_nested_documents_with_searchable_attributes(index_with_documents, nested_movies):
    """Tests search on nested fields with searchable attribute."""
    index = index_with_documents("nested_fields_index", nested_movies)
    response_searchable_attributes = index.update_searchable_attributes(["title", "info.comment"])
    index.wait_for_task(response_searchable_attributes.task_uid)
    response = index.search("An awesome")
    assert isinstance(response, dict)
    assert response["hits"][0]["id"] == 5
    assert len(response["hits"]) == 1


def test_search_on_nested_documents_with_sortable_attributes(index_with_documents, nested_movies):
    """Tests search on nested fields with searchable attribute and sortable attributes."""
    index = index_with_documents("nested_fields_index", nested_movies)
    response_settings = index.update_settings(
        {
            "searchableAttributes": ["title", "info.comment"],
            "sortableAttributes": ["info.reviewNb"],
        }
    )
    index.wait_for_task(response_settings.task_uid)
    response = index.search("", {"sort": ["info.reviewNb:desc"]})
    assert isinstance(response, dict)
    assert response["hits"][0]["id"] == 6


def test_custom_search_params_with_matching_strategy_all(index_with_documents):
    """Tests search with matching strategy param set to all"""
    response = index_with_documents().search(
        "man loves",
        {
            "limit": 5,
            "matchingStrategy": "all",
        },
    )

    assert isinstance(response, dict)
    assert len(response["hits"]) == 1


def test_custom_search_params_with_matching_strategy_last(index_with_documents):
    """Tests search with matching strategy param set to last"""
    response = index_with_documents().search(
        "man loves",
        {
            "limit": 5,
            "matchingStrategy": "last",
        },
    )

    assert isinstance(response, dict)
    assert len(response["hits"]) > 1


def test_custom_search_params_with_matching_strategy_frequency(index_with_documents):
    """Tests search with matching strategy param set to frequency"""
    response = index_with_documents().search(
        "man loves",
        {
            "limit": 5,
            "matchingStrategy": "frequency",
        },
    )

    assert isinstance(response, dict)
    assert len(response["hits"]) > 1


def test_custom_search_params_with_pagination_parameters(index_with_documents):
    """Tests search with matching strategy param set to last"""
    response = index_with_documents().search("", {"hitsPerPage": 1, "page": 1})

    assert isinstance(response, dict)
    assert len(response["hits"]) == 1
    assert response["hitsPerPage"] == 1
    assert response["page"] == 1
    assert response["totalPages"] is not None
    assert response["totalHits"] is not None
    assert "estimatedTotalHits" is not response


def test_custom_search_params_with_pagination_parameters_at_zero(index_with_documents):
    """Tests search with matching strategy param set to last"""
    response = index_with_documents().search("", {"hitsPerPage": 0, "page": 0})

    assert isinstance(response, dict)
    assert len(response["hits"]) == 0
    assert response["hitsPerPage"] == 0
    assert response["page"] == 0
    assert response["totalPages"] is not None
    assert response["totalHits"] is not None
    assert "estimatedTotalHits" is not response


def test_attributes_to_search_on_search(index_with_documents):
    response = index_with_documents().search(
        "How to Train Your Dragon", opt_params={"attributesToSearchOn": ["title", "overview"]}
    )
    assert response["hits"][0]["id"] == "166428"


def test_attributes_to_search_on_search_no_match(index_with_documents):
    response = index_with_documents().search(
        "How to Train Your Dragon", opt_params={"attributesToSearchOn": ["id"]}
    )
    assert response["hits"] == []


def test_show_ranking_score_details(index_with_documents):
    """Tests search with show ranking score details"""
    response = index_with_documents().search(
        "man loves",
        {"showRankingScoreDetails": True},
    )

    assert isinstance(response, dict)
    assert len(response["hits"]) > 1
    assert response["hits"][0]["_rankingScoreDetails"] is not None
    assert response["hits"][0]["_rankingScoreDetails"]["words"] is not None
    assert response["hits"][0]["_rankingScoreDetails"]["words"]["score"] == 1


def test_show_ranking_score(index_with_documents):
    """Tests search with show ranking score"""
    response = index_with_documents().search(
        "man loves",
        {"showRankingScore": True},
    )

    assert isinstance(response, dict)
    assert len(response["hits"]) > 1
    assert response["hits"][0]["_rankingScore"] is not None
    assert response["hits"][0]["_rankingScore"] >= 0.9


def test_vector_search(index_with_documents_and_vectors):
    """Tests vector search with hybrid parameters."""
    response = index_with_documents_and_vectors().search(
        "",
        opt_params={"vector": [0.1, 0.2], "hybrid": {"semanticRatio": 1.0, "embedder": "default"}},
    )
    assert len(response["hits"]) > 0
    # Check that semanticHitCount field is present in the response
    assert "semanticHitCount" in response
    # With semanticRatio = 1.0, all hits should be semantic
    assert response["semanticHitCount"] == len(response["hits"])


def test_hybrid_search(index_with_documents_and_vectors):
    """Tests hybrid search with semantic ratio and embedder."""
    response = index_with_documents_and_vectors().search(
        "movie", opt_params={"hybrid": {"semanticRatio": 0.5, "embedder": "default"}}
    )
    assert len(response["hits"]) > 0
    # Check that semanticHitCount field is present in the response
    assert "semanticHitCount" in response
    # semanticHitCount should be an integer
    assert isinstance(response["semanticHitCount"], int)


def test_search_distinct(index_with_documents):
    index_with_documents().update_filterable_attributes(["genre"])
    response = index_with_documents().search("with", {"distinct": "genre"})
    genres = dict(Counter([x.get("genre") for x in response["hits"]]))
    assert isinstance(response, dict)
    assert len(response["hits"]) == 11
    assert genres == {None: 9, "action": 1, "Sci Fi": 1}
    assert response["hits"][0]["id"] == "399579"


@pytest.mark.parametrize(
    "query, ranking_score_threshold, expected",
    (
        ("Husband and wife", 1, 0),
        ("Husband and wife", 0.9, 1),
        ("wife", 0.9, 0),
        ("wife", 0.5, 2),
    ),
)
def test_search_ranking_threshold(query, ranking_score_threshold, expected, index_with_documents):
    response = index_with_documents().search(
        query, {"rankingScoreThreshold": ranking_score_threshold}
    )
    assert len(response["hits"]) == expected


def test_vector_search_with_retrieve_vectors(index_with_documents_and_vectors):
    """Tests vector search with retrieveVectors parameter."""
    response = index_with_documents_and_vectors().search(
        "",
        opt_params={
            "vector": [0.1, 0.2],
            "retrieveVectors": True,
            "hybrid": {"semanticRatio": 1.0, "embedder": "default"},
        },
    )
    assert len(response["hits"]) > 0
    # Check that the first hit has a _vectors field
    assert "_vectors" in response["hits"][0]
    # Check that the _vectors field contains the default embedder
    assert "default" in response["hits"][0]["_vectors"]


def test_get_similar_documents_with_identical_vectors(empty_index):
    """Tests get_similar_documents method with documents having identical vectors."""
    # Create documents with identical vector embeddings
    identical_vector = [0.5, 0.5]
    documents = [
        {"id": "doc1", "title": "Document 1", "_vectors": {"default": identical_vector}},
        {"id": "doc2", "title": "Document 2", "_vectors": {"default": identical_vector}},
        {"id": "doc3", "title": "Document 3", "_vectors": {"default": identical_vector}},
        # Add a document with a different vector to verify it's not returned first
        {"id": "doc4", "title": "Document 4", "_vectors": {"default": [0.1, 0.1]}},
    ]

    # Set up the index with the documents
    index = empty_index()

    # Configure the embedder
    settings_update_task = index.update_embedders(
        {
            "default": {
                "source": "userProvided",
                "dimensions": 2,
            }
        }
    )
    index.wait_for_task(settings_update_task.task_uid)

    # Add the documents
    document_addition_task = index.add_documents(documents)
    index.wait_for_task(document_addition_task.task_uid)

    # Test get_similar_documents with doc1
    response = index.get_similar_documents({"id": "doc1", "embedder": "default"})

    # Verify response structure
    assert isinstance(response, dict)
    assert "hits" in response
    assert len(response["hits"]) >= 2  # Should find at least doc2 and doc3
    assert "id" in response
    assert response["id"] == "doc1"

    # Verify that doc2 and doc3 are in the results (they have identical vectors to doc1)
    result_ids = [hit["id"] for hit in response["hits"]]
    assert "doc2" in result_ids
    assert "doc3" in result_ids

    # Verify that doc4 is not the first result (it has a different vector)
    if "doc4" in result_ids:
        assert result_ids[0] != "doc4"
