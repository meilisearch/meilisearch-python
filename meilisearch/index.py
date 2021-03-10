import urllib
from datetime import datetime
from time import sleep
from meilisearch._httprequests import HttpRequests
from meilisearch.errors import MeiliSearchTimeoutError

# pylint: disable=too-many-public-methods
class Index():
    """
    Indexes routes wrapper.

    Index class gives access to all indexes routes and child routes (inherited).
    https://docs.meilisearch.com/reference/api/indexes.html
    """

    config = None
    http = None
    uid = None
    primary_key = None

    def __init__(self, config, uid, primary_key=None):
        """
        Parameters
        ----------
        config : dict
            Config object containing permission and location of MeiliSearch.
        uid: str
            UID of the index on which to perform the index actions.
        primary_key (optional): str
            Primary-key of the index.
        """
        self.config = config
        self.http = HttpRequests(config)
        self.uid = uid
        self.primary_key = primary_key

    def delete(self):
        """Delete the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(f'{self.config.paths.index}/{self.uid}')

    def update(self, **body):
        """Update the index primary-key.

        Parameters
        ----------
        body: **kwargs
            Accepts primaryKey as an updatable parameter.
            Ex: index.update(primaryKey='name')

        Returns
        -------
        index : Index
            An instance of Index

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        payload = {}
        primary_key = body.get('primaryKey', None)
        if primary_key is not None:
            payload['primaryKey'] = primary_key
        response = self.http.put(f'{self.config.paths.index}/{self.uid}', payload)
        self.primary_key = response['primaryKey']
        return self

    def fetch_info(self):
        """Fetch the info of the index.

        Returns
        -------
        index : Index
            An instance of Index

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        index_dict = self.http.get(f'{self.config.paths.index}/{self.uid}')
        self.primary_key = index_dict['primaryKey']
        return self

    def get_primary_key(self):
        """Get the primary key.

        Returns
        -------
        primary_key: str | None
            String containing the primary key.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.fetch_info().primary_key

    @classmethod
    def create(cls, config, uid, options=None):
        """Create the index.

        Parameters
        ----------
        uid: str
            UID of the index.
        options: dict, optional
            Options passed during index creation (ex: { 'primaryKey': 'name' }).

        Returns
        -------
        index : Index
            An instance of Index containing the information of the newly created index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if options is None:
            options = {}
        payload = {**options, 'uid': uid}
        index_dict = HttpRequests(config).post(config.paths.index, payload)
        return cls(config, index_dict['uid'], index_dict['primaryKey'])

    def get_all_update_status(self):
        """Get all update status

        Returns
        -------
        update: list
            List of all enqueued and processed actions of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.update}'
        )

    def get_update_status(self, update_id):
        """Get one update status

        Parameters
        ----------
        update_id: int
            identifier of the update to retrieve

        Returns
        -------
        update: list
            List containing the details of the update status.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.update}/{update_id}'
        )

    def wait_for_pending_update(self, update_id, timeout_in_ms=5000, interval_in_ms=50):
        """Wait until MeiliSearch processes an update, and get its status.

        Parameters
        ----------
        update_id: int
            identifier of the update to retrieve
        timeout_in_ms (optional): int
            time the method should wait before raising a MeiliSearchTimeoutError
        interval_in_ms (optional): int
            time interval the method should wait (sleep) between requests

        Returns
        -------
        update: dict
            Dictionary containing the details of the processed update status.

        Raises
        ------
        MeiliSearchTimeoutError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        start_time = datetime.now()
        elapsed_time = 0
        while elapsed_time < timeout_in_ms:
            get_update = self.get_update_status(update_id)
            if get_update['status'] != 'enqueued':
                return get_update
            sleep(interval_in_ms / 1000)
            time_delta = datetime.now() - start_time
            elapsed_time = time_delta.seconds * 1000 + time_delta.microseconds / 1000
        raise MeiliSearchTimeoutError(f'timeout of ${timeout_in_ms}ms has exceeded on process ${update_id} when waiting for pending update to resolve.')

    def get_stats(self):
        """Get stats of the index.

        Get information about the number of documents, field frequencies, ...
        https://docs.meilisearch.com/reference/api/stats.html

        Returns
        -------
        stats: dict
            Dictionary containing stats about the given index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.stat}'
        )

    def search(self, query, opt_params=None):
        """Search in the index.

        Parameters
        ----------
        query: str
            String containing the searched word(s)
        opt_params (optional): dict
            Dictionary containing optional query parameters
            https://docs.meilisearch.com/reference/api/search.html#search-in-an-index

        Returns
        -------
        results: dict
            Dictionary with hits, offset, limit, processingTime and initial query

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if opt_params is None:
            opt_params = {}
        body = {
            'q': query,
            **opt_params
        }
        return self.http.post(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.search}',
            body=body
        )

    def get_document(self, document_id):
        """Get one document with given document identifier.

        Parameters
        ----------
        document_id: str
            Unique identifier of the document.

        Returns
        -------
        document: dict
            Dictionary containing the documents information.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}/{document_id}'
        )

    def get_documents(self, parameters=None):
        """Get a set of documents from the index.

        Parameters
        ----------
        parameters (optional): dict
            parameters accepted by the get documents route: https://docs.meilisearch.com/reference/api/documents.html#get-all-documents

        Returns
        -------
        document: dict
            Dictionary containing the documents information.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if parameters is None:
            parameters = {}

        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}?{urllib.parse.urlencode(parameters)}'
        )

    def add_documents(self, documents, primary_key=None):
        """Add documents to the index.

        Parameters
        ----------
        documents: list
            List of documents. Each document should be a dictionary.
        primary_key (optional): string
            The primary-key used in index. Ignored if already set up.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if primary_key is None:
            url = f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}'
        else:
            primary_key = urllib.parse.urlencode({'primaryKey': primary_key})
            url = f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}?{primary_key}'
        return self.http.post(url, documents)

    def update_documents(self, documents, primary_key=None):
        """Update documents in the index.

        Parameters
        ----------
        documents: list
            List of documents. Each document should be a dictionary.
        primary_key (optional): string
            The primary-key used in index. Ignored if already set up

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        if primary_key is None:
            url = f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}'
        else:
            primary_key = urllib.parse.urlencode({'primaryKey': primary_key})
            url = f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}?{primary_key}'
        return self.http.put(url, documents)


    def delete_document(self, document_id):
        """Delete one document from the index.

        Parameters
        ----------
        document_id: str
            Unique identifier of the document.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}/{document_id}'
        )

    def delete_documents(self, ids):
        """Delete multiple documents from the index.

        Parameters
        ----------
        list: list
            List of unique identifiers of documents.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}/delete-batch',
            ids
        )

    def delete_all_documents(self):
        """Delete all documents from the index.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.document}'
        )


    # GENERAL SETTINGS ROUTES

    def get_settings(self):
        """Get settings of the index.

        https://docs.meilisearch.com/reference/api/settings.html

        Returns
        -------
        settings: dict
            Dictionary containing the settings of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.setting}'
        )

    def update_settings(self, body):
        """Update settings of the index.

        https://docs.meilisearch.com/reference/api/settings.html#update-settings

        Parameters
        ----------
        body: dict
            Dictionary containing the settings of the index.
            More information:
            https://docs.meilisearch.com/reference/api/settings.html#update-settings

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.setting}',
            body
        )

    def reset_settings(self):
        """Reset settings of the index to default values.

        https://docs.meilisearch.com/reference/api/settings.html#reset-settings

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            f'{self.config.paths.index}/{self.uid}/{self.config.paths.setting}'
        )

    # RANKING RULES SUB-ROUTES

    def get_ranking_rules(self):
        """
        Get ranking rules of the index.

        Returns
        -------
        settings: list
            List containing the ranking rules of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.ranking_rules)
        )

    def update_ranking_rules(self, body):
        """
        Update ranking rules of the index.

        Parameters
        ----------
        body: list
            List containing the ranking rules.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.ranking_rules),
            body
        )

    def reset_ranking_rules(self):
        """Reset ranking rules of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.ranking_rules),
        )


    # DISTINCT ATTRIBUTE SUB-ROUTES

    def get_distinct_attribute(self):
        """
        Get distinct attribute of the index.

        Returns
        -------
        settings: str | None
            String containing the distinct attribute of the index. If no distinct attribute None is returned.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.distinct_attribute)
        )

    def update_distinct_attribute(self, body):
        """
        Update distinct attribute of the index.

        Parameters
        ----------
        body: str
            String containing the distinct attribute.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.distinct_attribute),
            body
        )

    def reset_distinct_attribute(self):
        """Reset distinct attribute of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.distinct_attribute),
        )

    # SEARCHABLE ATTRIBUTES SUB-ROUTES

    def get_searchable_attributes(self):
        """
        Get searchable attributes of the index.

        Returns
        -------
        settings: list
            List containing the searchable attributes of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.searchable_attributes)
        )

    def update_searchable_attributes(self, body):
        """
        Update searchable attributes of the index.

        Parameters
        ----------
        body: list
            List containing the searchable attributes.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.searchable_attributes),
            body
        )

    def reset_searchable_attributes(self):
        """Reset searchable attributes of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.searchable_attributes),
        )

    # DISPLAYED ATTRIBUTES SUB-ROUTES

    def get_displayed_attributes(self):
        """
        Get displayed attributes of the index.

        Returns
        -------
        settings: list
            List containing the displayed attributes of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.displayed_attributes)
        )

    def update_displayed_attributes(self, body):
        """
        Update displayed attributes of the index.

        Parameters
        ----------
        body: list
            List containing the displayed attributes.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.displayed_attributes),
            body
        )

    def reset_displayed_attributes(self):
        """Reset displayed attributes of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.displayed_attributes),
        )

    # STOP WORDS SUB-ROUTES

    def get_stop_words(self):
        """
        Get stop words of the index.

        Returns
        -------
        settings: list
            List containing the stop words of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.stop_words)
        )

    def update_stop_words(self, body):
        """
        Update stop words of the index.

        Parameters
        ----------
        body: list
            List containing the stop words.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.stop_words),
            body
        )

    def reset_stop_words(self):
        """Reset stop words of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.stop_words),
        )

    # SYNONYMS SUB-ROUTES

    def get_synonyms(self):
        """
        Get synonyms of the index.

        Returns
        -------
        settings: dict
            Dictionary containing the synonyms of the index.

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.synonyms)
        )

    def update_synonyms(self, body):
        """
        Update synonyms of the index.

        Parameters
        ----------
        body: dict
            Dictionary containing the synonyms.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.synonyms),
            body
        )

    def reset_synonyms(self):
        """Reset synonyms of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.synonyms),
        )

    # ATTRIBUTES FOR FACETING SUB-ROUTES

    def get_attributes_for_faceting(self):
        """
        Get attributes for faceting of the index.

        Returns
        -------
        settings: list
            List containing the attributes for faceting of the index

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.get(
            self.__settings_url_for(self.config.paths.attributes_for_faceting)
        )

    def update_attributes_for_faceting(self, body):
        """
        Update attributes for faceting of the index.

        Parameters
        ----------
        body: list
            List containing the attributes for faceting.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.post(
            self.__settings_url_for(self.config.paths.attributes_for_faceting),
            body
        )

    def reset_attributes_for_faceting(self):
        """Reset attributes for faceting of the index to default values.

        Returns
        -------
        update: dict
            Dictionary containing an update id to track the action:
            https://docs.meilisearch.com/reference/api/updates.html#get-an-update-status

        Raises
        ------
        MeiliSearchApiError
            An error containing details about why MeiliSearch can't process your request. MeiliSearch error codes are described here: https://docs.meilisearch.com/errors/#meilisearch-errors
        """
        return self.http.delete(
            self.__settings_url_for(self.config.paths.attributes_for_faceting),
        )

    def __settings_url_for(self, sub_route):
        return f'{self.config.paths.index}/{self.uid}/{self.config.paths.setting}/{sub_route}'
