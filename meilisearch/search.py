from ._httprequests import HttpRequests
import urllib

class Search:
    search_path = 'search'

    def __init__(self, parent_path, config, uid=None, name=None):
        self.config = config
        self.name = name
        self.uid = uid
        self.index_path = parent_path

    def search(self, parameters):
        return HttpRequests.get(
            self.config, 
            '{}/{}/{}?{}'.format(
                self.index_path,
                self.uid,
                self.search_path,
                urllib.parse.urlencode(parameters))
            ).json()