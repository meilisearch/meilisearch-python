import requests

class HttpRequests:

    @staticmethod
    def get(config, path):
        request = requests.get(
            config.url + '/' + path,
            headers={
                'X-Meili-Api-Key': config.apikey,
                'Content-Type': 'application/json'
            }
        )
        return HttpRequests.__validate(request)

    @staticmethod
    def post(config, path, body=None):
        if body is None:
            body = {}
        request = requests.post(
            config.url + '/' + path,
            headers={
                'x-meili-api-key': config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return HttpRequests.__validate(request)

    @staticmethod
    def put(config, path, body=None):
        if body is None:
            body = {}
        request = requests.put(
            config.url + '/' + path,
            headers={
                'x-meili-api-key': config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return HttpRequests.__validate(request)

    @staticmethod
    def patch(config, path, body=None):
        if body is None:
            body = {}
        request = requests.patch(
            config.url + '/' + path,
            headers={
                'x-meili-api-key': config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return HttpRequests.__validate(request)

    @staticmethod
    def delete(config, path, body=None):
        if body is None:
            body = {}
        request = requests.delete(
            config.url + '/' + path,
            headers={
                'x-meili-api-key': config.apikey,
                'content-type': 'application/json'
            },
            json=body
        )
        return HttpRequests.__validate(request)

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
