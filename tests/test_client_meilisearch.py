import os
import sys
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import meilisearch

class TestClient:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ Client """
    def test_get_client(self):
        """Tests a call to get a client instance of MeiliSearch"""
        self.client = meilisearch.Client("http://127.0.0.1:7 00", "123")
        assert self.client.config

    def test_get_client_without_apikey(self):
        """Tests a call to get a client instance of MeiliSearch"""
        self.client = meilisearch.Client("http://127.0.0.1:7700")
        assert self.client.config
