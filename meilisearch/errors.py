from __future__ import annotations

import json

from requests import Response


class MeilisearchError(Exception):
    """Generic class for Meilisearch error handling"""

    def __init__(self, message: str) -> None:
        self.message = message
        super().__init__(self.message)

    def __str__(self) -> str:
        return f"MeilisearchError. Error message: {self.message}"


class MeilisearchApiError(MeilisearchError):
    """Error sent by Meilisearch API"""

    def __init__(self, error: str, request: Response) -> None:
        self.status_code = request.status_code
        self.code = None
        self.link = None
        self.type = None

        if request.text:
            json_data = json.loads(request.text)
            self.message = json_data.get("message")
            self.code = json_data.get("code")
            self.link = json_data.get("link")
            self.type = json_data.get("type")
        else:
            self.message = error
        super().__init__(self.message)

    def __str__(self) -> str:
        if self.code and self.link:
            return f"MeilisearchApiError. Error code: {self.code}. Error message: {self.message} Error documentation: {self.link} Error type: {self.type}"

        return f"MeilisearchApiError. {self.message}"


class MeilisearchCommunicationError(MeilisearchError):
    """Error when connecting to Meilisearch"""

    def __str__(self) -> str:
        return f"MeilisearchCommunicationError, {self.message}"


class MeilisearchTimeoutError(MeilisearchError):
    """Error when Meilisearch operation takes longer than expected"""

    def __str__(self) -> str:
        return f"MeilisearchTimeoutError, {self.message}"
