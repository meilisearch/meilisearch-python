from meilisearch._httprequests import HttpRequests


class Update:
    """
    Update routes wrapper

    Index's parent that gives access to all the update methods of meilisearch.
    https://docs.meilisearch.com/references/updates.html#get-an-update-status

    Attributes
    ----------
    update_path:
        Update url path
    """

    update_path = 'updates'

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

    def get_updates(self):
        """Get updates from meilisearch

        Returns
        ----------
        update: `list`
            List of all enqueued and processed actions of the index.
        """

        return HttpRequests.get(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.update_path)).json()

    def get_update(self, updateId):
        """Get one update from meilisearch

        Parameters
        ----------
        updateId: int
            identifier of the update to retieve
        Returns
        ----------
        update: `list`
            List of all enqueued and processed actions of the index.
        """

        return HttpRequests.get(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.update_path,
            updateId)).json()
