# pylint: disable=invalid-name

def test_dump_creation(client, index_with_documents):
    """Tests the creation of a Meilisearch dump."""
    index_with_documents("indexUID-dump-creation")
    dump = client.create_dump()
    assert dump['taskUid'] is not None
    client.wait_for_task(dump['taskUid'])
    dump_status = client.get_task(dump['taskUid'])
    assert dump_status['status'] == 'succeeded'
    assert dump_status['type'] == 'dumpCreation'
