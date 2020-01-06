from meilisearch._httprequests import HttpRequests


class Schema:
    """
    Schema routes wrapper

    Index's parent that gives access to all the schemas methods of meilisearch.
    https://docs.meilisearch.com/references/indexes.html#get-one-index-schema

    Attributes
    ----------
    schema_path:
        Schema url path
    """

    schema_path = 'schema'

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

    def get_schema(self):
        """Get schema of index

        Returns
        ----------
        update: `dict`
            Schema definition
        """

        return HttpRequests.get(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.schema_path)).json()

    def update_schema(self, schema):
        """Update schema of index
        Parameters
        ----------
        schema: dict, optional
            dict containing the schema of the index.
            https://docs.meilisearch.com/main_concepts/indexes.html#schema-definition
        Returns
        ----------
        update: `dict`
            Schema definition
        """

        return HttpRequests.put(
            self.config,
            '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.schema_path),
            schema).json()
