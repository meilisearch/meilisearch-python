from meilisearch._httprequests import HttpRequests


class Key:
    """
    Key routes wrapper

    Index's parent that gives access to all the keys methods of meilisearch.
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

        return HttpRequests.get(self.config, self.key_path).json()

    def get_key(self, key):
        """Get information about a given key

        Parameters
        ----------
        key: str
            Key value
        Returns
        ----------
        key: dict
            Information about a given key
            https://docs.meilisearch.com/references/keys.html#get-one-key
        """

        return HttpRequests.get(self.config, '{}/{}'.format(self.key_path, key)).json()

    def create_key(self, body):
        """Create a key.

        Create a key with custom permissions, scope, description and expire date.
        More info here https://docs.meilisearch.com/advanced_guides/keys.html.

        Parameters
        ----------
        body: dict
            Dictionnary with all information linked to the key that will be created.
            https://docs.meilisearch.com/references/keys.html#create-key
        Returns
        ----------
        key: dict
            Information about the created key
        """

        return HttpRequests.post(self.config, self.key_path, body).json()

    def update_key(self, key, body):
        """Update a key.

        Update a key with custom permissions, scope, description and expire date.
        More info here https://docs.meilisearch.com/advanced_guides/keys.html.

        Parameters
        ----------
        key: str
            Key value
        body: dict
            Dictionnary with all information to update.
            https://docs.meilisearch.com/references/keys.html#update-key
        Returns
        ----------
        key: dict
            Information about the updated key
        """

        return HttpRequests.put(self.config, '{}/{}'.format(self.key_path, key), body).json()

    def delete_key(self, key):
        """Delete a key.

        Delete a given key.
        More info here https://docs.meilisearch.com/references/keys.html#delete-key

        Parameters
        ----------
        key: str
            Key value
        """

        return HttpRequests.delete(self.config, '{}/{}'.format(self.key_path, key))
