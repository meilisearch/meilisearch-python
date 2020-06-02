import json

class MeiliSearchError(Exception):
    """Generic class for MeiliSearch error handling"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'MeiliSearchError, {self.message}'

class MeiliSearchApiError(MeiliSearchError):
    """Error sent by MeiliSearch API"""

    def __init__(self, error, request):
        self.status_code = request.status_code
        if request.text:
            self.message = f'{json.loads(request.text)["message"]}'
        else:
            self.message = error
        super().__init__(self.message)

    def __str__(self):
        return f'MeiliSearchApiError, HTTP status: {self.status_code} -> {self.message}'

class MeiliSearchCommunicationError(MeiliSearchError):
    """Error connecting to MeiliSearch"""

    def __str__(self):
        return f'MeiliSearchCommunicationError, {self.message}'
