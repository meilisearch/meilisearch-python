import json
import requests
from meilisearch.errors import (
    MeiliSearchApiError,
    MeiliSearchCommunicationError,
    MeiliSearchTimeoutError,
)

class HttpRequests:
    def __init__(self, config):
        self.config = config
        self.headers = {
            'X-Meili-Api-Key': self.config.api_key,
            'Content-Type': 'application/json'
        }

    def send_request(self, http_method, path, body=None):
        try:
            request_path = self.config.url + '/' + path
            request = http_method(
                request_path,
                timeout=self.config.timeout,
                headers=self.headers,
                data=json.dumps(body) if body else "null"
            )
            return self.__validate(request)

        except requests.exceptions.Timeout as err:
            raise MeiliSearchTimeoutError(err) from err
        except requests.exceptions.ConnectionError as err:
            raise MeiliSearchCommunicationError(err) from err

    def get(self, path):
        return self.send_request(requests.get, path)

    def post(self, path, body=None):
        return self.send_request(requests.post, path, body)

    def put(self, path, body=None):
        return self.send_request(requests.put, path, body)

    def delete(self, path, body=None):
        return self.send_request(requests.delete, path, body)

    @staticmethod
    def __to_json(request):
        if request.content == b'':
            return request
        return request.json()

    @staticmethod
    def __validate(request):
        try:
            request.raise_for_status()
            return HttpRequests.__to_json(request)
        except requests.exceptions.HTTPError as err:
            raise MeiliSearchApiError(err, request) from err
