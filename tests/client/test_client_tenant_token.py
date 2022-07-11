# pylint: disable=invalid-name

from re import search
import pytest
import meilisearch
from tests import BASE_URL, MASTER_KEY
from meilisearch.errors import MeiliSearchApiError
import datetime

def test_generate_tenant_token_with_search_rules(get_private_key, index_with_documents):
    """Tests create a tenant token with only search rules."""
    index_with_documents()
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    token = client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=["*"])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('', {
        'limit': 5
    })
    assert isinstance(response, dict)
    assert len(response['hits']) == 5
    assert response['query'] == ''

def test_generate_tenant_token_with_search_rules_on_one_index(get_private_key, empty_index):
    """Tests create a tenant token with search rules set for one index."""
    empty_index()
    empty_index('tenant_token')
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    token = client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=['indexUID'])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert response['query'] == ''
    with pytest.raises(MeiliSearchApiError):
        response = token_client.index('tenant_token').search('')

def test_generate_tenant_token_with_api_key(client, get_private_key, empty_index):
    """Tests create a tenant token with search rules and an api key."""
    empty_index()
    token = client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=["*"], api_key=get_private_key['key'])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert response['query'] == ''

def test_generate_tenant_token_with_expires_at(client, get_private_key, empty_index):
    """Tests create a tenant token with search rules and expiration date."""
    empty_index()
    client = meilisearch.Client(BASE_URL, get_private_key['key'])
    tomorrow = datetime.datetime.utcnow() + datetime.timedelta(days=1)

    token = client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=["*"], expires_at=tomorrow)

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert response['query'] == ''

def test_generate_tenant_token_with_empty_search_rules_in_list(get_private_key):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=[''])

def test_generate_tenant_token_without_search_rules_in_list(get_private_key):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=[])

def test_generate_tenant_token_without_search_rules_in_dict(get_private_key):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules={})

def test_generate_tenant_token_with_empty_search_rules_in_dict(get_private_key):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules={''})

def test_generate_tenant_token_with_bad_expires_at(client, get_private_key):
    """Tests create a tenant token with a bad expires at."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    yesterday = datetime.datetime.utcnow() + datetime.timedelta(days=-1)

    with pytest.raises(Exception):
        client.generate_tenant_token(api_key_uid=get_private_key['uid'], search_rules=["*"], expires_at=yesterday)

def test_generate_tenant_token_with_no_api_key(client):
    """Tests create a tenant token with no api key."""
    client = meilisearch.Client(BASE_URL)

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules=["*"])

def test_generate_tenant_token_with_no_uid(client, get_private_key):
    """Tests create a tenant token with no uid."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(api_key_uid=None, search_rules=["*"])
