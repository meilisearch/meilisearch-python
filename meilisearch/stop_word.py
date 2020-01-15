from meilisearch._httprequests import HttpRequests


class StopWord:
    """
    Stop-words routes wrapper

    Index's parent that gives access to all the stop-words methods of meilisearch.
    https://docs.meilisearch.com/references/stats.html#get-stat-of-an-index

    Attributes
    ----------
    stop_word_path: str
        Version url path
    """
    stop_word_path = 'stop-words'

    def __init__(self, parent_path, config, uid=None, name=None):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        name: str
            Name of the index on which to perform the operation.
        uid: str
            Uid of the index on which to perform the operation.
        schema: dict
            Schema definition of index.
        index_path: str
            Index url path
        """

        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path

    def get_stop_words(self):
        """Get stop words list

        Get all the stop words of the index
        https://docs.meilisearch.com/references/stop_words.html

        Returns
        ----------
        stop_words: `list`
            List containing all the stop words of the given index

        """

        return HttpRequests.get(
            self.config, '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.stop_word_path
            )).json()

    def add_stop_words(self, body):
        """Add a list of stop words

        https://docs.meilisearch.com/references/stop_words.html

        Parameters
        ----------
        body: `list`
            List of stop words.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status

        """

        return HttpRequests.patch(
            self.config, '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.stop_word_path
            ),
            body
        ).json()

    # WAIING FOR UPDATE
    def delete_stop_words(self, body):
        """Delete a list of stop words

        https://docs.meilisearch.com/references/stop_words.html

        Parameters
        ----------
        body: `list`
            List of stop words.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config, '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.stop_word_path
            ),
            body
        ).json()
