import json
from typing import Any, Callable, Dict, List, Optional, Union
import requests
from meilisearch.config import Config
from meilisearch.errors import (
    MeiliSearchApiError,
    MeiliSearchCommunicationError,
    MeiliSearchTimeoutError,
)
from meilisearch.version import qualified_version

class HttpRequests:
    def __init__(self, config: Config) -> None:
        self.config = config
        self.headers = {
            'Authorization': f'Bearer {self.config.api_key}',
            'User-Agent': qualified_version(),
        }

    def send_request(
        self,
        http_method: Callable,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
        content_type: Optional[str] = None,
    ) -> Any:
        if content_type:
            self.headers['Content-Type'] = content_type
        try:
            request_path = self.config.url + '/' + path
            if isinstance(body, bytes):
                request = http_method(
                    request_path,
                    timeout=self.config.timeout,
                    headers=self.headers,
                    data=body
                )
            else:
                request = http_method(
                    request_path,
                    timeout=self.config.timeout,
                    headers=self.headers,
                    data=json.dumps(body) if body else "null"
                )
            return self.__validate(request)

        except requests.exceptions.Timeout as err:
            raise MeiliSearchTimeoutError(str(err)) from err
        except requests.exceptions.ConnectionError as err:
            raise MeiliSearchCommunicationError(str(err)) from err

    def get(
        self, path: str
    ) -> Any:
        return self.send_request(requests.get, path)

    def post(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
        content_type: Optional[str] = 'application/json',
    ) -> Any:
        return self.send_request(requests.post, path, body, content_type)

    def patch(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str], str]] = None,
        content_type: Optional[str] = 'application/json',
    ) -> Any:
        return self.send_request(requests.patch, path, body, content_type)

    def put(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str]]] = None,
        content_type: Optional[str] = 'application/json',
    ) -> Any:
        return self.send_request(requests.put, path, body, content_type)

    def delete(
        self,
        path: str,
        body: Optional[Union[Dict[str, Any], List[Dict[str, Any]], List[str]]] = None,
    ) -> Any:
        return self.send_request(requests.delete, path, body)

    @staticmethod
    def __to_json(
        request: requests.Response
    ) -> Any:
        if request.content == b'':
            return request
        return request.json()

    @staticmethod
    def __validate(
        request: requests.Response
    ) -> Any:
        try:
            request.raise_for_status()
            return HttpRequests.__to_json(request)
        except requests.exceptions.HTTPError as err:
            raise MeiliSearchApiError(str(err), request) from err
