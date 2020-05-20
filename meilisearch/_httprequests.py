import requests

class HttpRequests:

    config = None
    headers = {}

    def __init__(self, config):
        self.config = config
        self.headers = {
            'X-Meili-Api-Key': self.config.apikey,
            'Content-Type': 'application/json'
        }


    def get(self, path):
        request = requests.get(
            self.config.url + '/' + path,
            headers=self.headers,
        )
        return self.__validate(request)

    def post(self, path, body=None):
        if body is None:
            body = {}
        request = requests.post(
            self.config.url + '/' + path,
            headers=self.headers,
            json=body
        )
        return self.__validate(request)

    def put(self, path, body=None):
        if body is None:
            body = {}
        request = requests.put(
            self.config.url + '/' + path,
            headers=self.headers,
            json=body
        )
        return self.__validate(request)

    def delete(self, path, body=None):
        if body is None:
            body = {}
        request = requests.delete(
            self.config.url + '/' + path,
            headers=self.headers,
            json=body
        )
        return self.__validate(request)

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
            raise Exception(err)
        except requests.exceptions.ConnectionError as err:
            raise Exception(err)
