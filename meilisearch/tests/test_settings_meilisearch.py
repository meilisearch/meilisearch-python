import meilisearch

class TestKey:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ settings route """
    def test_add_settings(self):
        """Tests an API call to add setting to an index in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.add_settings({
            "rankingOrder": [
                "_sum_of_typos",
                "_number_of_words",
                "_word_proximity",
                "_sum_of_words_attribute",
                "_sum_of_words_position",
                "_exact",
                "release_date"
            ],
            "distinctField": "",
            "rankingRules": {
                "release_date": "dsc"
            }
        })
        assert isinstance(response, object)
        assert 'updateId' in response

    def test_update_settings(self):
        """Tests an API call to update settings of an index in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.replace_settings({
            "rankingOrder": [
                "_sum_of_typos",
                "_number_of_words",
                "_word_proximity",
                "_sum_of_words_attribute",
                "_sum_of_words_position",
                "_exact",
                "release_date"
            ],
            "distinctField": "",
            "rankingRules": {
                "release_date": "dsc"
            }
        })
        assert isinstance(response, object)
        assert 'updateId' in response


    def test_get_settings(self):
        """Tests an API call to get settings of an index in MeiliSearch"""
        index = self.client.get_index(uid="movies_uid")
        response = index.get_settings()
        assert isinstance(response, object)
        assert 'rankingOrder' in response
