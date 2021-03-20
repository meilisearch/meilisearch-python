class Config:
    """
    Client's credentials and configuration parameters
    """

    class Paths():
        health = "health"
        keys = 'keys'
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
        attributes_for_faceting = 'attributes-for-faceting'
        dumps = 'dumps'

    def __init__(self, url, api_key=None, timeout=None):
        """
        Parameters
        ----------
        url: str
            The url to the MeiliSearch API (ex: http://localhost:7700)
        api_key (optional): str
            The optional API key to access MeiliSearch
        """

        self.url = url
        self.api_key = api_key
        self.timeout = timeout
        self.paths = self.Paths()
