from meilisearch._httprequests import HttpRequests
import urllib

# pylint: disable=too-many-ancestors
class Index():
    """
    Indexes routes wrapper

    Index class gives access to all indexes routes and child routes (herited).
    https://docs.meilisearch.com/references/indexes.html
    """

    config = None
    uid = ""

    class Update:
        """
        Update routes wrapper

        Index's parent that gives access to all the update methods of MeiliSearch.
        https://docs.meilisearch.com/references/updates.html#get-an-update-status

        """


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
            self.config.paths.index = parent_path

    class Stat:
        """
        Stats routes wrapper

        Index's parent that gives access to all the stats methods of MeiliSearch.
        https://docs.meilisearch.com/references/stats.html#get-stat-of-an-index

        """


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
            self.config.paths.index = parent_path

    class Search:
        """
        Search routes wrapper

        Index's parent that gives access to all the search methods of meilisearch.
        https://docs.meilisearch.com/references/search.html#search-in-an-index

        """

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
            index_path: str
                Index url path
            """
            self.config = config
            self.name = name
            self.uid = uid
            self.config.paths.index = parent_path

    class Document:
        """
        Documents routes wrapper

        Index's parent that gives access to all the documents methods of MeiliSearch.
        https://docs.meilisearch.com/references/documents.html

        """


        def __init__(self, parent_path, config, uid=None, name=None):
            """
            Parameters
            ----------
            config : Config
                Config object containing permission and location of MeiliSearch
            name: str
                Name of the index on which to perform the document actions.
            uid: str
                Uid of the index on which to perform the document actions.
            index_path: str
                Index url path
            """
            self.config = config
            self.name = name
            self.uid = uid
            self.config.paths.index = parent_path

    class Setting:
        """
        Settings routes wrapper

        Index's parent that gives access to all the settings methods of meilisearch.
        https://docs.meilisearch.com/references/settings.html

        """

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
            self.config.paths.index = parent_path

    def __init__(self, config, uid):
        """
        Parameters
        ----------
        config : Config
            Config object containing permission and location of meilisearch
        uid: str
            Uid of the index on which to perform the index actions.
        index_path: str
            Index url path
        """
        self.config = config
        self.uid = uid

    def delete(self):
        """Delete an index from meilisearch

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(self.config, '{}/{}'.format(self.config.paths.index, self.uid))

    def update(self, **body):
        """Update an index from meilisearch

        Parameters
        ----------
        body: **kwargs
            Accepts primaryKey as an updatable parameter.

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        payload = {}
        primary_key = body.get('primaryKey', None)
        if primary_key is not None:
            payload['primaryKey'] = primary_key
        return HttpRequests.put(self.config, '{}/{}'.format(self.config.paths.index, self.uid), payload)

    def info(self):
        """Get info of index

        Returns
        ----------
        index: `dict`
            Dictionnary containing index information.
        """
        return HttpRequests.get(self.config, '{}/{}'.format(self.config.paths.index, self.uid))

    def get_primary_key(self):
        """Get the primary key

        Returns
        ----------
        primary_key: str
            String containing primary key.
        """
        return self.info()['primaryKey']

    @staticmethod
    def create(config, **body):
        """Create an index.

        Parameters
        ----------
            body: **kwargs
            Accepts uid, name and primaryKey as parameter.

        Returns
        -------
        index : Index
            an instance of Index containing the information of the newly created index
        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        payload = {}
        uid = body.get('uid', None)
        if uid is not None:
            payload['uid'] = uid
        name = body.get('name', None)
        if name is not None:
            payload['name'] = name
        primary_key = body.get('primary_key', None)
        if primary_key is not None:
            payload['primaryKey'] = primary_key
        return HttpRequests.post(config, config.paths.index, payload)

    @staticmethod
    def get_indexes(config):
        """Get all indexes from meilisearch.

        Returns
        -------
        indexes : list
            List of indexes (dict)
        Raises
        ------
        HTTPError
            In case of any error found here https://docs.meilisearch.com/references/#errors-status-code
        """
        return HttpRequests.get(config, config.paths.index)

    @staticmethod
    def get_index(config, uid):
        """Get Index instance from given index

        If the argument `uid` aren't passed in, it will raise an exception.

        Returns
        -------
        index : Index
            Instance of Index with the given index.
        Raises
        ------
        Exception
            If index UID is missing.
        """
        if uid is not None:
            return Index(config, uid=uid)
        raise Exception('Uid is needed to find index')

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
                self.config.paths.index,
                self.uid,
                self.config.paths.update
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
                self.config.paths.index,
                self.uid,
                self.config.paths.update,
                update_id
            )
        )

    def get_stats(self):
        """Get stats of an index

        Get information about number of documents, fieldsfrequencies, ...
        https://docs.meilisearch.com/references/stats.html
        Returns
        ----------
        stats: `dict`
            Dictionnary containing stats about the given index.
        """
        return HttpRequests.get(
            self.config,
            '{}/{}/{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.stat,
            )
        )

    # pylint: disable=dangerous-default-value
    # Not dangerous because opt_params is not modified in the method
    # See: https://stackoverflow.com/questions/26320899/why-is-the-empty-dictionary-a-dangerous-default-value-in-python
    def search(self, query, opt_params={}):
        """Search in meilisearch

        Parameters
        ----------
        query: str
            String containing the searched word(s)
        opt_params: dict
            Dictionnary containing optional query parameters
            https://docs.meilisearch.com/references/search.html#search-in-an-index
        Returns
        ----------
        results: `dict`
            Dictionnary with hits, offset, limit, processingTime and initial query
        """
        search_param = {'q': query}
        params = {**search_param, **opt_params}
        return HttpRequests.get(
            self.config,
            '{}/{}/{}?{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.search,
                urllib.parse.urlencode(params))
        )

    def get_document(self, document_id):
        """Get one document with given document identifier

        Parameters
        ----------
        document_id: str
            Unique identifier of the document.
        Returns
        ----------
        document: `dict`
            Dictionnary containing the documents information
        """
        return HttpRequests.get(
            self.config,
            '{}/{}/{}/{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document,
                document_id
            )
        )

    def get_documents(self, parameters=None):
        """Get a set of documents from the index

        Parameters
        ----------
        parameters (optional): dict
            parameters accepted by the get documents route: https://docs.meilisearch.com/references/documents.html#get-all-documents
        Returns
        ----------
        document: `dict`
            Dictionnary containing the documents information
        """
        if parameters is None:
            parameters = {}

        return HttpRequests.get(
            self.config,
            '{}/{}/{}?{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document,
                urllib.parse.urlencode(parameters))
            )

    def add_documents(self, documents, primary_key=None):
        """Add documents to the index

        Parameters
        ----------
        documents: list
            List of dics containing each a document, or json string
        primary_key: string
            The primary-key used in MeiliSearch index. Ignored if already set up.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        if primary_key is None:
            url = '{}/{}/{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document
            )
        else:
            url = '{}/{}/{}?{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document,
                urllib.parse.urlencode({'primaryKey': primary_key})
            )
        return HttpRequests.post(self.config, url, documents)

    def update_documents(self, documents, primary_key=None):
        """Update documents in the index

        Parameters
        ----------
        documents: list
            List of dics containing each a document, or json string
        primary_key: string
            The primary-key used in MeiliSearch index. Ignored if already set up.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        if primary_key is None:
            url = '{}/{}/{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document
            )
        else:
            url = '{}/{}/{}?{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document,
                urllib.parse.urlencode({'primaryKey': primary_key})
            )
        return HttpRequests.put(self.config, url, documents)


    def delete_document(self, document_id):
        """Add documents to the index

        Parameters
        ----------
        document_id: str
            Unique identifier of the document.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            '{}/{}/{}/{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document,
                document_id
            )
        )

    def delete_documents(self, ids):
        """Delete multiple documents of the index

        Parameters
        ----------
        list: list
            List of unique identifiers of documents.
        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.post(
            self.config,
            '{}/{}/{}/delete-batch'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document
            ),
            ids
        )

    def delete_all_documents(self):
        """Delete all documents of the index

        Returns
        ----------
        update: `dict`
            Dictionnary containing an update id to track the action:
            https://docs.meilisearch.com/references/updates.html#get-an-update-status
        """
        return HttpRequests.delete(
            self.config,
            '{}/{}/{}'.format(
                self.config.paths.index,
                self.uid,
                self.config.paths.document
            )
        )


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
                self.config.paths.index,
                self.uid,
                self.config.paths.setting
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
                self.config.paths.index,
                self.uid,
                self.config.paths.setting
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
                self.config.paths.index,
                self.uid,
                self.config.paths.setting
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
            self.__settings_url_for(self.config.paths.ranking_rules)
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
            self.__settings_url_for(self.config.paths.ranking_rules),
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
            self.__settings_url_for(self.config.paths.ranking_rules),
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
            self.__settings_url_for(self.config.paths.distinct_attribute)
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
            self.__settings_url_for(self.config.paths.distinct_attribute),
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
            self.__settings_url_for(self.config.paths.distinct_attribute),
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
            self.__settings_url_for(self.config.paths.searchable_attributes)
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
            self.__settings_url_for(self.config.paths.searchable_attributes),
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
            self.__settings_url_for(self.config.paths.searchable_attributes),
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
            self.__settings_url_for(self.config.paths.displayed_attributes)
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
            self.__settings_url_for(self.config.paths.displayed_attributes),
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
            self.__settings_url_for(self.config.paths.displayed_attributes),
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
            self.__settings_url_for(self.config.paths.stop_words)
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
            self.__settings_url_for(self.config.paths.stop_words),
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
            self.__settings_url_for(self.config.paths.stop_words),
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
            self.__settings_url_for(self.config.paths.synonyms)
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
            self.__settings_url_for(self.config.paths.synonyms),
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
            self.__settings_url_for(self.config.paths.synonyms),
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
            self.__settings_url_for(self.config.paths.accept_new_fields)
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
            self.__settings_url_for(self.config.paths.accept_new_fields),
            body
        )

    def __settings_url_for(self, sub_route):
        return '{}/{}/{}/{}'.format(
            self.config.paths.index,
            self.uid,
            self.config.paths.setting,
            sub_route
        )

