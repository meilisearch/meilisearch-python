from typing_extensions import assert_type

from meilisearch import Client
from meilisearch.models.index import WordPosition
from meilisearch.models.task import TaskInfo


def check_index_word_position(client: Client) -> None:
    index = client.index("test")
    assert_type(index.get_word_position_settings(), WordPosition)
    assert_type(index.get_word_position(), WordPosition)
    assert_type(index.update_word_position_settings({"enabled": False}), TaskInfo)
    assert_type(index.update_word_position({"enabled": False}), TaskInfo)
    assert_type(index.reset_word_position_settings(), TaskInfo)
    assert_type(index.reset_word_position(), TaskInfo)
