class Config:
    """
    A client's credentials and configuration parameters
    """

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
