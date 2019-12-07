import pdb
from client import Client
from index import Index
from config import Config

pdb.set_trace()
clienta = Client("http://127.0.0.1:7700", None)

print(clienta.get_all_indexes().json())
# print(clienta.config.url)
# index2 = clienta.create_index(name="movies")
# print(index2.uid, "uid")