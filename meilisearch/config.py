class Config:
    """
    A client's credentials and configuration parameters
    """

    class Paths():
        health = "health"
        keys = 'keys'
        sys_info = 'sys-info'
        version = 'version'
        index = 'indexes'
        update = 'updates'
        stat = 'stats'
        search = 'search'
        document = 'documents'
        setting = 'settings'
        ranking_rules = 'ranking-rules'
        distinct_attribute = 'distinct-attribute'
        searchable_attributes = 'searchable-attributes'
        displayed_attributes = 'displayed-attributes'
        stop_words = 'stop-words'
        synonyms = 'synonyms'
        accept_new_fields = 'accept-new-fields'

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
        self.paths = self.Paths()
