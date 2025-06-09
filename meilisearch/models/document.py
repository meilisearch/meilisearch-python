from typing import Any, Dict, Iterator, List


class Document:
    def __init__(self, doc: Dict[str, Any]) -> None:
        self.__dict__.update(**doc)

    def __getattr__(self, attr: str) -> Any:
        if attr in self.__dict__:
            return self.__dict__[attr]
        raise AttributeError(f"{self.__class__.__name__} object has no attribute {attr}")

    def __iter__(self) -> Iterator:
        return iter(self.__dict__.items())


class DocumentsResults:
    def __init__(self, resp: Dict[str, Any]) -> None:
        self.results: List[Document] = [Document(doc) for doc in resp["results"]]
        self.offset: int = resp["offset"]
        self.limit: int = resp["limit"]
        self.total: int = resp["total"]
