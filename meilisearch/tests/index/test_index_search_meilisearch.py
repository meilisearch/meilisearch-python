
class TestSearch:

    """ TESTS: search route """

    def test_basic_search(self, indexed_small_movies):
        """Tests search with an simple query"""
        response = indexed_small_movies[0].search('How to Train Your Dragon')
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'

    def test_basic_search_with_empty_params(self, indexed_small_movies):
        """Tests search with an simple query and empty params"""
        response = indexed_small_movies[0].search('How to Train Your Dragon', {})
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'
        assert '_formatted' not in response['hits'][0]

    def test_basic_search_with_empty_query(self, indexed_small_movies):
        """Tests search with empty query and empty params"""
        response = indexed_small_movies[0].search('')
        assert isinstance(response, object)
        assert len(response['hits']) == 20
        assert response['query'] == ''

    def test_basic_search_with_placeholder(self, indexed_small_movies):
        """Tests search with no query [None] and empty params"""
        response = indexed_small_movies[0].search(None, {})
        assert isinstance(response, object)
        assert len(response['hits']) == 20

    def test_custom_search(self, indexed_small_movies):
        """Tests search with an simple query and custom parameter (attributesToHighlight)"""
        response = indexed_small_movies[0].search(
            'Dragon',
            {
                'attributesToHighlight': ['title']
            }
        )
        assert isinstance(response, object)
        assert response['hits'][0]['id'] == '166428'
        assert '_formatted' in response['hits'][0]
        assert 'dragon' in response['hits'][0]['_formatted']['title'].lower()

    def test_custom_search_with_empty_query(self, indexed_small_movies):
        """Tests search with empty query and custom parameter (attributesToHighlight)"""
        response = indexed_small_movies[0].search(
            '',
            {
                'attributesToHighlight': ['title']
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 20
        assert response['query'] == ''

    def test_custom_search_with_placeholder(self, indexed_small_movies):
        """Tests search with no query [None] and custom parameter (limit)"""
        response = indexed_small_movies[0].search(
            None,
            {
                'limit': 5
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 5

    def test_custom_search_params_with_wildcard(self, indexed_small_movies):
        """Tests search with '*' in query params"""
        response = indexed_small_movies[0].search(
            'a',
            {
                'limit': 5,
                'attributesToHighlight': ['*'],
                'attributesToRetrieve': ['*'],
                'attributesToCrop': ['*'],
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 5
        assert '_formatted' in response['hits'][0]
        assert "title" in response['hits'][0]['_formatted']

    def test_custom_search_params_with_simple_string(self, indexed_small_movies):
        """Tests search with simple string in query params"""
        response = indexed_small_movies[0].search(
            'a',
            {
                'limit': 5,
                'attributesToHighlight': ['title'],
                'attributesToRetrieve': ['title'],
                'attributesToCrop': ['title'],
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 5
        assert '_formatted' in response['hits'][0]
        assert 'title' in response['hits'][0]['_formatted']
        assert not 'release_date' in response['hits'][0]['_formatted']

    def test_custom_search_params_with_string_list(self, indexed_small_movies):
        """Tests search with string list in query params"""
        response = indexed_small_movies[0].search(
            'a',
            {
                'limit': 5,
                'attributesToRetrieve': ['title', 'overview'],
                'attributesToHighlight': ['title'],
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 5
        assert 'title' in response['hits'][0]
        assert 'overview' in response['hits'][0]
        assert not 'release_date' in response['hits'][0]
        assert 'title' in response['hits'][0]['_formatted']
        assert not 'overview' in response['hits'][0]['_formatted']

    def test_custom_search_params_with_facets_distribution(self, indexed_small_movies):
        update = indexed_small_movies[0].update_attributes_for_faceting(['genre'])
        indexed_small_movies[0].wait_for_pending_update(update['updateId'])
        response = indexed_small_movies[0].search(
            'world',
            {
                'facetsDistribution': ['genre']
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 12
        assert 'facetsDistribution' in response
        assert 'exhaustiveFacetsCount' in response
        assert response['exhaustiveFacetsCount']
        assert 'genre' in response['facetsDistribution']
        assert response['facetsDistribution']['genre']['cartoon'] == 1
        assert response['facetsDistribution']['genre']['action'] == 3
        assert response['facetsDistribution']['genre']['fantasy'] == 1

    def test_custom_search_params_with_facet_filters(self, indexed_small_movies):
        update = indexed_small_movies[0].update_attributes_for_faceting(['genre'])
        indexed_small_movies[0].wait_for_pending_update(update['updateId'])
        response = indexed_small_movies[0].search(
            'world',
            {
                'facetFilters': [['genre:action']]
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 3
        assert 'facetsDistribution' not in response
        assert 'exhaustiveFacetsCount' not in response

    def test_custom_search_params_with_multiple_facet_filters(self, indexed_small_movies):
        update = indexed_small_movies[0].update_attributes_for_faceting(['genre'])
        indexed_small_movies[0].wait_for_pending_update(update['updateId'])
        response = indexed_small_movies[0].search(
            'world',
            {
                'facetFilters': ['genre:action', ['genre:action', 'genre:action']]
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 3
        assert 'facetsDistribution' not in response
        assert 'exhaustiveFacetsCount' not in response

    def test_custom_search_params_with_many_params(self, indexed_small_movies):
        update = indexed_small_movies[0].update_attributes_for_faceting(['genre'])
        indexed_small_movies[0].wait_for_pending_update(update['updateId'])
        response = indexed_small_movies[0].search(
            'world',
            {
                'facetFilters': [['genre:action']],
                'attributesToRetrieve': ['title', 'poster']
            }
        )
        assert isinstance(response, object)
        assert len(response['hits']) == 3
        assert 'facetsDistribution' not in response
        assert 'exhaustiveFacetsCount' not in response
        assert 'title' in response['hits'][0]
        assert 'poster' in response['hits'][0]
        assert 'overview' not in response['hits'][0]
        assert 'release_date' not in response['hits'][0]
        assert response['hits'][0]['title'] == 'Avengers: Infinity War'
