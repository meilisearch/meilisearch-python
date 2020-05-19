class Config:
    """
    A client's credentials and configuration parameters
    """

    health_path = "health"
    key_path = 'keys'
    sys_info_path = 'sys-info'
    version_path = 'version'
    index_path = 'indexes'
    update_path = 'updates'
    stat_path = 'stats'
    search_path = 'search'
    document_path = 'documents'
    setting_path = 'settings'
    ranking_rules_path = 'ranking-rules'
    distinct_attribute_path = 'distinct-attribute'
    searchable_attributes_path = 'searchable-attributes'
    displayed_attributes_path = 'displayed-attributes'
    stop_words_path = 'stop-words'
    synonyms_path = 'synonyms'
    accept_new_fields_path = 'accept-new-fields'

    def __init__(self, url, apikey=None):
        """
        Parameters
        ----------
        url : str
            The url to the MeiliSearch API (ex: http://localhost:7700)
        apikey : str
            The optional API key to access MeiliSearch
        """

        self.url = url
        self.apikey = apikey
