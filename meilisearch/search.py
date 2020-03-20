import urllib
from meilisearch._httprequests import HttpRequests

class Search:
    """
    Search routes wrapper

    Index's parent that gives access to all the search methods of meilisearch.
    https://docs.meilisearch.com/references/search.html#search-in-an-index

    Attributes
    ----------
    search_path:
        Search url path
    """
    search_path = 'search'

    def __init__(self, parent_path, config, uid=None, name=None):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        name: str
            Name of the index on which to perform the index actions.
        uid: str
            Uid of the index on which to perform the index actions.
        index_path: str
            Index url path
        """
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path

    # pylint: disable=dangerous-default-value
    # Not dangerous because opt_params is not modified in the method
    # See: https://stackoverflow.com/questions/26320899/why-is-the-empty-dictionary-a-dangerous-default-value-in-python
    def search(self, query, opt_params={}):
        """Search in meilisearch

        Parameters
        ----------
        query: str
            String containing the searched word(s)
        opt_params: dict
            Dictionnary containing optional query parameters
            https://docs.meilisearch.com/references/search.html#search-in-an-index
        Returns
        ----------
        results: `dict`
            Dictionnary with hits, offset, limit, processingTime and initial query
        """
        search_param = {'q': query}
        params = {**search_param, **opt_params}
        return HttpRequests.get(
            self.config,
            '{}/{}/{}?{}'.format(
                self.index_path,
                self.uid,
                self.search_path,
                urllib.parse.urlencode(params))
        )
