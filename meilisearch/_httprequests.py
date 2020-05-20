import requests

class HttpRequests:

    config = None

    def __init__(self, config):
        self.config = config


    def get(self, path):
        request = requests.get(
            self.config.url + '/' + path,
            headers={
                'X-Meili-Api-Key': self.config.apikey,
                'Content-Type': 'application/json'
            }
        )
        return self.__validate(request)

    def post(self, path, body=None):
        if body is None:
            body = {}
        request = requests.post(
            self.config.url + '/' + path,
            headers={
                'x-meili-api-key': self.config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return self.__validate(request)

    def put(self, path, body=None):
        if body is None:
            body = {}
        request = requests.put(
            self.config.url + '/' + path,
            headers={
                'x-meili-api-key': self.config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return self.__validate(request)

    def patch(self, path, body=None):
        if body is None:
            body = {}
        request = requests.patch(
            self.config.url + '/' + path,
            headers={
                'x-meili-api-key': self.config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return self.__validate(request)

    def delete(self, path, body=None):
        if body is None:
            body = {}
        request = requests.delete(
            self.config.url + '/' + path,
            headers={
                'x-meili-api-key': self.config.apikey,
                'content-type': 'application/json'
            },
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
