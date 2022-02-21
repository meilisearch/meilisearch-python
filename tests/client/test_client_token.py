# pylint: disable=invalid-name

from re import search
import meilisearch
from tests import BASE_URL, MASTER_KEY
import datetime

def test_generate_tenant_token_with_search_rules(get_private_key, index_with_documents):
    """Tests create a tenant token with only search rules."""
    index_with_documents()
    key = get_private_key

    client = meilisearch.Client(BASE_URL, key['key'])

    token = client.generate_tenant_token(search_rules=["*"])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_generate_tenant_token_with_api_key(client, get_private_key, index_with_documents):
    """Tests create a tenant token with only search rules."""
    index_with_documents()
    key = get_private_key

    token = client.generate_tenant_token(search_rules=["*"], api_key=key['key'])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_generate_tenant_token_with_expired_at(client, get_private_key, index_with_documents):
    """Tests create a tenant token with only search rules."""
    index_with_documents()
    key = get_private_key

    client = meilisearch.Client(BASE_URL, key['key'])

    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1, hours=3)
    timestamp = datetime.datetime.timestamp(tomorrow)

    token = client.generate_tenant_token(search_rules=["*"], expired_at=int(timestamp))

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_generate_tenant_token_without_search_rules(get_private_key, index_with_documents):
    """Tests create a tenant token with only search rules."""
    index_with_documents()
    key = get_private_key

    client = meilisearch.Client(BASE_URL, key['key'])

    token = client.generate_tenant_token(search_rules='')

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''
