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
        schema: dict
            Schema definition of index.
        index_path: str
            Index url path
        """

        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path

    def search(self, parameters):
        """Search in meilisearch

        Parameters
        ----------
        parameters: dict
            Dictionnary containing all available query parameter from the search route
            https://docs.meilisearch.com/references/search.html#search-in-an-index
        Returns
        ----------
        results: `dict`
            Dictionnary with hits, offset, limit, processingTime and initial query
        """

        return HttpRequests.get(
            self.config,
            '{}/{}/{}?{}'.format(
                self.index_path,
                self.uid,
                self.search_path,
                urllib.parse.urlencode(parameters))
        ).json()
