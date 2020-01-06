from meilisearch._httprequests import HttpRequests


class Setting:
    """
    Settings routes wrapper

    Index's parent that gives access to all the settings methods of meilisearch.
    https://docs.meilisearch.com/references/settings.html

    Attributes
    ----------
    setting_path:
        Settings url path
    """

    setting_path = 'settings'

    def __init__(self, parent_path, config, uid=None, name=None):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        name: str
            Name of the index on which to perform the actions.
        uid: str
            Uid of the index on which to perform the actions.
        index_path: str
            Index url path
        """

        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path

    def get_settings(self):
        """Get settings of given Index

        Get the settings of the index.
        https://docs.meilisearch.com/references/settings.html

        Returns
        ----------
        document: `dict`
            Dictionnary containing the settings of the index
        """

        return HttpRequests.get(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.setting_path
        )).json()

    def add_settings(self, body):
        """Add settings to the given Index

        Add settings to the given index.
        https://docs.meilisearch.com/references/settings.html#add-or-update-settings
        Parameters
        ----------
        body: `dict`
            Dictionnary containing the settings of the index
            More information :
            https://docs.meilisearch.com/references/settings.html#add-or-update-settings

        Returns
        ----------
        document: `dict`
            Dictionnary containing the settings of the index
        """

        return HttpRequests.post(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.setting_path
        ),
                                 body
                                 ).json()

    def replace_settings(self, body):
        """Replace settings to the given Index

        Replace settings to the given index. This overrides the old settings.
        https://docs.meilisearch.com/references/settings.html#add-or-update-settings
        Parameters
        ----------
        body: `dict`
            Dictionnary containing the settings of the index
            More information :
            https://docs.meilisearch.com/references/settings.html#add-or-update-settings

        Returns
        ----------
        document: `dict`
            Dictionnary containing the settings of the index
        """

        return self.add_settings(body)
