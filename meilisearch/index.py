from ._httprequests import HttpRequests

class Index:
    path = '/indexes'

    def __init__(self, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        print('name is {} and uid is {}'.format(self.name, self.uid))
    

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
    
    @staticmethod
    def create(config, **body):
        payload = {}
        name = body.get("name", None)
        uid = body.get("uid", None)
        if name is not None:
            payload["name"] = name
        if uid is not None:
            payload["uid"] = uid
        response = HttpRequests.post(config, Index.path, payload)
        return  response.json()

    @staticmethod
    def get_all_indexes(config):
        return HttpRequests.get(config, Index.path).json()

    @staticmethod
    def get_index(config, **params):
        name = params.get("name", None)
        uid = params.get("uid", None)
        if uid is not None:
            return Index(config, uid=uid, name=name)
        elif name is not None:
            indexes = Index.get_all_indexes(config)
            index = list(filter(lambda index: index["name"] == name, indexes))
            if len(index) == 0:
                raise Exception('Index not found')
            index = index[0]
            return Index(config, name=index["name"], uid=index["uid"])

    def add_documents(self):
            print("qweqwe")
        # create add_documents request