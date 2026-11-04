from unittest.mock import MagicMock

from meilisearch.config import Config
from meilisearch.models.document import DocumentsResults
from meilisearch.task import TaskHandler


def _make_handler() -> TaskHandler:
    handler = TaskHandler(Config("http://localhost:7700", "masterKey"))
    handler.http = MagicMock()
    return handler


def test_get_task_documents_no_params():
    handler = _make_handler()
    handler.http.get.return_value = {
        "results": [{"id": 1, "title": "foo"}],
        "offset": 0,
        "limit": 20,
        "total": 1,
    }

    result = handler.get_task_documents(1)

    handler.http.get.assert_called_once_with("tasks/1/documents")
    assert isinstance(result, DocumentsResults)
    assert result.total == 1
    assert result.limit == 20
    assert result.offset == 0
    assert dict(result.results[0]) == {"id": 1, "title": "foo"}


def test_get_task_documents_with_params():
    handler = _make_handler()
    handler.http.get.return_value = {
        "results": [],
        "offset": 0,
        "limit": 5,
        "total": 0,
    }

    handler.get_task_documents(2, {"limit": 5, "offset": 10})

    handler.http.get.assert_called_once_with("tasks/2/documents?limit=5&offset=10")
