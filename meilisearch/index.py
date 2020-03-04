from meilisearch._httprequests import HttpRequests
from meilisearch.schema import Schema
from meilisearch.update import Update
from meilisearch.document import Document
from meilisearch.synonym import Synonym
from meilisearch.search import Search
from meilisearch.stat import Stat
from meilisearch.setting import Setting
from meilisearch.stop_word import StopWord

# pylint: disable=too-many-ancestors
class Index(Schema, Update, Document, Search, Synonym, Stat, Setting, StopWord):
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

    def __init__(self, config, uid=None, name=None, schema=None):
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

        Schema.__init__(self, Index.index_path, config, name, uid)
        Update.__init__(self, Index.index_path, config, name, uid)
        Search.__init__(self, Index.index_path, config, name, uid)
        Document.__init__(self, Index.index_path, config, name, uid)
        Synonym.__init__(self, Index.index_path, config, name, uid)
        Stat.__init__(self, Index.index_path, config, name, uid)
        Setting.__init__(self, Index.index_path, config, name, uid)
        StopWord.__init__(self, Index.index_path, config, name, uid)
        self.config = config
        self.name = name
        self.uid = uid
        self.schema = schema

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
            Accepts name as an updatable parameter.

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """

        payload = {}
        name = body.get("name", None)
        if name is not None:
            payload["name"] = name
        return HttpRequests.put(self.config, '{}/{}'.format(self.index_path, self.uid), payload).json()

    def info(self):
        """Get info of index

        Returns
        ----------
        index: `dict`
            Dictionnary containing index information.
        """

        return HttpRequests.get(self.config, '{}/{}'.format(self.index_path, self.uid)).json()

    @staticmethod
    def create(config, name, uid=None, schema=None):
        """Create an index.

        If the argument `uid` isn't passed in, it will be generated
        by meilisearch.
        If the argument `name` isn't passed in, it will raise an error.

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
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        """

        payload = {}
        if name is not None:
            payload["name"] = name
        if uid is not None:
            payload["uid"] = uid
        if schema is not None:
            payload["schema"] = schema
        response = HttpRequests.post(config, Index.index_path, payload)
        return response.json()

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

        return HttpRequests.get(config, Index.index_path).json()

    @staticmethod
    def get_index(config, name=None, uid=None):
        """Get Index instance from given index

        If the arguments `name` and `uid` aren't passed in, it
        will raise an exception.

        Returns
        -------
        index : Index
            Instance of Index with the given index.
        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        if uid is not None:
            return Index(config, uid=uid, name=name)
        if name is None:
            raise Exception('Name or Uid is needed to find index')
        indexes = Index.get_indexes(config)
        index = list(filter(lambda index: index["name"] == name, indexes))
        if len(index) == 0:
            raise Exception('Index not found')
        index = index[0]
        return Index(config, name=index["name"], uid=index["uid"])
