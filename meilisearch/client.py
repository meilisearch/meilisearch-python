import pdb
import requests
# from meilisearch._http_request import HttpRequest
class Config:
    def __init__(self, url, apikey):
        self.url = url
        self.apikey = apikey


class Index():
    def __init__(self, name, config):
        self.name = name
        self.config = config
        # create_index request

    def add_documents():
        print("qweqwe")
        # create add_documents request

class Client():
    def __init__(self, url, apikey):
        self.config = Config(url, apikey)
    
    def create_index(self, name):
        return Index(name, self.config)

pdb.set_trace()
clienta = Client("url","apikey")
print(clienta.config.url)