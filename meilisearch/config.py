class Config:
    """
    A client's credentials and configuration parameters

    """

    def __init__(self, url, apikey=None):
        """
        Parameters
        ----------
        url : str
            The url to the meilisearch API (ex: http://localhost:8080)
        apikey : str
            The optionnal apikey to access meilisearch
        """

        self.url = url
        self.apikey = apikey
