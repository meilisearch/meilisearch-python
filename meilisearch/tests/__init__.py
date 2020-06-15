MASTER_KEY = 'masterKey'
BASE_URL = 'http://127.0.0.1:7700'

def clear_all_indexes(client):
    indexes = client.get_indexes()
    for index in indexes:
        client.get_index(index['uid']).delete()
