from meilisearch._httprequests import HttpRequests

class Version:
    """
    Version routes wrapper

    Index's parent that gives access to all the version methods of meilisearch.
    https://docs.meilisearch.com/references/version.html#get-version-of-meilisearch

    """
    version_path = 'version'

    def __init__(self, config):
        """
        Attributes
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        """
        self.config = config

    def get_version(self):
        """Get version meilisearch

        Returns
        ----------
        version: dict
            Information about version of meilisearch.
        """
        return HttpRequests.get(self.config, self.version_path)

    def version(self):
        """Alias for get_version

        Returns
        ----------
        version: dict
            Information about version of meilisearch.
        """
        return self.get_version()
