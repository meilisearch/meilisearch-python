from datetime import datetime
from time import sleep

MASTER_KEY = 'masterKey'
BASE_URL = 'http://127.0.0.1:7700'

def clear_all_indexes(client):
    indexes = client.get_indexes()
    for index in indexes:
        client.get_index(index['uid']).delete()


# Waits until the end of the dump creation.
# Raises a TimeoutError if the `timeout_in_ms` is reached.
def wait_for_dump_creation(client, dump_uid, timeout_in_ms=10000, interval_in_ms=500):
    start_time = datetime.now()
    elapsed_time = 0
    while elapsed_time < timeout_in_ms:
        dump = client.get_dump_status(dump_uid)
        if dump['status'] != 'in_progress':
            return
        sleep(interval_in_ms / 1000)
        time_delta = datetime.now() - start_time
        elapsed_time = time_delta.seconds * 1000 + time_delta.microseconds / 1000
    raise TimeoutError
