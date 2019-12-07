from .index import Index
from ._httprequests import HttpRequests

class Document(Index):
    path = '/document/'
    def delete(self):
        return HttpRequests.delete(self.config, '{}/{}'.format(Index.path, self.uid))
    
    def update(self, **body):
        payload = {}
        name = body.get("name", None)
        if name is not None:
            payload["name"] = name
        return HttpRequests.put(self.config, '{}/{}'.format(Index.path, self.uid), payload).json()

    # TODO : should this be called get or info
    def info(self):
        return HttpRequests.get(self.config, '{}/{}'.format(Index.path, self.uid)).json()
    
    def update_schema(self, schema):
        return HttpRequests.put(self.config, '{}/{}'.format(Index.path, self.uid)).json()
