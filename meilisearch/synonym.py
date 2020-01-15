# from meilisearch._httprequests import HttpRequests
# import urllib


class Synonym:
    synonym_path = 'search'

    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path

    # def list_one_synonym(self, synonym):
    #     return HttpRequests.get(
    #         self.config,
    #         '{}/{}/{}/{}'.format(
    #             self.index_path,
    #             self.uid,
    #             self.synonym_path,
    #             synonym
    #         )).json()

    # def list_all_synonyms(self):
    #     return HttpRequests.get(
    #         self.config,
    #         '{}/{}/{}'.format(
    #             self.index_path,
    #             self.uid,
    #             self.synonym_path,
    #         )).json()
