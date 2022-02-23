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

    token = client.generate_tenant_token(search_rules=["*"])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_generate_tenant_token_with_api_key(client, get_private_key, index_with_documents):
    """Tests create a tenant token with only search rules."""
    index_with_documents()
    token = client.generate_tenant_token(search_rules=["*"], api_key=get_private_key['key'])

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_generate_tenant_token_with_expires_at(client, get_private_key, index_with_documents):
    """Tests create a tenant token with search rules and expiration date."""
    index_with_documents()
    client = meilisearch.Client(BASE_URL, get_private_key['key'])
    tomorrow = datetime.datetime.now() + datetime.timedelta(days=1)

    token = client.generate_tenant_token(search_rules=["*"], expires_at=tomorrow)

    token_client = meilisearch.Client(BASE_URL, token)
    response = token_client.index('indexUID').search('')
    assert isinstance(response, dict)
    assert len(response['hits']) == 20
    assert response['query'] == ''

def test_generate_tenant_token_with_empty_search_rules_in_list(get_private_key, index_with_documents):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules=[''])

def test_generate_tenant_token_without_search_rules_in_list(get_private_key, index_with_documents):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules=[])

def test_generate_tenant_token_without_search_rules_in_dict(get_private_key, index_with_documents):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules={})

def test_generate_tenant_token_wit_empty_search_rules_in_dict(get_private_key, index_with_documents):
    """Tests create a tenant token without search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules={''})

def test_generate_tenant_token_with_master_key(client, index_with_documents):
    """Tests create a tenant token with master key."""
    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules=['*'])

def test_generate_tenant_token_with_bad_expires_at(client, get_private_key):
    """Tests create a tenant token with only search rules."""
    client = meilisearch.Client(BASE_URL, get_private_key['key'])

    yesterday = datetime.datetime.now() + datetime.timedelta(days=-1)

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules=["*"], expires_at=yesterday)

def test_generate_tenant_token_with_no_api_key(client):
    """Tests create a tenant token with only search rules."""
    client = meilisearch.Client(BASE_URL)

    with pytest.raises(Exception):
        client.generate_tenant_token(search_rules=["*"])

