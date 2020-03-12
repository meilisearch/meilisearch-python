# from meilisearch._httprequests import HttpRequests

class Synonym:
    synonym_path = 'search'

    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path
