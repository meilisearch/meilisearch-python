import requests


class HttpRequests:
    @staticmethod
    def get(config, path):
        try:
            r = requests.get(
                config.url + '/' + path,
                headers={
                    'x-meili-api-key': config.apikey,
                    'content-type': 'application/json'
                }
            )
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        except requests.exceptions.ConnectionError as err:
            raise Exception(err)

    @staticmethod
    def post(config, path, body=None):
        try:
            if body is None:
                body = {}
            r = requests.post(
                config.url + '/' + path,
                headers={
                    'x-meili-api-key': config.apikey,
                    'content-type': 'application/json'
                },
                json=body
            )
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        except requests.exceptions.ConnectionError as err:
            raise Exception(err)

    @staticmethod
    def put(config, path, body=None):
        try:
            if body is None:
                body = {}
            r = requests.put(
                config.url + '/' + path,
                headers={
                    'x-meili-api-key': config.apikey,
                    'content-type': 'application/json'
                },
                json=body
            )
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        except requests.exceptions.ConnectionError as err:
            raise Exception(err)

    @staticmethod
    def patch(config, path, body=None):
        try:
            if body is None:
                body = {}
            r = requests.patch(
                config.url + '/' + path,
                headers={
                    'x-meili-api-key': config.apikey,
                    'content-type': 'application/json'
                },
                json=body
            )
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        except requests.exceptions.ConnectionError as err:
            raise Exception(err)

    @staticmethod
    def delete(config, path, body=None):
        try:
            if body is None:
                body = {}
            r = requests.delete(
                config.url + '/' + path,
                headers={
                    'x-meili-api-key': config.apikey,
                    'content-type': 'application/json'
                },
                json=body
            )
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as err:
            raise Exception(err)
        except requests.exceptions.ConnectionError as err:
            raise Exception(err)
