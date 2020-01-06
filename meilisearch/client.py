from meilisearch.index import Index
from meilisearch.health import Health
from meilisearch.key import Key
from meilisearch.config import Config
from meilisearch.sys_info import SysInfo
from meilisearch.stat import Stat
from meilisearch.version import Version


class Client(Health, Key, SysInfo, Version):
    """
    A client for the meilisearch API

    A client instance is needed for every meilisearch API method to know the location of
    meilisearch and his permissions.
    """

    def __init__(self, url, apikey=None):
        """
        Parameters
        ----------
        url : str
            The url to the meilisearch API (ex: http://localhost:8080)
        apikey : str
            The optionnal apikey to access the meilisearch api
        """
        config = Config(url, apikey)
        Health.__init__(self, config)
        Key.__init__(self, config)
        SysInfo.__init__(self, config)
        Version.__init__(self, config)
        self.config = config

    def create_index(self, name, uid=None, schema=None):
        """Create an index.

        If the argument `uid` isn't passed in, it will be generated
        by meilisearch.

        Parameters
        ----------
        name: str
            Name of the index
        uid: str, optional
            uid of the index
        schema: dict, optional
            dict containing the schema of the index.
            https://docs.meilisearch.com/main_concepts/indexes.html#schema-definition
        Returns
        -------
        index : Index
            an instance of Index containing the information of the newly created index
        Raises
        ------
        HTTPError
            In case of any other error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        index = Index.create(self.config, name=name, uid=uid, schema=schema)
        return Index(self.config, name=index["name"], uid=index["uid"], schema=schema)

    def get_indexes(self):
        """Get all indexes.

        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        Returns
        -------
        list
            List of indexes in dictionnary format. (e.g [{ 'name': 'movies' 'uid': '12345678' }])
        """
        return Index.get_indexes(self.config)


    def get_index(self, uid=None, name=None):
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
        return Index.get_index(self.config, uid=uid, name=name)

    def get_all_stats(self):
        """Get statistics about indexes, database size and update date.

        Returns
        -------
        stats : dict
            Dictionnary with information about indexes, database size and update date.
        """
        return Stat.get_all_stats(self.config)
