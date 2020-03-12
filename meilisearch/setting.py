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
    ranking_rules_path = 'ranking-rules'
    distinct_attribute_path = 'distinct-attribute'
    searchable_attributes_path = 'searchable-attributes'
    displayed_attributes_path = 'displayed-attributes'
    stop_words_path = 'stop-words'
    synonyms_path = 'synonyms'
    accept_new_fields_path = 'accept-new-fields'

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


    # GENERAL SETTINGS ROUTES

    def get_settings(self):
        """Get settings of an index

        https://docs.meilisearch.com/references/settings.html

        Returns
        ----------
        settings: `dict`
            Dictionnary containing the settings of the index
        """
        return HttpRequests.get(
            self.config,
            '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.setting_path
            )
        )

    def update_settings(self, body):
        """Update settings of an index

        https://docs.meilisearch.com/references/settings.html#update-settings
        Parameters
        ----------
        body: `dict`
            Dictionnary containing the settings of the index
            More information :
            https://docs.meilisearch.com/references/settings.html#update-settings

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.setting_path
            ),
            body
        )

    def reset_settings(self):
        """Reset settings of an index to default values

        https://docs.meilisearch.com/references/settings.html#reset-settings

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.setting_path
            ),
        )

    # RANKING RULES SUB-ROUTES

    def get_ranking_rules(self):
        """
        Get ranking rules of an index

        Returns
        ----------
        settings: `list`
            List containing the ranking rules of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.ranking_rules_path)
        )

    def update_ranking_rules(self, body):
        """
        Update ranking rules of an index

        Parameters
        ----------
        body: `list`
            List containing the ranking rules

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.ranking_rules_path),
            body
        )

    def reset_ranking_rules(self):
        """Reset ranking rules of an index to default values

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            self.__settings_url_for(self.ranking_rules_path),
        )


    # DISTINCT ATTRIBUTE SUB-ROUTES

    def get_distinct_attribute(self):
        """
        Get distinct attribute of an index

        Returns
        ----------
        settings: `str`
            String containing the distinct attribute of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.distinct_attribute_path)
        )

    def update_distinct_attribute(self, body):
        """
        Update distinct attribute of an index

        Parameters
        ----------
        body: `str`
            String containing the distinct attribute

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.distinct_attribute_path),
            body
        )

    def reset_distinct_attribute(self):
        """Reset distinct attribute of an index to default values

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            self.__settings_url_for(self.distinct_attribute_path),
        )

    # SEARCHABLE ATTRIBUTES SUB-ROUTES

    def get_searchable_attributes(self):
        """
        Get searchable attributes of an index

        Returns
        ----------
        settings: `list`
            List containing the searchable attributes of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.searchable_attributes_path)
        )

    def update_searchable_attributes(self, body):
        """
        Update searchable attributes of an index

        Parameters
        ----------
        body: `list`
            List containing the searchable attributes

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.searchable_attributes_path),
            body
        )

    def reset_searchable_attributes(self):
        """Reset searchable attributes of an index to default values

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            self.__settings_url_for(self.searchable_attributes_path),
        )

    # DISPLAYED ATTRIBUTES SUB-ROUTES

    def get_displayed_attributes(self):
        """
        Get displayed attributes of an index

        Returns
        ----------
        settings: `list`
            List containing the displayed attributes of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.displayed_attributes_path)
        )

    def update_displayed_attributes(self, body):
        """
        Update displayed attributes of an index

        Parameters
        ----------
        body: `list`
            List containing the displayed attributes

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.displayed_attributes_path),
            body
        )

    def reset_displayed_attributes(self):
        """Reset displayed attributes of an index to default values

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            self.__settings_url_for(self.displayed_attributes_path),
        )

    # STOP WORDS SUB-ROUTES

    def get_stop_words(self):
        """
        Get stop words of an index

        Returns
        ----------
        settings: `list`
            List containing the stop words of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.stop_words_path)
        )

    def update_stop_words(self, body):
        """
        Update stop words of an index

        Parameters
        ----------
        body: `list`
            List containing the stop words

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.stop_words_path),
            body
        )

    def reset_stop_words(self):
        """Reset stop words of an index to default values

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            self.__settings_url_for(self.stop_words_path),
        )

    # SYNONYMS SUB-ROUTES

    def get_synonyms(self):
        """
        Get synonyms of an index

        Returns
        ----------
        settings: `dict`
            Dictionnary containing the synonyms of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.synonyms_path)
        )

    def update_synonyms(self, body):
        """
        Update synonyms of an index

        Parameters
        ----------
        body: `dict`
            Dictionnary containing the synonyms

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.synonyms_path),
            body
        )

    def reset_synonyms(self):
        """Reset synonyms of an index to default values

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            self.__settings_url_for(self.synonyms_path),
        )

    # ACCEPT-NEW-FIELDS SUB-ROUTES

    def get_accept_new_fields(self):
        """
        Get accept-new-fields value of an index

        Returns
        ----------
        settings: `bool`
            Boolean containing the accept-new-fields value of the index
        """
        return HttpRequests.get(
            self.config,
            self.__settings_url_for(self.accept_new_fields_path)
        )

    def update_accept_new_fields(self, body):
        """
        Update accept-new-fields value of an index

        Parameters
        ----------
        body: `bool`
            Boolean containing the accept-new-fields value

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            self.__settings_url_for(self.accept_new_fields_path),
            body
        )

    def __settings_url_for(self, sub_route):
        return '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.setting_path,
            sub_route
        )
