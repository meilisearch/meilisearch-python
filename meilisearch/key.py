from meilisearch._httprequests import HttpRequests

class Key:
    """
    Key routes wrapper

    Index's parent that gives access to all the keys methods of MeiliSearch.
    https://docs.meilisearch.com/references/keys.html

    Attributes
    ----------
    index_path:
        Index url path
    """
    key_path = 'keys'

    def __init__(self, config):
        """
        Attributes
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        """
        self.config = config

    def get_keys(self):
        """Get all keys created

        Get list of all the keys that were created and all their related information.

        Returns
        ----------
        keys: list
            List of keys and their information.
            https://docs.meilisearch.com/references/keys.html#get-keys
        """
        return HttpRequests.get(self.config, self.key_path)
