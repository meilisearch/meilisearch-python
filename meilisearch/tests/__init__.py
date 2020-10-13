import time

MASTER_KEY = 'masterKey'
BASE_URL = 'http://127.0.0.1:7700'

def clear_all_indexes(client):
    indexes = client.get_indexes()
    for index in indexes:
        client.get_index(index['uid']).delete()

def wait_for_dump_creation(client, dump_uid):
    dump_status = client.get_dump_status(dump_uid)
    while dump_status['status'] == 'processing':
        time.sleep(0.1)
        dump_status = client.get_dump_status(dump_uid)
