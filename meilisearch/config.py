class Config:
    """
    A client's credentials and configuration parameters

    Attributes
    ----------
    url : str
        The url to the meilisearch API (ex: http://localhost:8080)
    apikey : str
        The optionnal apikey to access meilisearch 
    """
    def __init__(self, url, apikey=None):
        self.url = url
        self.apikey = apikey