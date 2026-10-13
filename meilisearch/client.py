from __future__ import annotations

import base64
import datetime
import hashlib
import hmac
import json
import re
from collections.abc import Iterator, Mapping, Sequence
from typing import Any
from urllib import parse

from meilisearch._httprequests import HttpRequests
from meilisearch.config import Config
from meilisearch.errors import MeilisearchApiError
from meilisearch.index import Index
from meilisearch.models.task import TaskInfo, TaskResults
from meilisearch.task import TaskHandler

class Client:
    """
    A client for the Meilisearch API

    A client instance can be used to access all indexes in a Meilisearch server.
    https://www.meilisearch.com/docs/reference/api/client
    """

    def __init__(
        self,
        url: str,
        api_key: str | None = None,
        *,
        timeout: int | None = None,
        client_agents: tuple[str, ...] | None = None,
        custom_headers: Mapping[str, str] | None = None,
    ) -> None:
        """
        Parameters
        ----------
        url:
            The url to the Meilisearch API (ex: http://localhost:7700)
        api_key:
            The optional API key to access Meilisearch
        timeout (optional):
            The amount of time in seconds that the client will wait for a response from the server.
            If the server does not respond within the specified time, the client will raise a MeilisearchTimeoutError.
        client_agents (optional):
            A tuple of strings that will be added to the User-Agent header of the client.
            This is useful for identifying the client that is making the request.
        custom_headers (optional):
            Custom headers to add when sending data to Meilisearch.
        """

        self.config = Config(url, api_key, timeout=timeout, client_agents=client_agents)

        # Store custom headers so they can be propagated to sub-clients (Index, TaskHandler, etc.)
        self._custom_headers = custom_headers

        self.http = HttpRequests(self.config, custom_headers)

        self.task_handler = TaskHandler(self.config, custom_headers)

    # ... (rest of the file remains the same, only docstring changed; full file update)
