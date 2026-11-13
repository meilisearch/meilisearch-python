from unittest.mock import MagicMock

from meilisearch.config import Config
from meilisearch.task import TaskHandler


def _make_handler() -> TaskHandler:
    handler = TaskHandler(Config("http://localhost:7700", "masterKey"))
    handler.http = MagicMock()
    return handler


def test_get_task_documents():
    handler = _make_handler()
    handler.http.get.return_value = '{"id":1,"title":"foo"}\n{"id":2,"title":"bar"}\n'

    result = handler.get_task_documents(1)

    handler.http.get.assert_called_once_with("tasks/1/documents", raw=True)
    assert result == [{"id": 1, "title": "foo"}, {"id": 2, "title": "bar"}]


def test_get_task_documents_empty_body():
    handler = _make_handler()
    handler.http.get.return_value = ""

    assert handler.get_task_documents(2) == []
    handler.http.get.assert_called_once_with("tasks/2/documents", raw=True)


def test_get_task_documents_keeps_unicode_line_separators():
    handler = _make_handler()
    handler.http.get.return_value = '{"id":1,"title":"a\u2028b"}\n{"id":2,"title":"caf\u00e9"}\n'

    assert handler.get_task_documents(3) == [
        {"id": 1, "title": "a\u2028b"},
        {"id": 2, "title": "caf\u00e9"},
    ]
