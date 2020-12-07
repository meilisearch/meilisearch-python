
def test_get_version(client):
    """Tests getting the version of the MeiliSearch instance."""
    response = client.get_version()
    assert 'pkgVersion' in response
    assert 'commitSha' in response
    assert 'buildDate' in response
