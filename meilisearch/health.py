from meilisearch._httprequests import HttpRequests

class Health:
    """
    Health routes wrapper

    Client's parent that gives access to all the health methods of meilisearch.
    https://docs.meilisearch.com/references/health.html

    Attributes
    ----------
    health_path:
        Health url path
    """
    health_path = 'health'

    def __init__(self, config):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        """
        self.config = config

    def health(self):
        """Get health of meilisearch

        `204` http status response when meilisearch is healthy.

        Raises
        ----------
        HTTPError
            If meilisearch is not healthy
        """
        return HttpRequests.get(self.config, self.health_path)

    def update_health(self, health):
        """Update health of meilisearch

        Update health of meilisearch to true or false.

        Parameters
        ----------
        health: bool
            Boolean reprensenting the healthyness of meilisearch. True for healthy.
        """
        return HttpRequests.put(self.config, self.health_path, {'health': health})
