from ._httprequests import HttpRequests
from .schema import Schema
from .update import Update
from .document import Document
from .synonym import Synonym
from .search import Search

class Index(Schema, Update, Document, Search, Synonym):
    index_path = '/indexes'

    def __init__(self, config, uid=None, name=None):
        Schema.__init__(self, Index.index_path, config, name, uid)
        Update.__init__(self, Index.index_path, config, name, uid)
        Search.__init__(self, Index.index_path, config, name, uid)
        Document.__init__(self, Index.index_path, config, name, uid)
        Synonym.__init__(self, Index.index_path, config, name, uid)
        self.config = config
        self.name = name
        self.uid = uid
        print('name is {} and uid is {}'.format(self.name, self.uid))
    

    def delete(self):
        return HttpRequests.delete(self.config, '{}/{}'.format(self.index_path, self.uid))
    
    def update(self, **body):
        payload = {}
        name = body.get("name", None)
        if name is not None:
            payload["name"] = name
        return HttpRequests.put(self.config, '{}/{}'.format(self.index_path, self.uid), payload).json()

    def info(self):
        return HttpRequests.get(self.config, '{}/{}'.format(self.index_path, self.uid)).json()
        
    @staticmethod
    def create(config, **body):
        payload = {}
        name = body.get("name", None)
        uid = body.get("uid", None)
        if name is not None:
            payload["name"] = name
        if uid is not None:
            payload["uid"] = uid
        response = HttpRequests.post(config, Index.index_path, payload)
        return  response.json()

    @staticmethod
    def get_all_indexes(config):
        return HttpRequests.get(config, Index.index_path).json()

    @staticmethod
    def get_index(config, **params):
        name = params.get("name", None)
        uid = params.get("uid", None)
        if uid is not None:
            return Index(config, uid=uid, name=name)
        if name is None:
            raise Exception('Name or Uid is needed to find index')
        indexes = Index.get_all_indexes(config)
        index = list(filter(lambda index: index["name"] == name, indexes))
        if len(index) == 0:
            raise Exception('Index not found')
        index = index[0]
        return Index(config, name=index["name"], uid=index["uid"])