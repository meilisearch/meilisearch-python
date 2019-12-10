from .index import Index
from .health import Health
from .key import Key
from .config import Config

class Client(Health, Key):
    """
    A client for the meilisearch API

    A client instance is needed for every meilisearch API method to know the location of 
    meilisearch and his permissions.

    Attributes
    ----------
    url : str
        The url to the meilisearch API (ex: http://localhost:8080)
    apikey : str
        The optionnal apikey to access the meilisearch api 

    """

    def __init__(self, url, apikey):
        """
        Parameters
        ----------
        url : str
            The url to the meilisearch API (ex: http://localhost:8080)
        apikey : str
            The optionnal apikey to access the meilisearch api 
        """
        config = Config(url, apikey)
        Health.__init__(self, config)
        Key.__init__(self, config)
        self.config = config
    
    def create_index(self, **body):
        name = body.get("name", None)
        uid = body.get("uid", None)
        index = Index.create(self.config, name=name, uid=uid)
        return Index(self.config, name=index["name"], uid=index["uid"])

    def get_all_indexes(self):
        return Index.get_all_indexes(self.config)

    def get_index(self, uid=None, name=None):
        print('Client', uid, name)
        return Index.get_index(self.config, uid=uid, name=name)
