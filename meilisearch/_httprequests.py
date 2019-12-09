import requests

class HttpRequests:
    @staticmethod
    def get(config, path): 
      try:
        r = requests.get(config.url + path)
        print(r.url)
        r.raise_for_status()
        return r
      except requests.exceptions.HTTPError as err:
        raise Exception(err)
      except requests.exceptions.ConnectionError as err:
        raise Exception(err)
          
    @staticmethod
    def post(config, path, body={}): 
      try:
        r = requests.post(config.url + path, json=body)
        r.raise_for_status()
        return r
      except requests.exceptions.HTTPError as err:
        raise Exception(err)
      except requests.exceptions.ConnectionError as err:
        raise Exception(err)

    @staticmethod
    def put(config, path, body={}): 
      try:
        r = requests.put(config.url + path, json=body)
        r.raise_for_status()
        return r
      except requests.exceptions.HTTPError as err:
        raise Exception(err)
      except requests.exceptions.ConnectionError as err:
        raise Exception(err)
    
    @staticmethod
    def patch(config, path, body={}): 
      try:
        r = requests.patch(config.url + path, json=body)
        r.raise_for_status()
        return r
      except requests.exceptions.HTTPError as err:
        raise Exception(err)
      except requests.exceptions.ConnectionError as err:
        raise Exception(err)

    @staticmethod
    def delete(config, path, body={}): 
      try:
        r = requests.delete(config.url + path, json=body)
        r.raise_for_status()
        return r
      except requests.exceptions.HTTPError as err:
        raise Exception(err)
      except requests.exceptions.ConnectionError as err:
        raise Exception(err)