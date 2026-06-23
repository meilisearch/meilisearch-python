import json
import re
from datetime import datetime
from functools import lru_cache
from typing import Any, Dict, List, Union

import pydantic

_CONCATENATED_JSON = re.compile(r"(?<=\})\s*(?=\{)")


@lru_cache(maxsize=1)
def is_pydantic_2() -> bool:
    try:
        # __version__ was added with Pydantic 2 so we know if this errors the version is < 2.
        # Still check the version as a fail safe incase __version__ gets added to verion 1.
        if int(pydantic.__version__[:1]) >= 2:  # type: ignore[attr-defined]
            return True

        # Raise an AttributeError to match the AttributeError on __version__ because in either
        # case we need to get to the same place.
        raise AttributeError  # pragma: no cover
    except AttributeError:  # pragma: no cover
        return False


def iso_to_date_time(iso_date: Union[datetime, str, None]) -> Union[datetime, None]:
    """Handle conversion of iso string to datetime.

    The microseconds from Meilisearch are sometimes too long for python to convert so this
    strips off the last digits to shorten it when that happens.
    """
    if not iso_date:
        return None

    if isinstance(iso_date, datetime):
        return iso_date

    try:
        return datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S.%fZ")
    except ValueError:
        split = iso_date.split(".")
        if len(split) < 2:
            raise
        reduce = len(split[1]) - 6
        reduced = f"{split[0]}.{split[1][:-reduce]}Z"
        return datetime.strptime(reduced, "%Y-%m-%dT%H:%M:%S.%fZ")


def parse_task_documents(raw_documents: str) -> List[Dict[str, Any]]:
    """Parse the payload returned by ``GET /tasks/{uid}/documents``.

    The endpoint may return a JSON array, a single JSON object, NDJSON, or
    several JSON objects concatenated without a separator. This normalizes all
    of those formats into a list of documents.
    """
    payload = raw_documents.strip()
    if not payload:
        return []

    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        documents: List[Dict[str, Any]] = []
        for line in payload.splitlines():
            for chunk in _CONCATENATED_JSON.split(line):
                stripped = chunk.strip()
                if stripped:
                    documents.append(json.loads(stripped))
        return documents

    return parsed if isinstance(parsed, list) else [parsed]
