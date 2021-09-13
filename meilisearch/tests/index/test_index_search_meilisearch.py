# pylint: disable=invalid-name

def test_basic_search(index_with_documents):
    """Tests search with an simple query."""
    response = index_with_documents().search('How to Train Your Dragon')
    assert isinstance(response, dict)
    assert response['hits'][0]['id'] == '166428'

def test_basic_search_with_empty_params(index_with_documents):
    """Tests search with a simple query and empty params."""
    response = index_with_documents().search('How to Train Your Dragon', {})
    assert isinstance(response, dict)
    assert response['hits'][0]['id'] == '166428'
    assert '_formatted' not in response['hits'][0]

def test_basic_search_with_empty_query(index_with_documents):
    """Tests search with an empty query and empty params."""
    response = index_with_documents().search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_basic_search_with_no_query(index_with_documents):
    """Tests search with no query [None] and empty params."""
    response = index_with_documents().search(None, {})
    assert isinstance(response, dict)
    assert len(response['hits']) == 20

def test_custom_search(index_with_documents):
    """Tests search with a simple query and a custom parameter (attributesToHighlight)."""
    response = index_with_documents().search(
        'Dragon',
        {
            'attributesToHighlight': ['title']
        }
    )
    assert isinstance(response, dict)
    assert response['hits'][0]['id'] == '166428'
    assert '_formatted' in response['hits'][0]
    assert 'dragon' in response['hits'][0]['_formatted']['title'].lower()

def test_custom_search_with_empty_query(index_with_documents):
    """Tests search with an empty query and custom parameter (attributesToHighlight)."""
    response = index_with_documents().search(
        '',
        {
            'attributesToHighlight': ['title']
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_custom_search_with_no_query(index_with_documents):
    """Tests search with no query [None] and a custom parameter (limit)."""
    response = index_with_documents().search(
        None,
        {
            'limit': 5
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 5

def test_custom_search_params_with_wildcard(index_with_documents):
    """Tests search with '*' in query params."""
    response = index_with_documents().search(
        'a',
        {
            'limit': 5,
            'attributesToHighlight': ['*'],
            'attributesToRetrieve': ['*'],
            'attributesToCrop': ['*'],
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 5
    assert '_formatted' in response['hits'][0]
    assert "title" in response['hits'][0]['_formatted']

def test_custom_search_params_with_simple_string(index_with_documents):
    """Tests search with a list of one string in query params."""
    response = index_with_documents().search(
        'a',
        {
            'limit': 5,
            'attributesToHighlight': ['title'],
            'attributesToRetrieve': ['title'],
            'attributesToCrop': ['title'],
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 5
    assert '_formatted' in response['hits'][0]
    assert 'title' in response['hits'][0]['_formatted']
    assert not 'release_date' in response['hits'][0]['_formatted']

def test_custom_search_params_with_string_list(index_with_documents):
    """Tests search with string list in query params."""
    response = index_with_documents().search(
        'a',
        {
            'limit': 5,
            'attributesToRetrieve': ['title', 'overview'],
            'attributesToHighlight': ['title'],
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 5
    assert 'title' in response['hits'][0]
    assert 'overview' in response['hits'][0]
    assert not 'release_date' in response['hits'][0]
    assert 'title' in response['hits'][0]['_formatted']
    assert 'overview' in response['hits'][0]['_formatted']

def test_custom_search_params_with_facets_distribution(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(['genre'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'facetsDistribution': ['genre']
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 12
    assert 'facetsDistribution' in response
    assert 'exhaustiveFacetsCount' in response
    assert not response['exhaustiveFacetsCount']
    assert 'genre' in response['facetsDistribution']
    assert response['facetsDistribution']['genre']['cartoon'] == 1
    assert response['facetsDistribution']['genre']['action'] == 3
    assert response['facetsDistribution']['genre']['fantasy'] == 1

def test_custom_search_params_with_filter_string(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(['genre'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'filter': 'genre = action'
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 3
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response

def test_custom_search_params_with_mutilple_filter_string(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(['genre', 'release_date'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'filter': 'genre = action AND release_date < 1550000000'
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 2
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response
    assert response['hits'][0]['title'] == 'Avengers: Infinity War'

def test_custom_search_params_with_filter(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(['genre'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'filter': [['genre = action']]
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 3
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response

def test_custom_search_params_with_multiple_filter(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(['genre'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'filter': ['genre = action', ['genre = action', 'genre = action']]
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 3
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response

def test_custom_search_params_with_many_params(index_with_documents):
    index = index_with_documents()
    update = index.update_filterable_attributes(['genre'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'filter': [['genre = action']],
            'attributesToRetrieve': ['title', 'poster']
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 3
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response
    assert 'title' in response['hits'][0]
    assert 'poster' in response['hits'][0]
    assert 'overview' not in response['hits'][0]
    assert 'release_date' not in response['hits'][0]
    assert response['hits'][0]['title'] == 'Avengers: Infinity War'

def test_custom_search_params_with_sort_string(index_with_documents):
    index = index_with_documents()
    response = index.update_ranking_rules([
        'words',
        'typo',
        'sort',
        'proximity',
        'attribute',
        'exactness'
    ])
    index.wait_for_pending_update(response['updateId'])
    update = index.update_sortable_attributes(['title'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'sort': ['title:asc']
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 12
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response
    assert response['hits'][0]['title'] == 'Alita: Battle Angel'
    assert response['hits'][1]['title'] == 'Aquaman'

def test_custom_search_params_with_sort_int(index_with_documents):
    index = index_with_documents()
    response = index.update_ranking_rules([
        'words',
        'typo',
        'sort',
        'proximity',
        'attribute',
        'exactness'
    ])
    index.wait_for_pending_update(response['updateId'])
    update = index.update_sortable_attributes(['release_date'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'sort': ['release_date:asc']
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 12
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response
    assert response['hits'][0]['title'] == 'Avengers: Infinity War'
    assert response['hits'][1]['title'] == 'Redcon-1'

def test_custom_search_params_with_multiple_sort(index_with_documents):
    index = index_with_documents()
    response = index.update_ranking_rules([
        'words',
        'typo',
        'sort',
        'proximity',
        'attribute',
        'exactness'
    ])
    index.wait_for_pending_update(response['updateId'])
    update = index.update_sortable_attributes(['title', 'release_date'])
    index.wait_for_pending_update(update['updateId'])
    response = index.search(
        'world',
        {
            'sort': ['title:asc', 'release_date:asc']
        }
    )
    assert isinstance(response, dict)
    assert len(response['hits']) == 12
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response
    assert response['hits'][0]['title'] == 'Alita: Battle Angel'
    assert response['hits'][1]['title'] == 'Aquaman'

def test_phrase_search(index_with_documents):
    response = index_with_documents().search('coco "dumbo"')
    assert isinstance(response, dict)
    assert len(response['hits']) == 1
    assert 'facetsDistribution' not in response
    assert 'exhaustiveFacetsCount' not in response
    assert 'title' in response['hits'][0]
    assert 'poster' in response['hits'][0]
    assert 'overview' in response['hits'][0]
    assert 'release_date' in response['hits'][0]
    assert response['hits'][0]['title'] == 'Dumbo'
    assert '_formatted' not in response['hits'][0]
