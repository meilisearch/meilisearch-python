from typing import Any

from typing_extensions import assert_type

from meilisearch import Client
from meilisearch.index import Index


def check_index_pagination(client: Client) -> None:
    indexes = client.get_indexes()
    assert_type(indexes["results"], list[Index])
    assert_type(indexes["limit"], int)
    assert_type(indexes["offset"], int)
    assert_type(indexes["total"], int)

    raw = client.get_raw_indexes()
    assert_type(raw["results"], list[dict[str, Any]])
    assert_type(raw["limit"], int)
    assert_type(raw["offset"], int)
    assert_type(raw["total"], int)
