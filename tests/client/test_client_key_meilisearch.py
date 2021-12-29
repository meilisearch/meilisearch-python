import pytest
from tests import common
from datetime import datetime, timedelta

def test_get_keys_default(client):
    """Tests if public and private keys have been generated and can be retrieved."""
    key = client.get_keys()
    assert isinstance(key, list)
    assert len(key) >= 2
    assert 'actions' in key[0]
    assert 'indexes' in key[0]
    assert key[0]['key'] is not None
    assert key[1]['key'] is not None

def test_get_key(client):
    """Tests if a key can be retrieved."""
    keys = client.get_keys()
    key = client.get_key(keys[0]['key'])
    assert isinstance(key, dict)
    assert 'actions' in key
    assert 'indexes' in key
    assert key['createdAt'] is not None

def test_get_key_inexistent(client):
    """Tests getting a key that does not exists."""
    with pytest.raises(Exception):
        client.get_key('No existing key')

def test_create_keys_default(client):
    """Tests the creation of a key with no optional argument."""
    key = client.create_key(options={ 'actions': ['*'], 'indexes': [common.INDEX_UID], 'expiresAt': None })
    assert isinstance(key, dict)
    assert 'key' in key
    assert 'actions' in key
    assert 'indexes' in key
    assert key['key'] is not None
    assert key['expiresAt'] is None
    assert key['createdAt'] is not None
    assert key['updatedAt'] is not None
    assert key['key'] is not None
    assert key['actions'] == ['*']
    assert key['indexes'] == [common.INDEX_UID]

def test_create_keys_with_options(client):
    """Tests the creation of a key with arguments."""
    key = client.create_key(options={ 'actions': ['*'], 'indexes': [common.INDEX_UID], 'description': 'Test key', 'expiresAt': datetime(2030, 6, 4, 21, 8, 12, 32).isoformat()[:-3]+'Z' })
    assert isinstance(key, dict)
    assert key['key'] is not None
    assert key['description'] == 'Test key'
    assert key['expiresAt'] is not None
    assert key['createdAt'] is not None
    assert key['updatedAt'] is not None
    assert key['actions'] == ['*']
    assert key['indexes'] == [common.INDEX_UID]

def test_create_keys_without_actions(client):
    """Tests the creation of a key with missing arguments."""
    with pytest.raises(Exception):
        client.create_key(options={'indexes': [common.INDEX_UID]})

def test_update_keys(client):
    """Tests updating a key."""
    key = client.create_key(options={ 'actions': ['*'], 'indexes': ['*'], 'expiresAt': None })
    assert key['actions'] == ['*']
    update_key = client.udpate_key(key=key['key'], options={ 'actions': ['search'] })
    assert update_key['key'] is not None
    assert update_key['expiresAt'] is None
    assert update_key['actions'] == ['search']

def test_delete_key(client):
    """Tests deleting a key."""
    key = client.create_key(options={ 'actions': ['*'], 'indexes': ['*'], 'expiresAt': None })
    resp = client.delete_key(key['key'])
    assert resp.status_code == 204

def test_delete_key_inexisting(client):
    """Tests deleting a key that does not exists."""
    with pytest.raises(Exception):
        client.delete_key('No existing key')
