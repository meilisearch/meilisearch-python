from .index import Index
from .config import Config

class Client:
    def __init__(self, url, apikey):
        self.config = Config(url, apikey)
    
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
