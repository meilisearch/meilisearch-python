MASTER_KEY = 'masterKey'
BASE_URL = 'http://127.0.0.1:7700'

def clear_all_indexes(client):
    indexes = client.get_indexes()
    uids = [index['uid'] for index in indexes]
    for uid in uids:
        client.get_index(uid).delete()
