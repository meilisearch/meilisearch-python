# pylint: disable=invalid-name


def test_snapshot_creation(client, index_with_documents):
    """Tests the creation of a Meilisearch snapshot."""
    index_with_documents("indexUID-snapshot-creation")
    snapshot= client.create_snapshot()
    client.wait_for_task(snapshot.task_uid)
    snapshot_status = client.get_task(snapshot.task_uid)
    assert snapshot_status.status == "succeeded"
    assert snapshot_status.type == "snapshotCreation"