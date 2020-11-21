

MASTER_KEY = 'masterKey'
BASE_URL = 'http://127.0.0.1:7700'

index_uid = 'indexUID'
index_uid2 = 'indexUID2'
index_uid3 = 'indexUID3'
index_uid4 = 'indexUID4'


# TODO: move this data
index_fixture = [
	{
		"uid": index_uid
	},
	{
		"uid": index_uid2,
		"options": {'primaryKey': 'book_id'}
	},
	{
		"uid": index_uid3,
		"options": {'uid': 'wrong', 'primaryKey': 'book_id'}
	}
]
