from ._httprequests import HttpRequests

class Schema:
    schema_path = 'schema'
    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path
        pass

    def get_schema(self):
        return HttpRequests.get(self.config, '{}/{}/{}'.format(
            self.index_path,
            self.uid,
            self.schema_path)).json()
    
    def update_schema(self, schema):
        return HttpRequests.put(
            self.config, 
            '{}/{}/{}'.format(
                self.index_path,
                self.uid,
                self.schema_path),
             schema).json()