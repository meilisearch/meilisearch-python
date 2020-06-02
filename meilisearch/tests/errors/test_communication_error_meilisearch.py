import pytest
import meilisearch
from meilisearch.errors import MeiliSearchCommunicationError
from meilisearch.tests import MASTER_KEY

class TestMeiliSearchCommunicationError:

    """ TESTS: MeiliSearchCommunicationError class """

    @staticmethod
    def test_meilisearch_communication_error_host():
        client = meilisearch.Client("http://wrongurl:1234", MASTER_KEY)
        with pytest.raises(MeiliSearchCommunicationError):
            client.create_index("some_index")
