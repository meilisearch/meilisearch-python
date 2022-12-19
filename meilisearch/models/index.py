from __future__ import annotations

from typing import Any, Dict, Iterator

from camel_converter import to_snake


class IndexStats:
    __dict: Dict

    def __init__(self, doc: Dict[str, Any]) -> None:
        self.__dict = doc
        for key, val in doc.items():
            key = to_snake(key)
            if isinstance(val, dict):
                setattr(self, key, IndexStats(val))
            else:
                setattr(self, key, val)

    def __getattr__(self, attr: str) -> Any:
        if attr in self.__dict.keys():
            return attr
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())  # type: ignore
