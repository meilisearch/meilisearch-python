import meilisearch

class TestSearch:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ search route """
    def test_search_documents(self):
        index = self.client.get_index(uid="movies_uid")
        response = index.search({
            'q': 'How to Train Your Dragon'
        })
        assert isinstance(response, object)
        assert response["hits"][0]["id"] == '166428'
