from meilisearch._httprequests import HttpRequests
from meilisearch.update import Update
from meilisearch.document import Document
from meilisearch.search import Search
from meilisearch.stat import Stat
from meilisearch.setting import Setting

# pylint: disable=too-many-ancestors
class Index(Update, Document, Search, Stat, Setting):
    """
    Indexes routes wrapper

    Index class gives access to all indexes routes and child routes (herited).
    https://docs.meilisearch.com/references/indexes.html

    Attributes
    ----------
    index_path:
        Index url path
    """
    index_path = 'indexes'

    def __init__(self, config, uid):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        uid: str
            Uid of the index on which to perform the index actions.
        index_path: str
            Index url path
        """
        Update.__init__(self, Index.index_path, config, uid)
        Search.__init__(self, Index.index_path, config, uid)
        Document.__init__(self, Index.index_path, config, uid)
        Stat.__init__(self, Index.index_path, config, uid)
        Setting.__init__(self, Index.index_path, config, uid)
        self.config = config
        self.uid = uid

    def delete(self):
        """Delete an index from meilisearch

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(self.config, '{}/{}'.format(self.index_path, self.uid))

    def update(self, **body):
        """Update an index from meilisearch

        Parameters
        ----------
        body: **kwargs
            Accepts primaryKey as an updatable parameter.

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        payload = {}
        primary_key = body.get('primaryKey', None)
        if primary_key is not None:
            payload['primaryKey'] = primary_key
        return HttpRequests.put(self.config, '{}/{}'.format(self.index_path, self.uid), payload)

    def info(self):
        """Get info of index

        Returns
        ----------
        index: `dict`
            Dictionnary containing index information.
        """
        return HttpRequests.get(self.config, '{}/{}'.format(self.index_path, self.uid))

    def get_primary_key(self):
        """Get the primary key

        Returns
        ----------
        primary_key: str
            String containing primary key.
        """
        return self.info()['primaryKey']

    @staticmethod
    def create(config, **body):
        """Create an index.

        Parameters
        ----------
            body: **kwargs
            Accepts uid, name and primaryKey as parameter.

        Returns
        -------
        index : Index
            an instance of Index containing the information of the newly created index
        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        payload = {}
        uid = body.get('uid', None)
        if uid is not None:
            payload['uid'] = uid
        name = body.get('name', None)
        if name is not None:
            payload['name'] = name
        primary_key = body.get('primary_key', None)
        if primary_key is not None:
            payload['primaryKey'] = primary_key
        return HttpRequests.post(config, Index.index_path, payload)

    @staticmethod
    def get_indexes(config):
        """Get all indexes from meilisearch.

        Returns
        -------
        indexes : list
            List of indexes (dict)
        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        return HttpRequests.get(config, Index.index_path)

    @staticmethod
    def get_index(config, uid):
        """Get Index instance from given index

        If the argument `uid` aren't passed in, it will raise an exception.

        Returns
        -------
        index : Index
            Instance of Index with the given index.
        Raises
        ------
        Exception
            If index UID is missing.
        """
        if uid is not None:
            return Index(config, uid=uid)
        raise Exception('Uid is needed to find index')
