import os
import sys
import time
import json
import pytest
import inspect

current_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

import meilisearch

class TestUpdates:
    client = meilisearch.Client("http://127.0.0.1:7700", "123")

    """ version route """
    def test_get_version(self):
        """Tests an API call to get the version of MeiliSearch"""
        response = self.client.get_version()
        assert 'pkgVersion' in response
