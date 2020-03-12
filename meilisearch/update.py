from meilisearch._httprequests import HttpRequests

class Update:
    """
    Update routes wrapper

    Index's parent that gives access to all the update methods of MeiliSearch.
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
            Config object containing permission and location of MeiliSearch
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

    def get_all_update_status(self):
        """Get all update status from MeiliSearch

        Returns
        ----------
        update: `list`
            List of all enqueued and processed actions of the index.
        """
        return HttpRequests.get(
            self.config,
            '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.update_path
            )
        )

    def get_update_status(self, update_id):
        """Get one update from MeiliSearch

        Parameters
        ----------
        update_id: int
            identifier of the update to retieve
        Returns
        ----------
        update: `list`
            List of all enqueued and processed actions of the index.
        """
        return HttpRequests.get(
            self.config,
            '{}/{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.update_path,
                update_id
            )
        )
