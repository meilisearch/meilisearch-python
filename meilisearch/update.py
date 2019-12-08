from ._httprequests import HttpRequests

class Update:
    update_path = 'updates'
    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path
        pass
    
    def get_updates(self):
        return HttpRequests.get(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.update_path)).json()
    def get_one_update(self, updateId):
        return HttpRequests.get(self.config, '{}/{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.update_path,
            updateId)).json()