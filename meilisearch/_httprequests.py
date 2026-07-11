from __future__ import annotations

import json
from collections.abc import Callable, Mapping, Sequence
from functools import lru_cache
from typing import Any

import requests

from meilisearch.config import Config
from meilisearch.errors import (
    MeilisearchApiError,
    MeilisearchCommunicationError,
    MeilisearchTimeoutError,
)
from meilisearch.models.index import PrefixSearch, ProximityPrecision
from meilisearch.version import qualified_version


class HttpRequests:
    def __init__(self, config: Config, custom_headers: Mapping[str, str] | None = None) -> None:
        self.config = config
        self.headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "User-Agent": _build_user_agent(config.client_agents),
        }

        if custom_headers is not None:
            self.headers.update(custom_headers)

    def send_request(
        self,
        http_method: Callable,
        path: str,
        body: Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | list[str]
        | bool
        | bytes
        | str
        | int
        | ProximityPrecision
        | None = None,
        content_type: str | None = None,
        *,
        serializer: type[json.JSONEncoder] | None = None,
    ) -> Any:
        if content_type:
            self.headers["Content-Type"] = content_type
        else:
            self.headers.pop("Content-Type", None)
        try:
            request_path = self.config.url + "/" + path
            if http_method.__name__ == "get":
                request = http_method(
                    request_path,
                    timeout=self.config.timeout,
                    headers=self.headers,
                )
            elif isinstance(body, bytes):
                request = http_method(
                    request_path,
                    timeout=self.config.timeout,
                    headers=self.headers,
                    data=body,
                )
            else:
                serialize_body = isinstance(body, dict) or body
                data = (
                    json.dumps(body, cls=serializer)
                    if isinstance(body, bool) or serialize_body
                    else ""
                    if body == ""
                    else "null"
                )

                request = http_method(
                    request_path, timeout=self.config.timeout, headers=self.headers, data=data
                )
            return self.__validate(request)

        except requests.exceptions.Timeout as err:
            raise MeilisearchTimeoutError(str(err)) from err
        except requests.exceptions.ConnectionError as err:
            raise MeilisearchCommunicationError(str(err)) from err
        except requests.exceptions.InvalidSchema as err:
            if "://" not in self.config.url:
                raise MeilisearchCommunicationError(
                    f"""
                    Invalid URL {self.config.url}, no scheme/protocol supplied.
                    Did you mean https://{self.config.url}?
                    """
                ) from err

            raise MeilisearchCommunicationError(str(err)) from err

    def get(self, path: str) -> Any:
        return self.send_request(requests.get, path)

    def post(
        self,
        path: str,
        body: Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | list[str]
        | bytes
        | str
        | None = None,
        content_type: str | None = "application/json",
        *,
        serializer: type[json.JSONEncoder] | None = None,
    ) -> Any:
        return self.send_request(requests.post, path, body, content_type, serializer=serializer)

    def patch(
        self,
        path: str,
        body: Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | list[str]
        | bytes
        | str
        | None = None,
        content_type: str | None = "application/json",
    ) -> Any:
        return self.send_request(requests.patch, path, body, content_type)

    def put(
        self,
        path: str,
        body: Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | list[str]
        | bool
        | bytes
        | str
        | int
        | PrefixSearch
        | ProximityPrecision
        | None = None,
        content_type: str | None = "application/json",
        *,
        serializer: type[json.JSONEncoder] | None = None,
    ) -> Any:
        return self.send_request(requests.put, path, body, content_type, serializer=serializer)

    def delete(
        self,
        path: str,
        body: Mapping[str, Any] | Sequence[Mapping[str, Any]] | list[str] | None = None,
    ) -> Any:
        return self.send_request(requests.delete, path, body)

    def post_stream(
        self,
        path: str,
        body: Mapping[str, Any]
        | Sequence[Mapping[str, Any]]
        | list[str]
        | bytes
        | str
        | None = None,
        content_type: str | None = "application/json",
        *,
        serializer: type[json.JSONEncoder] | None = None,
    ) -> requests.Response:
        """Send a POST request with streaming enabled.

        Returns the raw response object for streaming consumption.
        """
        if content_type:
            self.headers["Content-Type"] = content_type
        else:
            self.headers.pop("Content-Type", None)
        try:
            request_path = self.config.url + "/" + path

            if isinstance(body, bytes):
                response = requests.post(
                    request_path,
                    timeout=self.config.timeout,
                    headers=self.headers,
                    data=body,
                    stream=True,
                )
            else:
                serialize_body = isinstance(body, dict) or body
                data = (
                    json.dumps(body, cls=serializer)
                    if isinstance(body, bool) or serialize_body
                    else ""
                    if body == ""
                    else "null"
                )

                response = requests.post(
                    request_path,
                    timeout=self.config.timeout,
                    headers=self.headers,
                    data=data,
                    stream=True,
                )

            # For streaming responses, we validate status but don't parse JSON
            if not response.ok:
                response.raise_for_status()

            return response

        except requests.exceptions.Timeout as err:
            raise MeilisearchTimeoutError(str(err)) from err
        except requests.exceptions.ConnectionError as err:
            raise MeilisearchCommunicationError(str(err)) from err
        except requests.exceptions.HTTPError as err:
            raise MeilisearchApiError(str(err), response) from err
        except requests.exceptions.InvalidSchema as err:
            if "://" not in self.config.url:
                raise MeilisearchCommunicationError(
                    f"""
                    Invalid URL {self.config.url}, no scheme/protocol supplied.
                    Did you mean https://{self.config.url}?
                    """
                ) from err

            raise MeilisearchCommunicationError(str(err)) from err

    @staticmethod
    def __to_json(request: requests.Response) -> Any:
        if request.content == b"":
            return request
        return request.json()

    @staticmethod
    def __validate(request: requests.Response) -> Any:
        try:
            request.raise_for_status()
            return HttpRequests.__to_json(request)
        except requests.exceptions.HTTPError as err:
            raise MeilisearchApiError(str(err), request) from err


@lru_cache(maxsize=1)
def _build_user_agent(client_agents: tuple[str, ...] | None = None) -> str:
    user_agent = qualified_version()
    if not client_agents:
        return user_agent

    return f"{user_agent};{';'.join(client_agents)}"
