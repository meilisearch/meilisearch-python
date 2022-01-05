MASTER_KEY = 'masterKey'
BASE_URL = 'http://127.0.0.1:7700'

INDEX_UID = 'indexUID'
INDEX_UID2 = 'indexUID2'
INDEX_UID3 = 'indexUID3'
INDEX_UID4 = 'indexUID4'

INDEX_FIXTURE = [
    {
        "uid": INDEX_UID
    },
    {
        "uid": INDEX_UID2,
        "options": {'primaryKey': 'book_id'}
    },
    {
        "uid": INDEX_UID3,
        "options": {'uid': 'wrong', 'primaryKey': 'book_id'}
    }
]
