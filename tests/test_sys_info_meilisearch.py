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

    """ sys-info route """
    def test_get_sys_info(self):
        """Tests an API call to check the system information of MeiliSearch"""
        response = self.client.get_sys_info()
        assert 'memoryUsage' in response
