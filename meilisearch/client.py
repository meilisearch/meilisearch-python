from meilisearch.index import Index
from meilisearch.config import Config
from meilisearch._httprequests import HttpRequests
from meilisearch.errors import MeiliSearchApiError, MeiliSearchError

class Client():
    """
    A client for the MeiliSearch API

    A client instance is needed for every MeiliSearch API method to know the location of
    MeiliSearch and its permissions.
    """

    config = None
    http = None

    def __init__(self, url, apiKey=None, timeout=None):
        """
        Parameters
        ----------
        url : str
            The url to the MeiliSearch API (ex: http://localhost:7700)
        apiKey : str
            The optional API key for MeiliSearch
        """
        self.config = Config(url, apiKey, timeout=timeout)

        self.http = HttpRequests(self.config)

    def create_index(self, uid, options=None):
        """Create an index.

        Parameters
        ----------
        uid: str
            UID of the index.
        options (optional): dict
            Options passed during index creation (ex: primaryKey).

        Returns
        -------
        index : Index
            An instance of Index containing the information of the newly created index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return Index.create(self.config, uid, options)

    def get_indexes(self):
        """Get all indexes.

        Returns
        -------
        indexes: list
            List of indexes in dictionary format. (e.g [{ 'uid': 'movies' 'primaryKey': 'objectID' }])

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.index)

    def get_index(self, uid):
        """Get the index.
        This index should already exist.

        Parameters
        ----------
        uid: str
            UID of the index.

        Returns
        -------
        index : Index
            An Index instance containing the information of the fetched index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return Index(self.config, uid).fetch_info()

    def index(self, uid):
        """Create a local reference to an index identified by UID, without doing an HTTP call.
        Calling this method doesn't create an index in the MeiliSearch instance, but grants access to all the other methods in the Index class.

        Parameters
        ----------
        uid: str
            UID of the index.

        Returns
        -------
        index : Index
            An Index instance.
        """
        if uid is not None:
            return Index(self.config, uid=uid)
        raise Exception('The index UID should not be None')

    def get_or_create_index(self, uid, options=None):
        """Get an index, or create it if it doesn't exist.

        Parameters
        ----------
        uid: str
            UID of the index
        options (optional): dict
            Options passed during index creation (ex: primaryKey)

        Returns
        -------
        index : Index
            An instance of Index containing the information of the retrieved or newly created index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        try:
            index_instance = self.get_index(uid)
        except MeiliSearchApiError as err:
            if err.error_code != 'index_not_found':
                raise err
            index_instance = self.create_index(uid, options)
        return index_instance

    def get_all_stats(self):
        """Get all stats of MeiliSearch

        Get information about database size and all indexes
        https://docs.meilisearch.com/reference/api/stats.html

        Returns
        -------
        stats: `dict`
            Dictionary containing stats about your MeiliSearch instance.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.stat)

    def health(self):
        """Get health of the MeiliSearch server.

        `200` HTTP status response when MeiliSearch is healthy.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.health)

    def is_healthy(self):
        """Get health of the MeiliSearch server.

        `200` HTTP status response when MeiliSearch is healthy.

        Return
        ------
        health: True | False
        """
        try:
            self.health()
        except MeiliSearchError:
            return False
        return True

    def get_keys(self):
        """Get all keys.

        Get the public and private keys.

        Returns
        -------
        keys: dict
            Dictionary of keys and their information.
            https://docs.meilisearch.com/reference/api/keys.html#get-keys

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.keys)

    def get_version(self):
        """Get version MeiliSearch

        Returns
        -------
        version: dict
            Information about the version of MeiliSearch.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(self.config.paths.version)

    def version(self):
        """Alias for get_version

        Returns
        -------
        version: dict
            Information about the version of MeiliSearch.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.get_version()

    def create_dump(self):
        """Trigger the creation of a MeiliSearch dump.

        Returns
        -------
        Dump: dict
            Information about the dump.
            https://docs.meilisearch.com/reference/api/dump.html#create-a-dump

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(self.config.paths.dumps)

    def get_dump_status(self, uid):
        """Retrieve the status of a MeiliSearch dump creation.

        Parameters
        ----------
        uid: str
            UID of the dump.

        Returns
        -------
        Dump status: dict
            Information about the dump status.
            https://docs.meilisearch.com/reference/api/dump.html#get-dump-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.config.paths.dumps + '/' + str(uid) + '/status'
        )
