from meilisearch.index import Index
from meilisearch.health import Health
from meilisearch.key import Key
from meilisearch.config import Config
from meilisearch.sys_info import SysInfo
from meilisearch.stat import Stat
from meilisearch.version import Version

class Client(Health, Key, SysInfo, Version):
    """
    A client for the MeiliSearch API

    A client instance is needed for every MeiliSearch API method to know the location of
    MeiliSearch and its permissions.
    """

    def __init__(self, url, apiKey=None):
        """
        Parameters
        ----------
        url : str
            The url to the MeiliSearch API (ex: http://localhost:7700)
        apiKey : str
            The optional API key for MeiliSearch
        """
        config = Config(url, apiKey)
        Health.__init__(self, config)
        Key.__init__(self, config)
        SysInfo.__init__(self, config)
        Version.__init__(self, config)
        self.config = config

    def create_index(self, uid, primary_key=None, name=None):
        """Create an index.

        If the argument `uid` isn't passed in, it will be generated
        by MeiliSearch.

        Parameters
        ----------
        uid: str
            UID of the index
        primary_key: str, optional
            Attribute used as unique document identifier
        name: str, optional
            Name of the index
        Returns
        -------
        index : Index
            an instance of Index containing the information of the newly created index
        Raises
        ------
        HTTPError
            In case of any other error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        index = Index.create(self.config, uid=uid, primary_key=primary_key, name=name)
        return Index(self.config, uid=index['uid'])

    def get_indexes(self):
        """Get all indexes.

        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        Returns
        -------
        list
            List of indexes in dictionnary format. (e.g [{ 'uid': 'movies' 'primaryKey': 'objectID' }])
        """
        return Index.get_indexes(self.config)


    def get_index(self, uid):
        """Get an index.

        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        Returns
        -------
        index : Index
            an instance of Index containing the information of the index found
        """
        return Index.get_index(self.config, uid=uid)

    def get_all_stats(self):
        """Get statistics about indexes, database size and update date.

        Returns
        -------
        stats : dict
            Dictionnary with information about indexes, database size and update date.
        """
        return Stat.get_all_stats(self.config)
