from meilisearch._httprequests import HttpRequests


class Stat:
    """
    Stats routes wrapper

    Index's parent that gives access to all the stats methods of meilisearch.
    https://docs.meilisearch.com/references/stats.html#get-stat-of-an-index

    Attributes
    ----------
    stat_path:
        Version url path
    """
    stat_path = 'stats'

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

    def get_stats(self):
        """Get stats of an index

        Get information about number of documents, fieldsfrequencies, ...
        https://docs.meilisearch.com/references/stats.html
        Returns
        ----------
        stats: `dict`
            Dictionnary containing stats about the given index.

        """
        return HttpRequests.get(self.config, '{}/{}'.format(self.stat_path, self.uid)).json()

    @staticmethod
    def get_all_stats(config):
        """Get all stats of meilisearch

        Get information about databasesize and all indexes
        https://docs.meilisearch.com/references/stats.html
        Returns
        ----------
        stats: `dict`
            Dictionnary containing stats about your meilisearch instance

        """
        return HttpRequests.get(config, Stat.stat_path).json()
